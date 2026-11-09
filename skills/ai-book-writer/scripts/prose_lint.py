#!/usr/bin/env python3
"""prose_lint.py - surface checks for fiction prose (ai-book-writer skill).

Reports, with line numbers:
  (a) weak sequence connectors ("and then", "then", "after that", "next", and Russian equivalents)
  (b) telling instead of showing ("he realized that", "she felt", "suddenly", "it was clear", ...)
  (c) beat weight, when the draft carries beat markers [B1]..[B8] or <!-- B1 -->..<!-- B8 -->
  (d) tense mix per paragraph (English only) and POV drift between paragraphs (English and Russian)

Every hit is a candidate for a human (or the co-writer) to read in context, not a verdict.
Dialogue in quotes, dash-dialogue lines and *italic* thoughts are masked before checks (a)-(d).
Python 3 standard library only.

Usage:
  python3 prose_lint.py scene.md
  python3 prose_lint.py scene.md --json
  python3 prose_lint.py chapter.txt --expect-tense past --expect-pov third --strict
  cat scene.md | python3 prose_lint.py -
"""
import argparse
import json
import re
import sys
from collections import OrderedDict

SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}
FLAGS = re.IGNORECASE | re.UNICODE

# ---------------------------------------------------------------- rules
# (rule id, language, regex, severity, message)
CONNECTOR_RULES = [
    ("and_then", "en", r"(?<!now )(?<!every )\band then\b", "high", "sequence connector: is this joint THEREFORE or BUT?"),
    ("after_that", "en", r"\bafter that\b", "high", "sequence connector: is this joint THEREFORE or BUT?"),
    ("then_opening", "en", r"(?:^|(?<=[.!?:;]\s)|(?<=[.!?]\s\s))then\b", "medium",
     "sentence opens with 'Then': check the cause behind the step"),
    ("then", "en", r"(?<!and )(?<!by )(?<!since )(?<!until )(?<!till )(?<!back )(?<!even )(?<!only )"
     r"(?<!just )(?<!right )(?<!but )\bthen\b", "low",
     "'then' inside a sentence: sequence or consequence?"),
    ("next_opening", "en", r"(?:^|(?<=[.!?:;]\s))next\b", "medium",
     "sentence opens with 'Next': check the cause behind the step"),
    ("time_jump", "en", r"(?:^|(?<=[.!?]\s))(?:later|afterwards|afterward|meanwhile|"
     r"the next (?:morning|day|evening|night|week))\b", "low",
     "time-jump opener: does the new paragraph have a reason to start?"),
    ("i_potom", "ru", r"\b[\u0438\u0430]\s+\u043f\u043e\u0442\u043e\u043c\b", "high", "sequence connector: is this joint THEREFORE or BUT?"),
    ("posle_etogo", "ru", r"\b\u043f\u043e\u0441\u043b\u0435 \u044d\u0442\u043e\u0433\u043e\b", "high", "sequence connector: is this joint THEREFORE or BUT?"),
    ("zatem", "ru", r"\b\u0437\u0430\u0442\u0435\u043c\b", "medium", "sequence connector: is this joint THEREFORE or BUT?"),
    ("potom", "ru", r"(?<!\u0438 )(?<!\u0430 )(?<!\u0418 )(?<!\u0410 )\b\u043f\u043e\u0442\u043e\u043c\b", "medium",
     "sequence connector: is this joint THEREFORE or BUT?"),
]

