# -------------------------------------------------------------------
# validate-and-push.ps1 — local test-fix-push loop
#
# Part of the its-magic quality chain:
#   Cursor AI loop  →  validate-and-push  →  CI auto-fix (GitHub)
#
# Reads TEST_COMMAND (and optionally LINT_FIX_COMMAND / FORMAT_COMMAND)
# from docs/engineering/runbook.md, runs them in a loop, and pushes
# only when everything passes.
# -------------------------------------------------------------------

Param(
  [int]$MaxAttempts = 5,
  [string]$Branch,
  [switch]$NoCommit
)

$ErrorActionPreference = "Stop"
$root = Resolve-Path (Join-Path $PSScriptRoot "..")

function Log-Info  { param($Msg) Write-Host "[info]  $Msg" -ForegroundColor Cyan }
function Log-Pass  { param($Msg) Write-Host "[pass]  $Msg" -ForegroundColor Green }
function Log-Fail  { param($Msg) Write-Host "[fail]  $Msg" -ForegroundColor Red }
function Log-Warn  { param($Msg) Write-Host "[warn]  $Msg" -ForegroundColor Yellow }

# --- Read commands from runbook ------------------------------------------

function Read-RunbookKey {
  param([string]$Key)
  $runbook = Join-Path $root "docs\engineering\runbook.md"
  if (-not (Test-Path $runbook -PathType Leaf)) { return "" }
  $content = Get-Content -Path $runbook -Raw
  $m = [regex]::Match($content, "(?m)^${Key}:[ \t]*(.+)$")
  if (-not $m.Success) { return "" }
  $val = $m.Groups[1].Value.Trim()
  if ($val -in @("", "...", "<...>", "TODO")) { return "" }
  return $val
}

$TestCmd      = Read-RunbookKey "TEST_COMMAND"
$LintCmd      = Read-RunbookKey "LINT_COMMAND"
$TypecheckCmd = Read-RunbookKey "TYPECHECK_COMMAND"
$LintFixCmd   = Read-RunbookKey "LINT_FIX_COMMAND"
$FormatCmd    = Read-RunbookKey "FORMAT_COMMAND"
$TimeoutRaw   = Read-RunbookKey "TEST_TIMEOUT_SECONDS"
$TimeoutSec   = 120
if ($TimeoutRaw -match '^\d+$') { $TimeoutSec = [int]$TimeoutRaw }

if (-not $TestCmd) {
  Log-Fail "TEST_COMMAND is required by sync policy and cannot be blank."
  Log-Warn "Reason code: TEST_COMMAND_MISSING"
  Log-Warn "Set TEST_COMMAND in docs/engineering/runbook.md and re-run."
  exit 1
}

if (-not $Branch) {
  $Branch = (git -C $root rev-parse --abbrev-ref HEAD 2>$null)
  if (-not $Branch) { $Branch = "main" }
}

Log-Info "validate-and-push loop"
Log-Info "Branch: $Branch  |  Max attempts: $MaxAttempts"
if ($TestCmd)    { Log-Info "TEST_COMMAND:     $TestCmd" }
if ($LintCmd)    { Log-Info "LINT_COMMAND:     $LintCmd" }
if ($TypecheckCmd) { Log-Info "TYPECHECK_COMMAND: $TypecheckCmd" }
if ($LintFixCmd) { Log-Info "LINT_FIX_COMMAND: $LintFixCmd" }
if ($FormatCmd)  { Log-Info "FORMAT_COMMAND:   $FormatCmd" }
Log-Info "TEST_TIMEOUT_SECONDS: $TimeoutSec"
Write-Host ""

function Run-Cmd {
  param(
    [string]$Cmd,
    [int]$TimeoutSeconds
  )
  $prev = $ErrorActionPreference
  $ErrorActionPreference = "Continue"
  try {
    $proc = Start-Process -FilePath "powershell" `
      -ArgumentList @("-NoProfile", "-NonInteractive", "-Command", $Cmd) `
      -WorkingDirectory $root `
      -PassThru `
      -WindowStyle Hidden
    if ($proc.WaitForExit($TimeoutSeconds * 1000)) {
      return @{ Success = ($proc.ExitCode -eq 0); TimedOut = $false }
    }
    try { $proc.Kill() } catch {}
    return @{ Success = $false; TimedOut = $true }
  } catch {
    return @{ Success = $false; TimedOut = $false }
  } finally {
    $ErrorActionPreference = $prev
  }
}

