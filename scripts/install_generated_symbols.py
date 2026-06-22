#!/usr/bin/env python3
"""Install generated {word}-{band}.png files into content + app symbol folders."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT.parent / "calyndra-app"
CURSOR_ASSETS = Path.home() / ".cursor" / "projects" / "c-Users-Auricrux-OneDrive-Future-Contractors-of-America-LLC" / "assets"
BANDS = ("sprout", "bud", "sprig", "vine", "bloom", "canopy")


def install(src_dir: Path) -> int:
    n = 0
    for png in sorted(src_dir.glob("*-*.png")):
        stem = png.stem
        if "-" not in stem:
            continue
        word, band = stem.split("-", 1)
        if band not in BANDS:
            continue
        for base in (ROOT / "symbols" / "images", APP / "assets" / "symbols"):
            dest = base / band / f"{word}.png"
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(png, dest)
        n += 1
        print(f"  {word}.png -> {band}/")
    return n


def main() -> None:
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else CURSOR_ASSETS
    if not src.is_dir():
        print(f"No asset dir: {src}")
        raise SystemExit(1)
    count = install(src)
    print(f"Installed {count} symbol(s).")


if __name__ == "__main__":
    main()
