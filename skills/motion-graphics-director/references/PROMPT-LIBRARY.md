# MOTION PROMPT LIBRARY · v0.1

A library of composable prompts for Claude Code + Remotion (and, where noted, for Omni Flash /
video models).

**Sources (4 tutorials):**
1. *AI Vox Style Motion Graphics Are Finally Usable (Gemini Omni)* — style-lock + swap action,
   master style sheet, two routes.
2. *Vox-Style Animated Charts With ONE PROMPT (Remotion + Claude Code)* — exact-numbers doctrine,
   paper textures, boil, props-not-code.
3. *Claude Design FINALLY Solved Motion Graphics* — 5 levels of anti-slop: data → font → icons →
   Lottie/images → transcript+research.
4. *I Made Vox-Style Motion Graphics Using Only Claude Code & Remotion* — three-layer scene,
   folder architecture, animate-with-intent, master sequence, VO sync.

---

## 0. HOW THIS IS ASSEMBLED

**The formula for one composition:**

```
BLOCK-00 SETUP          (once per project)
+ BLOCK-01 STYLE CORE   (once per project, after that — just say "same project, same look")
+ BLOCK-02 ARCHITECTURE (once per project, if it's a multi-scene film)
+ 1 × CAM               (exactly one deliberate camera move)
+ 1–3 × ENT / VAL       (entrances and data moves)
+ 1–2 × ANN             (annotations, accents)
+ FIN                   (finish layer, always on)
+ QA                    (comparison toggles)
```

**Three mixing rules:**
1. **One camera move per composition.** Two = mush. If you want a second one, that's a second
   composition.
2. **A maximum of 3 element moves at once.** Everything else gets spread across frames via stagger.
3. **The FIN layer is never turned off** — it's what tells "drawn" apart from "generated." But
   text never goes inside the filter.

**The style in these blocks is a placeholder, not hardcoded.**
Every hex value, typeface, and texture number in the blocks below belongs to the **reference pack
`paper-vox`**, shown for illustration. Before sending a prompt, substitute the values from your
project's `STYLE-PACK.md` by role:

| Role in the block | Where it comes from |
|---|---|
| plate / background | `BASE` |
| text | `INK`, `DECK` |
| axes, grid | `STRUCTURE` |
| hero | `ACCENT` |
| outlines, underlines, arrows | `STROKE` |
| phrase highlight | `MARKER` |
| everything else | `MUTED` |
| texture, grain, edge | `SURFACE`, `EDGE` |

An empty slot in the pack means the block that requires it **does not apply** in this project.
Each pack lists its own allowed and **forbidden** block IDs — check against that, not against
taste. A spring with overshoot is appropriate in `clay` and inappropriate in `paper-vox`.

**Format of each entry:** ID · what it is · parameters as numbers · ready-to-use prompt block ·
what it pairs with · what to avoid.

---

---

## 0.1 FORMAT: why the numbers in these blocks can't be ported blindly

All numbers in the catalog below are given in the **reference format `1920×1080 @ 30fps`** (the
format test-01 was built and verified at). When the format changes, **two different classes of
numbers get recalculated by two different rules** — and this is the most common hidden mistake
when porting.

### Class A — timings: divided by fps

Frame values (`frame 40`, `stagger 8`, `46 frames`) express **duration**, not a count.
Coefficient = `new fps / 30`.

| → 23.976 fps (×0.8) | was | becomes |
|---|---|---|
| headline / deck / grid | 6 / 12 / 24 | **5 / 10 / 19** |
| bars: start · cascade · grow | 40 · 8 · 46 | **32 · 6 · 37** |
| count-up | 24 | **19** |
| highlight: start · duration | 30 · 34 | **24 · 27** |
| boil: crossfade every | 4 | **3** |
| composition length | 180 (6.00s) | **144 (6.01s)** |
| seat chart: reveal · threshold · leaders · total | 100 · 158 · 150 · 210 | **80 · 126 · 120 · 168** |

### Class B — texture: scales with resolution

`feTurbulence` computes frequency in **user units**, not fractions of the frame. At 3840, the same
shape is twice as large in units — meaning twice as many noise periods land on it, so the marker
edge gets finer and the grain gets denser. To **preserve the look**, frequencies are divided by the
resolution coefficient, and amplitudes are multiplied by it.

