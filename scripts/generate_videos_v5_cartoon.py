# -*- coding: utf-8 -*-
"""Calyndra cartoon episodes v5 - feelings story + v4 episodes."""
from __future__ import annotations

import importlib.util
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = Path.home() / ".cursor" / "projects" / "c-Users-Auricrux-OneDrive-Future-Contractors-of-America-LLC" / "assets"
FRAMES = ROOT / "videos" / "frames"

_v4_path = ROOT / "scripts" / "generate_videos_v4_long.py"
_spec = importlib.util.spec_from_file_location("v4", _v4_path)
v4 = importlib.util.module_from_spec(_spec)
sys.modules["v4"] = v4
_spec.loader.exec_module(v4)

SPROUT_FEELINGS_STORY = {
    "id": "sprout_feelings_story_long",
    "audience": "toddler",
    "title": "Feelings with Caly Sprout",
    "scenes": [
        ("Hi friend! Let's talk about feelings.", "cartoon_feelings_happy.png", "bounce"),
        ("Feelings live inside all of us.", "cartoon_feelings_happy.png", "zoom"),
        ("HAPPY looks like a big smile and warm sunshine.", "cartoon_feelings_happy.png", "celebrate"),
        ("You can tap the HAPPY picture when you feel happy.", "cartoon_feelings_happy.png", "pulse"),
        ("SAD can happen when something feels hard.", "cartoon_feelings_sad.png", "pan"),
        ("SAD is okay. Grown-ups can sit with you.", "cartoon_feelings_sad.png", "zoom"),
        ("You can tap SAD. A hug might help if you want one.", "cartoon_feelings_sad.png", "bounce"),
        ("MAD can feel hot, like steam.", "cartoon_feelings_mad.png", "pan"),
        ("Take a breath. In... and out.", "cartoon_feelings_mad.png", "pulse"),
        ("You can tap MAD or ask for a BREAK.", "cartoon_feelings_mad.png", "zoom"),
        ("All feelings are real. All feelings are okay.", "cartoon_feelings_happy.png", "celebrate"),
        ("Your grown-up loves you in every feeling.", "cartoon_feelings_sad.png", "pan"),
        ("Picture words help you share feelings.", "cartoon_word_parade.png", "parade"),
        ("Let's parade our words: happy, sad, help, more!", "cartoon_word_parade.png", "celebrate"),
        ("You did wonderful listening. Bye bye, friend!", "cartoon_feelings_happy.png", "bounce"),
    ],
}

_orig_animate = v4.animate_frame


def animate_frame(base, caption, t, motion):
    if motion == "parade":
        return _orig_animate(base, caption, t, "pan")
    return _orig_animate(base, caption, t, motion)


v4.animate_frame = animate_frame

EPISODES = [
    SPROUT_FEELINGS_STORY,
]


def main() -> None:
    FRAMES.mkdir(parents=True, exist_ok=True)
    for name in (
        "cartoon_word_parade.png",
        "cartoon_feelings_happy.png",
        "cartoon_feelings_sad.png",
        "cartoon_feelings_mad.png",
    ):
        src = ASSETS / name
        if src.exists():
            shutil.copy(src, FRAMES / name)

    v4.OUT.mkdir(parents=True, exist_ok=True)
    web_v = v4.WEB / "videos"
    flutter_v = v4.FLUTTER / "assets" / "videos"
    web_v.mkdir(parents=True, exist_ok=True)
    flutter_v.mkdir(parents=True, exist_ok=True)

    for ep in EPISODES:
        print(f"Building cartoon {ep['id']}...")
        with tempfile.TemporaryDirectory() as td:
            result = v4.build_episode(ep, Path(td))
            if result and result.exists():
                shutil.copy(result, web_v / result.name)
                shutil.copy(result, flutter_v / result.name)
                print(f"  OK {result.name}")
            else:
                print(f"  FAILED {ep['id']}")


if __name__ == "__main__":
    main()
