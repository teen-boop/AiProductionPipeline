#!/usr/bin/env python3
"""Understand and organize a project's references.

  01_REFERENCES/
    EXTERNAL/{FILM,ART,ADS,PHOTO,MOTION,OTHER}/R012_FILM_<name>.jpg     found material: look only
    INTERNAL/{CHARACTERS,LOCATIONS,PROPS,STYLE}/{LOCKED,CANDIDATES}/R020_CHARACTERS_<name>.png
    PROMPTS/R031_PROMPT_<name>.md
    PERSONAL/  (real people: NOT copied; indexed where they already are)
    REFERENCES_INDEX.csv   one row per reference: id, origin, class, state, role, used_in, source, notes
    _sheets/   contact sheets for classifying by eye

Commands
  scan   --project P --src DIR [--src DIR=EXTERNAL/FILM ...]   -> _refs_plan.csv + contact sheets (no copying)
  apply  --project P [--move]                                   -> copy per the (edited) plan, update the index
  use    --project P --id R012 --shot S03 [--role "face and outfit only"]
  lock   --project P --id R020                                  -> CANDIDATES -> LOCKED (copy, old stays)
  leak   --project P --path DIR                                 -> fail if any EXTERNAL/PERSONAL file is inside DIR
"""
import argparse, csv, hashlib, os, re, shutil, subprocess, sys, time

IMAGE = {".png", ".jpg", ".jpeg", ".webp", ".heic", ".tif", ".tiff", ".gif", ".avif"}
VIDEO = {".mp4", ".mov", ".m4v", ".webm"}
TEXT = {".md", ".txt"}
INTERNAL_CLASSES = ["CHARACTERS", "LOCATIONS", "PROPS", "STYLE"]
EXTERNAL_CLASSES = ["FILM", "ART", "ADS", "PHOTO", "MOTION", "OTHER"]
INDEX_COLS = ["id", "origin", "class", "state", "file", "original", "hash", "w", "h", "role", "used_in", "source_url",
              "author", "license", "notes", "added"]
PLAN_COLS = ["id", "origin", "class", "state", "confidence", "why", "original", "w", "h", "role", "source_url", "notes", "hash", "sheet"]

PERSONAL_RE = re.compile(r"(^|[_\-\s/])(img_\d{3,}|dsc[_f]?\d+|pxl_\d+|selfie|headshot|passport|my_?face|real_?photo|"
                         r"photo_of_me|face_?photo|me_|portrait_real|voice_?sample)", re.I)
EXT_HINT = re.compile(r"pinterest|pinimg|screenshot|screen_shot|still|frame_from|film_?still|criterion|imdb|behance|"
                      r"artstation|dribbble|_sl\d+_|amazon|instagram|youtube|vimeo|ad_ref|competitor|moodboard|inspo", re.I)
HASH_NAME = re.compile(r"^[0-9a-f]{16,}|^[0-9a-f]{8}-[0-9a-f]{4}", re.I)
INT_HINT = re.compile(r"lovart|seedance|kling|nano_?banana|gpt_?image|higgsfield|krea|midjourney|_gen_|generated|"
                      r"character_?sheet|persona|turnaround|plate|room_?map|prop_?sheet|style_?frame|style_?card|keyframe|"
                      r"diptych|lock", re.I)
CLASS_HINT = [("CHARACTERS", re.compile(r"char|persona|face|cast|hero|actor|turnaround|outfit|wardrobe|portrait", re.I)),
              ("LOCATIONS", re.compile(r"loc|room|plate|interior|exterior|street|set_|environment|bg_|background|map", re.I)),
              ("PROPS", re.compile(r"prop|object|product|vehicle|weapon|item|robot|device", re.I)),
              ("STYLE", re.compile(r"style|look|palette|grade|lut|mood|tone|texture|lighting", re.I))]
EXT_CLASS_HINT = [("ADS", re.compile(r"\bad[s_\-]|advert|commercial|campaign|brand|competitor", re.I)),
                  ("FILM", re.compile(r"film|movie|still|scene|cinema|criterion|shot_from", re.I)),
                  ("ART", re.compile(r"art|paint|illustr|poster|artist|artstation|behance", re.I)),
                  ("PHOTO", re.compile(r"photo|unsplash|editorial", re.I))]
LOCK_HINT = re.compile(r"locked|approved|final|canon|master|_ok\b", re.I)


def clean(s, n=48):
    return re.sub(r"_+", "_", re.sub(r"[^\w\-]+", "_", s)).strip("_")[:n]


