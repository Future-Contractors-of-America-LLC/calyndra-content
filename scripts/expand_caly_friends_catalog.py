#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add 6 Caly and Friends episodes per age band (baby-adult) to catalog + scripts + beats."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "videos" / "caly_friends_catalog.json"
BEATS_OUT = ROOT / "videos" / "caly_friends_story_beats.json"
SCRIPTS = ROOT / "videos" / "scripts"

BAND_META = {
    "baby": ("seed", "Caly Seed", 300, 50),
    "toddler": ("sprout", "Caly Sprout", 600, 100),
    "child": ("bud", "Caly Bud", 900, 150),
    "tween": ("sprig", "Caly Sprig", 1200, 200),
    "teen": ("vine", "Caly Vine", 1800, 300),
    "adult": ("bloom", "Caly Bloom", 2700, 450),
}

# id_suffix, title, friend, lesson, beats[(caption, tag)]
NEW_EPISODES: dict[str, list[tuple]] = {
    "baby": [
        (
            "wren_lullaby_nest",
            "Wren's Lullaby Nest",
            "Wren",
            "God's love shelters us like a warm nest.",
            [
                ("Hello, little one. Wren built a soft nest today.", "welcome"),
                ("I'm Wren the chick. Cheep, cheep!", "friend"),
                ("Elder Oak rustles a gentle lullaby.", "mentor"),
                ("Your grown-up can rock you side to side.", "caregiver"),
                ("God keeps you safe in His caring arms.", "lesson"),
                ("Snuggle close. Rest is a gift.", "rest"),
                ("Bye-bye, sleepy friend.", "farewell"),
            ],
        ),
        (
            "dot_twinkle_pause",
            "Dot's Twinkle Pause",
            "Dot",
            "Small beauties remind us God sees every detail.",
            [
                ("Look! A tiny dot of light on a leaf.", "welcome"),
                ("I'm Dot the ladybug. Twinkle, twinkle!", "friend"),
                ("Pause with Elder Oak and breathe slowly.", "mentor"),
                ("Tap when you see something small and lovely.", "interactive"),
                ("Every little wonder is on purpose.", "lesson"),
                ("You are precious to God.", "celebrate"),
                ("See you soon, twinkle friend.", "farewell"),
            ],
        ),
        (
            "pebble_slow_river",
            "Pebble's Slow River",
            "Pebble",
            "Patience is a gift we can practice together.",
            [
                ("The river moves slow and steady.", "welcome"),
                ("I'm Pebble the turtle. One step at a time.", "friend"),
                ("Elder Oak says hurry is not always help.", "mentor"),
                ("Your grown-up can count to three with you.", "caregiver"),
                ("Waiting can be peaceful, not scary.", "lesson"),
                ("You did wonderful waiting.", "celebrate"),
                ("Slow waves goodbye.", "farewell"),
            ],
        ),
        (
            "lumi_gentle_glow",
            "Lumi's Gentle Glow",
            "Lumi",
            "Even a small light pushes back the dark.",
            [
                ("When the meadow grows dim, a glow appears.", "welcome"),
                ("I'm Lumi the firefly. I shine gently.", "friend"),
                ("Elder Oak says light and love never run out.", "mentor"),
                ("Clap softly when Lumi glows.", "play"),
                ("Jesus is the light that never leaves us.", "lesson"),
                ("Your smile glows too.", "celebrate"),
                ("Goodnight, glowing friend.", "farewell"),
            ],
        ),
        (
            "coco_splash_joy",
            "Coco's Splash Joy",
            "Coco",
            "Simple joys are gifts to thank God for.",
            [
                ("Splash! Coco found a puddle to play in.", "welcome"),
                ("I'm Coco the duckling. Quack with joy!", "friend"),
                ("Elder Oak laughs with the rain.", "mentor"),
                ("Splash your hands gently with your grown-up.", "play"),
                ("Thank You, God, for water and giggles.", "lesson"),
                ("Joy bubbles up when we share.", "share"),
                ("Bye-bye, splashy friend!", "farewell"),
            ],
        ),
        (
            "nuzzle_soft_hum",
            "Nuzzle's Soft Hum",
            "Nuzzle",
            "Gentle rhythms remind us God holds us close.",
            [
                ("Shhh. Nuzzle found a quiet corner.", "welcome"),
                ("I'm Nuzzle the lamb. Hum with me.", "friend"),
                ("Elder Oak sways a slow lullaby.", "mentor"),
                ("Your grown-up can hum a soft tune.", "caregiver"),
                ("God's love is steady like a heartbeat.", "lesson"),
                ("Rest your eyes. You are safe.", "rest"),
                ("Sweet dreams, humming friend.", "farewell"),
            ],
        ),
    ],
    "toddler": [
        (
            "maple_acorn_share",
            "Maple's Acorn Share",
            "Maple",
            "Giving something away can grow friendship.",
            [
                ("Maple found shiny acorns under Elder Oak.", "welcome"),
                ("I'm Maple the squirrel. Want one?", "friend"),
                ("Sharing means both friends can smile.", "lesson"),
                ("One for you, one for me. Thank you!", "share"),
                ("Elder Oak says generous hearts grow tall.", "mentor"),
                ("Tap SHARE when you give.", "interactive"),
                ("See you in the treetops!", "farewell"),
            ],
        ),
        (
            "sunny_pollen_parade",
            "Sunny's Pollen Parade",
            "Sunny",
            "We each have work that helps the whole garden.",
            [
                ("Buzz! Sunny leads a pollen parade.", "welcome"),
                ("I'm Sunny the bee. Follow the happy hum!", "friend"),
                ("Every job in God's garden matters.", "lesson"),
                ("March your feet to the beat.", "play"),
                ("Elder Oak waves from the hive tree.", "mentor"),
                ("You helped the flowers today!", "celebrate"),
                ("Buzz-bye, parade friend!", "farewell"),
            ],
        ),
        (
            "petal_color_dance",
            "Petal's Color Dance",
            "Petal",
            "God made colors to celebrate life.",
            [
                ("Petal flutters through rainbow petals.", "welcome"),
                ("I'm Petal the butterfly. Dance with me!", "friend"),
                ("Red, yellow, blue  all on purpose.", "lesson"),
                ("Spin when you hear your favorite color.", "interactive"),
                ("Elder Oak loves every hue you are.", "mentor"),
                ("Beautiful dancing, friend!", "celebrate"),
                ("Float away until next time.", "farewell"),
            ],
        ),
        (
            "brook_splash_share",
            "Brook's Splash Share",
            "Brook",
            "Kindness at the stream ripples outward.",
            [
                ("Brook splashes cool water for friends.", "welcome"),
                ("I'm Brook the otter. Splash and share!", "friend"),
                ("When we help, joy multiplies.", "lesson"),
                ("Offer a turn. There is room for you.", "include"),
                ("Elder Oak says gentle hands matter.", "mentor"),
                ("You shared like a superstar!", "celebrate"),
                ("See you by the stream!", "farewell"),
            ],
        ),
        (
            "hazel_hide_seek",
            "Hazel's Hide and Seek",
            "Hazel",
            "Being found means you are loved.",
            [
                ("One, two, three  hide with Hazel!", "welcome"),
                ("I'm Hazel the hedgehog. Peek-a-boo!", "friend"),
                ("Your grown-up can seek you gently.", "caregiver"),
                ("Found you! Hugs are always okay.", "play"),
                ("God sees you even when you hide.", "lesson"),
                ("Elder Oak giggles in the leaves.", "mentor"),
                ("Bye-bye, hiding friend!", "farewell"),
            ],
        ),
        (
            "sprout_rain_boots",
            "Sprout's Rain Boots",
            "Sprout",
            "Joyful play in hard weather builds resilience.",
            [
                ("Rain drops! Sprout pulls on bright boots.", "welcome"),
                ("I'm Sprout the frog. Splish, splash!", "friend"),
                ("Puddles are for jumping, not hiding.", "lesson"),
                ("Jump when you hear SPLASH!", "play"),
                ("Elder Oak laughs under the rain hat.", "mentor"),
                ("You turned a gray day bright.", "celebrate"),
                ("Boot stomp goodbye!", "farewell"),
            ],
        ),
    ],
    "child": [
        (
            "river_dam_teamwork",
            "River's Dam Teamwork",
            "River",
            "Working together honors how God made community.",
            [
                ("River is building a dam with friends.", "welcome"),
                ("I'm River the beaver. Teamwork time!", "friend"),
                ("Many hands make light work.", "lesson"),
                ("Tap HELP when someone needs you.", "interactive"),
                ("Elder Oak says serve one another.", "mentor"),
                ("You built something good today.", "celebrate"),
                ("Dam friends forever!", "farewell"),
            ],
        ),
        (
            "sky_truth_treetop",
            "Sky's Truth Treetop",
            "Sky",
            "Truth spoken kindly builds trust.",
            [
                ("Sky perches high to see the whole meadow.", "welcome"),
                ("I'm Sky the blue jay. Honest words help.", "friend"),
                ("Tell the truth with a gentle heart.", "lesson"),
                ("I'm sorry. Let's try again.", "repair"),
                ("Elder Oak listens before judging.", "mentor"),
                ("Brave truth-telling today!", "celebrate"),
                ("Fly safe, honest friend.", "farewell"),
            ],
        ),
        (
            "clover_meadow_invite",
            "Clover's Meadow Invite",
            "Clover",
            "Including others reflects God's welcome.",
            [
                ("Clover spots a friend alone on the edge.", "welcome"),
                ("I'm Clover the deer. Come play with us!", "friend"),
                ("There is always room for one more.", "include"),
                ("Kind invites change someone's day.", "lesson"),
                ("Elder Oak opens wide branches.", "mentor"),
                ("You made someone feel seen.", "celebrate"),
                ("Meadow friends, see you soon!", "farewell"),
            ],
        ),
        (
            "flint_night_courage",
            "Flint's Night Courage",
            "Flint",
            "Courage means trying even when we feel unsure.",
            [
                ("The trail grows dark. Flint stays calm.", "welcome"),
                ("I'm Flint the owl. Breathe with me.", "friend"),
                ("Fear is real. You can still be brave.", "lesson"),
                ("Hold your grown-up's hand if you want.", "caregiver"),
                ("God is with you in the dark and light.", "mentor"),
                ("You were courageous tonight.", "celebrate"),
                ("Hoot-goodnight, brave friend.", "farewell"),
            ],
        ),
        (
            "briar_bridge_help",
            "Briar's Bridge Help",
            "Briar",
            "Helping across a gap is love in action.",
            [
                ("A stream blocks the path. Briar has a plan.", "welcome"),
                ("I'm Briar the rabbit. Let's build a bridge.", "friend"),
                ("HELP can be a bridge for someone.", "interactive"),
                ("Small acts carry big love.", "lesson"),
                ("Elder Oak steadies the boards.", "mentor"),
                ("Bridge builders win today!", "celebrate"),
                ("Hop home, helper friend.", "farewell"),
            ],
        ),
        (
            "thistle_trail_markers",
            "Thistle's Trail Markers",
            "Thistle",
            "Leaving kind markers helps others find their way.",
            [
                ("Thistle marks a winding forest trail.", "welcome"),
                ("I'm Thistle the fox. Follow the kind signs.", "friend"),
                ("Small markers can guide big journeys.", "lesson"),
                ("Tap MARK when you spot a trail sign.", "interactive"),
                ("Elder Oak says help others find the path.", "mentor"),
                ("You guided a friend today.", "celebrate"),
                ("Trail marker goodbye!", "farewell"),
            ],
        ),
    ],
    "tween": [
        (
            "ash_honest_echo",
            "Ash's Honest Echo",
            "Ash",
            "What we repeat online should be true and kind.",
            [
                ("Ash hears an echo that isn't quite true.", "welcome"),
                ("I'm Ash the raccoon. Let's check the facts.", "friend"),
                ("Words bounce farther than we think.", "lesson"),
                ("Pause before you pass a story along.", "interactive"),
                ("Elder Oak says wisdom listens first.", "mentor"),
                ("You chose honesty today.", "celebrate"),
                ("Echo goodbye, truth friend.", "farewell"),
            ],
        ),
        (
            "pike_listen_lake",
            "Pike's Listen Lake",
            "Pike",
            "Listening well is a superpower.",
            [
                ("Pike stands still at the quiet lake.", "welcome"),
                ("I'm Pike the heron. Listen with me.", "friend"),
                ("Everyone deserves to be heard.", "lesson"),
                ("Repeat back what you heard.", "interactive"),
                ("Elder Oak models patient ears.", "mentor"),
                ("Great listening, friend.", "celebrate"),
                ("Still waters goodbye.", "farewell"),
            ],
        ),
        (
            "juniper_trail_choice",
            "Juniper's Trail Choice",
            "Juniper",
            "Choices show who we are becoming.",
            [
                ("Two trails fork. Juniper pauses.", "welcome"),
                ("I'm Juniper the fox. Choose with care.", "friend"),
                ("The kind path is not always easy.", "lesson"),
                ("You can say no without being cruel.", "repair"),
                ("Elder Oak trusts your growing heart.", "mentor"),
                ("Integrity looks good on you.", "celebrate"),
                ("Trail friends until next time.", "farewell"),
            ],
        ),
        (
            "ridge_team_patience",
            "Ridge's Team Patience",
            "Ridge",
            "Teams win when patience meets practice.",
            [
                ("Ridge coaches friends through a tough game.", "welcome"),
                ("I'm Ridge the hawk. We learn together.", "friend"),
                ("Patience is strength, not weakness.", "lesson"),
                ("Cheer for tries, not only wins.", "include"),
                ("Elder Oak says growth takes seasons.", "mentor"),
                ("Team patience champion!", "celebrate"),
                ("Soar on, teammate.", "farewell"),
            ],
        ),
        (
            "willow_wind_apology",
            "Willow's Wind Apology",
            "Willow",
            "A real apology heals friendships.",
            [
                ("Wind rattles branches. Feelings got hurt.", "welcome"),
                ("I'm Willow the deer. Let's repair this.", "friend"),
                ("I'm sorry. I hear you. How can I help?", "repair"),
                ("Forgiveness is a journey, not a race.", "lesson"),
                ("Elder Oak makes space for both voices.", "mentor"),
                ("You mended something important.", "celebrate"),
                ("Gentle goodbye, healing friend.", "farewell"),
            ],
        ),
        (
            "lane_crosswalk_care",
            "Lane's Crosswalk Care",
            "Lane",
            "Looking out for others is leadership in action.",
            [
                ("Lane waits at a busy crosswalk.", "welcome"),
                ("I'm Lane the deer. We go together.", "friend"),
                ("Notice who needs an extra pause.", "lesson"),
                ("Offer your arm. Slow is okay.", "include"),
                ("Elder Oak says care slows us down on purpose.", "mentor"),
                ("You led with kindness today.", "celebrate"),
                ("Safe crossing, care friend.", "farewell"),
            ],
        ),
    ],
    "teen": [
        (
            "atlas_road_integrity",
            "Atlas's Road Integrity",
            "Atlas",
            "Integrity means matching actions to values.",
            [
                ("Atlas faces a shortcut that isn't fair.", "welcome"),
                ("I'm Atlas the wolf. Walk the right road.", "friend"),
                ("Character shows when no one is watching.", "lesson"),
                ("You can stand alone and still be kind.", "mentor"),
                ("Elder Oak walked hard paths too.", "mentor"),
                ("Integrity is courage in quiet moments.", "celebrate"),
                ("Road friends, until next crossing.", "farewell"),
            ],
        ),
        (
            "nova_signal_truth",
            "Nova's Signal Truth",
            "Nova",
            "Truth protects people we care about.",
            [
                ("Nova spots rumors spreading fast.", "welcome"),
                ("I'm Nova the raven. Signal truth clearly.", "friend"),
                ("Speak up with facts and compassion.", "lesson"),
                ("Silence can hurt when truth is needed.", "interactive"),
                ("Elder Oak says love and truth belong together.", "mentor"),
                ("You protected someone today.", "celebrate"),
                ("Fly true, signal friend.", "farewell"),
            ],
        ),
        (
            "ember_stand_kind",
            "Ember's Stand Kind",
            "Ember",
            "Standing up can still be gentle.",
            [
                ("Someone is left out at the crossroads.", "welcome"),
                ("I'm Ember the fox. Stand with them.", "friend"),
                ("Courage and kindness are teammates.", "lesson"),
                ("Invite. Include. Interrupt cruelty.", "include"),
                ("Elder Oak opens the circle wider.", "mentor"),
                ("You changed the room today.", "celebrate"),
                ("Warm goodbye, brave friend.", "farewell"),
            ],
        ),
        (
            "harbor_anchor_peace",
            "Harbor's Anchor Peace",
            "Harbor",
            "Peace is a practice we can choose daily.",
            [
                ("Waves churn. Harbor breathes slow.", "welcome"),
                ("I'm Harbor the seal. Anchor in calm.", "friend"),
                ("You cannot control every storm.", "lesson"),
                ("Breathe in hope. Breathe out fear.", "rest"),
                ("God's peace guards hearts and minds.", "mentor"),
                ("You found calm in the chaos.", "celebrate"),
                ("Drift peaceful, anchor friend.", "farewell"),
            ],
        ),
        (
            "summit_service_path",
            "Summit's Service Path",
            "Summit",
            "Service turns gratitude into action.",
            [
                ("Summit sees a need on the high path.", "welcome"),
                ("I'm Summit the eagle. Serve with joy.", "friend"),
                ("Use your strengths for others.", "lesson"),
                ("Small service moves mountains.", "interactive"),
                ("Elder Oak served the meadow for years.", "mentor"),
                ("Grateful service looks like love.", "celebrate"),
                ("Soar onward, servant friend.", "farewell"),
            ],
        ),
        (
            "cipher_digital_pause",
            "Cipher's Digital Pause",
            "Cipher",
            "Pausing before posting protects people and peace.",
            [
                ("Cipher sees a heated thread growing fast.", "welcome"),
                ("I'm Cipher the owl. Pause before you post.", "friend"),
                ("Words online travel farther than we think.", "lesson"),
                ("Breathe. Reread. Choose kindness.", "interactive"),
                ("Elder Oak says wisdom waits one beat.", "mentor"),
                ("You chose peace over speed.", "celebrate"),
                ("Log off with grace, pause friend.", "farewell"),
            ],
        ),
    ],
    "adult": [
        (
            "dawn_gratitude_table",
            "Dawn's Gratitude Table",
            "Dawn",
            "Gratitude turns ordinary mornings into gifts.",
            [
                ("Dawn sets a simple table at sunrise.", "welcome"),
                ("I'm Dawn the songbird. Name three mercies.", "friend"),
                ("Thankfulness rewires a weary heart.", "lesson"),
                ("Even hard days hold small gifts.", "mentor"),
                ("Your voice, however you speak, matters.", "lesson"),
                ("Share thanks with someone today.", "share"),
                ("Morning blessing until tomorrow.", "farewell"),
            ],
        ),
        (
            "cedar_legacy_give",
            "Cedar's Legacy Give",
            "Cedar",
            "What we give outlives what we keep.",
            [
                ("Cedar tends seedlings for the next generation.", "welcome"),
                ("I'm Cedar the stag. Plant for tomorrow.", "friend"),
                ("Legacy is love passed forward.", "lesson"),
                ("Mentor someone younger today.", "interactive"),
                ("Elder Oak remembers every planter.", "mentor"),
                ("Your generosity roots deep.", "celebrate"),
                ("Steady goodbye, legacy friend.", "farewell"),
            ],
        ),
        (
            "meadow_mercy_return",
            "Meadow's Mercy Return",
            "Meadow",
            "Mercy restores what shame tries to steal.",
            [
                ("A friend returns after a hard season.", "welcome"),
                ("I'm Meadow the sheep. Welcome them home.", "friend"),
                ("Forgiveness is freedom for both sides.", "lesson"),
                ("I'm glad you're here. Let's begin again.", "repair"),
                ("Elder Oak kept a place at the table.", "mentor"),
                ("Mercy multiplies hope.", "celebrate"),
                ("Gentle farewell, mercy friend.", "farewell"),
            ],
        ),
        (
            "harbor_hope_ripple",
            "Harbor's Hope Ripple",
            "Harbor",
            "Hope shared becomes hope multiplied.",
            [
                ("Harbor sends encouragement across the water.", "welcome"),
                ("I'm Harbor the dolphin. Ripple hope outward.", "friend"),
                ("One kind message can change a week.", "lesson"),
                ("Text, call, or pray for someone.", "interactive"),
                ("God uses ordinary hands as lifelines.", "mentor"),
                ("You started a hope ripple.", "celebrate"),
                ("Wave goodbye, hope bearer.", "farewell"),
            ],
        ),
        (
            "stone_steadfast_prayer",
            "Stone's Steadfast Prayer",
            "Stone",
            "Steadfast prayer anchors busy lives.",
            [
                ("Stone stands still while the world rushes.", "welcome"),
                ("I'm Stone the crane. Pause and pray.", "friend"),
                ("Bring worries to God in honest words.", "lesson"),
                ("Rest is not laziness. It is trust.", "rest"),
                ("Elder Oak has prayed through every season.", "mentor"),
                ("Steadfast heart, well done.", "celebrate"),
                ("Peaceful goodbye, prayer friend.", "farewell"),
            ],
        ),
        (
            "root_deep_gratitude",
            "Root's Deep Gratitude",
            "Root",
            "Gratitude rooted deep sustains us through every season.",
            [
                ("Root kneels by old roots at dusk.", "welcome"),
                ("I'm Root the badger. Name what held you today.", "friend"),
                ("Gratitude is not denial. It is strength.", "lesson"),
                ("Write one mercy before sleep.", "interactive"),
                ("Elder Oak remembers every planter's hands.", "mentor"),
                ("Your thankful heart roots deep.", "celebrate"),
                ("Rest well, grateful friend.", "farewell"),
            ],
        ),
    ],
}


