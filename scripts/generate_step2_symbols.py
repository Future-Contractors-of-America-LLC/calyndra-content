#!/usr/bin/env python3
"""Emit word-band jobs for STEP 2 symbol art generation."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPT_SCRIPT = ROOT / "scripts" / "symbol_prompt.py"
BATCH_SCRIPT = ROOT / "scripts" / "symbol_batch_prompts.py"
BANDS = ("sprout", "bud", "sprig", "vine", "bloom", "canopy")
APP_SPRout = ROOT.parent / "calyndra-app" / "assets" / "symbols" / "sprout"

STEP2_WORDS = [
    "crib", "blocks", "splash", "clap", "peek", "cuddle", "lullaby", "yum", "owie", "blankie",
    "potty", "bubbles", "sandbox", "truck", "puzzle", "sticker", "wagon", "cereal", "yogurt", "tricycle",
    "science", "guitar", "soccer", "birthday", "museum", "camping", "scooter", "tablet", "spelling", "kite",
    "algebra", "presentation", "permission", "detention", "orchestra", "robotics", "podcast", "charger",
    "earbuds", "debate", "volunteer", "mindfulness", "syllabus", "textbook", "yearbook",
    "drivers-license", "internship", "scholarship", "credit-card", "rideshare", "diploma", "tuition",
    "roommate", "budget", "streaming", "social-media", "part-time", "parking", "copay", "gig-work",
    "mortgage", "retirement", "taxes", "benefits", "pension", "warranty", "subscription",
    "direct-deposit", "overtime", "performance-review", "onboarding", "hr", "contractor",
    "regulation", "patience", "breathe", "visual-schedule", "celebrate", "modeling",
    "scaffold", "prompt-wait", "reinforcement",
]


def action_for(word: str) -> str:
    out = subprocess.check_output(
        [sys.executable, str(BATCH_SCRIPT.with_name("symbol_batch_prompts.py"))],
        text=True,
        cwd=str(ROOT),
    )
    # fallback: import ACTIONS from symbol_batch_prompts
    from symbol_batch_prompts import ACTIONS  # noqa: WPS433

    return ACTIONS.get(word, f"Happy Caly demonstrating the word {word}.")


def main() -> None:
    from symbol_batch_prompts import ACTIONS

    existing = {p.stem for p in APP_SPRout.glob("*.png")} if APP_SPRout.is_dir() else set()
    jobs = []
    for word in STEP2_WORDS:
        if word in existing:
            continue
        action = ACTIONS.get(word, f"Happy Caly demonstrating the word {word}.")
        for band in BANDS:
            prompt = subprocess.check_output(
                [sys.executable, str(PROMPT_SCRIPT), band, word, action],
                text=True,
            ).strip()
            jobs.append({"word": word, "band": band, "filename": f"{word}-{band}.png", "prompt": prompt})
    out = ROOT / "generated" / "step2-symbol-jobs.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(jobs, indent=2), encoding="utf-8")
    print(f"Wrote {len(jobs)} jobs to {out.name} ({len(STEP2_WORDS)} words)")


if __name__ == "__main__":
    main()
