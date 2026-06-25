# -*- coding: utf-8 -*-
"""Audio specialist: narration mastering for cartoon episodes."""
from __future__ import annotations

import subprocess
from pathlib import Path

from caly_video_quality import FFMPEG, PROFILE_NAME

# Broadcast-friendly loudness targets
_LOUDNORM = "loudnorm=I=-16:TP=-1.5:LRA=11"
_CHAIN = f"highpass=f=80,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120,{_LOUDNORM}"


def master_narration(src: Path, dest: Path | None = None) -> Path:
    """Apply EQ, compression, and loudness normalization to TTS clip."""
    out = dest or src.with_name(f"{src.stem}_mastered.mp3")
    q = "0" if PROFILE_NAME == "uhd" else "2"
    subprocess.run(
        [
            FFMPEG,
            "-y",
            "-i",
            str(src),
            "-af",
            _CHAIN,
            "-c:a",
            "libmp3lame",
            "-q:a",
            q,
            str(out),
        ],
        check=True,
        capture_output=True,
    )
    return out
