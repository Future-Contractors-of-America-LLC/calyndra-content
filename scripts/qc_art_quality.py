#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Art quality QC - symbol PNG coverage, dimensions, manifest alignment, sidecar handFingers."""

from __future__ import annotations

import json
import struct
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_SYMBOLS = ROOT.parent / "calyndra-app" / "assets" / "symbols"
VOCAB_DIR = ROOT / "vocabulary"
META_DIR = ROOT / "symbols" / "meta"
MANIFEST_PATH = ROOT / "band-art-manifest.json"
OUT_REPORT = ROOT / "ART_QC_REPORT.md"

AUDIENCES = ("baby", "toddler", "child", "tween", "teen", "adult", "caregiver")
MIN_DIM = 128
MAX_DIM = 2048
TARGET_DIM = 512
BOOTSTRAP_BANDS = ("seed",)
REQUIRED_BANDS = ("sprout", "bud", "sprig", "vine", "bloom", "canopy")
FAMILY_BAND_REQUIREMENTS: dict[str, tuple[str, ...]] = {
    "little_brother": ("bud", "sprig", "vine", "bloom", "canopy"),
    "best_friend": ("bud", "sprig", "vine", "bloom", "canopy"),
}
HAND_VISIBLE_WORDS = frozenset({
    "help", "more", "stop", "wait", "please", "love", "hug", "clap", "wash", "wet",
    "listen", "open", "close", "want", "need", "modeling", "scaffold", "prompt-wait",
    "reinforcement", "yes", "no", "again", "celebrate", "hug", "cuddle", "peek",
    "up", "down", "hot", "cold", "dry", "big", "little", "friend", "mommy", "daddy",
    "symbol_help", "symbol_more",
})


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def png_dimensions(path: Path) -> tuple[int, int] | None:
    try:
        with path.open("rb") as f:
            if f.read(8) != b"\x89PNG\r\n\x1a\n":
                return None
            f.read(4)  # IHDR chunk length (13)
            if f.read(4) != b"IHDR":
                return None
            w, h = struct.unpack(">II", f.read(8))
            return w, h
    except OSError:
        return None


def asset_to_path(image_asset: str) -> Path:
    """Map vocabulary imageAsset to calyndra-app path."""
    rel = image_asset.replace("assets/symbols/", "")
    return APP_SYMBOLS / rel.replace("/", "\\").replace("\\", "/")


def resolve_symbol_png(band: str, word_id: str) -> Path | None:
    """Return PNG path, falling back sprout->seed for bootstrap band."""
    direct = APP_SYMBOLS / band / f"{word_id}.png"
    if direct.is_file():
        return direct
    if band == "seed":
        fallback = APP_SYMBOLS / "sprout" / f"{word_id}.png"
        if fallback.is_file():
            return fallback
    return None


def check_manifest_assets(issues: list[str], warnings: list[str]) -> list[tuple[str, int, int, str]]:
    """Every manifest word must exist in each required band folder."""
    rows: list[tuple[str, int, int, str]] = []
    if not MANIFEST_PATH.is_file():
        issues.append("MANIFEST: band-art-manifest.json missing - run qc_band_assets.py.")
        return rows
    manifest = load_json(MANIFEST_PATH)
    words = sorted(set(manifest.get("generatedWords", {})) | set(manifest.get("placeholderWords", [])))
    if not words:
        issues.append("MANIFEST: no words listed in band-art-manifest.json.")
        return rows
    for band in REQUIRED_BANDS:
        missing = 0
        for word in words:
            bands_for_word = FAMILY_BAND_REQUIREMENTS.get(word, REQUIRED_BANDS)
            if band not in bands_for_word:
                continue
            if not (APP_SYMBOLS / band / f"{word}.png").is_file():
                missing += 1
                issues.append(f"MANIFEST: `{word}` missing in `{band}/`.")
        status = "PASS" if missing == 0 else "FAIL"
        rows.append((band, len(words) - missing, len(words), status))
    seed_missing = sum(1 for w in words if not resolve_symbol_png("seed", w))
    if seed_missing:
        warnings.append(f"BOOTSTRAP: seed/ missing {seed_missing} PNG(s) (sprout fallback may apply).")
    rows.insert(0, ("seed (bootstrap)", len(words) - seed_missing, len(words), "WARN" if seed_missing else "PASS"))
    return rows


