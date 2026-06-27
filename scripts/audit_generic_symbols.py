#!/usr/bin/env python3
"""Report symbol PNGs that are byte-identical to band portrait (generic placeholders)."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT.parent / "calyndra-app" / "assets"
PORTRAITS = APP / "caly-bands"
SYMS = APP / "symbols"
BANDS = ("seed", "sprout", "bud", "sprig", "vine", "bloom", "canopy")


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    total_generic = 0
    for band in BANDS:
        portrait = PORTRAITS / f"{band}.png"
        if not portrait.is_file() and band == "seed":
            portrait = PORTRAITS / "sprout.png"
        if not portrait.is_file():
            continue
        ph = file_hash(portrait)
        band_dir = SYMS / band
        if not band_dir.is_dir():
            continue
        pngs = list(band_dir.glob("*.png"))
        generic = [p.stem for p in pngs if file_hash(p) == ph]
        total_generic += len(generic)
        print(f"{band}: {len(generic)}/{len(pngs)} portrait-identical")
        if generic:
            print("  ", ", ".join(sorted(generic)[:12]), ("..." if len(generic) > 12 else ""))
    print(f"Total generic: {total_generic}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
