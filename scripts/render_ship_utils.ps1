function Write-RenderLog($msg, $log) {
  $line = "$(Get-Date -Format o) $msg"
  Write-Host $line
  $line | Out-File $log -Append -Encoding utf8
}

function Push-GitMain {
  param(
    [string]$RepoPath,
    [string]$Log,
    [switch]$LargeBuffer
  )
  Set-Location $RepoPath
  for ($attempt = 1; $attempt -le 4; $attempt++) {
    git pull --rebase origin main 2>&1 | Out-File $Log -Append -Encoding utf8
    if ($LargeBuffer) {
      git -c http.postBuffer=524288000 -c http.lowSpeedLimit=0 -c http.lowSpeedTime=999999 push origin main 2>&1 | Out-File $Log -Append -Encoding utf8
    } else {
      git push origin main 2>&1 | Out-File $Log -Append -Encoding utf8
    }
    if ($LASTEXITCODE -eq 0) { return $true }
    Write-RenderLog "WARN: push attempt $attempt failed in $RepoPath" $Log
    Start-Sleep -Seconds 5
  }
  return $false
}

function Ship-Episode {
  param(
    [string]$Root,
    [string]$Content,
    [string]$WebmName,
    [string]$Log,
    [string]$CommitLabel = "full render"
  )
  $app = Join-Path $Root "calyndra-app"
  $flutter = Join-Path $Root "calyndra-mobile-flutter"

  Set-Location $Content
  python scripts/sync_cartoon_catalog_from_webms.py 2>&1 | Out-File $Log -Append -Encoding utf8
  git add videos/caly_friends_catalog.json
  git diff --cached --quiet
  if (-not $?) {
    git commit -m "Mark $WebmName complete after $CommitLabel."
    if (Push-GitMain -RepoPath $Content -Log $Log) {
      Write-RenderLog "Pushed content catalog for $WebmName" $Log
    } else {
      Write-RenderLog "FAIL content push for $WebmName" $Log
    }
  }

  Set-Location $app
  git pull --rebase origin main 2>&1 | Out-File $Log -Append -Encoding utf8
  git add content/videos/caly_friends_catalog.json "videos/$WebmName"
  git diff --cached --quiet
  if (-not $?) {
    git commit -m "Ship $CommitLabel $WebmName."
    if (Push-GitMain -RepoPath $app -Log $Log -LargeBuffer) {
      Write-RenderLog "Pushed app video $WebmName" $Log
    } else {
      Write-RenderLog "FAIL app push for $WebmName" $Log
    }
  }

  Set-Location $flutter
  git pull --rebase origin main 2>&1 | Out-File $Log -Append -Encoding utf8
  git add "assets/videos/$WebmName"
  git diff --cached --quiet
  if (-not $?) {
    git commit -m "Sync $CommitLabel $WebmName to mobile."
    if (Push-GitMain -RepoPath $flutter -Log $Log -LargeBuffer) {
      Write-RenderLog "Pushed flutter video $WebmName" $Log
    } else {
      Write-RenderLog "FAIL flutter push for $WebmName" $Log
    }
  }

  Set-Location $Content
}