def check_vocab_assets(issues: list[str], warnings: list[str]) -> list[tuple[str, int, int, str]]:
    """Expanded vocabulary coverage — ship gate requires 100%."""
    rows: list[tuple[str, int, int, str]] = []
    for aud in AUDIENCES:
        vocab_path = VOCAB_DIR / f"{aud}-words.json"
        if not vocab_path.is_file():
            issues.append(f"VOCAB: missing `{vocab_path.name}`.")
            rows.append((aud, 0, 0, "FAIL"))
            continue
        vocab = load_json(vocab_path)
        symbols = vocab.get("symbols", [])
        missing = 0
        for sym in symbols:
            asset = sym.get("imageAsset", "")
            word_id = sym.get("id", "")
            if not asset:
                missing += 1
                continue
            png = asset_to_path(asset)
            if not png.is_file() and aud == "baby":
                resolved = resolve_symbol_png("seed", word_id)
                if resolved and resolved.is_file():
                    continue
            if not png.is_file():
                missing += 1
            if sym.get("placeholderArt") is True:
                warnings.append(f"PLACEHOLDER: `{aud}`/`{word_id}` has placeholderArt=true.")
        if missing:
            issues.append(f"VOCAB: `{aud}` missing {missing}/{len(symbols)} imageAsset PNG(s).")
        rows.append((aud, len(symbols) - missing, len(symbols), "PASS" if missing == 0 else "FAIL"))
    return rows


def check_dimensions(issues: list[str], warnings: list[str]) -> tuple[int, int]:
    ok = bad = 0
    if not APP_SYMBOLS.is_dir():
        issues.append(f"SYMBOLS: `{APP_SYMBOLS}` not found.")
        return 0, 0
    for png in sorted(APP_SYMBOLS.rglob("*.png")):
        dims = png_dimensions(png)
        if dims is None:
            bad += 1
            issues.append(f"DIM: unreadable PNG `{png.name}` in `{png.parent.name}`.")
            continue
        w, h = dims
        if w != h:
            warnings.append(f"DIM: `{png.parent.name}/{png.name}` not square ({w}x{h}).")
        if w < MIN_DIM or h < MIN_DIM or w > MAX_DIM or h > MAX_DIM:
            bad += 1
            warnings.append(f"DIM: `{png.parent.name}/{png.name}` size {w}x{h} outside {MIN_DIM}-{MAX_DIM} - run optimize_symbol_assets.py.")
        elif w != TARGET_DIM:
            warnings.append(f"DIM: `{png.parent.name}/{png.name}` is {w}x{h} (target {TARGET_DIM}).")
            ok += 1
        else:
            ok += 1
    return ok, bad


def check_manifest(issues: list[str], warnings: list[str]) -> tuple[int, int, int]:
    if not MANIFEST_PATH.is_file():
        issues.append("MANIFEST: band-art-manifest.json missing - run qc_band_assets.py.")
        return 0, 0, 0
    manifest = load_json(MANIFEST_PATH)
    placeholders = manifest.get("placeholderWords", [])
    for word in placeholders:
        issues.append(f"MANIFEST: `{word}` still marked placeholder (identical across bands).")
    bootstrap = set(manifest.get("bootstrapBands", []))
    generated = set(manifest.get("generatedWords", {}))
    issue_count = manifest.get("issueCount", 0)
    if issue_count:
        for item in manifest.get("issues", [])[:20]:
            warnings.append(f"MANIFEST: {item}")
        if issue_count > 20:
            warnings.append(f"MANIFEST: ... and {issue_count - 20} more issue(s) in manifest.")
    return len(generated), len(placeholders), len(bootstrap)


