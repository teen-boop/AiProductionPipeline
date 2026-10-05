---
name: motion-graphics-director
description: Entry-point orchestrator for AI motion-graphics work (Vox-style explainers, animated charts, collage clips). Decides which of the two production routes applies — CODE (Remotion + Claude Code, for numbers/charts/typography/programmatic scale) or VIDEO (Omni Flash / video models, for dynamic collage, camera moves, big blocks) — then routes to the correct companion skill in the correct order. Owns the shared prompt library of 46 composable animation blocks. Use whenever starting or resuming a motion-graphics project, when it is unclear which route or skill applies, when asked which animation to use for a beat, or when assembling a multi-scene explainer. Triggers on motion graphics, vox style, animated chart, remotion, explainer video, which route, animation library, motion prompt, bar chart animation, boil, style sheet, collage clip.
---

# Motion Graphics Director

## Why this exists

Motion-graphics work here splits into two production routes that share ONE visual language but have completely different mechanics, failure modes and prompt shapes. Picking the wrong route wastes the most time of any decision in this pipeline. This skill makes that decision explicitly, then hands off.

## Design is per-project, always

The pipeline is constant; the design is not. Every project gets its own **STYLE PACK** built against one fixed ten-slot schema (`motion-style-core`). Shipped packs — `paper-vox`, `blueprint`, `clay` — are worked examples, **not house style**. Reusing one because it is convenient is how every project ends up looking identical. Reach for an existing pack only when the project genuinely belongs to that family, and say so out loud.

Everything downstream reads **slots**, not colors: the prompt library, the Remotion builder and the video route work unchanged across wildly different looks. Any hex or font in the library is an example filling, to be substituted from the project's pack — and an empty slot means that block is not used in this project.

## Step 0 — always: which route?

| The shot needs | Route | Why |
|---|---|---|
| Exact numbers, charts, axes, counting values | **CODE** | video models still fabricate digits |
| Fine typography, small labels, dense text | **CODE** | video models warp type below headline size |
| Programmatic scale (N variants, data-driven) | **CODE** | one composition, swapped props |
| Precise timing to a voice-over | **CODE** | frame-accurate sequencing |
| Dynamic camera, orbits, dives, parallax depth | **VIDEO** | expensive and stiff to fake in code |
| Photo/collage cutouts, halftone people, torn paper | **VIDEO** | or CODE with pre-made cutouts |
| Big blocks, logos, chunky headline type only | **VIDEO** | fast route, no intermediate frame |
| A whole multi-scene explainer film | **CODE** | scene architecture + master sequence |

Mixed piece? That is normal and correct — the hybrid wins. Route **per shot**, not per project. Both routes must draw from the same STYLE CORE.

## Order of operations (never reorder)

1. **Script → voice-over → scenes.** The script IS the timeline. Each beat maps to one visual. Never build scenes before the VO exists, or the timing gets rebuilt twice.
2. **Lock the STYLE CORE** → `motion-style-core`. Nothing is generated before this exists.
3. **Design & references intake** → `motion-design-references`. Inspect the folder before asking anything, split every reference into STYLE vs ASSET, lock approved images, write the INDEX.
4. **Build per route** → `motion-remotion-build` (CODE) or `motion-video-route` (VIDEO).
5. **Assemble** → master sequence, VO sync, music, render.

## The roster

| Skill | Phase | Owns |
|---|---|---|
| `motion-style-core` | 2 | the project's STYLE PACK — fonts, palette roles, surface, edge, motion vocabulary |
| `motion-design-references` | 3 | reference intake, STYLE/ASSET split, locked images, INDEX, Lovart attachment sets |
| `motion-remotion-build` | 4 | Remotion project, props, exact numbers, render |
| `motion-video-route` | 4 | master style sheet image, image→video, shot blocks |

## The prompt library

`references/PROMPT-LIBRARY.md` — 46 composable blocks in 9 groups (ING, CAM, ENT, VAL, ANN, FIN, TRN, AUD, QA), plus 5 assembled combos and a compatibility matrix.

**Composition formula for any one shot:**
```
SETUP + STYLE CORE + 1×CAM + 1–3×ENT/VAL + 1–2×ANN + FIN + QA
```

**Three mixing rules — enforce these, they are the difference between designed and generated:**
1. Exactly one camera move per composition. Wanting a second means it is a second composition.
2. At most three element movements at once; everything else is spread by stagger.
3. The FIN finish layer is never off — but text never enters a displacement filter.

Check the compatibility matrix before combining. Known bad pairs: boil + 3D rotate, line race + parallax, wave + 3D rotate.

## Before any prompt leaves — the anti-slop gate

Run the 12-point checklist in `references/PROMPT-LIBRARY.md §7`. The three that catch the most failures:
- **Is the font named explicitly?** A default font is the single biggest slop tell.
- **Has the model's default been named and forbidden?** (rings→grid, bouncy ease→marker pace, straight wipe→torn edge)
- **Is there exactly one hero accent,** with everything else muted?

## Doctrine

`references/DOCTRINE.md` — the extracted rules from the four source tutorials, and the combined architecture diagram. Read it when a decision feels arbitrary; the answer is usually already there.
