#!/usr/bin/env python3
"""cut_timecodes.py — frame-accurate timecode blocks of a source video (for video-to-video edit prompts).

AUTO:    cut_timecodes.py auto VIDEO [--threshold 0.30] [--soft 0.12] [--min 0.4] [--fps N] [--beat-min 4] [--beat-step 0.5] [--out DIR]
           detects every cut: HARD (scene score > --threshold) and SOFT (a lone score peak > --soft, 5x its neighbours —
           cuts between dark or similar shots) plus black frames, snaps everything to the frame grid,
           merges cuts closer than --min seconds (black frames are never merged away), writes DIR/segments.json + DIR/segments.md,
           DIR/segments_sheet.jpg (first / middle / last frame of every block) and, for every block longer than --beat-min seconds,
           DIR/beats_bNN.jpg (a frame every --beat-step seconds) to time the ACTIONS inside a long take.
MANUAL:  cut_timecodes.py manual VIDEO "3.21, 7.10, 12.00" [--fps N] [--frames] [--out DIR]
           the user's cut times; with --frames they are seconds.FRAMES from an editing timeline ("3.21" = 3 s + 21 frames).
CHECK:   cut_timecodes.py check DIR/segments.json   — blocks are continuous, no gaps/overlaps, end == video end.
Duration comes from the VIDEO stream (frame count / fps), never the container (audio/data streams make it longer).
Times are printed as seconds with two decimals, as SS.FF and as frame numbers."""
import json, os, re, subprocess, sys
from fractions import Fraction
from PIL import Image, ImageDraw


def probe(video):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames", "-show_entries",
                          "stream=r_frame_rate,nb_read_frames", "-of", "default=nw=1", video], capture_output=True, text=True).stdout
    kv = dict(l.split("=", 1) for l in out.split() if "=" in l)
    return float(Fraction(kv["r_frame_rate"])), int(kv["nb_read_frames"])


def scores(video):
    """ffmpeg scene score of every frame (frame i vs frame i-1)."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", video, "-vf", "scale=320:-2,select='gte(scene,0)',metadata=print:key=lavfi.scene_score",
                        "-an", "-f", "null", "-"], capture_output=True, text=True)
    return [float(x) for x in re.findall(r"scene_score=([0-9.]+)", r.stderr)]


def detect(sc, threshold, soft, ratio=5.0, win=12):
    """Frame numbers of cuts: HARD = score above threshold; SOFT = a lone peak above `soft` that is `ratio`x the local median
    (cuts between two dark or similar shots score low but still stand out from their neighbours)."""
    hard, quiet = [], []
    for i, v in enumerate(sc):
        if i == 0: continue
        if v > threshold: hard.append(i); continue
        nb = sorted(sc[max(1, i - win):i] + sc[i + 1:i + 1 + win]) or [0.0]
        if v > soft and v >= ratio * max(nb[len(nb) // 2], 0.004) and v == max(sc[max(1, i - 2):i + 3]): quiet.append(i)
    return hard, quiet


def black(video, fps, ymax=20.0):
    """[(start, end)] in seconds of black frames (mean luma <= ymax on 0-255), any length — a single black frame counts."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", video, "-vf", "scale=160:-2,signalstats,metadata=print:key=lavfi.signalstats.YAVG",
                        "-an", "-f", "null", "-"], capture_output=True, text=True)
    ys = [float(y) for y in re.findall(r"YAVG=([0-9.]+)", r.stderr)]
    runs, a = [], None
    for i, y in enumerate(ys + [255.0]):
        if y <= ymax and a is None: a = i
        if y > ymax and a is not None: runs.append((round(a / fps, 3), round(i / fps, 3))); a = None
    return runs


def ssff(t, fps):
    f = int(round(t * fps)); s, fr = divmod(f, int(round(fps)))
    return f"{s:02d}.{fr:02d}"


def snap(t, fps):
    return int(round(t * fps))


def blocks(cut_frames, nframes, fps, min_len, keep=()):
    """cut_frames / keep are frame numbers; keep = cuts that survive the --min merge (black frame edges)."""
    min_f = min_len * fps; pts = [0]
    for c in sorted(set(cut_frames) | set(keep)):
        if c <= 0 or c >= nframes: continue
        if c in keep or (c - pts[-1] >= min_f and nframes - c >= min_f):
            pts.append(c)
    pts.append(nframes)
    return [{"n": i + 1, "start_f": a, "end_f": b, "start": round(a / fps, 3), "end": round(b / fps, 3)}
            for i, (a, b) in enumerate(zip(pts, pts[1:]))]


