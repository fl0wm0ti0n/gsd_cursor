Param(
  [string]$RepoRoot,
  [int]$TimeoutSeconds = 120
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

function Invoke-Installer($ScriptPath, [string[]]$ScriptArgs) {
  $allArgs = @("-ExecutionPolicy", "Bypass", "-NonInteractive", "-File", $ScriptPath) + $ScriptArgs
  $proc = Start-Process powershell -ArgumentList $allArgs -PassThru -NoNewWindow -Wait:$false
  if ($proc.WaitForExit($script:TimeoutSeconds * 1000)) {
    return $proc.ExitCode
  }
  try { $proc.Kill() } catch {}
  throw "Installer timed out after $($script:TimeoutSeconds)s"
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
$script:TimeoutSeconds = $TimeoutSeconds
$root = Resolve-RepoRoot
$tpl = Join-Path $root "template"

# 1) Base structure checks
Assert-True "template/ folder exists" (Test-Path $tpl -PathType Container)
Assert-True "Commands folder exists" (Test-Path (Join-Path $tpl ".cursor\commands"))
Assert-True "Rules folder exists" (Test-Path (Join-Path $tpl ".cursor\rules"))
Assert-True "Skills folder exists" (Test-Path (Join-Path $tpl ".cursor\skills\its-magic\templates"))
Assert-True "Agents folder exists" (Test-Path (Join-Path $tpl ".cursor\agents"))
Assert-True "Hooks config exists" (Test-Path (Join-Path $tpl ".cursor\hooks.json"))
Assert-True "Docs folder exists" (Test-Path (Join-Path $tpl "docs"))
Assert-True "Sprints folder exists" (Test-Path (Join-Path $tpl "sprints"))
Assert-True "Handoffs folder exists" (Test-Path (Join-Path $tpl "handoffs"))
Assert-True "Decisions folder exists" (Test-Path (Join-Path $tpl "decisions"))
Assert-True "Workflows folder exists" (Test-Path (Join-Path $tpl ".github\workflows"))

# 2) Command/rule counts
Assert-True "22 commands exist" ((Count-Files (Join-Path $tpl ".cursor\commands") "*.md") -eq 22)
Assert-True "5 rules exist" ((Count-Files (Join-Path $tpl ".cursor\rules") "*.mdc") -eq 5)
Assert-True "7 agents exist" ((Count-Files (Join-Path $tpl ".cursor\agents") "*.mdc") -eq 7)

# 3) Command content sections
$commandFiles = Get-ChildItem -Path (Join-Path $tpl ".cursor\commands") -Filter "*.md" -File
foreach ($file in $commandFiles) {
  $content = Get-Content -Path $file.FullName -Raw
  $hasSections = $content -match "## Subagents" -and
    $content -match "## Inputs" -and
    $content -match "## Outputs" -and
    $content -match "## Stop conditions"
  Assert-True "Command sections present: $($file.Name)" $hasSections
}

# 4) Runbook keys and workflows
$runbook = Join-Path $tpl "docs\engineering\runbook.md"
Assert-True "Runbook contains TEST_COMMAND" (File-Contains $runbook "TEST_COMMAND")
Assert-True "Runbook contains LINT_COMMAND" (File-Contains $runbook "LINT_COMMAND")
Assert-True "Runbook contains TYPECHECK_COMMAND" (File-Contains $runbook "TYPECHECK_COMMAND")
Assert-True "Runbook contains DEPLOY_STAGING_COMMAND" (File-Contains $runbook "DEPLOY_STAGING_COMMAND")
Assert-True "Runbook contains DEPLOY_PROD_COMMAND" (File-Contains $runbook "DEPLOY_PROD_COMMAND")

$ci = Join-Path $tpl ".github\workflows\ci.yml"
$deploy = Join-Path $tpl ".github\workflows\deploy.yml"
Assert-True "CI workflow references TEST_COMMAND" (File-Contains $ci "TEST_COMMAND")
Assert-True "CI workflow references LINT_COMMAND" (File-Contains $ci "LINT_COMMAND")
Assert-True "CI workflow references TYPECHECK_COMMAND" (File-Contains $ci "TYPECHECK_COMMAND")
Assert-True "Deploy workflow references DEPLOY_STAGING_COMMAND" (File-Contains $deploy "DEPLOY_STAGING_COMMAND")
Assert-True "Deploy workflow references DEPLOY_PROD_COMMAND" (File-Contains $deploy "DEPLOY_PROD_COMMAND")

# 5) Hooks config schema
try {
  $hooksJson = Get-Content -Path (Join-Path $tpl ".cursor\hooks.json") -Raw | ConvertFrom-Json
  $schemaOk = ($hooksJson.version -is [int]) -and ($null -ne $hooksJson.hooks)
  Assert-True "Hooks schema valid" $schemaOk
} catch {
  Assert-True "Hooks schema valid" $false $_.Exception.Message
}

# 6) Installer test (PowerShell) - missing mode into temp dir
$tempRoot = Join-Path $root "tests\.tmp-install"
if (Test-Path $tempRoot) { Remove-Item -Recurse -Force $tempRoot -ErrorAction SilentlyContinue }
New-Item -ItemType Directory -Path $tempRoot | Out-Null

$installer = Join-Path $root "installer.ps1"
if (Test-Path $installer -PathType Leaf) {
  try {
    Invoke-Installer $installer @("-Target", $tempRoot, "-Mode", "missing", "-Create")
    $installed = Test-Path (Join-Path $tempRoot ".cursor\commands\intake.md")
    Assert-True "Installer (ps1) installs commands" $installed
  } catch {
    Assert-True "Installer (ps1) installs commands" $false $_.Exception.Message
  }
} else {
  Assert-True "Installer (ps1) exists" $false
}

# 7) Backup test (overwrite mode + backup)
if (Test-Path $installer -PathType Leaf) {
  try {
    $testFile = Join-Path $tempRoot ".cursor\commands\intake.md"
    Set-Content -Path $testFile -Value "override"
    Invoke-Installer $installer @("-Target", $tempRoot, "-Mode", "overwrite", "-Backup")
    $backupDir = Get-ChildItem -Path (Join-Path $tempRoot "backups") -Directory -ErrorAction SilentlyContinue | Select-Object -First 1
    $backupOk = $false
    if ($backupDir) {
      $backupOk = Test-Path (Join-Path $backupDir.FullName ".cursor\commands\intake.md")
    }
    Assert-True "Installer backup created" $backupOk
  } catch {
    Assert-True "Installer backup created" $false $_.Exception.Message
  }
}

# 8) Upgrade mode test
if (Test-Path $installer -PathType Leaf) {
  $upgradeTemp = Join-Path $root "tests\.tmp-upgrade"
  if (Test-Path $upgradeTemp) { Remove-Item -Recurse -Force $upgradeTemp -ErrorAction SilentlyContinue }
  New-Item -ItemType Directory -Path $upgradeTemp | Out-Null

  try {
    Invoke-Installer $installer @("-Target", $upgradeTemp, "-Mode", "missing", "-Create")

    $versionFile = Join-Path $upgradeTemp ".its-magic-version"
    Assert-True "Version file written on install" (Test-Path $versionFile -PathType Leaf)

    $userFile = Join-Path $upgradeTemp "docs\product\vision.md"
    Set-Content -Path $userFile -Value "# My Custom Vision"

    $frameworkFile = Join-Path $upgradeTemp ".cursor\commands\intake.md"
    Set-Content -Path $frameworkFile -Value "modified-framework"

    Invoke-Installer $installer @("-Target", $upgradeTemp, "-Mode", "upgrade")

    $frameworkRestored = -not ((Get-Content -Path $frameworkFile -Raw) -match "modified-framework")
    Assert-True "Upgrade restores framework files" $frameworkRestored

    $userPreserved = (Get-Content -Path $userFile -Raw) -match "My Custom Vision"
    Assert-True "Upgrade preserves user data" $userPreserved

    $versionUpdated = (Test-Path $versionFile -PathType Leaf)
    Assert-True "Version file updated after upgrade" $versionUpdated
  } catch {
    Assert-True "Upgrade test" $false $_.Exception.Message
  }

  if (Test-Path $upgradeTemp) { Remove-Item -Recurse -Force $upgradeTemp -ErrorAction SilentlyContinue }
}

# 9) Memory-audit command checks (US-0024)
$auditActive = Join-Path $root ".cursor\commands\memory-audit.md"
$auditTemplate = Join-Path $tpl ".cursor\commands\memory-audit.md"
Assert-True "memory-audit command exists (active)" (Test-Path $auditActive -PathType Leaf)
Assert-True "memory-audit command exists (template)" (Test-Path $auditTemplate -PathType Leaf)

$readmeActive = Join-Path $root "README.md"
$readmeTemplate = Join-Path $tpl "README.md"
Assert-True "README mentions memory-audit timing (active)" (File-Contains $readmeActive "Pre-handoff")
Assert-True "README mentions memory-audit timing (template)" (File-Contains $readmeTemplate "Pre-handoff")

$runbookActive = Join-Path $root "docs\engineering\runbook.md"
Assert-True "Runbook mentions memory-audit timing" (File-Contains $runbookActive "Pre-handoff")

Assert-True "memory-audit routes template drift to US-0017 (active)" (File-Contains $auditActive "US-0017")
Assert-True "memory-audit routes template drift to US-0017 (template)" (File-Contains $auditTemplate "US-0017")

Assert-True "memory-audit scope boundary section exists (active)" (File-Contains $auditActive "Scope boundary: US-0024 vs US-0017")
Assert-True "memory-audit scope boundary section exists (template)" (File-Contains $auditTemplate "Scope boundary: US-0024 vs US-0017")

# 10) Remote config contract checks (US-0036)
$remoteActive = Join-Path $root ".cursor\remote.json"
$remoteTemplate = Join-Path $tpl ".cursor\remote.json"
Assert-True "remote.json exists (active)" (Test-Path $remoteActive -PathType Leaf)
Assert-True "remote.json exists (template)" (Test-Path $remoteTemplate -PathType Leaf)

try {
  $activeRemoteJson = Get-Content -Path $remoteActive -Raw | ConvertFrom-Json
  $activeSchemaOk = ($activeRemoteJson.version -is [int]) -and
    ([string]::IsNullOrWhiteSpace($activeRemoteJson.defaultTarget) -eq $false) -and
    ($activeRemoteJson.targets.Count -ge 2)
  Assert-True "remote.json schema valid (active)" $activeSchemaOk
} catch {
  Assert-True "remote.json schema valid (active)" $false $_.Exception.Message
}

try {
  $templateRemoteJson = Get-Content -Path $remoteTemplate -Raw | ConvertFrom-Json
  $templateSchemaOk = ($templateRemoteJson.version -is [int]) -and
    ([string]::IsNullOrWhiteSpace($templateRemoteJson.defaultTarget) -eq $false) -and
    ($templateRemoteJson.targets.Count -ge 2)
  Assert-True "remote.json schema valid (template)" $templateSchemaOk
} catch {
  Assert-True "remote.json schema valid (template)" $false $_.Exception.Message
}

Assert-True "README documents remote mode-aware behavior (active)" (File-Contains $readmeActive "REMOTE_EXECUTION=0")
Assert-True "README documents remote mode-aware behavior (template)" (File-Contains $readmeTemplate "REMOTE_EXECUTION=0")
Assert-True "Runbook documents remote fail-fast format" (File-Contains $runbookActive "[REMOTE_CONFIG_ERROR]")

$executeActive = Join-Path $root ".cursor\commands\execute.md"
$executeTemplate = Join-Path $tpl ".cursor\commands\execute.md"
Assert-True "execute command has remote fail-fast guidance (active)" (File-Contains $executeActive "REMOTE_CONFIG_ERROR")
Assert-True "execute command has remote fail-fast guidance (template)" (File-Contains $executeTemplate "REMOTE_CONFIG_ERROR")
Assert-True "execute command includes disabled-mode skip guidance (active)" (File-Contains $executeActive "REMOTE_EXECUTION=0")
Assert-True "execute command includes disabled-mode skip guidance (template)" (File-Contains $executeTemplate "REMOTE_EXECUTION=0")

Assert-True "runbook lists negative path: missing config" (File-Contains $runbookActive "Missing config file")
Assert-True "runbook lists negative path: malformed JSON" (File-Contains $runbookActive "Malformed JSON")
Assert-True "runbook lists negative path: invalid value or enum" (File-Contains $runbookActive "Invalid value or enum")
Assert-True "runbook lists negative path: security violation" (File-Contains $runbookActive "Security violation")

# 11) Auto continuation deterministic contract checks (US-0037)
$autoActive = Join-Path $root ".cursor\commands\auto.md"
$autoTemplate = Join-Path $tpl ".cursor\commands\auto.md"
$resumeActive = Join-Path $root ".cursor\commands\resume.md"
$resumeTemplate = Join-Path $tpl ".cursor\commands\resume.md"
$pauseActive = Join-Path $root ".cursor\commands\pause.md"
$pauseTemplate = Join-Path $tpl ".cursor\commands\pause.md"
$coreActive = Join-Path $root ".cursor\rules\core.mdc"
$coreTemplate = Join-Path $tpl ".cursor\rules\core.mdc"

Assert-True "auto includes explicit start-from contract (active)" (File-Contains $autoActive "start-from=<phase>")
Assert-True "auto includes explicit start-from contract (template)" (File-Contains $autoTemplate "start-from=<phase>")

Assert-True "auto precedence includes argument > resume > state (active)" (File-Contains $autoActive "Resolve start phase in strict order:")
Assert-True "auto precedence includes argument > resume > state (template)" (File-Contains $autoTemplate "Resolve start phase in strict order:")

Assert-True "auto requires fail-fast on stale resume brief (active)" (File-Contains $autoActive "present but stale or unparseable, fail fast")
Assert-True "auto requires fail-fast on stale resume brief (template)" (File-Contains $autoTemplate "present but stale or unparseable, fail fast")

Assert-True "auto includes AUTO_RESUME_ERROR format (active)" (File-Contains $autoActive "[AUTO_RESUME_ERROR] <code>: <summary>. Source=<source>. Fix: <action>.")
Assert-True "auto includes AUTO_RESUME_ERROR format (template)" (File-Contains $autoTemplate "[AUTO_RESUME_ERROR] <code>: <summary>. Source=<source>. Fix: <action>.")

Assert-True "auto includes required error code INVALID_START_FROM (active)" (File-Contains $autoActive "INVALID_START_FROM")
Assert-True "auto includes required error code RESUME_STATE_CONFLICT (active)" (File-Contains $autoActive "RESUME_STATE_CONFLICT")
Assert-True "auto includes required error code STATE_PHASE_UNRECOVERABLE (active)" (File-Contains $autoActive "STATE_PHASE_UNRECOVERABLE")
Assert-True "auto includes required error code INVALID_START_FROM (template)" (File-Contains $autoTemplate "INVALID_START_FROM")
Assert-True "auto includes required error code RESUME_STATE_CONFLICT (template)" (File-Contains $autoTemplate "RESUME_STATE_CONFLICT")
Assert-True "auto includes required error code STATE_PHASE_UNRECOVERABLE (template)" (File-Contains $autoTemplate "STATE_PHASE_UNRECOVERABLE")

Assert-True "auto includes breadcrumb fields (active)" (File-Contains $autoActive "resolution_source")
Assert-True "auto includes breadcrumb stop reason (active)" (File-Contains $autoActive "stop_reason")
Assert-True "auto includes breadcrumb fields (template)" (File-Contains $autoTemplate "resolution_source")
Assert-True "auto includes breadcrumb stop reason (template)" (File-Contains $autoTemplate "stop_reason")

Assert-True "pause references AUTO_RESUME_ERROR contract (active)" (File-Contains $pauseActive "[AUTO_RESUME_ERROR]")
Assert-True "pause references AUTO_RESUME_ERROR contract (template)" (File-Contains $pauseTemplate "[AUTO_RESUME_ERROR]")

Assert-True "resume references deterministic precedence guidance (active)" (File-Contains $resumeActive "argument > resume brief > state fallback")
Assert-True "resume references deterministic precedence guidance (template)" (File-Contains $resumeTemplate "argument > resume brief > state fallback")

Assert-True "core rule defines DEC-0017 continuation contract (active)" (File-Contains $coreActive "DEC-0017")
Assert-True "core rule defines DEC-0017 continuation contract (template)" (File-Contains $coreTemplate "DEC-0017")
Assert-True "core rule preserves stop conditions in continuation mode (active)" (File-Contains $coreActive "Preserve existing stop/gate controls in continuation mode")
Assert-True "core rule preserves stop conditions in continuation mode (template)" (File-Contains $coreTemplate "Preserve existing stop/gate controls in continuation mode")

# 12) Sync policy guarded auto-push checks (US-0038)
$scratchpadActive = Join-Path $root ".cursor\scratchpad.md"
$scratchpadTemplate = Join-Path $tpl ".cursor\scratchpad.md"
$runbookTemplate = Join-Path $tpl "docs\engineering\runbook.md"
$validatePs1 = Join-Path $root "scripts\validate-and-push.ps1"
$validateSh = Join-Path $root "scripts\validate-and-push.sh"

Assert-True "scratchpad includes SYNC_POLICY_MODE (active)" (File-Contains $scratchpadActive "SYNC_POLICY_MODE")
Assert-True "scratchpad includes SYNC_POLICY_MODE (template)" (File-Contains $scratchpadTemplate "SYNC_POLICY_MODE")
Assert-True "scratchpad includes AUTO_PUSH_BRANCH_ALLOWLIST (active)" (File-Contains $scratchpadActive "AUTO_PUSH_BRANCH_ALLOWLIST")
Assert-True "scratchpad includes AUTO_PUSH_BRANCH_ALLOWLIST (template)" (File-Contains $scratchpadTemplate "AUTO_PUSH_BRANCH_ALLOWLIST")

Assert-True "auto command documents guarded eligibility chain (active)" (File-Contains $autoActive "Guarded auto-push eligibility chain")
Assert-True "auto command documents guarded eligibility chain (template)" (File-Contains $autoTemplate "Guarded auto-push eligibility chain")
Assert-True "auto command includes BRANCH_NOT_ALLOWLISTED reason code (active)" (File-Contains $autoActive "BRANCH_NOT_ALLOWLISTED")
Assert-True "auto command includes BRANCH_NOT_ALLOWLISTED reason code (template)" (File-Contains $autoTemplate "BRANCH_NOT_ALLOWLISTED")
Assert-True "runbook documents sync reason code TEST_TIMEOUT (active)" (File-Contains $runbookActive "TEST_TIMEOUT")
Assert-True "runbook documents sync reason code TEST_TIMEOUT (template)" (File-Contains $runbookTemplate "TEST_TIMEOUT")

Assert-True "validate-and-push.ps1 requires TEST_COMMAND" (File-Contains $validatePs1 "TEST_COMMAND is required by sync policy")
Assert-True "validate-and-push.sh requires TEST_COMMAND" (File-Contains $validateSh "TEST_COMMAND is required by sync policy")
Assert-True "validate-and-push.ps1 supports optional TYPECHECK_COMMAND" (File-Contains $validatePs1 "TYPECHECK_COMMAND")
Assert-True "validate-and-push.sh supports optional TYPECHECK_COMMAND" (File-Contains $validateSh "TYPECHECK_COMMAND")

# 13) Release queue + per-sprint notes contract checks (US-0040)
$releaseCommandActive = Join-Path $root ".cursor\commands\release.md"
$releaseCommandTemplate = Join-Path $tpl ".cursor\commands\release.md"
$releaseNotesActive = Join-Path $root "handoffs\release_notes.md"
$releaseQueueActive = Join-Path $root "handoffs\release_queue.md"
$releaseQueueTemplate = Join-Path $tpl "handoffs\release_queue.md"
$releaseNotesTemplate = Join-Path $tpl "handoffs\release_notes.md"
$sprintNotesTemplate = Join-Path $root "handoffs\releases\Sxxxx-release-notes.md"
$templateSprintNotesTemplate = Join-Path $tpl "handoffs\releases\Sxxxx-release-notes.md"

Assert-True "release queue artifact exists (active)" (Test-Path $releaseQueueActive -PathType Leaf)
Assert-True "release queue artifact exists (template)" (Test-Path $releaseQueueTemplate -PathType Leaf)
Assert-True "sprint notes template exists (active)" (Test-Path $sprintNotesTemplate -PathType Leaf)
Assert-True "sprint notes template exists (template)" (Test-Path $templateSprintNotesTemplate -PathType Leaf)

Assert-True "release command references sprint-scoped canonical notes path (active)" (File-Contains $releaseCommandActive "handoffs/releases/Sxxxx-release-notes.md")
Assert-True "release command references sprint-scoped canonical notes path (template)" (File-Contains $releaseCommandTemplate "handoffs/releases/Sxxxx-release-notes.md")
Assert-True "release command references canonical queue artifact (active)" (File-Contains $releaseCommandActive "handoffs/release_queue.md")
Assert-True "release command references canonical queue artifact (template)" (File-Contains $releaseCommandTemplate "handoffs/release_queue.md")

Assert-True "release command enforces target sprint only mutation (active)" (File-Contains $releaseCommandActive "only the target sprint row may")
Assert-True "release command enforces target sprint only mutation (template)" (File-Contains $releaseCommandTemplate "only the target sprint row may")
Assert-True "release command defines unresolved sprint fail-safe (active)" (File-Contains $releaseCommandActive "RELEASE_SPRINT_UNRESOLVED")
Assert-True "release command defines unresolved sprint fail-safe (template)" (File-Contains $releaseCommandTemplate "RELEASE_SPRINT_UNRESOLVED")
Assert-True "release command defines mismatch reason code QUEUE_ENTRY_MISSING (active)" (File-Contains $releaseCommandActive "QUEUE_ENTRY_MISSING")
Assert-True "release command defines mismatch reason code NOTES_REF_MISSING (active)" (File-Contains $releaseCommandActive "NOTES_REF_MISSING")
Assert-True "release command defines mismatch reason code STATUS_TRANSITION_INVALID (active)" (File-Contains $releaseCommandActive "STATUS_TRANSITION_INVALID")
Assert-True "release command defines legacy unresolved migration reason code (active)" (File-Contains $releaseCommandActive "LEGACY_NOTES_SPRINT_UNRESOLVED")
Assert-True "release command defines legacy unresolved migration reason code (template)" (File-Contains $releaseCommandTemplate "LEGACY_NOTES_SPRINT_UNRESOLVED")

Assert-True "legacy release notes file documents pointer compatibility (active)" (File-Contains $releaseNotesActive "Legacy Compatibility Pointer")
Assert-True "legacy release notes file references queue visibility (active)" (File-Contains $releaseNotesActive "handoffs/release_queue.md")
Assert-True "legacy release notes file documents pointer compatibility (template)" (File-Contains $releaseNotesTemplate "Legacy Compatibility Pointer")
Assert-True "legacy release notes file references queue visibility (template)" (File-Contains $releaseNotesTemplate "handoffs/release_queue.md")

Assert-True "runbook documents release queue contract (active)" (File-Contains $runbookActive "Release queue and sprint notes contract")
Assert-True "runbook documents release queue contract (template)" (File-Contains $runbookTemplate "Release queue and sprint notes contract")
Assert-True "README documents US-0040 release notes model (active)" (File-Contains $readmeActive "Release notes model (US-0040)")
Assert-True "README documents US-0040 release notes model (template)" (File-Contains $readmeTemplate "Release notes model (US-0040)")

# Cleanup
if (Test-Path (Join-Path $root "tests\.tmp-install")) {
  Remove-Item -Recurse -Force (Join-Path $root "tests\.tmp-install") -ErrorAction SilentlyContinue
}

# Report
$reportPath = Join-Path $root "tests\report.md"
$timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
$passCount = ($Results | Where-Object { $_.Status -eq "PASS" }).Count
$failCount = ($Results | Where-Object { $_.Status -eq "FAIL" }).Count

@"
# its-magic Test Report

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
