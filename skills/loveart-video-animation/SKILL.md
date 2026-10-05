---
name: loveart-video-animation
description: Skill for creating consistent image sequences for video animation exclusively in Love Art. Use when user works with story scripts, reference images, character face replacement while preserving style lighting and pose, location databases, recurring subjects/objects (pets, secondary characters, props, vehicles, etc.), clothing consistency, multi-shot adaptation from existing wide shot to close-up inside same location, Nano Banana 2 or GPT Image 2.0 generations. Triggers on video animation, loveart, nano banana, face swap reference, build story block, generate image series, location refs bedroom kitchen street, adapt close-up from wide shot.
---

# Love Art Video Animation

## Overview

This skill creates consistent image sequences intended for video animation. It works only with image generation inside Love Art (primarily free Nano Banana 2 at 2K/4K and GPT Image 2.0 for face work). The skill never invents story details. It manages locked references for the main character (face + body), locations with named angles, recurring subjects/objects and clothing so every generated frame stays visually coherent.

**Recurring subject/object** is the general category this skill locks for consistency: any pet, animal, secondary character, prop, or object that appears more than once and must look identical every time (a cat, a car, a specific mug, a sibling character — whatever the story actually has). Don't assume the recurring subject is an animal or a cat — treat it as a variable per project, and identify what it actually is from the script before locking a reference for it.

## Core Principles

- Style, color, lighting, composition and body from the base reference image are sacred. Only facial identity can be replaced.
- Every face that appears (main or secondary) must be forced to match its locked reference.
- Presence of the character or any recurring subject/object is driven strictly by the approved script.
- One prompt = one generation. Batch size is determined by the number of prompts in the current story block (usually up to 8 free images).
- **Critical multi-shot rule**: when several prompts share the same location and a master frame (usually a wide shot) already exists, subsequent prompts (close-ups, different angles, detail shots) must be adapted from that existing image, not written as independent generations.

## Workflow Stages

### Stage 1 — Script

1. User initiates with requests to create a story, video or animation.
2. Work only on text. Format the script cleanly with numbered scenes or beats.
3. Do not expand or invent plot, characters or events unless the user explicitly asks.
4. Present the finished script for approval before any visual work.

### Stage 2 — Reference Locking

After script approval the skill extracts and locks:

- **Main character** (face + body). User already has preferred reference images (animated or realistic style). These become the base.
- **Face replacement rule**: when a prototype face is supplied, apply only facial identity (bone structure, eye shape, nose, mouth, likeness). Everything else (hair, body pose, clothing, background, lighting, art style) stays pixel-consistent with the base image.
- **Locations**: create or use a named database (bedroom, kitchen, store, street_next_to_house, street_next_to_shop, etc.). If a room has multiple camera angles, each angle is a separate locked reference.
  - **Building a location's reference sheet from an existing character shot**: when a location is only known from a photo/render that has a character (or animal) in it, first strip the subject out — attach that image and prompt "Change to: an empty [location] with no person present. This is an edit of the reference image, not a new scene — keep the exact same room, furniture, lighting and art style. Remove the character completely." This produces the location's base clean plate at matching quality/style to the source.
  - **Minimum 3 angles per location.** One clean plate is not enough to cover a full scene's coverage without drift. From the base clean plate, generate at least 2 more angle variations chained the same way as character reframes: "Change to: a wider/closer view..." or "Change to: a view from [a different wall/corner]...", each time attaching the clean base (not a previous variation) so all angles stay anchored to the same room geometry. Name them `<location>_angle1` (the base), `_angle2`, `_angle3`, etc.
  - This location-sheet building is independent of character generation — do it once per location, before or alongside the story-block prompt construction, and reuse across every block set in that location.
- **Recurring subjects/objects**: whatever the script actually has (pet, animal, secondary character, prop, vehicle, etc.) — each gets its own dedicated locked reference for consistency.
- **Clothing and other fixed parameters**: locked when they must stay constant across frames.

### Character-locking discipline (adapted from `character-builder`, style-agnostic parts only)

`character-builder` is built for photoreal humans on a flat gray plate — its default render register (photoreal, 3D-render negations, flat-shadowless-plate) does NOT apply here; this project's locked style is semi-realistic anime illustration and stays that way. What DOES transfer, because it's about prompt discipline rather than render style:

