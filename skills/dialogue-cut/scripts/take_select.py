#!/usr/bin/env python3
"""Pick the best reading of every script line from word-timed takes and write a CANDIDATE dialogue cut.

Usage:
  python3 take_select.py --script script.txt --takes take01.srt:/abs/take01.wav@01:00:00:00 take02.cues.json ... \
                         --out edit/dialogue [--fps 24] [--srt] [--min-recall 0.6]

script.txt   one spoken line per line; empty lines ignored; "## Title" starts a chapter.
timings      DEFAULT: DaVinci Resolve's own transcription, as phrase cues:
               <take>.srt        subtitles exported from Resolve (Create Subtitles from Audio, then export the track)
               <take>.cues.json  the JSON of the Resolve MCP timeline get_transcript(with_timecodes=true); an optional
                                 "timeline_start" ("01:00:00:00") or "source" field is read
             Word times inside a cue are spread by character length (phrase-level precision).
             ALSO accepted: word-level JSON from any transcriber (flat list of {"word","start","end","probability"},
             whisper {"segments":[{"words":[...]}]} or {"words":[...]}).
take spec    <timings>[:<media>[@offset]]  media is the source file; offset (seconds or HH:MM:SS:FF) is subtracted from
             cue times, e.g. take01.srt:/abs/take01.mov@01:00:00:00 for a timeline that starts at 1 hour.

Writes into --out (never touches dialogue_cut.json, the approved plan):
  dialogue_cut.candidate.json   clips in record order: id, line, text, take, source, in, out (frame-snapped), recall, score,
                                flag, alternatives; plus "fps". render-cut-verification reads it as a cut list.
  dialogue_cut.candidate.md     a review table: line, chosen take, times, recall, flags, runner-up
  subtitles.candidate.srt       with --srt: cues on the record timeline (84 chars, 2 lines of ~42, 6 s max, break on 0.7 s gaps)

Scoring (per reading): 100*recall - 2.5*extra words - 2*fillers + 4*mean word probability
                       - 35 if a redo cue follows within 3 s, +2 for the last reading of the line in that take.
Choice: best reading with recall >= --min-recall; else the best with recall >= 0.3, flagged LOOSE; else MISSING (ask for a pickup).
Word times from speech recognition are only good to about 50-100 ms: edges here are padded candidates. Run
dialogue-audio-finish/scripts/edge_qa.py on the result before anyone listens to it as a cut.
Standard library only.
"""
import argparse
import difflib
import json
import math
import os
import re
import sys
import unicodedata

FILLERS = {"um", "umm", "uh", "uhm", "erm", "er", "ah", "hmm", "mm", "mhm",
           "\u044d", "\u044d\u044d", "\u044d\u044d\u044d", "\u044d\u043c", "\u044d\u043c\u043c", "\u0430\u043c", "\u043c\u043c", "\u0445\u043c", "\u043c\u043c\u043c"}
REDO = re.compile(r"\b(scratch that|from the top|take two|let me (redo|start over|try again)|one more time|"
                  r"\u0441\u043d\u0430\u0447\u0430\u043b\u0430|\u0435\u0449[\u0435\u0451] \u0440\u0430\u0437|\u0437\u0430\u043d\u043e\u0432\u043e|\u0434\u0430\u0432\u0430\u0439 \u0435\u0449[\u0435\u0451]|\u043f\u0435\u0440\u0435\u0437\u0430\u043f\u0438\u0448\u0443|\u0441\u0442\u043e\u043f)\b")
PAD_IN, PAD_OUT = 0.08, 0.12
NUMS = {"zero": "0", "one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7",
        "eight": "8", "nine": "9", "ten": "10", "hundred": "100", "percent": "%"}
CONTRACTIONS = {"don't": "do not", "can't": "cannot", "won't": "will not", "it's": "it is", "i'm": "i am",
                "you're": "you are", "we're": "we are", "they're": "they are", "that's": "that is",
                "there's": "there is", "isn't": "is not", "doesn't": "does not", "didn't": "did not",
                "gonna": "going to", "wanna": "want to", "gotta": "got to", "let's": "let us"}


