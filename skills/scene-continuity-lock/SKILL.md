---
name: scene-continuity-lock
description: Prompt-level continuity guard for one scene — for BOTH storyboard panels and final frames. Builds a SCENE STATE sheet (who sits/lies where on which piece of furniture, pose, held props, prop states such as a box open or closed, light, time, camera axis) and checks every shot prompt against the PREVIOUS and the NEXT prompt of the same scene before generation — then injects a verbatim CONTINUITY block into each prompt and QCs each generated frame against it. Catches characters changing seats, a character ending a scene on a different chair than he started on, an animal moving between seats with no cause, props changing state, duplicated objects, and reverse shots that fail to mirror left/right. Extends storyboard-continuity-tracker (text ledger) down to the actual prompts and images. Use for every multi-shot scene before writing or generating its prompts, after any frame is rejected for continuity, and whenever the user says "continuity", "he was sitting somewhere else", "the cup was on the table", "previous and next frame", "watch the scene details".
---

# Scene Continuity Lock

## This project first (binding)

This skill arrives at every project knowing nothing about it. Before applying any default written below:

1. **Study this project.** Read its brief or script, every file in its references folder (images, video frames, saved prompts and their notes) and the results already approved in it. Say what you see in concrete terms before generating or writing anything.
2. **Learn from this project's results.** After each approved result, add to this project's `LESSONS.md` what was asked, the prompt or setting that produced it and why it worked; after each rejection, what failed and the fix. Read `LESSONS.md` before the next task. For this project it overrides the defaults below.
3. **Stay inside this project.** Never open, copy or imitate material from another project, brand or earlier job: no images, fonts, prompts, names or folders from elsewhere. What is missing comes from this project's own sources or from the user.
4. **Examples here are samples.** Every name, date, place or line used as an example in this skill is invented sample data. Do not carry it into the work.
5. **Improve the skill, not a memory of one project.** When a lesson would help any project, propose it to the user as a general rule with no project names in it.

## Why
Each prompt is generated alone, so each one re-imagines the scene: the character seated at the table in shot 1 stands by the window in shot 2, the closed suitcase becomes open, the cup moves to the other hand, the reverse shot keeps the same left-to-right order as the front shot. `storyboard-continuity-tracker` catches this in the shot list. This skill carries the same state INTO every prompt as hard text and checks the neighbours on both sides.

## Inputs
- Shot list of ONE scene (in order).
- `ROOM_MAP.md` from `location-room-map` (walls, seat map, camera table). If it is missing for an interior with more than one camera direction, run that skill first.
- Character/prop locks of the project.

## Step 1: SCENE STATE sheet (before any prompt)
Write `continuity/<EPISODE>_<SCENE>.md` with:
- **Time and light:** e.g. late evening; which lamps are on; screens on/off and what they show.
- **Seat map**, as seen from the master camera, left → right: each character, which furniture, which part, pose, facing.
- **Props table:** each prop, its location, state (open/closed, on/off, full/spilled) and who holds it.
- **Single-object list:** things that exist exactly once (lamp, suitcase, radio).
- **Camera axis:** where the master camera stands; which side is the 180° line. A reverse shot MIRRORS the order: left becomes right.
- **Per-shot rows:** shot → camera position → wall behind (from the room map) → START state → END state for every entity, including off-frame ones.

## Step 2: neighbour check (for each shot N)
Against **N−1**:
- Every entity's START equals N−1's END, or the change is a shown, causal action in N.
- Same furniture, same seat, same side. A character who stays put is **where he was**.
- Prop states carry over: a suitcase doesn't close itself, a cup doesn't move to another person.
- Light and time carry over (night stays night, the same lamps stay on).
- Reverse or OTS shot: order mirrored, background = the correct wall from the room map, not the master wall.

Against **N+1**:
- N's END state makes N+1 possible. If N+1 needs the suitcase open on the bed, N must already have it there. If N+1 picks up the cup with the left hand, N leaves that hand free.
- Anything N+1 reveals (a door, a window, an object) is present or explicitly set up in N.

Any failure → rewrite the prompt, add a bridging shot, or ask the user. Never generate around a known break.

## Step 3: CONTINUITY block (verbatim at the end of every prompt, before the face clause)
```
CONTINUITY (same scene as previous and next shot):
Time/light: [ ... ]
Positions, left to right as seen in THIS shot: [ ... ] (mirrored from the master if reverse)
Props: [object: place, state, who holds it] ...
Exactly one: [lamp, suitcase, radio, ...] — never duplicate them.
Background wall: [WALL S — the wall with the entrance door], not the window wall.
Previous shot ended with: [ ... ]. Next shot begins with: [ ... ].
```

## Step 4: post-generation QC (each frame, before approving)
Check against the sheet: seats and sides, poses, props and their states, single objects (count them), background wall, light and time, faces and costumes. Name every failed item. Rejected frames go to the project's `_rejected/` folder with a one-line reason in the sheet, and the fix goes into the prompt, not just a retry.

## Storyboards are checked the same way (mandatory)
Pencil storyboard panels drift exactly like final frames (character on the floor in panel 1, on a chair in panel 2; a round lamp instead of the square one; closed suitcase instead of open; non-mirrored reverse). So:
- Every storyboard prompt gets a short **CONTINUITY (storyboard)** block from the SAME scene sheet: positions left to right in THIS panel, furniture each one is on, key props and their states, the background wall. Exactly the same facts as the final-frame prompt, only shorter.
- Every panel is QC'd against the sheet before approval, item by item (seats, sides, floor vs furniture, props, counts of single objects, wall). A rejected panel is regenerated with the fix written into the prompt.
- An approved panel set becomes the **layout lock** for the final frames: final-frame prompts must match the approved panel's placement, and the sheet is the single source of truth for both. If the user approves a deviation in a panel, update the sheet first, then both prompt sets.
- Check the storyboard as a SEQUENCE too: lay the panels side by side and walk each entity through every panel (where is Character A in panel 1, 2, 3…?).

## Step 5: keep the sheet alive
After a frame is approved, update its END state from what the image ACTUALLY shows (if the user approves a deviation, e.g. the cup on the shelf, it becomes canon and the following prompts change). The next prompt is always written from the approved image's real state.