def qhash(p):
    h, size = hashlib.sha1(), os.path.getsize(p)
    with open(p, "rb") as f:
        h.update(f.read(1 << 20))
        if size > 2 << 20:
            f.seek(-(1 << 20), 2); h.update(f.read(1 << 20))
    return f"{size}:{h.hexdigest()}"


def dims(p):
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                              "-of", "csv=p=0", p], capture_output=True, text=True, timeout=30).stdout.strip()
        w, h = out.split("\n")[0].split(",")[:2]
        return int(w), int(h)
    except Exception:
        return "", ""


def camera_make(p):
    """Phone/camera photos carry a camera make: strong sign of a real photo (macOS Spotlight metadata)."""
    try:
        out = subprocess.run(["mdls", "-raw", "-name", "kMDItemAcquisitionMake", p], capture_output=True, text=True, timeout=10).stdout
        return "" if out.strip() in ("(null)", "") else out.strip()
    except Exception:
        return ""


def sidecar_text(p):
    stem = os.path.splitext(p)[0]
    for ext in (".txt", ".md", ".url", ".json"):
        if os.path.exists(stem + ext) and stem + ext != p:
            try:
                return open(stem + ext, errors="ignore").read(4000)
            except Exception:
                pass
    return ""


def guess(path, forced, gen_hashes, h):
    fn, ext = os.path.basename(path), os.path.splitext(path)[1].lower()
    low = path.lower()
    if forced:
        parts = forced.upper().split("/")
        origin = parts[0]; cls = parts[1] if len(parts) > 1 else ("MOTION" if ext in VIDEO else "OTHER") if origin == "EXTERNAL" else "?"
        state = parts[2] if len(parts) > 2 else ("LOCKED" if LOCK_HINT.search(low) else "CANDIDATES")
        return origin, cls, state if origin == "INTERNAL" else "", "high", "forced by --src"
    if ext in TEXT:
        return "PROMPTS", "PROMPT", "", "high", "text file"
    if h in gen_hashes:
        origin, why = "INTERNAL", "listed in GENERATION_LOG"
    elif PERSONAL_RE.search(low) or (ext in IMAGE and camera_make(path)):
        return "PERSONAL", "PEOPLE", "", "medium", "camera photo or personal-photo name"
    elif INT_HINT.search(low):
        origin, why = "INTERNAL", "generator/sheet word in name"
    elif EXT_HINT.search(low) or HASH_NAME.match(fn) or re.search(r"https?://", sidecar_text(path)):
        origin, why = "EXTERNAL", "download/hash name or source URL"
    else:
        origin, why = "?", "no clue in name: look at the sheet"
    if origin == "INTERNAL":
        cls = next((c for c, rx in CLASS_HINT if rx.search(low)), "?")
        return origin, cls, "LOCKED" if LOCK_HINT.search(low) else "CANDIDATES", "medium" if cls != "?" else "low", why
    if origin == "EXTERNAL":
        cls = "MOTION" if ext in VIDEO else next((c for c, rx in EXT_CLASS_HINT if rx.search(low)), "?")
        return origin, cls, "", "medium" if cls != "?" else "low", why
    return "?", "?", "", "low", why


def refs_root(project):
    return os.path.join(os.path.abspath(project), "01_REFERENCES")


def read_csv(p):
    if not os.path.exists(p):
        return []
    with open(p, newline="") as f:
        return list(csv.DictReader(f))


def write_csv(p, rows, cols):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(rows)


def next_id(rows):
    nums = [int(r["id"][1:]) for r in rows if re.fullmatch(r"R\d+", r.get("id", ""))]
    return (max(nums) if nums else 0) + 1


