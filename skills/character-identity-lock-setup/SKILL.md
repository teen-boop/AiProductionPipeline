---
name: character-identity-lock-setup
description: >-
  Builds a locked visual-identity reference system for a recurring character
  — a set of reference images (a multi-panel turnaround sheet plus a
  standalone bust portrait) for every distinct age or life-stage that
  character appears at, generated from real photo identity sources and
  hosted so every later generation can attach the correct one. Prevents a
  character's face from drifting between shots, and prevents an AI image
  generator from ever inventing the face freehand from text alone. Use at
  the start of any project with a recurring character who appears across
  multiple ages, outfits, or a long span of scenes, before generating any
  scene that includes them. Triggers on lock a character's face, age
  reference sheet, turnaround sheet, identity lock, character consistency
  across ages, recurring character reference, keep the face consistent.
---

# Character Identity Lock — Setup

## Why this exists

An AI image generator asked to draw "the same man, but now at 35" from
nothing but a text description will drift — the face changes shot to shot,
sometimes subtly, sometimes not. The fix is not a better prompt; it's a
**locked reference image** for each distinct stage the character appears
at, generated once, reused everywhere. Every later scene generation
attaches the correct reference instead of re-describing the face in words.

This is the setup step that has to happen before any scene-level
generation for that character — build it once per character, then never
touch it again unless the user asks for a redo.

## When this runs

- At the very start of a project that has a recurring character, before
  any scene/shot is generated involving them.
- Whenever a new character is introduced partway through a project.
- Whenever the user asks to redo or add variants for an already-locked
  character's reference set.

## Inputs needed before starting

1. **Real photo identity source(s)** for the character — one or more
   actual photographs (archival, reference, or the user's own) that the
   generated face must be derived from. Never invent a face from a text
   description alone if any real photo source exists or can be supplied —
   ask for one if the character is meant to resemble a real or
   pre-existing person and none has been provided yet.
2. **The list of distinct ages/stages the character needs to exist at.**
   Pull this directly from the script/story, not a generic spread — if the
   narrative only ever shows the character at three specific ages, build
   three sets, not five. Confirm the exact ages/stages with the user if the
   source material is ambiguous about how many are needed.
3. **A wardrobe/context note per age/stage** — what era, role, and
   clothing register the character is in at that point in the story (a
   schoolboy uniform at 11, an apprentice's work clothes at 16, a
   director's suit at 35, etc.). This drives the reference sheet's
   wardrobe description; get it right once here so every downstream scene
   prompt can just say "wearing the locked reference outfit" instead of
   re-describing it.

## What gets generated, per age/stage

**Two assets per age/stage, both attached to the same identity photo
source(s):**

### 1. Turnaround reference sheet

ONE composite image, four panels on a single seamless neutral studio
background, consistent soft even lighting across all four panels (no
dramatic/cinematic lighting here — this is a clean production reference,
not a final shot):
- Panel 1: full body, front view, standing straight, arms relaxed, facing
  camera.
- Panel 2: full body, back view, same pose/outfit, seen from directly
  behind.
- Panel 3: close-up, front view, head and shoulders, calm neutral
  expression.
- Panel 4: close-up, profile view, head and shoulders, exact 90-degree
  side view.

Generate **two variants** per age/stage when the project allows it (e.g. one
full-color, one monochrome/black-and-white) — a genuinely different-looking
pair, not two near-duplicates, so the user has a real choice of which reads
better once dropped into an actual scene, rather than committing to the
first result.

### 2. Standalone bust portrait

One single close portrait — head and shoulders/bust, front-facing or a
very slight three-quarter turn, calm neutral expression, same plain studio
background, full color. This is a separate image from the turnaround
sheet's own close-up panel — it exists because a single strong portrait is
often more useful to reference or show for approval than a panel cropped
out of a four-panel composite.

## Prompt template (reuse verbatim, only swap age/wardrobe per stage)

```
Character turnaround reference sheet — ONE single composite image, four panels arranged left to right on one seamless neutral mid-grey studio background, consistent soft even studio lighting across all four panels (no dramatic cinematic lighting — clean production reference sheet, no lens flare, no heavy grain). [Full color photograph, natural period color palette. / Monochrome grey-tone photograph.]
Panel 1 (full body, front view): standing straight, arms relaxed at sides, facing camera directly, full body head to shoes.
Panel 2 (full body, back view): same person, same pose, same outfit, seen directly from behind.
Panel 3 (close-up, front view): head and shoulders, facing camera, calm neutral expression.
Panel 4 (close-up, profile view): head and shoulders, exact 90-degree side view.
Identity: [attachment(s)] are photograph(s) of [the real person/character description]. Use them strictly as the facial identity source across all four panels: exact bone structure, eye shape, nose shape, mouth shape, brow line, hairline shape, and overall likeness, adapted naturally to age [AGE], [year/era], [age-appropriate build/skin/posture note].
Wardrobe (same in all 4 panels): [wardrobe description for this age/stage].
All four panels must show the exact same person, same outfit, same hairstyle, same lighting. [Full color / Monochrome], photorealistic, not illustrated, not painted, not a drawing[, not black and white].
```

Bust portrait template:
```
A single standalone studio portrait — head and shoulders bust, front-facing with a very slight three-quarter turn, calm neutral expression, on a plain neutral mid-grey studio background, soft even studio lighting, full color photograph.
Identity: [attachment(s)] are photograph(s) of [the real person/character description]. Use them strictly as the facial identity source, adapted naturally to age [AGE], [year/era], [age-appropriate build note]. Wardrobe: [wardrobe description for this age/stage]. Full color, photorealistic, not illustrated, not painted, not a drawing, not black and white.
```

## Process

1. **Gather identity photo source(s) and the age/stage list** (see Inputs
   above) before generating anything.
2. **Write the wardrobe/context note for every age/stage** — one or two
   sentences each, grounded in the actual story, not generic.
3. **Generate both turnaround-sheet variants and the bust portrait for
   each age/stage**, using the templates above, attaching the identity
   photo source(s) every time.
4. **Host every approved result somewhere with a stable, reusable URL**
   (whatever the project's generation platform provides — a CDN upload, an
   asset library, etc.) — a locked reference that only exists as a local
   file with no shareable reference path isn't attachable to future
   generations on most platforms.
5. **Record the full index** — one line per age/stage with its reference
   URL(s) — in a single, obvious, durable project file (a production log,
   a script breakdown, whatever the project already uses as its source of
   truth). Every future scene-generation prompt for this character must
   pull the matching age/stage's URL from this index and attach it
   explicitly. Never let a scene prompt describe the character's face in
   free text as a substitute for attaching the reference.
6. **If the user asks for a redo**, generate new variants alongside the
   old ones (versioned, e.g. a `_v2` suffix) rather than overwriting —
   keep the original until the user has actually picked a replacement.

## Handoff to scene generation

Once the reference index exists, every downstream scene/shot prompt for
this character (written by whatever prompt-writing skill the project
uses) must:
- Attach the correct age/stage's reference URL(s) from the index.
- Never re-describe the character's face from scratch in the prompt text
  — describe expression/action/context, not bone structure, since the
  attached reference already carries that.
