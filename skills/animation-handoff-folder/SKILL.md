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

## This project first (binding)

This skill arrives at every project knowing nothing about it. Before applying any default written below:

1. **Study this project.** Read its brief or script, every file in its references folder (images, video frames, saved prompts and their notes) and the results already approved in it. Say what you see in concrete terms before generating or writing anything.
2. **Learn from this project's results.** After each approved result, add to this project's `LESSONS.md` what was asked, the prompt or setting that produced it and why it worked; after each rejection, what failed and the fix. Read `LESSONS.md` before the next task. For this project it overrides the defaults below.
3. **Stay inside this project.** Never open, copy or imitate material from another project, brand or earlier job: no images, fonts, prompts, names or folders from elsewhere. What is missing comes from this project's own sources or from the user.
4. **Examples here are samples.** Every name, date, place or line used as an example in this skill is invented sample data. Do not carry it into the work.
5. **Improve the skill, not a memory of one project.** When a lesson would help any project, propose it to the user as a general rule with no project names in it.

The user animates by hand. For each frame they open the picture, copy its prompt and paste it into the video tool. The folder has to
be trustworthy: every picture in it is final, and every picture has its prompt.

## Layout

```
ANIMATION/                     (one flat folder — no subfolders)
  0000_PROMPTS.txt             every prompt, in the same order as the pictures
  0130_A4_market_at_dawn.png
  0170d_A4_two_sellers — Town_Square.png
  1620f_D2_letter_from_home.png
  …
```

- File name: `<storyboard number>_<beat>_<label>.png`. Sorting by name equals story order.
- Letter suffixes for inserted frames must keep that order: `a … y`, then `za, zb, …`. Never `aa`, which sorts between `a` and `b` in
  Finder, so the user cannot find the frames and every "End frame = the NEXT picture" pairing breaks.
- Each prompt entry has:
  - the file name and the duration;
  - the continuous-shot prompt with timed beats (`0–5 s: …`);
  - a colour lock line, generated from the frame's own palette;
  - a negative line.
- **Keyframe chains:** the entry starts with `KLING: Start frame = this picture, End frame = the picture <exact file name of the end frame>`.
  Never write "the NEXT picture in this folder": as soon as another frame is inserted between a start and its end (transitions,
  interleaved micro-stories), the next picture is the wrong one. Resolve the end frame from the chain's pairs at sync time; if it is not
  final yet, say so. The last keyframe of a chain says it is a start frame only.

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
6. Rebuild the browsable page with `animation-prompts-page`. When the user wants to see the prompts, open that page; never paste the list.
7. Report: `ANIMATION: <n> final frames + prompts`. If the count changed by something other than what you delivered, investigate before
   telling the user it is ready.

## Never

- Never put frames waiting for QC or generation in the folder ("they will appear when ready").
- Never split the prompts into several files or subfolders. One folder and one list is the contract.
