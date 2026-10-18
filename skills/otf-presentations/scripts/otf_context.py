#!/usr/bin/env python3
"""otf_context.py — builds the CONTEXT MANIFEST for an OTF presentation / animation from the project's real material.

  otf_context.py OUT_DIR --brief "what the video is for, from the chat" [--refs DIR ...] [--assets DIR ...] [--fonts DIR ...]
                 [--style-lock STYLE_LOCK.json] [--top 24]

It reads (never uploads):
  · reference frames (+ the source prompt embedded in PNG metadata: Midjourney 'Description', A1111 'parameters', 'prompt')
  · STYLE_LOCK.json (the director's look) — palette + metrics
  · asset folders (stills + videos): ranks stills by how close they are to the look (contrast, saturation, warm accents)
  · font folders (.ttf/.otf): classifies each family (serif display / condensed sans / grotesk / script / mono) and proposes pairings
  · text docs (*.md/*.txt) next to the assets: titles, headings, claims
Writes OUT_DIR/otf-context.json + otf-context.md + palette.png + hero_sheet.jpg. The model then fills the "from chat" section and the
open questions, shows the manifest to the user and only then plans the video."""
import glob, json, os, re, subprocess, sys
from PIL import Image, ImageDraw, ImageStat

IMG = (".png", ".jpg", ".jpeg", ".webp"); VID = (".mp4", ".mov", ".webm", ".m4v"); FONT = (".ttf", ".otf")


def arg_list(name):
    a = sys.argv; out = []
    for i, x in enumerate(a):
        if x == name and i + 1 < len(a):
            out.append(a[i + 1])
    return out


def arg(name, default=None):
    v = arg_list(name); return v[0] if v else default


def files(dirs, exts, limit=4000):
    out = []
    for d in dirs:
        for root, _, fs in os.walk(d):
            if "/." in root or "/_rejected" in root:
                continue
            out += [os.path.join(root, f) for f in fs if f.lower().endswith(exts) and not f.startswith(("._", "_orig", "_rejected"))]
            if len(out) > limit:
                return out
    return out


def metrics(p):
    im = Image.open(p).convert("RGB"); im.thumbnail((320, 320)); L = im.convert("L")
    s = ImageStat.Stat(im.convert("HSV")).mean[1]; px = list(im.getdata())
    warm = sum(1 for r, g, b in px if r > 150 and r > b + 40 and r >= g) / len(px)
    return {"contrast": round(ImageStat.Stat(L).stddev[0], 1), "saturation": round(s, 1), "warm": round(warm * 100, 2),
            "mean": round(ImageStat.Stat(L).mean[0], 1)}


def look_score(m, ref):
    if not ref:
        return m["contrast"] * 0.6 + m["saturation"] * 0.3 + min(m["warm"], 20)
    return -abs(m["saturation"] - ref["saturation"]) - abs(m["warm"] - ref["warm"]) * 2 - abs(m["contrast"] - ref["contrast"])


def embedded_prompt(p):
    try:
        info = Image.open(p).info
    except Exception:
        return ""
    for k in ("Description", "parameters", "prompt", "Comment"):
        if info.get(k):
            return str(info[k])[:1200]
    return ""


def palette(paths, n=8):
    tiles = []
    for p in paths[:12]:
        im = Image.open(p).convert("RGB"); im.thumbnail((160, 160)); tiles.append(im)
    if not tiles:
        return []
    W = sum(t.size[0] for t in tiles); H = max(t.size[1] for t in tiles); strip = Image.new("RGB", (W, H)); x = 0
    for t in tiles:
        strip.paste(t, (x, 0)); x += t.size[0]
    q = strip.quantize(colors=n, method=Image.MEDIANCUT); pal = q.getpalette()[: n * 3]; counts = sorted(q.getcolors(), reverse=True)
    out = []
    for c, idx in counts:
        r, g, b = pal[idx * 3: idx * 3 + 3]; out.append({"hex": f"#{r:02x}{g:02x}{b:02x}", "share": round(c / (W * H) * 100, 1)})
    return out


