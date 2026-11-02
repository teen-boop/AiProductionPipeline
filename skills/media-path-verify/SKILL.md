---
name: media-path-verify
description: >-
  Before any export, assembly, hand-off or batch that reads media from disk, checks that every referenced file is really there on
  the REAL drive: finds missing files, external drives that remounted under a new name ("MyDrive" became "MyDrive 1"), and
  "phantom" volume folders (a leftover /Volumes/<name> folder on the boot disk that holds a stale or partial copy while the real
  drive is unplugged). Suggests relinks but never applies one without the user's yes, and never deletes a phantom folder that holds
  files. Reads plain path lists, JSON (cut plans, takes_index.json, pipeline configs), FCPXML/XML/EDL and HTML compositions. Use when
  the user says "media offline", "clips are red in the timeline", "the drive was unplugged", "files not found", before
  nle-timeline-assembly / davinci-series-assembly / animation-handoff-folder exports, or when a project lives on an external drive.
  Includes scripts/verify_media.py.
user-invocable: true
---

# Media Path Verify

Projects in this pipeline usually live on an external drive. An exported timeline that points at files the editor cannot reach
imports as offline media, and a phantom `/Volumes/<name>` folder makes a plain "does it exist?" check lie.

## 1. Run the check

```
python3 scripts/verify_media.py edit/cutplan.json takes_library/takes_index.json --json edit/media_check.json
```

Any mix of inputs works: media paths, JSON, text lists, `.fcpxml`, `.xml`, `.edl`, `.html`. Exit code 0 = all ok.

## 2. Read the statuses

- `ok`: the file exists, and its volume is a real mount.
- `missing`: not found. Usually the drive is unplugged or remounted under a new name.
- `phantom`: the path resolves, but `/Volumes/<name>` is a plain folder on the boot disk. Do not export against it: those files
  may be an old or partial copy.

## 3. Fix missing files

1. Ask the user to plug in or remount the drive, then re-run the check.
2. If the script prints `SUGGESTED RELINK /Volumes/X -> /Volumes/X 1`, show it to the user and ask:
   "The drive came back as 'X 1'. Point this project at 'X 1'?" Only after a yes:
   ```
   python3 scripts/verify_media.py --rewrite "/Volumes/X" "/Volumes/X 1" --from edit/cutplan.json --to edit/cutplan.relinked.json
   ```
   The rewrite always goes to a NEW file. Re-run the check on that file before using it.
3. Still missing: list the files and ask where they are. Do not guess a look-alike file.

## 4. Fix a phantom volume

The clean fix is: eject the real drive, remove the leftover folder, remount so the drive gets its own name back. Before suggesting
that, look inside the folder (the script prints how many entries it holds). If it holds files, they may be work that was saved
there while the drive was away: tell the user and let them decide. Never delete it yourself.

## 5. Then continue

Only when the check exits 0, run the export or assembly. Planning (cut lists, selects, prompts) does not need the drive; only the
step that reads the media does, so run this check right before that step, not at the start of the session.

## Never

- Never relink automatically, and never edit the original plan file in place; rewrites go to a new file after a yes.
- Never delete a phantom folder or any file it holds.
- Never export or assemble while any path is missing or phantom.
- Never substitute a similarly named file for a missing one.
