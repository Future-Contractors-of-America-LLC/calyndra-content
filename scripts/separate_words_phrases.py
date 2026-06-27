#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Move phrase-only IDs out of *-words.json into *-phrases.json (if missing there)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VOCAB = ROOT / "vocabulary"
APP = ROOT.parent / "calyndra-app" / "content"
AUDIENCES = ("baby", "toddler", "child", "tween", "teen", "adult", "caregiver")

# IDs that exist in phrases files — must not appear in words files
PHRASE_ONLY_HINTS = frozenset({
    "all-done", "dont-like", "thank-you", "schedule-change",
    "clarify", "privacy", "repeat-slower", "running-late", "allergy",
})


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sort_phrases(phrases: list[dict]) -> list[dict]:
    return sorted(phrases, key=lambda p: str(p.get("label", "")).lower())


def sort_symbols(symbols: list[dict]) -> list[dict]:
    return sorted(symbols, key=lambda s: str(s.get("label", "")).lower())


def process_audience(aud: str) -> int:
    words_path = VOCAB / f"{aud}-words.json"
    phrases_path = VOCAB / f"{aud}-phrases.json"
    if not words_path.is_file():
        return 0
    words_doc = load_json(words_path)
    phrases_doc = load_json(phrases_path) if phrases_path.is_file() else {
        "id": f"{aud}-phrases",
        "title": f"Phrases ({aud})",
        "ageBand": aud,
        "phrases": [],
    }
    phrase_ids = {p.get("id") for p in phrases_doc.get("phrases", [])}
    moved = 0
    kept: list[dict] = []
    for sym in words_doc.get("symbols", []):
        sid = sym.get("id", "")
        if sid in phrase_ids or sid in PHRASE_ONLY_HINTS:
            if sid not in phrase_ids:
                phrases_doc.setdefault("phrases", []).append({
                    "id": sid,
                    "label": sym.get("label", sid),
                    "category": sym.get("category") or "phrase",
                    "speakText": sym.get("label", sid),
                })
                phrase_ids.add(sid)
            moved += 1
            continue
        kept.append(sym)
    if not moved:
        return 0
    words_doc["symbols"] = sort_symbols(kept)
    phrases_doc["phrases"] = sort_phrases(phrases_doc.get("phrases", []))
    write_json(words_path, words_doc)
    write_json(phrases_path, phrases_doc)
    for base in (APP,):
        if base.is_dir():
            write_json(base / words_path.name, words_doc)
            write_json(base / phrases_path.name, phrases_doc)
    print(f"{aud}: moved {moved} phrase id(s) out of words")
    return moved


def main() -> int:
    total = sum(process_audience(aud) for aud in AUDIENCES)
    print(f"Done. {total} symbol(s) moved to phrases.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
