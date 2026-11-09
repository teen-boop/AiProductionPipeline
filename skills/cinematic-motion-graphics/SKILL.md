---
name: cinematic-motion-graphics
description: >-
  Motion graphics for cinema and documentary: graphics that live INSIDE the film's look (its palette, grain, halation, deep blacks,
  24 fps pacing) instead of a SaaS or social-media look. The cinematic / documentary category set that motion-graphics-director routes
  to. Nine categories: period map with an animated route (era-correct names, ink line, ship marker, date per stop, vector or baked
  raster lane), date / time / place stamps and countdown clocks, archival press headline and telegram reveals, documentary lower
  thirds and name cards for historical persons, fact and stat cards (letterpress count-up, ledger tables, to-scale silhouettes),
  timelines / chronologies, blueprint and technical-drawing animation, title / chapter / end cards, and composite overlays on footage
  (tracked callouts, text behind subject, grade-matched). Runs brief -> category -> JSON shot plan -> assets -> code build (HyperFrames
  HTML + GSAP or Remotion, rendered locally) -> verify (spec lint, frame snapshots, contact sheet, legibility, safe areas, alpha check)
  -> approve -> render (MP4, ProRes 4444 or WebM alpha) -> NLE hand-off. Every period graphic carries a verified accuracy line; no
  on-screen word without the user's approval. Use when the user asks for an "animated map with the route", "voyage map", "route
  animation", "date stamp", "time and place title", "countdown clock", "documentary lower third", "name card", "newspaper headline
  animation", "telegram reveal", "fact card", "stat in film look", "timeline graphic", "chronology", "blueprint animation",
  "technical drawing animation", "title card", "chapter card", "end card", "callout over footage", "graphics for the documentary",
  "make the graphics look like the film".
---

# Cinematic Motion Graphics

A documentary graphic is a shot of the film, not a widget laid on top of it. It shares the film's blacks, grain, light and tempo,
it says only what the user approved, and every period claim it makes has a source. This skill holds the nine cinematic categories,
the film-look rules they share, one JSON shot plan, and a verify gate. Builds are code (exact text, exact numbers, exact dates);
video models are used only for moving plates, and only after the user says yes.

## Where it sits in the pipeline

`motion-graphics-director` decides CODE vs VIDEO per shot. When the project is a film, a documentary or a period series, it hands
the shot here; this skill picks the category, writes the spec and builds on the CODE route. It reuses, never duplicates:

