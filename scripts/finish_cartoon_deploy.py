#!/usr/bin/env python3
"""After full cartoon renders: update catalog status, sync Flutter, run QC."""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "videos" / "caly_friends_catalog.json"
APP_VIDEOS = ROOT.parent / "calyndra-app" / "videos"
FLUTTER_VIDEOS = ROOT.parent / "calyndra-mobile-flutter" / "assets" / "videos"
FF = imageio_ffmpeg.get_ffmpeg_exe()
MIN_RATIO = 0.85


def probe_duration(path: Path) -> float:
    r = subprocess.run([FF, "-i", str(path)], capture_output=True, text=True)
    m = re.search(r"Duration:\s*(\d+):(\d+):([\d.]+)", r.stderr)
    if not m:
        return 0.0
    h, mn, s = m.groups()
    return float(h) * 3600 + float(mn) * 60 + float(s)


def main() -> int:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    FLUTTER_VIDEOS.mkdir(parents=True, exist_ok=True)
    updated = 0
    lines: list[str] = []

    for ep in catalog["episodes"]:
        webm = APP_VIDEOS / ep["webm"]
        target = ep["targetDurationSec"]
        if not webm.exists():
            lines.append(f"MISSING {ep['id']}")
            continue
        dur = probe_duration(webm)
        ratio = dur / target if target else 0
        ok = ratio >= MIN_RATIO
        lines.append(f"{ep['id']}: {dur:.0f}s / {target}s ({ratio * 100:.0f}%) {'FULL' if ok else 'SHORT'}")
        if ok and ep.get("status") != "full":
            ep["status"] = "full"
            ep["pilot"] = False
            ep["renderedUtc"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            updated += 1
        shutil.copy2(webm, FLUTTER_VIDEOS / webm.name)

    CATALOG_PATH.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    print(f"Catalog: {updated} episode(s) marked full")
    for line in lines:
        print(line)

    qc = subprocess.run([sys.executable, str(ROOT / "scripts/qc_cartoon_catalog.py")], cwd=str(ROOT))
    return qc.returncode


if __name__ == "__main__":
    sys.exit(main())
