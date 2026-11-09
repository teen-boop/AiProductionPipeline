# lower-third - documentary name cards for historical persons

## Intent

Name a person on screen with the restraint of a documentary: name, role at that moment, years. It identifies; it does not brand.

## When to use

- First appearance of a person (a portrait, an archival photo, an actor playing a historical person, a contemporary interviewee).
- Once per person per episode, unless the narration re-introduces them after a long gap.
- Not for places or dates (use `date-stamp`).

## Layout

- Lower left in 16:9 (left 8 %, baseline 10-12 % from the bottom), away from the face and hands; 9:16: lower third above the
  caption zone.
- Line 1: the name in the film's serif or grotesque, mixed case or caps per the pack.
- Line 2: role at the time of the scene and years in a smaller, tracked face: "Captain, RMS Titanic  1850-1912".
- An optional hairline rule between or before the lines. No box. For a bright plate, a soft gradient scrim (black at 20-35 %,
  feathered over 300-400 px) behind the lower band only.
- The same position, size and timing for every name card in the film.

## Motion

- Name: fade + 8-12 px rise, `sine.out`, 14-18 frames. Rule draws (`rule_draw`) under it. Role and years follow 6-10 frames later.
- Hold at least the read time of both lines together (usually 3-4 s).
- Exit: fade 14-18 frames, or cut with the shot. No slide-out, no wipe bar.

## Film look

Ink at the highlight tone of the film; grain inside the ink; faint halation if the film has it. The scrim, when used, is in the film's
shadow tone, never a neutral grey. Contrast checked over the real plate.

## Accuracy

- Spelling of the name as the sources and the film use it (including diacritics and initials).
- The role and rank at the time of the scene, not a later or earlier one.
- Birth and death years from a source; a dash between years, no "circa" unless the source says so.
- An actor portraying a historical person: the card names the person, not the actor, unless the user decides otherwise.

## Spec example

```json
{
  "category": "lower-third", "period": 1912, "fps": 24,
  "canvas": { "w": 1920, "h": 1080, "aspect": "16:9" }, "duration_s": 5, "export": "prores4444", "background": "transparent",
  "texts": [
    { "id": "name", "text": "EDWARD JOHN SMITH", "font": "Period Serif", "approved": true, "in_s": 0.4, "enter_s": 0.7, "hold_s": 3.4, "box": [154, 880, 820, 64] },
    { "id": "role", "text": "CAPTAIN, RMS TITANIC  1850-1912", "font": "Ledger Mono", "approved": true, "in_s": 0.7, "enter_s": 0.7, "hold_s": 3.1, "box": [154, 950, 820, 36] }
  ],
  "accuracy": [ { "claim": "Name, rank in April 1912 and life years", "source": "fill from period-fact-check", "status": "pending" } ],
  "content": { "person": { "name": "Edward John Smith", "role": "Captain, RMS Titanic", "years": "1850-1912" },
               "position": "lower-left", "scrim": { "opacity": 0.3, "height_px": 360 } }
}
```

## QC

- Name and role are readable together for at least the summed read time.
- Nothing overlaps the face, hands or a subtitle line; boxes inside title-safe.
- All name cards in the episode share position, size and timing (contact sheet of every card side by side).
