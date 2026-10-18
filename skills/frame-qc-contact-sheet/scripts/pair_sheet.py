#!/usr/bin/env python3
"""pair_sheet.py OUT.jpg START END [START END ...] — one row per pair (start | end) to QC change-to frames and keyframe chains.
Also accepts chains: pass K1 K2 K3 with --chain 3 to lay out rows of 3."""
import os, sys
from PIL import Image, ImageDraw


def main(out, paths, per_row=2, w=600, h=338):
    rows = [paths[i:i + per_row] for i in range(0, len(paths), per_row)]
    sheet = Image.new("RGB", (w * per_row, (h + 4) * len(rows)))
    draw = ImageDraw.Draw(sheet)
    for r, row in enumerate(rows):
        for c, p in enumerate(row):
            sheet.paste(Image.open(p).convert("RGB").resize((w, h)), (c * w, r * (h + 4)))
            draw.text((c * w + 4, r * (h + 4) + 4), os.path.basename(p)[:44], fill=(255, 255, 0))
    sheet.save(out, quality=82)
    print(len(rows), "rows ->", out)


if __name__ == "__main__":
    args = sys.argv[1:]
    n = 2
    if "--chain" in args:
        i = args.index("--chain"); n = int(args[i + 1]); del args[i:i + 2]
    if len(args) < 3:
        sys.exit(__doc__)
    main(args[0], args[1:], per_row=n)
