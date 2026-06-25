# Re-render complete episodes that are not yet at the target profile; ship each after success.
$root = "C:\Users\Auricrux\OneDrive - Future Contractors of America LLC"
$content = Join-Path $root "calyndra-content"
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$log = Join-Path $content "videos\upgrade_hd_$stamp.log"
$env:PYTHONUNBUFFERED = "1"
$env:CALY_VIDEO_PROFILE = if ($env:CALY_VIDEO_PROFILE) { $env:CALY_VIDEO_PROFILE } else { "hd" }

. (Join-Path $content "scripts\render_ship_utils.ps1")

function Write-Log($msg) {
  Write-RenderLog $msg $log
}

Write-Log "=== quality upgrade start (profile=$env:CALY_VIDEO_PROFILE) ==="
Set-Location $content
python scripts/sync_cartoon_catalog_from_webms.py 2>&1 | Out-File $log -Append -Encoding utf8

$target = $env:CALY_VIDEO_PROFILE
$upgradeJson = python -c @"
import json, os
from pathlib import Path
target = os.environ.get('CALY_VIDEO_PROFILE', 'hd')
c = json.loads(Path('videos/caly_friends_catalog.json').read_text(encoding='utf-8'))
ids = [
    e['id'] for e in c['episodes']
    if e.get('status') == 'complete' and e.get('videoProfile') != target
]
print('\n'.join(ids))
"@

$ids = @($upgradeJson -split "`n" | Where-Object { $_ -match '\S' })
Write-Log "Episodes to upgrade: $($ids.Count)"

foreach ($id in $ids) {
  Set-Location $content
  Write-Log "Upgrading $id to $target ..."
  python scripts/generate_caly_friends_episodes.py --upgrade-hd --id $id 2>&1 | Tee-Object -FilePath $log -Append
  $catalog = Get-Content (Join-Path $content "videos\caly_friends_catalog.json") -Raw | ConvertFrom-Json
  $ep = $catalog.episodes | Where-Object { $_.id -eq $id } | Select-Object -First 1
  if ($ep.videoProfile -eq $target) {
    Ship-Episode -Root $root -Content $content -WebmName $ep.webm -Log $log -CommitLabel "$target upgrade"
    Write-Log "Upgraded $id"
  } else {
    Write-Log "SKIP upgrade ship: $id profile=$($ep.videoProfile)"
  }
}

python scripts/qc_cartoon_catalog.py 2>&1 | Tee-Object -FilePath $log -Append
Write-Log "=== quality upgrade done ==="
