---
name: visual-story-4-references
description: STEP 4 of 8 in the sequential visual-story pipeline. The reference-building step. For each scene, extract every character, location, and recurring prop from the scene's prompt, and generate a locked reference sheet for each one using a single shared 4-part template (character / location / prop sheets all share the same structure). This is what keeps people, rooms, and objects consistent across scenes. Run AFTER visual-story-3-cast-world. Next step: visual-story-5-exposition.
---

# Visual story — Step 3: Reference sheets (characters, locations, props)

**Step 3 of 5.** Before this: `visual-story-2-script` (a finished script segmented into numbered
scenes). After this: `visual-story-6-production`.

This is the step that most directly prevents the drift failure mode — people, rooms, and objects
looking different every time they're generated. The fix is the same for all three: build a locked
reference BEFORE using them across scenes, then attach it every time.

**The output of this step is a Production Design Guide — a design "bible" for the whole story, not a
pile of loose images.** The intended pipeline (confirmed by the user with reference examples): **story
→ break it down into this reference bible → then storyboard.** Read
`references/production-design-guide.md` — it defines the two tiers (polished per-item design sheets +
one consolidated Production Design Guide board with CHARACTER DESIGN / PROPS / SET DESIGN / NOTES FOR
ART DEPARTMENT sections) and the order of work. Do the whole bible before storyboarding
(`visual-story-8-storyboard`).

## The extraction pass — do this per scene, from the script

For each scene's prompt/description, read back through the text and **literally extract**:
- every **character** who appears,
- every **location** the scene uses,
- every **recurring prop/object** (a telephone, an invention, a vehicle, a cart) that appears here
  or is set up to reappear later.

This is a concrete extraction over the prompt text, not a vague "keep an eye out."

## Build a reference sheet for each — one shared template shape

All three sheet types use the **same 4-part structure** (Subject description → Layout of views →
Style & Consistency → Requirements). Don't improvise a different shape per item — the consistent
template is what makes these reliable to generate and QC the same way every time.

| Item type | Template | What it is |
|---|---|---|
| Character | `assets/character-sheet-prototype.md` (**default for anything animated or recurring**) / `character-sheet-basic.md` (minor) / `character-sheet-full.md` (leads) / `character-sheet-state.md` (locked wet/injured/costume state) | Prototype map: 4 close-up head angles in a 2x2 grid on the left + one headless full-length on the right, nothing in the hands. Real face photo attached |
| Location | `assets/location-sheet-basic.md` | 4-angle turnaround of the room |
| Prop | `assets/prop-sheet-basic.md` | 4-view turnaround of the object |

**Locations also get a practical first reference:** the scene's main character shot framed so the
room behind them is clearly visible — this doubles as the location's working reference and goes
straight into production use, alongside the turnaround sheet. Full workflow, folder structure, and
the "ask when unclear whether something needs a reference" rule are in
`references/location-and-prop-references.md`.

## The lock-in rule (applies to everything built here)

Once a reference sheet is approved, it becomes canonical — attach it to every later generation that
includes that character/location/prop, the same way a character's real face photo is always
attached. For characters specifically, the face-photo + approved-portrait + mandatory-clause rules
are in `references/character-lock.md` — read it; those rules are load-bearing and were established
through direct correction.

## Save into the folder structure from step 1

- Reference sheets → `01_References/Characters|Locations|Props/<name>/`
- Keep old versions (rename with a suffix), never overwrite.

## Test-batch gate before mass production

Before generating a whole scene's coverage, generate a small sample and get explicit user approval
on style, color, identity-lock, aspect ratio. Don't batch-produce against unapproved references.

## Order of work (from `production-design-guide.md`)

1. Fill in the **NOTES FOR ART DEPARTMENT** first — Tone / Time / Palette / Texture / Theme — because
   every sheet must obey it (this also seeds the STYLE LOCK block used in step 4).
2. Extract every character, prop, and location from the script.
3. Generate + approve each per-item design sheet, each obeying the notes/palette.
4. Assemble the consolidated Production Design Guide board from the approved sheets (assemble the
   approved sheets into the layout — don't try to generate the whole multi-section board in one shot;
   text labels and per-panel fidelity are unreliable that way).

## When done

The story has a complete Production Design Guide: an approved design sheet for every character,
location, and recurring prop, plus the consolidated board and the art-department notes. **Next:
`visual-story-6-production` to generate scenes, or `visual-story-8-storyboard` to storyboard — both
pull their look from this locked bible.**
