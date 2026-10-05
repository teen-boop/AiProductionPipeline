---
name: visual-story-8-storyboard
description: FINAL production step of the sequential visual-story pipeline — the storyboard. This is what actually goes into production, done ONLY after the script is final, the Production Design Guide is locked, the scene stills are face-locked, and all reference tests have passed. Produces a shot list (table), storyboard frames (numbered panels with slug-line headers + ACTION/DIALOGUE captions), and a motion-annotated layer (RED body / BLUE camera / GREEN framing / ORANGE lighting / YELLOW VFX) that decides the movements — then assembles the Seedance animation prompt in the dense CAMERA/LOOK/STYLE/CHARACTER/SETTING/SCENES format. Style must match the design guide. Test with GPT Image 2.0.
---

# Visual story — Storyboard (the production-ready step)

**This is the last step, and it goes straight into production.** Do it ONLY when all of these are
true:
- the script is final and segmented into numbered scenes (`visual-story-2-script`),
- the **Production Design Guide is locked** — every character/location/prop has an approved design
  sheet, plus the NOTES FOR ART DEPARTMENT (`visual-story-4-references`),
- the scene stills are generated and faces are locked/replaced (`visual-story-6-production`),
- the reference tests have all passed.

By this point it's clear which shots the scene needs and which movements to add. **The storyboard is
where those get committed, not explored** — no experimenting with look or identity here; that's
already locked upstream. Full format spec in `references/storyboard-formats.md` and
`references/seedance-storyboard-format.md` — read both.

## Hard requirements (from direct user direction)

- **The face must be IDENTICAL to the real reference in every panel.** This is the top priority. A
  storyboard whose face has drifted from the real actor is a failure, no matter how good the layout.
  So on every storyboard generation, attach BOTH the character's **real face photo** AND the approved
  finished still (and the character sheet if one exists), and append the mandatory face clause:
  *"Maintain precise facial proportions and identity, and keep the eye color exactly as in the
  reference — use my image with accurate face 100%."* Attaching only the finished still is NOT enough
  — the real face photo must be in the attachment set, exactly as in the character-lock rule from
  `visual-story-4-references`. In a multi-panel grid this matters more, not less: the face has to hold
  identical across all 12 panels.
- **At least 12 panels per storyboard sheet**, on one image (3×4 or 4×3 grid). Not 6, not 9 — 12
  minimum. Break the scene's beats finer if needed to reach 12.
- **Every panel has a description** — slug line + ACTION/DIALOGUE, exactly like the reference boards.
- **Every panel states a camera movement** — static/push/pull/pan/tilt/track/orbit/handheld. Required
  on each panel, even "static."

## Produce, in this order

1. **Shot list (table) — 12+ rows.** One row per shot:
   `# | Size | Angle | Camera move | Subject | Action/Dialogue`. Camera move is a required column.
   This is the coverage plan; every row becomes a frame. (Sizes: WS/MWS/MS/MCU/CU/OTS/etc.)
2. **Storyboard frames — 12+ panels.** Numbered panels, each with a slug-line header
   (`1. EXT. CLOCK TOWER — WIDE ESTABLISHING SHOT`), the frame drawn in a consistent style (clean
   sketch OR the finished film look — attach design-guide sheets if finished-look), an
   `ACTION / DIALOGUE:` caption, and a `CAM:` camera-move label. Generate the frames CLEAN (no baked
   text — it garbles); the slug lines / captions / camera-move labels / motion arrows are composited
   as a layout/overlay pass, numbered to match the panels.
3. **Motion annotations — the movements layer (the bridge to animation).** Colored arrows over each
   frame, standard legend printed on the sheet:
   - **RED = body movement**, **BLUE = camera movement**, **GREEN = framing/composition**,
     **ORANGE = lighting direction**, **YELLOW = VFX/energy**.
   - Each panel also carries shot# + framing + **lens** (`1. WIDE DIAGONAL 24mm`).
   - Draw trajectories, not just poses.
4. **Assemble the Seedance prompt** from all three: the shot list gives the beats, the annotations
   give the movement. Each color maps to a section of the dense prompt — RED→SCENES action,
   BLUE→CAMERA, GREEN→shot size/lens per beat, ORANGE→LOOK, YELLOW→inline `[VFX:]` tags. Nothing
   about the motion is invented at the Seedance stage; it's decided and drawn here first.

## The style-match rule (still the thing that breaks everything if ignored)

The written Seedance `LOOK`/`STYLE` sections, the storyboard frames, and the finished stills must all
describe the SAME world — palette, lighting, film stock — anchored to the design guide's NOTES FOR
ART DEPARTMENT. The storyboard plans motion; the design guide owns the look; they must agree.

## Tooling — which engine, and the one real gotcha

**nano-banana-pro via Lovart works fine and free** for single-image generations AND multi-panel
sheets (turnarounds, storyboard grids) — this was the workhorse all through the project (character
shots, 4-panel location/prop turnarounds, the whole v7/v8 rework, convergence groups). Lovart's CLI
does route everything through its `chat` (agent) endpoint, but for nano-banana that has been reliable
and cost-free. Default to it: `--prefer-models '{"IMAGE":["generate_image_nano_banana_pro"]}'`.

Two genuine gotchas, both verified live — the distinction is by MODEL, not by "agent vs not":
- **GPT Image 2 on Lovart is paid and step-gated.** The Lovart agent runs it per-panel and prompts
  for paid-credit confirmation each step (17, then 16+ credits), and its first output was a single
  portrait, not a grid. So do NOT use GPT Image 2 via Lovart for a multi-panel storyboard. If GPT
  Image 2 is specifically wanted, use **Krea's direct `generate_image` with `openai/gpt-image-2`**
  (one generation, no agent) — paid, but predictable.
- **Occasional text-only flake on complex multi-panel prompts** — the Lovart agent sometimes responds
  with text and no artifact. Per platform notes this is transient; a straightforward re-submit
  (phrased "generate one image now: ...") usually triggers the generation. If it flakes twice, switch
  to Krea direct `generate_image` (`google/nano-banana-pro`) rather than burning more attempts.

## When done

The scene has a shot list + storyboard frames + motion annotations + an assembled Seedance prompt,
all style-locked to the Production Design Guide. This is production-ready. The actual Seedance video
generation is the paid step that follows, driven by the prompt this step produced.
