#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate gentle instrumental music beds for Caly Show sing-along episodes."""

from __future__ import annotations

import json
import math
import struct
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "games" / "sing-along-catalog.json"
APP_OUT = ROOT.parent / "calyndra-app" / "content" / "sing-along" / "music"
CONTENT_OUT = ROOT / "content" / "sing-along" / "music"

SAMPLE_RATE = 44100
BASE_FREQ = {"baby": 392.0, "toddler": 440.0, "child": 494.0, "tween": 523.25,
             "teen": 587.33, "adult": 659.25, "caregiver": 440.0}


def audience_from_episode_id(eid: str) -> str:
    prefix = eid.split("-")[0]
    mapping = {"seed": "baby", "sprout": "toddler", "bud": "child", "sprig": "tween",
               "vine": "teen", "bloom": "adult", "canopy": "caregiver"}
    return mapping.get(prefix, "toddler")


def synth_bed(loop_ms: int, audience: str) -> list[float]:
    """32–45s loopable bed — caly-show.js sets audio.loop=true."""
    duration_ms = min(loop_ms, 45_000)
    samples = int(SAMPLE_RATE * duration_ms / 1000)
    root = BASE_FREQ.get(audience, 440.0)
    pent = [root, root * 1.125, root * 1.25, root * 1.5, root * 1.6875]
    buf: list[float] = []
    beat_hz = 0.75 if audience in ("baby", "toddler") else 1.0
    for i in range(samples):
        t = i / SAMPLE_RATE
        tone = 0.0
        for j, f in enumerate(pent):
            tone += math.sin(2 * math.pi * f * t) * (0.12 / (j + 1))
        pulse = 0.5 + 0.5 * math.sin(2 * math.pi * beat_hz * t)
        env = min(1.0, i / (SAMPLE_RATE * 2), (samples - i) / (SAMPLE_RATE * 3))
        buf.append(max(-1.0, min(1.0, tone * pulse * env * 0.55)))
    return buf


def write_wav(path: Path, samples: list[float]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        frames = b"".join(struct.pack("<h", int(s * 32767 * 0.9)) for s in samples)
        wf.writeframes(frames)


def main() -> int:
    if not CATALOG.is_file():
        print("Run gen_sing_along_catalog.py first.")
        return 1
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    made = 0
    for aud, block in catalog.get("audiences", {}).items():
        for ep in block.get("episodes", []):
            bed = ep.get("musicBed")
            if not bed:
                continue
            rel = bed.replace("content/sing-along/music/", "")
            duration = int(ep.get("durationMs") or 180_000)
            audience = audience_from_episode_id(ep.get("id", aud))
            samples = synth_bed(duration, audience)
            for out_root in (APP_OUT, CONTENT_OUT):
                dest = out_root / rel
                write_wav(dest, samples)
            made += 1
            print(f"  {rel} ({duration // 1000}s)")
    print(f"Generated {made} sing-along music bed(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
