# Material selection

The trailer is cut from the project's own approved frames and clips. This step finds them, ranks them by the look, shows
what must not be used, and ends with the user approving the pick. Source folders are read-only throughout.

## 1. Context first (reuse, do not rebuild)

Run the context step of `otf-presentations` (its `otf_context.py`) with the project's reference folder, final frames folder,
clip folders and `STYLE_LOCK.json`. Take from its manifest:
- the look metrics and palette (the ranking target);
- the source prompts embedded in the reference PNGs (Midjourney `Description`, `parameters`, `prompt`): their vocabulary
  is reused in any missing-shot prompt;
- the glyph-tested font pairing (add `--cyrillic` when any version is in a Cyrillic language);
- text docs: logline, beats, shot list, story notes.

If the project has no style lock, ask whether to make one with `style-lock-guard` (`init` from the director's key frames)
before ranking. Without it, ranking falls back to the references' average metrics, then to generic contrast and saturation.

## 2. Inventory and rank

```
python3 scripts/pick_material.py <project> --out <project>/trailer/<run>/material \
  --style-lock <project>/STYLE_LOCK.json --format 16:9 --top 24
```

What it does:
- walks the project (hidden folders, `trailer/` and earlier outputs are skipped) and lists every still and clip;
- probes clips (duration, size, fps) and pulls three small preview frames per clip into its own `_frames/` folder;
- measures the look with the same metrics and score as `otf-presentations`, turns it into a 0-100 percentile, and adds a
  bonus for clips that really move (`--clip-bonus`, default 15) and for material in approved folders (`--approved-bonus`);
- writes `material.csv` / `material.json` with paths relative to the project, `contact_sheet.jpg` (top N usable) and
  `rejected_sheet.jpg`.

### Status (from the path)

| Status | Path contains | Use |
|---|---|---|
| `approved` | approved, final, selects, keep, hero, animation | First choice |
| `unreviewed` | none of the markers | Usable after the user sees it on the sheet |
| `unapproved` | wip, draft, test, tmp, preview, proxy | Only if the user picks it by name |
| `rejected` | rejected, discard, trash, unused, `_orig`, bad, failed | Never, unless the user rescues it by name |

If the project keeps approval somewhere else (a shot-list tracker, a storyboard page, a `generation-log`), read that too and
override the path status. Say which source you used.

### Flags

| Flag | Meaning | What to do |
|---|---|---|
| `short` | clip under `--min-clip` seconds | Only for the peak cluster |
| `near-static` | the clip barely moves | Treat as a still: needs a second motion layer or a generated clip |
| `fpsNN` | not 24 fps | Conform before the edit; never let the renderer retime silently |
| `aspect` | does not match the target format | Reframe with `frame-crop-guard`, or skip |
| `lowres` | would need more than 1.4x upscale | Do not use at full frame |
| `error:...` | unreadable file | Report, never guess |

## 3. Build the pick

1. Look at `contact_sheet.jpg` yourself, then open the best candidates at full size. Run `style-lock-guard compare` on the
   top stills; anything it calls `FLAT` drops out.
2. Fill the coverage matrix in the plan: one row per beat of the chosen structure, the shots that cover it, and the gap.
3. Rules for the pick:
   - **Moving first.** A clip beats a still for every beat; a still is used only as a living still (3-8 % push plus one
     moving layer) and never more than about a quarter of the shots.
   - **Every take once.** A shot may come back only as a deliberate callback (open and end).
   - **Faces in about one shot of three or four.** Backs, hands, silhouettes and details hide identity drift. Check every
     face that is used with `frame-qc-contact-sheet` (`face_crops.py` against the identity reference).
   - **Scale alternation.** Never two neighbours at the same scale; the matrix shows scale per shot.
   - **One palette.** A shot that breaks the hue family is either graded with `video-color-grade` or dropped.
   - **Trim handles.** AI clips often start on a frozen or morphing frame and degrade at the tail: plan `src_in` after the
     first 6-12 frames and stop before the motion breaks.
   - **Must-show and banned** from the chat override the ranking in both directions.
4. Build the pick sheet for the user: `frame-qc-contact-sheet` (`contact_sheet.py`) on the picked stills and preview frames,
   in trailer order, plus the list of beats that have no material (they become generation requests).

## 4. Gate: the user approves the pick

Show: the pick sheet, the coverage matrix, the rejected sheet if it holds anything tempting, and the gaps. Proceed only on a
yes. Record the approval (date, any changes the user made) in `TRAILER_PLAN.md`.
