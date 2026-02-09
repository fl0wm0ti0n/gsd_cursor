Param(
  [string]$RepoRoot
)

$ErrorActionPreference = "Stop"

function Resolve-RepoRoot {
  if ($RepoRoot) { return (Resolve-Path $RepoRoot).Path }
  return (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
}

function Add-Result($Name, $Status, $Details = "") {
  $script:Results += [pscustomobject]@{
    Name = $Name
    Status = $Status
    Details = $Details
  }
}

function Assert-True($Name, $Condition, $Details = "") {
  if ($Condition) { Add-Result $Name "PASS" $Details }
  else { Add-Result $Name "FAIL" $Details }
}

function File-Contains($Path, $Text) {
  if (-not (Test-Path $Path -PathType Leaf)) { return $false }
  return (Get-Content -Path $Path -Raw) -match [regex]::Escape($Text)
}

function Count-Files($Path, $Filter) {
  if (-not (Test-Path $Path -PathType Container)) { return 0 }
  return (Get-ChildItem -Path $Path -Filter $Filter -File).Count
}

$Results = @()
$root = Resolve-RepoRoot

# 1) Base structure checks
Assert-True "Commands folder exists" (Test-Path (Join-Path $root ".cursor\commands"))
Assert-True "Rules folder exists" (Test-Path (Join-Path $root ".cursor\rules"))
Assert-True "Skills folder exists" (Test-Path (Join-Path $root ".cursor\skills\gsd-team\templates"))
Assert-True "Agents folder exists" (Test-Path (Join-Path $root ".cursor\agents"))
Assert-True "Hooks config exists" (Test-Path (Join-Path $root ".cursor\hooks.json"))
Assert-True "Docs folder exists" (Test-Path (Join-Path $root "docs"))
Assert-True "Sprints folder exists" (Test-Path (Join-Path $root "sprints"))
Assert-True "Handoffs folder exists" (Test-Path (Join-Path $root "handoffs"))
Assert-True "Decisions folder exists" (Test-Path (Join-Path $root "decisions"))
Assert-True "Workflows folder exists" (Test-Path (Join-Path $root ".github\workflows"))

# 2) Command/rule counts
Assert-True "10 commands exist" ((Count-Files (Join-Path $root ".cursor\commands") "*.md") -eq 10)
Assert-True "4 rules exist" ((Count-Files (Join-Path $root ".cursor\rules") "*.mdc") -eq 4)
Assert-True "6 agents exist" ((Count-Files (Join-Path $root ".cursor\agents") "*.mdc") -eq 6)

# 3) Command content sections
$commandFiles = Get-ChildItem -Path (Join-Path $root ".cursor\commands") -Filter "*.md" -File
foreach ($file in $commandFiles) {
  $content = Get-Content -Path $file.FullName -Raw
  $hasSections = $content -match "## Subagents" -and
    $content -match "## Inputs" -and
    $content -match "## Outputs" -and
    $content -match "## Stop conditions"
  Assert-True "Command sections present: $($file.Name)" $hasSections
}

# 4) Runbook keys and workflows
$runbook = Join-Path $root "docs\engineering\runbook.md"
Assert-True "Runbook contains TEST_COMMAND" (File-Contains $runbook "TEST_COMMAND")
Assert-True "Runbook contains LINT_COMMAND" (File-Contains $runbook "LINT_COMMAND")
Assert-True "Runbook contains TYPECHECK_COMMAND" (File-Contains $runbook "TYPECHECK_COMMAND")
Assert-True "Runbook contains DEPLOY_STAGING_COMMAND" (File-Contains $runbook "DEPLOY_STAGING_COMMAND")
Assert-True "Runbook contains DEPLOY_PROD_COMMAND" (File-Contains $runbook "DEPLOY_PROD_COMMAND")

$ci = Join-Path $root ".github\workflows\ci.yml"
$deploy = Join-Path $root ".github\workflows\deploy.yml"
Assert-True "CI workflow references TEST_COMMAND" (File-Contains $ci "TEST_COMMAND")
Assert-True "CI workflow references LINT_COMMAND" (File-Contains $ci "LINT_COMMAND")
Assert-True "CI workflow references TYPECHECK_COMMAND" (File-Contains $ci "TYPECHECK_COMMAND")
Assert-True "Deploy workflow references DEPLOY_STAGING_COMMAND" (File-Contains $deploy "DEPLOY_STAGING_COMMAND")
Assert-True "Deploy workflow references DEPLOY_PROD_COMMAND" (File-Contains $deploy "DEPLOY_PROD_COMMAND")

# 5) Hooks config schema
try {
  $hooksJson = Get-Content -Path (Join-Path $root ".cursor\hooks.json") -Raw | ConvertFrom-Json
  $schemaOk = ($hooksJson.version -is [int]) -and ($hooksJson.hooks -is [hashtable])
  Assert-True "Hooks schema valid" $schemaOk
} catch {
  Assert-True "Hooks schema valid" $false $_.Exception.Message
}

# 6) Installer test (PowerShell) - missing mode into temp dir
$tempRoot = Join-Path $root "tests\.tmp-install"
if (Test-Path $tempRoot) { Remove-Item -Recurse -Force $tempRoot }
New-Item -ItemType Directory -Path $tempRoot | Out-Null

$installer = Join-Path $root "gsd-installer.ps1"
if (Test-Path $installer -PathType Leaf) {
  & $installer -Target $tempRoot -Mode missing -Create | Out-Null
  $installed = Test-Path (Join-Path $tempRoot ".cursor\commands\gsd-intake.md")
  Assert-True "Installer (ps1) installs commands" $installed
} else {
  Assert-True "Installer (ps1) exists" $false
}

# 7) Backup test (overwrite mode + backup)
if (Test-Path $installer -PathType Leaf) {
  $readmePath = Join-Path $tempRoot "README.md"
  Set-Content -Path $readmePath -Value "override"
  & $installer -Target $tempRoot -Mode overwrite -Backup | Out-Null
  $backupDir = Get-ChildItem -Path (Join-Path $tempRoot "gsd-backups") -Directory -ErrorAction SilentlyContinue | Select-Object -First 1
  $backupOk = $false
  if ($backupDir) {
    $backupOk = Test-Path (Join-Path $backupDir.FullName "README.md")
  }
  Assert-True "Installer backup created" $backupOk
}

# Report
$reportPath = Join-Path $root "tests\report.md"
$timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
$passCount = ($Results | Where-Object { $_.Status -eq "PASS" }).Count
$failCount = ($Results | Where-Object { $_.Status -eq "FAIL" }).Count

@"
# GSD Kit Test Report

Timestamp: $timestamp
Pass: $passCount
Fail: $failCount

## Results
"@ | Set-Content -Path $reportPath

foreach ($r in $Results) {
  $line = "- [$($r.Status)] $($r.Name)"
  if ($r.Details) { $line += " - $($r.Details)" }
  Add-Content -Path $reportPath -Value $line
}

Write-Host "Report written to: $reportPath"

if ($failCount -gt 0) { exit 1 }
exit 0

