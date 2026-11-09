# Film look - the rules every category inherits

A graphic passes when a viewer cannot tell where the photography ends and the graphic begins. It fails when it looks like a
dashboard, a slide or a social sticker laid over a film. These rules apply to all nine categories; a category file only adds to them.

## 1. Where the look comes from (read, never redefine)

In this order, and quote what you read into the spec's `look.notes`:

1. **`STYLE_LOCK.json`** (`style-lock-guard`): the measured contrast, tonal range, shadow depth (p5), saturation and the share of
   warm light accents of the director's own reference frames. These numbers are targets for the graphic too.
2. **Style card** (`reference-style-builder`): palette as 60/30/10 with measured hex values, light, grain, film stock, negatives.
3. **`STYLE-PACK.md`** (`motion-style-core`): if the project has no motion pack yet, derive a "film pack" from 1 and 2 and fill
   the ten slots: BASE = the film's shadow tone, INK = its highlight tone (paper-white, not #FFFFFF), ACCENT = the warm practical
   colour (one element per frame), SURFACE = the film's grain, EDGE = how the film's light falls off. Mark it VERIFIED: no until a
   frame is rendered and compared.
4. **Graded frames of the actual neighbouring shots.** Sample black, mid and highlight with `video-color-grade`'s inspect_frame
   tool on the shot before and after the graphic. The graphic sits between them.

If none of these exist, stop and ask for the reference frames. Do not invent a "cinematic" palette.

## 2. Tone

- **Deep blacks.** The plate black of a full-frame graphic matches the film's p5 shadow (typically very dark, near #05-#0C), never a
  lifted charcoal grey. A flat, milky graphic between two contrasty shots is the most common failure.
- **Highlights are not white.** Type ink tops out at the film's highlight tone (a warm paper-white, for example #EDE3CF). Pure
  #FFFFFF reads as a computer.
- **Mid-tones carry texture**, not gradients: paper, linen, film grain, hatching.
- **Warm vs cool** follows the lock: if the film plays warm practicals against a cool ambient, a map or document plate is lit the
  same way (a warm pool of light from one side, cool falloff).

## 3. Grain, halation, vignette, optics

- **Grain** matches the plate in size and strength. Deterministic: a new seeded noise every frame, driven by the timeline, never by
  a clock or an unseeded random.
  - Full-frame graphic: one grain layer over everything.
  - Alpha overlay: grain lives **inside the ink only** (the footage already has its grain). A full-frame grain or vignette in an
    alpha file adds a grey veil over the whole shot; the render check measures this.
- **Halation**: when the film shows it, bright type gets a faint warm bloom (red-orange, 10-20 % alpha, 10-16 px at 1080p). Never
  a coloured glow, never on dark ink over paper.
- **Vignette**: on full-frame plates, a soft oval falloff matched to the film (usually 15-30 %). On overlays, none: the footage
  carries its own.
- **Optics**: a physical plate (paper map, document, drawing) behaves like a photographed prop: one focal plane, gentle falloff
  toward the far edge when the camera is tilted, oval bokeh and horizontal flare only if the film is anamorphic. Flat type is never
  blurred for "depth" unless it sits on a defocused plane. Generated plates follow the project's own optics rules through
  `cinematic-prompt-writer`.

## 4. Colour pipeline (one grade, never two)

Pick one and write it in the spec:
- **Graded colours**: build with colours sampled from graded frames; the file is final and goes on top of the graded timeline.
- **Neutral + LUT**: build neutral, apply the project's `.cube` from `video-color-grade` once (in the NLE or with ffmpeg), so the
  graphic moves with any later grade change.
Applying the LUT to a graphic that was already built from graded samples double-grades it.

## 5. Typography

- Faces belong to the era and the film, not to software: for the 1900s-1910s, for example, a Scotch or Didone roman, an engraved or
  Clarendon display, a period grotesque, a typewriter or ledger mono, hand-drafting capitals for drawings. Not geometric SaaS sans.
- Name exact families and weights in the spec; load them from local files with `@font-face`. A missing glyph falls back to a system
  face silently, so every face is glyph-tested for every script on screen (`otf-presentations` font check, `--cyrillic` when the
  project language needs it) and the result is written into the spec (`"glyph_test": "pass"`).
- Caps with tracking (0.12-0.35 em) for stamps and labels; true small caps when the font has them; tabular numerals for anything
  that counts or aligns.
- One language per render. A bilingual project delivers separate files; an English cut shows zero Cyrillic and vice versa.

## 6. Safe areas

| Aspect | Text must stay inside | Notes |
|---|---|---|
| 16:9 | 5 % inset each side (title-safe) | lower-third baseline at or above 10 % from the bottom |
| 9:16 | left 6 %, top 14 %, right 12 %, bottom 20 % | platform UI covers the top, the right rail and the caption zone |
| 2.39:1 inside 16:9 | the picture area | text in the letterbox bars only for deliberate chapter cards |
| 1:1, 4:5 | 5 % / 8 % top, 12 % bottom for 4:5 | |

Design each aspect as its own layout (re-flow, re-scale, move the map centre). Never deliver a centre crop of the 16:9 as the 9:16.
The template's `guides` variable and the spec `box` fields make this checkable.

## 7. Banned tells (the SaaS / social look)

Rounded cards with drop shadows, glassmorphism, gradient fills, neon or coloured glows, emoji, icon sets, progress pills, social
handles, logo stings, brand colours that are not in the film, bouncy springs and overshoot, scale-pop entrances, whip zooms,
3D rotating cards, lens flares added for "energy", particles, confetti, light leaks that the film does not have, perfectly clean
vector edges over a grainy plate.

## 8. Accuracy line

Every period graphic carries an `accuracy` list in its spec: one line per claim the frame makes (date, time, place name, border,
livery, number, title of a person), each with a source from `period-fact-check`. Period names are used as of the date shown
(Queenstown, not Cobh, in 1912; no borders that did not yet exist). When sources disagree, say which one the graphic follows. A
pending line blocks the final render, not the draft.
