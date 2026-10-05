---
name: seedance-prompt-writer
description: >-
  Writes production-grade Seedance 2.0/2.5 video prompts on a locked 16-slot
  spine (header, style prefix, no-on-screen-text, CRITICAL blocks, assets,
  geometry map, first frame, FOV-degree optics, camera, action timing,
  physics chain, acting, audio, locks), merged with this project's
  mandatory rules: NO MUSIC, English-by-default, every prompt fully
  standalone (no citations to other clips), percentage-based color doctrine
  tied to a physical source, and shot-size reasoning from
  storyboard-shot-selection. @tags identify which reference image to attach
  and live ONLY in the reference list above the prompt, never inside the
  prompt body - the body uses plain visual descriptors instead. Use
  whenever writing, rewriting, or reviewing a Seedance prompt for this
  project. Triggers on write a seedance prompt, seedance scene, FOV, shot
  blocking, CRITICAL block, physics chain, dialogue protocol, seedance
  formatting, build a shot.
---

# Seedance Prompt Writer (project-merged, v2)

The project's house grammar for Seedance prompts. Merges three sources:
`anthropic-skills:seedance-clean` (block structure, FOV-degree optics),
`cinema-director-v3` (the stricter 16-slot spine, CRITICAL blocks,
percentage color doctrine, physics chain, dialogue protocol, repair-pass
table - this is the dominant structural source now), and this project's own
rules built across `loveart-video-animation`, `storyboard-shot-selection`,
`storyboard-continuity-tracker`, `storyboard-reference-assembly`, and
`video-clip-continuity-chain`.

## Where this sits in the pipeline

Runs at Phase 5 (Video Prompts) of `loveart-project-director`, after the
shot list has been sized (`storyboard-shot-selection`) and
continuity-checked (`storyboard-continuity-tracker` / `video-clip-continuity-chain`).

## STEP ZERO — target version

Before writing anything, establish Seedance 2.0 (≤9 image refs, ≤15s) or
2.5 (≤50 refs, ≤30s). If unstated, ask once in one line. A 2.5-shaped
prompt fed to 2.0 silently drops references and truncates.

## The @tag / no-names resolution (read this before writing ACTIVE REFERENCES)

Two rules from the merged sources look like they conflict and don't:

- `seedance-clean`'s tagging system uses `@tag` to mean "attach this image
  here."
- `cinema-director-v3`'s house rule says **no character names or tags
  anywhere in the prompt body** - visual descriptors only, because names
  and tags drift models.

**Resolution:** `@tags` from this project's canonical registry (below)
identify *which reference image to attach*, and that's all they do. List
them in a **numbered reference list above the code block** (not inside
it). Inside the actual prompt text that gets sent to Seedance, refer to
every character/prop/location by its **visual descriptor**, never by its
tag. `@char_Alice` becomes, in the prompt body, "the young woman with the
black blunt bob and grey-green eyes." The tag tells *you* (and the
attachment UI) what to load; the descriptor is what the model reads.

This also resolves the earlier "context isolation vs continuity chain"
tension from v1 of this skill: `cinema-director-v3`'s own house rule
already states it more sharply than v1 did - **"No internal production
context. No 'carried through from the previous scene,' no 'matching the
earlier plate.' Every prompt is standalone with everything restated
fresh."** Adopt that verbatim. When a shot continues from an
already-written shot, restate the inherited state as plain present-tense
fact (a small ceramic cup sits untouched on the desk) - never as a
citation to a filename, clip number, or "as before."

## Canonical @tag Registry (this project — reference-list only, never in the prompt body)

**Characters:** `@char_Alice`, `@char_cat`, `@char_opossum_v1`

**Wardrobe (3 outfits):** `@wardrobe-morning-home-int` (home), `@prop_wadrobe-ext` (street/7-11, current canon - no uniform change), `@prop_wardrobe-store-int` (uniform, reference only, not in active script)

**Locations:** `@loc_bedrooom_v1`, `@loc_kitchen_v1`, `@loc_living-desk`, `@loc_corridor_v1`, `@loc_store-ext_v1`, `@loc_store-int`

