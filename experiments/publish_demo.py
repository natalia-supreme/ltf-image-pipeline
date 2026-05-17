#!/usr/bin/env python3
"""
Publish the 12 APPROVED demo images into the git-tracked gallery folder
and write gallery/manifest.json with public GitHub raw URLs for Lovable.

Run from the repo root:
    python3 experiments/publish_demo.py
"""

import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.publish import publish  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "experiments/presentation/gallery_manifest.json"
IMAGES = ROOT / "experiments/output"


def main() -> None:
    config = yaml.safe_load((ROOT / "config.yaml").read_text())
    seed = json.loads(SEED.read_text())

    records = [{
        "file_path": str(IMAGES / item["file"]),
        "title": item["title"],
        "category": item["category"],
        "style_key": item["style_key"],
        "format": item.get("format", "square"),
        "status": item["status"],
        "reusable": item["reusable"],
    } for item in seed]

    manifest_path = publish(records, config)
    data = json.loads(manifest_path.read_text())
    print(f"published {len(data)} images -> {manifest_path}")
    print(f"sample URL: {data[0]['url']}")


if __name__ == "__main__":
    main()