| → 3840×2160 (×2) | was | becomes | rule |
|---|---|---|---|
| EDGE baseFrequency | 0.02 | **0.01** | ÷2 |
| EDGE displacement scale | 4 | **8** | ×2 |
| speckle frequency | 0.42 | **0.21** | ÷2 |
| grain noise scale | 0.72 | **0.36** | ÷2 |
| entire px layout | — | ×2 | ×2 |
| opacity, strength, weights | 0.34 · 16% · 28% | **unchanged** | dimensionless |

### Rule

**A pack must declare its reference format.** A texture number without a stated resolution isn't a
value, it's a riddle: the tutorial's `baseFrequency 5` looks sensible right up until you ask "at
what frame size." Slot 10 `VERIFIED` records the format at which a number was actually verified by
rendering.


## 1. BLOCK-00 · SETUP (written once, in the project's very first prompt)

```
Set up a fresh Remotion project — TypeScript, 1920x1080 at 30fps, one composition
per shot, previewable in Remotion Studio.

Every visual decision must be an editable prop in the Studio side panel (color
pickers, number fields, positions, scales, timings, and the data itself) so I can
tune shots without touching code.

Never use random numbers anywhere — derive every bit of noise from the frame
number, so parallel render workers stay in sync and the export doesn't flicker.

Animate with only two primitives: spring for anything that pops or lands, and
interpolate for anything that travels or fades. Never pass a duration to a spring —
let the physics run.

When installing new dependencies, check for existing lockfiles and use the right
package manager.

Give me prop controls for every element on screen, including position, scale,
rotation and opacity.
```

> **Rule from tutorial 4:** after tweaking values in Studio, **they need to be saved** back into
> props — otherwise they're lost on restart. Ask Claude: `write my current Studio values back into
> the default props`.

---

## 2. BLOCK-01 · STYLE CORE — style declaration (filled in from the project's pack)

Template. Values in angle brackets come from the project's `STYLE-PACK.md`.

```
STYLE: <one dense phrase: what the frame should look like — printed / drafted / moulded>.
Plate <BASE> with <SURFACE: plate treatment, in numbers>.
<SURFACE: grain — opacity, blend, scale, refresh, or "no grain">.
<INK> for text, <DECK> for secondary text, <STRUCTURE> for axes and rules.
Exactly one hero element per frame, expressed by <this pack's hero mechanism:
ACCENT color / line weight / scale>; everything else <MUTED>.
<STROKE> is reserved for strokes, underlines and arrows only — never a fill.
<MARKER> is reserved for <its one job> — omit this line if the slot is empty.
Typography: <exact typefaces and weights>, sharp, never warped.
Edges: <EDGE — marker jitter with numbers / a precise ruled line / a soft matte bevel>.
Text never goes inside a displacement filter.
```

For illustration, the rest of the catalog below uses the `paper-vox` pack's values
(`BASE #F7F4EC · INK #1C1B19 · DECK #5A5648 · STRUCTURE #6F6940 · ACCENT #D0674C ·
STROKE #D62E1F · MARKER #F5C842 · MUTED #A9BCC2`, DM Serif Display + Oswald) —
**this is a sample fill, not the project default.**

> **Anti-slop #1 (tutorial 3): the font is the #1 tell.** Never leave the default. Sources:
> Fontshare, Open Foundry, Google Fonts, Typewolf; identify a font from someone else's design:
> fonts.inuse.com; pull typography off a site: Firecrawl with `branding` enabled.

## 3. BLOCK-02 · SCENE ARCHITECTURE (for a multi-scene film)

```
Project architecture: each scene lives in its own folder with its own assets.
Every scene shares ONE identical locked background image, copied into each scene
folder — the background never moves and never changes across the film, so the whole
piece reads as a single continuous shot rather than a series of cuts.

Every scene is built from three layers:
  BACKGROUND — the shared locked plate, static.
  MIDGROUND  — black-and-white halftone cutouts of people, springing up.
  FOREGROUND — structures, vehicles, scenery cutouts, entering on their own beat.

Same fonts and same accent palette in every scene. Only the midground and
foreground cutouts change.
```

