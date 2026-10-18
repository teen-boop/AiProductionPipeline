---
name: segment-reference-lock
description: >-
  For a video-to-video edit prompt built on timecode blocks: assigns the references (characters, location, props) to EVERY block — either
  AUTOMATICALLY (by looking at the block's frames and the reference images) or MANUALLY (the user picks) — and automatically writes a
  LOOK LOCK line into every block from the confirmed reference descriptions, or from the scene's base details when a block has no image
  reference, so faces, wardrobe, location and grade stay stable from block to block. Also carries each block's MOTION and VOICE line.
  Use after video-cut-timecodes and before assembling a Seedance 2.5 Edit / Higgsfield / Kling video-to-video prompt, or when an edit
  drifts (wrong outfit, swapped characters, changed room) in some shots.
user-invocable: true
---

# Segment Reference Lock

The model reads a long prompt unevenly. A description that appears only once, in the mapping at the top, holds in the first shots and
fades later. Restating the look **inside every block** keeps the image stable for the whole clip. The restatement uses the same words
every time, because changing the wording changes the result.

## Inputs

- `segments.json` — the confirmed blocks from `video-cut-timecodes`.
- **REFS** — one entry per attached reference image with its tag (`@img-N`, in the user's upload order), its kind
  (character / location / prop / grade) and a one-line **look** description.
  - Write the look from what you SEE in the image: face, hair, every visible garment, colours and materials.
  - Show the list to the user and have it confirmed **before** anything else. Images pasted into chat have no names, and guessing which
    image is which character swaps outfits.
- **BASE details** (optional) — for things in the scene that have no image reference: named locations, wardrobe by character name,
  props, light and grade. Take them from the project's continuity sheet (`scene-continuity-lock`) or the script breakdown, never invent
  them.

## 1. Assign references to blocks — ask: automatic or manual

Ask ONE question (in the user's language) with two options:

**Automatic.** For each block, look at the first, middle and last frames of the block (`segments_sheet.jpg` from
`video-cut-timecodes`), and decide:
- which characters are visible, and who is who (by position, size and costume in the source);
- which location the block is in;
- which props are in frame;
- the framing (wide / medium / close / over-the-shoulder / point-of-view);
- the eye line of each character: where they look; "never into the lens" unless it is a point-of-view shot.

Then show the result as a table (block | time | framing | references | eyes) and let the user correct single cells.

**Manual.** Show the empty table (block | time) and let the user fill in the references per block, for example "3: @img-1, @img-5,
@img-7". Fill in framing and eyes from the frames yourself, and mark them as yours.

Write the confirmed table to `assign.json`:
```json
{"3": {"refs": ["@img-1","@img-2"], "framing": "medium two-shot in the cabin",
       "eyes": "Andrews looks down at his notebook, never into the lens",
       "base_location": "cabin", "base_chars": [], "base_props": ["chair"]}}
```

## 2. Voice per block

- The default is the ORIGINAL voice: the same words, intonation and timing as the source, with lips in sync.
- If the user wants new or changed words, ASK them for the exact text, who says it, and in which block. Never write dialogue yourself.
  Put it in `voice.json`: `{"3": {"mode": "new", "speaker": "@img-1", "text": "…"}}`. A block that must be silent gets
  `{"mode": "silent"}`.
- New words must fit the block's length. Allow about 2.5 words per second, and warn the user if the text is longer.

## 3. Build the blocks

```
python3 scripts/segment_blocks.py segments.json refs.json assign.json --base base.json --voice voice.json --video @vid-1 --out blocks.txt
```

Every block comes out as:
```
[10.1-15.1 s] BLOCK 3 — medium two-shot in the cabin; Andrews (@img-1), the stewardess (@img-2).
MOTION: exactly as in @vid-1 10.1-15.1 s — the same body movement, gestures, facial expressions, eye direction, camera move, framing and timing; nothing added, nothing re-described.
EYES: Andrews looks down at his notebook, never into the lens.
VOICE: the original voice, words, intonation and timing of @vid-1 10.1-15.1 s, lips in sync; no new words.
LOOK LOCK: Andrews (@img-1): …; the stewardess (@img-2): …; location: exactly as in @vid-1 in this range; light and grade: ….
```

The script stops with an error if any block has no assignment. Fix that first (automatically or manually).

## Rules

- A look description is written once, confirmed, then **copied verbatim** into every block. Never paraphrase it per block.
- A location reference transfers the look only, never its layout. The layout and camera angle always come from the source video.
- A block with no reference and no base detail for a location gets "exactly as in the source". The script never invents a place.
- If the user changes a reference image, rebuild all blocks. Do not patch some of them.
- Props that carry over between blocks or parts keep the same words and an explicit state ("the black folding chair, now knocked over").
