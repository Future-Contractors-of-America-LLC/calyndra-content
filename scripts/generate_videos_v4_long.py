# -*- coding: utf-8 -*-
"""
Long-form original Calyndra cartoon episodes (2-5 min).
Illustrated frames + programmatic animation + Caly Neural TTS narration.
All content is original IP - see CONTENT_ORIGIN.md.
"""
from __future__ import annotations

import json
import math
import shutil
import subprocess
import tempfile
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = Path.home() / ".cursor" / "projects" / "c-Users-Auricrux-OneDrive-Future-Contractors-of-America-LLC" / "assets"
FRAMES = ROOT / "videos" / "frames"
OUT = ROOT / "videos"
WEB = ROOT.parent / "calyndra-app"
FLUTTER = ROOT.parent / "calyndra-mobile-flutter"
SPEAK_API = "https://calyndra-central.azurewebsites.net/api/caly/speak"

from caly_video_quality import (
    AUDIO_BITRATE,
    FFMPEG,
    PROFILE_NAME,
    VIDEO_FPS,
    VIDEO_HEIGHT,
    VIDEO_WIDTH,
    fit_frame,
    mux_av as _mux_av,
    scale,
    write_segment,
)
from caly_animation import draw_caption_bar, draw_celebration_particles, motion_params

FPS = VIDEO_FPS

# Toddler episode ~2.5 min when narrated slowly
MEET_CALY_SPROUT_LONG = {
    "id": "meet_caly_sprout_long",
    "audience": "toddler",
    "title": "Meet Caly Sprout (full episode)",
    "scenes": [
        ("Hi! I'm Caly Sprout! Welcome to Calyndra!", "video_meet_sprout_wave.png", "bounce"),
        ("I am your friendly helper for picture words.", "video_meet_sprout_wave.png", "zoom"),
        ("Picture words help you tell grown-ups what you want.", "video_meet_symbols_float.png", "pan"),
        ("Like help, more, eat, and play!", "video_meet_symbols_float.png", "bounce"),
        ("See the HELP picture? It means I need help.", "video_help_symbol.png", "zoom"),
        ("You can tap a picture on the screen.", "video_meet_tap_word.png", "pan"),
        ("Or point to it. Or look at it. All of those count!", "video_meet_tap_word.png", "bounce"),
        ("A grown-up who loves you will listen.", "video_help_listen.png", "zoom"),
        ("You never have to use words with your mouth.", "video_help_listen.png", "pan"),
        ("Pictures are a real way to talk!", "video_meet_symbols_float.png", "bounce"),
        ("Let's try together. Can you find HELP?", "video_help_symbol.png", "pulse"),
        ("Tap the screen when you see it!", "video_help_tap.png", "bounce"),
        ("Wonderful! Every try is a win!", "video_meet_celebrate.png", "celebrate"),
        ("You can say no anytime. No is always okay.", "video_quest_no.png", "pan"),
        ("MORE means I want another one. Let's find MORE!", "video_meet_symbols_float.png", "pulse"),
        ("EAT means I am hungry. Yum yum!", "video_meet_symbols_float.png", "bounce"),
        ("PLAY means let's have fun together!", "video_meet_tap_word.png", "celebrate"),
        ("Let's sing: Hello, hello, Caly Sprout! We use our words and shout them out!", "video_meet_celebrate.png", "celebrate"),
        ("Help and more and play and eat. Every word is oh-so sweet!", "video_meet_celebrate.png", "bounce"),
        ("Can you tap HELP one more time? Great trying!", "video_help_tap.png", "pulse"),
        ("Can you tap MORE? Wonderful!", "video_meet_symbols_float.png", "bounce"),
        ("Your grown-up is so proud when you use picture words.", "video_help_listen.png", "zoom"),
        ("Remember: every try is a win, even a small try.", "video_meet_celebrate.png", "pan"),
        ("I am so happy you are here. Let's play and learn!", "video_meet_celebrate.png", "celebrate"),
        ("See you next time, friend. Bye bye from Caly Sprout!", "video_meet_sprout_wave.png", "bounce"),
    ],
}

