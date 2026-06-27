#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regenerate band word symbols — word-specific gestures, Caly-universe family art.

Replaces portrait-identical (generic) PNGs and renders family/friend symbols.
Output: calyndra-app/assets/symbols/{band}/{word_id}.png
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT.parent / "calyndra-app"
PORTRAITS = APP / "assets" / "caly-bands"
SYMBOLS = APP / "assets" / "symbols"
VOCAB = ROOT / "vocabulary"
META = ROOT / "symbols" / "meta"
SIZE = 512

BANDS = ("seed", "sprout", "bud", "sprig", "vine", "bloom", "canopy")
AUDIENCE_BAND = {
    "baby": "seed",
    "toddler": "sprout",
    "child": "bud",
    "tween": "sprig",
    "teen": "vine",
    "adult": "bloom",
    "caregiver": "canopy",
}

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

OUTLINE = "#2d6a4f"
SKIN = "#ffcba4"
PALM = "#f4a582"

# Load family renderer from sibling script
_family_mod_path = ROOT / "scripts" / "render_caly_family_symbols.py"
_spec = importlib.util.spec_from_file_location("render_caly_family_symbols", _family_mod_path)
_family_mod = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(_family_mod)

FAMILY_WORDS = frozenset(_family_mod.FAMILY_SPECS.keys())


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def portrait_hash(band: str) -> str | None:
    path = PORTRAITS / f"{band}.png"
    if not path.is_file() and band == "seed":
        path = PORTRAITS / "sprout.png"
    return file_hash(path) if path.is_file() else None


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
    if not path.is_file() and band == "seed":
        path = PORTRAITS / "sprout.png"
    img = Image.open(path).convert("RGBA")
    scale = 0.52 if band == "seed" else 0.58
    w, h = img.size
    img = img.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
    return ImageEnhance.Color(img).enhance(BAND_HUE[band])


def finger_arc(cx: float, cy: float, angle_deg: float, length: float) -> list[tuple[float, float]]:
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
    for ang_off, flen in zip(base_angles, lengths):
        angle = palm_angle + sign * ang_off
        pts = finger_arc(cx, cy - 8 * s, angle, 52 * s * flen)
        draw.line(pts, fill=SKIN, width=max(3, int(7 * s)))
        draw.ellipse(
            [pts[-1][0] - 5 * s, pts[-1][1] - 5 * s, pts[-1][0] + 5 * s, pts[-1][1] + 5 * s],
            fill=SKIN,
            outline=OUTLINE,
            width=max(1, int(2 * s)),
        )


