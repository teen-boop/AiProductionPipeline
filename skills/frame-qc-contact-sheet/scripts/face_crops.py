#!/usr/bin/env python3
"""face_crops.py OUT.jpg REF.png IMG@x,y[,r] ... — the identity reference first, then a crop of each image centred on the face at
(x, y) given as FRACTIONS of width/height (0..1); r = half-width of the crop as a fraction (default 0.12). Compare hairline, face width
and age side by side. Read x,y off a contact sheet (position inside the cell / cell size)."""
import sys
from PIL import Image


def main(out, ref, specs, cell=(330, 380)):
    ims = [Image.open(ref).convert("RGB")]
    for s in specs:
        path, coords = s.rsplit("@", 1)
        v = [float(c) for c in coords.split(",")]
        x, y, r = v[0], v[1], (v[2] if len(v) > 2 else 0.12)
        im = Image.open(path).convert("RGB"); W, H = im.size; rv = r * 1.6
        ims.append(im.crop((int(max(0, x - r) * W), int(max(0, y - rv) * H), int(min(1, x + r) * W), int(min(1, y + rv) * H))))
    cols = 4; rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", ((cell[0] + 20) * cols, (cell[1] + 20) * rows))
    for i, im in enumerate(ims):
        im = im.resize(cell) if i else im.copy()
        if not i:
            im.thumbnail(cell)
        sheet.paste(im, ((i % cols) * (cell[0] + 20), (i // cols) * (cell[1] + 20)))
    sheet.save(out, quality=88)
    print(len(ims) - 1, "faces ->", out)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2], sys.argv[3:])
