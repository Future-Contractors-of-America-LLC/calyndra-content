#!/usr/bin/env python3
"""QC sing-along-catalog.json - verify 5+ episodes per younger band, duration, voice keys."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "games" / "sing-along-catalog.json"
VOICE = ROOT / "games" / "caly-voice-scripts.json"
OUT_REPORT = ROOT / "SING_ALONG_QC_REPORT.md"

YOUNGER_BANDS = ("baby", "toddler", "child")
OPTIONAL_BANDS = ("tween",)
MIN_EPISODES = 5
DURATION_MIN_MS = 120_000
DURATION_MAX_MS = 240_000
MIN_BEATS = 4


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    issues: list[str] = []
    if not CATALOG.exists():
        print(f"MISSING: {CATALOG}")
        return 1

    catalog = load_json(CATALOG)
    voice = load_json(VOICE) if VOICE.exists() else {}
    audiences = catalog.get("audiences", {})
    summary_rows: list[tuple[str, int, int, int]] = []

    check_bands = list(YOUNGER_BANDS) + list(OPTIONAL_BANDS)
    for aud in check_bands:
        block = audiences.get(aud)
        if not block:
            issues.append(f"MISSING AUDIENCE: `{aud}` not in catalog.")
            continue

        episodes = block.get("episodes", [])
        new_eps = [e for e in episodes if e.get("isNew", True)]
        existing = [e for e in episodes if not e.get("isNew", True)]

        if aud in YOUNGER_BANDS and len(episodes) < MIN_EPISODES:
            issues.append(
                f"INSUFFICIENT: `{aud}` has {len(episodes)} episodes (need {MIN_EPISODES}+)."
            )

        summary_rows.append((aud, len(episodes), len(existing), len(new_eps)))

        for ep in episodes:
            eid = ep.get("id", "?")
            dur = ep.get("durationMs")
            if dur is None or dur < DURATION_MIN_MS or dur > DURATION_MAX_MS:
                issues.append(
                    f"DURATION: `{aud}/{eid}` durationMs={dur} "
                    f"(expected {DURATION_MIN_MS}-{DURATION_MAX_MS})."
                )

            beats = ep.get("beats") or []
            if len(beats) < MIN_BEATS:
                issues.append(f"BEATS: `{aud}/{eid}` has {len(beats)} beats (need {MIN_BEATS}+).")

            for i, beat in enumerate(beats):
                for field in ("ms", "pose", "lyric", "word", "mascotCue"):
                    if field not in beat or beat[field] in (None, ""):
                        issues.append(f"BEAT FIELD: `{aud}/{eid}` beat[{i}] missing `{field}`.")

            for key_name in ("voiceIntroKey", "voiceBeatKey"):
                vk = ep.get(key_name)
                if not vk:
                    issues.append(f"VOICE KEY MISSING: `{aud}/{eid}` has empty {key_name}.")
                    continue
                if not vk.startswith("show_"):
                    issues.append(f"VOICE KEY PREFIX: `{aud}/{eid}` key `{vk}` must start with show_.")
                scripts = voice.get(aud, {})
                if vk not in scripts:
                    issues.append(
                        f"VOICE KEY ABSENT: `{aud}/{eid}` key `{vk}` not in caly-voice-scripts.json."
                    )

            if not ep.get("bandPortrait"):
                issues.append(f"PORTRAIT MISSING: `{aud}/{eid}` has no bandPortrait.")

            if not ep.get("title"):
                issues.append(f"TITLE MISSING: `{aud}/{eid}` has no title.")

    lines = [
        "# Sing-along catalog QC report",
        "",
        f"Generated: **{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}**",
        "",
        "## Summary",
        "",
        "| Audience | Total | Existing | New | Status |",
        "|----------|-------|----------|-----|--------|",
    ]
    for aud, total, existing, new in summary_rows:
        required = aud in YOUNGER_BANDS
        status = "PASS" if (not required or total >= MIN_EPISODES) else "FAIL"
        lines.append(f"| {aud} | {total} | {existing} | {new} | {status} |")

    lines.extend([
        "",
        f"**Issues:** {len(issues)}",
        "",
        "## Rules checked",
        "",
        f"- At least {MIN_EPISODES} episodes per baby/toddler/child",
        f"- `durationMs` in [{DURATION_MIN_MS}, {DURATION_MAX_MS}] (~2-4 min)",
        "- Each episode has 4+ beats with ms/pose/lyric/word/mascotCue",
        "- All `show_*` voice keys present in `caly-voice-scripts.json` per audience",
        "- `bandPortrait` and `title` set on every episode",
        "",
        "## Issues",
        "",
    ])
    if issues:
        lines.extend(f"- {i}" for i in issues)
    else:
        lines.append("- None")

    OUT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"QC: {len(summary_rows)} audiences, {len(issues)} issues")
    print(f"Wrote {OUT_REPORT.name}")
    for aud, total, _e, new in summary_rows:
        print(f"  {aud}: {total} episodes ({new} new)")
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
