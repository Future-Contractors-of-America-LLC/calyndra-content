# Single entry: keep Ultra HD specialist production running until done.
# Usage: powershell -File scripts/start_continuous_production.ps1
$root = "C:\Users\Auricrux\OneDrive - Future Contractors of America LLC"
$watchdog = Join-Path $root "calyndra-content\scripts\render_ultra_watchdog.ps1"
& $watchdog
