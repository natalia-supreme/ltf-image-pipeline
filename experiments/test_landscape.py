#!/usr/bin/env python3
"""
One-style landscape test: regenerate the hero F duel composed for the
Google Search 1.91:1 horizontal asset (1200x628), recomposed wide
(NOT cropped from the square).

Run from repo root:
    python3 experiments/test_landscape.py
"""

import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.generate import _call_fal, _crop_to_spec  # noqa: E402
from experiments.compare_directions import DIRECTIONS  # noqa: E402

STYLE = "F-twocolour-duel"
SIZE = {"label": "landscape", "width": 1200, "height": 628}

# Wide-composition steer (nano-banana-2 ignores size args, so we tell it
# to frame for a horizontal banner; then we crop to exact 1200x628).
WIDE = (
    " IMPORTANT FRAMING: compose this as a WIDE horizontal 1.91:1 "
    "cinematic banner — landscape orientation, the two players centred "
    "with generous empty headroom above and breathing space on both "
    "sides, plenty of stadium/sky around them, nothing important near "
    "the top or bottom edges (safe for a wide crop)."
)


def main() -> None:
    import yaml
    config = yaml.safe_load(Path("config.yaml").read_text())
    prompt = DIRECTIONS[STYLE] + WIDE

    print(f"-> generating {STYLE} in landscape 1200x628 ...")
    url = _call_fal(prompt, SIZE, config)
    raw = requests.get(url, timeout=120).content
    final = _crop_to_spec(raw, SIZE["width"], SIZE["height"])
    out = Path("experiments/output") / f"arsenal-burnley-{STYLE}-landscape.png"
    out.write_bytes(final)
    print(f"   saved -> {out}")


if __name__ == "__main__":
    main()
