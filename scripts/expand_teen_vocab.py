# -*- coding: utf-8 -*-
"""Expand teen-adult vocabulary to 60 functional words."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "vocabulary" / "teen-adult-functional.json"
FLUTTER = ROOT.parent / "calyndra-mobile-flutter" / "assets" / "vocabulary" / PATH.name
WEB = ROOT.parent / "calyndra-app" / "content" / PATH.name

NEW = [
    {"id": "wait", "label": "wait", "category": "core", "description": "Ask for time before responding or acting."},
    {"id": "listen", "label": "please listen", "category": "communication", "description": "Request full attention respectfully."},
    {"id": "repeat-slower", "label": "repeat slower", "category": "communication", "description": "Ask someone to slow down and repeat."},
    {"id": "clarify", "label": "I don't understand", "category": "communication", "description": "Signal confusion without blame."},
    {"id": "topic-change", "label": "change topic", "category": "communication", "description": "Redirect conversation comfortably."},
    {"id": "leave", "label": "I want to leave", "category": "autonomy", "description": "Exit a space or situation."},
    {"id": "stay", "label": "I want to stay", "category": "autonomy", "description": "Remain where you feel safe."},
    {"id": "space", "label": "need space", "category": "regulation", "description": "Request physical or emotional distance."},
    {"id": "hug", "label": "hug please", "category": "social", "description": "Ask for consensual comfort."},
    {"id": "high-five", "label": "high five", "category": "social", "description": "Celebrate without pressure."},
    {"id": "introduce", "label": "introduce me", "category": "social", "description": "Support in social introductions."},
    {"id": "schedule-change", "label": "schedule change", "category": "life", "description": "Flag a change in plans."},
    {"id": "running-late", "label": "running late", "category": "life", "description": "Communicate delay proactively."},
    {"id": "cancel", "label": "cancel plans", "category": "life", "description": "Opt out of plans respectfully."},
    {"id": "grocery", "label": "grocery store", "category": "life", "description": "Community errand vocabulary."},
    {"id": "restaurant", "label": "restaurant", "category": "life", "description": "Dining out communication."},
    {"id": "order", "label": "my order", "category": "life", "description": "State food or item choice."},
    {"id": "allergy", "label": "food allergy", "category": "health", "description": "Disclose dietary needs clearly."},
    {"id": "nausea", "label": "feel sick", "category": "health", "description": "Report illness without diagnosis."},
    {"id": "rest", "label": "need rest", "category": "regulation", "description": "Request downtime for recovery."},
]

STYLE = "spark"


def main() -> None:
    data = json.loads(PATH.read_text(encoding="utf-8"))
    existing = {s["id"] for s in data["symbols"]}
    for sym in NEW:
        if sym["id"] in existing:
            continue
        sym["imageAsset"] = f"assets/symbols/{STYLE}/{sym['id']}.png"
        data["symbols"].append(sym)
    # ensure descriptions on all
    for sym in data["symbols"]:
        if "description" not in sym:
            sym["description"] = f"Functional AAC symbol: {sym['label']}."
        if "imageAsset" not in sym:
            style = "core" if sym.get("category") in ("life", "autonomy") else STYLE
            sym["imageAsset"] = f"assets/symbols/{style}/{sym['id']}.png"
    data["description"] = f"{len(data['symbols'])} functional teen and adult AAC symbols with descriptions."
    PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    FLUTTER.parent.mkdir(parents=True, exist_ok=True)
    FLUTTER.write_text(PATH.read_text(encoding="utf-8"), encoding="utf-8")
    WEB.write_text(PATH.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"Teen-adult vocab: {len(data['symbols'])} symbols")


if __name__ == "__main__":
    main()
