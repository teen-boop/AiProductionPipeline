#!/usr/bin/env python3
"""Render a labelled reference-map contact sheet.  ref_map_sheet.py map.json out.jpg
Paths in map.json are relative to the map file. Rows without local images are listed as text."""
import json, sys, pathlib
from PIL import Image, ImageDraw, ImageFont
m = pathlib.Path(sys.argv[1]); out = sys.argv[2]; M = json.load(open(m)); base = m.parent
W, H, COLS = 420, 236, 5
try: F = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20); FS = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 15)
except Exception: F = FS = ImageFont.load_default()
blocks = []
for row, refs in M["rows"].items():
    ims = []
    for r in refs:
        p = base / r["path"] if r.get("path") else None
        if p and p.exists():
            try: ims.append((Image.open(p).convert("RGB"), r))
            except Exception: pass
    blocks.append((row, ims, [r for r in refs if not (r.get("path") and (base / r["path"]).exists())]))
height = sum(40 + ((len(i) + COLS - 1) // COLS) * (H + 40) + 22 * len(t) for _, i, t in blocks) + 60
sheet = Image.new("RGB", (W * COLS, height), (12, 16, 16)); d = ImageDraw.Draw(sheet); y = 10
d.text((10, y), M.get("task", ""), font=F, fill=(240, 220, 180)); y += 50
for row, ims, txt in blocks:
    d.text((10, y), row, font=F, fill=(120, 220, 200)); y += 34
    for k, (im, r) in enumerate(ims):
        x = (k % COLS) * W; yy = y + (k // COLS) * (H + 40); im.thumbnail((W - 8, H)); sheet.paste(im, (x + 4, yy))
        d.text((x + 6, yy + H + 4), (r.get("id") or pathlib.Path(r["path"]).stem)[:40] + " · " + r.get("role", "")[:30], font=FS, fill=(220, 220, 220))
    y += ((len(ims) + COLS - 1) // COLS) * (H + 40)
    for r in txt: d.text((14, y), "· " + (r.get("id") or r.get("link", ""))[:120] + "  " + r.get("why", "")[:80], font=FS, fill=(200, 200, 200)); y += 22
    y += 6
sheet.save(out, quality=88); print("wrote", out)