TELLING_RULES = [
    ("realized", "en", r"\b(?:(?:I|he|she|they|we|you)\s+(?:suddenly\s+|finally\s+|slowly\s+)?)?"
     r"(?:realized|realised|realizes|realises|understood|understands)\b(?:\s+that\b)?", "medium",
     "the character concludes for the reader: show the evidence that makes the reader conclude"),
    ("knew_that", "en", r"\b(?:knew|noticed|recognized|recognised|sensed)\s+that\b", "medium",
     "filter verb + that: show the thing itself"),
    ("felt", "en", r"\b(?:I|he|she|they|we|you)\s+(?:felt|feels|sensed|senses)\b", "medium",
     "named feeling: show it through the body, an action or an object"),
    ("named_emotion", "en", r"\b(?:I|he|she|they|we)\s+(?:was|were|is|are)\s+(?:so\s+|very\s+|really\s+)?"
     r"(?:angry|sad|happy|afraid|scared|nervous|furious|jealous|ashamed|anxious|lonely|relieved|"
     r"terrified|excited|devastated|heartbroken)\b", "medium",
     "named emotion: show what the emotion makes the character do"),
    ("suddenly", "en", r"\bsuddenly\b", "low", "'suddenly' announces surprise instead of staging it"),
    ("it_was_clear", "en", r"\bit (?:was|is|seemed|became) (?:clear|obvious|evident|apparent)\b", "medium",
     "the narrator states the conclusion: dramatize what makes it clear"),
    ("ponyal_chto", "ru", r"\b(?:\u043f\u043e\u043d\u044f\u043b|\u043f\u043e\u043d\u0438\u043c\u0430\u043b)[\u0430\u0438]?\s*,?\s*\u0447\u0442\u043e\b", "medium",
     "the character concludes for the reader: show the evidence"),
    ("pochuvstvoval", "ru", r"\b\u043f\u043e\u0447\u0443\u0432\u0441\u0442\u0432\u043e\u0432\u0430\u043b[\u0430\u0438]?\b", "medium",
     "named feeling: show it through the body, an action or an object"),
    ("osoznal", "ru", r"\b\u043e\u0441\u043e\u0437\u043d\u0430\u043b[\u0430\u0438]?\b", "medium", "the character concludes for the reader: show the evidence"),
    ("oshchutil", "ru", r"\b\u043e\u0449\u0443\u0442\u0438\u043b[\u0430\u0438]?\b", "low", "named sensation: often a filter, show the thing itself"),
    ("vdrug", "ru", r"\b\u0432\u0434\u0440\u0443\u0433\b", "low", "'suddenly' announces surprise instead of staging it"),
    ("bylo_yasno", "ru", r"\b\u0431\u044b\u043b\u043e (?:\u044f\u0441\u043d\u043e|\u043f\u043e\u043d\u044f\u0442\u043d\u043e|\u043e\u0447\u0435\u0432\u0438\u0434\u043d\u043e)\b", "medium",
     "the narrator states the conclusion: dramatize what makes it clear"),
]

COMPILED = [(cat, rid, lang, re.compile(rx, FLAGS), sev, msg)
            for cat, rules in (("connector", CONNECTOR_RULES), ("telling", TELLING_RULES))
            for rid, lang, rx, sev, msg in rules]

BEAT_RE = re.compile(r"\[\s*B([1-8])\s*\]|<!--\s*B([1-8])\s*-->", re.IGNORECASE)
WORD_RE = re.compile(r"[^\W\d_]+(?:['\u2019-][^\W\d_]+)*", re.UNICODE)
CYR_RE = re.compile(r"[\u0400-\u04ff]")
LAT_RE = re.compile(r"[A-Za-z]")

# ---------------------------------------------------------------- tense lexicon (English)
PAST_AUX = {"was", "were", "had", "did", "wasn't", "weren't", "hadn't", "didn't", "couldn't", "wouldn't"}
PRES_AUX = {"is", "are", "am", "has", "does", "isn't", "aren't", "hasn't", "doesn't", "can't", "won't",
            "i'm", "he's", "she's", "it's", "we're", "they're", "you're"}
IRREGULAR_PAST = set("""
said went came saw took made knew thought told felt got gave found left stood sat ran held kept brought began
looked turned walked asked tried seemed wanted opened closed pulled pushed waited answered smiled laughed moved
stopped started reached watched heard spoke wrote drew drove threw grew broke chose fell flew forgot froze hid
lay led lost meant met paid rang rose sang sank shook shot slept slid spent stole struck swam swore taught tore
understood woke wore won bent bit blew bought caught dealt dug fed fought fled hung knelt lit sought sold sent
shone shut slung spun sprang stuck stung stank strode stretched swung wept wound
""".split())
SUBJECT_3S = {"he", "she", "it"}
SUBJECT_OTHER = {"i", "we", "they", "you"}
NOT_VERB_S = {"is", "was", "has", "does", "his", "its", "this", "thus", "us", "yes", "as", "always",
              "perhaps", "besides", "sometimes", "less", "unless", "across", "news", "towards", "afterwards"}
