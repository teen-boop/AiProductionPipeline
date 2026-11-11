---
name: identity-fix-pass
description: >-
  Fixes a WRONG FACE in an otherwise good frame without re-shooting it: re-generates the same image with only the head replaced by the
  locked identity (bust + turnaround), verifies the result with face crops next to the reference, and places the fixed frame into the
  same storyboard slot — including fixes of frames that were themselves already fixes. Use when the user says "wrong face", "that is not his face",
  "this is not him", or when QC finds an identity mismatch (hairline, face width, age) on a named character.
user-invocable: true
---

# Identity Fix Pass

## This project first (binding)

This skill arrives at every project knowing nothing about it. Before applying any default written below:

1. **Study this project.** Read its brief or script, every file in its references folder (images, video frames, saved prompts and their notes) and the results already approved in it. Say what you see in concrete terms before generating or writing anything.
2. **Learn from this project's results.** After each approved result, add to this project's `LESSONS.md` what was asked, the prompt or setting that produced it and why it worked; after each rejection, what failed and the fix. Read `LESSONS.md` before the next task. For this project it overrides the defaults below.
3. **Stay inside this project.** Never open, copy or imitate material from another project, brand or earlier job: no images, fonts, prompts, names or folders from elsewhere. What is missing comes from this project's own sources or from the user.
4. **Examples here are samples.** Every name, date, place or line used as an example in this skill is invented sample data. Do not carry it into the work.
5. **Improve the skill, not a memory of one project.** When a lesson would help any project, propose it to the user as a general rule with no project names in it.

## Inputs

- The frame with the wrong face.
- The character's identity bust and turnaround for the right age. See `character-identity-lock-setup`.
- One sentence that describes the face. Name the features models get wrong: hairline (receding at the temples, high forehead), face
  width, jaw, nose, facial hair, age.

## Prompt (keep-everything edit)

Attach the images in this order:
1. The EXISTING FRAME.
2. The identity bust.
3. The identity turnaround.

Then write:
```
Re-shoot image 1 EXACTLY — same composition, framing, camera angle, lens, place, people, poses, clothes, film grain and depth of field —
and change ONLY what is listed here:
IDENTITY FIX. The man's current face and hair are WRONG (<what is wrong: hairline too low and full / face too narrow>) — replace his
whole head with <NAME at AGE>: <the identity sentence>. Keep his expression, pose, clothes and everything else.
<if needed: he takes the hat off indoors so the hairline shows / which of the people is him / remove lens streaks>
```

Rules:
- Say which person it is when there are several: "the man on the LEFT with the folder; the woman on the right stays as she is".
- Name what is wrong in the current face. "Make it him" alone does not move the model.
- If a hat hides the hairline and the scene allows it, take the hat off. The hairline is the strongest identity cue.

## Verify — never on thumbnails

Make a face sheet: `face_crops.py OUT.jpg BUST.png FIXED.png@x,y …` (see `frame-qc-contact-sheet`). Compare:
- the hairline and temples;
- face width and cheekbones;
- eyes, nose and jaw;
- the apparent age.

Accept only if the face reads as the same man as the bust.

## Placement

- The fixed frame replaces the old one **in the same slot** of the storyboard and keeps the old frame's video prompt. Name the file
  `<old name>_idfix<N>.png` so the prompt lookup can strip `_idfix<N>` repeatedly and find the original prompt.
- **A fix of a fix:** if the frame you replace is itself `…_idfix1.png`, its replacement must be applied **after** the first fix.
  Otherwise the first fix overwrites the new one. See `storyboard-insert-ops` ("late" ordering).

## When to stop editing and re-shoot

If two identity edits in a row fail, the composition fights the face. This happens with profile views, small faces in wide shots, or
heavy shadow. Re-shoot the frame as a new composition with the identity references attached. Do not edit a third time.
