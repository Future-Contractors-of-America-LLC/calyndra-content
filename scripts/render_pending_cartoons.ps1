# Renders script-only Caly and Friends episodes one at a time; ships each to git after success.
$root = "C:\Users\Auricrux\OneDrive - Future Contractors of America LLC"
$content = Join-Path $root "calyndra-content"
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$log = Join-Path $content "videos\pending_render_$stamp.log"
$env:PYTHONUNBUFFERED = "1"
$env:CALY_VIDEO_PROFILE = "uhd"

. (Join-Path $content "scripts\render_ship_utils.ps1")

function Write-Log($msg) {
  Write-RenderLog $msg $log
}

Write-Log "=== pending render start ==="
Set-Location $content

$pendingJson = python -c @"
import json
from pathlib import Path
c = json.loads(Path('videos/caly_friends_catalog.json').read_text(encoding='utf-8'))
ids = [e['id'] for e in c['episodes'] if e.get('status') == 'script-only']
print('\n'.join(ids))
"@

$ids = @($pendingJson -split "`n" | Where-Object { $_ -match '\S' })
Write-Log "Pending episodes: $($ids.Count)"

foreach ($id in $ids) {
  Set-Location $content
  Write-Log "Rendering $id ..."
  python scripts/generate_caly_friends_episodes.py --id $id 2>&1 | Tee-Object -FilePath $log -Append
  if ($LASTEXITCODE -ne 0) {
    Write-Log "WARN: render exit code $LASTEXITCODE for $id"
  }

  $catalog = Get-Content (Join-Path $content "videos\caly_friends_catalog.json") -Raw | ConvertFrom-Json
  $ep = $catalog.episodes | Where-Object { $_.id -eq $id } | Select-Object -First 1
  if ($ep.status -eq "complete") {
    Ship-Episode -Root $root -Content $content -WebmName $ep.webm -Log $log -CommitLabel "full render"
    Write-Log "Shipped $id"
  } else {
    Write-Log "SKIP ship: $id still not complete"
  }
}

Set-Location $content
python scripts/qc_cartoon_catalog.py 2>&1 | Tee-Object -FilePath $log -Append
python scripts/qc_ecosystem.py 2>&1 | Tee-Object -FilePath $log -Append
Write-Log "=== pending render done ==="

Write-Log "=== hand off to continuous Ultra HD pipeline ==="
& (Join-Path $content "scripts\render_continuous_ultra.ps1")