**Props:** `@prop_journal` (sketchbook), `@prop_kettle_v1`, `@prop_email_v1`, `@prop_money-jar`

Resolve anything not listed through `storyboard-reference-assembly` (canon
location plate mandatory) and flag the gap rather than inventing a tag -
the user's asset library expects exact matches.

## Mandatory project rules (layered on top of the spine below)

1. **NO MUSIC** - covered by the spine's own music-suppression tail (slot
   15), which is already stronger than a bare "no music" line. Never trim
   it down to less than the full tail given there.
2. **English by default.** Full prompt in English. Exception: a
   character's actual spoken dialogue or on-screen text the story
   specifically requires, in that language - everything else stays
   English.
3. **Shot-size reasoning carries over from `storyboard-shot-selection`.**
   Fold the established reason (orientation/gesture/action/emotion/object
   contact/detail accent/dialogue/relationship) into the OPTICS choice -
   don't re-derive it, and don't let two adjacent shots collapse to the
   same FOV without a stated reason.
4. **Color fidelity to locked references.** The percentage color doctrine
   (slot 10) must bind its bands to this project's actual locked palette
   for that location/prop, not a generic mood word - this project has a
   documented history of color drifting from references.
5. **Physical in-scene text is a physical object, never on-screen-text.**
   The email screen, the TV ad, a jar label - these are real content that
   exists in the scene and gets described in Assets/Geometry Map with
   shape, color, placement and legibility, same as `cinema-director-v3`
   treats garment prints and signage. The NO ON-SCREEN TEXT block (slot 3)
   still applies to everything else - captions, subtitles, UI, watermarks.

## THE SPINE (locked order — from cinema-director-v3, use as-is)

```
1.  HEADER              shot count · runtime · timecodes · cut policy · speed policy
2.  STYLE PREFIX        invariants — for this project: semi-realistic anime
                        illustration, cinematic lighting, soft painterly
                        rendering, detailed textures (NOT photoreal, NOT
                        3D render, NOT game-cutscene — this project's style
                        IS the illustrated/anime register, so the render-quad
                        negation flips: state what it must NOT collapse into,
                        which is flat/generic AI-illustration mush, not
                        photorealism)
3.  NO ON-SCREEN TEXT   mandatory, always here — see rule 5 above for the
                        physical-text carve-out
4.  CRITICAL BLOCKS     scene-specific, cap 4, ALL-CAPS, ordered by importance
5.  ASSETS              visual descriptor + THIS SCENE action + fidelity
                        assertion — NO @tags inside this block, see resolution above
6.  GEOMETRY MAP        absolute frame position, depth planes, vertical relationship
7.  FIRST FRAME         what's already happening at frame one — kill the
                        empty establishing hold
8.  OPTICS              FOV in degrees per shot, shot-selection reason inline
9.  CAMERA              register (locked-off/gentle/heavy/violent handheld),
                        physicality, per-shot behavior
10. LIGHT & COLOUR      direction/quality/temperature + percentage doctrine,
                        every band bound to a source and to this project's
                        locked palette
11. ATMOSPHERE          air density, depth planes, source-bound vapor only
12. ACTION TIMING       timecoded beats, hard cuts inline, every visible
                        body accounted for every beat
13. PHYSICS             the 7-step chain, scaled to what's actually moving
14. ACTING              brow/forehead matched to the line, eyeline target,
                        emotional arc as a slide not a state
15. AUDIO               diegetic default + full music-suppression tail
                        (NO MUSIC lives here, in full), or dialogue protocol
                        when the scene has real speech
16. LOCKS               positive ordered chain of what must hold across
                        cuts — no restatement of CRITICAL blocks
```

Use only the slots the shot needs; drop the rest. Consult
`cinema-director-v3`'s full text for the mechanics of each slot (FOV
anchor table, camera register table, physics chain detail, dialogue
protocol, repair-pass table) — this skill states only where the project's
own rules override or extend it, above.

