# Install GenerateImage outputs into calyndra-content + bundles
param(
  [string]$AssetsDir = "$env:USERPROFILE\.cursor\projects\c-Users-Auricrux-OneDrive-Future-Contractors-of-America-LLC\assets",
  [string]$Base = "C:\Users\Auricrux\OneDrive - Future Contractors of America LLC"
)
$content = Join-Path $Base "calyndra-content\symbols\images"
$flutter = Join-Path $Base "calyndra-mobile-flutter\assets\symbols"
$web = Join-Path $Base "calyndra-app\assets\symbols"
Get-ChildItem $AssetsDir -Filter "*_sprout.png" | ForEach-Object {
  $id = $_.BaseName -replace "_sprout$",""
  $dest = "$id.png"
  foreach ($root in @("$content\sprout", "$flutter\sprout", "$web\sprout")) {
    Copy-Item $_.FullName (Join-Path $root $dest) -Force
  }
}
Get-ChildItem $AssetsDir -Filter "*_quest.png" | ForEach-Object {
  $id = $_.BaseName -replace "_quest$",""
  $dest = "$id.png"
  foreach ($root in @("$content\quest", "$flutter\quest", "$web\quest")) {
    Copy-Item $_.FullName (Join-Path $root $dest) -Force
  }
}
Write-Host "Installed GenerateImage symbols from $AssetsDir"
