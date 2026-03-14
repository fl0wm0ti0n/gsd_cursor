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
Assert-True "23 commands exist" ((Count-Files (Join-Path $tpl ".cursor\commands") "*.md") -eq 23)
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
Assert-True "Runbook documents US-0015 intentional empty commands (template)" (File-Contains $runbook "Intentional empty commands (US-0015)")

$ci = Join-Path $tpl ".github\workflows\ci.yml"
$deploy = Join-Path $tpl ".github\workflows\deploy.yml"
Assert-True "CI workflow references TEST_COMMAND" (File-Contains $ci "TEST_COMMAND")
Assert-True "CI workflow references LINT_COMMAND" (File-Contains $ci "LINT_COMMAND")
Assert-True "CI workflow references TYPECHECK_COMMAND" (File-Contains $ci "TYPECHECK_COMMAND")
Assert-True "Deploy workflow references DEPLOY_STAGING_COMMAND" (File-Contains $deploy "DEPLOY_STAGING_COMMAND")
Assert-True "Deploy workflow references DEPLOY_PROD_COMMAND" (File-Contains $deploy "DEPLOY_PROD_COMMAND")
Assert-True "README documents US-0015 intent contract (template)" (File-Contains (Join-Path $tpl "README.md") "US-0015 intent contract")

