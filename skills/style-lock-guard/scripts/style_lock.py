#!/usr/bin/env python3
"""style_lock.py — keeps the director's look from silently disappearing from prompts.

  init    STYLE_LOCK.json REF.png [REF.png ...]   read the reference frames (and the source prompt embedded in their PNG metadata, e.g. Midjourney
                                                  'Description'), measure their look, write the lock file. Edit "required" / "forbidden" after.
  lint    STYLE_LOCK.json PROMPT.txt [PACK_DIR]   FAIL if a required style phrase is missing, a forbidden phrase is present, or (with PACK_DIR)
                                                  the style reference images are not attached LAST. Exit 1 on failure — use it as a gate before sending.
  compare STYLE_LOCK.json IMG [IMG ...]           measure each image (contrast, shadow depth, highlight range, saturation, warm accents) against the
                                                  references; prints FLAT / OK per image and writes a side-by-side sheet next to the first image."""
import json, os, re, sys
from PIL import Image, ImageStat, ImageDraw


def metrics(path):
    im = Image.open(path).convert("RGB"); im.thumbnail((480, 480))
    L = im.convert("L"); hist = L.histogram(); n = sum(hist)
    def pct(p):
        c = 0
        for i, v in enumerate(hist):
            c += v
            if c >= n * p:
                return i
        return 255
    hsv = im.convert("HSV"); s = ImageStat.Stat(hsv).mean[1]
    px = list(im.getdata()); warm = sum(1 for r, g, b in px if r > 150 and r > b + 40 and r >= g) / len(px)
    return {"contrast": round(ImageStat.Stat(L).stddev[0], 1), "p5": pct(0.05), "p95": pct(0.95),
            "range": pct(0.95) - pct(0.05), "saturation": round(s, 1), "warm": round(warm * 100, 2)}


def source_prompt(path):
    info = Image.open(path).info
    for k in ("Description", "parameters", "prompt", "Comment", "Title"):
        if info.get(k):
            return str(info[k])
    return ""


def init(lock, refs):
    ms = [metrics(r) for r in refs]
    avg = {k: round(sum(m[k] for m in ms) / len(ms), 2) for k in ms[0]}
    data = {"style_refs": [os.path.abspath(r) for r in refs],
            "source_prompts": {os.path.basename(r): source_prompt(r) for r in refs},
            "ref_metrics": avg,
            "required": ["No flat lighting", "shallow depth of field", "film grain", "anamorphic"],
            "forbidden": ["no golden hour", "no direct sun", "desaturated, muted palette", "lifted blacks", "soft-to-medium matte contrast"],
            "tolerance": {"saturation": 0.8, "warm": 0.25, "range": 0.8}}
    json.dump(data, open(lock, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({k: data[k] for k in ("ref_metrics", "required", "forbidden")}, indent=1))
    for k, v in data["source_prompts"].items():
        print(f"\nSOURCE PROMPT of {k}:\n{v or '(none embedded)'}")


def lint(lock, prompt_path, pack=None):
    d = json.load(open(lock, encoding="utf-8")); t = open(prompt_path, encoding="utf-8").read(); low = t.lower(); errs = []
    edit = "re-shoot image 1 exactly" in low          # keep-everything edits (identity / colour fixes) inherit the look from image 1
    for r in ([] if edit else d["required"]):
        if r.lower() not in low:
            errs.append(f"missing required style phrase: '{r}'")
    for f in d["forbidden"]:
        if f.lower() in low:
            errs.append(f"contradicting phrase present: '{f}'")
    if pack and not edit:
        refs = sorted((x for x in os.listdir(pack) if x.startswith("ref_") and not x.startswith("._") and not x.endswith(".txt")),
                      key=lambda x: int(re.match(r"ref_(\d+)_", x).group(1)))
        names = [os.path.basename(s) for s in d["style_refs"]]
        last = refs[-len(names):] if refs else []
        if not any(any(n in x for n in names) for x in last):
            errs.append("no director style reference attached LAST (found: " + ", ".join(last) + ")")
    print("style-lint: OK" if not errs else "style-lint: FAIL\n  - " + "\n  - ".join(errs))
    return not errs


def compare(lock, imgs):
    d = json.load(open(lock, encoding="utf-8")); ref = d["ref_metrics"]; tol = d["tolerance"]; ok_all = True
    print(f"refs: {ref}")
    for p in imgs:
        m = metrics(p); flags = []
        # calibrated on real frames: flat grey frames keep their contrast but lose saturation and every warm light accent
        if m["saturation"] < ref["saturation"] * tol.get("saturation", 0.8): flags.append("washed-out colour")
        if ref["warm"] > 1 and m["warm"] < ref["warm"] * tol.get("warm", 0.25): flags.append("no warm light accents (sun / lamps / portholes)")
        if m["range"] < ref["range"] * tol["range"]: flags.append("compressed tonal range")
        if m["p5"] > ref["p5"] + 25: flags.append("milky / lifted blacks")
        verdict = "FLAT — " + ", ".join(flags) if flags else "OK"
        ok_all &= not flags
        print(f"{os.path.basename(os.path.dirname(p)) or p}/{os.path.basename(p)}: {m} -> {verdict}")
    w, h = 480, 270; allp = d["style_refs"] + list(imgs)
    sheet = Image.new("RGB", (w * 3, h * ((len(allp) + 2) // 3))); dr = ImageDraw.Draw(sheet)
    for i, p in enumerate(allp):
        im = Image.open(p).convert("RGB"); im.thumbnail((w, h)); x, y = (i % 3) * w, (i // 3) * h
        sheet.paste(im, (x, y)); dr.text((x + 4, y + 4), ("REF " if p in d["style_refs"] else "NEW ") + os.path.basename(p)[:34], fill=(255, 255, 0))
    out = os.path.join(os.path.dirname(os.path.abspath(imgs[0])), "_style_compare.jpg"); sheet.save(out, quality=85); print("sheet:", out)
    return ok_all


if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    cmd, lock = sys.argv[1], sys.argv[2]
    if cmd == "init":
        init(lock, sys.argv[3:])
    elif cmd == "lint":
        sys.exit(0 if lint(lock, sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else None) else 1)
    elif cmd == "compare":
        sys.exit(0 if compare(lock, sys.argv[3:]) else 1)
    else:
        sys.exit(__doc__)
