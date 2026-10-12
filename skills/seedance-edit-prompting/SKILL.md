---
name: seedance-edit-prompting
description: Write and verify prompts for Seedance 2.5 video edit on Higgsfield (and Genjutsu / Ad Multiplier) when replacing characters, wardrobe, or backgrounds in existing footage while keeping the original motion, expressions, cuts, and timing. Use before writing any Seedance, Higgsfield Edit, or video-to-video prompt, before claiming a result matches its source, and when a generation drifts from the reference video.
---

# Seedance 2.5 edit prompting

Editing is a locked task: the source video fixes the timeline, aspect ratio, and (approximately) duration. The model re-renders frames, so anything not protected explicitly can drift. Everything below exists to keep the source performance intact.

## Hard limits

- Edit input: keep under 20 s when possible, 30 s maximum (Genjutsu: 4-30 s). Duration stays close to the source.
- References: up to 30 images; one to eight subjects per image set is most reliable; one clear subject per image, full outfit visible when clothing must transfer.
- Timestamps: whole seconds, continuous ranges without gaps; one decimal only for a real boundary. Treat them as time budgets, not frame-exact cut points.
- Output is regenerated, so quality drops slightly with each chained pass.
- Muzzle flashes, smoke, saliva, bullet impacts, and other short effects are drawn unreliably in edit mode, and adding an "Added effect" line to a recast prompt made the whole motion drift in repeated runs while the same prompt without effect lines matched the source. Never put effects in the recast prompt; recast first, composite effects in post (ffmpeg) or run a separate add-only edit on the approved result.
- Same prompt and inputs give different results on every run; no seed control is exposed on `seedance_2_5`. Keep an approved take before retrying.

## Prompt formula (worked on multi-shot footage)

1. ASSET MAPPING: one line per input. Each answers: whose is it, what exactly is taken from it, what must NOT be inherited.
   - `@video1`: the locked source. Use ONLY for action order, body movement, facial expressions, eye direction, cuts, camera, framing, timing. Never inherit clothing, faces, rooms, backgrounds.
   - `@imageN`: one character each (face, hair, makeup, full wardrobe, named garments), one location (setting only, no people), one continuity frame (look and grade only, not framing).
2. IDENTITY LINK: if two different-looking sources are the same character (for example a mannequin and the actor who plays it in cutaways), say they are one person with the same face, outfit, and props in every shot.
3. BRIEF: one sentence. State that actions are preserved exactly and not re-described.
4. SHOT ORDER: continuous time ranges, each shot named by framing and who is in it. Do not narrate actions the source already contains.
5. GLOBAL CONSTRAINTS: backgrounds per shot type, outfit consistency, no new actions or camera moves, no text, logos, watermarks.

Rules:
- Use "preserve the original action order and timing exactly" instead of describing the action again. Re-described actions cause drift.
- One target per change line; never merge two different targets into one sentence.
- Name the target by what is visible (clothing, position, object), not by a label the model has to guess.
- Never add scene details the user did not ask for (lights, props, effects). Ask or omit.
- Negative constraints go in one final list, not repeated through the prompt.
- Start multi-video prompts with "Edit @video1". Say add, remove, replace, or modify explicitly.
- Fence a change in time with "Edit seconds X-Y" when only part of a clip changes.
- Number of simultaneous changes: few. Many connected changes across the whole frame push the edit toward full regeneration and the motion is lost.

## Higgsfield tool choice

- Seedance 2.5 Edit: prompt-described or Draw to Edit (mark the region on a frame). Draft mode (480p) for cheap tests, finalize later. `bitrate_mode: high` for dark or foggy scenes.
- Genjutsu Motion Transfer: keeps motion, camera, timing; rebuilds the scene from references. Object Swap: replaces a selected character, outfit, product, location, or object.
- Ad Multiplier: 4-30 s source, edit or recreate, person reference image is authoritative for the whole look.
- Tag syntax in the Higgsfield UI is mention chips; write `@video1`, `@image1` and attach in the stated order.

## When footage is complex

- Many cuts, new scene types, or short key events: cut the source by scene type or by event, regenerate each piece, and splice back with ffmpeg at the original cut times.
- Short events (spit, shot) get their own clip of 4+ s with one added-effect line each and the surrounding performance marked "exactly as in @video1".
- Joining two generated pieces: if a seam shows, describe how video 1 exits and from which viewpoint video 2 begins; "connect naturally" is too vague.

## Two prompt modes

- Exact-copy recast (default): the prompt carries asset mapping, identity link, shot order, and "exactly as in @video1" per shot. It matched the source on ordinary scenes (motion correlation about 0.63 on a 30 s multi-shot clip).
- Beat-described scene: for shots the model cannot copy faithfully (rotated or point-of-view shots, falls, blows), keep the cuts, camera angles, tilt, and timing from @video1 but describe the action beats in a few sentences and accept variation. This worked where the exact-copy prompt kept drifting.

## Before describing the source

- Identify the exact source file the user uploaded and its time base (probe duration, locate it in the original, list its cuts). A shot-order timeline written for a different clip length makes the whole generation drift.
- Ask what unusual shots mean (rotated frame, handheld, point of view of a character) before describing them; guessing produced a wrong description of a point-of-view shot.
- When the user says not to describe a person's actions, write "exactly as in @video1" for that person and nothing else.
- Genjutsu Motion Transfer ignored the reference wardrobe on repeated runs; Seedance Edit with asset mapping followed it.

## Verify with numbers, not by eye

Never state that a result matches the source from a few sampled frames. Measure:

```python
import subprocess, numpy as np
W,H,FPS=64,36,10
def energy(args):
    raw=subprocess.run(["ffmpeg","-v","error"]+args+["-vf",f"fps={FPS},scale={W}:{H},format=gray","-f","rawvideo","-"],capture_output=True).stdout
    n=len(raw)//(W*H); fr=np.frombuffer(raw[:n*W*H],np.uint8).reshape(n,H,W).astype(float)
    return np.abs(np.diff(fr,axis=0)).mean(axis=(1,2))
# energy(["-ss",START,"-t",LEN,"-i",ORIGINAL]) vs energy(["-i",RESULT]); clip at the 90th percentile,
# correlate over lags -3..+3 s. Lag 0 correlation near 0.6+ and best lag near 0 = motion matches.
```

Also compare cut times (scene-change detection), and view paired frames from original and result at the same timestamps (ffmpeg `xstack`). Report the numbers and label each claim verified or unverified.

## Process before sending a prompt

1. Look at the source (contact sheet, cut list, per-shot content) before describing it.
2. Convert user timestamps to the trimmed clip's time base and say which base is used.
3. Re-read the prompt for: invented details, re-described actions, merged targets, missing identity link, tag order matching the upload order.
4. If the user says it does not match, measure first, then change one variable.
