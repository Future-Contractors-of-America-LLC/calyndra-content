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
APP = ROOT.parent / "calyndra-app"
CATALOG = ROOT / "videos" / "caly_friends_catalog.json"
FRAMES = ROOT / "videos" / "frames"
FRIENDS_FRAMES = FRAMES / "caly-friends"
WEB_VIDEOS = APP / "videos"
FLUTTER_VIDEOS = ROOT.parent / "calyndra-mobile-flutter" / "assets" / "videos"
BANDS_DIR = APP / "assets" / "caly-bands"
FRIENDS_DIR = APP / "assets" / "caly-friends"

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
    "pip_soft_breeze_long": [
        ("Hello, little one. Feel the soft breeze.", "welcome"),
        ("I'm Pip! The breeze tickles my nose.", "friend"),
        ("Elder Oak says God made gentle things for us.", "mentor"),
        ("Your grown-up can sway with you.", "caregiver"),
        ("Round and round. You are safe and loved.", "play"),
        ("In and out. Rest in God's gentle care.", "rest"),
        ("Bye-bye, friend. You are wonderfully made.", "farewell"),
    ],
    "pip_moonlight_snuggle_long": [
        ("Hello, sleepy friend. The moon is out.", "welcome"),
        ("I'm Pip. Snuggle time feels so nice.", "friend"),
        ("Elder Oak watches over us at night.", "mentor"),
        ("Your grown-up can snuggle you close.", "caregiver"),
        ("God made the night gentle and safe.", "lesson"),
        ("Shhh. Rest now. You are loved.", "rest"),
        ("Sweet dreams, little one.", "farewell"),
    ],
    "pip_twinkle_toes_long": [
        ("Hello! Let's wiggle our twinkle toes.", "welcome"),
        ("I'm Pip! Watch my toes go twinkle-twinkle.", "friend"),
        ("Elder Oak says every part of you is special.", "mentor"),
        ("Your grown-up can wiggle toes with you.", "caregiver"),
        ("Hop, hop! God made you to move with joy.", "play"),
        ("Twinkle... rest. You did so well.", "rest"),
        ("Bye-bye, twinkle toes!", "farewell"),
    ],
    "pip_rainbow_wave_long": [
        ("Hello, friend! Look what came after the rain.", "welcome"),
        ("I'm Pip! Red, orange, yellow - hello!", "friend"),
        ("Elder Oak says rainbows remind us of God's promise.", "mentor"),
        ("Your grown-up can name the colors with you.", "caregiver"),
        ("Wave hello to every beautiful color!", "play"),
        ("God keeps promises. You are loved.", "lesson"),
        ("Bye-bye, rainbow. See you again soon.", "farewell"),
    ],
    "pip_heartbeat_lullaby_long": [
        ("Hello, little heart. I'm Caly Seed.", "welcome"),
        ("I'm Pip. Ba-bum, ba-bum. Can you feel it?", "friend"),
        ("Elder Oak's love is steady like a heartbeat.", "mentor"),
        ("Your grown-up's heart beats for you too.", "caregiver"),
        ("Ba-bum. You are safe. Ba-bum. You are loved.", "play"),
        ("Rest now. God's love never stops beating for you.", "rest"),
        ("Goodnight, little heart.", "farewell"),
    ],
    "fern_flower_surprise_long": [
        ("Welcome to my garden! I'm Fern the fox.", "welcome"),
        ("Let's surprise Pip with flowers today.", "friend"),
        ("Kind surprises are like sunshine for the heart.", "mentor"),
        ("Shhh. Quiet steps make the surprise special.", "play"),
        ("For me? Wow! Thank you, Fern!", "share"),
        ("Sharing joy makes friendship grow.", "lesson"),
        ("See you in the garden soon!", "farewell"),
    ],
    "fern_patience_pots_long": [
        ("Today we plant seeds and practice patience.", "welcome"),
        ("Plant, water, and wait. Good things take time.", "friend"),
        ("Elder Oak says hope grows in quiet waiting.", "mentor"),
        ("Every day we look, but we don't pull yet.", "play"),
        ("Look! It grew! Waiting was worth it!", "celebrate"),
        ("You waited so well. I'm proud of you.", "lesson"),
        ("See you tomorrow, little sprouts!", "farewell"),
    ],
    "fern_butterfly_visit_long": [
        ("A butterfly came to visit! Walk softly.", "welcome"),
        ("Gentle hands. Gentle steps. Gentle hearts.", "friend"),
        ("God asks us to be gentle with all His creatures.", "mentor"),
        ("Your turn next, Pip. We take turns gently.", "share"),
        ("It trusts you because you were so gentle.", "lesson"),
        ("Thank you for visiting us, little butterfly.", "celebrate"),
        ("Gentleness makes friends of us all.", "farewell"),
    ],
    "fern_weeding_teamwork_long": [
        ("Oh no! Too many weeds. I need help.", "welcome"),
        ("Many hands make light work. Let's team up!", "friend"),
        ("Elder Oak says friends help friends grow.", "mentor"),
        ("Pull, pull, sing! Teamwork makes it fun.", "play"),
        ("Rest and share. Then we finish strong.", "share"),
        ("We did it together! What a beautiful garden.", "celebrate"),
        ("Teamwork today, friendship forever.", "farewell"),
    ],
    "fern_seed_gift_long": [
        ("These are my favorite seeds. I love them.", "welcome"),
        ("What if sharing them grows something even better?", "friend"),
        ("A gift given freely comes back in friendship.", "mentor"),
        ("For you, Moss. I want you to grow these too.", "share"),
        ("Thank you! I'll take good care of them.", "include"),
        ("Now we both have beauty because you shared.", "celebrate"),
        ("Sharing seeds planted joy in two places.", "farewell"),
    ],
    "moss_bridge_builders_long": [
        ("We're stuck on different sides. We need a bridge.", "welcome"),
        ("Moss the bear builds bridges, not walls.", "friend"),
        ("Strong roots hold up what friends build together.", "mentor"),
        ("Every friend has a job. Together we can do this.", "include"),
        ("Step by step, we connected two worlds.", "lesson"),
        ("Crossing together is better than staying apart.", "celebrate"),
        ("Bridge builders forever! See you on the path.", "farewell"),
    ],
    "moss_lost_and_found_long": [
        ("My ribbon is lost. It was my favorite.", "welcome"),
        ("Don't worry, Pip. We'll find it together.", "friend"),
        ("Everyone has a search spot. No friend left behind.", "include"),
        ("I see something blue near the berry bush!", "play"),
        ("Found it! You never gave up on your friend.", "lesson"),
        ("Thank you for looking until you found it.", "celebrate"),
        ("Seekers of the lost are heroes in God's eyes.", "farewell"),
    ],
    "moss_campfire_stories_long": [
        ("Welcome to Moss's campfire circle.", "welcome"),
        ("Tonight we share stories that warm the heart.", "friend"),
        ("Long ago, a tiny seed trusted the soil and grew.", "mentor"),
        ("Every friend has a story worth hearing.", "include"),
        ("Listen first. Then your turn to share.", "lesson"),
        ("Stories are like stars. They light up the dark.", "rest"),
        ("Same time next week? Stories keep us close.", "farewell"),
    ],
    "moss_apology_path_long": [
        ("I didn't mean to break it. Fern is so sad.", "welcome"),
        ("Before we fix the pot, let's calm our hearts.", "friend"),
        ("The apology path helps us say what matters.", "mentor"),
        ("Sorry means I care that I hurt you.", "lesson"),
        ("I'm sorry I broke your pot. Can we fix it together?", "repair"),
        ("I forgive you. Let's make something new.", "include"),
        ("Repair makes friendship stronger than before.", "celebrate"),
    ],
    "moss_team_harvest_long": [
        ("Harvest day! The garden gave us so much.", "welcome"),
        ("Pick together, share together, feast together.", "friend"),
        ("God gives seedtime and harvest. Give thanks.", "mentor"),
        ("We keep some and share some. That's how we grow.", "share"),
        ("There's always room for one more friend.", "include"),
        ("Thank you for food, friends, and this day.", "celebrate"),
        ("Team harvest complete. Until next season!", "farewell"),
    ],
    "reed_rumor_mist_long": [
        ("Something feels wrong. Stories are spreading.", "welcome"),
        ("I'm Reed. Before I speak, I perch and listen.", "friend"),
        ("Is it true? Is it kind? Is it needed?", "lesson"),
        ("Words spread fast. Truth takes courage.", "mentor"),
        ("Moss, I heard something. Can we talk honestly?", "repair"),
        ("The truth was simpler than the rumor.", "celebrate"),
        ("We checked facts. We won't spread mist again.", "farewell"),
    ],
    "reed_patience_listeners_long": [
        ("Everyone wants to talk. Who will listen?", "welcome"),
        ("Today I practice patience listening.", "friend"),
        ("Let them finish. Then you respond.", "interactive"),
        ("Deep listening helps friends grow strong.", "mentor"),
        ("I hear you. You're afraid the frost will come.", "lesson"),
        ("Did I understand you right? Tell me more.", "include"),
        ("Patience listeners change the whole meadow.", "celebrate"),
    ],
    "reed_honest_feather_long": [
        ("I found something special. Should I tell?", "welcome"),
        ("A small lie. No one will know.", "friend"),
        ("Lies get heavier every moment you carry them.", "lesson"),
        ("Truth may be hard, but it sets you free.", "mentor"),
        ("I found it and hid it. I'm sorry I lied.", "repair"),
        ("Honesty makes your wings strong again.", "celebrate"),
        ("We choose truth, even when it's hard.", "farewell"),
    ],
    "reed_storm_shelter_long": [
        ("A big storm is coming. Everyone find shelter!", "welcome"),
        ("Follow me to Elder Oak. We'll be safe together.", "friend"),
        ("God is our shelter when the world feels wild.", "mentor"),
        ("Close together. Breathe slow. You're not alone.", "rest"),
        ("Storms are loud, but they don't last forever.", "lesson"),
        ("We weathered it because we stayed together.", "celebrate"),
        ("The storm passed. We are stronger together.", "farewell"),
    ],
    "reed_mentor_circle_long": [
        ("Welcome to the mentor circle. Everyone teaches.", "welcome"),
        ("I learned from Elder Oak. Now I teach you.", "friend"),
        ("Each ring is a year of wisdom. I share mine.", "mentor"),
        ("Even the smallest friend has wisdom to share.", "include"),
        ("Teaching and learning go round and round.", "lesson"),
        ("The circle never breaks when we pass it on.", "celebrate"),
        ("Mentor circle complete. Wisdom grows here.", "farewell"),
    ],
    "sage_truth_telling_long": [
        ("Someone hid this damage. People could get hurt.", "welcome"),
        ("Staying quiet feels easier. But is it right?", "friend"),
        ("Truth without love can wound. Love without truth can harm.", "lesson"),
        ("The trail bridge is broken. We need to fix it now.", "repair"),
        ("Courageous truth protects the whole community.", "mentor"),
        ("Truth brought us together to make things right.", "celebrate"),
        ("We choose to tell the truth, even when it's hard.", "farewell"),
    ],
    "sage_peer_pressure_long": [
        ("Cross it to prove you're brave. Everyone's doing it.", "welcome"),
        ("I want friends. But this doesn't feel right.", "friend"),
        ("An anchor holds you steady when waves push hard.", "lesson"),
        ("No thank you. Let's find a safer way across.", "interactive"),
        ("Real friends respect your no.", "include"),
        ("You stayed true. That is real courage.", "mentor"),
        ("Integrity is choosing the harder right.", "celebrate"),
    ],
    "sage_forgiveness_trail_long": [
        ("I've carried this hurt for too long.", "welcome"),
        ("Forgiveness is a path, not a single step.", "lesson"),
        ("Put down what weighs you down. Travel lighter.", "mentor"),
        ("I release this. It doesn't serve me anymore.", "rest"),
        ("I was wrong. I'm sorry. Will you forgive me?", "repair"),
        ("Forgiveness doesn't forget. It frees.", "friend"),
        ("I am free. I can help others on this path too.", "celebrate"),
    ],
    "sage_service_saturday_long": [
        ("I planned to do nothing today.", "welcome"),
        ("What if doing something for others fills you up?", "friend"),
        ("Every can is someone's meal. That matters.", "lesson"),
        ("Serving can be quiet. Listening is service too.", "mentor"),
        ("Our meadow looks better because we showed up.", "share"),
        ("I thought I'd lose my day. I gained perspective.", "celebrate"),
        ("Same time next month. Who's in?", "farewell"),
    ],
    "sage_steady_anchor_long": [
        ("Everything is changing. I feel lost.", "welcome"),
        ("Change is a wave. Values are your anchor.", "lesson"),
        ("I choose what stays steady inside me.", "friend"),
        ("Bend with change. Stay rooted in what matters.", "mentor"),
        ("Waves crash. My anchor holds.", "rest"),
        ("When things shift, remember what you value.", "share"),
        ("Steady inside. Ready for what's next.", "celebrate"),
    ],
    "laurel_evening_rest_long": [
        ("Another full day. When do I rest?", "welcome"),
        ("Rest isn't lazy. It's how we refill.", "friend"),
        ("Even the earth rests each night. So may you.", "mentor"),
        ("I release today. Tomorrow can wait.", "rest"),
        ("Thank you, body, for carrying me today.", "lesson"),
        ("Into Your hands I rest my day.", "celebrate"),
        ("Rest well. Morning grace will come.", "farewell"),
    ],
    "laurel_caregiver_breath_long": [
        ("Caregiving is love in action. And it's exhausting.", "welcome"),
        ("You can't pour from an empty cup.", "lesson"),
        ("Four in, hold, four out. Strength returns.", "mentor"),
        ("This minute of breath is a gift to them too.", "rest"),
        ("I'm back. And I'm fully here now.", "caregiver"),
        ("Your peace helps us feel safe.", "celebrate"),
        ("Caregivers breathe together. We sustain each other.", "farewell"),
    ],
    "laurel_gratitude_journal_long": [
        ("This week felt like one long gray cloud.", "welcome"),
        ("Three lines each night. Blessings you almost missed.", "mentor"),
        ("Small things. But my chest feels lighter.", "friend"),
        ("Gratitude doesn't erase pain. It sits beside it.", "lesson"),
        ("Look how many mercies hid in ordinary days.", "celebrate"),
        ("Try three lines tonight. See what changes.", "share"),
        ("I won't forget. Thank You for today.", "farewell"),
    ],
    "laurel_community_table_long": [
        ("There's room for everyone at this table.", "welcome"),
        ("You belong here. Will you come eat with us?", "friend"),
        ("Many hands make the meal. Many hearts fill the room.", "include"),
        ("We thank God for food and for each other.", "mentor"),
        ("This table holds joy and sorrow both.", "lesson"),
        ("I hadn't laughed like that in months.", "celebrate"),
        ("Same table, new stories. See you next month.", "farewell"),
    ],
    "laurel_legacy_roots_long": [
        ("What will remain when my season changes?", "welcome"),
        ("Every lesson you taught is still growing.", "friend"),
        ("Each ring held a winter and a spring. So will yours.", "mentor"),
        ("We plant today what shade others will enjoy tomorrow.", "lesson"),
        ("Your roots are in everything I am becoming.", "share"),
        ("For the friends who come after us. Read when ready.", "celebrate"),
        ("Legacy isn't fame. It's love that keeps on rooting.", "farewell"),
    ],
}

