---
name: storyboard-camera-continuity-ledger
description: >-
  Reads a sequence's narrative/shot list, extracts the camera movement
  within each shot and the transition type between consecutive shots
  (push-in, pull-back, pan, tilt, crane, tracking, whip, match-cut,
  straight cut, etc.), and persists them into a per-project continuity
  ledger file — a small database other work (animation/video prompts,
  editing, future sequences reusing the same locations) can read back
  later instead of re-deriving camera logic from scratch. Also cross-checks
  that image/video prompts written by other skills (`cinematic-prompt-writer`,
  `storyboard-narrative-breakdown`, a project's own Lovart/Seedance prompt
  skill) actually contain the bridging detail the ledger says a transition
  needs. Works in any project — creates its own ledger file if none exists
  yet. Use whenever camera movement or cut logic needs to be tracked,
  reused, or checked across a sequence of shots. Triggers on camera
  movement, track the cuts, continuity ledger, what transition happens
  here, does this prompt have the bridge, camera database.
---

# Storyboard Camera Continuity Ledger

## Why this exists

Camera movement and transition logic ("the camera pushes in on the poster,"
"smoke match-cuts into the train's smoke") is usually only written down once,
inside a paragraph of narrative prose, and then either re-derived from
memory or silently dropped by the time actual prompts get written — twice
over, once for stills and again later for any video/animation pass. This
skill is the place that information gets extracted once, recorded
durably, and then checked against.

It is a **data-and-QC layer**, not a prompt-writing skill — it never writes
image/video prompt text itself; it records what the camera is doing and
verifies other skills' prompts actually reflect it.

## Where this sits relative to other skills

- Runs **alongside** `storyboard-narrative-breakdown` (see that skill's
  "Step 5"): as mini-scenes get segmented and prompted, this skill logs
  their camera action and bridge data into the ledger and flags any prompt
  that's missing its required bridging detail.
- Feeds forward into **video/animation prompt writing** later (e.g.
  `seedance-prompt-writer` or any project-specific video-prompt skill) — the
  camera-movement column is exactly what a video prompt's camera-direction
  section needs, already decided and consistent, instead of reinvented shot
  by shot.
- Distinct from `storyboard-continuity-tracker`, which tracks *physical
  state* of entities (pose, position) shot-to-shot. This skill tracks
  *camera behavior and cut logic* instead — the two are complementary and
  often run on the same sequence.

## The ledger file

One ledger per project. On first use in a project, look for an existing one
at (in order): `continuity/CAMERA_LEDGER.md`, `CAMERA_LEDGER.md` in the
project root, or any file whose name contains "camera" and "ledger"/
"continuity". If none exists, create `continuity/CAMERA_LEDGER.md` in the
project root and say so — don't create a second ledger file if one already
exists under a different name; ask once if it's ambiguous which existing
file is the ledger.

Ledger format — one row per shot, appended in sequence order, never
reordered or deleted (mark superseded rows `[SUPERSEDED]` instead of
removing them, so the history of a sequence's cutting logic stays legible):

```markdown
| # | Sequence | Shot label | Camera movement | Incoming transition | Outgoing transition | Bridge detail | Source |
|---|----------|-----------|------------------|---------------------|---------------------|----------------|--------|
| 1 | opening_montage | City poster | Push-in (fly toward) | none — cold open | Match-cut via poster→window | poster text visible, then reveal window above it | narrative-breakdown 2026-09-06 |
```

- **Camera movement**: the formal term(s) for what the camera does *during*
  this shot (see vocabulary below). Multiple movements in one shot are
  written in order, e.g. "Push-in, then tilt up."
- **Incoming/outgoing transition**: the cut/join type at each end of the
  shot (see vocabulary below).
- **Bridge detail**: the specific visual element that must appear in both
  this shot's prompt and its neighbor's prompt for the transition to
  actually read as continuous (e.g. "chimney smoke, thick grey, rising
  vertically" — specific enough that you could check a generated image
  against it).
- **Source**: which skill/session/date produced this row, so a later
  cross-check knows where to find the corresponding prompt text.

## Camera-movement vocabulary (map source-text phrasing to these terms)

Narrative prose describes camera action colloquially, in whatever language
the source narrative is written — map it to one formal term rather than
logging the raw phrase as-is (log the raw quote too, in the ledger's
Source-adjacent notes, but the Camera-movement column itself must use
these terms so later lookups are consistent):

| Colloquial phrasing (examples) | Formal term |
|---|---|
| camera flies in / pushes in / zooms toward / gets closer | **Push-in** (dolly/fly toward subject) |
| camera pulls back / backs away / retreats | **Pull-back** (dolly/fly away from subject) |
| camera rises / climbs / lifts up | **Tilt-up** or **Crane-up** (use Crane-up if the camera's *position* rises, Tilt-up if it stays put and the lens angle changes) |
| camera lowers / descends / drops down | **Tilt-down** or **Crane-down** |
| camera moves alongside / glides past | **Tracking shot** (lateral move alongside the subject) |
| camera follows (someone/something) | **Follow shot** (tracking, subject-led) |
| camera turns / swings around | **Pan** (horizontal) or **Tilt** (vertical), infer from context |
| camera moves along (a wire/line/edge) | **Tracking shot along a line** — note the guiding element explicitly (e.g. "tracks along telephone wires") |
| hard cut / sharp cut / straight to the next shot | **Straight cut** |
| smoke/dust/object turns into another smoke/dust/object | **Match-cut** — log the shared visual element in Bridge detail |
| smoke/dust morphs into / dissolves into | **Match-dissolve** (if described as a gradual morph rather than an instant cut) |

If a phrase doesn't map cleanly, log your best-fit term and note the
ambiguity rather than inventing a new vocabulary term silently — keep the
vocabulary closed so the ledger stays queryable.

## Process

1. **Identify the sequence** being logged (a name/label — reuse
   `storyboard-narrative-breakdown`'s mini-scene numbering if this is
   running alongside that skill).

2. **For each shot, extract** the camera movement (map to the vocabulary
   above) and the transition at both ends, from the source narrative or shot
   list. If running alongside `storyboard-narrative-breakdown`, this is the
   "Camera action (source text)" field plus the incoming/outgoing bridge
   fields it already extracted — don't re-derive from scratch, reuse its
   segmentation.

3. **Append one row per shot** to the ledger file, in order. Never silently
   overwrite an existing row for a shot that's being revised — append a new
   row and mark the old one `[SUPERSEDED]`, so the ledger keeps a record of
   how the sequence's cutting logic evolved (useful when a later re-edit
   needs to know what changed and why).

4. **Cross-check prompts against the ledger.** For every row with a
   non-empty Bridge detail, find that shot's actual generated prompt text
   (from whichever skill wrote it) and confirm the bridge element is
   described there in a way that matches the row *and* that the neighboring
   shot's prompt describes the same element consistently (same visual
   qualities — don't let one prompt call it "thick black smoke" and the
   next call it "a thin white wisp"). Flag any mismatch immediately, naming
   the exact wording that needs to change, rather than deferring the check
   to generation time when it's more expensive to fix.

5. **When asked to help build an animation/video prompt for an already-
   logged sequence**, read the relevant ledger rows first — the camera
   movement and transition columns are the camera-direction content that
   prompt needs; don't re-derive it from the original narrative again.

## What this skill does NOT do

- Does not write image or video prompt text itself (that's
  `cinematic-prompt-writer` / `storyboard-narrative-breakdown` / the
  project's own video-prompt skill).
- Does not decide shot *size* (that's `storyboard-shot-selection`).
- Does not track character/object physical *state* (that's
  `storyboard-continuity-tracker`).
