---
name: manual-image-pack
description: >-
  Hand-generation workflow for image frames — the image counterpart of the
  video-prompt pipeline. When automated generation is slow, blocked or too
  expensive, this skill turns every frame still to be made into a ready-to-use
  folder: PROMPT.txt to copy, the reference images already copied in and
  numbered in attach order, INFO.txt with what/how many/where, and a slot for
  the result (RESULT_1.png …). Then it collects the user's finished frames back
  into the project (format check, auto-crop of thin black bars, correct file
  names in the correct folders), unblocks change-to frames that were waiting for
  them, QCs them by eye, and wires them into the storyboard and the per-frame
  video prompts (with an automatic COLOUR LOCK). Use whenever the user says they
  will generate images themselves/by hand, asks for a folder with prompts and
  references, asks to "collect/take the frames", or drops RESULT files into the
  pack. Triggers on manual generation, generate by hand, prompt + references
  folder, collect the frames, take the frames, place the frames, I generated
  the images.
user-invocable: true
---

# Manual Image Pack

One frame = one folder. The user should only have to open a folder, copy
`PROMPT.txt`, attach `ref_1…`, `ref_2…` in order, generate, and save the result
as `RESULT_1.png` in the same folder. Everything else — prompt writing,
reference choice, naming, placing, QC, storyboard and video-prompt updates — is
this skill's job.

Bundled scripts (Python 3 + Pillow):

- `scripts/build_pack.py` — builds the pack from a jobs JSON.
- `scripts/intake.py` — collects RESULT files into the project and unblocks dependants.

Prompt structure and blocks: `references/prompt-blocks.md`.

## Phase 1 — Build the job list

1. **Collect what is still missing.** Take it from the project's own records,
   in this order: an existing generation queue (jobs JSON) if there is one; the
   storyboard manifest's MISSING / PENDING / FIX slots; the user's latest
   requests ("redo X", "more frames for Y", reference images to recreate).
   Stop all automated generation for these frames first, so the same frame is
   never produced twice.
2. **Write one job per generation** (fields in `build_pack.py`'s docstring):
   `id`, `base` (output prefix), `folder` (destination in the project),
   `prompt`, `refs`, `after`, `section`.
   - Build every prompt from the blocks in `references/prompt-blocks.md`:
     REFERENCES → SCENE → CHARACTER LOCK → domain locks (ship, period,
     night…) → LOOK + OPTICS → FORMAT. The LOOK block is mandatory: it is what
     separates a film still from a glossy AI poster.
   - **References, in attach order:** the location or composition reference
     first, then the identity references for the character at the right age,
     then object or style locks. Write in the prompt what each attached image
     means ("The FIRST attached image is…").
   - **Change-to frames** (close-up, a few seconds later, end frame of a
     first/last pair): the first ref is `@<parent job id>#<n>`. The pack shows
     it as a placeholder until the parent frame exists.
   - **Grade lock (mandatory):** a hand-used app or model will not know the
     series' colours, grain or depth of field. Attach one approved frame of
     the same scene (or same mood) as the LAST ref and add the GRADE LOCK +
     FILM STOCK block (`references/prompt-blocks.md` §5b), with the grade
     described in words, derived from that frame. Change-to frames match
     their start frame instead. Never use a frame that is being redone as the
     grade reference.
   - Ask for 2 variations or 2 different shots per job, never 4+. The user is
     clicking by hand.
   - **One image per prompt.** A model used by hand draws "Image 1 / Image 2"
     requests as ONE split-screen picture. `build_pack.py` therefore splits
     every multi-shot job into PROMPT_1.txt, PROMPT_2.txt … (one standalone
     single-image prompt each, same references → RESULT_1.png, RESULT_2.png …)
     and every prompt forbids split screens, diptychs and side-by-side panels.
   - Keep historical and continuity rules inside the prompt text itself (the
     user will not remember them).
3. **Sections** = the priority order the user should work in. The user's
   newest requests come first, then the climax or missing story beats, then
   gaps, close-ups and identity fixes, then optional extras. Pass them as
   `sections.json` (`[["01_NAME", "^regex_on_id"], …]`).

## Phase 2 — Build the pack

```bash
python3 scripts/build_pack.py --jobs jobs.json --out <PROJECT>/MANUAL_GEN \
  --root <PROJECT> --sections sections.json --lang en --style-file <style template.md>
```

- The pack lives **inside the project** (the user opens it in Finder), never in a temp folder.
- `--lang` sets the language of INFO.txt and README.md (English by default; add a translation table in the script for other languages). Prompts stay in English.
- It refuses to rebuild over a pack that already holds RESULT files. Run intake first.
- Also put the project's style template next to the pack, so the user can write their own frames in the same style.
- Tell the user:
  - the folder path;
  - the sections, in priority order;
  - that a `.txt` in place of a ref means "do the other folder first";
  - to save results as RESULT_1.png in the same folder;
  - to say "collect the frames" when ready.

## Phase 3 — Intake (when the user says the frames are ready)

```bash
python3 scripts/intake.py --pack <PROJECT>/MANUAL_GEN --dry-run   # see what will happen
python3 scripts/intake.py --pack <PROJECT>/MANUAL_GEN
```

Then, for every delivered frame:

1. **QC by eye.** Build a contact sheet and Read it. Check:
   - 16:9, with no bars or rounded borders left;
   - faces match the identity references for that age;
   - domain rules (ship details, period, no anachronisms);
   - no unmotivated bokeh or flares;
   - the frame actually tells the beat.
2. If a frame fails QC, move it to the project folder's `_rejected/` with the reason in the filename. Tell the user why, and give the exact fix to add to that folder's PROMPT.txt. Edit PROMPT.txt yourself if the user agrees.
3. **Wire accepted frames into the project:**
   - add or replace them in the storyboard manifest, in story order (close-ups right after their parent frame);
   - rebuild the storyboard;
   - give every frame a single-start-frame video prompt with small, motivated camera moves. The COLOUR LOCK is derived from the frame itself.
   - Only an end frame that was generated via change-to FROM its start frame may be used as a first+last pair.
4. Report to the user:
   - delivered, accepted and rejected counts;
   - which waiting folders are now unblocked (their placeholder became a real ref image).

## Phase 4 — Keep the pack fresh

After intake, folders that were delivered can stay (they hold `_delivered/`).
If the plan changes (new requests, rejected frames to redo), update the jobs
list. Mark delivered jobs `done` with their `outputs`, so change-to children get
the real start frame copied in, then rebuild the pack.

## Rules

- One frame per job folder, one prompt per folder.
- Never ask the user to look up a reference. Every image they need is already in the folder.
- Never overwrite an existing project frame. Intake takes the next free index, and replacements happen only through the storyboard manifest.
- Keep the API keys of any generation service out of every file in the pack.
- Never auto-delete the user's results. Rejected frames go to `_rejected/`, not the bin.
