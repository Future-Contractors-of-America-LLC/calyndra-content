#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render hand-visible AAC symbols with explicit five-finger hands on band portraits."""

from __future__ import annotations

import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT.parent / "calyndra-app"
PORTRAITS = APP / "assets" / "caly-bands"
OUT = (
    Path.home()
    / ".cursor"
    / "projects"
    / "c-Users-Auricrux-OneDrive-Future-Contractors-of-America-LLC"
    / "assets"
    / "hand-visible"
)
META = ROOT / "symbols" / "meta"
SIZE = 512
BANDS = ("seed", "sprout", "bud", "sprig", "vine", "bloom", "canopy")

HAND_VISIBLE = (
    "help", "more", "stop", "wait", "please", "love", "hug", "clap", "wash", "wet",
    "listen", "open", "close", "want", "need", "modeling", "scaffold", "prompt-wait",
    "reinforcement", "yes", "no", "again", "celebrate", "cuddle", "peek",
    "up", "down", "hot", "cold", "dry", "big", "little", "friend", "mommy", "daddy",
    "symbol_help", "symbol_more",
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

BAND_HUE = {
    "seed": 0.98,
    "sprout": 1.00,
    "bud": 1.03,
    "sprig": 1.06,
    "vine": 1.09,
    "bloom": 1.12,
    "canopy": 1.15,
}

PORTRAIT_BAND = {
    "seed": "seed",
    "sprout": "sprout",
    "bud": "bud",
    "sprig": "sprig",
    "vine": "vine",
    "bloom": "bloom",
    "canopy": "canopy",
}

OUTLINE = "#2d6a4f"
SKIN = "#ffcba4"
PALM = "#f4a582"


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
    src = PORTRAIT_BAND.get(band, band)
    path = PORTRAITS / f"{src}.png"
    img = Image.open(path).convert("RGBA")
    scale = 0.58 if band != "seed" else 0.52
    w, h = img.size
    img = img.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
    return ImageEnhance.Color(img).enhance(BAND_HUE[band])


def finger_arc(cx: float, cy: float, angle_deg: float, length: float, width: float) -> list[tuple[float, float]]:
    """Five points along a finger from knuckle."""
    rad = math.radians(angle_deg)
    return [
        (cx + math.cos(rad) * length * t, cy + math.sin(rad) * length * t)
        for t in (0.0, 0.35, 0.65, 0.85, 1.0)
    ]


def draw_hand(
    draw: ImageDraw.ImageDraw,
    cx: int,
    cy: int,
    scale: float,
    palm_angle: float,
    finger_spread: float,
    mirror: bool = False,
) -> None:
    """Draw palm + exactly five distinct fingers."""
    s = scale
    sign = -1 if mirror else 1
    palm_w, palm_h = 34 * s, 42 * s
    draw.ellipse(
        [cx - palm_w, cy - palm_h, cx + palm_w, cy + palm_h],
        fill=PALM,
        outline=OUTLINE,
        width=max(2, int(3 * s)),
    )
    base_angles = [-finger_spread * 2, -finger_spread, 0, finger_spread, finger_spread * 2]
    lengths = [0.72, 0.88, 0.95, 0.82, 0.68]
    for i, (ang_off, flen) in enumerate(zip(base_angles, lengths)):
        angle = palm_angle + sign * ang_off
        pts = finger_arc(cx, cy - 8 * s, angle, 52 * s * flen, 8 * s)
        draw.line(pts, fill=SKIN, width=max(3, int(7 * s)))
        draw.ellipse(
            [pts[-1][0] - 5 * s, pts[-1][1] - 5 * s, pts[-1][0] + 5 * s, pts[-1][1] + 5 * s],
            fill=SKIN,
            outline=OUTLINE,
            width=max(1, int(2 * s)),
        )


def draw_gesture(draw: ImageDraw.ImageDraw, word: str, band: str) -> None:
    o = {"seed": 0, "sprout": 2, "bud": 4, "sprig": 6, "vine": 8, "bloom": 10, "canopy": 12}[band]
    cx, cy = SIZE - 145 + o, SIZE // 2 - 10
    s = 1.0 + o * 0.02

    if word in ("help", "symbol_help", "want", "need"):
        draw_hand(draw, cx, cy, s, -90, 14)
    elif word in ("more", "symbol_more", "please"):
        draw_hand(draw, cx - 35, cy + 10, s, -100, 12)
        draw_hand(draw, cx + 35, cy + 10, s, -80, 12, mirror=True)
    elif word in ("stop", "wait", "prompt-wait", "no"):
        draw_hand(draw, cx, cy, s * 1.1, -90, 8)
        draw.line([(cx - 55 * s, cy - 70 * s), (cx + 55 * s, cy + 70 * s)], fill="#e63946", width=int(8 * s))
    elif word in ("clap", "celebrate", "yes", "again"):
        draw_hand(draw, cx - 28, cy, s, -70, 16)
        draw_hand(draw, cx + 28, cy, s, -110, 16, mirror=True)
    elif word in ("wash", "wet", "dry"):
        draw_hand(draw, cx, cy, s, -95, 13)
        for i in range(4):
            draw.ellipse(
                [cx - 60 + i * 18, cy - 90 - i * 8, cx - 42 + i * 18, cy - 72 - i * 8],
                outline="#48cae4",
                width=3,
            )
    elif word == "listen":
        draw_hand(draw, cx + 40, cy + 20, s * 0.9, -60, 10, mirror=True)
        draw.arc([cx - 70, cy - 90, cx + 10, cy - 10], 200, 340, fill=OUTLINE, width=4)
    elif word in ("open", "close"):
        draw_hand(draw, cx, cy, s, -85, 11)
        draw.rectangle([cx - 80, cy - 60, cx + 20, cy + 40], outline="#8d5524", width=5)
    elif word in ("hug", "love", "cuddle", "friend"):
        draw_hand(draw, cx - 40, cy, s, -75, 14)
        draw_hand(draw, cx + 40, cy, s, -105, 14, mirror=True)
        draw.ellipse([cx - 18, cy - 55, cx + 18, cy - 19], fill="#ff8fab", outline=OUTLINE, width=3)
    elif word in ("up",):
        draw_hand(draw, cx, cy + 30, s, -110, 12)
        draw.polygon([(cx, cy - 95), (cx - 25, cy - 55), (cx + 25, cy - 55)], fill=OUTLINE)
    elif word in ("down",):
        draw_hand(draw, cx, cy - 20, s, -70, 12)
        draw.polygon([(cx, cy + 75), (cx - 25, cy + 35), (cx + 25, cy + 35)], fill=OUTLINE)
    elif word in ("hot", "cold"):
        draw_hand(draw, cx, cy, s, -90, 12)
        icon = "?" if word == "hot" else "?"
        draw.text((cx - 20, cy - 95), icon, fill=OUTLINE)
    elif word in ("big", "little"):
        draw_hand(draw, cx - 30, cy, s, -90, 12)
        r = 45 if word == "big" else 18
        draw.ellipse([cx + 10, cy - r, cx + 10 + 2 * r, cy + r], outline=OUTLINE, width=5)
    elif word in ("mommy", "daddy", "peek"):
        draw_hand(draw, cx, cy, s, -90, 14)
    elif word in ("modeling", "scaffold", "reinforcement"):
        draw_hand(draw, cx - 25, cy, s, -85, 13)
        draw_hand(draw, cx + 35, cy - 15, s * 0.85, -95, 11, mirror=True)
    else:
        draw_hand(draw, cx, cy, s, -90, 13)


def render(word: str, band: str) -> Image.Image:
    base = gradient(BAND_TINT[band])
    portrait = load_portrait(band)
    px = 16 + {"seed": 0, "sprout": 0, "bud": 2, "sprig": 4, "vine": 6, "bloom": 8, "canopy": 10}[band]
    py = SIZE - portrait.size[1] - 12
    base.paste(portrait, (px, py), portrait)
    draw = ImageDraw.Draw(base)
    draw_gesture(draw, word, band)
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
                "reviewedUtc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "source": "render_hand_visible_symbols.py",
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def main() -> None:
    words = HAND_VISIBLE
    if len(sys.argv) > 1:
        words = tuple(sys.argv[1:])
    OUT.mkdir(parents=True, exist_ok=True)
    made = 0
    for word in words:
        for band in BANDS:
            dest = OUT / f"{word}-{band}.png"
            render(word, band).save(dest, "PNG")
            write_sidecar(word, band)
            made += 1
    print(f"Rendered {made} hand-visible tiles -> {OUT}")


if __name__ == "__main__":
    main()
