#!/usr/bin/env python3
"""pick_material.py - inventory a film project's stills and generated clips for a trailer, rank them by closeness
to the project look, flag takes that must not be used, and draw a contact sheet for the user to approve the pick.

Usage:
  python3 pick_material.py PROJECT_DIR --out OUT_DIR [--style-lock STYLE_LOCK.json] [--refs DIR ...]
                           [--format 16:9|9:16|1:1] [--top 24] [--min-clip 1.5] [--clip-bonus 15]
                           [--max-clips 400] [--skip DIR_NAME ...]

Reads only. Writes into OUT_DIR (which must not hold source material):
  material.csv        every still and clip, ranked, with status, flags and paths RELATIVE to PROJECT_DIR
  material.json       the same plus the look metrics used and where the ranking came from
  contact_sheet.jpg   the top N usable items, labelled rank / kind / length / flags (aspect kept, no stretching)
  rejected_sheet.jpg  items flagged rejected or unapproved, so the user can rescue one on purpose
  _frames/            small preview frames pulled from clips (the clip files are never touched)
Hidden folders, the skill's own output root (trailer/) and any folder holding an earlier material.json or
TRAILER_PLAN.md are never inventoried.

Ranking: the look metrics and score come from the sibling skill otf-presentations (scripts/otf_context.py,
functions metrics + look_score) when it is installed next to this skill; set OTF_PRESENTATIONS_DIR to point
elsewhere. Without it a reduced fallback (contrast + saturation only) is used and the report says so.
Score = look closeness as a 0-100 percentile within the project, plus --clip-bonus for a clip that really moves
(mean frame difference across the clip) and --approved-bonus for material in an approved/selects/final folder.
Needs Python 3 + Pillow, and ffmpeg/ffprobe on PATH for clips.
"""
import argparse
import csv
import importlib.util
import json
import os
import re
import subprocess
import sys

from PIL import Image, ImageChops, ImageDraw, ImageStat

IMG = (".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff")
VID = (".mp4", ".mov", ".m4v", ".webm", ".mkv")
REJECT_TOKENS = re.compile(r"(^|[_\-. /])(rejected?|discard(ed)?|trash|bin|unused|_orig|orig_bars|bad|fail(ed)?)([_\-. /]|$)", re.I)
APPROVED_TOKENS = re.compile(r"(^|[_\-. /])(approved?|final|finals|selects?|keep|hero|animation|ok)([_\-. /]|$)", re.I)
WIP_TOKENS = re.compile(r"(^|[_\-. /])(wip|draft|test|tmp|temp|preview|proxy)([_\-. /]|$)", re.I)
ASPECTS = {"16:9": 16 / 9, "9:16": 9 / 16, "1:1": 1.0, "4:5": 0.8, "2.39:1": 2.39}


def load_ranker():
    here = os.path.dirname(os.path.abspath(__file__))
    cands = [os.environ.get("OTF_PRESENTATIONS_DIR", ""),
             os.path.join(here, "..", "..", "otf-presentations")]
    for c in cands:
        p = os.path.join(c, "scripts", "otf_context.py") if c else ""
        if p and os.path.isfile(p):
            spec = importlib.util.spec_from_file_location("otf_context", p)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod.metrics, mod.look_score, getattr(mod, "embedded_prompt", None), "otf-presentations"

    def metrics(path):  # reduced fallback, only used when otf-presentations is not installed
        im = Image.open(path).convert("RGB")
        im.thumbnail((256, 256))
        return {"contrast": round(ImageStat.Stat(im.convert("L")).stddev[0], 1),
                "saturation": round(ImageStat.Stat(im.convert("HSV")).mean[1], 1), "warm": 0.0,
                "mean": round(ImageStat.Stat(im.convert("L")).mean[0], 1)}

    def look_score(m, ref):
        if not ref:
            return m["contrast"] * 0.6 + m["saturation"] * 0.3
        return -abs(m["contrast"] - ref["contrast"]) - abs(m["saturation"] - ref["saturation"])

    return metrics, look_score, None, "fallback (otf-presentations not found)"


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def probe(path):
    r = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
             "stream=width,height,r_frame_rate:format=duration", "-of", "json", path])
    try:
        d = json.loads(r.stdout)
        s = d["streams"][0]
        num, den = (s.get("r_frame_rate") or "0/1").split("/")
        fps = round(float(num) / float(den), 3) if float(den) else 0.0
        return {"width": int(s["width"]), "height": int(s["height"]), "fps": fps,
                "duration": round(float(d["format"]["duration"]), 2)}
    except (KeyError, IndexError, ValueError, json.JSONDecodeError):
        return None


