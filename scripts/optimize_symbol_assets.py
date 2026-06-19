# -*- coding: utf-8 -*-
"""Resize and compress Calyndra symbol PNGs for fast mobile loading."""
from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT.parent
TARGETS = [
    BASE / "calyndra-app" / "assets" / "symbols",
    BASE / "calyndra-mobile-flutter" / "assets" / "symbols",
    ROOT / "symbols" / "images",
]
MASCOTS = [
    BASE / "calyndra-app" / "assets",
    BASE / "calyndra-mobile-flutter" / "assets" / "images",
]
SIZE = 512
WEBP_QUALITY = 82
PNG_OPTIMIZE = True


def process_png(path: Path) -> tuple[int, int]:
  """Return (before_bytes, after_bytes) for PNG + WebP sibling."""
  before = path.stat().st_size
  img = Image.open(path).convert("RGBA")
  img = img.resize((SIZE, SIZE), Image.Resampling.LANCZOS)
  # Flatten to RGB on white for smaller PNG
  bg = Image.new("RGB", (SIZE, SIZE), (255, 255, 255))
  bg.paste(img, mask=img.split()[3] if img.mode == "RGBA" else None)
  bg.save(path, "PNG", optimize=PNG_OPTIMIZE)
  webp = path.with_suffix(".webp")
  bg.save(webp, "WEBP", quality=WEBP_QUALITY, method=6)
  after = path.stat().st_size + webp.stat().st_size
  return before, after


def main() -> None:
  total_before = 0
  total_after = 0
  count = 0
  for root in TARGETS:
    if not root.exists():
      continue
    for png in root.rglob("*.png"):
      b, a = process_png(png)
      total_before += b
      total_after += a
      count += 1
      print(f"  {png.name}: {b//1024}KB -> {(a)//1024}KB (png+webp)")

  for masc_dir in MASCOTS:
    for name in ("caly_sprout.png", "caly_quest.png", "caly_guide.png", "caly_spark.png", "caly_core.png"):
      p = masc_dir / name
      if p.exists():
        b, a = process_png(p)
        total_before += b
        total_after += a
        count += 1
        print(f"  mascot {name}: {b//1024}KB -> {a//1024}KB")

  print(f"Done: {count} assets, {total_before//1024//1024}MB -> {total_after//1024//1024}MB")


if __name__ == "__main__":
  main()
