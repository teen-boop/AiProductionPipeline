# ARCHETYPE · vox-clip

## 1. IDENTITY
- **Name:** `vox-clip`
- **Mood:** documentary explainer, calm, one detail per frame
- **For source:** a short fact, a video frame, one quote-fact from an article
- **Origin:** sample reference (a freeze frame from a news explainer video
  with a newspaper clipping inset)

## 2. SURFACE
Not a table — **a light stage**: light beige paper with a barely visible grid
(thin lines, the ruling of a paste-up table), and on top — a dark torn strip
(a scrap of another sheet) crossing the top edge of the frame as a framing.
The clipping is **one cut-out fragment**, not the whole page.

## 3. TYPE
- Source masthead: bold serif, small, in the corner of the clipping ("The Guardian")
- Headline: bold serif, large, 1 line, sentence case (not all caps)
- Byline: serif, italic on the name, regular weight
- Date: thin serif, small, under the byline
- Studio caption/brand mark (optional) — thin caps in the corner of the frame

## 4. PALETTE
Base — warm beige/cream. Ink — dark grey/black. **Accent —
red**, exactly one rectangular highlight block behind part of the headline.

## 5. IMAGERY TREATMENT
A photo is not required in this archetype — the reference carries none at all.
If needed — halftone b/w, small, supporting, not the hero of the frame.

## 6. ANNOTATION DEVICE
**A rectangular highlighter block** behind part of the headline (not the whole
line — specifically the key phrase), the hot color goes behind the letters,
the letters stay on top.

**⚠️ If the frame will later be animated** (the highlighter must slide in/
be drawn on as a separate motion, rather than being a finished detail of a
static image) — **do not bake the highlight into the generation at all**. The
static frame carries only the printed text with no color block behind it; the
highlighter itself is added as a separate layer in Remotion (width shift,
timing, multiply), as a separate animated layer. Otherwise you get
two highlighters — the drawn one and the animated one — or you have to clean
out the drawn one before overlaying the animated one, which is unnecessary.
Ask/clarify before generating: is this frame the final image or a base plate
for animation?

## 7. LAYOUT COMPLEXITY
Minimal. One clipping: masthead + headline + byline + date.
No article body. This is a direct application of the text-in-image law: the
headline is the only large text, everything else is just service captions.

**Addendum (a web card with a dek paragraph):**
the source sometimes carries a coherent paragraph under the headline that is
the substance of the material, not decorative filler. **Rule: if the paragraph
is the reason the frame exists at all, it goes into the generation as real
readable text, in a large legible font, as a second zone of the same clipping
(masthead+headline on top, paragraph below — as one and the same cut-out piece
of the page, not two different clippings).** Illegible texture (see
`editorial-broadsheet §8`) remains the default **only for decorative filler** —
when the source has no paragraph but the empty space still needs to be covered
with paper texture. As soon as the source has a meaningful paragraph, the
default switches to real text. Do not decide on your own that it is
"unimportant": if the user sent text and asks for it to be inserted, it is
important by definition.

## 8. TEXT FIDELITY RISK
Low. All readable text is a one-line headline (5–9 words) plus a
short byline. The model handles this reliably if the font is large and bold.
The risk is concentrated on the **name in the byline** — the generator can
distort a short name of a real person by 1–2 letters; when the cost of an
error is high (a real person) — set the byline by code over an empty line,
as in §9-B.

## 9. FILL-IN PROMPT TEMPLATE

**9-A — with text from the model** (for non-critical sources, the name is not a real person):
```
Generate ONE image, 16:9 landscape, 2K.

SCENE: a single torn news clipping pasted on a plain light beige stage with a
faint grid ruling barely visible beneath it, photographed straight down. A
dark torn strip of paper crosses the very top edge of the frame like a loose
overlapping sheet. The clipping itself sits in the lower-left two thirds of
the frame: a small bold serif publication wordmark "{SOURCE_NAME}" at the top
of the clipping, below it one bold serif headline on a single line reading
"{HEADLINE}", with a solid red rectangular highlight block directly behind
the words "{HIGHLIGHT_PHRASE}" (the highlight sits behind the letters, ink
stays on top). Below the headline, a smaller byline line "{BYLINE}" in
serif italic, and a thin date line "{DATE}" beneath it.

STYLE: warm cream paper, dark ink type, matte print texture, faint paper
grain, soft flat lighting, no gloss, no 3D, no glossy screen glare.

CRITICAL: every visible word must be exactly one of the strings given above.
No body paragraphs, no extra headlines, no lorem ipsum, no invented words,
no watermark, no logos beyond the named publication wordmark, no UI chrome.
```

**9-B — with a real name/date** (a rule from practice: we do not trust the
generator with real names — leave an empty line, fill it in by code):
```
[the same prompt, but:]
below the headline, leave a clean empty line of matching width where a
byline would go — completely blank, no placeholder text — and a second
shorter empty line beneath it for a date. No text of any kind in either
blank line.
```

**9-C — without the highlight, for later highlighter animation** (the default
when the frame is a base plate for Remotion rather than the final image):
```
[the same prompt, but remove entirely:]
"with a solid red rectangular highlight block directly behind the words
{HIGHLIGHT_PHRASE} (the highlight sits behind the letters, ink stays on top)"

[replace with:]
the headline is printed plainly, no colour block behind any part of it —
every word the same flat ink colour, no emphasis device baked into the image.

[and add to CRITICAL:]
No highlighting, no coloured background block, no underline, no circle or
any other annotation mark anywhere in the image — the annotation is added
separately afterward. The plain text must still read as exactly
"{HEADLINE}" so the phrase "{HIGHLIGHT_PHRASE}" is identifiable within it
for that later step.
```

## 10. VERIFIED
⚠️ Not verified by render. A direct analogue of the proven mechanics from the
"text set in code" approach — the same "no names to the generator"
principle, carried over here as a rule, not a hypothesis.
