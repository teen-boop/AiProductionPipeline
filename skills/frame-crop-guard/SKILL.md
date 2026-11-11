---
name: frame-crop-guard
description: >-
  Catches bad crops before a render. A tall narrow tile showing a landscape frame keeps a background prop and loses the
  face. A character sheet gets cut in half. A close-up is cropped through the eyes. A vertical version keeps the
  wrong side of the frame. The skill lays out the real compositions in headless Chrome to read the exact box,
  object-fit and object-position of every image and video, including the vertical layout. It finds faces and
  people in each source with Apple Vision and computes what is really visible after the push-in. Each crop is
  flagged LOST_SUBJECT, FACE_OUT, FACE_CUT, FACE_AT_EDGE, BODY_CUT, HEAVY_CROP or DISTORTED, with the
  object-position that fixes it or the advice to change the box. Writes a report and a sheet that shows each crop
  window on its source. Use before rendering any HyperFrames, Remotion or HTML video, slide or poster that places
  photos or clips in tiles, when the user says frames are badly cropped, "the crop cuts the face", "check the crops",
  or after changing a layout or swapping assets. Includes scripts/crop_boxes.mjs, crop_check.py and subjects.swift.
user-invocable: true
---

# Frame Crop Guard

## This project first (binding)

This skill arrives at every project knowing nothing about it. Before applying any default written below:

1. **Study this project.** Read its brief or script, every file in its references folder (images, video frames, saved prompts and their notes) and the results already approved in it. Say what you see in concrete terms before generating or writing anything.
2. **Learn from this project's results.** After each approved result, add to this project's `LESSONS.md` what was asked, the prompt or setting that produced it and why it worked; after each rejection, what failed and the fix. Read `LESSONS.md` before the next task. For this project it overrides the defaults below.
3. **Stay inside this project.** Never open, copy or imitate material from another project, brand or earlier job: no images, fonts, prompts, names or folders from elsewhere. What is missing comes from this project's own sources or from the user.
4. **Examples here are samples.** Every name, date, place or line used as an example in this skill is invented sample data. Do not carry it into the work.
5. **Improve the skill, not a memory of one project.** When a lesson would help any project, propose it to the user as a general rule with no project names in it.

A crop is a decision about who the shot is about. `object-fit: cover` in a box with a different shape from the source makes that decision silently, from the centre. Left unchecked it can keep a background prop instead of two faces, show a person from behind, or cut a character sheet in half, and nobody sees it until the render. This skill checks every crop against the people in the source before anything is rendered.

## 1. Read the real layout

```
node scripts/crop_boxes.mjs --width 1920 --height 1080 --out qc/boxes_16x9.json promo-16x9/compositions/*.html
node scripts/crop_boxes.mjs --width 1080 --height 1920 --out qc/boxes_9x16.json promo-9x16/compositions/*.html
```

- Each composition (`<template>` sub-compositions or plain pages) is laid out in headless Chrome at the target size. Scripts are not run, so this is the resting CSS layout, which is where crops are decided.
- **Vertical layouts:** a class that a runtime adds must be named. The default for a vertical size is `#root=is-portrait`; check which class this project's own runtime adds. Without it the check measures the landscape CSS. Pass `--portrait-class "<selector>=<class>"` for other engines, or `""` to switch it off.
- For every `<img>` and `<video>` the script writes the box, object-fit, object-position, natural size, the clipping parent and `data-media-start`.

## 2. Check every crop

```
python3 scripts/crop_check.py qc/boxes_16x9.json --out qc/crops_16x9 --push 1.08
```

- **Faces and people.** Apple Vision finds faces and whole people in each source; for a video it uses the frame at media start + 0.5 s. The detector is compiled once from `subjects.swift` into `~/.cache/frame-crop-guard`. It needs macOS and the Xcode command line tools.
- **Visible window.** The part of the source that is visible comes from cover, contain or fill, object-position and the clipping parent. It is then shrunk by `--push`, the largest push-in the composition applies to media.

| Flag | Level | Meaning |
|---|---|---|
| LOST_SUBJECT | high | the source has faces, none is kept at 90% or more |
| FACE_OUT | high (largest face) | a face is outside the crop |
| FACE_CUT | high | a face is cut by the edge (15 to 90% visible) |
| DISTORTED | high | `object-fit: fill` stretches the image |
| FACE_AT_EDGE | medium | a whole face sits within 3% of the edge |
| BODY_CUT | medium | a person whose face is kept loses over 40% of the body (sheets, full-length shots) |
| HEAVY_CROP | medium | under 35% of a faceless source is visible (boards, text, wide plates) |

For each flagged item the report gives a fix. Either it is the `object-position` that centres the faces (or the people), or it says the subject is larger than the window: use contain, a wider box, or another source frame. The exit code is 1 while any high flag remains.

## 3. Look, then fix

Open `sheet.jpg`. It shows each source with the visible window in yellow, kept faces in green and lost or cut faces in red. The detector misses faces in profile, in silhouette and at very small sizes. It also sees faces you do not care about, such as a crew member at the edge of a set photo. The sheet is where you decide.

Fixes, best first:
1. **Match the box to the source.** Give tiles the source's aspect ratio (`aspect-ratio: 16 / 9`, a grid with `auto` columns and `justify-content: center`) instead of stretching a row of narrow strips. Fewer, larger tiles beat many slivers.
2. **Show fewer items in the vertical layout** (`:nth-child(n+4) { display: none }`) rather than squeezing every tile.
3. **Use the suggested `object-position`** for the layout where it applies (for example `#root.is-portrait #id img { object-position: 50% 14%; }`).
4. **`object-fit: contain`** on a matching background for screenshots, app pages and posters: their edges carry the content.
5. **Another source frame** when the subject is larger than any window the layout can give.

Re-run steps 1 and 2 until no high flags remain, for every aspect ratio. Then render, and check the encoded file with `render-cut-verification`.

## Never

- Never place a landscape frame in a tall tile, or the reverse, without running this check.
- Never trust a centre crop on character sheets, turnarounds, group shots or app screenshots.
- Never check only the landscape layout: vertical versions crop differently and fail more often.
- Never call a layout clean from the report alone; look at the sheet.
