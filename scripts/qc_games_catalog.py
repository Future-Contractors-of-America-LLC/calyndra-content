#!/usr/bin/env python3
"""QC band-games-catalog.json - verify 5+ new games per band, duration, voice keys."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "games" / "band-games-catalog.json"
VOICE = ROOT / "games" / "caly-voice-scripts.json"
OUT_REPORT = ROOT / "GAMES_QC_REPORT.md"

AUDIENCES = ("baby", "toddler", "child", "tween", "teen", "adult", "caregiver")
MIN_NEW_GAMES = 5
DURATION_MIN = 3
DURATION_MAX = 5


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

    for aud in AUDIENCES:
        block = audiences.get(aud)
        if not block:
            issues.append(f"MISSING AUDIENCE: `{aud}` not in catalog.")
            continue

        games = block.get("games", [])
        new_games = [g for g in games if g.get("isNew")]
        existing = [g for g in games if not g.get("isNew")]

        if len(new_games) < MIN_NEW_GAMES:
            issues.append(
                f"INSUFFICIENT NEW: `{aud}` has {len(new_games)} new games (need {MIN_NEW_GAMES}+)."
            )

        summary_rows.append((aud, len(games), len(existing), len(new_games)))

        for g in games:
            gid = g.get("id", "?")
            dur = g.get("durationMinutes")
            if dur is None or dur < DURATION_MIN or dur > DURATION_MAX:
                issues.append(
                    f"DURATION: `{aud}/{gid}` durationMinutes={dur} (expected {DURATION_MIN}-{DURATION_MAX})."
                )

            for key_name in ("voiceIntroKey", *[
                f"voicePromptKeys[{i}]" for i in range(len(g.get("voicePromptKeys") or []))
            ]):
                if key_name.startswith("voicePromptKeys"):
                    idx = int(key_name.split("[")[1].rstrip("]"))
                    vk = (g.get("voicePromptKeys") or [])[idx]
                else:
                    vk = g.get(key_name)
                if not vk:
                    issues.append(f"VOICE KEY MISSING: `{aud}/{gid}` has empty {key_name}.")
                    continue
                scripts = voice.get(aud, {})
                if vk not in scripts:
                    issues.append(f"VOICE KEY ABSENT: `{aud}/{gid}` key `{vk}` not in caly-voice-scripts.json.")

            mode = g.get("mode")
            if not mode:
                issues.append(f"MODE MISSING: `{aud}/{gid}` has no mode.")

            if not g.get("bandPortrait"):
                issues.append(f"PORTRAIT MISSING: `{aud}/{gid}` has no bandPortrait.")

            rounds = g.get("minRounds", 0)
            if rounds < 4:
                issues.append(f"ROUNDS LOW: `{aud}/{gid}` minRounds={rounds} (expect ~6-8 for 3-5 min).")

    lines = [
        "# Games catalog QC report",
        "",
        f"Generated: **{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}**",
        "",
        "## Summary",
        "",
        "| Audience | Total | Existing | New | Status |",
        "|----------|-------|----------|-----|--------|",
    ]
    for aud, total, existing, new in summary_rows:
        status = "PASS" if new >= MIN_NEW_GAMES else "FAIL"
        lines.append(f"| {aud} | {total} | {existing} | {new} | {status} |")

    lines.extend([
        "",
        f"**Issues:** {len(issues)}",
        "",
        "## Rules checked",
        "",
        f"- At least {MIN_NEW_GAMES} new games (`isNew: true`) per audience",
        f"- `durationMinutes` in [{DURATION_MIN}, {DURATION_MAX}]",
        "- All `voiceIntroKey` and `voicePromptKeys` present in `caly-voice-scripts.json` per audience",
        "- `bandPortrait` and `mode` set on every game",
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
        print(f"  {aud}: {new} new / {total} total")
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
