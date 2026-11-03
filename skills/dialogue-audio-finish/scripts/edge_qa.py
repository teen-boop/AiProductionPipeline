#!/usr/bin/env python3
"""Measure the audio at every dialogue edge: is a word clipped, is there dead air, does the level jump between clips?

Usage:
  python3 edge_qa.py plan  dialogue_cut.candidate.json --out qc/edges [--apply]
  python3 edge_qa.py render final.mp4 --cuts-file cutplan.json | --cuts "3.2,7.9" --out qc/edges_render

plan    reads clips with source, in, out (dialogue-cut output, or any cut plan with file/src_in/src_out) and checks
        each clip on its SOURCE audio. --apply writes <plan>.edges.json with suggested edges; it never overwrites the plan.
render  checks each cut time on the encoded file: a join that lands inside sound, and level jumps across the cut.

Method (1 ms resolution): a mono decode band-passed 80-8000 Hz (speech) and 3500-11000 Hz (s/sh/t tails); an 8 ms RMS
envelope in dB every 1 ms; the room floor is the 12th percentile of each band. Speech is floor+20 dB, a breath sits
10-20 dB over the floor. Thresholds:
  in/out inside sound     loudest 6 ms at the edge > floor+20, unless the edge sits in a real dip (within 4 dB of the
                          quietest point of +-40 ms, and that point 12 dB under the local peak). If 40 ms past the edge
                          stays > floor+15 the cut is inside continuous speech: the suggestion moves it to the nearest
                          pause (30 ms under floor+10) within 0.6 s; otherwise the onset/tail is followed to silence.
  sibilant tail cut       last 6 ms of the high band > high floor+24 while the next 40 ms is still > high floor+15
  dead air                > 90 ms of silence at the head, > 110 ms at the tail
  level jump              > 7 dB between voiced medians of the last 400 ms of a clip and the first 400 ms of the next
                          clip, when they come from different sources
Also reports per-source speech level (70th percentile of voiced envelope) with the gain to the median, and the quietest
1.5 s of each source as room tone. Numbers are evidence, not a verdict: listen to every flagged edge.
Needs ffmpeg on PATH. Standard library only.
"""
import argparse
import array
import json
import math
import os
import shutil
import subprocess
import sys

HOP_MS, WIN_MS = 1, 8
SPEECH, BREATH, CONNECT, SIB, SIB_NEXT = 20.0, 10.0, 15.0, 24.0, 15.0
HEAD_MAX, TAIL_MAX, JUMP_MAX = 90, 110, 7.0
PAD_IN, PAD_OUT = 30, 14


