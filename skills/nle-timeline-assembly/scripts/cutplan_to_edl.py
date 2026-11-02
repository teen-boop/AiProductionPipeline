#!/usr/bin/env python3
"""Validate a cut plan (cutplan.json) and export it as CMX3600 EDLs plus a marker list.

Usage:
  python3 cutplan_to_edl.py cutplan.json --out <dir> [--no-probe]

cutplan.json:
{
  "name": "EP01 rough cut",
  "fps": 24,                       # 23.976 / 24 / 25 / 29.97 / 30 ... (EDL timecode uses the nominal integer rate, NDF)
  "start_tc": "01:00:00:00",
  "clips": [                        # video events, in record order per track
    {"id": "S01", "file": "/abs/path/shot01.mp4", "src_in": 0.0, "src_out": 3.5,
     "track": "V1", "record_in": null,              # null = butt against the previous clip on the same track
     "transition_after": {"type": "cut"},           # or {"type": "dissolve", "frames": 8} (written as a note, not an EDL event)
     "motion": {"type": "push_in", "from": 1.0, "to": 1.08},   # note only; apply in the NLE
     "marker": "S01 - hero enters"}
  ],
  "audio": [                        # optional audio events (music, VO, SFX)
    {"id": "MUSIC", "file": "/abs/path/bed.wav", "src_in": 0.0, "src_out": 60.0, "track": "A2", "record_in": 0.0,
     "base_db": -18, "duck": [[3.0, 8.5, -28]]}    # note only; ducking windows in record seconds
  ]
}

Writes into --out:
  <name>_<track>.edl   one EDL per track (Resolve and Premiere both import CMX3600 per track)
  markers.csv          record timecode, frame, track, id, marker text
  notes.csv            per-event notes the EDL cannot carry (transitions, motion, levels, ducking)
  report.txt           totals, gaps, overlaps, missing files, out-of-range source times

Exit code 1 if any blocking problem is found (overlap, missing file, src_out <= src_in, src_out beyond media length).
Standard library only; ffprobe is used for media length when available (skip with --no-probe).
"""
import csv
import json
import os
import shutil
import subprocess
import sys


def die(msg):
    sys.exit(msg)


def nominal(fps):
    return int(round(float(fps)))


def tc_to_frames(tc, fpsn):
    h, m, s, f = [int(x) for x in tc.replace(";", ":").split(":")]
    return ((h * 60 + m) * 60 + s) * fpsn + f


def frames_to_tc(n, fpsn):
    f = n % fpsn
    s = n // fpsn
    return f"{s // 3600:02d}:{(s // 60) % 60:02d}:{s % 60:02d}:{f:02d}"


def sec_to_frames(sec, fps):
    return int(round(float(sec) * float(fps)))


def probe_seconds(path):
    if not shutil.which("ffprobe"):
        return None
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
            capture_output=True, text=True, timeout=30,
        ).stdout.strip()
        return float(out) if out else None
    except (ValueError, subprocess.SubprocessError):
        return None


def reel_name(path):
    # Short ASCII reel; the real file name goes into the FROM CLIP NAME comment.
    return "AX"


