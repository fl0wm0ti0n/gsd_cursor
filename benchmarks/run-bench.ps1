Param(
  [string]$RepoRoot
)

$ErrorActionPreference = "Stop"

function Resolve-RepoRoot {
  if ($RepoRoot) { return (Resolve-Path $RepoRoot).Path }
  return (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
}

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

$root = Resolve-RepoRoot
$scenarioDir = Join-Path $root "benchmarks\scenarios"
$tmpRoot = Join-Path $root "benchmarks\.tmp"
$reportPath = Join-Path $root "benchmarks\bench-report.md"

if (-not (Test-Path $tmpRoot)) { New-Item -ItemType Directory -Path $tmpRoot | Out-Null }

$scenarios = Get-ChildItem -Path $scenarioDir -Filter "*.scn" -File
$results = @()
$totalStart = Get-Date

foreach ($scn in $scenarios) {
  $parsed = Parse-Scenario $scn.FullName
  $meta = $parsed.Meta
  $id = $meta["id"]
  $name = $meta["name"]
  $steps = $meta["steps"]
  $scenarioStart = Get-Date

  $scenarioRoot = Join-Path $tmpRoot ("{0}-{1}" -f $id, (Get-Date).ToUniversalTime().ToString("yyyyMMdd-HHmmssZ"))
  New-Item -ItemType Directory -Path $scenarioRoot -Force | Out-Null

  $installer = Join-Path $root "installer.ps1"
  if (Test-Path $installer -PathType Leaf) {
    & $installer -Target $scenarioRoot -Mode missing -Create | Out-Null
  }

  $missingFiles = @()
  foreach ($rel in $parsed.Require) {
    $path = Join-Path $scenarioRoot $rel
    if (-not (Test-Path $path -PathType Leaf)) {
      Ensure-Parent $path
      Set-Content -Path $path -Value "# Auto-generated stub"
      $missingFiles += $rel
    }
  }

  $sectionErrors = @()
  foreach ($line in $parsed.Sections) {
    $parts = $line.Split("|")
    if ($parts.Count -lt 2) { continue }
    $path = Join-Path $scenarioRoot $parts[0].Trim()
    $headings = $parts[1].Split(";") | ForEach-Object { $_.Trim() } | Where-Object { $_ }
    if (-not (File-ContainsAll $path $headings)) {
      $sectionErrors += $parts[0].Trim()
    }
  }

  $scenarioEnd = Get-Date
  $duration = [math]::Round(($scenarioEnd - $scenarioStart).TotalSeconds, 2)
  $requiredCount = $parsed.Require.Count
  $missingCount = $missingFiles.Count
  $sectionCount = $parsed.Sections.Count
  $sectionErrorCount = $sectionErrors.Count

  $status = if ($missingCount -eq 0 -and $sectionErrorCount -eq 0) { "PASS" } else { "FAIL" }
  $results += [pscustomobject]@{
    Id = $id
    Name = $name
    Steps = $steps
    Duration = $duration
    Required = $requiredCount
    Missing = $missingCount
    Sections = $sectionCount
    SectionErrors = $sectionErrorCount
    Status = $status
  }
}

$totalEnd = Get-Date
$totalDuration = [math]::Round(($totalEnd - $totalStart).TotalSeconds, 2)
$passCount = ($results | Where-Object { $_.Status -eq "PASS" }).Count
$failCount = ($results | Where-Object { $_.Status -eq "FAIL" }).Count
$timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")

@"
# its-magic Benchmark Report

Timestamp: $timestamp
Scenarios: $($results.Count)
Pass: $passCount
Fail: $failCount
TotalDurationSeconds: $totalDuration

## Results
"@ | Set-Content -Path $reportPath

foreach ($r in $results) {
  Add-Content -Path $reportPath -Value ("- [{0}] {1} ({2}) | Steps={3} | DurationSeconds={4} | Required={5} Missing={6} | Sections={7} SectionErrors={8}" -f $r.Status, $r.Id, $r.Name, $r.Steps, $r.Duration, $r.Required, $r.Missing, $r.Sections, $r.SectionErrors)
}

Add-Content -Path $reportPath -Value ""
Add-Content -Path $reportPath -Value "Notes: This benchmark simulates agent output by creating stubs for missing artifacts. It is intended for regression comparison of kit changes."

Write-Host "Report written to: $reportPath"
if ($failCount -gt 0) { exit 1 }
exit 0

