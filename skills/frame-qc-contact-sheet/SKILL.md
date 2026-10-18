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

Looking at one full-size image at a time is slow, and it hides problems that only show side by side: colour jumps, flipped orientation,
or the same pose across time. Always QC on sheets.

## Tools (`scripts/`, Python 3 + Pillow)

| Script | Use |
|---|---|
| `contact_sheet.py OUT.jpg IMG…` | A 2-column grid, each cell labelled with its file or folder name |
| `pair_sheet.py OUT.jpg START END [START END …]` (`--chain 3` for K1 K2 K3 rows) | Rows of start → end for change-to frames and keyframe chains |
| `face_crops.py OUT.jpg REF.png IMG@x,y[,r] …` | The identity reference plus crops centred on (x, y) as fractions of width and height, for face checks |
| `trim_bars.py IMG…` | Detects near-black rows at the top and bottom and crops them, keeping 16:9. The original is kept as `_orig_bars_*` |

## The checklist (apply to every frame)

1. **Format:**
   - full-bleed 16:9;
   - no letterbox bars, rounded corners or vignette frame;
   - no split screen.
2. **Text:** no readable text except what the shot needs; no wrong names.
3. **Hero count and shape:**
   - exactly one of each hero;
   - signature features correct (for example, exactly 4 funnels and smoke only where it should be).
4. **Period:**
   - no anachronisms in clothes, machines, buildings or the stage of construction;
   - the right city or country.
5. **Physics and safety:** the action is plausible; nobody is in danger in a way the story does not intend.
6. **Identity:** in-focus faces match the reference (hairline, face width, age). Check them with `face_crops.py`; thumbnails lie.
7. **Optics and grade:**
   - shallow depth of field;
   - the series grade;
   - no sourceless bokeh orbs or blue streaks;
   - no glossy CGI.
8. **Story beat:** the frame shows what the script line says (time of day, the ship sinking rather than level, and so on).
9. **Chains:** use `pair_sheet.py` and check:
   - the same world;
   - time moving forward;
   - the same orientation;
   - no colour jump between the frames.

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

- Never deliver a frame you did not look at. Deliver an explicit list of accepted files, never "everything in the folder".
- A frame that was claimed by a worker before you changed its prompt comes back with the OLD prompt. Check its timestamp against your edit.
