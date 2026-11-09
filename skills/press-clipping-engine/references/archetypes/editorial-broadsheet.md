# ARCHETYPE · editorial-broadsheet

## 1. IDENTITY
- **Name:** `editorial-broadsheet`
- **Mood:** a real publication, clean, editorial, lots of material
  on one page
- **For source:** a long article, a thread, a digest — when you need to show
  "this is a real magazine" rather than a clipping of one quote
- **Origin:** "ORIGEN" (Spanish-language tabloid), "EXTRA KUNST"
  (German museum newspaper)

## 2. SURFACE
The whole full page, shot flat/almost flat (not a table, not a collage of
scraps) — the page itself is the frame. Cream/light paper with no dirt
and no torn edges — this is clean print design, not an archive.

## 3. TYPE
- Masthead: large, centered, serif or condensed serif, may be
  colored (red in ORIGEN) — the only place where the accent color is
  allowed in the type itself
- A thin rule under the masthead, under it a small italic tagline
- Section labels: caps, small, tracked
- Story headlines: bold serif/sans, of different sizes by story importance
- Byline: "by/por {AUTHOR}", small, under the headline
- Body: 2–4 lines per story, small serif — this is exactly the risk zone (§8)
- A page number/"page N" reference at the end of each block

## 4. PALETTE
Cream base, black ink, **one accent** — red, reserved for the
issue number/kicker labels, never floods large areas.

## 5. IMAGERY TREATMENT
**Real color or black-and-white photographs**, not a halftone screen — this
is clean editorial photography with ordinary continuous-tone printing, cropped
rectangularly, no torn edges.

## 6. ANNOTATION DEVICE
Here the annotation device is **absent** — the page itself is the finished
design. The hierarchy of importance is achieved by headline size and photo
area, not by a hand-drawn mark on top.

## 7. LAYOUT COMPLEXITY
**High.** 4–6 separate stories on one page, each with its own mini
hierarchy (label → headline → byline → body → page number).

## 8. TEXT FIDELITY RISK
**High, and this is a systemic limitation of the archetype, not chance.**
A multi-column body is unavoidable: either the model inserts readable lorem
ipsum (verified many times), or it distorts words. Two working paths:
- **A. Headlines as content, body as texture** — ask for real
  headlines of 2–4 stories (short, reliable), and everything below the byline
  demand as "illegible grey typographic texture, no lorem ipsum,
  nothing resolves into letters" — exactly the formula confirmed as working
  on an earlier project archive.
- **B. Blank page + code** — generate the whole page with empty text
  zones, overlay all the text as a layer on top (the most reliable, but goes
  beyond a single Nano Banana prompt — do not choose by default).
Path A is the default for this archetype.

## 9. FILL-IN PROMPT TEMPLATE
```
Generate ONE image, 16:9 landscape, 2K.

SCENE: a complete flat-lay newspaper/magazine front page, photographed
straight down, filling the frame edge to edge. Centered at top, a large bold
serif masthead reading "{MASTHEAD}", a thin rule beneath it, a small italic
tagline "{TAGLINE}" under the rule. Below, {N} distinct story blocks arranged
in a grid, each with a small all-caps section label, a bold headline, a
byline "by {AUTHOR}", and a short body paragraph. The dominant story (largest,
lower half) carries the headline "{LEAD_HEADLINE}" beside a large photograph
described as: {PHOTO_DESCRIPTION}.

Story headlines, exactly these and nothing else:
1. "{HEADLINE_1}" — byline "{AUTHOR_1}"
2. "{HEADLINE_2}" — byline "{AUTHOR_2}"
3. "{HEADLINE_3}" — byline "{AUTHOR_3}"

STYLE: cream paper, black ink, clean modern editorial typesetting, real
photographic imagery (not halftone), matte print finish, soft even lighting,
no gloss, no 3D render look.

CRITICAL: every headline and byline above must render exactly as given, no
misspellings. All body paragraph text beneath each headline must be
ILLEGIBLE grey typographic texture — the rhythm and line length of real
prose, but nothing may resolve into actual letters, and absolutely no lorem
ipsum or any real or invented words in the body copy. Page numbers may appear
as short digit groups only ("p. {N}"), never as words. No watermark, no logos
beyond the named masthead, no UI chrome.
```

## 10. VERIFIED
⚠️ Not verified by render. The formula "headline as real text / body as
forbidden lorem ipsum, illegible texture only" is carried over from
confirmed practice from an earlier project (`plateFLAT3`, the third attempt after two
failures with readable lorem ipsum).