BEATS_FILE = ROOT / "videos" / "caly_friends_story_beats.json"
AUDIENCE_BAND = {
    "baby": "seed",
    "toddler": "sprout",
    "child": "bud",
    "tween": "sprig",
    "teen": "vine",
    "adult": "bloom",
    "caregiver": "canopy",
}


def load_story_beats() -> dict[str, list[tuple[str, str]]]:
    beats: dict[str, list[tuple[str, str]]] = {
        k: list(v) for k, v in STORY_BEATS.items()
    }
    if BEATS_FILE.is_file():
        extra = json.loads(BEATS_FILE.read_text(encoding="utf-8"))
        for ep_id, rows in extra.items():
            beats[ep_id] = [(str(c), str(t)) for c, t in rows]
    return beats


def load_ep_band(catalog: dict) -> dict[str, str]:
    mapping = dict(EP_BAND)
    for ep in catalog.get("episodes", []):
        band = ep.get("band")
        if band in AUDIENCE_BAND:
            mapping[ep["id"]] = AUDIENCE_BAND[band]
    return mapping


_LEGACY_STORY_BEATS = STORY_BEATS
STORY_BEATS = _LEGACY_STORY_BEATS  # default; use load_story_beats() at runtime

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

EP_BAND: dict[str, str] = {
    "pip_gentle_hello_long": "seed",
    "fern_garden_share_long": "sprout",
    "moss_kindness_trail_long": "bud",
    "reed_wisdom_perch_long": "sprig",
    "sage_crossroads_long": "vine",
    "laurel_morning_song_long": "bloom",
    "pip_soft_breeze_long": "seed",
    "pip_moonlight_snuggle_long": "seed",
    "pip_twinkle_toes_long": "seed",
    "pip_rainbow_wave_long": "seed",
    "pip_heartbeat_lullaby_long": "seed",
    "fern_flower_surprise_long": "sprout",
    "fern_patience_pots_long": "sprout",
    "fern_butterfly_visit_long": "sprout",
    "fern_weeding_teamwork_long": "sprout",
    "fern_seed_gift_long": "sprout",
    "moss_bridge_builders_long": "bud",
    "moss_lost_and_found_long": "bud",
    "moss_campfire_stories_long": "bud",
    "moss_apology_path_long": "bud",
    "moss_team_harvest_long": "bud",
    "reed_rumor_mist_long": "sprig",
    "reed_patience_listeners_long": "sprig",
    "reed_honest_feather_long": "sprig",
    "reed_storm_shelter_long": "sprig",
    "reed_mentor_circle_long": "sprig",
    "sage_truth_telling_long": "vine",
    "sage_peer_pressure_long": "vine",
    "sage_forgiveness_trail_long": "vine",
    "sage_service_saturday_long": "vine",
    "sage_steady_anchor_long": "vine",
    "laurel_evening_rest_long": "bloom",
    "laurel_caregiver_breath_long": "bloom",
    "laurel_gratitude_journal_long": "bloom",
    "laurel_community_table_long": "bloom",
    "laurel_legacy_roots_long": "bloom",
}

