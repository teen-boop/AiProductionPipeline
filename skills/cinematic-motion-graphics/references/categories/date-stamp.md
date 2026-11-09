# date-stamp - date, time and place stamps, clocks, countdowns

## Intent

Anchor the viewer in time and place with the least possible graphic: a typed or stamped date, a time that settles on the event, a
place line. It should feel like a ledger entry, a ship's log or a typewriter, not a news ticker.

## When to use

- The first shot of a sequence that jumps in time or place.
- A clock running toward an event ("23:31 ... 23:40"), or a countdown the narration counts with.
- A chapter of hours ("02:05", "02:17", "02:20") repeated across a sequence: same position, same font, every time.

## Layout

- Lower left inside title-safe (16:9: left 8 %, bottom 9 %); 9:16: lower third above the caption zone, left 6 %.
- Hierarchy: date (largest after the clock), time (largest when the clock matters), rule, place (smallest, tracked caps).
- Never centred over a face; never over the brightest area of the plate (check the composite).
- A sequence of stamps keeps one position and one size so the eye knows where to look.

## Motion

- `typewriter` for the date: one character per 2-4 frames, spaces included.
- `clock_settle` for the time: minutes tick from `time_from` to `time_to`, `power2.out`, so the last minutes slow down onto the
  event; a small dot or tick marks the arrival.
- `rule_draw` under the clock; place line fades in after the date is complete.
- Countdown: the same mechanics in reverse; seconds only when the narration lives in seconds.
- Exit with a slow fade at the end of the sentence or on the cut.

## Template

`assets/templates/date-stamp.html` (this skill) is a working HyperFrames composition: 1920x1080, 24 fps, 8 s, variables `date`,
`time_from`, `time_to`, `place`, `transparent`, `guides`, `grain`. It passes `hyperframes lint` and `check`, and renders ProRes
4444 with a clean alpha (`--format mov --variables '{"transparent":true}'`). Swap the generic font stacks for the project's
glyph-tested face and the colour tokens for the lock's values.

## Film look

- Paper-white ink at the film's highlight tone, faint warm halation only if the film has it.
- Grain inside the ink in alpha mode, over the whole frame on a plate.
- Typewriter / ledger mono with tabular numerals; tracked caps for the place.
- No boxes, no pills, no blinking cursor, no digital seven-segment clock unless the film's world has one.

## Accuracy

- Which clock: ship's time, local time, GMT? Name it in the accuracy line; label it on screen only if the narration does.
- 12 h vs 24 h notation as the film's language and period would write it; the date order of the language (14 April 1912).
- Place name of the period.

## Spec example

Full file: `assets/examples/date-stamp-1912.json`.

```json
"texts": [
  { "id": "date",  "text": "14 APRIL 1912",  "approved": true, "in_s": 0.6, "enter_s": 1.4, "hold_s": 5.2, "box": [154, 770, 760, 70] },
  { "id": "time",  "text": "23:40",          "approved": true, "in_s": 2.2, "enter_s": 2.4, "hold_s": 2.6, "box": [154, 850, 300, 90] },
  { "id": "place", "text": "NORTH ATLANTIC", "approved": true, "in_s": 3.2, "enter_s": 0.8, "hold_s": 3.2, "box": [154, 950, 600, 40] }
],
"content": { "variables": { "date": "14 APRIL 1912", "time_from": "23:31", "time_to": "23:40", "place": "NORTH ATLANTIC", "transparent": true } }
```

## QC

- Snapshot mid-typewriter, mid-clock, at the arrival and in the hold: the clock shows whole minutes only, the last value is exactly
  `time_to`.
- The full stamp holds at least the read time after the clock lands.
- Alpha veil check passes; composite over the plate is readable at phone size.