| Need | Skill (by name) |
|---|---|
| Route decision, 46-block prompt library, board effects | `motion-graphics-director` |
| Style pack (ten slots) derived from the film; the blueprint pack | `motion-style-core` |
| Reference intake, STYLE vs ASSET split | `motion-design-references` |
| Remotion build (alternative engine), exact-numbers doctrine | `motion-remotion-build` |
| Moving plate from a video model (only with the user's yes) | `motion-video-route` |
| Generated newspaper / document stills | `press-clipping-engine` |
| The film's look lock; lint and compare generated plates | `style-lock-guard` |
| LUT, frame inspection, grade match of overlays | `video-color-grade` |
| Title behind a person | `text-behind-subject` |
| Dates, names, places, liveries, numbers | `period-fact-check` |
| Font glyph test (Cyrillic) | `otf-presentations` (font check of its context script) |
| Encoded-file check, NLE hand-off | `render-cut-verification`, `nle-timeline-assembly` |

## Hard rules

1. **The film owns the look.** Palette, black level, grain, halation and contrast come from the project's `STYLE_LOCK.json` or style
   card, read before any design. Deep blacks, never flat grey; highlights never pure white. Details: `references/film-look.md`.
2. **No unapproved words.** Every on-screen string is listed in the spec with `"approved": true` from the user. Spelling, case and
   language are part of the approval.
3. **Accuracy line on every period graphic.** Run `period-fact-check`; each claim gets a source. A pending claim blocks the final
   render. Never invent a headline, a quote, a number or a place name and present it as real.
4. **24 fps** unless the timeline demands otherwise (then say why in `fps_reason`).
5. **Readable holds.** About 3 words per second, never under 1.5 s fully readable, after the entrance ends. Cinema eases, no
   overshoot. Details: `references/motion-timing.md`.
6. **Fonts tested, not guessed.** Local `@font-face` files only; glyph-tested for every script on screen (Cyrillic when the project
   language needs it). One language per render.
7. **Safe areas** for 16:9 and 9:16 are designed per aspect, not cropped.
8. **Assets:** only the project's own material or assets generated through the pipeline route after the user's yes. No stock
   catalogs, no remote URLs at render time.
9. **Local engines only.** HyperFrames CLI, Remotion and ffmpeg run on this machine. No vendor skill auto-update, no sign-in, no
   cloud render, no publish.

## Categories

Pick one per shot. Each file has intent, when to use, layout and motion rules, film-look rules, a spec example and QC.

| id | Use it for | File |
|---|---|---|
| `period-map` | a voyage or route on an era-correct map | `references/categories/period-map.md` |
| `date-stamp` | "14 April 1912, 23:40", place lines, clocks, countdowns | `references/categories/date-stamp.md` |
| `press-headline` | newspaper, telegram, document reveal | `references/categories/press-headline.md` |
| `lower-third` | name, role and years of a person | `references/categories/lower-third.md` |
| `fact-card` | a number, a ledger, a to-scale comparison | `references/categories/fact-card.md` |
| `timeline` | an era chronology with events and photos | `references/categories/timeline.md` |
| `blueprint` | hull plans, sections, schematics drawn in | `references/categories/blueprint.md` |
| `title-card` | episode, chapter and end cards | `references/categories/title-card.md` |
| `composite-overlay` | callouts and type over footage | `references/categories/composite-overlay.md` |

Ambiguous between two? Ask one question. A shot that needs two categories is two specs layered on one timeline.

## Workflow

| # | Phase | Output | Gate |
|---|---|---|---|
| 1 | Brief | narration beat, purpose, aspect(s), language(s) | the user's words, not ours |
| 2 | Category | one id from the table | one question at most |
| 3 | Spec | `motion/<shot-id>/shot-plan.json` | `spec_lint.py` passes |
| 4 | Assets | project files or approved generations | user's yes before any paid call |
| 5 | Build | `motion/<shot-id>/index.html` (or a Remotion comp) | engine lint clean |
| 6 | Verify | snapshots, contact sheet, alpha and legibility checks | looked at, not assumed |
| 7 | Approve | preview + one question: "render, or what changes?" | explicit "render" |
| 8 | Render | `renders/<shot-id>_<lang>_<aspect>.mov` / `.mp4` | probe matches the spec |
| 9 | Hand-off | file + record-in on the cut plan | `nle-timeline-assembly` |

**1 Brief.** Read the script or VO line the graphic lands on, the project's `STYLE_LOCK.json` / style card / `STYLE-PACK.md`, and the
language plan. Ask only what is missing, in one message.

**3 Spec.** Fill the shot plan (`references/shot-plan.md`; full examples in `assets/examples/period-map-1912.json` and
`assets/examples/date-stamp-1912.json`). List every word, its timing and its approval; the accuracy list; fonts with glyph-test
results; assets with origin. Then:

```bash
python3 <skill>/scripts/spec_lint.py motion/<shot-id>/shot-plan.json
```

**4 Assets.** Use what the project has (scans, plates, approved frames, traced vectors). A missing plate is generated only through
the project's route (`press-clipping-engine`, `cinematic-prompt-writer` + `style-lock-guard`, `motion-video-route`) and only after
the user's yes; record `"user_approved": true` in the spec. Generated plates carry no lettering: all text is set in code.

**5 Build.** Start from the category file and, for stamps, `assets/templates/date-stamp.html`. Copy it to `motion/<shot-id>/index.html`
(do not scaffold with a command that installs or updates skills). For a period map, project the route first:

```bash
python3 <skill>/scripts/route_overlay.py motion/<shot-id>/shot-plan.json -o motion/<shot-id>/route-coords.json
```

Engine contract, determinism rules, Remotion settings and ffmpeg recipes: `references/build-and-render.md`.

**6 Verify.** In order, each one looked at:
1. `spec_lint.py` again (texts may have changed during the build).
2. `npx hyperframes lint` and `npx hyperframes check` in the shot folder (an overlay that fades in from nothing will warn
   `first_frame_empty`; that is expected for overlays only).
3. `npx hyperframes snapshot --at <qc.snapshots_at>` with `guides` on: opening, each arrival or reveal, the hold, the exit.
4. Composite one snapshot over the real plate frame (ffmpeg recipe in `references/build-and-render.md`) and read it at phone size.
5. Generated plates: `style-lock-guard` compare against the lock.

**7 Approve.** Show the contact sheet and the preview. Ask once: "render, or what changes?" Never render on silence.

**8 Render.** First `spec_lint.py --final` (every accuracy line verified). One file per language and aspect. Probe it (fps, frame count, size, `yuva` pixel format for alpha). For alpha, measure
a frame where nothing should be visible: alpha must be 0 everywhere (a full-frame grain or vignette inside an overlay lays a grey
veil over the footage).

**9 Hand-off.** Give `nle-timeline-assembly` the file, its track (V2 and up for overlays) and its `record_in`. After the cut is
exported, `render-cut-verification` checks the graphic on the encoded film.

## Project layout

```
<project>/
  STYLE_LOCK.json  STYLE-PACK.md            the film's look (inherited, never redefined here)
  motion/<shot-id>/
    shot-plan.json  route-coords.json       spec, projected route (maps only)
    index.html  fonts/  plates/             build, local fonts, frozen plates
    qc/  renders/                           snapshots, contact sheets, final files
```

## Resume

| State | Continue at |
|---|---|
| no `shot-plan.json` | 1-3 |
| spec lint fails | 3 (fix spec, ask for approvals) |
| spec passes, assets missing | 4 |
| no `index.html` | 5 |
| build exists, no contact sheet in `qc/` | 6 |
| verified, not approved | 7 |
| approved, no render | 8 |
| render exists | probe, then 9 |

## Files

- `references/film-look.md` - global film-look rules: tone, grain, halation, type, safe areas, language, banned SaaS tells.
- `references/motion-timing.md` - cinema eases, read time, holds, VO sync, the primitive vocabulary.
- `references/shot-plan.md` - the JSON shot plan, field by field.
- `references/build-and-render.md` - engine contract, scaffolding, verify and render commands, alpha and ffmpeg recipes.
- `references/categories/*.md` - the nine categories.
- `scripts/spec_lint.py` - lints a shot plan (approvals, read time, safe areas, accuracy, fonts, assets, fps, export).
- `scripts/route_overlay.py` - projects a route (vector projection or georeferenced raster plate) into per-leg SVG paths and stop timings.
- `assets/templates/date-stamp.html` - working HyperFrames composition: typewriter date, settling clock, ledger rule, place line,
  deterministic grain; alpha-ready.
- `assets/examples/period-map-1912.json`, `assets/examples/date-stamp-1912.json` - complete shot plans.
