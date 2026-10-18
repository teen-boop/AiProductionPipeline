---
name: seedance-edit-prompting
description: Write and verify prompts for Seedance 2.5 video edit on Higgsfield (and Genjutsu / Ad Multiplier) when replacing characters, wardrobe, or backgrounds in existing footage while keeping the original motion, expressions, voice, cuts, and timing. A prompt built on another video is assembled from TIMECODE BLOCKS (one per cut, detected automatically or entered manually), each with an exact-motion line, a voice line (original voice by default; new words only when the user gives the exact text) and a LOOK LOCK taken from the references or the base details. Use before writing any Seedance, Higgsfield Edit, or video-to-video prompt, before claiming a result matches its source, and when a generation drifts from the reference video.
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

## Timecoded prompt from a source video (default whenever the prompt is based on another video)

The final prompt repeats the source exactly: motion, expressions, eye direction, camera, cuts, timing and voice. It is assembled from
one block per shot, so every block carries its own motion, voice and look lines.

1. **Timecode blocks:** run `video-cut-timecodes`. It creates a new block at every cut and shows a sheet of the frames in each block.
   - If a block is wrong, ask the user (one question, two options): re-detect **automatically**, or enter the cut times **manually**
     (seconds, or SS.FF from the editing timeline).
   - Do not continue until `cut_timecodes.py check` says OK and the user has confirmed the blocks.
2. **References per block:** run `segment-reference-lock`.
   - First confirm the cast list: each `@img-N` with its one-line look.
   - Then ask: assign the references to the blocks **automatically** (from the block frames) or **manually** (the user picks per block).
3. **Voice:**
   - The default is the original voice, words, intonation and timing of the source range, with lips in sync.
   - If any text has to be added or changed, **ask the user for the exact words, the speaker and the block**. Never write dialogue
     yourself, and never "improve" the original lines. Check that the words fit the block's length (about 2.5 words per second).
4. **Look lock:** every block gets a LOOK LOCK line, filled in automatically.
   - Copy the confirmed reference description verbatim.
   - Where a block has no image reference, use the base details: the continuity sheet's location, wardrobe, props and light.
   - Where neither exists, write "exactly as in @vid-1 in this range". Never invent.
5. **Assemble the prompt:**
   ```
   Edit @vid-1.
   ASSET MAPPING: … (one line per tag; @vid-1 = motion, timing, cuts, camera and voice ONLY)
   IDENTITY LINK: … (if needed)
   BRIEF: preserve the original action order, timing, motion and voice exactly; change only the looks listed below.
   [0.0-3.9 s] BLOCK 1 — … MOTION … EYES … VOICE … LOOK LOCK …
   [3.9-7.4 s] BLOCK 2 — …
   …
   GLOBAL CONSTRAINTS: no new actions, camera moves, cuts or words; no text, logos, watermarks; <colour negatives for replaced props>.
   ```
   The block text comes from `segment_blocks.py` and is pasted unchanged. Add a change line inside a block only for what the user asked
   to change in that block.
6. **After generation:**
   - Measure motion (the energy correlation below) and cut times against the block list.
   - Check the voice by ear at the block boundaries.
   - Report each claim as verified or unverified.

## Prompt formula (worked on multi-shot footage)

