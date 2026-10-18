#!/usr/bin/env python3
"""segment_blocks.py — builds the per-timecode-block part of a video-to-video edit prompt.

  segment_blocks.py SEGMENTS.json REFS.json ASSIGN.json [--base BASE.json] [--voice VOICE.json] [--video @vid-1] [--out blocks.txt]

SEGMENTS.json  from video-cut-timecodes (blocks with start/end)
REFS.json      {"@img-1": {"name": "Koss", "kind": "character", "look": "man in the black leather biker jacket, short dark hair …"}, …}
               kind = character | location | prop | grade   (look = the confirmed one-line description of THAT reference)
ASSIGN.json    {"1": {"refs": ["@img-1", "@img-3"], "framing": "medium two-shot", "eyes": "Koss looks off to the left, never into the lens"}, …}
               (made automatically by looking at the block frames, or typed by the user — the script does not guess)
BASE.json      optional base details used when a block has no image reference for something:
               {"locations": {"street": "…", "cabin": "…"}, "light": "…", "wardrobe": {"Koss": "…"}, "props": {"chair": "…"}}
               a block uses them only when ASSIGN names them: "base_location": "cabin", "base_chars": ["Koss"], "base_props": ["chair"]
VOICE.json     optional {"3": {"mode": "new", "speaker": "@img-1", "text": "exact words"}, …}; every other block keeps the original voice.

Every block gets: TIMECODE · FRAMING · MOTION (exactly as in the source range) · VOICE · LOOK LOCK (auto-filled from the reference
descriptions, or from BASE details when no reference covers it)."""
import json, sys


def load(p, default=None):
    return json.load(open(p, encoding="utf-8")) if p else default


def arg(name, default=None):
    a = sys.argv
    return a[a.index(name) + 1] if name in a else default


def main():
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    segs = load(sys.argv[1])["segments"]; refs = load(sys.argv[2]); assign = load(sys.argv[3])
    base = load(arg("--base"), {}); voice = load(arg("--voice"), {}); vid = arg("--video", "@vid-1")
    out, missing = [], []
    for s in segs:
        n = str(s["n"]); a = assign.get(n)
        if not a:
            missing.append(n); continue
        rng = f"{s['start']:.1f}-{s['end']:.1f} s"
        used = [r for r in a.get("refs", []) if r in refs]
        chars = [r for r in used if refs[r]["kind"] == "character"]
        locs = [r for r in used if refs[r]["kind"] == "location"]
        props = [r for r in used if refs[r]["kind"] == "prop"]
        who = ", ".join(f"{refs[r]['name']} ({r})" for r in chars) or "no characters"
        lines = [f"[{rng}] BLOCK {n} — {a.get('framing', 'framing exactly as in ' + vid)}; {who}."]
        lines.append(f"MOTION: exactly as in {vid} {rng} — the same body movement, gestures, facial expressions, eye direction, "
                     f"camera move, framing and timing; nothing added, nothing re-described.")
        if a.get("eyes"):
            lines.append(f"EYES: {a['eyes']}.")
        v = voice.get(n)
        if v and v.get("mode") == "new":
            sp = refs.get(v["speaker"], {}).get("name", v["speaker"])
            lines.append(f"VOICE: {sp} ({v['speaker']}) says exactly: \"{v['text']}\" — in the original voice, with lips in sync; "
                         f"no other words in this block.")
        elif v and v.get("mode") == "silent":
            lines.append("VOICE: no speech in this block.")
        else:
            lines.append(f"VOICE: the original voice, words, intonation and timing of {vid} {rng}, lips in sync; no new words.")
        look = [f"{refs[r]['name']} ({r}): {refs[r]['look']}" for r in chars]
        for c in a.get("base_chars", []):                                  # characters in the block without an image reference
            if c in base.get("wardrobe", {}):
                look.append(f"{c}: {base['wardrobe'][c]}")
        if locs:
            look += [f"location ({r}): {refs[r]['look']} — look only, the layout and camera angle stay as in {vid}" for r in locs]
        elif a.get("base_location") in base.get("locations", {}):
            look.append(f"location: {base['locations'][a['base_location']]} — the layout and camera angle stay as in {vid}")
        else:
            look.append(f"location: exactly as in {vid} in this range")          # nothing known → never invent a place
        look += [f"{refs[r]['name']} ({r}): {refs[r]['look']}" for r in props]
        for p in a.get("base_props", []):
            if p in base.get("props", {}):
                look.append(f"{p}: {base['props'][p]}")
        if base.get("light"):
            look.append(f"light and grade: {base['light']}")
        lines.append("LOOK LOCK: " + "; ".join(look) + ".")
        out.append("\n".join(lines))
    text = "\n\n".join(out)
    if arg("--out"):
        open(arg("--out"), "w", encoding="utf-8").write(text + "\n")
    print(text)
    if missing:
        print(f"\n!! blocks without an assignment: {', '.join(missing)} — assign them (auto by looking at the frames, or manually) first.",
              file=sys.stderr); sys.exit(2)


if __name__ == "__main__":
    main()