- **Prompt economy.** When a strong identity reference is attached (the canonical prototype, the turnaround sheet), the reference carries the identity load — don't re-describe face structure, skin tone, or eye shape the reference already shows. Spend the prompt's words on what the reference can't say: this shot's pose, expression, wardrobe delta, and composition. A sentence that just re-describes something already visible in the attached reference gets cut unless it's load-bearing for this specific composition.
- **Text-first wardrobe/outfit proposal.** Before generating a new outfit or a wardrobe variant, write it out in plain text (every garment, color, fit) and get it confirmed — same as Stage 1 requires script approval before visual work. Never combine a new-outfit proposal and its first generation in the same step; text iteration is free, generation is not.
- **The hold clause (identity firewall) for point-edits.** Any edit that changes one specific thing about an already-locked character (hair, an accessory, an expression) must explicitly state what's changing AND explicitly state that everything else is held identical to the locked reference — face, proportions, art style, unrelated wardrobe. Without the hold clause, a "change the hair color" edit quietly drifts the face along with it. This is the same mechanism `video-clip-continuity-chain` uses for props across clips, applied here to a single character across a point-edit.
- **Version, don't overwrite, a re-lock.** If a character's canonical look changes materially (new outfit becomes the new default, a hairstyle change), keep the old locked reference and name the new one distinctly (`CANONICAL_prototype_v2...`) rather than deleting history — old scenes/panels may still need to match the old version.

### Stage 2 — Reference Extraction Pass (Mandatory Whenever Source References Exist)

When the user supplies existing reference photos/renders (not blank-slate generation), run this
three-way extraction on each usable source image before doing anything else with it. Each
extraction is its own generation, so one source photo can produce up to 3 new locked assets:

1. **Extract wardrobe** — isolate the clothing/outfit visible in the source image as a clean
   flat-lay or garment-only reference, keeping the exact colors and image tones from the
   source (do not reinterpret the palette), plain neutral background, no person wearing it.
2. **Describe and extract props** — isolate each distinct prop/object visible in the source
   image as its own clean close-up reference, keeping the exact colors and image tones from
   the source, plain neutral background. One source image can yield several separate prop
   extractions if it shows multiple distinct objects.
3. **Remove subject, keep background only** — the existing "strip the subject" technique
   above, producing the location's clean plate.

Not every source image needs all three (a pure location photo with no clothing/props visible
only needs step 3; a tight object photo only needs step 2). Decide per image which
extractions actually apply — don't force an extraction that has nothing to extract.

**Model:** use `generate_image_nano_banana_pro` (free tier) for this pass, one generation at
a time — Lovart allows only one task running at once, never launch a second extraction before
the previous one finishes.

**Batch size:** a full extraction pass across a reference library commonly produces on the
order of 30-50 new images (several source photos × up to 3 extractions each). This is
expected and fine at the free tier, but run it as a background batch with clear per-image
logging, not as a single giant untracked call — see `detail-reference-intake` for how newly
produced extraction results get catalogued into the project's locked-reference index
afterward.

All subsequent generations must attach the relevant locked references.

### Stage 3 — Prompt Construction for a Story Block

1. Split the approved block into sequential visual prompts (typically 8).
2. For every prompt:
   - Specify the exact location name and angle from the location database.
   - Include or exclude the main character and any recurring subjects/objects strictly according to the script (who/what is in frame, who/what has left).
   - If a face appears, force it to the locked facial reference.
3. **Multi-shot adaptation inside one location (very important)**:
   - When the first (or master) image of a location already exists — usually a wide shot with the character, correct face, correct clothing and background — treat it as the visual source of truth for that location.
   - All following prompts that stay in the same location (close-up of face, close-up of hands, medium shot, slight angle change, detail shot) must be written as adaptations of the existing master image, not as independent full-scene generations.
   - The goal is that clothing, background, lighting, color palette and overall look remain extremely close between the wide shot and every close-up / alternative angle.
   - In the prompt explicitly instruct the model to keep the same background, same clothing appearance, same lighting and same style as the provided master/wide-shot reference, changing only framing, camera distance or the specific detail requested by the script.
4. Output structure:
   - Locked References block (Character, Locations with names, Animals, Clothing)
   - Numbered prompts ready for Love Art, with clear notes when a prompt is an adaptation of a previous master frame

### Stage 3.5 — Block-to-Block Continuity (Mandatory)

