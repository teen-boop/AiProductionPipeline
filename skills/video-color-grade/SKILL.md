---
name: video-color-grade
description: >-
  Grades video and stills with deterministic local code (ffmpeg + Python numpy/scipy/Pillow), never a generative model: cinematic
  looks (teal and orange, bleach bypass, noir, duotone, faded 70s, pastel film, tobacco), golden hour, blue hour and day-for-night,
  black and white with one kept or swapped color, relight presets, camera log (S-Log3) to Rec.709, and a Reinhard Lab match to a
  reference frame. Every color look is baked to a 33-point .cube LUT that also loads in DaVinci Resolve, Premiere and After Effects.
  Frame count, timing, framing and audio are kept. Use to give a series of generated clips ONE shared look (pairs with
  style-lock-guard), to match a clip to the approved key frame, or when the user says "color grade this", "make it teal and orange",
  "match the colors of this frame", "day for night", "black and white but keep the red", "convert the log footage", "export a LUT for
  Resolve", "show me a look grid", or "make a grading showreel". Includes scripts/render_looks.py, scripts/match.py,
  scripts/inspect_frame.py and scripts/showreel.py.
user-invocable: true
---

# Video Color Grade

## This project first (binding)

This skill arrives at every project knowing nothing about it. Before applying any default written below:

1. **Study this project.** Read its brief or script, every file in its references folder (images, video frames, saved prompts and their notes) and the results already approved in it. Say what you see in concrete terms before generating or writing anything.
2. **Learn from this project's results.** After each approved result, add to this project's `LESSONS.md` what was asked, the prompt or setting that produced it and why it worked; after each rejection, what failed and the fix. Read `LESSONS.md` before the next task. For this project it overrides the defaults below.
3. **Stay inside this project.** Never open, copy or imitate material from another project, brand or earlier job: no images, fonts, prompts, names or folders from elsewhere. What is missing comes from this project's own sources or from the user.
4. **Examples here are samples.** Every name, date, place or line used as an example in this skill is invented sample data. Do not carry it into the work.
5. **Improve the skill, not a memory of one project.** When a lesson would help any project, propose it to the user as a general rule with no project names in it.

Adapted from scenario-labs/skills, MIT (see `LICENSE-scenario.txt`).

Every grade here is math the agent writes, measures and tunes; no generative model touches the pixels. Per-pixel color operations
bake into a 33-point `.cube` LUT that ffmpeg applies. Spatial operations (relight, keyed or masked selective color) run per frame in
numpy before the LUT. Results are exact, identical on every frame and editable: the same LUT loads in Resolve, Premiere and After
Effects. Framing, motion and frame count are kept, so a seamless loop stays seamless and a graded clip drops back into the cut at the
same length.

New footage is out of scope: this skill only grades what already exists. Paths below are relative to this skill's folder.

## Where it sits in our pipeline

- **One look across a series.** Generated clips from separate runs drift in color (one warmer, one milky, one greener). Grade them
  all with the same look file after generation so the series reads as one film. `style-lock-guard` locks the look at prompt time and
  measures drift; this skill corrects what still drifted, in post, without regenerating.
- **Match a clip to the approved key frame.** When a video model returns a clip whose color left the approved still (from
  `keyframe-chain-builder` or the storyboard), run `match.py` against that still and apply the `match` look.
- **Hand off to the NLE.** Deliver `renders/luts/*.cube` so the editor can apply or tweak the same grade in DaVinci Resolve or
  Premiere when the cut is built with `nle-timeline-assembly` or `davinci-series-assembly`.
- **Check after.** Contact-sheet the graded frames with `frame-qc-contact-sheet`, and run `render-cut-verification` on the final
  encode.

## Setup: ffmpeg + a Python venv

The scripts need `ffmpeg`/`ffprobe` on the PATH and Python with **numpy, scipy and Pillow**. If the system Python's numpy is broken
or missing (a wrong-architecture wheel is common on Apple Silicon), make a venv once and run every script with its python:

```
python3 -m venv venv_grade
venv_grade/bin/pip install numpy scipy pillow
venv_grade/bin/python scripts/render_looks.py ...
```

Keep the venv outside the project and outside this skill folder. Each script prints its usage when run without arguments, refuses to
overwrite outputs without `--force`, and makes no network calls.

## Quick reference

- [render_looks.py](scripts/render_looks.py): applies looks to a video (one mp4 per look, audio copied) or to one frame (PNG stills
  plus a labeled `grid.jpg`), and writes `luts/<key>.cube` for each look.
- [inspect_frame.py](scripts/inspect_frame.py): `grid` (pixel coordinates), `sample` (hue, saturation and brightness percentiles of
  rectangles), `key` (red overlay of what a selective key keeps, with blob sizes).
- [match.py](scripts/match.py): measures a reference image for the `match` op, a Reinhard transfer in CIE Lab.
- [showreel.py](scripts/showreel.py): a reel of every look, with a typed name panel, wipes on one continuous clip, a grid finale, and
  an optional end card and music.
- [grade.py](scripts/grade.py), [spatial.py](scripts/spatial.py), [media.py](scripts/media.py): the color ops and LUT writer,
  relight and keying, ffmpeg I/O. The scripts above import them.
- [looks_library.json](assets/looks_library.json): 21 tuned starting looks, including day-for-night, keyed black and white, a
  reference match and four relight presets.
- [looks.json](examples/looks.json): twelve tuned looks, with mask-based black and white plus one color.
- [ops.md](references/ops.md), [looks.md](references/looks.md), [keying.md](references/keying.md),
  [relight.md](references/relight.md): every op, how each library look is built, keys and masks, relighting.

## Steps

