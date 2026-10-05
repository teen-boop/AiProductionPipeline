# QC, continuity checks, and identity fixes

## Image QC before delivery — actually look, every time

Before calling a generated image good, scrutinize every distinct region/panel, not just the overall
composition. Check for: blur/ghosting that doesn't match surrounding sharpness, warped anatomy,
duplicated features, text/logo errors, mismatched lighting between panels that should match, and
wrong location/background bleeding in from an unrelated reference image that was also attached (e.g.
a face-reference portrait's own backdrop leaking into a new scene). This matters most for
multi-panel outputs (turnaround sheets, group shots, montages) or generations that combine several
reference images — one bad panel/variant can hide next to good ones.

**Before treating a face/hair mismatch as a generation defect, re-check the reference photo file
itself — it may have been swapped.** If a character's face/hair suddenly looks "wrong" or
inconsistent across repeated attempts despite correct prompting, check the reference folder's file
list/timestamps for a newer photo (`find <folder> -newer <known-recent-file>`, or just re-view every
file) before assuming it's a model failure. If the photo changed, the new photo is correct and the
old approved portrait needs regenerating to match it — not the other way around. This can happen
more than once on the same project; re-check every time, don't assume it's settled after the first
fix.

## Automated continuity check — run this before delivering any coverage sequence

Whenever a shot depends on a master, a character sheet, or a locked scene detail (i.e. almost every
production shot after the first in a scene), run this checklist before marking it delivered:

1. **STYLE LOCK present and verbatim.** Diff the prompt's STYLE LOCK block against the project's
   canonical block (`04-prompt-engineering.md`) word for word. A paraphrase is a fail — it must be
   pasted, not re-typed from memory.
2. **Master attached where the shot requires it.** Any shot that isn't the scene's first
   establishing/wide must have that master image attached as a reference, not just referenced in
   text.
3. **Locked details match verbatim.** Compare the shot's clothing/prop/hairstyle/wetness-dirt
   description against the scene's fixed description string. Flag any word-level drift (a "brown
   jacket" that was "rust-brown canvas jacket" three shots ago is a fail).
4. **Weather/physical-state consistency.** If the master or scene establishes rain/snow/mud/etc.,
   confirm every character shown has the expected physical evidence of it (see
   `04-prompt-engineering.md`) — and confirm no character shows evidence of a condition the scene
   hasn't established.
5. **Face references attached, correct order, correct people.** Master → character sheet → real
   face photo → approved portrait, one full set per character in frame — no missing photo, no photo
   covering the wrong person in a multi-character shot.
6. **Visual QC pass.** Run the general image-QC checklist above on the actual output, not just the
   prompt.

Treat any single failed check as "not yet approved" — don't deliver a shot that fails this list and
plan to fix it later; fix it before it becomes the reference for the next shot in the chain, or the
drift compounds.

## Character sheet QC

When reviewing a generated character sheet (turnaround, full production, or state variant) before
locking it in as canonical:
- Every panel shows the same face, body proportions, hairstyle, and costume — check panel-to-panel,
  not just each panel in isolation.
- No panel has accidentally introduced a prop, logo, or background element not specified in the
  template.
- Background is genuinely neutral/plain as specified — a sheet with any environmental detail baked
  in will contaminate every shot that references it later.
- If any panel is off, regenerate the sheet rather than mixing panels from two different generations
  — a composite sheet built from two runs risks two subtly different faces being treated as the same
  canonical identity downstream.

## Fixing one character's identity — minor correction (patch in place)

Use this when a character's canonical look changes mid-project due to a **minor correction** (new
reference photo, corrected costume detail) — not a full identity change (see
`05-character-lock.md` for that case, which uses clean-slate regeneration instead). For each
existing delivered shot that shows the outdated look:

1. Upload the EXISTING scene image as reference #1.
2. Upload the character's NEW correct reference photo as reference #2.
3. Prompt: "Image #1 is the existing shot. Image #2 is the character's correct reference photo.
   Recreate image #1 exactly as-is — same composition, same [other elements] unchanged — but replace
   [character]'s hair/face to match image #2 exactly: [specific new features]. Maintain precise
   facial proportions and identity from image #2 for [character], and keep [other character]'s
   face/identity unchanged from image #1."

This holds the whole scene fixed and only corrects the identity, which is far more reliable than
re-describing the entire scene from text alone. The model doesn't always honor "same composition
exactly" perfectly — it can occasionally reinterpret a single continuous frame as a split/diptych
layout. Check the result against the original composition, not just the identity fix, before
delivering.
