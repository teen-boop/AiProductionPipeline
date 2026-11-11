---
name: versions-and-archive
description: >-
  Version, archive and disk-space rules for AI video projects. supersede: a new version of a final or approved file takes
  the exact old path and name (so links, indexes and posts keep working) and the old one goes to _previous/<name>_v01_<date>.
  report: shows where the space goes (_previous, _rejected, editor caches and proxies, temp/partial downloads, duplicate
  content across folders, takes rejected in the generation log but not moved), changing nothing. archive: after delivery,
  copies previous / rejected / delivered / generated material to 99_ARCHIVE or another drive with SHA-256 verification and a
  manifest; sources go to the Finder Trash only on the user's yes and only after every copy verified. Nothing is ever
  hard-deleted. Use when the user says "new version", "replace the final", "keep the old one", "free up space", "the drive is
  full", "archive the project", "clean up", after a delivery, or before moving a project to another drive. Includes
  scripts/versions.py.
user-invocable: true
---

# Versions and Archive

## This project first (binding)

This skill arrives at every project knowing nothing about it. Before applying any default written below:

1. **Study this project.** Read its brief or script, every file in its references folder (images, video frames, saved prompts and their notes) and the results already approved in it. Say what you see in concrete terms before generating or writing anything.
2. **Learn from this project's results.** After each approved result, add to this project's `LESSONS.md` what was asked, the prompt or setting that produced it and why it worked; after each rejection, what failed and the fix. Read `LESSONS.md` before the next task. For this project it overrides the defaults below.
3. **Stay inside this project.** Never open, copy or imitate material from another project, brand or earlier job: no images, fonts, prompts, names or folders from elsewhere. What is missing comes from this project's own sources or from the user.
4. **Examples here are samples.** Every name, date, place or line used as an example in this skill is invented sample data. Do not carry it into the work.
5. **Improve the skill, not a memory of one project.** When a lesson would help any project, propose it to the user as a general rule with no project names in it.

## Version rules

- **Final paths are stable.** A fixed re-render replaces the file at the same path and with the same name. Never put
  `_v2`, `_final_final` or a date into a final's name: version numbers live only in `_previous/`.
- **Old versions go next to the file:** `<dir>/_previous/<stem>_v01_<YYYYMMDD><ext>`, then `_v02`, … Numbers only grow.
- **Takes are not versions.** Raw generations are takes (`S03_take04`); their history is in GENERATION_LOG.jsonl
  (`parent`, `status`). Rejected takes go to `03_GENERATED/_rejected/`.
- Every organizer (final-outputs-organizer, edit-media-bins, reference-library-organizer) skips `_previous` and
  `_rejected`, so old material never leaks into finals, bins or deliveries.

```
python3 scripts/versions.py supersede --target "<final path>" --with "<new render>"           # dry run
python3 scripts/versions.py supersede --target "<final path>" --with "<new render>" --apply   # after the user's yes
```

## Space report (changes nothing)

```
python3 scripts/versions.py report --project "<project>"
```

Show the user the totals per bucket and the biggest items. Read it this way:
- **caches / proxies** (CacheClip, Render Cache, Optimized Media, Proxy, Peak/Media Cache files): the editor rebuilds them.
  The user deletes them from the editor or Finder; offer, do not do it.
- **duplicate content**: same file in several folders. Copies in `04_EDIT` are intended while editing. Copies of the same
  clip inside several render/asset folders (for example `promo-16x9/assets` and `promo-9x16/assets`) are the usual waste:
  suggest one shared assets folder for the next build, do not delete working copies a build still reads.
- **rejected not moved**: offer to move them into `_rejected/`.
- **_previous**: archive candidates once the delivery is accepted.

## Archive after delivery

```
python3 scripts/versions.py archive --project P --what previous [--dest "<archive drive>/ARCHIVE/<Project>"]          # dry run
python3 scripts/versions.py archive --project P --what previous --dest "…" --apply                                        # copy + verify
python3 scripts/versions.py archive --project P --what previous --dest "…" --apply --trash-source                         # + free space
```

`--what`: `previous`, `rejected`, `delivered` (06_DELIVERY), `generated` (all raw takes; only once the project is closed).
Relative paths are kept, so anything can be restored to where it was. ARCHIVE_MANIFEST.csv records source, destination,
size, SHA-256 and the verification result.

## Rules

- No hard deletes, ever. The only removal path is `--trash-source` (Finder Trash, recoverable), only after the user says yes
  to that exact list and only when every copy verified. Never empty the Trash.
- Ask before archiving `generated`: approved takes may still be needed for re-edits; check `generation-log report` first.
- Before archiving to an external drive, run `media-path-verify` on the destination (renamed or phantom volumes).
- Never archive 01_REFERENCES/PERSONAL to a shared or cloud drive.

## Related skills

`final-outputs-organizer`, `edit-media-bins`, `generation-log`, `delivery-package`, `media-path-verify`.