COMMON_BASE = set("""
walk look say go come see take know think want feel turn stand sit run hold open close wait keep try tell ask
need hear watch pull push reach smile laugh move stop start begin leave put get make give find stare shrug nod
lean step lift drop count check pick
""".split())
ED_EXCEPT = {"need", "feed", "bed", "red", "seed", "speed", "indeed", "hundred", "shed", "bleed", "breed", "proceed",
             "succeed", "exceed", "greed", "weed", "sled", "fled", "wed", "led"}

# ---------------------------------------------------------------- POV lexicon
FIRST_PERSON = {"i", "me", "my", "mine", "myself", "we", "us", "our", "ours", "ourselves",
                "\u044f", "\u043c\u0435\u043d\u044f", "\u043c\u043d\u0435", "\u043c\u043d\u043e\u0439", "\u043c\u043d\u043e\u044e", "\u043c\u043e\u0439", "\u043c\u043e\u044f", "\u043c\u043e\u0451", "\u043c\u043e\u0435", "\u043c\u043e\u0438", "\u043c\u043e\u0435\u0433\u043e", "\u043c\u043e\u0435\u0439",
                "\u043c\u043e\u0438\u0445", "\u043c\u043e\u044e", "\u043c\u043e\u0438\u043c", "\u043c\u043e\u0438\u043c\u0438", "\u043c\u043e\u0435\u043c\u0443", "\u043c\u044b", "\u043d\u0430\u0441", "\u043d\u0430\u043c", "\u043d\u0430\u043c\u0438", "\u043d\u0430\u0448", "\u043d\u0430\u0448\u0430", "\u043d\u0430\u0448\u0435",
                "\u043d\u0430\u0448\u0438", "\u043d\u0430\u0448\u0435\u0433\u043e", "\u043d\u0430\u0448\u0435\u0439", "\u043d\u0430\u0448\u0438\u0445", "\u043d\u0430\u0448\u0443"}
THIRD_PERSON = {"he", "him", "his", "himself", "she", "her", "hers", "herself",
                "\u043e\u043d", "\u0435\u0433\u043e", "\u0435\u043c\u0443", "\u043d\u0435\u0433\u043e", "\u043d\u0435\u043c\u0443", "\u043d\u0438\u043c", "\u043d\u0451\u043c", "\u043d\u0435\u043c", "\u043e\u043d\u0430", "\u0435\u0451", "\u0435\u0435", "\u0435\u0439", "\u043d\u0435\u0439",
                "\u043d\u0435\u0451", "\u043d\u0435\u0435", "\u043d\u0435\u044e", "\u0435\u044e"}


# ---------------------------------------------------------------- parsing
def read_text(path):
    if path == "-":
        return sys.stdin.read()
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def split_lines(text):
    """Return prose lines as dicts and beat-marker events. Skips front matter, code fences, headings,
    HTML comments (except beat markers, which are recorded and removed)."""
    raw = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    lines, in_code, in_comment, in_front = [], False, False, False
    for idx, line in enumerate(raw, start=1):
        if idx == 1 and line.strip() == "---":
            in_front = True
            lines.append({"n": idx, "text": "", "blank": True, "markers": []})
            continue
        if in_front:
            if line.strip() == "---":
                in_front = False
            lines.append({"n": idx, "text": "", "blank": True, "markers": []})
            continue
        if line.strip().startswith("```"):
            in_code = not in_code
            lines.append({"n": idx, "text": "", "blank": True, "markers": []})
            continue
        if in_code:
            lines.append({"n": idx, "text": "", "blank": True, "markers": []})
            continue
        markers = []
        # record beat markers with their column, then blank them out (keep columns stable)
        def _mark(m):
            markers.append((m.start(), int(m.group(1) or m.group(2))))
            return " " * (m.end() - m.start())
        line = BEAT_RE.sub(_mark, line)
        # strip other HTML comments, possibly multi-line
        out, i = [], 0
        while i < len(line):
            if in_comment:
                j = line.find("-->", i)
                if j == -1:
                    out.append(" " * (len(line) - i)); i = len(line)
                else:
                    out.append(" " * (j + 3 - i)); i = j + 3; in_comment = False
            else:
                j = line.find("<!--", i)
                if j == -1:
                    out.append(line[i:]); i = len(line)
                else:
                    out.append(line[i:j]); i = j; in_comment = True
                    out.append("    "); i += 4
        line = "".join(out)
        stripped = line.strip()
        is_heading = stripped.startswith("#")
        blank = (not stripped) or is_heading or bool(re.fullmatch(r"[-*_=\s]{3,}", stripped))
        lines.append({"n": idx, "text": "" if is_heading else line, "blank": blank, "markers": markers})
    return lines


