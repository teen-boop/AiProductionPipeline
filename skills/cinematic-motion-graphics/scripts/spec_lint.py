#!/usr/bin/env python3
"""Lint a cinematic motion-graphics shot plan (shot-plan JSON) before anything is built or rendered.

Checks, one line each (PASS / WARN / FAIL):
  - envelope: id, category (one of the nine), fps (24 unless a reason is given), canvas, duration, export;
  - look: a STYLE_LOCK or style card is named (the graphic inherits the film's look);
  - every on-screen text is approved by the user, held long enough to read (about 3 words per second,
    never under the minimum hold) and ends inside the duration;
  - text boxes, when given, sit inside the title-safe area of their canvas (16:9 or 9:16 rules);
  - period graphics carry an accuracy list (claim + source); pending claims block the final render;
  - fonts cover the script of the texts (Cyrillic texts need a font marked cyrillic and glyph-tested);
  - assets are the project's own or generated with the user's yes; no stock, no remote URLs;
  - alpha exports declare a transparent background.
Exit code 1 if any FAIL. Pure Python 3, no dependencies.
With --final (before the delivery render) an unverified accuracy line is a FAIL instead of a WARN.
Usage: python3 spec_lint.py SHOT_PLAN.json [more.json ...] [--wps 3] [--min-hold 1.5] [--final]
"""
import argparse, json, re, sys

CATEGORIES = {"period-map", "date-stamp", "press-headline", "lower-third", "fact-card",
              "timeline", "blueprint", "title-card", "composite-overlay"}
PERIOD_CATEGORIES = {"period-map", "press-headline", "timeline", "blueprint"}
EXPORTS = {"mp4", "prores4444", "webm-alpha", "png-sequence"}
ALPHA = {"prores4444", "webm-alpha", "png-sequence"}
CYR = re.compile("[\u0400-\u04FF]")
# title-safe insets as shares of width / height: (left, top, right, bottom)
SAFE = {"16:9": (0.05, 0.05, 0.05, 0.05), "9:16": (0.06, 0.14, 0.12, 0.20), "1:1": (0.05, 0.05, 0.05, 0.05),
        "4:5": (0.05, 0.08, 0.05, 0.12), "2.39:1": (0.05, 0.05, 0.05, 0.05)}


def words(t):
    return len([w for w in re.split(r"\s+", t.strip()) if w])