1. **Look at the source.** `ffprobe` it and pull three or four frames from different moments. Note whether it is log (milky, flat),
   normal, or already graded. The library looks were tuned on a soft, slightly desaturated source; on a contrasty or already
   stylized one (most generated clips), cut saturation and contrast by about a third. Note the light direction and the key objects'
   colors.
2. **Set up `looks.json`.** Copy `assets/looks_library.json` or `examples/looks.json` next to the clip, then keep, rename, add or
   delete looks. A look holds `name` and `settings` (the reel's two label lines), optional `relight`, optional `selective`, `ops`
   (baked into the LUT), and optional `vignette`, `grain` and `halation`. They apply in that order. Keys sort the outputs; keys
   starting with `_` are notes. For a series, keep ONE looks file in the project and grade every clip from it.
3. **Still test before any video.**
   `python3 scripts/render_looks.py clip.mp4 --looks looks.json --out still_test --frame 40`, then open `grid.jpg`. Check that every
   look differs from the source, none clips or turns skin orange, and skin stays believable outside the stylized looks. Iterate here:
   a still takes seconds, a render minutes. Test two frames on a moving clip.
4. **Keyed looks: measure, then preview.** `inspect_frame.py grid` for full-resolution coordinates (the still-test `grid.jpg` tiles
   are downscaled), `sample` on the object and on what shares its color (skin, lips, ground), then `key ... --frame 10 90 160` for
   the overlay: red on a gray frame marks what is kept. The separating dimension is often brightness or saturation, not hue. For an
   exact result, use object masks (below).
5. **Relight** at 0.3 to 1 stop, from the side that already holds the highlights. It changes light character, never geometry or cast
   shadows: tell the user so.
6. **Match a reference** with
   `python3 scripts/match.py clip.mp4 reference.png match/reference.json [--crop w:h:x:y]`, then use
   `{"op": "match", "stats": "match/reference.json"}` (the path resolves next to the looks file). Use the approved key frame as the
   reference when matching a generated clip back to it. Re-measure whenever the source changes. Matching the same kind of scene at
   another hour is a convincing time-of-day change.
7. **Log footage.** The `decode_log` op reads Sony S-Log3 only. For other camera log formats, convert to Rec.709 first with the
   camera maker's own LUT (in Resolve or with ffmpeg `lut3d`), then grade the Rec.709 result with a look that drops `decode_log`.
8. **Render** with
   `python3 scripts/render_looks.py clip.mp4 --looks looks.json --out renders [--only k1,k2]`.
   - Pure color looks go straight through ffmpeg.
   - Relit and keyed looks take about 1 to 2 s per 1080p frame together, so run long clips in the background.
   - A look whose mask or match stats are missing is skipped with a message.
   - Verify that each render's frame count equals the source's, and sweep keyed and relit renders for flicker, skin and edges.
9. **Reel (optional)**:
   `python3 scripts/showreel.py --renders renders --looks looks.json --source 00_ungraded --out reel.mp4 --order k1,k2 --music track.mp3`.
   Put a dramatic look (duotone, noir) second or third, and prefer a clip that loops cleanly. The reel normalizes music to about
   -18 LUFS and carries no branding by default. Add an end card only when the user asks, with their own `--credit` text or `--logo`
   (a white transparent PNG). Music must be a track the user may use.
10. **Deliver** the renders, `renders/luts/*.cube` (Resolve: Color page, LUTs; Premiere: Lumetri, Creative, Look), the grid and the
    reel. Name which looks have spatial parts: their LUT alone is only the color, so an editor needs a mask or a relight node too.

## Worked example: black and white with one kept color

1. Make one black/white mask video per object with whatever segmentation or roto tool is at hand (a local video segmenter, a
   Resolve Magic Mask matte export, an NLE roto matte). Mask the exact clip you grade. The mask never changes a pixel.
2. Overlay each mask's outline on two or three full-resolution frames. Its frame count must equal the clip's.
3. Give the look a `selective` block. A mask entry with a `key` keeps only the keyed color inside that object, so the white panels of
   a red pump stay gray:

```json
"selective": {
  "masks": [{"path": "masks/jacket.mp4"},
            {"path": "masks/pump.mp4", "key": {"center": 11, "width": 18, "min_sat": 0.28, "max_val": 0.62}}],
  "weights": [0.3, 0.55, 0.15], "sat": 1.7, "val": 1.05
}
```

4. Still test, then render. To swap the color (red to gold), add `"shift": 34` to the same block.

Without masks, a key alone works when the object's color is not shared by skin or the background; see `references/keying.md`.

## Common mistakes

- **Grading each clip of a series by eye.** Use one looks file for the whole series, and a `match` to the approved key frame when a
  clip drifted, so the result is repeatable.
- **A color key alone for one kept color.** Skin, lips and warm backgrounds share the object's color and turn up colored at the
  edges. Use masks plus a key inside the object whenever the object sits near skin.
- **Hue-only keys.** A teal car reflecting a warm sky has almost no teal pixels, and lips share a red jacket's hue. Separate by
  brightness or saturation, set `min_area`, and preview. If it still leaks, tell the user it needs a mask.
- **Heuristic region masks ("change only the sky").** Hair, columns and motion blur leak through. Offer a graduated filter or a
  reference match instead.
- **One source's tuning on another.** Re-run the still test on every new source; already-stylized generated clips need lighter
  settings than the library defaults.
- **Trademarks as look names.** Keep movie titles and film-stock brands out of public names; use descriptive ones ("Scorched
  Desert", "Vintage Slide").
- **`-shortest` with audio slightly shorter than the video.** ffmpeg drops the last frame and the loop breaks. The scripts avoid it;
  keep it that way in custom commands.
- **Grading alone.** Grading is taste: show grids and short previews, and iterate on what the user points at.
