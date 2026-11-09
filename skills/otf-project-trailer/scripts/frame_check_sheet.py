#!/usr/bin/env python3
"""frame_check_sheet.py - one labelled frame from the middle of every shot of an ENCODED trailer, on one sheet.

Usage:
  python3 frame_check_sheet.py RENDER.mp4 --out SHEET.jpg [--cuts edit/cuts.json | --times "0,1.5,3.0" | --every 1.0]
                               [--cols 4] [--width 480]

  --cuts   the trailer cut list: {"shots": [{"id": "S01", "beat": "cold open", "record_in": 0.0, "record_out": 1.5}, ...]}
           (the same file render-cut-verification accepts with --cuts-file). The frame is taken at each shot's middle.
  --times  shot start times on the render timeline; the frame is taken halfway to the next start.
  --every  no cut list: one frame every N seconds.

The sheet keeps each frame's aspect (9:16 is not stretched) and labels it with shot id, beat and timecode at the
render's frame rate, so a wrong shot, a title in the wrong language, a fallback font or a flat grade is visible at a
glance. Reads the render only; writes SHEET.jpg (frames go through a system temp folder that is removed). Needs ffmpeg/ffprobe and Pillow.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw


def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=r_frame_rate:format=duration", "-of", "json", path], capture_output=True, text=True)
    d = json.loads(r.stdout or "{}")
    num, den = d["streams"][0]["r_frame_rate"].split("/")
    return float(d["format"]["duration"]), float(num) / float(den)


def tc(t, fps):
    f = int(round(t * fps))
    fr = int(round(fps))
    return f"{f // (fr * 60):02d}:{(f // fr) % 60:02d}:{f % fr:02d}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("render")
    ap.add_argument("--out", required=True)
    ap.add_argument("--cuts")
    ap.add_argument("--times")
    ap.add_argument("--every", type=float)
    ap.add_argument("--cols", type=int, default=4)
    ap.add_argument("--width", type=int, default=480)
    a = ap.parse_args()
    if os.path.abspath(a.out) == os.path.abspath(a.render):
        sys.exit("refusing to write over the render")
    dur, fps = probe(a.render)

    shots = []
    if a.cuts:
        d = json.load(open(a.cuts, encoding="utf-8"))
        for i, s in enumerate(d.get("shots", d) if isinstance(d, dict) else d):
            t0 = float(s.get("record_in", 0))
            t1 = float(s.get("record_out", t0 + 1))
            shots.append((s.get("id", f"S{i + 1:02d}"), s.get("beat", ""), t0, (t0 + t1) / 2))
    elif a.times:
        starts = sorted(float(x) for x in a.times.split(",") if x.strip()) + [dur]
        shots = [(f"S{i + 1:02d}", "", s, (s + e) / 2) for i, (s, e) in enumerate(zip(starts, starts[1:]))]
    else:
        step = a.every or 1.0
        n = max(1, int(dur / step))
        shots = [(f"T{i + 1:02d}", "", i * step, min(i * step + step / 2, dur - 1 / fps)) for i in range(n)]

    tmp = tempfile.mkdtemp(prefix="trailer_sheet_")
    cells = []
    try:
        for i, (sid, beat, start, mid) in enumerate(shots):
            dst = os.path.join(tmp, f"f{i:03d}.png")
            subprocess.run(["ffmpeg", "-v", "error", "-n", "-ss", f"{mid:.3f}", "-i", a.render, "-frames:v", "1", dst],
                           capture_output=True)
            if not os.path.exists(dst):
                continue
            im = Image.open(dst).convert("RGB")
            w = a.width
            h = int(w * 9 / 16) + 24
            cell = Image.new("RGB", (w, h), (10, 10, 10))
            im.thumbnail((w, h - 24))
            cell.paste(im, ((w - im.size[0]) // 2, (h - 24 - im.size[1]) // 2))
            dr = ImageDraw.Draw(cell)
            dr.rectangle((0, h - 24, w, h), fill=(0, 0, 0))
            dr.text((5, h - 19), f"{sid} {tc(start, fps)}  {beat}"[:72], fill=(255, 220, 0))
            cells.append(cell)
        if not cells:
            sys.exit("no frames extracted")
        cols = min(a.cols, len(cells))
        rows = (len(cells) + cols - 1) // cols
        cw, ch = cells[0].size
        sheet = Image.new("RGB", (cw * cols, ch * rows))
        for i, c in enumerate(cells):
            sheet.paste(c, ((i % cols) * cw, (i // cols) * ch))
        sheet.save(a.out, quality=88)
        print(f"{len(cells)} shots, {dur:.2f} s at {fps:g} fps -> {a.out}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
