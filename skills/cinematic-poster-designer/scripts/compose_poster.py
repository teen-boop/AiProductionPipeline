#!/usr/bin/env python3
"""Lay clean film-poster typography over generated key art (the generator never draws text).

Usage:
  python3 compose_poster.py ART.png OUT.png --title "FILM TITLE" [--layout wide-top|giant-bottom|serif-center|side-vertical]
      [--tagline "..."] [--credits "A FILM BY ... · ..."] [--date "IN CINEMAS SOON"] [--size 2000x3000]
      [--ink "#f3eee8"] [--accent "#f0962b"] [--scrim 0.0-1.0]

Layouts:
  wide-top      thin caps with very wide tracking near the top (FILM TITLE A)
  giant-bottom  heavy condensed caps filling the width at the bottom (FILM TITLE B)
  serif-center  small elegant serif title in the middle of negative space (FILM TITLE C)
  side-vertical a stacked title down the right edge, grotesk, tight leading (FILM TITLE D)
Every layout adds an optional tagline, a credit block and a date line in small caps at the bottom.
The art is cover-cropped to the poster size; --scrim darkens the band behind the title.
Fonts are macOS system fonts (Avenir Next, Avenir Next Condensed, Didot, Helvetica Neue).
"""
import argparse
from PIL import Image, ImageDraw, ImageFont

F = "/System/Library/Fonts/"
S = F + "Supplemental/"
FONTS = {
    "thin": (F + "Avenir Next.ttc", 7),          # Ultra Light
    "regular": (F + "Avenir Next.ttc", 7 + 0),
    "medium": (F + "Avenir Next.ttc", 5),
    "heavy_cond": (F + "Avenir Next Condensed.ttc", 8),
    "serif": (S + "Didot.ttc", 0),
    "grotesk": (F + "HelveticaNeue.ttc", 1),
}

def font(kind, size):
    path, idx = FONTS[kind]
    for i in (idx, 0):
        try:
            return ImageFont.truetype(path, size, index=i)
        except Exception:
            continue
    return ImageFont.load_default()

def trim_bars(img, thresh=14):
    """Remove letterbox / pillarbox bars (near-black rows or columns at the edges)."""
    g = img.convert("L")
    w, h = g.size
    def dark_row(y): return max(g.crop((0, y, w, y + 1)).getdata()) < thresh
    def dark_col(x): return max(g.crop((x, 0, x + 1, h)).getdata()) < thresh
    t = 0
    while t < h // 4 and dark_row(t): t += 1
    b = h
    while b > h * 3 // 4 and dark_row(b - 1): b -= 1
    l = 0
    while l < w // 4 and dark_col(l): l += 1
    r = w
    while r > w * 3 // 4 and dark_col(r - 1): r -= 1
    return img.crop((l, t, r, b))

def cover(img, w, h):
    s = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    l, t = (img.width - w) // 2, (img.height - h) // 2
    return img.crop((l, t, l + w, t + h))

def tracked(draw, xy, text, f, fill, tracking, anchor_center=True, W=None):
    widths = [draw.textlength(c, font=f) for c in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x, y = xy
    if anchor_center:
        x = (W - total) / 2
    for c, cw in zip(text, widths):
        draw.text((x, y), c, font=f, fill=fill)
        x += cw + tracking
    return total

def fit(draw, text, kind, max_w, start):
    size = start
    while size > 10:
        f = font(kind, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 4
    return font(kind, size)

def scrim(img, top, bottom, strength):
    if strength <= 0:
        return img
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for y in range(top, bottom):
        a = int(255 * strength * (1 - abs((y - (top + bottom) / 2) / ((bottom - top) / 2))) ** 0.6)
        d.line([(0, y), (img.width, y)], fill=(0, 0, 0, a))
    return Image.alpha_composite(img.convert("RGBA"), ov)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("art"); ap.add_argument("out")
    ap.add_argument("--title", required=True); ap.add_argument("--tagline", default="")
    ap.add_argument("--credits", default=""); ap.add_argument("--date", default="")
    ap.add_argument("--layout", default="wide-top"); ap.add_argument("--size", default="2000x3000")
    ap.add_argument("--ink", default="#f3eee8"); ap.add_argument("--accent", default="#f0962b")
    ap.add_argument("--scrim", type=float, default=0.0)
    a = ap.parse_args()
    W, H = map(int, a.size.split("x"))
    img = cover(trim_bars(Image.open(a.art).convert("RGB")), W, H)
    m = int(W * 0.07)
    L = a.layout
    if L == "wide-top":
        img = scrim(img, 0, int(H * 0.22), a.scrim)
    elif L == "giant-bottom":
        img = scrim(img, int(H * 0.68), H, a.scrim)
    elif L == "serif-center":
        img = scrim(img, int(H * 0.40), int(H * 0.62), a.scrim)
    img = img.convert("RGBA"); d = ImageDraw.Draw(img)
    t = a.title.upper() if L != "serif-center" else a.title
    if L == "wide-top":
        f = font("thin", int(W * 0.075))
        tr = int(W * 0.035)
        while tracked(ImageDraw.Draw(Image.new("RGB", (1, 1))), (0, 0), t, f, a.ink, tr, False) > W - 2 * m and tr > 0:
            tr -= 4
        tracked(d, (0, int(H * 0.075)), t, f, a.ink, tr, True, W)
        if a.tagline:
            tracked(d, (0, int(H * 0.045)), a.tagline.upper(), font("medium", int(W * 0.016)), a.ink, int(W * 0.006), True, W)
    elif L == "giant-bottom":
        f = fit(d, t, "heavy_cond", W - 2 * m, int(W * 0.4))
        bb = d.textbbox((0, 0), t, font=f)
        d.text((m - bb[0], int(H * 0.86) - (bb[3] - bb[1]) - bb[1]), t, font=f, fill=a.accent)
        if a.tagline:
            d.text((m, int(H * 0.86) - (bb[3] - bb[1]) - int(H * 0.035)), a.tagline, font=font("medium", int(W * 0.02)), fill=a.ink)
    elif L == "serif-center":
        f = fit(d, t, "serif", W - 4 * m, int(W * 0.09))
        tracked(d, (0, int(H * 0.50)), t, f, a.ink, int(W * 0.012), True, W)
        if a.tagline:
            tracked(d, (0, int(H * 0.50) + int(W * 0.13)), a.tagline.upper(), font("regular", int(W * 0.016)), a.ink, int(W * 0.008), True, W)
    elif L == "side-vertical":
        words = t.title().split() if len(t.split()) > 1 else [t]
        f = fit(d, max(words, key=len), "grotesk", int(W * 0.5), int(W * 0.16))
        y = int(H * 0.55)
        for wd in words:
            bb = d.textbbox((0, 0), wd, font=f)
            d.text((W - m - (bb[2] - bb[0]) - bb[0], y), wd, font=f, fill=a.ink)
            y += int((bb[3] - bb[1]) * 1.05)
    # bottom block: credits + date, small caps, centred
    y = int(H * 0.925)
    if a.credits:
        cf = font("medium", int(W * 0.0125))
        for line in a.credits.split("|"):
            tracked(d, (0, y), line.strip().upper(), cf, a.ink, int(W * 0.003), True, W)
            y += int(W * 0.02)
    if a.date:
        tracked(d, (0, y + int(W * 0.005)), a.date.upper(), font("medium", int(W * 0.016)), a.accent, int(W * 0.006), True, W)
    img.convert("RGB").save(a.out, quality=95)
    print("saved", a.out, img.size)

if __name__ == "__main__":
    main()
