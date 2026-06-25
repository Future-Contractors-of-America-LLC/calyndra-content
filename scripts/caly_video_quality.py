# -*- coding: utf-8 -*-
"""Shared motion-picture render profile for Calyndra cartoon episodes."""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

from PIL import Image

try:
    import imageio_ffmpeg

    FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    FFMPEG = "ffmpeg"

_PROFILE = os.environ.get("CALY_VIDEO_PROFILE", "uhd" if os.environ.get("CALY_SHIP") else "hd").strip().lower()

if _PROFILE in ("uhd", "4k", "ultra"):
    VIDEO_WIDTH = 3840
    VIDEO_HEIGHT = 2160
    VP9_CRF = 20
    VP9_TILE_COLUMNS = 3
    AUDIO_BITRATE = "256k"
    PROFILE_NAME = "uhd"
elif _PROFILE in ("draft", "preview"):
    VIDEO_WIDTH = 1280
    VIDEO_HEIGHT = 720
    VP9_CRF = 32
    VP9_TILE_COLUMNS = 1
    AUDIO_BITRATE = "96k"
    PROFILE_NAME = "draft"
else:
    VIDEO_WIDTH = 1920
    VIDEO_HEIGHT = 1080
    VP9_CRF = 18
    VP9_TILE_COLUMNS = 2
    AUDIO_BITRATE = "192k"
    PROFILE_NAME = "hd"

VIDEO_FPS = 24
# Layout/design baseline was 1280x720
DESIGN_WIDTH = 1280
DESIGN_HEIGHT = 720
SCALE = VIDEO_WIDTH / DESIGN_WIDTH


def scale(n: int | float) -> int:
    return int(round(n * SCALE))


def fit_frame(img: Image.Image) -> Image.Image:
    if img.size == (VIDEO_WIDTH, VIDEO_HEIGHT):
        return img
    return img.resize((VIDEO_WIDTH, VIDEO_HEIGHT), Image.Resampling.LANCZOS)


def write_segment(frames: list[Image.Image], path: Path) -> None:
    """Encode scene clip with high-quality VP9 (CRF, not default 32)."""
    if not frames:
        raise ValueError("no frames")
    w, h = frames[0].size
    cmd = [
        FFMPEG,
        "-y",
        "-f",
        "rawvideo",
        "-pix_fmt",
        "rgb24",
        "-s",
        f"{w}x{h}",
        "-r",
        str(VIDEO_FPS),
        "-i",
        "pipe:0",
        "-an",
        "-c:v",
        "libvpx-vp9",
        "-crf",
        str(VP9_CRF),
        "-b:v",
        "0",
        "-row-mt",
        "1",
        "-tile-columns",
        str(VP9_TILE_COLUMNS),
        "-pix_fmt",
        "yuv420p",
        str(path),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    assert proc.stdin is not None
    try:
        for frame in frames:
            rgb = frame.convert("RGB")
            if rgb.size != (w, h):
                rgb = fit_frame(rgb)
            proc.stdin.write(rgb.tobytes())
    finally:
        proc.stdin.close()
    stderr = proc.stderr.read().decode("utf-8", errors="replace") if proc.stderr else ""
    code = proc.wait()
    if code != 0:
        raise RuntimeError(f"ffmpeg VP9 encode failed ({code}): {stderr[-500:]}")


def mux_av(video: Path, audio: Path, out: Path) -> bool:
    """Mux mastered narration; copy video stream (fade applied during frame gen)."""
    try:
        from caly_audio_master import master_narration

        mastered = master_narration(audio, audio.parent / f"{audio.stem}_m.mp3")
    except Exception:
        mastered = audio
    try:
        subprocess.run(
            [
                FFMPEG,
                "-y",
                "-i",
                str(video),
                "-i",
                str(mastered),
                "-c:v",
                "copy",
                "-c:a",
                "libopus",
                "-b:a",
                AUDIO_BITRATE,
                "-shortest",
                str(out),
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def encode_still_webm(dest: Path, img: Image.Image, seconds: float) -> bool:
    png = dest.with_suffix(".png")
    fit_frame(img).save(png)
    try:
        subprocess.run(
            [
                FFMPEG,
                "-y",
                "-loop",
                "1",
                "-i",
                str(png),
                "-c:v",
                "libvpx-vp9",
                "-crf",
                str(VP9_CRF),
                "-b:v",
                "0",
                "-t",
                str(seconds),
                "-pix_fmt",
                "yuv420p",
                "-an",
                str(dest),
            ],
            check=True,
            capture_output=True,
        )
        return dest.exists()
    except subprocess.CalledProcessError:
        return False
    finally:
        png.unlink(missing_ok=True)
