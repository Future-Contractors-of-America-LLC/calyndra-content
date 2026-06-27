#!/usr/bin/env python3
"""Sort vocabulary and phrase JSON files alphabetically by label."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VOCAB = ROOT / "vocabulary"
AUDIENCES = ("baby", "toddler", "child", "tween", "teen", "adult", "caregiver")


def sort_file(path: Path, key: str, list_key: str) -> bool:
    if not path.is_file():
        return False
    data = json.loads(path.read_text(encoding="utf-8"))
    items = data.get(list_key)
    if not items:
        return False
    sorted_items = sorted(items, key=lambda x: str(x.get(key, "")).lower())
    if items == sorted_items:
        return False
    data[list_key] = sorted_items
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return True


def main() -> int:
    changed = 0
    for aud in AUDIENCES:
        words = VOCAB / f"{aud}-words.json"
        phrases = VOCAB / f"{aud}-phrases.json"
        if sort_file(words, "label", "symbols"):
            print(f"Sorted {words.name}")
            changed += 1
        if sort_file(phrases, "label", "phrases"):
            print(f"Sorted {phrases.name}")
            changed += 1
    print(f"Done. {changed} file(s) updated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
