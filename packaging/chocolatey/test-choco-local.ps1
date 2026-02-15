<#
.SYNOPSIS
  Test the Chocolatey package locally (no upload needed).
.DESCRIPTION
  Packs, installs from local .nupkg, runs a quick smoke test, then uninstalls.
  Must be run as Administrator.
.PARAMETER SkipUninstall
  Keep the package installed after testing.
#>
param(
    [switch]$SkipUninstall
)

$ErrorActionPreference = 'Stop'
$chocoDir = Split-Path -Parent $MyInvocation.MyCommand.Path

function Log($msg)  { Write-Host "[test-choco] $msg" -ForegroundColor Cyan }
function Pass($msg) { Write-Host "[test-choco] PASS - $msg" -ForegroundColor Green }
function Fail($msg) { Write-Host "[test-choco] FAIL - $msg" -ForegroundColor Red }

# --- Check admin ---
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Fail "This script must be run as Administrator."
    Write-Host "  Right-click PowerShell -> 'Run as Administrator', then retry." -ForegroundColor Yellow
    exit 1
}

# --- Clean old nupkg files ---
Log "Cleaning old .nupkg files ..."
Get-ChildItem -Path $chocoDir -Filter "*.nupkg" | Remove-Item -Force

# --- Pack ---
Log "Running choco pack ..."
Push-Location $chocoDir
choco pack
if ($LASTEXITCODE -ne 0) { Fail "choco pack failed"; Pop-Location; exit 1 }

$nupkg = Get-ChildItem -Path $chocoDir -Filter "*.nupkg" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $nupkg) { Fail "No .nupkg file created"; Pop-Location; exit 1 }
Pass "Package created: $($nupkg.Name)"

# --- Uninstall previous version (if any) ---
$isInstalled = choco list --local-only --exact its-magic 2>$null | Select-String 'its-magic'
if ($isInstalled) {
    Log "Removing previous its-magic install ..."
    choco uninstall its-magic -y --force 2>$null | Out-Null
} else {
    Log "No previous its-magic install found (clean slate)"
}

# --- Install from local source ---
Log "Installing from local package ..."
choco install its-magic --source "." --pre --force -y
if ($LASTEXITCODE -ne 0) { Fail "choco install failed"; Pop-Location; exit 1 }
Pass "choco install succeeded"
Pop-Location

# --- Smoke test: check the shim exists ---
Log "Running smoke tests ..."
$shimPath = Join-Path $env:ChocolateyInstall "bin\its-magic.cmd"
if (Test-Path $shimPath) {
    Pass "Shim exists: $shimPath"
} else {
    # Chocolatey may create .exe shim instead
    $shimExe = Join-Path $env:ChocolateyInstall "bin\its-magic.exe"
    if (Test-Path $shimExe) {
        Pass "Shim exists: $shimExe"
    } else {
        Fail "Shim not found at $shimPath or $shimExe"
    }
}

# --- Smoke test: run its-magic --help ---
Log "Testing 'its-magic --help' ..."
$helpOutput = & its-magic --help 2>&1 | Out-String
if ($helpOutput -match 'its-magic|Usage|target') {
    Pass "its-magic --help works"
    Write-Host $helpOutput -ForegroundColor DarkGray
} else {
    Fail "its-magic --help did not return expected output"
    Write-Host $helpOutput
}

# --- Uninstall ---
if (-not $SkipUninstall) {
    Log "Uninstalling ..."
    choco uninstall its-magic -y
    if ($LASTEXITCODE -ne 0) { Fail "choco uninstall failed" }
    else { Pass "Uninstall succeeded" }
} else {
    Log "Skipping uninstall (-SkipUninstall flag set)"
}

# --- Summary ---
Write-Host ""
Log "=========================================="
Log "  Local Chocolatey test complete!"
Log "=========================================="
