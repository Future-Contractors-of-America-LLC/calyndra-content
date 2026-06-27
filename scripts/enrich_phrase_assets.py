#!/usr/bin/env python3
"""Add imageAsset to phrase JSON when band symbol PNG exists."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VOCAB = ROOT / "vocabulary"
APP = ROOT.parent / "calyndra-app" / "content"
SYMS = ROOT.parent / "calyndra-app" / "assets" / "symbols"

AUDIENCE_BAND = {
    "baby": "seed",
    "toddler": "sprout",
    "child": "bud",
    "tween": "sprig",
    "teen": "vine",
    "adult": "bloom",
    "caregiver": "canopy",
}

# phrase id -> symbol file stem when they differ
ALIASES = {
    "all-done": "all_done",
    "dont-like": "no",
    "thank-you": "please",
    "i-need-help": "help",
    "love-you-baby": "love",
    "love-you": "love",
    "night-night": "sleep",
    "up-up": "up",
    "change-diaper": "diaper",
    "more-milk": "milk",
    "more-please": "more",
    "hold-me": "hug",
    "gentle-hands": "gentle",
    "running-late": "wait",
    "repeat-slower": "wait",
}


def symbol_exists(band: str, stem: str) -> bool:
    return (SYMS / band / f"{stem}.png").is_file()


def enrich_phrases(aud: str) -> int:
    band = AUDIENCE_BAND[aud]
    path = VOCAB / f"{aud}-phrases.json"
    if not path.is_file():
        return 0
    doc = json.loads(path.read_text(encoding="utf-8"))
    updated = 0
    for ph in doc.get("phrases", []):
        pid = ph.get("id", "")
        if ph.get("imageAsset") or ph.get("videoShort"):
            continue
        stem = None
        for candidate in (pid, pid.replace("-", "_"), ALIASES.get(pid, "")):
            if candidate and symbol_exists(band, candidate):
                stem = candidate
                break
        if not stem:
            continue
        ph["imageAsset"] = f"assets/symbols/{band}/{stem}.png"
        updated += 1
    if updated:
        path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        if APP.is_dir():
            (APP / path.name).write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"{aud}: enriched {updated} phrase(s) with imageAsset")
    return updated


def main() -> int:
    total = sum(enrich_phrases(aud) for aud in AUDIENCE_BAND)
    print(f"Total enriched: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
