#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Voice profile QC - Azure Neural voices, manifest version, no legacy robotic names."""

from __future__ import annotations

import ast
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CENTRAL_TTS = ROOT.parent / "calyndra-central" / "speech_tts.py"
APP_VOICE_JS = ROOT.parent / "calyndra-app" / "js" / "caly-voice.js"
VOICE_MANIFEST = ROOT.parent / "calyndra-app" / "content" / "voice" / "manifest.json"
OUT_REPORT = ROOT / "VOICE_QC_REPORT.md"

AUDIENCES = ("baby", "toddler", "child", "tween", "teen", "adult", "caregiver")

# Legacy / robotic browser or standard voices - must not appear in production profiles.
LEGACY_VOICE_PATTERNS = (
    r"en-US-David",
    r"en-US-Mark",
    r"en-US-Zira",
    r"en-US-Guy",
    r"en-US-Amber",
    r"en-US-Jessa",
    r"en-GB-Ryan",
    r"en-GB-Sonia",
    r"Google UK English Male",
    r"Microsoft David",
    r"Microsoft Mark",
    r"Microsoft Zira",
    r"Compact",
    r"Desktop",
)

# Required: Azure Neural voice short names used in speech_tts.py
REQUIRED_NEURAL = {
    "baby": "AriaNeural",
    "toddler": "AriaNeural",
    "child": "AnaNeural",
    "tween": "AvaNeural",
    "teen": "JennyNeural",
    "adult": "AvaNeural",
    "caregiver": "JennyNeural",
}

MIN_STYLE_DEGREE = 0.65


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def extract_voice_profiles() -> dict[str, dict]:
    text = CENTRAL_TTS.read_text(encoding="utf-8")
    match = re.search(r"VOICE_PROFILES\s*=\s*(\{.*?\n\})\s*\n", text, re.DOTALL)
    if not match:
        raise ValueError("Could not parse VOICE_PROFILES from speech_tts.py")
    return ast.literal_eval(match.group(1))


def extract_app_profile_version() -> int:
    text = APP_VOICE_JS.read_text(encoding="utf-8")
    m = re.search(r"VOICE_PROFILE_VERSION\s*=\s*(\d+)", text)
    return int(m.group(1)) if m else 0


def check_central_profiles(issues: list[str], warnings: list[str]) -> list[tuple[str, str, str, str, str]]:
    if not CENTRAL_TTS.is_file():
        issues.append("TTS: calyndra-central/speech_tts.py not found.")
        return []

    profiles = extract_voice_profiles()
    rows: list[tuple[str, str, str, str, str]] = []
    central_text = CENTRAL_TTS.read_text(encoding="utf-8")

    for pat in LEGACY_VOICE_PATTERNS:
        if re.search(pat, central_text, re.I):
            issues.append(f"TTS: legacy/robotic voice pattern `{pat}` found in speech_tts.py.")

    for aud in AUDIENCES:
        prof = profiles.get(aud)
        if not prof:
            issues.append(f"TTS: missing VOICE_PROFILES entry for `{aud}`.")
            rows.append((aud, "-", "-", "-", "FAIL"))
            continue
        voice = prof.get("voice", "")
        rate = prof.get("rate", "")
        style = prof.get("style", "")
        degree = prof.get("styledegree", "")
        status = "PASS"
        expected = REQUIRED_NEURAL.get(aud, "")
        if "Neural" not in voice:
            issues.append(f"TTS: `{aud}` voice `{voice}` is not Azure Neural.")
            status = "FAIL"
        elif expected and expected not in voice:
            warnings.append(f"TTS: `{aud}` uses `{voice}` (expected contains `{expected}`).")
        if not style:
            warnings.append(f"TTS: `{aud}` missing express-as style (less human).")
            status = "WARN" if status == "PASS" else status
        try:
            deg_f = float(str(degree).strip())
            if deg_f < MIN_STYLE_DEGREE:
                warnings.append(f"TTS: `{aud}` styledegree {deg_f} below {MIN_STYLE_DEGREE}.")
        except (TypeError, ValueError):
            if style:
                warnings.append(f"TTS: `{aud}` styledegree missing or invalid.")
        rows.append((aud, voice, rate, style or "-", status))
    return rows


