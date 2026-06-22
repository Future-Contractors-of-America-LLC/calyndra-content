#!/usr/bin/env python3
"""Build age-band vocabulary JSON with growing word counts and phrase lists."""

from __future__ import annotations

import json
import shutil
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_CONTENT = ROOT.parent / "calyndra-app" / "content"
VOCAB = ROOT / "vocabulary"

BAND_DIR = {
    "toddler": "sprout",
    "child": "bud",
    "tween": "sprig",
    "teen": "vine",
    "adult": "bloom",
    "caregiver": "canopy",
}

PHRASES = {
    "toddler": [
        {"id": "more-please", "label": "more please", "category": "core", "speakText": "More please!"},
        {"id": "all-done", "label": "all done", "category": "core", "speakText": "All done!"},
        {"id": "help-me", "label": "help me", "category": "core", "speakText": "Help me!"},
        {"id": "my-turn", "label": "my turn", "category": "social", "speakText": "My turn!"},
        {"id": "go-play", "label": "go play", "category": "activities", "speakText": "Go play!"},
        {"id": "want-that", "label": "I want that", "category": "core", "speakText": "I want that!"},
        {"id": "need-help", "label": "I need help", "category": "core", "speakText": "I need help!"},
        {"id": "look-at", "label": "look at this", "category": "core", "speakText": "Look at this!"},
        {"id": "come-here", "label": "come here", "category": "social", "speakText": "Come here!"},
        {"id": "love-you", "label": "love you", "category": "social", "speakText": "Love you!"},
        {"id": "yucky", "label": "no thank you", "category": "core", "speakText": "No thank you."},
        {"id": "bathroom-please", "label": "bathroom please", "category": "routine", "speakText": "Bathroom please!"},
    ],
    "child": [
        {"id": "can-i-have", "label": "Can I have more?", "category": "core", "speakText": "Can I have more?"},
        {"id": "need-break", "label": "I need a break", "category": "regulation", "speakText": "I need a break."},
        {"id": "thank-you", "label": "Thank you", "category": "social", "speakText": "Thank you!"},
        {"id": "please-help", "label": "Please help me", "category": "core", "speakText": "Please help me."},
        {"id": "where-is", "label": "Where is it?", "category": "questions", "speakText": "Where is it?"},
        {"id": "dont-like", "label": "I don't like that", "category": "preferences", "speakText": "I don't like that."},
        {"id": "my-turn-phrase", "label": "It's my turn", "category": "social", "speakText": "It's my turn!"},
        {"id": "share-please", "label": "Can we share?", "category": "social", "speakText": "Can we share?"},
        {"id": "feel-happy", "label": "I feel happy", "category": "feelings", "speakText": "I feel happy!"},
        {"id": "feel-sad", "label": "I feel sad", "category": "feelings", "speakText": "I feel sad."},
        {"id": "too-loud", "label": "It's too loud", "category": "regulation", "speakText": "It's too loud."},
        {"id": "wait-please", "label": "Wait please", "category": "core", "speakText": "Wait please."},
        {"id": "lets-play", "label": "Let's play", "category": "activities", "speakText": "Let's play!"},
        {"id": "read-book", "label": "Read a book", "category": "activities", "speakText": "Read a book!"},
        {"id": "go-home", "label": "I want to go home", "category": "places", "speakText": "I want to go home."},
    ],
    "tween": [
        {"id": "dont-understand", "label": "I don't understand", "category": "core", "speakText": "I don't understand."},
        {"id": "say-again", "label": "Can you say that again?", "category": "core", "speakText": "Can you say that again?"},
        {"id": "need-space", "label": "I need space", "category": "regulation", "speakText": "I need space."},
        {"id": "not-ready", "label": "I'm not ready yet", "category": "core", "speakText": "I'm not ready yet."},
        {"id": "pick-different", "label": "Can we pick something else?", "category": "preferences", "speakText": "Can we pick something else?"},
        {"id": "feel-overwhelmed", "label": "I feel overwhelmed", "category": "feelings", "speakText": "I feel overwhelmed."},
        {"id": "can-we-talk", "label": "Can we talk about it?", "category": "social", "speakText": "Can we talk about it?"},
        {"id": "homework-help", "label": "I need help with homework", "category": "school", "speakText": "I need help with homework."},
        {"id": "join-game", "label": "Can I join the game?", "category": "social", "speakText": "Can I join the game?"},
        {"id": "pass-turn", "label": "I'll pass this turn", "category": "social", "speakText": "I'll pass this turn."},
        {"id": "schedule-change", "label": "The schedule changed", "category": "routine", "speakText": "The schedule changed."},
        {"id": "need-quiet", "label": "I need a quiet place", "category": "regulation", "speakText": "I need a quiet place."},
    ],
    "teen": [
        {"id": "moment-respond", "label": "I need a moment to respond", "category": "core", "speakText": "I need a moment to respond."},
        {"id": "not-comfortable", "label": "I'm not comfortable with that", "category": "boundaries", "speakText": "I'm not comfortable with that."},
        {"id": "repeat-slower", "label": "Can you repeat that slower?", "category": "core", "speakText": "Can you repeat that slower?"},
        {"id": "clarify", "label": "Can you clarify?", "category": "core", "speakText": "Can you clarify?"},
        {"id": "privacy", "label": "I need privacy", "category": "boundaries", "speakText": "I need privacy."},
        {"id": "consent-no", "label": "I don't consent to that", "category": "boundaries", "speakText": "I don't consent to that."},
        {"id": "running-late", "label": "I'm running late", "category": "functional", "speakText": "I'm running late."},
        {"id": "cancel-plans", "label": "I need to cancel", "category": "functional", "speakText": "I need to cancel."},
        {"id": "feel-anxious", "label": "I feel anxious", "category": "feelings", "speakText": "I feel anxious."},
        {"id": "talk-later", "label": "Can we talk later?", "category": "social", "speakText": "Can we talk later?"},
        {"id": "need-doctor", "label": "I need to see a doctor", "category": "health", "speakText": "I need to see a doctor."},
        {"id": "order-food", "label": "I'd like to order food", "category": "functional", "speakText": "I'd like to order food."},
    ],
    "adult": [
        {"id": "schedule-meeting", "label": "I'd like to schedule a meeting", "category": "work", "speakText": "I'd like to schedule a meeting."},
        {"id": "need-clarification", "label": "I need clarification", "category": "work", "speakText": "I need clarification."},
        {"id": "follow-up", "label": "I will follow up by email", "category": "work", "speakText": "I will follow up by email."},
        {"id": "running-late-adult", "label": "I'm running late for work", "category": "work", "speakText": "I'm running late for work."},
        {"id": "need-accommodation", "label": "I need an accommodation", "category": "work", "speakText": "I need an accommodation."},
        {"id": "pay-bill", "label": "I need to pay a bill", "category": "functional", "speakText": "I need to pay a bill."},
        {"id": "make-appointment", "label": "I need to make an appointment", "category": "health", "speakText": "I need to make an appointment."},
        {"id": "transport-help", "label": "I need help with transport", "category": "functional", "speakText": "I need help with transport."},
        {"id": "allergy", "label": "I have a food allergy", "category": "health", "speakText": "I have a food allergy."},
        {"id": "repeat-email", "label": "Please repeat that in writing", "category": "core", "speakText": "Please repeat that in writing."},
    ],
    "caregiver": [
        {"id": "model-word", "label": "Let's model this word", "category": "coaching", "speakText": "Let's model this word together."},
        {"id": "take-time", "label": "Take your time", "category": "coaching", "speakText": "Take your time. I'm listening."},
        {"id": "good-try", "label": "Good try!", "category": "coaching", "speakText": "Good try! That counts."},
        {"id": "your-choice", "label": "Your choice matters", "category": "coaching", "speakText": "Your choice matters."},
        {"id": "we-can-wait", "label": "We can wait", "category": "coaching", "speakText": "We can wait. No rush."},
        {"id": "want-break", "label": "Do you want a break?", "category": "coaching", "speakText": "Do you want a break?"},
        {"id": "show-me", "label": "Show me how you feel", "category": "coaching", "speakText": "Show me how you feel."},
        {"id": "i-see-you", "label": "I see you trying", "category": "coaching", "speakText": "I see you trying."},
        {"id": "not-emergency", "label": "This is support, not emergency care", "category": "boundary", "speakText": "This is support, not emergency care."},
        {"id": "assent-first", "label": "We follow assent first", "category": "coaching", "speakText": "We follow assent first."},
    ],
}

