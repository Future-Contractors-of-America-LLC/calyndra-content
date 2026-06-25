#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate sing-along-catalog.json and show_* voice keys in caly-voice-scripts.json."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG_OUT = ROOT / "games" / "sing-along-catalog.json"
VOICE = ROOT / "games" / "caly-voice-scripts.json"

BAND = {
    "baby": ("seed", "Seed"),
    "toddler": ("sprout", "Sprout"),
    "child": ("bud", "Bud"),
    "tween": ("sprig", "Sprig"),
    "teen": ("vine", "Vine"),
    "adult": ("bloom", "Bloom"),
    "caregiver": ("canopy", "Canopy"),
}

POSES = ("wave", "listen-ear", "drum-dance", "jump-celebrate")
CUES = ("wave", "listen", "dance", "celebrate")


def beat(ms: int, lyric: str, word: str, idx: int) -> dict:
    return {
        "ms": ms,
        "pose": POSES[idx % 4],
        "lyric": lyric,
        "word": word,
        "mascotCue": CUES[idx % 4],
    }


def episode(
    eid: str,
    title: str,
    description: str,
    scene: str,
    words: list[str],
    lyrics: list[str],
    *,
    duration_ms: int = 180_000,
    is_new: bool = True,
) -> dict:
    assert len(words) == len(lyrics) == 4
    step = duration_ms // 5
    beats = [beat(step * i, lyrics[i], words[i], i) for i in range(4)]
    key = eid.replace("-", "_")
    return {
        "id": eid,
        "title": title,
        "description": description,
        "durationMs": duration_ms,
        "scene": scene,
        "voiceIntroKey": f"show_{key}_intro",
        "voiceBeatKey": f"show_{key}_beat",
        "musicBed": f"content/sing-along/music/{eid}.wav",
        "isNew": is_new,
        "beats": beats,
    }


