# ARCHETYPE — schema

A fixed set of slots for one visual archetype of newspaper/magazine
stylization. The slots do not change — the values do. Every archetype in
`references/archetypes/` fills in these ten items.

---

## 1. IDENTITY
- **Name:** `<kebab-case>`
- **Mood:** 3–5 words
- **Which screenshot source it suits:** social media post / article /
  document / chat / video frame / photo — specifically, not "universal"
- **Origin:** which reference(s) gave rise to the archetype

## 2. SURFACE — what the clipping lies on
Table (photographed) / flat solid background in a brand color / ruled
paper stage / document card. In numbers: if paper — its condition (dirt,
wear, bending — with a caveat from practice: a fold breaks the straightness
of lines, acceptable only if the scene does not carry small precise text).

## 3. TYPE — hierarchy
The order is always: **masthead → headline → dek/byline/date → (opt.) body**.
For each level: the typeface character (condensed bold / blackletter /
serif / sans), case, position.

## 4. PALETTE
Base + ink + **one hot accent** (in this genre almost always red —
confirmed independently in 6 of 8 references). The accent is reserved
**only** for the annotation device (see §6) — never a decorative fill.

## 5. IMAGERY TREATMENT
What a photograph inside the clipping looks like in this archetype: halftone
b/w print (grain, screen) — or a real color photo — or an illustration/comic
panel. This is decided **per archetype**, not the same for all.

## 6. ANNOTATION DEVICE — what carries meaning on top of the print
Exactly one technique per archetype, the one that sets it apart from the
others: highlighter · hand-drawn circle/underline · redaction bar ·
rubber stamp · torn/lifted corner revealing the text beneath it.

## 7. LAYOUT COMPLEXITY
A single clipping (one detail) — or a full multi-column page.
This directly determines the amount of text that will have to be generated.

## 8. TEXT FIDELITY RISK
**Mandatory slot.** How much real readable text the archetype demands from
the model, and how reliable that is:
- headline in a large bold font, 2–6 words — low risk
- byline/date, small, a short line — medium risk
- dense multi-column text — high risk, the model systematically either
  mixes up letters in names or inserts readable lorem ipsum
  (confirmed many times in practice)

## 9. FILL-IN PROMPT TEMPLATE
A ready template in English with `{PLACEHOLDERS}`, reproducing the structure
of §2–§7 in a single block, with an explicit critical-list of prohibitions at
the end.

## 10. VERIFIED
What is confirmed by render and what is a hypothesis. A new archetype always
starts with the mark "not verified".
