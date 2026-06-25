#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Style consistency QC — Caly-universe family symbols and registry alignment."""

from __future__ import annotations

import hashlib
import json
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_SYMBOLS = ROOT.parent / "calyndra-app" / "assets" / "symbols"
PORTRAITS = ROOT.parent / "calyndra-app" / "assets" / "caly-bands"
REGISTRY = ROOT / "caly_character_registry.json"

FAMILY_WORDS = ("mommy", "daddy", "little_brother", "best_friend")
# Bands where each family symbol must exist
FAMILY_BANDS = {
    "mommy": ("seed", "sprout", "bud", "sprig", "vine", "bloom", "canopy"),
    "daddy": ("seed", "sprout", "bud", "sprig", "vine", "bloom", "canopy"),
    "little_brother": ("bud", "sprig", "vine", "bloom", "canopy"),
    "best_friend": ("bud", "sprig", "vine", "bloom", "canopy"),
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def png_hash(path: Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


def png_dimensions(path: Path) -> tuple[int, int] | None:
    try:
        with path.open("rb") as f:
            if f.read(8) != b"\x89PNG\r\n\x1a\n":
                return None
            f.read(4)
            if f.read(4) != b"IHDR":
                return None
            w, h = struct.unpack(">II", f.read(8))
            return w, h
    except OSError:
        return None


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    if not REGISTRY.is_file():
        errors.append("REGISTRY: caly_character_registry.json missing.")
        return 1

    registry = load_json(REGISTRY)
    family = registry.get("familyMembers")
    if not family:
        errors.append("REGISTRY: familyMembers block missing — add Caly-universe mom, dad, little brother.")
    else:
        for key in ("mommy", "daddy", "littleBrother"):
            if key not in family:
                errors.append(f"REGISTRY: familyMembers.{key} missing.")

    child_friends = registry.get("friendsByBand", {}).get("child", {}).get("friends", [])
    river = next((f for f in child_friends if f.get("name") == "River"), None)
    if not river:
        errors.append("REGISTRY: River friend missing from child band.")
    elif not river.get("bestFriend"):
        errors.append("REGISTRY: River must be marked bestFriend in child band.")
    elif river.get("neurodiversityProfile") != "autistic":
        errors.append("REGISTRY: River neurodiversityProfile must be 'autistic'.")

    for word, bands in FAMILY_BANDS.items():
        hashes: dict[str, str] = {}
        for band in bands:
            png = APP_SYMBOLS / band / f"{word}.png"
            if not png.is_file():
                errors.append(f"SYMBOL: missing `{band}/{word}.png` (Caly-universe family art).")
                continue
            dims = png_dimensions(png)
            if dims and (dims[0] < 128 or dims[1] < 128):
                errors.append(f"SYMBOL: `{band}/{word}.png` too small {dims}.")
            h = png_hash(png)
            if h:
                hashes[band] = h
        if len(set(hashes.values())) == 1 and len(hashes) > 1:
            warnings.append(
                f"STYLE: `{word}` identical PNG across all bands — expected band-unique Caly family art."
            )

    # Family symbols must not match unrelated portrait file byte-for-byte (human stock art check)
    for word in ("mommy", "daddy"):
        for band in FAMILY_BANDS[word]:
            sym = APP_SYMBOLS / band / f"{word}.png"
            portrait = PORTRAITS / f"{band}.png"
            if sym.is_file() and portrait.is_file():
                if png_hash(sym) == png_hash(portrait):
                    errors.append(
                        f"STYLE: `{band}/{word}.png` is identical to band portrait — must be distinct family symbol."
                    )

    print(f"Style QC: {len(errors)} issue(s), {len(warnings)} warning(s).")
    for w in warnings:
        print(f"  WARN: {w}")
    for e in errors:
        print(f"  FAIL: {e}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