def pictogram(draw: ImageDraw.ImageDraw, word: str, cx: int, cy: int, band: str) -> None:
    """Word-specific prop icon (not generic portrait)."""
    o = {"seed": 0, "sprout": 2, "bud": 4, "sprig": 6, "vine": 8, "bloom": 10, "canopy": 12}[band]
    fill = "#ff8fab"
    accent = "#52b788"
    w = word.replace("-", "_")

    if w in ("eat", "yum", "cereal", "yogurt", "snack", "hungry"):
        draw.polygon([(cx + o, cy - 50), (cx - 40 + o, cy + 40), (cx + 40 + o, cy + 40)], fill=accent, outline=OUTLINE, width=4)
        draw.rectangle([cx + 30 + o, cy - 70, cx + 50 + o, cy + 10], fill=fill, outline=OUTLINE, width=3)
    elif w in ("drink", "milk", "water", "juice", "bottle"):
        draw.polygon([(cx - 35 + o, cy - 45), (cx + 35 + o, cy - 45), (cx + 20 + o, cy + 45), (cx - 20 + o, cy + 45)], fill="#48cae4", outline=OUTLINE, width=4)
    elif w in ("bathroom", "potty", "toilet", "diaper"):
        draw.rounded_rectangle([cx - 45 + o, cy - 30, cx + 45 + o, cy + 50], radius=12, fill="#e8f4f8", outline=OUTLINE, width=4)
        draw.ellipse([cx - 35 + o, cy - 55, cx + 35 + o, cy - 5], outline=OUTLINE, width=4)
    elif w in ("sleep", "night_night", "lullaby", "tired", "blankie"):
        draw.polygon([(cx - 50 + o, cy + 30), (cx + 50 + o, cy + 30), (cx + o, cy - 40)], fill=accent, outline=OUTLINE, width=4)
        draw.ellipse([cx + 25 + o, cy - 70, cx + 55 + o, cy - 40], fill="#ffeaa7", outline=OUTLINE, width=3)
    elif w in ("play", "toy", "blocks", "bubbles", "sandbox", "puzzle"):
        draw.ellipse([cx - 50 + o, cy - 20, cx + 50 + o, cy + 50], fill=fill, outline=OUTLINE, width=4)
    elif w in ("home", "house"):
        draw.polygon([(cx + o, cy - 55), (cx - 55 + o, cy + 5), (cx + 55 + o, cy + 5)], fill=accent, outline=OUTLINE, width=4)
        draw.rectangle([cx - 40 + o, cy + 5, cx + 40 + o, cy + 55], fill=fill, outline=OUTLINE, width=3)
    elif w in ("school", "homework", "read", "book", "spelling"):
        draw.rectangle([cx - 45 + o, cy - 50, cx + 45 + o, cy + 50], fill="#fff", outline=OUTLINE, width=4)
        draw.line([(cx + o, cy - 50), (cx + o, cy + 50)], fill=OUTLINE, width=3)
    elif w in ("happy", "excited", "celebrate"):
        draw.arc([cx - 45 + o, cy - 45, cx + 45 + o, cy + 45], 200, 340, fill=OUTLINE, width=5)
    elif w in ("sad", "hurt", "owie", "pain"):
        draw.arc([cx - 45 + o, cy, cx + 45 + o, cy + 60], 20, 160, fill=OUTLINE, width=5)
    elif w in ("car", "bus", "wagon", "tricycle", "scooter"):
        draw.ellipse([cx - 55 + o, cy, cx - 15 + o, cy + 40], fill=OUTLINE)
        draw.ellipse([cx + 15 + o, cy, cx + 55 + o, cy + 40], fill=OUTLINE)
        draw.rounded_rectangle([cx - 50 + o, cy - 35, cx + 50 + o, cy + 15], radius=8, fill=accent, outline=OUTLINE, width=3)
    elif w in ("friend",):
        draw.ellipse([cx - 55 + o, cy - 15, cx - 5 + o, cy + 45], fill=accent, outline=OUTLINE, width=4)
        draw.ellipse([cx + 5 + o, cy - 15, cx + 55 + o, cy + 45], fill=fill, outline=OUTLINE, width=4)
        draw_hand(draw, cx - 30 + o, cy + 55, 0.7, -90, 12)
        draw_hand(draw, cx + 30 + o, cy + 55, 0.7, -90, 12, mirror=True)
    elif w in ("music", "guitar", "sing"):
        draw.ellipse([cx - 40 + o, cy, cx + o, cy + 40], fill=OUTLINE)
        draw.rectangle([cx + o, cy - 50, cx + 20 + o, cy + 20], fill=OUTLINE)
    elif w in ("dog", "cat", "pet"):
        draw.ellipse([cx - 40 + o, cy - 20, cx + 40 + o, cy + 40], fill="#d4a574", outline=OUTLINE, width=4)
        draw.polygon([(cx + 30 + o, cy - 35), (cx + 50 + o, cy - 55), (cx + 55 + o, cy - 25)], fill="#d4a574", outline=OUTLINE)
    else:
        key = sum(ord(c) for c in word) % 5
        if key == 0:
            draw.ellipse([cx - 55 + o, cy - 55, cx + 55 + o, cy + 55], outline=OUTLINE, width=5, fill=accent)
        elif key == 1:
            draw.rectangle([cx - 50 + o, cy - 40, cx + 50 + o, cy + 40], outline=OUTLINE, width=5, fill=fill)
        elif key == 2:
            draw.polygon([(cx + o, cy - 60), (cx + 60 + o, cy + 50), (cx - 60 + o, cy + 50)], outline=OUTLINE, fill=accent)
        elif key == 3:
            draw.rounded_rectangle([cx - 65 + o, cy - 35, cx + 65 + o, cy + 35], radius=16, outline=OUTLINE, width=5, fill=fill)
        else:
            draw.chord([cx - 60 + o, cy - 60, cx + 60 + o, cy + 60], 30, 150, outline=OUTLINE, width=5, fill=accent)


