# Production Design Guide — the reference "bible" for a story

The output of the reference step is not a pile of loose turnaround images — it's a **Production
Design Guide**: an organized design bible that pulls the whole story's look into a consistent,
labeled system. This is the format professional AI-film pipelines use (ref: the "Until the Last
Wait" production design guide and single-character design sheets the user supplied). Two tiers:

1. **Per-item design sheets** — one polished sheet per character, plus prop and location sheets.
2. **A consolidated Production Design Guide board** — a single master spread laying every item out
   in labeled sections, so the whole story's design reads at a glance and every downstream
   generation (and the storyboard) pulls from one locked source.

The pipeline the user wants: **story → break it down into this reference bible → then storyboard.**
Do the whole bible before storyboarding.

## Tier 1 — per-character design sheet (richer than a bare 4-view)

Match the supplied examples. A full character design sheet contains, on one clean sheet with a
consistent neutral/tinted background:

- **TURNAROUND** — front, side (profile), back. For a lead, add a 3/4 view. Full body, head to toe,
  same scale across views.
- **EXPRESSIONS / DETAILS** — several head close-ups: key expressions and/or a 3/4 and profile face,
  plus tight crops of distinguishing features (hairstyle from behind, a scar, an accessory).
- **AGE / STATE VARIANTS when the story needs them** — e.g. MAIN ACTOR (YOUNG) and MAIN ACTOR (OLD)
  as separate labeled turnaround rows, or a wet/injured/costume-change state (see
  `assets/character-sheet-state.md`).
- **ASSOCIATED PROP** — if the character carries a signature object, show it on the sheet (the
  skates on the roller-derby sheet, the collar near the dog).
- **COLOR PALETTE** — a row of hex swatches for that character's costume/skin/hair key colors.
- **LABELS** — role name in a clean caption (MAIN ACTOR, THE REAPER, DOG). Keep any baked-in text
  minimal and legible; text can garble, so prefer captions only where they read cleanly and keep the
  authoritative naming in the written spec.

Attach the character's real face photo (for identity) when generating the sheet. Once approved, the
sheet is canonical — attach it to every later generation of that character.

## Tier 1 — prop and location sheets

- **Prop sheet** — the object isolated on neutral grey, front / back / detail / 3/4, plus a palette
  swatch row if it has signature colors. Template: `assets/prop-sheet-basic.md`.
- **Location sheet** — the room from 4 angles (wide establishing / reverse / feature detail / side),
  labeled in slate format `INT./EXT. PLACE — TIME OF DAY`. Template: `assets/location-sheet-basic.md`.

## Tier 2 — the consolidated Production Design Guide board

One master spread, laid out in labeled sections like a real production design guide. It's a **very
wide horizontal board (~2.4:1)** on a single consistent parchment/cream background, with thin section
dividers and clean serif labels. Sections, following the reference example precisely:

- **Title block (far-left vertical column):** "A FILM BY [studio/author]" small, then the large
  story **TITLE**, then the subtitle "PRODUCTION DESIGN GUIDE", then a **LOG LINE** heading with one
  sentence, then one tall key poster/mood image that sets the tone (the emotional anchor shot).
- **CHARACTER DESIGN (center, largest area, its own header band):** each character in its **own
  bordered box with a caption header** (e.g. `MAIN ACTOR (YOUNG)`, `MAIN ACTOR (OLD)`, `DOG (YOUNG)`,
  `DOG (OLD)`, `THE REAPER`), each box showing a 3-view turnaround (front / side / back). Group by
  importance: leads first (with age/state variants as their own separate labeled boxes), then
  supporting, then non-human/special figures (animals, a personified figure). Boxes tile across two
  rows.
- **PROPS (right vertical column, its own header):** each recurring prop isolated on the parchment
  background, labeled (`DOG COLLAR & TAG`), often with a detail view + a flat/laid-out view + close
  detail of a sub-element (the tag).
- **SET DESIGN (lower center band, its own header):** each key location as a small strip of 3–4
  frames, labeled in slate format (`INT. HOSPITAL ROOM — NIGHT`, `EXT. CITY STREET — RAINY DAY`),
  and **each location gets its own flat colour-palette swatch row directly beneath its frames** — so
  every location carries its own key colours, not just each character.
- **NOTES FOR ART DEPARTMENT (lower-right corner block):** the story's global art direction as short
  bulleted lines, each with a concrete value — **Tone** (e.g. "Melancholic, realistic, restrained"),
  **Time** (era, e.g. "Contemporary"), **Palette** (e.g. "Desaturated, cold blues and warm browns"),
  **Texture** (e.g. "Real-world materials, worn, lived-in"), **Theme** (e.g. "Loyalty, time, and the
  promise beyond life"). This is the written companion to the STYLE LOCK block; it's what keeps every
  sheet and every scene in one world. A small ghosted mood image can sit under it.

The board can be **assembled** (compose the already-approved individual sheets into one layout — most
reliable, no re-generation risk) rather than generated from scratch in one shot. Generating a whole
multi-section board in a single pass is unreliable for text labels and per-panel fidelity; prefer
building the individual sheets first, approving each, then laying them into the board.

## Order of work

1. From the finished script (step 2), extract every character, prop, and location (the extraction
   pass in `location-and-prop-references.md`).
2. Fill in the **NOTES FOR ART DEPARTMENT** first — tone/time/palette/texture/theme — because every
   sheet must obey it. This doubles as the seed of the STYLE LOCK block used in production (step 4).
3. Generate and approve each per-item design sheet (character / prop / location), each obeying the
   notes/palette.
4. Assemble the consolidated Production Design Guide board from the approved sheets.
5. Only then move to storyboarding (`visual-story-8-storyboard`), which pulls its look from this
   locked bible so the storyboard's style matches the design guide exactly.

## Why a bible, not loose images

A production design guide is a single source of truth: when a scene weeks later needs a character,
a prop, or a room, it's pulled from the approved bible instead of re-described from memory — which is
what keeps a long project looking like one film. It's the same lock-in logic as a single character
portrait, scaled to the whole story at once.
