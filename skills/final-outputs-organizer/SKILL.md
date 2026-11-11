---
name: final-outputs-organizer
description: >-
  Gathers every FINISHED video of a project into one predictable tree:
  FINAL_OUTPUTS/<Category>/<NN>-<Title>/<aspect>/[<LANG>]/<file> (for example
  FINAL_OUTPUTS/Tutorials/02-Step_Minis_13s/9x16/RU/…). Category comes from the source folder (Tutorials, Promos,
  Long_Videos, Commercials…); NN is a stable order number that never changes once given; aspect (16x9, 9x16, 1x1, 4x5…) is
  measured with ffprobe, never guessed from the name; a language folder is added only when a title exists in more than one
  language. Dry run first: writes an editable plan CSV, copies only after the user's yes, never overwrites, never deletes, skips
  _previous / tmp / test / QC / working files and exact duplicates, and writes INDEX.md + _manifest.csv. Use when the user says
  "organize the final videos", "put all finals in one place", "sort by aspect ratio / language", "where is the 9x16 RU version",
  "final outputs folder", after a batch of renders is delivered, or before sharing/uploading a project's videos.
  Includes scripts/organize_finals.py.
user-invocable: true
---

# Final Outputs Organizer

## This project first (binding)

This skill arrives at every project knowing nothing about it. Before applying any default written below:

1. **Study this project.** Read its brief or script, every file in its references folder (images, video frames, saved prompts and their notes) and the results already approved in it. Say what you see in concrete terms before generating or writing anything.
2. **Learn from this project's results.** After each approved result, add to this project's `LESSONS.md` what was asked, the prompt or setting that produced it and why it worked; after each rejection, what failed and the fix. Read `LESSONS.md` before the next task. For this project it overrides the defaults below.
3. **Stay inside this project.** Never open, copy or imitate material from another project, brand or earlier job: no images, fonts, prompts, names or folders from elsewhere. What is missing comes from this project's own sources or from the user.
4. **Examples here are samples.** Every name, date, place or line used as an example in this skill is invented sample data. Do not carry it into the work.
5. **Improve the skill, not a memory of one project.** When a lesson would help any project, propose it to the user as a general rule with no project names in it.

Renders end up scattered: `renders/`, `promo-9x16/`, `tutorials/EN/…`, dated export folders. Anyone who later needs
"the 1x1 Russian version of tutorial 2" should find it by walking one tree, without opening a single file.

## The tree

```
<project root>/          (05_FINAL_OUTPUTS/ in projects made by project-scaffold)
  FINAL_OUTPUTS/
    INDEX.md                    every item and file, regenerated on each apply
    _plan.csv                   last plan (editable)
    _manifest.csv               source -> destination of everything copied
    Tutorials/
      01-Full_Tutorial/
        16x9/EN/…  16x9/RU/…  9x16/EN/…  9x16/RU/…
      02-Step_Minis_13s/
        1x1/EN/…   9x16/RU/…
    Promos/
      01-Launch_Teaser/16x9/…
      02-Feature_Promos_8s/9x16/01_first-feature_8s_9x16.mp4
    Long_Videos/
      01-Orchard_Main_Film/…
```

Order of levels is fixed: **Category → NN-Title → aspect → language (only if needed) → file.**

- **Category**: a plain name, no number (`Tutorials`, `Promos`, `Long_Videos`, `Commercials`, `Portfolio`). Taken from the
  first folder under the source, with a leading number stripped (`2_Tutorials` → `Tutorials`), or forced with `DIR=Category`.
- **NN-Title**: one video, or one series of related videos (`01-Tutorial`, `03-Promo_Rise`, `01-Long_Video`). `NN` is
  two digits. Leading numbers in the source (`S03_`, `Video1_`, `02_`) set the order and are removed from the title. Numbers
  already present in FINAL_OUTPUTS are kept forever, so links and posts that cite "Promos/04" stay valid. New titles get the
  next free number.
- **aspect**: measured from the pixels (rotation tag respected), nearest of 16x9, 9x16, 1x1, 4x5, 5x4, 4x3, 3x4, 21x9, 2x1
  within 4 %. Anything else shows as `other_WxH`. Never trust `_9x16` in a filename: the probe wins.
- **language**: from a folder named `EN`/`RU`/… or an uppercase token in the filename (`_RU_`, `-EN.`), or a lowercase one
  only as the final suffix (`video_ru.mp4`). Lowercase words like "it" in the middle of a name are never read as a language.
  The folder appears only when the title exists in two or more languages (`--always-lang` forces it).
- **file**: the original filename, cleaned of unsafe characters. Two different files with the same destination get `__2`.

## Workflow

1. **Ask only what you cannot read from disk**, in one message: the project root, and which folders hold finished videos.
   Never treat raw generations (Seedance/Kling takes, frames) as finals: those belong to `edit-media-bins`.
2. **Dry run** (changes nothing on disk except writing the plan):
   ```
   python3 scripts/organize_finals.py --root "<project>" \
     --src "<project>/renders" \
     --src "<project>/tutorials=Tutorials" \
     --src "<project>/shorts_8s=Promos/Feature_Promos_8s"      # whole folder = one series
   ```
   `DIR=Category` forces the category. `DIR=Category/Title` makes the whole folder one title (a series), otherwise every
   subfolder becomes its own title.
3. **Show the user the summary**, not the CSV: one line per `Category/NN-Title` with its aspect/language counts, plus every
   `CHECK` line (conflicts, odd aspects) and how many files were skipped and why. Point out titles that look like raw clips
   rather than finals.
4. **Let the user correct it.** Edits go into `FINAL_OUTPUTS/_plan.csv`: change `category`, `order`, `title`, `lang`, or set
   `status` to `skip`. Re-run with `--from-plan` to re-check. Do not hand-edit `dest`; it is recomputed.
5. **Apply only after a clear yes:**
   ```
   python3 scripts/organize_finals.py --root "<project>" --from-plan "<project>/FINAL_OUTPUTS/_plan.csv" --apply
   ```
   Copies by default; the originals stay where they are. `--move` only when the user explicitly asks to move. Re-running is
   safe: identical files report `same`, nothing is copied twice.
6. **Report**: number copied, the INDEX.md path, and any `conflict` rows (a different file already sits at the destination;
   it was not overwritten, so the user decides which one is final).

## Status values in the plan

| status | meaning |
|---|---|
| `new` | will be copied |
| `same` | identical file already at the destination |
| `conflict` | a different file is at the destination; nothing is overwritten |
| `dup` | same content as another source file (size + first/last MiB hash); only the first is kept |
| `skip` | path contains `_previous`, `tmp`, `test`, `qc`, `working`, `frames`, `draft`, `wip`, `backup`, `archive`, `proxy`, or starts with `_`/`.`; use `--include-skipped` to take them |

## Rules

- Never delete or overwrite anything, in the sources or in FINAL_OUTPUTS. Replacing a final is the user's call: they move
  the old file to `_previous/` themselves, or tell you to.
- New version of a final (re-render with a fix): same title, same number, same folder. The old file goes to a `_previous`
  folder next to it, only on the user's yes.
- After apply, if the project posts or links to videos, use paths from INDEX.md, never from the scattered sources.
- External drive: run `media-path-verify` first if the sources live on a drive that was unplugged or renamed.

## Related skills

- `edit-media-bins`: raw generated material grouped for the edit (before the final exists).
- `animation-handoff-folder`: final frames + prompts for hand animation.
- `davinci-series-assembly`, `nle-timeline-assembly`: build timelines from finals or bins.
