#!/usr/bin/env python3
"""Build a delivery package for a client or a platform. Dry run by default; --apply writes it. Never uploads.

  deliver.py --project P --target client --client "Acme" --files A.mp4 B.mp4 [--version 2] [--zip] [--loudness] [--apply]
  deliver.py --project P --target instagram_reels --from-final "Promos/03-Rise" [--lang EN] [--apply]

Output: P/06_DELIVERY/<YYYY-MM-DD>_<target>[_<client>]/
  <files renamed by the target's rule>, matching .srt/.vtt captions, <name>_thumb.jpg,
  DELIVERY_NOTE.md (what, specs, checks), CHECKSUMS.sha256, optional <folder>.zip
"""
import argparse, csv, glob, hashlib, json, os, re, shutil, subprocess, sys, time, zipfile

# Limits as commonly published; platforms change them. When a file is near a limit, check the platform's current help page.
SPECS = {
    "client":          dict(aspects=None, max_s=None, max_mb=None, codecs={"h264", "hevc", "prores"}, lufs=None),
    "youtube":         dict(aspects={"16x9"}, max_s=12 * 3600, max_mb=256000, codecs={"h264", "hevc"}, lufs=-14),
    "youtube_shorts":  dict(aspects={"9x16", "1x1"}, max_s=180, max_mb=None, codecs={"h264", "hevc"}, lufs=-14),
    "tiktok":          dict(aspects={"9x16"}, max_s=600, max_mb=4000, codecs={"h264", "hevc"}, lufs=-14),
    "instagram_reels": dict(aspects={"9x16"}, max_s=180, max_mb=4000, codecs={"h264", "hevc"}, lufs=-14),
    "instagram_feed":  dict(aspects={"4x5", "1x1", "16x9"}, max_s=3600, max_mb=4000, codecs={"h264", "hevc"}, lufs=-14),
    "linkedin":        dict(aspects={"16x9", "1x1", "9x16", "4x5"}, max_s=600, max_mb=5000, codecs={"h264"}, lufs=-14),
    "x":               dict(aspects={"16x9", "1x1", "9x16"}, max_s=140, max_mb=512, codecs={"h264"}, lufs=-14),
}
ASPECTS = [("16x9", 16 / 9), ("9x16", 9 / 16), ("1x1", 1.0), ("4x5", 0.8), ("4x3", 4 / 3), ("21x9", 2.37)]
VIDEO = {".mp4", ".mov", ".m4v", ".webm"}
LANGS = {"EN", "RU", "ES", "DE", "FR", "IT", "PT", "UK", "PL", "ZH", "JA", "KO", "AR", "HE", "TR", "NL"}


def clean(s):
    return re.sub(r"_+", "_", re.sub(r"[^A-Za-z0-9\-]+", "_", s)).strip("_")


def qhash(p):
    h, size = hashlib.sha1(), os.path.getsize(p)
    with open(p, "rb") as f:
        h.update(f.read(1 << 20))
        if size > 2 << 20:
            f.seek(-(1 << 20), 2); h.update(f.read(1 << 20))
    return f"{size}:{h.hexdigest()}"


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


def probe(p):
    j = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                   "stream=codec_type,codec_name,width,height,r_frame_rate,pix_fmt:format=duration",
                                   "-of", "json", p], capture_output=True, text=True).stdout or "{}")
    v = next((s for s in j.get("streams", []) if s.get("codec_type") == "video"), {})
    au = next((s for s in j.get("streams", []) if s.get("codec_type") == "audio"), {})
    n, _, d = (v.get("r_frame_rate") or "0/1").partition("/")
    w, h = v.get("width") or 0, v.get("height") or 0
    asp = "?"
    if w and h:
        name, val = min(ASPECTS, key=lambda a: abs(a[1] - w / h))
        asp = name if abs(val - w / h) / val < 0.04 else f"{w}x{h}"
    return dict(w=w, h=h, aspect=asp, vcodec=v.get("codec_name"), pix=v.get("pix_fmt"),
                fps=round(float(n) / float(d or 1), 3) if float(d or 1) else 0, acodec=au.get("codec_name"),
                dur=float(j.get("format", {}).get("duration", 0) or 0), mb=os.path.getsize(p) / 1e6)


def loudness(p):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", p, "-af", "ebur128", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", err)
    return float(m[-1]) if m else None


def lang_of(path):
    for part in reversed(path.split(os.sep)):
        for tok in re.split(r"[_\-. ]+", part):
            if tok in LANGS:
                return tok
    return ""


