# Renders script-only Caly and Friends episodes one at a time; ships each to git after success.
$root = "C:\Users\Auricrux\OneDrive - Future Contractors of America LLC"
$content = Join-Path $root "calyndra-content"
$app = Join-Path $root "calyndra-app"
$flutter = Join-Path $root "calyndra-mobile-flutter"
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$log = Join-Path $content "videos\pending_render_$stamp.log"

function Write-Log($msg) {
  $line = "$(Get-Date -Format o) $msg"
  Write-Host $line
  $line | Out-File $log -Append -Encoding utf8
}

function Ship-Episode($webmName) {
  Set-Location $content
  python scripts/sync_cartoon_catalog_from_webms.py 2>&1 | Out-File $log -Append -Encoding utf8
  git add videos/caly_friends_catalog.json
  git diff --cached --quiet
  if (-not $?) {
    git commit -m "Mark $webmName complete after full render."
    git push origin main
    Write-Log "Pushed content catalog for $webmName"
  }

  Set-Location $app
  git pull --rebase origin main 2>&1 | Out-File $log -Append -Encoding utf8
  git add content/videos/caly_friends_catalog.json "videos/$webmName"
  git diff --cached --quiet
  if (-not $?) {
    git commit -m "Ship full render $webmName."
    git -c http.postBuffer=524288000 push origin main
    Write-Log "Pushed app video $webmName (triggers SWA + blob deploy)"
  }

  Set-Location $flutter
  git pull --rebase origin main 2>&1 | Out-File $log -Append -Encoding utf8
  git add "assets/videos/$webmName"
  git diff --cached --quiet
  if (-not $?) {
    git commit -m "Sync full render $webmName to mobile."
    git -c http.postBuffer=524288000 push origin main
    Write-Log "Pushed flutter video $webmName"
  }
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
  Write-Log "Rendering $id ..."
  python scripts/generate_caly_friends_episodes.py --id $id 2>&1 | Tee-Object -FilePath $log -Append
  if ($LASTEXITCODE -ne 0) {
    Write-Log "WARN: render exit code $LASTEXITCODE for $id"
  }

  $catalog = Get-Content (Join-Path $content "videos\caly_friends_catalog.json") -Raw | ConvertFrom-Json
  $ep = $catalog.episodes | Where-Object { $_.id -eq $id } | Select-Object -First 1
  if ($ep.status -eq "complete") {
    Ship-Episode $ep.webm
    Write-Log "Shipped $id"
  } else {
    Write-Log "SKIP ship: $id still not complete"
  }
}

python scripts/qc_cartoon_catalog.py 2>&1 | Tee-Object -FilePath $log -Append
python scripts/qc_ecosystem.py 2>&1 | Tee-Object -FilePath $log -Append
Write-Log "=== pending render done ==="
