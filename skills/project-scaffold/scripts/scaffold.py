#!/usr/bin/env python3
"""Create (or complete) the standard project tree. Never deletes, never renames, never moves.

  scaffold.py --root "<drive>/PROJECTS" --name "Rise_Promo" [--type promo] [--aspects 16x9,9x16] [--langs EN,RU]
  scaffold.py --check "<drive>/PROJECTS/Rise_Promo"     # report what is missing / misplaced
"""
import argparse, json, os, re, sys, time

TREE = {
    "00_BRIEF": "Brief, script, client notes, deadlines. BRIEF.md is the source of truth for the project.",
    "01_REFERENCES/EXTERNAL": "Found material we do not own (films, artists, ads, photos). Look/mood only. Never shipped, never public.",
    "01_REFERENCES/INTERNAL/CHARACTERS/LOCKED": "Approved character sheets. The only images used as identity references.",
    "01_REFERENCES/INTERNAL/CHARACTERS/CANDIDATES": "Character options not approved yet.",
    "01_REFERENCES/INTERNAL/LOCATIONS/LOCKED": "Approved location plates and room maps.",
    "01_REFERENCES/INTERNAL/LOCATIONS/CANDIDATES": "",
    "01_REFERENCES/INTERNAL/PROPS/LOCKED": "Approved prop sheets.",
    "01_REFERENCES/INTERNAL/PROPS/CANDIDATES": "",
    "01_REFERENCES/INTERNAL/STYLE/LOCKED": "Approved style frames, style card, palette.",
    "01_REFERENCES/INTERNAL/STYLE/CANDIDATES": "",
    "01_REFERENCES/PROMPTS": "Reference prompts worth copying (ours or found), each with a 'why it works' note.",
    "01_REFERENCES/PERSONAL": "Real photos of real people (faces, voices). Private: indexed in place, never copied out, never public.",
    "02_PROMPTS": "Prompt files per shot/series. One prompt = one file or one block with its shot code.",
    "03_GENERATED/IMAGES": "Raw image generations as downloaded. GENERATION_LOG.jsonl sits in 03_GENERATED.",
    "03_GENERATED/VIDEO": "Raw video generations as downloaded.",
    "03_GENERATED/AUDIO": "Music, VO, SFX generations.",
    "03_GENERATED/_rejected": "Takes the user rejected. Skipped by every organizer.",
    "04_EDIT": "Editor bins (edit-media-bins), timelines, cut plans, project files.",
    "05_FINAL_OUTPUTS": "Finished renders only (final-outputs-organizer): Category/NN-Title/aspect/[LANG].",
    "06_DELIVERY": "Packages sent to clients or platforms (delivery-package), one dated folder per delivery.",
    "07_POSTING": "Captions, post texts, thumbnails, schedule, links of published posts.",
    "99_ARCHIVE": "Superseded and delivered material moved out of the way (versions-and-archive).",
}
README = """# {name}

Created {date} by project-scaffold. Type: {type}. Aspects: {aspects}. Languages: {langs}.

| Folder | What goes here |
|---|---|
{rows}

Rules
- Names are English only: folders, files, codes. Shot codes: S01, S02 … (insert: S03a). Takes: <Shot>_take01.
- Originals are never moved by tools; organizers copy. Old versions go to `_previous/` next to the file.
- 01_REFERENCES/EXTERNAL and 01_REFERENCES/PERSONAL never leave this project (no delivery, no public repo, no posts).
"""


def clean(s):
    return re.sub(r"_+", "_", re.sub(r"[^\w\-]+", "_", s)).strip("_")


def create(root, name, ptype, aspects, langs):
    proj = os.path.join(root, clean(name))
    made = []
    for rel in TREE:
        p = os.path.join(proj, rel)
        if not os.path.isdir(p):
            os.makedirs(p); made.append(rel)
    meta_path = os.path.join(proj, "PROJECT.json")
    meta = json.load(open(meta_path)) if os.path.exists(meta_path) else {}
    meta.setdefault("name", clean(name)); meta.setdefault("created", time.strftime("%Y-%m-%d"))
    meta["type"] = ptype or meta.get("type", "")
    meta["aspects"] = aspects or meta.get("aspects", [])
    meta["languages"] = langs or meta.get("languages", [])
    meta["paths"] = {"references": "01_REFERENCES", "prompts": "02_PROMPTS", "generated": "03_GENERATED",
                     "generation_log": "03_GENERATED/GENERATION_LOG.jsonl", "edit": "04_EDIT",
                     "final_outputs": "05_FINAL_OUTPUTS", "delivery": "06_DELIVERY", "posting": "07_POSTING",
                     "archive": "99_ARCHIVE"}
    json.dump(meta, open(meta_path, "w"), indent=2)
    rd = os.path.join(proj, "README.md")
    if not os.path.exists(rd):
        rows = "\n".join(f"| `{k}` | {v} |" for k, v in TREE.items() if v)
        open(rd, "w").write(README.format(name=meta["name"], date=meta["created"], type=meta["type"] or "-",
                                          aspects=", ".join(meta["aspects"]) or "-", langs=", ".join(meta["languages"]) or "-",
                                          rows=rows))
    brief = os.path.join(proj, "00_BRIEF", "BRIEF.md")
    if not os.path.exists(brief):
        open(brief, "w").write("# Brief\n\n- Goal:\n- Audience:\n- Deliverables (title x aspect x language):\n"
                               "- Platforms:\n- Deadline:\n- Must show:\n- Banned:\n- Budget for generations:\n")
    print(f"project: {proj}\ncreated {len(made)} folders" + ("" if made else " (tree already complete)"))
    for m in made:
        print("  +", m)


VIDEO = {".mp4", ".mov", ".m4v", ".webm"}
IMAGE = {".png", ".jpg", ".jpeg", ".webp"}


def check(proj):
    missing = [k for k in TREE if not os.path.isdir(os.path.join(proj, k))]
    print("missing folders:", ", ".join(missing) or "none")
    loose = [f for f in os.listdir(proj) if os.path.isfile(os.path.join(proj, f))
             and os.path.splitext(f)[1].lower() in VIDEO | IMAGE]
    if loose:
        print(f"{len(loose)} media files loose in the project root (should be in 03_GENERATED or 05_FINAL_OUTPUTS):")
        for f in loose[:15]:
            print("  ", f)
    nonascii = []
    for dp, dns, fns in os.walk(proj):
        dns[:] = [d for d in dns if d != "PERSONAL"]
        for n in dns + fns:
            if not n.isascii():
                nonascii.append(os.path.join(dp, n))
    if nonascii:
        print(f"{len(nonascii)} names are not English/ASCII:")
        for n in nonascii[:15]:
            print("  ", os.path.relpath(n, proj))
    extra = [d for d in os.listdir(proj) if os.path.isdir(os.path.join(proj, d)) and not d.startswith(".")
             and d not in {k.split("/")[0] for k in TREE}]
    if extra:
        print("folders outside the standard tree:", ", ".join(sorted(extra)))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root"); ap.add_argument("--name"); ap.add_argument("--type", default="")
    ap.add_argument("--aspects", default=""); ap.add_argument("--langs", default="")
    ap.add_argument("--check")
    a = ap.parse_args()
    if a.check:
        return check(os.path.abspath(a.check))
    if not (a.root and a.name):
        ap.error("--root and --name, or --check")
    split = lambda s: [x.strip() for x in s.split(",") if x.strip()]
    create(os.path.abspath(a.root), a.name, a.type, split(a.aspects), [x.upper() for x in split(a.langs)])


if __name__ == "__main__":
    sys.exit(main())
