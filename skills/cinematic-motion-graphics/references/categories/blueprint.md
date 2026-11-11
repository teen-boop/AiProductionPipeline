# blueprint - plans, cross-sections and schematics drawn in

## Intent

Explain how a thing is built or how it failed, the way the period's own drawing office drew it: lines drafted in order, labels with
leaders, dimensions, then the explanatory change (water filling a chamber, a part moving).

## When to use

- The narration explains structure: chambers, gates, sluices, pumps, a mechanism.
- A drafting-office scene of the film needs a drawing that comes alive.
- Not for maps (use `period-map`) or numbers alone (use `fact-card`).

## Style source

Start from `motion-style-core`'s blueprint pack (two-tone, hierarchy by line weight, no bounce) and adapt it to the film:
- **Cyanotype blueprint:** white lines on Prussian blue, the paper slightly uneven, the film's grain on top.
- **Linen or paper ink drawing** (what a drawing office mostly produced): dark ink on cream linen, hatched sections, colour washes
  only where the period drawings used them.
Pick the one the film's world would show and write it in the spec. Inside the film's look, a blueprint plate still gets the lock's
black level and light falloff; it is a lit object, not a flat screen.

## Drawing source

The project's own vector trace of a public-domain or rights-cleared plan, or a drawing built from verified dimensions. A generated
plate may give texture, but lines that the narration points at are drawn as code vectors so they are exact and animatable. Never
invent internal structure.

## Layout

- The object fills 70-80 % of the width in the title-safe area, horizon level, on a faint construction grid.
- Labels in drafting capitals (mono or hand-lettering face), leader lines with a dot or arrow at the part, dimension lines with
  ticks and the value centred above.
- A title block (bottom right) only if the film's drawing would have one, with approved text only.

## Motion

- Draw order like a draughtsman: centreline and datum -> outer profile -> chambers -> gates -> details -> leaders and labels ->
  dimensions. `ink_draw` with constant speed (300-500 px/s), `power1.inOut` per stroke group.
- Hero part by weight (a heavier line) and position, not by colour.
- Explanatory change: filling as a flat wash rising chamber by chamber (clip-path or mask height), at a slow steady pace,
  with each chamber's label lighting up; parts move with a hard, damped stop, never a bounce.
- One camera move: a slow pan along the structure or a push into a section.

## Film look

Lines are slightly imperfect (ink or chalk density varies), the paper shows texture, grain from the lock. No glow, no neon cyan, no
HUD elements, no scanning bars.

## Accuracy

- Number and position of chambers, gates, sluices and culverts from a source drawing.
- Which chambers filled and in what order, with the source's wording ("the upper two" vs "three") and its uncertainty.
- Units and dimension values as the drawing states them.

## Spec example

```json
{
  "category": "blueprint", "period": 1900, "fps": 24,
  "canvas": { "w": 1920, "h": 1080, "aspect": "16:9" }, "duration_s": 12, "export": "mp4", "background": "plate",
  "texts": [
    { "id": "lbl_gates", "text": "LOCK GATES", "approved": true, "in_s": 5.0, "enter_s": 0.6, "hold_s": 3.0 },
    { "id": "lbl_fill", "text": "UPPER CHAMBER FILLS FIRST", "approved": true, "in_s": 8.0, "enter_s": 0.6, "hold_s": 3.0 }
  ],
  "accuracy": [ { "claim": "Gate positions and the order the chambers fill", "source": "fill from period-fact-check", "status": "pending" } ],
  "content": { "drawing": { "source": "plates/lock_section_trace.svg", "style": "linen ink", "layers": ["datum", "profile", "chambers", "gates", "labels"] },
               "draw_order": ["datum", "profile", "chambers", "gates", "labels"], "labels": ["lbl_gates", "lbl_fill"], "dimensions": [] }
}
```

## QC

- Drawn lines match the traced source when overlaid (difference snapshot).
- Labels never cross a line they do not point at; leaders end on their part.
- The fill order and count match the accuracy line.