def draw_gesture(draw: ImageDraw.ImageDraw, word: str, band: str) -> None:
    o = {"seed": 0, "sprout": 2, "bud": 4, "sprig": 6, "vine": 8, "bloom": 10, "canopy": 12}[band]
    cx, cy = SIZE - 145 + o, SIZE // 2 - 10
    s = 1.0 + o * 0.02
    w = word.replace("-", "_")

    if w in FAMILY_WORDS:
        return
    if w in ("help", "want", "need", "i_need_help"):
        draw_hand(draw, cx, cy, s, -90, 14)
    elif w in ("more", "please"):
        draw_hand(draw, cx - 35, cy + 10, s, -100, 12)
        draw_hand(draw, cx + 35, cy + 10, s, -80, 12, mirror=True)
    elif w in ("stop", "wait", "no"):
        draw_hand(draw, cx, cy, s * 1.1, -90, 8)
        draw.line([(cx - 55 * s, cy - 70 * s), (cx + 55 * s, cy + 70 * s)], fill="#e63946", width=int(8 * s))
    elif w in ("yes", "all_done", "again", "clap"):
        draw_hand(draw, cx - 28, cy, s, -70, 16)
        draw_hand(draw, cx + 28, cy, s, -110, 16, mirror=True)
    elif w in ("go",):
        draw.polygon([(cx - 30, cy - 40), (cx + 50, cy), (cx - 30, cy + 40)], fill=OUTLINE)
    elif w in ("up",):
        draw.polygon([(cx, cy - 70), (cx - 25, cy - 30), (cx + 25, cy - 30)], fill=OUTLINE)
    elif w in ("down",):
        draw.polygon([(cx, cy + 70), (cx - 25, cy + 30), (cx + 25, cy + 30)], fill=OUTLINE)
    elif w in ("hug", "love", "hug_please"):
        draw_hand(draw, cx - 40, cy, s, -75, 14)
        draw_hand(draw, cx + 40, cy, s, -105, 14, mirror=True)
        draw.ellipse([cx - 18, cy - 55, cx + 18, cy - 19], fill="#ff8fab", outline=OUTLINE, width=3)

    pictogram(draw, word, SIZE // 2 + 40, SIZE // 2 - 60, band)


def render_family(word: str, band: str) -> Image.Image | None:
    specs = _family_mod.FAMILY_SPECS
    if word in specs:
        return _family_mod.render_family(word, band, specs[word])
    return None


def render_word(word: str, band: str, label: str) -> Image.Image:
    family = render_family(word, band)
    if family is not None:
        return family
    base = gradient(BAND_TINT[band])
    portrait = load_portrait(band)
    px = 16 + {"seed": 0, "sprout": 0, "bud": 2, "sprig": 4, "vine": 6, "bloom": 8, "canopy": 10}[band]
    py = SIZE - portrait.size[1] - 12
    base.paste(portrait, (px, py), portrait)
    draw = ImageDraw.Draw(base)
    draw_gesture(draw, word, band)
    # Word label chip for disambiguation
    try:
        font = ImageFont.truetype("arial.ttf", 22)
    except OSError:
        font = ImageFont.load_default()
    chip = (label or word)[:16]
    bbox = draw.textbbox((0, 0), chip, font=font)
    tw = bbox[2] - bbox[0]
    draw.rounded_rectangle([12, 12, 24 + tw, 44], radius=8, fill=(255, 255, 255, 230), outline=OUTLINE, width=2)
    draw.text((18, 16), chip, fill=OUTLINE, font=font)
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
                "style": "caly-universe-regenerated",
                "reviewedUtc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "source": "regenerate_band_word_symbols.py",
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def collect_words() -> tuple[dict[str, set[str]], dict[tuple[str, str], str]]:
    by_band: dict[str, set[str]] = {b: set() for b in BANDS}
    labels: dict[tuple[str, str], str] = {}
    for aud, band in AUDIENCE_BAND.items():
        path = VOCAB / f"{aud}-words.json"
        if not path.is_file():
            continue
        for sym in json.loads(path.read_text(encoding="utf-8")).get("symbols", []):
            wid = sym.get("id")
            if not wid:
                continue
            by_band[band].add(wid)
            labels[(band, wid)] = sym.get("label", wid)
    return by_band, labels


def main() -> int:
    force_all = "--all" in sys.argv
    force_generic = "--generic" in sys.argv or force_all
    family_only = "--family" in sys.argv

    by_band, labels = collect_words()
    made = skipped = 0

    # Always refresh canonical family symbols
    for word, spec in _family_mod.FAMILY_SPECS.items():
        for band in spec["bands"]:
            dest = SYMBOLS / band / f"{word}.png"
            dest.parent.mkdir(parents=True, exist_ok=True)
            _family_mod.render_family(word, band, spec).save(dest, "PNG")
            write_sidecar(word, band)
            made += 1

    for band in BANDS:
        ph = portrait_hash(band)
        words = sorted(by_band.get(band, set()))
        for word in words:
            if family_only and word not in FAMILY_WORDS and word not in ("friend", "mama", "dada"):
                continue
            if word in _family_mod.FAMILY_SPECS:
                continue
            dest = SYMBOLS / band / f"{word}.png"
            if dest.is_file() and not force_all:
                if force_generic and ph and file_hash(dest) == ph:
                    pass
                elif not force_generic:
                    skipped += 1
                    continue
            label = labels.get((band, word), word)
            img = render_word(word, band, label)
            dest.parent.mkdir(parents=True, exist_ok=True)
            img.save(dest, "PNG")
            write_sidecar(word, band)
            made += 1

    print(f"Regenerated {made} symbol(s), skipped {skipped}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
