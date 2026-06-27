#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vocabulary UX QC — sort order, words/phrases separation, family symbol presence."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VOCAB = ROOT / "vocabulary"
APP_SYMBOLS = ROOT.parent / "calyndra-app" / "assets" / "symbols"

AUDIENCES = ("baby", "toddler", "child", "tween", "teen", "adult", "caregiver")
BAND_DIRS = {
    "baby": "seed",
    "toddler": "sprout",
    "child": "bud",
    "tween": "sprig",
    "teen": "vine",
    "adult": "bloom",
    "caregiver": "canopy",
}
FAMILY_WORDS = ("mommy", "daddy", "mama", "dada", "best_friend", "friend")
PHRASE_CATEGORIES = {"phrase", "phrases", "nursery-phrase"}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def labels_sorted(symbols: list[dict]) -> bool:
    labels = [str(s.get("label", "")).lower() for s in symbols]
    return labels == sorted(labels)


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    for aud in AUDIENCES:
        words_path = VOCAB / f"{aud}-words.json"
        phrases_path = VOCAB / f"{aud}-phrases.json"
        if not words_path.is_file():
            errors.append(f"WORDS: missing {words_path.name}")
            continue

        words = load_json(words_path)
        symbols = words.get("symbols") or []
        phrase_ids: set[str] = set()
        if phrases_path.is_file():
            phrases = load_json(phrases_path).get("phrases") or []
            phrase_ids = {p.get("id", "") for p in phrases if p.get("id")}
            if phrases and not labels_sorted(phrases):
                errors.append(f"SORT: {aud}-phrases.json not alphabetical by label")
        else:
            warnings.append(f"PHRASES: missing {aud}-phrases.json")

        if symbols and not labels_sorted(symbols):
            errors.append(f"SORT: {aud}-words.json not alphabetical by label")

        for sym in symbols:
            sid = sym.get("id", "")
            cat = (sym.get("category") or "").lower()
            if cat in PHRASE_CATEGORIES or sid in phrase_ids:
                errors.append(f"MIXED: {aud}-words.json contains phrase '{sid}' — move to {aud}-phrases.json")

        band = BAND_DIRS.get(aud, aud)
        band_dir = APP_SYMBOLS / band
        for word in FAMILY_WORDS:
            sym_path = band_dir / f"{word}.png"
            if not sym_path.is_file():
                warnings.append(f"FAMILY: {band}/{word}.png missing")

    for line in warnings:
        print("WARN:", line)
    for line in errors:
        print("FAIL:", line)

    if errors:
        print(f"VOCAB_UX_QC: FAIL ({len(errors)} errors, {len(warnings)} warnings)")
        return 1
    print(f"VOCAB_UX_QC: PASS ({len(warnings)} warnings)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
