---
name: nle-timeline-assembly
description: >-
  NLE-agnostic rough-cut assembly. Turns a shot list or cut list (per-shot clip, source in/out, track, transition, small motion,
  marker, music/VO levels and ducking windows) into ONE validated cut plan (cutplan.json), then builds it in whichever editor is
  available: DaVinci Resolve through the DaVinci Resolve MCP, Adobe Premiere Pro through the Premiere Pro MCP, or no MCP at all via
  CMX3600 EDL + marker/notes CSV that both editors import. Inspect first, build in a NEW named timeline, read back after every change,
  stop on any failure. Use when the user says "cut it together", "build the rough cut", "put the shots on the timeline with these
  in/out points", "assemble in Premiere", "assemble in DaVinci", "export an EDL", "give me something I can import", or after the
  video clips of a shot list are generated. For back-to-back finished parts with one marker each, use davinci-series-assembly.
user-invocable: true
---

# NLE Timeline Assembly

## This project first (binding)

This skill arrives at every project knowing nothing about it. Before applying any default written below:

1. **Study this project.** Read its brief or script, every file in its references folder (images, video frames, saved prompts and their notes) and the results already approved in it. Say what you see in concrete terms before generating or writing anything.
2. **Learn from this project's results.** After each approved result, add to this project's `LESSONS.md` what was asked, the prompt or setting that produced it and why it worked; after each rejection, what failed and the fix. Read `LESSONS.md` before the next task. For this project it overrides the defaults below.
3. **Stay inside this project.** Never open, copy or imitate material from another project, brand or earlier job: no images, fonts, prompts, names or folders from elsewhere. What is missing comes from this project's own sources or from the user.
4. **Examples here are samples.** Every name, date, place or line used as an example in this skill is invented sample data. Do not carry it into the work.
5. **Improve the skill, not a memory of one project.** When a lesson would help any project, propose it to the user as a general rule with no project names in it.

`davinci-series-assembly` lays finished parts end to end. This skill cuts a real edit: each shot trimmed to its own source range,
placed on its own track, with transitions, small motion, markers and a ducked music bed. The plan is written once and can be built
in Resolve, in Premiere, or exported as files, so the editor is a backend, not the method.

## 1. Gather the inputs (read only)

1. The shot order: from `seedance-shotlist-tracker`, the storyboard, the user's list, or `video-cut-timecodes` blocks.
2. The files: absolute paths of the accepted clips (`ANIMATION/` hand-off folder or `generated/`). Never pick a rejected take
   (`_rejected_*`).
3. Probe every clip: `ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,duration -of json <file>`.
   All clips on one timeline must share frame rate and size. If one differs, say so and conform or re-render it first. Never let the
   editor retime silently.
