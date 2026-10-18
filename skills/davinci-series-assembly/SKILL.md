---
name: davinci-series-assembly
description: >-
  Assembles a SERIES of finished clips (presentation parts, block reels, episode segments — e.g. OTF_part1 … OTF_partN) into a DaVinci
  Resolve timeline in the right order, through the DaVinci Resolve MCP: probes and validates the clips (fps, size, duration, audio),
  imports them into a dated Media Pool folder, creates a NEW timeline (never overwrites or deletes an existing one), places the clips
  back to back, adds a named marker at every part, verifies the result (item count, gaps/overlaps, total length) and saves the project.
  Also writes a concatenated preview master with ffmpeg. Use when the user says "put it on the timeline", "edit it together", "assemble in
  DaVinci", "lay the parts out", or after a multi-part presentation is rendered.
user-invocable: true
---

# DaVinci Series Assembly

## 1. Prepare and validate (local, free)

```
python3 scripts/series_manifest.py <out>/series.json part1.mp4 part2.mp4 … [--sort] \
  --titles "Part 1 — …|Part 2 — …|…" --master <out>/series_master.mp4
```

- The clips stay in the order given. `--sort` orders them naturally by name, so part2 comes before part10.
- The script FAILS on mixed frame rates or sizes. Re-render the odd clip or conform it first. Never let Resolve silently retime it.
- Each clip's record start (seconds and frames) becomes its marker position.
- `series_master.mp4` is a stream-copied concatenation. Watch the joins in it before touching Resolve.

## 1b. Match the timeline frame rate first

Read the target timeline's rate (`timeline get_setting timelineFrameRate`). If the clips differ, re-render them at that rate before
assembling, and do not let Resolve drop or repeat frames. Use the user's existing timeline if they named one (append to its end),
otherwise create a new one.

## 2. Resolve: project and media

Use the DaVinci Resolve MCP tools.

1. `project_manager get_current`. Use the project the user named, or the current one. Never create, load or close another project
   without asking, and never delete one.
2. Create the Media Pool folder:
   `media_pool add_subfolder` → `<Series name>/<YYYY-MM-DD>`, then `set_current_folder` to it.
3. Import the clips:
   `media_pool safe_import_media {paths:[…in order…], target_folder:"…", dry_run:true}`, then run it again with `dry_run:false`.
   Map each returned clip ID back to its file name. Do not rely on import order.

## 3. Build the timeline

1. Create the timeline from the clip IDs in series order:
   `media_pool create_timeline_from_clips {name:"<Series name> <date>", clip_ids:[…], if_exists:"version"}`.
   - `if_exists: version` means an existing timeline with that name is never replaced; a new version is made instead.
   - Make sure the timeline frame rate matches the clips. If the project rate differs, tell the user. Do not change project settings
     unasked.
2. Add markers: `timeline_markers add {frame: record_start_frame, name: "<title>", color: "Blue", note: "<file>"}`, one per part.

Marker colors Resolve accepts: Blue, Cyan, Green, Yellow, Red, Pink, Purple, Fuchsia, Rose, Lavender, Sky, Mint, Lemon, Sand, Cocoa,
Cream. There is no "Orange". For a bilingual or multi-series reel, give each series and language its own colour (e.g. RU pipeline Blue,
RU presentations Purple, EN pipeline Green, EN presentations Cyan), and prefix every marker name with the language: "RU · …", "EN · …".

When the user asks to redo an existing assembly on a NAMED timeline:
1. Remove only the old items and markers that this skill placed there; the MCP archives a version first.
2. Append the new series.
Never touch anything else on that timeline.

## 4. Verify (never report "done" without this)

- `timeline probe_timeline_structure` must show:
  - item count = number of clips on V1 (and on A1 if they have audio);
  - items in the right order;
  - each item's duration matching `series.json`.
- `timeline detect_gaps_overlaps` must report no gaps and no overlaps.
- The timeline end minus its start equals the series total, within one frame per clip.
- `project_manager save`.
- Report to the user:
  - the timeline name;
  - the folder;
  - a table with part, start timecode, duration and title;
  - the path of the preview master.

## Rules

- **Never delete or overwrite** timelines, clips, folders or projects. Use only creating and versioning actions. Destructive MCP
  actions are off-limits unless the user asks for that exact deletion.
- Do not move the user's other timelines or change the current timeline's contents. Work only in the new timeline.
- Paths with spaces and Cyrillic are fine for Resolve. Still pass absolute paths.
- If a part is re-rendered later, import the new file and create a new timeline version. Do not swap media under an existing timeline
  silently.