FRIEND_PORTRAIT: dict[str, str] = {
    "Pip": "pip-baby.png",
    "Fern": "fern-toddler.png",
    "Moss": "moss-child.png",
    "Reed": "reed-tween.png",
    "Sage": "sage-teen.png",
    "Laurel": "laurel-adult.png",
}

TAG_STYLE: dict[str, dict[str, str]] = {
    "welcome": {"fill": "#d8f3dc", "accent": "#52b788", "glyph": "☀"},
    "friend": {"fill": "#ffe0ec", "accent": "#ff8fab", "glyph": "♥"},
    "mentor": {"fill": "#e9edc9", "accent": "#588157", "glyph": "🌿"},
    "caregiver": {"fill": "#e0f2fe", "accent": "#7ec8ff", "glyph": "🤝"},
    "play": {"fill": "#fff3bf", "accent": "#ffd43b", "glyph": "★"},
    "lesson": {"fill": "#e7f5ff", "accent": "#4dabf7", "glyph": "✦"},
    "rest": {"fill": "#ede7f6", "accent": "#b197fc", "glyph": "☾"},
    "share": {"fill": "#fff0f6", "accent": "#f783ac", "glyph": "⇄"},
    "interactive": {"fill": "#e6fcf5", "accent": "#38d9a9", "glyph": "◎"},
    "include": {"fill": "#fff4e6", "accent": "#ffa94d", "glyph": "＋"},
    "repair": {"fill": "#f3f0ff", "accent": "#9775fa", "glyph": "↺"},
    "celebrate": {"fill": "#fff9db", "accent": "#fab005", "glyph": "✧"},
    "farewell": {"fill": "#f8f0fc", "accent": "#da77f2", "glyph": "♡"},
}