$passed = $false
for ($attempt = 1; $attempt -le $MaxAttempts; $attempt++) {
  Log-Info "--- Attempt $attempt / $MaxAttempts ---"

  Push-Location $root
  $allOk = $true

  # 1. Optional auto-fix helpers
  if ($FormatCmd) {
    Log-Info "Running formatter..."
    $formatResult = Run-Cmd -Cmd $FormatCmd -TimeoutSeconds $TimeoutSec
    if ($formatResult.Success) {
      Log-Pass "Format OK"
    } else {
      Log-Warn "Formatter reported issues (non-blocking)"
    }
  }

  # 2. Try lint fix if available
  if ($LintFixCmd) {
    Log-Info "Running lint auto-fix..."
    Run-Cmd -Cmd $LintFixCmd -TimeoutSeconds $TimeoutSec | Out-Null
  }

  # 2. Mandatory test baseline
  Log-Info "Running mandatory TEST_COMMAND..."
  $testResult = Run-Cmd -Cmd $TestCmd -TimeoutSeconds $TimeoutSec
  if ($testResult.Success) {
    Log-Pass "TEST_COMMAND passed"
  } else {
    if ($testResult.TimedOut) {
      Log-Fail "TEST_COMMAND timed out"
      Log-Warn "Reason code: TEST_TIMEOUT"
    } else {
      Log-Fail "TEST_COMMAND failed"
      Log-Warn "Reason code: TEST_FAILED"
    }
    $allOk = $false
  }

  # 3. Optional lint check
  if ($LintCmd) {
    Log-Info "Running optional LINT_COMMAND..."
    $lintResult = Run-Cmd -Cmd $LintCmd -TimeoutSeconds $TimeoutSec
    if ($lintResult.Success) {
      Log-Pass "Lint OK"
    } else {
      Log-Fail "Lint failed"
      Log-Warn "Reason code: OPTIONAL_CHECK_FAILED"
      $allOk = $false
    }
  } else {
    Log-Info "LINT_COMMAND not configured -> skipped"
  }

  # 4. Optional typecheck check
  if ($TypecheckCmd) {
    Log-Info "Running optional TYPECHECK_COMMAND..."
    $typecheckResult = Run-Cmd -Cmd $TypecheckCmd -TimeoutSeconds $TimeoutSec
    if ($typecheckResult.Success) {
      Log-Pass "Typecheck OK"
    } else {
      Log-Fail "Typecheck failed"
      Log-Warn "Reason code: OPTIONAL_CHECK_FAILED"
      $allOk = $false
    }
  } else {
    Log-Info "TYPECHECK_COMMAND not configured -> skipped"
  }

  Pop-Location

  if ($allOk) {
    Log-Pass "All checks passed on attempt $attempt."
    $passed = $true
    break
  }

  if ($attempt -ge $MaxAttempts) {
    Log-Fail "Reached max attempts ($MaxAttempts). Aborting push."
    Write-Host ""
    Log-Warn "Fix the issues above, then re-run:"
    Log-Warn "  powershell scripts\validate-and-push.ps1"
    exit 1
  }

  Write-Host ""
  Log-Warn "Fix the failing checks, then press Enter to retry (or Ctrl+C to abort)..."
  Read-Host | Out-Null
}

if (-not $passed) { exit 1 }

Write-Host ""

if (-not $NoCommit) {
  Push-Location $root
  $status = git status --porcelain
  if ($status) {
    Log-Info "Staging and committing changes..."
    git add -A
    git commit -m "fix: address check failures (validate-and-push)"
  } else {
    Log-Info "Working tree clean, nothing to commit."
  }

  Log-Info "Pushing to origin/$Branch..."
  git push origin $Branch
  Log-Pass "Push successful."
  Pop-Location
} else {
  Log-Info "Auto-commit disabled (--NoCommit). Push manually when ready."
}
