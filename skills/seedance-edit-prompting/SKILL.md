---
name: seedance-edit-prompting
description: Write and verify prompts for Seedance 2.5 video edit on Higgsfield (and Genjutsu / Ad Multiplier) when replacing characters, wardrobe, or backgrounds in existing footage while keeping the original motion, expressions, voice, cuts, and timing. A prompt built on another video is assembled from TIMECODE BLOCKS (one per cut, detected automatically or entered manually), each with an exact-motion line, a voice line (original voice by default; new words only when the user gives the exact text) and a LOOK LOCK taken from the references or the base details. Use before writing any Seedance, Higgsfield Edit, or video-to-video prompt, before claiming a result matches its source, and when a generation drifts from the reference video.
---

# Seedance 2.5 edit prompting

## This project first (binding)

This skill arrives at every project knowing nothing about it. Before applying any default written below:

1. **Study this project.** Read its brief or script, every file in its references folder (images, video frames, saved prompts and their notes) and the results already approved in it. Say what you see in concrete terms before generating or writing anything.
2. **Learn from this project's results.** After each approved result, add to this project's `LESSONS.md` what was asked, the prompt or setting that produced it and why it worked; after each rejection, what failed and the fix. Read `LESSONS.md` before the next task. For this project it overrides the defaults below.
3. **Stay inside this project.** Never open, copy or imitate material from another project, brand or earlier job: no images, fonts, prompts, names or folders from elsewhere. What is missing comes from this project's own sources or from the user.
4. **Examples here are samples.** Every name, date, place or line used as an example in this skill is invented sample data. Do not carry it into the work.
5. **Improve the skill, not a memory of one project.** When a lesson would help any project, propose it to the user as a general rule with no project names in it.

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
   - A location image also overrides the layout of wide shots: its centered path replaced the source floor markings, so Character A ended up standing on the path and Character B beside it. Map it as look only ("never its layout, track position or camera angle") and anchor the geometry to the source ("the path goes exactly where the two floor markings are in @video1").
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
- Turning a visible source object into something else: describe the target state and where it sits, not the source object. "The green cardboard box becomes the wooden crate" left the cardboard in three runs; "her hands rest on top of a wooden crate that stands exactly where the box stands on the table" plus "no green objects in any shot" produced the crate. Do not repeat the source object's material or color in the prompt.
- Prop swaps: one line with a time range, describing only the target, plus a color negative for the source prop. Verified wording: "From 3 s to 8.9 s, what the person from @image1 holds in their hands is an umbrella: a long black shaft with a curved wooden handle, in exactly the same place in their hands as in @video1" with "no yellow objects in any shot" gave a real umbrella and kept motion (correlation 0.72, all cuts in place).
  - Working rule, confirmed once for a vehicle (next point): for any object that must change (in a hand or anywhere in the frame), attach a reference photo or picture of the target object alone and map it as its own `@imageN`. Follow it by default and offer to prepare the object image. Evidence so far: the umbrella swap above worked text-only once the wording described only the target, so the image is an extra lever, not a proven requirement. Suggested mapping line (untested): "@image5: the umbrella. Take only its shape, size and materials; object only, no hands or background."
  - Confirmed once: a reference photo of a pickup truck mapped as "@image4: the vehicle. Take only the shape, size, color and details of this red pickup truck; vehicle only, no background" turned a white sedan into the pickup truck in every shot of two clips (no text-only comparison run).
  - Failed: naming the source prop ("the yellow tennis racket becomes an umbrella") kept the racket, even in a short, non-repeated line.
- The same holds for negatives: "no office chair" left the chair under the seated woman; "she sits on the wooden park bench with the slats visible beside her" plus "nothing under her except the wooden park bench" removed it.
- Flipping the screen direction of a vehicle: one short line about the vehicle only ("in the wide shots the front of the pickup truck, with the grille and headlights, is on the left side of the frame and its rear is on the right side"). People's positions already come from @video1, so the rider on the left ends up with their back to the direction of travel and the figure on the right ends up at the rear. A longer version that also said who faces which way and named an action between the two riders made the motion drift; the short line kept it (correlation 0.55, all cuts in place).
  - Failed: an umbrella mentioned six times with "opens it, in every frame, from the first frame" dropped motion correlation from 0.81 to -0.08 and put the open umbrella into nearly every shot. No action verbs for the prop, no repeats in the shot order or constraints.
- Quantities: give numbers and size per shot type. "Many books on the shelf" was ignored; "at least twelve thick hardback books standing upright", written separately for low-angle shots, close-ups and wide shots, came out as a full shelf.
- When a result is close and the user lists what was missed, strengthen exactly those points in the same prompt and keep the rest; do not switch to another workflow (second pass, splitting, recoloring the source) unless the user asks.

## Per-shot character lock

Same actors often play several characters in the source, and the model mixes up who is who, what they wear and where they look. In every prompt:

