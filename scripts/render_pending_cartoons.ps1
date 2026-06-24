# Renders all script-only Caly and Friends episodes; commits after each band batch.
$root = "C:\Users\Auricrux\OneDrive - Future Contractors of America LLC"
$content = Join-Path $root "calyndra-content"
$app = Join-Path $root "calyndra-app"
$flutter = Join-Path $root "calyndra-mobile-flutter"
$log = Join-Path $content "videos\pending_render.log"

"=== pending render $(Get-Date -Format o) ===" | Out-File $log -Encoding utf8

Set-Location $content
python scripts/generate_caly_friends_episodes.py --pending 2>&1 | Tee-Object -FilePath $log -Append

python scripts/qc_cartoon_catalog.py 2>&1 | Tee-Object -FilePath $log -Append
python scripts/qc_ecosystem.py 2>&1 | Tee-Object -FilePath $log -Append

Set-Location $content
git add videos/caly_friends_catalog.json scripts/generate_caly_friends_episodes.py
git diff --cached --quiet
if (-not $?) {
  git commit -m "Mark rendered Caly and Friends episodes complete."
  git push origin main
}

Set-Location $app
git pull --rebase origin main 2>&1 | Out-Null
git add app/index.html content/videos/caly_friends_catalog.json videos/*_long.webm
git diff --cached --quiet
if (-not $?) {
  git commit -m "Ship full Caly and Friends cartoon renders and dynamic catalog UI."
  git push origin main
}

Set-Location $flutter
git add assets/videos/*_long.webm
git diff --cached --quiet
if (-not $?) {
  git commit -m "Sync full Caly and Friends cartoon renders to mobile."
  git push origin main
}

"=== done $(Get-Date -Format o) ===" | Out-File $log -Append -Encoding utf8
