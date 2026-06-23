# -*- coding: utf-8 -*-
"""Caly and Friends cartoon episodes - scene expansion + optional pilot render."""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "videos" / "caly_friends_catalog.json"
FRAMES = ROOT / "videos" / "frames"
FRIENDS_FRAMES = FRAMES / "caly-friends"
WEB_VIDEOS = ROOT.parent / "calyndra-app" / "videos"

_v4_path = ROOT / "scripts" / "generate_videos_v4_long.py"
_spec = importlib.util.spec_from_file_location("v4", _v4_path)
v4 = importlib.util.module_from_spec(_spec)
sys.modules["v4"] = v4
_spec.loader.exec_module(v4)

PALETTE = {
    "mint": "#b8f0d8",
    "skyBlue": "#7ec8ff",
    "cream": "#fff8e8",
    "outline": "#2d6a4f",
    "coral": "#ff6b6b",
}

STORY_BEATS: dict[str, list[tuple[str, str]]] = {
    "pip_gentle_hello_long": [
        ("Hello, little one. I'm Caly Seed.", "welcome"),
        ("And I'm Pip the bunny! Peek-a-boo!", "friend"),
        ("Elder Oak keeps our meadow safe and shady.", "mentor"),
        ("Your grown-up can play peek-a-boo with you.", "caregiver"),
        ("Where is Pip? There you are!", "play"),
        ("God made you special. Every giggle counts.", "lesson"),
        ("In and out. You are safe and loved.", "rest"),
        ("Bye-bye, friend. You are wonderfully made.", "farewell"),
    ],
    "fern_garden_share_long": [
        ("Welcome to Fern's garden! I'm Caly Sprout.", "welcome"),
        ("I'm Fern the fox. I grow flowers for friends.", "friend"),
        ("Sharing means both of us can smile.", "lesson"),
        ("Elder Oak says kind words are sunshine for the heart.", "mentor"),
        ("One for you, one for me. Thank you!", "share"),
        ("Tap SHARE when you want to give.", "interactive"),
        ("Every kind share is a win!", "celebrate"),
        ("See you in the garden soon!", "farewell"),
    ],
    "moss_kindness_trail_long": [
        ("This is the Kindness Trail! I'm Caly Bud.", "welcome"),
        ("I'm Moss the bear. Every kind choice glows.", "friend"),
        ("Use HELP when someone needs you.", "interactive"),
        ("Sharing is not losing. It multiplies joy.", "lesson"),
        ("Come play! There is room for you.", "include"),
        ("Elder Oak says kindness roots grow deep.", "mentor"),
        ("You lit the path today. Well done!", "celebrate"),
        ("Trail friends forever. See you soon!", "farewell"),
    ],
    "reed_wisdom_perch_long": [
        ("Before you speak, perch and listen. I'm Reed.", "friend"),
        ("I'm Caly Sprig. Words are tools we choose.", "welcome"),
        ("Not every story you hear is the whole truth.", "lesson"),
        ("Elder Oak says wisdom grows in quiet moments.", "mentor"),
        ("I'm sorry. I hear you. Let's try again.", "repair"),
        ("You listened well today.", "celebrate"),
    ],
    "sage_crossroads_long": [
        ("Every crossroads is a character choice.", "welcome"),
        ("I'm Sage. Integrity matches actions to values.", "friend"),
        ("You can say no without being cruel.", "lesson"),
        ("Elder Oak: the right path is not always easy.", "mentor"),
        ("Courage looks like inclusion.", "celebrate"),
    ],
    "laurel_morning_song_long": [
        ("Morning invites us to notice goodness.", "welcome"),
        ("I'm Laurel. I'm Caly Bloom. Grateful for today.", "friend"),
        ("Your voice, however you speak, matters.", "lesson"),
        ("Service turns gratitude into action.", "mentor"),
        ("Even hard days hold small mercies.", "mentor"),
        ("Thank you for this day. Rest well.", "farewell"),
    ],
}

MOTION_BY_TAG = {
    "welcome": "bounce",
    "friend": "bounce",
    "mentor": "pan",
    "caregiver": "zoom",
    "play": "celebrate",
    "lesson": "pulse",
    "rest": "pan",
    "share": "bounce",
    "interactive": "pulse",
    "include": "bounce",
    "repair": "zoom",
    "celebrate": "celebrate",
    "farewell": "bounce",
}


