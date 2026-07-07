$ErrorActionPreference = 'Stop'

# --- Config ---
$packageName = 'its-magic'
# UPDATE: url and checksum before each release
$url         = 'https://github.com/fl0wm0ti0n/its-magic/archive/refs/tags/v0.1.3-3.zip'
$checksum    = '187d60367f16f43288353aacc72f0bf018566489dd4356ef8735ed680a5b9d12'
$checksumType= 'sha256'

# --- Download & extract ---
$toolsDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

Install-ChocolateyZipPackage -PackageName $packageName `
    -Url $url `
    -UnzipLocation $toolsDir `
    -Checksum $checksum `
    -ChecksumType $checksumType

# --- Find the extracted installer script (no Node.js needed) ---
$installerPath = Get-ChildItem -Path $toolsDir -Recurse -File -Filter "installer.ps1" |
    Select-Object -First 1 -ExpandProperty FullName

if (-not $installerPath) {
    throw "installer.ps1 not found in extracted archive. Installation failed."
}

# --- Create a .cmd wrapper so 'its-magic' works from any shell ---
$wrapperCmd = Join-Path $toolsDir "its-magic.cmd"
$wrapperContent = @"
@echo off
powershell -ExecutionPolicy Bypass -File "$installerPath" %*
"@
Set-Content -Path $wrapperCmd -Value $wrapperContent -Encoding ASCII

# --- Register the shim ---
Install-BinFile -Name 'its-magic' -Path $wrapperCmd

# --- Banner (Base64-encoded to avoid encoding issues) ---
$prev = [Console]::OutputEncoding
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$b64 = 'ICDilojilojilZfilojilojilojilojilojilojilojilojilZfilojilojilojilojilojilojilojilZcgICAgICDilojilojilojilZcgICDilojilojilojilZcg4paI4paI4paI4paI4paI4pWXICDilojilojilojilojilojilojilZcg4paI4paI4pWXIOKWiOKWiOKWiOKWiOKWiOKWiOKVlwogIOKWiOKWiOKVkeKVmuKVkOKVkOKWiOKWiOKVlOKVkOKVkOKVneKWiOKWiOKVlOKVkOKVkOKVkOKVkOKVnSAgICAgIOKWiOKWiOKWiOKWiOKVlyDilojilojilojilojilZHilojilojilZTilZDilZDilojilojilZfilojilojilZTilZDilZDilZDilZDilZ0g4paI4paI4pWR4paI4paI4pWU4pWQ4pWQ4pWQ4pWQ4pWdCiAg4paI4paI4pWRICAg4paI4paI4pWRICAg4paI4paI4paI4paI4paI4paI4paI4pWX4paI4paI4paI4paI4paI4pWX4paI4paI4pWU4paI4paI4paI4paI4pWU4paI4paI4pWR4paI4paI4paI4paI4paI4paI4paI4pWR4paI4paI4pWRICDilojilojilojilZfilojilojilZHilojilojilZEgICAgIAogIOKWiOKWiOKVkSAgIOKWiOKWiOKVkSAgIOKVmuKVkOKVkOKVkOKVkOKWiOKWiOKVkeKVmuKVkOKVkOKVkOKVkOKVneKWiOKWiOKVkeKVmuKWiOKWiOKVlOKVneKWiOKWiOKVkeKWiOKWiOKVlOKVkOKVkOKWiOKWiOKVkeKWiOKWiOKVkSAgIOKWiOKWiOKVkeKWiOKWiOKVkeKWiOKWiOKVkSAgICAgCiAg4paI4paI4pWRICAg4paI4paI4pWRICAg4paI4paI4paI4paI4paI4paI4paI4pWRICAgICAg4paI4paI4pWRIOKVmuKVkOKVnSDilojilojilZHilojilojilZEgIOKWiOKWiOKVkeKVmuKWiOKWiOKWiOKWiOKWiOKWiOKVlOKVneKWiOKWiOKVkeKVmuKWiOKWiOKWiOKWiOKWiOKWiOKVlwogIOKVmuKVkOKVnSAgIOKVmuKVkOKVnSAgIOKVmuKVkOKVkOKVkOKVkOKVkOKVkOKVnSAgICAgIOKVmuKVkOKVnSAgICAg4pWa4pWQ4pWd4pWa4pWQ4pWdICDilZrilZDilZ0g4pWa4pWQ4pWQ4pWQ4pWQ4pWQ4pWdIOKVmuKVkOKVnSDilZrilZDilZDilZDilZDilZDilZ0='
$art = [System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($b64))
$lines = $art -split "`n"
$colors = @('Magenta','Magenta','Magenta','Cyan','Cyan','Cyan')
Write-Host ""
for ($i = 0; $i -lt $lines.Count; $i++) {
    Write-Host $lines[$i] -ForegroundColor $colors[$i]
}
Write-Host ""
Write-Host "                         AI dev team" -ForegroundColor Yellow
Write-Host "                    Installation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "  Run: its-magic --help" -ForegroundColor White
Write-Host ""
[Console]::OutputEncoding = $prev














































