def paragraphs_of(lines):
    paras, cur = [], []
    for ln in lines:
        if ln["blank"]:
            if cur:
                paras.append(cur); cur = []
        else:
            cur.append(ln)
    if cur:
        paras.append(cur)
    return paras


OPEN_CLOSE = {"\u201c": "\u201d", "\u00ab": "\u00bb", "\u201e": "\u201c"}
DASHES = ("\u2014", "\u2013")


def mask_dialogue(para):
    """Return masked copies of the paragraph's lines: spoken text and *italic* thoughts become spaces."""
    masked, state = [], None  # state: None or the closing quote char
    for ln in para:
        text = ln["text"]
        chars = list(text)
        stripped = text.lstrip()
        # dash dialogue: "- Speech, - narration. - Speech."
        if stripped[:1] in DASHES and state is None:
            start = len(text) - len(stripped)
            parts = re.split(r"(\s[\u2014\u2013]\s)", stripped[1:])
            pos, speech = start + 1, True
            for part in parts:
                if re.fullmatch(r"\s[\u2014\u2013]\s", part):
                    speech = not speech
                elif speech:
                    for k in range(pos, pos + len(part)):
                        chars[k] = " "
                pos += len(part)
            masked.append("".join(chars))
            continue
        for k, ch in enumerate(chars):
            if state is None:
                if ch == '"':
                    state = '"'; chars[k] = " "
                elif ch in OPEN_CLOSE:
                    state = OPEN_CLOSE[ch]; chars[k] = " "
            else:
                closing = ch == state
                chars[k] = " "
                if closing:
                    state = None
        line = "".join(chars)
        line = re.sub(r"(?<![*\w])\*(?!\s)[^*]+?(?<!\s)\*(?![*\w])", lambda m: " " * len(m.group(0)), line)
        line = re.sub(r"(?<![_\w])_(?!\s)[^_]+?(?<!\s)_(?![_\w])", lambda m: " " * len(m.group(0)), line)
        masked.append(line)
    return masked


def context(text, start, end, width=38):
    a, b = max(0, start - width), min(len(text), end + width)
    snippet = text[a:b].strip()
    return ("..." if a > 0 else "") + re.sub(r"\s+", " ", snippet) + ("..." if b < len(text) else "")


def detect_language(text):
    cyr, lat = len(CYR_RE.findall(text)), len(LAT_RE.findall(text))
    return "ru" if cyr > lat else "en"


# ---------------------------------------------------------------- checks
def check_patterns(paras, findings):
    for para in paras:
        masked = mask_dialogue(para)
        for ln, mtext in zip(para, masked):
            taken = []
            for cat, rid, lang, rx, sev, msg in COMPILED:
                for m in rx.finditer(mtext):
                    if any(m.start() < e and s < m.end() for s, e in taken):
                        continue
                    if rid == "then":
                        head = mtext[:m.start()]
                        clause = re.split(r"[.!?;]", head)[-1]
                        if re.search(r"\bif\b", clause, FLAGS):
                            continue
                    taken.append((m.start(), m.end()))
                    findings.append({
                        "category": cat, "rule": rid, "severity": sev, "line": ln["n"], "col": m.start() + 1,
                        "match": ln["text"][m.start():m.end()], "context": context(ln["text"], m.start(), m.end()),
                        "message": msg})