# 4b) Homebrew stable formula version sync (US-0016)
$pkgJsonPath = Join-Path $root "package.json"
$brewStable = Join-Path $root "packaging\homebrew\its-magic.rb"
try {
  $pkgVersion = (Get-Content -Path $pkgJsonPath -Raw | ConvertFrom-Json).version
  $brewStableRaw = Get-Content -Path $brewStable -Raw
  Assert-True "Homebrew stable formula URL uses npm version tag" ($brewStableRaw -match [regex]::Escape("v$pkgVersion.tar.gz"))
  Assert-True "Homebrew stable formula version matches npm version" ($brewStableRaw -match [regex]::Escape("version `"$pkgVersion`""))
} catch {
  Assert-True "Homebrew stable formula version sync checks" $false $_.Exception.Message
}

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
    $manifestInstalled = Test-Path (Join-Path $tempRoot "docs\engineering\context\installer-owned-paths.manifest")
    $freshStatusReport = Join-Path $tempRoot "docs\engineering\status-normalization-report.md"
    $freshResearch = Join-Path $tempRoot "docs\engineering\research.md"
    Assert-True "Installer (ps1) installs commands" $installed
    Assert-True "Installer (ps1) installs ownership manifest" $manifestInstalled
    Assert-True "Fresh install has neutral status-normalization report" (File-Contains $freshStatusReport "(none yet)")
    Assert-True "Fresh install has no seeded status-normalization row" (-not (File-Contains $freshStatusReport "US-0018"))
    Assert-True "Fresh install research has no hardcoded DEC-0011 reference" (-not (File-Contains $freshResearch "DEC-0011"))
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
    $scratchpadExample = Join-Path $upgradeTemp ".cursor\scratchpad.local.example.md"
    $scratchpadLocal = Join-Path $upgradeTemp ".cursor\scratchpad.local.md"
    Set-Content -Path $scratchpadExample -Value "modified-local-example-marker"
    Set-Content -Path $scratchpadLocal -Value "user-local-marker=keep"

    Invoke-Installer $installer @("-Target", $upgradeTemp, "-Mode", "upgrade")

    $frameworkRestored = -not ((Get-Content -Path $frameworkFile -Raw) -match "modified-framework")
    Assert-True "Upgrade restores framework files" $frameworkRestored

    $userPreserved = (Get-Content -Path $userFile -Raw) -match "My Custom Vision"
    Assert-True "Upgrade preserves user data" $userPreserved

    $scratchpadExampleRefreshed = -not ((Get-Content -Path $scratchpadExample -Raw) -match "modified-local-example-marker") -and
      (Get-Content -Path $scratchpadExample -Raw) -match "RELEASE_PUBLISH_MODE=confirm"
    Assert-True "Upgrade refreshes scratchpad local example" $scratchpadExampleRefreshed

    $scratchpadLocalPreserved = (Get-Content -Path $scratchpadLocal -Raw) -match "user-local-marker=keep"
    Assert-True "Upgrade preserves user scratchpad local overrides" $scratchpadLocalPreserved

    $versionUpdated = (Test-Path $versionFile -PathType Leaf)
    Assert-True "Version file updated after upgrade" $versionUpdated
  } catch {
    Assert-True "Upgrade test" $false $_.Exception.Message
  }

  if (Test-Path $upgradeTemp) { Remove-Item -Recurse -Force $upgradeTemp -ErrorAction SilentlyContinue }
}

# 9) Clean-repo safety test (direct installer path)
if (Test-Path $installer -PathType Leaf) {
  $cleanTemp = Join-Path $root "tests\.tmp-cleanrepo"
  if (Test-Path $cleanTemp) { Remove-Item -Recurse -Force $cleanTemp -ErrorAction SilentlyContinue }
  New-Item -ItemType Directory -Path $cleanTemp | Out-Null

  try {
    Invoke-Installer $installer @("-Target", $cleanTemp, "-Mode", "missing", "-Create")

    $markerDir = Join-Path $cleanTemp "src"
    New-Item -ItemType Directory -Path $markerDir -Force | Out-Null
    $markerFile = Join-Path $markerDir "keep.txt"
    Set-Content -Path $markerFile -Value "non-framework marker"

    Invoke-Installer $installer @("-Target", $cleanTemp, "-CleanRepo", "-Yes")

    $frameworkRemoved = -not (Test-Path (Join-Path $cleanTemp ".cursor") -PathType Container) -and
      -not (Test-Path (Join-Path $cleanTemp "docs\engineering") -PathType Container) -and
      -not (Test-Path (Join-Path $cleanTemp "docs\user-guides") -PathType Container) -and
      -not (Test-Path (Join-Path $cleanTemp "scripts\validate-and-push.ps1") -PathType Leaf) -and
      -not (Test-Path (Join-Path $cleanTemp "scripts\validate-and-push.sh") -PathType Leaf) -and
      -not (Test-Path (Join-Path $cleanTemp ".github\workflows\ci.yml") -PathType Leaf) -and
      -not (Test-Path (Join-Path $cleanTemp ".github\workflows\deploy.yml") -PathType Leaf) -and
      -not (Test-Path (Join-Path $cleanTemp ".its-magic-version") -PathType Leaf)
    $markerPreserved = Test-Path $markerFile -PathType Leaf
    Assert-True "Clean-repo removes framework artifacts (installer)" $frameworkRemoved
    Assert-True "Clean-repo preserves non-framework marker (installer)" $markerPreserved
  } catch {
    Assert-True "Clean-repo safety test (installer)" $false $_.Exception.Message
  }

  if (Test-Path $cleanTemp) { Remove-Item -Recurse -Force $cleanTemp -ErrorAction SilentlyContinue }
}

# 10) CLI lifecycle tests (`its-magic` command path)
$cli = Join-Path $root "bin\its-magic.js"
$nodeCmd = Get-Command node -ErrorAction SilentlyContinue
if ((Test-Path $cli -PathType Leaf) -and $nodeCmd) {
  $cliTemp = Join-Path $root "tests\.tmp-cli-lifecycle"
  if (Test-Path $cliTemp) { Remove-Item -Recurse -Force $cliTemp -ErrorAction SilentlyContinue }
  New-Item -ItemType Directory -Path $cliTemp | Out-Null

  try {
    & node $cli --target $cliTemp --mode missing --create | Out-Null
    Assert-True "CLI missing install writes version file" (Test-Path (Join-Path $cliTemp ".its-magic-version") -PathType Leaf)
    Assert-True "CLI missing install writes command file" (Test-Path (Join-Path $cliTemp ".cursor\commands\intake.md") -PathType Leaf)
    Assert-True "CLI missing install writes ownership manifest" (Test-Path (Join-Path $cliTemp "docs\engineering\context\installer-owned-paths.manifest") -PathType Leaf)
    Assert-True "CLI missing install status-normalization report is neutral" (File-Contains (Join-Path $cliTemp "docs\engineering\status-normalization-report.md") "(none yet)")
    Assert-True "CLI missing install research has no DEC-0011 reference" (-not (File-Contains (Join-Path $cliTemp "docs\engineering\research.md") "DEC-0011"))

    $cliFrameworkFile = Join-Path $cliTemp ".cursor\commands\intake.md"
    Set-Content -Path $cliFrameworkFile -Value "cli-overwrite-marker"
    & node $cli --target $cliTemp --mode overwrite --backup | Out-Null
    $cliBackupDir = Get-ChildItem -Path (Join-Path $cliTemp "backups") -Directory -ErrorAction SilentlyContinue | Select-Object -First 1
    $cliBackupOk = $false
    if ($cliBackupDir) {
      $cliBackupOk = Test-Path (Join-Path $cliBackupDir.FullName ".cursor\commands\intake.md")
    }
    Assert-True "CLI overwrite mode creates backup snapshot" $cliBackupOk

    $cliUserFile = Join-Path $cliTemp "docs\product\vision.md"
    Set-Content -Path $cliUserFile -Value "# CLI User Data Marker"
    Set-Content -Path $cliFrameworkFile -Value "cli-upgrade-framework-marker"
    $cliScratchpadExample = Join-Path $cliTemp ".cursor\scratchpad.local.example.md"
    $cliScratchpadLocal = Join-Path $cliTemp ".cursor\scratchpad.local.md"
    Set-Content -Path $cliScratchpadExample -Value "cli-modified-local-example-marker"
    Set-Content -Path $cliScratchpadLocal -Value "cli-local-marker=keep"
    & node $cli --target $cliTemp --mode upgrade | Out-Null
    $cliFrameworkRestored = -not ((Get-Content -Path $cliFrameworkFile -Raw) -match "cli-upgrade-framework-marker")
    $cliUserPreserved = (Get-Content -Path $cliUserFile -Raw) -match "CLI User Data Marker"
    $cliScratchpadExampleRefreshed = -not ((Get-Content -Path $cliScratchpadExample -Raw) -match "cli-modified-local-example-marker") -and
      (Get-Content -Path $cliScratchpadExample -Raw) -match "RELEASE_PUBLISH_MODE=confirm"
    $cliScratchpadLocalPreserved = (Get-Content -Path $cliScratchpadLocal -Raw) -match "cli-local-marker=keep"
    Assert-True "CLI upgrade restores framework files" $cliFrameworkRestored
    Assert-True "CLI upgrade preserves user data" $cliUserPreserved
    Assert-True "CLI upgrade refreshes scratchpad local example" $cliScratchpadExampleRefreshed
    Assert-True "CLI upgrade preserves user scratchpad local overrides" $cliScratchpadLocalPreserved

    $markerDir = Join-Path $cliTemp "src"
    New-Item -ItemType Directory -Path $markerDir -Force | Out-Null
    $markerFile = Join-Path $markerDir "keep.txt"
    Set-Content -Path $markerFile -Value "cli-marker"
    & node $cli --clean-repo --target $cliTemp --yes | Out-Null
    $cliFrameworkRemoved = -not (Test-Path (Join-Path $cliTemp ".cursor") -PathType Container) -and
      -not (Test-Path (Join-Path $cliTemp "docs\engineering") -PathType Container) -and
      -not (Test-Path (Join-Path $cliTemp "docs\user-guides") -PathType Container) -and
      -not (Test-Path (Join-Path $cliTemp "scripts\validate-and-push.ps1") -PathType Leaf) -and
      -not (Test-Path (Join-Path $cliTemp "scripts\validate-and-push.sh") -PathType Leaf) -and
      -not (Test-Path (Join-Path $cliTemp ".github\workflows\ci.yml") -PathType Leaf) -and
      -not (Test-Path (Join-Path $cliTemp ".github\workflows\deploy.yml") -PathType Leaf) -and
      -not (Test-Path (Join-Path $cliTemp ".its-magic-version") -PathType Leaf)
    $cliMarkerPreserved = Test-Path $markerFile -PathType Leaf
    Assert-True "CLI clean-repo removes framework artifacts" $cliFrameworkRemoved
    Assert-True "CLI clean-repo preserves non-framework marker" $cliMarkerPreserved
  } catch {
    Assert-True "CLI lifecycle tests" $false $_.Exception.Message
  }

  try {
    & node $cli --target $cliTemp --mode invalid-mode 2>&1 | Out-Null
    Assert-True "CLI invalid mode fails fast" ($LASTEXITCODE -ne 0)
  } catch {
    Assert-True "CLI invalid mode fails fast" $true
  }

  if (Test-Path $cliTemp) { Remove-Item -Recurse -Force $cliTemp -ErrorAction SilentlyContinue }
} else {
  Assert-True "CLI lifecycle preconditions (node + bin/its-magic.js)" $false
}

# 11) Memory-audit command checks (US-0024)
$auditActive = Join-Path $root ".cursor\commands\memory-audit.md"
$auditTemplate = Join-Path $tpl ".cursor\commands\memory-audit.md"
Assert-True "memory-audit command exists (active)" (Test-Path $auditActive -PathType Leaf)
Assert-True "memory-audit command exists (template)" (Test-Path $auditTemplate -PathType Leaf)

$readmeActive = Join-Path $root "README.md"
$readmeTemplate = Join-Path $tpl "README.md"
Assert-True "README documents US-0015 intent contract (active)" (File-Contains $readmeActive "US-0015 intent contract")
Assert-True "README mentions memory-audit timing (active)" (File-Contains $readmeActive "Pre-handoff")
Assert-True "README mentions memory-audit timing (template)" (File-Contains $readmeTemplate "Pre-handoff")

$runbookActive = Join-Path $root "docs\engineering\runbook.md"
Assert-True "Runbook documents US-0015 intentional empty commands (active)" (File-Contains $runbookActive "Intentional empty commands (US-0015)")
Assert-True "Runbook mentions memory-audit timing" (File-Contains $runbookActive "Pre-handoff")

Assert-True "memory-audit routes template drift to US-0017 (active)" (File-Contains $auditActive "US-0017")
Assert-True "memory-audit routes template drift to US-0017 (template)" (File-Contains $auditTemplate "US-0017")

Assert-True "memory-audit scope boundary section exists (active)" (File-Contains $auditActive "Scope boundary: US-0024 vs US-0017")
Assert-True "memory-audit scope boundary section exists (template)" (File-Contains $auditTemplate "Scope boundary: US-0024 vs US-0017")

# 12) Remote config contract checks (US-0036)
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

# 13) Auto continuation deterministic contract checks (US-0037)
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
Assert-True "auto documents optional backlog-drain mode (active)" (File-Contains $autoActive "Optional backlog-drain mode (US-0044 / DEC-0022)")
Assert-True "auto documents optional backlog-drain mode (template)" (File-Contains $autoTemplate "Optional backlog-drain mode (US-0044 / DEC-0022)")
Assert-True "auto includes backlog drain reason BACKLOG_MAX_STORIES_REACHED (active)" (File-Contains $autoActive "BACKLOG_MAX_STORIES_REACHED")
Assert-True "auto includes backlog drain reason BACKLOG_MAX_STORIES_REACHED (template)" (File-Contains $autoTemplate "BACKLOG_MAX_STORIES_REACHED")

Assert-True "pause references AUTO_RESUME_ERROR contract (active)" (File-Contains $pauseActive "[AUTO_RESUME_ERROR]")
Assert-True "pause references AUTO_RESUME_ERROR contract (template)" (File-Contains $pauseTemplate "[AUTO_RESUME_ERROR]")

Assert-True "resume references deterministic precedence guidance (active)" (File-Contains $resumeActive "argument > resume brief > state fallback")
Assert-True "resume references deterministic precedence guidance (template)" (File-Contains $resumeTemplate "argument > resume brief > state fallback")

Assert-True "core rule defines DEC-0017 continuation contract (active)" (File-Contains $coreActive "DEC-0017")
Assert-True "core rule defines DEC-0017 continuation contract (template)" (File-Contains $coreTemplate "DEC-0017")
Assert-True "core rule preserves stop conditions in continuation mode (active)" (File-Contains $coreActive "Preserve existing stop/gate controls in continuation mode")
Assert-True "core rule preserves stop conditions in continuation mode (template)" (File-Contains $coreTemplate "Preserve existing stop/gate controls in continuation mode")

# 14) Sync policy guarded auto-push checks (US-0038)
$scratchpadActive = Join-Path $root ".cursor\scratchpad.md"
$scratchpadTemplate = Join-Path $tpl ".cursor\scratchpad.md"
$runbookTemplate = Join-Path $tpl "docs\engineering\runbook.md"
$validatePs1 = Join-Path $root "scripts\validate-and-push.ps1"
$validateSh = Join-Path $root "scripts\validate-and-push.sh"

Assert-True "scratchpad includes SYNC_POLICY_MODE (active)" (File-Contains $scratchpadActive "SYNC_POLICY_MODE")
Assert-True "scratchpad includes SYNC_POLICY_MODE (template)" (File-Contains $scratchpadTemplate "SYNC_POLICY_MODE")
Assert-True "scratchpad includes AUTO_PUSH_BRANCH_ALLOWLIST (active)" (File-Contains $scratchpadActive "AUTO_PUSH_BRANCH_ALLOWLIST")
Assert-True "scratchpad includes AUTO_PUSH_BRANCH_ALLOWLIST (template)" (File-Contains $scratchpadTemplate "AUTO_PUSH_BRANCH_ALLOWLIST")
Assert-True "scratchpad includes AUTO_BACKLOG_DRAIN (active)" (File-Contains $scratchpadActive "AUTO_BACKLOG_DRAIN")
Assert-True "scratchpad includes AUTO_BACKLOG_DRAIN (template)" (File-Contains $scratchpadTemplate "AUTO_BACKLOG_DRAIN")
Assert-True "scratchpad includes AUTO_BACKLOG_MAX_STORIES (active)" (File-Contains $scratchpadActive "AUTO_BACKLOG_MAX_STORIES")
Assert-True "scratchpad includes AUTO_BACKLOG_MAX_STORIES (template)" (File-Contains $scratchpadTemplate "AUTO_BACKLOG_MAX_STORIES")

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

# 15) Release queue + per-sprint notes contract checks (US-0040)
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

# 16) Post-QA release findings workflow checks (US-0042)
$releaseToDevActive = Join-Path $root "handoffs\release_to_dev.md"
$releaseToDevTemplate = Join-Path $tpl "handoffs\release_to_dev.md"
$releaseFindingsTemplate = Join-Path $tpl "sprints\S0001\release-findings.md"

Assert-True "release command references release findings artifact (active)" (File-Contains $releaseCommandActive "sprints/Sxxxx/release-findings.md")
Assert-True "release command references release findings artifact (template)" (File-Contains $releaseCommandTemplate "sprints/Sxxxx/release-findings.md")
Assert-True "release command references release_to_dev handoff (active)" (File-Contains $releaseCommandActive "handoffs/release_to_dev.md")
Assert-True "release command references release_to_dev handoff (template)" (File-Contains $releaseCommandTemplate "handoffs/release_to_dev.md")
Assert-True "release command includes release gate fail reason RELEASE_TEST_FAILED (active)" (File-Contains $releaseCommandActive "RELEASE_TEST_FAILED")
Assert-True "release command includes release gate fail reason RELEASE_TEST_FAILED (template)" (File-Contains $releaseCommandTemplate "RELEASE_TEST_FAILED")

Assert-True "release_to_dev handoff exists (active)" (Test-Path $releaseToDevActive -PathType Leaf)
Assert-True "release_to_dev handoff exists (template)" (Test-Path $releaseToDevTemplate -PathType Leaf)
Assert-True "release findings template exists (template)" (Test-Path $releaseFindingsTemplate -PathType Leaf)

Assert-True "runbook documents post-QA release issue workflow (active)" (File-Contains $runbookActive "Post-QA release issue workflow (US-0042)")
Assert-True "runbook documents post-QA release issue workflow (template)" (File-Contains $runbookTemplate "Post-QA release issue workflow (US-0042)")
Assert-True "README documents post-QA release issue workflow (active)" (File-Contains $readmeActive "Post-QA release issue workflow (US-0042)")
Assert-True "README documents post-QA release issue workflow (template)" (File-Contains $readmeTemplate "Post-QA release issue workflow (US-0042)")

# 17) Backlog reconciliation invariant checks (US-0043)
Assert-True "release command documents backlog reconciliation contract (active)" (File-Contains $releaseCommandActive "Backlog reconciliation contract (US-0043 / DEC-0021)")
Assert-True "release command documents backlog reconciliation contract (template)" (File-Contains $releaseCommandTemplate "Backlog reconciliation contract (US-0043 / DEC-0021)")
Assert-True "release command includes drift reason code BACKLOG_STATUS_DRIFT (active)" (File-Contains $releaseCommandActive "BACKLOG_STATUS_DRIFT")
Assert-True "release command includes drift reason code BACKLOG_STATUS_DRIFT (template)" (File-Contains $releaseCommandTemplate "BACKLOG_STATUS_DRIFT")
Assert-True "runbook documents backlog reconciliation invariant (active)" (File-Contains $runbookActive "Backlog reconciliation invariant (US-0043)")
Assert-True "runbook documents backlog reconciliation invariant (template)" (File-Contains $runbookTemplate "Backlog reconciliation invariant (US-0043)")
Assert-True "README documents backlog reconciliation invariant (active)" (File-Contains $readmeActive "Backlog reconciliation invariant (US-0043)")
Assert-True "README documents backlog reconciliation invariant (template)" (File-Contains $readmeTemplate "Backlog reconciliation invariant (US-0043)")
Assert-True "runbook documents optional backlog-drain auto mode (active)" (File-Contains $runbookActive "Optional backlog-drain auto mode (US-0044)")
Assert-True "runbook documents optional backlog-drain auto mode (template)" (File-Contains $runbookTemplate "Optional backlog-drain auto mode (US-0044)")
Assert-True "README documents optional backlog-drain auto mode (active)" (File-Contains $readmeActive "backlog-drain mode (US-0044)")
Assert-True "README documents optional backlog-drain auto mode (template)" (File-Contains $readmeTemplate "backlog-drain mode (US-0044)")

# 18) Explicit bulk sprint planning checks (US-0046)
$sprintPlanActive = Join-Path $root ".cursor\commands\sprint-plan.md"
$sprintPlanTemplate = Join-Path $tpl ".cursor\commands\sprint-plan.md"

Assert-True "sprint-plan supports explicit --bulk trigger (active)" (File-Contains $sprintPlanActive "--bulk")
Assert-True "sprint-plan supports explicit --bulk trigger (template)" (File-Contains $sprintPlanTemplate "--bulk")
Assert-True "sprint-plan documents SPRINT_BULK_MAX_STORIES (active)" (File-Contains $sprintPlanActive "SPRINT_BULK_MAX_STORIES")
Assert-True "sprint-plan documents SPRINT_BULK_MAX_STORIES (template)" (File-Contains $sprintPlanTemplate "SPRINT_BULK_MAX_STORIES")
Assert-True "sprint-plan includes bounded bulk stop reason (active)" (File-Contains $sprintPlanActive "SPRINT_BULK_MAX_SPRINTS_REACHED")
Assert-True "sprint-plan includes bounded bulk stop reason (template)" (File-Contains $sprintPlanTemplate "SPRINT_BULK_MAX_SPRINTS_REACHED")

Assert-True "scratchpad includes SPRINT_BULK_MAX_STORIES (active)" (File-Contains $scratchpadActive "SPRINT_BULK_MAX_STORIES")
Assert-True "scratchpad includes SPRINT_BULK_MAX_STORIES (template)" (File-Contains $scratchpadTemplate "SPRINT_BULK_MAX_STORIES")
Assert-True "scratchpad includes SPRINT_BULK_MAX_SPRINTS (active)" (File-Contains $scratchpadActive "SPRINT_BULK_MAX_SPRINTS")
Assert-True "scratchpad includes SPRINT_BULK_MAX_SPRINTS (template)" (File-Contains $scratchpadTemplate "SPRINT_BULK_MAX_SPRINTS")

Assert-True "runbook documents explicit bulk sprint planning mode (active)" (File-Contains $runbookActive "Explicit bulk sprint planning mode (US-0046)")
Assert-True "runbook documents explicit bulk sprint planning mode (template)" (File-Contains $runbookTemplate "Explicit bulk sprint planning mode (US-0046)")
Assert-True "README documents explicit sprint-plan bulk mode (active)" (File-Contains $readmeActive "sprint-plan --bulk")
Assert-True "README documents explicit sprint-plan bulk mode (template)" (File-Contains $readmeTemplate "sprint-plan --bulk")

# 19) Explicit bulk execute orchestration checks (US-0047)
Assert-True "auto command documents explicit --execute-bulk argument (active)" (File-Contains $autoActive "--execute-bulk")
Assert-True "auto command documents explicit --execute-bulk argument (template)" (File-Contains $autoTemplate "--execute-bulk")
Assert-True "auto command documents AUTO_EXECUTE_BULK control (active)" (File-Contains $autoActive "AUTO_EXECUTE_BULK")
Assert-True "auto command documents AUTO_EXECUTE_BULK control (template)" (File-Contains $autoTemplate "AUTO_EXECUTE_BULK")
Assert-True "auto command includes EXEC_BULK_MAX_ITEMS_REACHED reason code (active)" (File-Contains $autoActive "EXEC_BULK_MAX_ITEMS_REACHED")
Assert-True "auto command includes EXEC_TEAM_SCOPE_BLOCKED reason code (active)" (File-Contains $autoActive "EXEC_TEAM_SCOPE_BLOCKED")
Assert-True "auto command includes EXEC_BULK_MAX_ITEMS_REACHED reason code (template)" (File-Contains $autoTemplate "EXEC_BULK_MAX_ITEMS_REACHED")
Assert-True "auto command includes EXEC_TEAM_SCOPE_BLOCKED reason code (template)" (File-Contains $autoTemplate "EXEC_TEAM_SCOPE_BLOCKED")

Assert-True "scratchpad includes AUTO_EXECUTE_BULK (active)" (File-Contains $scratchpadActive "AUTO_EXECUTE_BULK")
Assert-True "scratchpad includes AUTO_EXECUTE_BULK (template)" (File-Contains $scratchpadTemplate "AUTO_EXECUTE_BULK")
Assert-True "scratchpad includes AUTO_EXECUTE_MAX_ITEMS (active)" (File-Contains $scratchpadActive "AUTO_EXECUTE_MAX_ITEMS")
Assert-True "scratchpad includes AUTO_EXECUTE_MAX_ITEMS (template)" (File-Contains $scratchpadTemplate "AUTO_EXECUTE_MAX_ITEMS")
Assert-True "scratchpad includes AUTO_TEAM_SCOPE_ENFORCE (active)" (File-Contains $scratchpadActive "AUTO_TEAM_SCOPE_ENFORCE")
Assert-True "scratchpad includes AUTO_TEAM_SCOPE_ENFORCE (template)" (File-Contains $scratchpadTemplate "AUTO_TEAM_SCOPE_ENFORCE")

Assert-True "runbook documents explicit bulk execute mode (active)" (File-Contains $runbookActive "Explicit bulk execute mode (US-0047)")
Assert-True "runbook documents explicit bulk execute mode (template)" (File-Contains $runbookTemplate "Explicit bulk execute mode (US-0047)")
Assert-True "README documents explicit auto execute bulk mode (active)" (File-Contains $readmeActive "auto --execute-bulk")
Assert-True "README documents explicit auto execute bulk mode (template)" (File-Contains $readmeTemplate "auto --execute-bulk")

Assert-True "execute command documents team-scope guardrails (active)" (File-Contains $executeActive "Team-scope guardrails for bulk execute mode")
Assert-True "execute command documents team-scope guardrails (template)" (File-Contains $executeTemplate "Team-scope guardrails for bulk execute mode")

# 20) Canonical status + normalization guard checks (US-0045)
$statusReportActive = Join-Path $root "docs\engineering\status-normalization-report.md"
$statusReportTemplate = Join-Path $tpl "docs\engineering\status-normalization-report.md"

Assert-True "release command documents canonical status guard section (active)" (File-Contains $releaseCommandActive "Canonical status source and global drift guard (US-0045 / DEC-0025)")
Assert-True "release command documents canonical status guard section (template)" (File-Contains $releaseCommandTemplate "Canonical status source and global drift guard (US-0045 / DEC-0025)")
Assert-True "release command includes CANONICAL_STATUS_CONFLICT reason code (active)" (File-Contains $releaseCommandActive "CANONICAL_STATUS_CONFLICT")
Assert-True "release command includes CANONICAL_STATUS_CONFLICT reason code (template)" (File-Contains $releaseCommandTemplate "CANONICAL_STATUS_CONFLICT")
Assert-True "auto documents canonical status contract (active)" (File-Contains $autoActive "Canonical status contract (US-0045)")
Assert-True "auto documents canonical status contract (template)" (File-Contains $autoTemplate "Canonical status contract (US-0045)")
Assert-True "execute documents canonical status contract (active)" (File-Contains $executeActive "Canonical status contract (US-0045)")
Assert-True "execute documents canonical status contract (template)" (File-Contains $executeTemplate "Canonical status contract (US-0045)")
Assert-True "sprint-plan documents planning source clarification (active)" (File-Contains $sprintPlanActive "Planning source clarification (US-0045)")
Assert-True "sprint-plan documents planning source clarification (template)" (File-Contains $sprintPlanTemplate "Planning source clarification (US-0045)")
Assert-True "runbook documents canonical ownership guard (active)" (File-Contains $runbookActive "Canonical status ownership and normalization guard (US-0045)")
Assert-True "runbook documents canonical ownership guard (template)" (File-Contains $runbookTemplate "Canonical status ownership and normalization guard (US-0045)")
Assert-True "README documents canonical story status guard (active)" (File-Contains $readmeActive "Canonical story status + normalization guard (US-0045)")
Assert-True "README documents canonical story status guard (template)" (File-Contains $readmeTemplate "Canonical story status + normalization guard (US-0045)")
Assert-True "status normalization report exists (active)" (Test-Path $statusReportActive -PathType Leaf)
Assert-True "status normalization report exists (template)" (Test-Path $statusReportTemplate -PathType Leaf)
Assert-True "status normalization report contains baseline row (active)" (File-Contains $statusReportActive "US-0018")
Assert-True "status normalization report template is neutral" (File-Contains $statusReportTemplate "(none yet)")

# 21) Guided intake mode checks (US-0033)
$intakeActive = Join-Path $root ".cursor\commands\intake.md"
$intakeTemplate = Join-Path $tpl ".cursor\commands\intake.md"
$poAgentActive = Join-Path $root ".cursor\agents\po.mdc"
$poAgentTemplate = Join-Path $tpl ".cursor\agents\po.mdc"

Assert-True "scratchpad includes INTAKE_GUIDED_MODE (active)" (File-Contains $scratchpadActive "INTAKE_GUIDED_MODE")
Assert-True "scratchpad includes INTAKE_GUIDED_MODE (template)" (File-Contains $scratchpadTemplate "INTAKE_GUIDED_MODE")
Assert-True "intake command documents guided mode (active)" (File-Contains $intakeActive "Guided mode behavior")
Assert-True "intake command documents guided mode (template)" (File-Contains $intakeTemplate "Guided mode behavior")
Assert-True "intake command documents low-touch mode (active)" (File-Contains $intakeActive "Low-touch behavior")
Assert-True "intake command documents low-touch mode (template)" (File-Contains $intakeTemplate "Low-touch behavior")
Assert-True "intake low-touch keeps duplicate safety (active)" (File-Contains $intakeActive "duplicate safety")
Assert-True "intake low-touch keeps duplicate safety (template)" (File-Contains $intakeTemplate "duplicate safety")
Assert-True "PO agent documents guided intake mode (active)" (File-Contains $poAgentActive "Guided intake mode")
Assert-True "PO agent documents guided intake mode (template)" (File-Contains $poAgentTemplate "Guided intake mode")
Assert-True "PO agent documents low-touch mode (active)" (File-Contains $poAgentActive "Low-touch mode")
Assert-True "PO agent documents low-touch mode (template)" (File-Contains $poAgentTemplate "Low-touch mode")
Assert-True "runbook documents guided intake mode (active)" (File-Contains $runbookActive "Guided intake mode (US-0033)")
Assert-True "runbook documents guided intake mode (template)" (File-Contains $runbookTemplate "Guided intake mode (US-0033)")
Assert-True "README documents guided intake behavior (active)" (File-Contains $readmeActive "Guided intake behavior (US-0033)")
Assert-True "README documents guided intake behavior (template)" (File-Contains $readmeTemplate "Guided intake behavior (US-0033)")

# 21b) Intake decomposition + risk-aware questioning checks (US-0051)
Assert-True "intake command documents deterministic decomposition evaluator (active)" (File-Contains $intakeActive "deterministic decomposition evaluator")
Assert-True "intake command documents deterministic decomposition evaluator (template)" (File-Contains $intakeTemplate "deterministic decomposition evaluator")
Assert-True "intake command preserves accept/merge/adjust user control (active)" (File-Contains $intakeActive "accept**, **merge**, or **adjust")
Assert-True "intake command preserves accept/merge/adjust user control (template)" (File-Contains $intakeTemplate "accept**, **merge**, or **adjust")
Assert-True "intake command documents bounded questioning (active)" (File-Contains $intakeActive "Keep questioning bounded")
Assert-True "intake command documents bounded questioning (template)" (File-Contains $intakeTemplate "Keep questioning bounded")
Assert-True "intake low-touch keeps no forced decomposition (active)" (File-Contains $intakeActive "single-story default (no forced decomposition)")
Assert-True "intake low-touch keeps no forced decomposition (template)" (File-Contains $intakeTemplate "single-story default (no forced decomposition)")

Assert-True "PO agent documents decomposition evaluator (active)" (File-Contains $poAgentActive "deterministic decomposition evaluator")
Assert-True "PO agent documents decomposition evaluator (template)" (File-Contains $poAgentTemplate "deterministic decomposition evaluator")
Assert-True "PO agent documents risk-triggered questioning (active)" (File-Contains $poAgentActive "breadth/risk is high")
Assert-True "PO agent documents risk-triggered questioning (template)" (File-Contains $poAgentTemplate "breadth/risk is high")
Assert-True "PO agent keeps low-touch single-story default (active)" (File-Contains $poAgentActive "single-story default unless user explicitly requests decomposition")
Assert-True "PO agent keeps low-touch single-story default (template)" (File-Contains $poAgentTemplate "single-story default unless user explicitly requests decomposition")

Assert-True "runbook documents intake decomposition and risk-aware questioning (active)" (File-Contains $runbookActive "Intake decomposition and risk-aware questioning (US-0051)")
Assert-True "runbook documents intake decomposition and risk-aware questioning (template)" (File-Contains $runbookTemplate "Intake decomposition and risk-aware questioning (US-0051)")
Assert-True "README documents intake decomposition and risk-aware questioning (active)" (File-Contains $readmeActive "Intake decomposition + risk-aware questioning (US-0051)")
Assert-True "README documents intake decomposition and risk-aware questioning (template)" (File-Contains $readmeTemplate "Intake decomposition + risk-aware questioning (US-0051)")

# 21c) Optional ID namespace bootstrap checks (US-0052)
$researchActive = Join-Path $root ".cursor\commands\research.md"
$researchTemplate = Join-Path $tpl ".cursor\commands\research.md"
$architectureCommandActive = Join-Path $root ".cursor\commands\architecture.md"
$architectureCommandTemplate = Join-Path $tpl ".cursor\commands\architecture.md"
$tlAgentActive = Join-Path $root ".cursor\agents\tech-lead.mdc"
$tlAgentTemplate = Join-Path $tpl ".cursor\agents\tech-lead.mdc"

Assert-True "scratchpad includes ID_NAMESPACE_BOOTSTRAP (active)" (File-Contains $scratchpadActive "ID_NAMESPACE_BOOTSTRAP")
Assert-True "scratchpad includes ID_NAMESPACE_BOOTSTRAP (template)" (File-Contains $scratchpadTemplate "ID_NAMESPACE_BOOTSTRAP")
Assert-True "intake command documents optional ID bootstrap (active)" (File-Contains $intakeActive "Optional fresh-project ID namespace bootstrap (US-0052 / DEC-0034)")
Assert-True "intake command documents optional ID bootstrap (template)" (File-Contains $intakeTemplate "Optional fresh-project ID namespace bootstrap (US-0052 / DEC-0034)")
Assert-True "intake command includes ineligible bootstrap diagnostic (active)" (File-Contains $intakeActive "ID_BOOTSTRAP_NOT_FRESH")
Assert-True "intake command includes ineligible bootstrap diagnostic (template)" (File-Contains $intakeTemplate "ID_BOOTSTRAP_NOT_FRESH")
Assert-True "research command documents bootstrap-aware ID policy (active)" (File-Contains $researchActive "ID_NAMESPACE_BOOTSTRAP=1")
Assert-True "research command documents bootstrap-aware ID policy (template)" (File-Contains $researchTemplate "ID_NAMESPACE_BOOTSTRAP=1")
Assert-True "architecture command documents DEC bootstrap policy (active)" (File-Contains $architectureCommandActive "DEC-0001")
Assert-True "architecture command documents DEC bootstrap policy (template)" (File-Contains $architectureCommandTemplate "DEC-0001")
Assert-True "PO agent documents story ID bootstrap policy (active)" (File-Contains $poAgentActive "Story ID policy (US-0052 / DEC-0034)")
Assert-True "PO agent documents story ID bootstrap policy (template)" (File-Contains $poAgentTemplate "Story ID policy (US-0052 / DEC-0034)")
Assert-True "Tech Lead agent documents decision ID bootstrap policy (active)" (File-Contains $tlAgentActive "Decision ID policy (US-0052 / DEC-0034)")
Assert-True "Tech Lead agent documents decision ID bootstrap policy (template)" (File-Contains $tlAgentTemplate "Decision ID policy (US-0052 / DEC-0034)")
Assert-True "runbook documents optional ID namespace bootstrap (active)" (File-Contains $runbookActive "Optional ID namespace bootstrap (US-0052)")
Assert-True "runbook documents optional ID namespace bootstrap (template)" (File-Contains $runbookTemplate "Optional ID namespace bootstrap (US-0052)")
Assert-True "README documents optional ID namespace bootstrap (active)" (File-Contains $readmeActive "Optional ID namespace bootstrap (US-0052)")
Assert-True "README documents optional ID namespace bootstrap (template)" (File-Contains $readmeTemplate "Optional ID namespace bootstrap (US-0052)")

# 21d) Context compaction and token profile checks (US-0053)
$askCommandActive = Join-Path $root ".cursor\commands\ask.md"
$askCommandTemplate = Join-Path $tpl ".cursor\commands\ask.md"
$stateArchiveReadmeActive = Join-Path $root "docs\engineering\state-archive\README.md"
$stateArchiveReadmeTemplate = Join-Path $tpl "docs\engineering\state-archive\README.md"
$stateActive = Join-Path $root "docs\engineering\state.md"
$stateTemplate = Join-Path $tpl "docs\engineering\state.md"
$decisionsIndexActive = Join-Path $root "docs\engineering\decisions.md"
$decisionsIndexTemplate = Join-Path $tpl "docs\engineering\decisions.md"

Assert-True "scratchpad includes TOKEN_PROFILE (active)" (File-Contains $scratchpadActive "TOKEN_PROFILE=balanced")
Assert-True "scratchpad includes TOKEN_PROFILE (template)" (File-Contains $scratchpadTemplate "TOKEN_PROFILE=balanced")
Assert-True "scratchpad documents manual override precedence (active)" (File-Contains $scratchpadActive "Manual-override precedence")
Assert-True "scratchpad documents manual override precedence (template)" (File-Contains $scratchpadTemplate "Manual-override precedence")
Assert-True "runbook documents context compaction and token profile mode (active)" (File-Contains $runbookActive "Context compaction and token profile mode (US-0053 / DEC-0035)")
Assert-True "runbook documents context compaction and token profile mode (template)" (File-Contains $runbookTemplate "Context compaction and token profile mode (US-0053 / DEC-0035)")
Assert-True "README documents context compaction and tiered token profile (active)" (File-Contains $readmeActive "Context compaction + tiered token profile (US-0053)")
Assert-True "README documents context compaction and tiered token profile (template)" (File-Contains $readmeTemplate "Context compaction + tiered token profile (US-0053)")
Assert-True "ask command documents narrow-read policy (active)" (File-Contains $askCommandActive "Apply narrow-read retrieval policy (US-0053)")
Assert-True "ask command documents narrow-read policy (template)" (File-Contains $askCommandTemplate "Apply narrow-read retrieval policy (US-0053)")
Assert-True "state documents active context surface policy (active)" (File-Contains $stateActive "Active context surface (US-0053 / DEC-0035)")
Assert-True "state template documents active context surface policy" (File-Contains $stateTemplate "Active context surface (US-0053 / DEC-0035)")
Assert-True "state archive README exists (active)" (Test-Path $stateArchiveReadmeActive -PathType Leaf)
Assert-True "state archive README exists (template)" (Test-Path $stateArchiveReadmeTemplate -PathType Leaf)
Assert-True "decisions index is compacted (active)" (File-Contains $decisionsIndexActive "Compact decision index (bounded summaries)")
Assert-True "decisions index includes canonical full records pointer (active)" (File-Contains $decisionsIndexActive "Full records live in decisions/DEC-xxxx.md")
Assert-True "decisions index includes canonical full records pointer (template)" (File-Contains $decisionsIndexTemplate "Full records live in decisions/DEC-xxxx.md")
Assert-True "release gate chain remains documented (active)" (File-Contains $releaseCommandActive "Release gate chain (US-0039 / DEC-0019)")
Assert-True "release gate chain remains documented (template)" (File-Contains $releaseCommandTemplate "Release gate chain (US-0039 / DEC-0019)")

# 21e) Configurable multi-target publish checks (US-0054)
$releaseTargetsActive = Join-Path $root "docs\engineering\release-targets.json"
$releaseTargetsTemplate = Join-Path $tpl "docs\engineering\release-targets.json"

Assert-True "scratchpad includes RELEASE_PUBLISH_MODE (active)" (File-Contains $scratchpadActive "RELEASE_PUBLISH_MODE=confirm")
Assert-True "scratchpad includes RELEASE_PUBLISH_MODE (template)" (File-Contains $scratchpadTemplate "RELEASE_PUBLISH_MODE=confirm")
Assert-True "scratchpad includes RELEASE_TARGETS_FILE (active)" (File-Contains $scratchpadActive "RELEASE_TARGETS_FILE=docs/engineering/release-targets.json")
Assert-True "scratchpad includes RELEASE_TARGETS_FILE (template)" (File-Contains $scratchpadTemplate "RELEASE_TARGETS_FILE=docs/engineering/release-targets.json")
Assert-True "runbook documents configurable multi-target publish mode (active)" (File-Contains $runbookActive "Configurable multi-target publish mode (US-0054 / DEC-0036)")
Assert-True "runbook documents configurable multi-target publish mode (template)" (File-Contains $runbookTemplate "Configurable multi-target publish mode (US-0054 / DEC-0036)")
Assert-True "README documents configurable multi-target publish mode (active)" (File-Contains $readmeActive "Configurable multi-target publish + confirmation gate (US-0054)")
Assert-True "README documents configurable multi-target publish mode (template)" (File-Contains $readmeTemplate "Configurable multi-target publish + confirmation gate (US-0054)")
Assert-True "release command includes configurable publish target section (active)" (File-Contains $releaseCommandActive "Optional configurable publish targets (US-0054 / DEC-0036)")
Assert-True "release command includes configurable publish target section (template)" (File-Contains $releaseCommandTemplate "Optional configurable publish targets (US-0054 / DEC-0036)")
Assert-True "release command includes publish config invalid reason code (active)" (File-Contains $releaseCommandActive "PUBLISH_TARGET_CONFIG_INVALID")
Assert-True "release command includes publish config invalid reason code (template)" (File-Contains $releaseCommandTemplate "PUBLISH_TARGET_CONFIG_INVALID")
Assert-True "release targets schema file exists (active)" (Test-Path $releaseTargetsActive -PathType Leaf)
Assert-True "release targets schema file exists (template)" (Test-Path $releaseTargetsTemplate -PathType Leaf)
Assert-True "release targets schema includes custom target type (active)" (File-Contains $releaseTargetsActive '"type": "custom"')
Assert-True "release targets schema includes ssh target type (active)" (File-Contains $releaseTargetsActive '"type": "ssh"')
Assert-True "release targets schema includes ssh target type (template)" (File-Contains $releaseTargetsTemplate '"type": "ssh"')

# 21f) Deterministic status reconciliation checks (US-0055)
$statusReconcileCommandActive = Join-Path $root ".cursor\commands\status-reconcile.md"
$statusReconcileCommandTemplate = Join-Path $tpl ".cursor\commands\status-reconcile.md"

Assert-True "status-reconcile command exists (active)" (Test-Path $statusReconcileCommandActive -PathType Leaf)
Assert-True "status-reconcile command exists (template)" (Test-Path $statusReconcileCommandTemplate -PathType Leaf)
Assert-True "status-reconcile command defines canonical precedence (active)" (File-Contains $statusReconcileCommandActive "Canonical precedence (US-0045 / DEC-0025)")
Assert-True "status-reconcile command defines canonical precedence (template)" (File-Contains $statusReconcileCommandTemplate "Canonical precedence (US-0045 / DEC-0025)")
Assert-True "status-reconcile command includes deterministic reason code STATUS_RECONCILE_APPLIED (active)" (File-Contains $statusReconcileCommandActive "STATUS_RECONCILE_APPLIED")
Assert-True "status-reconcile command includes deterministic reason code STATUS_RECONCILE_APPLIED (template)" (File-Contains $statusReconcileCommandTemplate "STATUS_RECONCILE_APPLIED")
Assert-True "runbook documents deterministic status reconciliation mode (active)" (File-Contains $runbookActive "Deterministic status reconciliation mode (US-0055 / DEC-0037)")
Assert-True "runbook documents deterministic status reconciliation mode (template)" (File-Contains $runbookTemplate "Deterministic status reconciliation mode (US-0055 / DEC-0037)")
Assert-True "README documents deterministic status reconciliation command (active)" (File-Contains $readmeActive "Deterministic status reconciliation command (US-0055)")
Assert-True "README documents deterministic status reconciliation command (template)" (File-Contains $readmeTemplate "Deterministic status reconciliation command (US-0055)")

# 21g) Upgrade-safe scratchpad example checks (US-0057)
$scratchpadLocalExampleActive = Join-Path $root ".cursor\scratchpad.local.example.md"
$scratchpadLocalExampleTemplate = Join-Path $tpl ".cursor\scratchpad.local.example.md"

Assert-True "scratchpad local example exists (active)" (Test-Path $scratchpadLocalExampleActive -PathType Leaf)
Assert-True "scratchpad local example exists (template)" (Test-Path $scratchpadLocalExampleTemplate -PathType Leaf)
Assert-True "scratchpad local example includes token profile override (active)" (File-Contains $scratchpadLocalExampleActive "TOKEN_PROFILE=balanced")
Assert-True "scratchpad local example includes detailed core behavior descriptions (active)" (File-Contains $scratchpadLocalExampleActive "- MAGIC_CONTEXT_STRICT: 0|1")
Assert-True "scratchpad local example includes detailed automation descriptions (template)" (File-Contains $scratchpadLocalExampleTemplate "- AUTO_FLOW_MODE: manual|auto_until_decision")
Assert-True "scratchpad local example includes release publish mode override (active)" (File-Contains $scratchpadLocalExampleActive "RELEASE_PUBLISH_MODE=confirm")
Assert-True "scratchpad local example includes release publish mode override (template)" (File-Contains $scratchpadLocalExampleTemplate "RELEASE_PUBLISH_MODE=confirm")
Assert-True "runbook documents scratchpad upgrade contract (active)" (File-Contains $runbookActive "Scratchpad example upgrade contract (US-0057 / DEC-0039)")
Assert-True "runbook documents scratchpad upgrade contract (template)" (File-Contains $runbookTemplate "Scratchpad example upgrade contract (US-0057 / DEC-0039)")
Assert-True "README documents scratchpad upgrade behavior (active)" (File-Contains $readmeActive "Upgrade behavior (US-0057):")
Assert-True "README documents scratchpad upgrade behavior (template)" (File-Contains $readmeTemplate "Upgrade behavior (US-0057):")

# 21h) Deterministic artifact ordering checks (US-0058)
$autoCmdActiveUs0058 = Join-Path $root ".cursor\commands\auto.md"
$autoCmdTemplateUs0058 = Join-Path $tpl ".cursor\commands\auto.md"
$artifactOrderingPolicyActive = Join-Path $root "docs\engineering\artifact-ordering-policy.md"
$artifactOrderingPolicyTemplate = Join-Path $tpl "docs\engineering\artifact-ordering-policy.md"

Assert-True "artifact ordering policy exists (active)" (Test-Path $artifactOrderingPolicyActive -PathType Leaf)
Assert-True "artifact ordering policy exists (template)" (Test-Path $artifactOrderingPolicyTemplate -PathType Leaf)
Assert-True "artifact ordering policy defines state append-bottom (active)" (File-Contains $artifactOrderingPolicyActive "docs/engineering/state.md")
Assert-True "artifact ordering policy defines backlog sorted-canonical (active)" (File-Contains $artifactOrderingPolicyActive "sorted-canonical")
Assert-True "artifact ordering policy includes anchor ambiguous reason code (active)" (File-Contains $artifactOrderingPolicyActive "ARTIFACT_ORDERING_ANCHOR_AMBIGUOUS")
Assert-True "auto command includes ordering guard (active)" (File-Contains $autoCmdActiveUs0058 "Deterministic artifact ordering guard (US-0058 / DEC-0040)")
Assert-True "auto command includes ordering guard (template)" (File-Contains $autoCmdTemplateUs0058 "Deterministic artifact ordering guard (US-0058 / DEC-0040)")
Assert-True "intake command includes ordering contract (active)" (File-Contains $intakeActive "Deterministic artifact ordering contract (US-0058 / DEC-0040)")
Assert-True "intake command includes ordering contract (template)" (File-Contains $intakeTemplate "Deterministic artifact ordering contract (US-0058 / DEC-0040)")
Assert-True "release command includes ordering contract (active)" (File-Contains $releaseCommandActive "Deterministic artifact ordering contract (US-0058 / DEC-0040)")
Assert-True "release command includes ordering contract (template)" (File-Contains $releaseCommandTemplate "Deterministic artifact ordering contract (US-0058 / DEC-0040)")
Assert-True "refresh-context includes ordering contract (active)" (File-Contains (Join-Path $root ".cursor\commands\refresh-context.md") "Deterministic artifact ordering contract (US-0058 / DEC-0040)")
Assert-True "refresh-context includes ordering contract (template)" (File-Contains (Join-Path $tpl ".cursor\commands\refresh-context.md") "Deterministic artifact ordering contract (US-0058 / DEC-0040)")
Assert-True "status-reconcile includes ordering contract (active)" (File-Contains $statusReconcileCommandActive "Deterministic artifact ordering contract (US-0058 / DEC-0040)")
Assert-True "status-reconcile includes ordering contract (template)" (File-Contains $statusReconcileCommandTemplate "Deterministic artifact ordering contract (US-0058 / DEC-0040)")
Assert-True "runbook documents deterministic artifact ordering mode (active)" (File-Contains $runbookActive "Deterministic artifact ordering and write discipline (US-0058 / DEC-0040)")
Assert-True "runbook documents deterministic artifact ordering mode (template)" (File-Contains $runbookTemplate "Deterministic artifact ordering and write discipline (US-0058 / DEC-0040)")
Assert-True "README documents deterministic ordering behavior (active)" (File-Contains $readmeActive "Deterministic ordering behavior (US-0058):")
Assert-True "README documents deterministic ordering behavior (template)" (File-Contains $readmeTemplate "Deterministic ordering behavior (US-0058):")
Assert-True "artifact ordering policy includes non-monotonic state timestamp reason code (active)" (File-Contains $artifactOrderingPolicyActive "STATE_TIMESTAMP_NON_MONOTONIC")
Assert-True "artifact ordering policy includes non-monotonic state timestamp reason code (template)" (File-Contains $artifactOrderingPolicyTemplate "STATE_TIMESTAMP_NON_MONOTONIC")

# 21i) Intake runtime capability and writer-safety checks (US-0059)
Assert-True "scratchpad includes INTAKE_SUBAGENT_FALLBACK (active)" (File-Contains $scratchpadActive "INTAKE_SUBAGENT_FALLBACK=deny")
Assert-True "scratchpad includes INTAKE_SUBAGENT_FALLBACK (template)" (File-Contains $scratchpadTemplate "INTAKE_SUBAGENT_FALLBACK=deny")
Assert-True "scratchpad local example includes INTAKE_SUBAGENT_FALLBACK (active)" (File-Contains $scratchpadLocalExampleActive "INTAKE_SUBAGENT_FALLBACK=deny")
Assert-True "scratchpad local example includes INTAKE_SUBAGENT_FALLBACK (template)" (File-Contains $scratchpadLocalExampleTemplate "INTAKE_SUBAGENT_FALLBACK=deny")
Assert-True "intake command documents capability fail-fast code (active)" (File-Contains $intakeActive "SUBAGENT_CAPABILITY_UNAVAILABLE")
Assert-True "intake command documents capability fail-fast code (template)" (File-Contains $intakeTemplate "SUBAGENT_CAPABILITY_UNAVAILABLE")
Assert-True "intake command documents concurrent writer fail-safe code (active)" (File-Contains $intakeActive "INTAKE_CONCURRENT_WRITER_DETECTED")
Assert-True "intake command documents concurrent writer fail-safe code (template)" (File-Contains $intakeTemplate "INTAKE_CONCURRENT_WRITER_DETECTED")
Assert-True "runbook documents intake runtime capability and writer safety mode (active)" (File-Contains $runbookActive "Intake runtime capability and single-writer safety (US-0059 / DEC-0041)")
Assert-True "runbook documents intake runtime capability and writer safety mode (template)" (File-Contains $runbookTemplate "Intake runtime capability and single-writer safety (US-0059 / DEC-0041)")
Assert-True "README documents intake runtime safety behavior (active)" (File-Contains $readmeActive "Intake runtime safety behavior (US-0059):")
Assert-True "README documents intake runtime safety behavior (template)" (File-Contains $readmeTemplate "Intake runtime safety behavior (US-0059):")

# 22) Optional cross-repo observability checks (US-0034)
$qaCommandActive = Join-Path $root ".cursor\commands\qa.md"
$qaCommandTemplate = Join-Path $tpl ".cursor\commands\qa.md"
$compatReportActive = Join-Path $root "docs\engineering\compatibility-report.md"
$compatReportTemplate = Join-Path $tpl "docs\engineering\compatibility-report.md"
$compatSignalsActive = Join-Path $root "docs\engineering\compatibility-signals.md"
$compatSignalsTemplate = Join-Path $tpl "docs\engineering\compatibility-signals.md"
$registryManifestActive = Join-Path $root "docs\engineering\manifests\registry.manifest.yaml"
$registryManifestTemplate = Join-Path $tpl "docs\engineering\manifests\registry.manifest.yaml"
$repoManifestActive = Join-Path $root "docs\engineering\manifests\repo.manifest.yaml"
$repoManifestTemplate = Join-Path $tpl "docs\engineering\manifests\repo.manifest.yaml"

Assert-True "scratchpad includes CROSS_REPO_OBSERVABILITY (active)" (File-Contains $scratchpadActive "CROSS_REPO_OBSERVABILITY")
Assert-True "scratchpad includes CROSS_REPO_OBSERVABILITY (template)" (File-Contains $scratchpadTemplate "CROSS_REPO_OBSERVABILITY")
Assert-True "scratchpad includes COMPATIBILITY_GATE_ON_CRITICAL (active)" (File-Contains $scratchpadActive "COMPATIBILITY_GATE_ON_CRITICAL")
Assert-True "scratchpad includes COMPATIBILITY_GATE_ON_CRITICAL (template)" (File-Contains $scratchpadTemplate "COMPATIBILITY_GATE_ON_CRITICAL")
Assert-True "scratchpad includes COMPATIBILITY_SOURCES (active)" (File-Contains $scratchpadActive "COMPATIBILITY_SOURCES")
Assert-True "scratchpad includes COMPATIBILITY_SOURCES (template)" (File-Contains $scratchpadTemplate "COMPATIBILITY_SOURCES")

Assert-True "intake command includes zero-overhead disabled behavior (active)" (File-Contains $intakeActive "CROSS_REPO_OBSERVABILITY=0")
Assert-True "intake command includes zero-overhead disabled behavior (template)" (File-Contains $intakeTemplate "CROSS_REPO_OBSERVABILITY=0")
Assert-True "architecture command includes compatibility mode contract (active)" (File-Contains $architectureCommandActive "Optional cross-repo observability architecture (US-0034)")
Assert-True "architecture command includes compatibility mode contract (template)" (File-Contains $architectureCommandTemplate "Optional cross-repo observability architecture (US-0034)")
Assert-True "execute command includes compatibility mode contract (active)" (File-Contains $executeActive "Optional compatibility observability execution contract (US-0034)")
Assert-True "execute command includes compatibility mode contract (template)" (File-Contains $executeTemplate "Optional compatibility observability execution contract (US-0034)")
Assert-True "qa command includes compatibility mode checks (active)" (File-Contains $qaCommandActive "Optional compatibility observability QA checks (US-0034)")
Assert-True "qa command includes compatibility mode checks (template)" (File-Contains $qaCommandTemplate "Optional compatibility observability QA checks (US-0034)")
Assert-True "release command includes compatibility critical reason code (active)" (File-Contains $releaseCommandActive "COMPATIBILITY_CRITICAL_OPEN")
Assert-True "release command includes compatibility critical reason code (template)" (File-Contains $releaseCommandTemplate "COMPATIBILITY_CRITICAL_OPEN")

Assert-True "runbook documents optional cross-repo observability mode (active)" (File-Contains $runbookActive "Optional cross-repo observability mode (US-0034)")
Assert-True "runbook documents optional cross-repo observability mode (template)" (File-Contains $runbookTemplate "Optional cross-repo observability mode (US-0034)")
Assert-True "README documents optional cross-repo observability (active)" (File-Contains $readmeActive "Optional cross-repo observability (US-0034)")
Assert-True "README documents optional cross-repo observability (template)" (File-Contains $readmeTemplate "Optional cross-repo observability (US-0034)")

Assert-True "compatibility report exists (active)" (Test-Path $compatReportActive -PathType Leaf)
Assert-True "compatibility report exists (template)" (Test-Path $compatReportTemplate -PathType Leaf)
Assert-True "compatibility signals exists (active)" (Test-Path $compatSignalsActive -PathType Leaf)
Assert-True "compatibility signals exists (template)" (Test-Path $compatSignalsTemplate -PathType Leaf)
Assert-True "registry manifest exists (active)" (Test-Path $registryManifestActive -PathType Leaf)
Assert-True "registry manifest exists (template)" (Test-Path $registryManifestTemplate -PathType Leaf)
Assert-True "repo manifest exists (active)" (Test-Path $repoManifestActive -PathType Leaf)
Assert-True "repo manifest exists (template)" (Test-Path $repoManifestTemplate -PathType Leaf)

# 23) Optional component-scoped execution checks (US-0035)
$componentScopeActive = Join-Path $root "docs\engineering\component-scope.md"
$componentScopeTemplate = Join-Path $tpl "docs\engineering\component-scope.md"
$componentScopeReportActive = Join-Path $root "docs\engineering\component-scope-report.md"
$componentScopeReportTemplate = Join-Path $tpl "docs\engineering\component-scope-report.md"

Assert-True "scratchpad includes COMPONENT_SCOPE_MODE (active)" (File-Contains $scratchpadActive "COMPONENT_SCOPE_MODE")
Assert-True "scratchpad includes COMPONENT_SCOPE_MODE (template)" (File-Contains $scratchpadTemplate "COMPONENT_SCOPE_MODE")
Assert-True "scratchpad includes TARGET_COMPONENTS (active)" (File-Contains $scratchpadActive "TARGET_COMPONENTS")
Assert-True "scratchpad includes TARGET_COMPONENTS (template)" (File-Contains $scratchpadTemplate "TARGET_COMPONENTS")

Assert-True "intake command includes component scope declaration contract (active)" (File-Contains $intakeActive "Optional component scope declaration (US-0035)")
Assert-True "intake command includes component scope declaration contract (template)" (File-Contains $intakeTemplate "Optional component scope declaration (US-0035)")
Assert-True "architecture command includes component scope contract (active)" (File-Contains $architectureCommandActive "Optional component-scope architecture (US-0035)")
Assert-True "architecture command includes component scope contract (template)" (File-Contains $architectureCommandTemplate "Optional component-scope architecture (US-0035)")
Assert-True "sprint-plan includes scoped task metadata contract (active)" (File-Contains $sprintPlanActive "Optional component-scoped planning (US-0035)")
Assert-True "sprint-plan includes scoped task metadata contract (template)" (File-Contains $sprintPlanTemplate "Optional component-scoped planning (US-0035)")
Assert-True "execute includes component-scope guardrails (active)" (File-Contains $executeActive "Optional component-scoped execution guardrails (US-0035)")
Assert-True "execute includes component-scope guardrails (template)" (File-Contains $executeTemplate "Optional component-scoped execution guardrails (US-0035)")
Assert-True "qa includes component-scope protection checks (active)" (File-Contains $qaCommandActive "Optional component-scope protection checks (US-0035)")
Assert-True "qa includes component-scope protection checks (template)" (File-Contains $qaCommandTemplate "Optional component-scope protection checks (US-0035)")
Assert-True "release includes component-scope violation reason code (active)" (File-Contains $releaseCommandActive "COMPONENT_SCOPE_VIOLATION_UNAPPROVED")
Assert-True "release includes component-scope violation reason code (template)" (File-Contains $releaseCommandTemplate "COMPONENT_SCOPE_VIOLATION_UNAPPROVED")

Assert-True "runbook documents optional component-scoped mode (active)" (File-Contains $runbookActive "Optional component-scoped execution mode (US-0035)")
Assert-True "runbook documents optional component-scoped mode (template)" (File-Contains $runbookTemplate "Optional component-scoped execution mode (US-0035)")
Assert-True "README documents optional component-scoped execution (active)" (File-Contains $readmeActive "Optional component-scoped execution (US-0035)")
Assert-True "README documents optional component-scoped execution (template)" (File-Contains $readmeTemplate "Optional component-scoped execution (US-0035)")

Assert-True "component scope artifact exists (active)" (Test-Path $componentScopeActive -PathType Leaf)
Assert-True "component scope artifact exists (template)" (Test-Path $componentScopeTemplate -PathType Leaf)
Assert-True "component scope report exists (active)" (Test-Path $componentScopeReportActive -PathType Leaf)
Assert-True "component scope report exists (template)" (Test-Path $componentScopeReportTemplate -PathType Leaf)

# 24) Optional spec-pack documentation checks (US-0031)
Assert-True "scratchpad includes SPEC_PACK_MODE (active)" (File-Contains $scratchpadActive "SPEC_PACK_MODE")
Assert-True "scratchpad includes SPEC_PACK_MODE (template)" (File-Contains $scratchpadTemplate "SPEC_PACK_MODE")
Assert-True "intake command includes spec-pack zero-overhead when disabled (active)" (File-Contains $intakeActive "SPEC_PACK_MODE=0")
Assert-True "intake command includes spec-pack zero-overhead when disabled (template)" (File-Contains $intakeTemplate "SPEC_PACK_MODE=0")
Assert-True "architecture command includes optional spec-pack step (active)" (File-Contains $architectureCommandActive "Optional spec-pack (US-0031)")
Assert-True "architecture command includes optional spec-pack step (template)" (File-Contains $architectureCommandTemplate "Optional spec-pack (US-0031)")
Assert-True "release command includes spec-pack completeness gate (active)" (File-Contains $releaseCommandActive "SPEC_PACK_INCOMPLETE")
Assert-True "release command includes spec-pack completeness gate (template)" (File-Contains $releaseCommandTemplate "SPEC_PACK_INCOMPLETE")
Assert-True "execute command includes optional spec-pack step (active)" (File-Contains $executeActive "Optional spec-pack (US-0031)")
Assert-True "execute command includes optional spec-pack step (template)" (File-Contains $executeTemplate "Optional spec-pack (US-0031)")
Assert-True "qa command includes optional spec-pack verification (active)" (File-Contains $qaCommandActive "Optional spec-pack verification (US-0031)")
Assert-True "qa command includes optional spec-pack verification (template)" (File-Contains $qaCommandTemplate "Optional spec-pack verification (US-0031)")
Assert-True "runbook documents optional spec-pack mode (active)" (File-Contains $runbookActive "Optional spec-pack documentation mode (US-0031)")
Assert-True "runbook documents optional spec-pack mode (template)" (File-Contains $runbookTemplate "Optional spec-pack documentation mode (US-0031)")
Assert-True "README documents optional spec-pack documentation (active)" (File-Contains $readmeActive "Optional spec-pack documentation (US-0031)")
Assert-True "README documents optional spec-pack documentation (template)" (File-Contains $readmeTemplate "Optional spec-pack documentation (US-0031)")
$specPackReadmeActive = Join-Path $root "docs\engineering\spec-pack\README.md"
$specPackReadmeTemplate = Join-Path $tpl "docs\engineering\spec-pack\README.md"
Assert-True "spec-pack README exists (active)" (Test-Path $specPackReadmeActive -PathType Leaf)
Assert-True "spec-pack README exists (template)" (Test-Path $specPackReadmeTemplate -PathType Leaf)

# 24b) Optional user-guide documentation checks (US-0032)
Assert-True "scratchpad includes USER_GUIDE_MODE (active)" (File-Contains $scratchpadActive "USER_GUIDE_MODE")
Assert-True "scratchpad includes USER_GUIDE_MODE (template)" (File-Contains $scratchpadTemplate "USER_GUIDE_MODE")
Assert-True "intake command includes user-guide zero-overhead when disabled (active)" (File-Contains $intakeActive "USER_GUIDE_MODE=0")
Assert-True "intake command includes user-guide zero-overhead when disabled (template)" (File-Contains $intakeTemplate "USER_GUIDE_MODE=0")
Assert-True "release command includes user-guide completeness gate (active)" (File-Contains $releaseCommandActive "USER_GUIDE_INCOMPLETE")
Assert-True "release command includes user-guide completeness gate (template)" (File-Contains $releaseCommandTemplate "USER_GUIDE_INCOMPLETE")
Assert-True "runbook documents optional user-guide mode (active)" (File-Contains $runbookActive "Optional user-guide documentation mode (US-0032)")
Assert-True "runbook documents optional user-guide mode (template)" (File-Contains $runbookTemplate "Optional user-guide documentation mode (US-0032)")
Assert-True "README documents optional user-guide documentation (active)" (File-Contains $readmeActive "Optional user-guide documentation (US-0032)")
Assert-True "README documents optional user-guide documentation (template)" (File-Contains $readmeTemplate "Optional user-guide documentation (US-0032)")
$userGuideReadmeActive = Join-Path $root "docs\user-guides\README.md"
$userGuideReadmeTemplate = Join-Path $tpl "docs\user-guides\README.md"
Assert-True "user-guides README exists (active)" (Test-Path $userGuideReadmeActive -PathType Leaf)
Assert-True "user-guides README exists (template)" (Test-Path $userGuideReadmeTemplate -PathType Leaf)

# 25) Release gate tightening checks (US-0039)
Assert-True "release command defines release gate chain US-0039 (active)" (File-Contains $releaseCommandActive "Release gate chain (US-0039 / DEC-0019)")
Assert-True "release command defines release gate chain US-0039 (template)" (File-Contains $releaseCommandTemplate "Release gate chain (US-0039 / DEC-0019)")
Assert-True "release command defines check-in test evidence validity (active)" (File-Contains $releaseCommandActive "RELEASE_TEST_EVIDENCE_MISSING")
Assert-True "release command defines check-in test evidence validity (template)" (File-Contains $releaseCommandTemplate "RELEASE_TEST_EVIDENCE_MISSING")
Assert-True "release command defines QA completion gate (active)" (File-Contains $releaseCommandActive "QA completion evidence gate (US-0039)")
Assert-True "release command defines QA completion gate (template)" (File-Contains $releaseCommandTemplate "QA completion evidence gate")
Assert-True "release command defines UAT completion gate (active)" (File-Contains $releaseCommandActive "UAT completion gate (US-0039)")
Assert-True "release command defines UAT completion gate (template)" (File-Contains $releaseCommandTemplate "UAT completion gate")
Assert-True "release command defines no-bypass default (active)" (File-Contains $releaseCommandActive "No-bypass default (US-0039)")
Assert-True "release command documents no bypass default (template)" (File-Contains $releaseCommandTemplate "no bypass")
Assert-True "release command defines override evidence contract (active)" (File-Contains $releaseCommandActive "RELEASE_GATE_OVERRIDE_APPROVED")
Assert-True "release command defines override evidence contract (template)" (File-Contains $releaseCommandTemplate "RELEASE_GATE_OVERRIDE_APPROVED")
Assert-True "runbook documents release gate chain US-0039 (active)" (File-Contains $runbookActive "Release gate chain (US-0039 / DEC-0019)")
Assert-True "runbook documents release gate chain US-0039 (template)" (File-Contains $runbookTemplate "Release gate chain (US-0039 / DEC-0019)")
Assert-True "runbook documents optional-command compatibility US-0039 (active)" (File-Contains $runbookActive "Optional-command compatibility (US-0039")
Assert-True "runbook documents optional-command compatibility US-0039 (template)" (File-Contains $runbookTemplate "Optional-command compatibility (US-0039")
Assert-True "qa command includes release gate prerequisite US-0039 (active)" (File-Contains $qaCommandActive "Release gate prerequisite (US-0039)")
Assert-True "qa command includes release gate prerequisite US-0039 (template)" (File-Contains $qaCommandTemplate "Release gate prerequisite (US-0039)")
Assert-True "core rule includes release gate no-bypass (active)" (File-Contains (Join-Path $root ".cursor\rules\core.mdc") "Release gate no-bypass (US-0039")

# 26) Per-phase isolation enforcement checks (US-0048)
$verifyWorkActive = Join-Path $root ".cursor\commands\verify-work.md"
$verifyWorkTemplate = Join-Path $tpl ".cursor\commands\verify-work.md"
$pauseCmdActive = Join-Path $root ".cursor\commands\pause.md"
$pauseCmdTemplate = Join-Path $tpl ".cursor\commands\pause.md"
$resumeCmdActive = Join-Path $root ".cursor\commands\resume.md"
$resumeCmdTemplate = Join-Path $tpl ".cursor\commands\resume.md"

Assert-True "auto enforces per-phase isolation (active)" (File-Contains $autoActive "Per-phase isolation enforcement (US-0048 / DEC-0029)")
Assert-True "auto enforces per-phase isolation (template)" (File-Contains $autoTemplate "Per-phase isolation enforcement (US-0048 / DEC-0029)")
Assert-True "auto includes isolation violation reason code (active)" (File-Contains $autoActive "PHASE_CONTEXT_ISOLATION_VIOLATION")
Assert-True "auto includes isolation violation reason code (template)" (File-Contains $autoTemplate "PHASE_CONTEXT_ISOLATION_VIOLATION")

Assert-True "runbook documents isolation evidence contract (active)" (File-Contains $runbookActive "Per-phase subagent isolation evidence (US-0048 / DEC-0029)")
Assert-True "runbook documents isolation evidence contract (template)" (File-Contains $runbookTemplate "Per-phase subagent isolation evidence (US-0048 / DEC-0029)")
Assert-True "runbook includes isolation reason code ISOLATION_EVIDENCE_INVALID (active)" (File-Contains $runbookActive "ISOLATION_EVIDENCE_INVALID")
Assert-True "runbook includes isolation reason code ISOLATION_EVIDENCE_INVALID (template)" (File-Contains $runbookTemplate "ISOLATION_EVIDENCE_INVALID")

Assert-True "verify-work includes isolation compliance gate (active)" (File-Contains $verifyWorkActive "Isolation compliance gate (US-0048 / DEC-0029)")
Assert-True "verify-work includes isolation compliance gate (template)" (File-Contains $verifyWorkTemplate "Isolation compliance gate (US-0048 / DEC-0029)")

Assert-True "release gate chain includes isolation gate (active)" (File-Contains $releaseCommandActive "Isolation compliance gate")
Assert-True "release gate chain includes isolation gate (template)" (File-Contains $releaseCommandTemplate "Isolation compliance gate")
Assert-True "release includes isolation reason code PHASE_CONTEXT_ISOLATION_MISSING (active)" (File-Contains $releaseCommandActive "PHASE_CONTEXT_ISOLATION_MISSING")
Assert-True "release includes isolation reason code PHASE_CONTEXT_ISOLATION_MISSING (template)" (File-Contains $releaseCommandTemplate "PHASE_CONTEXT_ISOLATION_MISSING")

Assert-True "pause records isolation provenance fields (active)" (File-Contains $pauseCmdActive "isolation_provenance_ref")
Assert-True "pause records isolation provenance fields (template)" (File-Contains $pauseCmdTemplate "isolation_provenance_ref")
Assert-True "resume validates isolation provenance (active)" (File-Contains $resumeCmdActive "Validate isolation provenance (US-0048 / DEC-0029)")
Assert-True "resume validates isolation provenance (template)" (File-Contains $resumeCmdTemplate "Validate isolation provenance (US-0048 / DEC-0029)")

Assert-True "README documents per-phase isolation evidence (active)" (File-Contains $readmeActive "Per-phase isolation evidence (US-0048 / DEC-0029)")
Assert-True "README documents per-phase isolation evidence (template)" (File-Contains $readmeTemplate "Per-phase isolation evidence (US-0048 / DEC-0029)")

Assert-True "dev agent documents isolation evidence (active)" (File-Contains (Join-Path $root ".cursor\agents\dev.mdc") "Isolation evidence (US-0048 / DEC-0029)")
Assert-True "dev agent documents isolation evidence (template)" (File-Contains (Join-Path $tpl ".cursor\agents\dev.mdc") "Isolation evidence (US-0048 / DEC-0029)")

# 26b) Strict runtime proof checks (US-0056)
Assert-True "auto documents strict runtime proof section (active)" (File-Contains $autoActive "Strict runtime proof enforcement (US-0056 / DEC-0038)")
Assert-True "auto documents strict runtime proof section (template)" (File-Contains $autoTemplate "Strict runtime proof enforcement (US-0056 / DEC-0038)")
Assert-True "auto includes runtime proof reason RUNTIME_PROOF_REUSED (active)" (File-Contains $autoActive "RUNTIME_PROOF_REUSED")
Assert-True "auto includes runtime proof reason RUNTIME_PROOF_REUSED (template)" (File-Contains $autoTemplate "RUNTIME_PROOF_REUSED")
Assert-True "auto includes strict-proof boundary step 11b (active)" (File-Contains $autoActive "11b. At each phase boundary, verify strict runtime attestation tuple exists")
Assert-True "auto includes strict-proof boundary step 11b (template)" (File-Contains $autoTemplate "11b. At each phase boundary, verify strict runtime attestation tuple exists")

Assert-True "verify-work documents strict runtime proof gate (active)" (File-Contains $verifyWorkActive "Strict runtime proof gate (US-0056 / DEC-0038)")
Assert-True "verify-work documents strict runtime proof gate (template)" (File-Contains $verifyWorkTemplate "Strict runtime proof gate (US-0056 / DEC-0038)")
Assert-True "release includes strict runtime proof gate (active)" (File-Contains $releaseCommandActive "Strict runtime proof gate (US-0056 / DEC-0038)")
Assert-True "release includes strict runtime proof gate (template)" (File-Contains $releaseCommandTemplate "Strict runtime proof gate (US-0056 / DEC-0038)")
Assert-True "release includes runtime proof reason code RUNTIME_PROOF_MISSING (active)" (File-Contains $releaseCommandActive "RUNTIME_PROOF_MISSING")
Assert-True "release includes runtime proof reason code RUNTIME_PROOF_MISSING (template)" (File-Contains $releaseCommandTemplate "RUNTIME_PROOF_MISSING")

Assert-True "runbook documents strict runtime proof contract (active)" (File-Contains $runbookActive "Strict runtime proof contract (US-0056 / DEC-0038)")
Assert-True "runbook documents strict runtime proof contract (template)" (File-Contains $runbookTemplate "Strict runtime proof contract (US-0056 / DEC-0038)")
Assert-True "README documents strict runtime proof section (active)" (File-Contains $readmeActive "Strict runtime proof (US-0056 / DEC-0038)")
Assert-True "README documents strict runtime proof section (template)" (File-Contains $readmeTemplate "Strict runtime proof (US-0056 / DEC-0038)")

# 27) Legacy DONE-story drift detection and guard (US-0049)
$legacyAuditActive = Join-Path $root "docs\engineering\legacy-drift-audit.md"
$legacyAuditTemplate = Join-Path $tpl "docs\engineering\legacy-drift-audit.md"
Assert-True "legacy-drift-audit.md exists at canonical path (active)" (Test-Path $legacyAuditActive -PathType Leaf)
Assert-True "legacy-drift-audit.md exists at canonical path (template)" (Test-Path $legacyAuditTemplate -PathType Leaf)
Assert-True "legacy-drift-audit schema includes reason_code and evidence_ref (active)" (File-Contains $legacyAuditActive "reason_code")
Assert-True "legacy-drift-audit schema includes reason_code and evidence_ref (template)" (File-Contains $legacyAuditTemplate "reason_code")
Assert-True "runbook documents Legacy DONE-story drift detection and guard (US-0049) (active)" (File-Contains $runbookActive "Legacy DONE-story drift detection and guard (US-0049)")
Assert-True "runbook documents Legacy DONE-story drift detection and guard (US-0049) (template)" (File-Contains $runbookTemplate "Legacy DONE-story drift detection and guard (US-0049)")
Assert-True "runbook includes legacy-drift reason code BACKLOG_DONE_ACCEPTANCE_UNCHECKED (active)" (File-Contains $runbookActive "BACKLOG_DONE_ACCEPTANCE_UNCHECKED")
Assert-True "runbook includes legacy-drift reason code BACKLOG_DONE_ACCEPTANCE_UNCHECKED (template)" (File-Contains $runbookTemplate "BACKLOG_DONE_ACCEPTANCE_UNCHECKED")
Assert-True "runbook documents one-time backfill idempotent when no drift (active)" (File-Contains $runbookActive "Idempotent when no drift")
Assert-True "runbook documents one-time backfill idempotent when no drift (template)" (File-Contains $runbookTemplate "Idempotent when no drift")
Assert-True "release command includes legacy drift guard step (US-0049) (active)" (File-Contains $releaseCommandActive "Legacy drift guard (US-0049")
Assert-True "release command includes legacy drift guard step (US-0049) (template)" (File-Contains $releaseCommandTemplate "Legacy drift guard (US-0049")
Assert-True "release command includes legacy-drift reason code BACKLOG_DONE_RELEASE_ARTIFACT_MISSING (active)" (File-Contains $releaseCommandActive "BACKLOG_DONE_RELEASE_ARTIFACT_MISSING")
Assert-True "release command includes legacy-drift reason code BACKLOG_DONE_RELEASE_ARTIFACT_MISSING (template)" (File-Contains $releaseCommandTemplate "BACKLOG_DONE_RELEASE_ARTIFACT_MISSING")

$releaseQueueContent = if (Test-Path $releaseQueueActive -PathType Leaf) { Get-Content -Path $releaseQueueActive -Raw } else { "" }
$hasS0013Released = $releaseQueueContent -match "\|\s*S0013\s*\|[^\r\n]*\|\s*released\s*\|"
$backlogPath = Join-Path $root "docs\product\backlog.md"
$backlogRaw = if (Test-Path $backlogPath -PathType Leaf) { Get-Content -Path $backlogPath -Raw } else { "" }
$us0041StatusDone = $backlogRaw -match "(?s)## US-0041[\s\S]*?- Status: DONE"
if ($hasS0013Released) {
  Assert-True "released sprint S0013 has reconciled backlog DONE state for US-0041" $us0041StatusDone
}

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
