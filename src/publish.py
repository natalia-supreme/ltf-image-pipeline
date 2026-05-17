"""
Step 7 — PUBLISH
Copy finished images into a git-tracked folder and write a manifest of
public raw-GitHub URLs that the Lovable gallery (or anything) can read.

Does NOT git push — that stays a manual, reviewable step (see README).
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path


def _raw_url(gh: dict, filename: str) -> str:
    return (
        f"https://raw.githubusercontent.com/{gh['owner']}/{gh['repo']}/"
        f"{gh['branch']}/{gh['folder']}/{filename}"
    )


def publish(records: list[dict], config: dict) -> Path | None:
    """records: list of {file_path, title, category, style_key, status,
    reusable}. Copies each file into the gallery folder and writes
    gallery/manifest.json with public URLs. Returns the manifest path.
    """
    pub = config.get("publish") or {}
    if not pub.get("enabled"):
        return None
    if pub.get("target") != "github":
        raise ValueError(f"unsupported publish target: {pub.get('target')}")

    gh = pub["github"]
    folder = Path(gh["folder"])
    folder.mkdir(parents=True, exist_ok=True)

    manifest = []
    for r in records:
        src = Path(r["file_path"])
        if not src.exists():
            continue
        dest = folder / src.name
        shutil.copy2(src, dest)
        manifest.append({
            "file": src.name,
            "url": _raw_url(gh, src.name),
            "title": r.get("title", src.stem),
            "category": r.get("category", ""),
            "style_key": r.get("style_key", ""),
            "status": r.get("status", "approved"),
            "reusable": r.get("reusable", False),
        })

    manifest_path = folder / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return manifest_path