def check(info, spec, lufs):
    fails, warns = [], []
    if spec["aspects"] and info["aspect"] not in spec["aspects"]:
        fails.append(f"aspect {info['aspect']} not accepted (wants {', '.join(sorted(spec['aspects']))})")
    if spec["max_s"] and info["dur"] > spec["max_s"]:
        fails.append(f"duration {info['dur']:.1f}s over {spec['max_s']}s")
    if spec["max_mb"] and info["mb"] > spec["max_mb"]:
        fails.append(f"size {info['mb']:.0f} MB over {spec['max_mb']} MB")
    if info["vcodec"] not in spec["codecs"]:
        fails.append(f"video codec {info['vcodec']} (wants {', '.join(sorted(spec['codecs']))})")
    if not info["acodec"]:
        warns.append("no audio track")
    elif info["acodec"] != "aac" and spec["lufs"]:
        warns.append(f"audio codec {info['acodec']} (platforms expect aac)")
    if info["pix"] and info["pix"] not in ("yuv420p", "yuvj420p") and spec["lufs"]:
        warns.append(f"pixel format {info['pix']} (platforms expect yuv420p)")
    if info["fps"] > 60:
        warns.append(f"{info['fps']} fps (over 60)")
    if min(info["w"], info["h"]) < 1080 and spec["lufs"]:
        warns.append(f"{info['w']}x{info['h']} is below 1080 on the short side")
    if lufs is not None and spec["lufs"] and abs(lufs - spec["lufs"]) > 2:
        warns.append(f"loudness {lufs:.1f} LUFS (target about {spec['lufs']})")
    return fails, warns


def private_hashes(project):
    idx = os.path.join(project, "01_REFERENCES", "REFERENCES_INDEX.csv")
    if not os.path.exists(idx):
        return {}
    with open(idx, newline="") as f:
        return {r["hash"]: r["id"] for r in csv.DictReader(f) if r["origin"] in ("EXTERNAL", "PERSONAL")}


