# DOCTRINE — what's extracted from the 4 tutorials

A set of rules the skill will be built on. The block library is in `PROMPT-LIBRARY.md`.

---

## T1 · Omni Flash (video route)

- Motion graphics on video models are usable 80–90% of the time. Omni Flash is strong at
  **understanding reference** and **typography**, weak at resolution.
- **Style-lock + swap action.** The prompt splits into a frozen part (STYLE / AUDIO / AVOID) and a
  swappable part (SHOT / ACTION). Only ACTION changes from clip to clip.
- **Master Style Sheet** — one 16:9 board, 6 panels: type specimen · palette with usage rules ·
  component zoo (one construction logic) · mini-scenes · motion thumbnails · the stage (a permanent
  empty background). `ONE IMAGE = THE RULEBOOK`.
- The sheet's skeleton is **style-agnostic** — the same for vox / clay / blueprint.
- **Two routes:** SAFE (style ref → image → video) for complex content, text, people, logos; FAST
  (style ref + prompt → video) for simple shapes. `SIMPLE = SKIP THE FRAME · COMPLEX = LOCK THE FRAME`.
- **The style block is mandatory in the video prompt too**, even when a frame is attached —
  otherwise the style drifts mid-clip.
- "Use the sheet for **materials only** — do NOT copy its layout or its flatness".
- Rule of thumb: ✅ big blocks, logos, chunky type · ❌ fine type, micro-detail. `LESS MOTION = SAFER`.
- One committed camera move per clip; the camera is an actor.
- Known faces get blocked → generate the image in a different model, overlay black bars over the
  eyes image-to-image, then go to video.
- Models: Omni Flash > Seedance 2.0 (cinematic, but falls apart on numbers) > Happy Horse;
  Kling 3.0 without a reference mode is unusable.

## T2 · Remotion charts (code route)

- One prompt = the whole project: server + style + animation + data.
- **Props, not code** — every visual decision is an editable prop in Studio.
- **Determinism** — no randomness; all noise comes from the frame number, otherwise flicker
  appears under parallel rendering.
- **Exact numbers** — blocks are explicitly tagged `(exact numbers)`.
- **Anti-default** — name the default the model will produce, and forbid it.
- **One sort order** for both coloring and reveal.
- **Physics driven by the chart's meaning** ("chart about nobody reaching a majority → no bouncy
  cartoon energy").
- **Real, cited data** + a control number for a sanity check + `no demo badge`.
- **Data is baked into props**, the render never hits the network.
- **Text never goes inside the filter.**
- Style inheritance by words: "next composition in the same project, same paper look".
- Toggles for comparison: freeze / lattice / scaffolding.
- Pace is described with a physical metaphor: "like a hand dragging a marker, not a bouncy ease".

## T3 · Claude Design — 5 levels of anti-slop

1. **Data.** Real numbers → animated chart → **codify the style as an asset**: "use this style for
   all future bar charts."
2. **Font — the #1 slop tell.** Never leave the default. Identify someone else's font:
   fonts.inuse.com. Pull typography off a site: Firecrawl with the `branding` flag. Free sources:
   Fontshare, Open Foundry, Google Fonts, Typewolf. Screenshot the font → "find the closest free
   equivalent."
3. **Icons.** Download the whole pack, **one style for the entire piece**, never mix packs.
4. **Lottie / images.** Keep ready-made Lottie JSON in a local repository and hand it over as an
   asset library; insert generated images as layers.
5. **Transcript + research.** Video → transcript with word-level timecodes → an agent finds the
   moments where animation would add value → a research agent pulls real numbers to match what's
   said. **"Most people miss the research step, so they get inaccurate data."**

## T4 · Vox explainer with Claude Code + Remotion

- **Order of work: script → VO → scenes.** The script is the timeline; every script beat maps to a
  visual. Table: VO line | midground asset | foreground asset | prompt for each.
- **Locked visual system**: one shared background for all scenes, same fonts and palette; only the
  mid/foreground change. This is what produces the feel of one continuous shot instead of a
  cut-up edit.
- **Three-layer scene**: background (locked, static) / midground (black-and-white halftone cutouts
  of people, popping up) / foreground (structures, vehicles, scenery).
- **Folder architecture**: one scene = one folder; the shared background is copied into each.
- Cutouts: transparent PNG → "make it black-and-white with a halftone pattern" → magazine texture.
- **Animate with intent**: only `spring` (pop) and `interpolate` (travel/fade). Don't name
  functions — write the intent in English.
- **An offset red outline behind every cutout** — the style's signature and a cheap pseudo-3D trick.
- **Prop controls are mandatory**, values tweaked in Studio **must be saved back into props**.
- **Master sequence**: scenes placed back to back, each lasting as long as its own VO segment.
- VO from ElevenLabs; choppy audio while scrubbing in Studio is normal, clean after render.
- Final output: a rendered 1080p MP4 with music and VO, or a clean composition plus mixing in
  Premiere.
- Assets can be pulled straight from Claude Code via MCP connectors.

---

## SUMMARY ARCHITECTURE (what goes into the skill)

```
                   ┌─────────────── STYLE CORE (shared) ───────────────┐
                   │   palette · font · texture · one hero accent      │
                   └──────────────┬───────────────────┬───────────────┘
                                  │                   │
                      VIDEO ROUTE │                   │ CODE ROUTE
                    (Omni Flash)  │                   │ (Remotion)
                                  ▼                   ▼
                    style sheet → image → video    props + exact numbers
                    dynamics, collage, camera       numbers, charts, typography
                    big blocks, logos                programmatic scale
                                  │                   │
                                  └────────┬──────────┘
                                           ▼
                                   MASTER SEQUENCE
                              script → VO → scenes → mix
```

**The shared doctrine layer for both routes:** lock-and-swap · exact numbers · anti-default · one
hero · determinism · motion driven by meaning · font named explicitly.
