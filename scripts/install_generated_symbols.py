#!/usr/bin/env python3
"""Install generated {word}-{band}.png files into content + app symbol folders."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT.parent / "calyndra-app"
CURSOR_ASSETS = Path.home() / ".cursor" / "projects" / "c-Users-Auricrux-OneDrive-Future-Contractors-of-America-LLC" / "assets"
BANDS = ("seed", "sprout", "bud", "sprig", "vine", "bloom", "canopy")


def parse_stem(stem: str) -> tuple[str, str] | None:
    """Return (word_id, band) when stem ends with a known band suffix."""
    for band in BANDS:
        suffix = f"-{band}"
        if stem.endswith(suffix):
            word = stem[: -len(suffix)]
            if word:
                return word, band
    return None


def install(src_dir: Path) -> int:
    n = 0
    for png in sorted(src_dir.glob("*-*.png")):
        parsed = parse_stem(png.stem)
        if not parsed:
            continue
        word, band = parsed
        dest = APP / "assets" / "symbols" / band / f"{word}.png"
        dest.parent.mkdir(parents=True, exist_ok=True)
        data = png.read_bytes()
        dest.write_bytes(data)
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
