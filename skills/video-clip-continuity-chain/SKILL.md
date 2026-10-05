---
name: video-clip-continuity-chain
description: Prevents prop/subject/object state mismatches at the boundary between separately-generated video clips (e.g. Seedance) that are meant to play back to back as one continuous scene. Forces every clip's prompt to explicitly restate the exact inherited state of every tracked entity from the end of the previous clip, instead of leaving it implied. Use whenever writing a video-generation prompt that continues from an already-written or already-generated clip, splitting a scene into multiple video prompts, or after a generated clip comes back with an object missing, added, or in the wrong state compared to the previous clip. Triggers on video clip continuity, seedance prompt chain, object disappeared between clips, laptop already open, prop missing in second clip, multi-clip scene.
---

# Video Clip Continuity Chain

## Why this exists

This is a costlier variant of the problem `storyboard-continuity-tracker` solves for still-image storyboards. The difference matters: a storyboard's shots are checked as *text*, before any image exists, so a caught mismatch costs nothing. A multi-clip video scene is different — each clip is an independent, **paid** generation call, not a reframe of a shared master. If clip 2's prompt doesn't explicitly account for an object that was clearly present at the end of clip 1 (a matcha bowl just set down, a laptop just shown opening), the video model has no constraint stopping it from omitting it, moving it, or re-doing an action that already happened — and the mismatch is only visible after the expensive generation completes, when the only fix is a costly regeneration.

The concrete failure this fixes: Part A of a scene ends with a matcha bowl placed on a desk and shots that imply the laptop's screen is on. Part B's prompt describes the character sitting down and "opening the laptop" (implying it was closed) and never mentions the matcha bowl at all. The generated clips don't match: the laptop appears already open in one and gets opened again in the other, and the matcha bowl vanishes. Both are real defects, and both were structurally guaranteed by the prompts themselves, not bad luck from the model.

## When this runs

Every time a scene's video coverage is split into more than one clip/prompt meant to be watched consecutively as one continuous scene — before writing clip N+1's prompt, and again as a final check before that clip is sent to generation. This is a text-only check with zero generation cost; skipping it is what makes the expensive kind of mistake possible.

## Process

1. **Re-read clip N's prompt in full** (the immediately preceding clip in the chain) before writing clip N+1. Do not rely on memory of what clip N "was about" — read the actual second-by-second scene description.

2. **Extract the exact state of every tracked entity at the literal last described moment of clip N**: every prop, every recurring subject/object, the character's pose/position, and the state of any device/screen (open/closed, on/off, what's displayed). Nothing with a state is exempt just because it wasn't the "headline subject" of clip N's last beat — a prop sitting quietly in the background still has a state that must carry forward.

3. **Write an explicit STATE HANDOFF block into clip N+1's prompt**, separate from and in addition to the general SETTING description — not folded silently into prose where it can be skipped or contradicted. Format:
   ```
   CONTINUING FROM PREVIOUS CLIP (inherited state, must match exactly at 0:00):
   - Matcha bowl: sitting on the desk where she set it down, untouched, unchanged.
   - Laptop: already open, screen already glowing - do NOT show it being opened again.
   - Cat: sitting on/beside the open sketchbook on the desk, same position as the end of the previous clip.
   - Character: standing beside the desk, having just finished the reaching/cat interaction.
   ```
   Every entry in this block must correspond to something clip N actually established — don't invent inherited state that clip N never showed either.

4. **If clip N+1 needs any of these to change**, that change must be an explicit, shown action within clip N+1's own scene description (e.g. "she picks up the matcha bowl and takes a sip," "she closes the laptop lid") — never a silent substitution where the new clip just starts in a different state with no stated cause. This is the same causal-consequence rule `storyboard-continuity-tracker` applies within a single sequence, applied across the clip boundary instead.

5. **Before sending clip N+1 to generation, diff clip N's ending state against clip N+1's STATE HANDOFF block side by side**, entity by entity. Any entity present at the end of clip N but missing from clip N+1's handoff block is a bug — fix the prompt before generating, not after watching the result.

6. **Apply this at every clip boundary in a chain**, not just the first one — a 3-clip chain has two boundaries to check (1→2 and 2→3), and each is an independent opportunity for the same class of drift.

## Output

Every clip prompt in a chain beyond the first carries its own STATE HANDOFF block at the top of its SCENES section, listing every inherited entity and its exact state. This block is what a human (or a follow-up check) diffs against the previous clip's ending — it is the artifact that makes the continuity check verifiable instead of implicit.

## Relationship to other skills

`storyboard-continuity-tracker` checks continuity across shots *within* a single planned sequence, before any image/video exists, and is cheap to fix. This skill checks continuity across the *generation boundary* between separately-produced video clips, where mistakes are expensive to fix — run both where they apply; they are not substitutes for each other.
