Param(
  [Parameter(Mandatory = $true)]
  [string]$PromptFile,
  [string]$ScenarioFile,
  [string]$OutputReport = "benchmarks/headless/headless-report.md",
  [string]$ProtocolReport = "benchmarks/headless/protocol.md",
  [int]$SummaryChars = 600
)

$ErrorActionPreference = "Stop"

function Ensure-Parent($Path) {
  $parent = Split-Path -Parent $Path
  if ($parent -and -not (Test-Path $parent)) {
    New-Item -ItemType Directory -Path $parent -Force | Out-Null
  }
}

function Parse-Scenario($Path) {
  $meta = @{}
  $require = New-Object System.Collections.Generic.List[string]
  $sections = New-Object System.Collections.Generic.List[string]
  $state = ""
  foreach ($line in Get-Content -Path $Path) {
    $t = $line.Trim()
    if (-not $t -or $t.StartsWith("#")) { continue }
    if ($t.StartsWith("[") -and $t.EndsWith("]")) {
      $state = $t.Trim("[", "]").ToLowerInvariant()
      continue
    }
    if ($state -eq "meta") {
      if ($t -match "^(.*?)=(.*)$") {
        $meta[$Matches[1].Trim()] = $Matches[2].Trim()
      }
      continue
    }
    if ($state -eq "require") { $require.Add($t); continue }
    if ($state -eq "sections") { $sections.Add($t); continue }
  }
  return @{
    Meta = $meta
    Require = $require
    Sections = $sections
  }
}

function File-ContainsAll($Path, $Headings) {
  if (-not (Test-Path $Path -PathType Leaf)) { return $false }
  $content = Get-Content -Path $Path -Raw
  foreach ($h in $Headings) {
    if (-not ($content -match [regex]::Escape($h))) { return $false }
  }
  return $true
}

if (-not (Test-Path $PromptFile -PathType Leaf)) {
  Write-Host "Prompt file not found: $PromptFile"
  exit 1
}

$rg = Get-Command rg -ErrorAction SilentlyContinue
if (-not $rg) {
  Write-Host "Missing dependency: ripgrep (rg)"
  Write-Host "Install on Windows: winget install BurntSushi.ripgrep"
  Write-Host "Then re-run this script."
  exit 1
}

$root = Resolve-Path (Join-Path $PSScriptRoot "..\..") | Select-Object -ExpandProperty Path

