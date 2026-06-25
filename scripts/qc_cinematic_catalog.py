#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cinematic QC — ship gate requires HD/UHD renders, not draft stubs."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "videos" / "caly_friends_catalog.json"
WEB_VIDEOS = ROOT.parent / "calyndra-app" / "videos"

BANDS = ("baby", "toddler", "child", "tween", "teen", "adult")
ALLOWED_PROFILES = frozenset({"hd", "uhd", "4k", "ultra", "motion-picture"})
MIN_WIDTH = 1920
MIN_HEIGHT = 1080


def main() -> int:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    errors: list[str] = []
    warnings: list[str] = []

    for ep in catalog.get("episodes", []):
        eid = ep.get("id", "?")
        profile = (ep.get("videoProfile") or "draft").strip().lower()
        status = ep.get("status", "")
        if status == "script-only":
            errors.append(f"{eid}: still script-only — run generate_caly_friends_episodes.py --render")
            continue
        if profile not in ALLOWED_PROFILES:
            if ep.get("pilot"):
                warnings.append(f"{eid}: pilot with profile `{profile}` — upgrade to hd/uhd before GA.")
            else:
                errors.append(f"{eid}: videoProfile `{profile}` not cinematic (need hd/uhd).")
        res = ep.get("videoResolution") or ""
        if res:
            try:
                w, h = (int(x) for x in res.lower().split("x"))
                if w < MIN_WIDTH or h < MIN_HEIGHT:
                    if ep.get("pilot"):
                        warnings.append(f"{eid}: pilot resolution {res} — schedule UHD re-render.")
                    elif w >= 1280 and h >= 720:
                        warnings.append(f"{eid}: resolution {res} — HD upgrade pending (target 1920x1080+).")
                    else:
                        errors.append(f"{eid}: resolution {res} below 1280x720.")
            except ValueError:
                warnings.append(f"{eid}: invalid videoResolution `{res}`.")
        webm = WEB_VIDEOS / ep.get("webm", "")
        if not webm.is_file():
            errors.append(f"{eid}: missing WebM `{ep.get('webm')}` in calyndra-app/videos.")

    print(f"Cinematic QC: {len(catalog.get('episodes', []))} episodes checked.")
    for w in warnings[:15]:
        print(f"  WARN: {w}")
    for e in errors[:30]:
        print(f"  FAIL: {e}")
    if len(errors) > 30:
        print(f"  ... and {len(errors) - 30} more")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
