#!/usr/bin/env python3
"""Mechanical QC of an ENCODED render: frame strips across every cut, black/flash frames, opening frames,
stream and duration checks, loudness. Writes evidence for VERIFY.md; it does not judge taste.

Usage:
  python3 cut_strips.py <render.mp4> --out <qc_dir> [--cuts "1.25,3.5" | --cuts-file edl.json | --detect 0.30]
                        [--side 5] [--opening 2.5] [--no-loudness] [--expect-duration S]

  --cuts / --cuts-file   cut times on the RENDER timeline (seconds). A JSON with "keep" ranges (dialogue_cut EDL),
                         a cut list with "record_in"/"start" fields, or a plain list of numbers is accepted.
  --detect T             no cut list: detect hard cuts with the ffmpeg scene score (default 0.30 when no cuts given).
  --side N               frames shown on each side of a cut (default 5 -> a 10-frame strip).
  --opening S            contact sheet of the first S seconds, every 2nd frame (default 2.5).

Writes into --out: strip_<NN>_<time>.jpg per cut, opening.jpg, report.json, report.md.
Needs ffmpeg + ffprobe on PATH and Pillow.
"""
import argparse
import json
import os
import re
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFont


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def probe(path):
    d = json.loads(run(["ffprobe", "-v", "error", "-show_entries",
                        "stream=codec_type,codec_name,width,height,r_frame_rate,avg_frame_rate,duration,nb_frames,sample_rate,channels"
                        ":format=duration,bit_rate", "-of", "json", path]).stdout)
    v = next(s for s in d["streams"] if s["codec_type"] == "video")
    au = next((s for s in d["streams"] if s["codec_type"] == "audio"), None)
    n, dd = v["r_frame_rate"].split("/")
    fps = float(n) / float(dd)
    return {"fps": fps, "width": v["width"], "height": v["height"], "vcodec": v.get("codec_name"),
            "video_duration": float(v.get("duration") or d["format"]["duration"]),
            "nb_frames": int(v["nb_frames"]) if v.get("nb_frames", "").isdigit() else None,
            "audio_duration": float(au["duration"]) if au and au.get("duration") else None,
            "audio": {"codec": au.get("codec_name"), "rate": au.get("sample_rate"), "channels": au.get("channels")} if au else None,
            "container_duration": float(d["format"]["duration"])}


def font(size):
    for f in ("/System/Library/Fonts/Supplemental/Arial.ttf", "/System/Library/Fonts/Helvetica.ttc",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "C:/Windows/Fonts/arial.ttf"):
        if os.path.exists(f):
            try:
                return ImageFont.truetype(f, size)
            except Exception:
                pass
    return ImageFont.load_default()


def frames(path, first, last, step, width, td):
    sel = "select='between(n\\,%d\\,%d)*not(mod(n-%d\\,%d))',scale=%d:-2" % (first, last, first, step, width)
    pat = os.path.join(td, "f_%04d.png")
    run(["ffmpeg", "-v", "error", "-y", "-i", path, "-vf", sel, "-fps_mode", "passthrough", pat])
    files = sorted(f for f in os.listdir(td) if f.startswith("f_"))
    return [os.path.join(td, f) for f in files]


