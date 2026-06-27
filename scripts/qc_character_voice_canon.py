#!/usr/bin/env python3
"""QC character voice canon uniqueness."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANON = ROOT / "character_voice_canon.json"


def main() -> int:
    if not CANON.is_file():
        print("Character voice QC FAIL: character_voice_canon.json missing — run build_character_voice_canon.py")
        return 1

    data = json.loads(CANON.read_text(encoding="utf-8"))
    chars = data.get("characters") or []
    if len(chars) < 40:
        print(f"Character voice QC FAIL: only {len(chars)} characters (expected >=40)")
        return 1

    tuples: dict[tuple, str] = {}
    for ch in chars:
        tts = ch.get("tts") or {}
        key = (tts.get("voice"), tts.get("rate"), tts.get("pitch"))
        cid = ch.get("id", "?")
        if key in tuples:
            print(f"Character voice QC FAIL: duplicate tuple {key} for {cid} and {tuples[key]}")
            return 1
        tuples[key] = cid

    print(f"Character voice QC PASS — {len(chars)} characters, {len(tuples)} unique tuples")
    return 0


if __name__ == "__main__":
    sys.exit(main())
