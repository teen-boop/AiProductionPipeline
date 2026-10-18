---
name: animation-handoff-folder
description: >-
  Keeps ONE flat hand-off folder for the animator: only FINAL frames, in ascending storyboard order, named by their storyboard number and
  label, plus ONE text file with every frame's animation prompt in the same order (and first/last-frame pairing for keyframe chains).
  Synced after every delivery: new frames copied, replaced frames removed, nothing pending. Use when the user wants to start animating,
  asks for "the animation folder", "all prompts in order", "what can I animate", or after any batch of frames is delivered.
user-invocable: true
---

# Animation Hand-off Folder

The user animates by hand. For each frame they open the picture, copy its prompt and paste it into the video tool. The folder has to
be trustworthy: every picture in it is final, and every picture has its prompt.

## Layout

```
ANIMATION/                     (one flat folder — no subfolders)
  0000_PROMPTS.txt             every prompt, in the same order as the pictures
  0130_A4_elite_on_Piccadilly.png
  0170d_A4_elite_and_poor — Hyde_Park.png
  1620f_D2_letter_from_America.png
  …
```

- File name: `<storyboard number>_<beat>_<label>.png`. Sorting by name equals story order.
- Each prompt entry has:
  - the file name and the duration;
  - the continuous-shot prompt with timed beats (`0–5 s: …`);
  - a colour lock line, generated from the frame's own palette;
  - a negative line.
- **Keyframe chains:** the entry starts with
  `KLING: Start frame = <this>, End frame = <next number>`. The last keyframe of a chain says it is a start frame only.

## Sync rules (run after every delivery)

1. The source of truth is the built storyboard. Copy the frames that are final, and only those.
2. Leave out:
   - frames whose beat is being re-shot;
   - frames with a pending replacement;
   - rejected versions.
3. Include new frames that were added into a rebuilt beat. Do not filter them out just because their name lacks the rebuild prefix.
4. Delete files that are no longer final. On exFAT/SMB volumes, compare names after Unicode NFC normalisation: NFD names otherwise fail
   to match and are never removed.
5. Every picture must have a prompt. A frame without its own prompt inherits it:
   - **identity fix:** strip `_idfix<N>` repeatedly until a known prompt is found;
   - **extra version:** use the prompt of version 1.
6. Report: `ANIMATION: <n> final frames + prompts`. If the count changed by something other than what you delivered, investigate before
   telling the user it is ready.

## Never

- Never put frames waiting for QC or generation in the folder ("they will appear when ready").
- Never split the prompts into several files or subfolders. The user asked for one folder and one list.
