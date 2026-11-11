#!/usr/bin/env python3
"""Copy generated material into an editor-ready bin tree (originals untouched).

    EDIT/<Project>/
      00_TIMELINES/   cut plans, EDL, FCPXML, XML, Resolve/Premiere project exports
      01_VIDEO/<NN_Group>/<Group>_<take>.mp4    generated clips, grouped by scene/shot
      02_STILLS/<NN_Group>/                     frames, keyframes, plates
      03_AUDIO/{MUSIC,VO,DIALOGUE,SFX,OTHER}/
      04_GFX/         titles, logos, overlays, lower thirds, alpha renders
      05_LUTS/        .cube / .3dl
      06_DOCS/        prompts, shot lists, notes
      EDIT_MANIFEST.csv  bin file -> source file, size, fps, resolution, duration

Dry run by default; --apply copies. Never moves, overwrites or deletes.

  edit_bins.py --project "Promo_Rise" --edit-root "<project>/EDIT" --src "<project>/generated" \
      [--src "<dir>=S03"] [--order shotlist.txt] [--apply] [--link]
"""
import argparse, csv, hashlib, json, os, re, shutil, subprocess, sys, time
from collections import Counter, defaultdict

VIDEO = {".mp4", ".mov", ".m4v", ".webm", ".mkv", ".mxf"}
IMAGE = {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff", ".exr", ".dpx", ".heic"}
AUDIO = {".wav", ".mp3", ".aif", ".aiff", ".m4a", ".flac", ".ogg"}
GFX_EXT = {".svg", ".psd", ".ai", ".eps", ".aep", ".mogrt"}
LUT = {".cube", ".3dl", ".lut"}
TIMELINE = {".edl", ".fcpxml", ".xml", ".drp", ".prproj", ".otio", ".aaf"}
DOCS = {".txt", ".md", ".csv", ".json", ".pdf", ".docx"}
SKIP_RE = re.compile(r"^(_|\.)|previous|rejected|reject|tmp|temp|cache|proxy|proxies|backup|trash", re.I)
GFX_RE = re.compile(r"title|logo|lower|overlay|gfx|graphic|caption|subtitle|endcard|end_card|alpha|watermark", re.I)
TIMELINE_JSON_RE = re.compile(r"cutplan|cut_plan|timeline|edl|cues|dialogue_cut", re.I)
AUDIO_KIND = [("VO", re.compile(r"\bvo\b|voice|narrat|voiceover|tts", re.I)),
              ("DIALOGUE", re.compile(r"dialog|dialogue|line_|lipsync|speech", re.I)),
              ("MUSIC", re.compile(r"music|song|track|bgm|score|suno|beat|theme", re.I)),
              ("SFX", re.compile(r"sfx|foley|whoosh|impact|ambien|room_?tone|fx_", re.I))]
SHOT_RE = re.compile(r"(?<![A-Za-z0-9])((?:SC|SH|SHOT|SCENE|EP|S|K|B|P|A|D)[_\-]?\d{1,4}[a-z]?)(?![0-9])", re.I)
TAKE_RE = re.compile(r"(?:take|_t|_v|ver)[_\-]?(\d{1,3})", re.I)
LEAD_RE = re.compile(r"^(\d{1,3})[_\-]([A-Za-z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)*)")
HINTS = {}
HASHY = re.compile(r"^[0-9a-f]{16,}|[0-9a-f]{8}-[0-9a-f]{4}-", re.I)
COLS = ["status", "bin", "group", "dest_name", "kind", "w", "h", "fps", "duration", "size", "src", "dest", "note"]


def clean(s):
    s = re.sub(r"[^\w\-.]+", "_", s).strip(" ._")
    return re.sub(r"_+", "_", s)


def quick_hash(p):
    h, size = hashlib.sha1(), os.path.getsize(p)
    with open(p, "rb") as f:
        h.update(f.read(1 << 20))
        if size > 2 << 20:
            f.seek(-(1 << 20), 2); h.update(f.read(1 << 20))
    return f"{size}:{h.hexdigest()}"


def probe(p):
    try:
        j = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                       "stream=width,height,r_frame_rate:format=duration", "-of", "json", p],
                                      capture_output=True, text=True, timeout=60).stdout or "{}")
        st = (j.get("streams") or [{}])[0]
        n, _, d = (st.get("r_frame_rate") or "0/1").partition("/")
        fps = round(float(n) / float(d or 1), 3) if float(d or 1) else 0
        return st.get("width", ""), st.get("height", ""), fps, round(float(j.get("format", {}).get("duration", 0) or 0), 2)
    except Exception:
        return "", "", "", ""


