---
name: ad-reference-edit-library
description: >-
  Turns a folder of reference videos (ads, spec spots, brand films, shorts) into a measured EDIT LIBRARY in one SQLite file:
  every shot with timecodes and a thumbnail (plus a second pass that finds the soft cuts dark scenes hide), contact sheets,
  transition candidates found automatically (whip pans and smear cuts, match cuts, flashes, dips) and confirmed by eye on
  8-frame strips, a transition vocabulary of 16 kinds with an AI-generation recipe for each, edit rhythm per reference (cuts per
  minute, median shot, pace by quarter, cuts landing on audio hits, a rhythm barcode), the edit grammar of each film (structure,
  devices, what we take), shot tags (product, sneakers, hands ...), a browsable LIBRARY.html, and Resolve clip lists for library
  timelines (all transitions by kind, all shots of a tag). Use when the user drops reference ads or links and says "study these
  videos", "build a transitions library", "how often do they cut", "find the transitions", "find all product shots", "what makes
  this edit dynamic", or before reference-rough-cut and before writing dynamic Seedance prompts. Includes scripts/edit_library.py.
user-invocable: true
---

# Ad Reference Edit Library

## This project first (binding)

This skill arrives at every project knowing nothing about it. Before applying any default written below:

1. **Study this project.** Read its brief or script, every file in its references folder (images, video frames, saved prompts and their notes) and the results already approved in it. Say what you see in concrete terms before generating or writing anything.
2. **Learn from this project's results.** After each approved result, add to this project's `LESSONS.md` what was asked, the prompt or setting that produced it and why it worked; after each rejection, what failed and the fix. Read `LESSONS.md` before the next task. For this project it overrides the defaults below.
3. **Stay inside this project.** Never open, copy or imitate material from another project, brand or earlier job: no images, fonts, prompts, names or folders from elsewhere. What is missing comes from this project's own sources or from the user.
4. **Examples here are samples.** Every name, date, place or line used as an example in this skill is invented sample data. Do not carry it into the work.
5. **Improve the skill, not a memory of one project.** When a lesson would help any project, propose it to the user as a general rule with no project names in it.

Reference films are material we study, not material we ship. They stay in `01_REFERENCES/EXTERNAL/` (see `project-scaffold`), and their frames never go to a generator as-is (logos, burnt-in subtitles, real faces).

## Setup

- `ffmpeg` and `ffprobe` on PATH. numpy and Pillow in a venv:
  `python3 -m venv ~/.venvs/edit-library && ~/.venvs/edit-library/bin/pip install numpy pillow`
- `PY=~/.venvs/edit-library/bin/python; L=<this skill>/scripts/edit_library.py`
- Every command: `$PY $L <command> --root <project>`. The database defaults to `<project>/DATABASE/edit_library.db`
  (`--db` for another file), videos to `01_REFERENCES/EXTERNAL/VIDEO`, output to `01_REFERENCES/EXTERNAL/ANALYSIS`.
  Every path stored in the database is relative to the project root.

## Getting the videos

The user's links go into `urls.txt` (one per line). Downloading is the user's job when a site blocks scripts: if `yt-dlp`
answers with a bot or sign-in check, stop and ask the user to download the files into the video folder by hand. Never try
other clients, proxies or cookie extraction to get past the check. File names do not matter: `ingest --urls urls.txt --rename`
matches files to links by YouTube title (oEmbed, no login) and renames them `REFnn_<title>`. It lists links with no file and files
with no link; fix a pair by hand with `link REFnn <url>`. Duplicates (same film twice, lower quality) go to `99_ARCHIVE/duplicates`.
Say the resolution out loud: web copies are often 480p, fine for motion, timing and composition, not for colour or detail stills.

## Workflow

