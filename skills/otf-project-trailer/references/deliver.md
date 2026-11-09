# Compose, render, verify, deliver

## 1. Compose (HyperFrames as a local render engine)

HyperFrames (`npx hyperframes ...`) and ffmpeg are used only as local engines. Do not run vendor update commands, do not sign in
to any account, do not use cloud render or `publish`, and do not pull stock media or catalogs.

1. Read the HyperFrames domain skills for the mechanics: `hyperframes-core` (clips, `<video>` with `data-media-start` for
   source in-points, audio), `hyperframes-animation`, `hyperframes-cli`. This skill owns the story, the pick, timing and
   look; HyperFrames owns composition structure and animation mechanics.
2. Prepare assets into `<run>/composition_<lang>/assets/` (ASCII file names, no spaces):
   - clips conformed to 24 fps and the target size, graded with the project LUT (`video-color-grade`), trimmed with handles;
     ffmpeg writes only into the run folder; source files are inputs only, passed one `-i "<file>"` each, never with `-y`
     on a path that could be a source;
   - stills at native size (never upscaled past 1.4x);
   - the spliced music bed;
   - font files from the glyph-tested pairing;
   - the grain plate if the plan has one.
3. Build the composition from `edit/cuts.json`: every time computed from the beat grid (`phase + n * period`), snapped to
   1/24 s, never typed by hand. Cards are layers over black or over the last hold.
4. Gate:
   - `npx hyperframes check` with zero errors;
   - `npx hyperframes snapshot` at 8-12 times (every beat boundary and every card), and look at every snapshot: wrong shot,
     fallback font, text over a face, a card in the wrong language, a flat or milky frame, anything on the banned list.

## 2. Preview gate

Offer `npx hyperframes preview` (local URL) or a draft render (`-q draft`) for the user to watch. Render the final only on a yes,
or when the user said to just finish.

## 3. Render

Per language and per format:

```
npx hyperframes render -q high -f 24 -o <run>/renders/<slug>_trailer_<lang>_<format>.mp4
```

Then:
- **Share copy encode** (for social upload): H.264, CRF 18, `-preset slow`, `yuv420p`, `+faststart`, audio copied. Never CRF
  27 or `-tune grain`: dark gradients band and grain smears.
- **Poster:** pick the strongest settled frame (usually the peak hold or the title over the last image), extract it at full
  size as `<slug>_trailer_<lang>_<format>.jpg`. For the social copy only, the poster may replace frame 0 (overlay on the first
  frame only, all other frames and timing unchanged), so feeds show it as the thumbnail. The master keeps its real frame 0.

## 4. Verify (gate before delivering)

1. Frame-check contact sheet of the ENCODED file, one frame per shot and card:
   ```
   python3 scripts/frame_check_sheet.py <render.mp4> --cuts <run>/edit/cuts.json --out <run>/qc/<name>_frames.jpg
   ```
   Look at it: shot order matches the plan, every card in the right language and font, no fallback glyph boxes, grade
   consistent, no shot from the rejected list.
2. `render-cut-verification` on the same encoded file, with the cut list:
   `cut_strips.py <render.mp4> --out <run>/qc/<name> --cuts-file <run>/edit/cuts.json --expect-duration <length>`.
   Look at every strip and the opening sheet; write `VERIFY.md` (measured / looked at / listened / open limits).
3. Check stream facts: 24 fps, size per format, audio and video lengths equal, loudness about -14 LUFS, true peak at or
   below -1 dBTP.
4. Language purity: the other script appears nowhere in the frames of a version.

Any fix goes back to the composition and renders to a NEW file name; re-verify. Never overwrite the file being checked.

## 5. Share copy (per language)

Write `<run>/share/share_<lang>.md`:

```markdown
Title: <the trailer's title line, as on the card>
Description: <1-2 lines in the tone's voice: the promise, then the release line>
Hashtags: <5-8: project and series name, genre, period or place, and craft tags such as AIFilm, AIFilmmaking,
GenerativeVideo, AICinema, the image and video tools only if the user wants them named>
Thumbnail: <poster file>
```

Rules: the user's own claims and words; no "excited to share"; no plot past the midpoint; no "Part N/M"; no handles or links
the user did not give. Translate, do not transliterate, hashtags where a native tag exists.

## 6. Optional: NLE hand-off

When the user wants to finish in an editor, convert `edit/cuts.json` into the `cutplan.json` of `nle-timeline-assembly`
(source path, `src_in`/`src_out`, `record_in`, transition, motion, marker = beat name) and let that skill build the
timeline in DaVinci Resolve or Premiere, or export an EDL. Hand over the graded clips, the LUT, the music bed, the title
cards rendered as PNG or ProRes 4444 with alpha, and the plan.

## 7. Output layout

```
<project>/trailer/<YYYY-MM-DD-HHMM>/
  TRAILER_PLAN.md            plan, beats, pick (relative source paths), approvals
  GENERATION_REQUESTS.md     only when shots were missing
  material/                  material.csv, material.json, contact_sheet.jpg, rejected_sheet.jpg
  audio/                     track, spliced bed, MUSIC_SOURCE.txt, grid.json
  edit/cuts.json             the cut list
  composition_<lang>/        one HyperFrames project per language
  renders/                   <slug>_trailer_<lang>_<format>.mp4 (+ .jpg poster, + _share.mp4)
  qc/                        frame-check sheets, cut strips, VERIFY.md per render
  share/share_<lang>.md
```

## 8. Report to the user

Paths of every render and its poster; the beat list with timestamps; which shots came from where (relative paths); requests
still open; assumptions; anything not fixed; the share copy inline when it is short.
