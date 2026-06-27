#!/usr/bin/env python3
"""Fix catalog videoProfile when WebM exists but profile stuck on draft."""

from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from caly_video_probe import probe_resolution, profile_from_resolution  # noqa: E402

CATALOG = ROOT / "videos" / "caly_friends_catalog.json"
APP_VIDEOS = ROOT.parent / "calyndra-app" / "videos"
APP_CATALOG = ROOT.parent / "calyndra-app" / "content" / "videos" / "caly_friends_catalog.json"
FLUTTER_VIDEOS = ROOT.parent / "calyndra-mobile-flutter" / "assets" / "videos"
MIN_BYTES = 500_000


def find_webm(name: str, *, allow_stub: bool = False) -> Path | None:
    min_size = 1 if allow_stub else MIN_BYTES
    for base in (APP_VIDEOS, FLUTTER_VIDEOS, ROOT / "videos"):
        p = base / name
        if p.is_file() and p.stat().st_size >= min_size:
            return p
    return None


def infer_profile(size_bytes: int) -> tuple[str, str]:
    if size_bytes >= 25_000_000:
        return "uhd", "3840x2160"
    if size_bytes >= 3_000_000:
        return "hd", "1920x1080"
    return "hd", "1280x720"


def profile_for_file(path: Path) -> tuple[str, str]:
    probed = probe_resolution(path)
    if probed:
        w, h = probed
        profile = profile_from_resolution(w, h)
        if profile == "sub-hd":
            profile = "draft"
        return profile, f"{w}x{h}"
    return infer_profile(path.stat().st_size)


def main() -> int:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    updated = 0
    APP_VIDEOS.mkdir(parents=True, exist_ok=True)
    for ep in catalog.get("episodes", []):
        webm_name = ep.get("webm", "")
        src = find_webm(webm_name, allow_stub=True)
        dest = APP_VIDEOS / webm_name
        if src:
            if not dest.is_file() or dest.stat().st_size < src.stat().st_size:
                shutil.copy2(src, dest)
        elif not dest.is_file():
            continue
        size = dest.stat().st_size
        if size < MIN_BYTES:
            changes = False
            if ep.get("status") == "complete":
                ep["status"] = "script-only"
                changes = True
            if ep.get("videoProfile") != "draft":
                ep["videoProfile"] = "draft"
                changes = True
            probed = probe_resolution(dest)
            if probed:
                res = f"{probed[0]}x{probed[1]}"
                if ep.get("videoResolution") != res:
                    ep["videoResolution"] = res
                    changes = True
            if changes:
                updated += 1
                print(f"  {ep['id']}: stub WebM ({size} bytes) — marked script-only/draft")
            continue
        profile, resolution = profile_for_file(dest)
        if profile == "draft" and size >= MIN_BYTES:
            profile = "hd"
        changes = False
        if ep.get("status") != "complete":
            ep["status"] = "complete"
            changes = True
        if ep.get("videoProfile") != profile:
            ep["videoProfile"] = profile
            changes = True
        if ep.get("videoResolution") != resolution:
            ep["videoResolution"] = resolution
            changes = True
        if ep.get("pilot") and profile in ("hd", "uhd"):
            ep["pilot"] = False
            changes = True
        if changes:
            ep["renderedUtc"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            updated += 1
            print(f"  {ep['id']}: -> {profile} {resolution} ({size // 1024}KB)")
        FLUTTER_VIDEOS.mkdir(parents=True, exist_ok=True)
        fdest = FLUTTER_VIDEOS / webm_name
        if not fdest.is_file() or fdest.stat().st_size < dest.stat().st_size:
            shutil.copy2(dest, fdest)
    catalog["lockedUtc"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    text = json.dumps(catalog, indent=2) + "\n"
    CATALOG.write_text(text, encoding="utf-8")
    APP_CATALOG.parent.mkdir(parents=True, exist_ok=True)
    APP_CATALOG.write_text(text, encoding="utf-8")
    print(f"Updated {updated} episode profile(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
