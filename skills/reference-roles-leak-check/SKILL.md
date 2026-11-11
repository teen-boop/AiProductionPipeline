---
name: reference-roles-leak-check
description: >-
  Gives every reference image in a multi-reference generation exactly ONE job (who, where, pose, angle, style, light, palette,
  material, expression, wear, inspiration, layout), writes a "do not take" line for each picture, orders the jobs so the one most
  likely to be ignored comes first, and runs a leak check on the result before it is kept: is each picture's job visible, and is
  anything ELSE from it visible (its face, its objects, its colors, its words). Use whenever a prompt carries two or more
  reference images (Nano Banana, GPT Image, Seedream, Seedance reference-to-video, Lovart attachments), when a reference
  "leaks" (a stranger's face pasted onto a character, a style card's props walking into the scene, a palette ignored), when a
  reference's role is ignored, or when the user says "combine these references", "take only the light from this", "the face
  came from the wrong picture". Adapted from scenario-labs/skills (MIT).
user-invocable: true
---

# Reference Roles and Leak Check

## This project first (binding)

This skill arrives at every project knowing nothing about it. Before applying any default written below:

1. **Study this project.** Read its brief or script, every file in its references folder (images, video frames, saved prompts and their notes) and the results already approved in it. Say what you see in concrete terms before generating or writing anything.
2. **Learn from this project's results.** After each approved result, add to this project's `LESSONS.md` what was asked, the prompt or setting that produced it and why it worked; after each rejection, what failed and the fix. Read `LESSONS.md` before the next task. For this project it overrides the defaults below.
3. **Stay inside this project.** Never open, copy or imitate material from another project, brand or earlier job: no images, fonts, prompts, names or folders from elsewhere. What is missing comes from this project's own sources or from the user.
4. **Examples here are samples.** Every name, date, place or line used as an example in this skill is invented sample data. Do not carry it into the work.
5. **Improve the skill, not a memory of one project.** When a lesson would help any project, propose it to the user as a general rule with no project names in it.

A reference image lends EVERYTHING it shows unless the prompt says otherwise. Hand a model a film still as a style reference
and the actor in that still walks into your frame. That is how a pasted-on face appears on an invented character: a scene
reference carried its own person, and nothing told the model to leave that person out.

The fix: each picture gets exactly one job, and for every picture the prompt says what NOT to take from it.

Platform independent: works with any multi-reference image or video model. Reference caps and how the prompt addresses
images ("Image 1", `@Image1`, attachment order) come from the model's own docs; check them before numbering.

## 1. Assign one job per picture

| Job | The picture lends | Typical "do not" line |
| --- | --- | --- |
| WHO (main subject) | the character, product | "Use only this person's face and hair. Do not copy the sheet's layout, labels or background." |
| WHERE (stage) | the place | "Do not include any person from this photo." |
| POSE | the body pose | "Do not show the mannequin or any wood." |
| ANGLE | the camera | "Do not include the windmill." |
| STYLE | medium, render, texture | "Do not include the actor, the set or the props of this still." |
| LIGHT | the light only | "Do not include the flowers or vase." |
| PALETTE | the only allowed colors | "No green anywhere." |
| MATERIAL | a surface | "Do not show any fish, fins or water." |
| EXPRESSION | the mood of a face | "Only the mood moves. No skin, nose or hair from this face." |
| WEAR | clothing or armor | "The character's own face stays visible; no mask." |
| INSPIRATION | a design idea, not the thing | "A gown designed from this jellyfish. Do not show a jellyfish." |
| LAYOUT | grid and composition | "Do not copy the word MONDAY." |

Prompt skeleton, one line per picture:

```text
<One sentence naming the medium.> Each reference picture has exactly one job:
Image N (<what it shows>) = <JOB> only. <What it lends, concretely.> Do not <what to leave out>.
...
<Framing: shot size, placement, mood, text rules.>
```

## 2. Rules that held

- **One job per picture.** Two jobs on one card (subject plus palette) blur both. A card that stays in the call but has no job
  gets "Image 4 = no job: ignore it completely."
- **One identity per picture, one main subject per run.** Two people in one frame: each gets its own WHO card from its own
  locked sheet (see `character-identity-lock-setup`), named by position ("Image 1 = the man on the LEFT"). Never let a scene
  reference supply a face.
- **The job most likely to be ignored goes first**, usually STYLE, with "This is the most important job." A clay scene came
  back as chrome CG until the Style line moved to the top.
- **Lend concretely.** "Copy its 3D render look, soft materials, warm bounce light" beats "use its style". A palette job
  names each element's color ("the hat is yellow, the coat is navy"); "palette only" barely recolors.
- **Settle conflicts between jobs.** Every picture carries more than its job: a style card brings its own colors, a subject
  photo its own fur. With a palette card, the style line adds "do not copy its colors". When that would recolor something the
  user cares about (their character, their product), ask before running.
- **Idea, not copy.** When a subject photo must not survive literally: "Use only the idea of a gecko. Do not copy the photo's
  pose, lighting, colors or realism."
- **Text** is quoted exactly with "No extra words, no duplicate text." Letter-perfect copy goes on top in the edit, not into
  the generation.
- **Clean cards.** Plain backgrounds, no readable signs or logos. Generate a missing card with its own text-to-image run, one
  idea per card.

## 3. Leak check before keeping

For EACH picture ask two questions: is its job visible, and is anything else from it visible?

- WHO: the face matches the identity sheet, not any other face in the call (run `independent-frame-critic` for faces).
- WHERE: no person, vehicle or sign from the location photo that the frame did not ask for.
- POSE and ANGLE: no mannequin, no wood, no prop from the sketch.
- STYLE: none of the style reference's own subject, set or objects.
- EXPRESSION: the mood moved, the face did not.
- LAYOUT: the grid moved, the reference's own words did not.
- PALETTE: no color outside the swatch.

Fix a leak by tightening THAT picture's line (add its "do not", or move its job up) and running again, never by retouching.
Log the fix in `generation-failure-fixes` when it is new.

Before rewriting a line for an ignored job, confirm the model actually received that picture (check the request log or the
platform's run details). A reference dropped by the API returns no job, whatever the wording.

## 4. Into video

When the kept frame is animated, the video prompt carries no jobs, only motion, camera and sound: the frame already holds
every job. For reference-to-video (Seedance with several images) keep the same one-job lines and add "Almost static, these do
not change: ..." for anything that must hold (see `seedance-prompt-writer`, `video-clip-continuity-chain`).

## Common mistakes

- **The main subject copied the photo.** Put STYLE first, use "only the idea of", make the palette strict.
- **A face from the wrong card.** A location or style still with a person in it, and no "do not include any person" line.
- **A logo by accident.** Generated billboards in red, white and blue swooshes read as a soda brand and get refused later. Say
  what signs show (waves, clouds, cranes), or "invented, blank signs, no logos".
- **A protected design named in the prompt.** Describe an original design instead of naming it.
- **Drift in the film.** A guitar changed color mid-clip. Ask for "almost static", list what must not change, move only what
  should.

Related: `storyboard-reference-assembly`, `segment-reference-lock`, `style-lock-guard`, `identity-fix-pass`.
