---
name: motion-remotion-build
description: The CODE route for motion graphics — building animated charts, editorial explainers and Vox-style scenes in Remotion driven by Claude Code, with no After Effects and no keyframes. Covers the one-prompt project setup, the exact-numbers doctrine, determinism rules that stop render flicker, prop controls and saving them back, the three-layer scene architecture, master sequence assembly, voice-over sync, QA toggles and render. Use whenever building or fixing a Remotion motion-graphics composition, an animated chart, a multi-scene explainer film, or when a render flickers, drifts, or looks digital instead of printed. Triggers on remotion, animated chart, bar chart, line race, seat chart, boil, prop controls, master sequence, render mp4, scene folder, voice over sync, exact numbers.
---

# Motion Remotion Build

Companion to `motion-style-core` (locks the look) and `motion-graphics-director` (owns the 46-block prompt library). Read the library before writing a composition prompt — do not improvise moves that already exist as blocks.

## The one-prompt setup (first prompt of every project)

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

Do not ask the user to set up a Remotion project separately. This prompt does it.

## The five laws

1. **Exact numbers.** Every parameter is a number, never an adjective. Mark the blocks `(exact numbers)` so the model knows not to interpret. "Slow" is not a spec; "34 frames" is.
2. **Props, not code.** Every visual decision must be tunable in the Studio panel. After tuning, **write the values back into the default props** — Studio edits are lost otherwise. Ask explicitly: `write my current Studio values back into the default props`.
3. **Determinism.** No `Math.random()` anywhere. Every noise seed derives from the frame number. Data is baked into props as plain arrays so the render never touches the network. Violating this produces flicker that only appears in the final multi-worker render, i.e. at the worst possible moment.
4. **Anti-default.** Name the thing the model will do by default, and forbid it, before describing what you want. `do not place the dots along curved rings like every default parliament chart does` beats three sentences describing a grid.
5. **Motion serves the thesis.** Pick physics from what the chart means. *A chart about nobody reaching a majority gets no bouncy cartoon energy.* Say the reason in the prompt — it makes the model choose consistently for everything you did not specify.

## Animating with intent

Write intent in plain English; never name the functions. The model picks `spring` and `interpolate` correctly on its own.

> Animate the White House spring up first, followed by the two figures right after. Stagger them so they don't all move at once. Give me an offset red marker stroke behind each cutout.

Describe tempo with a physical metaphor, not an easing name: **"a steady marker pace that only softens right at the end — like a hand dragging a marker, not a bouncy ease."**

## Composition assembly

Pull blocks from the library:
```
STYLE CORE + 1×CAM + 1–3×ENT/VAL + 1–2×ANN + FIN + QA
```
Inherit style by reference, never by repetition: **"next composition in the same project, same paper look"**.

## Data compositions

- Real, cited data only. Source printed in the deck. No demo badge anywhere.
- Include a **sanity-check value** in the prompt: `the US ends day 45 around 743,000 — sanity-check against that`. This is the cheapest defense against fabricated series.
- Bake the fetched numbers into props as plain arrays.
- **One sort order** used for both coloring and reveal. Never two.
- Racing line charts: rebuild each line every frame from only the days that have happened, so heads stay on the same day — otherwise the longest path wins the race for no reason.

## Multi-scene film architecture

```
Each scene lives in its own folder with its own assets.
Every scene shares ONE identical locked background, copied into each scene folder —
it never moves and never changes, so the film reads as a single continuous shot.
Three layers per scene:
  BACKGROUND  shared plate, static
  MIDGROUND   black-and-white halftone cutouts of people, springing up
  FOREGROUND  structures, vehicles, scenery, entering on their own beat
Same fonts and palette everywhere. Only mid and foreground change.
```

Cutout prep: `convert this transparent PNG to black and white with a halftone dot pattern finish, keep the alpha channel` — that is what produces the printed-magazine feel instead of a pasted photo.

**Order:** script → voice-over → scenes → master sequence. Never scenes first.

Master sequence:
```
Stitch all scenes into one composition in script order, each playing exactly as long
as its narration segment, back to back as a single film. Each scene must start and
end on its own narration line.
```

## QA before render

- `freeze toggle` — compare boil on/off
- `variant toggle` — compare layout A/B
- `scaffolding toggle` — grid, margins, baselines
- Errors: paste the error straight back with `fix this error, please`. Do not debug it by hand first.
- Audio sounding jerky while scrubbing in Studio is normal and disappears on render — do not chase it.

## Render

```
Render the whole thing as a 1080p MP4 with the music and voice-over mixed in.
```
If the user prefers finishing in Premiere: render the clean composition only, and hand over the VO and music as separate files.

## Failure table

| Symptom | Cause | Fix |
|---|---|---|
| Flicker in final render only | `Math.random` somewhere | seeds from frame number |
| Values lost after restart | Studio edits never saved | write values back to default props |
| Type looks melted | text inside the displacement filter | move text outside the filter |
| Edges clipped | filter region too small | oversize the filter region |
| Lines drift sideways during boil | noise weights don't sum to 1 | normalize the weights |
| Roughness pulses mid-blend | displacement not normalized | divide by the weight vector length |
| One line finishes early | line drawn by path length | rebuild per frame from elapsed days |
| Looks digital, not printed | FIN layer missing or disabled | grain + marker edge + speckle |
