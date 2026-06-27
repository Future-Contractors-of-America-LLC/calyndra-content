"""Load ~/.calyndra/local.env into os.environ (optional local dev secrets)."""

from __future__ import annotations

import os
from pathlib import Path


def load_local_env() -> bool:
    env_file = Path.home() / ".calyndra" / "local.env"
    if not env_file.is_file():
        return False
    for line in env_file.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if key and (key not in os.environ or not str(os.environ.get(key, "")).strip()):
            os.environ[key] = val
    return bool(os.getenv("AZURE_SPEECH_KEY"))


if __name__ == "__main__":
    ok = load_local_env()
    print("loaded" if ok else "missing")
