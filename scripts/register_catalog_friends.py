#!/usr/bin/env python3
"""Register new Caly Friends characters from expanded catalog."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "caly_character_registry.json"
CATALOG = ROOT / "videos" / "caly_friends_catalog.json"

SPECIES = {
    "Wren": "chick",
    "Dot": "ladybug",
    "Pebble": "turtle",
    "Lumi": "firefly",
    "Coco": "duckling",
    "Nuzzle": "lamb",
    "Maple": "squirrel",
    "Sunny": "bee",
    "Petal": "butterfly",
    "Brook": "otter",
    "Hazel": "hedgehog",
    "Sprout": "frog",
    "River": "beaver",
    "Sky": "blue jay",
    "Clover": "deer",
    "Flint": "owl",
    "Briar": "rabbit",
    "Thistle": "fox",
    "Ash": "raccoon",
    "Pike": "heron",
    "Juniper": "fox",
    "Ridge": "hawk",
    "Willow": "deer",
    "Lane": "deer",
    "Atlas": "wolf",
    "Nova": "raven",
    "Ember": "fox",
    "Harbor": "seal",
    "Summit": "eagle",
    "Cipher": "owl",
    "Dawn": "songbird",
    "Cedar": "stag",
    "Meadow": "sheep",
    "Stone": "crane",
    "Root": "badger",
}

# Harbor dolphin for adult episode uses same name; species overridden per band below
BAND_SPECIES_OVERRIDE = {
    ("adult", "Harbor"): "dolphin",
    ("teen", "Harbor"): "seal",
}


def slug(name: str) -> str:
    return name.lower().replace(" ", "-")


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    friends_by_band = registry.setdefault("friendsByBand", {})
    assets = registry.setdefault("assets", [])
    asset_ids = {a["id"] for a in assets}
    added = 0

    for ep in catalog["episodes"]:
        band = ep["band"]
        name = ep["friend"]
        band_friends = friends_by_band.setdefault(band, {"friends": [], "mentor": friends_by_band.get(band, {}).get("mentor") or friends_by_band.get("baby", {}).get("mentor")})
        if "friends" not in band_friends:
            band_friends["friends"] = []
        names = {f["name"] for f in band_friends["friends"]}
        if name in names:
            continue
        species = BAND_SPECIES_OVERRIDE.get((band, name), SPECIES.get(name, "friend"))
        portrait = f"assets/caly-friends/{slug(name)}-{band}.png"
        band_friends["friends"].append(
            {
                "name": name,
                "species": species,
                "portrait": portrait,
                "role": f"{name} story friend",
                "agesWithBand": registry["ageRangesByBand"].get(band, band),
                "lessonTheme": ep.get("lesson", "kindness"),
                "status": "bootstrap",
            }
        )
        asset_id = f"friend-{slug(name)}-{band}"
        if asset_id not in asset_ids:
            assets.append(
                {
                    "id": asset_id,
                    "path": portrait,
                    "type": "friend-portrait",
                    "band": band,
                    "status": "bootstrap",
                    "generatedUtc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "note": "bootstrap portrait pending dedicated art",
                }
            )
            asset_ids.add(asset_id)
        added += 1

    registry["version"] = registry.get("version", 6) + 1
    registry["lockedUtc"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    REGISTRY.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    print(f"Registered {added} new friend(s)")


if __name__ == "__main__":
    main()
