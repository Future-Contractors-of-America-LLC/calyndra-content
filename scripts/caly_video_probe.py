#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Probe WebM resolution and duration via ffmpeg stderr."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

try:
    import imageio_ffmpeg

    FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    FFMPEG = "ffmpeg"

UHD_WIDTH = 3840
UHD_HEIGHT = 2160
HD_WIDTH = 1920
HD_HEIGHT = 1080


def probe_duration(path: Path) -> float | None:
    if not path.is_file():
        return None
    try:
        result = subprocess.run([FFMPEG, "-i", str(path)], capture_output=True, text=True, check=False)
        match = re.search(r"Duration:\s*(\d+):(\d+):([\d.]+)", result.stderr)
        if match:
            hours, minutes, seconds = match.groups()
            return float(hours) * 3600 + float(minutes) * 60 + float(seconds)
    except Exception:
        pass
    return None


def probe_resolution(path: Path) -> tuple[int, int] | None:
    if not path.is_file():
        return None
    try:
        result = subprocess.run([FFMPEG, "-i", str(path)], capture_output=True, text=True, check=False)
        match = re.search(r"(\d{3,5})x(\d{3,5})", result.stderr)
        if match:
            return int(match.group(1)), int(match.group(2))
    except Exception:
        pass
    return None


def profile_from_resolution(width: int, height: int) -> str:
    if width >= UHD_WIDTH and height >= UHD_HEIGHT:
        return "uhd"
    if width >= HD_WIDTH and height >= HD_HEIGHT:
        return "hd"
    if width >= 1280 and height >= 720:
        return "draft"
    return "sub-hd"


def resolve_webm_path(ep: dict, *roots: Path) -> Path | None:
    name = ep.get("webm") or ""
    if not name:
        return None
    for root in roots:
        candidate = root / name
        if candidate.is_file():
            return candidate
    return None