def sheets(rows, out_dir, per=12, cell=360):
    os.makedirs(out_dir, exist_ok=True)
    pics = [r for r in rows if os.path.splitext(r["original"])[1].lower() in IMAGE | VIDEO]
    for i in range(0, len(pics), per):
        batch = pics[i:i + per]
        name = f"sheet_{i // per + 1:02d}"
        args, fl = ["ffmpeg", "-y", "-v", "error"], []
        for j, r in enumerate(batch):
            src = r["original"]
            args += (["-ss", "1"] if os.path.splitext(src)[1].lower() in VIDEO else []) + ["-i", src]
            fl.append(f"[{j}:v]scale={cell}:{cell}:force_original_aspect_ratio=decrease,pad={cell}:{cell}:(ow-iw)/2:(oh-ih)/2:color=gray,setsar=1,format=rgb24[c{j}]")
        cols = 4
        while len(batch) % cols and len(batch) > cols:
            fl.append(f"color=gray:s={cell}x{cell}:d=1,format=rgb24[c{len(batch)}]"); batch = batch + [None]
        n = len(batch)
        layout = "|".join(f"{(k % cols) * cell}_{(k // cols) * cell}" for k in range(n))
        fl.append("".join(f"[c{k}]" for k in range(n)) + (f"xstack=inputs={n}:layout={layout}" if n > 1 else "null"))
        res = subprocess.run(args + ["-filter_complex", ";".join(fl), "-frames:v", "1", os.path.join(out_dir, name + ".jpg")],
                             capture_output=True, text=True)
        with open(os.path.join(out_dir, name + ".txt"), "w") as f:
            f.write("cells left to right, top to bottom\n")
            for k, r in enumerate(x for x in batch if x):
                f.write(f"{k + 1:2d}  {r['id']}  {r['origin']}/{r['class']}  {os.path.basename(r['original'])}\n")
                r["sheet"] = f"{name}#{k + 1}"
        if res.returncode:
            print("sheet failed:", name, res.stderr[-300:])


def cmd_scan(a):
    root = refs_root(a.project)
    index = read_csv(os.path.join(root, "REFERENCES_INDEX.csv"))
    known = {r["hash"]: r for r in index}
    gen_hashes = set()
    log = os.path.join(os.path.abspath(a.project), "03_GENERATED", "GENERATION_LOG.jsonl")
    if os.path.exists(log):
        import json
        for line in open(log):
            try:
                gen_hashes.add(json.loads(line).get("hash", ""))
            except Exception:
                pass
    rows, seen, nid = [], set(), next_id(index)
    for spec in a.src:
        src, _, forced = spec.partition("=")
        for dp, dns, fns in os.walk(os.path.abspath(src)):
            dns[:] = sorted(d for d in dns if not d.startswith((".", "_sheets")))
            for fn in sorted(fns):
                p = os.path.join(dp, fn)
                ext = os.path.splitext(fn)[1].lower()
                if fn.startswith(".") or ext not in IMAGE | VIDEO | TEXT or fn == "REFERENCES_INDEX.csv":
                    continue
                h = qhash(p)
                if h in seen:
                    continue
                seen.add(h)
                if h in known:
                    continue  # already organized
                origin, cls, state, conf, why = guess(p, forced, gen_hashes, h)
                w, hh = dims(p) if ext in IMAGE | VIDEO else ("", "")
                src_url = (re.search(r"https?://\S+", sidecar_text(p)) or [""])[0]
                rows.append(dict(id=f"R{nid:03d}", origin=origin, **{"class": cls}, state=state, confidence=conf, why=why,
                                 original=p, w=w, h=hh, role="", source_url=src_url, notes="", hash=h, sheet=""))
                nid += 1
    sheets(rows, os.path.join(root, "_sheets"))
    plan = os.path.join(root, "_refs_plan.csv")
    write_csv(plan, rows, PLAN_COLS)
    from collections import Counter
    print("new references:", len(rows), "| already indexed:", len(index))
    for k, n in sorted(Counter(f"{r['origin']}/{r['class']}" + (f"/{r['state']}" if r['state'] else "") for r in rows).items()):
        print(f"  {k}: {n}")
    unsure = [r for r in rows if "?" in (r["origin"], r["class"])]
    print(f"to decide by eye: {len(unsure)} (see {os.path.join(root, '_sheets')})")
    print("plan:", plan)


def dest_for(root, r):
    ext = os.path.splitext(r["original"])[1].lower()
    stem = os.path.splitext(os.path.basename(r["original"]))[0]
    tail = "" if HASH_NAME.match(stem) else "_" + clean(stem)
    if r["origin"] == "EXTERNAL":
        return os.path.join(root, "EXTERNAL", r["class"], f"{r['id']}_{r['class']}{tail}{ext}")
    if r["origin"] == "INTERNAL":
        return os.path.join(root, "INTERNAL", r["class"], r["state"] or "CANDIDATES", f"{r['id']}_{r['class']}{tail}{ext}")
    if r["origin"] == "PROMPTS":
        return os.path.join(root, "PROMPTS", f"{r['id']}_PROMPT{tail}{ext}")
    return ""


