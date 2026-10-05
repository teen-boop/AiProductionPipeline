---
name: motion-style-core
description: Builds and locks a per-project STYLE PACK for motion graphics — the swappable design layer. Every project gets its own pack (fonts, palette with roles, surface, edge treatment, depth, motion vocabulary, negatives) filled against one fixed schema, so the pipeline stays constant while the design changes completely from project to project. Derives a new pack from a reference image, a brand, or a described mood; ships tested packs (paper-vox, blueprint, clay) as starting points, never as defaults. Also owns the anti-slop pass, especially font sourcing. Use at the start of any motion-graphics project, when adapting to a new look, when a frame looks generic or AI-slop, or when style drifts between shots. Triggers on style pack, lock the style, new design for this project, palette, which font, looks like AI slop, style drift, master style sheet, visual system, blueprint style, clay style, paper style.
---

# Motion Style Core

## The rule this skill exists to enforce

**The pipeline is constant. The design is not.** Every project gets its own STYLE PACK, written once, referenced by name afterwards ("same project, same look"). Style is never re-described per shot — re-describing is how drift happens.

**There is no default look.** `references/packs/` holds worked examples, not house style. Starting a project by reusing `paper-vox` because it is there is exactly how every piece ends up looking the same. Reach for an existing pack only when the project genuinely belongs to that family, and say so out loud when you do.

## The schema is fixed, the values are not

Ten slots, in `references/STYLE-PACK-SCHEMA.md`:

`IDENTITY · TYPE · PALETTE · SURFACE · EDGE · DEPTH · MOTION VOCABULARY · NEGATIVES · STAGE · VERIFIED`

Every pack fills the same ten. That is what makes the prompt library, the Remotion builder and the video route work unchanged across wildly different designs — they read slots, not colors.

**Empty slots are legal and meaningful.** Blueprint has no MARKER and no grain; clay has no STROKE and no axes. An empty slot tells the downstream blocks there is nothing to substitute — it is information, not an omission. Never fill a slot just to fill it.

## Building a pack

### Step 1 — the font, always first
The default font is the single largest tell of AI-generated design. Never accept one.

1. Take the reference the user has, or ask what the piece should feel like.
2. Identify a font in the wild: **fonts.inuse.com**. Pull a site's typography with Firecrawl using the `branding` format.
3. Source it: **Fontshare**, **Open Foundry**, **Google Fonts**, **Typewolf**. For a brand used repeatedly, recommend buying the real face — cheapest quality upgrade available.
4. Write exact family names and weights into the pack. "A condensed sans" is not a value.

### Step 2 — derive the palette as roles, not colors
A palette is a list of **jobs**. Every swatch gets a hex and a rule. Fill the fixed roles: BASE, INK, DECK, STRUCTURE, ACCENT, STROKE, MARKER, MUTED.

**The one-hero rule holds in every pack, but each pack decides how hero is expressed** — paper-vox does it with a hot accent color, blueprint with line weight on a strictly two-tone plate, clay with scale and position. Ask the pack: *what makes one thing dominant here?* If two things read as hero, the shot has no point yet; fix the shot, not the color.

### Step 3 — surface, edge, depth in numbers
These three decide whether the piece reads as printed, drafted, or moulded. Adjectives are not values — `28% opacity`, `baseFrequency 0.02`, `1.5px ruled` are.

**Edge is the signature slot.** It is the fastest way to tell two packs apart, and the fastest thing to get wrong: marker-edge base frequency is scale-sensitive — 0.02–0.05 at 1920x1080; values of 1 and above collapse into invisible pixel fuzz (verified in test-01).

### Step 4 — motion vocabulary, allowed and forbidden
List which PROMPT-LIBRARY block IDs belong to this pack **and which are banned**. The bans matter more: paper-vox forbids CAM-02 because a 3D rotate breaks the paper plane; clay forbids every FIN paper texture; blueprint forbids springs with overshoot. Give the tempo as a physical metaphor — "a hand dragging a marker", "a part seating into its socket", "clay settling".

A bouncy spring is right in clay and wrong in paper-vox. That judgment lives in the pack, not in the animator's taste.

### Step 5 — write it
`<project>/STYLE-PACK.md`, all ten slots. Mark in VERIFIED what has actually been rendered and what has not. An untested number is a hypothesis and must be labelled as one.

## Master style sheet (VIDEO route)

Also generate one 16:9 board — six panels:

1. **TYPE SPECIMEN** — H1 sample, hero stat sample, annotation label sample. Real words, never lorem.
2. **PALETTE** — labeled swatches with hex and the usage rule printed.
3. **COMPONENT ZOO** — 5–6 components sharing ONE construction logic.
4. **MINI-SCENES** — 3 example frames.
5. **MOTION THUMBNAILS** — 4 storyboard frames, arrows only.
6. **THE STAGE** — the persistent background: empty, pre-lit, evenly toned.

Baked-in typography is intentional here — this is a style guide, and it is what the model reads. `ONE IMAGE = THE RULEBOOK`.

Downstream, every prompt carries this sentence verbatim:

> Use the attached style sheet for **materials only** — do NOT copy the sheet's layout or its flatness.

Without it the model reproduces the sheet's grid instead of its language.

## Deriving a new pack from a reference

When the user brings a reference image or a brand:
1. Read it in concrete detail before naming it — color blocking, where weight sits, how edges terminate, how much empty space, what carries emphasis. Do not shortcut to a style label ("looks Vox-ish") and generate from the label.
2. Map what you see onto the ten slots. Name what is missing rather than inventing it.
3. Ask only about what genuinely cannot be read off the reference — usually motion tempo and the hero mechanism.
4. Write the pack, mark everything VERIFIED: no.
5. Render one test frame carrying every slot, and only then mark numbers verified.

## The anti-slop pass — before any pack is approved

1. Fonts named exactly, with weights?
2. Every swatch has a **rule**, not just a hex?
3. Exactly one hero mechanism, and is it stated?
4. Surface / edge / depth in numbers, not adjectives?
5. Forbidden blocks listed, not just allowed ones?
6. Negatives written?
7. Icons or assets, if any, from a single pack in a single style — never mixed sources?
8. Does anything here exist only because it was copied from another project's pack?

## Hand-off

Pack locked → `motion-design-references` (reference intake and Lovart assembly) → the route builders. Nothing is generated before the pack exists; every frame made before it will be reshot.
