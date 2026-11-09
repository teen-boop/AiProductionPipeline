# timeline - era chronology with events and photos

## Intent

Lay out the order of events and how far apart they were, so the viewer feels time passing: a ruled line of years, events pinned
along it, photos where the film has them.

## When to use

- The narration covers a span (construction years, a career, a war) and the gaps between events matter.
- A recap at the start of an episode or before the climax.
- Not for a single date (use `date-stamp`).

## Layout

- **Horizontal (16:9):** the axis at about 58-62 % of the frame height, years as ticks below, events above with a short leader
  to their tick; photos above the labels, same size and treatment.
- **Vertical (9:16):** the axis down the left third, events to the right, the camera travelling down.
- Spacing proportional to time. When a gap is too long to draw, compress it with a visible break (two short slashes on the axis)
  and say so in the spec (`breaks`).
- At most 3-4 events readable on screen at once; the camera travels for more.

## Motion

- `rule_draw` of the axis, ticks appearing as it passes them.
- One camera move: a truck along the axis (horizontal) or a slow descent (vertical) at a constant, slow pace, easing only at the
  ends; the active event sits in the centre third.
- Each event: `ink_pool` on the tick, leader draws, label fades in, photo `rack_reveal`s; the active event gets weight, earlier ones
  dim to the muted tone.
- Holds on each event long enough to read label + date.

## Film look

The axis and ticks are ink or engraved lines on the film's paper or dark plate; photos are the project's own archival or generated
frames, graded to the lock, with a thin paper border or a soft vignette, never rounded corners or drop shadows.

## Accuracy

- Every event date with its source; the precision the source supports (day, month or year only).
- Photos: what each one shows, and whether it is archival or a recreation (the film decides whether to mark recreations).

## Spec example

```json
{
  "category": "timeline", "period": 1912, "fps": 24,
  "canvas": { "w": 1920, "h": 1080, "aspect": "16:9" }, "duration_s": 14, "export": "mp4", "background": "plate",
  "texts": [
    { "id": "e1", "text": "31 MARCH 1909  KEEL LAID", "approved": true, "in_s": 1.5, "enter_s": 0.8, "hold_s": 2.4 },
    { "id": "e2", "text": "31 MAY 1911  LAUNCHED", "approved": true, "in_s": 5.0, "enter_s": 0.8, "hold_s": 2.4 },
    { "id": "e3", "text": "10 APRIL 1912  MAIDEN VOYAGE", "approved": true, "in_s": 8.8, "enter_s": 0.8, "hold_s": 3.0 }
  ],
  "accuracy": [ { "claim": "Keel laying, launch and departure dates", "source": "fill from period-fact-check", "status": "pending" } ],
  "content": { "orientation": "horizontal", "range": [1909, 1912],
               "events": [ { "date": "1909-03-31", "label": "KEEL LAID", "photo": "plates/slipway.png" },
                           { "date": "1911-05-31", "label": "LAUNCHED", "photo": "plates/launch.png" },
                           { "date": "1912-04-10", "label": "MAIDEN VOYAGE", "photo": "plates/departure.png" } ],
               "breaks": [], "camera": { "move": "truck", "px_per_year": 900 } }
}
```

## QC

- Distances between ticks match the dates (measure on a snapshot).
- Each event readable for its read time while it is the active one.
- Photos share one treatment; none is a stock image.
