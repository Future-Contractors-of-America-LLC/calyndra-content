# Re-render complete episodes that are not yet Full HD; ship each after success.
$root = "C:\Users\Auricrux\OneDrive - Future Contractors of America LLC"
$content = Join-Path $root "calyndra-content"
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$log = Join-Path $content "videos\upgrade_hd_$stamp.log"
$env:PYTHONUNBUFFERED = "1"
$env:CALY_VIDEO_PROFILE = "hd"

function Write-Log($msg) {
  $line = "$(Get-Date -Format o) $msg"
  Write-Host $line
  $line | Out-File $log -Append -Encoding utf8
}

function Ship-Episode($webmName) {
  $app = Join-Path $root "calyndra-app"
  $flutter = Join-Path $root "calyndra-mobile-flutter"
  Set-Location $content
  python scripts/sync_cartoon_catalog_from_webms.py 2>&1 | Out-File $log -Append -Encoding utf8
  git add videos/caly_friends_catalog.json
  git diff --cached --quiet
  if (-not $?) {
    git commit -m "Upgrade $webmName to Full HD catalog metadata."
    git push origin main
  }
  Set-Location $app
  git pull --rebase origin main 2>&1 | Out-File $log -Append -Encoding utf8
  git add content/videos/caly_friends_catalog.json "videos/$webmName"
  git diff --cached --quiet
  if (-not $?) {
    git commit -m "Ship Full HD upgrade $webmName."
    git -c http.postBuffer=524288000 push origin main
  }
  Set-Location $flutter
  git pull --rebase origin main 2>&1 | Out-File $log -Append -Encoding utf8
  git add "assets/videos/$webmName"
  git diff --cached --quiet
  if (-not $?) {
    git commit -m "Sync Full HD upgrade $webmName to mobile."
    git -c http.postBuffer=524288000 push origin main
  }
  Set-Location $content
}

Write-Log "=== HD upgrade start ==="
Set-Location $content
python scripts/sync_cartoon_catalog_from_webms.py 2>&1 | Out-File $log -Append -Encoding utf8

$upgradeJson = python -c @"
import json
from pathlib import Path
c = json.loads(Path('videos/caly_friends_catalog.json').read_text(encoding='utf-8'))
ids = [
    e['id'] for e in c['episodes']
    if e.get('status') == 'complete' and e.get('videoProfile') != 'hd' and e.get('videoProfile') != 'uhd'
]
print('\n'.join(ids))
"@

$ids = @($upgradeJson -split "`n" | Where-Object { $_ -match '\S' })
Write-Log "Episodes to upgrade: $($ids.Count)"

foreach ($id in $ids) {
  Set-Location $content
  Write-Log "Upgrading $id to Full HD ..."
  python scripts/generate_caly_friends_episodes.py --upgrade-hd --id $id 2>&1 | Tee-Object -FilePath $log -Append
  $catalog = Get-Content (Join-Path $content "videos\caly_friends_catalog.json") -Raw | ConvertFrom-Json
  $ep = $catalog.episodes | Where-Object { $_.id -eq $id } | Select-Object -First 1
  if ($ep.videoProfile -eq "hd" -or $ep.videoProfile -eq "uhd") {
    Ship-Episode $ep.webm
    Write-Log "Upgraded $id"
  } else {
    Write-Log "SKIP upgrade ship: $id profile=$($ep.videoProfile)"
  }
}

python scripts/qc_cartoon_catalog.py 2>&1 | Tee-Object -FilePath $log -Append
Write-Log "=== HD upgrade done ==="