def kind_of(path):
    fn = os.path.basename(path); ext = os.path.splitext(fn)[1].lower()
    if ext in LUT: return "05_LUTS", "lut"
    if ext in TIMELINE: return "00_TIMELINES", "timeline"
    if ext == ".json" and TIMELINE_JSON_RE.search(fn): return "00_TIMELINES", "timeline"
    if ext in GFX_EXT: return "04_GFX", "gfx"
    if ext in AUDIO:
        for name, rx in AUDIO_KIND:
            if rx.search(path): return f"03_AUDIO/{name}", "audio"
        return "03_AUDIO/OTHER", "audio"
    if ext in VIDEO: return ("04_GFX", "gfx") if GFX_RE.search(fn) else ("01_VIDEO", "video")
    if ext in IMAGE: return ("04_GFX", "gfx") if GFX_RE.search(fn) else ("02_STILLS", "still")
    if ext in DOCS: return "06_DOCS", "doc"
    return None, None


def group_of(src_root, forced, path):
    if forced:
        return clean(forced)
    rel = os.path.relpath(path, src_root).split(os.sep)
    m = LEAD_RE.match(rel[-1])  # 01_BRANDNAME_take.mp4 -> group BRANDNAME, edit position 1
    if m and not SHOT_RE.fullmatch(m.group(2)):
        g = clean(m.group(2)).upper()
        HINTS.setdefault(g, int(m.group(1)))
        return g
    for part in [os.path.splitext(rel[-1])[0]] + rel[-2::-1]:
        m = SHOT_RE.search(part)
        if m and not HASHY.match(part):
            return m.group(1).upper().replace("-", "_")
    return clean(rel[-2]) if len(rel) > 1 else clean(os.path.basename(src_root)) or "UNSORTED"


def nat(s):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", s)]


def plan(sources, edit_root, order_file, include_skipped):
    order = []
    if order_file:
        order = [l.strip().upper() for l in open(order_file) if l.strip() and not l.startswith("#")]
    rows, seen = [], {}
    for spec in sources:
        src, _, forced = spec.partition("=")
        src = os.path.abspath(src)
        for dp, dns, fns in os.walk(src):
            if os.path.abspath(dp).startswith(edit_root):
                dns[:] = []; continue
            dns.sort(key=nat)
            for fn in sorted(fns, key=nat):
                p = os.path.join(dp, fn)
                b, kind = kind_of(p)
                if not b or fn.startswith("."):
                    continue
                rel = os.path.relpath(p, src).split(os.sep)
                bad = next((d for d in rel if SKIP_RE.search(d)), None)
                r = dict(status="plan", bin=b, kind=kind, group="", dest_name="", w="", h="", fps="", duration="",
                         size=os.path.getsize(p), src=p, dest="", note="", mtime=os.path.getmtime(p))
                if bad and not include_skipped:
                    r.update(status="skip", note=f"skipped: '{bad}'"); rows.append(r); continue
                r["hash"] = quick_hash(p)
                if r["hash"] in seen:
                    r.update(status="dup", note=f"same file as {seen[r['hash']]}"); rows.append(r); continue
                seen[r["hash"]] = p
                if kind in ("video", "still") and forced and GFX_RE.fullmatch(forced.split("/")[0]):
                    r["bin"], r["kind"], kind = "04_GFX", "gfx", "gfx"   # DIR=GFX (or LOGO, TITLE...) files are graphics
                if kind in ("video", "still"):
                    r["group"] = group_of(src, forced, p)
                if kind in ("video", "gfx") and os.path.splitext(fn)[1].lower() in VIDEO:
                    r["w"], r["h"], r["fps"], r["duration"] = probe(p)
                rows.append(r)
    # group folder numbering: shot list order first, then natural order
    groups = sorted({r["group"] for r in rows if r["group"]}, key=lambda g: (g not in order, order.index(g) if g in order else 0,
                                                                   HINTS.get(g, 10 ** 6), nat(g)))
    gname = {g: f"{i:02d}_{g}" for i, g in enumerate(groups, 1)}
    # take numbers inside a group: by explicit take/version token, then by creation time
    takes = defaultdict(list)
    for r in rows:
        if r["group"] and r["status"] == "plan":
            takes[(r["bin"], r["group"])].append(r)
    for (b, g), items in takes.items():
        items.sort(key=lambda r: (int(TAKE_RE.search(os.path.basename(r["src"])).group(1))
                                  if TAKE_RE.search(os.path.basename(r["src"])) else 999, r["mtime"]))
        for i, r in enumerate(items, 1):
            stem = os.path.splitext(os.path.basename(r["src"]))[0]
            readable = "" if HASHY.match(stem) else "_" + clean(stem)[:60]
            stamp = time.strftime("%m%d-%H%M", time.localtime(r["mtime"]))
            r["dest_name"] = f"{g}_take{i:02d}{readable}_{stamp}{os.path.splitext(r['src'])[1].lower()}"
    for r in rows:
        if r["status"] != "plan":
            continue
        name = r["dest_name"] or clean(os.path.basename(r["src"]))
        r["dest_name"] = name
        r["dest"] = os.path.join(edit_root, r["bin"], gname[r["group"]], name) if r["group"] else os.path.join(edit_root, r["bin"], name)
    # collisions and what is already there
    taken = {}
    for r in rows:
        if r["status"] != "plan":
            continue
        d, n = r["dest"], 2
        base, ext = os.path.splitext(d)
        while d in taken:
            d = f"{base}__{n}{ext}"; n += 1
        taken[d] = 1; r["dest"] = d
        if os.path.exists(d):
            r["status"] = "same" if quick_hash(d) == r["hash"] else "conflict"
            if r["status"] == "conflict":
                r["note"] = "different file already in the bin; not overwritten"
        else:
            r["status"] = "new"
    return rows


