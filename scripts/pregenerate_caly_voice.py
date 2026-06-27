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
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_VOICE = ROOT.parent / "calyndra-app" / "content" / "voice"
SCRIPTS_PATH = ROOT / "games" / "caly-voice-scripts.json"
VOCAB_DIR = ROOT / "vocabulary"
APP_VOICE_JS = ROOT.parent / "calyndra-app" / "js" / "caly-voice.js"

# Optional ~/.calyndra/local.env from scripts/setup_local_speech_env.ps1
sys.path.insert(0, str(ROOT / "scripts"))
try:
    from load_local_env import load_local_env

    load_local_env()
except ImportError:
    pass

AUDIENCES = ("baby", "toddler", "child", "tween", "teen", "adult", "caregiver")
VOCAB_LABEL_LIMIT = 24

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


def app_profile_version() -> int:
    if not APP_VOICE_JS.is_file():
        return 2
    m = re.search(r"VOICE_PROFILE_VERSION\s*=\s*(\d+)", APP_VOICE_JS.read_text(encoding="utf-8"))
    return int(m.group(1)) if m else 2


def vocab_labels(audience: str) -> list[str]:
    path = VOCAB_DIR / f"{audience}-words.json"
    if not path.is_file():
        return []
    data = load_json(path)
    return [s.get("label", s.get("id", "")) for s in data.get("symbols", []) if s.get("label") or s.get("id")]


def collect_lines(audience: str, scripts: dict, labels: list[str]) -> dict[str, str]:
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

    templates = {k: v for k, v in band.items() if isinstance(v, str) and "{" in v}
    for label in labels[:VOCAB_LABEL_LIMIT]:
        for tkey, tpl in templates.items():
            spoken = tpl.replace("{word}", label)
            lines[f"{tkey}_{slug(label)}"] = spoken

    return lines


def write_skeleton_manifest(profile_version: int) -> Path:
    manifest_path = APP_VOICE / "manifest.json"
    if manifest_path.is_file():
        existing = load_json(manifest_path)
        if existing.get("generated") and existing.get("byText"):
            print(f"Keeping existing generated manifest ({len(existing.get('byText', {}))} clips).")
            # Ensure all audience keys exist for QC without wiping clips
            audiences = existing.setdefault("audiences", {})
            for aud in AUDIENCES:
                audiences.setdefault(aud, {})
            manifest_path.write_text(json.dumps(existing, indent=2), encoding="utf-8")
            return manifest_path
    manifest = {
        "version": profile_version,
        "profileVersion": profile_version,
        "generated": False,
        "audiences": {aud: {} for aud in AUDIENCES},
        "byText": {},
    }
    APP_VOICE.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest_path


def main() -> int:
    profile_version = app_profile_version()
    key = os.getenv("AZURE_SPEECH_KEY", "").strip()
    if not key:
        print("AZURE_SPEECH_KEY not set - writing manifest skeleton only.")
        print("Set the key and re-run to generate MP3 files for all 7 audiences.")
        path = write_skeleton_manifest(profile_version)
        print(f"Wrote {path}")
        return 0

    scripts = load_json(SCRIPTS_PATH)
    manifest: dict = {
        "version": profile_version,
        "profileVersion": profile_version,
        "generated": True,
        "audiences": {aud: {} for aud in AUDIENCES},
        "byText": {},
    }

    total_ok = total_fail = 0
    for audience in AUDIENCES:
        labels = vocab_labels(audience)
        out_dir = APP_VOICE / audience
        out_dir.mkdir(parents=True, exist_ok=True)
        lines = collect_lines(audience, scripts, labels)
        print(f"\n=== {audience}: {len(lines)} lines (vocab sample {len(labels[:VOCAB_LABEL_LIMIT])}) ===")
        for file_key, spoken in lines.items():
            rel = f"content/voice/{audience}/{file_key}.mp3"
            out_path = out_dir / f"{file_key}.mp3"
            if out_path.exists() and out_path.stat().st_size > 1024:
                print(f"  skip (cached) {file_key}")
                manifest["audiences"][audience][file_key] = rel
                manifest["byText"][text_hash(spoken)] = rel
                total_ok += 1
                continue
            audio, err, _ = synthesize_speech(spoken, audience)
            if err and "429" in str(err):
                time.sleep(2.0)
                audio, err, _ = synthesize_speech(spoken, audience)
            time.sleep(0.12)
            if err or not audio:
                print(f"  FAIL {file_key}: {err}")
                total_fail += 1
                continue
            out_path.write_bytes(audio)
            print(f"  ok {file_key} ({len(audio) // 1024}KB)")
            manifest["audiences"][audience][file_key] = rel
            manifest["byText"][text_hash(spoken)] = rel
            total_ok += 1

    manifest_path = APP_VOICE / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"\nManifest: {manifest_path}")
    print(f"Done: {total_ok} clips OK, {total_fail} failed across {len(AUDIENCES)} audiences.")
    return 0 if total_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