def check_beats(lines, findings):
    words = OrderedDict((str(b), 0) for b in range(1, 9))
    unmarked, current, seen, first_line = 0, None, [], None
    for ln in lines:
        text, markers = ln["text"], sorted(ln["markers"])
        cuts = [0] + [c for c, _ in markers] + [len(text)]
        beats = [current] + [b for _, b in markers]
        for (a, b), beat in zip(zip(cuts, cuts[1:]), beats):
            n = len(WORD_RE.findall(text[a:b])) if not ln["blank"] or markers else 0
            if beat is None:
                unmarked += n
            else:
                words[str(beat)] += n
        for _, b in markers:
            current = b
            seen.append(b)
            if first_line is None:
                first_line = ln["n"]
    result = {"present": bool(seen), "words": dict(words), "percent": {}, "unmarked_words": unmarked,
              "missing": [], "warnings": []}
    if not seen:
        return result
    total = sum(words.values())
    if total == 0:
        return result
    pct = {k: round(100.0 * v / total, 1) for k, v in words.items()}
    result["percent"] = pct
    result["missing"] = [int(k) for k, v in words.items() if v == 0]
    opening = pct["1"] + pct["2"]
    bottom = pct["3"] + pct["4"] + pct["5"] + pct["6"]
    line = first_line or 1
    if opening > 25:
        msg = "beats 1-2 take %.0f%% of the words (> 25%%): the scene starts too early, enter closer to beat 3" % opening
        result["warnings"].append(msg)
        findings.append({"category": "beat_weight", "rule": "opening_heavy", "severity": "medium", "line": line,
                         "col": 1, "match": "B1+B2 %.0f%%" % opening, "context": "", "message": msg})
    if bottom < 50:
        msg = "beats 3-6 take %.0f%% of the words (< 50%%): the descent is too thin, the bulk belongs in 3-6" % bottom
        result["warnings"].append(msg)
        findings.append({"category": "beat_weight", "rule": "bottom_thin", "severity": "medium", "line": line,
                         "col": 1, "match": "B3-B6 %.0f%%" % bottom, "context": "", "message": msg})
    if result["missing"]:
        msg = "no words under beat(s) %s: missing beat or missing marker" % ", ".join(map(str, result["missing"]))
        result["warnings"].append(msg)
        findings.append({"category": "beat_weight", "rule": "missing_beat", "severity": "low", "line": line,
                         "col": 1, "match": "", "context": "", "message": msg})
    if unmarked and total and unmarked > 0.1 * (total + unmarked):
        result["warnings"].append("%d words before the first marker are not counted" % unmarked)
    return result


def tense_counts(para, masked):
    past, present, samples = 0, 0, {"past": [], "present": []}
    prev = None
    for ln, mtext in zip(para, masked):
        for m in WORD_RE.finditer(mtext.replace("\u2019", "'")):
            tok = m.group(0).lower()
            kind = None
            if tok in PAST_AUX:
                kind = "past"
            elif tok in PRES_AUX:
                kind = "present"
            elif tok in IRREGULAR_PAST:
                kind = "past"
            elif prev in SUBJECT_3S | SUBJECT_OTHER and tok.endswith("ed") and len(tok) > 3 and tok not in ED_EXCEPT:
                kind = "past"
            elif prev in SUBJECT_3S and tok.endswith("s") and not tok.endswith("ss") and len(tok) > 2 \
                    and tok not in NOT_VERB_S:
                kind = "present"
            elif prev in SUBJECT_OTHER and tok in COMMON_BASE:
                kind = "present"
            if kind == "past":
                past += 1
            elif kind == "present":
                present += 1
            if kind and len(samples[kind]) < 3:
                samples[kind].append("L%d '%s'" % (ln["n"], m.group(0)))
            prev = tok
    return past, present, samples


