#!/usr/bin/env python3
"""Organize finished videos into one FINAL_OUTPUTS tree.

    FINAL_OUTPUTS/<Category>/<NN>-<Title>/<aspect>/[<LANG>]/<file>

Dry run by default: it writes a plan CSV you can edit (category, order, title, lang)
and prints a summary. Nothing is copied until --apply. Originals are never moved
unless --move is passed, and nothing is ever overwritten or deleted.

Examples
  # 1. plan (no changes)
  organize_finals.py --root "/path/project" --src "/path/project/renders"
  # several sources, one forced category, one folder forced to be a single title (series)
  organize_finals.py --root P --src P/renders --src "P/tutorials=Tutorials" --src "P/shorts=Promos/Skill_Promos_8s"
  # 2. user edits P/FINAL_OUTPUTS/_plan.csv, then
  organize_finals.py --root P --from-plan P/FINAL_OUTPUTS/_plan.csv --apply
"""
import argparse, csv, hashlib, json, os, re, shutil, subprocess, sys
from collections import Counter, defaultdict

VIDEO_EXT = {".mp4", ".mov", ".m4v", ".webm", ".mkv"}
LANGS = {"EN", "RU", "ES", "DE", "FR", "IT", "PT", "UK", "UA", "PL", "ZH", "JA", "KO", "AR", "HE", "TR", "NL"}
ASPECTS = [("16x9", 16 / 9), ("9x16", 9 / 16), ("1x1", 1.0), ("4x5", 4 / 5), ("5x4", 5 / 4),
           ("4x3", 4 / 3), ("3x4", 3 / 4), ("21x9", 2.37), ("2x1", 2.0)]
SKIP_RE = re.compile(r"^(_|\.)|previous|tmp|temp|rejected|reject|draft|wip|test|qc|working|frames|"
                     r"backup|archive|old$|proxy|proxies|cache", re.I)
NOISE_DIRS = re.compile(r"^(final|finals|render|renders|export|exports|out|output|outputs|delivery|"
                        r"master|masters|v\d+)$", re.I)
ORDER_PREFIX = re.compile(r"^(?:s|ep|e|video|part|ch|v)?(\d+)[_\-. ]+", re.I)
COLS = ["status", "category", "order", "title", "aspect", "lang", "filename", "duration", "size", "src", "dest", "note"]


def clean(s):
    s = re.sub(r"[^\w\-. ]+", "_", s).strip(" ._")
    return re.sub(r"_+", "_", s.replace(" ", "_"))


def strip_order(s):
    m = ORDER_PREFIX.match(s)
    return (s[m.end():], int(m.group(1))) if m else (s, None)


def aspect_label(w, h):
    if not w or not h:
        return "unknown"
    r = w / h
    name, val = min(ASPECTS, key=lambda a: abs(a[1] - r))
    return name if abs(val - r) / val < 0.04 else f"other_{w}x{h}"


def probe(path):
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                              "stream=width,height:stream_side_data=rotation:stream_tags=rotate:format=duration",
                              "-of", "json", path], capture_output=True, text=True, timeout=60).stdout
        j = json.loads(out or "{}")
        st = (j.get("streams") or [{}])[0]
        w, h = st.get("width"), st.get("height")
        rot = st.get("tags", {}).get("rotate") or next(
            (sd.get("rotation") for sd in st.get("side_data_list", []) if "rotation" in sd), 0)
        if w and h and abs(int(float(rot or 0))) % 180 == 90:
            w, h = h, w
        return w, h, round(float(j.get("format", {}).get("duration", 0) or 0), 2)
    except Exception:
        return None, None, 0.0


def quick_hash(path):
    """size + sha1 of first and last MiB: fast on external drives, good enough to spot copies."""
    h = hashlib.sha1()
    size = os.path.getsize(path)
    with open(path, "rb") as f:
        h.update(f.read(1 << 20))
        if size > 2 << 20:
            f.seek(-(1 << 20), 2)
            h.update(f.read(1 << 20))
    return f"{size}:{h.hexdigest()}"


def lang_of(parts, stem):
    for p in parts:
        if p.upper() in LANGS and len(p) == 2:
            return p.upper()
    toks = re.split(r"[_\-. ]+", stem)
    for tok in toks:  # uppercase tokens only: "loop-it-forever" must not become Italian
        if len(tok) == 2 and tok.isupper() and tok in LANGS:
            return tok
    last = toks[-1] if toks else ""  # lowercase only as the final suffix: video_ru.mp4
    return last.upper() if len(last) == 2 and last.upper() in LANGS else ""


