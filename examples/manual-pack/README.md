# Manual pack example

```bash
python3 ~/.claude/skills/manual-image-pack/scripts/build_pack.py \
  --jobs examples/manual-pack/jobs.example.json --sections examples/manual-pack/sections.example.json \
  --out MANUAL_GEN --root . --lang en --style-file docs/PROMPT_STYLE_TEMPLATE.md

# after you saved RESULT_1.png files into the frame folders:
python3 ~/.claude/skills/manual-image-pack/scripts/intake.py --pack MANUAL_GEN --dry-run
python3 ~/.claude/skills/manual-image-pack/scripts/intake.py --pack MANUAL_GEN
```

`@s01_dock_wide#1` in `refs` means: use the first result of job `s01_dock_wide`. Until that frame exists, the pack holds a `.txt` placeholder. Intake swaps in the real frame as soon as it is delivered.
