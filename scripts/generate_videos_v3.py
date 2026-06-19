# -*- coding: utf-8 -*-
"""Educational cartoon WebM v3 - illustrated scene frames + caption bar."""
from __future__ import annotations

import math
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = Path.home() / ".cursor" / "projects" / "c-Users-Auricrux-OneDrive-Future-Contractors-of-America-LLC" / "assets"
FRAMES = ROOT / "videos" / "frames"
FLUTTER = ROOT.parent / "calyndra-mobile-flutter"
WEB = ROOT.parent / "calyndra-app"
OUT = ROOT / "videos"

CLIPS = [
    {
        "id": "meet_caly_sprout",
        "scenes": [
            ("Hi! I'm Caly Sprout!", "video_meet_sprout_wave.png"),
            ("Pictures help you ask for things.", "video_meet_symbols_float.png"),
            ("Tap a word. A grown-up helps.", "video_meet_tap_word.png"),
            ("Every try is a win!", "video_meet_celebrate.png"),
        ],
    },
    {
        "id": "first_word_help",
        "scenes": [
            ("Sometimes we need help.", "video_help_need.png"),
            ("This picture means HELP.", "video_help_symbol.png"),
            ("Tap or point to ask.", "video_help_tap.png"),
            ("Grown-ups listen!", "video_help_listen.png"),
            ("You did it!", "video_help_celebrate.png"),
        ],
    },
    {
        "id": "caly_quest_adventure",
        "scenes": [
            ("Welcome to Caly Quest!", "video_quest_title.png"),
            ("Pick words for your adventure.", "video_quest_grid.png"),
            ("Your words. Your choices.", "video_quest_choice.png"),
            ("No is always okay.", "video_quest_no.png"),
            ("Ready for your next word?", "video_quest_celebrate.png"),
        ],
    },
]


def _font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for name in ("arialbd.ttf", "Arial Bold.ttf", "arial.ttf", "segoeuib.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def load_frame(name: str) -> Image.Image:
    for base in (FRAMES, ASSETS):
        path = base / name
        if path.exists():
            img = Image.open(path).convert("RGB")
            return img.resize((1280, 720), Image.Resampling.LANCZOS)
    raise FileNotFoundError(name)


def compose_scene(img: Image.Image, caption: str, t: float) -> Image.Image:
    """Ken Burns zoom + rounded caption bar."""
    w, h = 1280, 720
    zoom = 1.0 + 0.04 * math.sin(t * math.pi)
    zw, zh = int(w * zoom), int(h * zoom)
    scaled = img.resize((zw, zh), Image.Resampling.LANCZOS)
    x0 = (zw - w) // 2
    y0 = (zh - h) // 2
    canvas = scaled.crop((x0, y0, x0 + w, y0 + h))

    d = ImageDraw.Draw(canvas)
    bar_h = 88
    d.rounded_rectangle((40, h - bar_h - 24, w - 40, h - 24), radius=22, fill=(255, 255, 255))
    d.rounded_rectangle((40, h - bar_h - 24, w - 40, h - 24), radius=22, outline=(255, 200, 100), width=4)
    font = _font(36)
    tw = d.textlength(caption, font=font)
    d.text(((w - tw) / 2, h - bar_h - 6), caption, fill=(45, 55, 65), font=font)
    return canvas


def build_frames(clip: dict, fps: int = 10, sec_per_scene: float = 4.5) -> list[Image.Image]:
    frames: list[Image.Image] = []
    per_scene = int(fps * sec_per_scene)
    for caption, frame_file in clip["scenes"]:
        base = load_frame(frame_file)
        for i in range(per_scene):
            t = i / max(per_scene - 1, 1)
            frames.append(compose_scene(base, caption, t))
    return frames


def write_webm(frames: list[Image.Image], path: Path, fps: int = 10) -> bool:
    try:
        import imageio.v3 as iio
        import numpy as np

        arr = [np.array(f) for f in frames]
        iio.imwrite(path, arr, fps=fps, codec="libvpx-vp9", quality=8)
        return True
    except Exception as exc:
        print(f"  encode failed: {exc}")
        return False


def main() -> None:
    FRAMES.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    flutter_v = FLUTTER / "assets" / "videos"
    web_v = WEB / "videos"
    flutter_v.mkdir(parents=True, exist_ok=True)
    web_v.mkdir(parents=True, exist_ok=True)

    for clip in CLIPS:
        for _, frame_file in clip["scenes"]:
            src = ASSETS / frame_file
            if src.exists():
                shutil.copy(src, FRAMES / frame_file)

    made = 0
    for clip in CLIPS:
        try:
            frames = build_frames(clip)
        except FileNotFoundError as e:
            print(f"Skip {clip['id']}: missing {e}")
            continue
        webm = OUT / f"{clip['id']}.webm"
        print(f"Encoding {webm.name} ({len(frames)} frames)...")
        if write_webm(frames, webm):
            shutil.copy(webm, flutter_v / webm.name)
            shutil.copy(webm, web_v / webm.name)
            made += 1
            print(f"  OK {webm}")
    print(f"Done: {made} v3 illustrated clips")


if __name__ == "__main__":
    main()