def norm_tokens(text):
    """Language-neutral normaliser: the same rules for script and recognised words, so they compare equal."""
    t = unicodedata.normalize("NFKC", text).lower().replace("\u0451", "\u0435").replace("’", "'").replace("%", " percent ")
    t = re.sub(r"[‐-―\-/]", " ", t)
    t = re.sub(r"[^\w' ]+", " ", t)
    out = []
    for w in t.split():
        w = w.strip("'")
        if not w:
            continue
        w = CONTRACTIONS.get(w, w)
        out += [NUMS.get(p, p) for p in w.split()]
    return out


def tc_seconds(v, fps):
    """Seconds from a number, "HH:MM:SS,mmm" (SRT) or "HH:MM:SS:FF" (timeline timecode)."""
    if isinstance(v, (int, float)):
        return float(v)
    v = str(v).strip().replace(";", ":")
    m = re.match(r"^(\d+):(\d+):(\d+)[,.](\d+)$", v)
    if m:
        h, mi, s, ms = m.groups()
        return int(h) * 3600 + int(mi) * 60 + int(s) + int(ms) / 10 ** len(ms)
    h, mi, s, f = [int(x) for x in v.split(":")]
    return h * 3600 + mi * 60 + s + f / fps


def load_cues(path, fps):
    """Phrase cues from DaVinci Resolve: an exported .srt, or the JSON of timeline get_transcript(with_timecodes)."""
    if path.lower().endswith(".srt"):
        cues = []
        for block in re.split(r"\n\s*\n", open(path, encoding="utf-8-sig").read().strip()):
            rows = block.strip().splitlines()
            for k, row in enumerate(rows):
                if "-->" in row:
                    a, b = [x.strip() for x in row.split("-->")]
                    cues.append({"start": a, "end": b, "text": " ".join(rows[k + 1:])})
                    break
        return cues, None, None
    d = json.load(open(path, encoding="utf-8"))
    d = d.get("result", d)
    return d.get("cues", []), d.get("source"), d.get("timeline_start")


def cue_words(cues, fps, offset):
    """Spread each cue's time over its words by character length. Cue timing is phrase-level, so edges MUST go
    through edge_qa.py; the word probability is set to 0.5 (unknown)."""
    words = []
    for c in cues:
        text = str(c.get("text", "")).strip()
        s = tc_seconds(c.get("start", c.get("start_tc", 0)), fps) - offset
        e = tc_seconds(c.get("end", c.get("end_tc", 0)), fps) - offset
        parts = text.split()
        total = sum(len(p) + 1 for p in parts) or 1
        t = s
        for p in parts:
            d = (e - s) * (len(p) + 1) / total
            words.append({"word": p, "start": t, "end": t + d, "probability": 0.5})
            t += d
    return words


def load_words(path, fps=24.0, offset=None):
    if path.lower().endswith(".srt") or path.lower().endswith(".cues.json"):
        cues, src, start = load_cues(path, fps)
        if offset is None:
            offset = tc_seconds(start, fps) if start else 0.0
        raw, d = cue_words(cues, fps, offset), None
    else:
        d = json.load(open(path, encoding="utf-8"))
        src = d.get("source") if isinstance(d, dict) else None
        if isinstance(d, dict):
            raw = d.get("words") or [w for s in d.get("segments", []) for w in s.get("words", [])]
        else:
            raw = d
    words = []
    for w in raw:
        text = str(w.get("word", w.get("text", ""))).strip()
        if not text or w.get("start") is None or w.get("end") is None:
            continue
        toks = norm_tokens(text)
        if not toks:
            continue
        p = w.get("probability", w.get("prob", w.get("score", 1.0)))
        for tok in toks:  # "it's" -> two tokens sharing the word's times
            words.append({"t": tok, "raw": text, "s": float(w["start"]), "e": float(w["end"]), "p": float(p)})
    return words, src


