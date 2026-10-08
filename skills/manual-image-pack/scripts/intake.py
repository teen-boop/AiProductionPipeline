#!/usr/bin/env python3
"""Collect the user's hand-made frames from a MANUAL GENERATION PACK into the project.

For every frame folder that has RESULT_*.png / .jpg / .jpeg / .webp files:
  1. checks the format — 16:9 within 2%; black bars on any edge are measured and,
     if thin (<= 8% of the side), cropped away and the image re-fitted to 16:9;
  2. copies each result to <job folder>/<base><k>.png (never overwrites: takes the next free k);
  3. moves the RESULT files into the frame folder's _delivered/ subfolder and appends to delivered.json;
  4. unblocks dependants: any ref_*.txt placeholder in the pack containing
     "WAITING_FOR: <this job id>#<k>" is replaced by a copy of that delivered frame.
Prints a report (delivered, auto-cropped, wrong aspect) so the frames can be QC'd before they go into the storyboard.

Usage: intake.py --pack PACK_DIR [--dry-run]
Requires Pillow.
"""
import argparse, glob, json, os, re, shutil, time
from PIL import Image

EXT = (".png", ".jpg", ".jpeg", ".webp")


def bars(im, thr=6, flat=3):
    """Edge rows/columns count as a bar only if they are BOTH near-black AND uniform —
    dark film content (shadows, night) has texture and is never cropped."""
    g = im.convert("L"); w, h = g.size
    def is_bar(vals):
        m = sum(vals) / len(vals); sd = (sum((v - m) ** 2 for v in vals) / len(vals)) ** 0.5
        return m <= thr and sd <= flat
    col = lambda x: is_bar([g.getpixel((x, y)) for y in range(0, h, 4)])
    row = lambda y: is_bar([g.getpixel((x, y)) for x in range(0, w, 4)])
    l = next((x for x in range(w // 4) if not col(x)), 0)
    r = next((x for x in range(w - 1, w * 3 // 4, -1) if not col(x)), w - 1)
    t = next((y for y in range(h // 4) if not row(y)), 0)
    b = next((y for y in range(h - 1, h * 3 // 4, -1) if not row(y)), h - 1)
    return l, t, r + 1, b + 1


def fix(path):
    im = Image.open(path).convert("RGB"); w, h = im.size
    l, t, r, b = bars(im); notes = []
    if (l, t, r, b) != (0, 0, w, h):
        if max(l, w - r) <= 0.08 * w and max(t, h - b) <= 0.08 * h:
            im = im.crop((l, t, r, b)); notes.append(f"bars cropped ({l},{t},{w - r},{h - b}px)")
        else:
            notes.append("LARGE BARS — check by eye")
    w, h = im.size; target = 16 / 9
    if abs(w / h - target) / target > 0.02:
        if w / h > target:
            nw = round(h * target); x = (w - nw) // 2; im = im.crop((x, 0, x + nw, h))
        else:
            nh = round(w / target); y = (h - nh) // 2; im = im.crop((0, y, w, y + nh))
        notes.append("re-fitted to 16:9")
    return im, notes


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--pack", required=True); ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(); report = []
    for jf in sorted(glob.glob(f"{a.pack}/**/job.json", recursive=True)):
        d = os.path.dirname(jf); job = json.load(open(jf, encoding="utf-8"))
        results = sorted(f for f in os.listdir(d) if f.upper().startswith("RESULT") and f.lower().endswith(EXT) and not f.startswith("._"))
        if not results:
            continue
        os.makedirs(job["folder"], exist_ok=True)
        log_path = f"{d}/delivered.json"; log = json.load(open(log_path)) if os.path.exists(log_path) else []
        for f in results:
            m = re.search(r"(\d+)", f); rn = int(m.group(1)) if m else 1; k = rn
            dst = f"{job['folder']}/{job['base']}{k}.png"
            while os.path.exists(dst):
                k += 1; dst = f"{job['folder']}/{job['base']}{k}.png"
            im, notes = fix(f"{d}/{f}")
            report.append((os.path.basename(d), f, os.path.basename(dst), notes))
            if a.dry_run:
                continue
            im.save(dst)
            os.makedirs(f"{d}/_delivered", exist_ok=True); shutil.move(f"{d}/{f}", f"{d}/_delivered/{f}")
            log.append({"result": f, "dest": dst, "notes": notes, "time": time.strftime("%Y-%m-%d %H:%M")})
            for ph in glob.glob(f"{a.pack}/**/ref_*.txt", recursive=True):
                if f"WAITING_FOR: {job['id']}#{rn}" in open(ph, encoding="utf-8").read():
                    i = re.match(r"ref_(\d+)_", os.path.basename(ph)).group(1)
                    shutil.copy(dst, os.path.join(os.path.dirname(ph), f"ref_{i}_{os.path.basename(dst)}")); os.remove(ph)
        if not a.dry_run:
            json.dump(log, open(log_path, "w"), ensure_ascii=False, indent=1)
    for folder, f, dst, notes in report:
        print(f"{folder}/{f} -> {dst}" + (f"   [{'; '.join(notes)}]" if notes else ""))
    print(f"{len(report)} result(s) {'would be ' if a.dry_run else ''}delivered.")


if __name__ == "__main__":
    main()