def tile(images, labels, cols, out, title, mark_after=None):
    ims = [Image.open(p).convert("RGB") for p in images]
    if not ims:
        return False
    w, h = ims[0].size
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (w + 4) + 4, 34 + rows * (h + 4) + 4), (16, 16, 16))
    d = ImageDraw.Draw(sheet)
    d.text((6, 8), title, fill=(230, 230, 230), font=font(16))
    f = font(max(11, w // 14))
    for i, (im, lab) in enumerate(zip(ims, labels)):
        x, y = 4 + (i % cols) * (w + 4), 34 + (i // cols) * (h + 4)
        sheet.paste(im, (x, y))
        d.rectangle([x, y, x + len(lab) * f.size * 0.6 + 6, y + f.size + 4], fill=(0, 0, 0))
        d.text((x + 3, y + 1), lab, fill=(255, 220, 90), font=f)
        if mark_after is not None and i == mark_after:
            d.rectangle([x + w, y, x + w + 3, y + h], fill=(255, 40, 40))
    sheet.save(out, quality=88)
    return True


def detect_cuts(path, thr):
    r = run(["ffmpeg", "-v", "info", "-i", path, "-vf", "select='gt(scene,%.3f)',showinfo" % thr, "-an", "-f", "null", "-"])
    return [float(m) for m in re.findall(r"pts_time:([0-9.]+)", r.stderr)]


def black_frames(path):
    r = run(["ffmpeg", "-v", "info", "-i", path, "-vf", "blackdetect=d=0:pix_th=0.10:pic_th=0.98", "-an", "-f", "null", "-"])
    out = []
    for m in re.finditer(r"black_start:([0-9.]+) black_end:([0-9.]+) black_duration:([0-9.]+)", r.stderr):
        out.append([float(m.group(1)), float(m.group(2)), float(m.group(3))])
    return out


def loudness(path):
    r = run(["ffmpeg", "-v", "info", "-nostats", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"])
    tail = r.stderr[r.stderr.rfind("Summary:"):] if "Summary:" in r.stderr else ""
    get = lambda k: (re.search(k + r":\s+(-?[0-9.]+|-inf)", tail) or [None, None])[1]
    return {"integrated_lufs": get("I"), "lra_lu": get("LRA"), "true_peak_dbfs": get("Peak")}


def load_cuts(a):
    cuts = []
    if a.cuts:
        cuts += [float(x) for x in a.cuts.split(",") if x.strip()]
    if a.cuts_file:
        with open(a.cuts_file) as fh:
            d = json.load(fh)
        if isinstance(d, dict) and "keep" in d:
            acc = 0.0
            for k0, k1 in d["keep"][:-1]:
                acc += k1 - k0
                cuts.append(acc)
        else:
            items = d.get("events") or d.get("clips") or d.get("shots") if isinstance(d, dict) else d
            for it in items or []:
                if isinstance(it, (int, float)):
                    cuts.append(float(it))
                elif isinstance(it, dict):
                    for k in ("record_in", "start", "time"):
                        if it.get(k) is not None:
                            cuts.append(float(it[k]))
                            break
    return sorted(c for c in set(round(c, 4) for c in cuts) if c > 0)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("render")
    ap.add_argument("--out", required=True)
    ap.add_argument("--cuts")
    ap.add_argument("--cuts-file")
    ap.add_argument("--detect", type=float)
    ap.add_argument("--side", type=int, default=5)
    ap.add_argument("--opening", type=float, default=2.5)
    ap.add_argument("--no-loudness", action="store_true")
    ap.add_argument("--expect-duration", type=float)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    info = probe(a.render)
    fps = info["fps"]
    cuts = load_cuts(a)
    source = "cut list"
    if not cuts:
        cuts = detect_cuts(a.render, a.detect or 0.30)
        source = "scene detection (threshold %.2f) - misses dissolves and cuts between similar dark shots" % (a.detect or 0.30)

    report = {"render": os.path.abspath(a.render), "streams": info, "cuts_source": source, "cuts": [], "issues": []}
    one = 1.0 / fps
    if info["audio_duration"] is not None and abs(info["audio_duration"] - info["video_duration"]) > 1.5 * one:
        report["issues"].append("audio %.3f s vs video %.3f s differ by more than one frame (last syllable cut or tail of silence?)"
                                % (info["audio_duration"], info["video_duration"]))
    if info["audio"] is None:
        report["issues"].append("no audio stream")
    if a.expect_duration and abs(info["video_duration"] - a.expect_duration) > 1.5 * one:
        report["issues"].append("duration %.3f s, expected %.3f s" % (info["video_duration"], a.expect_duration))

    for i, c in enumerate(cuts, 1):
        n = int(round(c * fps))
        with tempfile.TemporaryDirectory() as td:
            fr = frames(a.render, max(0, n - a.side), n + a.side - 1, 1, 256, td)
            labels = ["%d" % k for k in range(max(0, n - a.side), max(0, n - a.side) + len(fr))]
            out = os.path.join(a.out, "strip_%02d_%07.3f.jpg" % (i, c))
            ok = tile(fr, labels, len(fr) or 1, out, "cut %d at %.3f s (frame %d); red bar = last frame before the cut" % (i, c, n),
                      mark_after=min(a.side, n) - 1)
        report["cuts"].append({"n": i, "time": c, "frame": n, "strip": out if ok else None})

    blacks = black_frames(a.render)
    for s, e, d in blacks:
        kind = "flash/black frame" if d <= 3 * one else "black interval"
        if s > one and e < info["video_duration"] - one:
            report["issues"].append("%s %.3f-%.3f s (%.0f frames) - intended?" % (kind, s, e, round(d * fps)))
    report["black"] = blacks

    with tempfile.TemporaryDirectory() as td:
        last = int(a.opening * fps)
        fr = frames(a.render, 0, last, 2, 320, td)
        report["opening_sheet"] = os.path.join(a.out, "opening.jpg")
        tile(fr, ["%d" % (k * 2) for k in range(len(fr))], 6, report["opening_sheet"],
             "first %.1f s, every 2nd frame: is the topic clear, is anything over the mouth, is frame 0 meaningful?" % a.opening)

    if not a.no_loudness and info["audio"]:
        report["loudness"] = loudness(a.render)

    with open(os.path.join(a.out, "report.json"), "w") as fh:
        json.dump(report, fh, indent=2)
    md = ["# Render QC: %s" % os.path.basename(a.render), "",
          "- %dx%d, %.3f fps, %s; video %.3f s, audio %s s, container %.3f s" % (
              info["width"], info["height"], fps, info["vcodec"], info["video_duration"],
              "%.3f" % info["audio_duration"] if info["audio_duration"] is not None else "n/a", info["container_duration"]),
          "- cuts: %d (%s)" % (len(cuts), source)]
    if report.get("loudness"):
        L = report["loudness"]
        md.append("- loudness: %s LUFS integrated, true peak %s dBFS, LRA %s LU (measured on this encoded file)"
                  % (L["integrated_lufs"], L["true_peak_dbfs"], L["lra_lu"]))
    md += ["", "## Mechanical issues"] + (["- " + x for x in report["issues"]] or ["- none found (this is not a visual or listening pass)"])
    md += ["", "## Strips to LOOK at (one per cut)"] + ["- cut %d %.3f s: %s" % (c["n"], c["time"], c["strip"]) for c in report["cuts"]]
    md += ["", "- opening: %s" % report["opening_sheet"]]
    with open(os.path.join(a.out, "report.md"), "w") as fh:
        fh.write("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
