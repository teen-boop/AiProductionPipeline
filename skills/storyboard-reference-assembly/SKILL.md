---
name: storyboard-reference-assembly
description: Assembles and verifies the complete set of locked reference images (character, recurring subjects/objects, exact location angle, props/details) that must be attached to a storyboard panel or shot before it is generated. Use when building a storyboard/raskadrovka, writing per-panel or per-shot prompts, deciding which reference images to attach, or checking whether a generated panel actually matches the project's canonical assets. Triggers on storyboard panel, raskadrovka, which references to attach, missing prop reference, panel doesn't match the reference, shot reference check.
---

# Storyboard Reference Assembly

## Why this exists

A concrete failure this skill fixes: a storyboard panel set in a previously-locked location was generated with a *plausible-looking but wrong* room — different bookshelf, different window, different lamp — because the panel's own one-line shot description ("she opens the laptop") didn't explicitly re-list every object in that room. The room reference existed in the project's locked-reference library the whole time; it just wasn't attached. A plausible room that is not the canon room is a failure, not an acceptable variation — the whole point of a locked reference is that it stops being negotiable once approved.

This skill is the checklist step that runs **before** any panel/shot prompt is finalized, so this class of miss cannot happen silently.

## When this runs

At the storyboard-building stage of `loveart-video-animation` (Stage 3 / panel construction), for every single panel or shot, before generation — whether panels are generated one-per-call or combined into one multi-panel sheet in a single call.

## Process

1. **Read the project's locked-reference index in full first** (e.g. `LOCKED-REFERENCES.md` or equivalent). Do this once at the start of the storyboard session, not per-panel from memory — memory drifts, the file doesn't.

1a. **If a `script-extractor` breakdown (or equivalent per-scene detail
   extraction) exists for this project's source material, read it too, in
   full, at the same time.** It answers a different question than the
   locked-reference index: the index tells you which asset file a noun
   maps to; the breakdown tells you what should be true for this shot's
   scene in the first place — its day/night value, which characters are
   present, what they're wearing, what location it's in. For any shot
   traceable to one of its scenes, pull day/night, wardrobe, and location
   facts from that scene's entry (and the cross-reference index for
   anything recurring), rather than re-reading the original source text or
   guessing from the shot's short description alone. Treat an
   **[inferred]** value in the breakdown as a resolved fact to carry
   through, not an invitation to pick something else.

2. **For each panel/shot, extract every noun that could map to a locked asset**, not just the subject of the one-line shot description:
   - The main character (always, if present in frame).
   - Every recurring subject/object present or implied by the script at this point in the story (pet, secondary character, prop, vehicle).
   - The location this shot happens in, and the specific *angle* if the location has multiple locked angles.
   - Every prop/detail that canonically belongs to this location or moment, even if the shot's short description doesn't name it (e.g. a shot description "she opens the laptop" still happens in a room that has a canon lamp, bookshelf, window, mug, plant — all of it, not just the laptop).

3. **Cross-reference each extracted noun against the locked-reference index.** For every match, resolve it to the exact file path or URL of the canonical asset — never a re-described or re-imagined version of it.

4. **A previously-established location's canonical reference is mandatory, not optional**, for any shot set there. Never let the generation model improvise an unreferenced room just because the text alone would produce *something* plausible. If the location has multiple locked angles, pick the angle that matches the shot's framing (or the one already used as that location's chained master — see `loveart-video-animation`'s master-shot chaining rule).

5. **Attach every matched reference to the generation call.** Do not thin out the attachment list to keep the prompt simple — if in doubt, attach it. Extra correct references cost nothing; a missing one produces silent drift.

6. **If a shot needs a prop/detail with no locked reference yet**, do not invent its appearance silently. Either generate and lock that reference first (per `loveart-video-animation` Stage 2), or flag it to the user before proceeding.

7. **Produce a short manifest per panel before generating**, and keep it next to the shot list:
   ```
   Panel 3 references: character (CANONICAL_prototype.png) + cat (CANONICAL_cat_prototype.png)
                        + location: desk_empty.png (angle1) + prop: sketchbook_portrait_state1.png
   ```
   After generation, check the result against this manifest, not just against the prose description — a missing bookshelf or a swapped lamp is a manifest violation even if the shot "looks fine" in isolation.

## The Canon Location Plate Is Not Optional, Even When Secondary Photos Exist

A location often has both (a) its canonical empty/clean location plate (e.g.
`kitchen_empty.png`) and (b) secondary in-scene photos that happen to be set in that
location (e.g. a photo of the cat drinking milk, a photo of ramen being poured). Secondary
photos are useful for prop/action detail, but they are NOT a substitute for the canon plate
- attaching only secondary photos and skipping the canon plate lets the model invent a
generic version of the room that can look nothing like the actual established location
(a real failure: a canon kitchen that is a dense apothecary workshop with dried herbs
hanging from the ceiling and dozens of labeled jars came back as a generic tiled kitchen,
because only the secondary action photos were attached and the canon plate was left out).
Always attach the canon location plate itself, first, and state explicitly in the prompt
that it is the locked room every panel must be staged inside - secondary photos are
additional prop/action references layered on top of it, not a replacement for it.

## Common miss patterns to check for explicitly

- A location shot attaches the character/recurring-subject references but omits the location's own canonical plate, letting the model invent the room.
- A prop that recurs across multiple scenes (a specific mug, a specific book) is described in text each time instead of referencing its one locked image, causing it to drift in appearance between panels.
- A shot in a location with multiple locked angles attaches the wrong angle (or no angle), instead of the one matching the requested framing or the location's established master.
- A background detail visible only "at the edges" of frame (a bookshelf behind the subject, a window's exact shape) is treated as unimportant and left unreferenced, when the location's canon includes it.
- A shot's day/night value drifts from its scene's script-extractor entry (e.g. a scene resolved as NIGHT gets a daylight-lit panel) because the prompt was written from the shot's short description alone instead of checking the breakdown.
- A character's standing wardrobe rule from the cross-reference index (e.g. "always wears a dark suit and sunglasses") is dropped or contradicted in one panel because it wasn't re-checked against the index for that shot.

## Color Fidelity (Non-Negotiable for Color Storyboards)

When a storyboard panel is generated in color (not a black-and-white sketch previz), the
panel's color grade, lighting temperature, and palette must match its attached location/prop
references exactly, not just approximately. This project has a documented history of color
and light drifting away from established references during generation (a past batch was
rejected outright for this reason). To prevent a repeat:

- Attach the actual color reference images (the location plate, the specific prop
  close-ups involved in the shot) every time, never rely on a text color description alone.
- State explicitly in the prompt: "match the exact color grade, lighting warmth, and
  palette of the attached reference images - do not reinterpret or shift the colors."
- After generation, check the panel's colors against the reference side by side, not just
  its composition/content - a compositionally-correct panel with drifted color/light is
  still a failure for this project.

## Output

Before generation, output the full manifest for every panel in the batch, so a human (or a follow-up check) can scan it in one pass and confirm nothing that should be attached was left out.