# Child subset: toddler + early school/social (target ~72)
CHILD_EXTRA_IDS = [
    "mad", "scared", "tired", "sick", "school", "read", "draw", "music", "outside",
    "friend", "family", "share", "turn", "please", "thank-you", "sorry", "break",
    "quiet", "loud", "like", "dont-like", "want", "need", "where", "what",
]

# Tween adds questions + tech + activities from child-expanded
TWEEN_EXTRA_IDS = [
    "who", "when", "why", "different", "same", "finished", "water", "computer",
    "phone", "park", "walk", "run", "swim", "dance", "sing", "write", "think",
    "try", "team", "together", "fast", "slow", "morning", "night", "today",
]

# Teen adds functional from teen-adult file
# Adult adds work/money/meeting from child-expanded tail


def load_json(name: str) -> dict:
    path = APP_CONTENT / name
    if not path.exists():
        path = VOCAB / name
    return json.loads(path.read_text(encoding="utf-8"))


def sym_map(symbols: list) -> dict[str, dict]:
    return {s["id"]: deepcopy(s) for s in symbols}


def band_asset(sym: dict, band: str) -> dict:
    s = deepcopy(sym)
    d = BAND_DIR[band]
    s["imageAsset"] = f"assets/symbols/{d}/{s['id']}.png"
    return s


