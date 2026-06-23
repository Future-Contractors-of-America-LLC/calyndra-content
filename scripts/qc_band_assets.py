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

BANDS = ("sprout", "bud", "sprig", "vine", "bloom", "canopy")
AUDIENCE = {
    "sprout": "toddler / Caly Sprout",
    "bud": "child / Caly Bud",
    "sprig": "tween / Caly Sprig",
    "vine": "teen / Caly Vine",
    "bloom": "adult / Caly Bloom",
    "canopy": "caregiver / Caly Canopy",
}


def md5(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()


def main() -> int:
    sprout_dir = APP_SYMBOLS / "sprout"
    if not sprout_dir.is_dir():
        print("Missing sprout symbols dir")
        return 1

    words = sorted(p.stem for p in sprout_dir.glob("*.png"))
    generated: dict[str, list[str]] = {}
    placeholder: list[str] = []
    issues: list[str] = []

    for word in words:
        hashes: dict[str, str] = {}
        for band in BANDS:
            p = APP_SYMBOLS / band / f"{word}.png"
            if p.exists():
                hashes[band] = md5(p)
        unique = len(set(hashes.values()))
        if unique == 1 and len(hashes) == len(BANDS):
            placeholder.append(word)
            issues.append(f"PLACEHOLDER: `{word}` is identical in all 6 band folders (not band-specific Caly art).")
        elif unique == len(BANDS):
            generated[word] = list(BANDS)
        else:
            partial = [b for b in BANDS if b in hashes]
            issues.append(f"PARTIAL: `{word}` has {unique} unique hashes across bands {partial}.")

    # Cross-band: sprout generated vs canopy should differ
    for word in generated:
        if hashes := {b: md5(APP_SYMBOLS / b / f"{word}.png") for b in BANDS}:
            if hashes.get("sprout") == hashes.get("canopy"):
                issues.append(f"FAIL: `{word}` sprout and canopy files are identical (wrong mascot).")

    manifest = {
        "updatedUtc": datetime.now(timezone.utc).isoformat(),
        "generatedWords": generated,
        "placeholderWords": placeholder,
        "generatedCount": len(generated),
        "placeholderCount": len(placeholder),
        "issueCount": len(issues),
        "issues": issues,
    }
    OUT_MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    lines = [
        "# Band art QC report",
        "",
        f"Generated: **{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}**",
        "",
        "## Summary",
        "",
        f"| Status | Count |",
        f"|--------|-------|",
        f"| Band-unique symbols (pass) | {len(generated)} |",
        f"| Placeholder copies (fail) | {len(placeholder)} |",
        f"| Issues logged | {len(issues)} |",
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
        "",
        "## Other media (manual check)",
        "",
        "- Videos/cartoons: still shared files; titles vary by audience but footage is not yet per-band.",
        "- Voice: Azure TTS profiles differ per audience in `speech_tts.py` (verify after central deploy).",
        "",
        "## Issues",
        "",
    ]
    lines.extend(f"- {i}" for i in issues) or lines.append("- None")
    OUT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"QC: {len(generated)} pass, {len(placeholder)} placeholder, {len(issues)} issues")
    print(f"Wrote {OUT_MANIFEST.name} and {OUT_REPORT.name}")
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