def classify(src_root, forced_cat, path):
    rel = os.path.relpath(path, src_root)
    parts = rel.split(os.sep)[:-1]
    stem = os.path.splitext(os.path.basename(path))[0]
    if forced_cat and "/" in forced_cat:  # DIR=Category/Title: the whole folder is one video or series
        cat, title = forced_cat.split("/", 1)
        return clean(cat), clean(strip_order(title)[0]), strip_order(title)[1], lang_of(parts, stem)
    if forced_cat:
        cat, rest = forced_cat, parts
    elif parts:
        cat, rest = strip_order(parts[0])[0], parts[1:]
    else:
        cat, rest = "Uncategorized", []
    title_dirs = [p for p in rest if p.upper() not in LANGS and not re.fullmatch(r"\d+x\d+", p)
                  and not NOISE_DIRS.match(p)]
    title_raw = title_dirs[0] if title_dirs else re.sub(r"[_\-. ](16x9|9x16|1x1|4x5|EN|RU)\b", "", stem, flags=re.I)
    title, hint = strip_order(title_raw)
    return clean(cat), clean(title) or "Untitled", hint, lang_of(rest, stem)


def existing_orders(final_root):
    """Keep numbers already given in FINAL_OUTPUTS: {(cat, title): order}."""
    got = {}
    if os.path.isdir(final_root):
        for cat in os.listdir(final_root):
            cdir = os.path.join(final_root, cat)
            if cat.startswith("_") or not os.path.isdir(cdir):
                continue
            for d in os.listdir(cdir):
                m = re.match(r"^(\d+)-(.+)$", d)
                if m:
                    got[(cat, m.group(2))] = int(m.group(1))
    return got


def dest_of(final_root, r, multi_lang):
    parts = [final_root, r["category"], f"{int(r['order']):02d}-{r['title']}", r["aspect"]]
    if r["lang"] and (multi_lang or r.get("force_lang")):
        parts.append(r["lang"])
    return os.path.join(*parts, r["filename"])


def finalize(rows, final_root, always_lang):
    langs = defaultdict(set)
    for r in rows:
        if r["status"] not in ("skip", "dup"):
            langs[(r["category"], r["title"])].add(r["lang"])
    taken = {}
    for r in rows:
        if r["status"] in ("skip", "dup"):
            continue
        multi = always_lang or len(langs[(r["category"], r["title"])] - {""}) > 1
        d = dest_of(final_root, r, multi)
        base, ext = os.path.splitext(d)
        n = 2
        while d in taken and taken[d] != r["hash"]:
            d = f"{base}__{n}{ext}"; n += 1
        taken[d] = r["hash"]
        r["dest"] = d
        if os.path.exists(d):
            same = quick_hash(d) == r["hash"]
            r["status"] = "same" if same else "conflict"
            r["note"] = "already there" if same else "different file already at dest; not overwritten"
        else:
            r["status"] = "new"


def build_plan(sources, final_root, include_skipped):
    rows, seen = [], {}
    for spec in sources:
        src, _, cat = spec.partition("=")
        src = os.path.abspath(src)
        for dp, dns, fns in os.walk(src):
            if os.path.abspath(dp).startswith(final_root):
                dns[:] = []; continue
            dns.sort(); fns.sort()
            for fn in fns:
                if os.path.splitext(fn)[1].lower() not in VIDEO_EXT or fn.startswith("."):
                    continue
                p = os.path.join(dp, fn)
                rel_dirs = os.path.relpath(p, src).split(os.sep)[:-1]
                bad = next((d for d in rel_dirs + [fn] if SKIP_RE.search(d)), None)
                category, title, hint, lang = classify(src, cat, p)
                w, h, dur = probe(p)
                r = dict(status="plan", category=category, order="", title=title, aspect=aspect_label(w, h),
                         lang=lang, filename=clean(os.path.splitext(fn)[0]) + os.path.splitext(fn)[1].lower(),
                         duration=dur, size=os.path.getsize(p), src=p, dest="", note="", hint=hint)
                if bad and not include_skipped:
                    r.update(status="skip", note=f"skipped: '{bad}' looks like a working/old file")
                else:
                    r["hash"] = quick_hash(p)
                    if r["hash"] in seen:
                        r.update(status="dup", note=f"same file as {seen[r['hash']]}")
                    else:
                        seen[r["hash"]] = p
                rows.append(r)
    # numbering per category: keep existing, then source hints, then alphabetical
    known = existing_orders(final_root)
    by_cat = defaultdict(dict)
    for r in rows:
        if r["status"] != "skip":
            by_cat[r["category"]].setdefault(r["title"], r["hint"])
    order = {}
    for cat, titles in by_cat.items():
        used = {v for (c, _), v in known.items() if c == cat}
        for t in titles:
            if (cat, t) in known:
                order[(cat, t)] = known[(cat, t)]
        rest = sorted((t for t in titles if (cat, t) not in order),
                      key=lambda t: (titles[t] is None, titles[t] or 0, t.lower()))
        n = 1
        for t in rest:
            while n in used:
                n += 1
            order[(cat, t)] = n; used.add(n)
    for r in rows:
        r["order"] = order.get((r["category"], r["title"]), "")
    return rows


