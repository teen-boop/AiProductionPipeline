# BOARD RECIPES · narration-aligned graphics for the CODE route

A board is one full-frame graphic that explains one beat of the narration: a process, a comparison, a number, a timeline, a
code excerpt, a quote. This file adds what the PROMPT-LIBRARY blocks do not cover:
- the seek contract every board must keep;
- how graphics lock to the voice;
- safe zones when a presenter or PiP camera shares the frame;
- the board brief chain;
- 18 board effects (BRD-01 to BRD-18) with exact structure, timing and easing for GSAP / HyperFrames.

The style still comes from the project's STYLE PACK. These recipes are mechanics, never a look.

Mechanics studied in the Eyeline board library (MIT, see the repository README), rebuilt here as recipes; no board files
are copied.

---

## 1. The seek contract (non-negotiable)

- The same time must produce the same pixels, also when seeking backward. No `setInterval`, no `Math.random()` at run time,
  no live network assets, no autoplaying video that runs on its own clock.
- HyperFrames: everything on the paused master timeline, `data-start`/`data-duration` on every timed layer. A plain HTML
  board exposes `window.seek(seconds)` that pauses all animations (`document.getAnimations()`, set `currentTime`) and sets
  every `<video>.currentTime`. Only touch a video when it is more than 35 ms off, or it stutters.
- Random-looking motion (scramble, mosaic, sparks) uses a seeded generator computed once at build time.
- CSS custom properties that animate (counters, spotlight or lens coordinates) must be registered with `@property`, or they
  jump instead of interpolating. GSAP tweens of plain objects with `onUpdate` are the safer route.
- Avoid the CSS `d: path()` animation (Chromium only); tween path data with GSAP instead.

## 2. Lock graphics to the voice

- **An element's in-time is the start of the word that names it.** Use word timings from the FINAL dialogue export
  (`dialogue-cut` / re-transcription), never from the script or a rough cut.
- **Minimum time on screen** for any text element: `max(1.5 s, 0.6 s + words / 3.2)`.
- **Never show an empty board.** The headline or the first element is there on frame one of the board.
- **Board to board:** the next board is opaque and fades in place over 0.38 s. Elements leave with a 0.28 to 0.35 s fade, or
  by collapsing to `scale 0.05` over 0.35 s.
- **Motion tokens:** one vocabulary per film, so motion reads as one system.

| Token | Values |
|---|---|
| pop | `y 14 -> 0`, `scale .985 -> 1`, 0.38 s `power3.out` |
| rise | `y 40 -> 0`, `scale .88 -> 1`, 0.75 s `power3.out` |
| stamp | from `scale 1.6, rotation -6`, 0.30 s `power4.out` |
| card | 0.50 s `back.out(1.5)` |
| write-on note | starts 0.25 s after its anchor, `+0.03 s` per character |
| arrow draw | duration = length in px / 900 |
| still tile | push-in `scale 1 -> 1.045`, linear over the whole hold |

- **CSS equivalents** when a board is pure CSS:
  - `power3.out` ≈ `cubic-bezier(.22,1,.36,1)`
  - `back.out` ≈ `cubic-bezier(.34,1.56,.64,1)`
  - `power3.inOut` ≈ `cubic-bezier(.65,0,.35,1)`
  - hard in-out ≈ `cubic-bezier(.76,0,.24,1)`
- **Sound on graphics:** a pop lands on the frame the element appears; a whoosh starts about 0.2 s early. Never put a sound on
  every element. Default is no SFX and no zoom unless the project asks for them.

## 3. Safe zones with a presenter or PiP camera (16:9, 1920×1080)

- 60 px outer margin. Title zone `x 60, y 64, 1800 × 112`. Credit or source line at `y 1040`, 18 px.
- Camera box lower right, `x 1400, y 704, 480 × 336`. Keep graphics out of `x >= 1240, y >= 586`. This gives an L-shaped
  layout: full width above y 586, only the left 1180 px below it.