def font_family(path):
    n = os.path.splitext(os.path.basename(path))[0]
    fam = re.split(r"[-_ ](Regular|Bold|Italic|Light|Medium|Black|Thin|Semi|Extra|Variable|VariableFont).*", n)[0]
    return fam.replace("VariableFont", "").strip(" -_")


CLASSES = [("serif display", r"cinzel|playfair|abril|bodoni|didot|garamond|cormorant|libre ?baskerville|georgia|times|trajan|dm ?serif|prata|lora|merriweather|crimson"),
           ("condensed sans", r"bebas|anton|oswald|league gothic|barlow condensed|fjalla|teko|archivo narrow|black ?ops"),
           ("grotesk sans", r"inter|helvetica|neue|barlow|roboto|manrope|montserrat|poppins|work sans|ibm plex sans|space grotesk|dm sans|archivo"),
           ("script", r"script|great vibes|pacifico|dancing|allura|parisienne"),
           ("mono", r"mono|courier|code|jetbrains|plex mono")]


def classify(fam):
    f = fam.lower()
    for c, rx in CLASSES:
        if re.search(rx, f):
            return c
    return "other"


def covers(path, text="\u0416\u0429\u042f\u0424\u041b\u0411"):
    """True if the font draws real glyphs for these Cyrillic capitals (not the .notdef box) — checked by rendering, no fontTools needed.
    Capitals only, so caps-only fonts (Bebas Neue) are judged correctly; missing glyphs all render as the SAME .notdef box."""
    from PIL import ImageFont
    try:
        f = ImageFont.truetype(path, 48)
        notdef = bytes(f.getmask("\uffff")); masks = []
        for ch in text:
            m = f.getmask(ch)
            if not m.getbbox():
                return False
            masks.append(bytes(m))
        real = [m for m in masks if m != notdef]
        return len(real) == len(masks) and len(set(masks)) >= len(masks) - 1
    except Exception:
        return False


def video_info(p):
    try:
        d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", p], capture_output=True, text=True).stdout.strip()
        return round(float(d), 1)
    except Exception:
        return None


