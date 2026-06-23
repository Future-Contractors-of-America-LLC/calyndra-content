#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render band-specific STEP2 symbol tiles from band portraits."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT.parent / "calyndra-app"
BANDS = ("sprout", "bud", "sprig", "vine", "bloom", "canopy")
PORTRAITS = APP / "assets" / "caly-bands"
OUT = (
    Path.home()
    / ".cursor"
    / "projects"
    / "c-Users-Auricrux-OneDrive-Future-Contractors-of-America-LLC"
    / "assets"
)
SIZE = 512

BAND_TINT = {
    "sprout": (210, 255, 230),
    "bud": (200, 245, 220),
    "sprig": (190, 235, 210),
    "vine": (180, 225, 200),
    "bloom": (170, 215, 190),
    "canopy": (160, 205, 180),
}

BAND_HUE = {
    "sprout": 1.00,
    "bud": 1.03,
    "sprig": 1.06,
    "vine": 1.09,
    "bloom": 1.12,
    "canopy": 1.15,
}

STEP2_WORDS = [
    "crib", "blocks", "splash", "clap", "peek", "cuddle", "lullaby", "yum", "owie", "blankie",
    "potty", "bubbles", "sandbox", "truck", "puzzle", "sticker", "wagon", "cereal", "yogurt", "tricycle",
    "science", "guitar", "soccer", "birthday", "museum", "camping", "scooter", "tablet", "spelling", "kite",
    "algebra", "presentation", "permission", "detention", "orchestra", "robotics", "podcast", "charger",
    "earbuds", "debate", "volunteer", "mindfulness", "syllabus", "textbook", "yearbook",
    "drivers-license", "internship", "scholarship", "credit-card", "rideshare", "diploma", "tuition",
    "roommate", "budget", "streaming", "social-media", "part-time", "parking", "copay", "gig-work",
    "mortgage", "retirement", "taxes", "benefits", "pension", "warranty", "subscription",
    "direct-deposit", "overtime", "performance-review", "onboarding", "hr", "contractor",
    "regulation", "patience", "breathe", "visual-schedule", "celebrate", "modeling",
    "scaffold", "prompt-wait", "reinforcement",
]


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


def load_portrait(band: str) -> Image.Image:
    path = PORTRAITS / f"{band}.png"
    img = Image.open(path).convert("RGBA")
    scale = 0.62
    w, h = img.size
    img = img.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
    return ImageEnhance.Color(img).enhance(BAND_HUE[band])


def pictogram(draw: ImageDraw.ImageDraw, word: str, cx: int, cy: int, band: str) -> None:
    offsets = {"sprout": 0, "bud": 4, "sprig": 8, "vine": 12, "bloom": 16, "canopy": 20}
    o = offsets[band]
    outline = "#2d6a4f"
    fill = "#ff8fab"
    accent = "#52b788"
    key = sum(ord(c) for c in word) % 5
    if key == 0:
        draw.ellipse([cx - 60 + o, cy - 60, cx + 60 + o, cy + 60], outline=outline, width=6, fill=accent)
    elif key == 1:
        draw.rectangle([cx - 55 + o, cy - 45, cx + 55 + o, cy + 45], outline=outline, width=6, fill=fill)
    elif key == 2:
        draw.polygon([(cx + o, cy - 65), (cx + 65 + o, cy + 55), (cx - 65 + o, cy + 55)], outline=outline, fill=accent)
    elif key == 3:
        draw.rounded_rectangle([cx - 70 + o, cy - 35, cx + 70 + o, cy + 35], radius=18, outline=outline, width=6, fill=fill)
    else:
        draw.chord([cx - 65 + o, cy - 65, cx + 65 + o, cy + 65], 30, 150, outline=outline, width=6, fill=accent)
    for i in range(3 + o // 4):
        draw.ellipse([cx + 80 + i * 7, cy - 80 + i * 5, cx + 88 + i * 7, cy - 72 + i * 5], fill=outline)


def render(word: str, band: str) -> Image.Image:
    base = gradient(BAND_TINT[band])
    portrait = load_portrait(band)
    px = 20 + {"sprout": 0, "bud": 2, "sprig": 4, "vine": 6, "bloom": 8, "canopy": 10}[band]
    py = SIZE - portrait.size[1] - 10
    base.paste(portrait, (px, py), portrait)
    draw = ImageDraw.Draw(base)
    pictogram(draw, word, SIZE - 140, SIZE // 2 - 20, band)
    seed = int(hashlib.md5(f"{word}-{band}".encode()).hexdigest()[:6], 16)
    draw.rectangle([0, 0, 3 + seed % 5, 3 + seed % 4], fill=BAND_TINT[band])
    return base.filter(ImageFilter.SHARPEN)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    skip_existing = "--force" not in sys.argv
    made = 0
    for word in STEP2_WORDS:
        for band in BANDS:
            dest = OUT / f"{word}-{band}.png"
            if skip_existing and dest.exists():
                continue
            render(word, band).save(dest, "PNG")
            made += 1
    print(f"Rendered {made} tiles -> {OUT}")


if __name__ == "__main__":
    main()
