# composite-overlay - graphics over live or generated footage

## Intent

Point at something inside a shot (a rider on the horizon, a window in a facade, a person in a crowd) or set type inside the shot's depth,
so the graphic seems to be in the scene: tracked, lit, focused, grained and graded like the footage.

## When to use

- The viewer must find a detail in a busy frame: a tracked callout with a leader line and a short label.
- A title or number inside the scene: type behind the subject (route to `text-behind-subject` for matting and the 3-layer
  composite).
- Not when the camera or subject moves too fast for a readable label; pick a calmer take or a held frame instead.

## Tracking

- Best: a planar or point track from the NLE (DaVinci Resolve tracker or Fusion), exported as per-frame `x, y` (and scale) for the
  shot's range, saved as JSON beside the spec.
- Slow camera or a locked-off generated clip: 2-4 hand-placed keyframes from snapshots, interpolated with `sine.inOut`, checked
  against the footage every 12 frames.
- The overlay's time 0 equals the plate's `in_s`; note it in the spec so the composite lines up.
- Labels stay steady: the leader end follows the track, the label box moves only with heavy smoothing (or not at all).

## Layout

- The label sits in empty sky, water or wall, never over a face; the leader is short (60-200 px) and does not cross the subject.
- One callout at a time; a second only after the first has left.
- Behind-subject type: the subject covers less than about 60 % of the frame and the type sits behind head and shoulders.

## Motion

- Leader draws from the target outward (`ink_draw`, 10-14 frames), a small `ink_pool` at the target, then the label fades in.
- Hold the read time; exit with a fade or on the cut.
- Moving graphics get motion blur equivalent to the footage's shutter (about half a frame at 24 fps) or move slowly enough not to
  need it.

## Grade and depth match

- Sample the plate's black, mid and highlight with `video-color-grade`'s frame inspection; ink at the plate's highlight tone, scrims
  at its shadow tone.
- Defocus the graphic to match the plane it sits in (a label on the far horizon is as soft as the horizon).
- Grain inside the ink, matched to the plate; no vignette added (the plate has its own).
- If the plate is graded later, prefer the `neutral+lut` pipeline so the overlay follows the grade.

## Accuracy

Whatever the callout names (a vehicle, a place, a person, a distance) has an accuracy line like any period graphic.

## Spec example

```json
{
  "category": "composite-overlay", "period": 1900, "fps": 24,
  "canvas": { "w": 1920, "h": 1080, "aspect": "16:9" }, "duration_s": 5, "export": "prores4444", "background": "transparent",
  "texts": [ { "id": "callout", "text": "SIGNAL TOWER", "approved": true, "in_s": 0.8, "enter_s": 0.6, "hold_s": 2.8, "box": [1180, 210, 360, 48] } ],
  "accuracy": [ { "claim": "Position of the signal tower on the ridge", "source": "fill from period-fact-check", "status": "pending" } ],
  "assets": [ { "role": "plate", "path": "plates/S041_take2.mp4", "origin": "generated", "user_approved": true } ],
  "content": { "plate": { "file": "plates/S041_take2.mp4", "in_s": 1.25 }, "track": { "file": "plates/S041_track.json" },
               "callouts": [ { "text_id": "callout", "target": "track", "leader_px": 140, "side": "right" } ], "depth": "far plane, soft" }
}
```

## QC

- Leader end stays on the target in snapshots across the whole hold (within 4 px at 1080p).
- Composite over the plate at the hold and at phone size: readable, not over a face, matched softness and grain.
- Alpha veil check passes.