EPISODES: dict[str, list[dict]] = {
    "baby": [
        episode(
            "seed-gentle-hello",
            "Caly Seed's Gentle Hello",
            "Soft hello song with hi, love, and gentle waves with family warmth.",
            "meadow",
            ["hi", "love", "more", "bye"],
            [
                "Hi, hi, hi! Soft hello! Tap HI - God loves you so!",
                "Love, love, love! Warm and bright! Tap LOVE - shine your light!",
                "More sweet songs? Gentle and slow! Tap MORE - watch us grow!",
                "Bye bye, little friend! Rest and glow! Tap BYE - soft and low!",
            ],
            duration_ms=165_000,
        ),
        episode(
            "seed-night-glow",
            "Seed's Night Glow Lullaby",
            "Bedtime lullaby with sleep, love, and peaceful night words.",
            "meadow",
            ["sleep", "love", "night", "bye"],
            [
                "Sleepy time, sleepy time! Tap SLEEP - rest divine!",
                "Love wraps round you, safe and near! Tap LOVE - angels here!",
                "Night night stars begin to show! Tap NIGHT - soft moon glow!",
                "Bye bye dreams, sweet and slow! Tap BYE - off we go!",
            ],
            duration_ms=195_000,
        ),
        episode(
            "seed-yummy-praise",
            "Seed's Yummy Praise Song",
            "Mealtime joy: eat, drink, more, and thankful all done.",
            "playroom",
            ["eat", "drink", "more", "all done"],
            [
                "Yummy yum! Bless this bite! Tap EAT - what a delight!",
                "Sip and smile, cool and clear! Tap DRINK - thankful cheer!",
                "More please? Gentle and true! Tap MORE - God cares for you!",
                "All done! Full and blessed! Tap ALL DONE - happy rest!",
            ],
            duration_ms=180_000,
        ),
        episode(
            "seed-feelings-soft",
            "Seed's Soft Feelings Song",
            "Happy, sad, hugs, and love - feelings are okay with Caly.",
            "meadow",
            ["happy", "sad", "hug please", "love"],
            [
                "Happy face! Joyful day! Tap HAPPY - clap and play!",
                "Sad sometimes - that's okay! Tap SAD - we pray and stay!",
                "Hug please! Warm and tight! Tap HUG PLEASE - love feels right!",
                "Love, love, love from up above! Tap LOVE - gentle dove!",
            ],
            duration_ms=175_000,
        ),
        episode(
            "seed-peek-play",
            "Seed's Peek and Play",
            "Playful peek-a-boo with ball, play, and happy yes.",
            "playroom",
            ["peek", "play", "ball", "yes"],
            [
                "Peek peek! Where am I? Tap PEEK - hello sky!",
                "Play time fun for you and me! Tap PLAY - one-two-three!",
                "Bouncy ball goes roll and spin! Tap BALL - let's begin!",
                "Yes! Yes! Good try today! Tap YES - hooray, hooray!",
            ],
            duration_ms=170_000,
        ),
        episode(
            "seed-family-circle",
            "Seed's Family Circle",
            "Mama, dada, love, and hugs - family circle song.",
            "meadow",
            ["mama", "dada", "love", "hug please"],
            [
                "Mama's here with open arms! Tap MAMA - safe from harm!",
                "Dada cheers you brave and strong! Tap DADA - sing along!",
                "Love connects our family tree! Tap LOVE - you and me!",
                "Hug please! Circle round and round! Tap HUG PLEASE - joy abounds!",
            ],
            duration_ms=185_000,
        ),
    ],
    "toddler": [
        episode(
            "caly-hello-song",
            "Caly's Hello Song",
            "Sprout's classic hello: hi, help, more, and bye on the beat.",
            "meadow",
            ["hi", "I need help", "more", "bye"],
            [
                "Hi, hi, hi! Wave hello! Tap HI - here we go!",
                "Help is here! Friends draw near! Tap HELP - loud and clear!",
                "More, more, more! Tap the floor! Tap MORE - encore!",
                "Bye bye bye! Wave up high! Tap BYE - see you sky!",
            ],
            duration_ms=180_000,
            is_new=False,
        ),
        episode(
            "sprout-help-power",
            "Sprout's Help Power Song",
            "Ask for help, say please, and celebrate brave tries.",
            "meadow",
            ["I need help", "please", "more", "yes"],
            [
                "Need some help? That's smart and true! Tap HELP - Caly's with you!",
                "Please and thank you - kind and sweet! Tap PLEASE - polite complete!",
                "More fun words? Let's explore! Tap MORE - hear them roar!",
                "Yes you can! Brave heart beats! Tap YES - victory treats!",
            ],
            duration_ms=195_000,
        ),
        episode(
            "sprout-feelings-dance",
            "Sprout's Feelings Dance",
            "Happy, sad, love, and hugs - dance your feelings out.",
            "playroom",
            ["happy", "sad", "love", "hug please"],
            [
                "Happy dance! Spin around! Tap HAPPY - joyful sound!",
                "Sad days pass - we're still here! Tap SAD - wipe the tear!",
                "Love your neighbor, love your friend! Tap LOVE - hearts ascend!",
                "Hug please! Squeeze so tight! Tap HUG PLEASE - feels just right!",
            ],
            duration_ms=185_000,
        ),
        episode(
            "sprout-yummy-fun",
            "Sprout's Yummy Fun Song",
            "Eat, drink, more, and all done - thankful mealtime fun.",
            "playroom",
            ["eat", "drink", "more", "all done"],
            [
                "Crunch and munch - yummy treat! Tap EAT - can't be beat!",
                "Glug glug drink - cool and fine! Tap DRINK - grape or lime!",
                "More please! Seconds please! Tap MORE - taste the breeze!",
                "All done plate! What a feast! Tap ALL DONE - happy beast!",
            ],
            duration_ms=175_000,
        ),
        episode(
            "sprout-play-outside",
            "Sprout's Outside Play Song",
            "Go, play, ball, and dog - outdoor adventure sing-along.",
            "meadow",
            ["go", "play", "ball", "dog"],
            [
                "Let's go go go outside today! Tap GO - run and play!",
                "Play ground swings and sunny skies! Tap PLAY - butterflies!",
                "Kick the ball - roll and bounce! Tap BALL - count by ounce!",
                "Woof woof dog! Furry friend! Tap DOG - play won't end!",
            ],
            duration_ms=190_000,
        ),
        episode(
            "sprout-family-song",
            "Sprout's Family Love Song",
            "Mommy, daddy, love, and bye - family gratitude song.",
            "meadow",
            ["mommy", "daddy", "love", "bye"],
            [
                "Mommy loves you day and night! Tap MOMMY - shining light!",
                "Daddy strong and kind and true! Tap DADDY - hugs for you!",
                "Love the gift from God above! Tap LOVE - gentle dove!",
                "Bye for now - see you soon! Tap BYE - afternoon!",
            ],
            duration_ms=180_000,
        ),
        episode(
            "sprout-gentle-choice",
            "Sprout's Gentle Choice Song",
            "Stop, wait, no, and yes - your body, your choice.",
            "meadow",
            ["stop", "wait", "no", "yes"],
            [
                "Stop and pause - breathe with me! Tap STOP - count to three!",
                "Wait right here - patience grows! Tap WAIT - calm and slow!",
                "No means no - your voice is strong! Tap NO - sing the song!",
                "Yes when ready - brave and free! Tap YES - that's the key!",
            ],
            duration_ms=200_000,
        ),
    ],
    "child": [
        episode(
            "bud-adventure-hello",
            "Bud's Adventure Hello",
            "Quest begins: hi, help, play, and grateful bye.",
            "meadow",
            ["hi", "I need help", "play", "bye"],
            [
                "Hi explorer! Quest begins! Tap HI - adventure wins!",
                "Brave help ask - friends unite! Tap HELP - shining light!",
                "Play the path through field and stream! Tap PLAY - teamwork dream!",
                "Bye brave bud - till we meet! Tap BYE - mission complete!",
            ],
            duration_ms=185_000,
        ),
        episode(
            "bud-kindness-quest",
            "Bud's Kindness Quest",
            "Please, love, share spirit - kindness on the beat.",
            "meadow",
            ["please", "love", "share", "thank you"],
            [
                "Please and thank you - kindness code! Tap PLEASE - gentle road!",
                "Love your neighbor - golden rule! Tap LOVE - Sunday school!",
                "Share your toys and share your time! Tap SHARE - rhythm rhyme!",
                "Thank you God for gifts each day! Tap THANK YOU - hip hooray!",
            ],
            duration_ms=195_000,
        ),
        episode(
            "bud-feelings-journey",
            "Bud's Feelings Journey",
            "Happy, sad, hurt, and gentle - name what you feel.",
            "playroom",
            ["happy", "sad", "hurt", "gentle"],
            [
                "Happy beats - drum and cheer! Tap HAPPY - bright and clear!",
                "Sad is real - we understand! Tap SAD - holding hand!",
                "Hurt? Tell someone - brave and true! Tap HURT - Caly's with you!",
                "Gentle breath in - peace flows through! Tap GENTLE - sky so blue!",
            ],
            duration_ms=190_000,
        ),
        episode(
            "bud-school-day",
            "Bud's School Day Song",
            "Go, book, wait, and all done - school routine sing-along.",
            "playroom",
            ["go", "book", "wait", "all done"],
            [
                "Time for school - grab your pack! Tap GO - don't look back!",
                "Open book - stories grow! Tap BOOK - read and know!",
                "Wait your turn - patience wins! Tap WAIT - calm begins!",
                "All done! Homework's through! Tap ALL DONE - proud of you!",
            ],
            duration_ms=200_000,
        ),
        episode(
            "bud-nature-praise",
            "Bud's Nature Praise",
            "Outside, dog, ball, and play - celebrate God's creation.",
            "meadow",
            ["outside", "dog", "ball", "play"],
            [
                "Outside air - warm and bright! Tap OUTSIDE - golden light!",
                "Faithful dog - loyal friend! Tap DOG - play won't end!",
                "Bounce the ball - teamwork call! Tap BALL - give your all!",
                "Play and laugh - grateful heart! Tap PLAY - joyful art!",
            ],
            duration_ms=175_000,
        ),
        episode(
            "bud-courage-stop",
            "Bud's Courage and Stop Song",
            "Stop, no, yes, and help - boundaries and bravery.",
            "meadow",
            ["stop", "no", "yes", "I need help"],
            [
                "Stop signal - body choice! Tap STOP - use your voice!",
                "No is strong - respect your space! Tap NO - winning race!",
                "Yes when ready - try again! Tap YES - sunshine rain!",
                "Ask for help - heroes do! Tap HELP - Caly's crew!",
            ],
            duration_ms=185_000,
        ),
    ],
    "tween": [
        episode(
            "sprig-vibe-hello",
            "Sprig's Vibe Hello",
            "Cool hello: hi, help, go, and bye at your pace.",
            "meadow",
            ["hi", "I need help", "go", "bye"],
            [
                "Hey - hi there! Tap HI when ready.",
                "Need help? Totally fine. Tap HELP - you're shining.",
                "Go for it - your call. Tap GO - standing tall.",
                "Bye for now - catch you later. Tap BYE - see you, creator.",
            ],
            duration_ms=170_000,
        ),
        episode(
            "sprig-gratitude-groove",
            "Sprig's Gratitude Groove",
            "Thank you, love, happy, and gentle - grateful groove.",
            "meadow",
            ["thank you", "love", "happy", "gentle"],
            [
                "Grateful heart - name your thanks. Tap THANK YOU - joy in ranks.",
                "Love is patient, love is kind. Tap LOVE - peace of mind.",
                "Happy moment - notice it. Tap HAPPY - legit.",
                "Gentle breath - you've got this. Tap GENTLE - gentle bliss.",
            ],
            duration_ms=180_000,
        ),
        episode(
            "sprig-friendship-beat",
            "Sprig's Friendship Beat",
            "Share, please, play, and yes - friendship on the beat.",
            "playroom",
            ["share", "please", "play", "yes"],
            [
                "Share the moment - pass it on. Tap SHARE - we're strong.",
                "Please goes far - kindness art. Tap PLEASE - from the heart.",
                "Play together - laugh and learn. Tap PLAY - take your turn.",
                "Yes to trying - growth is real. Tap YES - how you feel.",
            ],
            duration_ms=175_000,
        ),
        episode(
            "sprig-boundary-power",
            "Sprig's Boundary Power",
            "Stop, no, wait, and help - your boundaries matter.",
            "meadow",
            ["stop", "no", "wait", "I need help"],
            [
                "Stop - pause when you need space. Tap STOP - steady pace.",
                "No is a full sentence. Tap NO - let it show.",
                "Wait - patience is a skill. Tap WAIT - breathe your fill.",
                "Help is strength, not weakness. Tap HELP - calm and meekness.",
            ],
            duration_ms=190_000,
        ),
        episode(
            "sprig-creative-flow",
            "Sprig's Creative Flow",
            "Book, music, go, and more - creative flow sing-along.",
            "playroom",
            ["book", "music", "go", "more"],
            [
                "Open book - worlds unfold. Tap BOOK - stories told.",
                "Music moves - feel the beat. Tap MUSIC - tap your feet.",
                "Go create - make something new. Tap GO - just for you.",
                "More ideas? Keep them flowing. Tap MORE - keep on growing.",
            ],
            duration_ms=185_000,
        ),
    ],
    "teen": [
        episode(
            "vine-honest-heart",
            "Vine's Honest Heart",
            "Sing about truth, respect, and finding your voice with Caly Vine.",
            "crossroads",
            ["truth", "respect", "voice", "friend"],
            [
                "Truth is light - speak with care. Tap TRUTH - stand aware.",
                "Respect goes both ways we share. Tap RESPECT - show you care.",
                "Your VOICE is yours - clear and strong. Tap VOICE - sing your song.",
                "Friends like River walk along. Tap FRIEND - we belong.",
            ],
            duration_ms=195_000,
        ),
        episode(
            "vine-calm-storm",
            "Calm Before the Storm",
            "Regulation sing-along with break, breathe, and help.",
            "meadow",
            ["break", "breathe", "help", "calm"],
            [
                "Need a BREAK? That is okay. Tap BREAK - pause and play.",
                "BREATHE in slow - let tension go. Tap BREATHE - gentle flow.",
                "Ask for HELP - brave and true. Tap HELP - I am with you.",
                "CALM returns - skies turn blue. Tap CALM - we made it through.",
            ],
            duration_ms=180_000,
        ),
        episode(
            "vine-river-song",
            "River and Caly Song",
            "Celebrating neurodiverse friendship with Caly's best friend River.",
            "stream",
            ["friend", "wait", "share", "joy"],
            [
                "RIVER waits - that's okay. Tap WAIT - we find our way.",
                "Different minds - gifts to share. Tap FRIEND - love and care.",
                "SHARE the moment, slow or fast. Tap SHARE - friendship lasts.",
                "JOY in being who we are. Tap JOY - near and far.",
            ],
            duration_ms=200_000,
        ),
        episode(
            "vine-my-space",
            "My Space, My Pace",
            "Assent-first sing-along about boundaries.",
            "garden",
            ["no", "space", "yes", "choice"],
            [
                "NO is power - use it well. Tap NO - truth to tell.",
                "My SPACE is mine - honor that. Tap SPACE - tit for tat.",
                "YES when ready - not before. Tap YES - open door.",
                "CHOICE is yours - always more. Tap CHOICE - explore.",
            ],
            duration_ms=175_000,
        ),
        episode(
            "vine-evening-glow",
            "Evening Glow",
            "Wind-down sing-along for teen band.",
            "sunset",
            ["rest", "grateful", "peace", "night"],
            [
                "REST your mind - day is done. Tap REST - setting sun.",
                "GRATEFUL heart - count the good. Tap GRATEFUL - understood.",
                "PEACE like leaves in evening air. Tap PEACE - God is there.",
                "NIGHT arrives - soft and deep. Tap NIGHT - gentle sleep.",
            ],
            duration_ms=190_000,
        ),
    ],
    "adult": [
        episode(
            "bloom-morning-grace",
            "Morning Grace",
            "Adult Bloom sing-along about gratitude and purpose.",
            "garden",
            ["grateful", "serve", "hope", "love"],
            [
                "GRATEFUL for this brand-new day. Tap GRATEFUL - light the way.",
                "SERVE with hands and open heart. Tap SERVE - do your part.",
                "HOPE grows where kindness starts. Tap HOPE - play your part.",
                "LOVE remains when day departs. Tap LOVE - work of art.",
            ],
            duration_ms=185_000,
        ),
        episode(
            "bloom-family-circle",
            "Family Circle Song",
            "Mom, dad, little brother, and Caly Bloom together.",
            "home",
            ["family", "mommy", "daddy", "love"],
            [
                "FAMILY circle, strong and wide. Tap FAMILY - side by side.",
                "MOMMY's warmth - gentle guide. Tap MOMMY - by your side.",
                "DADDY's strength - safe inside. Tap DADDY - stride by stride.",
                "LOVE holds all - our joy and pride. Tap LOVE - open wide.",
            ],
            duration_ms=195_000,
        ),
        episode(
            "bloom-work-rest",
            "Work and Rest",
            "Balance sing-along for adult learners.",
            "meadow",
            ["work", "rest", "help", "peace"],
            [
                "WORK with purpose, one step more. Tap WORK - shut the door.",
                "REST restores what stress may steal. Tap REST - truly feel.",
                "HELP is strength, not shame to show. Tap HELP - let it flow.",
                "PEACE returns when rhythms grow. Tap PEACE - soft and slow.",
            ],
            duration_ms=180_000,
        ),
        episode(
            "bloom-voice-rise",
            "Voice Rise",
            "AAC advocacy sing-along.",
            "stage",
            ["voice", "speak", "listen", "share"],
            [
                "Your VOICE matters - never small. Tap VOICE - stand tall.",
                "SPEAK your truth with calm and care. Tap SPEAK - fill the air.",
                "LISTEN deep - others share. Tap LISTEN - show you care.",
                "SHARE the words that set you free. Tap SHARE - harmony.",
            ],
            duration_ms=190_000,
        ),
        episode(
            "bloom-evening-thanks",
            "Evening Thanks",
            "Closing gratitude sing-along.",
            "sunset",
            ["thanks", "rest", "hope", "night"],
            [
                "THANKS for words we used today. Tap THANKS - grace to stay.",
                "REST your voice - you've had your say. Tap REST - end of day.",
                "HOPE for tomorrow's bright display. Tap HOPE - on the way.",
                "NIGHT brings peace - softly lay. Tap NIGHT - night and day.",
            ],
            duration_ms=175_000,
        ),
    ],
    "caregiver": [
        episode(
            "canopy-model-song",
            "Model and Tap Song",
            "Caregiver co-play sing-along for aided language stimulation.",
            "classroom",
            ["model", "wait", "celebrate", "help"],
            [
                "MODEL the word - slow and clear. Tap MODEL - learner hears.",
                "WAIT for response - patience here. Tap WAIT - drawing near.",
                "CELEBRATE each try with cheer. Tap CELEBRATE - sincere.",
                "HELP when needed, never fear. Tap HELP - always near.",
            ],
            duration_ms=185_000,
        ),
        episode(
            "canopy-assent-first",
            "Assent First Lullaby",
            "Honoring skip, pause, and no in sing-along play.",
            "meadow",
            ["pause", "no", "yes", "choice"],
            [
                "PAUSE anytime - that's okay. Tap PAUSE - gentle way.",
                "NO means no - we honor that. Tap NO - tit for tat.",
                "YES when ready - patient wait. Tap YES - celebrate.",
                "CHOICE belongs to every mate. Tap CHOICE - assent is great.",
            ],
            duration_ms=180_000,
        ),
        episode(
            "canopy-gentle-routine",
            "Gentle Routine Song",
            "Daily routine words for co-play.",
            "home",
            ["eat", "wash", "play", "sleep"],
            [
                "EAT together - nourish well. Tap EAT - ring the bell.",
                "WASH hands clean - splash and dry. Tap WASH - reach the sky.",
                "PLAY with joy - laugh out loud. Tap PLAY - proud and proud.",
                "SLEEP time comes - soft cloud. Tap SLEEP - rest allowed.",
            ],
            duration_ms=195_000,
        ),
        episode(
            "canopy-family-team",
            "Family Team Song",
            "Caregiver band family circle with Caly Canopy.",
            "garden",
            ["team", "love", "help", "together"],
            [
                "TEAM means all of us as one. Tap TEAM - work begun.",
                "LOVE in action, day by day. Tap LOVE - lead the way.",
                "HELP each other, come what may. Tap HELP - hip hooray.",
                "TOGETHER strong in every way. Tap TOGETHER - stay.",
            ],
            duration_ms=190_000,
        ),
        episode(
            "canopy-evening-calm",
            "Evening Calm for Caregivers",
            "Wind-down co-regulation sing-along.",
            "sunset",
            ["calm", "breathe", "thanks", "rest"],
            [
                "CALM your body, calm your mind. Tap CALM - gentle kind.",
                "BREATHE together, slow and deep. Tap BREATHE - peaceful sleep.",
                "THANKS for showing up today. Tap THANKS - grace to stay.",
                "REST tonight - you've paved the way. Tap REST - end of day.",
            ],
            duration_ms=175_000,
        ),
    ],
}

