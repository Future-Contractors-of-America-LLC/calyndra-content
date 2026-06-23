#!/usr/bin/env python3
"""Quality control for per-band Caly symbol art."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_SYMBOLS = ROOT.parent / "calyndra-app" / "assets" / "symbols"
OUT_MANIFEST = ROOT / "band-art-manifest.json"
OUT_REPORT = ROOT / "BAND_QC_REPORT.md"

# Audience key -> band folder, mascot nickname, age band (app selector values).
AUDIENCE_BAND_MAP: dict[str, dict[str, str]] = {
    "toddler": {"band": "sprout", "nickname": "Sprout", "age": "2-4"},
    "child": {"band": "bud", "nickname": "Bud", "age": "5-8"},
    "tween": {"band": "sprig", "nickname": "Sprig", "age": "9-12"},
    "teen": {"band": "vine", "nickname": "Vine", "age": "13-17"},
    "adult": {"band": "bloom", "nickname": "Bloom", "age": "18+"},
    "caregiver": {"band": "canopy", "nickname": "Canopy", "age": "caregiver"},
}

# Future band - landing / baby audience only; symbol QC not required yet.
FUTURE_AUDIENCE_BAND_MAP: dict[str, dict[str, str]] = {
    "baby": {"band": "seed", "nickname": "Seed", "age": "0-23mo"},
}

BANDS = tuple(entry["band"] for entry in AUDIENCE_BAND_MAP.values())
FUTURE_BANDS = tuple(entry["band"] for entry in FUTURE_AUDIENCE_BAND_MAP.values())

# Reverse lookup: band folder -> audience metadata (required bands only).
BAND_TO_AUDIENCE: dict[str, dict[str, str]] = {
    entry["band"]: {"audience": aud, "nickname": entry["nickname"], "age": entry["age"]}
    for aud, entry in AUDIENCE_BAND_MAP.items()
}


def md5(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()


def band_word_stems(band: str) -> set[str]:
    band_dir = APP_SYMBOLS / band
    if not band_dir.is_dir():
        return set()
    return {p.stem for p in band_dir.glob("*.png")}


def validate_band_folders() -> tuple[list[str], set[str]]:
    """Ensure required band folders exist and share the same word count."""
    issues: list[str] = []
    counts: dict[str, int] = {}
    stems_by_band: dict[str, set[str]] = {}

    for band in BANDS:
        band_dir = APP_SYMBOLS / band
        if not band_dir.is_dir():
            issues.append(f"MISSING FOLDER: `{band}` symbols dir does not exist.")
            counts[band] = 0
            stems_by_band[band] = set()
            continue
        stems = band_word_stems(band)
        stems_by_band[band] = stems
        counts[band] = len(stems)

    present = {b: c for b, c in counts.items() if c > 0}
    if len(set(present.values())) > 1:
        detail = ", ".join(f"{b}={c}" for b, c in sorted(present.items()))
        issues.append(f"WORD COUNT MISMATCH across band folders: {detail}.")

    if present:
        reference = next(iter(present))
        ref_stems = stems_by_band[reference]
        for band in BANDS:
            if band == reference or counts[band] == 0:
                continue
            missing = ref_stems - stems_by_band[band]
            extra = stems_by_band[band] - ref_stems
            if missing:
                issues.append(
                    f"MISSING FILES: `{band}` lacks {len(missing)} word(s) present in `{reference}` "
                    f"(e.g. {', '.join(sorted(missing)[:5])})."
                )
            if extra:
                issues.append(
                    f"EXTRA FILES: `{band}` has {len(extra)} word(s) not in `{reference}` "
                    f"(e.g. {', '.join(sorted(extra)[:5])})."
                )

    words: set[str] = set()
    for stems in stems_by_band.values():
        words |= stems
    if not words and not issues:
        issues.append("No symbol PNGs found in any required band folder.")

    return issues, words


def cross_band_hash_issues(word: str, hashes: dict[str, str]) -> list[str]:
    """Every required band must differ from every other for band-unique art."""
    found: list[str] = []
    bands_present = [b for b in BANDS if b in hashes]
    for i, left in enumerate(bands_present):
        for right in bands_present[i + 1 :]:
            if hashes[left] == hashes[right]:
                left_aud = BAND_TO_AUDIENCE[left]["audience"]
                right_aud = BAND_TO_AUDIENCE[right]["audience"]
                found.append(
                    f"IDENTICAL: `{word}` `{left}` ({left_aud}) and `{right}` ({right_aud}) "
                    f"share the same file hash."
                )
    return found


def main() -> int:
    folder_issues, words = validate_band_folders()
    issues: list[str] = list(folder_issues)

    if not words:
        print("No words to QC")
        for i in issues:
            print(i)
        return 1

    words_sorted = sorted(words)
    generated: dict[str, list[str]] = {}
    placeholder: list[str] = []

    for word in words_sorted:
        hashes: dict[str, str] = {}
        for band in BANDS:
            p = APP_SYMBOLS / band / f"{word}.png"
            if p.exists():
                hashes[band] = md5(p)

        if len(hashes) < len(BANDS):
            missing = [b for b in BANDS if b not in hashes]
            issues.append(f"INCOMPLETE: `{word}` missing in band folder(s): {', '.join(missing)}.")
            continue

        unique = len(set(hashes.values()))
        if unique == 1:
            placeholder.append(word)
            issues.append(
                f"PLACEHOLDER: `{word}` is identical in all {len(BANDS)} band folders "
                f"(not band-specific Caly art)."
            )
        elif unique == len(BANDS):
            generated[word] = list(BANDS)
            issues.extend(cross_band_hash_issues(word, hashes))
        else:
            partial = [b for b in BANDS if b in hashes]
            issues.append(f"PARTIAL: `{word}` has {unique} unique hashes across bands {partial}.")
            issues.extend(cross_band_hash_issues(word, hashes))

    manifest = {
        "updatedUtc": datetime.now(timezone.utc).isoformat(),
        "audienceBandMap": AUDIENCE_BAND_MAP,
        "futureAudienceBandMap": FUTURE_AUDIENCE_BAND_MAP,
        "generatedWords": generated,
        "placeholderWords": placeholder,
        "generatedCount": len(generated),
        "placeholderCount": len(placeholder),
        "issueCount": len(issues),
        "issues": issues,
    }
    OUT_MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    mapping_lines = [
        "## Band -> audience mapping",
        "",
        "| Band folder | Mascot | Audience | Age band |",
        "|-------------|--------|----------|----------|",
    ]
    for band in BANDS:
        meta = BAND_TO_AUDIENCE[band]
        mapping_lines.append(
            f"| `{band}` | {meta['nickname']} | {meta['audience']} | {meta['age']} |"
        )
    mapping_lines.extend(
        [
            "",
            "### Future (not required in symbol QC yet)",
            "",
            "| Band folder | Mascot | Audience | Age band |",
            "|-------------|--------|----------|----------|",
        ]
    )
    for aud, entry in FUTURE_AUDIENCE_BAND_MAP.items():
        mapping_lines.append(
            f"| `{entry['band']}` | {entry['nickname']} | {aud} | {entry['age']} |"
        )

    lines = [
        "# Band art QC report",
        "",
        f"Generated: **{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}**",
        "",
        "## Summary",
        "",
        "| Status | Count |",
        "|--------|-------|",
        f"| Band-unique symbols (pass) | {len(generated)} |",
        f"| Placeholder copies (fail) | {len(placeholder)} |",
        f"| Issues logged | {len(issues)} |",
        f"| Required band folders | {len(BANDS)} |",
        f"| Words checked | {len(words_sorted)} |",
        "",
        *mapping_lines,
        "",
        "## Pass: band-unique words",
        "",
        ", ".join(f"`{w}`" for w in sorted(generated)) or "(none)",
        "",
        "## Fail: placeholder (same file in every band folder)",
        "",
        "These still show old Sprout/human/object art for every age band until regenerated per mascot.",
        "",
        ", ".join(f"`{w}`" for w in sorted(placeholder)) or "(none)",
        "",
        "## Rules for regeneration",
        "",
        "- Match band portrait reference exactly (Sprout romper, Bud tee, Sprig tendrils, Vine hoodie, Bloom cardigan, Canopy dress).",
        "- **Do not** use Canopy dress/canopy leaves unless band is `canopy`.",
        "- Happy expression default; five fingers per visible hand.",
        "- Each band folder must contain the same word set; hashes must differ across sprout, bud, sprig, vine, bloom, and canopy.",
        "",
        "## Other media (manual check)",
        "",
        "- Videos/cartoons: still shared files; titles vary by audience but footage is not yet per-band.",
        "- Voice: Azure TTS profiles differ per audience in `speech_tts.py` (verify after central deploy).",
        "",
        "## Issues",
        "",
    ]
    if issues:
        lines.extend(f"- {i}" for i in issues)
    else:
        lines.append("- None")
    OUT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"QC: {len(generated)} pass, {len(placeholder)} placeholder, {len(issues)} issues")
    print(f"Wrote {OUT_MANIFEST.name} and {OUT_REPORT.name}")
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
