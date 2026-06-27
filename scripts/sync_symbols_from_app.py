#!/usr/bin/env python3
"""Copy regenerated symbols from calyndra-app to calyndra-content and Flutter."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_SYM = ROOT.parent / "calyndra-app" / "assets" / "symbols"
CONTENT_SYM = ROOT / "symbols" / "images"
FLUTTER_SYM = ROOT.parent / "calyndra-mobile-flutter" / "assets" / "symbols"
BANDS = ("seed", "sprout", "bud", "sprig", "vine", "bloom", "canopy")


def sync_band(band: str) -> int:
    src = APP_SYM / band
    if not src.is_dir():
        return 0
    n = 0
    for png in src.glob("*.png"):
        for base in (CONTENT_SYM, FLUTTER_SYM):
            dest = base / band / png.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(png, dest)
        n += 1
    return n


def main() -> int:
    total = sum(sync_band(b) for b in BANDS)
    print(f"Synced {total} PNGs per target from calyndra-app -> content + flutter.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
