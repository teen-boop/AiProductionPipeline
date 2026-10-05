---
name: loveart-project-director
description: The entry-point orchestrator for a Love Art video-animation project. Reads what phase of work the user is asking for (project setup, reference locking, storyboarding, full-panel generation, video-prompt writing) and routes to the correct companion skill(s) in the correct order, instead of leaving skill sequencing to memory. Use whenever starting or resuming work on a Love Art story/animation project, or when it's unclear which skill/stage applies to the current request. Triggers on new project setup, what's next for this project, build the storyboard, generate the panels, which skill do I need, project pipeline, raskadrovka workflow.
---

# Love Art Project Director

## Why this exists

This project accumulates skills as distinct, narrow tools (one per concern: shot-size logic, continuity, reference assembly, folder intake...). That's correct for keeping each one sharp, but it creates a new failure mode: picking the wrong skill for the moment, running them out of order, or skipping one silently. This skill is the dispatcher — it doesn't replace any of the specialist skills, it decides which ones apply right now and in what order, so that decision isn't re-made ad hoc every session.

## The skill roster, by phase

**Phase 1 — Project Setup** (`loveart-video-animation` Stage 1)
- Confirm new-project status and output folder (per the standing project-folder rule: originals stay untouched, outputs go to a dedicated project folder).
- Get the script approved, in text, before any visual work starts.

**Phase 2 — Reference Locking** (`loveart-video-animation` Stage 2, plus `detail-reference-intake`)
- Lock the main character (face + body), locations (with named angles), recurring subjects/objects, and clothing.
- Run `detail-reference-intake` at the start of this phase (and re-check it at the start of any later session) to pull in any new screenshots the user has dropped into `reference/working detailed references/` and fold them into the locked-reference index.

**Phase 3 — Storyboarding** (three companion skills, run in this fixed order, on the text shot list, before any image exists)
1. `storyboard-shot-selection` — for every beat, determine which shot size's defined narrative job (orientation / gesture / action / emotion / object contact / detail accent / dialogue / relationship) it actually needs, and write the reason inline. Flags/fixes adjacent shots that would share the same job without justification.
2. `storyboard-continuity-tracker` — build the state ledger for the character and every recurring subject/object/handled prop across the now-sized shot list, and verify each shot's starting state is either identical carryover or an explicit shown consequence of the previous shot's ending state. Fixes or flags state-teleportation.
3. `storyboard-reference-assembly` — per panel, read the locked-reference index in full, resolve every noun in the shot (including the full canonical environment of its location, not just what the one-line description names) to its exact locked asset, and produce the attachment manifest for generation.

**Phase 4 — Generation** (`loveart-video-animation` Stage 4)
- Master-shot chaining, "Change to:" reframe discipline, face replacement technique — using the manifests and ledger produced in Phase 3 as the source of truth for what to attach and what state each shot should show.

**Phase 5 — Video Prompts** (`seedance-prompt-writer`, which itself wraps `loveart-video-animation`'s video-specific rules plus `video-clip-continuity-chain`, delivered via `seedance-shotlist-tracker`)
- Write every Seedance prompt with `seedance-prompt-writer` — it merges the general Seedance block-structure technique (FOV in degrees, @tag references, positive-only phrasing) with this project's mandatory rules (NO MUSIC, English-by-default, color fidelity to locked references).
- Whenever a scene is split into more than one clip meant to play consecutively, run `video-clip-continuity-chain` before writing each clip after the first: re-read the previous clip's exact ending state for every prop/subject. Per `seedance-prompt-writer`'s resolution of the context-isolation rule, write that inherited state as a plain present-tense fact in the new clip's own `SCENE CONTEXT`/`POSITIVE LOCKS` — never as a citation to the previous clip's filename. This is not optional polish — an uncaught mismatch here is only visible after a paid generation completes, unlike an image-storyboard mismatch which is free to catch and fix.
- Once a batch of clips (a scene, several scenes, or the full episode) is finalized, run `seedance-shotlist-tracker` to package them into one interactive, checkbox-per-clip HTML production tracker (published as an Artifact) — this is a delivery/tracking layer only, it never writes or simplifies prompt content itself, only `seedance-prompt-writer`'s real output goes into it.

## Process

1. **Identify the phase the current request actually belongs to** — don't assume; a request like "let's build a storyboard for scene X" is Phase 3 even if some Phase 2 references are still missing (in which case, flag the gap and route back to Phase 2 for just the missing piece, rather than skipping it).
2. **Run the skills for that phase in the documented order.** Don't skip a step because it "seems obvious this time" — the whole point of splitting these out was that skipping the obvious-seeming step is exactly where past drift came from (a locked desk reference existed and still didn't get used, because no explicit reference-assembly pass ran).
3. **If a phase surfaces a problem** (continuity break, missing reference, unjustified shot), fix or flag it before moving to the next phase — don't carry a known problem forward into generation "to save time."
4. **When resuming a project across sessions**, always re-run Phase 2's `detail-reference-intake` check first — the working-references folder may have gained new files since the last session even if nothing else changed.
5. **State which phase and which skill(s) are active** when doing the work, so the user can follow and correct the routing itself if it's wrong — this routing is a working assumption, not a black box.

## What this skill is not

It doesn't contain generation rules, taxonomy, or continuity logic itself — all of that stays in the specialist skills so each one can be corrected independently. This skill only owns the map of which one applies when.
