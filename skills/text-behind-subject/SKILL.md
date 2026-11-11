---
name: text-behind-subject
description: >-
  The "depth text" effect: a big word, title or number placed BETWEEN the background and the person (or animal, robot, product), so
  the subject stands in front of the type. Covers shot suitability (medium shot with headroom; the subject must not fill the frame),
  matting only the seconds needed (Apple Vision person segmentation, rembg/RVM-style matting, DaVinci Magic Mask, Premiere/After
  Effects roto), mask cleanup (temporal smoothing, shrink, grow, feather), alpha export (VP9 webm with alpha or ProRes 4444), the
  3-layer composite in HyperFrames, Remotion or an NLE, and the QC. Works for video and for stills (posters, covers). Use when the user
  says "put the text behind her", "title behind the character", "number behind the presenter", "depth text", "text behind person",
  "subject in front of the title", "poster with the title behind the hero".
user-invocable: true
---

# Text Behind Subject

## This project first (binding)

This skill arrives at every project knowing nothing about it. Before applying any default written below:

1. **Study this project.** Read its brief or script, every file in its references folder (images, video frames, saved prompts and their notes) and the results already approved in it. Say what you see in concrete terms before generating or writing anything.
2. **Learn from this project's results.** After each approved result, add to this project's `LESSONS.md` what was asked, the prompt or setting that produced it and why it worked; after each rejection, what failed and the fix. Read `LESSONS.md` before the next task. For this project it overrides the defaults below.
3. **Stay inside this project.** Never open, copy or imitate material from another project, brand or earlier job: no images, fonts, prompts, names or folders from elsewhere. What is missing comes from this project's own sources or from the user.
4. **Examples here are samples.** Every name, date, place or line used as an example in this skill is invented sample data. Do not carry it into the work.
5. **Improve the skill, not a memory of one project.** When a lesson would help any project, propose it to the user as a general rule with no project names in it.

> **Optional — not every time.** Offer this effect where it helps (covers, title cards, a promo hook, a chapter opener) and use it only when the user agrees. It should stay a rare accent, not a default style.

Three layers: the original shot at the back, the big type in the middle, the cut-out subject on top. It reads as premium and costs
nothing to generate, but only works on the right shot and only if the matte edge is clean.

## 1. Is the shot suitable? (check before matting)

- Medium or wider shot, with background visible above the head and on both sides.
- Measure subject coverage on the matte (white pixels / frame). Under about 30 %: ideal. Above about 60 %: the subject hides the
  type; do not use the effect. A selfie close-up (about 90 % coverage) fails; a medium shot at under 60 % works.
- Clean, low-detail background behind the head and shoulders is best.
- If the shot is not suitable and it is still to be generated, ask for it as a medium shot with headroom (in a presenter script mark
  the segment `depth`; in a shot list note "headroom for title behind subject").
- Use it 2-4 times per piece: the opening claim, a key number, a chapter title, a quote. Not every sentence.

## 2. Matte only the seconds you need

Matting a whole long take is slow; cut the range first (`--from` / `--to` or an in/out on the timeline), and remember the range start
because the composite needs it to line up.

Pick a matting route:
- **macOS**: Apple Vision person segmentation (high-quality mode), frame by frame, compiled locally.
- **Any OS**: an open-source matting model (rembg / robust video matting style). Check its licence before adding it to a project.
- **DaVinci Resolve**: Magic Mask (person) on the clip, then render with alpha.
- **Premiere / After Effects**: Roto Brush or object mask, then render with alpha.
- Non-human subjects (robot, product, animal): use an object/salient segmentation model, or Magic Mask object mode.

## 3. Clean the matte

- **Temporal smoothing**: average the mask over about 3 neighbouring frames to stop edge flicker.
- **Shrink** 1-2 px when a grey or background-coloured halo shows around the subject.
- **Grow** about 1 px when hair or fingers get eaten (it brings a little background back; accept a trace).
- **Feather** about 1.5 px.
- Always export a grey mask preview next to the alpha file and look at it in motion before compositing.

Export the cut-out: VP9 with alpha in `.webm` (small; plays transparent in HyperFrames and Remotion), or ProRes 4444 `.mov` for NLEs.

## 4. Composite

1. Bottom: the original shot.
2. Middle: the type. Very large (in landscape about 30-45 % of the frame height), set behind the head and shoulders (around 36 % from
   the top in landscape, about 28 % in vertical). Animate in: rise, slam, slide, or a counting number that snaps to the exact final
   value.
3. Top: the cut-out, aligned by the range start time and the same scale and position as the bottom layer. If the bottom layer has a
   punch-in or camera move, apply the identical transform to the cut-out, or the subject will jump on entry and exit.
4. The type must still read with the subject in front: the important letters or digits stay visible beside the head, not behind it.

HyperFrames: three stacked timed elements (video, text, transparent video) inside one clip, the transparent video seeked to the same
time as the base. Stills (posters, covers): same three layers in code or in an editor; set the type in code, never generated.

## 5. QC

- Contact sheet of the first, middle and last frame of each use, plus a 200 % crop of the edge around the hair and shoulders.
- Reject: halo, flicker, missing hands or hair, type hidden by the subject, subject jumping on entry or exit, text clashing with
  burned-in captions.

## Never

- Never use it on a close-up where the subject fills the frame.
- Never matte the whole video when only a few seconds are used.
- Never composite a cut-out that is offset in time or scale from the base layer.
- Never generate the type inside an image model; set it in code or the editor.
- Never ship without checking the matte edge in motion.