INTRO_TEMPLATES = {
    "baby": "Soft sing-along time! I am Caly {nick}. Tap words gently with your grown-up!",
    "toddler": "Sing-along time! I am Caly {nick}! Tap the words on the beat - hooray!",
    "child": "Caly Show time! Bud adventure sing-along - tap words when you hear them!",
    "tween": "Caly Show - Sprig style. Tap words at your pace. Skip anytime.",
    "teen": "Caly Show - Vine band. Your voice, your rhythm. Tap when ready.",
    "adult": "Caly Show - Bloom. Tap words that match your mood today.",
    "caregiver": "Caly Show - Canopy. Model and tap together with your learner.",
}

BEAT_TEMPLATES = {
    "baby": "Soft tap for {word}! Gentle and sweet!",
    "toddler": "Tap {word}! {word}! On the beat!",
    "child": "Quest tap: {word}! Go for it!",
    "tween": "Tap {word} when you're ready.",
    "teen": "Tap {word} — your pace, your choice.",
    "adult": "Tap {word} when it fits the lyric.",
    "caregiver": "Model {word} — tap together.",
}


def voice_lines(aud: str, ep: dict) -> tuple[str, str]:
    nick = BAND[aud][1]
    title = ep["title"]
    intro = INTRO_TEMPLATES[aud].format(nick=nick)
    if aud == "baby":
        intro = f"{title}! {intro}"
    elif aud == "toddler":
        intro = f"{title}! {intro}"
    elif aud == "child":
        intro = f"{title} - {intro}"
    else:
        intro = f"{title}. {intro}"
    beat = BEAT_TEMPLATES[aud]
    return intro, beat


def main() -> None:
    catalog = {
        "id": "sing-along-catalog",
        "version": "1.0.0",
        "updatedUtc": datetime.now(timezone.utc).isoformat(),
        "description": "Per-audience Caly Show sing-along episodes - interactive tap-and-sing with mascot.",
        "audiences": {},
    }

    voice = json.loads(VOICE.read_text(encoding="utf-8"))

    for aud, eps in EPISODES.items():
        portrait, nickname = BAND[aud]
        for ep in eps:
            ep["bandPortrait"] = portrait
        catalog["audiences"][aud] = {
            "bandPortrait": portrait,
            "nickname": nickname,
            "episodes": eps,
        }
        block = voice.setdefault(aud, {})
        for ep in eps:
            intro, beat = voice_lines(aud, ep)
            block[ep["voiceIntroKey"]] = intro
            block[ep["voiceBeatKey"]] = beat

    CATALOG_OUT.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    VOICE.write_text(json.dumps(voice, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {CATALOG_OUT.name} - episodes per band:")
    for aud, eps in EPISODES.items():
        new = sum(1 for e in eps if e.get("isNew", True))
        print(f"  {aud}: {len(eps)} total ({new} new)")


if __name__ == "__main__":
    main()
