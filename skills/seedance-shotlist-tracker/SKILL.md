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

## This project first (binding)

This skill arrives at every project knowing nothing about it. Before applying any default written below:

1. **Study this project.** Read its brief or script, every file in its references folder (images, video frames, saved prompts and their notes) and the results already approved in it. Say what you see in concrete terms before generating or writing anything.
2. **Learn from this project's results.** After each approved result, add to this project's `LESSONS.md` what was asked, the prompt or setting that produced it and why it worked; after each rejection, what failed and the fix. Read `LESSONS.md` before the next task. For this project it overrides the defaults below.
3. **Stay inside this project.** Never open, copy or imitate material from another project, brand or earlier job: no images, fonts, prompts, names or folders from elsewhere. What is missing comes from this project's own sources or from the user.
4. **Examples here are samples.** Every name, date, place or line used as an example in this skill is invented sample data. Do not carry it into the work.
5. **Improve the skill, not a memory of one project.** When a lesson would help any project, propose it to the user as a general rule with no project names in it.

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
   elsewhere (e.g. the clip numbers used in
   the project's shooting script) - don't renumber for the tracker's
   own convenience.
3. **One checkbox per clip** (not per internal CUT) - the user ticks a clip
   once it's been generated and accepted.
4. **One collapsible reference section at the top**, if the project has a
   shared style/canon note worth surfacing (e.g. a link back to
   the project's reference lock file or tag registry) - optional, keep it short;
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
  project's existing scene structure (e.g. the shooting script's
  table) rather than inventing new groupings.

## Relationship to other skills

`seedance-prompt-writer` is the source of truth for every prompt's actual
content. `storyboard-continuity-tracker` / `video-clip-continuity-chain`
are what make the prompts correct before they ever reach this skill. This
skill only ever runs after those are done - it has no opinion on shot
sizing, continuity, or prompt grammar, and never generates a prompt on its
own.
