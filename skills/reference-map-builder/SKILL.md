---
name: reference-map-builder
description: Find references for a specific task (an ad, a promo, a film scene) and build one REFERENCE MAP that every later stage reads - which reference controls the look, which the camera and edit, which the type and title animation, which the hero, location and props - built first from the project's own approved frames and reference library, then topped up with current trends and the season (holiday, summer, launch season). Writes REFERENCE_MAP.md with a role line per reference and renders a labelled contact sheet. Use before scripting or generating a new ad or promo, when asked "find references", "what should this look like", "build a mood board", "what is trending now", "make it seasonal", or when frames look generic. Triggers - reference map, find references, mood board, trend references, seasonal look, reference roles.
---

# Reference map builder

## This project first (binding)

1. **Study this project.** Read the brief or script, `LESSONS.md`, the approved frames and the reference library before searching anywhere else. Approved frames outrank anything found online.
2. **Learn from results.** Every approval or rejection of a reference goes to `LESSONS.md` with the reason.
3. **Stay inside this project.** Use this project's folders and the links the research found for this task; never copy references from another project.
4. **Examples are samples.**

## What a reference map holds

Every task gets ONE map with these rows. Each reference has exactly one ROLE, written as a line the generator will read.

| Row | Controls | Typical source | Role line |
|---|---|---|---|
| LOOK | colour, light, contrast, grain, depth | the project's approved frames first | "look only: colour, light, contrast; never its content" |
| CAMERA | angle, lens, framing, move | stills from real commercials and films | "camera only: angle, lens, framing; never its people, place, text" |
| EDIT | cut rhythm, transitions, pace shape | reference videos with measured stats | "edit only: rhythm and transitions" |
| TYPE | fonts, kinetic title moves | trend research, seasonal campaigns | "type only: font, size, motion" |
| HERO | face, body, wardrobe | approved hero card | "identity: keep exactly" |
| LOCATION | room, plan, state | location card | "place: same room, same light state" |
| PROPS | shape, material, wear | prop cards | "object: same design" |
| TREND | what is current this season | trend research with dates | "inspiration only" |
| SEASON | seasonal cues (light, colour, props, wording) | calendar + research | "season cues only" |

## Workflow

1. **Task line.** One sentence: who the ad is for, what it sells, length, format, season.
2. **Mine the project.** List approved frames and their look; pick LOOK refs from them. Pull CAMERA and EDIT refs from the project's reference library (stills by shot id, edit stats, transition list).
3. **Search outward (lean).** 5 to 10 web searches: current award and viral ads in the task's category, seasonal campaigns, type trends. Keep real links and dates. Never invent a link.
4. **Season.** Name the season and 3 to 5 cues (light, colour accents, props, wording) that fit the approved look without breaking it.
5. **Write the map.** `REFERENCE_MAP.md` in the task folder: task line, one table row per reference (id, path or link, row, role line, why), then gaps (rows with no reference yet).
6. **Render the sheet.** Fill `map.json` (rows with local image paths) and run `python3 scripts/ref_map_sheet.py map.json out.jpg`: a labelled contact sheet grouped by row, for the user's approval.
7. **Approve before generating.** Show the sheet; generation uses only approved rows. Hand the map to `preproduction-setup-check` (cards and refs per scene).

## map.json shape

```json
{"task": "one sentence", "rows": {"LOOK": [{"path": "frames/F007.jpg", "role": "look only", "why": "amber lamp vs teal"}], "CAMERA": [...]}}
```
