#!/usr/bin/env python3
"""Crop a clean N-panel storyboard grid and re-lay it out with a typographic
caption strip under each panel (slug line + CAM + ACTION/DIALOGUE).

Usage:
  caption_storyboard.py --src grid.png --out captioned.png --captions captions.json
                        [--cols 3] [--rows 4] [--inset 6]
                        [--title "TITLE: MY FILM"] [--scene "SCENE 01 — THE CALL"] [--page "PAGE 1 of 1"]
                        [--font-bold PATH.ttf] [--font PATH.ttf]

captions.json — a list of [slug, cam, action] triples, one per panel, in reading order, e.g.
  [["1. INT. THREE-DOOR ROOM — WS", "CAM: static", "Empty symmetrical room. (soft room tone)"],
   ["2. INT. THREE-DOOR ROOM — WS", "CAM: slow push in", "The center door begins to open."]]
"""
import argparse, json, os
from PIL import Image, ImageDraw, ImageFont

ap = argparse.ArgumentParser()
ap.add_argument("--src", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--captions", required=True)
ap.add_argument("--cols", type=int, default=3)
ap.add_argument("--rows", type=int, default=4)
ap.add_argument("--inset", type=int, default=6, help="trim a few px off each cell to drop the white gutter")
ap.add_argument("--title", default="TITLE")
ap.add_argument("--scene", default="SCENE 01")
ap.add_argument("--page", default="PAGE 1 of 1")
ap.add_argument("--font-bold", default="/System/Library/Fonts/Supplemental/Arial Bold.ttf")
ap.add_argument("--font", default="/System/Library/Fonts/Supplemental/Arial.ttf")
args = ap.parse_args()

COLS, ROWS, INSET = args.cols, args.rows, args.inset
CAPS = [tuple(c) for c in json.load(open(args.captions, encoding="utf-8"))]

im = Image.open(args.src).convert("RGB")
W, H = im.size
cw, ch = W / COLS, H / ROWS

# crop the panels
panels = []
for r in range(ROWS):
    for c in range(COLS):
        box = (int(c*cw)+INSET, int(r*ch)+INSET, int((c+1)*cw)-INSET, int((r+1)*ch)-INSET)
        panels.append(im.crop(box))

pw, ph = panels[0].size
CAP_H = 92
GUT = 18
MARGIN = 34
TITLE_H = 64

sheet_w = COLS*pw + (COLS-1)*GUT + 2*MARGIN
sheet_h = TITLE_H + ROWS*(ph+CAP_H) + (ROWS-1)*GUT + 2*MARGIN
sheet = Image.new("RGB", (sheet_w, sheet_h), (247, 245, 239))  # parchment
d = ImageDraw.Draw(sheet)

def font(path, size):
    return ImageFont.truetype(path, size) if os.path.exists(path) else ImageFont.load_default()
F_TITLE = font(args.font_bold, 24)
F_SLUG  = font(args.font_bold, 15)
F_CAM   = font(args.font, 13)
F_ACT   = font(args.font, 14)

# title bar
d.text((MARGIN, MARGIN-6), args.title, font=F_TITLE, fill=(40,40,40))
d.text((sheet_w//2-90, MARGIN+2), args.scene, font=F_SLUG, fill=(70,70,70))
d.text((sheet_w-MARGIN-120, MARGIN+2), args.page, font=F_SLUG, fill=(70,70,70))
d.line((MARGIN, MARGIN+TITLE_H-14, sheet_w-MARGIN, MARGIN+TITLE_H-14), fill=(180,178,170), width=1)

for i, (panel, (slug, cam, act)) in enumerate(zip(panels, CAPS)):
    r, c = divmod(i, COLS)
    x = MARGIN + c*(pw+GUT)
    y = MARGIN + TITLE_H + r*(ph+CAP_H+GUT)
    # frame border
    sheet.paste(panel, (x, y))
    d.rectangle((x-1, y-1, x+pw, y+ph), outline=(120,118,112), width=1)
    # caption box
    cy = y + ph
    d.rectangle((x-1, cy, x+pw, cy+CAP_H), outline=(120,118,112), width=1, fill=(255,254,250))
    tx, ty = x+8, cy+7
    d.text((tx, ty), slug, font=F_SLUG, fill=(25,25,25))
    d.text((tx, ty+21), cam, font=F_CAM, fill=(150,60,40))  # camera move accent
    # wrap action to width
    words = act.split(); line=""; ly=ty+40
    for w in words:
        test=(line+" "+w).strip()
        if d.textlength(test, font=F_ACT) > pw-16:
            d.text((tx, ly), line, font=F_ACT, fill=(45,45,45)); ly+=17; line=w
        else:
            line=test
    if line: d.text((tx, ly), line, font=F_ACT, fill=(45,45,45))

sheet.save(args.out, quality=95)
print("saved", args.out, sheet.size)