def pov_counts(masked):
    first = third = 0
    for mtext in masked:
        for m in WORD_RE.finditer(mtext):
            tok = m.group(0).lower()
            if tok in FIRST_PERSON:
                first += 1
            elif tok in THIRD_PERSON:
                third += 1
    return first, third


def check_tense_pov(paras, lang, expect_tense, expect_pov, findings):
    rows = []
    for para in paras:
        masked = mask_dialogue(para)
        past, present, samples = tense_counts(para, masked) if lang == "en" else (0, 0, {})
        first, third = pov_counts(masked)
        if first >= 2 and first >= 0.3 * (first + third):
            pov = "first"
        elif third >= 2 and first == 0:
            pov = "third"
        else:
            pov = None
        rows.append({"line": para[0]["n"], "past": past, "present": present, "samples": samples,
                     "first": first, "third": third, "pov": pov})
    narration = {"tense": None, "tense_source": None, "pov": None, "pov_source": None}

    if lang == "en":
        tp, tr = sum(r["past"] for r in rows), sum(r["present"] for r in rows)
        if expect_tense:
            narration["tense"], narration["tense_source"] = expect_tense, "expected"
        elif tp + tr:
            narration["tense"], narration["tense_source"] = ("past" if tp >= tr else "present"), "detected"
        main = narration["tense"]
        if main:
            other = "present" if main == "past" else "past"
            for r in rows:
                total = r["past"] + r["present"]
                if total >= 4 and r[other] / float(total) >= 0.6:
                    findings.append({
                        "category": "tense", "rule": "tense_flip", "severity": "medium", "line": r["line"], "col": 1,
                        "match": "%s %d / %s %d" % (other, r[other], main, r[main]),
                        "context": ", ".join(r["samples"].get(other, [])),
                        "message": "paragraph reads in %s tense while the narration is %s" % (other, main)})
                elif total >= 6 and min(r["past"], r["present"]) / float(total) >= 0.35:
                    findings.append({
                        "category": "tense", "rule": "tense_mix", "severity": "low", "line": r["line"], "col": 1,
                        "match": "past %d / present %d" % (r["past"], r["present"]),
                        "context": ", ".join(r["samples"].get(other, [])),
                        "message": "past and present mixed inside one paragraph: check each verb"})

    classified = [r["pov"] for r in rows if r["pov"]]
    if expect_pov:
        narration["pov"], narration["pov_source"] = expect_pov, "expected"
    elif classified:
        narration["pov"] = "first" if classified.count("first") > classified.count("third") else "third"
        narration["pov_source"] = "detected"
    main = narration["pov"]
    if main:
        for r in rows:
            if main == "third" and r["pov"] == "first":
                findings.append({
                    "category": "pov", "rule": "pov_first_in_third", "severity": "medium", "line": r["line"],
                    "col": 1, "match": "first %d / third %d" % (r["first"], r["third"]), "context": "",
                    "message": "first-person narration in a third-person text: POV drift, or an unmarked "
                               "letter / diary / thought?"})
            elif main == "first" and r["pov"] == "third" and r["third"] >= 4:
                findings.append({
                    "category": "pov", "rule": "narrator_absent", "severity": "low", "line": r["line"], "col": 1,
                    "match": "first %d / third %d" % (r["first"], r["third"]), "context": "",
                    "message": "the first-person narrator vanishes here: check the POV has not slipped into "
                               "another character's head"})
    return narration


# ---------------------------------------------------------------- report
CATEGORY_TITLES = OrderedDict([
    ("connector", "Weak sequence connectors -> check the joint (references/causality.md), not just the word"),
    ("telling", "Telling instead of showing -> references/prose-checks.md, 'Show, don't tell'"),
    ("beat_weight", "Beat weight -> references/circle.md, 'Beat weight'"),
    ("tense", "Tense -> references/prose-checks.md, 'Tense holds'"),
    ("pov", "POV -> references/prose-checks.md, 'POV does not jump'"),
])


