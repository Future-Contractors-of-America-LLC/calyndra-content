# -*- coding: utf-8 -*-
"""QC Caly and Friends cartoon catalog - episodes per band and duration targets."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "videos" / "caly_friends_catalog.json"
REGISTRY = ROOT / "caly_character_registry.json"
WEB_VIDEOS = ROOT.parent / "calyndra-app" / "videos"

try:
    import imageio_ffmpeg

    FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    FFMPEG = "ffmpeg"

BANDS = ("baby", "toddler", "child", "tween", "teen", "adult")
TOLERANCE = 0.35


def probe_duration(path: Path) -> float | None:
    if not path.exists():
        return None
    try:
        r = subprocess.run(
            [FFMPEG, "-i", str(path)],
            capture_output=True,
            text=True,
        )
        import re

        m = re.search(r"Duration:\s*(\d+):(\d+):([\d.]+)", r.stderr)
        if m:
            h, mn, s = m.groups()
            return float(h) * 3600 + float(mn) * 60 + float(s)
    except Exception:
        pass
    return None


def main() -> int:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    episodes = catalog["episodes"]

    errors: list[str] = []
    warnings: list[str] = []
    by_band: dict[str, list] = {b: [] for b in BANDS}

    for ep in episodes:
        band = ep["band"]
        if band not in by_band:
            errors.append(f"Unknown band {band} for {ep['id']}")
            continue
        by_band[band].append(ep)

        webm = WEB_VIDEOS / ep["webm"]
        script = ROOT / ep["script"]
        if not script.exists():
            errors.append(f"Missing script: {ep['script']}")
        if not webm.exists():
            if ep.get("status") == "script-only":
                warnings.append(f"Script-only (no webm yet): {ep['webm']}")
            else:
                errors.append(f"Missing webm: {ep['webm']}")
        else:
            dur = probe_duration(webm)
            target = ep["targetDurationSec"]
            if dur is not None:
                if ep.get("status") == "script-only":
                    warnings.append(f"{ep['webm']}: placeholder {dur:.0f}s (target {target}s full)")
                elif ep.get("status") == "pilot" and dur < target * 0.15:
                    warnings.append(f"Pilot {ep['webm']}: {dur:.0f}s (full target {target}s)")

        friends = registry.get("friendsByBand", {}).get(band, {}).get("friends", [])
        friend_names = {f["name"] for f in friends}
        if ep["friend"] not in friend_names:
            errors.append(f"{ep['id']}: friend {ep['friend']} not in registry for {band}")

    for band in BANDS:
        eps = by_band[band]
        if not eps:
            errors.append(f"No Caly and Friends episode for band: {band}")
        else:
            titles = ", ".join(e["title"] for e in eps)
            print(f"  {band}: {len(eps)} episode(s) - {titles}")

    print("\nQC summary")
    print(f"  Episodes: {len(episodes)}")
    print(f"  Errors: {len(errors)}")
    print(f"  Warnings: {len(warnings)}")
    for msg in errors:
        print(f"  ERROR: {msg}")
    for msg in warnings:
        print(f"  WARN: {msg}")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
