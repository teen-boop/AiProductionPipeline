---
name: otf-project-trailer
description: >-
  Cuts a short cinematic TRAILER or TEASER for one of our own projects (a film, an episode, a series, or the AI production
  pipeline itself) from the project's own approved frames and generated clips, never from website code or app screenshots.
  Inventories stills and clips, ranks them by closeness to the project look (style lock, otf-presentations ranking), prefers
  moving clips, flags rejected and unapproved takes, and gets the pick approved on a contact sheet. Picks a cinematic
  structure (full trailer, 15 s teaser, mood piece, documentary trailer with fact cards, series trailer, making-of) with
  timing per beat, writes style-locked generation requests for missing shots (never spends credits without a yes), cuts on a
  measured music grid with flash and dip-to-black devices, sets titles in glyph-tested fonts, keeps the film look of the
  style lock, renders each language as its own 24 fps file, verifies the encoded render, and writes share copy per language.
  Use when the user says "make a trailer", "trailer from our frames", "teaser for the episode", "announce the series",
  "season trailer", "cut a teaser", "15-second teaser", "trailer for the film", "promo cut from our shots", "trailer for
  the pipeline", or wants to show a finished project to filmmakers.
user-invocable: true
---

# OTF Project Trailer

## This project first (binding)

This skill arrives at every project knowing nothing about it. Before applying any default written below:

1. **Study this project.** Read its brief or script, every file in its references folder (images, video frames, saved prompts and their notes) and the results already approved in it. Say what you see in concrete terms before generating or writing anything.
2. **Learn from this project's results.** After each approved result, add to this project's `LESSONS.md` what was asked, the prompt or setting that produced it and why it worked; after each rejection, what failed and the fix. Read `LESSONS.md` before the next task. For this project it overrides the defaults below.
3. **Stay inside this project.** Never open, copy or imitate material from another project, brand or earlier job: no images, fonts, prompts, names or folders from elsewhere. What is missing comes from this project's own sources or from the user.
4. **Examples here are samples.** Every name, date, place or line used as an example in this skill is invented sample data. Do not carry it into the work.
5. **Improve the skill, not a memory of one project.** When a lesson would help any project, propose it to the user as a general rule with no project names in it.

A trailer sells one promise with the project's best real images. This skill finds those images, builds a cinematic structure
around them, asks for anything missing, and cuts it to measured music in the project's own look. It is for film and
documentary makers who work with AI-generated stills and video. For a client's product or brand film use `cinematic-promo-film`;
for a video that explains how something works use `otf-presentations`.

```
chat + project folder (frames, clips, STYLE_LOCK.json, story notes)
   | 1 context + inventory      otf-presentations context, scripts/pick_material.py
   | 2 pick on a contact sheet  ............................ GATE: user approves the pick
   | 3 structure + plan         TRAILER_PLAN.md ............ GATE: user approves the plan
   | 4 missing shots?           GENERATION_REQUESTS.md ..... GATE: yes per request and cost
   | 5 music grid + cut list    music-beat-grid, edit/cuts.json
   | 6 compose per language     HyperFrames (local), check + snapshots
   | 7 render + verify          frame_check_sheet.py, render-cut-verification ... GATE before delivery
   | 8 deliver                  renders, posters, share copy per language, optional NLE timeline
```

## Invocation

Natural language or options. Parse everything before touching files; ask once, in one message, only for what is missing and
cannot be inferred (usually: which project folder, and the release line).

| Option | Values | Default |
|---|---|---|
| project | folder with frames / clips / `STYLE_LOCK.json` / notes | current folder |
| `--structure` | `full`, `teaser`, `mood`, `documentary`, `series`, `making-of` | inferred from the subject |
| `--duration` | seconds | full 30-60 (30 for social), teaser 15 |
| `--format` | `16:9`, `9:16`, `1:1` (several allowed) | `16:9` |
| `--tone` | `epic`, `intimate`, `mystery`, `elegiac`, `documentary`, `kinetic`, or free text | inferred |
| `--lang` | e.g. `en,ru` | the language of the chat + English |
| `--logline` | one line | from the project's notes |
| `--release` | date / platform / "coming soon" | ask |
| `--voice` | voice-over on | off (music only) |
| `--nle` | also build an editor timeline | off |

Free direction ("like an old spy-film trailer") maps to the nearest tone for timing and is kept verbatim in the plan.
Tone details: [references/tones.md](references/tones.md).

## Output folder

`<project>/trailer/<YYYY-MM-DD-HHMM>/`, one per run, never overwriting an earlier run. Layout in
[references/deliver.md](references/deliver.md). Source folders are read-only for the whole run.

## Step 1. Context and inventory

**Read:** [references/selection.md](references/selection.md)

1. From the chat, in the user's words: subject, logline, purpose, audience, languages, formats, length, release line,
   must-show, banned.
