#!/usr/bin/env python3
import json
import re
import subprocess
from pathlib import Path

import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT / "videos/caly_friends_catalog.json").read_text())
app = ROOT.parent / "calyndra-app" / "videos"

for ep in catalog["episodes"]:
    p = app / ep["webm"]
    target = ep["targetDurationSec"]
    if not p.exists():
        print(f"{ep['id']}: MISSING target={target}s")
        continue
    r = subprocess.run([FF, "-i", str(p)], capture_output=True, text=True)
    m = re.search(r"Duration:\s*(\d+):(\d+):([\d.]+)", r.stderr)
    dur = float(m.group(1)) * 3600 + float(m.group(2)) * 60 + float(m.group(3)) if m else 0
    pct = (dur / target * 100) if target else 0
    ok = "OK" if dur >= target * 0.85 else "SHORT"
    print(f"{ep['id']}: {dur:.0f}s / {target}s ({pct:.0f}%) {ok} status={ep.get('status')}")
