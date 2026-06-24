#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Procedural friend portraits: band Caly portrait plus warm animal companion."""

from __future__ import annotations

import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT.parent / "calyndra-app"
BANDS_DIR = APP / "assets" / "caly-bands"
OUT_DIR = APP / "assets" / "caly-friends"
SIZE = 512
OUTLINE = "#2d6a4f"
SKIN = "#ffcba4"

FRIENDS: tuple[tuple[str, str, str, str], ...] = (
    ("pip-baby.png", "seed", "Pip", "bunny"),
    ("fern-toddler.png", "sprout", "Fern", "fox"),
    ("moss-child.png", "bud", "Moss", "bear"),
    ("reed-tween.png", "sprig", "Reed", "owl"),
    ("sage-teen.png", "vine", "Sage", "deer"),
    ("laurel-adult.png", "bloom", "Laurel", "cardinal"),
    ("elder-oak-caregiver.png", "canopy", "Elder Oak", "oak"),
)

BAND_TINT = {
    "seed": (220, 250, 235),
    "sprout": (210, 255, 230),
    "bud": (200, 245, 220),
    "sprig": (190, 235, 210),
    "vine": (180, 225, 200),
    "bloom": (170, 215, 190),
    "canopy": (160, 205, 180),
}


def gradient(bg: tuple[int, int, int]) -> Image.Image:
    img = Image.new("RGB", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(img)
    for y in range(SIZE):
        t = y / SIZE
        r = int(bg[0] * (1 - t) + 180 * t)
        g = int(bg[1] * (1 - t) + 230 * t)
        b = int(bg[2] * (1 - t) + 255 * t)
        draw.line([(0, y), (SIZE, y)], fill=(r, g, b))
    return img


def load_band(band: str, target_h: int) -> Image.Image:
    path = BANDS_DIR / f"{band}.png"
    img = Image.open(path).convert("RGBA")
    scale = target_h / img.size[1]
    img = img.resize((int(img.size[0] * scale), target_h), Image.Resampling.LANCZOS)
    return ImageEnhance.Color(img).enhance(1.02)


def draw_five_finger_wave(draw: ImageDraw.ImageDraw, cx: int, cy: int, s: float) -> None:
    palm = "#f4a582"
    draw.ellipse([cx - 14 * s, cy - 18 * s, cx + 14 * s, cy + 18 * s], fill=palm, outline=OUTLINE, width=max(2, int(2 * s)))
    for ang, flen in zip((-28, -14, 0, 14, 28), (0.7, 0.88, 0.95, 0.82, 0.68)):
        rad = math.radians(-100 + ang)
        ex = cx + math.cos(rad) * 38 * s * flen
        ey = cy + math.sin(rad) * 38 * s * flen
        draw.line([(cx, cy - 6 * s), (ex, ey)], fill=SKIN, width=max(2, int(5 * s)))
        draw.ellipse([ex - 4 * s, ey - 4 * s, ex + 4 * s, ey + 4 * s], fill=SKIN, outline=OUTLINE, width=1)


def draw_bunny(draw: ImageDraw.ImageDraw, cx: int, cy: int, s: float) -> None:
    fur = "#f8f0e8"
    draw.ellipse([cx - 55 * s, cy - 20 * s, cx + 55 * s, cy + 70 * s], fill=fur, outline=OUTLINE, width=4)
    draw.ellipse([cx - 35 * s, cy - 75 * s, cx - 5 * s, cy + 5 * s], fill=fur, outline=OUTLINE, width=3)
    draw.ellipse([cx + 5 * s, cy - 75 * s, cx + 35 * s, cy + 5 * s], fill=fur, outline=OUTLINE, width=3)
    draw.ellipse([cx - 22 * s, cy - 8 * s, cx - 8 * s, cy + 6 * s], fill="#2d6a4f")
    draw.ellipse([cx + 8 * s, cy - 8 * s, cx + 22 * s, cy + 6 * s], fill="#2d6a4f")
    draw.arc([cx - 18 * s, cy + 8 * s, cx + 18 * s, cy + 28 * s], 10, 170, fill="#ff8fab", width=3)
    draw_five_finger_wave(draw, cx + 48 * s, cy + 30 * s, 0.55 * s)


def draw_fox(draw: ImageDraw.ImageDraw, cx: int, cy: int, s: float) -> None:
    orange = "#e07a3a"
    draw.polygon([(cx, cy - 60 * s), (cx - 50 * s, cy + 30 * s), (cx + 50 * s, cy + 30 * s)], fill=orange, outline=OUTLINE, width=3)
    draw.polygon([(cx - 38 * s, cy - 45 * s), (cx - 55 * s, cy - 85 * s), (cx - 18 * s, cy - 35 * s)], fill=orange, outline=OUTLINE, width=2)
    draw.polygon([(cx + 38 * s, cy - 45 * s), (cx + 55 * s, cy - 85 * s), (cx + 18 * s, cy - 35 * s)], fill=orange, outline=OUTLINE, width=2)
    draw.ellipse([cx - 40 * s, cy - 15 * s, cx + 40 * s, cy + 45 * s], fill="#ffe8d0", outline=OUTLINE, width=3)
    draw.ellipse([cx - 18 * s, cy - 5 * s, cx - 6 * s, cy + 7 * s], fill=OUTLINE)
    draw.ellipse([cx + 6 * s, cy - 5 * s, cx + 18 * s, cy + 7 * s], fill=OUTLINE)
    draw.polygon([(cx - 6 * s, cy + 12 * s), (cx, cy + 22 * s), (cx + 6 * s, cy + 12 * s)], fill=OUTLINE)
    for fx, fy in [(cx - 55, cy - 10), (cx + 45, cy - 5), (cx - 20, cy + 55)]:
        draw.ellipse([fx - 8 * s, fy - 8 * s, fx + 8 * s, fy + 8 * s], fill="#ff8fab", outline=OUTLINE, width=2)


def draw_bear(draw: ImageDraw.ImageDraw, cx: int, cy: int, s: float) -> None:
    brown = "#8b5a3c"
    draw.ellipse([cx - 60 * s, cy - 25 * s, cx + 60 * s, cy + 65 * s], fill=brown, outline=OUTLINE, width=4)
    draw.ellipse([cx - 70 * s, cy - 55 * s, cx - 30 * s, cy - 15 * s], fill=brown, outline=OUTLINE, width=3)
    draw.ellipse([cx + 30 * s, cy - 55 * s, cx + 70 * s, cy - 15 * s], fill=brown, outline=OUTLINE, width=3)
    draw.ellipse([cx - 38 * s, cy - 20 * s, cx + 38 * s, cy + 30 * s], fill="#c49a6c", outline=OUTLINE, width=3)
    draw.ellipse([cx - 20 * s, cy - 8 * s, cx - 8 * s, cy + 4 * s], fill=OUTLINE)
    draw.ellipse([cx + 8 * s, cy - 8 * s, cx + 20 * s, cy + 4 * s], fill=OUTLINE)
    draw.ellipse([cx - 8 * s, cy + 8 * s, cx + 8 * s, cy + 20 * s], fill="#5c3d2e")
    draw_five_finger_wave(draw, cx - 62 * s, cy + 20 * s, 0.5 * s)


def draw_owl(draw: ImageDraw.ImageDraw, cx: int, cy: int, s: float) -> None:
    body = "#6b4f3a"
    draw.ellipse([cx - 55 * s, cy - 40 * s, cx + 55 * s, cy + 60 * s], fill=body, outline=OUTLINE, width=4)
    draw.ellipse([cx - 45 * s, cy - 55 * s, cx - 5 * s, cy - 15 * s], fill="#f5f0e8", outline=OUTLINE, width=3)
    draw.ellipse([cx + 5 * s, cy - 55 * s, cx + 45 * s, cy - 15 * s], fill="#f5f0e8", outline=OUTLINE, width=3)
    draw.ellipse([cx - 32 * s, cy - 42 * s, cx - 12 * s, cy - 22 * s], fill=OUTLINE)
    draw.ellipse([cx + 12 * s, cy - 42 * s, cx + 32 * s, cy - 22 * s], fill=OUTLINE)
    draw.polygon([(cx - 8 * s, cy - 18 * s), (cx, cy - 8 * s), (cx + 8 * s, cy - 18 * s)], fill="#f4a582")
    draw.arc([cx - 20 * s, cy + 5 * s, cx + 20 * s, cy + 25 * s], 15, 165, fill="#ff8fab", width=3)


def draw_deer(draw: ImageDraw.ImageDraw, cx: int, cy: int, s: float) -> None:
    tan = "#c9a87c"
    draw.ellipse([cx - 45 * s, cy - 15 * s, cx + 45 * s, cy + 55 * s], fill=tan, outline=OUTLINE, width=4)
    draw.ellipse([cx - 35 * s, cy - 50 * s, cx + 35 * s, cy + 5 * s], fill="#e8d4b8", outline=OUTLINE, width=3)
    draw.line([(cx - 25 * s, cy - 48 * s), (cx - 35 * s, cy - 90 * s)], fill=OUTLINE, width=4)
    draw.line([(cx - 15 * s, cy - 50 * s), (cx - 5 * s, cy - 88 * s)], fill=OUTLINE, width=4)
    draw.line([(cx + 15 * s, cy - 50 * s), (cx + 5 * s, cy - 88 * s)], fill=OUTLINE, width=4)
    draw.line([(cx + 25 * s, cy - 48 * s), (cx + 35 * s, cy - 90 * s)], fill=OUTLINE, width=4)
    draw.ellipse([cx - 16 * s, cy - 28 * s, cx - 4 * s, cy - 16 * s], fill=OUTLINE)
    draw.ellipse([cx + 4 * s, cy - 28 * s, cx + 16 * s, cy - 16 * s], fill=OUTLINE)
    draw.ellipse([cx - 10 * s, cy - 10 * s, cx + 10 * s, cy + 5 * s], fill="#8b6914")


def draw_cardinal(draw: ImageDraw.ImageDraw, cx: int, cy: int, s: float) -> None:
    red = "#d62828"
    draw.ellipse([cx - 40 * s, cy - 20 * s, cx + 40 * s, cy + 50 * s], fill=red, outline=OUTLINE, width=3)
    draw.polygon([(cx + 30 * s, cy - 15 * s), (cx + 70 * s, cy - 5 * s), (cx + 35 * s, cy + 10 * s)], fill=red, outline=OUTLINE, width=2)
    draw.ellipse([cx - 25 * s, cy - 45 * s, cx + 25 * s, cy + 5 * s], fill=red, outline=OUTLINE, width=3)
    draw.polygon([(cx, cy - 50 * s), (cx + 12 * s, cy - 35 * s), (cx - 2 * s, cy - 30 * s)], fill="#f4a582")
    draw.ellipse([cx - 10 * s, cy - 28 * s, cx - 2 * s, cy - 20 * s], fill=OUTLINE)
    draw.ellipse([cx + 2 * s, cy - 28 * s, cx + 10 * s, cy - 20 * s], fill=OUTLINE)


def draw_oak(draw: ImageDraw.ImageDraw, cx: int, cy: int, s: float) -> None:
    trunk = "#6b4423"
    draw.rounded_rectangle([cx - 22 * s, cy - 10 * s, cx + 22 * s, cy + 75 * s], radius=8, fill=trunk, outline=OUTLINE, width=3)
    draw.ellipse([cx - 75 * s, cy - 95 * s, cx + 75 * s, cy + 25 * s], fill="#52b788", outline=OUTLINE, width=4)
    draw.ellipse([cx - 55 * s, cy - 75 * s, cx - 15 * s, cy - 35 * s], fill="#74c69d", outline=OUTLINE, width=2)
    draw.ellipse([cx + 15 * s, cy - 80 * s, cx + 60 * s, cy - 35 * s], fill="#74c69d", outline=OUTLINE, width=2)
    for i in range(5):
        ax = cx - 40 * s + i * 20 * s
        draw.ellipse([ax - 10 * s, cy - 70 * s, ax + 10 * s, cy - 50 * s], fill="#95d5b2", outline=OUTLINE, width=1)


DRAWERS = {
    "bunny": draw_bunny,
    "fox": draw_fox,
    "bear": draw_bear,
    "owl": draw_owl,
    "deer": draw_deer,
    "cardinal": draw_cardinal,
    "oak": draw_oak,
}


def render_portrait(band: str, name: str, species: str) -> Image.Image:
    base = gradient(BAND_TINT[band])
    caly = load_band(band, 340)
    px = 8
    py = SIZE - caly.size[1] - 10
    base.paste(caly, (px, py), caly)
    overlay = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    DRAWERS[species](draw, int(SIZE * 0.72), int(SIZE * 0.58), 1.0)
    base = Image.alpha_composite(base.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(base)
    draw.rounded_rectangle((6, 6, SIZE - 6, SIZE - 6), radius=24, outline=OUTLINE, width=4)
    try:
        font = ImageFont.truetype("arialbd.ttf", 22)
    except OSError:
        font = ImageFont.load_default()
    label = name
    tw = draw.textlength(label, font=font)
    draw.rounded_rectangle((SIZE - tw - 28, 12, SIZE - 10, 44), radius=12, fill="#fff8e8", outline=OUTLINE, width=2)
    draw.text((SIZE - tw - 18, 16), label, fill=OUTLINE, font=font)
    return base.filter(ImageFilter.SHARPEN)


def main() -> None:
    force = "--force" in sys.argv
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    made = 0
    for fname, band, name, species in FRIENDS:
        dest = OUT_DIR / fname
        if dest.exists() and not force:
            print(f"  skip {fname}")
            continue
        render_portrait(band, name, species).save(dest, "PNG")
        print(f"  wrote {dest.name}")
        made += 1
    print(f"Generated {made} friend portrait(s) -> {OUT_DIR}")


if __name__ == "__main__":
    main()