**Preparing cutouts:**
```
Take the transparent PNG in this folder and convert it to black and white with a
halftone dot pattern finish, so it reads like a printed magazine cutout rather
than a digital photo. Keep the alpha channel intact.
```

**Master sequence (once all scenes are ready):**
```
Stitch all the scenes together into one composition in script order, each playing
for exactly as long as its narration segment, running back to back as a single
film. Each scene must start and end on its own narration line.
```

---

# 4. ANIMATION CATALOG

## ING · Ingesting material

### ING-01 · Image import + OCR word boxes
Lets you animate annotations over a raster image (newspaper, article, screenshot) landing
precisely on words.
```
Import the image at <PATH> into the project. Use the tesseract CLI to do OCR and
find the pixel positions of the text. Bake the resulting word boxes into the props
as a plain array, so the render never depends on running OCR again.
```
**Pairs with:** ANN-02, CAM-01, CAM-02, ENT-02. **Avoid:** annotating "by eye" without OCR —
10–20px misses are immediately visible.

### ING-02 · Generous pad on a clean plate
```
Load the image and pad it generously on a white Full HD background, centered, with
at least 12% margin on every side.
```

### ING-03 · Bake fetched data
```
Pull the real <SOURCE> numbers for <SUBJECT>, aligned as <ALIGNMENT RULE>.
Sanity-check: <CONTROL VALUE> — if your fetched series disagrees, stop and tell me.
Bake the fetched numbers into the props as plain day-by-day arrays so the render
never depends on the network.
```
**Rule:** real, cited data, source in the deck, `no demo badge anywhere`.

### ING-04 · Green-screen stock layer
```
Use the keyed <OCEAN/SMOKE/CROWD> video in this folder as a live layer between the
background plate and the foreground cutouts. Its background is already removed —
composite it straight, do not add a shadow.
```

---

## CAM · Camera moves (exactly one per composition)

### CAM-01 · Slow push-in
```
While the composition runs for <N> seconds, slowly and very subtly zoom into it.
The move must be barely perceptible — the frame should feel alive, not zoomed.
```
Guideline: 1.00 → 1.06 over 5 seconds, ease-in-out.

### CAM-02 · 3D card rotate
```
Slightly rotate the artwork in 3D from left to right across the whole composition.
Total rotation around 15deg on each axis, arriving at rest, never oscillating.
```
**Pairs with:** ING-01/02, ENT-02, ANN-02.

### CAM-03 · Drift hold
```
Hold the shot and let the camera drift slowly across the stage — a 2% move over
the full duration, no easing bumps.
```
The default for scenes where all the motion is given to the elements.

### CAM-04 · Layer parallax
```
Separate the background, midground and foreground onto three depth planes and move
them at different rates as the camera travels, so the shot has true parallax. The
nearest plane carries a slight blur as it crosses the lens.
```

### CAM-05 · Rack focus between planes
```
Rack focus from the foreground plane to the midground plane over 18 frames,
crossfading a blur of 0px to 6px and back, so attention transfers between layers.
```

### CAM-06 · Climb alongside the hero element
```
As the hero bar rockets up, the camera tilts up and climbs alongside it, the bar
face rushing past the lens with a slight dutch tilt, the smaller elements shrinking
below in deep focus falloff. Settle at the trembling summit.
```
Taken from the Omni prompt; in Remotion it's done as a combination of scale + translateY + blur
across neighboring layers.

---

## ENT · Element entrances

### ENT-01 · Mask rise (headline)
```
The headline rises in from behind a mask at frame 6, the deck at frame 12.
Nothing overshoots — text lands flat.
```

### ENT-02 · Blur-in reveal
```
At the beginning, blur the whole composition and unblur it over 1 second.
Nothing else animates until the blur has finished.
```
**Pairs with:** a mandatory "first breath" for ING-01/02 compositions.

### ENT-03 · Spring pop with overshoot (cutout)
```
Animate <ELEMENT> springing up into place with a slight overshoot, landing with a
small settle. Give it an offset red marker stroke behind the cutout, so it reads as
a physical paper layer lifted off the page.
```
The offset red outline is the Vox style's signature; it gives pseudo-3D for free.

