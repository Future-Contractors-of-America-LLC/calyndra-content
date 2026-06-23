#!/usr/bin/env python3
"""Expand caly-voice-scripts.json with baby, tween, category, and new game keys."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VOICE = ROOT / "games" / "caly-voice-scripts.json"

# Base keys shared structure - audience-specific text
NEW_KEYS = {
    "category_intro": {
        "baby": "Which group? Soft and calm!",
        "toddler": "Category quest! Which group does it belong to?",
        "child": "Category challenge! Sort the symbol!",
        "tween": "Category sort - which group fits?",
        "teen": "Which category fits this symbol?",
        "adult": "Select the matching category.",
        "caregiver": "Model category sorting - celebrate tries.",
    },
    "category_prompt": {
        "baby": "Soft group for {word}?",
        "toddler": "What group is {word} in?",
        "child": "Which category is {word}?",
        "tween": "Category for {word}?",
        "teen": "Category of {word}?",
        "adult": "Category: {word}.",
        "caregiver": "Name the category for {word} together.",
    },
    "kindness_chain_intro": {
        "baby": "Kind words, soft and warm! Tap with Caly Seed!",
        "toddler": "Kindness chain! Link kind words with Sprout!",
        "child": "Kindness chain! Build kind choices with Bud!",
        "tween": "Kindness chain - patience and care with Sprig.",
        "teen": "Kindness chain. Kind words, your pace.",
        "adult": "Kindness chain - link supportive symbols.",
        "caregiver": "Kindness chain preview - model, don't test.",
    },
    "kindness_chain_prompt": {
        "baby": "Tap kind {word}! Soft and sweet!",
        "toddler": "Next kind word: {word}! Share the kindness!",
        "child": "Add {word} to the kindness chain!",
        "tween": "Kindness link: {word}.",
        "teen": "Kind word: {word}.",
        "adult": "Link {word} in the chain.",
        "caregiver": "Model {word} - celebrate the try.",
    },
    "word_garden_intro": {
        "baby": "Little garden! Grow soft words!",
        "toddler": "Word garden! Plant words with Sprout!",
        "child": "Word garden quest! Grow {word} seeds!",
        "tween": "Word garden - grow your vocabulary.",
        "teen": "Word garden. Plant the right symbol.",
        "adult": "Word garden - match and grow.",
        "caregiver": "Word garden - model planting words.",
    },
    "word_garden_prompt": {
        "baby": "Water {word}! Grow, grow!",
        "toddler": "Water the {word} seed! {word}!",
        "child": "Grow {word} in the garden!",
        "tween": "Plant {word} in your garden.",
        "teen": "Grow {word}.",
        "adult": "Select {word} to grow.",
        "caregiver": "Say {word} as you model the tap.",
    },
    "friend_find_intro": {
        "baby": "Peek peek! Find Caly friend!",
        "toddler": "Friend find! Where is Caly's friend?",
        "child": "Friend find quest! Spot the right symbol!",
        "tween": "Friend find - match Caly's clue.",
        "teen": "Find the symbol Caly describes.",
        "adult": "Locate the matching friend symbol.",
        "caregiver": "Friend find - joint attention practice.",
    },
    "friend_find_prompt": {
        "baby": "Find {word}! Peek peek!",
        "toddler": "Find friend {word}! {word}!",
        "child": "Which one is {word}? Find them!",
        "tween": "Find {word} among the choices.",
        "teen": "Locate {word}.",
        "adult": "Find {word}.",
        "caregiver": "Point to {word} together if helpful.",
    },
    "rhythm_words_intro": {
        "baby": "Pat pat! Soft beats with Caly!",
        "toddler": "Rhythm words! Clap and tap with Sprout!",
        "child": "Rhythm words! Tap on the beat!",
        "tween": "Rhythm words - tap when ready.",
        "teen": "Rhythm words. Your tempo.",
        "adult": "Rhythmic symbol practice.",
        "caregiver": "Rhythm words - clap and model.",
    },
    "rhythm_words_prompt": {
        "baby": "Pat {word}! Soft beat!",
        "toddler": "Tap {word} on the beat! {word}!",
        "child": "On the beat: {word}!",
        "tween": "Beat tap: {word}.",
        "teen": "Tap {word} on beat.",
        "adult": "Rhythm: {word}.",
        "caregiver": "Model {word} on the beat.",
    },
    "story_pick_intro": {
        "baby": "Tiny story! Pick what happens!",
        "toddler": "Story pick! What happens next, Sprout?",
        "child": "Story adventure! Pick the next part!",
        "tween": "Story pick - shape what happens next.",
        "teen": "Story pick. Choose the path.",
        "adult": "Story branch - select next beat.",
        "caregiver": "Story pick - model choices aloud.",
    },
    "story_pick_prompt": {
        "baby": "Pick {word}! Story grows!",
        "toddler": "Story goes to {word}! Pick {word}!",
        "child": "What if we pick {word}? Go!",
        "tween": "Story path: {word}.",
        "teen": "Next: {word}.",
        "adult": "Branch: {word}.",
        "caregiver": "Narrate choosing {word}.",
    },
    "gratitude_glow_intro": {
        "baby": "Thank you glow! Warm and bright!",
        "toddler": "Gratitude glow! Thankful words shine!",
        "child": "Gratitude glow! What are you thankful for?",
        "tween": "Gratitude glow - notice good things.",
        "teen": "Gratitude glow. Name what matters.",
        "adult": "Gratitude practice with symbols.",
        "caregiver": "Gratitude glow - model thankful words.",
    },
    "gratitude_glow_prompt": {
        "baby": "Glow for {word}! Thank you!",
        "toddler": "Thankful for {word}! {word} glows!",
        "child": "Grateful for {word}! Tap to glow!",
        "tween": "Grateful: {word}.",
        "teen": "Thankful for {word}.",
        "adult": "Gratitude: {word}.",
        "caregiver": "Say thankful for {word}.",
    },
    "consent_stop_intro": {
        "baby": "Pause pause! Gentle stop is okay!",
        "toddler": "Stop and go! Your body, your choice!",
        "child": "Consent stop! Pause anytime you need!",
        "tween": "Consent and stop - your boundaries count.",
        "teen": "Consent and stop. Pause is always okay.",
        "adult": "Boundary practice - stop and pause.",
        "caregiver": "Model assent and stop - assent-first.",
    },
    "consent_stop_prompt": {
        "baby": "Tap {word} for gentle pause!",
        "toddler": "Tap {word} when you need a break!",
        "child": "Need a pause? Tap {word}!",
        "tween": "Boundary word: {word}.",
        "teen": "Stop or pause: {word}.",
        "adult": "Select {word} to pause.",
        "caregiver": "Model {word} for pause and assent.",
    },
    "schedule_builder_intro": {
        "baby": "First then! Little steps!",
        "toddler": "Schedule time! First, then, done!",
        "child": "Build your schedule! Order the steps!",
        "tween": "Schedule builder - plan your steps.",
        "teen": "Schedule builder. Order at your pace.",
        "adult": "Routine ordering practice.",
        "caregiver": "Schedule builder - model first/then.",
    },
    "schedule_builder_prompt": {
        "baby": "Next step: {word}!",
        "toddler": "Then comes {word}! Tap {word}!",
        "child": "Put {word} next in the schedule!",
        "tween": "Next in order: {word}.",
        "teen": "Schedule step: {word}.",
        "adult": "Order: {word}.",
        "caregiver": "Model step {word} in sequence.",
    },
}

BABY_BASE = {
    "game_intro": "Hello, little one! I am Caly - call me Seed! Soft words and gentle play!",
    "tap_intro": "Soft tap! Listen for the word!",
    "tap_prompt": "Gentle tap! Find {word}! {word}!",
    "match_intro": "Soft match! Which is {word}?",
    "caly_says_intro": "Caly says! Listen softly, then tap!",
    "caly_says_listen": "Caly says: {word}! Soft and calm!",
    "parade_intro": "Slow parade! Watch the words float!",
    "bubble_intro": "Gentle bubbles! Pop the word bubble!",
    "bubble_prompt": "Pop {word}! Soft pop!",
    "peek_intro": "Peek-a-boo! Where is Caly Seed?",
    "peek_found": "Found me! Peek-a-boo! Hello!",
    "song_circle_intro": "Soft song circle! Pat along!",
    "song_circle_cue": "Happy tap! Tap HAPPY gently!",
    "correct": [
        "Soft yay! You did it!",
        "Gentle clap! Wonderful!",
        "Sweet try! So proud!",
    ],
    "try_again": [
        "Soft try! Look again!",
        "That's okay! Gentle skip!",
    ],
    "skip": "Skip skip! That's okay! Calm pause!",
    "streak_3": "Three gentle wins! So sweet!",
    "caregiver_cue": "Grown-ups: soft voice, no rush. Model calmly.",
}

TWEEN_BASE = {
    "game_intro": "Hey! Caly (Sprig) here. Word games at your pace - skip anytime.",
    "tap_intro": "Find the symbol on the board.",
    "tap_prompt": "Which picture is {word}?",
    "match_intro": "Match {word} to the picture.",
    "caly_says_intro": "Caly Says - listen, tap when ready.",
    "caly_says_listen": "Caly says: {word}.",
    "parade_intro": "Symbol parade - find the named word.",
    "bubble_intro": "Bubble pop - tap the word you hear.",
    "bubble_prompt": "Pop {word}.",
    "peek_intro": "Peek-a-Caly - find where I'm hiding.",
    "peek_found": "Found me! Nice one.",
    "song_circle_intro": "Song circle - tap on beat if you want.",
    "song_circle_cue": "Tap HAPPY on the beat!",
    "correct": [
        "Nice one!",
        "Got it!",
        "Solid pick!",
        "Well done!",
    ],
    "try_again": [
        "Not quite - try again or skip.",
        "Good effort! Another try?",
    ],
    "skip": "Skip anytime. Your choice.",
    "streak_3": "Three in a row! On a roll.",
    "caregiver_cue": "Support only if asked - no pressure.",
}


def main() -> None:
    data = json.loads(VOICE.read_text(encoding="utf-8"))

    if "baby" not in data:
        data["baby"] = dict(BABY_BASE)
    if "tween" not in data:
        data["tween"] = dict(TWEEN_BASE)

    audiences = ("baby", "toddler", "child", "tween", "teen", "adult", "caregiver")
    for aud in audiences:
        block = data.setdefault(aud, {})
        for key, per_aud in NEW_KEYS.items():
            if key not in block and aud in per_aud:
                block[key] = per_aud[aud]

    VOICE.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"Updated {VOICE}")


if __name__ == "__main__":
    main()
