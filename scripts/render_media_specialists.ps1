# Continuous Ultra HD render with specialist media pipeline (animation / video / audio).
$root = "C:\Users\Auricrux\OneDrive - Future Contractors of America LLC"
$content = Join-Path $root "calyndra-content"
$env:PYTHONUNBUFFERED = "1"
$env:CALY_VIDEO_PROFILE = "uhd"
$env:CALY_MEDIA_SPECIALISTS = "1"

& (Join-Path $content "scripts\render_continuous_ultra.ps1")