### ENT-04 · Staggered entrance (multiple objects)
```
Animate <A> spring up first, followed by <B> and <C> right after. Stagger them so
they don't all move at once — 8 frames between each.
```
**Rule from tutorial 4:** phrase it in English as intent, not as function names.

### ENT-05 · Travelling wave (a collection of hundreds of elements)
```
Reveal the elements as a single wave sweeping left to right over 100 frames,
starting at frame 40. Each element pops in with a small crisp spring — damping 19,
stiffness 280, mass 0.6, no clamping — that lands almost flat. Don't pass a duration
to the spring; let the physics run. Stagger each element by its position in the
sorted order, so roughly thirty are mid-pop at any instant: a travelling wave, not
a queue.
```
**Key:** "no bouncy cartoon energy" is chosen to fit the chart's meaning.

### ENT-06 · Staggered card snap-in
```
Three cards snap in one after another at different depths, forming a triangle,
staggered by 6 frames, each with a short spring and no bounce.
```

### ENT-07 · Torn-edge wipe
```
Reveal the panel behind a torn paper edge that travels across the frame over 20
frames, the tear line irregular and hand-made, never a straight wipe.
```

### ENT-08 · Gridlines & baseline fade
```
Gridlines and the baseline fade in at frame 24, at 40% ink, before any data appears.
```

---

## VAL · Data moves

### VAL-01 · Bar grow at marker pace
```
Bars start at frame 40, one after another with an 8-frame stagger, each growing for
46 frames at a steady marker pace that only softens right at the end — like a hand
dragging a marker, not a bouncy ease.
```

### VAL-02 · Count-up
```
Values count up over 24 frames as each bar finishes, landing exactly on the real
number, thousands separators formatted.
```

### VAL-03 · Line race with locked heads
```
Draw the lines on left to right with a small dot riding each line's head, and make
sure every head sits on the same day at the same moment — rebuild each line every
frame from only the days that have happened so far, so no line races ahead just
because its path is longer. The playhead advances at the same steady marker pace as
the bars.
```
**This is the most common mistake in racing charts.**

### VAL-04 · Threshold line draw
```
After the data settles, draw in a dashed threshold line at <VALUE> starting frame
158 with a small label, then leader lines out to each series name and count from
frame 150, labels fading in as their lines land.
```

### VAL-05 · Lattice carve (anti-default)
```
Important — do not place the dots along curved rings like every default chart does.
Build them on a straight up-and-down grid (aligned vertical columns and horizontal
rows) and carve the target shape out of that grid, so rows and columns line up like
halftone print. Sort the elements once by angle, left to right, and use that one
order for both the coloring and the reveal — never two different orders.
```

### VAL-06 · Label collision push-apart
```
Series labels fade in right as each line arrives at its end, and push overlapping
labels apart so they never collide.
```

---

## ANN · Annotations and accents

### ANN-01 · Marker highlight swipe
```
The yellow marker highlight swipes across the key phrase starting at frame 30,
taking 34 frames — slow, like a real hand. The highlight sits behind the text.
```

### ANN-02 · Rough.js highlighter over OCR'd words
```
After the blur is done, evolve a highlighter from left to right using rough.js over
the words "<WORD A>" and "<WORD B>", using the OCR word boxes. Make sure the marker
appears behind the text.
```
**Pairs with:** ING-01 (mandatory), ENT-02, CAM-01/02.

### ANN-03 · Underline swipe
```
A red underline swipes beneath the headline word over 12 frames, hand-drawn, with
the stroke slightly overshooting the word on both ends.
```

### ANN-04 · Scribble circle callout
```
Circle <ELEMENT> with a rough.js hand-drawn ellipse that draws itself over 16
frames, two overlapping passes, red, sitting on top of everything.
```

### ANN-05 · Pin drop + caption
```
A map pin drops onto <LOCATION> with a short spring and a small shadow, then the
caption "<CAPTION>" fades in beside it 6 frames later on a mustard label.
```

### ANN-06 · Arrow draw + chips racing
```
A thick arrow draws itself card-to-card into a closed loop; coin chips race along
it, the nearest whipping past the lens with motion blur.
```

