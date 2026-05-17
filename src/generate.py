"""
Step 4 — GENERATE
Call FAL AI with the built prompt and save the resulting image to disk.

In --dry-run mode no API call is made: the prompt is printed and an
empty placeholder file is written, so the whole flow can be verified
without spending money or even needing the key yet.
"""

from __future__ import annotations

import io
import os
import re
from pathlib import Path

import requests
from PIL import Image

# Rough per-image cost estimate, only used for reporting in the CSV/log.
ESTIMATED_COST_PER_IMAGE = 0.04


def _slugify(text: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return text or "image"


def _crop_to_spec(image_bytes: bytes, target_w: int, target_h: int) -> bytes:
    """Center-crop the image to the target aspect ratio, then resize to the
    exact target dimensions. Guarantees Google-spec output regardless of
    what the model returned.
    """
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    src_w, src_h = img.size
    target_ratio = target_w / target_h
    src_ratio = src_w / src_h

    if src_ratio > target_ratio:
        # source too wide -> crop the sides
        new_w = int(src_h * target_ratio)
        left = (src_w - new_w) // 2
        box = (left, 0, left + new_w, src_h)
    else:
        # source too tall -> crop top/bottom
        new_h = int(src_w / target_ratio)
        top = (src_h - new_h) // 2
        box = (0, top, src_w, top + new_h)

    img = img.crop(box).resize((target_w, target_h), Image.LANCZOS)
    out = io.BytesIO()
    img.save(out, format="PNG")
    return out.getvalue()


def generate_image(*, prompt, event_name, size, config, dry_run=False) -> dict:
    """Generate one image. Returns {file_path, cost}."""
    images_dir = Path(config["output"]["images_dir"])
    images_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{_slugify(event_name)}-{size['label']}.png"
    file_path = images_dir / filename

    if dry_run:
        file_path.write_bytes(b"")  # placeholder so the flow completes
        return {"file_path": file_path, "cost": 0.0}

    image_url = _call_fal(prompt, size, config)

    img = requests.get(image_url, timeout=120)
    img.raise_for_status()

    # The model may ignore size args, so crop to the exact Google spec.
    final_bytes = _crop_to_spec(img.content, size["width"], size["height"])
    file_path.write_bytes(final_bytes)

    return {"file_path": file_path, "cost": ESTIMATED_COST_PER_IMAGE}


def _call_fal(prompt: str, size: dict, config: dict) -> str:
    """Call FAL and return the URL of the generated image."""
    import fal_client  # imported here so --dry-run works without it installed

    if not os.environ.get("FAL_KEY"):
        raise RuntimeError(
            "FAL_KEY is not set. Put it in a .env file (see .env.example) "
            "or export it before running."
        )

    fal_cfg = config["fal"]
    arguments = {
        "prompt": prompt,
        # Hint the size to the model. nano-banana-2 tends to ignore this,
        # so the output is always center-cropped to the exact spec after
        # download (see _crop_to_spec). Harmless if the model respects it.
        "image_size": {"width": size["width"], "height": size["height"]},
    }
    arguments.update(fal_cfg.get("arguments") or {})

    result = fal_client.subscribe(fal_cfg["model"], arguments=arguments)

    images = result.get("images") or result.get("image") or []
    if isinstance(images, dict):
        images = [images]
    if not images:
        raise RuntimeError(f"FAL returned no images. Raw response: {result}")
    return images[0]["url"]
