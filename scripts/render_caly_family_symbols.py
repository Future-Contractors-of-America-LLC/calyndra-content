#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render Caly-universe family AAC symbols — plant mascots, not human portraits."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT.parent / "calyndra-app"
PORTRAITS = APP / "assets" / "caly-bands"
SYMBOLS = APP / "assets" / "symbols"
META = ROOT / "symbols" / "meta"
SIZE = 512
OUTLINE = "#2d6a4f"

BAND_TINT = {
    "seed": (220, 250, 235),
    "sprout": (210, 255, 230),
    "bud": (200, 245, 220),
    "sprig": (190, 235, 210),
    "vine": (180, 225, 200),
    "bloom": (170, 215, 190),
    "canopy": (160, 205, 180),
}

FAMILY_SPECS = {
    "mommy": {
        "bands": ("seed", "sprout", "bud", "sprig", "vine", "bloom", "canopy"),
        "scale": 1.05,
        "accessory": "flower_crown",
        "label": "Mom",
    },
    "daddy": {
        "bands": ("seed", "sprout", "bud", "sprig", "vine", "bloom", "canopy"),
        "scale": 1.08,
        "accessory": "leaf_cap",
        "label": "Dad",
    },
    "little_brother": {
        "bands": ("bud", "sprig", "vine", "bloom", "canopy"),
        "scale": 0.78,
        "accessory": "tiny_leaves",
        "label": "Bro",
    },
    "best_friend": {
        "bands": ("bud", "sprig", "vine", "bloom", "canopy"),
        "scale": 0.92,
        "accessory": "river_beaver",
        "label": "River",
    },
    "friend": {
        "bands": ("seed", "sprout", "bud", "sprig", "vine", "bloom", "canopy"),
        "scale": 0.9,
        "accessory": "river_beaver",
        "label": "Friend",
    },
    "mama": {
        "bands": ("seed", "sprout"),
        "scale": 1.02,
        "accessory": "flower_crown",
        "label": "Mama",
    },
    "dada": {
        "bands": ("seed", "sprout"),
        "scale": 1.04,
        "accessory": "leaf_cap",
        "label": "Dada",
    },
}


def gradient(tint: tuple[int, int, int]) -> Image.Image:
    img = Image.new("RGBA", (SIZE, SIZE), (255, 248, 232, 255))
    draw = ImageDraw.Draw(img)
    for y in range(SIZE):
        blend = y / SIZE
        r = int(tint[0] * (1 - blend) + 126 * blend)
        g = int(tint[1] * (1 - blend) + 200 * blend)
        b = int(tint[2] * (1 - blend) + 255 * blend)
        draw.line([(0, y), (SIZE, y)], fill=(r, g, b, 255))
    return img


def load_portrait(band: str) -> Image.Image | None:
    path = PORTRAITS / f"{band}.png"
    if not path.is_file() and band == "seed":
        path = PORTRAITS / "sprout.png"
    if not path.is_file():
        return None
    return Image.open(path).convert("RGBA")


def draw_hand(draw: ImageDraw.ImageDraw, cx: int, cy: int, scale: float, angle: float, fingers: int = 5) -> None:
    palm = int(22 * scale)
    draw.ellipse([cx - palm, cy - palm, cx + palm, cy + palm], fill=OUTLINE)
    for i in range(fingers):
        a = angle + (i - 2) * 14
        import math

        rad = math.radians(a)
        fx = cx + int(math.cos(rad) * 38 * scale)
        fy = cy + int(math.sin(rad) * 38 * scale)
        draw.line([(cx, cy), (fx, fy)], fill=OUTLINE, width=int(5 * scale))


def draw_accessory(draw: ImageDraw.ImageDraw, kind: str, band: str) -> None:
    if kind == "flower_crown":
        for i, x in enumerate(range(180, 340, 40)):
            draw.ellipse([x, 48, x + 28, 76], fill="#ff8fab", outline=OUTLINE, width=2)
    elif kind == "leaf_cap":
        draw.polygon([(256, 40), (200, 90), (312, 90)], fill="#52b788", outline=OUTLINE)
    elif kind == "tiny_leaves":
        draw.ellipse([230, 55, 250, 75], fill="#95d5b2", outline=OUTLINE, width=2)
        draw.ellipse([262, 50, 282, 70], fill="#95d5b2", outline=OUTLINE, width=2)
    elif kind == "river_beaver":
        draw.ellipse([200, 380, 312, 430], fill="#8B5A2B", outline=OUTLINE, width=3)
        draw.ellipse([220, 360, 260, 400], fill="#A0724A", outline=OUTLINE, width=2)
        draw.rectangle([270, 395, 310, 415], fill="#5C4033", outline=OUTLINE, width=2)


def render_family(word: str, band: str, spec: dict) -> Image.Image:
    base = gradient(BAND_TINT[band])
    portrait = load_portrait(band)
    scale = spec["scale"]
    draw = ImageDraw.Draw(base)
    if portrait:
        pw, ph = portrait.size
        target_h = int(SIZE * 0.55 * scale)
        target_w = int(pw * target_h / ph)
        portrait = portrait.resize((target_w, target_h), Image.Resampling.LANCZOS)
        px = (SIZE - target_w) // 2
        py = SIZE - target_h - 24
        base.paste(portrait, (px, py), portrait)
    draw_accessory(draw, spec["accessory"], band)
    draw_hand(draw, SIZE // 2 + 90, SIZE // 2 + 40, 0.9 * scale, -70)
    draw_hand(draw, SIZE // 2 - 90, SIZE // 2 + 40, 0.9 * scale, -110)
    return base.filter(ImageFilter.SHARPEN)


def write_sidecar(word: str, band: str) -> None:
    path = META / band / f"{word}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "wordId": word,
                "band": band,
                "handFingers": 5,
                "expression": "happy",
                "style": "caly-universe-family",
                "reviewedUtc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "source": "render_caly_family_symbols.py",
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def main() -> int:
    made = 0
    for word, spec in FAMILY_SPECS.items():
        for band in spec["bands"]:
            dest = SYMBOLS / band / f"{word}.png"
            dest.parent.mkdir(parents=True, exist_ok=True)
            render_family(word, band, spec).save(dest, "PNG")
            write_sidecar(word, band)
            made += 1
            print(f"  {band}/{word}.png")
    print(f"Rendered {made} Caly-universe family symbol(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
