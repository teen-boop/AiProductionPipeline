# Poster devices — distilled from the liked reference library

Each device is one visual idea a poster is built on. A strong poster uses ONE main device (sometimes a second, quieter one) plus one
typography layout. The ids are stable so prompts and notes can refer to them. Update this file only from references listed in
`LIKED.md` (the user's favourites).

## A. Image devices

| id | Device | What it looks like | Copy-ready art direction |
|---|---|---|---|
| D01 | **Object replaces the head** | A figure whose head is a tree, a cloud of threads, a helmet with a glowing visor | `a figure in a dark coat whose head is replaced by <object>, the object grows naturally from the collar, photographed, not illustrated` |
| D02 | **Lone figure in fog** | One small figure in a vast misty field, everything else soft and pale | `a single small figure stands in a wide misty field of tall grass, everything beyond 20 m dissolves in white fog, muted greens` |
| D03 | **Silhouette window (double exposure)** | A dark silhouette (hooded figure, profile) filled with a whole second scene | `the dark silhouette of <figure> fills the frame; inside the silhouette, as a clean double exposure, <second scene>; plain pale background around it` |
| D04 | **Shard reveal** | Sharp triangles or slits cut into a plain page, each showing a fragment of a face | `a plain off-white paper surface with three sharp triangular cut-outs; through each cut-out we see a fragment of the same face: an eye, the lips, the nose` |
| D05 | **Torn collage** | Black-and-white face fragments torn and layered, one red circle, handwriting accents | `a black-and-white collage of torn photo fragments of the same face, layered off-register, one solid red circle behind them, paper grain` |
| D06 | **Single colour field** | The whole poster one saturated colour; the subject is a silhouette or one textured object | `the whole frame is a single saturated <colour> field; a <subject> rendered only in that colour family with deep shadows` |
| D07 | **Censor bar** | A flat red bar over the face of an otherwise documentary photo | `a documentary photo of <figure> seen from behind or front; a flat solid red rectangle covers the head` |
| D08 | **Wedge of light** | A dark room, one hard triangle of light on the floor, a tiny figure at its edge | `a dark empty room; one hard triangular wedge of warm light falls across the floor from a door; a tiny figure stands at the edge of the light` |
| D09 | **The still one** | A motion-blurred crowd; one person perfectly sharp and still | `a crowded street shot at a slow shutter, everyone streaks past as blur; one person in the middle stands perfectly still and sharp` |
| D10 | **Spotlight circle in a crowd** | A grey documentary crowd; one face inside a coloured circle | `a monochrome crowded train interior; one tired face is inside a solid red circle that keeps its colour while everything else is grey` |
| D11 | **Surreal object in a landscape** | Mirrors / doors / monoliths standing in a misty field or water | `dozens of tall mirrors stand upright in a misty boggy field, reflecting the grey sky, puddles in front` |
| D12 | **Light stripes from above** | A tiny figure seen from high above, crossing bars of hard light and shadow | `top-down view of a tiny figure crossing a floor striped by hard bars of golden light and black shadow, long shadows` |
| D13 | **Glow silhouette** | A soft-focus profile silhouette backlit by a single coloured glow | `a soft out-of-focus profile silhouette against a deep red-orange glow, halation, film grain, minimal` |
| D14 | **Prop as the world** | One giant textured prop fills the poster (a coat whose folds become mountain ridges) | `an extreme close-up of <prop> whose texture becomes a landscape: <detail>, a figure tiny on it` |
| D15 | **Uncanny corridor** | A yellowed office corridor in deep perspective, a face looming close at one side | `a sickly yellow empty office corridor with fluorescent panels in deep perspective; a man's face huge and close at the left edge, half out of frame` |

## B. Typography layouts (rendered in code, never by the generator)

| id | Layout | Seen in | compose_poster.py |
|---|---|---|---|
| T1 | Thin caps, very wide tracking, top | FILM TITLE A, FILM TITLE B (bottom variant) | `--layout wide-top` |
| T2 | Heavy condensed caps filling the width, bottom, accent colour | FILM TITLE C, FILM TITLE D | `--layout giant-bottom` |
| T3 | Small elegant serif in negative space, centre | FILM TITLE E, FILM TITLE F | `--layout serif-center` |
| T4 | Stacked grotesk words down one side, tight leading | a stacked three-word title | `--layout side-vertical` |

Common to all: a credit block in tiny tracked caps at the bottom, a date line in the accent colour, and generous negative space. The
title never covers the subject's face.

## C. Palettes seen

- Fog green + grey + one warm glow (helmet visor, flowers).
- Black and white + one red element (bar, circle, wedge).
- One saturated field: orange, red, yellow.
- Monochrome grey crowd + one red.
- Teal night + amber.

## D. Composition rules

- One idea, readable at thumbnail size (cover the text: does the image still say something?).
- The subject is small OR the subject is a fragment — never a medium "standing hero" shot.
- 40–60% negative space (fog, sky, a flat field, paper).
- Real photographic texture: film grain, paper grain, fog; no glossy CGI.
