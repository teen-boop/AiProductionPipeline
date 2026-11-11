---
name: frame-qc-contact-sheet
description: >-
  Fast, reliable QC of a batch of generated stills. Builds labelled contact sheets, start|end pair sheets for keyframe chains and face
  crops next to the identity reference, and scans for black letterbox bars; then applies a fixed defect checklist and writes one
  rejection line per failed frame. Use after every generation batch, before delivering frames into the storyboard, or when the user says
  "check the frames", "collect the frames", "QC". Includes scripts: contact_sheet.py, pair_sheet.py, face_crops.py, trim_bars.py.
user-invocable: true
---

# Frame QC with Contact Sheets

## This project first (binding)

This skill arrives at every project knowing nothing about it. Before applying any default written below:

1. **Study this project.** Read its brief or script, every file in its references folder (images, video frames, saved prompts and their notes) and the results already approved in it. Say what you see in concrete terms before generating or writing anything.
2. **Learn from this project's results.** After each approved result, add to this project's `LESSONS.md` what was asked, the prompt or setting that produced it and why it worked; after each rejection, what failed and the fix. Read `LESSONS.md` before the next task. For this project it overrides the defaults below.
3. **Stay inside this project.** Never open, copy or imitate material from another project, brand or earlier job: no images, fonts, prompts, names or folders from elsewhere. What is missing comes from this project's own sources or from the user.
4. **Examples here are samples.** Every name, date, place or line used as an example in this skill is invented sample data. Do not carry it into the work.
5. **Improve the skill, not a memory of one project.** When a lesson would help any project, propose it to the user as a general rule with no project names in it.

Looking at one full-size image at a time is slow, and it hides problems that only show side by side: colour jumps, flipped orientation,
or the same pose across time. Always QC on sheets.

## Tools (`scripts/`, Python 3 + Pillow)

| Script | Use |
|---|---|
| `contact_sheet.py OUT.jpg IMG…` | A 2-column grid, each cell labelled with its file or folder name |
| `pair_sheet.py OUT.jpg START END [START END …]` (`--chain 3` for K1 K2 K3 rows) | Rows of start → end for change-to frames and keyframe chains |
| `face_crops.py OUT.jpg REF.png IMG@x,y[,r] …` | The identity reference plus crops centred on (x, y) as fractions of width and height, for face checks |
| `trim_bars.py IMG…` | Detects near-black rows at the top and bottom and crops them, keeping 16:9. The original is kept as `_orig_bars_*` |

## Two passes, never one

1. **Sheet pass** (`contact_sheet.py`): consistency ACROSS frames — the same face, product, grade, orientation, no colour jump.
   A sheet cell is too small to judge anything inside one frame.
2. **Full-size pass, one frame at a time:** every frame that shows hands, limbs, bodies touching objects or each other,
   a person in a vehicle, text or a hero product is opened at full size (or a 100% crop of that region). Skipping this pass is
   how a wrong arm, a sixth finger or a second product reaches the edit. A frame that only passed the sheet pass is NOT checked.

## The checklist (apply to every frame)

1. **Format:**
   - the project's target ratio (9:16, 16:9, 1:1 — read it from the brief, never assume 16:9), full-bleed;
   - no letterbox bars, rounded corners, vignette frame, split screen, colour panels or hard rectangles in the sky.
2. **Text:** no readable text except what the shot needs; no wrong names; no real brands, logos or brand-like marks.
3. **Hero count and shape:**
   - exactly one of each hero (person, product, vehicle); no duplicate product lying in the frame (extra sneaker pair, second bottle);
   - signature features correct (the product's colours and shape match its master; the vehicle's design matches its sheet).
4. **Anatomy and body continuity** (full-size pass):
   - count arms, hands and fingers of every person: two of each, five fingers, no fused or extra digits;
   - **trace every visible limb back to its body.** An arm entering from a frame edge must belong to the person on that side;
     a hand on a steering wheel, a product or another person must connect to a shoulder you can see or that is plausibly
     just out of frame on the SAME side as that person;
   - the grip is real: fingers wrap the object, the object is not floating or clipping through the hand;
   - in vehicles: the driver sits behind the wheel, on the side the wheel is on; the arms reach it from the driver's body;
     the view through the windows matches the direction of travel;
   - heads, necks and shoulders sit naturally; no twisted torsos, no limbs bending the wrong way.
5. **World and period:**
   - no anachronisms in clothes, machines, buildings;
   - the right city, country and season for the brief.
6. **Physics and safety:** the action is plausible (shadows match the light, water and dust behave, objects rest on surfaces);
   nobody is in danger in a way the story does not intend.
7. **Identity:** in-focus faces match the reference (hairline, face width, age). Check them with `face_crops.py`; thumbnails lie.
8. **Optics and grade:**
   - the look the brief asks for (lens, depth of field, grain);
   - the series grade;
   - no sourceless bokeh orbs or streaks;
   - no glossy CGI.
9. **Story beat:** the frame shows what its intent line says (action, time of day, location).
10. **Chains:** use `pair_sheet.py` and check:
   - the same world;
   - time moving forward;
   - the same orientation;
   - no colour jump between the frames.

## Video clips (extra checks)

For generated VIDEO, sample the first frame, frames every 0.5 s, and the frames around any camera change, and check:

- **Burned-in subtitles or captions** the model added (a line of text at the bottom that nobody asked for) — reject.
- **Frozen first frame** — the first 0.3–1 s identical to the start image with no motion, then a jump — trim or reject.
- **Unasked angle change** around 2.5–3 s (the model cuts to a second camera) — keep only the first continuous seconds.
- **Gibberish on-screen text** (signs, screens) — mask, crop or reject.
- **Mid-transition frames** look clean (no ghost of the previous shot).

## Writing the result

- **Accepted:** list it for delivery. Crop the bars first if there are only thin ones.
- **Rejected:**
  1. Rename the result to `_rejected_vN_RESULT_1.png`. Never delete it.
  2. Append one `FIX:` or `ACCURACY FIX:` line to the frame's prompt. Take it from `generation-failure-fixes`.
  3. Let the queue regenerate it.
- Report the outcome to the user in a short table: frame | verdict | reason.

## Rules

- **Source files are read-only.** Never run ffmpeg (or any tool) with `-y` while a project path can end up in the argument list:
  - Write output only to a scratch or presentation folder.
  - Pass inputs as a quoted array (`-i "$f"` per file). An unquoted list splits differently in zsh and bash, and ffmpeg then treats
    the leftover paths as OUTPUT files and overwrites them.
  - Prefer the bundled Pillow scripts for contact sheets.
  - If duplicate checksums suddenly appear among source frames, stop and report. It is damage, not a pre-existing duplicate.

- Never deliver a frame you did not look at at full size when it shows hands, limbs, contact, a vehicle interior or text.
- Never deliver a frame you did not look at. Deliver an explicit list of accepted files, never "everything in the folder".
- A frame that was claimed by a worker before you changed its prompt comes back with the OLD prompt. Check its timestamp against your edit.