### ANN-07 · Leader lines
```
Leader lines draw out from each element to its label over 10 frames, the label
fading in as its line lands.
```

### ANN-08 · Ticking counter
```
The stat counter ticks upward in discrete steps, never smoothly, one step every 2
frames, with a tiny vertical jitter on each tick.
```

---

## FIN · Finish layers (always on)

### FIN-01 · Marker edge (frozen turbulence)
```
Give the shapes wobbly hand-drawn marker edges with an SVG feTurbulence filter:
fractal noise, base frequency 0.02, 3 octaves, displacement scale 4, and freeze the
seed — no boiling, the edge holds still. Oversize the filter region so the edges
never clip. Text never goes inside the filter.
```
> **VERIFIED (test-01).** The tutorial names `base frequency 5` — this is a **scale error**: at
> 1920px it produces invisible micro-dust along the edge. The working range is **0.02–0.05**.
> `0.02 / scale 4` gives a clean marker edge. `0.03 / scale 6` is already torn paper, the edge
> eaten away.

### FIN-02 · In-shape speckle
```
Clip a paper-grain speckle inside each shape and multiply it into the fill: noise
frequency 0.42, strength 0.34.
```

### FIN-03 · The boil (living line tremor)
```
Give the strokes a living hand-drawn simmer: run two SVG turbulence fields —
fractal noise, base frequency 0.022, 2 octaves — on seeds n and n+1, and crossfade
between them every 4 frames with the displacement at scale 2.5. Blend, don't swap:
regenerating the noise every few frames just buzzes. Keep the two noise weights
always adding up to one so the lines don't drift sideways mid-blend, divide the
displacement by the length of the weight vector so the roughness doesn't pulse at
the middle of each blend, and give me a freeze toggle so I can compare boil on
against boil off. Derive the seeds from the frame number, never randomness.
```
Too little boil is dead. Too much is "buzz." `scale 2.5` is the working middle ground.

### FIN-04 · Frame grain
See BLOCK-01: 16% opacity, overlay, noise 0.72, refresh every 2 frames.

### FIN-05 · Offset keyline (halftone cutout)
```
Every cutout gets a rough white keyline and one offset hot-red stroke behind it,
so it pops off the plate like a physical paper layer.
```

### FIN-06 · Alert wash
```
ALERT WASH: the entire frame floods to the hot accent tone in one beat, holds 4
frames, and drains back.
```
For one hit across the whole film. Twice, and it becomes a crutch.

### FIN-07 · Vignette hold
```
A very soft warm vignette across the plate, 8% strength, static, never animated.
```

---

## TRN · Transitions between scenes

### TRN-01 · Locked-plate handoff (default)
```
The shared background never changes between scenes — only the midground and
foreground cutouts leave and enter, so the film reads as one continuous shot.
Outgoing cutouts drop down and out over 10 frames while the incoming ones spring up.
```

### TRN-02 · Paper slide
```
The whole plate slides <LEFT/UP> by one frame width over 16 frames with a torn edge
leading, carrying the next scene in behind it.
```

### TRN-03 · Match-cut on a shared element
```
Hold <ELEMENT> in place across the cut while everything else changes around it,
then let it transform into <NEW ELEMENT> over 12 frames.
```

---

## AUD · Sound and sync

### AUD-01 · VO-driven timeline
```
Embed the voice-over into the composition and sequence the scenes to it. Each scene
should start and end on its own narration line.
```
Order of work: **VO first, then scenes.** The script is the timeline.

### AUD-02 · Sound-design only (for video models)
```
AUDIO: sound design only — paper pops, whooshes, stamps, ticks.
No music. No voice-over. No narration. No lyrics.
```

---

## QA · Toggles (mandatory)

### QA-01 · Freeze toggle
`give me a freeze toggle so I can compare boil on against boil off`

### QA-02 · Variant toggle
`give me a toggle between the ring layout and the grid layout so I can compare them side by side`

### QA-03 · Scaffolding toggle
`give me a scaffolding toggle that shows the grid, margins and baselines over the composition`

---

# 5. READY-MADE COMBOS