def decode(path, sr, band):
    cmd = ["ffmpeg", "-v", "error", "-i", path, "-vn", "-ac", "1", "-ar", str(sr),
           "-af", f"highpass=f={band[0]},lowpass=f={band[1]}", "-f", "s16le", "-"]
    raw = subprocess.run(cmd, capture_output=True).stdout
    a = array.array("h")
    a.frombytes(raw[: len(raw) // 2 * 2])
    if sys.byteorder == "big":
        a.byteswap()
    return a


def envelope(samples, sr):
    """8 ms RMS in dB, one value per 1 ms."""
    blk = sr * HOP_MS // 1000
    n = len(samples) // blk
    e = [0.0] * n
    for i in range(n):
        s = 0
        for v in samples[i * blk:(i + 1) * blk]:
            s += v * v
        e[i] = s / blk
    out, acc = [0.0] * n, 0.0
    for i in range(n):
        acc += e[i]
        if i >= WIN_MS:
            acc -= e[i - WIN_MS]
        out[i] = 10 * math.log10(acc / min(i + 1, WIN_MS) / 32768.0 ** 2 + 1e-12)
    return out


def pct(vals, p):
    if not vals:
        return None
    v = sorted(vals)
    return v[min(len(v) - 1, int(p / 100 * len(v)))]


class Track:
    def __init__(self, path):
        self.path = path
        self.eb = envelope(decode(path, 16000, (80, 8000)), 16000)
        self.eh = envelope(decode(path, 24000, (3500, 11000)), 24000)
        self.fb, self.fh = pct(self.eb, 12), pct(self.eh, 12)
        voiced = [x for x in self.eb if x > self.fb + SPEECH]
        top = max(voiced) if voiced else None
        self.level = pct([x for x in voiced if x > top - 30], 70) if voiced else None

    def seg(self, a, b, hi=False):
        e = self.eh if hi else self.eb
        return e[max(0, a):max(0, min(len(e), b))] or [-120.0]

    def loud(self, i):
        return self.eb[i] > self.fb + SPEECH if 0 <= i < len(self.eb) else False

    def room_tone(self):
        best, start = None, 0
        for s in range(0, min(len(self.eb), 600000) - 1500, 500):
            m = sum(self.eb[s:s + 1500]) / 1500
            if best is None or m < best:
                best, start = m, s
        return {"start": start / 1000, "dur": 1.5, "mean_db": round(best, 1) if best is not None else None}


def at_dip(t, i):
    """The edge sits in a real dip: within 4 dB of the quietest point of +-40 ms, and that point is 12 dB under the peak."""
    w = t.seg(i - 40, i + 40)
    return max(t.seg(i - 3, i + 3)) <= min(w) + 4 and min(w) <= max(w) - 12


def quiet_run(t, a, b, step):
    """First index from a towards b (step +1/-1) that starts 30 ms under floor+BREATH; None if there is none."""
    k = a
    while (k < b) if step > 0 else (k > b):
        if all(t.eb[x] <= t.fb + BREATH for x in range(min(k, k + 30 * step), max(k, k + 30 * step)) if 0 <= x < len(t.eb)):
            return k
        k += step
    return None


def check_in(t, i):
    head = max(t.seg(i, i + 6))
    issues, sug = [], i
    if head > t.fb + SPEECH and not at_dip(t, i):
        if min(t.seg(i - 40, i)) > t.fb + CONNECT:
            q = quiet_run(t, i, i - 600, -1)
            issues.append("in: inside continuous speech (cuts into a word or phrase)"
                          + ("" if q is not None else "; no pause within 0.6 s, listen"))
            if q is not None:
                sug = q - PAD_IN
        else:
            issues.append("in: starts inside a sound (clipped onset)")
            j = i
            while j > i - 120 and t.eb[max(0, j - 1)] > t.fb + BREATH:
                j -= 1
            sug = j - PAD_IN
    else:
        j = i
        while j < len(t.eb) - 20 and not all(t.loud(k) for k in range(j, j + 20)):
            j += 1
        if j - i > HEAD_MAX:
            issues.append(f"in: {j - i} ms of dead air before the first sound")
            k = j
            while k > j - 60 and t.eb[max(0, k - 1)] > t.fb + BREATH:  # keep a plosive burst
                k -= 1
            sug = k - PAD_IN
    return issues, max(0, sug)


def check_out(t, o):
    tail = max(t.seg(o - 6, o))
    issues, sug = [], o
    if tail > t.fb + SPEECH and not at_dip(t, o):
        if min(t.seg(o, o + 40)) > t.fb + CONNECT:
            q = quiet_run(t, o, o + 600, 1)
            issues.append("out: inside continuous speech (cuts off a word or phrase)"
                          + ("" if q is not None else "; no pause within 0.6 s, listen"))
            if q is not None:
                sug = q + PAD_OUT
        else:
            issues.append("out: ends inside a sound (clipped word)")
            j = o
            while j < o + 120 and j < len(t.eb) and t.eb[j] > t.fb + BREATH:
                j += 1
            sug = j + PAD_OUT
    else:
        j = o
        while j > 20 and not all(t.loud(k) for k in range(j - 20, j)):
            j -= 1
        if o - j > TAIL_MAX:
            issues.append(f"out: {o - j} ms of dead air after the last sound")
            k = j
            while k < j + 40 and k < len(t.eb) and t.eb[k] > t.fb + BREATH:  # follow the decay
                k += 1
            sug = k + PAD_OUT
    if sug == o and max(t.seg(o - 6, o, True)) > t.fh + SIB and min(t.seg(o, o + 40, True)) > t.fh + SIB_NEXT:
        issues.append("out: cuts an s/sh/t tail")
        j = o
        while j < o + 80 and j < len(t.eh) and t.eh[j] > t.fh + SIB_NEXT:
            j += 1
        sug = j + PAD_OUT
    return issues, sug


def voiced_median(t, a, b):
    v = [x for x in t.seg(a, b) if x > t.fb + SPEECH]
    return pct(v, 50) if len(v) > 40 else None


def load_plan(path):
    d = json.load(open(path, encoding="utf-8"))
    fps = float(d.get("fps", 24))
    clips = []
    for c in d.get("clips", []):
        src = c.get("source") or c.get("file")
        i, o = c.get("in", c.get("src_in")), c.get("out", c.get("src_out"))
        if src and i is not None and o is not None:
            clips.append({"id": c.get("id", f"C{len(clips) + 1:02d}"), "source": src, "in": float(i), "out": float(o)})
    return d, fps, clips


def load_cuts(a):
    cuts = [float(x) for x in (a.cuts or "").split(",") if x.strip()]
    if a.cuts_file:
        d = json.load(open(a.cuts_file, encoding="utf-8"))
        if isinstance(d, dict) and "keep" in d:
            acc = 0.0
            for k0, k1 in d["keep"][:-1]:
                acc += k1 - k0
                cuts.append(acc)
        else:
            items = (d.get("clips") or d.get("events") or []) if isinstance(d, dict) else d
            acc = 0.0
            for it in items:
                if isinstance(it, (int, float)):
                    cuts.append(float(it))
                elif it.get("record_in") is not None:
                    cuts.append(float(it["record_in"]))
                elif it.get("in", it.get("src_in")) is not None:
                    acc += float(it.get("out", it.get("src_out"))) - float(it.get("in", it.get("src_in")))
                    cuts.append(acc)
    return sorted(c for c in set(round(c, 4) for c in cuts) if c > 0)


def write(out, name, rep, lines):
    os.makedirs(out, exist_ok=True)
    json.dump(rep, open(os.path.join(out, "edges.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(os.path.join(out, "edges.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("\n".join(lines[-3:]))


def run_plan(a):
    d, fps, clips = load_plan(a.target)
    if not clips:
        sys.exit("no clips with source/in/out in the plan")
    tracks = {}
    for c in clips:
        if c["source"] not in tracks:
            if not os.path.exists(c["source"]):
                sys.exit(f"missing source: {c['source']}")
            tracks[c["source"]] = Track(c["source"])
    levels = [t.level for t in tracks.values() if t.level is not None]
    ref = pct(levels, 50) if levels else None
    rows, flagged, sugg = [], 0, {}
    for n, c in enumerate(clips):
        t = tracks[c["source"]]
        i, o = int(round(c["in"] * 1000)), int(round(c["out"] * 1000))
        iss_i, si = check_in(t, i)
        iss_o, so = check_out(t, o)
        issues = iss_i + iss_o
        if n + 1 < len(clips) and clips[n + 1]["source"] != c["source"]:
            nx = clips[n + 1]
            t2 = tracks[nx["source"]]
            j = int(round(nx["in"] * 1000))
            m1, m2 = voiced_median(t, o - 400, o), voiced_median(t2, j, j + 400)
            if m1 is not None and m2 is not None and abs(m1 - m2) > JUMP_MAX:
                issues.append(f"level jump to {nx['id']}: {m2 - m1:+.1f} dB")
        if issues:
            flagged += 1
        if si != i or so != o:
            ai, ao = si / 1000, so / 1000
            sugg[c["id"]] = {"audio_in": round(ai, 3), "audio_out": round(ao, 3),
                             "in": round(math.floor(ai * fps + 1e-9) / fps, 4),
                             "out": round(math.ceil(ao * fps - 1e-9) / fps, 4)}
        rows.append({"id": c["id"], "source": c["source"], "in": c["in"], "out": c["out"],
                     "issues": issues, "suggested": sugg.get(c["id"])})
    srcs = {p: {"speech_db": round(t.level, 1) if t.level is not None else None,
                "gain_to_median_db": round(ref - t.level, 1) if ref is not None and t.level is not None else None,
                "floor_db": round(t.fb, 1), "room_tone": t.room_tone()} for p, t in tracks.items()}
    rep = {"mode": "plan", "plan": a.target, "clips": rows, "sources": srcs}
    md = ["# Edge QA (plan)", "", "| id | in | out | issues | suggested in/out (audio exact) |", "|---|---|---|---|---|"]
    for r in rows:
        s = r["suggested"]
        md.append(f"| {r['id']} | {r['in']} | {r['out']} | {'; '.join(r['issues']) or 'ok'} | "
                  f"{(str(s['audio_in']) + ' / ' + str(s['audio_out'])) if s else ''} |")
    md += ["", "| source | speech dB | gain to median | room tone |", "|---|---|---|---|"]
    for p, s in srcs.items():
        md.append(f"| {os.path.basename(p)} | {s['speech_db']} | {s['gain_to_median_db']} | "
                  f"{s['room_tone']['start']} s +1.5 s |")
    if a.apply and sugg:
        d2 = json.loads(json.dumps(d))
        for c in d2.get("clips", []):
            if c.get("id") in sugg:
                c.update({k: v for k, v in sugg[c["id"]].items()})
                c["edge_qa"] = "moved"
        d2["status"] = "candidate"
        dst = os.path.splitext(a.target)[0] + ".edges.json"
        if os.path.exists(dst):
            sys.exit(f"refusing to overwrite {dst}")
        json.dump(d2, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        md.append(f"\nSuggested edges written to {dst} (the original plan is untouched).")
    md += ["", f"{len(rows)} clips, {flagged} flagged, {len(sugg)} with suggested edges.",
           "Listen to every flagged edge in context; a measured dip is not proof a word is complete."]
    write(a.out, "edges", rep, md)


def run_render(a):
    t = Track(a.target)
    cuts = load_cuts(a)
    if not cuts:
        sys.exit("no cut times: give --cuts or --cuts-file")
    rows, flagged = [], 0
    for c in cuts:
        i = int(round(c * 1000))
        issues = []
        edge = max(t.seg(i - 6, i + 6))
        if edge > t.fb + SPEECH and not at_dip(t, i):
            issues.append("join inside sound (listen for a clipped or doubled syllable)")
        m1, m2 = voiced_median(t, i - 400, i), voiced_median(t, i, i + 400)
        if m1 is not None and m2 is not None and abs(m1 - m2) > JUMP_MAX:
            issues.append(f"level jump {m2 - m1:+.1f} dB")
        flagged += bool(issues)
        rows.append({"time": c, "issues": issues})
    rep = {"mode": "render", "file": a.target, "floor_db": round(t.fb, 1), "cuts": rows}
    md = ["# Edge QA (render)", "", "| cut s | issues |", "|---|---|"]
    md += [f"| {r['time']} | {'; '.join(r['issues']) or 'ok'} |" for r in rows]
    md += ["", f"{len(rows)} cuts, {flagged} flagged.", "Listen to every flagged join on the delivered file."]
    write(a.out, "edges", rep, md)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=["plan", "render"])
    ap.add_argument("target")
    ap.add_argument("--out", required=True)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--cuts")
    ap.add_argument("--cuts-file")
    a = ap.parse_args()
    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg not found on PATH")
    run_plan(a) if a.mode == "plan" else run_render(a)


if __name__ == "__main__":
    main()
