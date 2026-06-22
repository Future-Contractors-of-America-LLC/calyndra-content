#!/usr/bin/env python3
"""Copy band symbol PNGs from calyndra-content to calyndra-app (and Flutter if present)."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT.parent / "calyndra-app"
FLUTTER = ROOT.parent / "calyndra-mobile-flutter"
BANDS = ("sprout", "bud", "sprig", "vine", "bloom", "canopy")


def sync_band(band: str) -> int:
    src_dir = ROOT / "symbols" / "images" / band
    if not src_dir.is_dir():
        return 0
    n = 0
    for png in src_dir.glob("*.png"):
        for base in (APP, FLUTTER):
            if not base.exists():
                continue
            dest = base / "assets" / "symbols" / band / png.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(png, dest)
        n += 1
    return n


def main() -> None:
    total = sum(sync_band(b) for b in BANDS)
    print(f"Synced {total} band symbol PNGs to app bundles.")


if __name__ == "__main__":
    main()
