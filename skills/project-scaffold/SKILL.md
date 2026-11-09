---
name: project-scaffold
description: >-
  Creates the ONE standard folder tree every AI video project starts with, so the other file skills know where things are:
  00_BRIEF, 01_REFERENCES (EXTERNAL / INTERNAL with LOCKED and CANDIDATES / PERSONAL), 02_PROMPTS, 03_GENERATED (+
  GENERATION_LOG.jsonl), 04_EDIT, 05_FINAL_OUTPUTS, 06_DELIVERY, 07_POSTING, 99_ARCHIVE, plus PROJECT.json (name, type,
  aspects, languages, paths), README.md and a BRIEF.md template. Only creates missing folders; never moves, renames or deletes.
  --check audits an existing project: missing folders, loose media in the root, non-English names, folders outside the tree.
  Use at the start of any new project, when the user says "new project", "set up the folders", "project structure", or when an
  old project is a mess and needs a standard layout. Includes scripts/scaffold.py.
user-invocable: true
---

# Project Scaffold

Every file skill in this bundle reads and writes inside the same tree. Make it first; everything else plugs in.

## The tree

```
<Project>/
  PROJECT.json        name, type, aspects, languages, paths used by the other skills
  README.md           what goes where (generated once, then the user's)
  00_BRIEF/BRIEF.md   goal, audience, deliverables (title x aspect x language), platforms, deadline, banned, budget
  01_REFERENCES/
    EXTERNAL/          found material we do not own: look/mood only, never shipped     (reference-library-organizer)
    INTERNAL/{CHARACTERS,LOCATIONS,PROPS,STYLE}/{LOCKED,CANDIDATES}
    PROMPTS/           reference prompts with "why it works" notes
    PERSONAL/          real people's photos/voice: private, indexed in place, never copied out
  02_PROMPTS/          prompts per shot or series
  03_GENERATED/{IMAGES,VIDEO,AUDIO,_rejected}  + GENERATION_LOG.jsonl                   (generation-log)
  04_EDIT/             editor bins and timelines                                         (edit-media-bins)
  05_FINAL_OUTPUTS/    Category/NN-Title/aspect/[LANG]                                   (final-outputs-organizer)
  06_DELIVERY/         YYYY-MM-DD_<target>/ packages                                     (delivery-package)
  07_POSTING/          captions, post texts, thumbnails, published links
  99_ARCHIVE/          superseded and delivered material                                 (versions-and-archive)
```

## Workflow

1. Ask once, in one message, only what is missing: where the project lives (drive/folder), its name, and, if the user knows,
   type, aspects and languages. Follow the user's rule on new projects: always ask whether it is a new project and where the
   folder goes.
2. Create:
   ```
   python3 scripts/scaffold.py --root "<parent folder>" --name "<Project_Name>" --type promo --aspects 16x9,9x16 --langs EN,RU
   ```
   Running it again on an existing project only adds missing folders and updates PROJECT.json fields that were passed.
3. Fill `00_BRIEF/BRIEF.md` from the conversation, especially the deliverables matrix (title x aspect x language): it is
   what `final-outputs-organizer` and `delivery-package` check against.
4. Existing messy project: `python3 scripts/scaffold.py --check "<project>"`, show the report, then propose moving content with
   the matching skill (references → reference-library-organizer, generations → generation-log + edit-media-bins, renders →
   final-outputs-organizer). Moving existing files happens only after the user's yes.

## Rules

- English only for every folder, file name and code (`S01`, `S03a`, `take01`, `16x9`, `EN`). `--check` lists names that are
  not plain ASCII; PERSONAL is excluded from that scan.
- The scaffold never moves or deletes anything. It does not touch folders it did not create.
- Two-digit prefixes keep the stages in production order in any file browser. Do not renumber them per project.