- Tags: the user names them `@vid-N` and `@img-N` (not `@video1` / `@image1`). Ask which number the video gets; keep the user's upload order.
- Before writing, confirm the cast: list each tag with a one-line visual description of that image ("@img-5 = Character A in the long green raincoat") and have the user confirm. Images pasted into chat have no names; guessing which image is which character swaps the characters' outfits.
- Every time a character's name appears anywhere in the prompt (mapping, identity link, shot order, dialogue), write the reference next to it: "Character A (@img-5)".
- Every shot line restates the outfit of each character in that shot in short form ("Character B (@img-4) in the yellow rain jacket and white shirt"), not only the mapping line.
- Every shot line states the eye line: into the lens only in a point-of-view shot from another character's eyes; otherwise say where he looks (below the lens, off to the side at X, up, away from the camera) and add "never into the lens". Check the source frames for the real eye direction and follow the user's corrections.
- When the user wants a different framing than the source (for example "wider, medium shot"), write it in that shot line ("medium shot, waist up, wider than in @vid-N") instead of "exactly as in".
- Props that carry over between parts (a stool, a suitcase) are described with the same words in every part, with their state ("the white wooden stool Character B sat on, now knocked over on its side").
- One actor shot every role separately (each shot has one person) but they share one place (a group in one room): add a "GROUP IN FRAME" line to every block — the named person stays the sharp main subject exactly as in @vid-1; the others appear at the sides of the frame, a step behind, partly cut and slightly out of focus, reacting quietly, never covering the main subject; in close shots only a shoulder or a hand at the very edge. Keep the fixed left/center/right order from an approved layout keyframe, and replace "one person per shot" in the constraints with "the named person is the main subject; the others only at the sides; each appears once".
- Dialogue from an SRT: subtract the timeline offset (01:00:00), check onsets against audio pauses (`silencedetect`), assign each line to the speaker by the shot it falls in.

## Light match: characters lit exactly like the location

Character references are usually studio sheets (flat even light, grey background). Seedance carries that light into the shot, so the people look pasted onto the location. Generic words like "warm light" do not fix it. Every prompt that puts characters into a location plate gets a measured LIGHT MATCH.

1. **Location plates first.** All zone plates of one scene must show the same room in the same state (same backdrop, same lights); a plate that still shows an old version of the room (e.g. an old backdrop behind the table) gives the model two conflicting setups. Fix plates before writing prompts. Prefer realistic, lived-in plates over glossy cinematic ones; glossy over-lit plates read as unreal.
   Pick ONE canonical version of each recurring set piece (for example a counter) and rebuild every other plate from it: generate the master with "the counter must be EXACTLY the counter in image N, identical in every detail, just seen from this angle", then edit each zone plate keeping its camera angle and swapping only that set piece. Check with a side-by-side sheet of all plates (and the keyframe) before writing prompts; without this check the plates of one room can show three different versions of the set piece (position, shape, light count).
2. **Inventory the plate's light** by looking at it and measuring it (crop average per region):
   ```bash
   avg(){ ffmpeg -v error -i "$1" -vf "crop=$2,scale=1:1,format=rgb24" -f rawvideo - | od -An -tu1; }   # crop=w:h:x:y
   ```
   Measure the brightest lit surface (e.g. the pool of light on the floor), the backdrop centre and edge, the room floor, a practical (sconce), and, in an approved keyframe, the faces. Write down: every visible source (where, pointing which way, hard or soft, colour), what is key / fill / bounce / practicals, the brightness relations (faces vs brightest surface vs backdrop vs room) and the colour cast on whites and blacks.
3. **Mapping:** each character reference line says "face, hair and clothes exactly as in this reference — never its light, background or colour"; the location plate line says "take its light and photographic style".
4. **LIGHT MATCH — CRITICAL block** (after the look lock): "Relight every person with the exact light of @img-N; take nothing of the light from the character references." Then the sources as a numbered list, "only these, nothing else", the exposure relations from the measurements in plain words, the colour cast (whites read warm cream, blacks stay warm-dark), contact shadows on the floor and on the wall behind, and "grain, noise and sharpness on the people identical to the background".
5. **Per shot:** one short light line naming where the key hits that person in that shot ("the overhead par light on his hair and shoulders, eye sockets in soft shadow").
6. **Keyframe:** generate and approve a still of the characters inside the plate first (characters full-body references, not head portraits — a head-portrait reference makes the model paste the person oversized in front of the set); attach it as "@img-N = how the light falls on the people and how big they are; never its framing".
7. **Negatives:** no flat or studio lighting, no grey studio background, no rim or back light the plate does not have, no cool fill, no light from the camera side, no glow.
8. **Verify:** crop a face and the nearby background in the result and compare their RGB relation with the plate/keyframe numbers; report it.

## Persona face and costume: never rely on the tag alone

