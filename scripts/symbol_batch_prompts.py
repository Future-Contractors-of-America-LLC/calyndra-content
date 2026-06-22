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
