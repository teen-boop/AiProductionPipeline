---
name: video-cut-timecodes
description: >-
  Splits a source video into TIMECODE BLOCKS — one block per shot, a new block at every cut — for video-to-video edit prompts (Seedance
  2.5 Edit, Higgsfield, Kling, Runway). Detects cuts automatically with ffmpeg, shows a sheet with the first / middle / last frame of every
  block, and when a block is wrong lets the user choose: re-detect AUTOMATICALLY (other sensitivity) or enter the cut times MANUALLY
  (seconds or SS.FF editing-timeline frames). Validates that blocks are continuous and end at the video's end. Use before writing any
  prompt that is based on another video, when the user gives a source clip for an edit/recast, or when generated cuts land at the wrong time.
user-invocable: true
---

# Video Cut Timecodes

The source video is the timeline. Each cut gets its own block, so every block can carry its own motion line, voice line, references and
look lock (`segment-reference-lock`). A missed cut merges two shots into one description, and the model then blends them.

## 1. Detect (automatic by default)

```
python3 scripts/cut_timecodes.py auto SOURCE.mp4 --fps 24 --out <project>/edit/<clip>_timecodes
```

- `--threshold` is the scene-change sensitivity. The default is 0.30. Use 0.20 for soft cuts and dissolves, 0.40 when camera moves or
  flashes create false cuts.
- `--min` is the shortest allowed block in seconds. The default is 0.4. Cuts closer together than this are merged.
- The script writes:
  - `segments.json` (machine-readable);
  - `segments.md` (a table in seconds and SS.FF at the fps);
  - `segments_sheet.jpg` (first, middle and last frame of every block).

## 2. Show the user and confirm

1. **Look at `segments_sheet.jpg` yourself first:**
   - Does one block contain two different shots? Then a cut was missed.
   - Do two consecutive blocks show the same shot? Then a false cut was found (a flash or a fast pan).
2. Show the user the table and the sheet, then ask ONE question with two options (in the user's language):
   - **Automatic.** Re-detect with a corrected sensitivity and re-check. Lower the threshold for missed cuts, raise it for false
     ones. Iterate at most twice, then switch to manual.
   - **Manual.** The user types the cut times: `"3.21, 7.10, 12.00"`. Ask whether these are seconds or SS.FF from an editing timeline.
     At 24 fps, "03.21" means 3 s + 21 frames = 3.875 s. Then run:
     ```
     cut_timecodes.py manual SOURCE.mp4 "3.21, 7.10, 12.00" --frames --fps 24 --out …
     ```
3. If the user only corrects one block ("cut #4 is at 9.12"), you may apply that single change directly, then show the table again.

## 3. Validate

```
python3 scripts/cut_timecodes.py check …/segments.json
```

The blocks must be continuous (no gaps, no overlaps), start at 0 and end at the video's duration. Any block shorter than 0.3 s is
almost always a false cut. Do not write a prompt until the check says OK and the user has confirmed the blocks.

## 4. Hand over

- The confirmed `segments.json` is the timeline for:
  - `segment-reference-lock` (references and look per block);
  - `seedance-edit-prompting` (the final prompt, one block per shot).
- Write block ranges in the prompt in seconds with one decimal, matching the source's time base. If the clip was trimmed from a longer
  video, say which base is used and convert the user's timestamps.

## Rules

- Never write a shot order from memory or from a different clip length. Every block comes from this file.
- Re-run the detection when the user re-uploads or re-trims the source.
- The tool is free and local (ffmpeg + Pillow). It never uploads the video anywhere.