def main():
    args = sys.argv[1:]
    if not args or args[0].startswith("-"):
        die(__doc__)
    plan_path = args[0]
    out_dir = args[args.index("--out") + 1] if "--out" in args else os.path.dirname(os.path.abspath(plan_path))
    do_probe = "--no-probe" not in args
    plan = json.load(open(plan_path, encoding="utf-8"))
    fps = float(plan.get("fps", 24))
    fpsn = nominal(fps)
    start = tc_to_frames(plan.get("start_tc", "01:00:00:00"), fpsn)
    name = plan.get("name", "cutplan")
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)
    os.makedirs(out_dir, exist_ok=True)

    problems, warnings = [], []
    tracks = {}  # track -> list of events
    notes, markers = [], []
    probed = {}

    events = [(e, "V") for e in plan.get("clips", [])] + [(e, "A") for e in plan.get("audio", [])]
    for e, kind in events:
        eid = e.get("id", "?")
        track = e.get("track", "V1" if kind == "V" else "A1")
        path = e.get("file", "")
        if not os.path.isabs(path):
            warnings.append(f"{eid}: path is not absolute: {path}")
        if not os.path.exists(path):
            problems.append(f"{eid}: file not found: {path}")
        s_in = sec_to_frames(e.get("src_in", 0), fps)
        s_out = sec_to_frames(e["src_out"], fps) if "src_out" in e else None
        if s_out is None and do_probe and os.path.exists(path):
            d = probed.setdefault(path, probe_seconds(path))
            s_out = sec_to_frames(d, fps) if d else None
        if s_out is None:
            problems.append(f"{eid}: no src_out and media length unknown")
            continue
        if s_out <= s_in:
            problems.append(f"{eid}: src_out ({s_out}f) must be after src_in ({s_in}f)")
            continue
        if do_probe and os.path.exists(path):
            d = probed.setdefault(path, probe_seconds(path))
            if d is not None and s_out > sec_to_frames(d, fps) + 1:
                problems.append(f"{eid}: src_out {e['src_out']}s is beyond the media length {d:.3f}s")
        lst = tracks.setdefault(track, [])
        if e.get("record_in") is not None:
            r_in = start + sec_to_frames(e["record_in"], fps)
        else:
            r_in = lst[-1]["r_out"] if lst else start
        ev = {"id": eid, "file": path, "s_in": s_in, "s_out": s_out, "r_in": r_in,
              "r_out": r_in + (s_out - s_in), "kind": kind, "track": track}
        lst.append(ev)
        if e.get("marker"):
            markers.append([frames_to_tc(r_in, fpsn), r_in - start, track, eid, e["marker"]])
        for key in ("transition_after", "motion", "effects", "base_db", "duck", "audio_db", "note"):
            if key in e and e[key] not in (None, {"type": "cut"}):
                notes.append([frames_to_tc(r_in, fpsn), track, eid, key, json.dumps(e[key], ensure_ascii=False)])

    report = [f"Plan: {name}  fps={fps} (EDL timecode at {fpsn} NDF)  start={frames_to_tc(start, fpsn)}"]
    for track, lst in sorted(tracks.items()):
        lst.sort(key=lambda x: x["r_in"])
        for a, b in zip(lst, lst[1:]):
            if b["r_in"] < a["r_out"]:
                problems.append(f"{track}: {b['id']} overlaps {a['id']} by {a['r_out'] - b['r_in']} frames")
            elif b["r_in"] > a["r_out"]:
                warnings.append(f"{track}: gap of {b['r_in'] - a['r_out']} frames between {a['id']} and {b['id']}")
        total = lst[-1]["r_out"] - lst[0]["r_in"]
        report.append(f"{track}: {len(lst)} events, {total} frames ({total / fps:.3f}s), "
                      f"{frames_to_tc(lst[0]['r_in'], fpsn)} -> {frames_to_tc(lst[-1]['r_out'], fpsn)}")
        # One EDL per track, so every audio EDL uses channel "A"; the NLE places it on the track you import it to.
        chan = "V" if lst[0]["kind"] == "V" else "A"
        edl = [f"TITLE: {name} {track}", "FCM: NON-DROP FRAME", ""]
        for i, ev in enumerate(lst, 1):
            edl.append(f"{i:03d}  {reel_name(ev['file']):<8} {chan:<5} C        "
                       f"{frames_to_tc(ev['s_in'], fpsn)} {frames_to_tc(ev['s_out'], fpsn)} "
                       f"{frames_to_tc(ev['r_in'], fpsn)} {frames_to_tc(ev['r_out'], fpsn)}")
            edl.append(f"* FROM CLIP NAME: {os.path.basename(ev['file'])}")
            edl.append(f"* COMMENT: {ev['id']}")
            edl.append("")
        with open(os.path.join(out_dir, f"{safe}_{track}.edl"), "w", encoding="utf-8") as f:
            f.write("\n".join(edl))

    with open(os.path.join(out_dir, "markers.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["record_tc", "frame_from_start", "track", "id", "marker"])
        w.writerows(markers)
    with open(os.path.join(out_dir, "notes.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["record_tc", "track", "id", "what", "value"])
        w.writerows(notes)
    report += ["", "BLOCKING:"] + (problems or ["none"]) + ["", "WARNINGS:"] + (warnings or ["none"])
    with open(os.path.join(out_dir, "report.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(report) + "\n")
    print("\n".join(report))
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
