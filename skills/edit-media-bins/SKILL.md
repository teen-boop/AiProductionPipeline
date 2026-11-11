---
name: edit-media-bins
description: >-
  Copies a project's GENERATED material (Seedance/Kling/Higgsfield clips with hash names, frames, plates, music, VO, SFX,
  titles, LUTs, cut plans, prompts) into one editor-ready bin tree, EDIT/<Project>/00_TIMELINES, 01_VIDEO/<NN_Shot>,
  02_STILLS/<NN_Shot>, 03_AUDIO/{MUSIC,VO,DIALOGUE,SFX}, 04_GFX, 05_LUTS, 06_DOCS, so the editor imports one folder and the
  bins already match the story order. Groups by shot/scene code (S03, SH010, K07, 01_BRAND), orders groups by the shot list,
  renames hash-named takes to <Shot>_take01_<time>, flags clips whose size/fps differ from the rest, writes EDIT_MANIFEST.csv
  (bin file -> original). The copy is for editing; originals never move. Dry run first, copy after the user's yes, never
  overwrites or deletes, re-runs add only new takes. Use when the user says "prepare for editing", "group the generations",
  "folder for the edit", "copy everything for Premiere/DaVinci", "where are the takes of shot 7", after a generation batch
  lands, or before nle-timeline-assembly. Includes scripts/edit_bins.py.
user-invocable: true
---

# Edit Media Bins

## This project first (binding)

This skill arrives at every project knowing nothing about it. Before applying any default written below:

1. **Study this project.** Read its brief or script, every file in its references folder (images, video frames, saved prompts and their notes) and the results already approved in it. Say what you see in concrete terms before generating or writing anything.
2. **Learn from this project's results.** After each approved result, add to this project's `LESSONS.md` what was asked, the prompt or setting that produced it and why it worked; after each rejection, what failed and the fix. Read `LESSONS.md` before the next task. For this project it overrides the defaults below.
3. **Stay inside this project.** Never open, copy or imitate material from another project, brand or earlier job: no images, fonts, prompts, names or folders from elsewhere. What is missing comes from this project's own sources or from the user.
4. **Examples here are samples.** Every name, date, place or line used as an example in this skill is invented sample data. Do not carry it into the work.
5. **Improve the skill, not a memory of one project.** When a lesson would help any project, propose it to the user as a general rule with no project names in it.

Generation tools drop files named `98d7125d…_690b358e….mp4` into download folders, references sit next to prompts, music is
somewhere else. An editor needs the opposite: one folder, grouped the way the film is cut, every take traceable back to its
source and prompt.

## The tree

```
<project>/04_EDIT/<Project>/      (04_EDIT in projects made by project-scaffold)
  EDIT_MANIFEST.csv         bin file -> source path, size, resolution, fps, duration
  _bins_plan_<Project>.csv  last plan
  00_TIMELINES/             cutplan.json, .edl, .fcpxml, .xml, .drp, .prproj
  01_VIDEO/
    01_S01/  S01_take01_<name>_1102-1145.mp4  S01_take02_…
    02_S02/  …
  02_STILLS/
    01_S01/  start/end frames, keyframes, plates for that shot
  03_AUDIO/ MUSIC/  VO/  DIALOGUE/  SFX/  OTHER/
  04_GFX/                   titles, logos, overlays, lower thirds, alpha renders, .psd/.svg/.aep
  05_LUTS/                  .cube .3dl
  06_DOCS/                  prompts, shot lists, notes
```

- **Group** (the `NN_` folder): from a shot code in the filename or its folders (`S03`, `SC12`, `SH010`, `K07`, `EP2`,
  `A4`), or a leading number + name (`01_BRANDNAME_…` → group `BRANDNAME`, position 1), or the parent folder, or the source folder.
  Force it with `--src DIR=S07`. `--src DIR=GFX` (or LOGO, TITLE, OVERLAY) sends every file from that folder to `04_GFX` instead of a shot group.
- **Group order**: `--order shotlist.txt` (one code per line, in cut order), then leading numbers, then natural sort
  (S2 before S10). The same group number is used in 01_VIDEO and 02_STILLS, so a shot's clips and frames line up.
- **Take names**: `<Group>_take<NN>[_<original name>]_<MMDD-HHMM>.<ext>`. Takes are numbered by an explicit take/version token,
  then by file time. Hash-like original names are dropped; readable ones are kept after the take number.
- **Audio type**: from path words: VO (vo, voice, narration, tts), DIALOGUE (dialogue, lipsync), MUSIC (music, song, track,
  suno, bgm, score), SFX (sfx, foley, whoosh, impact, ambience, room tone).
- Versions of one render (a silent master and the same master with sound) are not takes of a shot: give them separate sources, or keep only the one the timeline uses.
- Skipped: `_previous`, `rejected`, `tmp`, `cache`, `proxy`, `backup`, `trash`, hidden files. Exact duplicates are copied once.

## Workflow

1. **Collect sources** (read only): download folders of the video/image tools, the frames folder, music, VO, the cut plan.
   Ask the user once for anything you cannot find, plus the project name and the shot list if one exists
   (`seedance-shotlist-tracker`, storyboard, `animation-handoff-folder`).
2. **Dry run:**
   ```
   python3 scripts/edit_bins.py --project "<Project>" --edit-root "<project>/04_EDIT" \
     --src "<downloads>/seedance" --src "<project>/frames" --src "<project>/music" \
     --src "<project>/edit" [--src "<dir>=S07"] [--order "<project>/edit/shot_order.txt"]
   ```
3. **Show the user** one line per bin with counts, every `FORMAT … differs` line (a clip at another size or fps will make
   the editor retime or letterbox it: re-render or conform before the cut), and groups named `UNSORTED` or after a random
   folder: offer to force them with `DIR=Group`.
4. **Apply after a yes:** same command plus `--apply`. Default is a real copy. `--link` hard-links instead (same volume only,
   no extra disk space; editing the bin file in place would change the original, so use it only for read-only editing).
5. **Re-run after every new generation batch.** Existing takes report `same`, new ones are added as the next take number.
   Files that are in the bins but come from no source are listed, never deleted.
6. Hand over: the bin root path, and, for building the timeline, `nle-timeline-assembly` (it reads paths from
   EDIT_MANIFEST.csv) or `davinci-series-assembly`.

## Rules

- The bins are a copy. Never edit, trim or re-encode inside the sources; never move or delete a source.
- Never overwrite a file in the bins: a different file at the same name becomes `__2` or is reported as `conflict`.
- Selecting the good take is the editor's job. Do not drop takes; mark rejected ones by moving them to `_rejected/`
  in the SOURCE only when the user says so, then re-run (rejected sources are skipped).
- Keep prompts next to the work: copy each shot's prompt file into `06_DOCS` so a take can be regenerated.
- External drive: run `media-path-verify` before handing the bins to an editor on another machine.

## Related skills

- `final-outputs-organizer`: where the finished renders go after the edit.
- `animation-handoff-folder`: approved frames + prompts for animating (before clips exist).
- `nle-timeline-assembly`, `davinci-series-assembly`: build the edit from these bins.