Story blocks are frequently very different from each other — different location, different lighting/weather, different outfit, different mood. This difference is often correct (the story moves on), but it is never something to assume silently. **Before generating the first shot of any new block, explicitly clarify with the user how this block connects to the end of the previous one:**

- Does the location carry over, change completely, or partially overlap (e.g. character passes back through an earlier location)?
- Does lighting/weather/time-of-day shift, and is there a transition shot for it (or should one be generated)?
- Does the outfit/appearance change here, and if so is there already a locked reference for the new outfit, or does one need to be created first?
- Is there a specific connecting beat the script implies (e.g. "closes the laptop" at the end of one block, "walks to the window" at the start of the next) that should be the literal first shot of the new block, rather than jumping straight to the block's own master shot?
- If the new block reuses a LOCATION from an earlier block (e.g. the character changes clothes in the same bedroom again), reuse that earlier block's master/locked reference for the location — do not generate a fresh, independently-drifted version of a location that already has a locked reference.

Ask this as a direct question if it isn't already obvious from the script; do not silently pick an assumption and generate. Getting the block boundary right is as important as getting the inside of a block right — a wrong assumption here breaks continuity for the whole rest of the sequence, not just one frame.

### Stage 4 — Generation in Love Art

- Primary engine for main scene generation: **Nano Banana 2** (prefer 2K or 4K free tier).
- Face replacement / identity transfer works better in **GPT Image 2.0**. Use it when the task is pure face swap on an existing base image.
- One prompt produces one image. Prepare the full batch so the user can generate up to ~8 images in one free session while keeping all references attached.
- After generation, present results in story order and flag any consistency drift (especially clothing or background mismatch between wide and close shots).