def write_script(path: Path, band: str, ep: dict, caly_name: str, duration: int, scenes: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# {ep['title']} ({band}, ~{duration // 60} min, {scenes} scenes)",
        "",
        "**Series:** Caly and Friends  ",
        f"**Band:** {band.title()} ({caly_name})  ",
        f"**Friend:** {ep['friend']}  ",
        "**Mentor:** Elder Oak  ",
        f"**Christian lesson:** {ep['lesson']}",
        "",
        "## Story arc",
        "",
        f"Caly and {ep['friend']} explore an age-appropriate adventure with Elder Oak. "
        "Caregiver co-play cues invite modeling, assent, and celebration.",
        "",
        "## Key beats",
        "",
        "| # | Tag | Narration |",
        "|---|-----|-----------|",
    ]
    for i, (caption, tag) in enumerate(ep["beats"], 1):
        lines.append(f"| {i} | {tag} | {caption} |")
    lines.extend(["", "Not medical advice. Original Calyndra characters only.", ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    existing_ids = {e["id"] for e in catalog["episodes"]}
    beats_all: dict[str, list[list[str]]] = {}

    if BEATS_OUT.is_file():
        beats_all = json.loads(BEATS_OUT.read_text(encoding="utf-8"))

    script_num = 12
    added = 0
    for band, episodes in NEW_EPISODES.items():
        _art, caly_name, duration, scenes = BAND_META[band]
        for suffix, title, friend, lesson, beat_list in episodes:
            ep_id = f"{suffix}_long"
            if ep_id in existing_ids:
                continue
            ep = {
                "id": ep_id,
                "band": band,
                "title": title,
                "friend": friend,
                "mentor": "Elder Oak",
                "targetDurationSec": duration,
                "targetSceneCount": scenes,
                "script": f"videos/scripts/{script_num:02d}-{suffix.replace('_', '-')}.md",
                "webm": f"{ep_id}.webm",
                "lesson": lesson,
                "pilot": False,
                "status": "script-only",
            }
            ep["beats"] = beat_list
            catalog["episodes"].append(ep)
            beats_all[ep_id] = [[c, t] for c, t in beat_list]
            write_script(ROOT / ep["script"], band, ep, caly_name, duration, scenes)
            existing_ids.add(ep_id)
            script_num += 1
            added += 1

    catalog["lockedUtc"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    CATALOG.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    BEATS_OUT.write_text(json.dumps(beats_all, indent=2) + "\n", encoding="utf-8")
    print(f"Added {added} episodes ({len(catalog['episodes'])} total)")
    print(f"Wrote {BEATS_OUT.name}")


if __name__ == "__main__":
    main()
