#!/usr/bin/env python3
"""
Turn styles.yaml into gallery/styles.json so Lovable's Styles list and
the pipeline read the SAME source of truth.

Workflow for adding a style (Mark):
    1. edit styles.yaml (copy a block, new key, write prompt)
    2. python3 build_styles.py
    3. git add -A && git commit -m "add style" && git push
    -> the new style appears as a selectable option automatically.

Run from the repo root:
    python3 build_styles.py
"""

from pathlib import Path
import json
import yaml

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "styles.yaml"
OUT = ROOT / "gallery" / "styles.json"

REQUIRED = {"key", "title", "category", "enabled", "needs", "prompt"}
VALID_CATEGORIES = {"head-to-head", "club-spotlight", "stadium-atmosphere"}


def main() -> None:
    data = yaml.safe_load(SRC.read_text(encoding="utf-8"))
    styles = data.get("styles", [])

    seen, out = set(), []
    for s in styles:
        missing = REQUIRED - s.keys()
        if missing:
            raise SystemExit(f"style {s.get('key','?')} missing: {missing}")
        if s["key"] in seen:
            raise SystemExit(f"duplicate style key: {s['key']}")
        if s["category"] not in VALID_CATEGORIES:
            raise SystemExit(
                f"{s['key']}: bad category '{s['category']}' "
                f"(use one of {sorted(VALID_CATEGORIES)})"
            )
        seen.add(s["key"])
        out.append({
            "key": s["key"],
            "title": s["title"],
            "category": s["category"],
            "enabled": bool(s["enabled"]),
            "has_players": bool(s.get("has_players", False)),
            "needs": s["needs"],
            "prompt": s["prompt"].strip(),
        })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False),
                   encoding="utf-8")

    enabled = sum(1 for s in out if s["enabled"])
    by_cat = {}
    for s in out:
        by_cat.setdefault(s["category"], 0)
        by_cat[s["category"]] += 1
    print(f"wrote {len(out)} styles ({enabled} enabled) -> {OUT}")
    print("by category:", by_cat)
    players = [s["key"] for s in out if s["has_players"]]
    if players:
        print("has invented players (Mark wants to move away):", players)


if __name__ == "__main__":
    main()
