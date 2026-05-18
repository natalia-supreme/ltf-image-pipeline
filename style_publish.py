#!/usr/bin/env python3
"""
STEP 2 of the Mark workflow: publish the previewed style.

Run ONLY after Mark approves the preview:
    python3 style_publish.py

Does everything:
  1. appends the style to styles.yaml (enabled)
  2. rebuilds gallery/styles.json  -> shows in Lovable Styles list
  3. adds the preview image to the gallery + manifest -> Lovable gallery
  4. git add + commit + push  -> live in a few minutes
  5. clears pending_style.yaml
"""

import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent


def sh(*args: str) -> None:
    subprocess.run(args, cwd=ROOT, check=True)


def main() -> None:
    pend = ROOT / "pending_style.yaml"
    if not pend.exists():
        raise SystemExit("No pending_style.yaml to publish.")
    s = yaml.safe_load(pend.read_text(encoding="utf-8"))
    key = s["key"]

    img = ROOT / "experiments" / "output" / f"arsenal-burnley-{key}.png"
    if not img.exists():
        raise SystemExit("No preview image. Run style_preview.py first "
                          "and have Mark approve it.")

    # 1. append to styles.yaml (text append preserves comments)
    styles_doc = yaml.safe_load((ROOT / "styles.yaml").read_text())
    if any(x["key"] == key for x in styles_doc["styles"]):
        print(f"'{key}' already in styles.yaml — skipping append")
    else:
        prompt_lines = s["prompt"].rstrip().splitlines()
        body = "\n".join("      " + ln for ln in prompt_lines)
        needs = s.get("needs", [])
        block = (
            f"\n  - key: {key}\n"
            f"    title: \"{s['title']}\"\n"
            f"    category: {s['category']}\n"
            f"    enabled: true\n"
            f"    has_players: {str(bool(s.get('has_players', False))).lower()}\n"
            f"    needs: {json.dumps(needs)}\n"
            f"    prompt: |\n{body}\n"
        )
        with (ROOT / "styles.yaml").open("a", encoding="utf-8") as f:
            f.write(block)
        print(f"appended '{key}' to styles.yaml")

    # 2. rebuild styles.json
    sh("python3", "build_styles.py")

    # 3. add to gallery seed + republish gallery/manifest.json
    seed_path = ROOT / "experiments" / "presentation" / "gallery_manifest.json"
    seed = json.loads(seed_path.read_text())
    if not any(x["style_key"] == key for x in seed):
        seed.append({
            "file": f"arsenal-burnley-{key}.png", "style_key": key,
            "title": s["title"], "category": s["category"],
            "format": "square", "status": "approved", "reusable": True,
        })
        seed_path.write_text(json.dumps(seed, indent=2))
    sh("python3", "experiments/publish_demo.py")

    # 4. commit + push
    sh("git", "add", "-A")
    sh("git", "commit", "-m", f"Add style '{key}' (Mark-approved)")
    sh("git", "push", "origin", "main")

    # 5. clear the staging file
    pend.unlink()
    print(f"\nDONE. '{key}' is live: it now shows in the Lovable Styles "
          f"list and its image is in the Lovable gallery (a few minutes "
          f"for GitHub cache).")


if __name__ == "__main__":
    main()