def check_manifest(issues: list[str], warnings: list[str]) -> tuple[int, int, bool]:
    app_version = extract_app_profile_version()
    if not VOICE_MANIFEST.is_file():
        issues.append("VOICE: calyndra-app/content/voice/manifest.json missing.")
        return app_version, 0, False
    manifest = load_json(VOICE_MANIFEST)
    m_version = manifest.get("profileVersion") or manifest.get("version") or 0
    generated = manifest.get("generated", False)
    audience_keys = manifest.get("audiences", {})
    clip_count = sum(len(v) for v in audience_keys.values() if isinstance(v, dict))

    if m_version < app_version:
        issues.append(
            f"VOICE: manifest profileVersion {m_version} < app VOICE_PROFILE_VERSION {app_version}."
        )
    if not generated:
        warnings.append("VOICE: manifest.generated is false - run pregenerate_caly_voice.py with AZURE_SPEECH_KEY.")
    for aud in AUDIENCES:
        if aud not in audience_keys or not audience_keys.get(aud):
            warnings.append(f"VOICE: manifest missing pregenerated clips for `{aud}`.")
    return app_version, clip_count, generated


def check_app_js(issues: list[str], warnings: list[str]) -> None:
    if not APP_VOICE_JS.is_file():
        issues.append("VOICE: calyndra-app/js/caly-voice.js not found.")
        return
    text = APP_VOICE_JS.read_text(encoding="utf-8")
    if "speakAzure" not in text:
        issues.append("VOICE: caly-voice.js missing Azure-first speakAzure path.")
    if "ROBOTIC_HINTS" not in text:
        warnings.append("VOICE: caly-voice.js missing ROBOTIC_HINTS filter.")
    if "humanizeForSpeech" not in text:
        issues.append("VOICE: caly-voice.js missing humanizeForSpeech.")
    for aud in AUDIENCES:
        if f'{aud}:' not in text and f'"{aud}"' not in text:
            warnings.append(f"VOICE: caly-voice.js may missing browser fallback for `{aud}`.")


def write_report(
    profile_rows: list[tuple[str, str, str, str, str]],
    app_version: int,
    clip_count: int,
    generated: bool,
    issues: list[str],
    warnings: list[str],
) -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    overall = "PASS" if not issues else "FAIL"
    lines = [
        "# Voice profile QC report",
        "",
        f"Generated: **{now}**",
        "",
        f"**Overall:** {overall} ({len(issues)} issue(s), {len(warnings)} warning(s))",
        "",
        f"- App VOICE_PROFILE_VERSION: **{app_version}**",
        f"- Manifest clips: **{clip_count}**",
        f"- Manifest generated: **{generated}**",
        "",
        "## Azure Neural profiles (speech_tts.py)",
        "",
        "| Audience | Voice | Rate | Style | Status |",
        "|----------|-------|------|-------|--------|",
    ]
    for aud, voice, rate, style, status in profile_rows:
        lines.append(f"| {aud} | {voice} | {rate} | {style} | {status} |")
    lines.extend(["", "## Issues", ""])
    if issues:
        lines.extend(f"- {i}" for i in issues)
    else:
        lines.append("- None")
    lines.extend(["", "## Warnings", ""])
    if warnings:
        lines.extend(f"- {w}" for w in warnings)
    else:
        lines.append("- None")
    OUT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    issues: list[str] = []
    warnings: list[str] = []

    profile_rows = check_central_profiles(issues, warnings)
    app_version, clip_count, generated = check_manifest(issues, warnings)
    check_app_js(issues, warnings)

    write_report(profile_rows, app_version, clip_count, generated, issues, warnings)

    print(f"Voice QC: {'PASS' if not issues else 'FAIL'} - {len(issues)} issue(s), {len(warnings)} warning(s)")
    print(f"Wrote {OUT_REPORT.name}")
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
