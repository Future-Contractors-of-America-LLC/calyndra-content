#!/usr/bin/env python3
"""Build a locked GenerateImage prompt for a band symbol word."""

from __future__ import annotations

BANDS = {
    "sprout": ("Sprout", "mint romper over pale pink tee, small leaves"),
    "bud": ("Bud", "soft rose-pink tee and green shorts, two head leaves"),
    "sprig": ("Sprig", "rose-pink tee, green leaf-pattern shorts, more leaves and tendrils"),
    "vine": ("Vine", "pink hoodie and sweatpants, vine leaves on head"),
    "bloom": ("Bloom", "modest cardigan, top, full-length trousers, bloom accents"),
    "canopy": ("Canopy", "modest long dress with cardigan, canopy leaves"),
}

NON_HAPPY = {
    "sad", "mad", "scared", "anxious", "frustrated", "overwhelmed",
    "uncomfortable", "pain", "nausea", "dont-like", "hurt",
}


def expression_clause(word_id: str) -> str:
    if word_id in NON_HAPPY:
        return (
            "Expression appropriate to the emotion word (still kid-safe, never horror). "
        )
    return "Warm HAPPY smile and bright friendly eyes. "


def prompt(band: str, word_id: str, action: str) -> str:
    nickname, outfit = BANDS[band]
    return (
        f"AAC symbol tile, square 1:1. Caly {nickname}, friendly green plant girl matching "
        f"band portrait reference ({outfit}, modest). {expression_clause(word_id)}"
        f"Exactly FIVE fingers on each visible hand, human-like. "
        f"{action} Chunky dark green outlines, soft mint-to-sky gradient background, "
        f"preschool cartoon style, no text, no letters. Original Calyndra IP."
    )


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 4:
        print("Usage: symbol_prompt.py <band> <word_id> <action description>")
        print("Example: symbol_prompt.py bud help reaching one open hand toward viewer asking for help")
        raise SystemExit(1)
    print(prompt(sys.argv[1], sys.argv[2], sys.argv[3]))
