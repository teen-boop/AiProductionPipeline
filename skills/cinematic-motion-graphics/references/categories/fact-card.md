# fact-card - numbers, ledgers and to-scale comparisons in film look

## Intent

Make one number felt: the length of a bridge, a tonnage, a count of people, set like letterpress or engraved type, or compared to
something the viewer knows, at true scale. Code route always: video models invent digits.

## When to use

- A single number the narration stresses (count up and settle).
- A short table the narration walks through (a ledger of wages, cargo, departments).
- A size comparison (a bridge against a city block, a building, another bridge), with silhouettes drawn to one scale.

## Layout

- **Single number:** the number large (30-45 % of frame height), the unit beside it in the same face at half size, the label below
  in tracked small caps. Centre-left or centre; never filling the frame edge to edge.
- **Ledger:** ruled rows like an account book or a manifest: hairline rules, tabular numerals right-aligned, labels left-aligned,
  at most 5-6 rows per card; split longer tables.
- **Comparison:** silhouettes on one baseline at one scale (`scale_px_per_m` in the spec), labelled with name and size; the
  reference object familiar to the audience of the film's language.

## Motion

- `count_settle`: a proxy from 0 (or a meaningful start) to the exact value, `power2.out`, 30-48 frames, then hold the exact final
  value. Format with the language's separators; tabular numerals so digits do not jump.
- Ledger: rows appear in reading order (`rule_draw` + fade, 6-10 frames apart); the hero row gets weight, not colour.
- Comparison: the familiar object first, then the subject drawn in (`ink_draw` of the outline or a slow wipe along its length),
  then the label. One camera move at most (a slow pull-out to reveal the full length).

## Film look

Letterpress: slight ink spread and uneven density inside the glyphs (ink grain), impression on paper if there is a paper plate.
Etched or engraved: fine hatching in silhouettes, hairline outlines. Palette from the lock; the accent colour, if any, on one element.
No chart-library styling: no rounded bars, no gridlines unless a ledger's rules, no legends.

## Accuracy

- Every number with its source and unit as the source states it (feet and inches, long tons); a conversion only if the
  film's language needs it, rounded honestly ("about 412 m").
- Where sources disagree (workforce and attendance counts often do), the accuracy line says which source is followed, and the card uses
  "about" if the narration does.
- Comparison silhouettes from real dimensions, all at the same scale; no artistic stretch.

## Spec example

```json
{
  "category": "fact-card", "period": 1900, "fps": 24,
  "canvas": { "w": 1920, "h": 1080, "aspect": "16:9" }, "duration_s": 7, "export": "mp4", "background": "plate",
  "texts": [
    { "id": "value", "text": "1350 FT 6 IN", "font": "Etched Serif", "approved": true, "in_s": 0.5, "enter_s": 1.6, "hold_s": 3.6 },
    { "id": "label", "text": "MAIN SPAN", "font": "Ledger Mono", "approved": true, "in_s": 2.0, "enter_s": 0.6, "hold_s": 3.4 }
  ],
  "accuracy": [ { "claim": "Main span 1350 ft 6 in", "source": "fill from period-fact-check", "status": "pending" } ],
  "content": { "value": 1350.5, "unit": "ft", "format": "{ft} FT {in} IN", "label": "MAIN SPAN",
               "comparison": { "items": [ { "name": "city block", "length_m": 80 }, { "name": "bridge", "length_m": 411.6 } ], "scale_px_per_m": 3.8 } }
}
```

## QC

- The final frame of the count shows exactly the approved value and format.
- Snapshot mid-count: no layout jump (tabular numerals), no overlapping unit.
- Silhouette lengths in pixels equal `length_m x scale_px_per_m` (measure on the snapshot).
