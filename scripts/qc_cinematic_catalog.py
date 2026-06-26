#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cinematic QC — ship gate requires probed UHD renders when CALY_SHIP=1."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "videos" / "caly_friends_catalog.json"
WEB_VIDEOS = ROOT.parent / "calyndra-app" / "videos"
LOCAL_VIDEOS = ROOT / "videos"

sys.path.insert(0, str(ROOT / "scripts"))
from caly_episode_duration import MIN_DURATION_RATIO, DURATION_TARGETS_SEC  # noqa: E402
from caly_video_probe import (  # noqa: E402
    profile_from_resolution,
    probe_duration,
    probe_resolution,
    resolve_webm_path,
    UHD_HEIGHT,
    UHD_WIDTH,
)

ALLOWED_PROFILES = frozenset({"hd", "uhd", "4k", "ultra", "motion-picture"})
MIN_WIDTH = 1920
MIN_HEIGHT = 1080


def require_uhd() -> bool:
    profile = (os.environ.get("CALY_VIDEO_PROFILE") or "").strip().lower()
    if os.environ.get("CALY_REQUIRE_UHD", "").strip() in ("1", "true", "yes"):
        return True
    if os.environ.get("CALY_SHIP", "").strip() in ("1", "true", "yes"):
        return True
    return profile in {"uhd", "4k", "ultra", "motion-picture"}


def require_duration() -> bool:
    return require_uhd() or os.environ.get("CALY_REQUIRE_DURATION", "").strip() in ("1", "true", "yes")


def main() -> int:
    strict_uhd = require_uhd()
    strict_duration = require_duration()
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    errors: list[str] = []
    warnings: list[str] = []

    for ep in catalog.get("episodes", []):
        episode_id = ep.get("id", "?")
        profile = (ep.get("videoProfile") or "draft").strip().lower()
        status = ep.get("status", "")
        if status == "script-only":
            errors.append(f"{episode_id}: still script-only — run generate_caly_friends_episodes.py --render")
            continue

        webm = resolve_webm_path(ep, WEB_VIDEOS, LOCAL_VIDEOS)
        if webm is None:
            errors.append(f"{episode_id}: missing WebM `{ep.get('webm')}` in app or content videos.")
            continue

        probed = probe_resolution(webm)
        duration = probe_duration(webm)
        band = ep.get("band") or ""
        target = int(ep.get("targetDurationSec") or DURATION_TARGETS_SEC.get(band, 0) or 0)

        if probed:
            width, height = probed
            probed_profile = profile_from_resolution(width, height)
            if strict_uhd and (width < UHD_WIDTH or height < UHD_HEIGHT):
                errors.append(
                    f"{episode_id}: probed {width}x{height} — UHD required ({UHD_WIDTH}x{UHD_HEIGHT}) when shipping."
                )
            elif not strict_uhd and (width < MIN_WIDTH or height < MIN_HEIGHT):
                if ep.get("pilot"):
                    warnings.append(f"{episode_id}: pilot resolution {width}x{height} — schedule UHD re-render.")
                elif width >= 1280 and height >= 720:
                    warnings.append(f"{episode_id}: resolution {width}x{height} — HD upgrade pending.")
                else:
                    errors.append(f"{episode_id}: resolution {width}x{height} below 1280x720.")

            catalog_res = ep.get("videoResolution") or ""
            if catalog_res:
                try:
                    catalog_w, catalog_h = (int(x) for x in catalog_res.lower().split("x"))
                    if probed and (catalog_w != width or catalog_h != height):
                        errors.append(
                            f"{episode_id}: catalog says {catalog_res} but file is {width}x{height}."
                        )
                except ValueError:
                    warnings.append(f"{episode_id}: invalid videoResolution `{catalog_res}`.")

            if profile not in ALLOWED_PROFILES:
                if ep.get("pilot"):
                    warnings.append(f"{episode_id}: pilot profile `{profile}` — upgrade before GA.")
                else:
                    errors.append(f"{episode_id}: videoProfile `{profile}` not cinematic (need hd/uhd).")
            elif strict_uhd and profile not in {"uhd", "4k", "ultra", "motion-picture"}:
                errors.append(f"{episode_id}: catalog profile `{profile}` but ship requires uhd.")
            elif probed_profile == "sub-hd":
                errors.append(f"{episode_id}: probed profile sub-hd ({width}x{height}).")
        else:
            errors.append(f"{episode_id}: unable to probe resolution for `{webm.name}`.")

        if strict_duration and target > 0 and duration is not None:
            minimum = target * MIN_DURATION_RATIO
            if duration < minimum:
                errors.append(
                    f"{episode_id}: duration {duration:.0f}s < {minimum:.0f}s "
                    f"({MIN_DURATION_RATIO:.0%} of {target}s target)."
                )
        elif duration is not None and duration < 30 and status in ("complete", "full"):
            warnings.append(f"{episode_id}: stub duration {duration:.0f}s on status={status}.")

    mode = "strict-uhd" if strict_uhd else "standard"
    print(f"Cinematic QC ({mode}): {len(catalog.get('episodes', []))} episodes checked.")
    for warning in warnings[:15]:
        print(f"  WARN: {warning}")
    for error in errors[:30]:
        print(f"  FAIL: {error}")
    if len(errors) > 30:
        print(f"  ... and {len(errors) - 30} more")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
