#!/usr/bin/env python3
"""Build locked character_voice_canon.json from registries."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CENTRAL = ROOT.parent / "calyndra-central"
ROOTS = Path(os.environ.get("ROOTS_GARDEN_CONTENT_ROOT", ROOT.parent / "roots-garden-content"))
OUT = ROOT / "character_voice_canon.json"

sys.path.insert(0, str(CENTRAL))
from speech_tts import VOICE_PROFILES  # noqa: E402

VOICE_POOL = [
    ("en-US-AriaNeural", "-20%", "+4%"),
    ("en-US-JaneNeural", "-18%", "+6%"),
    ("en-US-AnaNeural", "-10%", "+5%"),
    ("en-US-AvaNeural", "+0%", "+2%"),
    ("en-US-JennyNeural", "+2%", "+0%"),
    ("en-US-MichelleNeural", "-4%", "-2%"),
    ("en-US-NancyNeural", "-6%", "-1%"),
    ("en-US-SaraNeural", "-12%", "+3%"),
    ("en-US-EmmaNeural", "-8%", "+4%"),
    ("en-US-AmberNeural", "-14%", "+5%"),
    ("en-US-MonicaNeural", "-5%", "+1%"),
    ("en-US-CoraNeural", "-16%", "+7%"),
    ("en-US-ElizabethNeural", "-3%", "-3%"),
    ("en-US-LunaNeural", "-22%", "+8%"),
    ("en-US-DavisNeural", "-7%", "-4%"),
    ("en-US-GuyNeural", "-9%", "-5%"),
    ("en-US-TonyNeural", "-11%", "-3%"),
    ("en-US-JasonNeural", "-13%", "-2%"),
    ("en-US-BrandonNeural", "-15%", "-1%"),
    ("en-US-RogerNeural", "-1%", "-6%"),
    ("en-US-SteffanNeural", "+1%", "-2%"),
    ("en-US-ChristopherNeural", "+3%", "-4%"),
    ("en-US-EricNeural", "-19%", "+2%"),
    ("en-US-JacobNeural", "-21%", "+1%"),
    ("en-US-BrianNeural", "-17%", "+0%"),
]


def _next_voice(used: set[tuple[str, str, str]], idx: int) -> dict:
    for step in range(len(VOICE_POOL) * 6):
        voice, rate, pitch = VOICE_POOL[(idx + step) % len(VOICE_POOL)]
        pitch_val = int(pitch.replace("%", "").replace("+", ""))
        rate_val = int(rate.replace("%", "").replace("+", ""))
        for delta in (0, 1, -1, 2, -2, 3, -3):
            trial_pitch = f"{pitch_val + delta:+d}%"
            trial_rate = f"{rate_val + (delta % 2):+d}%"
            key = (voice, trial_rate, trial_pitch)
            if key not in used:
                used.add(key)
                return {"voice": voice, "rate": trial_rate, "pitch": trial_pitch}
    raise RuntimeError("exhausted voice pool")


def main() -> int:
    registry = json.loads((ROOT / "caly_character_registry.json").read_text(encoding="utf-8"))
    characters: list[dict] = []
    used: set[tuple[str, str, str]] = set()
    idx = 0

    nicknames = registry.get("nicknamesByBand") or {}
    for band, profile in VOICE_PROFILES.items():
        vp = {
            "voice": profile["voice"],
            "rate": profile["rate"],
            "pitch": profile["pitch"],
            "style": profile.get("style", "friendly"),
        }
        used.add((vp["voice"], vp["rate"], vp["pitch"]))
        characters.append(
            {
                "id": f"caly-{band}",
                "displayName": f"Caly ({nicknames.get(band, band)})",
                "universe": "calyndra",
                "role": "primary-mascot",
                "band": band,
                "personality": profile.get("arc", ""),
                "tts": vp,
            }
        )

    seen_friends: set[str] = set()
    for band, block in (registry.get("friendsByBand") or {}).items():
        for friend in block.get("friends") or []:
            name = str(friend.get("name") or "").strip()
            if not name:
                continue
            key = name.lower()
            if key in seen_friends:
                continue
            seen_friends.add(key)
            vp = _next_voice(used, idx)
            idx += 1
            characters.append(
                {
                    "id": f"friend-{key}",
                    "displayName": name,
                    "universe": "caly-friends",
                    "role": friend.get("role", "friend"),
                    "band": band,
                    "personality": friend.get("lessonTheme") or friend.get("role", ""),
                    "tts": vp,
                }
            )
        mentor = block.get("mentor") or {}
        if mentor.get("name") and "elder-oak" not in {c["id"] for c in characters}:
            if not any(c["id"] == "friend-elder-oak" for c in characters):
                vp = _next_voice(used, idx)
                idx += 1
                characters.append(
                    {
                        "id": "friend-elder-oak",
                        "displayName": mentor["name"],
                        "universe": "caly-friends",
                        "role": mentor.get("role", "mentor"),
                        "band": "caregiver",
                        "personality": mentor.get("lessonTheme", "mentor"),
                        "tts": vp,
                    }
                )

    for fam_id, fam in (registry.get("familyMembers") or {}).items():
        vp = _next_voice(used, idx)
        idx += 1
        characters.append(
            {
                "id": f"family-{fam_id}",
                "displayName": fam.get("displayName", fam_id),
                "universe": "caly-family",
                "role": fam.get("relation", "family"),
                "band": fam.get("band") or fam.get("appearsFromBand", "seed"),
                "personality": fam.get("note", ""),
                "tts": vp,
            }
        )

    if (ROOTS / "root_character_registry.json").is_file():
        roots = json.loads((ROOTS / "root_character_registry.json").read_text(encoding="utf-8"))
        for portrait in roots.get("portraits") or []:
            pid = portrait.get("id")
            if not pid or any(c["id"] == f"root-{pid}" for c in characters):
                continue
            vp = _next_voice(used, idx)
            idx += 1
            characters.append(
                {
                    "id": f"root-{pid}",
                    "displayName": portrait.get("displayName", pid),
                    "universe": "roots-garden",
                    "role": portrait.get("role", "character"),
                    "band": portrait.get("band", "rootSprouts"),
                    "personality": portrait.get("subtitle", ""),
                    "tts": vp,
                }
            )

    lock_lines = [
        "## CHARACTER VOICE LOCK",
        "- Each character has a unique voice tuple (voice+rate+pitch); never swap.",
        "- Caly is one maturing plant friend; friends and Root's Garden speak as themselves.",
        f"- Canon version: {len(characters)} characters locked.",
    ]
    canon = {
        "version": 1,
        "generatedUtc": __import__("datetime").datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "characters": characters,
        "llm": {"systemLock": "\n".join(lock_lines)},
    }
    OUT.write_text(json.dumps(canon, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT} ({len(characters)} characters)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