def check_sidecars(issues: list[str], warnings: list[str]) -> tuple[int, int, int]:
    reviewed = 0
    bad_fingers = 0
    missing_for_hands = 0
    if not META_DIR.is_dir():
        warnings.append("META: symbols/meta/ not created yet - sidecar QC skipped (optional).")
        return 0, 0, 0
    for sidecar in sorted(META_DIR.rglob("*.json")):
        try:
            meta = load_json(sidecar)
        except json.JSONDecodeError:
            issues.append(f"META: invalid JSON `{sidecar.relative_to(ROOT)}`.")
            continue
        reviewed += 1
        fingers = meta.get("handFingers")
        word_id = meta.get("wordId", sidecar.stem)
        if fingers is None:
            continue
        if fingers in (0, "none", "n/a"):
            continue
        if fingers != 5:
            bad_fingers += 1
            issues.append(f"META: `{sidecar.relative_to(ROOT)}` handFingers={fingers!r} (require 5).")
    if META_DIR.is_dir():
        for word in HAND_VISIBLE_WORDS:
            for band_dir in APP_SYMBOLS.iterdir():
                if not band_dir.is_dir():
                    continue
                png = band_dir / f"{word}.png"
                sidecar = META_DIR / band_dir.name / f"{word}.json"
                if png.is_file() and not sidecar.is_file():
                    missing_for_hands += 1
        if missing_for_hands:
            warnings.append(
                f"META: {missing_for_hands} hand-visible symbol(s) lack sidecar metadata (optional until art review)."
            )
    return reviewed, bad_fingers, missing_for_hands


def write_report(
    manifest_rows: list[tuple[str, int, int, str]],
    vocab_rows: list[tuple[str, int, int, str]],
    dim_ok: int,
    dim_bad: int,
    gen_count: int,
    ph_count: int,
    bootstrap_count: int,
    meta_reviewed: int,
    meta_bad: int,
    issues: list[str],
    warnings: list[str],
) -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    overall = "PASS" if not issues else "FAIL"
    lines = [
        "# Art quality QC report",
        "",
        f"Generated: **{now}**",
        "",
        f"**Overall:** {overall} ({len(issues)} issue(s), {len(warnings)} warning(s))",
        "",
        "## Manifest band folders (ship gate)",
        "",
        "| Band | PNGs OK | Manifest words | Status |",
        "|------|---------|----------------|--------|",
    ]
    for band, ok, total, status in manifest_rows:
        lines.append(f"| {band} | {ok} | {total} | {status} |")
    lines.extend([
        "",
        "## Expanded vocabulary coverage (ship gate)",
        "",
        "| Audience | PNGs OK | Total symbols | Status |",
        "|----------|---------|---------------|--------|",
    ])
    for aud, ok, total, status in vocab_rows:
        lines.append(f"| {aud} | {ok} | {total} | {status} |")
    lines.extend([
        "",
        "## Dimensions",
        "",
        f"- Pass (readable): **{dim_ok}** PNG(s)",
        f"- Fail (out of range): **{dim_bad}**",
        f"- Target: **{TARGET_DIM}x{TARGET_DIM}** (warnings if different)",
        "",
        "## Manifest",
        "",
        f"- Band-unique words: **{gen_count}**",
        f"- Placeholder words: **{ph_count}**",
        f"- Bootstrap bands: **{bootstrap_count}**",
        "",
        "## Sidecar metadata",
        "",
        f"- Reviewed sidecars: **{meta_reviewed}**",
        f"- Bad handFingers: **{meta_bad}**",
        "",
        "## Issues",
        "",
    ])
    if issues:
        lines.extend(f"- {i}" for i in issues)
    else:
        lines.append("- None")
    lines.extend(["", "## Warnings", ""])
    if warnings:
        lines.extend(f"- {w}" for w in warnings[:50])
        if len(warnings) > 50:
            lines.append(f"- ... and {len(warnings) - 50} more")
    else:
        lines.append("- None")
    OUT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    issues: list[str] = []
    warnings: list[str] = []

    manifest_rows = check_manifest_assets(issues, warnings)
    vocab_rows = check_vocab_assets(issues, warnings)
    dim_ok, dim_bad = check_dimensions(issues, warnings)
    gen_count, ph_count, bootstrap_count = check_manifest(issues, warnings)
    meta_reviewed, meta_bad, _ = check_sidecars(issues, warnings)

    write_report(
        manifest_rows,
        vocab_rows, dim_ok, dim_bad, gen_count, ph_count, bootstrap_count,
        meta_reviewed, meta_bad, issues, warnings,
    )

    print(f"Art QC: {'PASS' if not issues else 'FAIL'} - {len(issues)} issue(s), {len(warnings)} warning(s)")
    print(f"Wrote {OUT_REPORT.name}")
    for i in issues[:10]:
        print(f"  ISSUE: {i}")
    if len(issues) > 10:
        print(f"  ... and {len(issues) - 10} more (see {OUT_REPORT.name})")
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
