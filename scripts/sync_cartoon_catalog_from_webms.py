#!/usr/bin/env python3
"""Mark catalog episodes complete when full WebM exists in calyndra-app."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "videos" / "caly_friends_catalog.json"
APP_VIDEOS = ROOT.parent / "calyndra-app" / "videos"
APP_CATALOG = ROOT.parent / "calyndra-app" / "content" / "videos" / "caly_friends_catalog.json"
FLUTTER_VIDEOS = ROOT.parent / "calyndra-mobile-flutter" / "assets" / "videos"
MIN_BYTES = 500_000

try:
    from caly_video_quality import FFMPEG, PROFILE_NAME, VIDEO_FPS, VIDEO_HEIGHT, VIDEO_WIDTH
except ImportError:
    FFMPEG = "ffmpeg"
    PROFILE_NAME = "hd"
    VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_FPS = 1920, 1080, 24


def probe_webm(webm: Path) -> dict[str, object]:
    meta: dict[str, object] = {}
    try:
        r = subprocess.run([FFMPEG, "-i", str(webm)], capture_output=True, text=True)
        import re

        m = re.search(r"(\d{3,4})x(\d{3,4})", r.stderr)
        if m:
            meta["videoResolution"] = f"{m.group(1)}x{m.group(2)}"
            w, h = int(m.group(1)), int(m.group(2))
            if w >= 3840:
                meta["videoProfile"] = "uhd"
            elif w >= 1920:
                meta["videoProfile"] = "hd"
            else:
                meta["videoProfile"] = "draft"
        m = re.search(r"(\d+(?:\.\d+)?)\s*fps", r.stderr)
        if m:
            meta["videoFps"] = int(float(m.group(1)))
    except Exception:
        pass
    return meta


def main() -> int:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    updated = 0
    for ep in catalog["episodes"]:
        webm = APP_VIDEOS / ep["webm"]
        if webm.is_file() and webm.stat().st_size >= MIN_BYTES:
            probed = probe_webm(webm)
            if ep.get("status") != "complete":
                ep["status"] = "complete"
                ep["pilot"] = False
                ep["renderedUtc"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                updated += 1
            for key, val in probed.items():
                if ep.get(key) != val:
                    ep[key] = val
                    updated += 1
            FLUTTER_VIDEOS.mkdir(parents=True, exist_ok=True)
            dest = FLUTTER_VIDEOS / ep["webm"]
            if not dest.exists() or dest.stat().st_size < webm.stat().st_size:
                shutil.copy2(webm, dest)
    catalog["lockedUtc"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    text = json.dumps(catalog, indent=2) + "\n"
    CATALOG.write_text(text, encoding="utf-8")
    APP_CATALOG.parent.mkdir(parents=True, exist_ok=True)
    APP_CATALOG.write_text(text, encoding="utf-8")
    print(f"Updated {updated} episode(s) to complete")
    pending = sum(1 for e in catalog["episodes"] if e.get("status") == "script-only")
    print(f"Pending script-only: {pending}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
