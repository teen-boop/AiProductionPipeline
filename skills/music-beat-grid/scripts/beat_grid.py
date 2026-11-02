#!/usr/bin/env python3
"""Measure a music track's beat grid, lay chapters on it, and check cut times against it.

Subcommands
  measure <audio> [--bpm-min 70] [--bpm-max 180] [--bpm HINT] [--bars] [--json out.json]
      Period and phase of the beat. The phase is measured twice: full band and kick band (low-pass 120 Hz).
      Off-beat hi-hats can pull the full-band phase half a beat late; use the KICK phase, and the script warns
      when the two disagree. --bars prints one row per bar (4 beats): RMS dB and low-band dB, to find the
      intro, the riser, the drop (a jump of roughly 10 dB in the low band), the break and the return.
  sheet --period P [--phase PH] [--fps 24] --length L --chapters "Intro:4, Build:8, Drop:8, Flurry:4, End:rest"
      Prints a cut sheet: chapter, beats, start/end seconds and frames. A chapter whose name starts with
      "Flurry" is split one cut per beat, then one per half beat (accelerating into the ending).
  snap --period P [--phase PH] [--fps 24] --cuts "1.77,4.23,7.5" | --cuts-file edl.json
      For each cut time: distance to the nearest beat and half beat, in ms and frames; flags cuts more than
      2 frames off. Accepts a dialogue_cut / cut-list JSON with "keep" ranges or a list of numbers.

Python 3 stdlib only; ffmpeg on PATH for measure.
"""
import argparse
import array
import json
import math
import subprocess
import sys

SR = 11025
HOP = 256  # ~23 ms


