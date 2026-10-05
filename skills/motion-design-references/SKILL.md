---
name: motion-design-references
description: Reference and design intake for a motion-graphics project — the step between locking a STYLE PACK and generating anything. Inspects what is actually in the project's references folder first and reports it, then has the user assign roles; sorts every reference into STYLE references (which teach the look and feed the pack) versus ASSET references (which supply a specific thing), builds the folder taxonomy and an INDEX, and defines which references get attached to which generation in Lovart. Each project has its own design, so this runs fresh per project and never inherits another project's references. Use when starting a project's visual work, when new reference screenshots arrive, when deciding what to attach to a generation, or when a generated image does not match the reference. Triggers on references folder, which references to attach, reference intake, new reference screenshot, assemble in lovart, design references, reference index, doesn't match the reference.
---

# Motion Design References

## Why this step exists

**Every project has its own design.** The pipeline and the ten-slot schema stay constant; the look does not. So references cannot live in the skill — they live in the project, get inventoried per project, and feed that project's STYLE PACK. Nothing is inherited from a previous project unless the user says so explicitly.

The failure this prevents: a folder of forty screenshots that nobody has classified, so at generation time the wrong three get attached, or the same "vibe" reference gets attached to everything and every frame drifts toward it.

## Law 1 — inspect before you ask

**Never ask the user what is in the folder. Look, then report what is actually there, then ask.**

1. List the references folder recursively. Report counts and what each file actually depicts — open them, do not guess from filenames.
2. Present the inventory.
3. **Then** ask the user to assign roles: which reference is the main character, which are secondary, which teach the look, what the aspect ratio is (never infer it — always ask).

## Law 2 — every reference is either STYLE or ASSET

This single split decides everything downstream. Ask of each file: **does it teach the look, or supply a thing?**

| | STYLE reference | ASSET reference |
|---|---|---|
| Answers | *how should this look* | *what exactly is this* |
| Feeds | the STYLE PACK slots | the generation as an attached image |
| Examples | a Vox frame, a poster, a palette, a type specimen, a texture | this character's face, this room's angle, this specific prop |
| Attached to a generation? | usually as the style sheet only | yes, per shot |
| Reused? | once, into the pack | every time that thing appears |

A file can be both — a frame that teaches the look *and* contains the hero prop. Then it is filed twice, with a note, never silently in one place.

## Law 3 — read the reference concretely before naming it

Do not shortcut to a style label ("looks Vox", "kind of Wes Anderson") and generate from the label. Before a reference feeds anything, write down in concrete terms:

- **Color blocking** — which areas carry which color, in what proportion, what is deliberately empty
- **Placement** — where the subject sits in frame, where weight and eye go
- **Composition** — symmetry, horizon, margins, how crowded
- **Edge and finish** — how forms terminate, grain, texture
- **Emphasis mechanism** — what makes one element dominant here

That description is what feeds the pack. The label feeds nothing.

## Law 4 — if the reference folder contains written prompts, they outrank mood

If a reference folder ships full text prompts alongside images, **copy their pattern** — exact fabric and color words, named props, how locations are described — into the script and into generation. Do not demote them to mood-board inspiration and write your own looser prompts.

## Folder taxonomy

```
<project>/
  STYLE-PACK.md
  references/
    INDEX.md
    style/            ← teach the look; feed the pack
      palette/  type/  texture/  composition/  motion/
    assets/           ← supply a thing; get attached per shot
      characters/<name>/
        source/       raw photos, as supplied — never edited, never moved
        locked/       APPROVED generated images — these are the reference from now on
      locations/<name>/
        establishing/ the master angle for the scene
        angles/
      props/<name>/
    working-details/  ← screenshots pulled from test generations, pending classification
```

**Originals stay put.** Anything the user supplied is never moved, renamed or overwritten; outputs go into the project folder.

## The lock rule

Once a character's first portrait is approved, **that approved image becomes the reference for every later appearance** — not the raw source photo. Same for a location's establishing shot and a prop's first clean render. Going back to the raw photo re-rolls identity and the face drifts.

`assets/*/locked/` is the only folder generation reads from. `source/` exists to make the locked image, once.

## INDEX.md

One row per reference. This is what gets consulted at generation time, not the folder listing.

| ID | File | Class | Depicts | Feeds | Locked? | Notes |
|---|---|---|---|---|---|---|
| `CHR-01` | assets/characters/anna/locked/portrait-v3.png | ASSET | Anna, 3/4, neutral | every Anna shot | ✅ | approved 01-09 |
| `STY-04` | style/composition/vox-frame-02.png | STYLE | halftone cutout + offset stroke | PACK: EDGE, DEPTH | — | |

## Assembly for Lovart

Before any generation, state the attachment set explicitly:

1. **The style sheet** — one image, always, carrying the pack.
2. **Character locks** — the approved image for each person in frame, plus their real face photo when identity must hold exactly.
3. **The location's establishing shot** — the master angle for that scene.
4. **Prop references** — only for props actually handled in this shot.

Keep the set tight. Every extra reference dilutes the ones that matter. If the platform caps references, drop prop references first, location second, never the character lock or the style sheet.

For sequential coverage inside one scene, use the validated pattern: `Change to <next beat>:` + the approved previous image + the real face photo + the exact mandatory face clause.

Companion skills for the mechanics: `storyboard-reference-assembly` (per-panel attachment sets), `detail-reference-intake` (new screenshots from test generations), `loveart-video-animation` (platform specifics).

## Gate before generation starts

1. Folder inspected and inventoried — not assumed?
2. Every reference classified STYLE or ASSET?
3. Aspect ratio stated by the user, not inferred?
4. STYLE PACK filled from the concrete readings, with untested numbers marked?
5. Every recurring character, location and prop has a **locked** image?
6. INDEX.md written?
7. Attachment set named for the first shot?

Anything unchecked → fix it now. A frame generated against an unclassified reference folder will be reshot.

## Hand-off

References indexed and locked → `motion-remotion-build` (CODE) or `motion-video-route` (VIDEO), per shot.
