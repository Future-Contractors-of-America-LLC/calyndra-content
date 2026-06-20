# -*- coding: utf-8 -*-
"""Batch-generate Caly voice MP3 clips via Azure Neural TTS.

Requires AZURE_SPEECH_KEY (and optional AZURE_SPEECH_REGION, default eastus2).
Outputs to calyndra-app/content/voice/{audience}/ and writes manifest.json.

Usage:
  cd calyndra-content
  set AZURE_SPEECH_KEY=...
  python scripts/pregenerate_caly_voice.py
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_VOICE = ROOT.parent / "calyndra-app" / "content" / "voice"
SCRIPTS_PATH = ROOT / "games" / "caly-voice-scripts.json"
TODDLER_VOCAB = ROOT.parent / "calyndra-app" / "content" / "toddler-core.json"
CHILD_VOCAB = ROOT.parent / "calyndra-app" / "content" / "child-expanded.json"

# Allow import of speech_tts from calyndra-central
CENTRAL = ROOT.parent / "calyndra-central"
sys.path.insert(0, str(CENTRAL))
from speech_tts import synthesize_speech  # noqa: E402


def slug(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    return s[:80] or "line"


def norm_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def text_hash(text: str) -> str:
    return hashlib.sha256(norm_text(text).encode("utf-8")).hexdigest()[:16]


def load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def collect_lines(audience: str, scripts: dict, vocab_labels: list[str]) -> dict[str, str]:
    """Return {file_key: spoken_text}."""
    band = scripts.get(audience, {})
    lines: dict[str, str] = {}

    for key, val in band.items():
        if key == "caregiver_cue":
            continue
        if isinstance(val, list):
            for i, line in enumerate(val):
                lines[f"{key}_{i}"] = line
        elif isinstance(val, str) and "{" not in val:
            lines[key] = val

    templates = {
        k: v for k, v in band.items() if isinstance(v, str) and "{" in v
    }
    for label in vocab_labels[:24]:
        for tkey, tpl in templates.items():
            spoken = tpl.replace("{word}", label)
            lines[f"{tkey}_{slug(label)}"] = spoken

    return lines


def main() -> int:
    key = os.getenv("AZURE_SPEECH_KEY", "").strip()
    if not key:
        print("AZURE_SPEECH_KEY not set — writing manifest skeleton only.")
        print("Set the key and re-run to generate MP3 files.")
        manifest = {"version": 1, "generated": False, "audiences": {}, "byText": {}}
        APP_VOICE.mkdir(parents=True, exist_ok=True)
        manifest_path = APP_VOICE / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        print(f"Wrote {manifest_path}")
        return 0

    scripts = load_json(SCRIPTS_PATH)
    toddler_labels = [s["label"] for s in load_json(TODDLER_VOCAB).get("symbols", [])]
    child_labels = [s["label"] for s in load_json(CHILD_VOCAB).get("symbols", [])]

    manifest: dict = {
        "version": 1,
        "generated": True,
        "audiences": {"toddler": {}, "child": {}},
        "byText": {},
    }

    for audience, labels in (("toddler", toddler_labels), ("child", child_labels)):
        out_dir = APP_VOICE / audience
        out_dir.mkdir(parents=True, exist_ok=True)
        lines = collect_lines(audience, scripts, labels)
        print(f"\n=== {audience}: {len(lines)} lines ===")
        for file_key, spoken in lines.items():
            rel = f"content/voice/{audience}/{file_key}.mp3"
            out_path = APP_VOICE / audience / f"{file_key}.mp3"
            if out_path.exists() and out_path.stat().st_size > 1024:
                print(f"  skip (cached) {file_key}")
            else:
                audio, err, _ = synthesize_speech(spoken, audience)
                if err or not audio:
                    print(f"  FAIL {file_key}: {err}")
                    continue
                out_path.write_bytes(audio)
                print(f"  ok {file_key} ({len(audio)//1024}KB)")
            manifest["audiences"][audience][file_key] = rel
            manifest["byText"][text_hash(spoken)] = rel

    manifest_path = APP_VOICE / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"\nManifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
