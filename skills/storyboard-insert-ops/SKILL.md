---
name: storyboard-insert-ops
description: >-
  Rules for placing delivered frames into a script-ordered storyboard through declarative ops (replace, remove, fill, after, before,
  rebuild_beat, *_late variants) so that new frames land in the right beat, replacements take the old frame's slot, re-done frames
  supersede their earlier versions, and nothing is lost when a whole beat is rebuilt. Use when adding new shots to an existing storyboard,
  replacing or fixing frames, rebuilding a beat, or when a delivered frame "did not show up" or showed up twice.
user-invocable: true
---

# Storyboard Insert Ops

The storyboard is a list of beats in script order. Each beat holds an ordered list of frames. Delivered frames are not hand-edited into
it. Each job maps to an **op**, and the builder applies all ops in a fixed order every time, so the result is reproducible.

## Ops

| Op | Effect |
|---|---|
| `replace` | Put the new frame in the slot of `match` (by file name). Applied first. |
| `remove` | Drop the frame `match`. |
| `fill` | Fill an empty "missing frame" slot whose label contains the text. |
| `after` / `before` | Insert next to the anchor `match`. Consecutive `after` ops on the same anchor keep their order: each one goes after the previously inserted frame. |
| `rebuild_beat` | Replace the whole frame list of a beat (a beat that was re-shot). Applied late. |
| `after_late` / `before_late` | Like after/before, but applied **after** `rebuild_beat`. Use these for anything added into a beat that is or may be rebuilt. |
| `replace_late` | A replacement applied last. Use it when the target is itself an inserted or rebuilt frame. |

Order of application: replace → remove → fill → after/before → rebuild_beat → *_late inserts → replace_late → **fixes of fixes**.

## Rules that prevent the classic bugs

- **New frames vanish.** They were inserted with `after` into a beat that `rebuild_beat` later re-created. Use `after_late` or
  `before_late`.
- **A fix is overwritten.** You replaced `X_idfix1.png`, but an earlier job turns `X.png` into `X_idfix1.png` later in the order. Put
  fixes whose target contains `_idfix` into a final "late2" list, after everything else.
- **Two versions of one shot.** A redo is delivered as `…_2.png`. Place only the **latest delivery per job** (`rs[-1]`). Never place
  every delivery.
- **Duplicate numbers.** Assign stable storyboard numbers with a `taken` set: `0170`, `0170a`, `0170b`, … Never reuse a number.
- **Labels cut off in file names.** Exported names often cut at `:`, so a label like "elite and poor: Hyde Park" becomes "elite and poor".
  Write labels with ` — `, never `:`.
- **Wrong anchors.** Anchor on a frame that will exist after all ops have run (check its file name in the built storyboard), not on a
  frame that a replacement renames.

## After every build, verify

- [ ] Count the frames per beat before and after the build. The difference equals the frames you delivered.
- [ ] Grep the built storyboard for the new file names. Each one appears exactly once, in the intended beat and position.
- [ ] The replaced frames no longer appear.
- [ ] Rebuild the downstream outputs (video prompts and the animation folder; see `animation-handoff-folder`).
