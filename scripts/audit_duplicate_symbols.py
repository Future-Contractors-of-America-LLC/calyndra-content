#!/usr/bin/env python3
"""Find duplicate symbol PNG hashes within each band (generic reused art)."""

from __future__ import annotations

import hashlib
from collections import defaultdict
from pathlib import Path

APP = Path(__file__).resolve().parents[1].parent / "calyndra-app" / "assets" / "symbols"
BANDS = ("seed", "sprout", "bud", "sprig", "vine", "bloom", "canopy")


def main() -> None:
    for band in BANDS:
        d = APP / band
        if not d.is_dir():
            continue
        by_hash: dict[str, list[str]] = defaultdict(list)
        for p in d.glob("*.png"):
            h = hashlib.sha256(p.read_bytes()).hexdigest()
            by_hash[h].append(p.stem)
        dupes = {h: words for h, words in by_hash.items() if len(words) > 1}
        total_duped = sum(len(w) for w in dupes.values())
        print(f"{band}: {len(dupes)} duplicate hash groups, {total_duped} files in dupes")
        for words in sorted(dupes.values(), key=len, reverse=True)[:3]:
            print(f"  {len(words)}x: {', '.join(sorted(words)[:6])}{'...' if len(words)>6 else ''}")


if __name__ == "__main__":
    main()