def cmd_apply(a):
    root = refs_root(a.project)
    plan = read_csv(os.path.join(root, "_refs_plan.csv"))
    idx_path = os.path.join(root, "REFERENCES_INDEX.csv")
    index = read_csv(idx_path)
    todo = [r for r in plan if r["origin"] not in ("?", "SKIP") and r["class"] != "?"]
    left = [r for r in plan if r not in todo]
    bad = [r for r in todo if (r["origin"] == "INTERNAL" and r["class"] not in INTERNAL_CLASSES) or
           (r["origin"] == "EXTERNAL" and r["class"] not in EXTERNAL_CLASSES)]
    if bad:
        for r in bad:
            print("INVALID class", r["origin"], r["class"], r["original"])
        return 1
    n = 0
    for r in todo:
        row = {k: r.get(k, "") for k in INDEX_COLS}
        row["added"] = time.strftime("%Y-%m-%d")
        if r["origin"] == "PERSONAL":
            row["file"] = r["original"]  # stays where it is, never copied
            row["role"] = row["role"] or "identity only; private"
        else:
            d = dest_for(root, r)
            os.makedirs(os.path.dirname(d), exist_ok=True)
            if not os.path.exists(d):
                (shutil.move if a.move else shutil.copy2)(r["original"], d); n += 1
            row["file"] = os.path.relpath(d, root)
            if r["origin"] == "EXTERNAL":
                row["role"] = row["role"] or "look only: palette, light, composition. Never its people, logos or text"
        index.append(row)
    write_csv(idx_path, index, INDEX_COLS)
    write_csv(os.path.join(root, "_refs_plan.csv"), left, PLAN_COLS)
    print(f"{'moved' if a.move else 'copied'} {n}; indexed {len(todo)}; still undecided {len(left)}. Index: {idx_path}")


def find(index, rid):
    r = next((x for x in index if x["id"] == rid), None)
    if not r:
        sys.exit(f"no reference {rid}")
    return r


def cmd_use(a):
    p = os.path.join(refs_root(a.project), "REFERENCES_INDEX.csv"); index = read_csv(p); r = find(index, a.id)
    shots = [s for s in r["used_in"].split(";") if s] + [a.shot]
    r["used_in"] = ";".join(dict.fromkeys(shots))
    if a.role:
        r["role"] = a.role
    write_csv(p, index, INDEX_COLS); print(a.id, "used in", r["used_in"], "| role:", r["role"])


def cmd_lock(a):
    root = refs_root(a.project); p = os.path.join(root, "REFERENCES_INDEX.csv"); index = read_csv(p); r = find(index, a.id)
    if r["origin"] != "INTERNAL" or r["state"] == "LOCKED":
        sys.exit("only INTERNAL candidates can be locked")
    src = os.path.join(root, r["file"])
    dst = src.replace(os.sep + "CANDIDATES" + os.sep, os.sep + "LOCKED" + os.sep)
    os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copy2(src, dst)
    r["state"], r["file"] = "LOCKED", os.path.relpath(dst, root)
    write_csv(p, index, INDEX_COLS); print("locked:", dst, "(candidate copy left in place)")


def cmd_leak(a):
    index = read_csv(os.path.join(refs_root(a.project), "REFERENCES_INDEX.csv"))
    private = {r["hash"]: r for r in index if r["origin"] in ("EXTERNAL", "PERSONAL")}
    hits, own = [], refs_root(a.project)
    for dp, dns, fns in os.walk(os.path.abspath(a.path)):
        if os.path.abspath(dp).startswith(own):  # the library itself is allowed to hold them
            dns[:] = []; continue
        for fn in fns:
            p = os.path.join(dp, fn)
            if os.path.splitext(fn)[1].lower() in IMAGE | VIDEO and not fn.startswith("."):
                h = qhash(p)
                if h in private:
                    hits.append((p, private[h]))
    for p, r in hits:
        print(f"LEAK {r['origin']} {r['id']}: {p}")
    print("leak check:", "FAIL" if hits else "OK", f"({len(private)} private references checked)")
    return 1 if hits else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    s = sp.add_parser("scan"); s.add_argument("--project", required=True); s.add_argument("--src", action="append", required=True)
    s = sp.add_parser("apply"); s.add_argument("--project", required=True); s.add_argument("--move", action="store_true")
    s = sp.add_parser("use"); s.add_argument("--project", required=True); s.add_argument("--id", required=True)
    s.add_argument("--shot", required=True); s.add_argument("--role")
    s = sp.add_parser("lock"); s.add_argument("--project", required=True); s.add_argument("--id", required=True)
    s = sp.add_parser("leak"); s.add_argument("--project", required=True); s.add_argument("--path", required=True)
    a = ap.parse_args()
    return {"scan": cmd_scan, "apply": cmd_apply, "use": cmd_use, "lock": cmd_lock, "leak": cmd_leak}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
