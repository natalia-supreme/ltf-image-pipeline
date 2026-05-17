"""
Step 3 — PROMPT
Fill the prompt template with the event's feed fields.

Any {placeholder} in the template file is replaced with the matching
feed field. Unknown placeholders are left blank rather than crashing.
"""

from __future__ import annotations

import re
from pathlib import Path

_PLACEHOLDER = re.compile(r"\{([a-zA-Z0-9_]+)\}")


def load_template(config: dict) -> str:
    template_file = config["prompt"]["template_file"]
    path = Path("prompts") / template_file
    return path.read_text(encoding="utf-8")


def build_prompt(template: str, event: dict) -> str:
    def _sub(match: re.Match) -> str:
        key = match.group(1)
        return event.get(key, "").strip()

    prompt = _PLACEHOLDER.sub(_sub, template)
    # Collapse the whitespace left by the template's line wrapping.
    return " ".join(prompt.split())


def derive_tag(event: dict, reuse_cfg: dict) -> str:
    """Derive the reuse tag (e.g. the home team) from a feed field."""
    field = reuse_cfg.get("derive_tag_from", "name")
    value = event.get(field, "").strip()
    if not value:
        return ""

    split_on = reuse_cfg.get("split_on")
    if split_on and split_on in value:
        parts = [p.strip() for p in value.split(split_on)]
        take = reuse_cfg.get("take", "first")
        value = parts[0] if take == "first" else parts[-1]
    return value
