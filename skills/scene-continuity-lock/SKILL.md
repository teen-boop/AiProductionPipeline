---
name: scene-continuity-lock
description: Prompt-level continuity guard for one scene — for BOTH storyboard panels and final frames. Builds a SCENE STATE sheet (who sits/lies where on which piece of furniture, pose, held props, prop states such as a box open or closed, light, time, camera axis) and checks every shot prompt against the PREVIOUS and the NEXT prompt of the same scene before generation — then injects a verbatim CONTINUITY block into each prompt and QCs each generated frame against it. Catches heroes changing seats, a character falling asleep on a different sofa than he sat on, a dog jumping from sofa to armchair, props changing state, duplicated objects, and reverse shots that fail to mirror left/right. Extends storyboard-continuity-tracker (text ledger) down to the actual prompts and images. Use for every multi-shot scene before writing or generating its prompts, after any frame is rejected for continuity, and whenever the user says "continuity", "он должен уснуть на том же диване", "пёс был на диване", "предыдущий и следующий кадр", "следи за деталями сцены".
---

# Scene Continuity Lock

## Why
Each prompt is generated alone, so each one re-imagines the scene: the dog that lay on the sofa in shot 1 sits in an armchair in shot 2, the closed box becomes open, the hero falls asleep on a different couch, the reverse shot keeps the same left-to-right order as the front shot. `storyboard-continuity-tracker` catches this in the shot list. This skill carries the same state INTO every prompt as hard text and checks the neighbours on both sides.

## Inputs
- Shot list of ONE scene (in order).
- `ROOM_MAP.md` from `location-room-map` (walls, seat map, camera table). If it is missing for an interior with more than one camera direction, run that skill first.
- Character/prop locks of the project.

## Step 1: SCENE STATE sheet (before any prompt)
Write `continuity/<EPISODE>_<SCENE>.md` with:
- **Time and light:** e.g. night 2 AM; which lamps are on; TV on/off and what is on screen.
- **Seat map**, as seen from the master camera, left → right: each character, which furniture, which part, pose, facing.
- **Props table:** each prop, its location, state (open/closed, on/off, full/spilled) and who holds it.
- **Single-object list:** things that exist exactly once (TV, box, guitar).
- **Camera axis:** where the master camera stands; which side is the 180° line. A reverse shot MIRRORS the order: left becomes right.
- **Per-shot rows:** shot → camera position → wall behind (from the room map) → START state → END state for every entity, including off-frame ones.

## Step 2: neighbour check (for each shot N)
Against **N−1**:
- Every entity's START equals N−1's END, or the change is a shown, causal action in N.
- Same furniture, same seat, same side. A character who sleeps does it **where he sat**.
- Prop states carry over: a box doesn't close itself, a bucket doesn't move to another cat.
- Light and time carry over (night stays night, the same lamps stay on).
- Reverse or OTS shot: order mirrored, background = the correct wall from the room map, not the master wall.

Against **N+1**:
- N's END state makes N+1 possible. If N+1 needs the box with a curtain, N must already have the box where N+1 finds it. If N+1 lifts him by the sides, N leaves his sides reachable.
- Anything N+1 reveals (curtain, door, object) is present or explicitly set up in N.

Any failure → rewrite the prompt, add a bridging shot, or ask the user. Never generate around a known break.

## Step 3: CONTINUITY block (verbatim at the end of every prompt, before the face clause)
```
CONTINUITY (same scene as previous and next shot):
Time/light: [ ... ]
Positions, left to right as seen in THIS shot: [ ... ] (mirrored from the master if reverse)
Props: [object: place, state, who holds it] ...
Exactly one: [TV, shoebox, guitar, ...] — never duplicate them.
Background wall: [WALL S — TV wall with entrance door], not the window wall.
Previous shot ended with: [ ... ]. Next shot begins with: [ ... ].
```

## Step 4: post-generation QC (each frame, before approving)
Check against the sheet: seats and sides, poses, props and their states, single objects (count them), background wall, light and time, faces and costumes. Name every failed item. Rejected frames go to `output/Vn/<shot>_vX_rejected.*` with a one-line reason in the sheet, and the fix goes into the prompt, not just a retry.

## Storyboards are checked the same way (mandatory)
Pencil storyboard panels drift exactly like final frames (dog on the floor in panel 1, on the sofa in panel 2; acoustic guitar instead of the Telecaster; closed box instead of open; non-mirrored reverse). So:
- Every storyboard prompt gets a short **CONTINUITY (storyboard)** block from the SAME scene sheet: positions left to right in THIS panel, furniture each one is on, key props and their states, the background wall. Exactly the same facts as the final-frame prompt, only shorter.
- Every panel is QC'd against the sheet before approval, item by item (seats, sides, floor vs furniture, props, counts of single objects, wall). A rejected panel is regenerated with the fix written into the prompt.
- An approved panel set becomes the **layout lock** for the final frames: final-frame prompts must match the approved panel's placement, and the sheet is the single source of truth for both. If the user approves a deviation in a panel, update the sheet first, then both prompt sets.
- Check the storyboard as a SEQUENCE too: lay the panels side by side and walk each entity through every panel (where is the dog in A1, A2, A3…?).

## Step 5: keep the sheet alive
After a frame is approved, update its END state from what the image ACTUALLY shows (if the user approves a deviation, e.g. the dog in the armchair, it becomes canon and the following prompts change). The next prompt is always written from the approved image's real state.
