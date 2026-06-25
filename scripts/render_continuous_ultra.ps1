# Continuous Ultra HD (4K) render loop until every episode is complete at videoProfile=uhd.
$root = "C:\Users\Auricrux\OneDrive - Future Contractors of America LLC"
$content = Join-Path $root "calyndra-content"
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$log = Join-Path $content "videos\continuous_ultra_$stamp.log"
$env:PYTHONUNBUFFERED = "1"
$env:CALY_VIDEO_PROFILE = "uhd"

. (Join-Path $content "scripts\render_ship_utils.ps1")

function Get-EpisodeQueues {
  Set-Location $content
  $json = python -c @"
import json
from pathlib import Path
c = json.loads(Path('videos/caly_friends_catalog.json').read_text(encoding='utf-8'))
pending = [e['id'] for e in c['episodes'] if e.get('status') == 'script-only']
upgrade = [
    e['id'] for e in c['episodes']
    if e.get('status') == 'complete' and e.get('videoProfile') != 'uhd'
]
print('PENDING:' + '|'.join(pending))
print('UPGRADE:' + '|'.join(upgrade))
"@
  $pending = @()
  $upgrade = @()
  foreach ($line in ($json -split "`n")) {
    if ($line -match '^PENDING:(.*)$') {
      if ($Matches[1]) { $pending = @($Matches[1] -split '\|' | Where-Object { $_ }) }
    }
    if ($line -match '^UPGRADE:(.*)$') {
      if ($Matches[1]) { $upgrade = @($Matches[1] -split '\|' | Where-Object { $_ }) }
    }
  }
  return @{ Pending = $pending; Upgrade = $upgrade }
}

function Render-One {
  param([string]$Id, [switch]$Upgrade)
  Set-Location $content
  Write-RenderLog "Rendering $Id (upgrade=$Upgrade) ..." $log
  if ($Upgrade) {
    python scripts/generate_caly_friends_episodes.py --upgrade-hd --id $Id 2>&1 | Tee-Object -FilePath $log -Append
  } else {
    python scripts/generate_caly_friends_episodes.py --id $Id 2>&1 | Tee-Object -FilePath $log -Append
  }
  if ($LASTEXITCODE -ne 0) {
    Write-RenderLog "WARN: render exit $LASTEXITCODE for $Id" $log
  }
  $catalog = Get-Content (Join-Path $content "videos\caly_friends_catalog.json") -Raw | ConvertFrom-Json
  $ep = $catalog.episodes | Where-Object { $_.id -eq $Id } | Select-Object -First 1
  if ($ep.videoProfile -eq "uhd") {
    Ship-Episode -Root $root -Content $content -WebmName $ep.webm -Log $log -CommitLabel "Ultra HD render"
    Write-RenderLog "Shipped Ultra HD $Id" $log
    return $true
  }
  Write-RenderLog "SKIP ship: $Id profile=$($ep.videoProfile) status=$($ep.status)" $log
  return $false
}

Write-RenderLog "=== continuous Ultra HD render start (3840x2160 @ 24fps) ===" $log
Set-Location $content
python scripts/sync_cartoon_catalog_from_webms.py 2>&1 | Out-File $log -Append -Encoding utf8

$cycle = 0
while ($true) {
  $cycle++
  $q = Get-EpisodeQueues
  $pendingCount = $q.Pending.Count
  $upgradeCount = $q.Upgrade.Count
  Write-RenderLog "Cycle $cycle — pending=$pendingCount upgrade=$upgradeCount" $log

  if ($pendingCount -eq 0 -and $upgradeCount -eq 0) {
    Write-RenderLog "All 36 episodes complete at Ultra HD." $log
    break
  }

  foreach ($id in $q.Pending) {
    Render-One -Id $id | Out-Null
  }
  foreach ($id in $q.Upgrade) {
    Render-One -Id $id -Upgrade | Out-Null
  }

  python scripts/qc_cartoon_catalog.py 2>&1 | Tee-Object -FilePath $log -Append
}

python scripts/qc_ecosystem.py 2>&1 | Tee-Object -FilePath $log -Append
Write-RenderLog "=== continuous Ultra HD render done ===" $log
