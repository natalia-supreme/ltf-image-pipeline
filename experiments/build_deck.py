#!/usr/bin/env python3
"""Assemble the Mark deliverables: a PDF deck + a PDF one-pager."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

PRES = Path("experiments/presentation")
W, H = 1600, 1000
RED = "#EA0000"
INK = "#1A1A1A"
GREY = "#666666"


def font(sz, bold=False):
    for p in [
        f"/System/Library/Fonts/Supplemental/Arial{' Bold' if bold else ''}.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]:
        try:
            return ImageFont.truetype(p, sz)
        except Exception:
            continue
    return ImageFont.load_default()


def slide():
    return Image.new("RGB", (W, H), "white")


def cover():
    im = slide()
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 14], fill=RED)
    d.text((90, 300), "LTF AI Ad-Creative Engine", fill=INK, font=font(64, True))
    d.text((90, 390), "Copyright-clean football creatives, generated from the live feed",
           fill=GREY, font=font(30))
    d.text((90, 470), "12 approved directions  ·  ~$0.08 / image  ·  IP-safe",
           fill=RED, font=font(28, True))
    d.text((90, H - 110), "Prepared by Natalia  ·  2026-05-17  ·  for Mark",
           fill=GREY, font=font(24))
    return im


def image_slide(title, src):
    im = slide()
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 70], fill=RED)
    d.text((40, 18), title, fill="white", font=font(30, True))
    sheet = Image.open(PRES / src).convert("RGB")
    scale = min((W - 80) / sheet.width, (H - 130) / sheet.height)
    sheet = sheet.resize((int(sheet.width * scale), int(sheet.height * scale)),
                         Image.LANCZOS)
    im.paste(sheet, ((W - sheet.width) // 2, 95))
    return im


def text_slide(title, lines):
    im = slide()
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 70], fill=RED)
    d.text((40, 18), title, fill="white", font=font(30, True))
    y = 130
    for kind, text in lines:
        if kind == "h":
            y += 18
            d.text((90, y), text, fill=RED, font=font(28, True)); y += 50
        elif kind == "b":
            d.text((120, y), "•  " + text, fill=INK, font=font(24)); y += 44
        else:
            d.text((90, y), text, fill=GREY, font=font(22)); y += 40
    return im


summary = text_slide("Summary & Decisions", [
    ("h", "What it is"),
    ("b", "Pipeline pulls the live LFT feed and generates ad creatives via FAL AI"),
    ("b", "Copyright-clean: no logos, kits, real players, or real venues"),
    ("b", "Invented two-colour kits make teams recognisable but legally distinct"),
    ("h", "Cost"),
    ("b", "~$0.08 / image. Reuse model: pay once per team, not per match"),
    ("b", "Full Premier League season = a few dollars, near-zero ongoing"),
    ("h", "Decisions I need from you"),
    ("b", "Which approved style(s) should the full feed run produce?"),
    ("b", "OK to productionise automatic per-match generation?"),
    ("b", "GitHub repo name/owner? (suggest Markvdeng/ltf-image-pipeline)"),
])

deck = [cover(),
        image_slide("Head-to-Head Match  —  7 approved", "01-head-to-head.png"),
        image_slide("Stadium Atmosphere  —  5 approved", "02-stadium-atmosphere.png"),
        summary]

deck[0].save(PRES / "LTF-AI-Creatives-Deck.pdf", save_all=True,
             append_images=deck[1:], resolution=150)
print("saved -> LTF-AI-Creatives-Deck.pdf  (4 pages)")

# One-pager: single dense page
one = slide()
d = ImageDraw.Draw(one)
d.rectangle([0, 0, W, 70], fill=RED)
d.text((40, 18), "LTF AI Ad-Creative Engine  —  One-Pager", fill="white",
       font=font(28, True))
blocks = [
    ("h", "The result"),
    ("b", "12 approved, copyright-clean football creatives, generated from the live feed"),
    ("b", "7 head-to-head match styles + 5 stadium-atmosphere styles"),
    ("h", "How the IP problem is solved"),
    ("b", "Never name real team/venue; generic stadium; matchup carried by ad headline"),
    ("b", "Invented two-colour kit (halved shirt) — recognisable, legally distinct"),
    ("b", "Official kits researched first, then deliberately avoided"),
    ("h", "How Mark owns it"),
    ("b", "config.yaml + prompts/football.txt + team_colours.yaml — all plain, editable"),
    ("b", "GitHub repo, Claude-Code-friendly, optional Lovable UI on top"),
    ("h", "Cost"),
    ("b", "~$0.08/image · reuse model · full PL season ≈ a few dollars"),
    ("h", "Decisions needed"),
    ("b", "Which style(s) for the full run? · Productionise? · GitHub repo name?"),
]
y = 120
for kind, text in blocks:
    if kind == "h":
        y += 14
        d.text((70, y), text, fill=RED, font=font(26, True)); y += 46
    else:
        d.text((100, y), "•  " + text, fill=INK, font=font(23)); y += 42
one.save(PRES / "LTF-One-Pager.pdf", resolution=150)
print("saved -> LTF-One-Pager.pdf  (1 page)")
