---
name: visual-story-6-production
description: STEP 6 of 8 in the sequential visual-story pipeline. Scene production. Builds the STYLE LOCK block, establishes master shots, generates every mini-scene's coverage attaching the locked character/location/prop references, uses the "Change to..." technique for sequential shots, and propagates continuity/weather across a scene. Run AFTER visual-story-5-exposition (reference sheets built). Next step: visual-story-7-platform-qc.
---

# Visual story — Step 4: Scene production

**Step 4 of 5.** Before this: `visual-story-4-references` (approved reference sheets for every
character/location/prop must exist). After this: `visual-story-7-platform-qc`.

Full mechanics, prompt skeletons, and worked examples are in `references/prompt-engineering.md` —
read it; this SKILL.md is the checklist.

## Build the STYLE LOCK block first (once per project)

After the style references and first approved masters exist, write a STYLE LOCK block (photographic
mode, light, depth of field, atmosphere, palette, film/technical, aspect ratio) and paste it
**verbatim** into every production prompt. Never re-derive the look from memory per-prompt — that's
how drift creeps in over a long shot list. Template in `references/prompt-engineering.md`.

## Master shot + continuity per scene

- The first approved wide/establishing shot of a location is that scene's **master** — attach it
  (plus the location reference sheet from step 3) to every other shot in the scene, not just
  re-described in text.
- **Weather/physical-state propagation:** if the master shows rain/snow/mud, every character
  entering that space afterward shows visible evidence of it (wet hair, damp fabric) — stated
  explicitly, not left to the model.
- Every locked visual detail (a stain, a torn sleeve, a prop, a hairstyle state) is copied
  **verbatim** across every prompt in the same mini-scene.

## Attach references on every generation

For each shot, attach: the scene's master shot → each in-frame character's sheet + real face photo +
approved portrait → each in-frame location/prop reference sheet. One face photo per person in a
multi-character frame. (Character-lock attachment order detail lives in step 3's
`character-lock.md`.)

## "Change to..." for sequential coverage within a mini-scene

To build the next beat of a mini-scene (wide→close-up, gaze shift, next action, or relocating an
established look), use an already-approved shot as a reference and write a prompt starting with
"Change to [the next beat]: keep/same [restated costume + identity details]." Always also attach the
character's real face photo, even alongside the base image. This depicts the next beat of ACTION in
the same continuous scene — not an unrelated alternate. Full technique + the three variant types
(reframe / redirect gaze / relocate) in `references/prompt-engineering.md`.

## Prompt series per mini-scene

Each mini-scene gets one anchor prompt plus additional prompts scaled to how many discrete actions
happen in it — a simple establishing beat needs 1–2; a multi-action sequence needs 5–6+, one per
beat.

## When done

Every scene's coverage is generated against the locked style + references. **Next:
`visual-story-7-platform-qc` — platform operation notes and the QC pass before delivery.**
