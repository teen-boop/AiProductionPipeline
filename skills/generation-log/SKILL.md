---
name: generation-log
description: >-
  Keeps ONE append-only log of every generated file (image, video, audio, 3D) in 03_GENERATED/GENERATION_LOG.jsonl: id
  (G0007), file, content hash, size/duration, tool, model, full prompt, references used (resolved to library ids like R020),
  params (duration, seed, aspect, resolution), cost and unit, shot code, job id, parent take, status (candidate / approved /
  rejected). Files are matched by content, so a take renamed or copied into the edit bins still finds its prompt. Commands:
  add, find, status, recipe (everything needed to regenerate a take or a shot), report (takes, approval rate and spend by
  model / tool / day / shot) and missing (files with no record, to backfill). Use right after EVERY generation that is
  downloaded, when the user asks "what prompt made this", "repeat this take", "how much did we spend", "which model worked
  best", before the edit, and when cleaning up. Includes scripts/genlog.py.
user-invocable: true
---

# Generation Log

A generated take without its prompt, model and references cannot be repeated or fixed. The log is the memory of the
project: one line per output file, written the moment the file lands on disk.

## Record

```json
{"id": "G0007", "time": "2026-11-09T11:42:10", "file": "/…/03_GENERATED/VIDEO/S03_take02.mp4", "hash": "8266790:ab12…",
 "w": 1920, "h": 1080, "duration": 10.0, "tool": "higgsfield", "model": "seedance_2_0",
 "prompt": "<the full prompt exactly as sent>", "prompt_file": "/…/02_PROMPTS/S03.md",
 "refs": ["R020", "R031"], "params": {"duration": 10, "resolution": "1080p", "seed": 1234},
 "cost": 40, "unit": "credits", "shot": "S03", "job_id": "…", "parent": "G0004", "status": "candidate", "note": ""}
```

- `refs`: pass ids or file paths; paths that are in REFERENCES_INDEX.csv are turned into their ids.
- `parent`: the take this one was built on ("change to" chains, edits, extensions, upscales).
- `cost`: the price the tool reported or confirmed, with its unit (`credits`, `usd`, `free`). Never invent one; leave it out
  if unknown.
- Status changes are appended as new lines; nothing in the log is ever rewritten or deleted.

## Workflow

1. **After every generation**, in the same step that downloads the result:
   ```
   python3 scripts/genlog.py add --project P --file "<out1>" [--file "<out2>"] --tool lovart --model nano_banana_2 \
     --prompt-file "<project>/02_PROMPTS/S03.md" --refs R020,R012 --cost 0 --unit free --shot S03 --params '{"aspect":"16:9"}'
   ```
   A batch from one prompt = one `add` with several `--file`. Download into `03_GENERATED/{IMAGES,VIDEO,AUDIO}`.
   A prompt is mandatory; the script refuses without one.
2. **When the user approves or rejects**: `genlog.py status --project P --id G0007 approved` (or `rejected`). Rejected takes
   go to `03_GENERATED/_rejected/` only with the user's yes; every organizer skips that folder.
3. **"What made this?"**: `genlog.py find --project P "<any copy of the file>"`.
4. **"Do it again / fix shot 3"**: `genlog.py recipe --project P --shot S03` lists approved takes first, with prompt,
   model, refs and params. Re-generate from that, then log the new take with `--parent`.
5. **Spend and quality**: `genlog.py report --project P --by model` (or `tool`, `day`, `shot`). Use it to answer "how much
   did we spend" and "which model gets approved most", and before asking the user to confirm the next paid batch.
6. **Backfill** an old project: `genlog.py missing --project P --path "<folder>"`, then add records for what can still be
   reconstructed (prompts files, tool history). Mark unknown fields as unknown in `--note`, never guess a prompt.

## Rules

- English only in tool, model, shot, params and notes. The prompt is stored exactly as sent, in whatever language it was.
- Never log a cost that was not confirmed; every paid batch still needs the user's yes on the exact price first.
- The log lives with the project and is never published (it contains prompts and private reference paths).

## Related skills

`project-scaffold` (creates 03_GENERATED), `reference-library-organizer` (ref ids; logged files count as INTERNAL),
`edit-media-bins` (copies takes; find still works on the copies), `versions-and-archive` (uses status to clean up),
`generation-queue-runner` (can call `add` after each job).
