#!/usr/bin/env python3
"""series_manifest.py — prepares a series of clips (e.g. Series_part1.mp4 … Series_partN.mp4) for assembly on a DaVinci Resolve timeline.

  series_manifest.py OUT.json CLIP [CLIP ...] [--sort] [--titles "Part 1 title|Part 2 title|…"] [--master MASTER.mp4]

  · keeps the given order; with --sort the clips are ordered naturally by file name (part2 before part10)
  · probes every clip (duration, fps, size, audio) with ffprobe and FAILS if they do not match each other (mixed fps / size)
  · computes each clip's record start on the timeline (seconds and frames at the series fps) → marker positions
  · --master also writes a concatenated preview master with ffmpeg (stream copy when possible) to check the cut outside Resolve"""
import json, os, re, subprocess, sys


def probe(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height,r_frame_rate:format=duration",
                        "-of", "json", p], capture_output=True, text=True)
    d = json.loads(r.stdout or "{}"); v = next((s for s in d.get("streams", []) if s.get("codec_type") == "video"), {})
    num, den = (v.get("r_frame_rate", "0/1").split("/") + ["1"])[:2]
    return {"path": os.path.abspath(p), "duration": round(float(d.get("format", {}).get("duration", 0)), 3),
            "fps": round(float(num) / float(den or 1), 3) if float(den or 1) else 0, "width": v.get("width"), "height": v.get("height"),
            "audio": any(s.get("codec_type") == "audio" for s in d.get("streams", []))}


def natural(p):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", os.path.basename(p))]


def main():
    a = sys.argv[1:]
    if len(a) < 2:
        sys.exit(__doc__)
    out = a[0]; titles = []; master = None; clips = []; sort = False
    i = 1
    while i < len(a):
        if a[i] == "--titles": titles = a[i + 1].split("|"); i += 2
        elif a[i] == "--master": master = a[i + 1]; i += 2
        elif a[i] == "--sort": sort = True; i += 1
        else: clips.append(a[i]); i += 1
    if sort:
        clips = sorted(clips, key=natural)
    items = [probe(c) for c in clips]
    fps = {x["fps"] for x in items}; size = {(x["width"], x["height"]) for x in items}
    errs = []
    if len(fps) > 1: errs.append(f"mixed frame rates: {sorted(fps)}")
    if len(size) > 1: errs.append(f"mixed sizes: {sorted(size)}")
    if any(x["duration"] <= 0 for x in items): errs.append("a clip has no duration (unreadable?)")
    f = items[0]["fps"] if items else 30; t = 0.0
    for n, x in enumerate(items):
        x["index"] = n + 1; x["title"] = titles[n] if n < len(titles) else os.path.splitext(os.path.basename(x["path"]))[0]
        x["record_start_s"] = round(t, 3); x["record_start_frame"] = int(round(t * f)); x["frames"] = int(round(x["duration"] * f)); t += x["duration"]
    data = {"fps": f, "size": list(size)[0] if size else None, "total_s": round(t, 3), "clips": items, "errors": errs}
    json.dump(data, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for x in items:
        print(f"{x['index']:>2}. {x['record_start_s']:>7.2f}s  {x['duration']:>6.2f}s  {x['width']}x{x['height']}@{x['fps']}  audio={x['audio']}  {x['title']}")
    print(f"total {t:.2f} s at {f} fps" + ("" if not errs else "\nERRORS: " + "; ".join(errs)))
    if master and not errs:
        lst = out + ".concat.txt"
        open(lst, "w").write("".join(f"file '{x['path']}'\n" for x in items))
        r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", "-movflags", "+faststart", master])
        print("master:", master if r.returncode == 0 else "FAILED (re-encode needed: different codecs)")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
