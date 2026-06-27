#!/usr/bin/env python3
"""Unified Calyndra ecosystem ship: QC gate → voice/symbols/sync → commit sibling repos.

Used by ship-ecosystem.yml CI and local primary-ship-machine runner.
Exit 1 on QC failure or sync error. Skips git push when --dry-run.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = Path(os.environ.get("CALYNDRA_CALYNDRA_APP_ROOT", ROOT.parent / "calyndra-app"))
FLUTTER = Path(os.environ.get("CALYNDRA_CALYNDRA_MOBILE_FLUTTER_ROOT", ROOT.parent / "calyndra-mobile-flutter"))
CENTRAL = Path(os.environ.get("CALYNDRA_CALYNDRA_CENTRAL_ROOT", ROOT.parent / "calyndra-central"))
RECEIPTS = CENTRAL / "calyndra" / "system" / "ship_receipts"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def run(cmd: list[str], *, cwd: Path | None = None, env: dict | None = None) -> subprocess.CompletedProcess:
    print(f"  $ {' '.join(cmd)}", flush=True)
    return subprocess.run(cmd, cwd=cwd or ROOT, env=env, text=True, capture_output=True)


def run_qc() -> tuple[bool, str]:
    r = run([sys.executable, "scripts/qc_ecosystem.py"])
    out = (r.stdout or "") + (r.stderr or "")
    print(out)
    return r.returncode == 0, out


def run_script(name: str, *, optional: bool = False) -> bool:
    path = ROOT / "scripts" / name
    if not path.is_file():
        if optional:
            print(f"  skip optional {name} (missing)")
            return True
        print(f"  FAIL missing script {name}")
        return False
    r = run([sys.executable, str(path)])
    if r.stdout:
        print(r.stdout)
    if r.returncode != 0:
        print(r.stderr or "")
        return False
    return True


def git_has_changes(repo: Path) -> bool:
    r = run(["git", "status", "--porcelain"], cwd=repo)
    return bool(r.stdout.strip())


def configure_git_push_auth(repo: Path) -> None:
    """Use PAT for cross-repo push in CI (GITHUB_TOKEN cannot push to sibling private repos)."""
    token = os.environ.get("CALYNDRA_SHIP_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        return
    r = run(["git", "remote", "get-url", "origin"], cwd=repo)
    remote = (r.stdout or "").strip()
    if not remote or token in remote:
        return
    if remote.startswith("https://github.com/"):
        path = remote.replace("https://github.com/", "").rstrip("/")
        if path.endswith(".git"):
            path = path[:-4]
        authed = f"https://x-access-token:{token}@github.com/{path}.git"
        run(["git", "remote", "set-url", "origin", authed], cwd=repo)


def git_commit_push(repo: Path, message: str, *, dry_run: bool) -> dict:
    if not repo.is_dir():
        return {"repo": str(repo), "status": "skipped", "reason": "missing"}
    if not git_has_changes(repo):
        return {"repo": repo.name, "status": "unchanged"}
    if dry_run:
        return {"repo": repo.name, "status": "dry-run-would-commit"}
    configure_git_push_auth(repo)
    run(["git", "add", "-A"], cwd=repo)
    r = run(["git", "commit", "-m", message], cwd=repo)
    if r.returncode != 0:
        return {"repo": repo.name, "status": "commit-failed", "detail": r.stderr}
    p = run(["git", "push", "origin", "main"], cwd=repo)
    if p.returncode != 0:
        return {"repo": repo.name, "status": "push-failed", "detail": p.stderr}
    return {"repo": repo.name, "status": "pushed"}


def write_receipt(payload: dict) -> None:
    if not CENTRAL.is_dir():
        return
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    ts = utc_now().replace(":", "").replace("-", "")
    path = RECEIPTS / f"ship-{ts}.json"
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    latest = RECEIPTS / "latest.json"
    latest.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Ship Calyndra ecosystem after QC pass")
    parser.add_argument("--dry-run", action="store_true", help="Run sync steps but do not git push")
    parser.add_argument("--skip-voice", action="store_true", help="Skip voice pregeneration")
    args = parser.parse_args()

    print("=== Ship ecosystem: completeness prep ===")
    os.environ.setdefault("CALY_SHIP", "1")
    os.environ.setdefault("CALY_REQUIRE_UHD", "1")
    os.environ.setdefault("CALY_VIDEO_PROFILE", "uhd")
    for prep in (
        "render_caly_family_symbols.py",
        "generate_expanded_vocab_symbols.py",
        "gen_sing_along_catalog.py",
        "generate_sing_along_music.py",
        "fix_video_catalog_profiles.py",
        "sync_cartoon_catalog_status.py",
    ):
        if not run_script(prep):
            write_receipt({"ok": False, "generatedUtc": utc_now(), "stage": "prep", "script": prep})
            print(f"SHIP BLOCKED: prep failed ({prep})")
            return 1

    print("=== Ship ecosystem: QC gate ===")
    ok, qc_out = run_qc()
    if not ok:
        write_receipt({"ok": False, "generatedUtc": utc_now(), "stage": "qc", "error": "QC failed"})
        print("SHIP BLOCKED: QC failed")
        return 1

    print("=== Ship ecosystem: voice + symbols ===")
    if not args.skip_voice:
        if not run_script("pregenerate_caly_voice.py"):
            write_receipt({"ok": False, "generatedUtc": utc_now(), "stage": "voice"})
            return 1
    if not run_script("sync_band_symbols_to_app.py"):
        return 1
    if not run_script("optimize_symbol_assets.py", optional=True):
        return 1

    print("=== Ship ecosystem: git push ===")
    app_result = git_commit_push(APP, "Ship ecosystem sync: content, symbols, voice", dry_run=args.dry_run)
    flutter_env = os.environ.copy()
    flutter_env["CALYNDRA_CONTENT_ROOT"] = str(ROOT)
    r = run([sys.executable, "scripts/sync_from_content.py"], cwd=FLUTTER, env=flutter_env)
    if r.returncode != 0:
        print(r.stderr or r.stdout)
        write_receipt({"ok": False, "generatedUtc": utc_now(), "stage": "flutter-sync"})
        return 1
    flutter_result = git_commit_push(FLUTTER, "Sync bundled assets from calyndra-content ship", dry_run=args.dry_run)

    receipt = {
        "ok": True,
        "generatedUtc": utc_now(),
        "qc": "pass",
        "app": app_result,
        "flutter": flutter_result,
        "dryRun": args.dry_run,
    }
    write_receipt(receipt)
    print(json.dumps(receipt, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
