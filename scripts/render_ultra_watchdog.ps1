# Watchdog: restart Ultra HD specialist pipeline until all 36 episodes are UHD.
$root = "C:\Users\Auricrux\OneDrive - Future Contractors of America LLC"
$content = Join-Path $root "calyndra-content"
$log = Join-Path $content "videos\ultra_watchdog.log"
$script = Join-Path $content "scripts\render_media_specialists.ps1"

function Log($msg) {
  $line = "$(Get-Date -Format o) $msg"
  Write-Host $line
  $line | Out-File $log -Append -Encoding utf8
}

function Test-AllUltra {
  Set-Location $content
  $n = python -c @"
import json
from pathlib import Path
c = json.loads(Path('videos/caly_friends_catalog.json').read_text(encoding='utf-8'))
eps = c['episodes']
pending = sum(1 for e in eps if e.get('status') != 'complete')
not_uhd = sum(1 for e in eps if e.get('videoProfile') != 'uhd')
print(not_uhd + pending)
"@
  return ([int]$n -eq 0)
}

Log "=== Ultra HD watchdog start ==="
$run = 0
while (-not (Test-AllUltra)) {
  $run++
  Log "Launch run #$run ..."
  $proc = Start-Process -FilePath "powershell.exe" `
    -ArgumentList @("-NoProfile", "-ExecutionPolicy", "Bypass", "-File", $script) `
    -WorkingDirectory $content `
    -PassThru -Wait -NoNewWindow
  Log "Run #$run exited code=$($proc.ExitCode)"
  if (Test-AllUltra) { break }
  Log "Not all UHD yet — restarting in 15s"
  Start-Sleep -Seconds 15
}

Log "=== All media at Ultra HD — watchdog done ==="
python scripts/qc_ecosystem.py 2>&1 | Out-File $log -Append -Encoding utf8