if (-not $ScenarioFile) {
  $promptBase = [System.IO.Path]::GetFileNameWithoutExtension($PromptFile)
  $candidate = Join-Path $root ("benchmarks\scenarios\" + $promptBase + ".scn")
  if (Test-Path $candidate -PathType Leaf) {
    $ScenarioFile = $candidate
  }
}

$scenario = $null
if ($ScenarioFile) {
  if (-not (Test-Path $ScenarioFile -PathType Leaf)) {
    Write-Host "Scenario file not found: $ScenarioFile"
    exit 1
  }
  $scenario = Parse-Scenario $ScenarioFile
}

$runId = "headless-" + (Get-Date).ToUniversalTime().ToString("yyyyMMdd-HHmmssZ")
$runRoot = Join-Path $root ("benchmarks\runs\" + $runId)
$workspace = Join-Path $runRoot "workspace"
New-Item -ItemType Directory -Path $workspace -Force | Out-Null

$installer = Join-Path $root "installer.ps1"
if (Test-Path $installer -PathType Leaf) {
  & $installer -Target $workspace -Mode missing -Create | Out-Null
}

Push-Location $workspace

$raw = Get-Content -Path $PromptFile -Raw
$blocks = $raw -split "(?m)^\s*---\s*$"

$results = @()
$protocol = @()
$step = 1
$totalStart = Get-Date

foreach ($block in $blocks) {
  $prompt = $block.Trim()
  if (-not $prompt) { continue }
  $start = Get-Date
  Write-Host "Running step $step"
  $output = & agent -p --force --output-format text $prompt 2>&1 | Out-String
  $exitCode = $LASTEXITCODE
  $end = Get-Date
  $duration = [math]::Round(($end - $start).TotalSeconds, 2)
  $status = if ($exitCode -eq 0) { "PASS" } else { "FAIL" }
  $results += [pscustomobject]@{
    Step = $step
    Duration = $duration
    Status = $status
    ExitCode = $exitCode
  }
  $summary = $output.Trim()
  if ($summary.Length -gt $SummaryChars) {
    $summary = $summary.Substring(0, $SummaryChars) + "..."
  }
  $protocol += [pscustomobject]@{
    Step = $step
    Prompt = $prompt
    Duration = $duration
    Status = $status
    ExitCode = $exitCode
    Summary = $summary
  }
  $step++
}

Pop-Location

$missingFiles = @()
$sectionErrors = @()
if ($scenario) {
  foreach ($rel in $scenario.Require) {
    $path = Join-Path $workspace $rel
    if (-not (Test-Path $path -PathType Leaf)) {
      $missingFiles += $rel
    }
  }
  foreach ($line in $scenario.Sections) {
    $parts = $line.Split("|")
    if ($parts.Count -lt 2) { continue }
    $path = Join-Path $workspace $parts[0].Trim()
    $headings = $parts[1].Split(";") | ForEach-Object { $_.Trim() } | Where-Object { $_ }
    if (-not (File-ContainsAll $path $headings)) {
      $sectionErrors += $parts[0].Trim()
    }
  }
}

$smokeChecks = @()
if ($scenario) {
  $id = $scenario.Meta["id"]
  if ($id -eq "S4") {
    $schemaPath = Join-Path $workspace "examples\webview-app\shared\schema.json"
    if (Test-Path $schemaPath -PathType Leaf) {
      try { Get-Content -Path $schemaPath -Raw | ConvertFrom-Json | Out-Null; $smokeChecks += "schema.json valid: PASS" }
      catch { $smokeChecks += "schema.json valid: FAIL" }
    }
    $indexPath = Join-Path $workspace "examples\webview-app\frontend\index.html"
    if (Test-Path $indexPath -PathType Leaf) {
      $indexContent = Get-Content -Path $indexPath -Raw
      $smokeChecks += "index references app.js: " + ($(if ($indexContent -match "app\.js") { "PASS" } else { "FAIL" }))
      $smokeChecks += "index references style.css: " + ($(if ($indexContent -match "style\.css") { "PASS" } else { "FAIL" }))
    }
  }
  if ($id -eq "S5") {
    $indexPath = Join-Path $workspace "examples\3d-animation\index.html"
    if (Test-Path $indexPath -PathType Leaf) {
      $indexContent = Get-Content -Path $indexPath -Raw
      $smokeChecks += "index references main.js: " + ($(if ($indexContent -match "main\.js") { "PASS" } else { "FAIL" }))
    }
    $mainPath = Join-Path $workspace "examples\3d-animation\main.js"
    if (Test-Path $mainPath -PathType Leaf) {
      $mainContent = Get-Content -Path $mainPath -Raw
      $smokeChecks += "main uses requestAnimationFrame: " + ($(if ($mainContent -match "requestAnimationFrame") { "PASS" } else { "FAIL" }))
    }
  }
}

$totalEnd = Get-Date
$totalDuration = [math]::Round(($totalEnd - $totalStart).TotalSeconds, 2)
$passCount = ($results | Where-Object { $_.Status -eq "PASS" }).Count
$failCount = ($results | Where-Object { $_.Status -eq "FAIL" }).Count
$timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")

$reportPath = Join-Path $root $OutputReport
Ensure-Parent $reportPath
$protocolPath = Join-Path $root $ProtocolReport
Ensure-Parent $protocolPath
$runReportPath = Join-Path $runRoot "reports\headless-report.md"
$runProtocolPath = Join-Path $runRoot "reports\protocol.md"
Ensure-Parent $runReportPath
Ensure-Parent $runProtocolPath

@"
# its-magic Headless Benchmark Report

Timestamp: $timestamp
PromptFile: $PromptFile
ScenarioFile: $ScenarioFile
Workspace: $workspace
Steps: $($results.Count)
Pass: $passCount
Fail: $failCount
TotalDurationSeconds: $totalDuration

## Validation
MissingFiles: $($missingFiles.Count)
SectionErrors: $($sectionErrors.Count)

## Results
"@ | Set-Content -Path $reportPath

foreach ($r in $results) {
  Add-Content -Path $reportPath -Value ("- [{0}] Step {1} | DurationSeconds={2} | ExitCode={3}" -f $r.Status, $r.Step, $r.Duration, $r.ExitCode)
}

if ($missingFiles.Count -gt 0) {
  Add-Content -Path $reportPath -Value ""
  Add-Content -Path $reportPath -Value "## Missing files"
  foreach ($m in $missingFiles) { Add-Content -Path $reportPath -Value "- $m" }
}
if ($sectionErrors.Count -gt 0) {
  Add-Content -Path $reportPath -Value ""
  Add-Content -Path $reportPath -Value "## Section errors"
  foreach ($s in $sectionErrors) { Add-Content -Path $reportPath -Value "- $s" }
}
if ($smokeChecks.Count -gt 0) {
  Add-Content -Path $reportPath -Value ""
  Add-Content -Path $reportPath -Value "## Smoke checks"
  foreach ($c in $smokeChecks) { Add-Content -Path $reportPath -Value "- $c" }
}

@"
# its-magic Headless Protocol

Timestamp: $timestamp
PromptFile: $PromptFile
ScenarioFile: $ScenarioFile
Workspace: $workspace

## Steps
"@ | Set-Content -Path $protocolPath

foreach ($p in $protocol) {
  Add-Content -Path $protocolPath -Value ""
  Add-Content -Path $protocolPath -Value ("### Step {0}" -f $p.Step)
  Add-Content -Path $protocolPath -Value ("Status: {0} | DurationSeconds={1} | ExitCode={2}" -f $p.Status, $p.Duration, $p.ExitCode)
  Add-Content -Path $protocolPath -Value ""
  Add-Content -Path $protocolPath -Value "Prompt:"
  Add-Content -Path $protocolPath -Value "```"
  Add-Content -Path $protocolPath -Value $p.Prompt
  Add-Content -Path $protocolPath -Value "```"
  Add-Content -Path $protocolPath -Value ""
  Add-Content -Path $protocolPath -Value "AI response (summary):"
  Add-Content -Path $protocolPath -Value "```"
  Add-Content -Path $protocolPath -Value $p.Summary
  Add-Content -Path $protocolPath -Value "```"
}

Copy-Item -Path $reportPath -Destination $runReportPath -Force
Copy-Item -Path $protocolPath -Destination $runProtocolPath -Force

Write-Host "Report written to: $reportPath"
Write-Host "Protocol written to: $protocolPath"
Write-Host "Run artifacts: $runRoot"
$validationFail = ($missingFiles.Count -gt 0) -or ($sectionErrors.Count -gt 0) -or ($smokeChecks -match "FAIL")
if ($failCount -gt 0 -or $validationFail) { exit 1 }
exit 0