def lint(path, wps, min_hold, final=False):
    out = []
    add = lambda lvl, msg: out.append((lvl, msg))
    try:
        s = json.load(open(path, encoding="utf-8"))
    except Exception as e:
        return [("FAIL", f"not valid JSON: {e}")]

    for k in ("id", "category", "fps", "canvas", "duration_s", "export", "texts"):
        if k not in s:
            add("FAIL", f"missing envelope key '{k}'")
    cat = s.get("category")
    if cat and cat not in CATEGORIES:
        add("FAIL", f"category '{cat}' is not one of: {', '.join(sorted(CATEGORIES))}")
    fps = s.get("fps")
    if fps is not None and fps != 24:
        add("WARN" if s.get("fps_reason") else "FAIL",
            f"fps {fps}: the film runs at 24 unless 'fps_reason' says why (matching a 25/30 timeline)")
    canvas = s.get("canvas", {})
    W, H, aspect = canvas.get("w"), canvas.get("h"), canvas.get("aspect")
    if W and H and aspect in SAFE and aspect not in ("2.39:1",):
        a, b = (float(x) for x in aspect.split(":"))
        if abs(W / H - a / b) > 0.01:
            add("FAIL", f"canvas {W}x{H} does not match aspect {aspect}")
    elif aspect and aspect not in SAFE:
        add("WARN", f"aspect {aspect}: no safe-area rule, check by eye")
    dur = s.get("duration_s", 0)
    exp = s.get("export")
    if exp and exp not in EXPORTS:
        add("FAIL", f"export '{exp}' is not one of: {', '.join(sorted(EXPORTS))}")
    if exp in ALPHA and s.get("background") != "transparent":
        add("FAIL", f"export '{exp}' is an alpha overlay: set \"background\": \"transparent\"")

    look = s.get("look", {})
    if not (look.get("style_lock") or look.get("style_card") or look.get("style_pack")):
        add("FAIL", "no look source: name the project's STYLE_LOCK, style card or style pack in 'look'")

    fonts = {f.get("family"): f for f in s.get("fonts", [])}
    texts = s.get("texts", [])
    if not texts:
        add("WARN", "no on-screen text listed (fine for a pure route or drawing; otherwise list every word)")
    for t in texts:
        tid, txt = t.get("id", "?"), t.get("text", "")
        if t.get("approved") is not True:
            add("FAIL", f"text '{tid}' is not approved by the user: \"{txt[:40]}\"")
        need = max(min_hold, words(txt) / wps)
        hold = t.get("hold_s")
        if hold is None:
            add("FAIL", f"text '{tid}' has no hold_s (time fully readable after its entrance)")
        elif hold + 1e-6 < need:
            add("FAIL", f"text '{tid}' holds {hold}s, needs >= {need:.1f}s ({words(txt)} words at {wps} w/s)")
        end = t.get("in_s", 0) + t.get("enter_s", 0) + (hold or 0)
        if dur and end > dur + 1e-6:
            add("FAIL", f"text '{tid}' is still on screen at {end:.2f}s, past duration {dur}s")
        box = t.get("box")
        if box and W and H and aspect in SAFE:
            l, tp, r, b = SAFE[aspect]
            x, y, w, h = box
            if x < W * l or y < H * tp or x + w > W * (1 - r) or y + h > H * (1 - b):
                add("FAIL", f"text '{tid}' box {box} leaves the {aspect} title-safe area")
        fam = t.get("font")
        if CYR.search(txt):
            f = fonts.get(fam)
            if not f or not f.get("cyrillic") or f.get("glyph_test") != "pass":
                add("FAIL", f"text '{tid}' is Cyrillic but font '{fam}' is not marked cyrillic with glyph_test pass")
        if fam and fam not in fonts:
            add("WARN", f"text '{tid}' uses font '{fam}' that is not in 'fonts'")
    for fam, f in fonts.items():
        if not f.get("file"):
            add("WARN", f"font '{fam}' has no local file: a render must not depend on a system or CDN font")

    period = s.get("period") or cat in PERIOD_CATEGORIES
    acc = s.get("accuracy", [])
    if period:
        if not acc:
            add("FAIL", "period graphic without an 'accuracy' list (run period-fact-check first)")
        for i, c in enumerate(acc):
            if not c.get("claim") or not c.get("source"):
                add("FAIL", f"accuracy[{i}] needs both 'claim' and 'source'")
            elif c.get("status") != "verified":
                add("FAIL" if final else "WARN", f"accuracy[{i}] not verified yet (blocks final render): {c['claim'][:60]}")

    for i, a in enumerate(s.get("assets", [])):
        src = str(a.get("path", ""))
        if re.match(r"^[a-z]+://", src):
            add("FAIL", f"asset[{i}] is a remote URL; freeze it into the project first")
        origin = a.get("origin")
        if origin not in ("project", "generated"):
            add("FAIL", f"asset[{i}] origin '{origin}': only the project's own or pipeline-generated assets")
        if origin == "generated" and a.get("user_approved") is not True:
            add("FAIL", f"asset[{i}] is generated without the user's recorded yes ('user_approved': true)")

    if not out:
        add("PASS", "all checks passed")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("specs", nargs="+")
    ap.add_argument("--wps", type=float, default=3.0, help="reading speed, words per second")
    ap.add_argument("--min-hold", type=float, default=1.5, help="minimum readable hold in seconds")
    ap.add_argument("--final", action="store_true", help="delivery gate: unverified accuracy lines fail")
    a = ap.parse_args()
    failed = False
    for p in a.specs:
        res = lint(p, a.wps, a.min_hold, a.final)
        print(f"== {p}")
        for lvl, msg in res:
            print(f"{lvl} {msg}")
        failed |= any(l == "FAIL" for l, _ in res)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
