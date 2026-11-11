---
name: story-continuity-ledger
description: Continuity memory for LONG illustrated stories (novels, series, multi-episode animation). Builds and maintains a versioned ledger of every recurring element — characters' current look and injuries, vehicles, props, locations, who-is-where — that ACCRUES as the story goes (a detail introduced in ch.2 becomes a locked reference for every later appearance) and CHANGES when the story changes it (new costume, a wound, a dented door, a coat handed over) by opening a new version that applies from that chapter on. Every recurring element gets its own reference image; prompts pull the version valid for the chapter being drawn. Includes a pre-generation checklist and a post-generation QC against the ledger. Use whenever generating more than one image across chapters/episodes of the same story, when a recurring object/vehicle/costume appears again, when a story event changes a character's look or a prop's state, or when the user complains about continuity errors ("it was different in the last chapter", "that is not her car", "he should have the coat"). Triggers on continuity, long story, series, recurring prop, vehicle reference, costume change, injury, recurring detail, errors between chapters.
---

# Story Continuity Ledger

## This project first (binding)

This skill arrives at every project knowing nothing about it. Before applying any default written below:

1. **Study this project.** Read its brief or script, every file in its references folder (images, video frames, saved prompts and their notes) and the results already approved in it. Say what you see in concrete terms before generating or writing anything.
2. **Learn from this project's results.** After each approved result, add to this project's `LESSONS.md` what was asked, the prompt or setting that produced it and why it worked; after each rejection, what failed and the fix. Read `LESSONS.md` before the next task. For this project it overrides the defaults below.
3. **Stay inside this project.** Never open, copy or imitate material from another project, brand or earlier job: no images, fonts, prompts, names or folders from elsewhere. What is missing comes from this project's own sources or from the user.
4. **Examples here are samples.** Every name, date, place or line used as an example in this skill is invented sample data. Do not carry it into the work.
5. **Improve the skill, not a memory of one project.** When a lesson would help any project, propose it to the user as a general rule with no project names in it.

## Why
Single-shot skills keep ONE scene consistent. Long stories break somewhere else: a detail established in chapter 2 (Character A's old delivery van) is re-invented in chapter 9 as a modern SUV; a wound from ch.5 vanishes in ch.7; Character B's uniform appears before the story gives it to her; one character shows up twice in a frame. The fix is a memory that (1) grows — every new recurring detail is registered and gets a reference image — and (2) is versioned — when the story changes a detail, a new version starts at that chapter and the old one stays valid for earlier chapters.

## Files (per project, next to the illustrations)
- `continuity/LEDGER.md` — the registry (format below). Single source of truth.
- `continuity/refs/<ENTITY_ID>__v<N>.png` — one reference image per entity version (prop sheet, vehicle turnaround, location master, costume sheet).
- `continuity/CHAPTER_STATE.md` — per chapter: who is present, where, what they carry/wear, what changed at the END of the chapter.
Characters' identity sheets stay in `characters/`; the ledger references them and adds only what changes (costume, wounds, age).

## Ledger format
```
## VAN_A  (vehicle)                first: ch03   owner: Character A
v1  ch03–ch05  old faded delivery van, single bench seat for 3 in the cab, closed cargo box, no back seat. ref: refs/VAN_A__v1.png
v2  ch06–      + dented left door, broken headlight (after the collision in ch06). ref: refs/VAN_A__v2.png
RULES: 3 people inside = shoulder to shoulder on the bench, nobody in a back seat. Whoever drives sits left.
```
Each entity: ID, type (character-state / vehicle / prop / costume / location / wound), first chapter, versions with chapter ranges, one-line visual spec (fixed wording reused verbatim in prompts), reference image, RULES (physical logic the model gets wrong).

## Process

### A. Building / growing (run once per chapter, in story order)
1. Read the chapter. List every element that is visual and could recur: vehicles, weapons, gadgets, jewellery, scars, costumes, rooms, signs-free locations, animals.
2. For each: already in ledger? → check whether the chapter CHANGES it (damage, handover, new clothes, injury, healing, age). Not in ledger and appears ≥2 times in the book (or is plot-important) → ADD with v1 starting this chapter.
3. Change detected → close current version at previous chapter, open v(N+1) from this chapter, write what changed and the cause.
4. Generate a reference image for every new entity/version BEFORE any scene uses it (prop/vehicle sheet: 3/4 front, side, rear, interior if relevant; neutral background; same art style as the book). Approve, save to `continuity/refs/`.
5. Update `CHAPTER_STATE.md`: present characters, location, what each wears/carries, end-of-chapter changes.

### B. Before every generation (checklist)
1. Determine the chapter → pull valid versions of every entity in the frame.
2. Attach: style refs → character sheets (+portrait) → entity refs (vehicle/prop/location) for the valid version. Name each image's role in the prompt.
3. Paste each entity's fixed spec line verbatim + its RULES.
4. State the exact head-count: "exactly N people: A, B, C — each appears once".
5. Age/costume/wound lines from the ledger for that chapter (e.g. "Character A's left hand bandaged" from ch05).
6. No-text clause.

### C. After every generation (QC against ledger)
Reject and regenerate if any: a character duplicated or missing; wrong version of a prop (modern car instead of the old van, uniform too early); a wound/scar missing or on the wrong side; impossible seating/physics vs RULES; age drift (adult shown as a child); text/subtitles; identity drift from the character sheet. Log rejects with the reason in `continuity/QC_LOG.md` — repeated reasons become new RULES.

### D. When the user corrects something
Their correction is a ledger edit first, an image fix second: update/add the entity or RULE, then regenerate every affected frame (search CHAPTER_STATE for chapters in that version's range).
