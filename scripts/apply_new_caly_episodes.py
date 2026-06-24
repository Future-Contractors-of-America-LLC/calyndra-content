# -*- coding: utf-8 -*-
"""Apply new Caly and Friends episodes from videos/caly_friends_new_episodes.json."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "videos" / "caly_friends_new_episodes.json"
CATALOG = ROOT / "videos" / "caly_friends_catalog.json"
GEN = ROOT / "scripts" / "generate_caly_friends_episodes.py"

BAND_META = {
    "baby": ("Caly Seed", "0-23 mo", 300, 50),
    "toddler": ("Caly Sprout", "2-4", 600, 100),
    "child": ("Caly Bud", "5-8", 900, 150),
    "tween": ("Caly Sprig", "9-12", 1200, 200),
    "teen": ("Caly Vine", "13-17", 1800, 300),
    "adult": ("Caly Bloom", "18+", 2700, 450),
}

FRIEND_LABEL = {
    "Pip": "Pip the bunny",
    "Fern": "Fern the fox",
    "Moss": "Moss the bear",
    "Reed": "Reed the owl",
    "Sage": "Sage the deer",
    "Laurel": "Laurel the cardinal",
}

EP_BAND_MAP = {
    "baby": "seed",
    "toddler": "sprout",
    "child": "bud",
    "tween": "sprig",
    "teen": "vine",
    "adult": "bloom",
}


def slug_from_id(ep_id: str) -> str:
    return ep_id.replace("_long", "").replace("_", "-")


def write_script(ep: dict) -> str:
    band = ep["band"]
    caly, age, dur, scenes = BAND_META[band]
    mins = dur // 60
    script_rel = f"videos/scripts/{ep['script_num']:02d}-{slug_from_id(ep['id'])}.md"
    path = ROOT / script_rel
    act_rows = "\n".join(f"| {a} | {s} | {b} |" for a, s, b in ep["acts"])
    key_rows = "\n".join(
        f"| {i + 1} | {v} | {d} |" for i, (v, d) in enumerate(ep["key_scenes"])
    )
    friend_label = FRIEND_LABEL[ep["friend"]]
    content = f"""# {ep['title']} ({band}, ~{mins} min, {scenes} scenes)

**Series:** Caly and Friends  
**Band:** {band.title()} ({caly}, {age})  
**Friend:** {friend_label}  
**Mentor:** Elder Oak  
**Christian lesson:** {ep['lesson']} ({ep['christian']}).

## Story arc

| Act | Scenes | Beats |
|-----|--------|-------|
{act_rows}

## Key scenes

| # | Visual | Dialogue |
|---|--------|----------|
{key_rows}

## Interactive tap-along

- Chapters at {ep['chapters']}.

**Status:** Script complete - full render pending batch job (`status: script-only`).

Not medical advice. Original Calyndra characters only.
"""
    path.write_text(content, encoding="utf-8")
    return script_rel


def catalog_entry(ep: dict, script_rel: str) -> dict:
    band = ep["band"]
    _, _, dur, scenes = BAND_META[band]
    return {
        "id": ep["id"],
        "band": band,
        "title": ep["title"],
        "friend": ep["friend"],
        "mentor": "Elder Oak",
        "targetDurationSec": dur,
        "targetSceneCount": scenes,
        "script": script_rel,
        "webm": f"{ep['id']}.webm",
        "lesson": ep["lesson"],
        "pilot": False,
        "status": "script-only",
    }


def patch_generator(new_eps: list[dict]) -> None:
    gen_text = GEN.read_text(encoding="utf-8")
    beats_lines: list[str] = []
    band_lines: list[str] = []
    for ep in new_eps:
        beats_lines.append(f'    "{ep["id"]}": [')
        for caption, tag in ep["beats"]:
            cap = caption.replace("\\", "\\\\").replace('"', '\\"')
            beats_lines.append(f'        ("{cap}", "{tag}"),')
        beats_lines.append("    ],")
        band_lines.append(f'    "{ep["id"]}": "{EP_BAND_MAP[ep["band"]]}",')

    idx = gen_text.find('    "laurel_morning_song_long":')
    end = gen_text.find("\n}", gen_text.find("    ],", idx))
    gen_text = gen_text[:end] + ",\n" + "\n".join(beats_lines) + gen_text[end:]

    band_marker = '    "laurel_morning_song_long": "bloom",'
    idx2 = gen_text.find(band_marker)
    end2 = gen_text.find("\n}", idx2)
    gen_text = gen_text[:end2] + "\n" + "\n".join(band_lines) + gen_text[end2:]
    GEN.write_text(gen_text, encoding="utf-8")


def write_render_queue(added: list[str], ep_by_id: dict) -> None:
    queue = ROOT / "videos" / "RENDER_QUEUE.md"
    lines = [
        "# Caly and Friends render queue",
        "",
        f"Updated: 2026-06-24 - {len(added)} new script-only episodes awaiting full render.",
        "",
        "## Pending full render (script-only)",
        "",
    ]
    for ep_id in added:
        meta = ep_by_id[ep_id]
        lines.append(
            f"- `{ep_id}` - {meta['title']} ({meta['band']}, {meta['targetDurationSec']}s) "
            f"-> `python scripts/generate_caly_friends_episodes.py --id {ep_id}`"
        )
    lines.extend([
        "",
        "## Batch command",
        "",
        "```bash",
        "python scripts/generate_caly_friends_episodes.py --all",
        "```",
        "",
        "Frames pregenerated via `--pregenerate-frames` (no full TTS render in content commit).",
    ])
    queue.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    new_eps: list[dict] = json.loads(DATA.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    existing_ids = {e["id"] for e in catalog["episodes"]}
    added: list[str] = []
    for ep in new_eps:
        if ep["id"] in existing_ids:
            continue
        script_rel = write_script(ep)
        catalog["episodes"].append(catalog_entry(ep, script_rel))
        added.append(ep["id"])
        print(f"ADD {ep['id']}")

    catalog["lockedUtc"] = "2026-06-24T12:00:00Z"
    CATALOG.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    if added:
        patch_generator([e for e in new_eps if e["id"] in added])
    ep_by_id = {e["id"]: e for e in catalog["episodes"]}
    write_render_queue(added, ep_by_id)
    print(f"Done: {len(added)} added, {len(catalog['episodes'])} total")


if __name__ == "__main__":
    main()
