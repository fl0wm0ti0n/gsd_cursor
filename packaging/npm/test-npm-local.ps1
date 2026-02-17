<#
.SYNOPSIS
  Test the npm package locally (no upload needed).
.DESCRIPTION
  Packs with npm pack, installs globally from the tarball, runs a smoke test
  into a temp directory, then uninstalls.
.PARAMETER SkipUninstall
  Keep the package installed after testing.
#>
param(
    [switch]$SkipUninstall
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path))
if (-not (Test-Path (Join-Path $repoRoot 'package.json'))) {
    $repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
}
if (-not (Test-Path (Join-Path $repoRoot 'package.json'))) {
    $repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
}

function Log($msg)  { Write-Host "[test-npm] $msg" -ForegroundColor Cyan }
function Pass($msg) { Write-Host "[test-npm] PASS - $msg" -ForegroundColor Green }
function Fail($msg) { Write-Host "[test-npm] FAIL - $msg" -ForegroundColor Red }

# --- Check prerequisites ---
$npmAvailable = $null -ne (Get-Command npm -ErrorAction SilentlyContinue)
if (-not $npmAvailable) {
    Fail "npm not found. Install Node.js first."
    exit 1
}

$nodeAvailable = $null -ne (Get-Command node -ErrorAction SilentlyContinue)
if (-not $nodeAvailable) {
    Fail "node not found. Install Node.js first."
    exit 1
}

Push-Location $repoRoot

# --- Clean old tarballs ---
Log "Cleaning old tarballs ..."
Get-ChildItem -Path $repoRoot -Filter "its-magic-*.tgz" | Remove-Item -Force

# --- Pack ---
Log "Running npm pack ..."
$prevEAP = $ErrorActionPreference
$ErrorActionPreference = 'Continue'
$packOutput = npm pack 2>&1 | Out-String
$ErrorActionPreference = $prevEAP
$tgzFile = Get-ChildItem -Path $repoRoot -Filter "its-magic-*.tgz" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $tgzFile) {
    Fail "npm pack did not create a .tgz file"
    Write-Host $packOutput
    Pop-Location; exit 1
}
Pass "Package created: $($tgzFile.Name)"

# --- Uninstall previous global install (if any) ---
Log "Removing previous global its-magic (if any) ..."
$ErrorActionPreference = 'Continue'
npm uninstall -g its-magic 2>&1 | Out-Null
$ErrorActionPreference = $prevEAP

# --- Install globally from local tarball ---
Log "Installing globally from local tarball ..."
$ErrorActionPreference = 'Continue'
npm install -g $tgzFile.FullName 2>&1 | Out-Null
$ErrorActionPreference = $prevEAP
if ($LASTEXITCODE -ne 0) {
    Fail "npm install -g failed"
    Pop-Location; exit 1
}
Pass "npm install -g succeeded"

# --- Smoke test: check the command exists ---
Log "Running smoke tests ..."
$whichResult = Get-Command its-magic -ErrorAction SilentlyContinue
if ($whichResult) {
    Pass "Command found: $($whichResult.Source)"
} else {
    Fail "its-magic command not found in PATH"
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

# --- Smoke test: install into a temp directory ---
$testDir = Join-Path $env:TEMP "its-magic-npm-test-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
Log "Testing install into temp dir: $testDir ..."
& its-magic --target $testDir --mode missing --create 2>&1 | Out-Null

$requiredFiles = @(
    ".cursor\commands\intake.md",
    ".cursor\rules\core.mdc",
    ".cursor\hooks.json",
    ".cursor\scratchpad.md",
    "docs\engineering\runbook.md"
)
$allFound = $true
foreach ($f in $requiredFiles) {
    $fp = Join-Path $testDir $f
    if (Test-Path $fp) {
        Pass "File installed: $f"
    } else {
        Fail "File missing: $f"
        $allFound = $false
    }
}

# Cleanup temp dir
if (Test-Path $testDir) { Remove-Item -Recurse -Force $testDir }

# --- Clean tarball ---
if ($tgzFile -and (Test-Path $tgzFile.FullName)) { Remove-Item $tgzFile.FullName -Force }

# --- Uninstall ---
if (-not $SkipUninstall) {
    Log "Uninstalling ..."
    $ErrorActionPreference = 'Continue'
    npm uninstall -g its-magic 2>&1 | Out-Null
    $ErrorActionPreference = $prevEAP
    if ($LASTEXITCODE -ne 0) { Fail "npm uninstall -g failed" }
    else { Pass "Uninstall succeeded" }
} else {
    Log "Skipping uninstall (-SkipUninstall flag set)"
}

Pop-Location

# --- Summary ---
Write-Host ""
Log "=========================================="
Log "  Local npm test complete!"
Log "=========================================="
