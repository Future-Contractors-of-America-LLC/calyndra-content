#!/usr/bin/env python3
"""Install generated symbols and report progress."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = Path.home() / ".cursor" / "projects" / "c-Users-Auricrux-OneDrive-Future-Contractors-of-America-LLC" / "assets"
STEP2_WORDS = 82
BANDS = 6
EXPECTED = STEP2_WORDS * BANDS


def count_assets() -> int:
    if not ASSETS.is_dir():
        return 0
    return len(list(ASSETS.glob("*-*.png")))


def main() -> None:
    n = count_assets()
    print(f"Assets dir: {n}/{EXPECTED} step2 images")
    if n == 0:
        return
    subprocess.run([sys.executable, str(ROOT / "scripts" / "install_generated_symbols.py")], check=False)
    subprocess.run([sys.executable, str(ROOT / "scripts" / "sync_band_symbol_dirs.py")], check=False)
    subprocess.run([sys.executable, str(ROOT / "scripts" / "qc_band_assets.py")], check=False)


if __name__ == "__main__":
    main()