def _font(size: int):
    for name in ("arialbd.ttf", "Arial Bold.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def friend_frame_name(ep_id: str, tag: str) -> str:
    return f"friends_{ep_id}_{tag}.png"


def ensure_friend_frame(ep_id: str, tag: str, title: str, friend: str) -> str:
    FRIENDS_FRAMES.mkdir(parents=True, exist_ok=True)
    fname = friend_frame_name(ep_id, tag)
    path = FRIENDS_FRAMES / fname
    if path.exists():
        return fname
    w, h = 1280, 720
    img = Image.new("RGB", (w, h), PALETTE["cream"])
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((80, 60, w - 80, h - 140), radius=40, fill=PALETTE["mint"], outline=PALETTE["outline"], width=6)
    d.ellipse((w // 2 - 120, 120, w // 2 + 120, 360), fill=PALETTE["skyBlue"], outline=PALETTE["outline"], width=5)
    title_font = _font(44)
    sub_font = _font(28)
    d.text((w // 2 - d.textlength(title, font=title_font) / 2, 400), title, fill=PALETTE["outline"], font=title_font)
    sub = f"Caly and Friends - {friend}"
    d.text((w // 2 - d.textlength(sub, font=sub_font) / 2, 460), sub, fill=PALETTE["outline"], font=sub_font)
    tag_text = tag.replace("_", " ").title()
    d.text((w // 2 - d.textlength(tag_text, font=sub_font) / 2, 520), tag_text, fill=PALETTE["coral"], font=sub_font)
    img.save(path)
    return fname


def expand_scenes(ep_meta: dict, pilot: bool = False) -> list[tuple[str, str, str]]:
    beats = STORY_BEATS[ep_meta["id"]]
    target = 12 if pilot else ep_meta["targetSceneCount"]
    scenes: list[tuple[str, str, str]] = []
    beat_idx = 0
    for i in range(target):
        caption, tag = beats[beat_idx % len(beats)]
        if not pilot and len(beats) > 1 and i > 0 and i % max(len(beats), 1) == 0:
            beat_idx += 1
            caption, tag = beats[beat_idx % len(beats)]
        elif pilot:
            beat_idx = i % len(beats)
            caption, tag = beats[beat_idx]
        frame = ensure_friend_frame(ep_meta["id"], tag, ep_meta["title"], ep_meta["friend"])
        motion = MOTION_BY_TAG.get(tag, "bounce")
        if pilot and i % 3 == 2:
            motion = "celebrate"
        scenes.append((caption, f"caly-friends/{frame}", motion))
        if not pilot:
            beat_idx = (beat_idx + 1) % len(beats)
    return scenes


def load_frame_patched(name: str) -> Image.Image:
    for base in (FRAMES, FRIENDS_FRAMES):
        p = base / name.replace("caly-friends/", "")
        if p.exists():
            return Image.open(p).convert("RGB").resize((1280, 720), Image.Resampling.LANCZOS)
    raise FileNotFoundError(name)


def write_placeholder_webm(dest: Path, title: str, seconds: float = 3.0) -> bool:
    try:
        ffmpeg = v4.FFMPEG
    except Exception:
        return False
    work = dest.parent
    png = work / f"_placeholder_{dest.stem}.png"
    w, h = 1280, 720
    img = Image.new("RGB", (w, h), PALETTE["cream"])
    d = ImageDraw.Draw(img)
    font = _font(36)
    msg = f"{title}\n(render pending)"
    lines = msg.split("\n")
    y = h // 2 - 40
    for line in lines:
        d.text((w // 2 - d.textlength(line, font=font) / 2, y), line, fill=PALETTE["outline"], font=font)
        y += 44
    img.save(png)
    try:
        subprocess.run(
            [
                ffmpeg, "-y", "-loop", "1", "-i", str(png),
                "-c:v", "libvpx-vp9", "-t", str(seconds), "-pix_fmt", "yuv420p",
                str(dest),
            ],
            check=True,
            capture_output=True,
        )
        png.unlink(missing_ok=True)
        return dest.exists()
    except Exception:
        return False


def build_episode_local(ep_meta: dict, scenes: list[tuple[str, str, str]], work: Path) -> Path | None:
    v4.load_frame = load_frame_patched
    ep = {
        "id": ep_meta["id"],
        "audience": ep_meta["band"],
        "title": ep_meta["title"],
        "scenes": scenes,
    }
    return v4.build_episode(ep, work)


def load_catalog() -> dict:
    return json.loads(CATALOG.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Caly and Friends cartoon episodes")
    parser.add_argument("--pilot", action="store_true", help="Render 12-scene pilots for baby/toddler/child")
    parser.add_argument("--all", action="store_true", help="Render all episodes (long-running)")
    parser.add_argument("--placeholder", action="store_true", help="Write stub webm for script-only episodes")
    parser.add_argument("--id", help="Render a single episode id")
    args = parser.parse_args()

    catalog = load_catalog()
    WEB_VIDEOS.mkdir(parents=True, exist_ok=True)
    FRAMES.mkdir(parents=True, exist_ok=True)

    def write_script_placeholders() -> None:
        for ep_meta in catalog["episodes"]:
            if ep_meta.get("status") != "script-only":
                continue
            dest = WEB_VIDEOS / ep_meta["webm"]
            if dest.exists():
                continue
            ok = write_placeholder_webm(dest, ep_meta["title"], seconds=5.0)
            print(f"Placeholder {'OK' if ok else 'FAIL'} {dest.name}")

    if args.placeholder and not args.pilot and not args.all and not args.id:
        write_script_placeholders()
        return

    if not args.pilot and not args.all and not args.id:
        parser.print_help()
        return

    for ep_meta in catalog["episodes"]:
        ep_id = ep_meta["id"]
        if args.id and ep_id != args.id:
            continue
        if args.pilot and not ep_meta.get("pilot"):
            continue
        if args.all and ep_meta.get("status") == "script-only" and not args.id:
            dest = WEB_VIDEOS / ep_meta["webm"]
            if not dest.exists():
                write_placeholder_webm(dest, ep_meta["title"], seconds=5.0)
                print(f"Placeholder {dest.name}")
            continue

        pilot = bool(args.pilot and ep_meta.get("pilot"))
        scenes = expand_scenes(ep_meta, pilot=pilot)
        print(f"Building {ep_id} ({len(scenes)} scenes, pilot={pilot})...")
        with tempfile.TemporaryDirectory() as td:
            result = build_episode_local(ep_meta, scenes, Path(td))
            dest = WEB_VIDEOS / ep_meta["webm"]
            if result and result.exists():
                shutil.copy(result, dest)
                print(f"  OK {dest.name}")
            else:
                print(f"  TTS/render failed - writing placeholder for {ep_id}")
                write_placeholder_webm(dest, ep_meta["title"], seconds=8.0 if pilot else 5.0)

    if args.pilot and args.placeholder:
        write_script_placeholders()


if __name__ == "__main__":
    main()
