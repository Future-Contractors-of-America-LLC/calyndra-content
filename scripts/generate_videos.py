"""Generate short AAC intro videos (WebM) from frame sequences. Run: python scripts/generate_videos.py"""
from __future__ import annotations

import math
import shutil
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
FLUTTER = ROOT.parent / "calyndra-mobile-flutter"
WEB = ROOT.parent / "calyndra-app"
OUT = ROOT / "videos"
FLUTTER_V = FLUTTER / "assets" / "videos"
WEB_V = WEB / "videos"

CLIPS = [
    ("welcome_aac", "Welcome to Caly", "sprout", 90),
    ("toddler_wave", "Caly Sprout waves hello", "sprout", 60),
    ("child_quest", "Quest adventure intro", "quest", 75),
    ("caregiver_assent", "Honor assent always", "core", 80),
    ("teen_spark", "Your words, your pace", "spark", 70),
]


def frame_welcome(i: int, total: int, style: dict, title: str) -> Image.Image:
    w, h = 640, 360
    img = Image.new("RGB", (w, h), style["bg"][:3])
    d = ImageDraw.Draw(img)
    t = i / max(total - 1, 1)
    bounce = int(math.sin(t * math.pi * 4) * 8)
    cx, cy = w // 2, h // 2 - 20 + bounce
    s = 70
    d.ellipse((cx - s, cy - s, cx + s, cy + s), fill=style["primary"])
    d.arc((cx - 40, cy - 20, cx + 40, cy + 30), 10, 170, fill=(255, 255, 255), width=4)
    d.text((w // 2 - len(title) * 5, h - 60), title, fill=(255, 255, 255))
    return img


def frame_wave(i: int, total: int, style: dict, title: str) -> Image.Image:
    w, h = 640, 360
    img = Image.new("RGB", (w, h), style["bg"][:3])
    d = ImageDraw.Draw(img)
    cx, cy = w // 2, h // 2
    s = 80
    d.ellipse((cx - s, cy - s, cx + s, cy + s), fill=style["primary"])
    angle = (i / total) * math.pi * 2
    hx = cx + s + 20
    hy = cy - 30 + int(math.sin(angle) * 25)
    d.line((hx, hy, hx + 40, hy - 50), fill=style["accent"], width=8)
    d.text((w // 2 - 80, h - 50), title, fill=(255, 255, 255))
    return img


def frame_quest(i: int, total: int, style: dict, title: str) -> Image.Image:
    w, h = 640, 360
    img = Image.new("RGB", (w, h), style["bg"][:3])
    d = ImageDraw.Draw(img)
    cx = int(w * 0.2 + (i / total) * w * 0.6)
    cy = h // 2
    d.polygon([(cx, cy - 40), (cx - 50, cy + 30), (cx + 50, cy + 30)], fill=style["accent"])
    for sx in range(0, w, 80):
        d.polygon([(sx, 20), (sx + 8, 40), (sx + 16, 20)], fill=(255, 255, 200))
    d.text((w // 2 - 90, h - 50), title, fill=(40, 60, 40))
    return img


def frame_assent(i: int, total: int, style: dict, title: str) -> Image.Image:
    w, h = 640, 360
    img = Image.new("RGB", (w, h), style["bg"][:3])
    d = ImageDraw.Draw(img)
    alpha = min(1.0, i / (total * 0.4))
    cx, cy = w // 2, h // 2
    r = int(60 + alpha * 20)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=style["primary"], width=5)
    d.line((cx - 30, cy, cx - 5, cy + 25), fill=style["accent"], width=6)
    d.line((cx - 5, cy + 25, cx + 35, cy - 25), fill=style["accent"], width=6)
    d.text((w // 2 - 110, h - 50), title, fill=style["primary"])
    return img


def frame_spark(i: int, total: int, style: dict, title: str) -> Image.Image:
    w, h = 640, 360
    img = Image.new("RGB", (w, h), style["bg"][:3])
    d = ImageDraw.Draw(img)
    pulse = 0.5 + 0.5 * math.sin(i / 8)
    cx, cy = w // 2, h // 2
    r = int(50 + pulse * 20)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=style["primary"], width=4)
    d.line((40, cy, w - 40, cy), fill=style["accent"], width=2)
    d.text((w // 2 - 100, h - 50), title, fill=style["primary"])
    return img


RENDERERS = {
    "welcome_aac": frame_welcome,
    "toddler_wave": frame_wave,
    "child_quest": frame_quest,
    "caregiver_assent": frame_assent,
    "teen_spark": frame_spark,
}

STYLES = {
    "sprout": {"bg": (60, 140, 110, 255), "primary": (120, 210, 170), "accent": (255, 220, 130)},
    "quest": {"bg": (80, 120, 70, 255), "primary": (180, 140, 60), "accent": (255, 200, 80)},
    "spark": {"bg": (22, 28, 48, 255), "primary": (0, 255, 200), "accent": (255, 60, 160)},
    "core": {"bg": (240, 244, 248, 255), "primary": (60, 80, 110), "accent": (90, 140, 200)},
}


def write_webm(frames: list[Image.Image], path: Path, fps: int = 12) -> bool:
    try:
        import imageio.v3 as iio
        import numpy as np

        arr = [np.array(f) for f in frames]
        iio.imwrite(path, arr, fps=fps, codec="libvpx-vp9", quality=8)
        return True
    except Exception as exc:
        print(f"  WebM encode failed ({exc}); saving frame sequence fallback")
        seq = path.with_suffix("")
        seq.mkdir(parents=True, exist_ok=True)
        for i, fr in enumerate(frames):
            fr.save(seq / f"frame_{i:03d}.png")
        (seq / "README.txt").write_text(
            f"Frame sequence fallback for {path.name}. Use video_player with Image sequence or install imageio-ffmpeg.",
            encoding="utf-8",
        )
        return False


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    FLUTTER_V.mkdir(parents=True, exist_ok=True)
    WEB_V.mkdir(parents=True, exist_ok=True)
    made = 0
    for clip_id, title, style_name, frames_n in CLIPS:
        style = STYLES[style_name]
        renderer = RENDERERS[clip_id]
        frames = [renderer(i, frames_n, style, title) for i in range(frames_n)]
        webm = OUT / f"{clip_id}.webm"
        ok = write_webm(frames, webm)
        if ok:
            shutil.copy(webm, FLUTTER_V / webm.name)
            shutil.copy(webm, WEB_V / webm.name)
            made += 1
            print(f"  {webm}")
        else:
            seq_flutter = FLUTTER_V / clip_id
            seq_web = WEB_V / clip_id
            if (OUT / f"{clip_id}").exists():
                shutil.copytree(OUT / clip_id, seq_flutter, dirs_exist_ok=True)
                shutil.copytree(OUT / clip_id, seq_web, dirs_exist_ok=True)
    print(f"Done: {made} WebM clips (+ frame fallbacks if encode unavailable)")


if __name__ == "__main__":
    main()