- A full-screen insert hides the camera: fade the camera out 0.25 s before the insert and back in over 0.35 s after it.
- 9:16 (1080×1920): title at the top, one visual in the middle, the camera in the bottom 480 px, no text under 36 px.
- Never leave the guide box visible in a delivery. Check for overflow at full size and readability at a quarter size.

## 4. The board brief chain (one approval per step)

1. **Transcript → brief.** For every visual, fill in the following fields:
   - board id;
   - the exact narration passage;
   - one takeaway;
   - the exact headline and labels;
   - layout: process, comparison, chart, timeline, layers, code, evidence or recap;
   - data with units, baseline and full source;
   - camera clearance;
   - the assets it needs.

   Also list camera-only passages, where no board helps. Write `TIMING PENDING` until the final word timings exist and
   `NEEDS SOURCE` for any number without one. Never invent claims, quotes, testimonials, links or benchmark numbers.
2. **Brief → static board.** One self-contained HTML per board: inline CSS and SVG, real editable text, no external requests.
   No motion yet. The user approves the static layout.
3. **Static → motion.** Add motion only from the approved brief's narration anchors (section 2).
4. **Review.** Write each finding as `file → element → problem → fix → severity`. Open the rendered board, not the source.
   Check that seeking backward gives the same frame. A QA sweep at 30 fps looks for elements appearing early or staying late,
   overlaps over 3 px, and videos more than 0.18 s off their target time.

One recurring visual anchor (a ladder, a map, a shelf) that returns across many boards carries a long explainer better than
a new layout per beat.

---

## 5. Board effects

Each block: structure, then the animation. Times in seconds, at the film's frame rate (PROMPT-LIBRARY §0.1 rules apply).

### BRD-01 · Line opens into a frame (footage reveal)
Video inside a wrapper div. Wrapper `clipPath`:
1. `inset(49.6% 50% 49.6% 50%)` → `inset(49.6% 0% 49.6% 0%)` over 0.5 s (a hairline grows across);
2. → `inset(0% round 14px)` over 0.9 s `power4.inOut`.

In parallel from step 1, the inner video goes `scale 1.12 → 1` over 1.6 s `power3.out`.

### BRD-02 · Tile becomes the full frame (insert from a grid)
Before the cut, the full-frame clip sits in the grid at its tile's rectangle: `clipPath: inset(T R B L round 8px)` in pixels.
It opens to `inset(0 round 0)` over 0.75 s `power3.inOut`, starting 0.22 s before the line that motivates it. The camera
layer follows the rule in §3.

### BRD-03 · Iris with ripple
The next layer runs `clipPath: circle(0% at X Y)` → `circle(80%)` over 1.1 s `power4.inOut`. A ring centred on the same point
goes `scale 0 → 1` and `opacity 1 → 0` over 1 s `expo.out`. Put X Y on the subject that the next shot is about.

### BRD-04 · Brush-stroke reveal
SVG `<mask>` with 2 or 3 white Bézier paths (stroke width 80 to 220, round caps) over the image or headline group. Each path
runs `strokeDashoffset` from its length to 0 over 2.2 s `power3.inOut`, staggered by 0.12 s.

### BRD-05 · Word knockout into footage
A black layer with white display text and `mix-blend-mode: multiply` sits over the video; the footage shows through the
letters.
1. The word goes `scale 0.6 → 1`, letter-spacing `0.1em → -0.04em`.
2. Then `scale 1 → 3.2` over 1.4 s `power4.in`.
3. The layer's opacity goes to 0 over 0.8 s, starting 0.9 s into step 2.

### BRD-06 · Scramble decode
Each character cycles seeded glyphs from `#%&@$*+=01`, changing every 0.11 s. Character i locks at `0.2 + i × 0.24` s.
Drive it from one `tl.to(state, {p: 1, onUpdate})` so the frame is a pure function of time.

### BRD-07 · Liquid fill inside type
SVG `clipPath` made from a `<text>` element. Inside it:
- two wave paths loop `x -300` (2 s and 3.2 s, the second reversed, `ease none`);
- the group's `y` rises from 300 to -40 over 5.4 s `sine.inOut`.

