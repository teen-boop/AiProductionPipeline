#!/usr/bin/env python3
"""Sort a project's reference images into a clean, indexed folder structure.

--scan   list every image in --src with its size, so each can be looked at and given a role:
         organize_refs.py --scan --src references/_inbox

Sort     copy (or --move) the files according to a mapping and write the index:
         organize_refs.py --src references/_inbox --dest references --map mapping.json [--move]

mapping.json — a list, one entry per file:
  [{"file": "IMG_0412.png", "category": "Characters", "name": "hero", "label": "age_39_bust", "note": "main character"},
   {"file": "dock.jpg",     "category": "Locations",  "name": "harbour_dock", "label": "master_wide"},
   {"file": "ship.png",     "category": "Props",      "name": "liner", "label": "side_view"}]
Categories: Characters, Locations, Props, Style, Recreate (any other name also works).
Result: <dest>/<Category>/<name>/NN_<label>.<ext>, plus <dest>/INDEX.md and <dest>/index.json.
Requires Pillow (only for --scan sizes).
"""
import argparse, json, os, re, shutil

IMG = (".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff", ".heic")


def slug(s):
    return re.sub(r"[^A-Za-z0-9._-]+", "_", s.strip()).strip("_") or "item"


def scan(src):
    try:
        from PIL import Image
    except ImportError:
        Image = None
    files = sorted(f for f in os.listdir(src) if f.lower().endswith(IMG) and not f.startswith("._"))
    for f in files:
        size = ""
        if Image:
            try:
                with Image.open(os.path.join(src, f)) as im:
                    size = f"{im.size[0]}x{im.size[1]}"
            except Exception:
                size = "?"
        print(f"{f}\t{size}")
    print(f"{len(files)} image(s)")


def sort(src, dest, mapping, move):
    entries = json.load(open(mapping, encoding="utf-8"))
    index, counters = [], {}
    for e in entries:
        f = os.path.join(src, e["file"])
        if not os.path.exists(f):
            print("MISSING", e["file"]); continue
        cat, name = slug(e["category"]), slug(e["name"])
        key = (cat, name); counters[key] = counters.get(key, 0) + 1
        ext = os.path.splitext(f)[1].lower()
        out_dir = os.path.join(dest, cat, name); os.makedirs(out_dir, exist_ok=True)
        out = os.path.join(out_dir, f"{counters[key]:02d}_{slug(e.get('label', 'ref'))}{ext}")
        (shutil.move if move else shutil.copy2)(f, out)
        index.append({"category": cat, "name": name, "label": e.get("label", ""), "path": os.path.relpath(out, dest),
                      "source": e["file"], "note": e.get("note", "")})
    json.dump(index, open(os.path.join(dest, "index.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    md = ["# Reference index", "", "Attach references by these paths. One folder per character / location / prop.", ""]
    for cat in sorted({i["category"] for i in index}):
        md += [f"## {cat}", "", "| name | file | label | note |", "|---|---|---|---|"]
        md += [f"| {i['name']} | `{i['path']}` | {i['label']} | {i['note']} |" for i in index if i["category"] == cat]
        md.append("")
    open(os.path.join(dest, "INDEX.md"), "w", encoding="utf-8").write("\n".join(md))
    print(f"{len(index)} reference(s) sorted into {dest}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True); ap.add_argument("--dest"); ap.add_argument("--map")
    ap.add_argument("--scan", action="store_true"); ap.add_argument("--move", action="store_true")
    a = ap.parse_args()
    if a.scan:
        scan(a.src)
    else:
        if not (a.dest and a.map):
            ap.error("--dest and --map are required unless --scan")
        sort(a.src, a.dest, a.map, a.move)