def warn_formats(rows):
    vids = [r for r in rows if r["kind"] == "video" and r["status"] in ("new", "same") and r["fps"]]
    if not vids:
        return []
    fmt = Counter((r["w"], r["h"], r["fps"]) for r in vids)
    main = fmt.most_common(1)[0][0]
    return [f"FORMAT {r['w']}x{r['h']}@{r['fps']} differs from main {main[0]}x{main[1]}@{main[2]}: {r['src']}"
            for r in vids if (r["w"], r["h"], r["fps"]) != main]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project", required=True)
    ap.add_argument("--edit-root", required=True, help="folder that holds EDIT trees, e.g. <project>/EDIT")
    ap.add_argument("--src", action="append", required=True, help="source folder, optionally DIR=Group (repeatable)")
    ap.add_argument("--order", help="text file: one group/shot code per line, in edit order")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--link", action="store_true", help="hard-link instead of copy (same volume only, saves space)")
    ap.add_argument("--include-skipped", action="store_true")
    a = ap.parse_args()

    root = os.path.join(os.path.abspath(a.edit_root), clean(a.project))
    rows = plan(a.src, root, a.order, a.include_skipped)
    os.makedirs(root, exist_ok=True)   # the plan always lives in the project's bin root, dry run or not
    plan_path = os.path.join(root, f"_bins_plan_{clean(a.project)}.csv")
    os.makedirs(os.path.dirname(plan_path), exist_ok=True)
    with open(plan_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS, extrasaction="ignore"); w.writeheader(); w.writerows(rows)

    print("status:", dict(Counter(r["status"] for r in rows)))
    tree = Counter(os.path.relpath(os.path.dirname(r["dest"]), root) for r in rows if r["status"] in ("new", "same", "conflict"))
    for k in sorted(tree, key=nat):
        print(f"  {k}: {tree[k]}")
    for line in warn_formats(rows)[:20]:
        print(" ", line)
    for r in rows:
        if r["status"] == "conflict":
            print("  CONFLICT", r["dest"])
    print("plan:", plan_path)
    if not a.apply:
        print("dry run: nothing copied. Re-run with --apply after the user's yes.")
        return
    n = 0
    for r in rows:
        if r["status"] != "new":
            continue
        os.makedirs(os.path.dirname(r["dest"]), exist_ok=True)
        if a.link:
            try:
                os.link(r["src"], r["dest"])
            except OSError:
                shutil.copy2(r["src"], r["dest"])
        else:
            shutil.copy2(r["src"], r["dest"])
        r["status"] = "copied"; n += 1
    man = os.path.join(root, "EDIT_MANIFEST.csv")
    old = []
    if os.path.exists(man):
        with open(man, newline="") as f:
            old = [x for x in csv.DictReader(f) if x["dest"] not in {r["dest"] for r in rows}]
    with open(man, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS, extrasaction="ignore"); w.writeheader()
        w.writerows(old + [r for r in rows if r["status"] in ("copied", "same")])
    # orphans: files in the bins whose source is gone (reported, never deleted)
    known = {r["dest"] for r in rows} | {x["dest"] for x in old}
    orphans = [os.path.join(dp, f) for dp, _, fs in os.walk(root) for f in fs
               if not f.startswith((".", "_bins_plan")) and f != "EDIT_MANIFEST.csv" and os.path.join(dp, f) not in known]
    print(f"copied: {n}. Manifest: {man}")
    for o in orphans[:20]:
        print("  NOT FROM ANY SOURCE (left in place):", o)


if __name__ == "__main__":
    sys.exit(main())
