# Character identity lock

## The rule

Whenever a real face-reference photo exists for a character, attach it as one of the image
references — every single generation, no exceptions. This holds even when also attaching a base/scene
image (e.g. for a "Change to..." variant, see `04-prompt-engineering.md`) or a character sheet —
attach the face photo together with them, not instead of them. Never rely on a base image or sheet
alone to carry identity forward, even if it already shows that character's face correctly.

## Canonical reference lock-in

Once a character's first portrait is approved as excellent, that GENERATED IMAGE becomes the
character's canonical reference from then on — not just the raw face photo.
- Attach BOTH the real face photo (identity ground truth) AND the approved portrait (locked
  costume/style/treatment) when generating any later scene featuring that character.
- If the character has a character sheet (see `assets/character-sheet-*.md`), attach that too.
- This matters most for multi-character/group shots — pull in each person's approved portrait and
  sheet, not just their raw photo.
- If a scene was generated using only the raw photo before an approved portrait existed, it's worth
  re-running once the portrait exists rather than treating the raw-photo-only version as final.

**Attachment order:** master shot (if applicable) → character sheet (if one exists) → real face
photo → approved portrait.

## Multi-character shots — one face reference per person, always

If a frame contains more than one named character, attach each character's own real face photo (and
approved portrait/sheet) as separate reference images — never let one photo implicitly cover a
second person's identity, even if the model renders them plausibly. One face photo per person in
frame, every time.

## Mandatory face clause

Append this exact clause to every prompt with a visible character face:

> "Maintain precise facial proportions and identity, and keep the eye color exactly as in the
> reference — use my image with accurate face 100%."

Spell out every clothing/prop detail in full every time (color, material, embroidered text,
placement) — never shorthand an established costume as "his usual uniform."

## Character rework = persona AND narrative function, always together

When a character's visual persona/reference is reassigned or significantly reworked (new look, new
vibe, new reference photos), that is not just a portrait update — the character's actual role in the
story must be reworked to match, in the same pass. A persona isn't decoration; it's who the
character IS, and who they are determines why they're in a scene and what they're doing there.

How to apply:
- Never treat "new look" and "new story function" as separable tasks. A character-rework request
  isn't done until both are updated together, in the same pass.
- Give the reworked persona a concrete GOAL that explains their action in their scene(s) — not a
  generic bystander errand dressed in a new costume. The persona should drive the plot beat, not the
  other way around (e.g. a scientist's action should be scientist-appropriate; a traveler's action
  should tie to travel).
- A "true self" bonus-reveal montage bolted onto the finale is not a substitute for rewriting the
  actual plot beat the character occupies. Don't reach for that shortcut.
- **Before generating any production images for a reworked character, run a small test batch of the
  NEW scene action/goal specifically, and get the user's explicit confirmation that the direction is
  understood correctly** — before reworking the rest of the story or generating full coverage. This
  is narrower than, and in addition to, the general project test-batch gate: it exists specifically
  to catch a misunderstood creative direction early, before it propagates through an entire
  character's rewritten scenes.

## Full identity change vs. minor identity correction — different techniques

These are two different situations that need different handling — don't apply one where the other
belongs.

**Full identity change** (the character's identity/persona is being genuinely swapped or
fundamentally reworked, per the rework rule above): once it happens, treat every prior generation
made under the OLD identity as obsolete for that character. Do not reference them as continuity, do
not try to blend old-look and new-look shots, do not carry forward "how they looked in shot 3" as an
implicit constraint. Regenerate whatever shots are needed against the NEW reference only, from a
clean slate for that character. Trying to preserve continuity with a discarded identity is what
causes drift and half-updated scenes — cut the cord fully instead.

**Minor identity correction** (same character, a corrected reference photo or a small costume-detail
fix — NOT a wholesale identity change): don't regenerate every shot from scratch. Patch existing
delivered shots in place instead — see `08-qc-and-fixes.md` for the exact technique.
