#!/usr/bin/env python3
"""Remove seed-band PNGs not in baby vocabulary (legacy sprout copies)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VOCAB = ROOT / "vocabulary"
APP_SYM = ROOT.parent / "calyndra-app" / "assets" / "symbols" / "seed"
CONTENT_SYM = ROOT / "symbols" / "images" / "seed"
FLUTTER_SYM = ROOT.parent / "calyndra-mobile-flutter" / "assets" / "symbols" / "seed"

KEEP_EXTRA = frozenset({
    "mommy", "daddy", "friend", "best_friend", "mama", "dada", "little_brother",
})


def allowed_ids() -> set[str]:
    ids: set[str] = set(KEEP_EXTRA)
    words = json.loads((VOCAB / "baby-words.json").read_text(encoding="utf-8"))
    ids.update(s["id"] for s in words.get("symbols", []) if s.get("id"))
    phrases = json.loads((VOCAB / "baby-phrases.json").read_text(encoding="utf-8"))
    ids.update(p["id"] for p in phrases.get("phrases", []) if p.get("id"))
    return ids


def prune_dir(path: Path, allowed: set[str]) -> int:
    if not path.is_dir():
        return 0
    removed = 0
    for png in path.glob("*.png"):
        if png.stem not in allowed:
            png.unlink(missing_ok=True)
            removed += 1
    return removed


def main() -> int:
    allowed = allowed_ids()
    total = 0
    for d in (APP_SYM, CONTENT_SYM, FLUTTER_SYM):
        n = prune_dir(d, allowed)
        if n:
            print(f"Pruned {n} from {d}")
        total += n
    remaining = len(list(APP_SYM.glob("*.png"))) if APP_SYM.is_dir() else 0
    print(f"Done. Removed {total} PNG(s). seed folder now {remaining} file(s), allowed {len(allowed)} ids.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
