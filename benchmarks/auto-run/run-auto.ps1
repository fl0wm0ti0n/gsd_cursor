Param(
  [Parameter(Mandatory = $true)]
  [string]$PromptFile,
  [string]$WindowTitle = "Cursor",
  [int]$DelaySeconds = 6,
  [int]$PreDelaySeconds = 3,
  [string]$SessionId
)

$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.Windows.Forms | Out-Null

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

if (-not (Test-Path $PromptFile -PathType Leaf)) {
  Write-Host "Prompt file not found: $PromptFile"
  exit 1
}

$root = Resolve-Path (Join-Path $PSScriptRoot "..\..") | Select-Object -ExpandProperty Path
$scratchpad = Join-Path $root ".cursor\scratchpad.md"
$logPath = Join-Path $root ".cursor\hooks\gsd-bench-log.jsonl"
$reportPath = Join-Path $root "benchmarks\live\live-bench-report.md"

if (-not $SessionId) {
  $SessionId = "run-" + (Get-Date).ToUniversalTime().ToString("yyyyMMdd-HHmmssZ")
}

$raw = Get-Content -Path $PromptFile -Raw
$blocks = $raw -split "(?m)^\s*---\s*$"

$wshell = New-Object -ComObject WScript.Shell
if (-not $wshell.AppActivate($WindowTitle)) {
  Write-Host "Warning: could not activate window: $WindowTitle"
}

Update-Scratchpad $scratchpad $SessionId
Write-Host "Live benchmark session: $SessionId"
Write-Host "Starting in $PreDelaySeconds seconds..."
Start-Sleep -Seconds $PreDelaySeconds

$step = 1
foreach ($block in $blocks) {
  $prompt = $block.Trim()
  if (-not $prompt) { continue }
  $prompt | Set-Clipboard
  [System.Windows.Forms.SendKeys]::SendWait("^v")
  [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
  Write-Host "Sent step $step"
  Start-Sleep -Seconds $DelaySeconds
  $step++
}

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

Ensure-Parent $reportPath
$timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")

@"
# GSD Kit Live Benchmark Report

Timestamp: $timestamp
Session: $SessionId
DurationSeconds: $duration

## Event Counts
- beforeShellExecution: $($counts.beforeShellExecution)
- beforeReadFile: $($counts.beforeReadFile)
- afterFileEdit: $($counts.afterFileEdit)
- stop: $($counts.stop)

## Errors
- none
"@ | Set-Content -Path $reportPath

Write-Host "Report written to: $reportPath"
exit 0
