#!/usr/bin/env python3
"""Print GenerateImage-ready prompts for a batch of symbol words across all bands."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPT_SCRIPT = ROOT / "scripts" / "symbol_prompt.py"
BANDS = ("sprout", "bud", "sprig", "vine", "bloom", "canopy")

ACTIONS = {
    "sad": "Gentle sad expression with one small tear, caregiver-validated warmth, still kid-safe.",
    "all-done": "Happy Caly pushing blocks away with finished smile, all done gesture.",
    "go": "Happy Caly walking forward with green go arrow.",
    "wait": "Happy patient smile with hourglass or pause palm, five fingers visible.",
    "home": "Happy Caly pointing at cozy house with heart window.",
    "hug": "Happy Caly with open arms for consent hug, small hearts nearby.",
    "sleep": "Happy Caly yawning beside cozy bed with moon and stars.",
    "up": "Happy Caly with arms reaching up and arrow pointing up.",
    "down": "Happy Caly sitting with arrow pointing down.",
    "water": "Happy Caly holding shiny water glass and water drop.",
    "hurt": "Soft concerned but hopeful expression, bandage on knee, kind and kid-safe not scary.",
    "milk": "Happy Caly holding cute milk carton with straw.",
    "juice": "Happy Caly holding bright juice box with straw.",
    "apple": "Happy Caly holding shiny red apple with leaf.",
    "please": "Happy Caly with hands together in please gesture, five fingers visible.",
    "love": "Happy Caly hugging big pink heart with warm smile.",
    "dog": "Happy Caly beside friendly golden puppy wagging tail.",
    "cat": "Happy Caly beside friendly orange kitten purring.",
    "again": "Happy Caly with circular repeat arrows, try again gesture.",
    "ball": "Happy Caly holding red playground ball.",
    "big": "Happy Caly pointing at large star next to small star.",
    "blanket": "Happy Caly wrapped in soft cozy blanket.",
    "book": "Happy Caly holding colorful open picture book.",
    "bus": "Happy Caly beside yellow school bus smiling.",
    "car": "Happy Caly beside small red toy car.",
    "clean": "Happy Caly with sparkle shine on clean surface.",
    "close": "Happy Caly closing door snug with smile.",
    "cold": "Happy Caly with snowflake and ice cube, brr gesture.",
    "cookie": "Happy Caly holding chocolate chip cookie.",
    "daddy": "Happy Caly waving beside warm father figure.",
    "dirty": "Happy Caly with small mud spot, still friendly.",
    "dry": "Happy Caly with fluffy towel drying hands.",
    "friend": "Happy Caly holding hands with friend figure.",
    "hot": "Happy Caly with steaming bowl, hot gesture.",
    "hungry": "Happy Caly rubbing tummy hungry gesture.",
    "listen": "Happy Caly with hand cupped to ear, sound waves.",
    "little": "Happy Caly pointing at tiny star next to big star.",
    "look": "Happy Caly with big friendly eyes looking.",
    "mad": "Frustrated but safe kid expression, not scary.",
    "mommy": "Happy Caly waving beside warm mother figure.",
    "need": "Happy Caly with gentle exclamation, I need gesture.",
    "open": "Happy Caly opening door with light coming through.",
    "scared": "Worried but safe expression, not horror.",
    "shoe": "Happy Caly holding colorful kids sneaker.",
    "tired": "Sleepy yawn expression, gentle and safe.",
    "toy": "Happy Caly hugging teddy bear toy.",
    "want": "Happy Caly reaching toward desired item.",
    "wash": "Happy Caly with soap bubbles washing hands, five fingers.",
    "wet": "Happy Caly with water splash on hands.",
    "symbol_eat": "Happy Caly eating with spoon, large clear eat pictogram.",
    "symbol_happy": "Happy Caly with big joyful smile and sparkles.",
    "symbol_help": "Happy Caly reaching open hand asking for help, five fingers.",
    "symbol_more": "Happy Caly with open palms asking for more.",
    "symbol_play": "Happy Caly jumping with red ball for play.",
}


def main() -> None:
    words = sys.argv[1:] if len(sys.argv) > 1 else ["sad", "all-done", "go", "wait", "home", "hug"]
    for word in words:
        action = ACTIONS.get(word, f"Happy Caly demonstrating the word {word}.")
        for band in BANDS:
            out = subprocess.check_output(
                [sys.executable, str(PROMPT_SCRIPT), band, word, action],
                text=True,
            ).strip()
            print(f"\n# {word}-{band}.png")
            print(out)


if __name__ == "__main__":
    main()
