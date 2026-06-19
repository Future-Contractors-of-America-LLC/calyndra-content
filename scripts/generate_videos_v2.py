# -*- coding: utf-8 -*-
"""Educational cartoon WebM clips v2 - narrative scenes with text panels."""
from __future__ import annotations

import math
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FLUTTER = ROOT.parent / "calyndra-mobile-flutter"
WEB = ROOT.parent / "calyndra-app"
OUT = ROOT / "videos"

CLIPS = [
    {
        "id": "meet_caly_sprout",
        "style": "sprout",
        "scenes": [
            ("Hi! I'm Caly Sprout!", "sprout"),
            ("Pictures help you ask for things.", "symbols"),
            ("Tap a word. A grown-up helps.", "tap"),
            ("Every try is a win!", "celebrate"),
        ],
    },
    {
        "id": "first_word_help",
        "style": "sprout",
        "scenes": [
            ("Sometimes we need help.", "need"),
            ("This picture means HELP.", "help"),
            ("Tap or point to ask.", "tap"),
            ("Grown-ups listen!", "listen"),
            ("You did it!", "celebrate"),
        ],
    },
    {
        "id": "caly_quest_adventure",
        "style": "quest",
        "scenes": [
            ("Welcome to Caly Quest!", "title"),
            ("Pick words for your adventure.", "grid"),
            ("Your words. Your choices.", "choice"),
            ("No is always okay.", "no"),
            ("Ready for your next word?", "celebrate"),
        ],
    },
    {
        "id": "respect_my_no",
        "style": "spark",
        "scenes": [
            ("Your voice matters.", "title"),
            ("No means no.", "no"),
            ("Good friends respect you.", "friends"),
            ("You decide when to use AAC.", "choice"),
        ],
    },
    {
        "id": "caregiver_quick_start",
        "style": "core",
        "scenes": [
            ("Welcome to Calyndra!", "title"),
            ("1. Choose an age band.", "step1"),
            ("2. Model one symbol.", "step2"),
            ("3. Play a quick game.", "step3"),
            ("4. Ask Caly anytime.", "step4"),
            ("Not medical advice.", "disclaimer"),
        ],
    },
]

STYLES = {
    "sprout": {"bg": (180, 230, 210), "primary": (80, 160, 130), "accent": (255, 210, 120), "text": (40, 70, 60)},
    "quest": {"bg": (120, 160, 100), "primary": (200, 160, 60), "accent": (255, 240, 180), "text": (50, 40, 20)},
    "spark": {"bg": (30, 35, 50), "primary": (124, 252, 0), "accent": (255, 80, 160), "text": (230, 230, 240)},
    "core": {"bg": (240, 244, 248), "primary": (60, 90, 130), "accent": (90, 150, 210), "text": (30, 40, 55)},
}


def _font(size: int):
    for name in ("arial.ttf", "Arial.ttf", "segoeui.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def draw_mascot(d: ImageDraw.ImageDraw, cx: int, cy: int, style: dict, mood: str) -> None:
    r = 55
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=style["primary"], outline=style["accent"], width=4)
    eye_y = cy - 12
    d.ellipse((cx - 22, eye_y - 10, cx - 8, eye_y + 6), fill=(255, 255, 255))
    d.ellipse((cx + 8, eye_y - 10, cx + 22, eye_y + 6), fill=(255, 255, 255))
    d.ellipse((cx - 18, eye_y - 4, cx - 12, eye_y + 2), fill=(40, 40, 40))
    d.ellipse((cx + 12, eye_y - 4, cx + 18, eye_y + 2), fill=(40, 40, 40))
    if mood == "celebrate":
        d.arc((cx - 30, cy + 5, cx + 30, cy + 35), 10, 170, fill=style["accent"], width=4)
    elif mood == "help":
        d.rectangle((cx + 40, cy - 30, cx + 90, cy + 40), fill=style["accent"], outline=(255, 255, 255), width=3)
        d.text((cx + 52, cy - 18), "HELP", fill=style["text"], font=_font(16))
    else:
        d.arc((cx - 25, cy + 8, cx + 25, cy + 28), 0, 180, fill=style["accent"], width=3)


def draw_scene(style_name: str, scene_key: str, caption: str, t: float) -> Image.Image:
    style = STYLES[style_name]
    w, h = 640, 360
    img = Image.new("RGB", (w, h), style["bg"])
    d = ImageDraw.Draw(img)
    bounce = int(math.sin(t * math.pi * 2) * 6)
    cx, cy = w // 2, 140 + bounce
    draw_mascot(d, cx, cy, style, scene_key if scene_key in ("help", "celebrate") else "normal")

    if scene_key == "symbols":
        for i, lbl in enumerate(("help", "more", "eat")):
            x = 120 + i * 160
            d.rounded_rectangle((x, 200, x + 100, 280), radius=12, fill=(255, 255, 255), outline=style["primary"], width=3)
            d.text((x + 18, 230), lbl, fill=style["text"], font=_font(18))
    elif scene_key == "grid":
        for row in range(2):
            for col in range(3):
                x, y = 100 + col * 150, 200 + row * 50
                d.rounded_rectangle((x, y, x + 120, y + 40), radius=8, fill=style["accent"])
    elif scene_key == "no":
        d.rounded_rectangle((w // 2 - 80, 200, w // 2 + 80, 280), radius=16, fill=(220, 80, 80))
        d.text((w // 2 - 28, 235), "NO", fill=(255, 255, 255), font=_font(28))
    elif scene_key.startswith("step"):
        step = scene_key[-1]
        d.ellipse((w // 2 - 30, 200, w // 2 + 30, 260), fill=style["accent"])
        d.text((w // 2 - 8, 218), step, fill=style["text"], font=_font(24))

    # Caption bar
    d.rounded_rectangle((20, h - 70, w - 20, h - 20), radius=14, fill=(255, 255, 255, 200))
    d.rectangle((20, h - 70, w - 20, h - 20), fill=(255, 255, 255))
    d.text((40, h - 58), caption, fill=style["text"], font=_font(22))
    return img


def build_frames(clip: dict, fps: int = 8, sec_per_scene: float = 4.0) -> list[Image.Image]:
    frames: list[Image.Image] = []
    per_scene = int(fps * sec_per_scene)
    for caption, key in clip["scenes"]:
        for i in range(per_scene):
            t = i / max(per_scene - 1, 1)
            frames.append(draw_scene(clip["style"], key, caption, t))
    return frames


def write_webm(frames: list[Image.Image], path: Path, fps: int = 8) -> bool:
    try:
        import imageio.v3 as iio
        import numpy as np

        arr = [np.array(f) for f in frames]
        iio.imwrite(path, arr, fps=fps, codec="libvpx-vp9", quality=7)
        return True
    except Exception as exc:
        print(f"  encode failed: {exc}")
        return False


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    FLUTTER_V = FLUTTER / "assets" / "videos"
    WEB_V = WEB / "videos"
    FLUTTER_V.mkdir(parents=True, exist_ok=True)
    WEB_V.mkdir(parents=True, exist_ok=True)
    made = 0
    for clip in CLIPS:
        frames = build_frames(clip)
        webm = OUT / f"{clip['id']}.webm"
        print(f"Encoding {webm.name} ({len(frames)} frames)...")
        if write_webm(frames, webm):
            shutil.copy(webm, FLUTTER_V / webm.name)
            shutil.copy(webm, WEB_V / webm.name)
            made += 1
            print(f"  OK {webm}")
    print(f"Done: {made} v2 clips")


if __name__ == "__main__":
    main()
