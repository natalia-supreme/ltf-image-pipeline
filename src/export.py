"""
Step 6 — EXPORT
Write a CSV mapping every event to its image file(s), including reused
images. This is the file you feed back into Channable.
"""

from __future__ import annotations

import csv
from pathlib import Path


def export_csv(config: dict, rows: list[dict]) -> Path:
    path = Path(config["output"]["csv_file"])
    path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = ["event_name", "tag", "size_label", "image_path",
                  "source", "cost"]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return path
