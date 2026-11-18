#!/usr/bin/env python3
"""Measure the camera path of every shot in a source video and print a CAMERA LOCK block for a Seedance edit prompt.

Usage:  python3 camera_path.py SOURCE.mp4 [--cuts 3.29,6.97] [--compare RESULT.mp4]

Each frame is compared with the FIRST frame of its shot (not with the previous frame: a slow push-in moves
less than a pixel per frame and is invisible frame to frame). For every 0.5 s it finds the scale and shift that
map the first frame onto the current one:
  scale > 1  = the frame got tighter  = camera pushed in (or zoomed)
  scale < 1  = the frame got wider    = camera pulled out
  dx > 0     = camera panned / slid right   (as % of frame width)
  dy > 0     = camera tilted / moved down   (as % of frame height)
With --compare it measures the result the same way and prints both paths side by side.
Needs ffmpeg and numpy.
"""
import subprocess, sys, re, argparse
import numpy as np

W, H, FPS = 320, 180, 4


def probe_dur(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                                capture_output=True, text=True).stdout.strip())


def detect_cuts(f, thr=0.15):
    err = subprocess.run(["ffmpeg", "-v", "info", "-i", f, "-vf", f"select='gt(scene,{thr})',showinfo", "-an", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    return [float(x) for x in re.findall(r"pts_time:([0-9.]+)", err)]


def frames(f, ss, t):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{ss:.3f}", "-t", f"{t:.3f}", "-i", f, "-vf",
                          f"fps={FPS},scale={W}:{H},format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    n = len(raw) // (W * H)
    return np.frombuffer(raw[:n * W * H], np.uint8).reshape(n, H, W).astype(float)


def warp(a, s, dx, dy):
    """Crop of `a` around (center+dx,dy) of size (W/s,H/s), resampled to WxH (s>=1)."""
    cw, ch = W / s, H / s
    cx, cy = W / 2 + dx, H / 2 + dy
    xs = np.clip((cx - cw / 2 + (np.arange(W) + .5) * cw / W).astype(int), 0, W - 1)
    ys = np.clip((cy - ch / 2 + (np.arange(H) + .5) * ch / H).astype(int), 0, H - 1)
    return a[ys][:, xs]


def ncc(a, b, m):
    a = a[m]; b = b[m]
    a = (a - a.mean()) / (a.std() + 1e-9); b = (b - b.mean()) / (b.std() + 1e-9)
    return float((a * b).mean())


def fit(a, b):
    """Find s,dx,dy with warp(a)~b (push-in) or warp(b)~a (pull-out). Returns scale, dx%, dy%."""
    m = np.zeros((H, W), bool); m[int(H * .06):int(H * .94), int(W * .06):int(W * .94)] = True
    best = (-2, 1.0, 0.0, 0.0)
    for direction in (1, -1):
        src, dst = (a, b) if direction == 1 else (b, a)
        cand = []
        for s in np.arange(1.0, 1.31, 0.02):
            for dx in range(-60, 61, 4):
                for dy in range(-36, 37, 3):
                    cand.append((ncc(warp(src, s, dx, dy), dst, m), s, dx, dy))
        c, s, dx, dy = max(cand)
        # refine
        for s2 in np.arange(s - .02, s + .021, .005):
            if s2 < 1: continue
            for dx2 in range(dx - 4, dx + 5, 1):
                for dy2 in range(dy - 3, dy + 4, 1):
                    c2 = ncc(warp(src, s2, dx2, dy2), dst, m)
                    if c2 > c: c, s, dx, dy = c2, s2, dx2, dy2
        if direction == -1:
            s, dx, dy = 1 / s, -dx / s, -dy / s
        if c > best[0]: best = (c, s, dx, dy)
    c, s, dx, dy = best
    return s, 100 * dx / W, 100 * dy / H, c


def shot_path(f, a, b):
    fr = frames(f, a + 0.04, b - a - 0.08)
    out = []
    for i in range(0, len(fr), 2):
        s, dx, dy, c = fit(fr[0], fr[i]) if i else (1.0, 0.0, 0.0, 1.0)
        out.append((a + i / FPS, s, dx, dy, c))
    # drop samples where the match broke (low correlation or a jump far from its neighbours)
    good = [out[0]]
    for q in out[1:]:
        prev = good[-1]
        jump = abs(100 * (q[1] - prev[1])) + abs(q[2] - prev[2]) + abs(q[3] - prev[3])
        if q[4] >= 0.35 and jump < 15:
            good.append(q)
    return good


def describe(path, a, b):
    """Plain-English camera line from a measured path."""
    t = [p[0] for p in path]; z = [100 * (p[1] - 1) for p in path]; x = [p[2] for p in path]; y = [p[3] for p in path]
    def moving(v, thr):
        idx = [i for i in range(1, len(v)) if abs(v[i] - v[i - 1]) >= thr]
        return (t[idx[0] - 1], t[idx[-1]]) if idx else None
    parts = []
    zr, xr, yr = moving(z, 0.4), moving(x, 0.4), moving(y, 0.4)
    if abs(z[-1]) >= 1.0:
        a0, a1 = zr or (a, b)
        parts.append(f"a slow physical dolly {'push-in' if z[-1] > 0 else 'pull-out'} from {a0:.1f} s to {a1:.1f} s: "
                     f"by the end of the shot everything in frame is about {abs(z[-1]):.0f}% {'bigger' if z[-1] > 0 else 'smaller'} than in its first frame")
    if abs(x[-1]) >= 1.0:
        a0, a1 = xr or (a, b)
        parts.append(f"a drift to the {'right' if x[-1] > 0 else 'left'} of about {abs(x[-1]):.0f}% of the frame width from {a0:.1f} s to {a1:.1f} s")
    if abs(y[-1]) >= 1.0:
        a0, a1 = yr or (a, b)
        parts.append(f"a tilt {'down' if y[-1] > 0 else 'up'} of about {abs(y[-1]):.0f}% of the frame height from {a0:.1f} s to {a1:.1f} s")
    if not parts:
        return "locked off on a tripod, no movement at all (measured: under 1% zoom and shift)"
    return "; ".join(parts) + "; otherwise steady, no shake"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("--cuts"); ap.add_argument("--compare")
    o = ap.parse_args()
    dur = probe_dur(o.src)
    cuts = [float(c) for c in o.cuts.split(",")] if o.cuts else [c for c in detect_cuts(o.src) if 0.3 < c < dur - 0.3]
    bounds = [0.0] + cuts + [dur]
    lines = []
    for k in range(len(bounds) - 1):
        a, b = bounds[k], bounds[k + 1]
        if b - a < 0.5:
            continue
        p = shot_path(o.src, a, b)
        r = shot_path(o.compare, a, min(b, probe_dur(o.compare))) if o.compare else None
        print(f"\n== SHOT {k + 1}  {a:.1f}-{b:.1f} s   (zoom %, dx % width, dy % height vs the shot's first frame)")
        for i, q in enumerate(p):
            row = f"{q[0]:5.1f}s  src zoom{100 * (q[1] - 1):+5.1f} dx{q[2]:+5.1f} dy{q[3]:+5.1f}"
            if r and i < len(r):
                row += f"   | result zoom{100 * (r[i][1] - 1):+5.1f} dx{r[i][2]:+5.1f} dy{r[i][3]:+5.1f}"
            print(row)
        lines.append(f"[{a:.1f}-{b:.1f} s] SHOT {k + 1}: {describe(p, a, b)}.")
    print("\n---- paste into the prompt ----")
    print("CAMERA LOCK (as important as the action; measured from @video1, copy it exactly): the camera is a physical camera, "
          "separate from everything that changes in the scene, and it moves exactly as in @video1 in every shot:")
    print("\n".join(lines))
    print("The framing at the first and the last frame of every shot equals @video1 at those moments. Never add a move "
          "@video1 does not have, never drop or shorten a move it has, never replace a dolly with a lens zoom, never a static frame where @video1 moves.")


if __name__ == "__main__":
    main()
