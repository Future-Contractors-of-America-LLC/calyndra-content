# -*- coding: utf-8 -*-
"""Episode duration targets per age band (must match caly_friends_catalog.json)."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

try:
    import imageio_ffmpeg

    FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    FFMPEG = "ffmpeg"

DURATION_TARGETS_SEC: dict[str, int] = {
    "baby": 300,      # 5 min
    "toddler": 600,   # 10 min
    "child": 900,     # 15 min
    "tween": 1200,    # 20 min
    "teen": 1800,     # 30 min
    "adult": 2700,    # 45 min
}

SCENE_PACING_SEC = 6
MIN_DURATION_RATIO = 0.85


def scene_count_for_band(band: str) -> int:
    target = DURATION_TARGETS_SEC[band]
    return target // SCENE_PACING_SEC


def probe_duration(path: Path) -> float | None:
    if not path.is_file():
        return None
    try:
        r = subprocess.run([FFMPEG, "-i", str(path)], capture_output=True, text=True)
        m = re.search(r"Duration:\s*(\d+):(\d+):([\d.]+)", r.stderr)
        if m:
            h, mn, s = m.groups()
            return float(h) * 3600 + float(mn) * 60 + float(s)
    except Exception:
        pass
    return None


def meets_duration_target(ep: dict, webm: Path) -> bool:
    target = ep.get("targetDurationSec") or DURATION_TARGETS_SEC.get(ep.get("band", ""), 0)
    if target <= 0:
        return True
    dur = probe_duration(webm)
    if dur is None:
        return False
    return dur >= target * MIN_DURATION_RATIO
