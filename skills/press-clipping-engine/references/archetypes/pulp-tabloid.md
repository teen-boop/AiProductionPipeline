# ARCHETYPE · pulp-tabloid

## 1. IDENTITY
- **Name:** `pulp-tabloid`
- **Mood:** loud, dramatic, a screaming headline, tabloid energy
- **For source:** a sensational fact, a meme-style exposé, one striking
  number/statement that demands maximum visual loudness
- **Origin:** sample reference A (a fan-made tabloid front page),
  sample reference B (a comic-style newspaper mockup)

## 2. SURFACE
A full page, dense, no torn edges and no table — a clean print mockup,
like editorial-broadsheet, but **noisier and rougher** in its typography.

## 3. TYPE
- Masthead: ornamental/blackletter OR bold condensed caps, often with
  boxes on the sides ("EXTRA EDITION", price, weather)
- Main headline: **huge, bold condensed caps, 1–2 lines**, may
  take up a third of the page height — literally the largest text
  in the whole genre
- Subhead: bold serif italic under the main headline
- Side teasers: a boxed caps label + a short bold headline + "Page N"
- An exclusive star/starburst badge (optional)

## 4. PALETTE
Black-and-white base (newsprint), **red** — the only colored element,
given entirely to §6.

## 5. IMAGERY TREATMENT
The central image is a **halftone b/w print**, large, dramatic
(creature/event/character), or an illustration in the spirit of a comic
panel — never a clean color photo.

## 6. ANNOTATION DEVICE
**A hand-drawn red mark directly over the headline or page**: an uneven
freehand ellipse/circle around part of the headline, OR an underline of one
word, OR a rectangular frame around a short inner teaser. Two passes,
uneven pressure — a wax-pencil line with a dry, broken edge.

## 7. LAYOUT COMPLEXITY
Medium-high: one dominant headline + 3–5 side teaser headlines
(no body) + one large image. Less continuous text than
editorial-broadsheet — the teasers are short, no paragraphs.

## 8. TEXT FIDELITY RISK
Medium. The main headline is large and reliable (exactly what the genre demands).
The risk is in the side teasers: 4–5 short lines, each must remain a
meaningful short phrase. The article body at the bottom of the page (if any) —
treat it as in editorial-broadsheet: illegible texture, not lorem ipsum.

## 9. FILL-IN PROMPT TEMPLATE
```
Generate ONE image, 16:9 landscape, 2K.

SCENE: a dense tabloid front page, photographed flat, filling the frame. A
bold masthead reading "{MASTHEAD}" across the top, flanked by a small boxed
label "{EDITION_LABEL}" on one side. Beneath it, ONE giant bold condensed
all-caps headline spanning almost the full width, reading "{HEADLINE}",
occupying roughly a third of the page height. A red hand-drawn rough circle
(two uneven passes, wax-pencil texture) encircles the phrase "{CIRCLED_WORDS}"
within that headline. Below the headline, a smaller bold italic subhead
reading "{SUBHEAD}", with a thin red hand-drawn underline beneath one word
of it. A large black-and-white halftone-print photograph fills the center of
the lower page: {PHOTO_DESCRIPTION}. Down the left side, a boxed sidebar
with a small caps label "{SIDEBAR_LABEL}" and three short teaser headlines:
"{TEASER_1}", "{TEASER_2}", "{TEASER_3}", each followed by a small "Page {N}".

STYLE: aged black-and-white newsprint, heavy ink contrast, visible halftone
dot pattern in the photo, matte, no gloss, no colour anywhere except the red
hand-drawn marks described above.

CRITICAL: every headline and label above must render exactly as given, no
misspellings, no extra words. The red mark must be the ONLY colour in the
frame. No lorem ipsum, no invented words, no body paragraphs beyond the
teasers listed, no watermark, no logos beyond the named masthead.
```

## 10. VERIFIED
⚠️ Not verified by render. The red hand-drawn circling in two uneven passes is a
common annotation technique; confirm it by a test render in this project
(check the circle at full size).
