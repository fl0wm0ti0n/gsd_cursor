Param(
  [string]$RepoRoot,
  [string]$SessionId
)

$ErrorActionPreference = "Stop"

function Resolve-RepoRoot {
  if ($RepoRoot) { return (Resolve-Path $RepoRoot).Path }
  return (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
}

function Ensure-Parent($Path) {
  $parent = Split-Path -Parent $Path
  if ($parent -and -not (Test-Path $parent)) {
    New-Item -ItemType Directory -Path $parent -Force | Out-Null
  }
}

function Update-Scratchpad($Path, $Session) {
  $lines = @()
  if (Test-Path $Path -PathType Leaf) {
    $lines = Get-Content -Path $Path
  }
  $found = $false
  for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match "^GSD_BENCH_SESSION=") {
      $lines[$i] = "GSD_BENCH_SESSION=$Session"
      $found = $true
    }
  }
  if (-not $found) {
    $lines += "GSD_BENCH_SESSION=$Session"
  }
  Set-Content -Path $Path -Value $lines
}

function Clear-Scratchpad($Path) {
  if (-not (Test-Path $Path -PathType Leaf)) { return }
  $lines = Get-Content -Path $Path
  for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match "^GSD_BENCH_SESSION=") {
      $lines[$i] = "GSD_BENCH_SESSION="
    }
  }
  Set-Content -Path $Path -Value $lines
}

function Parse-Jsonl($Path, $Session) {
  $events = @()
  if (-not (Test-Path $Path -PathType Leaf)) { return $events }
  foreach ($line in Get-Content -Path $Path) {
    if (-not $line.Trim()) { continue }
    try {
      $obj = $line | ConvertFrom-Json
      if ($obj.session -eq $Session) { $events += $obj }
    } catch {}
  }
  return $events
}

$root = Resolve-RepoRoot
$scratchpad = Join-Path $root ".cursor\scratchpad.md"
$logPath = Join-Path $root ".cursor\hooks\bench-log.jsonl"
$reportPath = Join-Path $root "benchmarks\live\live-bench-report.md"

if (-not $SessionId) {
  $SessionId = "run-" + (Get-Date).ToUniversalTime().ToString("yyyyMMdd-HHmmssZ")
}

Write-Host "Live benchmark session: $SessionId"
Update-Scratchpad $scratchpad $SessionId
Write-Host "Session set in scratchpad. Run your scenario in Cursor now."
Read-Host "Press Enter when the scenario is complete"

Clear-Scratchpad $scratchpad
Write-Host "Session cleared. Generating report..."

$events = Parse-Jsonl $logPath $SessionId
$start = $events | Select-Object -First 1
$end = $events | Select-Object -Last 1

$duration = 0
if ($start -and $end) {
  $duration = [math]::Round((New-TimeSpan -Start $start.ts -End $end.ts).TotalSeconds, 2)
}

$counts = @{
  beforeShellExecution = 0
  beforeReadFile = 0
  afterFileEdit = 0
  stop = 0
}
foreach ($e in $events) {
  if ($counts.ContainsKey($e.event)) { $counts[$e.event]++ }
}

$failures = @()
foreach ($e in $events) {
  if ($e.event -eq "beforeShellExecution" -and $e.command -match "Blocked") {
    $failures += "Blocked command: $($e.command)"
  }
}

Ensure-Parent $reportPath
$timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")

@"
# its-magic Live Benchmark Report

Timestamp: $timestamp
Session: $SessionId
DurationSeconds: $duration

## Event Counts
- beforeShellExecution: $($counts.beforeShellExecution)
- beforeReadFile: $($counts.beforeReadFile)
- afterFileEdit: $($counts.afterFileEdit)
- stop: $($counts.stop)

## Errors
"@ | Set-Content -Path $reportPath

if ($failures.Count -eq 0) {
  Add-Content -Path $reportPath -Value "- none"
} else {
  foreach ($f in $failures) { Add-Content -Path $reportPath -Value "- $f" }
}

Write-Host "Report written to: $reportPath"
exit 0