Typical failure: a mapping line says only "face, hair and build AND outfit exactly as in this reference (@ref-A)". Seedance keeps the source actor's own hair, facial hair, shirt and shoes, so the character looks nothing like the reference and does not match the costume. When the source actor resembles the character, the model treats the existing face as "close enough".

- Write the persona look out in full in the mapping line: hair, facial hair, scars or marks, every garment, shoes, gloves. Name the source actor's differing features as negatives ("never a moustache, cropped hair, green polo shirt, brown boots").
- Attach one full-body costume image as its own `@img-N` next to the tag. Find one in the project (`references/<persona>`, stills, posters) and crop it if needed.
- Generate an approved keyframe of the persona inside the scene plate, in the source pose, and map it first ("how he looks, how big he is, how the light falls on him; never its pose").
- Start the mapping with "The man in @vid-1 is replaced completely by <name>".

## Change requests: parse per character, read back before generating

Users write fast, often without commas. A request like "make the hat a bigger umbrella a striped one" meant "make the hat bigger (Character A keeps it), change the umbrella to a striped one (Character B)". If it is read as "replace A's hat with a big striped umbrella", every image generated on that reading is wasted.

1. Split the sentence into change units at every noun + "to": `X → Y`. If a unit can attach to the previous or the next word, list every possible reading.
2. Map each unit to the cast table: who holds or wears the object now (from the confirmed cast and props). A change that moves an object to a different character, removes a character's signature prop or gives two people the same prop is suspicious. Prefer the reading where every character keeps one distinct object.
3. Before any generation or prompt rewrite, write one read-back line per character: "A: hat → bigger hat · B: plain umbrella → striped · C: no change". If two readings remain, ask one question with both options. Do not generate on a guess.
4. After the user confirms, put the final mapping into the mapping lines and into GLOBAL CONSTRAINTS as negatives ("B's umbrella is striped only, no plain umbrella").

## Higgsfield tool choice

- Seedance 2.5 Edit: prompt-described or Draw to Edit (mark the region on a frame). Draft mode (480p) for cheap tests, finalize later. `bitrate_mode: high` for dark or foggy scenes.
- Genjutsu Motion Transfer: keeps motion, camera, timing; rebuilds the scene from references. Object Swap: replaces a selected character, outfit, product, location, or object.
- Ad Multiplier: 4-30 s source, edit or recreate, person reference image is authoritative for the whole look.
- Tag syntax in the Higgsfield UI is mention chips; write `@video1`, `@image1` and attach in the stated order.

## When footage is complex

- Many cuts, new scene types, or short key events: cut the source by scene type or by event, regenerate each piece, and splice back with ffmpeg at the original cut times.
- Short events (spit, shot) get their own clip of 4+ s with one added-effect line each and the surrounding performance marked "exactly as in @video1".
- Joining two generated pieces: if a seam shows, describe how video 1 exits and from which viewpoint video 2 begins; "connect naturally" is too vague.
- Higgsfield moderation checks the uploaded video, not only the prompt: a source shot can be flagged NSFW even when the prompt is harmless. Fix it in the source first: restyle those shots (for example as an outline effect) or cut the flagged element out, then upload again.
- Shots with a stylized effect (bright outlines on black) still work as motion guides: "take only the shapes, poses and movement from them and render them as normal photographic close-ups like the close-ups at X-Y s", plus "no outline, negative or neon effect" in the constraints.
- A black area where a person was cut out stays dark and blurred unless the prompt says what it is: "the left part of the frame is black and empty because a person was cut out; fill that whole area with the man from @image1, seen from behind..." plus "no empty or black areas in any frame".

## Bridge between two clips (omni_reference)

The user cuts a few seconds from the end of one approved clip and the start of the next, and the model generates the missing middle. Confirmed once in practice.

- Inputs: `@video1` = the opening clip, `@video2` = the ending clip, then the usual character and prop images. Mode `omni_reference`, 16:9, duration = opening + middle + ending (allow about 1.5 s per beat in the middle).
- TIMELINE with exact seconds: "0-3.7 s: @video1 exactly as it is"; the middle; "12.9-16 s: @video2 exactly as it is, including its cut at 15.5 s".
- The middle: the user's beats as a numbered list, in order, each one sentence; "choose any camera angles and cuts"; the last beat ends "in the same positions as in the first frame of @video2".
- A CONTINUITY block instead of camera instructions: the vehicle moves fast the whole time; it drives in the same screen direction in every outside shot as in both clips; the camera stays on the same side of the vehicle so screen direction never flips; the background rushes past in the same direction; same light, outfits and positions.
- Measured: the opening was repeated almost frame for frame (per-frame image correlation 0.91); the ending only approximately (0.43, its cut landed 0.5 s early). If the ending must match exactly, lay the original clip over it in editing.
- A character's state goes into that character's mapping line, in plain visual words: "she has just come in from heavy rain, so in every shot she looks soaked: wet hair stuck to her forehead, the coat dark with water, the collar turned up, drops on her face" worked.

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