A percent counter is tied to the same tween's progress.

### BRD-08 · Spotlight hop
A full-frame overlay:
`radial-gradient(circle at var(--sx) var(--sy), transparent calc(var(--sr) - 6px), rgba(12,12,14,.82) calc(var(--sr) + 30px))`.
1. Tween `--sx/--sy` from target to target over 1.2 s `power3.inOut`, with a 1.4 s hold on each.
2. To finish, open `--sr` from 150 px to 520 px.

### BRD-09 · Magnifier lens
A copy of the content at `scale 1.9` inside a layer clipped to `circle(120px at var(--lx) var(--ly))`, plus a lens rim ring at
the same coordinates. The coordinates tween over 2.6 s `power3.inOut` to the detail, then a label pops in (`back.out`).
Good for tables, screenshots and long lists.

### BRD-10 · Virtual camera with minimap
The content group gets `x`, `y` and `scale` moves (up to 2.4), 0.6 to 0.8 s each, `power3.inOut`. A small inset map draws a
rectangle that is the inverse of the view: width and height = 100% / scale, position = the view origin. It is tweened on the
same timeline. The viewer always knows where they are in a large diagram.

### BRD-11 · Line draw with a rider
Path drawn by `strokeDashoffset` over 2.4 s `power2.inOut`. A dot rides it (`motionPath {path, align}` or `offset-distance`)
with the same ease and duration. Node badges pop in (`scale 0 → 1`, `back.out(1.7)`) as the dot passes them, for example at
10%, 34% and 60%.

### BRD-12 · Cinematic open
Two black bars cover the top and bottom halves. They split to `yPercent -100 / +100` over 2 s `power4.inOut`. At +1.6 s the
title tracks in: `letterSpacing .5em → .18em`, `blur 14px → 0` and opacity, over 2 s `expo.out`.

### BRD-13 · Printed receipt / ticket
The paper is masked above. It runs `y -560 → 0` over 4.6 s with `ease: "steps(18)"`, a dot-matrix stutter. Then a stamp slams
in from `scale 2.4, rotation -14, opacity 0` over 0.25 s `power4.in`. Good for costs, totals and "what you get" lists.

### BRD-14 · Exploded layers
A parent with `perspective`. The group turns to `rotationX 14, rotationY -38`. The layers separate in `z`
(-240, -120, 0) over about 1.5 s `power3.inOut`, and labels fade in staggered by 0.3 s. Reverse to collapse. Shows that a
picture is built from layers (references, frame, grade, captions).

### BRD-15 · Gooey merge
SVG filter `feGaussianBlur stdDeviation 16` followed by
`feColorMatrix values="1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 22 -9"` on a group of circles. The circles tween from spread-out
positions to the centre over 3 s `power3.inOut`, stagger 0.05. Many inputs become one.

### BRD-16 · Squash and follow-through
A drop runs `y -420 → 0` over 0.5 s `power2.in`. On landing, `scaleX 1.25 / scaleY .75` for 0.08 s, then back (yoyo). A hanging
tag swings `rotation 16 → 0` with `elastic.out(1, .3)`. The shadow ellipse goes `scaleX .3 → 1.2 → 1`. For a product or icon
landing with weight.

### BRD-17 · Deck fan-out
N cards stacked with `transformOrigin "50% 120%"`. Each goes to `x (i - (N-1)/2) × 150` and `rotation (i - (N-1)/2) × 13` over
0.8 s `back.out(1.3)`, stagger 0.05. Options, variants, takes.

### BRD-18 · Odometer counter
Each digit is a 0 to 9 column inside an overflow window. `yPercent` runs to the target digit over 1.4 s `power3.out`,
staggered by 0.25 s from the right-most digit. Reads better than a count-up (VAL-02) for big round numbers.

**Pick per beat, not per film:** one hero effect per board, plus pop/rise tokens for the rest. Two hero effects on one board
compete.