1. ASSET MAPPING: one line per input. Each answers: whose is it, what exactly is taken from it, what must NOT be inherited.
   - `@video1`: the locked source. Use ONLY for action order, body movement, facial expressions, eye direction, cuts, camera, framing, timing. Never inherit clothing, faces, rooms, backgrounds.
   - `@imageN`: one character each (face, hair, makeup, full wardrobe, named garments), one location (setting only, no people), one continuity frame (look and grade only, not framing), one image per object that must change in the footage (the target object only).
   - A location image also overrides the layout of wide shots: its centered track replaced the source planks, so the tied man ended up lying along the rails and the other man beside them. Map it as look only ("never its layout, track position or camera angle") and anchor the geometry to the source ("the rails go exactly where the two wooden planks are in @video1").
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
- Number of simultaneous changes: the count alone did not break motion (12 separate change lines held correlation 0.63 on a 30 s clip). Repeated emphasis and added effects did; see the next two rules.
- Turning a visible source object into something else: describe the target state and where it sits, not the source object. "The blue foam tube becomes the steel rail" left the foam in three runs; "the back of his head and his neck rest on top of a steel rail that runs along the line of the long tube under his neck" plus "no blue objects in any shot" produced the rail. Do not repeat the source object's material or color in the prompt.
- Prop swaps: one line with a time range, describing only the target, plus a color negative for the source prop. Verified wording: "From 3 s to 8.9 s, what the man from @image1 holds in his hands is an axe: a long wooden handle with a heavy grey steel head, in exactly the same place in his hands as in @video1" with "no red objects in any shot" gave a real axe and kept motion (correlation 0.72, all cuts in place).
  - The user's working rule, confirmed once for a vehicle (next point): for any object that must change (in a hand or anywhere in the frame), attach a reference photo or picture of the target object alone and map it as its own `@imageN`. Follow it by default and offer to prepare the object image. Evidence so far: the axe swap above worked text-only once the wording described only the target, so the image is an extra lever, not a proven requirement. Suggested mapping line (untested): "@image5: the axe. Take only its shape, size and materials; object only, no hands or background."
  - Confirmed once: a reference photo of a Humvee mapped as "@image4: the vehicle. Take only the shape, size, color and details of this military Humvee; vehicle only, no background" turned a white BMW into the Humvee in every shot of two clips (no text-only comparison run).
  - Failed: naming the source prop ("the red-and-black bar clamp becomes an axe") kept the clamp, even in a short, non-repeated line.
- The same holds for negatives: "no treadmill" left the treadmill under the walking man; "his feet step on the asphalt and the road moves under him as he walks" plus "nothing under his feet except the asphalt of the road" removed it.
- Flipping the screen direction of a vehicle: one short line about the vehicle only ("in the wide shots the front of the Humvee, with the grille and headlights, is on the left side of the frame and its rear is on the right side"). People's positions already come from @video1, so the rider on the left ends up with his back to the direction of travel and the figure leaving on the right falls off the rear. A longer version that also said who faces which way and that one man "throws" the other made the motion drift; the short line kept it (correlation 0.55, all cuts in place).
  - Failed: an axe mentioned six times with "raises it, in every frame, from the first frame" dropped motion correlation from 0.81 to -0.08 and put the raised axe into nearly every shot. No action verbs for the prop, no repeats in the shot order or constraints.
- Quantities: give numbers and size per shot type. "Many turns of rope" was ignored; "at least eight tight turns as thick as a thumb", written separately for low-angle shots, close-ups and wide shots, came out as thick coils.
- When a result is close and the user lists what was missed, strengthen exactly those points in the same prompt and keep the rest; do not switch to another workflow (second pass, splitting, recoloring the source) unless the user asks.

## Per-shot character lock (user's standing rule)

Same actors often play several characters in the source, and the model mixes up who is who, what they wear and where they look. In every prompt:

- Tags: the user names them `@vid-N` and `@img-N` (not `@video1` / `@image1`). Ask which number the video gets; keep the user's upload order.
- Before writing, confirm the cast: list each tag with a one-line visual description of that image ("@img-5 = man in the black leather biker jacket") and have the user confirm. Images pasted into chat have no names; guessing which image is which character swapped Koss and Archi's outfits in both parts.
- Every time a character's name appears anywhere in the prompt (mapping, identity link, shot order, dialogue), write the reference next to it: "Archi (@img-5)".
- Every shot line restates the outfit of each character in that shot in short form ("Biggy (@img-4) in the grey tweed blazer and striped henley"), not only the mapping line.
- Every shot line states the eye line: into the lens only in a point-of-view shot from another character's eyes; otherwise say where he looks (below the lens, off to the side at X, up, away from the camera) and add "never into the lens". Check the source frames for the real eye direction and follow the user's corrections.
- When the user wants a different framing than the source (for example "wider, medium shot"), write it in that shot line ("medium shot, waist up, wider than in @vid-N") instead of "exactly as in".
- Props that carry over between parts (a chair, a sack) are described with the same words in every part, with their state ("the black metal folding chair Koss sat on, now knocked over on its side").
- Dialogue from an SRT: subtract the timeline offset (01:00:00), check onsets against audio pauses (`silencedetect`), assign each line to the speaker by the shot it falls in.

## Higgsfield tool choice

