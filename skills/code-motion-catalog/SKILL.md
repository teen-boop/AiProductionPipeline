---
name: code-motion-catalog
description: Catalog and kit for impressive 3D motion graphics built in code with three.js (no generator credits, the exact product every frame, film look from accumulation rendering, synthesized sound). Holds style cards with what makes each style work and its pitfalls, ready sample styles (Studio Product hero film, Split-Flap Board, Layer Stack explainer), the STAGE and SOUND kits, a player, a headless-Chrome renderer (storyboard stills and MP4 with sound) and a score template for longer edits. Use when the user wants a product hero shot or lock-up, a numbers or ranking board, a layered "how it works" explainer, a 3D chapter inside a presentation or an ad, when the user pastes a three.js style reference to learn from, or when animation-project-manager asks for a code animation. Triggers - 3D product animation, three.js motion graphic, studio product shot, split-flap board, layer stack, explainer in 3D, add this animation style to the catalog.
---

# Code motion catalog

## This project first (binding)
1. **Study this project.** Read its brief, references and approved results; the product shape and colours come from the
   project's approved product reference, never from a sample file.
2. **Learn from this project's results** in the project's `LESSONS.md`.
3. **Stay inside this project.** No names, images, fonts or copy from another project.
4. **Examples here are samples.** TIDE and every line in `kit/styles/` are invented sample data.
5. **Improve the skill, not a memory of one project:** general lessons go to `references/CATALOG.md` without project names.

## What is here
- `references/CATALOG.md` style cards (look, the idea that makes it work, build tricks, camera, pitfalls), how to use the
  pieces in a longer edit, sound rules.
- `kit/` copy it into the project as `04_EDIT/code-motion/`:
  - `lib/stage.js`, `lib/sound.js` the kits; never edit them in a project.
  - `styles/*.js` sample styles; copy one and change its content block.
  - `player.html?style=<name>` live preview with scrub and sound.
  - `render.mjs` `stills <style> <dir> t1,t2` (storyboard, 16 samples) and `video <style> <out.mp4>` (full samples, sound,
    -15 LUFS); `NO_TEXT=1` renders without the overlay type. Needs Chrome and `puppeteer-core` (`PUPPETEER_CORE`,
    `CHROME_PATH` env vars if they are not in the default places).
  - `score-template.html` + `score.mjs` synthesized music bed and hits for a whole edit, mixed under the chapters.

## Workflow
1. **Pick the style** from the catalog by what the beat must do: one product and one claim -> Studio Product; a list,
   ranking or numbers -> Split-Flap; a process or a stack -> Layer Stack.
2. **Content block first:** finishes and profile from the product reference, rows or layers, copy, the schedule.
   Facts and numbers need a source; otherwise say what happens, not how much.
3. **Storyboard:** `node render.mjs stills ...` 3-6 stills, notes per beat (time, exact text, what moves, camera, sound),
   assumed facts listed. Wait for the user's OK.
4. **Render** `node render.mjs video ...`; look at 5-6 frames (legibility on a phone, nothing cut at the frame edge,
   lock-up lines under ~1050 px wide at 1920), check loudness.
5. **Cut it in** (see CATALOG "Using the pieces in a longer edit"); record what worked in the project's `LESSONS.md`.

## Adding a new style ("learn from this")
When the user pastes a three.js style reference (style card + source): save the source as `kit/styles/<id>.js` with
invented sample content, add a style card to `references/CATALOG.md` (look, motion, the idea that makes it work, build
tricks, camera, pitfalls, good for), and keep the kits unchanged unless the new style needs a kit feature.

## Rules
- `update(t)` sets the whole frame for t: no `Math.random`, `Date` or timers; use `K.rng(seed)`.
- Everything is built in code: no downloaded models, images or HDRIs.
- No made-up claims on screen. Big, readable words; the first frame is already worth looking at; the last second holds.
