#!/usr/bin/env python3
"""Ensure band-named symbol folders exist (sprout,bud,sprig,vine,bloom,canopy)."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
APP_SYMBOLS = ROOT / "calyndra-app" / "assets" / "symbols"
CONTENT_SYMBOLS = ROOT / "calyndra-content" / "symbols" / "images"
BANDS = ("sprout", "bud", "sprig", "vine", "bloom", "canopy")
SOURCE = "sprout"


def sync_dir(base: Path) -> None:
    src = base / SOURCE
    if not src.is_dir():
        print(f"skip {base}: no {SOURCE}/")
        return
    for band in BANDS:
        if band == SOURCE:
            continue
        dst = base / band
        dst.mkdir(parents=True, exist_ok=True)
        for png in src.glob("*.png"):
            target = dst / png.name
            if not target.exists():
                shutil.copy2(png, target)
        print(f"{dst.relative_to(ROOT)}: {len(list(dst.glob('*.png')))} png")


def main() -> None:
    sync_dir(APP_SYMBOLS)
    if CONTENT_SYMBOLS.parent.exists():
        sync_dir(CONTENT_SYMBOLS)


if __name__ == "__main__":
    main()
