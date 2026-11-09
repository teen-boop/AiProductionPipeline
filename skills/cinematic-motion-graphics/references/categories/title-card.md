# title-card - episode titles, chapter cards, end cards

## Intent

Open, divide and close the film with type that belongs to it: the series title, the episode title, chapter titles, end and credit
cards. Kinetic, but with the restraint of a main-title sequence: the motion is in light, tracking and timing, not in effects.

## When to use

- Episode open (after the cold open), chapter breaks, the end card and credits.
- A title that sits behind a person: route to `text-behind-subject` for the matte and composite; this file sets the type and timing.

## Layout

- Centred or left-aligned on the film's optical centre (slightly above the geometric centre), inside title-safe.
- Series title, episode number and episode title as one lockup that never changes position or proportion across episodes.
- Chapter cards: one line (or a numeral + a line), smaller than the episode title, same face family.
- End cards: credits in one or two columns, generous leading, nothing smaller than legible at phone size.
- Over black (the film's black, not #000 if the lock's black is warmer) or over a held plate darkened by the film's vignette.

## Motion

- Fade from black or `iris` open; letters may fade in with a 1-2 frame stagger per character, never fly in.
- Tracking breath: letter-spacing eases from about 0.30 em to 0.24 em over the hold (`sine.inOut`); a 2-3 % `push_in` on the plate.
- A light sweep across the type only if the film's light would do it (a passing practical, a lighthouse beam), soft and slow.
- Hold: read time plus a beat (titles carry weight); exit with a dip to black or a cut on the music.

## Film look

Faces from the film's pack (a period display serif, engraved caps, or the series' own lockup). Ink at the highlight tone; halation and
grain as in the film; deep black ground. Never a logo sting, a glitch, a shimmer sweep, a gradient or a 3D extrusion.

## Accuracy

- Titles and chapter names exactly as approved, in the render's language; one language per file.
- No part counters or labels the user did not ask for.
- Credits: names and roles exactly as supplied by the user; nothing added.

## Spec example

```json
{
  "category": "title-card", "fps": 24,
  "canvas": { "w": 1920, "h": 1080, "aspect": "16:9" }, "duration_s": 7, "export": "mp4", "background": "plate",
  "texts": [
    { "id": "series", "text": "<SERIES TITLE>", "font": "Display Serif", "approved": true, "in_s": 0.8, "enter_s": 1.2, "hold_s": 4.2 },
    { "id": "episode", "text": "<EPISODE TITLE>", "font": "Display Serif", "approved": true, "in_s": 1.8, "enter_s": 1.0, "hold_s": 3.4 }
  ],
  "accuracy": [],
  "content": { "kind": "episode", "lines": ["series", "episode"], "lockup": "plates/series_lockup.svg", "background": "film black + vignette" }
}
```

## QC

- The lockup matches previous episodes (overlay the hold frame on the last episode's).
- No fallback glyphs (check every character, including accented and Cyrillic ones in that language's render).
- Hold long enough to read; the exit lands on the music or the cut.