## CRITICAL blocks — project-relevant triggers

Cap at 4, ordered by importance, first content in the prompt after Style
Prefix/No-Text. Common ones for this project:

- `THE SCRIPT` — any scene with real dialogue (e.g. the tourist's line in
  Scene 5: "Oh, wow. That's very Hopper...", her "Thank you"). Always the
  first CRITICAL block when present, restated verbatim in AUDIO, and
  restated again inside its Action Timing beat — three times total, this
  overrides the no-repetition rule.
- `NOBODY ELSE IS IN THE FRAME` — the empty-store beats (Scene 4, Scene 6,
  Scene 7) where the model might invent extras.
- `THE GEOMETRY` / `THE STAGING` — any shot where a prop's position must
  not invert or drift (matcha cup's exact desk position, the cat's
  position relative to the sketchbook).
- `TWO DISTINCT DESIGNS` — anywhere the cat and the opossum could get
  confused, or the money jar and any other jar/container in frame.

## Dialogue protocol (for the tourist scene and any future spoken line)

Generated dialogue fails when the script is buried in Action Timing
without being stated up top. Fix: state it twice, plainly, nowhere else in
a competing form.

1. `THE SCRIPT` as the first CRITICAL block — speaker tags (by visual
   descriptor, not name/tag), verbatim lines, in order, silences marked.
2. AUDIO restates the same script verbatim with delivery physics, closes
   with the full music-suppression tail plus "no invented dialogue, no
   substituted phrasing."
3. Action Timing carries the line once more inside its physical beat
   (mic distance, body action bound to it).

Never write phoneme/mouth mechanics for generated dialogue (that's the
lipsync protocol, for attached audio tracks only, not used in this
project's Seedance-generates-its-own-speech scenes).

## Repair pass (project-tuned — check this before the generic one)

| Symptom | Fix |
|---|---|
| A prop (matcha cup, sketchbook) vanishes between clips | Geometry Map / Locks didn't restate its exact position as present-tense fact in the new clip |
| Laptop/door/lid already open when it should still be closed | Action Timing's state-change beat is missing, or Locks didn't say "opens exactly once, at [beat]" |
| Tourist's line doesn't render as scripted, model invents something else | THE SCRIPT isn't the first CRITICAL block, or Audio didn't restate it verbatim |
| Room doesn't match the established location | Canon location plate wasn't in the reference list, or Geometry Map re-described a generic room instead of the locked one |
| Color drifts from the established warm apothecary-kitchen palette | Color doctrine bands aren't bound to this project's actual locked reference — restate the specific palette, not a mood word |
| Cat and opossum blend or swap markings | Promote to a `TWO DISTINCT DESIGNS` CRITICAL block |
| Extra people appear in an empty-store beat | Add `NOBODY ELSE IS IN THE FRAME` as a CRITICAL block |
| Everything else | Fall back to `cinema-director-v3`'s full repair-pass table |

## Checklist (project version)

- Target Seedance version established (2.0 vs 2.5)?
- Style Prefix states the anime-illustration register, not photoreal?
- NO ON-SCREEN TEXT present, with physical in-scene text (screens, jar
  labels) carved out as physical objects elsewhere, not as an exception
  clause inside this block?
- CRITICAL blocks capped at 4, ordered, and THE SCRIPT first when dialogue
  exists?
- Assets use visual descriptors only — zero `@tags` inside the code block?
- Reference list above the code block uses the project's real @tag
  registry, not invented names?
- Every inherited/continuing state is a plain present-tense fact, with no
  "as before," "continuing from," filename, or scene-number anywhere in
  the prompt body?
- OPTICS FOV in degrees, shot-selection reason inline, no adjacent-shot
  collapse?
- Color doctrine in percentage bands, each bound to a physical source and
  to this project's actual locked palette?
- Physics chain present when anything has mass/contact/impact?
- AUDIO carries the full music-suppression tail (not a bare "no music")?
- LOCKS is an ordered positive chain, doesn't restate CRITICAL blocks?
