---
name: detail-reference-intake
description: Watches a project's "working detailed references" folder for new screenshots/stills captured from test generations or test animations, identifies what specific reusable detail each new file shows, and locks it into the project's canonical reference index so every later generation stage (storyboard, full panels, video) uses it. Use at the start of any work session on a project that has this folder, before storyboarding or generating new panels. Triggers on working detailed references, new reference screenshot, detail from test generation, catalog new prop reference, folder has new stills.
---

# Detail Reference Intake

## Why this exists

Not every reusable visual detail is planned in advance. Often the best version of a small recurring object (a cup, a jar label, a piece of furniture) shows up as a side effect of an unrelated test — a test animation render, a still frame, an experiment that wasn't primarily about that object at all. The user's workflow for capturing these is simple: screenshot the good frame, drop it into the project's `working detailed references` folder. Nothing about the filename or the moment it was captured says what detail it's actually good for — that has to be figured out by looking at it.

Without a deliberate intake step, these files just sit in the folder, get referenced verbally from memory ("that matcha cup, it's small"), drift, or get forgotten entirely by the next generation batch. This skill is the step that turns "there's a new file in the folder" into "this is now a locked, named reference used everywhere it applies."

## Folder convention

Every project has (or should have) a folder at:
```
reference/working detailed references/
```
This is distinct from `reference/props/` (deliberately-generated, already-cataloged detail assets) and from `reference/locations/_empty_no_character/` (deliberately-generated location plates). Files here are raw captures — often named by their source tool (e.g. `Still 2026-08-29 164500_1.2.1.png`), not by content. Treat the filename as a source ID, never as a description.

## When this runs

At the start of any work session that touches this project, before storyboarding (`storyboard-reference-assembly`, `storyboard-continuity-tracker`) or generating any new panel. Also whenever the user mentions they've added something to this folder.

## Process

1. **List the folder and diff against what's already catalogued.** The project's locked-reference index (e.g. `LOCKED-REFERENCES.md`) should have a section listing which source filenames from this folder have already been catalogued (see Output below). Any file in the folder not listed there is new and needs intake.

2. **Look at every new file directly** (do not skip this — the filename tells you nothing). For each one, determine:
   - What specific, reusable detail does this frame actually show clearly? (an object, a prop, a piece of furniture, a texture, a specific lighting treatment, a label design — anything concrete and nameable.)
   - Is it a genuinely NEW detail (nothing like it is locked yet), or does it show an EXISTING locked subject/location from a new angle or lighting that's worth keeping as an alternate reference?
   - Is it usable on its own (e.g. a clean close-up of one object), or does it only make sense as supporting context (e.g. a blurry secondary element visible in a shot that was really about something else)? Only catalog what's actually clear and usable.

3. **Name and describe each new detail like any other locked reference** — a short canonical name, a concrete visual description (materials, size, color, distinguishing marks), and the source file. Example:
   ```
   Matcha cup: small ceramic cup, speckled grey-cream glaze with faint brown/rust speckling,
   simple rounded shape, small enough to be held in both hands.
   Source: working detailed references/Still 2026-08-29 164500_1.4.1.png
   ```

4. **Add each new detail to the project's locked-reference index** (`LOCKED-REFERENCES.md` or equivalent), in a dedicated section for details sourced this way, so `storyboard-reference-assembly` picks it up like any other canonical asset in its checklist pass.

5. **Mark the source file as catalogued** (add it to the "already processed" list in the same section) so the next intake pass doesn't re-examine it.

6. **If a new file conflicts with an existing locked detail** (e.g. it shows the same object but different from what's already canon), do not silently overwrite the lock — flag the conflict to the user and ask which version is canon going forward.

## Output

Update the locked-reference index with a section shaped like:

```
## WORKING DETAILED REFERENCES (from test generations)

Folder: reference/working detailed references/

Catalogued:
- [detail name] — [description] — source: [filename]
- [detail name] — [description] — source: [filename]

Not yet catalogued / needs review: [filenames, if any are ambiguous or unclear and need the user's input]
```

Any detail catalogued here is now mandatory input for `storyboard-reference-assembly` whenever a shot involves it — treat it exactly like a deliberately-generated prop reference, not as a lesser or optional source.
