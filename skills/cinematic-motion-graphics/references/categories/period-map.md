# period-map - a voyage or route on an era-correct map

## Intent

Show where and when: an ink line travels across a map of the period, a ship (or train, or column) marker rides its head, and each
stop is stamped with its date as the line arrives. The map is a prop of the film (paper, engraving, chart), lit and graded like the
neighbouring shots.

## When to use

- A journey the narration follows stop by stop (a 1912 liner route Belfast -> Southampton -> Cherbourg -> Queenstown -> the
  North Atlantic, with New York as the intended, never reached, destination).
- Where something happened relative to something else (a position at sea, a front line, a coastal route).
- Not for a single place name (use `date-stamp`) or for statistics by region (use `fact-card`).

## Two lanes

| Lane | Map source | Use when |
|---|---|---|
| **vector** | coastline data (Natural Earth or similar) frozen into the project, drawn in SVG as an engraving | clean chart look, any extent, cheap to re-frame |
| **raster** | a period map plate: the project's own scan (rights cleared) or a generated plate (no lettering) | the film needs a real printed map, paper texture, period cartography |

**Vector lane.** Project with `route_overlay.py` (`projection: mercator` for sea charts, `equirect` for a plain atlas sheet),
`bounds` around the route and `padding_px` for the safe area. Draw coastlines as hairlines (1-1.5 px at 1080p), sea as fine
horizontal hatching or a flat paper tone, land in the paper tone, a graticule every 5 or 10 degrees with period degree marks. Modern
borders are wrong on a period map: draw coast only, or use a historical boundary set for that year (no border across Ireland in
1912; Austria-Hungary, the Ottoman and Russian Empires as they stood).

**Raster lane.** Georeference the plate: read 3-6 control points (graticule crossings, harbour mouths, capes) at full resolution as
`{lon, lat, x, y}`, then:

```bash
python3 <skill>/scripts/route_overlay.py shot-plan.json --lane raster -o route-coords.json   # fails above RMS 6 px
```

A high RMS means the points were misread or the plate is not in the projection named in the spec (many period charts are Mercator;
atlas sheets are often conic, which an affine fit cannot follow: use local control points around the route only, or the vector
lane). Bake the plate at twice the output size if the camera pushes in, and put the plate and the SVG overlay inside **one**
transformed wrapper so the line can never drift off the printed coast.

## Layout

- The route occupies the middle two thirds; the head of the line stays inside the centre third during camera moves.
- Labels: period names in the spec's serif caps, beside the stop on the `label_side`, never over the line or a coast. Close stops
  (Southampton and Cherbourg at Atlantic scale) get a leader line or a short inset.
- Date stamps: mono, smaller than the place name, under it.
- A cartouche or legend only if the film's period map would have one; never a modern legend box.

## Motion

- Per leg, `ink_draw` with a duration proportional to the leg's `share` from `route-coords.json`, `power1.inOut`, then a short
  pause at the stop (`ink_pool` + the label typing in) before the next leg.
- `marker_ride`: the marker sits at the line head; position and heading come from `getPointAtLength` of the current leg, inside an
  `onUpdate` of a progress proxy. A side-view ship silhouette (engraved, not an icon) faces the direction of travel.
- `intended` legs (planned, never sailed) draw last, dashed and lighter, or not at all; never as solid as the real voyage.
- One camera move: a slow push toward the active region or a pan that follows the head. No globe spin, no whip zoom.

```js
// sketch: legs drawn in order, durations from route-coords.json
let t = 1.0;
coords.legs.filter(l => l.share !== null).forEach((l, i) => {
  const p = document.getElementById("leg-" + i), len = p.getTotalLength();
  p.style.strokeDasharray = len; p.style.strokeDashoffset = len;          // static hidden state
  const d = DRAW_S * l.share;
  tl.to(p, { strokeDashoffset: 0, duration: d, ease: "power1.inOut" }, t);
  t += d + STOP_PAUSE_S;
});
```

## Film look

Paper plate from the project (scan or generated) multiplied under near-black warm ink; light from one side like a desk lamp on a
chart (warm pool, cool falloff, per the lock); the film's grain over the whole frame; vignette matched to the film; an optional
shallow focus falloff if the camera is tilted over the paper. The ink line is slightly irregular in opacity (ink grain), never a
clean vector glow.

## Accuracy

- Place names as of the date shown (Queenstown, Kingstown, Constantinople, St. Petersburg...).
- Each stop's date, and arrival vs departure: say which one the stamp shows.
- The route shape (via points) from a source, not "a plausible line".
- What did not happen is drawn as intended (dashed) and labelled only if the user approves the wording.

## Spec example

Full file: `assets/examples/period-map-1912.json`. The route part:

```json
"route": {
  "lane": "vector", "projection": "mercator",
  "bounds": { "lon": [-76, 2], "lat": [36, 57] }, "padding_px": 96,
  "stops": [
    { "id": "queenstown", "name": "QUEENSTOWN", "lon": -8.29, "lat": 51.85, "date": "11 APRIL 1912", "label_side": "left" },
    { "id": "collision", "name": "", "lon": -49.95, "lat": 41.73, "date": "14 APRIL 1912, 23:40", "label_side": "below" }
  ],
  "legs": [
    { "from": "queenstown", "to": "collision", "via": [[-47.0, 42.0]], "densify": "great-circle", "style": "solid" },
    { "from": "collision", "to": "newyork", "via": [[-69.6, 40.6]], "style": "intended" }
  ]
}
```

## QC

- `route_overlay.py` prints no safe-area warning; raster RMS under the gate.
- Snapshot at every stop arrival: the line head, the marker and the label agree; no label on the line or the coast.
- The solid line ends where the real voyage ended.
- Compare against a period map of the same area by eye: coast shape, names, absence of later borders.
