#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate missing expanded-vocabulary symbol PNGs in Caly-universe tile style."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
APP_SYMBOLS = ROOT.parent / "calyndra-app" / "assets" / "symbols"
PORTRAITS = ROOT.parent / "calyndra-app" / "assets" / "caly-bands"
VOCAB_DIR = ROOT / "vocabulary"
MANIFEST = ROOT / "band-art-manifest.json"
SIZE = 512

AUDIENCE_BAND = {
    "baby": "seed",
    "toddler": "sprout",
    "child": "bud",
    "tween": "sprig",
    "teen": "vine",
    "adult": "bloom",
    "caregiver": "canopy",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def render_tile(band: str, word_id: str, label: str) -> Image.Image:
    tint = (200, 245, 220)
    img = Image.new("RGBA", (SIZE, SIZE), (255, 248, 232, 255))
    draw = ImageDraw.Draw(img)
    for y in range(SIZE):
        g = int(tint[1] * (1 - y / SIZE) + 200 * (y / SIZE))
        draw.line([(0, y), (SIZE, y)], fill=(tint[0], g, tint[2], 255))
    portrait = PORTRAITS / f"{band}.png"
    if band == "seed" and not portrait.is_file():
        portrait = PORTRAITS / "sprout.png"
    if portrait.is_file():
        p = Image.open(portrait).convert("RGBA")
        ph = int(SIZE * 0.45)
        pw = int(p.width * ph / p.height)
        p = p.resize((pw, ph), Image.Resampling.LANCZOS)
        img.paste(p, ((SIZE - pw) // 2, SIZE - ph - 40), p)
    text = (label or word_id)[:14]
    try:
        font = ImageFont.truetype("arial.ttf", 28)
    except OSError:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((SIZE - tw) // 2, 24), text, fill="#2d6a4f", font=font)
    return img.filter(ImageFilter.SHARPEN)


def main() -> int:
    made = skipped = 0
    for aud, band in AUDIENCE_BAND.items():
        vocab_path = VOCAB_DIR / f"{aud}-words.json"
        if not vocab_path.is_file():
            continue
        vocab = load_json(vocab_path)
        for sym in vocab.get("symbols", []):
            asset = sym.get("imageAsset", "")
            word_id = sym.get("id", "")
            if not asset or not word_id:
                continue
            rel = asset.replace("assets/symbols/", "").replace("/", "\\")
            dest = APP_SYMBOLS / rel.replace("\\", "/")
            if dest.is_file():
                skipped += 1
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            render_tile(band, word_id, sym.get("label", word_id)).save(dest, "PNG")
            made += 1
    print(f"Expanded vocab symbols: {made} created, {skipped} already present.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
