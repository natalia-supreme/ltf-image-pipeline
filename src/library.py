"""
Step 2 + 5 — LIBRARY (dedupe / store / reuse)

The library is a single JSON file that records every image generated,
its tags, and whether it has been marked reusable.

Reuse model: an image tagged "Arsenal" can be reused for ANY future
event tagged "Arsenal" instead of generating (and paying) again.
"""

from __future__ import annotations

import json
from pathlib import Path


def load_library(config: dict) -> dict:
    path = Path(config["output"]["library_file"])
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"images": []}


def save_library(config: dict, library: dict) -> None:
    path = Path(config["output"]["library_file"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(library, indent=2, ensure_ascii=False), encoding="utf-8")


def find_reusable(library: dict, tag: str, size_label: str, reuse_cfg: dict):
    """Return an existing image for this tag + size, or None."""
    if not tag:
        return None
    only_marked = reuse_cfg.get("only_reuse_marked", True)
    for img in library["images"]:
        if img.get("tag") != tag:
            continue
        if img.get("size_label") != size_label:
            continue
        if only_marked and not img.get("reusable", False):
            continue
        return img
    return None


def add_image(library: dict, *, event_name, tag, size_label,
              file_path, prompt, model, cost) -> dict:
    record = {
        "event_name": event_name,
        "tag": tag,
        "size_label": size_label,
        "file_path": str(file_path),
        "prompt": prompt,
        "model": model,
        "cost": cost,
        "reusable": False,  # operator flips this to True for the good ones
        "usages": [event_name],
    }
    library["images"].append(record)
    return record


def record_reuse(image: dict, event_name: str) -> None:
    image.setdefault("usages", [])
    if event_name not in image["usages"]:
        image["usages"].append(event_name)