def main():
    if len(sys.argv) < 2 or sys.argv[1].startswith("-"):
        sys.exit(__doc__)
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    brief = arg("--brief", ""); top = int(arg("--top", 24))
    refs = files(arg_list("--refs"), IMG); assets = files(arg_list("--assets"), IMG); vids = files(arg_list("--assets"), VID)
    fonts = files(arg_list("--fonts") or [os.path.expanduser("~/Library/Fonts"), "/Library/Fonts"], FONT)
    lock = json.load(open(arg("--style-lock"), encoding="utf-8")) if arg("--style-lock") else {}
    ref_m = lock.get("ref_metrics")
    ref_entries = [{"path": p, "source_prompt": embedded_prompt(p), **metrics(p)} for p in refs]
    if not ref_m and ref_entries:
        ref_m = {k: sum(e[k] for e in ref_entries) / len(ref_entries) for k in ("contrast", "saturation", "warm")}
    scored = []
    for p in assets:
        try:
            m = metrics(p); scored.append({"path": p, "score": round(look_score(m, ref_m), 1), **m})
        except Exception:
            pass
    scored.sort(key=lambda x: -x["score"]); hero = scored[:top]
    pal = palette([e["path"] for e in ref_entries] or [h["path"] for h in hero])
    fams = {}
    for f in fonts:
        fam = font_family(f); e = fams.setdefault(fam, {"family": fam, "class": classify(fam), "files": [], "cyrillic": False})
        e["files"].append(f); e["cyrillic"] = e["cyrillic"] or covers(f)
    need_cyr = bool(re.search("[\u0400-\u04FF]", brief)) or "--cyrillic" in sys.argv
    by_class = {}
    for v in fams.values():
        by_class.setdefault(v["class"], []).append(v["family"] + ("" if v["cyrillic"] else " (no Cyrillic)"))
    PREF = {"serif display": ["Cormorant", "Playfair", "Cinzel", "Libre", "Lora", "Abril"], "condensed sans": ["Oswald", "Bebas", "Anton"],
            "grotesk sans": ["Inter", "Montserrat", "Manrope", "DMSans", "Barlow", "Roboto"]}
    def pick(cls, fallback):
        ok = [v for v in fams.values() if v["class"] == cls and (v["cyrillic"] or not need_cyr)]
        ok.sort(key=lambda v: next((i for i, k in enumerate(PREF.get(cls, [])) if v["family"].lower().startswith(k.lower())), 99))
        return ok[0]["family"] if ok else fallback
    pair = {"display": pick("serif display", "Georgia"), "accent": pick("condensed sans", "Oswald"), "body": pick("grotesk sans", "Helvetica Neue"),
            "needs_cyrillic": need_cyr}
    texts = []
    for d in arg_list("--assets"):
        for p in glob.glob(os.path.join(d, "*.md"))[:6] + glob.glob(os.path.join(d, "*.txt"))[:6]:
            try:
                t = open(p, encoding="utf-8", errors="ignore").read()
                texts.append({"path": p, "headings": re.findall(r"^#{1,3} (.+)$", t, re.M)[:20]})
            except Exception:
                pass
    data = {"brief_from_chat": brief, "style_lock": arg("--style-lock"), "ref_metrics": ref_m, "palette": pal,
            "references": ref_entries, "hero_stills": hero, "videos": [{"path": v, "duration": video_info(v)} for v in vids[:60]],
            "fonts": {"by_class": by_class, "proposed_pairing": pair}, "texts": texts,
            "to_fill_by_model": {"purpose": "", "audience": "", "length_s": "", "format": "", "must_show": [], "claims_in_their_words": [],
                                 "banned": [], "tone": "", "animation_vocabulary": [], "open_questions": []}}
    json.dump(data, open(os.path.join(out, "otf-context.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # palette swatch + hero sheet
    if pal:
        sw = Image.new("RGB", (120 * len(pal), 120)); dr = ImageDraw.Draw(sw)
        for i, c in enumerate(pal):
            dr.rectangle((i * 120, 0, i * 120 + 119, 119), fill=c["hex"]); dr.text((i * 120 + 6, 100), c["hex"], fill=(255, 255, 255))
        sw.save(os.path.join(out, "palette.png"))
    if hero:
        w, h = 400, 225; cols = 4; rows = (min(len(hero), 16) + cols - 1) // cols; sh = Image.new("RGB", (w * cols, h * rows)); dr = ImageDraw.Draw(sh)
        for i, e in enumerate(hero[:16]):
            im = Image.open(e["path"]).convert("RGB"); im.thumbnail((w, h)); sh.paste(im, ((i % cols) * w, (i // cols) * h))
            dr.text(((i % cols) * w + 4, (i // cols) * h + 4), f"{i + 1}. {os.path.basename(e['path'])[:36]}", fill=(255, 255, 0))
        sh.save(os.path.join(out, "hero_sheet.jpg"), quality=82)
    md = [f"# OTF context manifest", "", f"**Brief from chat:** {brief or '(fill in)'}", "",
          "## Look", f"- style lock: `{arg('--style-lock')}`" if arg("--style-lock") else "- no style lock (metrics from the references)",
          f"- reference metrics: {ref_m}", "- palette: " + ", ".join(f"{c['hex']} ({c['share']}%)" for c in pal), "",
          "## Source prompts embedded in the references"] + [f"- `{os.path.basename(e['path'])}`: {e['source_prompt'][:300]}" for e in ref_entries if e["source_prompt"]] + [
          "", f"## Hero stills (top {len(hero)} by closeness to the look) — see hero_sheet.jpg"] + [f"{i + 1}. `{e['path']}`" for i, e in enumerate(hero)] + [
          "", "## Videos"] + [f"- `{v['path']}` · {v['duration']} s" for v in data["videos"][:20]] + [
          "", "## Fonts available", *[f"- {c}: " + ", ".join(sorted(set(v))[:12]) for c, v in by_class.items()],
          f"- **proposed pairing:** display = {pair['display']}, accent = {pair['accent']}, body = {pair['body']}", "",
          "## To fill from the chat before planning", "purpose · audience · length · format · must-show · claims (their words) · banned · tone · "
          "animation vocabulary · open questions"]
    open(os.path.join(out, "otf-context.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md[:40])); print(f"\n-> {out}/otf-context.json · otf-context.md · palette.png · hero_sheet.jpg")


if __name__ == "__main__":
    main()