FIRST_WORD_HELP_LONG = {
    "id": "first_word_help_long",
    "audience": "toddler",
    "title": "Your First Word: Help (full episode)",
    "scenes": [
        ("Sometimes things are hard to reach.", "video_help_need.png", "pan"),
        ("Or too heavy. Or confusing. That is okay!", "video_help_need.png", "zoom"),
        ("When you need help, use the HELP picture.", "video_help_symbol.png", "pulse"),
        ("HELP means: please help me.", "video_help_symbol.png", "zoom"),
        ("Look at the open hand reaching up.", "video_help_symbol.png", "bounce"),
        ("Your grown-up can show you HELP on a board.", "video_meet_tap_word.png", "pan"),
        ("You tap HELP. They come help you.", "video_help_tap.png", "bounce"),
        ("You can also point. Or bring the picture to them.", "video_help_tap.png", "pan"),
        ("Grown-ups want to help you.", "video_help_listen.png", "zoom"),
        ("They might not know until you show the picture.", "video_help_listen.png", "pan"),
        ("That is why HELP is such a powerful word!", "video_help_symbol.png", "pulse"),
        ("Let's practice. Imagine a toy on a shelf.", "video_help_need.png", "pan"),
        ("Tap HELP in your mind. Now tap it on the screen!", "video_help_tap.png", "bounce"),
        ("Yes! You asked for help!", "video_help_celebrate.png", "celebrate"),
        ("Let's practice HELP again. HELP, HELP, HELP!", "video_help_symbol.png", "pulse"),
        ("Show HELP when your shoe is tricky to put on.", "video_help_need.png", "pan"),
        ("Show HELP when you cannot open a snack.", "video_help_need.png", "zoom"),
        ("Show HELP when you feel stuck. That is smart!", "video_help_symbol.png", "bounce"),
        ("Your grown-up will come. They want to help you.", "video_help_listen.png", "zoom"),
        ("One more time! Find HELP and tap!", "video_help_tap.png", "pulse"),
        ("I am proud of you. You did it!", "video_help_celebrate.png", "celebrate"),
        ("HELP is your super word. Use it anytime.", "video_help_symbol.png", "zoom"),
        ("Bye bye! You are a HELP superstar!", "video_help_celebrate.png", "celebrate"),
    ],
}

CALY_QUEST_LONG = {
    "id": "caly_quest_adventure_long",
    "audience": "child",
    "title": "Caly Quest Adventure (full episode)",
    "scenes": [
        ("Welcome, explorer! I am Caly Quest!", "video_quest_title.png", "bounce"),
        ("Every adventure needs the right words.", "video_quest_title.png", "zoom"),
        ("Pick a word tile to start your quest.", "video_quest_grid.png", "pan"),
        ("Each picture is a tool for your journey.", "video_quest_grid.png", "bounce"),
        ("You choose which word to use.", "video_quest_choice.png", "zoom"),
        ("Your words. Your choices. Your adventure.", "video_quest_choice.png", "pan"),
        ("Friends on a quest respect each other.", "video_quest_choice.png", "bounce"),
        ("Sometimes you say yes. Sometimes you say no.", "video_quest_no.png", "pulse"),
        ("No is always okay. Good friends listen.", "video_quest_no.png", "zoom"),
        ("You can take a break when you need one.", "video_quest_no.png", "pan"),
        ("School, home, play - words go everywhere.", "video_quest_grid.png", "pan"),
        ("At school you might use HELP or BATHROOM.", "video_quest_grid.png", "bounce"),
        ("With friends you might use SHARE or MY TURN.", "video_quest_choice.png", "pan"),
        ("If something feels too loud, use QUIET or BREAK.", "video_quest_no.png", "zoom"),
        ("Practice picking a word. Which one fits your quest today?", "video_quest_grid.png", "pulse"),
        ("Tap a word in the app and ask Caly about it!", "video_quest_choice.png", "bounce"),
        ("Every word you learn is a new power.", "video_quest_title.png", "zoom"),
        ("Quest with me, we will find the way. New words to learn every day!", "video_quest_celebrate.png", "celebrate"),
        ("Ask Caly when you want to learn a new word.", "video_quest_celebrate.png", "bounce"),
        ("Ready for your next word? Let's go!", "video_quest_celebrate.png", "celebrate"),
        ("Great questing today, explorer. See you soon!", "video_quest_title.png", "bounce"),
    ],
}

EPISODES = [MEET_CALY_SPROUT_LONG, FIRST_WORD_HELP_LONG, CALY_QUEST_LONG]


