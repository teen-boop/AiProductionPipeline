# Storyboard formats — the production-ready artifacts

The storyboard is the LAST step before animation and **the thing that actually goes into
production**. Do it only after: the script is final, the Production Design Guide is locked, the
scene stills are generated and face-locked, and the reference tests have all passed. By this point
it's clear which shots the scene needs and which movements to add — storyboard is where those
decisions get committed, not explored.

There are three paired deliverables (confirmed by reference examples the user supplied). Produce them
in this order: **shot list → storyboard frames → motion annotations**, then assemble the Seedance
prompt (`seedance-storyboard-format.md`) from all three.

## Panel count — minimum 12

**Every storyboard sheet has AT LEAST 12 panels** (matching the reference examples — the 12-shot
"Two Birds" board and the 12-shot action board). Lay them out as a 3×4 or 4×3 grid (or more panels
if the scene needs them). Six or nine is not enough — plan the scene's full coverage to 12+ beats.
If a scene is short, break its beats finer (more shot sizes / angles / inserts) to reach 12.

## 1. Shot list (the structured plan — a table)

Before drawing anything, lay the scene out as a shot-list table of **12+ rows**. Every row carries a
**camera movement** — this is required, one per panel:

| # | Size | Angle | Camera move | Subject | Action / Dialogue |
|---|------|-------|-------------|---------|-------------------|
| 1 | WS | Eye-level | Static / locked-off | Clock tower | Establishing. (Soft wind ambience.) |
| 2 | MW | Eye-level | Slow push in | Tower dome | Birds flutter and land. |
| 3 | MS | Eye-level | Static | Two birds | BIRD 1: "Nice view today, isn't it?" |
| 4 | OTS | Eye-level | Slight pan | Over bird 1 | BIRD 2: "Yeah... you can see everything from up here." |

- **Size** — standard abbreviations: WS / MWS / MS / MCU / CU / ECU / TWO-SHOT / OTS.
- **Angle** — Eye-level / Low / High / Overhead / etc.
- **Camera move** — REQUIRED per panel: Static (locked-off) / Push in / Pull out / Pan L-R / Tilt
  up-down / Track / Orbit / Handheld / Crane. Name it even when it's "static" — that's a deliberate
  choice. This column feeds the BLUE camera-movement annotation layer AND the Seedance `CAMERA`
  section directly.
- **Subject** — short label of what the shot is of.
- **Action / Dialogue** — 1–3 lines: what happens + framing note, plus any spoken line verbatim (the
  reference caption style). Becomes the beat lines in the Seedance `SCENES` section.

This table IS the scene's coverage plan. Every one of its 12+ rows becomes a storyboard frame with
its own description and camera move.

## 2. Storyboard frames (the drawn panels)

Lay the shots out as a numbered grid of **12+ panels** (3×4 or 4×3) or a vertical strip. Each panel:

- **Slug-line header:** `[shot#]. [INT./EXT.] [LOCATION] — [SHOT SIZE]`
  (e.g. `1. EXT. CLOCK TOWER — WIDE ESTABLISHING SHOT`).
- **The frame:** the shot, drawn in a consistent style — either clean pencil-sketch storyboard style
  OR the project's finished film look (match whatever the production wants; keep it consistent across
  all panels). For the finished-look version, attach the design-guide sheets so character/costume/
  location match.
- **`ACTION / DIALOGUE:` caption** below the frame: the action beat and any spoken line, verbatim
  from the shot list.
- **Camera move label** on the panel (e.g. `CAM: slow push in`) — every panel states its camera
  movement, per the reference.

Top of the sheet carries `TITLE:` / `PROJECT:` / `PAGE: x of y`.

**Where the text lives — captions are a post-process, never baked into the generation.** Image
models garble baked-in text (verified: "2003" came out "2005 / 2063 / SORTIE" across panels). So:
1. Generate the clean 12+ frame grid, face-locked (real face photo + still + clause), NO text in the
   image.
2. Add captions as a **post-processing layout pass** with PIL/Pillow: crop the grid into its N
   panels, then rebuild a sheet where each panel sits above a clean typographic caption box (slug
   line + `CAM:` move + ACTION/DIALOGUE), with a `TITLE / SCENE / PAGE` bar on top. This is exactly
   how the reference boards get clean frames AND crisp per-panel text.

**Working caption script** (`assets/caption_storyboard.py`, validated on a 3×4 board — even-grid crop + parchment sheet +
Arial, camera move in an accent color): crop each cell with a small inset to drop the white gutter,
paste onto a parchment canvas, draw slug (bold) / CAM (accent) / wrapped action per panel. Reuse the
same script per scene; only the captions JSON and the grid size (`--cols/--rows`) change. Keep a copy of
it with the project. Fonts: `/System/Library/Fonts/Supplemental/Arial Bold.ttf` and `Arial.ttf` exist
on macOS.

The colored **motion-annotation arrows** (RED body / BLUE camera / GREEN framing / ORANGE lighting /
YELLOW VFX) are the same kind of overlay pass — drawn on top of the clean frames, not generated.

## 3. Motion-annotated storyboard (the movement layer — the bridge to animation)

This is the "what movements to add" layer, and it's what feeds Seedance directly. Over each frame,
draw colored annotation arrows using this **standard color legend** (print the legend on the sheet):

- **RED = body movement** — the subject's motion: a kick arc, a lunge direction, a head turn, a
  reach. Draw the trajectory, not just the pose.
- **BLUE = camera movement** — push in, pull out, pan, tilt, orbit, track, handheld. Arrow shows the
  camera's move.
- **GREEN = framing / composition** — the frame type / composition note (tight frame, layered depth,
  circular composition, negative space for scale).
- **ORANGE = lighting direction** — where key light comes from / lighting hits.
- **YELLOW = VFX / energy** — elemental or effect motion (dust lift, air ribbons, water ripple,
  shockwave, energy vortex).

Each annotated panel also carries its shot number + framing + **lens** (e.g. `1. WIDE DIAGONAL 24mm`,
`2. HANDHELD CLOSE 35mm`). Lens choice is part of the plan — wide (16–28mm) for scale/action,
normal (35–50mm) for coverage, long (85mm) for compressed/isolated.

## How the annotations map to the Seedance prompt

The motion layer is not decoration — each color maps to a section of the dense Seedance prompt
(`seedance-storyboard-format.md`):

- **RED (body movement)** → the `SCENES` action lines. Name direction + distance + start/end pose.
- **BLUE (camera movement)** → the `CAMERA` section. If the camera must hold, say what it's NOT
  doing.
- **GREEN (framing)** → the shot size/lens stated per beat.
- **ORANGE (lighting)** → the `LOOK` section (key light behavior) — must also match the design
  guide's palette/lighting notes.
- **YELLOW (VFX/energy)** → inline `[VFX: ...]` tags on the relevant beat in `SCENES`.

So the sequence is: shot list defines the beats → storyboard frames show them → motion annotations
specify the movement → all of it assembles into the Seedance dense prompt. Nothing about the
movement is invented at the Seedance stage; it's all decided and drawn here first.

## Style-match rule (unchanged, still critical)

Whatever style the storyboard frames use, the written Seedance prompt's `LOOK`/`STYLE` sections and
the finished stills must describe the SAME world — palette, lighting, film stock — anchored to the
Production Design Guide's NOTES FOR ART DEPARTMENT. The storyboard plans motion; the design guide
owns the look; they must agree.
