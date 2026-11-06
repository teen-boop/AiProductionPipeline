#!/usr/bin/env python3
"""Side-by-side identity sheet: every face in each candidate frame next to the character's reference face, same scale.

Usage: python3 face_compare.py --ref sheet_or_bust.png [--ref second_ref.png] --out compare.jpg frame1.png frame2.jpg clip.mp4 ...
Videos are sampled at 1 s and at the middle. Faces come from frame-crop-guard's Apple Vision detector
(~/.cache/frame-crop-guard/subjects, compiled on its first run); without it, the whole frame is shown.
Each row: REF | face 1 | face 2 ... of one frame, all 300 px squares, labelled with the file name.
The sheet is the input of pass 1 and pass 2 of the identity triple check in SKILL.md; it never decides on its own.
"""
import argparse, os, subprocess, tempfile
from PIL import Image, ImageDraw

DET = os.path.expanduser("~/.cache/frame-crop-guard/subjects")
S = 300


def faces(paths):
    if not os.path.exists(DET):
        return {p: [] for p in paths}
    out = subprocess.run([DET, *paths], capture_output=True, text=True).stdout
    res = {}
    for line in out.splitlines():
        p, _size, f, _h = (line.split("\t") + ["", "", ""])[:4]
        res[p] = [tuple(float(v) for v in b.split(",")) for b in f.split(";") if b.strip()]
    return res


def crops(path, boxes, minw=0.03):
    im = Image.open(path).convert("RGB")
    W, H = im.size
    got = []
    for b in sorted(boxes, key=lambda b: -(b[2] - b[0])):
        if b[2] - b[0] < minw:
            continue
        cx, cy = (b[0] + b[2]) / 2 * W, (b[1] + b[3]) / 2 * H
        s = max((b[2] - b[0]) * W, (b[3] - b[1]) * H) * 1.6
        got.append(im.crop((int(cx - s / 2), int(cy - s / 2), int(cx + s / 2), int(cy + s / 2))).resize((S, S)))
    if not got:
        im.thumbnail((S, S)); got = [im]
    return got


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", action="append", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("frames", nargs="+")
    a = ap.parse_args()
    tmp, items = tempfile.mkdtemp(), []
    for f in a.frames:
        if f.lower().endswith((".mp4", ".mov")):
            dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout or 2)
            for t in (1.0, dur / 2):
                j = os.path.join(tmp, f"{len(items)}.jpg")
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", f, "-frames:v", "1", j])
                items.append((j, f"{os.path.basename(f)} @{t:.1f}s"))
        else:
            items.append((f, os.path.basename(f)))
    fb = faces([p for p, _ in items] + a.ref)
    ref = [c for r in a.ref for c in crops(r, fb.get(r, []))[:1]]
    rows = [(lab, crops(p, fb.get(p, []))) for p, lab in items]
    cols = len(ref) + max(len(c) for _, c in rows)
    sheet = Image.new("RGB", (cols * (S + 6), len(rows) * (S + 30)), "black")
    d = ImageDraw.Draw(sheet)
    for i, (lab, cs) in enumerate(rows):
        y = i * (S + 30)
        for j, c in enumerate(ref + cs):
            sheet.paste(c, (j * (S + 6), y))
            d.text((j * (S + 6) + 4, y + 4), "REF" if j < len(ref) else f"face {j - len(ref) + 1}", fill="yellow")
        d.text((4, y + S + 8), lab[-90:], fill="yellow")
    sheet.save(a.out, quality=88)
    print(a.out, len(rows), "frames")


if __name__ == "__main__":
    main()
