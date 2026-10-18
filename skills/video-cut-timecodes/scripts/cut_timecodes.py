#!/usr/bin/env python3
"""cut_timecodes.py — one timecode block per shot of a source video (for video-to-video edit prompts).

AUTO:    cut_timecodes.py auto VIDEO [--threshold 0.30] [--min 0.4] [--fps 24] [--out DIR]
           detects every cut (ffmpeg scene score), merges cuts closer than --min seconds, writes DIR/segments.json + DIR/segments.md
           and DIR/segments_sheet.jpg (first / middle / last frame of every block) so the blocks can be checked by eye.
MANUAL:  cut_timecodes.py manual VIDEO "0, 3.21, 7.10, 12.00" [--fps 24] [--frames] [--out DIR]
           the user's cut times; with --frames they are seconds.FRAMES from an editing timeline ("3.21" = 3 s + 21 frames at --fps).
CHECK:   cut_timecodes.py check DIR/segments.json   — blocks are continuous, no gaps/overlaps, end == duration.
Times are printed both as seconds (one decimal) and as SS.FF at --fps."""
import json, os, re, subprocess, sys
from PIL import Image, ImageDraw


def duration(video):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", video],
                         capture_output=True, text=True).stdout.strip()
    return float(out)


def detect(video, threshold):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", video, "-vf", f"select='gt(scene,{threshold})',showinfo", "-an", "-f", "null", "-"],
                       capture_output=True, text=True)
    return [float(m) for m in re.findall(r"pts_time:([0-9.]+)", r.stderr)]


def ssff(t, fps):
    s = int(t); f = int(round((t - s) * fps))
    if f == fps: s, f = s + 1, 0
    return f"{s:02d}.{f:02d}"


def blocks(cuts, dur, min_len):
    pts = [0.0]
    for c in sorted(cuts):
        if c - pts[-1] >= min_len and dur - c >= min_len:
            pts.append(round(c, 3))
    pts.append(round(dur, 3))
    return [{"n": i + 1, "start": pts[i], "end": pts[i + 1]} for i in range(len(pts) - 1)]


def frame_at(video, t, path):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", video, "-frames:v", "1", "-vf", "scale=320:-2", path])


def sheet(video, segs, out_dir, fps):
    tmp = os.path.join(out_dir, "_frames"); os.makedirs(tmp, exist_ok=True)
    rows = []
    for s in segs:
        ts = [s["start"] + 0.05, (s["start"] + s["end"]) / 2, max(s["start"], s["end"] - 0.08)]
        ims = []
        for k, t in enumerate(ts):
            p = os.path.join(tmp, f"b{s['n']:02d}_{k}.jpg"); frame_at(video, t, p)
            ims.append(Image.open(p).convert("RGB") if os.path.exists(p) else Image.new("RGB", (320, 180)))
        rows.append((s, ims))
    w, h = 320, rows[0][1][0].size[1] if rows else 180
    img = Image.new("RGB", (w * 3 + 150, (h + 6) * len(rows)), (20, 20, 20)); d = ImageDraw.Draw(img)
    for i, (s, ims) in enumerate(rows):
        y = i * (h + 6)
        d.text((6, y + 6), f"#{s['n']}\n{s['start']:.1f}-{s['end']:.1f}s\n{ssff(s['start'], fps)}-{ssff(s['end'], fps)}", fill=(255, 255, 0))
        for k, im in enumerate(ims):
            img.paste(im.resize((w, h)), (150 + k * w, y))
    p = os.path.join(out_dir, "segments_sheet.jpg"); img.save(p, quality=85); return p


def write(video, segs, out_dir, fps, mode, extra=None):
    os.makedirs(out_dir, exist_ok=True)
    data = {"video": os.path.basename(video), "duration": segs[-1]["end"], "fps": fps, "mode": mode, "segments": segs, **(extra or {})}
    json.dump(data, open(os.path.join(out_dir, "segments.json"), "w"), indent=1)
    md = [f"Source: {data['video']} · {data['duration']:.2f} s · {len(segs)} blocks · mode: {mode}", "",
          "| # | seconds | SS.FF @%d | length |" % fps, "|---|---|---|---|"]
    md += [f"| {s['n']} | {s['start']:.1f}–{s['end']:.1f} | {ssff(s['start'], fps)}–{ssff(s['end'], fps)} | {s['end'] - s['start']:.1f} s |" for s in segs]
    open(os.path.join(out_dir, "segments.md"), "w").write("\n".join(md) + "\n")
    print("\n".join(md)); print("sheet:", sheet(video, segs, out_dir, fps))


def check(path):
    d = json.load(open(path)); s = d["segments"]; ok = True
    if abs(s[0]["start"]) > 1e-6: print("first block does not start at 0"); ok = False
    for a, b in zip(s, s[1:]):
        if abs(a["end"] - b["start"]) > 1e-3: print(f"gap/overlap between #{a['n']} and #{b['n']}"); ok = False
    if abs(s[-1]["end"] - d["duration"]) > 0.05: print("last block does not end at the video end"); ok = False
    if any(x["end"] - x["start"] < 0.3 for x in s): print("a block shorter than 0.3 s — probably a false cut"); ok = False
    print("check: OK" if ok else "check: FIX the blocks above"); return ok


def arg(name, default, cast=float):
    a = sys.argv
    return cast(a[a.index(name) + 1]) if name in a else default


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    mode, src = sys.argv[1], sys.argv[2]
    if mode == "check":
        sys.exit(0 if check(src) else 1)
    fps = arg("--fps", 24, int); out = arg("--out", os.path.splitext(src)[0] + "_timecodes", str); dur = duration(src)
    if mode == "auto":
        th = arg("--threshold", 0.30); mn = arg("--min", 0.4)
        segs = blocks(detect(src, th), dur, mn); write(src, segs, out, fps, "auto", {"threshold": th, "min": mn})
    elif mode == "manual":
        vals = [v.strip() for v in sys.argv[3].replace(";", ",").split(",") if v.strip()]
        def to_s(v):
            if "--frames" in sys.argv and "." in v:
                s, f = v.split("."); return int(s) + int(f) / fps
            return float(v)
        cuts = [to_s(v) for v in vals if to_s(v) > 0]
        segs = blocks(cuts, dur, 0.0); write(src, segs, out, fps, "manual")
    else:
        sys.exit(__doc__)