**MANDATORY master-shot chaining (never generate a block's shots independently):**

Independent text-to-image generation of every shot in a block — even with the same style-reference images attached — produces a DIFFERENT room every time (wall positions, furniture scale, window placement all drift). This is a hard failure, not a minor inconsistency, and must be prevented structurally, not just described as a preference:

1. Before generating anything else in a location/block, generate exactly ONE **master shot** — the widest/establishing frame that shows the most of the environment. If the block's prompt list already labels one "establishing shot" or "wide shot", that is the master. If none is explicitly labeled, use the first, most environment-revealing prompt in the block as the master.
2. Generate the master using text-to-image (with any style-reference images) as normal — this is the only independently-generated shot in the block.
3. Every other shot in that same block/location MUST be generated as an **image-edit reframe of the master**, not a new text-to-image call:
   - Pass the master image as the base reference (Image A). Always reframe from the ORIGINAL master, never chain off a previous reframe's output — chaining compounds drift.
   - Phrase the prompt as **"Change to: [subject/action from the original shot prompt]"**, not "create" or "generate" — verbs that imply new-scene generation cause the model to duplicate elements already in the reference (e.g. two of the same recurring subject instead of one) instead of treating the image as ground truth. Follow with an explicit anti-duplication line: "This is an edit of the reference image, not a new scene — the room, character, and any recurring subjects/objects shown are ground truth and each appear only once. Do not duplicate [name the specific subject, e.g. the cat/the dog/the car] or any other element." Then the room/geometry preservation clause: "Keep the exact same room geometry, proportions, lighting and art style. Only change the framing, camera distance, and the specific action/expression described."
   - This applies even when the shot also needs a face-swap: reframe from the master first (identity-agnostic), then run face replacement on the reframed result as a separate step.
4. If a block spans multiple sub-locations (e.g. bedroom → kitchen), treat each sub-location as its own chain with its own master shot.
5. Never reuse one block's master as the reframe base for a different location — that guarantees drift instead of preventing it.
6. **Pose/motion continuity from the previous frame is conditional, not automatic.** When chaining master + previous-frame as dual references, only instruct the model to continue the character's pose/motion if the current shot is a direct continuation of the SAME action. If the current shot's own description is about a different subject (e.g. a close-up on a recurring subject/object with no character hand action mentioned) or a different action, explicitly say so: "If the new shot describes a different subject or action, follow the shot description exactly and do NOT carry over the previous frame's hand gestures, held objects, or in-progress actions into this frame." Otherwise the model will bleed an unrelated gesture (e.g. a pouring motion) from the previous shot into a frame that never asked for it — this is the same failure class as the geometry-drift and duplication problems above, just applied to hands/actions instead of rooms/recurring subjects.
7. **Recurring subjects/objects and secondary characters must follow the script, not the master image.** A reframe edit conditioned on the master tends to visually preserve whatever was in the master frame, even when the current shot's text doesn't mention it — the opposite failure of the room-geometry problem this whole section solves. For every reframe, explicitly state the presence of each locked recurring subject/object relative to the master:
   - If the master contains a recurring subject/object or character absent from the current shot: add "[Name the specific subject, e.g. the cat/the dog/the car] is not present in this frame — do not include it even though it appears in the base image."
   - If the current shot needs a recurring subject/object or character absent from the master: add "Add [subject description] to this frame as described, even though it is not in the base image."
   - This is the same rule as the general Consistency Rules below, applied specifically to the mechanics of image-conditioned reframing.

## Face Replacement Technique (Critical)

When the user supplies a base image (Image A) and a face prototype (Image B), use this exact approach:

Edit Image A only in the face region. Image A is the base and source of truth for everything except facial identity: keep the exact same background, the exact same body pose and position, the exact same hair, the exact same clothing (adjust only if the user explicitly requests a change such as removing a logo), the exact same lighting, and the exact same art style. Do not regenerate, shift, crop, or reinterpret the background or body — treat them as fixed and untouched.

Image B is used strictly as a facial identity reference — take only bone structure, eye shape, nose shape, mouth shape, and general facial likeness from Image B.

Task: Replace only the face inside Image A with a face that has Image B's facial identity, but sculpt and adapt that face to exactly match Image A's existing head angle, head tilt, and gaze direction. Do not import Image B's head angle or pose. Also adapt the new face to express Image A's exact original emotion and expression. Do not transfer Image B's expression under any circumstance.

Think of this as sculpting Image B's facial identity onto Image A's existing head pose and expression, not pasting Image B's face as-is. Everything outside the face must remain pixel-consistent with Image A.

Always adapt this template to the specific images and required emotion/pose of the current frame.

## Multi-Shot Continuity Inside One Location (Critical New Rule)

This is one of the most important consistency mechanisms of the skill.

Typical workflow the user follows:

1. Generate (or already have) a **wide / master shot** of the character in the location (face already replaced, clothing and background correct).
2. Next prompts in the same location need close-ups, different angles or detail shots.

Rules the skill must follow:

- Never write the close-up prompt as a completely independent generation that only mentions the location name.
- Always treat the existing wide/master image as the visual base.
- Instruct the model to keep:
  - the exact same background and environment
  - the exact same clothing appearance and folds
  - the exact same lighting and color temperature
  - the exact same art style
- Change only:
  - framing (wide → medium → close-up)
  - camera angle (slightly)
  - focus (face, hands, object, etc.)
  - expression or small action required by the script

Example adaptation logic:

- Master prompt result: wide shot, girl sitting on sofa in living_room, correct face, cream t-shirt, golden light.
- Next prompt should not say “close-up of a girl sitting on a sofa…”.
- Instead it should say something equivalent to:  
  “Using the provided wide-shot image as the base, create a close-up of the girl’s face. Keep the exact same cream t-shirt, the exact same sofa and background elements visible at the edges, the exact same golden lighting and art style. Only change the framing to a tight close-up of the face while preserving head angle and expression continuity.”

The final set of frames (wide + close-ups) must look like they were filmed in the same physical space with the same costume, so they can be cut together in animation without visual jumps.

## Location Database

Maintain a simple named set of locations. Examples:

- bedroom
- kitchen
- store
- street_next_to_house
- street_next_to_shop
- living_room
- bathroom
- park
- cafe_interior
- cafe_exterior

When a location has multiple angles, store them as:

- bedroom_angle_front
- bedroom_angle_side
- bedroom_angle_window

The skill must always reference locations by these exact names so the correct visual reference is attached.

## Consistency Rules (Non-Negotiable)

- Character identity, face, body proportions and locked clothing remain constant unless the script explicitly changes them.
- Location geometry, lighting and key props stay locked once chosen.
- Every recurring subject/object (pet, animal, secondary character, prop, vehicle — whatever the script has) keeps the same appearance across all its appearances, at any framing/size (wide, medium, close-up, detail).
- If the character or a recurring subject/object leaves the frame according to the script, remove it completely from that prompt and its references.
- If it re-enters later, re-introduce it only at the correct moment using the same locked reference.
- Every generated face (main or secondary) must be forced to its reference.
- Wide shots and close-ups of the same location must share the same background, clothing appearance and lighting so they form a coherent visual sequence.
- Every video-generation prompt (Seedance or any other video model) must explicitly state **NO MUSIC** — no soundtrack, no score, no background music. Ambient/diegetic sound only (footsteps, rain, dialogue, room tone). Add this as its own line, not buried inside a general sound-cues sentence, so it cannot be dropped or overlooked.
- Every generation prompt, script, and scenario is written in **English by default**. The only exception: if a shot specifically calls for a subject's spoken dialogue or on-screen text/voice in another language, write that specific spoken/written line in the language the subject actually speaks or the text is actually in — everything else around it (scene description, camera directions, style notes, shot rationale) still stays in English.

## Output Format for a Story Block

```
=== LOCKED REFERENCES ===
Character: [description + note about face prototype if used]
Locations: bedroom_angle_front, kitchen, street_next_to_house ...
Recurring subjects/objects: [name + description, one per locked subject the script actually has]
Clothing: [fixed items]
Master frames already available: [list any existing wide shots that later prompts must adapt from]

=== GENERATION PROMPTS ===
Prompt 1 (master / wide shot):
[full prompt]
Location: living_room
...

Prompt 2 (adaptation of Prompt 1):
[prompt that explicitly references the previous master image and asks only for new framing]
Location: living_room (same)
Base image: result of Prompt 1
...
```

## Platform Priority inside Love Art

1. Nano Banana 2 (2K/4K) — main scene generation, free batch.
2. GPT Image 2.0 — preferred for precise face replacement on an existing base image and for clean reframing / close-up adaptations.
3. Other available engines only if the user explicitly requests them.

## Storyboard Step — Companion Skills (Mandatory at Raskadrovka Time)

When the current task is building a storyboard/raskadrovka (a shot list broken down by cinematography plan type — wide/medium/close-up/OTS/etc — before or in place of full production generation), three companion skills run alongside this one, in this order, for every scene/block being storyboarded:

1. **`storyboard-shot-selection`** — run first, on the approved beat/scene list, before shot sizes are finalized. For every beat, determines which shot type's defined narrative job (orientation, gesture, action, emotion, object contact, detail accent, dialogue, relationship) the beat actually needs, and writes that reason inline next to the chosen shot type. Checks that no two adjacent shots share the same job/framing without justification — this is what stops a storyboard from stacking two redundant medium shots back to back, or using an establishing shot for a reaction.
2. **`storyboard-continuity-tracker`** — run next, on the same drafted text shot list, before any image is generated. Builds a state ledger for the character and every recurring subject/object/handled prop across the shots and verifies each shot's starting state is either an identical carryover from the previous shot or an explicit, shown consequence of it. Fixes or flags any state-teleportation between shots before generation.
3. **`storyboard-reference-assembly`** — run per panel/shot, immediately before generating it. Reads the project's locked-reference index in full, extracts every noun in the shot (including the location's full canonical environment, not just what the one-line shot description names), resolves each to its exact locked asset, and produces a reference manifest that must be attached to the generation call. This is what prevents a locked location (e.g. a specific desk with a specific bookshelf and lamp) from being silently reinvented because the shot text alone would also produce *a* plausible room.

Both are lightweight, text-first checks — they cost no generation credits and should run even when the storyboard step is producing a single multi-panel sheet in one generation call (in that case, the reference manifest is the union of every panel's requirements, all attached to that one call).

A third companion skill runs even earlier, at the start of any work session on a project: **`detail-reference-intake`**. It watches the project's `reference/working detailed references/` folder for new screenshots/stills the user has captured from test generations or test animations (details that emerged as a side effect of an unrelated test, not planned in advance), identifies what specific reusable detail each new file shows, and locks it into the project's reference index so `storyboard-reference-assembly` picks it up like any other canonical asset. Run this before storyboarding whenever the project has this folder.

## Additional Resources

- Location name examples and expansion: `references/locations.md`
- Face replacement prompt templates: `references/face-swap-templates.md`
- Multi-shot adaptation examples: `references/multi-shot-adaptation.md`
- Storyboard reference checklist: `storyboard-reference-assembly` skill
- Storyboard shot-to-shot state continuity: `storyboard-continuity-tracker` skill
- Storyboard shot-size rationale (why this shot, here): `storyboard-shot-selection` skill
- Working-references folder intake: `detail-reference-intake` skill
- Cross-clip video continuity (prop/state handoff between separate video generations): `video-clip-continuity-chain` skill