def write_csv(path, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS + ["hash"], extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def read_csv(path):
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["category"], r["title"] = clean(r["category"]), clean(r["title"])
        r["lang"] = r["lang"].upper().strip()
        r["force_lang"] = False
        if r["status"] in ("same", "conflict", "new", "plan"):
            r["status"] = "plan"
    return rows


def write_index(final_root):
    lines = ["# FINAL OUTPUTS", "", "Generated by final-outputs-organizer. Do not edit by hand.", ""]
    for cat in sorted(os.listdir(final_root)):
        cdir = os.path.join(final_root, cat)
        if cat.startswith("_") or not os.path.isdir(cdir):
            continue
        lines.append(f"## {cat}")
        for item in sorted(os.listdir(cdir)):
            idir = os.path.join(cdir, item)
            if not os.path.isdir(idir):
                continue
            files = [os.path.relpath(os.path.join(dp, f), idir) for dp, _, fs in os.walk(idir) for f in sorted(fs)
                     if os.path.splitext(f)[1].lower() in VIDEO_EXT]
            lines.append(f"- **{item}** ({len(files)} files)")
            lines += [f"  - {f}" for f in sorted(files)]
        lines.append("")
    with open(os.path.join(final_root, "INDEX.md"), "w") as f:
        f.write("\n".join(lines))


def summary(rows):
    st = Counter(r["status"] for r in rows)
    print("status:", dict(st))
    tree = defaultdict(Counter)
    for r in rows:
        if r["status"] in ("new", "same", "conflict"):
            item = f"{int(r['order']):02d}-{r['title']}"
            parts = r["dest"].split(os.sep)
            sub = "/".join(parts[parts.index(item) + 1:-1]) if item in parts else r["aspect"]
            tree[f"{r['category']}/{item}"][sub] += 1
    for k in sorted(tree):
        print(f"  {k}: " + ", ".join(f"{a}={n}" for a, n in sorted(tree[k].items())))
    for r in rows:
        if r["status"] == "conflict" or r["aspect"].startswith(("other", "unknown")):
            print(f"  CHECK {r['status']} {r['aspect']}: {r['src']}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", required=True, help="project root; FINAL_OUTPUTS is created inside it")
    ap.add_argument("--src", action="append", default=[], help="source folder, optionally DIR=Category (repeatable)")
    ap.add_argument("--from-plan", help="use an edited plan CSV instead of scanning")
    ap.add_argument("--plan", help="where to write the plan CSV (default FINAL_OUTPUTS/_plan.csv)")
    ap.add_argument("--apply", action="store_true", help="copy files (default is dry run)")
    ap.add_argument("--move", action="store_true", help="move instead of copy (only on the user's explicit yes)")
    ap.add_argument("--always-lang", action="store_true", help="add a language folder even when a title has one language")
    ap.add_argument("--include-skipped", action="store_true", help="also take _previous/tmp/test/qc files")
    a = ap.parse_args()

    # projects made by project-scaffold use 05_FINAL_OUTPUTS; older ones FINAL_OUTPUTS
    scaffolded = os.path.isdir(os.path.join(os.path.abspath(a.root), "05_FINAL_OUTPUTS"))
    final_root = os.path.join(os.path.abspath(a.root), "05_FINAL_OUTPUTS" if scaffolded else "FINAL_OUTPUTS")
    plan_path = a.plan or os.path.join(final_root, "_plan.csv")
    if a.from_plan:
        rows = read_csv(a.from_plan)
    elif a.src:
        rows = build_plan(a.src, final_root, a.include_skipped)
    else:
        ap.error("give --src or --from-plan")
    finalize(rows, final_root, a.always_lang)
    write_csv(plan_path, rows)
    summary(rows)
    print(f"plan: {plan_path}")
    if not a.apply:
        print("dry run: nothing copied. Review the plan, then re-run with --from-plan <plan> --apply")
        return
    done = 0
    for r in rows:
        if r["status"] != "new":
            continue
        os.makedirs(os.path.dirname(r["dest"]), exist_ok=True)
        (shutil.move if a.move else shutil.copy2)(r["src"], r["dest"])
        r["status"] = "moved" if a.move else "copied"
        done += 1
    write_csv(os.path.join(final_root, "_manifest.csv"), [r for r in rows if r["status"] in ("copied", "moved", "same")])
    write_index(final_root)
    print(f"{'moved' if a.move else 'copied'}: {done}. Manifest and INDEX.md written in {final_root}")


if __name__ == "__main__":
    sys.exit(main())
