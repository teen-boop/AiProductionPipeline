---
name: ai-visual-production-director
description: >-
  The entry-point orchestrator for this whole skill bundle — turning a
  story/script into a consistent, identity-locked sequence of AI-generated
  images and video. Reads what phase of work the user is asking for
  (raw screenplay parsing, character/reference setup, turning prose into a
  shot list, shot sizing and continuity, reference assembly, still-image
  prompt writing, camera/transition tracking, video-prompt writing) and
  routes to the correct companion skill(s) in the correct order, instead of
  leaving skill sequencing to memory. Tool-agnostic — works with any image/video
  generation platform; two companion skills (`loveart-video-animation`,
  `loveart-project-director`) are the Lovart-specific implementation of
  some of these phases if that's the platform in use. Use whenever starting
  or resuming a visual-production project, or when it's unclear which skill
  in this bundle applies to the current request. Triggers on which skill do
  I need, project pipeline, what's next for this project, start a new
  visual project, production pipeline.
---

# AI Visual Production Director

## Why this exists

This bundle is a set of narrow, single-purpose skills (character locking,
narrative segmentation, shot sizing, continuity, reference assembly,
still-prompt writing, camera tracking, video-prompt writing) deliberately
kept separate so each one stays sharp and independently correctable. The
failure mode that creates is picking the wrong skill for the moment,
running them out of order, or silently skipping one. This skill is the
dispatcher: it doesn't replace any of the specialist skills, it decides
which ones apply right now and in what order.

## The skill roster, by phase

**Phase -2 — Generation backend** (once per project, before anything is
generated; re-run when a tool or key changes)
- `generation-backend-setup` — asks whether a CLI, an API or an MCP
  connector is available, connects it safely (keys only in environment
  variables, never in files), tests it and records it in
  `pipeline.config.json`. If nothing can be connected it switches the
  project to MANUAL MODE: it collects the references, sorts them into
  `references/<Category>/<name>/` with an index, and hands over the
  prompt list plus a manual pack (`manual-image-pack`).

**Phase -1 — Script/Story Parsing** (whenever the source material is a
formatted screenplay OR any narrative text — a short story, novel
excerpt, literary adaptation — with actual scenes, characters, and
dialogue, rather than an already-itemized shot list)
- `script-extractor` — reads the source scene by scene (or scene-equivalent
  unit, for prose) and extracts five categories per scene (location with
  INT/EXT and day/night, characters present, props, key actions,
  wardrobe/appearance), keeping every detail tied to its specific scene
  and building a cross-reference index for anything recurring (a
  character's standing wardrobe rule, a prop that reappears, a location
  used more than once). This is what turns raw source material into
  usable input for Phase 0 (which characters need locking, what their
  default look is) and Phase 3 (what a shot's props/wardrobe/day-night
  should resolve to). If the source is pure camera-direction prose
  ("camera flies toward X, then we see Y" — no scenes/characters to
  extract, just a shot path already), skip straight to Phase 1 —
  `storyboard-narrative-breakdown` handles that case directly instead.

  **Its output is binding downstream, not just informational.** Once a
  script-extractor breakdown exists for a project, Phase 3 and Phase 4
  below must resolve a shot's day/night, wardrobe, and location facts from
  that breakdown's per-scene entry and cross-reference index — never
  re-derive or re-guess them from the shot's own one-line description in
  isolation. This is the specific mechanism that stops day/night from
  flipping between shots of one continuous scene, and stops a character's
  established wardrobe or a location's established look from silently
  drifting shot to shot — see each skill's own Process for exactly how it
  applies this.

**Phase 0 — Character & Reference Setup** (run once per character/asset,
before any scene generation)
- `character-identity-lock-setup` — for every recurring character, build a
  locked reference set (turnaround sheet + bust portrait per age/stage)
  from real photo identity sources, hosted and indexed so every later
  generation attaches the correct one instead of drawing the face freehand.
- `detail-reference-intake` — if the project keeps a "working detailed
  references" intake folder for ad hoc captured details (props, location
  angles found during other work), run this at the start of every session
  to catalogue anything new before storyboarding.

**Phase 1 — Narrative → Shot List** (only if starting from continuous
prose rather than an already-itemized shot list)
- `storyboard-narrative-breakdown` — segments a paragraph of "camera does
  X, then Y, then we see Z" narrative into discrete, numbered mini-scenes
  (location, event, incoming/outgoing visual bridge), and writes the first
  pass of prompts for each. If the shot list already exists as discrete
  items, skip straight to Phase 2.
- Run `storyboard-camera-continuity-ledger` **alongside** this phase, not
  after it — as each mini-scene gets its camera action and bridge data
  extracted, log it into the ledger immediately (see that skill's own
  Process). This keeps the camera-movement/transition record synchronized
  with the shot list from the start instead of reconstructed later.

**Phase 2 — Shot Refinement** (on the text shot list, before any image
exists)
1. `storyboard-shot-selection` — for every beat, determine which shot
   size's defined narrative job (orientation / gesture / action / emotion
   / object contact / detail accent / dialogue / relationship) it actually
   needs, and write the reason inline. Flags/fixes adjacent shots sharing
   the same job without justification.