def grab(path, t, dst):
    """One small frame at time t into dst (inside OUT_DIR). The source is only ever an -i input; -n never overwrites."""
    if not os.path.exists(dst):
        run(["ffmpeg", "-v", "error", "-n", "-ss", f"{max(t, 0):.3f}", "-i", path, "-frames:v", "1",
             "-vf", "scale=480:-2", dst])
    return dst if os.path.exists(dst) else None


def motion(frames):
    """Mean absolute luma difference between consecutive preview frames (0 = frozen)."""
    ims = [Image.open(f).convert("L").resize((160, 90)) for f in frames if f]
    if len(ims) < 2:
        return 0.0
    diffs = [ImageStat.Stat(ImageChops.difference(a, b)).mean[0] for a, b in zip(ims, ims[1:])]
    return round(sum(diffs) / len(diffs), 2)


def status_of(rel):
    if REJECT_TOKENS.search(rel) or os.path.basename(rel).startswith(("_rejected", "_orig")):
        return "rejected"
    if WIP_TOKENS.search(rel):
        return "unapproved"
    if APPROVED_TOKENS.search(rel):
        return "approved"
    return "unreviewed"


DEFAULT_SKIP = {"trailer", "_frames", "node_modules", "__pycache__"}
OUTPUT_MARKERS = ("material.json", "TRAILER_PLAN.md", "hyperframes.json")


def walk(project, skip):
    """Every still and clip under project, leaving out hidden folders, skipped folders and earlier skill outputs."""
    for root, dirs, files in os.walk(project):
        if root != project and any(m in files for m in OUTPUT_MARKERS):
            dirs[:] = []
            continue
        dirs[:] = sorted(d for d in dirs if not d.startswith(".") and os.path.abspath(os.path.join(root, d)) not in skip
                         and d not in skip)
        for f in sorted(files):
            if f.startswith(("._", ".")):
                continue
            low = f.lower()
            if low.endswith(IMG) or low.endswith(VID):
                yield os.path.join(root, f)


