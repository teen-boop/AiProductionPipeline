# Character sheet — animation prototype map

The **prototype map** is the character's single locked identity artefact for animation work: four
close-up head angles in a 2x2 grid on the left, one headless full-length body view on the right.
The head grid locks the face from every angle the animation will ever need; the headless full-length locks
body proportions and the complete costume without competing with the head column for attention.

Use this instead of `character-sheet-basic.md` whenever the character will be animated or will
recur across many shots. Fill in the brackets, reuse the rest verbatim.

```
Create a character map reference sheet of the same character, laid out as ONE single image.

Character: [age, build, facial features, hairstyle and hair length, skin tone, costume,
accessories, key identifying details]

LAYOUT — one single 16:9 landscape image, plain flat neutral background, split into two zones:

LEFT ZONE (left two-thirds of the image) — four large close-up head-and-shoulders views of the
same character in a 2x2 grid, evenly spaced, all at the same scale and the same eye level:
  top-left: front view, facing camera straight on
  top-right: three-quarter view, head turned 45 degrees
  bottom-left: side view, full 90-degree profile
  bottom-right: back view, back of the head, showing how the hair sits from behind

RIGHT ZONE (right third of the image) — one single full-length standing view of the same
character, arms relaxed at the sides, feet slightly apart, occupying the full height of the image.
CROP THE HEAD OUT of this view: the top edge of the full-length view cuts straight across the
collarbones, so nothing above the collarbones is visible: no chin, no mouth, no hair, no neck. This view exists to lock body proportions and the complete
costume.

CRITICAL: the character holds NOTHING. No props, no equipment, no bags, no balls, no rackets, no
objects of any kind in either hand. Both hands empty and clearly visible.

Style & Consistency: the same face, the same body proportions, the same hairstyle, the same
outfit, the same colors and the same accessories in every view. Even neutral lighting with soft
shadows across all views. Clean symmetrical layout, generous spacing between views, no overlap
between the head grid and the full-length view.

Requirements: plain flat neutral background only. No text, no labels, no captions, no numbers, no
logos, no watermarks, no props, no furniture, no extra characters, no cast shadows on the
background.
```

## What to attach

1. The character's **real face photo** — identity ground truth, always.
2. Any additional real photos of that person (different angles, different light) if the project's
   references folder has them — more angles measurably improve the profile and back views.
3. If the project has its own **STYLE LOCK** block (a locked painted/illustrated look), append it
   to the prompt and attach the style reference too, so the prototype is born in the final style
   rather than as a photoreal sheet that has to be restyled later.

## Costume: one prototype per costume, not one per character

If a character appears in materially different costume across the story (competition uniform vs
street clothes vs formal), generate a **separate prototype map per costume**, named
`<name>_prototype_<costume>`. The head grid is the same face each time; the headless full-length
is what actually changes. Don't try to fit two costumes into one map — the layout has exactly one
full-length slot, and splitting it breaks the body-proportion lock.

## QC before locking in

Reject and regenerate if any of these are true — they all silently poison every later generation:

- the four head views are not the **same person** (check jaw width, eye spacing, hairline, ear shape)
- the profile view is actually a three-quarter (a common failure — the far eye is still visible)
- the back view invents a hairstyle that contradicts the front view
- **a head appears on the full-length view** (the single most common failure of this layout). Watch for
  the creeping version: a sliver of chin or hair ends at the top edge, then lips on the next sheet.
  "Neck and shoulders down" was not tight enough in practice; the collarbone crop is.
- anything is in the hands
- text, labels, or numbers got generated anywhere on the sheet
- the full-length body proportions contradict the head grid's apparent age/build

Once approved, this map becomes canonical: attach it alongside the real face photo for every later
generation of this character — see `references/character-lock.md`.
