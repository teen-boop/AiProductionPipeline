# STYLE PACK — schema

A fixed set of slots. **The slots never change — only the values do.**
This is the mechanism behind "every project gets its own design": a new project = a new pack using
this same schema.

Project file: `<project>/STYLE-PACK.md`

---

## 1. IDENTITY
- **Pack name:** `<kebab-case>`
- **Reference format:** `<W×H @ fps>` — **mandatory.** All numbers in the SURFACE and EDGE slots
  are only valid at this format; timings in MOTION VOCABULARY are only valid at its fps.
  Porting to another format follows the rule in `PROMPT-LIBRARY §0.1` (frequencies ÷ scale,
  amplitudes × scale, timings × fps ratio).
- **Mood:** 3–5 words
- **Purpose:** what kind of material this style serves
- **Origin:** the reference/brand/previous project it was derived from

## 2. TYPE
| Role | Typeface | Weight | Size guide | Case |
|---|---|---|---|---|
| Headline | | | | |
| Deck / caption | | | | |
| Label / axis | | | | |
| Numeral / stat | | | | |

Rules: where caps apply, where italics apply, tracking, what's forbidden.
**Typefaces are named precisely. "Generic grotesque" is not a value.**

## 3. PALETTE
Roles are fixed, hex values are filled in. Every swatch must carry a *rule*, not just a color.

| Role | Hex | Usage rule |
|---|---|---|
| BASE — plate/background | | |
| INK — primary text | | |
| DECK — secondary text | | |
| STRUCTURE — axes, grid, rules | | |
| ACCENT — hero | | **exactly one element per frame** |
| STROKE — outlines, underlines, arrows | | never a fill |
| MARKER — highlight/secondary accent | | |
| MUTED — everything that isn't the hero | | |

A pack may leave a slot empty (e.g. the two-tone blueprint pack has no MARKER) — but the slot stays
in place, so library blocks know there's nothing to substitute.

## 4. SURFACE
What covers the plate. In numbers, not adjectives.
- the base and its treatment
- grain: opacity / blend / scale / refresh
- additional layers

## 5. EDGE
How the shape ends — the style's signature.
Options: marker jitter (feTurbulence bf/octaves/scale/seed) · a precise ruled line · a soft matte
bevel · torn paper · clean vector.

## 6. DEPTH
Flat / a layered diorama with real distance between layers / a volumetric matte render.
This determines which CAM blocks are even applicable.

## 7. MOTION VOCABULARY
- **Allowed blocks:** list of IDs from PROMPT-LIBRARY
- **Forbidden blocks:** and why
- **Pace:** a physical metaphor ("a hand dragging a marker," "a part settling into a slot," "clay
  settling")

## 8. NEGATIVES
This pack's own AVOID list, on top of the base one.

## 9. STAGE *(for the VIDEO route)*
The permanent background world: empty, pre-lit, level, ready to receive elements.

## 10. VERIFIED
Which numbers have actually been verified by rendering, and in which test. Unverified items are
marked as unverified.