def frame_at(video, t, path, w=320):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", video, "-frames:v", "1",
                    "-vf", f"scale={w}:-2", "-pix_fmt", "yuvj420p", path])
    return Image.open(path).convert("RGB") if os.path.exists(path) else Image.new("RGB", (w, w * 9 // 16))


def sheet(video, segs, out_dir, fps):
    tmp = os.path.join(out_dir, "_frames"); os.makedirs(tmp, exist_ok=True)
    rows = []
    for s in segs:
        ts = [s["start"] + 0.5 / fps, (s["start"] + s["end"]) / 2, max(s["start"], s["end"] - 1.5 / fps)]
        rows.append((s, [frame_at(video, t, os.path.join(tmp, f"b{s['n']:02d}_{k}.jpg")) for k, t in enumerate(ts)]))
    w, h = 320, rows[0][1][0].size[1]
    img = Image.new("RGB", (w * 3 + 170, (h + 6) * len(rows)), (20, 20, 20)); d = ImageDraw.Draw(img)
    for i, (s, ims) in enumerate(rows):
        y = i * (h + 6)
        d.text((6, y + 6), f"#{s['n']} {s.get('kind', '')}\n{s['start']:.2f}-{s['end']:.2f}s\n{ssff(s['start'], fps)}-{ssff(s['end'], fps)}\n"
                           f"f{s['start_f']}-{s['end_f']}", fill=(255, 255, 0))
        for k, im in enumerate(ims):
            img.paste(im.resize((w, h)), (170 + k * w, y))
    p = os.path.join(out_dir, "segments_sheet.jpg"); img.save(p, quality=85); return p


def beats(video, segs, out_dir, fps, beat_min, step):
    """A frame every `step` s for each long block: actions inside one take get their own times from these."""
    tmp = os.path.join(out_dir, "_frames"); os.makedirs(tmp, exist_ok=True); paths = []
    for s in segs:
        if s["end"] - s["start"] < beat_min: continue
        ts, t = [], s["start"]
        while t < s["end"] - 0.5 / fps:
            ts.append(t); t = round(t + step, 3)
        ims = [frame_at(video, t + 0.5 / fps, os.path.join(tmp, f"beat{s['n']:02d}_{k:03d}.jpg"), 400) for k, t in enumerate(ts)]
        cols = 6; w, h = 400, ims[0].size[1]
        img = Image.new("RGB", (w * cols, h * ((len(ims) + cols - 1) // cols)), (20, 20, 20)); d = ImageDraw.Draw(img)
        for k, (t, im) in enumerate(zip(ts, ims)):
            x, y = (k % cols) * w, (k // cols) * h; img.paste(im.resize((w, h)), (x, y))
            d.rectangle((x, y, x + 120, y + 16), fill=(0, 0, 0)); d.text((x + 4, y + 2), f"{t:.2f}s  f{snap(t, fps)}", fill=(255, 255, 0))
        p = os.path.join(out_dir, f"beats_b{s['n']:02d}.jpg"); img.save(p, quality=85); paths.append(p)
    return paths


def write(video, segs, out_dir, fps, nframes, mode, extra=None, beat_min=4.0, step=0.5):
    os.makedirs(out_dir, exist_ok=True)
    data = {"video": os.path.basename(video), "duration": round(nframes / fps, 3), "frames": nframes, "fps": fps,
            "mode": mode, "segments": segs, **(extra or {})}
    json.dump(data, open(os.path.join(out_dir, "segments.json"), "w"), indent=1)
    md = [f"Source: {data['video']} · {data['duration']:.2f} s · {nframes} frames @ {fps:g} fps · {len(segs)} blocks · mode: {mode}", "",
          f"| # | seconds | SS.FF @{fps:g} | frames | length | kind |", "|---|---|---|---|---|---|"]
    md += [f"| {s['n']} | {s['start']:.2f}–{s['end']:.2f} | {ssff(s['start'], fps)}–{ssff(s['end'], fps)} | {s['start_f']}–{s['end_f']} | "
           f"{s['end'] - s['start']:.2f} s | {s.get('kind', 'shot')} |" for s in segs]
    bp = beats(video, segs, out_dir, fps, beat_min, step)
    if bp:
        md += ["", f"Long takes (≥{beat_min:g} s) — time the actions inside them from: " + ", ".join(os.path.basename(p) for p in bp)]
    open(os.path.join(out_dir, "segments.md"), "w").write("\n".join(md) + "\n")
    print("\n".join(md)); print("sheet:", sheet(video, segs, out_dir, fps))


def check(path):
    d = json.load(open(path)); s = d["segments"]; ok = True
    if s[0]["start_f"] != 0: print("first block does not start at frame 0"); ok = False
    for a, b in zip(s, s[1:]):
        if a["end_f"] != b["start_f"]: print(f"gap/overlap between #{a['n']} and #{b['n']}"); ok = False
    if s[-1]["end_f"] != d["frames"]: print("last block does not end at the last video frame"); ok = False
    for x in s:
        if x["end"] - x["start"] < 0.3 and x.get("kind") != "black":
            print(f"#{x['n']} is shorter than 0.3 s and not black — probably a false cut (a flash or a fast pan)"); ok = False
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
    pfps, nframes = probe(src)
    fps = arg("--fps", pfps); out = arg("--out", os.path.splitext(src)[0] + "_timecodes", str)
    bm = arg("--beat-min", 4.0); st = arg("--beat-step", 0.5)
    if mode == "auto":
        th = arg("--threshold", 0.30); mn = arg("--min", 0.4); so = arg("--soft", 0.12)
        bl = black(src, fps); keep = {snap(t, fps) for a, b in bl for t in (a, b)}
        hard, quiet = detect(scores(src), th, so)
        segs = blocks(hard + quiet, nframes, fps, mn, keep)
        for s in segs:
            if any(snap(a, fps) <= s["start_f"] and s["end_f"] <= snap(b, fps) for a, b in bl): s["kind"] = "black"
            elif s["start_f"] in quiet: s["kind"] = "shot (soft cut)"
        write(src, segs, out, fps, nframes, "auto", {"threshold": th, "soft": so, "min": mn, "soft_cuts": quiet, "black": bl}, bm, st)
    elif mode == "manual":
        vals = [v.strip() for v in sys.argv[3].replace(";", ",").split(",") if v.strip()]
        def to_f(v):
            if "--frames" in sys.argv and "." in v:
                s, f = v.split("."); return int(s) * int(round(fps)) + int(f)
            return snap(float(v), fps)
        segs = blocks([to_f(v) for v in vals], nframes, fps, 0.0, {to_f(v) for v in vals})
        write(src, segs, out, fps, nframes, "manual", None, bm, st)
    else:
        sys.exit(__doc__)