def _font(size: int):
    for name in ("arialbd.ttf", "Arial Bold.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def load_frame(name: str) -> Image.Image:
    for base in (FRAMES, ASSETS):
        p = base / name
        if p.exists():
            return fit_frame(Image.open(p).convert("RGB"))
    raise FileNotFoundError(name)


def animate_frame(base: Image.Image, caption: str, t: float, motion: str) -> Image.Image:
    w, h = VIDEO_WIDTH, VIDEO_HEIGHT
    zoom, dy, et = motion_params(motion, t, scale)

    zw, zh = int(w * zoom), int(h * zoom)
    scaled = base.resize((zw, zh), Image.Resampling.LANCZOS)
    x0 = (zw - w) // 2
    y0 = max(0, min((zh - h) // 2 + dy, zh - h))
    canvas = scaled.crop((x0, y0, x0 + w, y0 + h))

    if motion == "celebrate":
        d = ImageDraw.Draw(canvas)
        draw_celebration_particles(d, w, h, et, scale)

    draw_caption_bar(canvas, caption, t=et, scale_fn=scale, font_loader=_font)
    return canvas


def fetch_tts(text: str, audience: str, dest: Path, retries: int = 4) -> bool:
    body = json.dumps({"text": text, "audience": audience}).encode("utf-8")
    for attempt in range(retries):
        req = urllib.request.Request(
            SPEAK_API,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                dest.write_bytes(resp.read())
            if dest.stat().st_size > 1000:
                return True
        except Exception as exc:
            wait = min(2 ** attempt, 16)
            print(f"    TTS fail (attempt {attempt + 1}/{retries}): {exc}")
            if attempt + 1 < retries:
                import time
                time.sleep(wait)
    return False


def audio_duration_sec(path: Path) -> float:
    try:
        r = subprocess.run(
            [
                FFMPEG, "-i", str(path), "-f", "null", "-",
            ],
            capture_output=True,
            text=True,
        )
        # ffmpeg prints duration to stderr: Duration: 00:00:04.52
        import re
        m = re.search(r"Duration:\s*(\d+):(\d+):([\d.]+)", r.stderr)
        if m:
            h, mn, s = m.groups()
            return max(float(h) * 3600 + float(mn) * 60 + float(s), 2.5)
    except Exception:
        pass
    # fallback from mp3 size (~16kB/s at 128kbps)
    return max(path.stat().st_size / 16000, 3.0)


def run_ffmpeg(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run([FFMPEG, *args], capture_output=True, text=True, check=True)


def mux_av(video: Path, audio: Path, out: Path) -> bool:
    if _mux_av(video, audio, out):
        return True
    shutil.copy(video, out)
    return False


def build_episode(ep: dict, work: Path) -> Path | None:
    scene_videos: list[Path] = []
    audience = ep["audience"]

    for i, (caption, frame_file, motion) in enumerate(ep["scenes"]):
        print(f"  scene {i+1}/{len(ep['scenes'])}: {caption[:50]}...")
        base = load_frame(frame_file)
        mp3 = work / f"s{i}.mp3"
        if not fetch_tts(caption, audience, mp3):
            print("    skip scene (no TTS)")
            continue
        dur = audio_duration_sec(mp3) + 1.0
        n_frames = max(int(dur * FPS), FPS * 2)
        frames = [animate_frame(base, caption, t / max(n_frames - 1, 1), motion) for t in range(n_frames)]
        seg_v = work / f"s{i}.webm"
        write_segment(frames, seg_v)
        seg_out = work / f"s{i}_av.webm"
        if mux_av(seg_v, mp3, seg_out):
            scene_videos.append(seg_out)
        else:
            scene_videos.append(seg_v)

    if not scene_videos:
        return None

    list_file = work / "concat.txt"
    list_file.write_text("\n".join(f"file '{p.resolve()}'" for p in scene_videos), encoding="utf-8")
    final = OUT / f"{ep['id']}.webm"
    try:
        run_ffmpeg([
            "-y", "-f", "concat", "-safe", "0", "-i", str(list_file),
            "-c", "copy", str(final),
        ])
    except Exception:
        shutil.copy(scene_videos[0], final)
    return final


def main() -> None:
    print(f"Video profile: {PROFILE_NAME} ({VIDEO_WIDTH}x{VIDEO_HEIGHT} @ {VIDEO_FPS}fps, CRF via caly_video_quality)")
    FRAMES.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    for ep in EPISODES:
        print(f"Building {ep['id']}...")
        with tempfile.TemporaryDirectory() as td:
            result = build_episode(ep, Path(td))
            if result and result.exists():
                for dest in (WEB / "videos", FLUTTER / "assets" / "videos"):
                    dest.mkdir(parents=True, exist_ok=True)
                    shutil.copy(result, dest / result.name)
                dur_probe = audio_duration_sec(result) if result.suffix == ".webm" else 0
                try:
                    r = subprocess.run(
                        [FFMPEG, "-i", str(result)],
                        capture_output=True, text=True,
                    )
                    import re
                    m = re.search(r"Duration:\s*(\d+):(\d+):([\d.]+)", r.stderr)
                    if m:
                        h, mn, s = m.groups()
                        dur_probe = float(h) * 3600 + float(mn) * 60 + float(s)
                except Exception:
                    pass
                print(f"  OK {result.name} (~{dur_probe:.0f}s)")
            else:
                print(f"  FAILED {ep['id']}")


if __name__ == "__main__":
    main()
