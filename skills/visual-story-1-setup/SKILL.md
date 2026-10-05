---
name: visual-story-1-setup
description: STEP 1 of 8 in the sequential visual-story pipeline. Project setup for turning a story into a consistent, identity-locked sequence of AI-generated images/video. Establishes the working folder, resolution, aspect ratio, project type, the references folder hierarchy (Characters / Locations / Props), Story-agnostic: FIRST inspect the references folder and report what is actually there, THEN ask the user to assign roles (which reference is the main character, which is secondary, the rest — people or animals) and to state the aspect ratio explicitly (never inferred). Run this FIRST, before any script or generation. Next step: visual-story-2-script.
---

# Visual story — Step 1: Project setup

**This is step 1 of an 8-part sequential pipeline. Do this first, in order:**
1. **visual-story-1-setup** ← you are here
2. visual-story-2-script
3. visual-story-3-cast-world
4. visual-story-4-references
5. visual-story-5-exposition
6. visual-story-6-production
7. visual-story-7-platform-qc
8. visual-story-8-storyboard

Do not skip ahead. Each step assumes the previous one is done.

## FIRST: inspect the references folder — before asking anything

This skill is **story-agnostic** — it must work for any project and assume NOTHING about the cast.
So the very first action is to **study the references folder and report what's actually there**, then
ask the user to assign roles. Never pre-fill character names, roles, or the look from prior knowledge.

1. **Locate and inventory `01_References/`** (or the project's references folder). For each
   `Characters/` subfolder, note: the folder name (may be a real name or a placeholder like
   "character 7"), whether it has a real face/subject photo, and whether it has a persona/concept
   subfolder. Do the same for any `Locations/` and `Props/` folders if present.
2. **Present the inventory to the user** as a plain list — "here's who/what I found in references" —
   so the role assignment is grounded in the actual files, not an assumption.

## New project vs. restart — when to ask for the folder

- **New project:** ASK the user where the project lives and where the references are — you don't know
  the paths yet, so get them explicitly before inspecting anything.
- **Restart / continuing an existing project:** do NOT ask for the location again — the working folder
  and references path are already known; reuse them. (If that known path is temporarily unavailable,
  say so and ask the user to reconnect it — don't re-ask as if it's a new project.)

## THEN ask the user, in one pass

Ask, and take explicit answers — never infer:

1. **Working folder.** For a NEW project, confirm where the project lives (and the references path).
   For a restart, this is already known — skip it.
2. **Who is the main character — and which reference is it?** Point the user at the inventory and let
   them map: which reference folder is the lead. Same question for the **secondary** character, and
   then the remaining references. **Characters can be animals, not only people.** The cast size is
   whatever the references contain — no reference left unused, no extra character invented. (Their
   tasks/arc/costume get worked out fully in step 3; here just capture role + which reference.)
3. **Aspect ratio.** Ask explicitly — 16:9 / 9:16 / 1:1 / 4:3 / other. **Never infer it from the
   references.** Lock it before the first generation; redoing a batch for the wrong ratio is
   expensive rework.
4. **Resolution.** 2K or 4K.
5. **Project type.** Series/TV, film, commercial/ad, music video, or other.

Capture the answers as short notes; step 3 (`visual-story-3-cast-world`) turns the role assignments
into the full cast & world bible (per-character goal/arc/costume/location/references + locations +
props).

## Build the folder structure

Inside the working folder, set up the references hierarchy and the scene-output convention now, so
everything generated later has a home. Full detail in `references/reference-taxonomy.md`.

**References — one folder per item, three categories:**
```
01_References/
  Characters/<character-name>/   -- real face photos + persona/concept (people AND animals)
  Locations/<location-name>/     -- location reference sheets (built in step 4)
  Props/<prop-name>/             -- recurring-prop reference sheets (built in step 4)
```

**Generations — scoped per scene, not per batch:**
```
Scene_<NN>_v<version>/
  Tests_v<version>/          -- exploratory attempts, not yet approved
  Working_frames_v<version>/ -- approved shots actually in the cut
```

## Decision tree — how much repeats

| Situation | What to do |
|---|---|
| Brand-new project | Full pipeline, steps 1→8 |
| New episode, same project | Skip this questionnaire if already established; reuse the locked cast bible + style + reference sheets exactly, go to step 2 for the new episode's script |
| Just adding one scene to an existing project | Skip to step 4 (references for any new character/location/prop), then step 5 (establishing shot) and step 6 |

## When done

Working folder confirmed, resolution/aspect/type locked, reference folders created. **Next:
`visual-story-2-script`.**
