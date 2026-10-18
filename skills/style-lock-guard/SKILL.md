---
name: style-lock-guard
description: >-
  Always-on guard that keeps the director's LOOK from silently disappearing or being overwritten. Locks the look to the director's own
  reference frames and the source prompt embedded in them (e.g. Midjourney/Krea PNG metadata), lints EVERY image prompt before it is
  sent (required style phrases present, no contradicting grade phrases like "no golden hour / desaturated / lifted blacks", the style
  frames attached LAST), gates the generation runner on that lint, and measures every result against the references to catch the
  "flat, grey, mediocre" look (washed-out colour, no warm light accents, milky blacks). Use when starting any image work in a project,
  before sending any prompt (including change-to / keyframe / fix prompts), when the user says a frame "doesn't look cinematic",
  "looks mediocre", "not like the reference", or "the style prompt got lost".
user-invocable: true
---

# Style Lock Guard

## The failure it prevents

A project's style block slowly drifts away from the director's references:
- a "grade" file made from an overcast frame becomes the colour target;
- a shared SERIES GRADE text quietly says "no direct sun, no golden hour, desaturated, matte contrast, lifted blacks";
- change-to prompts drop the style blocks.

The frames come out flat and grey. Every frame "passes" QC because nobody checks against the original references, but the director
sees "very mediocre". The guard makes the references, not our derived texts, the source of truth, and checks every step mechanically.

## 1. Lock the look (once per project, or when the director gives new references)

```
python3 scripts/style_lock.py init STYLE_LOCK.json REF1.png REF2.png [REF3.png …]
```

- Use the director's OWN key frames for the shot family. Exteriors and epic shots get one lock; interiors may get their own.
- `init` prints the **source prompt** embedded in each reference. Midjourney writes it into the PNG `Description`; other tools write
  `parameters` or `prompt`. Read it and reuse its vocabulary in the project's style block: time of day, lighting words, camera and lens,
  "No flat lighting…", grain. The words that produced the look are the best words to reproduce it.
- `init` also measures the references: contrast, tonal range, shadow depth (p5), saturation and the share of warm light accents.
- Edit `required` (phrases every prompt must contain) and `forbidden` (phrases that contradict the look) in `STYLE_LOCK.json`.

## 2. Lint every prompt before it is sent (a gate, not a suggestion)

```
python3 scripts/style_lock.py lint STYLE_LOCK.json PROMPT.txt PACK_DIR
```

The lint fails, and the prompt must NOT be sent, if:
- a required style phrase is missing;
- a forbidden, contradicting phrase is present;
- none of the director's style frames is attached LAST.

Keep-everything edits ("Re-shoot image 1 EXACTLY …", such as identity or colour fixes) inherit the look from image 1. For them, only the
forbidden check applies.

**Wire it into the runner.** Before `generate()`, call the lint. On failure, write a `.style_<result>` marker, log the reasons and skip
the job, so it is never sent. Fix the prompt, delete the marker, and the job runs.

## 3. Measure every result against the references

```
python3 scripts/style_lock.py compare STYLE_LOCK.json RESULT.png [RESULT2.png …]
```

- It prints `OK` or `FLAT — <reasons>` per image and writes `_style_compare.jpg` with the references and the new frames side by side.
- The thresholds were calibrated on real frames. Flat grey frames keep their contrast but lose **saturation** (below 0.8 × the
  references) and every **warm light accent** (below 0.25 × the references). Milky blacks show as a p5 more than 25 levels above the
  references.
- A `FLAT` result is rejected like any other QC failure. The fix is in the prompt's light, not in the colour: add a real key light (low
  sun through clouds, rays, warm practical lamps or portholes against a cool sky), and attach the style frames last.

## 4. When the director says "not cinematic"

1. Put the director's reference frames and the new frames on ONE sheet with `compare`. Name the differences concretely: depth, light
   source, colour contrast (warm against cool), grain, anamorphic streaks, rays.
2. Read the source prompt of the references again (step 1). Find which of your style texts contradicts it, and fix that text at the
   source: the shared grade block, not one prompt.
3. Re-lint the pending packs. Every one that fails gets fixed or re-packed before anything is sent.

## Rules

- A derived grade file (a "GRADE_xx" frame picked from earlier output) must never replace the director's references as the style
  target.
- A style block is never shortened in change-to, keyframe or fix prompts. The lint enforces this.
- A new reference from the director means `init` again, and a re-lint of everything pending.
