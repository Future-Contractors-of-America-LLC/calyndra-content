# Watchdog: restart Ultra HD specialist pipeline until all 72 episodes are UHD + on-length.
$root = "C:\Users\Auricrux\OneDrive - Future Contractors of America LLC"
$content = Join-Path $root "calyndra-content"
$log = Join-Path $content "videos\ultra_watchdog.log"
$pipeline = Join-Path $content "scripts\render_continuous_ultra.ps1"

$env:PYTHONUNBUFFERED = "1"
$env:CALY_VIDEO_PROFILE = "uhd"
$env:CALY_MEDIA_SPECIALISTS = "1"

function Log($msg) {
  $line = "$(Get-Date -Format o) $msg"
  Write-Host $line
  $line | Out-File $log -Append -Encoding utf8
}

function Get-RemainingCount {
  Set-Location $content
  $n = python -c @"
import json, sys
from pathlib import Path
sys.path.insert(0, 'scripts')
from caly_episode_duration import meets_duration_target
c = json.loads(Path('videos/caly_friends_catalog.json').read_text(encoding='utf-8'))
app = Path('..') / 'calyndra-app' / 'videos'
n = 0
for e in c['episodes']:
    if e.get('status') != 'complete':
        n += 1
        continue
    webm = app / e['webm']
    if e.get('videoProfile') != 'uhd' or not meets_duration_target(e, webm):
        n += 1
print(n)
"@
  return [int]$n
}

Log "=== Ultra HD watchdog start (animation + audio + video specialists) ==="
$run = 0
while ((Get-RemainingCount) -gt 0) {
  $run++
  $remaining = Get-RemainingCount
  Log "Launch run #$run (remaining=$remaining) ..."
  Set-Location $content
  $code = 0
  try {
    & $pipeline 2>&1 | Tee-Object -FilePath $log -Append
    if ($null -ne $LASTEXITCODE) { $code = $LASTEXITCODE }
  } catch {
    Log "ERROR run #$run : $($_.Exception.Message)"
    $code = 1
  }
  Log "Run #$run exited code=$code"
  if ((Get-RemainingCount) -eq 0) { break }
  Log "Not all UHD/on-length yet - restarting in 30s"
  Start-Sleep -Seconds 30
}

Log "=== All 72 episodes Ultra HD and on-length - production complete ==="
python scripts/qc_ecosystem.py 2>&1 | Out-File $log -Append -Encoding utf8