def human_report(res):
    out = []
    n = res["narration"]
    out.append("prose_lint: %s  (language: %s, %d words, %d paragraphs)" % (
        res["file"], res["language"], res["words"], res["paragraphs"]))
    tense = "%s (%s)" % (n["tense"], n["tense_source"]) if n["tense"] else ("n/a" if res["language"] != "en" else "unknown")
    pov = "%s person (%s)" % (n["pov"], n["pov_source"]) if n["pov"] else "unknown"
    out.append("Narration: tense %s | POV %s" % (tense, pov))
    b = res["beats"]
    if b["present"]:
        out.append("Beat weight: " + "  ".join("B%s %s%%" % (k, v) for k, v in b["percent"].items())
                   + "   (B1-2 %.0f%%, B3-6 %.0f%%)" % (
                       sum(b["percent"].get(k, 0) for k in "12"), sum(b["percent"].get(k, 0) for k in "3456")))
    else:
        out.append("Beat weight: no beat markers ([B1]..[B8] or <!-- B1 -->) found, skipped")
    out.append("")
    for cat, title in CATEGORY_TITLES.items():
        items = [f for f in res["findings"] if f["category"] == cat]
        if not items:
            continue
        out.append("== %s (%d)" % (title, len(items)))
        for f in items:
            loc = "L%d:%d" % (f["line"], f["col"])
            line = "  %-9s %-6s %-22s %s" % (loc, f["severity"], f["rule"], f["message"])
            out.append(line)
            detail = f["context"] or ""
            if f["match"] and f["category"] in ("connector", "telling"):
                detail = '"%s"  %s' % (f["match"], detail)
            elif f["match"]:
                detail = ("%s  %s" % (f["match"], detail)).strip()
            if detail:
                out.append("            " + detail)
        out.append("")
    s = res["summary"]
    out.append("Summary: %d finding(s): high %d, medium %d, low %d. Hits are candidates; read each in context."
               % (s["total"], s["high"], s["medium"], s["low"]))
    return "\n".join(out)


def lint(text, name, lang="auto", expect_tense=None, expect_pov=None):
    lines = split_lines(text)
    paras = paragraphs_of(lines)
    prose = "\n".join(ln["text"] for ln in lines if not ln["blank"])
    language = detect_language(prose) if lang == "auto" else lang
    findings = []
    check_patterns(paras, findings)
    beats = check_beats(lines, findings)
    narration = check_tense_pov(paras, language, expect_tense, expect_pov, findings)
    cat_rank = {c: i for i, c in enumerate(CATEGORY_TITLES)}
    findings.sort(key=lambda f: (cat_rank[f["category"]], f["line"], f["col"]))
    summary = {"total": len(findings)}
    for sev in SEVERITY_ORDER:
        summary[sev] = sum(1 for f in findings if f["severity"] == sev)
    for cat in CATEGORY_TITLES:
        summary[cat] = sum(1 for f in findings if f["category"] == cat)
    return {"file": name, "language": language, "words": len(WORD_RE.findall(prose)), "paragraphs": len(paras),
            "narration": narration, "beats": beats, "findings": findings, "summary": summary}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Surface checks for fiction prose (ai-book-writer).")
    ap.add_argument("file", help="text or markdown file, or - for stdin")
    ap.add_argument("--json", action="store_true", help="print machine-readable JSON")
    ap.add_argument("--lang", choices=["auto", "en", "ru"], default="auto",
                    help="prose language (tense check runs for English only)")
    ap.add_argument("--expect-tense", choices=["past", "present"], help="narration tense declared by the book profile")
    ap.add_argument("--expect-pov", choices=["first", "third"], help="narration POV declared by the book profile")
    ap.add_argument("--strict", action="store_true", help="exit 1 when any high or medium finding remains")
    args = ap.parse_args(argv)
    try:
        text = read_text(args.file)
    except OSError as exc:
        print("prose_lint: cannot read %s: %s" % (args.file, exc), file=sys.stderr)
        return 2
    res = lint(text, args.file, args.lang, args.expect_tense, args.expect_pov)
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print(human_report(res))
    if args.strict and (res["summary"]["high"] or res["summary"]["medium"]):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
