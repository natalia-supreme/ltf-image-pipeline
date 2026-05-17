#!/usr/bin/env python3
"""Tile the approved images into labelled contact sheets for Mark."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path("experiments/output")
SHEETS = Path("experiments/presentation")
SHEETS.mkdir(parents=True, exist_ok=True)

HEAD_TO_HEAD = [
    ("F-twocolour-duel",      "1. Halved-kit duel (HERO)"),
    ("2-golden-duel-2col",    "2. Golden duel"),
    ("3-night-duel-2col",     "3. Night duel"),
    ("4-explosive-duel-2col", "4. Explosive duel"),
    ("foot-v1-flare",         "5. Foot v foot - flare"),
    ("foot-v3-strike",        "6. Foot v foot - strike"),
    ("foot-v4-groundlevel",   "7. Foot v foot - ground"),
]
ATMOSPHERE = [
    ("B-fan-pov",       "1. Fan POV"),
    ("A-ball-motion",   "2. Ball in motion"),
    ("3-pitch-tunnel",  "3. Pitch / tunnel"),
    ("4b-hero-2col",    "4. Single hero"),
    ("5b-epic-bowl",    "5. Epic stadium bowl"),
]

TILE, PAD, COLS = 360, 16, 4
CAPH, TITLEH = 34, 60


def _font(sz, bold=False):
    for p in [
        f"/System/Library/Fonts/Supplemental/Arial{' Bold' if bold else ''}.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]:
        try:
            return ImageFont.truetype(p, sz)
        except Exception:
            continue
    return ImageFont.load_default()


def sheet(title, items, fname):
    rows = (len(items) + COLS - 1) // COLS
    W = COLS * TILE + (COLS + 1) * PAD
    H = TITLEH + rows * (TILE + CAPH + PAD) + PAD
    canvas = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(canvas)
    d.rectangle([0, 0, W, TITLEH], fill="#EA0000")
    d.text((PAD, 16), title, fill="white", font=_font(26, True))

    for i, (key, cap) in enumerate(items):
        r, c = divmod(i, COLS)
        x = PAD + c * (TILE + PAD)
        y = TITLEH + PAD + r * (TILE + CAPH + PAD)
        im = Image.open(OUT / f"arsenal-burnley-{key}.png").convert("RGB")
        im = im.resize((TILE, TILE), Image.LANCZOS)
        canvas.paste(im, (x, y))
        d.text((x, y + TILE + 8), cap, fill="#1A1A1A", font=_font(18, True))

    canvas.save(SHEETS / fname, quality=92)
    print(f"saved -> {SHEETS / fname}  ({W}x{H})")


sheet("LTF AI Creatives  -  Head-to-Head Match  (7 approved)",
      HEAD_TO_HEAD, "01-head-to-head.png")
sheet("LTF AI Creatives  -  Stadium Atmosphere  (5 approved)",
      ATMOSPHERE, "02-stadium-atmosphere.png")