def decode(path, lowpass=None):
    cmd = ["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR)]
    if lowpass:
        cmd += ["-af", "lowpass=f=%d,lowpass=f=%d" % (lowpass, lowpass)]
    cmd += ["-f", "s16le", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    a = array.array("h")
    a.frombytes(raw[: len(raw) // 2 * 2])
    if sys.byteorder == "big":
        a.byteswap()
    return a


def energy(samples):
    out = []
    for i in range(0, len(samples) - HOP, HOP):
        seg = samples[i:i + HOP]
        out.append(sum(x * x for x in seg) / HOP)
    return out


def onset_env(e):
    logs = [math.log10(x + 1.0) for x in e]
    env = [0.0] + [max(0.0, logs[i] - logs[i - 1]) for i in range(1, len(logs))]
    m = sum(env) / len(env) if env else 0
    return [x - m for x in env]


def autocorr_period(env, bpm_min, bpm_max):
    fr = SR / HOP
    lo, hi = int(fr * 60 / bpm_max), int(fr * 60 / bpm_min) + 1
    best, best_lag = -1e18, lo
    n = len(env)
    for lag in range(max(1, lo), min(hi, n - 1)):
        s = sum(env[i] * env[i + lag] for i in range(n - lag)) / (n - lag)
        if s > best:
            best, best_lag = s, lag
    return best_lag / fr


def fold_strength(env, period, bins=48):
    fr = SR / HOP
    h = [0.0] * bins
    for i, v in enumerate(env):
        if v > 0:
            ph = ((i / fr) % period) / period
            h[int(ph * bins) % bins] += v
    k = max(range(bins), key=lambda j: h[j])
    peak = h[k] / (sum(h) / bins + 1e-9)
    return peak, (k + 0.5) / bins * period


def refine(env, period):
    best = (0, period, 0)
    for step in range(-60, 61):
        p = period * (1 + step * 0.0005)
        s, ph = fold_strength(env, p)
        if s > best[0]:
            best = (s, p, ph)
    return best[1], best[2]


def db(x):
    return 10 * math.log10(x + 1e-12) - 90.3  # relative to int16 full scale


def measure(a):
    full = decode(a.audio)
    low = decode(a.audio, 120)
    ef, el = energy(full), energy(low)
    envf, envl = onset_env(ef), onset_env(el)
    lo, hi = a.bpm_min, a.bpm_max
    if a.bpm:
        lo, hi = a.bpm * 0.92, a.bpm * 1.08
    p0 = autocorr_period(envl if sum(1 for x in envl if x > 0) > 10 else envf, lo, hi)
    period, phase_kick = refine(envl, p0)
    _, phase_full = fold_strength(envf, period)
    dur = len(full) / SR
    res = {"file": a.audio, "duration": round(dur, 3), "period": round(period, 5), "bpm": round(60 / period, 2),
           "phase_kick": round(phase_kick, 4), "phase_full": round(phase_full, 4)}
    diff = abs(((phase_full - phase_kick + period / 2) % period) - period / 2)
    print("duration %.2f s   beat %.4f s = %.2f BPM" % (dur, period, 60 / period))
    print("phase (kick band, USE THIS) %.3f s   phase (full band) %.3f s" % (phase_kick, phase_full))
    if diff > period / 4:
        print("WARNING: full-band phase is %.0f ms away from the kick phase (off-beat hats?). Use the kick phase." % (diff * 1000))
        res["phase_warning"] = True
    if a.bars:
        fr = SR / HOP
        bar = 4 * period
        print("\nbar  start s   RMS dB  low dB")
        prev = None
        t = phase_kick
        n = 1
        while t < dur:
            i0, i1 = int(t * fr), int(min(dur, t + bar) * fr)
            if i1 <= i0:
                break
            r = db(sum(ef[i0:i1]) / (i1 - i0))
            l = db(sum(el[i0:i1]) / (i1 - i0))
            mark = "  <- low band +%.0f dB" % (l - prev) if prev is not None and l - prev >= 8 else ""
            print("%3d  %7.3f  %6.1f  %6.1f%s" % (n, t, r, l, mark))
            prev, t, n = l, t + bar, n + 1
    if a.json:
        with open(a.json, "w") as fh:
            json.dump(res, fh, indent=2)


def sheet(a):
    P, fps, L = a.period, a.fps, a.length
    fr = lambda t: int(round(t * fps))
    print("beat %.4f s (%.2f BPM), %g fps, %.2f frames per beat, phase %.3f s\n" % (P, 60 / P, fps, P * fps, a.phase))
    print("%-24s %11s %9s %9s %13s" % ("chapter", "beats", "start s", "end s", "frames"))
    b = 0.0
    for part in [c.strip() for c in a.chapters.split(",") if c.strip()]:
        name, n = part.rsplit(":", 1)
        name, n = name.strip(), n.strip()
        t0 = a.phase + b * P if b else 0.0
        nb = (L - a.phase) / P - b if n == "rest" else float(n)
        t1 = L if n == "rest" else a.phase + (b + nb) * P
        print("%-24s %11s %9.3f %9.3f %13s" % (name, "%.1f-%.1f" % (b, b + nb), t0, t1, "%d-%d" % (fr(t0), fr(t1))))
        if name.lower().startswith("flurry"):
            s = 0.0
            while s < nb - 1e-6:
                t = a.phase + (b + s) * P
                print("%-24s %11s %9.3f %9s %13d" % ("  cut", "%.1f" % (b + s), t, "", fr(t)))
                s += 1.0 if s < nb / 2 else 0.5
        b += nb
    print("\ntotal %.3f s = %d frames" % (L, fr(L)))


def snap_check(a):
    cuts = []
    if a.cuts:
        cuts = [float(x) for x in a.cuts.split(",") if x.strip()]
    if a.cuts_file:
        with open(a.cuts_file) as fh:
            d = json.load(fh)
        if isinstance(d, dict) and "keep" in d:
            acc = 0.0
            for k0, k1 in d["keep"][:-1]:
                acc += k1 - k0
                cuts.append(acc)
        elif isinstance(d, list):
            cuts += [float(x) for x in d]
    P, fps, ph = a.period, a.fps, a.phase
    bad = 0
    print("%9s %12s %12s %8s" % ("cut s", "to beat ms", "to half ms", "frames"))
    for c in cuts:
        k = (c - ph) / P
        db_ = (k - round(k)) * P
        dh = (k * 2 - round(k * 2)) * P / 2
        best = min(abs(db_), abs(dh))
        fr = best * fps
        flag = "  OFF GRID" if fr > 2 else ""
        bad += 1 if flag else 0
        print("%9.3f %+12.0f %+12.0f %8.1f%s" % (c, db_ * 1000, dh * 1000, fr, flag))
    print("\n%d of %d cuts more than 2 frames from a beat or half beat" % (bad, len(cuts)))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("measure")
    m.add_argument("audio")
    m.add_argument("--bpm-min", type=float, default=70)
    m.add_argument("--bpm-max", type=float, default=180)
    m.add_argument("--bpm", type=float)
    m.add_argument("--bars", action="store_true")
    m.add_argument("--json")
    s = sub.add_parser("sheet")
    s.add_argument("--period", type=float, required=True)
    s.add_argument("--phase", type=float, default=0.0)
    s.add_argument("--fps", type=float, default=24)
    s.add_argument("--length", type=float, required=True)
    s.add_argument("--chapters", required=True)
    c = sub.add_parser("snap")
    c.add_argument("--period", type=float, required=True)
    c.add_argument("--phase", type=float, default=0.0)
    c.add_argument("--fps", type=float, default=24)
    c.add_argument("--cuts")
    c.add_argument("--cuts-file")
    a = ap.parse_args()
    {"measure": measure, "sheet": sheet, "snap": snap_check}[a.cmd](a)


if __name__ == "__main__":
    main()
