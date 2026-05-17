#!/usr/bin/env python3
"""
LTF Image Pipeline — runs the whole flow end to end.

    FETCH  ->  DEDUPE/REUSE  ->  PROMPT  ->  GENERATE  ->  STORE  ->  EXPORT

Usage:
    python main.py                # real run (needs FAL_KEY)
    python main.py --dry-run      # no API calls, verify the flow
    python main.py --limit 3      # only process the first 3 events

Everything you'd normally want to change lives in:
    config.yaml          (feed, sizes, model, reuse rules)
    prompts/football.txt (how the images look)
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import yaml

from src.fetch_feed import fetch_feed
from src.build_prompt import load_template, build_prompt, derive_tag
from src.library import (load_library, save_library, find_reusable,
                         add_image, record_reuse)
from src.generate import generate_image
from src.export import export_csv
from src.publish import publish


def _load_env() -> None:
    """Minimal .env loader so there are no extra dependencies."""
    env_path = Path(".env")
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip())


def main() -> None:
    parser = argparse.ArgumentParser(description="LTF Image Pipeline")
    parser.add_argument("--dry-run", action="store_true",
                        help="no FAL calls, just verify the flow")
    parser.add_argument("--limit", type=int, default=0,
                        help="only process the first N events (0 = all)")
    args = parser.parse_args()

    _load_env()
    config = yaml.safe_load(Path("config.yaml").read_text(encoding="utf-8"))

    print("1. FETCH  — downloading feed ...")
    events = fetch_feed(config)
    if args.limit:
        events = events[: args.limit]
    print(f"   {len(events)} events after filtering\n")

    template = load_template(config)
    library = load_library(config)
    reuse_cfg = config["reuse"]
    sizes = config["fal"]["sizes"]

    csv_rows: list[dict] = []
    generated = reused = 0
    total_cost = 0.0

    for ev in events:
        name = ev.get("name", "Unnamed event")
        tag = derive_tag(ev, reuse_cfg)
        prompt = build_prompt(template, ev)
        print(f"-> {name}   (tag: {tag or 'none'})")

        for size in sizes:
            existing = (find_reusable(library, tag, size["label"], reuse_cfg)
                        if reuse_cfg.get("enabled") else None)

            if existing:
                record_reuse(existing, name)
                reused += 1
                source = "reused"
                file_path = existing["file_path"]
                cost = 0.0
                print(f"   [{size['label']}] reused existing image")
            else:
                result = generate_image(
                    prompt=prompt, event_name=name, size=size,
                    config=config, dry_run=args.dry_run,
                )
                add_image(library, event_name=name, tag=tag,
                          size_label=size["label"],
                          file_path=result["file_path"], prompt=prompt,
                          model=config["fal"]["model"], cost=result["cost"])
                generated += 1
                source = "dry-run" if args.dry_run else "generated"
                file_path = result["file_path"]
                cost = result["cost"]
                total_cost += cost
                print(f"   [{size['label']}] {source} -> {file_path}")

            csv_rows.append({
                "event_name": name, "tag": tag,
                "size_label": size["label"], "image_path": str(file_path),
                "source": source, "cost": cost,
            })

    save_library(config, library)
    csv_path = export_csv(config, csv_rows)

    pub_records = [{
        "file_path": r["image_path"],
        "title": r["event_name"],
        "category": "match",
        "style_key": "",
        "status": "pending",
        "reusable": False,
    } for r in csv_rows]
    manifest_path = publish(pub_records, config)

    print("\n" + "=" * 50)
    print(f"  generated : {generated}")
    print(f"  reused    : {reused}")
    print(f"  est. cost : ${total_cost:.2f}")
    print(f"  CSV       : {csv_path}")
    print(f"  library   : {config['output']['library_file']}")
    if manifest_path:
        print(f"  published : {manifest_path}")
    print("=" * 50)
    if args.dry_run:
        print("  (dry run — no images were actually generated)")


if __name__ == "__main__":
    main()
