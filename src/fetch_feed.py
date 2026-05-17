"""
Step 1 — FETCH
Download the XML feed and turn it into a clean list of event dicts.
"""

from __future__ import annotations

import datetime as _dt
import xml.etree.ElementTree as ET

import requests


def fetch_feed(config: dict) -> list[dict]:
    """Download the feed and return a list of event dictionaries.

    Each event dict is just {xml_tag: text_value} for every child tag of
    a <match> element, so it adapts automatically if the feed adds fields.
    """
    feed_cfg = config["feed"]
    url = feed_cfg["url"]
    item_element = feed_cfg["item_element"]

    resp = requests.get(url, timeout=60)
    resp.raise_for_status()

    root = ET.fromstring(resp.content)

    events: list[dict] = []
    for item in root.iter(item_element):
        event = {child.tag: (child.text or "").strip() for child in item}
        events.append(event)

    events = _apply_filters(events, feed_cfg)
    return events


def _apply_filters(events: list[dict], feed_cfg: dict) -> list[dict]:
    only = feed_cfg.get("only_categories") or []
    skip_past = feed_cfg.get("skip_past_events", False)

    filtered = []
    for ev in events:
        if only and ev.get("category") not in only:
            continue
        if skip_past and _is_past(ev.get("datetime", "")):
            continue
        filtered.append(ev)
    return filtered


def _is_past(datetime_str: str) -> bool:
    """Feed datetime looks like '2026-05-18 20:00:00'. Returns True if past."""
    if not datetime_str:
        return False
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            when = _dt.datetime.strptime(datetime_str, fmt)
            return when < _dt.datetime.now()
        except ValueError:
            continue
    return False  # if we can't parse it, don't drop it