def find_side(src, exts):
    stem = os.path.splitext(src)[0]
    for e in exts:
        hits = glob.glob(glob.escape(stem) + e) + glob.glob(glob.escape(stem) + "*" + e)
        if hits:
            return sorted(hits)[0]
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project", required=True)
    ap.add_argument("--target", required=True, choices=sorted(SPECS))
    ap.add_argument("--client", default="")
    ap.add_argument("--files", nargs="*", default=[])
    ap.add_argument("--from-final", help="Category/NN-Title inside 05_FINAL_OUTPUTS (or FINAL_OUTPUTS)")
    ap.add_argument("--lang", help="only this language")
    ap.add_argument("--version", type=int, default=1)
    ap.add_argument("--zip", action="store_true"); ap.add_argument("--loudness", action="store_true")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    P = os.path.abspath(a.project)
    spec = SPECS[a.target]
    files = [os.path.abspath(f) for f in a.files]
    if a.from_final:
        for base in ("05_FINAL_OUTPUTS", "FINAL_OUTPUTS"):
            d = os.path.join(P, base, a.from_final)
            if os.path.isdir(d):
                files += sorted(os.path.join(dp, f) for dp, dns, fs in os.walk(d) for f in fs
                                if os.path.splitext(f)[1].lower() in VIDEO and "_previous" not in dp
                                and not f.startswith("."))   # skip hidden and macOS "._" metadata files
                break
        else:
            sys.exit(f"not found: {a.from_final}")
    if a.lang:
        files = [f for f in files if lang_of(f) == a.lang.upper()]
    if not files:
        sys.exit("no files")

    tag = clean(a.target) + (f"_{clean(a.client)}" if a.client else "")
    out = os.path.join(P, "06_DELIVERY", f"{time.strftime('%Y-%m-%d')}_{tag}")
    private = private_hashes(P)
    rows, blocked = [], False
    for f in files:
        info = probe(f)
        lufs = loudness(f) if a.loudness else None
        fails, warns = check(info, spec, lufs)
        if qhash(f) in private:
            fails.append(f"is private reference {private[qhash(f)]} (EXTERNAL/PERSONAL): never deliver")
        if a.from_final:  # the NN-Title folder, not the aspect/lang folders under it
            title = clean(re.sub(r"^\d+-", "", os.path.basename(a.from_final.rstrip("/"))))
        else:
            title = clean(os.path.splitext(os.path.basename(f))[0])
        lang = lang_of(f)
        if a.target == "client":
            name = "_".join(x for x in [clean(a.client), title, info["aspect"], lang, f"v{a.version:02d}"] if x)
        else:
            name = "_".join(x for x in [title, a.target, info["aspect"], lang] if x)
        ext = os.path.splitext(f)[1].lower()
        rows.append(dict(src=f, name=name + ext, info=info, lufs=lufs, fails=fails, warns=warns,
                         srt=find_side(f, [".srt", ".vtt"]), thumb=find_side(f, ["_thumb.jpg", "_thumb.png", ".jpg", ".png"])))
        blocked |= bool(fails)

    names = [r["name"] for r in rows]
    for r in rows:
        if names.count(r["name"]) > 1:
            r["fails"].append("two files would get the same name: give them different titles or languages"); blocked = True
    for r in rows:
        i = r["info"]
        print(f"{'FAIL' if r['fails'] else 'WARN' if r['warns'] else 'OK  '}  {r['name']}  "
              f"{i['w']}x{i['h']} {i['fps']}fps {i['vcodec']}/{i['acodec']} {i['dur']:.1f}s {i['mb']:.1f}MB"
              + (f" {r['lufs']:.1f}LUFS" if r['lufs'] is not None else ""))
        for x in r["fails"]:
            print("      FAIL", x)
        for x in r["warns"]:
            print("      warn", x)
        print(f"      captions: {os.path.basename(r['srt']) if r['srt'] else 'none'} | thumbnail: "
              f"{os.path.basename(r['thumb']) if r['thumb'] else 'auto frame (replace with a designed one)'}")
    print("package:", out)
    if not a.apply:
        print("dry run." + (" Fix the FAIL lines first." if blocked else " Re-run with --apply after the user's yes."))
        return 1 if blocked else 0
    if blocked:
        sys.exit("FAIL lines present: nothing written")
    if os.path.exists(out) and [x for x in os.listdir(out) if not x.startswith(".")]:
        sys.exit(f"{out} already exists: delivery folders are never overwritten (use --version or a later date)")
    os.makedirs(out, exist_ok=True)
    made = []
    for r in rows:
        d = os.path.join(out, r["name"]); shutil.copy2(r["src"], d); made.append(d)
        stem = os.path.splitext(d)[0]
        if r["srt"]:
            c = stem + os.path.splitext(r["srt"])[1]; shutil.copy2(r["srt"], c); made.append(c)
        t = stem + "_thumb.jpg"
        if r["thumb"] and r["thumb"].lower().endswith((".jpg", ".jpeg")):
            shutil.copy2(r["thumb"], t)
        else:
            src = r["thumb"] or r["src"]
            subprocess.run(["ffmpeg", "-y", "-v", "error"] + ([] if r["thumb"] else ["-ss", f"{r['info']['dur'] / 3:.2f}"])
                           + ["-i", src, "-frames:v", "1", "-q:v", "2", t])
        if os.path.exists(t):
            made.append(t)
    with open(os.path.join(out, "DELIVERY_NOTE.md"), "w") as f:
        f.write(f"# Delivery: {tag}\n\nDate: {time.strftime('%Y-%m-%d')}  \nTarget: {a.target}  \nFiles: {len(rows)}\n\n")
        f.write("| File | Size | Aspect | FPS | Codec | Duration | Captions | Notes |\n|---|---|---|---|---|---|---|---|\n")
        for r in rows:
            i = r["info"]
            f.write(f"| {r['name']} | {i['w']}x{i['h']} | {i['aspect']} | {i['fps']} | {i['vcodec']}/{i['acodec']} | "
                    f"{i['dur']:.1f}s | {'yes' if r['srt'] else 'no'} | {'; '.join(r['warns']) or '-'} |\n")
        f.write("\nVerify with: `shasum -a 256 -c CHECKSUMS.sha256`\n")
    with open(os.path.join(out, "CHECKSUMS.sha256"), "w") as f:
        for m in sorted(made):
            f.write(f"{sha256(m)}  {os.path.basename(m)}\n")
    if a.zip:
        z = out + ".zip"
        with zipfile.ZipFile(z, "w", zipfile.ZIP_STORED) as zf:
            for fn in sorted(x for x in os.listdir(out) if not x.startswith(".")):
                zf.write(os.path.join(out, fn), os.path.join(os.path.basename(out), fn))
        print("zip:", z)
    print(f"written {len(made)} files + DELIVERY_NOTE.md + CHECKSUMS.sha256 in {out}")


if __name__ == "__main__":
    sys.exit(main())
