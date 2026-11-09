# Shot plan - the JSON spec

One file per graphic: `motion/<shot-id>/shot-plan.json`. It is the contract between the brief and the build, and the thing the user
approves line by line. Plain JSON (no comments) so `spec_lint.py` and `route_overlay.py` can read it. Complete examples:
`assets/examples/period-map-1912.json`, `assets/examples/date-stamp-1912.json`.

## Envelope (every category)

| Field | Type | Meaning |
|---|---|---|
| `id` | string | shot id from the shot list or cut plan, e.g. `EP01_MG_MAP_01` |
| `category` | string | one of `period-map`, `date-stamp`, `press-headline`, `lower-third`, `fact-card`, `timeline`, `blueprint`, `title-card`, `composite-overlay` |
| `period` | number, optional | the year the graphic depicts; makes the accuracy list mandatory |
| `narration_beat` | string | the VO line and timecode the graphic lands on |
| `fps` | number | 24; anything else needs `fps_reason` |
| `canvas` | object | `{ "w", "h", "aspect" }`; aspect is `16:9`, `9:16`, `1:1`, `4:5` or `2.39:1` |
| `variants` | array, optional | other aspects or languages, each rendered and checked as its own file |
| `duration_s` | number | total length, matching the slot on the cut plan |
| `export` | string | `mp4` (full-frame), `prores4444`, `webm-alpha` or `png-sequence` (alpha overlays) |
| `background` | string | `plate` (the graphic has its own plate) or `transparent` (required for alpha exports) |
| `engine` | string | `hyperframes` or `remotion` |
| `template` | string, optional | the template the build starts from |
| `look` | object | `style_lock`, `style_card` and/or `style_pack` paths, plus `notes` quoting what was read |
| `colour_pipeline` | string, optional | `graded` or `neutral+lut` (see film-look section 4) |

## Words

`texts[]` lists every string that will appear, including labels, dates, units and credits:

| Field | Meaning |
|---|---|
| `id` | stable id, reused as the element id in the build |
| `text` | the exact string, in the render's language and case |
| `font` | a family listed in `fonts` |
| `approved` | `true` only after the user approved this exact string |
| `in_s` | when the entrance starts |
| `enter_s` | how long the entrance takes (typewriter, fade, draw) |
| `hold_s` | how long it stays fully readable after the entrance |
| `box` | optional `[x, y, w, h]` in canvas pixels, checked against the safe area |

## Facts, fonts, assets

- `accuracy[]`: `{ "claim", "source", "status": "pending" | "verified", "note" }`. One line per checkable claim. Required when
  `period` is set or the category is `period-map`, `press-headline`, `timeline` or `blueprint`.
- `fonts[]`: `{ "family", "file", "cyrillic": bool, "glyph_test": "pass" | "fail" | "untested" }`. Cyrillic text needs a font with
  `cyrillic: true` and `glyph_test: "pass"`.
- `assets[]`: `{ "role", "path", "origin": "project" | "generated", "user_approved": bool, "rights": "..." }`. Paths are project-local
  and frozen; generated assets need the user's recorded yes.

## Content (per category)

`content` holds what the category file describes; the main shapes:

| Category | `content` |
|---|---|
| `period-map` | `route { lane, projection, bounds, padding_px, stops[], legs[], control_points[], ship_marker }`, `plate`, `camera` |
| `date-stamp` | `variables { date, time_from, time_to, place, transparent, grain }`, `layout` |
| `press-headline` | `document { kind, plate, headline_area, keyword, source_citation }`, `camera`, `annotation` |
| `lower-third` | `person { name, role, years }`, `position`, `scrim` |
| `fact-card` | `value`, `unit`, `format`, `label`, `ledger_rows[]` or `comparison { items[], scale_px_per_m }` |
| `timeline` | `orientation`, `range`, `events[] { date, label, photo }`, `breaks[]`, `camera` |
| `blueprint` | `drawing { source, layers[] }`, `draw_order[]`, `labels[]`, `dimensions[]` |
| `title-card` | `kind` (episode / chapter / end), `lines[]`, `lockup`, `background` |
| `composite-overlay` | `plate { file, in_s }`, `track { file | points[] }`, `callouts[]`, `depth` |

A route stop: `{ "id", "name", "lon", "lat", "date", "label_side" }`. A leg: `{ "from", "to", "via": [[lon, lat]...],
"densify": "great-circle" | "none", "style": "solid" | "intended" }`. A control point (raster lane):
`{ "lon", "lat", "x", "y" }` read off the plate at full resolution.

## QC

`qc.snapshots_at[]`: proof times (seconds): the first frame, each reveal or arrival, the hold, the exit. The verify step snapshots
these and builds the contact sheet.

## Invariants

- Every visible string is in `texts[]` and approved; nothing appears that is not listed.
- `in_s + enter_s + hold_s` of every text ends inside `duration_s`.
- Alpha exports have `background: transparent`.
- Period graphics have a non-empty accuracy list; the final render waits until every line is `verified`.
- One spec per aspect-language file, or `variants` listing each one with its own boxes.
