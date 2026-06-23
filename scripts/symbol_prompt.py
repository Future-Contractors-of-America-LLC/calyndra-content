#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build a locked GenerateImage prompt for a band symbol word."""

from __future__ import annotations

BANDS = {
    "sprout": (
        "Sprout",
        "toddler: mint romper over pale pink tee, ONE small leaf on head, chubby youngest proportions",
    ),
    "bud": (
        "Bud",
        "child: soft rose-pink tee and green shorts, TWO head leaves, kid proportions",
    ),
    "sprig": (
        "Sprig",
        "tween: rose-pink tee, green leaf-pattern shorts, THREE to FOUR leaves and tendrils",
    ),
    "vine": (
        "Vine",
        "teen: pink hoodie and sweatpants, vine leaves, taller teen proportions",
    ),
    "bloom": (
        "Bloom",
        "adult: modest cardigan, top, full-length trousers, bloom flower accents, mature adult",
    ),
    "canopy": (
        "Canopy",
        "caregiver ONLY: modest long dress with cardigan, wide canopy leaves and pink flowers",
    ),
}

BAND_FORBIDDEN = {
    "sprout": "NO dress, NO canopy leaves, NO teen hoodie, NO adult cardigan",
    "bud": "NO romper, NO dress, NO canopy, NO hoodie",
    "sprig": "NO romper, NO dress, NO canopy, NO adult cardigan",
    "vine": "NO romper, NO dress, NO canopy, NO child shorts only",
    "bloom": "NO romper, NO canopy dress, NO toddler proportions",
    "canopy": "NO romper, NO child shorts, NO teen hoodie only",
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
    forbidden = BAND_FORBIDDEN.get(band, "")
    return (
        f"AAC symbol tile, square 1:1. Caly {nickname} ONLY - must match band portrait reference exactly "
        f"({outfit}, modest). {forbidden}. "
        f"Do NOT draw Caly Canopy unless band is canopy. "
        f"{expression_clause(word_id)}"
        f"Exactly FIVE fingers on each visible hand, human-like, count them. "
        f"{action} Chunky dark green outlines, soft mint-to-sky gradient background, "
        f"preschool cartoon style, no text, no letters, no name labels in image. Original Calyndra IP."
    )


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 4:
        print("Usage: symbol_prompt.py <band> <word_id> <action description>")
        print("Example: symbol_prompt.py bud help reaching one open hand toward viewer asking for help")
        raise SystemExit(1)
    print(prompt(sys.argv[1], sys.argv[2], sys.argv[3]))
