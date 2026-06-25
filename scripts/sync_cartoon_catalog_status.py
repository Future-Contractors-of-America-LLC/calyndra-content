#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Align cartoon catalog metadata with shipped WebM files."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "videos" / "caly_friends_catalog.json"
WEB_VIDEOS = ROOT.parent / "calyndra-app" / "videos"


def main() -> int:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    updated = 0
    for ep in catalog.get("episodes", []):
        webm = WEB_VIDEOS / ep.get("webm", "")
        if not webm.is_file():
            continue
        if ep.get("status") == "script-only":
            ep["status"] = "complete"
            updated += 1
        if ep.get("videoProfile") in (None, "draft") and not ep.get("pilot"):
            ep["videoProfile"] = "hd"
            ep["videoResolution"] = ep.get("videoResolution") or "1920x1080"
            updated += 1
        elif ep.get("pilot") and ep.get("videoProfile") == "draft":
            ep["videoProfile"] = "hd"
            ep["videoResolution"] = "1280x720"
            updated += 1
    CATALOG.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    print(f"Updated {updated} catalog field(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
