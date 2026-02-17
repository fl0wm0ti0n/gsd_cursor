$ErrorActionPreference = 'Stop'

# --- Config ---
$packageName = 'its-magic'
# UPDATE: url and checksum before each release
$url         = 'https://github.com/fl0wm0ti0n/gsd_cursor/archive/refs/tags/v0.1.2-11.zip'
$checksum    = '835961dc11f74423e971767306e1b99bd0c5eca6ca9712b71f6053cf9981da4e'
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

$extractedRoot = Split-Path -Parent $installerPath

# --- Create a .cmd wrapper so 'its-magic' works from any shell ---
$wrapperCmd = Join-Path $toolsDir "its-magic.cmd"
$wrapperContent = @"
@echo off
if "%~1"=="--help" goto :help
if "%~1"=="-h" goto :help
if "%~1"=="/?" goto :help
powershell -ExecutionPolicy Bypass -File "$installerPath" %*
goto :eof
:help
echo its-magic - AI dev team
echo.
echo Usage:
echo   its-magic --target ^<path^> --mode missing [--backup] [--create]
echo.
echo Options:
echo   --target   Target repository path (required)
echo   --mode     missing ^| overwrite ^| interactive (default: missing)
echo   --backup   Backup files before overwrite
echo   --create   Create target directory if missing
echo   --help     Show this help
"@
Set-Content -Path $wrapperCmd -Value $wrapperContent -Encoding ASCII

# --- Register the shim ---
Install-BinFile -Name 'its-magic' -Path $wrapperCmd

# --- Banner ---
$prev = [Console]::OutputEncoding
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Write-Host ""
Write-Host "  ¦¦+¦¦¦¦¦¦¦¦+¦¦¦¦¦¦¦+      ¦¦¦+   ¦¦¦+ ¦¦¦¦¦+  ¦¦¦¦¦¦+ ¦¦+ ¦¦¦¦¦¦+" -ForegroundColor Magenta
Write-Host "  ¦¦¦+--¦¦+--+¦¦+----+      ¦¦¦¦+ ¦¦¦¦¦¦¦+--¦¦+¦¦+----+ ¦¦¦¦¦+----+" -ForegroundColor Magenta
Write-Host "  ¦¦¦   ¦¦¦   ¦¦¦¦¦¦¦+¦¦¦¦¦+¦¦+¦¦¦¦+¦¦¦¦¦¦¦¦¦¦¦¦¦¦  ¦¦¦+¦¦¦¦¦¦     " -ForegroundColor Magenta
Write-Host "  ¦¦¦   ¦¦¦   +----¦¦¦+----+¦¦¦+¦¦++¦¦¦¦¦+--¦¦¦¦¦¦   ¦¦¦¦¦¦¦¦¦     " -ForegroundColor Cyan
Write-Host "  ¦¦¦   ¦¦¦   ¦¦¦¦¦¦¦¦      ¦¦¦ +-+ ¦¦¦¦¦¦  ¦¦¦+¦¦¦¦¦¦++¦¦¦+¦¦¦¦¦¦+" -ForegroundColor Cyan
Write-Host "  +-+   +-+   +------+      +-+     +-++-+  +-+ +-----+ +-+ +-----+" -ForegroundColor Cyan
Write-Host ""
Write-Host "                         AI dev team" -ForegroundColor Yellow
Write-Host "                    Installation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "  Run: its-magic --help" -ForegroundColor White
Write-Host ""
[Console]::OutputEncoding = $prev