### COMBO-A · "Highlighted article" (the reference example)
`ING-01 + ING-02 + CAM-01 + CAM-02 + ENT-02 + ANN-02`
```
Import the following image into the project: '<PATH>'. Use tesseract CLI to do OCR
and find the positions of the text. In Remotion, make a new composition where you
load the image and pad the article generously on a white Full HD background.
While the composition is running for 5 seconds, slowly, very subtly zoom into it and
slightly rotate the article in 3D from left to right; the overall rotation should be
around 15deg for each axis. At the beginning, blur the whole composition and unblur
it over 1 second. After the blur is done, evolve a highlighter from left to right
using rough.js over the words "<WORD A>" and "<WORD B>". The image has a white
background — make sure the marker appears behind the text.
When installing new dependencies, check for existing lockfiles and use the right
package manager.
```

### COMBO-B · "Paper bar chart"
`BLOCK-01 + ING-03 + ENT-01 + ENT-08 + VAL-01 + VAL-02 + ANN-01 + FIN-01 + FIN-02 + FIN-04`
One composition, 180 frames, 30fps. The hero is one bar, the rest are muted.

### COMBO-C · "Wave of hundreds of elements"
`BLOCK-01 + VAL-05 + ENT-05 + VAL-04 + ANN-07 + FIN-01 + QA-02`
210 frames. Mandatory: the grid anti-default and a single sort order.

### COMBO-D · "Line race with boil"
`BLOCK-01 + ING-03 + VAL-03 + VAL-06 + ANN-01 + FIN-03 + QA-01`
The only place boil is turned on. Bars and text have no boil.

### COMBO-E · "Explainer-film scene"
`BLOCK-02 + ENT-03 + ENT-04 + CAM-03 + FIN-05 + TRN-01 + AUD-01`
The background is locked, cutouts enter in a cascade, a red offset outline on each.

---

# 6. COMPATIBILITY MATRIX

| | CAM-01 | CAM-02 | CAM-03 | CAM-04 | CAM-06 |
|---|---|---|---|---|---|
| ANN-02 highlighter | ✅ | ✅ | ✅ | ⚠️ jitters | ❌ |
| VAL-01 bars | ✅ | ❌ | ✅ | ❌ | ✅ |
| VAL-03 line race | ✅ | ❌ | ✅ | ❌ | ❌ |
| ENT-05 wave | ⚠️ | ❌ | ✅ | ❌ | ❌ |
| ENT-03 cutout pop | ✅ | ⚠️ | ✅ | ✅ | ✅ |
| FIN-03 boil | ✅ | ⚠️ | ✅ | ⚠️ | ❌ |

⚠️ = okay, but halve the camera amplitude. ❌ = do not combine.

---

# 7. ANTI-DEFAULT / ANTI-SLOP CHECKLIST

Before sending any prompt, check:

1. **Is the font named explicitly?** The default font is the #1 tell of slop.
2. **Is the default the model would produce on its own named and forbidden?** (rings → grid,
   bouncy ease → marker pace, clean wipe → torn edge)
3. **Are all parameters given as numbers?** Blocks are tagged `(exact numbers)`.
4. **Is there exactly one hero accent?** Everything else is muted.
5. **Is randomness excluded?** All noise comes from the frame number.
6. **Is data baked into props?** The render must not hit the network.
7. **Is there a control number to verify the data?**
8. **Is text outside the displacement filter?**
9. **One sort order for both coloring and reveal?**
10. **Have prop controls been requested, and are values saved back into props?**
11. **Are icons/assets from a single pack, one style for the whole piece?**
12. **Is the motion justified by the frame's meaning, not by taste?**

---

# 8. BACKLOG FOR ADDITIONS

Drafts not yet written up as blocks — add them as they come up in actual work:

- Lottie library: a local repository of JSON icons, handed to Claude as an asset pack
  (tutorial 3, level 3).
- Transcript with word-level timecodes → selecting moments for animation (tutorial 3, levels 4–5).
- A research agent to enrich numbers before animating (Firecrawl / web search).
- A map with a route and a moving dot.
- An exploding stack of "paper layers" (explode view).
- Isometric cross-section / blueprint style (a second STYLE CORE).
- Clay style (a third STYLE CORE).
- A timeline bar with a running playhead.
- A "before/after" wipe comparison.
