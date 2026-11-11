---
name: video-cut-timecodes
description: >-
  Frame-accurate breakdown of a source video into TIMECODE BLOCKS — one block per shot, a new block at every cut — plus the timing of
  the ACTIONS inside long takes, for video-to-video edit prompts (Seedance 2.5 Edit, Higgsfield, Kling, Runway). Detects hard cuts,
  SOFT cuts (between dark or similar shots, which a plain scene threshold misses) and black frames, snaps every time to the frame grid,
  takes the duration from the video stream (not the container), and draws a frame sheet per block plus a beat sheet (a frame every
  0.5 s) for every take longer than 4 s. When a block is wrong the user chooses: re-detect AUTOMATICALLY or enter cut times MANUALLY
  (seconds or SS.FF). Use before writing any prompt based on another video, when the user gives a source clip for an edit/recast, when
  the user says the timecodes are wrong, or when generated cuts land at the wrong time.
user-invocable: true
---

# Video Cut Timecodes

## This project first (binding)

This skill arrives at every project knowing nothing about it. Before applying any default written below:

1. **Study this project.** Read its brief or script, every file in its references folder (images, video frames, saved prompts and their notes) and the results already approved in it. Say what you see in concrete terms before generating or writing anything.
2. **Learn from this project's results.** After each approved result, add to this project's `LESSONS.md` what was asked, the prompt or setting that produced it and why it worked; after each rejection, what failed and the fix. Read `LESSONS.md` before the next task. For this project it overrides the defaults below.
3. **Stay inside this project.** Never open, copy or imitate material from another project, brand or earlier job: no images, fonts, prompts, names or folders from elsewhere. What is missing comes from this project's own sources or from the user.
4. **Examples here are samples.** Every name, date, place or line used as an example in this skill is invented sample data. Do not carry it into the work.
5. **Improve the skill, not a memory of one project.** When a lesson would help any project, propose it to the user as a general rule with no project names in it.

The source video is the timeline. Each cut gets its own block, so every block can carry its own motion line, voice line, references and
look lock (`segment-reference-lock`). A missed cut merges two shots into one description, and the model then blends them. A wrong time
inside a long take puts the action on the wrong moment.

## What goes wrong without this skill (all seen in real projects)

- **Missed cuts between dark or similar shots.** A cut from wide to close on a dark set scored 0.21–0.25. That is under the
  0.30 threshold, but ten times its neighbours (about 0.02). The result was 6 blocks instead of 9.
- **Rounded times.** One decimal turns 2.875 into 2.9 and 4.333 into 4.3. Seedance then cuts a few frames off.
- **Wrong duration.** The container duration includes audio and data streams (16.53 s against 16.46 s of real video).
- **A lost end frame.** A single black frame at the end was merged into the last shot by the minimum-length rule.
- **Guessed action times inside a long take.** "Bends at 9.5 s" was guessed from 1-second samples. In reality the subject stops at
  9.0 s and starts to bend at 13.5 s.

## 1. Detect (automatic by default)

```
python3 scripts/cut_timecodes.py auto SOURCE.mp4 --out <project>/edit/<clip>_timecodes
```

- **fps and the frame count** are read from the video stream.
- **Cut types:**
  - HARD: scene score above `--threshold`. The default is 0.30.
  - SOFT: a lone peak above `--soft` (default 0.12) that is at least 5x the median of its ±12 neighbours. These are marked
    `shot (soft cut)`.
  - **Black frames:** mean luma ≤ 20 of 255. They become their own `black` blocks and are never merged away.
- `--min` (default 0.4 s) merges only false hard/soft cuts that sit too close together.
- **Outputs:**
  - `segments.json` holds frame numbers (`start_f`/`end_f`) plus seconds.
  - `segments.md` is a table in seconds (2 decimals), SS.FF and frames.
  - `segments_sheet.jpg` shows the first, middle and last frame of every block.
  - `beats_bNN.jpg` is written for every block of 4 s or longer: a frame every 0.5 s, each labelled with its time and frame number.
    Tune with `--beat-min` and `--beat-step`.

## 2. Look before you trust it (mandatory)

1. **`segments_sheet.jpg`:**
   - Does one block contain two different shots? Then a cut was missed. Do two consecutive blocks show the same shot? Then a false
     cut was found (a flash or a fast pan).
2. **Every `beats_bNN.jpg`:**
   - A sudden jump in framing between two neighbouring frames is a missed cut. Find its exact frame with a finer sheet
     (`--beat-step 0.0417` = every frame) and add it manually.
   - For a real single take, write down the action beats from the labelled frames: when the subject starts walking, stops, bends,
     touches, releases, and when the camera starts or stops moving. Use these times. Never guess them from coarse samples.
   - Note dissolves and fades: they get a block of their own, or a line "dissolve from X to Y over A–B s".
3. **Tell the user about any `black` or very short blocks.** They belong in the prompt ("one black frame, exactly as in @vid-1").

## 3. Confirm with the user

Show the table and the sheets, then ask ONE question with two options (in the user's language):

- **Automatic.** Re-detect with another sensitivity:
  - for missed cuts, lower `--soft` to 0.08 or `--threshold` to 0.20;
  - for false cuts, raise them.
  - Iterate at most twice, then switch to manual.
- **Manual.** The user types the cut times, for example `"3.21, 7.10, 12.00"`. Ask whether they are seconds or SS.FF from an editing
  timeline. At 24 fps, "03.21" means 3 s + 21 frames. Then run:
  ```
  cut_timecodes.py manual SOURCE.mp4 "3.21, 7.10, 12.00" --frames --out …
  ```

If the user corrects one block ("cut #4 is at 9.12"), apply that single change directly and show the table again.

## 4. Validate

```
python3 scripts/cut_timecodes.py check …/segments.json
```

- The blocks must be continuous on the frame grid, start at frame 0 and end at the last video frame.
- A block shorter than 0.3 s that is not `black` is almost always a false cut.
- Do not write a prompt until the check says OK.

## 5. Hand over to the prompt

- The confirmed `segments.json` is the timeline for:
  - `segment-reference-lock`;
  - `seedance-edit-prompting` (one block per shot).
- **Write block ranges with two decimals** (`[2.88-4.33 s]`), exactly from the table. Do not round to whole or half seconds.
- **A long take split into sub-blocks for the action beats** is labelled "same take, no cut", with the beat times from the beat sheet.
  This stops the model from inventing cuts there.
- **The last block ends at the real video end**, including black frames.
- **If the clip was trimmed from a longer video,** say which time base is used and convert the user's timestamps.

## Rules

- Never write a shot order or an action time from memory, from a different clip length, or from 1-second samples. Every time comes
  from this script's table or beat sheets.
- Re-run the detection when the user re-uploads or re-trims the source.
- The tool is free and local (ffmpeg + Pillow). It never uploads the video anywhere.
