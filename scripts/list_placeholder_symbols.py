#!/usr/bin/env python3
"""List placeholder words still needing band-specific art."""

from __future__ import annotations

import json
from pathlib import Path

MANIFEST = Path(__file__).resolve().parents[1] / "band-art-manifest.json"


def main() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    words = data.get("placeholderWords", [])
    print(f"{len(words)} placeholders:")
    for w in words:
        print(w)


if __name__ == "__main__":
    main()