def _font(size: int):
    for name in ("arialbd.ttf", "Arial Bold.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _load_rgba(path: Path, target_h: int) -> Image.Image | None:
    if not path.is_file():
        return None
    img = Image.open(path).convert("RGBA")
    scale = target_h / img.size[1]
    return img.resize((int(img.size[0] * scale), target_h), Image.Resampling.LANCZOS)


def _paste_centered(base: Image.Image, sprite: Image.Image, cx: int, bottom: int) -> None:
    x = cx - sprite.size[0] // 2
    y = bottom - sprite.size[1]
    base.paste(sprite, (x, y), sprite)


def friend_frame_name(ep_id: str, tag: str) -> str:
    return f"friends_{ep_id}_{tag}.png"


def ensure_friend_frame(
    ep_id: str,
    tag: str,
    title: str,
    friend: str,
    *,
    force: bool = False,
) -> str:
    FRIENDS_FRAMES.mkdir(parents=True, exist_ok=True)
    fname = friend_frame_name(ep_id, tag)
    path = FRIENDS_FRAMES / fname
    if path.exists() and not force:
        return fname

    band = EP_BAND.get(ep_id, "sprout")
    style = TAG_STYLE.get(tag, TAG_STYLE["welcome"])
    w, h = 1280, 720
    img = Image.new("RGB", (w, h), PALETTE["cream"])
    d = ImageDraw.Draw(img)

    for y in range(h):
        t = y / h
        r = int(255 * (1 - t) + 184 * t)
        g = int(248 * (1 - t) + 240 * t)
        b = int(232 * (1 - t) + 216 * t)
        d.line([(0, y), (w, y)], fill=(r, g, b))

    d.rounded_rectangle((60, 50, w - 60, h - 110), radius=36, fill=style["fill"], outline=PALETTE["outline"], width=5)
    d.rounded_rectangle((90, 80, w - 90, h - 200), radius=28, fill="#ffffff", outline=PALETTE["outline"], width=3)

    caly = _load_rgba(BANDS_DIR / f"{band}.png", 320)
    if caly:
        _paste_centered(img, caly, 340, h - 220)
    else:
        d.ellipse((220, 120, 460, 360), fill=PALETTE["skyBlue"], outline=PALETTE["outline"], width=5)

    friend_file = FRIEND_PORTRAIT.get(friend)
    if tag == "mentor":
        friend_sprite = _load_rgba(FRIENDS_DIR / "elder-oak-caregiver.png", 300)
    elif friend_file:
        friend_sprite = _load_rgba(FRIENDS_DIR / friend_file, 300)
    else:
        friend_sprite = None
    if friend_sprite:
        _paste_centered(img, friend_sprite, 940, h - 220)
    else:
        d.ellipse((820, 140, 1060, 380), fill=PALETTE["mint"], outline=PALETTE["outline"], width=5)

    tag_text = tag.replace("_", " ").title()
    pill_w = max(180, d.textlength(tag_text, font=_font(26)) + 70)
    pill_x = w - pill_w - 100
    d.rounded_rectangle((pill_x, 70, pill_x + pill_w, 120), radius=20, fill=style["accent"], outline=PALETTE["outline"], width=3)
    glyph_font = _font(22)
    title_font = _font(44)
    sub_font = _font(26)
    d.text((pill_x + 16, 82), style["glyph"], fill="#ffffff", font=glyph_font)
    d.text((pill_x + 48, 84), tag_text, fill="#ffffff", font=sub_font)

    d.text((w // 2 - d.textlength(title, font=title_font) / 2, h - 175), title, fill=PALETTE["outline"], font=title_font)
    sub = f"Caly and Friends · {friend}"
    d.text((w // 2 - d.textlength(sub, font=sub_font) / 2, h - 125), sub, fill=PALETTE["outline"], font=sub_font)
    d.line([(120, h - 95), (w - 120, h - 95)], fill=style["accent"], width=3)

    img.save(path)
    return fname


def pregenerate_all_frames(*, force: bool = False) -> int:
    catalog = load_catalog()
    made = 0
    for ep in catalog["episodes"]:
        ep_id = ep["id"]
        beats = STORY_BEATS.get(ep_id, [])
        seen: set[str] = set()
        for _caption, tag in beats:
            if tag in seen:
                continue
            seen.add(tag)
            ensure_friend_frame(ep_id, tag, ep["title"], ep["friend"], force=force)
            made += 1
    return made


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
    parser.add_argument("--pending", action="store_true", help="Render script-only episodes only")
    parser.add_argument("--placeholder", action="store_true", help="Write stub webm for script-only episodes")
    parser.add_argument("--id", help="Render a single episode id")
    parser.add_argument("--pregenerate-frames", action="store_true", help="Build polished frames for all STORY_BEATS tags")
    parser.add_argument("--force-frames", action="store_true", help="Regenerate frames even if PNG exists")
    args = parser.parse_args()

    catalog = load_catalog()
    WEB_VIDEOS.mkdir(parents=True, exist_ok=True)
    FRAMES.mkdir(parents=True, exist_ok=True)

    if args.pregenerate_frames:
        n = pregenerate_all_frames(force=args.force_frames)
        print(f"Pregenerated {n} friend frame(s) -> {FRIENDS_FRAMES}")
        if not args.pilot and not args.all and not args.id and not args.placeholder:
            return

    def write_script_placeholders() -> None:
        for ep_meta in catalog["episodes"]:
            if ep_meta.get("status") != "script-only":
                continue
            dest = WEB_VIDEOS / ep_meta["webm"]
            if dest.exists():
                continue
            ok = write_placeholder_webm(dest, ep_meta["title"], seconds=5.0)
            print(f"Placeholder {'OK' if ok else 'FAIL'} {dest.name}")

    if args.placeholder and not args.pilot and not args.all and not args.id and not args.pending:
        write_script_placeholders()
        return

    if not args.pilot and not args.all and not args.id and not args.pending:
        parser.print_help()
        return

    def save_catalog() -> None:
        CATALOG.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")

    for ep_meta in catalog["episodes"]:
        ep_id = ep_meta["id"]
        if args.id and ep_id != args.id:
            continue
        if args.pending and ep_meta.get("status") != "script-only":
            continue
        if args.pilot and not ep_meta.get("pilot"):
            continue

        pilot = bool(args.pilot and ep_meta.get("pilot"))
        scenes = expand_scenes(ep_meta, pilot=pilot)
        print(f"Building {ep_id} ({len(scenes)} scenes, pilot={pilot})...")
        with tempfile.TemporaryDirectory() as td:
            result = build_episode_local(ep_meta, scenes, Path(td))
            dest = WEB_VIDEOS / ep_meta["webm"]
            if result and result.exists():
                shutil.copy(result, dest)
                FLUTTER_VIDEOS.mkdir(parents=True, exist_ok=True)
                shutil.copy(result, FLUTTER_VIDEOS / ep_meta["webm"])
                if ep_meta.get("status") == "script-only":
                    ep_meta["status"] = "complete"
                    ep_meta["pilot"] = False
                    save_catalog()
                print(f"  OK {dest.name}")
            else:
                print(f"  TTS/render failed - writing placeholder for {ep_id}")
                write_placeholder_webm(dest, ep_meta["title"], seconds=8.0 if pilot else 5.0)

    if args.pilot and args.placeholder:
        write_script_placeholders()


if __name__ == "__main__":
    main()
