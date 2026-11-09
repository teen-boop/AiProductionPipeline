# ARCHETYPE · redacted-dossier

## 1. IDENTITY
- **Name:** `redacted-dossier`
- **Mood:** official document, secrecy, investigation
- **For source:** a leak, an official document, a screenshot of a chat with
  sensitive content — when the fact "this is a document" matters more than "this is a
  newspaper"
- **Origin:** the cover of the book "REDACTED" (Calvin Harris)

## 2. SURFACE
A flat document card, light warm beige/cream background, no torn
edges and no table — designed as an official form, not as a newspaper clipping.
Two small round clip marks at the top (canvas/punch holes) — an optional
detail of the form's authenticity.

## 3. TYPE
- Top line: `CASE FILE {NUMBER} · {DIVISION}`, mono/caps, small
- Classification line: `CLASSIFICATION: {LEVEL} — DO NOT DISTRIBUTE`, small, muted
- **Stamped word** large in a black box, caps, maximum weight —
  the main visual anchor of the frame
- Headline under it: bold caps, large, but smaller than the stamp
- Body — a caps texture repeated many times across the whole card (see §8)
- A rubber stamp, small, at the bottom, rotated a few degrees
- Boxed meta labels at the bottom (caps, framed)

## 4. PALETTE
Warm beige background, black ink and black redaction bars, **red**
reserved strictly for the rubber stamp and one accent word in the caption.

## 5. IMAGERY TREATMENT
There are no images in this archetype at all — the reference is purely typographic.
If a photo is needed — halftone b/w, small, not the focus of the composition.

## 6. ANNOTATION DEVICE
**A redaction bar** (a black rectangle over a line of text) as the main
technique, and a **rubber stamp** as the secondary one. One of the bars has a
"torn/lifted corner" under which a few letters of the real word are visible —
the effect of the black tape physically peeling off.

## 7. LAYOUT COMPLEXITY
Medium: one stamp, one headline, several paragraphs of repeating
placeholder texture, several redaction bars within it, one rubber
stamp, two boxed labels.

## 8. TEXT FIDELITY RISK
**The lowest in the genre for body text — and this is a design feature,
not a workaround.** The body here is **by design** an illegible/repeating caps texture
(in the reference, literally service words like PENDING/UNVERIFIED/SOURCE
repeat in rows) — the model does not need to invent coherent prose, only
keep the rhythm of the caps lines. The risk is concentrated entirely on the
**stamped word** and the **headline** — both short and large, reliable.

## 9. FILL-IN PROMPT TEMPLATE
```
Generate ONE image, 4:5 portrait, 2K.

SCENE: a flat document card on a warm beige background, photographed
straight on. Two small circular punch-hole marks near the top edge. A thin
rule beneath a small header line reading "CASE FILE {NUMBER} · {DIVISION}",
and below it a smaller classification line reading "CLASSIFICATION:
{LEVEL} — DO NOT DISTRIBUTE". Centered below that, one large black
rectangular stamp block with bold white all-caps text reading "{STAMP_WORD}".
Beneath the stamp, a bold black all-caps headline reading "{HEADLINE}".

Below the headline, several lines of dense body copy made ENTIRELY of the
same short set of repeating all-caps filler words ({FILLER_WORDS_LIST},
comma separated, reused in varied order across the lines) — this is
intentional repeated-word texture standing in for classified text, not real
prose. Two or three solid black horizontal redaction bars overlap parts of
this text mid-line. One redaction bar near the middle of the page has its
right edge peeled back slightly like lifted tape, revealing a few real
letters underneath reading "{PEEK_LETTERS}".

Near the bottom, a small rotated red rubber-stamp badge with a thin double
border reading "{STAMP_PHRASE}", and two small boxed caps labels reading
"{META_LABEL_1}" and "{META_LABEL_2}".

STYLE: warm beige paper, black ink and black redaction blocks, one red
rubber-stamp accent, flat even lighting, matte, no gloss, light paper grain.

CRITICAL: the stamp word, the headline, the peek letters, the rubber-stamp
phrase and both meta labels must render exactly as given, no misspellings.
The repeating body texture must use ONLY the filler words listed — no other
real or invented words, no lorem ipsum. No watermark, no logos, no colour
beyond the single red stamp.
```

## 10. VERIFIED
⚠️ Not verified by render. The "redaction bar + repeating service words instead
of prose" technique directly uses a finding from an earlier project (`REDACTION` in pack
v0.2) — the only new part is the torn corner with letters peeking through, which
requires a separate check for failure (the model may produce readable text instead
of partially hidden text).
