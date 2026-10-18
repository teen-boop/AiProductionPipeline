#!/usr/bin/env python3
"""trim_bars.py IMG [IMG ...] — crop black letterbox bars (near-black full rows at the top/bottom) and keep the original aspect ratio
by cropping the sides proportionally; the original is saved next to it as _orig_bars_<name>. Dark film content is not touched:
a row counts as a bar only if its mean brightness is below 6/255 across the full width."""
import os, shutil, sys
from PIL import Image


def dark(L, y):
    W = L.size[0]
    return sum(L.crop((0, y, W, y + 1)).getdata()) / W < 6


def trim(path):
    im = Image.open(path).convert("RGB"); L = im.convert("L"); W, H = im.size; t = b = 0
    while t < H // 6 and dark(L, t): t += 1
    while b < H // 6 and dark(L, H - 1 - b): b += 1
    if t <= 2 and b <= 2:
        return False
    d, n = os.path.split(path)
    shutil.copy(path, os.path.join(d, "_orig_bars_" + n))
    m = max(t, b) + 2; cx = int(m * W / H)
    im.crop((cx, m, W - cx, H - m)).resize((W, H), Image.LANCZOS).save(path)
    print(f"trimmed {path}: top {t}px, bottom {b}px")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for p in sys.argv[1:]:
        trim(p)