| Step | Command | What to check |
|---|---|---|
| 1 | `init`, `ingest --urls urls.txt --rename` | every link has a file; vertical vs horizontal noted |
| 2 | `cuts` | shot counts look plausible (a 60 s ad with 2 shots means a wrong threshold; `--th 0.2`) |
| 3 | `refine` | adds sub-shots `<id>a, b, c` inside every shot over 4 s: dark scenes hide soft cuts. Parent ids never change, so cut lists stay valid |
| 4 | `sheets`, then LOOK at every sheet | name each film's look and story in one line; set `group REFnn <GROUP>` (style group) |
| 5 | `transitions`, `strips` | candidates + review sheets of 12 strips (`ANALYSIS/transitions/_review_NN.jpg`) |
| 6 | review the sheets, record `verdict` | see the review protocol below |
| 7 | `rhythm` | cuts/min, median shot, pace shape, on-hit %, barcode per film |
| 8 | `grammar REFnn "structure" "devices" "what we take"` | one row per film, written from the sheets and strips |
| 9 | `tag <clip_id> <tag> "note"` | product, sneakers, hands, logo ... whatever the brief needs |
| 10 | `library` | writes `ANALYSIS/LIBRARY.html` and reports missing images (must be 0) |
| 11 | `clips transitions --pool pool.json`, `clips tag:<tag> --pool pool.json` | Resolve clip_infos for library timelines |

Re-running `transitions` keeps every verdict already recorded. `report` prints one-screen totals.

### Review protocol (keeps tokens low)

- Look at review sheets, never at single strips, 12 per image. With more than ~150 candidates, review in score order and stop
  when two sheets in a row add nothing.
- A candidate is TOP when you would copy the move, GOOD when it is usable, NO otherwise (plain cut, end card, title over picture,
  a duplicate of another film's moment).
- Name the KIND by what the frames show, not by the detector type: a WHIP candidate may really be a BODY_WIPE, a MATCH candidate a PUNCH_IN.
- Kinds: PORTAL, SPIN, WHIP_PAN, WHIP (smear cut inside an action), PUSH_IN, OBJECT_WIPE, BODY_WIPE, CAMERA_BLOCK, FLASH, ECHO,
  MATCH_CUT, GRAPHIC_MATCH, PRODUCT_PUSH, PUNCH_IN, GRAPHIC_SLIDE, DISSOLVE. A new kind is allowed; the library lists it at the end.
- The note says what happens in eight words or fewer ("bottle handed out of the painting").
- Before using any shot from a long take, look at its sub-shots: the thumbnail of a 20 s "shot" may show a moment that is not where you cut.

### Reading the rhythm

- `cuts_per_min` and `pct_under_05` say how hard a film cuts; `pace_shape` says how the tempo moves (accelerates, fast middle peak,
  long final hold).
- `cuts_on_onset_pct` is an indication, not proof: dense music makes chance hits common. Under ~30% means the edit follows the
  picture, not the beat. For a real beat grid use `music-beat-grid`.
- The barcode: one bar per shot, wider = longer, taller and red = faster.

## Library timelines in DaVinci Resolve

Import the reference files into a `01_REFERENCES` bin first (`media_pool.safe_import_media`), and write `pool.json`
`{"REF01": "<media pool clip id>", ...}` from the import result. Then `clips transitions --pool pool.json` prints clip_infos
(1 s before and after each TOP/GOOD transition, grouped by kind) and writes an index TSV with the record frame of every item.
Create the timeline with `media_pool.create_timeline_from_clips` (name it `00_LIB_TRANSITIONS`, `if_exists: fail`), check
`timeline.detect_gaps_overlaps` (must be 0), and add one marker per kind at its first record frame from the index. Marker colours
Resolve accepts: Blue, Cyan, Green, Yellow, Red, Pink, Purple, Fuchsia, Rose, Lavender, Sky, Mint, Lemon, Sand, Cocoa, Cream.
Same for `clips tag:product` (`00_SEL_PRODUCTS`). Never delete or overwrite an existing timeline: rename the old one `zz_...`.

## Hand-off

- `reference-rough-cut` builds rough cuts from the shot table, the tags and the transitions of this library.
- `cinema-director-v3` (its `references/ad-transitions-and-pace.md`) turns a chosen transition kind into the exit and entry of two generated clips.
- `video-cut-timecodes` is the frame-exact tool for ONE source clip used in a video-to-video edit; this skill is the overview of many films.