def read_script(path):
    lines, chapter = [], None
    for raw in open(path, encoding="utf-8"):
        s = raw.strip()
        if not s:
            continue
        if s.startswith("##"):
            chapter = s.lstrip("#").strip()
            continue
        toks = [t for t in norm_tokens(s) if t not in FILLERS]
        if toks:
            lines.append({"text": s, "toks": toks, "chapter": chapter})
    return lines


def readings(line, take):
    """Every attempt at this line inside one take: aligned spans with recall >= 0.3, overlaps resolved by score."""
    L, W = line["toks"], take["content"]
    if not W:
        return []
    heads = set(L[:3])
    span_max = int(len(L) * 1.6) + 4
    found = []
    for i, w in enumerate(W):
        if w["t"] not in heads:
            continue
        span = W[i:i + span_max]
        sm = difflib.SequenceMatcher(None, L, [x["t"] for x in span], autojunk=False)
        blocks = [b for b in sm.get_matching_blocks() if b.size]
        matched = sum(b.size for b in blocks)
        recall = matched / len(L)
        if recall < 0.3:
            continue
        first = blocks[0].b
        last = blocks[-1].b + blocks[-1].size - 1
        used = span[first:last + 1]
        extra = len(used) - matched
        s, e = used[0]["s"], used[-1]["e"]
        fillers = sum(1 for f in take["fillers"] if s <= f["s"] <= e)
        after = " ".join(x["t"] for x in take["all"] if e < x["s"] <= e + 3.0)
        redo = bool(REDO.search(after))
        prob = sum(x["p"] for x in used) / len(used)
        score = 100 * recall - 2.5 * extra - 2 * fillers + 4 * prob - (35 if redo else 0)
        found.append({"take": take["name"], "source": take["source"], "in": s, "out": e, "recall": round(recall, 3),
                      "extra": extra, "fillers": fillers, "redo_after": redo, "prob": round(prob, 3),
                      "score": score, "words": [{"w": x["raw"], "s": x["s"], "e": x["e"]} for x in used]})
    found.sort(key=lambda r: -r["score"])
    kept = []
    for r in found:  # one reading per stretch of audio
        if all(r["out"] <= k["in"] or r["in"] >= k["out"] for k in kept):
            kept.append(r)
    if kept:
        max(kept, key=lambda r: r["in"])["score"] += 2
    return kept


def snap(t, fps, up):
    f = t * fps
    return (math.ceil(f - 1e-9) if up else math.floor(f + 1e-9)) / fps