2. Run the context step of `otf-presentations` (`otf-presentations/scripts/otf_context.py`) on the project's references,
   frames, clips and style lock: look metrics, palette, embedded source prompts, glyph-tested fonts (`--cyrillic` when a
   version needs it), story docs.
3. Inventory and rank everything:
   `python3 scripts/pick_material.py <project> --out <run>/material --format <fmt>`
   (ranked `material.csv` with relative paths, `contact_sheet.jpg`, `rejected_sheet.jpg`; it reuses the
   `otf-presentations` look score when that skill is installed).

## Step 2. The pick (gate)

Look at the sheets, open the best candidates at full size, run `style-lock-guard compare` on the top stills, fill the
coverage matrix (beat by beat), and show the user the pick sheet in trailer order plus the gaps.
**Gate:** the user approves the pick. Rejected or unapproved takes are used only when the user names them.

## Step 3. Structure and plan (gate)

**Read:** [references/structures.md](references/structures.md), [references/plan-template.md](references/plan-template.md)

Choose the structure, set beat timing for the duration, assign shots to beats, write every on-screen line per language, and
write `<run>/TRAILER_PLAN.md`.
**Gate:** the user approves the plan (or said "just do it": then list assumptions in the final report).

## Step 4. Missing shots (gate, only if needed)

**Read:** [references/missing-shots.md](references/missing-shots.md)

For each real gap write a still prompt and a video prompt that follow the style lock (linted with `style-lock-guard`),
with the route through the project's generation backend (`generation-backend-setup`; manual packs via
`manual-image-pack`) and the cost.
**Gate:** generate nothing until the user says yes to the request and its cost. New results go through QC and back into
the ranking.

## Step 5. Music grid and cut list

**Read:** [references/edit-rules.md](references/edit-rules.md)

Measure the track with `music-beat-grid`, splice it to length on beat boundaries, lock the accent cuts, and write
`<run>/edit/cuts.json` (record times snapped to 24 fps; cards included as entries).

## Step 6. Compose per language

**Read:** [references/deliver.md](references/deliver.md), and the `hyperframes-core` / `hyperframes-cli` skills for mechanics.

One composition folder per language. Clips graded to one look (`video-color-grade`), conformed to 24 fps, trimmed with
handles; titles set in code with the tested fonts; grain and halation on the picture layer only.
**Gate:** `npx hyperframes check` clean, and every snapshot looked at.

## Step 7. Render and verify (gate)

Render each language and format at 24 fps. Then, on the ENCODED file:
`python3 scripts/frame_check_sheet.py <render> --cuts <run>/edit/cuts.json --out <run>/qc/<name>_frames.jpg`,
and `render-cut-verification` with the same cut list, plus `VERIFY.md`.
**Gate:** nothing is delivered until both were looked at and the stream checks pass.

## Step 8. Deliver

Renders, posters, the frame-check sheet, `share/share_<lang>.md` (title, 1-2 line description, hashtags) per language,
optional `nle-timeline-assembly` hand-off. Report paths, beats with timestamps, sources, open requests and assumptions.

## Creative laws

- **Real material only.** Every shot is the project's own approved frame or clip, or a generated shot the user approved.
- **In motion from frame 1.** No logo, no fade-in, no text in the first 1.5 s.
- **One promise.** The trailer sells one question or feeling; no spoilers past the midpoint.
- **Accelerate, break, release.** Shots shorten into the peak, one designed rhythm break, the end is a hold into the title.
- **Hard cuts.** Plus at most two overexposure flashes and the dip-to-black breath; no wipes, spins or glitches.
- **The look is the style lock.** The lock's own blacks, light and palette, and the depth of field and lens
  character of the frames; never a flat grey "film look".
- **Few faces.** About one face shot in three or four.
- **Text small and late.** Titles in glyph-tested fonts, held long enough to read; at most three intertitles.
- **Music only** unless the user asks for voice; SFX only on request.
- **No labels.** No "Part N/M" or "Episode N" over picture, no watermark, no channel bug, no logo slam.

## Never

- Never generate, queue or pay for anything without the user's yes on that request and its cost.
- Never write into source folders; ffmpeg outputs go only into the run folder.
- Never use a rejected take silently, never upscale past 1.4x, never mix scripts in one language version.
- Never run vendor update, sign-in, cloud render or publish commands; HyperFrames and ffmpeg run locally only.
- Never post or upload; delivery means files in the run folder.

## Related skills

`otf-presentations` (context, fonts, rhythm guide), `style-lock-guard`, `frame-qc-contact-sheet`, `frame-crop-guard`,
`music-beat-grid`, `video-color-grade`, `keyframe-chain-builder`, `generation-backend-setup`, `manual-image-pack`,
`period-fact-check`, `render-cut-verification`, `nle-timeline-assembly`, `dialogue-audio-finish` (voice-over only).
`retention-packaging-plan` is for creator formats; do not apply its tricks to a trailer unless the user asks.
