---
name: storyboard-continuity-tracker
description: Tracks the physical state (position, pose, action) of the character, every recurring subject/object, and actively-handled props across a sequence of storyboard shots, and validates that each shot's starting state either matches the previous shot's ending state or is an explicit, shown, logical consequence of it. Use when building or ordering a multi-shot storyboard/raskadrovka, checking whether shot N+1 logically follows from shot N, or diagnosing why a shot sequence feels disconnected. Triggers on storyboard sequence, shot order check, continuity between frames, does the next shot follow, state jump between panels.
---

# Storyboard Continuity Tracker

## This project first (binding)

This skill arrives at every project knowing nothing about it. Before applying any default written below:

1. **Study this project.** Read its brief or script, every file in its references folder (images, video frames, saved prompts and their notes) and the results already approved in it. Say what you see in concrete terms before generating or writing anything.
2. **Learn from this project's results.** After each approved result, add to this project's `LESSONS.md` what was asked, the prompt or setting that produced it and why it worked; after each rejection, what failed and the fix. Read `LESSONS.md` before the next task. For this project it overrides the defaults below.
3. **Stay inside this project.** Never open, copy or imitate material from another project, brand or earlier job: no images, fonts, prompts, names or folders from elsewhere. What is missing comes from this project's own sources or from the user.
4. **Examples here are samples.** Every name, date, place or line used as an example in this skill is invented sample data. Do not carry it into the work.
5. **Improve the skill, not a memory of one project.** When a lesson would help any project, propose it to the user as a general rule with no project names in it.

## Why this exists

Shots generated independently (even from the same locked references) can silently teleport a subject's state between frames: a dog lying by a chair in shot 3 shows up drinking from a bowl across the room in shot 4 with no shown transition. Each shot can look individually correct and still make the sequence read as disconnected or broken when cut together, because nothing checked that shot 4's starting state actually follows from shot 3's ending state.

This skill is the check that catches that class of error **before** generation, while the shot list is still text.

## When this runs

At the storyboard-building stage of `loveart-video-animation`, after the shot list for a scene/block is drafted and before any panel is generated — this is a text-only check on the shot descriptions themselves. Use it together with `storyboard-reference-assembly` (which ensures the right assets are attached); this skill ensures the shots make sense as a sequence in the first place.

## Process

1. **Identify every entity to track** for the scene: the main character, every recurring subject/object present at any point in the scene (pet, secondary character), and any prop that gets actively picked up, moved, or handled (a glass, a drawer, a notebook).

2. **Build a state ledger**: one row per tracked entity, one column per shot number, each cell holding that entity's physical state (position + pose/action) at the **end** of that shot. Fill it in shot order from the drafted shot descriptions — this is a plain reading exercise, not invention.

3. **Check every shot-to-shot transition** for every tracked entity. The state at the **start** of shot N+1 must be one of:
   - **(a) Identical carryover** from shot N's end-state — the default, most common, always valid case (nothing about the entity needed to change, so it didn't).
   - **(b) An explicit, shown, causal consequence** of shot N's ending action — e.g. "dog lying by the chair, ears up" (end of shot N) → "dog gets up and walks to the door" (shot N+1) is a valid, direct consequence. The shot N+1 description must itself state the transition, not just a new resting state.
   - **Anything else is a continuity break**: e.g. shot N ends with the dog lying by the chair, and shot N+1 (with no transition shown) places it drinking from a bowl across the room. This is invalid even if each shot is individually plausible.

4. **When a break is found, fix it before generating** — one of:
   - Insert an additional connecting shot that shows the transition (the dog getting up, walking, settling).
   - Rewrite shot N+1's description so it explicitly states the causal action that explains the new state.
   - If neither fits the story, flag the specific conflict to the user rather than silently picking one.

5. **This applies independently to every tracked entity in the same shot**, not just the one the shot's headline description is "about." A shot framed as a close-up on the character's face still has to account for where the dog and the props are, even if they're only at the edge of frame or just offscreen.

6. **A held/handled prop cannot teleport** between hands, surfaces, or off-frame without a shown or stated action — the same rule as for subjects, applied to objects currently in use (a glass being carried, a drawer being opened, a notebook being picked up).

## Output format

Output the ledger alongside the finalized shot list so drift is visible at a glance:

```
| Shot | Dog (end state)                          | Character (end state)              |
|------|-------------------------------------------|-------------------------------------|
| 1    | lying by the chair                         | entering room, holding a glass       |
| 2    | lying by the chair (unchanged)  | setting the glass down on the table  |
| 3    | lying by the chair, being called   | holding a hand out to the dog      |
| 4    | staying put, refusing to move       | small amused smile                  |
| 5    | lying by the chair (unchanged - not shown leaving) | sitting at the table, opening the drawer |
| 6    | lying by the chair (unchanged)                | reading the letter, OTS framing     |
```

If a row shows a state with no shot explaining how it got there, that is the bug to fix, not a stylistic note.

## Relationship to other rules

This is a text-level planning check and does not replace the image-generation-time rules in `loveart-video-animation` (master-shot chaining, conditional pose continuity, "recurring subjects follow the script not the master image"). Those rules keep a single generated image accurate to its own shot description; this skill keeps the sequence of shot descriptions accurate to each other before any image exists.

After this text-level ledger is clean, run `scene-continuity-lock`: it turns the ledger into a CONTINUITY block inside every storyboard-panel prompt AND every final-frame prompt and QCs each generated panel/frame against it (seats, floor vs furniture, prop states, mirrored order on reverse shots, correct background wall from `location-room-map`).