def label_cell(im, w, h, text, colour):
    cell = Image.new("RGB", (w, h), (12, 12, 12))
    im = im.copy()
    im.thumbnail((w, h - 22))
    cell.paste(im, ((w - im.size[0]) // 2, (h - 22 - im.size[1]) // 2))
    d = ImageDraw.Draw(cell)
    d.rectangle((0, h - 22, w, h), fill=(0, 0, 0))
    d.text((5, h - 18), text[:70], fill=colour)
    return cell


def sheet(items, out_path, cols=4, w=480, h=292):
    if not items:
        return False
    rows = (len(items) + cols - 1) // cols
    sh = Image.new("RGB", (w * cols, h * rows), (0, 0, 0))
    for i, it in enumerate(items):
        try:
            im = Image.open(it["_thumb"]).convert("RGB")
        except Exception:
            continue
        kind = f"CLIP {it['duration_s']}s" if it["kind"] == "clip" else "STILL"
        flags = (" !" + ",".join(it["flags"].split(";"))) if it["flags"] else ""
        tag = {"approved": "OK ", "unapproved": "WIP ", "rejected": "REJ "}.get(it["status"], "")
        text = f"{it['rank']}. {tag}{kind} {os.path.basename(it['rel_path'])[:28]}{flags}"
        colour = (255, 90, 90) if it["status"] == "rejected" else (255, 220, 0) if it["flags"] else (235, 235, 235)
        sh.paste(label_cell(im, w, h, text, colour), ((i % cols) * w, (i // cols) * h))
    sh.save(out_path, quality=86)
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project")
    ap.add_argument("--out", required=True)
    ap.add_argument("--style-lock")
    ap.add_argument("--refs", action="append", default=[])
    ap.add_argument("--format", default="16:9", choices=sorted(ASPECTS))
    ap.add_argument("--top", type=int, default=24)
    ap.add_argument("--min-clip", type=float, default=1.5)
    ap.add_argument("--clip-bonus", type=float, default=15.0, help="points added to a clip that really moves (score scale 0-100)")
    ap.add_argument("--approved-bonus", type=float, default=5.0)
    ap.add_argument("--max-clips", type=int, default=400)
    ap.add_argument("--skip", action="append", default=[],
                    help="folder name or path to leave out (repeatable); trailer/, _frames/ and earlier outputs are always left out")
    a = ap.parse_args()

    project = os.path.abspath(a.project)
    out = os.path.abspath(a.out)
    if not os.path.isdir(project):
        sys.exit(f"not a folder: {a.project}")
    os.makedirs(os.path.join(out, "_frames"), exist_ok=True)
    skip = {out} | DEFAULT_SKIP | {os.path.abspath(s) if os.sep in s else s for s in a.skip}
    metrics, look_score, embedded_prompt, ranker = load_ranker()

    lock_path = a.style_lock or (os.path.join(project, "STYLE_LOCK.json") if os.path.isfile(os.path.join(project, "STYLE_LOCK.json")) else None)
    ref = None
    if lock_path:
        try:
            ref = json.load(open(lock_path, encoding="utf-8")).get("ref_metrics")
        except (OSError, json.JSONDecodeError):
            ref = None
    if not ref and a.refs:
        ms = []
        for d in a.refs:
            for p in walk(os.path.abspath(d), set()):
                if p.lower().endswith(IMG):
                    try:
                        ms.append(metrics(p))
                    except Exception:
                        pass
        if ms:
            ref = {k: sum(m[k] for m in ms) / len(ms) for k in ("contrast", "saturation", "warm")}
    target = ASPECTS[a.format]

    items, n_clips = [], 0
    for i, p in enumerate(walk(project, skip)):
        rel = os.path.relpath(p, project)
        low = p.lower()
        flags, it = [], {"kind": "clip" if low.endswith(VID) else "still", "rel_path": rel, "status": status_of(rel),
                         "duration_s": "", "fps": "", "motion": "", "embedded_prompt": ""}
        try:
            if it["kind"] == "still":
                with Image.open(p) as im:
                    w, h = im.size
                it["_thumb"] = p
                if embedded_prompt:
                    it["embedded_prompt"] = embedded_prompt(p)[:240].replace("\n", " ")
            else:
                n_clips += 1
                if n_clips > a.max_clips:
                    continue
                info = probe(p)
                if not info:
                    raise ValueError("unreadable")
                w, h, dur = info["width"], info["height"], info["duration"]
                it.update(duration_s=dur, fps=info["fps"])
                base = os.path.join(out, "_frames", f"c{i:05d}")
                frames = [grab(p, dur * f, f"{base}_{k}.jpg") for k, f in enumerate((0.15, 0.5, 0.85))]
                it["_thumb"] = frames[1] or frames[0]
                if not it["_thumb"]:
                    raise ValueError("no-frame")
                it["motion"] = motion(frames)
                if dur < a.min_clip:
                    flags.append("short")
                if it["motion"] < 1.0:
                    flags.append("near-static")
                if info["fps"] and abs(info["fps"] - 24) > 0.05:
                    flags.append(f"fps{info['fps']:g}")
            m = metrics(it["_thumb"])
        except Exception as e:  # unreadable file: list it, never crash the inventory
            it.update(width="", height="", score=-999, look_score="", flags=f"error:{e if isinstance(e, ValueError) else type(e).__name__}", _thumb=None)
            items.append(it)
            continue
        aspect = w / h if h else 0
        if aspect and abs(aspect - target) / target > 0.08:
            flags.append("aspect")
        long_edge_needed = 1920 if a.format in ("16:9", "9:16", "2.39:1") else 1080
        if max(w, h) < long_edge_needed / 1.4:
            flags.append("lowres")
        it.update(width=w, height=h, look_score=round(look_score(m, ref), 2), flags=";".join(flags),
                  contrast=m.get("contrast"), saturation=m.get("saturation"), warm=m.get("warm"))
        items.append(it)

    # look closeness -> 0..100 percentile within this project, then bonuses that mean the same on every project
    scored = sorted((x for x in items if x.get("look_score") != ""), key=lambda x: x["look_score"])
    for k, x in enumerate(scored):
        pct = 100.0 * k / max(len(scored) - 1, 1)
        moving = x["kind"] == "clip" and isinstance(x["motion"], float) and x["motion"] >= 1.0
        x["look_pct"] = round(pct, 1)
        x["score"] = round(pct + (a.clip_bonus if moving else 0) + (a.approved_bonus if x["status"] == "approved" else 0), 1)

    usable = [x for x in items if x["status"] != "rejected" and not str(x.get("flags", "")).startswith("error")]
    others = [x for x in items if x not in usable]
    usable.sort(key=lambda x: (x["status"] == "unapproved", -x["score"]))
    others.sort(key=lambda x: -x.get("score", -999))
    for r, x in enumerate(usable + others, 1):
        x["rank"] = r

    cols = ["rank", "kind", "status", "score", "look_pct", "look_score", "motion", "duration_s", "fps", "width", "height",
            "contrast", "saturation", "warm", "flags", "rel_path", "embedded_prompt"]
    with open(os.path.join(out, "material.csv"), "w", newline="", encoding="utf-8") as fh:
        wr = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        wr.writeheader()
        for x in usable + others:
            wr.writerow(x)
    sheet([x for x in usable if x.get("_thumb")][: a.top], os.path.join(out, "contact_sheet.jpg"))
    sheet([x for x in items if x["status"] in ("rejected", "unapproved") and x.get("_thumb")][: a.top],
          os.path.join(out, "rejected_sheet.jpg"))
    for x in items:
        x["thumb"] = os.path.relpath(x.pop("_thumb"), out) if x.get("_thumb") and x["_thumb"].startswith(out) else ""
    summary = {"project": os.path.basename(project), "ranker": ranker, "style_lock": os.path.basename(lock_path) if lock_path else None,
               "ref_metrics": ref, "format": a.format, "counts": {
                   "stills": sum(1 for x in items if x["kind"] == "still"), "clips": sum(1 for x in items if x["kind"] == "clip"),
                   "rejected": sum(1 for x in items if x["status"] == "rejected"),
                   "unapproved": sum(1 for x in items if x["status"] == "unapproved"),
                   "approved": sum(1 for x in items if x["status"] == "approved")},
               "skipped_clips_over_max": max(0, n_clips - a.max_clips), "items": usable + others}
    json.dump(summary, open(os.path.join(out, "material.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print(f"ranker: {ranker}; look reference: {'style lock' if lock_path and ref else 'refs' if ref else 'none (generic contrast/saturation)'}")
    print(f"items: {summary['counts']}")
    for x in usable[:12]:
        print(f"  {x['rank']:>3}. {x['kind']:5} {x['status']:10} score {x['score']:>7} {x['flags'] or '-':18} {x['rel_path']}")
    print(f"-> {out}/material.csv, material.json, contact_sheet.jpg, rejected_sheet.jpg")


if __name__ == "__main__":
    main()
