#!/usr/bin/env python3
"""Full Calyndra ecosystem QC - runs all content QC scripts plus cross-repo checks."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT.parent / "calyndra-app"
APP_CONTENT = APP / "content"
APP_SYMBOLS = APP / "assets" / "symbols"
CENTRAL_TTS = ROOT.parent / "calyndra-central" / "speech_tts.py"
OUT_REPORT = ROOT / "ECOSYSTEM_QC_REPORT.md"

AUDIENCES = ("baby", "toddler", "child", "tween", "teen", "adult", "caregiver")
YOUNGER_BANDS = ("baby", "toddler", "child")
CARTOON_BANDS = ("baby", "toddler", "child", "tween", "teen", "adult")
MIN_NEW_GAMES = 5
MIN_SING_ALONG = 5

QC_SCRIPTS = (
    "qc_band_assets.py",
    "qc_art_quality.py",
    "qc_voice_profiles.py",
    "qc_games_catalog.py",
    "qc_sing_along_catalog.py",
    "qc_cartoon_catalog.py",
)

SYNC_FILES: tuple[tuple[str, str], ...] = (
    ("band-art-manifest.json", "band-art-manifest.json"),
    ("games/band-games-catalog.json", "band-games-catalog.json"),
    ("games/sing-along-catalog.json", "sing-along-catalog.json"),
    ("games/caly-voice-scripts.json", "caly-voice-scripts.json"),
    ("caly_character_registry.json", "caly_character_registry.json"),
    ("videos/caly_friends_catalog.json", "videos/caly_friends_catalog.json"),
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def run_qc_script(name: str) -> tuple[int, str]:
    script = ROOT / "scripts" / name
    r = subprocess.run(
        [sys.executable, str(script)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    out = (r.stdout or "") + (r.stderr or "")
    return r.returncode, out.strip()


def check_vocab(issues: list[str]) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    for aud in AUDIENCES:
        words = ROOT / "vocabulary" / f"{aud}-words.json"
        phrases = ROOT / "vocabulary" / f"{aud}-phrases.json"
        words_ok = words.is_file()
        phrases_ok = phrases.is_file()
        if not words_ok:
            issues.append(f"VOCAB: missing `{words.name}` for `{aud}`.")
        if not phrases_ok:
            issues.append(f"VOCAB: missing `{phrases.name}` for `{aud}`.")
        status = "PASS" if words_ok and phrases_ok else "FAIL"
        rows.append((aud, "yes" if words_ok else "no", status))
    return rows


def check_games(issues: list[str]) -> list[tuple[str, int, str]]:
    catalog = load_json(ROOT / "games" / "band-games-catalog.json")
    rows: list[tuple[str, int, str]] = []
    for aud in AUDIENCES:
        block = catalog.get("audiences", {}).get(aud, {})
        new_count = sum(1 for g in block.get("games", []) if g.get("isNew"))
        status = "PASS" if new_count >= MIN_NEW_GAMES else "FAIL"
        if new_count < MIN_NEW_GAMES:
            issues.append(f"GAMES: `{aud}` has {new_count} new games (need {MIN_NEW_GAMES}+).")
        rows.append((aud, new_count, status))
    return rows


def check_sing_along(issues: list[str]) -> list[tuple[str, int, str]]:
    catalog = load_json(ROOT / "games" / "sing-along-catalog.json")
    rows: list[tuple[str, int, str]] = []
    for aud in YOUNGER_BANDS:
        block = catalog.get("audiences", {}).get(aud, {})
        count = len(block.get("episodes", []))
        status = "PASS" if count >= MIN_SING_ALONG else "FAIL"
        if count < MIN_SING_ALONG:
            issues.append(f"SING-ALONG: `{aud}` has {count} episodes (need {MIN_SING_ALONG}+).")
        rows.append((aud, count, status))
    return rows


def check_cartoon_catalog(issues: list[str]) -> list[tuple[str, int, str]]:
    catalog = load_json(ROOT / "videos" / "caly_friends_catalog.json")
    episodes = catalog.get("episodes", [])
    by_band: dict[str, int] = {b: 0 for b in CARTOON_BANDS}
    for ep in episodes:
        band = ep.get("band")
        if band in by_band:
            by_band[band] += 1
    rows: list[tuple[str, int, str]] = []
    for band in CARTOON_BANDS:
        count = by_band[band]
        status = "PASS" if count >= 1 else "FAIL"
        if count < 1:
            issues.append(f"CARTOON: no Caly and Friends episode for band `{band}`.")
        rows.append((band, count, status))
    if not episodes:
        issues.append("CARTOON: caly_friends_catalog.json has zero episodes.")
    return rows


def check_symbol_counts(issues: list[str]) -> list[tuple[str, int, int, str]]:
    manifest_path = ROOT / "band-art-manifest.json"
    if not manifest_path.is_file():
        issues.append("MANIFEST: band-art-manifest.json missing - run qc_band_assets.py first.")
        return []

    manifest = load_json(manifest_path)
    expected_words = set(manifest.get("generatedWords", {})) | set(manifest.get("placeholderWords", []))
    expected_count = len(expected_words)

    band_map = manifest.get("audienceBandMap", {})
    rows: list[tuple[str, int, int, str]] = []
    for aud, entry in band_map.items():
        band = entry["band"]
        band_dir = APP_SYMBOLS / band
        actual = len(list(band_dir.glob("*.png"))) if band_dir.is_dir() else 0
        status = "PASS" if actual == expected_count else "FAIL"
        if actual != expected_count:
            issues.append(
                f"SYMBOLS: `{band}` ({aud}) has {actual} PNGs, manifest expects {expected_count}."
            )
        rows.append((band, actual, expected_count, status))
    return rows


def check_baby_in_index(issues: list[str]) -> tuple[str, str]:
    app_index = APP / "app" / "index.html"
    if not app_index.is_file():
        issues.append("INDEX: calyndra-app/app/index.html missing.")
        return "app/index.html", "FAIL"
    text = app_index.read_text(encoding="utf-8")
    if 'value="baby"' in text and "baby:" in text:
        return "app/index.html", "PASS"
    issues.append("INDEX: baby audience not wired in app/index.html.")
    return "app/index.html", "FAIL"


def check_speech_tts_all_neural(issues: list[str]) -> tuple[str, str]:
    """All seven audiences must use Azure Neural voices with human-like styles."""
    if not CENTRAL_TTS.is_file():
        issues.append("TTS: calyndra-central/speech_tts.py not found.")
        return "speech_tts.py neural profiles (7 bands)", "FAIL"
    text = CENTRAL_TTS.read_text(encoding="utf-8")
    ok = True
    for aud in AUDIENCES:
        if f'"{aud}"' not in text:
            issues.append(f"TTS: missing `{aud}` in VOICE_PROFILES.")
            ok = False
            continue
        # crude but fast: each audience block should reference Neural voice
        block = re.search(rf'"{aud}"\s*:\s*\{{[^}}]+\}}', text, re.DOTALL)
        if not block or "Neural" not in block.group(0):
            issues.append(f"TTS: `{aud}` profile missing Azure Neural voice.")
            ok = False
    return "speech_tts.py neural profiles (7 bands)", "PASS" if ok else "FAIL"


def sync_manifests_to_app() -> list[str]:
    copied: list[str] = []
    for src_rel, dest_rel in SYNC_FILES:
        src = ROOT / src_rel
        if not src.is_file():
            continue
        dest = APP_CONTENT / dest_rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        copied.append(dest_rel)

    vocab_src = ROOT / "vocabulary"
    for src in sorted(vocab_src.glob("*.json")):
        dest = APP_CONTENT / src.name
        shutil.copy2(src, dest)
        copied.append(src.name)
    return copied


def write_report(
    qc_results: list[tuple[str, int, str]],
    vocab_rows: list[tuple[str, str, str]],
    games_rows: list[tuple[str, int, str]],
    sing_rows: list[tuple[str, int, str]],
    cartoon_rows: list[tuple[str, int, str]],
    symbol_rows: list[tuple[str, int, int, str]],
    index_check: tuple[str, str],
    tts_check: tuple[str, str],
    art_qc: tuple[str, str],
    voice_qc: tuple[str, str],
    synced: list[str],
    issues: list[str],
) -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    overall = "PASS" if not issues else "FAIL"

    lines = [
        "# Ecosystem QC report",
        "",
        f"Generated: **{now}**",
        "",
        f"**Overall:** {overall} ({len(issues)} issue(s))",
        "",
        "## Summary",
        "",
        "| Check | Result |",
        "|-------|--------|",
    ]
    for name, code, _out in qc_results:
        lines.append(f"| `{name}` | {'PASS' if code == 0 else 'FAIL'} |")
    lines.append(f"| Vocabulary files (words per band) | {'PASS' if all(r[2]=='PASS' for r in vocab_rows) else 'FAIL'} |")
    lines.append(f"| Games catalog (5+ new per band) | {'PASS' if all(r[2]=='PASS' for r in games_rows) else 'FAIL'} |")
    lines.append(f"| Sing-along (5+ baby/toddler/child) | {'PASS' if all(r[2]=='PASS' for r in sing_rows) else 'FAIL'} |")
    lines.append(f"| Caly and Friends episodes | {'PASS' if all(r[2]=='PASS' for r in cartoon_rows) else 'FAIL'} |")
    lines.append(f"| Symbol PNG counts vs manifest | {'PASS' if all(r[3]=='PASS' for r in symbol_rows) else 'FAIL'} |")
    lines.append(f"| {index_check[0]} baby audience | {index_check[1]} |")
    lines.append(f"| {tts_check[0]} | {tts_check[1]} |")
    lines.append(f"| Art quality (`qc_art_quality.py`) | {art_qc[1]} |")
    lines.append(f"| Voice profiles (`qc_voice_profiles.py`) | {voice_qc[1]} |")
    lines.append(f"| Manifest sync to calyndra-app/content | {len(synced)} file(s) |")

    lines.extend(["", "## Vocabulary", "", "| Band | words.json | Status |", "|------|------------|--------|"])
    for aud, words_ok, status in vocab_rows:
        lines.append(f"| {aud} | {words_ok} | {status} |")

    lines.extend(["", "## Games (new per band)", "", "| Band | New games | Status |", "|------|-----------|--------|"])
    for aud, count, status in games_rows:
        lines.append(f"| {aud} | {count} | {status} |")

    lines.extend(["", "## Sing-along episodes", "", "| Band | Episodes | Status |", "|------|----------|--------|"])
    for aud, count, status in sing_rows:
        lines.append(f"| {aud} | {count} | {status} |")

    lines.extend(["", "## Caly and Friends", "", "| Band | Episodes | Status |", "|------|----------|--------|"])
    for band, count, status in cartoon_rows:
        lines.append(f"| {band} | {count} | {status} |")

    lines.extend([
        "",
        "## Symbol folders vs manifest",
        "",
        "| Band folder | PNG count | Manifest expected | Status |",
        "|-------------|-----------|-------------------|--------|",
    ])
    for band, actual, expected, status in symbol_rows:
        lines.append(f"| `{band}` | {actual} | {expected} | {status} |")

    lines.extend(["", "## Synced to calyndra-app/content", ""])
    if synced:
        lines.extend(f"- `{p}`" for p in synced)
    else:
        lines.append("- (none)")

    lines.extend(["", "## Sub-script output", ""])
    for name, code, out in qc_results:
        lines.append(f"### {name} (exit {code})")
        lines.append("")
        lines.append("```")
        lines.append(out or "(no output)")
        lines.append("```")
        lines.append("")

    lines.extend(["", "## Issues", ""])
    if issues:
        lines.extend(f"- {i}" for i in issues)
    else:
        lines.append("- None")

    OUT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    issues: list[str] = []
    qc_results: list[tuple[str, int, str]] = []

    print("=== Running content QC scripts ===")
    for script in QC_SCRIPTS:
        code, out = run_qc_script(script)
        qc_results.append((script, code, out))
        print(f"  {script}: {'PASS' if code == 0 else 'FAIL'}")
        if code != 0:
            issues.append(f"QC script `{script}` exited {code}.")

    print("\n=== Ecosystem checks ===")
    vocab_rows = check_vocab(issues)
    games_rows = check_games(issues)
    sing_rows = check_sing_along(issues)
    cartoon_rows = check_cartoon_catalog(issues)
    symbol_rows = check_symbol_counts(issues)
    index_check = check_baby_in_index(issues)
    tts_check = check_speech_tts_all_neural(issues)
    art_exit = next((c for n, c, _ in qc_results if n == "qc_art_quality.py"), 1)
    voice_exit = next((c for n, c, _ in qc_results if n == "qc_voice_profiles.py"), 1)
    art_qc = ("qc_art_quality.py", "PASS" if art_exit == 0 else "FAIL")
    voice_qc = ("qc_voice_profiles.py", "PASS" if voice_exit == 0 else "FAIL")

    print("\n=== Syncing manifests to calyndra-app/content ===")
    synced = sync_manifests_to_app()
    print(f"  Copied {len(synced)} file(s)")

    write_report(
        qc_results,
        vocab_rows,
        games_rows,
        sing_rows,
        cartoon_rows,
        symbol_rows,
        index_check,
        tts_check,
        art_qc,
        voice_qc,
        synced,
        issues,
    )
    print(f"\nWrote {OUT_REPORT.name}")
    print(f"Ecosystem QC: {'PASS' if not issues else 'FAIL'} ({len(issues)} issue(s))")
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