4. Ask once, in one message, only what is missing:
   - "Which editor: DaVinci (MCP), Premiere (MCP), or files to import (EDL)?"
   - "Timeline name and frame rate?" (default: `<project> rough <YYYY-MM-DD>`, the clips' rate)
   - "Music or voice-over to lay under it, and at what level?"

## 2. Write the cut plan

Write `edit/cutplan.json` (schema in `scripts/cutplan_to_edl.py`). One entry per shot:

```json
{"id": "S07", "file": "/abs/ANIMATION/S07/S07_take2.mp4", "src_in": 0.42, "src_out": 3.92, "track": "V1",
 "transition_after": {"type": "cut"}, "motion": {"type": "push_in", "from": 1.0, "to": 1.06},
 "marker": "S07 - she opens the letter"}
```

Rules for the plan:
- Times are in seconds and are snapped to the frame grid by the script. Trim the first 6-12 frames of AI clips when they start on a
  frozen or morphing frame; trim the tail where motion degrades.
- `record_in: null` butts the clip against the previous one on its track. Give an explicit `record_in` only for overlays and audio.
- Transitions: hard cuts by default. A dissolve only where the story needs time to pass. Follow the project's rhythm guide
  (`otf-presentations/references/EDIT_PATTERNS.md`) for pace and scale alternation.
- Motion: small and motivated (push-in or pull-out of 3-8 %). Never animate a shot the video model already moves.
- Audio: music bed with `base_db` (about -18 dB under voice) and `duck` windows `[start, end, ducked_db]` in record seconds.

Plan files and versions:
- Anything a script or an agent proposes is a candidate: `edit/cutplan.candidate.json`. Only the user's approval copies it to
  `edit/cutplan.json`.
- The previous approved plan goes to `edit/history/cutplan.<YYYYMMDD-HHMMSS>.json` first.
- Write through a temp file plus rename, never in place.
- Never load a candidate into an open editor session that the user is working in.

Frame grid and sound edges:
- Snap the picture `src_in` down and `src_out` up to the frame grid, so a shot never loses its own last frame or word.
- Dialogue and any clip with speech keep exact audio edges (`audio_in`/`audio_out` from `dialogue-audio-finish`) on a split or
  separate audio track, with room tone under the gap.
- Never trim a speaking clip on a round number by eye. Run `dialogue-audio-finish/scripts/edge_qa.py plan` on the plan first.

Validate and export (this also produces the file route):

```
python3 scripts/cutplan_to_edl.py edit/cutplan.json --out edit/export
```

It fails on overlaps, missing files, reversed or out-of-range source times. Fix the plan, never the report. Read `report.txt`
(gaps, totals) before building anything.

## 3. Build it (pick one backend)

### A. DaVinci Resolve (DaVinci Resolve MCP)

1. `project_manager get_current`. Work in the project the user named or the current one; never create, load or close another.
2. `media_pool add_subfolder` -> `<project>/rough/<YYYY-MM-DD>`; import the plan's files with `safe_import_media`
   (`dry_run: true` first, then `false`). Map clip IDs back to file names; never rely on import order.
3. Create a NEW timeline (`if_exists: "version"`), set to the plan's frame rate. Never append into the user's cut unasked.
4. Place each event with its source range and record frame (the MCP's append-with-clip-info action: start frame, end frame, record
   frame, track index; read the action schema first, do not guess field names).
5. Markers from `markers.csv` (`timeline_markers add`). Transitions, motion and levels from `notes.csv`, only where the MCP exposes
   them; list the rest for the user as "apply by hand: ..." with timecodes.
6. Read back: `probe_timeline_structure` and `detect_gaps_overlaps` must match `report.txt` (event count per track, order, total).
7. `project_manager save`.

### B. Adobe Premiere Pro (Premiere Pro MCP)

1. `verify_premiere_connection` first. If it fails or says the user must act, pass the message on word for word and STOP. Do not call
   any editing tool against a closed bridge.
2. Most tools are hidden: find them with `search_tools` (e.g. "import media", "add to timeline batch", "trim clip", "add transition",
   "keyframe", "marker", "ducking"), read the schema with `get_tool_schema`, run them with `invoke_tool`. Never invent tool names.
3. Inspect: project info, sequences, items. `import_media` the plan's files and keep the returned item IDs.
4. New sequence: `create_sequence_from_clips` (settings from the media) or `duplicate_sequence` with `clearContents: true`. Do not
   create a blank sequence without a real `.sqpreset`; Premiere may open a dialog that blocks the bridge.
5. Place the events (batch add), trim to source ranges, add transitions, Scale keyframes for push-ins, markers, and music ducking
   from the `duck` windows.
6. Read back the sequence after each step with the narrowest list/get tool. Any `success: false` is a stop: report the exact error,
   re-inspect, never retry blindly.
7. Save only after the user agrees; offer `export_as_fcp_xml` as a portable copy.
8. Privacy note for the user: that MCP sends anonymous usage telemetry by default; opt out with `PREMIERE_MCP_TELEMETRY=0`.

### C. No MCP: files to import

Hand over `edit/export/`:
- `<name>_V1.edl`, `<name>_A2.edl` ... one per track. Import in Resolve (File > Import > Timeline, choose the media folder) or
  Premiere (File > Import), one EDL per track.
- `markers.csv` and `notes.csv`: everything an EDL cannot carry (markers, dissolves, motion, levels, ducking), with timecodes.
- Say plainly: "The EDL carries cuts only. Dissolves, push-ins and ducking are listed in notes.csv with timecodes."

## 4. Verify and report

- The built timeline has the same event count, order and total length as `report.txt` (within one frame per event).
- Watch the joins: extract the frame on each side of every cut (`ffmpeg -ss <t> -frames:v 1`) on a contact sheet
  (`frame-qc-contact-sheet`). Look for a flash frame, a duplicated frame, or a jump in the middle of a dissolve.
- Report: timeline/sequence name, backend, table of `id | record TC | duration | marker`, and the list of "apply by hand" items.
- When the cut goes to another editor or another person, write `edit/HANDOFF.md` with these fields:
  - project and plan version, with the sha256 of `cutplan.json`;
  - the approved dialogue/VO WAV and its sha256 (the only narration; nobody reprocesses it);
  - the source folders and relink notes: files are matched by name plus byte size, and absolute paths are never stored;
  - the EDL/XML files;
  - captions and word timings of the final export;
  - graphics renders and their timeline JSON;
  - canvas, fps and camera placement;
  - known issues;
  - approvals (cut, graphics, final, publication), each `pending` until the user signs it off.

## Never

- Never edit, overwrite or delete the user's existing timelines, sequences, bins or projects. New, named, versioned only.
- Never call editing tools before the connection check passes, and never retry a failed call without re-inspecting state.
- Never report "done" without the read-back matching the plan.
- Never let the editor conform a mismatched frame rate or size silently.
- Never run raw script-execution tools (ExtendScript eval, DOM inspect) unless the user explicitly asks for that exact operation.
- Never export over an existing file, and never save over the project without the user's yes.
