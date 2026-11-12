---
name: reference-rough-cut
description: >-
  Builds the reel FIRST from pieces of reference films (an animatic made of real ad footage), so motion, rhythm and transitions
  are decided in the edit before anything is generated: a cut list of library shots (clip id, length, where inside the shot,
  action, transition out, named blocks) becomes a gap-free DaVinci Resolve timeline with block markers, a preview MP4 made straight
  from the reference files, a contact-strip QC, a 9:16 copy when asked, and finally one GENERATION SLOT per shot (length in frames,
  reference clip and time, action, transition in and out) that the video-prompt skills turn into Seedance prompts. Use when the
  user says "cut the reel from the references first", "lay the references on the timeline and start editing", "build an animatic
  from these ads", "make style versions of the reel", "replace this shot", or after ad-reference-edit-library. Includes
  scripts/rough_cut.py.
user-invocable: true
---

# Reference Rough Cut

## This project first (binding)

This skill arrives at every project knowing nothing about it. Before applying any default written below:

1. **Study this project.** Read its brief or script, every file in its references folder (images, video frames, saved prompts and their notes) and the results already approved in it. Say what you see in concrete terms before generating or writing anything.
2. **Learn from this project's results.** After each approved result, add to this project's `LESSONS.md` what was asked, the prompt or setting that produced it and why it worked; after each rejection, what failed and the fix. Read `LESSONS.md` before the next task. For this project it overrides the defaults below.
3. **Stay inside this project.** Never open, copy or imitate material from another project, brand or earlier job: no images, fonts, prompts, names or folders from elsewhere. What is missing comes from this project's own sources or from the user.
4. **Examples here are samples.** Every name, date, place or line used as an example in this skill is invented sample data. Do not carry it into the work.
5. **Improve the skill, not a memory of one project.** When a lesson would help any project, propose it to the user as a general rule with no project names in it.

The rough cut is a plan made of borrowed footage. It never ships: every shot in it is replaced by a generated shot later.

## Needs

- The project's edit library (`ad-reference-edit-library`): tables `reference_videos` and `ref_clips` in `DATABASE/edit_library.db`
  (any database with those two tables works: `--db`).
- `ffmpeg`. DaVinci Resolve through the DaVinci Resolve MCP for the timeline; without it, `nle-timeline-assembly` exports an EDL.
- `R=<this skill>/scripts/rough_cut.py`; every command takes `--root <project>`.

## 1. Write the cut list

`04_EDIT/<REEL>_vNN_cutlist.tsv`, TAB separated, one shot per line:

```
# BLOCK OPEN
REF03_S012	1.6	0.5	face hold, push-in
REF01_S017	0.9	0.5	object handed out of a painting	MATCH_CUT
```

Columns: shot id (a sub-shot id like `REF04_S032d` is fine), seconds, position inside the shot (0 = head, 0.5 = middle,
1 = tail), action in a few words, optional transition out (a kind from the library). `# BLOCK <name>` starts a block; blocks become markers.

How to choose, from the library rather than taste:
- **Pace.** Take the target style's numbers from `edit_stats`: median shot length, share under 0.5 s, pace shape. Copy the shape
  (calm hold, burst, calm hold; or accelerate into a long final hold). A 15 s style piece is 12-18 shots, a showreel blocks of 8-14.
- **Rhymes.** Chain shots by a shared shape, object or motion direction (clock to clock, hand to hand, ball to ball, the product
  passed between worlds). A hard cut between two unrelated shots needs a reason: a beat, a sound, a change of block.
- **Transitions.** Pick TOP/GOOD moves from the library and write their kind in column 5 of the shot BEFORE the transition.
- **Aspect.** For 16:9 use horizontal references; a vertical reference shows pillarbox bars. Flag it, or move that piece to the 9:16 cut.
- **Never** use a shot with burnt-in subtitles, a readable brand name or a recognisable real person as the planned look of a
  generated shot without saying so; it stays a motion reference only.

## 2. Check, build, assemble

1. `python3 $R check <cutlist> --root <project>`: unknown ids stop the run; a line inside a long take that has sub-shots is
   flagged. Look at its sub-shots (or a frame strip) before trusting the position: long dark takes often hold several shots.
2. `python3 $R build <REEL> <cutlist> --pool 04_EDIT/pool.json --root <project> > clip_infos.json`: writes `cut_shots` rows and
   `<cutlist>.blocks.tsv`. `pool.json` maps `REFnn` to the Resolve media pool clip id (from the import result).
3. Resolve: `media_pool.create_timeline_from_clips` with the clip_infos (name `<REEL>_<STYLE>_vNN_ROUGH_16x9`,
   `if_exists: fail`). The script already handles the two traps:
   - `end_frame` is EXCLUSIVE; with `end - 1` every clip comes up one frame short and the timeline shows 1-frame gaps.
   - sources at 25/30 fps on a 24 fps timeline get one spare frame, otherwise rate conform leaves 1-2 frame gaps.
4. `timeline.detect_gaps_overlaps` must report 0 and 0. Add one marker per block from the blocks TSV (frame = record_frame).
5. Never delete or overwrite a timeline: a failed or replaced version is renamed `zz_<name>_old`, the new one gets the clean name.
6. Linked reference audio blocks `replace_source_range`; to change one shot, edit the cut list and rebuild a new version.

**9:16 copy (only when the user wants it now):** `timeline.duplicate` (it moves the current timeline pointer to the copy), then on
the copy `set_setting useCustomSettings 1`, `timelineResolutionWidth 1080`, `timelineResolutionHeight 1920`,
`timelineInputResMismatchBehavior scaleToCrop`. Centre crop cuts wide shots and readouts: list the shots that need reframing.

## 3. Preview and look at it

- `python3 $R preview <cutlist> 04_EDIT/previews/<name>.mp4 --root <project> [--aspect 9x16] [--audio]`: silent by default
  (reference music fights the cut).
- `python3 $R qc <preview.mp4> --root <project>` and LOOK at the strip: every planned moment must be on screen (a position inside
  a long take can land on the wrong moment), no black frames, no burnt-in text you did not plan.
- Send the preview to the user. Write what changed since the last version and what you noticed.

## 4. Slots for generation

`python3 $R slots <REEL> --root <project>` writes `02_PROMPTS/<REEL>/SLOTS.md` and `slots.json`: per shot the length in
seconds and frames, the record time, the reference clip and its in point, the thumbnail, the action and the transition in and
out. Hand it to the video-prompt skills (`cinema-director-v3`, `seedance-prompt-writer`). A slot whose transition is not CUT gets
its exit (clip A) and entry (clip B) written from `cinema-director-v3/references/ad-transitions-and-pace.md`. The rule for every
slot: copy the reference's motion, camera move, timing and composition; never its people, logos, text or exact frames.

## Versions

`v01`, `v02` ... per reel; each version keeps its cut list, timeline and preview. Record the version and status in the `reels`
table and the decision (what the user asked to change) in `LESSONS.md`.