def pick_symbols(source: dict[str, dict], ids: list[str], band: str) -> list[dict]:
    out = []
    for i in ids:
        if i in source:
            out.append(band_asset(source[i], band))
    return out


def merge_unique(*id_lists: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for lst in id_lists:
        for i in lst:
            if i not in seen:
                seen.add(i)
                out.append(i)
    return out


def build_sets() -> dict[str, dict]:
    toddler_data = load_json("toddler-core.json")
    child_data = load_json("child-expanded.json")
    teen_data = load_json("teen-adult-functional.json")

    toddler_map = sym_map(toddler_data["symbols"])
    child_map = sym_map(child_data["symbols"])
    teen_map = sym_map(teen_data["symbols"])

    toddler_ids = [s["id"] for s in toddler_data["symbols"]]
    child_ids = merge_unique(toddler_ids, CHILD_EXTRA_IDS)
    tween_ids = merge_unique(child_ids, TWEEN_EXTRA_IDS, [s["id"] for s in child_data["symbols"] if s["id"] not in child_ids])
    teen_ids = merge_unique(tween_ids, [s["id"] for s in teen_data["symbols"]])
    adult_extra = [
        "work", "email", "meeting", "schedule", "calendar", "money", "pay", "buy",
        "job", "store", "doctor", "nurse", "message", "call", "video", "map",
        "sell", "tomorrow", "yesterday", "directions", "left", "right", "forward",
        "backward", "grocery", "restaurant", "order", "allergy", "grandma", "grandpa",
    ]
    adult_ids = merge_unique(teen_ids, [i for i in adult_extra if i in child_map or i in teen_map])

    all_source = {**toddler_map, **child_map, **teen_map}

    caregiver_ids = merge_unique(
        toddler_ids[:20],
        ["break", "wait", "please", "thank-you", "share", "listen", "quiet"],
    )

    return {
        "toddler": {
            "id": "toddler-core",
            "title": "Toddler Core (2-4)",
            "description": "53 core words + 12 short phrases for Caly Sprout.",
            "ageBand": "toddler",
            "nickname": "Sprout",
            "symbols": pick_symbols(all_source, toddler_ids, "toddler"),
            "phrases": PHRASES["toddler"],
        },
        "child": {
            "id": "child-vocab",
            "title": "Child Vocabulary (5-8)",
            "description": f"{len(child_ids)} words + phrases for Caly Bud - builds on toddler core.",
            "ageBand": "child",
            "nickname": "Bud",
            "symbols": pick_symbols(all_source, child_ids, "child"),
            "phrases": PHRASES["child"],
        },
        "tween": {
            "id": "tween-vocab",
            "title": "Tween Vocabulary (9-12)",
            "description": f"{len(tween_ids)} words + phrases for Caly Sprig - questions, school, and social growth.",
            "ageBand": "tween",
            "nickname": "Sprig",
            "symbols": pick_symbols(all_source, tween_ids, "tween"),
            "phrases": PHRASES["tween"],
        },
        "teen": {
            "id": "teen-vocab",
            "title": "Teen Vocabulary (13-17)",
            "description": f"{len(teen_ids)} words + phrases for Caly Vine - autonomy, health, and boundaries.",
            "ageBand": "teen",
            "nickname": "Vine",
            "symbols": pick_symbols(all_source, teen_ids, "teen"),
            "phrases": PHRASES["teen"],
        },
        "adult": {
            "id": "adult-vocab",
            "title": "Adult Vocabulary (18+)",
            "description": f"{len(adult_ids)} words + phrases for Caly Bloom - work, health, and daily living.",
            "ageBand": "adult",
            "nickname": "Bloom",
            "symbols": pick_symbols(all_source, adult_ids, "adult"),
            "phrases": PHRASES["adult"],
        },
        "caregiver": {
            "id": "caregiver-vocab",
            "title": "Caregiver Modeling",
            "description": f"{len(caregiver_ids)} model words + coaching phrases for Caly Canopy.",
            "ageBand": "caregiver",
            "nickname": "Canopy",
            "symbols": pick_symbols(all_source, caregiver_ids, "caregiver"),
            "phrases": PHRASES["caregiver"],
        },
    }


def write_outputs(sets: dict[str, dict]) -> None:
    file_map = {
        "toddler": "toddler-core.json",
        "child": "child-vocab.json",
        "tween": "tween-vocab.json",
        "teen": "teen-vocab.json",
        "adult": "adult-vocab.json",
        "caregiver": "caregiver-vocab.json",
    }
    for band, data in sets.items():
        name = file_map[band]
        text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
        (VOCAB / name).write_text(text, encoding="utf-8")
        (APP_CONTENT / name).write_text(text, encoding="utf-8")
        print(
            f"{name}: {len(data['symbols'])} symbols, {len(data['phrases'])} phrases"
        )


def main() -> None:
    sets = build_sets()
    write_outputs(sets)


if __name__ == "__main__":
    main()
