---
name: storyboard-continuity-tracker
description: Tracks the physical state (position, pose, action) of the character, every recurring subject/object, and actively-handled props across a sequence of storyboard shots, and validates that each shot's starting state either matches the previous shot's ending state or is an explicit, shown, logical consequence of it. Use when building or ordering a multi-shot storyboard/raskadrovka, checking whether shot N+1 logically follows from shot N, or diagnosing why a shot sequence feels disconnected. Triggers on storyboard sequence, shot order check, continuity between frames, does the next shot follow, state jump between panels.
---

# Storyboard Continuity Tracker

## Why this exists

Shots generated independently (even from the same locked references) can silently teleport a subject's state between frames: a cat sitting on a desk in shot 3 shows up grooming itself on a windowsill in shot 4 with no shown transition. Each shot can look individually correct and still make the sequence read as disconnected or broken when cut together, because nothing checked that shot 4's starting state actually follows from shot 3's ending state.

This skill is the check that catches that class of error **before** generation, while the shot list is still text.

## When this runs

At the storyboard-building stage of `loveart-video-animation`, after the shot list for a scene/block is drafted and before any panel is generated — this is a text-only check on the shot descriptions themselves. Use it together with `storyboard-reference-assembly` (which ensures the right assets are attached); this skill ensures the shots make sense as a sequence in the first place.

## Process

1. **Identify every entity to track** for the scene: the main character, every recurring subject/object present at any point in the scene (pet, secondary character), and any prop that gets actively picked up, moved, or handled (a cup, a laptop lid, a sketchbook).

2. **Build a state ledger**: one row per tracked entity, one column per shot number, each cell holding that entity's physical state (position + pose/action) at the **end** of that shot. Fill it in shot order from the drafted shot descriptions — this is a plain reading exercise, not invention.

3. **Check every shot-to-shot transition** for every tracked entity. The state at the **start** of shot N+1 must be one of:
   - **(a) Identical carryover** from shot N's end-state — the default, most common, always valid case (nothing about the entity needed to change, so it didn't).
   - **(b) An explicit, shown, causal consequence** of shot N's ending action — e.g. "cat sitting on desk, pawing at the book" (end of shot N) → "cat jumps down off the desk" (shot N+1) is a valid, direct consequence. The shot N+1 description must itself state the transition, not just a new resting state.
   - **Anything else is a continuity break**: e.g. shot N ends with the cat sitting on the desk, and shot N+1 (with no transition shown) places it grooming itself on a windowsill across the room. This is invalid even if each shot is individually plausible.

4. **When a break is found, fix it before generating** — one of:
   - Insert an additional connecting shot that shows the transition (the cat jumping down, walking, settling).
   - Rewrite shot N+1's description so it explicitly states the causal action that explains the new state.
   - If neither fits the story, flag the specific conflict to the user rather than silently picking one.

5. **This applies independently to every tracked entity in the same shot**, not just the one the shot's headline description is "about." A shot framed as a close-up on the character's face still has to account for where the cat and the props are, even if they're only at the edge of frame or just offscreen.

6. **A held/handled prop cannot teleport** between hands, surfaces, or off-frame without a shown or stated action — the same rule as for subjects, applied to objects currently in use (a mug being carried, a laptop being opened, a sketchbook being picked up).

## Output format

Output the ledger alongside the finalized shot list so drift is visible at a glance:

```
| Shot | Cat (end state)                          | Character (end state)              |
|------|-------------------------------------------|-------------------------------------|
| 1    | sitting on sketchbook on desk              | entering room, holding matcha       |
| 2    | sitting on sketchbook on desk (unchanged)  | setting matcha down next to laptop  |
| 3    | sitting on sketchbook, being reached for   | reaching a hand toward the cat      |
| 4    | pressing paws down, refusing to move       | small amused smile                  |
| 5    | sitting on desk (unchanged - not shown leaving) | sitting at chair, opening laptop |
| 6    | sitting on desk (unchanged)                | reading the screen, OTS framing     |
```

If a row shows a state with no shot explaining how it got there, that is the bug to fix, not a stylistic note.

## Relationship to other rules

This is a text-level planning check and does not replace the image-generation-time rules in `loveart-video-animation` (master-shot chaining, conditional pose continuity, "recurring subjects follow the script not the master image"). Those rules keep a single generated image accurate to its own shot description; this skill keeps the sequence of shot descriptions accurate to each other before any image exists.
