#!/usr/bin/env python3
"""Rebuild *-vocab.json and toddler-core.json from separated words + phrases files."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VOCAB = ROOT / "vocabulary"
APP = ROOT.parent / "calyndra-app" / "content"
AUDIENCES = ("baby", "toddler", "child", "tween", "teen", "adult", "caregiver")
COMBINED_NAMES = {
    "baby": "baby-vocab.json",
    "toddler": "toddler-core.json",
    "child": "child-vocab.json",
    "tween": "tween-vocab.json",
    "teen": "teen-vocab.json",
    "adult": "adult-vocab.json",
    "caregiver": "caregiver-vocab.json",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    for aud in AUDIENCES:
        words_path = VOCAB / f"{aud}-words.json"
        phrases_path = VOCAB / f"{aud}-phrases.json"
        if not words_path.is_file():
            continue
        words = load(words_path)
        phrases = load(phrases_path) if phrases_path.is_file() else {"phrases": []}
        combined = {
            "id": words.get("id", f"{aud}-vocab").replace("-words", "-vocab"),
            "title": words.get("title", "").replace("Words", "Vocabulary"),
            "description": words.get("description", ""),
            "ageBand": words.get("ageBand", aud),
            "nickname": words.get("nickname", ""),
            "symbols": words.get("symbols", []),
            "phrases": phrases.get("phrases", []),
        }
        name = COMBINED_NAMES[aud]
        write(VOCAB / name, combined)
        if APP.is_dir():
            write(APP / name, combined)
        print(f"Rebuilt {name}: {len(combined['symbols'])} words, {len(combined['phrases'])} phrases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
