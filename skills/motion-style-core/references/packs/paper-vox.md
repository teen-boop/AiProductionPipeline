# STYLE PACK · paper-vox

## 1. IDENTITY
- **Name:** `paper-vox`
- **Mood:** newsroom-serious, layered, tactile, slightly retro
- **Purpose:** documentary explainers, editorial graphics, collage breakdowns
- **Origin:** MG-VOXSTAGE from tutorials 1–2

## 2. TYPE
| Role | Typeface | Weight | Size | Case |
|---|---|---|---|---|
| Headline | DM Serif Display | Regular | 76 | mixed, key word in italics |
| Deck | DM Serif Display | Italic | 24 | mixed |
| Label / axis | Oswald | Regular, tracking 1.4 | 22 | CAPS |
| Numeral | DM Serif Display | Regular | 53 | — |

Forbidden: warped letters, default system font.

## 3. PALETTE
| Role | Hex | Rule |
|---|---|---|
| BASE | `#F7F4EC` | plate, everywhere |
| INK | `#1C1B19` | all primary text |
| DECK | `#5A5648` | secondary text, sources |
| STRUCTURE | `#6F6940` | axes and ticks, opacity 0.22 |
| ACCENT | `#D0674C` | exactly one element per frame |
| STROKE | `#D62E1F` | outlines, underlines, arrows — never a fill |
| MARKER | `#F5C842` | phrase highlighting only |
| MUTED | `#A9BCC2` | everything that isn't the hero |

## 4. SURFACE
Paper scan at 28% opacity over the base, warmed with a 50% BASE tint. Without the scan, the flat
base reads through.
Frame grain: **16% opacity, overlay, scale 0.72, refresh every 2 frames**, seed = `floor(frame/2)`.

## 5. EDGE
Marker jitter: `feTurbulence` fractal, **base frequency 0.02, 3 octaves, displacement scale 4,
seed frozen**. Filter region enlarged so edges don't clip.
In-shape speckle: noise frequency 0.42, strength 0.34, multiply.

## 6. DEPTH
A layered paper diorama. For the CODE route — flat layers with an offset outline; for VIDEO — real
distance between cutouts, shallow depth of field.

## 7. MOTION VOCABULARY
- **Allowed:** ENT-01/03/04/05/07/08 · VAL-01…06 · ANN-01…08 · FIN-01/02/03/04/05/06 · CAM-01/03/04/05
- **Forbidden:** CAM-02 (the 3D rotation breaks the paper plane)
- **Pace:** "a hand dragging a marker" — steady motion, easing only on exit; `Easing.bezier(0.2, 0, 0.3, 1)`

## 8. NEGATIVES
No glossy CG. No lens flares. No invented logos. Every visible word comes from approved samples.

## 9. STAGE
A muted archival map field, evenly toned, empty, pre-lit.

## 10. VERIFIED
✅ test-01: the full palette, score, grain, EDGE 0.02/4, speckle, marker pace.
⚠️ Not verified: FIN-03 boil, STAGE, the VIDEO route.
