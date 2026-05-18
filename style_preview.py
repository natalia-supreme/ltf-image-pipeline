#!/usr/bin/env python3
"""
STEP 1 of the Mark workflow: preview a new style.

Claude writes `pending_style.yaml` (see pending_style.example.yaml),
then runs:  python3 style_preview.py

Generates ONE preview image with FAL (using demo colours: home =
Arsenal red/white, away = Burnley claret/sky-blue) so Mark can judge it.
Nothing is published yet. Needs a FAL key in .env.
"""

import sys
from pathlib import Path

import requests
import yaml

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from src.generate import _call_fal, _crop_to_spec  # noqa: E402
from main import _load_env  # noqa: E402

DEMO = {
    "home_primary": "bright red", "home_secondary": "white",
    "away_primary": "deep claret / burgundy", "away_secondary": "sky blue",
}
SIZE = {"label": "square", "width": 1200, "height": 1200}


def main() -> None:
    _load_env()
    pend = ROOT / "pending_style.yaml"
    if not pend.exists():
        raise SystemExit("No pending_style.yaml. Create one first "
                         "(see pending_style.example.yaml).")

    s = yaml.safe_load(pend.read_text(encoding="utf-8"))
    for f in ("key", "title", "category", "prompt"):
        if not s.get(f):
            raise SystemExit(f"pending_style.yaml missing '{f}'")

    prompt = s["prompt"]
    for k, v in DEMO.items():
        prompt = prompt.replace("{" + k + "}", v)

    config = yaml.safe_load((ROOT / "config.yaml").read_text())
    out = ROOT / "experiments" / "output" / f"arsenal-burnley-{s['key']}.png"
    out.parent.mkdir(parents=True, exist_ok=True)

    print(f"-> previewing style '{s['key']}' ...")
    url = _call_fal(prompt, SIZE, config)
    raw = requests.get(url, timeout=120).content
    out.write_bytes(_crop_to_spec(raw, SIZE["width"], SIZE["height"]))
    print(f"   preview saved -> {out}")
    print("\nShow this image to Mark. If he likes it, run:")
    print("   python3 style_publish.py")
    print("If not, edit pending_style.yaml and run this again.")


if __name__ == "__main__":
    main()
