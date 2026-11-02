#!/usr/bin/env python3
"""Measure the palette of one or more images and report it as a 60/30/10-style split.

Usage: python3 palette.py image1.jpg [image2.png ...] [--k 6]
Prints, per image and for all images together: the dominant colours (hex), their share of
the frame, and a suggested 60/30/10 reading (dominant / secondary / accent). The accent is
the most saturated colour that covers at least 2% of the frame, not simply the third-largest.
Needs Pillow (pip install pillow).
"""
import sys, colorsys
from PIL import Image

def colours(path, k):
    im = Image.open(path).convert("RGB")
    im.thumbnail((240, 240))
    q = im.quantize(colors=k, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()[: k * 3]
    counts = sorted(q.getcolors(), reverse=True)
    total = sum(c for c, _ in counts)
    out = []
    for c, i in counts:
        r, g, b = pal[i * 3 : i * 3 + 3]
        h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
        out.append({"hex": f"#{r:02x}{g:02x}{b:02x}", "share": c / total, "sat": s, "light": l})
    return out

def split(cols):
    dom = cols[0]
    rest = cols[1:]
    acc = max((c for c in rest if c["share"] >= 0.02), key=lambda c: c["sat"] * (0.5 + c["light"]), default=None)
    sec = next((c for c in rest if c is not acc), None)
    return dom, sec, acc

def show(name, cols):
    print(f"\n{name}")
    for c in cols:
        print(f"  {c['hex']}  {c['share']*100:5.1f}%  sat {c['sat']:.2f}  light {c['light']:.2f}")
    d, s, a = split(cols)
    print(f"  60 dominant {d['hex']} · 30 secondary {s['hex'] if s else '-'} · 10 accent {a['hex'] if a else '-'}")

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    k = int(sys.argv[sys.argv.index("--k") + 1]) if "--k" in sys.argv else 6
    args = [a for a in args if a != str(k)]
    merged = {}
    for p in args:
        cols = colours(p, k)
        show(p, cols)
        for c in cols:
            merged[c["hex"]] = merged.get(c["hex"], 0) + c["share"] / len(args)
    if len(args) > 1:
        print("\nALL IMAGES (top colours by average share):")
        for hx, sh in sorted(merged.items(), key=lambda x: -x[1])[:k]:
            print(f"  {hx}  {sh*100:5.1f}%")