def srt_time(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def wrap2(text, width=42):
    if len(text) <= width:
        return text
    words, best, cut = text.split(), None, 0
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        d = abs(len(a) - len(b))
        if best is None or d < best:
            best, cut = d, i
    return " ".join(words[:cut]) + "\n" + " ".join(words[cut:])


def subtitles(clips):
    cues, cur = [], None
    for c in clips:
        if c["flag"] == "MISSING":
            continue
        shift = c["record_in"] - c["in"]
        for w in c["words"]:
            s, e, txt = w["s"] + shift, w["e"] + shift, w["w"].strip()
            if cur and (s - cur["e"] > 0.7 or len(cur["text"]) + 1 + len(txt) > 84 or e - cur["s"] > 6.0):
                cues.append(cur)
                cur = None
            if cur is None:
                cur = {"s": s, "e": e, "text": txt}
            else:
                cur["e"], cur["text"] = e, cur["text"] + " " + txt
    if cur:
        cues.append(cur)
    out = []
    for i, q in enumerate(cues):
        nxt = cues[i + 1]["s"] if i + 1 < len(cues) else q["e"] + 0.3
        end = min(q["e"] + 0.3, nxt - 0.01)
        out.append(f"{i + 1}\n{srt_time(q['s'])} --> {srt_time(end)}\n{wrap2(q['text'])}\n")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--script", required=True)
    ap.add_argument("--takes", nargs="+", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--fps", type=float, default=24.0)
    ap.add_argument("--min-recall", type=float, default=0.6)
    ap.add_argument("--srt", action="store_true")
    a = ap.parse_args()

    takes = []
    for spec in a.takes:
        path, _, media = spec.partition(":") if not os.path.exists(spec) else (spec, "", "")
        offset = None
        if "@" in media:
            media, _, off = media.rpartition("@")
            offset = tc_seconds(off, a.fps) if ":" in off else float(off)
        words, src = load_words(path, a.fps, offset)
        name = re.sub(r"(\.words|\.cues)?\.(json|srt)$", "", os.path.basename(path))
        takes.append({"name": name, "source": media or src or re.sub(r"(\.words|\.cues)?\.(json|srt)$", "", path),
                      "all": words, "content": [w for w in words if w["t"] not in FILLERS],
                      "fillers": [w for w in words if w["t"] in FILLERS]})
    lines = read_script(a.script)
    if not lines:
        sys.exit("script has no spoken lines")

    clips, rec = [], 0.0
    for n, line in enumerate(lines, 1):
        cands = sorted((r for t in takes for r in readings(line, t)), key=lambda r: -r["score"])
        good = [r for r in cands if r["recall"] >= a.min_recall]
        pick = good[0] if good else (cands[0] if cands else None)
        flag = "OK" if good else ("LOOSE" if pick else "MISSING")
        clip = {"id": f"L{n:02d}", "line": n, "chapter": line["chapter"], "text": line["text"], "flag": flag}
        if pick:
            if pick["redo_after"]:
                clip["flag"] += " REDO-CUE-AFTER"
            if pick["fillers"]:
                clip["flag"] += f" FILLERS:{pick['fillers']}"
            i, o = snap(max(0.0, pick["in"] - PAD_IN), a.fps, False), snap(pick["out"] + PAD_OUT, a.fps, True)
            clip.update({"take": pick["take"], "source": pick["source"], "in": round(i, 4), "out": round(o, 4),
                         "record_in": round(rec, 4), "recall": pick["recall"], "score": round(pick["score"], 1),
                         "words": pick["words"],
                         "alternatives": [{k: (round(r[k], 3) if isinstance(r[k], float) else r[k])
                                           for k in ("take", "in", "out", "recall", "score")} for r in cands[1:4]]})
            rec += o - i
        clips.append(clip)

    os.makedirs(a.out, exist_ok=True)
    plan = {"fps": a.fps, "status": "candidate", "pad_in": PAD_IN, "pad_out": PAD_OUT, "clips": clips}
    tmp = os.path.join(a.out, ".dialogue_cut.candidate.json.tmp")
    json.dump(plan, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    os.replace(tmp, os.path.join(a.out, "dialogue_cut.candidate.json"))

    md = ["# Dialogue cut CANDIDATE (not approved)", "",
          "| id | line | take | in | out | recall | score | flag | runner-up |", "|---|---|---|---|---|---|---|---|---|"]
    for c in clips:
        alt = c.get("alternatives") or []
        ru = f"{alt[0]['take']} {alt[0]['score']}" if alt else ""
        md.append(f"| {c['id']} | {c['text'][:50]} | {c.get('take', '')} | {c.get('in', '')} | {c.get('out', '')} | "
                  f"{c.get('recall', '')} | {c.get('score', '')} | {c['flag']} | {ru} |")
    miss = [c["id"] for c in clips if c["flag"].startswith(("MISSING", "LOOSE"))]
    md += ["", f"Total {rec:.2f} s, {len(clips)} lines. Needs a pickup or a listen: {', '.join(miss) or 'none'}."]
    open(os.path.join(a.out, "dialogue_cut.candidate.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    if a.srt:
        open(os.path.join(a.out, "subtitles.candidate.srt"), "w", encoding="utf-8").write(subtitles(clips))
    print(f"{len(clips)} lines, {len(miss)} flagged, total {rec:.2f} s -> {a.out}")


if __name__ == "__main__":
    main()
