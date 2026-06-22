# -*- coding: utf-8 -*-
"""Sync symbol PNGs from calyndra-content to Flutter and web bundles."""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FLUTTER = ROOT.parent / "calyndra-mobile-flutter"
WEB = ROOT.parent / "calyndra-app"
STYLES = ("sprout", "bud", "sprig", "vine", "bloom", "canopy", "quest", "spark", "core")


def sync() -> int:
    n = 0
    for style in STYLES:
        src_dir = ROOT / "symbols" / "images" / style
        if not src_dir.exists():
            continue
        for png in src_dir.glob("*.png"):
            for base in (FLUTTER, WEB):
                dest = base / "assets" / "symbols" / style / png.name
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(png, dest)
            n += 1
    for name in (
        "toddler-core.json",
        "child-vocab.json",
        "tween-vocab.json",
        "teen-vocab.json",
        "adult-vocab.json",
        "caregiver-vocab.json",
        "child-expanded.json",
        "teen-adult-functional.json",
    ):
        src = ROOT / "vocabulary" / name
        if src.exists():
            shutil.copy2(src, FLUTTER / "assets" / "vocabulary" / name)
            shutil.copy2(src, WEB / "content" / name)
    print(f"Synced {n} symbol PNGs + vocabulary JSON.")
    return n


if __name__ == "__main__":
    sync()
