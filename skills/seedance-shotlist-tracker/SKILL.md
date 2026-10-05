---
name: seedance-shotlist-tracker
description: >-
  Packages an already-written set of Seedance prompts (from
  seedance-prompt-writer) into ONE self-contained, interactive HTML
  shot-list document — a checkbox per scene/clip, a copy button on every
  prompt, progress persisted in the viewer's browser. This is a delivery/
  tracking layer, not a prompt-writing method: it never invents its own
  prompt content or a weaker style-prefix format, it packages the project's
  real, already-approved prompts verbatim. Use after a batch of clips for a
  scene or episode has been finalized, to produce or update the shootable
  production checklist. Triggers on shot list, shotlist, production
  tracker, checklist for the episode, HTML shotlist, track which clips are
  done.
---

# Seedance Shotlist Tracker

A small, focused companion to `seedance-prompt-writer`. Where that skill
writes the *content* of each prompt, this skill handles *delivery*:
assembling everything already written into one browsable, trackable
document instead of a folder of loose `.md` files with no shared view of
progress.

## When this runs

At Phase 5 of `loveart-project-director`, after a batch of Seedance prompts
exist (a scene, a block of scenes, or the full episode) and the user wants
a single document to work from while actually generating - ticking off
clips as they're produced, copying each prompt straight into Seedance.

## What this is not

This is not a second prompt-writing grammar. Never fall back to a
simplified Style Prefix / Characters / Scene / CUT format here - every
prompt embedded in the tracker is the real, full prompt already produced by
`seedance-prompt-writer` (16-slot spine, CRITICAL blocks, the project's
actual @tag registry resolved to visual descriptors, etc.), copied in
verbatim. This skill only lays them out with checkboxes and copy buttons;
it does not simplify or re-derive them.

## Process

1. **Gather the finalized prompts** for the scope being tracked (one scene,
   several scenes, or the whole episode) from the project's working
   folder - the actual prompt text inside each already-written `.md` file's
   code block.
2. **Preserve the project's real scene/clip numbering** exactly as used
   elsewhere (e.g. clip 1-17 of the full episode per
   `EPISODE_shooting_script_full.md`) - don't renumber for the tracker's
   own convenience.
3. **One checkbox per clip** (not per internal CUT) - the user ticks a clip
   once it's been generated and accepted.
4. **One collapsible reference section at the top**, if the project has a
   shared style/canon note worth surfacing (e.g. a link back to
   `LOCKED-REFERENCES.md` or the @tag registry) - optional, keep it short;
   this is a working checklist, not a re-export of the bible.
5. **Build as a self-contained HTML file**: inline CSS/JS, no external
   dependencies, a copy button per prompt block, checkbox state persisted
   in the viewer's own browser storage so progress survives reloads.
6. **Publish it properly** - this is an interactive page meant to be opened
   and used repeatedly, not a static file to read once. Use the Artifact
   tool to publish it (self-contained HTML + browser-local persistence is
   exactly what Artifacts are for) rather than just writing a local file.
   When updating an already-published tracker with new/changed clips,
   republish to the same Artifact URL rather than creating a new one.
7. **On revision** (a clip's prompt changes, a new clip is added, scope
   expands from one scene to the full episode): re-publish the same
   document with the change applied. Keep existing clip numbers stable so
   the viewer's saved checkbox progress doesn't reset.

## Output shape

- Title bar with the project/scope name.
- Optional collapsible canon/reference note at the top.
- One block per clip: clip number + one-line description (what happens),
  a checkbox, and the full prompt in a monospace block with a Copy button.
- Clips grouped by scene when tracking a multi-scene span, matching the
  project's existing scene structure (e.g. `EPISODE_shooting_script_full.md`'s
  table) rather than inventing new groupings.

## Relationship to other skills

`seedance-prompt-writer` is the source of truth for every prompt's actual
content. `storyboard-continuity-tracker` / `video-clip-continuity-chain`
are what make the prompts correct before they ever reach this skill. This
skill only ever runs after those are done - it has no opinion on shot
sizing, continuity, or prompt grammar, and never generates a prompt on its
own.