2. `storyboard-continuity-tracker` — build the state ledger for the
   character and every recurring subject/object/handled prop across the
   shot list, and verify each shot's starting state is either identical
   carryover or an explicit shown consequence of the previous shot's
   ending state. Fixes or flags state-teleportation.

**Phase 3 — Reference Assembly** (per shot, before generation)
- `storyboard-reference-assembly` — reads the project's locked-reference
  index in full, resolves every noun in the shot (including the full
  canonical environment of its location, not just what the one-line
  description names) to its exact locked asset from Phase 0, and produces
  the attachment manifest for generation.

**Phase 4 — Still-Image Prompt Writing**
- `cinematic-prompt-writer` — writes the actual wide/medium/close-up
  prompt text for a shot, in the project's locked style (or a sensible
  default if none exists yet), using the Phase 3 attachment manifest.
- If the project's generation platform is Lovart specifically, use
  `loveart-video-animation` (and its orchestrator `loveart-project-director`)
  instead — those two skills cover the same phases with Lovart-specific
  technique (face-replacement method, master-shot chaining, the "Change
  to:" reframe discipline, Nano Banana/GPT Image 2.0 specifics).
- If the user generates the frames BY HAND (automation is slow, blocked or
  too costly), use `manual-image-pack`: it packs every frame still to make
  into its own folder (PROMPT.txt + numbered reference images + INFO.txt),
  then collects the user's RESULT files back into the project, QCs them and
  wires them into the storyboard and the video prompts.

**Phase 5 — Video/Animation Prompt Writing**
- `seedance-prompt-writer` — writes production-grade Seedance-format video
  prompts, reading the camera-movement and transition data straight out of
  the Phase 1 ledger instead of re-deriving it from the original narrative.
  Merges in a project's own mandatory rules (no-music, color-fidelity
  doctrine, etc.) when the project defines them.
- `cinema-director-v3` — a newer, tool-agnostic alternative covering the
  same ground on a locked 16-slot prompt spine (assets, geometry map,
  FOV-degree optics, physics, acting, audio, a locks chain), plus dialogue/
  performance scenes and lipsync, which `seedance-prompt-writer` doesn't
  cover. Prefer this one for a project with no established Seedance-prompt
  conventions of its own; use `seedance-prompt-writer` when the project
  already has mandatory rules this skill should inherit.
- Whenever a scene is split into more than one clip meant to play
  consecutively, run `video-clip-continuity-chain` before writing each clip
  after the first — it forces the new clip's prompt to explicitly restate
  the exact inherited state of every tracked entity from the end of the
  previous clip, rather than leaving it implied.
- Once a batch of clips is finalized, run `seedance-shotlist-tracker` to
  package them into one interactive, checkbox-per-clip production tracker —
  a delivery/tracking layer only; it never writes or simplifies prompt
  content, it packages what the video-prompt skill already produced.

## Motion graphics — a separate, parallel track

Everything above assumes character-driven narrative scenes. If the work
is instead animated charts, typographic explainers, or collage/camera-move
motion graphics with no characters to lock, that's a different track
entirely: start at `motion-graphics-director` instead of Phase -1. It
owns its own routing (CODE via `motion-remotion-build` vs VIDEO via
`motion-video-route`), its own reference-locking skill
(`motion-design-references`), and its own style system
(`motion-style-core`) in place of this bundle's character/location
reference-locking phases. Don't mix the two tracks on one shot — a shot
either has characters and a scene (use the phases above) or is a
chart/typography/collage shot with a locked style pack (use
`motion-graphics-director`).

## Process

0. **Check `pipeline.config.json`.** If it is missing, run
   `generation-backend-setup` first. If it says `"type": "manual"`, every
   generation step ends in prompts + a manual pack instead of a call.
1. **Identify the phase the current request actually belongs to** — don't
   assume. "Let's build a shot list for this scene" is Phase 1/2 even if
   some Phase 0 references are still missing (in which case, flag the gap
   and route back to Phase 0 for just the missing piece, rather than
   skipping it). If the user hands over a formatted screenplay rather than
   prose or a shot list, that's Phase -1 first, regardless of what phase
   they think they're asking for.
2. **Run the skills for that phase in the documented order.** Don't skip a
   step because it "seems obvious this time" — skipping the
   obvious-seeming step is exactly where continuity drift and identity
   drift come from in practice.
3. **If a phase surfaces a problem** (continuity break, missing reference,
   unjustified shot, missing bridge detail), fix or flag it before moving
   to the next phase — don't carry a known problem forward into generation
   "to save time." A mismatch caught at the text stage is free to fix; the
   same mismatch caught after a paid generation is not.
4. **When resuming a project across sessions**, re-check Phase 0 first — a
   references-intake folder may have gained new files, or the user may
   want to add an age/stage to an already-locked character, since the last
   session even if nothing else changed.
5. **State which phase and which skill(s) are active** when doing the
   work, so the user can follow and correct the routing itself if it's
   wrong — this routing is a working assumption, not a black box.

## What this skill is not

It doesn't contain generation rules, taxonomy, style blocks, or continuity
logic itself — all of that stays in the specialist skills so each one can
be corrected independently. This skill only owns the map of which one
applies when.
