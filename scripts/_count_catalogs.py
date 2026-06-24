#!/usr/bin/env python3
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
games = json.loads((root / "games/band-games-catalog.json").read_text(encoding="utf-8"))
sing = json.loads((root / "games/sing-along-catalog.json").read_text(encoding="utf-8"))
cartoon = json.loads((root / "videos/caly_friends_catalog.json").read_text(encoding="utf-8"))
bands = ["baby", "toddler", "child", "tween", "teen", "adult", "caregiver"]

print("GAMES per audience:")
for b in bands:
    g = games["audiences"].get(b, {}).get("games", [])
    new = sum(1 for x in g if x.get("isNew"))
    print(f"  {b}: {len(g)} total, {new} isNew")

print("SING-ALONG per audience:")
for b in bands:
    eps = sing["audiences"].get(b, {}).get("episodes", [])
    print(f"  {b}: {len(eps)}")

print(f"CARTOONS: {len(cartoon['episodes'])} episodes")
for ep in cartoon["episodes"]:
    print(f"  {ep['band']}: {ep['title']} status={ep.get('status')}")

print("VOCAB:")
for f in sorted((root / "vocabulary").glob("*-words.json")):
    data = json.loads(f.read_text(encoding="utf-8"))
    words = data.get("words") or data.get("items") or []
    print(f"  {f.stem}: {len(words)}")

phrases_dir = root / "phrases"
if phrases_dir.is_dir():
    print("PHRASES:")
    for f in sorted(phrases_dir.glob("*-phrases.json")):
        data = json.loads(f.read_text(encoding="utf-8"))
        items = data.get("phrases") or data.get("items") or []
        print(f"  {f.stem}: {len(items)}")
