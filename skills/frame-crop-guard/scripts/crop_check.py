#!/usr/bin/env python3
"""Check every cropped image and video in a layout: does the crop keep the faces and the people it was chosen for?

Usage:
  python3 crop_check.py boxes.json --out qc/crops [--push 1.08] [--min-area 0.35]

boxes.json comes from crop_boxes.mjs (the real boxes, object-fit and object-position of every <img>/<video>).
For each item it computes the part of the source that is visible (cover, contain, fill, object-position, the clipping
parent) and shrinks it by --push (the largest push-in/zoom applied to media; 1.0 if nothing zooms), then finds faces and
people in the source with Apple Vision (scripts/subjects.swift, compiled on first use; macOS only) and flags:

  LOST_SUBJECT  the source has faces but none of them is visible at 90% or more       (high)
  FACE_OUT      a face is outside the window (15% or less of it visible)               (high when it is the largest face)
  FACE_CUT      a face is cut by the window edge (15 to 90% visible)                   (high)
  FACE_AT_EDGE  a whole face sits within 3% of the window edge                         (medium)
  BODY_CUT      a person whose face is visible keeps under 60% of the body (sheets, full-length shots)  (medium)
  HEAVY_CROP    under --min-area of the source is visible (boards, text, wide plates)  (medium)
  DISTORTED     object-fit: fill with an aspect change over 2%                         (high)
Blurred fills (a CSS blur filter) are skipped: they decorate the space around the real image.

For every flagged item it suggests the object-position that centres the faces (or people) in the window, or says the
subject does not fit the box and needs contain, a wider box, or another source frame.
Writes report.md, report.json and sheet.jpg (source with the window in yellow, faces green when kept, red when cut).
Needs Pillow, ffmpeg (for video frames) and swiftc (Xcode command line tools).
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(os.path.expanduser("~"), ".cache", "frame-crop-guard")


def detector():
    exe = os.path.join(CACHE, "subjects")
    src = os.path.join(HERE, "subjects.swift")
    if not os.path.exists(exe) or os.path.getmtime(exe) < os.path.getmtime(src):
        os.makedirs(CACHE, exist_ok=True)
        r = subprocess.run(["swiftc", "-O", src, "-o", exe], capture_output=True, text=True)
        if r.returncode:
            sys.exit("could not compile subjects.swift (needs macOS + Xcode command line tools):\n" + r.stderr[-800:])
    return exe


def parse_boxes(s):
    return [tuple(float(v) for v in b.split(",")) for b in s.split(";") if b.strip()]


def detect(paths):
    out = {}
    if not paths:
        return out
    r = subprocess.run([detector(), *paths], capture_output=True, text=True)
    for line in r.stdout.splitlines():
        p, size, faces, humans = (line.split("\t") + ["", "", ""])[:4]
        out[p] = {"faces": parse_boxes(faces), "humans": parse_boxes(humans)}
    return out


def video_frame(path, t, tmp):
    dst = os.path.join(tmp, f"v{abs(hash((path, t)))}.jpg")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", path, "-frames:v", "1", dst], check=False)
    return dst if os.path.exists(dst) else None


def pos_frac(token):
    t = token.strip()
    if t in ("left", "top"):
        return 0.0
    if t in ("right", "bottom"):
        return 1.0
    if t == "center":
        return 0.5
    m = re.match(r"(-?[\d.]+)%", t)
    return float(m.group(1)) / 100 if m else 0.5


def window(it, nat, push):
    """Visible part of the source as normalised x0,y0,x1,y1, plus the drawn geometry."""
    bx, by, bw, bh = it["box"]
    nw, nh = nat
    toks = (it.get("pos") or "50% 50%").split()
    px, py = pos_frac(toks[0]), pos_frac(toks[1] if len(toks) > 1 else "50%")
    fit = it.get("fit") or "fill"
    if fit == "cover":
        s = max(bw / nw, bh / nh)
    elif fit in ("contain", "scale-down"):
        s = min(bw / nw, bh / nh)
    else:
        s = None
    if s is None:
        x0, y0, dw, dh = bx, by, bw, bh
    else:
        dw, dh = nw * s, nh * s
        x0, y0 = bx + (bw - dw) * px, by + (bh - dh) * py
    cx0, cy0, cx1, cy1 = bx, by, bx + bw, by + bh
    if it.get("clip"):
        c = it["clip"]
        cx0, cy0, cx1, cy1 = max(cx0, c[0]), max(cy0, c[1]), min(cx1, c[2]), min(cy1, c[3])
    if push > 1:  # a push-in shows less around the centre of the box
        mx, my = (cx0 + cx1) / 2, (cy0 + cy1) / 2
        hw, hh = (cx1 - cx0) / 2 / push, (cy1 - cy0) / 2 / push
        cx0, cx1, cy0, cy1 = mx - hw, mx + hw, my - hh, my + hh
    win = [max(0, (cx0 - x0) / dw), max(0, (cy0 - y0) / dh), min(1, (cx1 - x0) / dw), min(1, (cy1 - y0) / dh)]
    return win, (bw, bh, dw, dh, px, py, fit)


def inter(a, b):
    w = max(0, min(a[2], b[2]) - max(a[0], b[0]))
    h = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    return w * h


def area(a):
    return max(0, a[2] - a[0]) * max(0, a[3] - a[1])


def suggest(target, geo, win):
    """object-position that centres the target box inside the box, or None when it cannot fit."""
    bw, bh, dw, dh, px, py, fit = geo
    if fit != "cover":
        return None, "uses " + fit
    ww, wh = win[2] - win[0], win[3] - win[1]
    if target[2] - target[0] > ww * 0.98 or target[3] - target[1] > wh * 0.98:
        return None, "subject is larger than the visible window: use contain, a wider box, or another source frame"
    cx, cy = (target[0] + target[2]) / 2, (target[1] + target[3]) / 2
    nx = px if dw - bw < 1 else min(1, max(0, (bw / 2 - cx * dw) / (bw - dw)))
    ny = py if dh - bh < 1 else min(1, max(0, (bh / 2 - cy * dh) / (bh - dh)))
    return f"{nx * 100:.0f}% {ny * 100:.0f}%", None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("boxes")
    ap.add_argument("--out", required=True)
    ap.add_argument("--push", type=float, default=1.08)
    ap.add_argument("--min-area", type=float, default=0.35)
    a = ap.parse_args()
    data = json.load(open(a.boxes, encoding="utf-8"))
    os.makedirs(a.out, exist_ok=True)
    tmp = tempfile.mkdtemp()
    src_for = {}
    for it in data["items"]:
        p = it.get("path")
        if not p or not os.path.exists(p):
            continue
        src_for[id(it)] = video_frame(p, it.get("mediaStart", 0) + 0.5, tmp) if it["tag"] == "video" else p
    det = detect(sorted(set(v for v in src_for.values() if v)))
    rows, tiles = [], []
    for it in data["items"]:
        if "blur(" in (it.get("filter") or ""):  # a blurred fill behind the real image is decoration, not a crop
            continue
        src = src_for.get(id(it))
        if not src:
            rows.append({**it, "flags": [["high", "MISSING", "media file not found"]]})
            continue
        nat = it["natural"] if it["natural"][0] else Image.open(src).size
        win, geo = window(it, nat, a.push)
        if win[2] <= win[0] or win[3] <= win[1]:  # clipped away in the resting layout (off-stage, behind a mask)
            rows.append({"file": it["file"], "src": it["src"], "flags": [], "note": "not visible in the resting layout"})
            continue
        d = det.get(src, {"faces": [], "humans": []})
        flags = []
        if geo[6] == "fill" and abs((nat[0] / nat[1]) / (geo[0] / geo[1]) - 1) > 0.02:
            flags.append(["high", "DISTORTED", "object-fit: fill stretches the image"])
        faces = sorted(d["faces"], key=area, reverse=True)
        kept = []
        for k, f in enumerate(faces):
            fr = inter(f, win) / (area(f) or 1)
            if fr >= 0.9:
                kept.append(f)
                ex = min(f[0] - win[0], win[2] - f[2], f[1] - win[1], win[3] - f[3])
                if ex < 0.03 * min(win[2] - win[0], win[3] - win[1]):
                    flags.append(["medium", "FACE_AT_EDGE", f"face {k + 1} touches the edge"])
            elif fr > 0.15:
                flags.append(["high", "FACE_CUT", f"face {k + 1} is cut by the edge ({fr:.0%} visible)"])
            elif k == 0 or area(f) > 0.25 * area(faces[0]):
                flags.append(["high" if k == 0 else "medium", "FACE_OUT", f"face {k + 1} is outside the crop"])
        if faces and not kept:
            flags.insert(0, ["high", "LOST_SUBJECT", f"{len(faces)} face(s) in the source, none kept"])
        for k, h in enumerate(d["humans"]):
            if any(inter(f, h) > 0.5 * area(f) for f in kept) and inter(h, win) / (area(h) or 1) < 0.6:
                flags.append(["medium", "BODY_CUT", f"person {k + 1} keeps {inter(h, win) / area(h):.0%} of the body"])
        if area(win) < a.min_area and not faces:
            flags.append(["medium", "HEAVY_CROP", f"only {area(win):.0%} of the source is visible"])
        fix = None
        if any(f[0] == "high" or f[1] in ("FACE_AT_EDGE", "BODY_CUT") for f in flags):
            tgt = faces[:3] or d["humans"][:2]
            if tgt:
                u = [min(b[0] for b in tgt), min(b[1] for b in tgt), max(b[2] for b in tgt), max(b[3] for b in tgt)]
                if any(f[1] == "BODY_CUT" for f in flags) and d["humans"]:
                    hs = d["humans"]
                    u = [min(b[0] for b in hs), min(b[1] for b in hs), max(b[2] for b in hs), max(b[3] for b in hs)]
                pos, why = suggest(u, geo, win)
                fix = f"object-position: {pos}" if pos else why
        rows.append({"file": it["file"], "src": it["src"], "id": it.get("id"), "box": [round(v) for v in it["box"]],
                     "fit": it["fit"], "pos": it["pos"], "window": [round(v, 3) for v in win],
                     "faces": len(faces), "kept": len(kept), "flags": flags, "fix": fix})
        if flags:
            im = Image.open(src).convert("RGB")
            im.thumbnail((420, 420))
            W, H = im.size
            dr = ImageDraw.Draw(im)
            dr.rectangle([win[0] * W, win[1] * H, win[2] * W, win[3] * H], outline=(255, 210, 0), width=4)
            for f in faces:
                ok = f in kept
                dr.rectangle([f[0] * W, f[1] * H, f[2] * W, f[3] * H], outline=(60, 220, 90) if ok else (255, 50, 40), width=3)
            label = f"{os.path.basename(it['file'])} {it['src'].split('/')[-1]}: {', '.join(x[1] for x in flags)}"
            tile = Image.new("RGB", (W, H + 28), (20, 16, 14))
            tile.paste(im, (0, 28))
            ImageDraw.Draw(tile).text((6, 7), label[:70], fill=(240, 235, 230))
            tiles.append(tile)
    bad = [r for r in rows if r.get("flags")]
    high = [r for r in bad if any(f[0] == "high" for f in r["flags"])]
    json.dump(rows, open(os.path.join(a.out, "report.json"), "w"), indent=1, default=str)
    md = ["# Crop check", "", f"{len(rows)} media boxes, {len(bad)} flagged, {len(high)} high. Push margin {a.push}.", "",
          "| file | media | flags | fix |", "|---|---|---|---|"]
    for r in bad:
        md.append(f"| {os.path.basename(r.get('file', ''))} | {r.get('src', '')} | "
                  f"{'; '.join(f'{x[1]} ({x[0]}): {x[2]}' for x in r['flags'])} | {r.get('fix') or ''} |")
    md += ["", "Yellow = what the layout shows. Green face = kept, red = cut or outside. Look at sheet.jpg before trusting a pass:",
           "a detector misses faces in profile, in silhouette and at very small sizes."]
    open(os.path.join(a.out, "report.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    if tiles:
        cols = 4
        w = max(t.size[0] for t in tiles)
        h = max(t.size[1] for t in tiles)
        sheet = Image.new("RGB", (cols * w, ((len(tiles) + cols - 1) // cols) * h), (10, 8, 7))
        for i, t in enumerate(tiles):
            sheet.paste(t, ((i % cols) * w, (i // cols) * h))
        sheet.save(os.path.join(a.out, "sheet.jpg"), quality=88)
    print(f"{len(rows)} boxes, {len(bad)} flagged ({len(high)} high) -> {a.out}")
    sys.exit(1 if high else 0)


if __name__ == "__main__":
    main()
