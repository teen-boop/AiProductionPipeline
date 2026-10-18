#!/usr/bin/env python3
"""contact_sheet.py OUT.jpg IMG [IMG ...] — 2-column grid of 800x450 cells, each labelled with its parent folder / file name."""
import os, sys
from PIL import Image, ImageDraw


def main(out, paths, cols=2, w=800, h=450):
    paths = [p for p in paths if os.path.isfile(p)]
    rows = (len(paths) + cols - 1) // cols
    sheet = Image.new("RGB", (w * cols, h * max(rows, 1)))
    draw = ImageDraw.Draw(sheet)
    for i, p in enumerate(paths):
        x, y = (i % cols) * w, (i // cols) * h
        sheet.paste(Image.open(p).convert("RGB").resize((w, h)), (x, y))
        label = os.path.basename(os.path.dirname(p)) if os.path.basename(p).startswith("RESULT") else os.path.basename(p)
        draw.rectangle((x, y, x + 300, y + 20), fill=(0, 0, 0)); draw.text((x + 4, y + 4), label[:48], fill=(255, 255, 0))
    sheet.save(out, quality=85)
    print(len(paths), "frames ->", out)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2:])