- Seedance 2.5 Edit: prompt-described or Draw to Edit (mark the region on a frame). Draft mode (480p) for cheap tests, finalize later. `bitrate_mode: high` for dark or foggy scenes.
- Genjutsu Motion Transfer: keeps motion, camera, timing; rebuilds the scene from references. Object Swap: replaces a selected character, outfit, product, location, or object.
- Ad Multiplier: 4-30 s source, edit or recreate, person reference image is authoritative for the whole look.
- Tag syntax in the Higgsfield UI is mention chips; write `@video1`, `@image1` and attach in the stated order.

## When footage is complex

- Many cuts, new scene types, or short key events: cut the source by scene type or by event, regenerate each piece, and splice back with ffmpeg at the original cut times.
- Short events (spit, shot) get their own clip of 4+ s with one added-effect line each and the surrounding performance marked "exactly as in @video1".
- Joining two generated pieces: if a seam shows, describe how video 1 exits and from which viewpoint video 2 begins; "connect naturally" is too vague.
- Higgsfield moderation checks the uploaded video, not only the prompt: an adult stand-in of short stature next to a gagged, tied man was flagged NSFW (likely read as a child). The user fixed it in the source by turning those shots into an outline effect and cutting the stand-in out.
- Shots with a stylized effect (bright outlines on black) still work as motion guides: "take only the shapes, poses and movement from them and render them as normal photographic close-ups like the close-ups at X-Y s", plus "no outline, negative or neon effect" in the constraints.
- A black area where a person was cut out stays dark and blurred unless the prompt says what it is: "the left part of the frame is black and empty because a person was cut out; fill that whole area with the man from @image1, seen from behind..." plus "no empty or black areas in any frame".

## Bridge between two clips (omni_reference)

The user cuts a few seconds from the end of one approved clip and the start of the next, and the model generates the missing middle. Worked on the first try; the user called the result excellent.

- Inputs: `@video1` = the opening clip, `@video2` = the ending clip, then the usual character and prop images. Mode `omni_reference`, 16:9, duration = opening + middle + ending (the middle had 9.2 s for six beats).
- TIMELINE with exact seconds: "0-3.7 s: @video1 exactly as it is"; the middle; "12.9-16 s: @video2 exactly as it is, including its cut at 15.5 s".
- The middle: the user's beats as a numbered list, in order, each one sentence; "choose any camera angles and cuts"; the last beat ends "in the same positions as in the first frame of @video2".
- A CONTINUITY block instead of camera instructions: the vehicle moves fast the whole time; it drives in the same screen direction in every outside shot as in both clips; the camera stays on the same side of the vehicle so screen direction never flips; the background rushes past in the same direction; same light, outfits and positions.
- Measured: the opening was repeated almost frame for frame (per-frame image correlation 0.91); the ending only approximately (0.43, its cut landed 0.5 s early). If the ending must match exactly, lay the original clip over it in editing.
- A character's state goes into his mapping line, without blood: "he has just been hit by a car, so in every shot he looks battered: wild messy hair, the suit torn, dusty and dirty, the tie loose and twisted, scratches and bruises on his face" worked.

## Two prompt modes

- Exact-copy recast (default): the prompt carries asset mapping, identity link, shot order, and "exactly as in @video1" per shot. It matched the source on ordinary scenes (motion correlation about 0.63 on a 30 s multi-shot clip).
- Beat-described scene: for shots the model cannot copy faithfully (rotated or point-of-view shots, falls, blows), keep the cuts, camera angles, tilt, and timing from @video1 but describe the action beats in a few sentences and accept variation. This worked where the exact-copy prompt kept drifting.

## Before describing the source

- Identify the exact source file the user uploaded and its time base (probe duration, locate it in the original, list its cuts). A shot-order timeline written for a different clip length makes the whole generation drift.
- The user writes timestamps as seconds.frames at 24 fps from the editing timeline: "03.21" is 3 s + 21 frames = 3.875 s, "13.06" is 13.25 s. Convert before use; on two clips every converted value matched a detected cut.
- Whatever happens in a segment that does not exist in the source (a bridge between two clips, an added middle, a new beat) is the user's decision. Ask what happens there before writing it; never invent the action.
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

0. Timecode blocks confirmed (`video-cut-timecodes`), references and look lock per block confirmed (`segment-reference-lock`), every new spoken word given by the user.

1. Look at the source (contact sheet, cut list, per-shot content) before describing it.
2. Convert user timestamps to the trimmed clip's time base and say which base is used.
3. Re-read the prompt for: invented details, re-described actions, merged targets, missing identity link, tag order matching the upload order.
4. If the user says it does not match, measure first, then change one variable.
