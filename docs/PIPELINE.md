# AI Production Pipeline (One Two Film) — step by step

| Step | What happens | Skills | Output in the project |
|---|---|---|---|
| 0. Backend | Connect a CLI / API / MCP generator, or choose manual mode | `generation-backend-setup` | `pipeline.config.json` (env var names only) |
| 1. Script | Parse the screenplay or prose into scenes, locations (day/night), characters, props, wardrobe | `script-extractor`, `visual-story-2-script` | script breakdown + cross-reference index |
| 2. References | Collect, view, assign roles and sort references; lock every character's face per age | `organize_refs.py`, `character-identity-lock-setup`, `detail-reference-intake` | `references/<Category>/<name>/…` + `INDEX.md` |
| 3. Shot list | Prose → numbered shots, shot sizes justified, camera and state continuity tracked | `storyboard-narrative-breakdown`, `storyboard-shot-selection`, `storyboard-camera-continuity-ledger`, `storyboard-continuity-tracker` | shot list + ledgers |
| 4. Frames | Per shot: resolve references, write the still prompt, generate (backend) or pack it (manual) | `storyboard-reference-assembly`, `cinematic-prompt-writer`, `manual-image-pack` | frames in `generated/…`, or `MANUAL_GEN/` |
| 5. QC | Format, identity, period, optics, story beat; reject with a reason and a prompt fix | `visual-story-7-platform-qc`, `manual-image-pack` intake | `_rejected/` with reasons |
| 6. Video | One frame = one clip; small motivated camera moves; colour lock; first+last pairs only from change-to frames | `cinema-director-v3`, `seedance-prompt-writer`, `video-clip-continuity-chain` | per-frame video prompts |
| 7. Storyboard | Frames in script order with labels; a checklist of clips | `visual-story-8-storyboard`, `seedance-shotlist-tracker` | storyboard sheet + tracker |

## Two working modes

- **Connected.** Claude calls your generator directly and respects your parallel limit. It never re-submits a job whose remote task is still running, and it adopts late results.
- **Manual.** Claude writes everything and packs it, and you click "generate". Each frame folder holds `PROMPT.txt`, the numbered reference images and an `INFO.txt`. Save `RESULT_1.png` into the folder and say "collect the frames".

Both modes produce the same project layout, so you can switch between them at any time.

## Principles

- **References first, then generation.** Every prompt names the exact reference files to attach and what each one means.
- **Change-to, not re-roll.** Close-ups and next moments are re-framed from the master frame, which keeps faces, light and colour identical.
- **Accuracy lives in the prompt.** Period, object and continuity rules are written into each prompt, not left to memory.
- **Film still, not AI poster.** Every prompt carries the LOOK and OPTICS blocks (see `PROMPT_STYLE_TEMPLATE.md`).
