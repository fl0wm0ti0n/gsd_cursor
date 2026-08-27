Param(
  [string]$Target,
  [ValidateSet("missing","overwrite","interactive","upgrade")]
  [string]$Mode,
  [string]$InstallHost,
  [switch]$Backup,
  [switch]$Create,
  [switch]$CleanRepo,
  [switch]$Yes,
  [switch]$Help,
  [switch]$Version
)

$ErrorActionPreference = "Stop"

# US-0121 / DEC-0120 §1: normalize-then-validate --host (PowerShell -Host landmine:
# we use -InstallHost internally; JS forwards -InstallHost <value>). Unknown or
# duplicate -> fail closed INSTALL_HOST_INVALID (ASCII, no GUI per D11).
$validHosts = @("cursor","opencode","both")
$hostValue = "cursor"
if ($PSBoundParameters.ContainsKey("InstallHost")) {
  $normalized = [string]$InstallHost
  if ($null -ne $normalized) { $normalized = $normalized.ToLowerInvariant().Trim() }
  if (-not ($validHosts -contains $normalized)) {
    Write-Host "[INSTALL_HOST_INVALID] unknown host value '$normalized'. Accepted: cursor | opencode | both (default: cursor)."
    exit 1
  }
  $hostValue = $normalized
}
# Duplicate -InstallHost detection: PowerShell Param() collapses duplicates to last-wins,
# so we re-scan $argv for count > 1 to enforce no-last-wins parity with JS/Python.
$hostArgCount = 0
foreach ($a in $args) {
  if ($a -eq "-InstallHost" -or $a -eq "--host") { $hostArgCount += 1 }
}
if ($hostArgCount -gt 1) {
  Write-Host "[INSTALL_HOST_INVALID] duplicate --host argv (no last-wins). Accepted: cursor | opencode | both (default: cursor)."
  exit 1
}

function Normalize-PathSafe($Path) {
  return [System.IO.Path]::GetFullPath($Path)
}

function Ensure-Parent($Path) {
  $parent = Split-Path -Parent $Path
  if ($parent -and -not (Test-Path $parent)) {
    New-Item -ItemType Directory -Path $parent -Force | Out-Null
  }
}

function Get-ManifestSection($ManifestPath, $SectionName) {
  $lines = Get-Content -Path $ManifestPath
  $inSection = $false
  $items = New-Object System.Collections.Generic.List[string]
  foreach ($raw in $lines) {
    $line = $raw.TrimEnd("`r").Trim()
    if ([string]::IsNullOrWhiteSpace($line)) { continue }
    if ($line.StartsWith("#")) { continue }
    if ($line.StartsWith("[") -and $line.EndsWith("]")) {
      $inSection = ($line -eq "[$SectionName]")
      continue
    }
    if ($inSection) { $items.Add($line) }
  }
  return $items
}

function Load-InstallerOwnershipManifest($SourceRoot, $ScriptRoot) {
  $candidates = @(
    (Join-Path $SourceRoot "docs/engineering/context/installer-owned-paths.manifest"),
    (Join-Path $ScriptRoot "docs/engineering/context/installer-owned-paths.manifest")
  ) | Select-Object -Unique

  foreach ($candidate in $candidates) {
    if (-not (Test-Path $candidate -PathType Leaf)) { continue }
    $installPaths = Get-ManifestSection -ManifestPath $candidate -SectionName "install_include_paths"
    $cleanPaths = Get-ManifestSection -ManifestPath $candidate -SectionName "clean_paths"
    $opencodeInstallPaths = Get-ManifestSection -ManifestPath $candidate -SectionName "opencode_install_include_paths"
    $opencodeCleanPaths = Get-ManifestSection -ManifestPath $candidate -SectionName "opencode_clean_paths"
    if ($installPaths.Count -eq 0 -or $cleanPaths.Count -eq 0) {
      throw "[INSTALL_MANIFEST_ERROR] $candidate is missing required sections or entries."
    }
    return [PSCustomObject]@{
      install_include_paths = @($installPaths)
      clean_paths = @($cleanPaths)
      opencode_install_include_paths = @($opencodeInstallPaths)
      opencode_clean_paths = @($opencodeCleanPaths)
      manifest_path = $candidate
    }
  }

  throw "[INSTALL_SOURCE_ERROR] installer-owned-paths.manifest not found. Reinstall its-magic to restore template assets."
}

function Host-GatesCursorRow($Rel, $HostValue) {
  # Returns True if the row should be SKIPPED for this host (DEC-0120 §4).
  if ($HostValue -eq "opencode") {
    return $Rel.StartsWith(".cursor/")
  }
  return $false
}

function Host-IncludesOpencode($HostValue) {
  return ($HostValue -eq "opencode") -or ($HostValue -eq "both")
}

function Host-IncludesCursor($HostValue) {
  return ($HostValue -eq "cursor") -or ($HostValue -eq "both")
}

function Build-EffectiveIncludePaths($InstallPaths, $OpencodeInstallPaths, $HostValue) {
  $effective = New-Object System.Collections.Generic.List[string]
  foreach ($rel in $InstallPaths) {
    if (Host-GatesCursorRow -Rel $rel -HostValue $HostValue) { continue }
    $effective.Add($rel) | Out-Null
  }
  if (Host-IncludesOpencode -HostValue $HostValue) {
    foreach ($rel in $OpencodeInstallPaths) { $effective.Add($rel) | Out-Null }
  }
  return $effective
}

function Build-EffectiveCleanPaths($CleanPaths, $OpencodeCleanPaths, $HostValue) {
  $effective = New-Object System.Collections.Generic.List[string]
  if (Host-IncludesCursor -HostValue $HostValue) {
    foreach ($rel in $CleanPaths) { $effective.Add($rel) | Out-Null }
  }
  if (Host-IncludesOpencode -HostValue $HostValue) {
    foreach ($rel in $OpencodeCleanPaths) { $effective.Add($rel) | Out-Null }
  }
  return $effective
}

function Emit-HostShrinkDiagnostics($TargetRoot, $HostValue) {
  $opencodePresent = Test-Path (Join-Path $TargetRoot ".opencode")
  $cursorPresent = Test-Path (Join-Path $TargetRoot ".cursor") -PathType Container
  if ($HostValue -eq "cursor" -and $opencodePresent) {
    Write-Host "[OPENCODE_ORPHANED_BY_CLEAN_CURSOR] .opencode/ exists from a prior --host both install; --host cursor does not remove it. Run 'its-magic --clean-repo --host opencode|both' to remove it."
  }
  if ($HostValue -eq "opencode" -and $cursorPresent) {
    Write-Host "[CURSOR_ORPHANED_BY_CLEAN_OPENCODE] .cursor/ exists from a prior --host both install; --host opencode does not remove it. Run 'its-magic --clean-repo --host cursor|both' to remove it."
  }
}

function List-SourceFiles($SourceRoot, $IncludePaths) {
  $files = New-Object System.Collections.Generic.List[string]
  foreach ($rel in $IncludePaths) {
    $src = Join-Path $SourceRoot $rel
    if (Test-Path $src -PathType Leaf) {
      $files.Add($rel)
    } elseif (Test-Path $src -PathType Container) {
      Get-ChildItem -Path $src -Recurse -File | ForEach-Object {
        $relPath = $_.FullName.Substring($SourceRoot.Length).TrimStart("\","/")
        $files.Add($relPath)
      }
    }
  }
  return $files | Select-Object -Unique | Sort-Object
}

function Backup-Files($TargetRoot, $RelPaths) {
  $timestamp = (Get-Date).ToUniversalTime().ToString("yyyyMMdd-HHmmssZ")
  $backupRoot = Join-Path $TargetRoot ("backups\" + $timestamp)
  foreach ($rel in $RelPaths) {
    $src = Join-Path $TargetRoot $rel
    if (Test-Path $src -PathType Leaf) {
      $dst = Join-Path $backupRoot $rel
      Ensure-Parent $dst
      Copy-Item -Path $src -Destination $dst -Force
    }
  }
  return $backupRoot
}

function Choose-Mode {
  Write-Host "Select install mode:"
  Write-Host "1) missing-only (copy only files that do not exist)"
  Write-Host "2) overwrite-all (replace existing files)"
  Write-Host "3) interactive (prompt per file)"
  Write-Host "4) upgrade (update framework files, preserve user data)"
  $choice = Read-Host "Enter 1, 2, 3, or 4"
  switch ($choice) {
    "1" { return "missing" }
    "2" { return "overwrite" }
    "4" { return "upgrade" }
    Default { return "interactive" }
  }
}

function Classify-File($RelPath) {
  $normalized = $RelPath -replace '\\','/'

  $mixedFiles = @('README.md')
  if ($mixedFiles -contains $normalized) { return 'mixed' }

  $frameworkPrefixes = @(
    '.cursor/commands/',
    '.cursor/rules/',
    '.cursor/agents/',
    '.cursor/skills/',
    '.cursor/hooks/',
    '.github/workflows/',
    'scripts/validate-and-push',
    'scripts/sync_push_gates',
    'docs/engineering/context/',
    'its_magic/'
  )
  $frameworkExact = @(
    '.cursor/hooks.json',
    '.cursor/scratchpad.local.example.md',
    '.cursor/model-catalog.local.example.json',
    '.cursor/model-catalog.local.example.cursor-only.json',
    '.cursor/model-catalog.local.example.level-1-easy.json',
    '.cursor/model-catalog.local.example.level-2-complex.json',
    '.cursor/model-catalog.local.example.level-3-mega.json',
    '.cursor/model-catalog.local.example.level-4-super.json',
    '.cursor/model-catalog.local.example.role-based-balanced.json',
    '.cursor/model-catalog.local.example.role-based-highend.json',
    '.cursor/model-catalog.local.example.role-based-balanced_cursor_only.json',
    'its_magic/.its-magic-version',
    'its_magic/README.md'
  )
  foreach ($p in $frameworkPrefixes) {
    if ($normalized.StartsWith($p)) { return 'framework' }
  }
  if ($frameworkExact -contains $normalized) { return 'framework' }

  $userDataPrefixes = @(
    'docs/product/',
    'docs/engineering/',
    'docs/user-guides/',
    'sprints/',
    'handoffs/',
    'decisions/'
  )
  foreach ($p in $userDataPrefixes) {
    if ($normalized.StartsWith($p)) { return 'user-data' }
  }

  return 'framework'
}

function Read-InstalledVersion($TargetRoot) {
  $primary = Join-Path $TargetRoot "its_magic\.its-magic-version"
  if (Test-Path $primary -PathType Leaf) {
    return (Get-Content -Path $primary -Raw).Trim()
  }
  $legacy = Join-Path $TargetRoot ".its-magic-version"
  if (Test-Path $legacy -PathType Leaf) {
    return (Get-Content -Path $legacy -Raw).Trim()
  }
  return "unknown"
}

function Write-InstalledVersion($TargetRoot, $Ver) {
  $primary = Join-Path $TargetRoot "its_magic\.its-magic-version"
  Ensure-Parent $primary
  Set-Content -Path $primary -Value $Ver -NoNewline

  $legacy = Join-Path $TargetRoot ".its-magic-version"
  if (Test-Path $legacy -PathType Leaf) {
    Remove-Item -Path $legacy -Force -ErrorAction SilentlyContinue
  }
}

function Sync-RootReadmeToItsMagic($TargetRoot, $FallbackReadme) {
  $marker = "intent contract:"
  $rootReadme = Join-Path $TargetRoot "README.md"
  $srcReadme = $null
  if ($FallbackReadme -and (Test-Path $FallbackReadme -PathType Leaf)) {
    if (-not (Test-Path $rootReadme -PathType Leaf)) {
      $srcReadme = $FallbackReadme
    } elseif (-not (Select-String -Path $rootReadme -Pattern $marker -Quiet)) {
      $srcReadme = $FallbackReadme
    }
  }
  if (-not $srcReadme -and (Test-Path $rootReadme -PathType Leaf)) {
    $srcReadme = $rootReadme
  } elseif (-not $srcReadme -and $FallbackReadme -and (Test-Path $FallbackReadme -PathType Leaf)) {
    $srcReadme = $FallbackReadme
  }
  if (-not $srcReadme) {
    return $false
  }
  $itsMagicReadme = Join-Path $TargetRoot "its_magic\README.md"
  Ensure-Parent $itsMagicReadme
  Copy-Item -Path $srcReadme -Destination $itsMagicReadme -Force
  return $true
}

function Read-RunbookKeyValue($RunbookPath, $Key) {
  if (-not (Test-Path $RunbookPath -PathType Leaf)) { return "" }
  $needle = "${Key}:"
  foreach ($raw in (Get-Content -Path $RunbookPath)) {
    if ($raw.StartsWith($needle)) {
      return $raw.Substring($needle.Length).Trim()
    }
  }
  return ""
}

function Write-RunbookKeyValue($RunbookPath, $Key, $Value) {
  if (-not (Test-Path $RunbookPath -PathType Leaf)) { return $false }
  $needle = "${Key}:"
  $lines = Get-Content -Path $RunbookPath
  $changed = $false
  for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i].StartsWith($needle)) {
      $lines[$i] = "$needle $Value"
      $changed = $true
      break
    }
  }
  if ($changed) {
    Set-Content -Path $RunbookPath -Value $lines
  }
  return $changed
}

function Test-PackageHasScript($TargetRoot, $ScriptName) {
  $pkgPath = Join-Path $TargetRoot "package.json"
  if (-not (Test-Path $pkgPath -PathType Leaf)) { return $false }
  try {
    $pkg = Get-Content -Path $pkgPath -Raw | ConvertFrom-Json
    if ($null -eq $pkg.scripts) { return $false }
    $value = $pkg.scripts.$ScriptName
    return -not [string]::IsNullOrWhiteSpace([string]$value)
  } catch {
    return $false
  }
}

function Get-DetectedRunbookDefaults($TargetRoot) {
  $defaults = @{
    TEST_COMMAND = ""
    LINT_COMMAND = ""
    TYPECHECK_COMMAND = ""
  }

  $testsSh = Join-Path $TargetRoot "tests\run-tests.sh"
  $pkgPath = Join-Path $TargetRoot "package.json"
  $goMod = Join-Path $TargetRoot "go.mod"
  $pyproject = Join-Path $TargetRoot "pyproject.toml"
  $requirements = Join-Path $TargetRoot "requirements.txt"
  $setupPy = Join-Path $TargetRoot "setup.py"

  $hasPkg = Test-Path $pkgPath -PathType Leaf
  $hasGo = Test-Path $goMod -PathType Leaf
  $hasPy = (Test-Path $pyproject -PathType Leaf) -or (Test-Path $requirements -PathType Leaf) -or (Test-Path $setupPy -PathType Leaf)

  if ($hasPkg -and (Test-PackageHasScript $TargetRoot "test")) {
    $defaults.TEST_COMMAND = "npm run test"
    if (Test-PackageHasScript $TargetRoot "lint") { $defaults.LINT_COMMAND = "npm run lint" }
    if (Test-PackageHasScript $TargetRoot "typecheck") { $defaults.TYPECHECK_COMMAND = "npm run typecheck" }
    return $defaults
  }

  if ($hasGo) {
    $defaults.TEST_COMMAND = "go test ./..."
    return $defaults
  }

  if ($hasPy) {
    $defaults.TEST_COMMAND = "python -m pytest"
    return $defaults
  }

  if (Test-Path $testsSh -PathType Leaf) {
    $defaults.TEST_COMMAND = "sh tests/run-tests.sh"
    return $defaults
  }

  return $defaults
}

function Test-BootstrapCommandValid($TargetRoot, $Key, $Command) {
  if ([string]::IsNullOrWhiteSpace($Command)) { return [PSCustomObject]@{ valid = $false; reason = "${Key}_UNDETECTED" } }

  if ($Command.StartsWith("npm run ")) {
    $npm = Get-Command "npm" -ErrorAction SilentlyContinue
    if (-not $npm) { return [PSCustomObject]@{ valid = $false; reason = "NPM_NOT_FOUND" } }
    $script = $Command.Substring("npm run ".Length).Trim()
    if (-not (Test-PackageHasScript $TargetRoot $script)) { return [PSCustomObject]@{ valid = $false; reason = "NPM_SCRIPT_MISSING:$script" } }
    return [PSCustomObject]@{ valid = $true; reason = "OK" }
  }

  if ($Command -eq "python -m pytest") {
    $python = Get-Command "python" -ErrorAction SilentlyContinue
    if (-not $python) { return [PSCustomObject]@{ valid = $false; reason = "PYTHON_NOT_FOUND" } }
    return [PSCustomObject]@{ valid = $true; reason = "OK" }
  }

  if ($Command.StartsWith("go test")) {
    $go = Get-Command "go" -ErrorAction SilentlyContinue
    if (-not $go) { return [PSCustomObject]@{ valid = $false; reason = "GO_NOT_FOUND" } }
    if (-not (Test-Path (Join-Path $TargetRoot "go.mod") -PathType Leaf)) {
      return [PSCustomObject]@{ valid = $false; reason = "GO_MOD_MISSING" }
    }
    return [PSCustomObject]@{ valid = $true; reason = "OK" }
  }

  if ($Command.StartsWith("powershell ")) {
    if (-not (Test-Path (Join-Path $TargetRoot "tests\run-tests.ps1") -PathType Leaf)) {
      return [PSCustomObject]@{ valid = $false; reason = "RUN_TESTS_PS1_MISSING" }
    }
    return [PSCustomObject]@{ valid = $true; reason = "OK" }
  }

  if ($Command.StartsWith("sh ")) {
    $sh = Get-Command "sh" -ErrorAction SilentlyContinue
    if (-not $sh) { return [PSCustomObject]@{ valid = $false; reason = "SH_NOT_FOUND" } }
    if (-not (Test-Path (Join-Path $TargetRoot "tests\run-tests.sh") -PathType Leaf)) {
      return [PSCustomObject]@{ valid = $false; reason = "RUN_TESTS_SH_MISSING" }
    }
    return [PSCustomObject]@{ valid = $true; reason = "OK" }
  }

  $exe = ($Command -split ' ')[0]
  if (-not (Get-Command $exe -ErrorAction SilentlyContinue)) {
    return [PSCustomObject]@{ valid = $false; reason = "EXECUTABLE_NOT_FOUND:$exe" }
  }
  return [PSCustomObject]@{ valid = $true; reason = "OK" }
}

function Test-ShouldBootstrapTestCommand($Current, $Candidate) {
  if ([string]::IsNullOrWhiteSpace($Candidate)) { return $false }
  if ([string]::IsNullOrWhiteSpace($Current)) { return $true }
  if ($Candidate.StartsWith("npm run test") -or $Candidate.StartsWith("sh tests/run-tests")) {
    $normalized = $Current.Trim().ToLowerInvariant()
    $kitDefaults = @(
      'powershell -executionpolicy bypass -file "tests/run-tests.ps1"',
      'powershell -executionpolicy bypass -file tests/run-tests.ps1'
    )
    foreach ($kitDefault in $kitDefaults) {
      if ($normalized -eq $kitDefault) { return $true }
    }
  }
  return $false
}

function Invoke-RunbookBootstrap($TargetRoot) {
  $runbookPath = Join-Path $TargetRoot "docs\engineering\runbook.md"
  if (-not (Test-Path $runbookPath -PathType Leaf)) {
    return [PSCustomObject]@{ ok = $true; notes = @() }
  }

  $defaults = Get-DetectedRunbookDefaults $TargetRoot
  $notes = New-Object System.Collections.Generic.List[string]
  $applied = New-Object System.Collections.Generic.List[string]

  foreach ($key in @("TEST_COMMAND","LINT_COMMAND","TYPECHECK_COMMAND")) {
    $current = Read-RunbookKeyValue -RunbookPath $runbookPath -Key $key
    $candidate = [string]$defaults[$key]
    if ($key -eq "TEST_COMMAND") {
      if (-not (Test-ShouldBootstrapTestCommand $current $candidate)) { continue }
    } elseif (-not [string]::IsNullOrWhiteSpace($current)) {
      continue
    }

    if ([string]::IsNullOrWhiteSpace($candidate)) {
      if ($key -eq "TEST_COMMAND") {
        $notes.Add("[RUNBOOK_BOOTSTRAP_ERROR] TEST_COMMAND_UNRESOLVED: could not detect a valid baseline test command. Fix: define TEST_COMMAND in docs/engineering/runbook.md or add detectable stack markers (package.json scripts.test, pyproject.toml, go.mod).")
      }
      continue
    }

    $valid = Test-BootstrapCommandValid -TargetRoot $TargetRoot -Key $key -Command $candidate
    if ($valid.valid) {
      if (Write-RunbookKeyValue -RunbookPath $runbookPath -Key $key -Value $candidate) {
        $applied.Add("$key=$candidate")
      }
    } elseif ($key -eq "TEST_COMMAND") {
      $notes.Add("[RUNBOOK_BOOTSTRAP_ERROR] TEST_COMMAND_INVALID:$($valid.reason). Fix: set a valid TEST_COMMAND in docs/engineering/runbook.md.")
    }
  }

  if ($applied.Count -gt 0) {
    $notes.Add("[RUNBOOK_BOOTSTRAP] Applied defaults: $($applied -join ', ')")
  }

  $finalTest = Read-RunbookKeyValue -RunbookPath $runbookPath -Key "TEST_COMMAND"
  $ok = -not [string]::IsNullOrWhiteSpace($finalTest)
  return [PSCustomObject]@{
    ok = $ok
    notes = @($notes)
  }
}

function Files-ContentEqual($PathA, $PathB) {
  $a = Get-Content -Path $PathA -Raw -ErrorAction SilentlyContinue
  $b = Get-Content -Path $PathB -Raw -ErrorAction SilentlyContinue
  return $a -eq $b
}

function Prompt-YesNo($Label, $Default = $false) {
  $suffix = if ($Default) { "Y/n" } else { "y/N" }
  $value = (Read-Host "$Label [$suffix]").ToLowerInvariant()
  if ([string]::IsNullOrWhiteSpace($value)) { return $Default }
  return @("y","yes") -contains $value
}

function Get-AppVersion($SourceRoot) {
  try {
    $pkgPath = Join-Path $SourceRoot "package.json"
    if (Test-Path $pkgPath -PathType Leaf) {
      $pkg = Get-Content -Path $pkgPath -Raw | ConvertFrom-Json
      if ($pkg.version) { return [string]$pkg.version }
    }
  } catch {}
  return "unknown"
}

function Invoke-ScratchpadPostinstall {
  param(
    [string]$TargetRoot,
    [string]$Mode
  )
  if (-not (Host-IncludesCursor -HostValue $hostValue)) {
    Write-Host "[CURSOR_HOST_HOOKS_SKIPPED] --host opencode does not materialize .cursor/ (scratchpad Model B + dev-env profile)."
    return
  }
  $installerPy = Join-Path $scriptDir "installer.py"
  if (-not (Test-Path $installerPy -PathType Leaf)) {
    Write-Host "[SCRATCHPAD_POSTINSTALL_ERROR] installer.py missing next to installer.ps1."
    exit 1
  }
  $py = Get-Command python -ErrorAction SilentlyContinue
  if (-not $py) {
    Write-Host "[SCRATCHPAD_POSTINSTALL_ERROR] PYTHON_NOT_FOUND: Python is required for scratchpad materialization/validation (Model B). Fix: install Python 3 and re-run."
    exit 1
  }
  & python $installerPy --scratchpad-postinstall --target $TargetRoot --mode $Mode
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

function Invoke-OpencodeModelCatalogHook {
  param(
    [string]$TargetRoot
  )
  if (-not (Host-IncludesOpencode -HostValue $hostValue)) {
    return
  }
  $catalogPath = Join-Path $TargetRoot ".opencode/model-catalog.local.json"
  if (-not (Test-Path $catalogPath -PathType Leaf)) {
    Write-Host "[OPENCODE_MODEL_CATALOG_SKIPPED] no .opencode/model-catalog.local.json at install target (optional catalog)."
    return
  }
  $scriptPath = Join-Path $scriptDir "scripts/opencode_model_catalog_apply.py"
  if (-not (Test-Path $scriptPath -PathType Leaf)) {
    Write-Host "[OPENCODE_MODEL_CATALOG_ERROR] scripts/opencode_model_catalog_apply.py not found next to installer.ps1."
    exit 1
  }
  $py = Get-Command python -ErrorAction SilentlyContinue
  if (-not $py) {
    Write-Host "[OPENCODE_MODEL_CATALOG_ERROR] PYTHON_NOT_FOUND: Python is required for OpenCode model catalog materialization."
    exit 1
  }
  & python $scriptPath --target $TargetRoot
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

function Invoke-InstallCompletenessValidation {
  param(
    [string]$TargetRoot
  )
  $installerPy = Join-Path $scriptDir "installer.py"
  if (-not (Test-Path $installerPy -PathType Leaf)) {
    Write-Host "[INSTALL_COMPLETENESS_FAILED] installer.py missing next to installer.ps1."
    exit 1
  }
  $py = Get-Command python -ErrorAction SilentlyContinue
  if (-not $py) {
    Write-Host "[INSTALL_COMPLETENESS_FAILED] PYTHON_NOT_FOUND: Python is required for deterministic installer completeness validation."
    exit 1
  }
  & python $installerPy --validate-install-completeness --target $TargetRoot
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

function Show-ItsMagicBanner([switch]$IncludeInstallMessage) {
  $prev = [Console]::OutputEncoding
  [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
  $b64 = 'ICDilojilojilZfilojilojilojilojilojilojilojilojilZfilojilojilojilojilojilojilojilZcgICAgICDilojilojilojilZcgICDilojilojilojilZcg4paI4paI4paI4paI4paI4pWXICDilojilojilojilojilojilojilZcg4paI4paI4pWXIOKWiOKWiOKWiOKWiOKWiOKWiOKVlwogIOKWiOKWiOKVkeKVmuKVkOKVkOKWiOKWiOKVlOKVkOKVkOKVneKWiOKWiOKVlOKVkOKVkOKVkOKVkOKVnSAgICAgIOKWiOKWiOKWiOKWiOKVlyDilojilojilojilojilZHilojilojilZTilZDilZDilojilojilZfilojilojilZTilZDilZDilZDilZDilZ0g4paI4paI4pWR4paI4paI4pWU4pWQ4pWQ4pWQ4pWQ4pWdCiAg4paI4paI4pWRICAg4paI4paI4pWRICAg4paI4paI4paI4paI4paI4paI4paI4pWX4paI4paI4paI4paI4paI4pWX4paI4paI4pWU4paI4paI4paI4paI4pWU4paI4paI4pWR4paI4paI4paI4paI4paI4paI4paI4pWR4paI4paI4pWRICDilojilojilojilZfilojilojilZHilojilojilZEgICAgIAogIOKWiOKWiOKVkSAgIOKWiOKWiOKVkSAgIOKVmuKVkOKVkOKVkOKVkOKWiOKWiOKVkeKVmuKVkOKVkOKVkOKVkOKVneKWiOKWiOKVkeKVmuKWiOKWiOKVlOKVneKWiOKWiOKVkeKWiOKWiOKVlOKVkOKVkOKWiOKWiOKVkeKWiOKWiOKVkSAgIOKWiOKWiOKVkeKWiOKWiOKVkeKWiOKWiOKVkSAgICAgCiAg4paI4paI4pWRICAg4paI4paI4pWRICAg4paI4paI4paI4paI4paI4paI4paI4pWRICAgICAg4paI4paI4pWRIOKVmuKVkOKVnSDilojilojilZHilojilojilZEgIOKWiOKWiOKVkeKVmuKWiOKWiOKWiOKWiOKWiOKWiOKVlOKVneKWiOKWiOKVkeKVmuKWiOKWiOKWiOKWiOKWiOKWiOKVlwogIOKVmuKVkOKVnSAgIOKVmuKVkOKVnSAgIOKVmuKVkOKVkOKVkOKVkOKVkOKVkOKVnSAgICAgIOKVmuKVkOKVnSAgICAg4pWa4pWQ4pWd4pWa4pWQ4pWdICDilZrilZDilZ0g4pWa4pWQ4pWQ4pWQ4pWQ4pWQ4pWdIOKVmuKVkOKVnSDilZrilZDilZDilZDilZDilZDilZ0='
  $art = [System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($b64))
  $lines = $art -split "`n"
  $colors = @('Magenta','Magenta','Magenta','Cyan','Cyan','Cyan')
  Write-Host ""
  for ($i = 0; $i -lt $lines.Count; $i++) {
    Write-Host $lines[$i] -ForegroundColor $colors[$i]
  }
  Write-Host ""
  Write-Host "                         AI dev team" -ForegroundColor Yellow
  if ($IncludeInstallMessage) {
    Write-Host "                    Installation complete!" -ForegroundColor Green
  }
  Write-Host ""
  [Console]::OutputEncoding = $prev
}

function Show-ItsMagicHelp($VersionString, $RepoUrl) {
  Show-ItsMagicBanner
  Write-Host "its-magic v$VersionString"
  Write-Host "Repository: $RepoUrl"
  Write-Host ""
  Write-Host "Install AI dev team workflow files into any Cursor repository."
  Write-Host ""
  Write-Host "Usage:"
  Write-Host "  its-magic --target <path> [--mode <mode>] [--backup] [--create]"
  Write-Host "  its-magic --clean-repo [--target <path>] [--yes]"
  Write-Host "  its-magic --help | --version"
  Write-Host ""
  Write-Host "Install options:"
  Write-Host "  --target <path>   Path to the repository where workflow files are installed."
  Write-Host "                    If omitted you will be prompted interactively."
  Write-Host "  --mode <mode>     How to handle files that already exist in the target:"
  Write-Host "                      missing      Only copy files that do not exist yet (default)."
  Write-Host "                                   Safe for repos that already have some workflow files."
  Write-Host "                      overwrite    Replace every file, even if it already exists."
  Write-Host "                                   Combine with --backup to keep a snapshot first."
  Write-Host "                      interactive  Ask per file whether to overwrite or skip."
  Write-Host "                      upgrade      Update framework files while preserving user data."
  Write-Host "                                   Use after updating its-magic to a newer version."
  Write-Host "  --backup          Before overwriting, save existing files to backups/<timestamp>/."
  Write-Host "                    Ignored when mode is 'missing' (nothing gets replaced)."
  Write-Host "  --create          Create the target directory if it does not exist."
  Write-Host "  -InstallHost <v>  Host-surface switch: cursor | opencode | both (default: cursor)."
  Write-Host "                    Normalized case-insensitive and whitespace-trimmed before validate."
  Write-Host "                    Unknown value -> exit with INSTALL_HOST_INVALID."
  Write-Host "                    Duplicate -InstallHost argv -> fail closed INSTALL_HOST_INVALID (no last-wins)."
  Write-Host "                    -InstallHost gates ONLY .cursor/ and .opencode/ trees; kernel paths"
  Write-Host "                    (docs/, scripts/, its_magic/, handoffs/, decisions/, sprints/,"
  Write-Host "                    .github/workflows/) always install regardless of -InstallHost."
  Write-Host "                    Note: -InstallHost (not -Host) avoids the PowerShell `$Host landmine."
  Write-Host "  Note: installer bootstraps runbook TEST/LINT/TYPECHECK commands from"
  Write-Host "        OS+stack detection; unresolved TEST_COMMAND fails fast with"
  Write-Host "        [RUNBOOK_BOOTSTRAP_ERROR] diagnostics."
  Write-Host "  Note: scratchpad Model B: .cursor/scratchpad.md is"
  Write-Host "        materialized when missing; Python 3 on PATH is required for validation."
  Write-Host "        Recovery: python installer.py --scratchpad-postinstall --target <repo> --mode missing"
  Write-Host ""
  Write-Host "Clean options:"
  Write-Host "  --clean-repo      Remove all its-magic workflow artifacts from the target repo"
  Write-Host "                    (owned paths from installer manifest, including .cursor,"
  Write-Host "                    docs/product, docs/engineering, docs/user-guides, sprints,"
  Write-Host "                    handoffs, decisions, workflow scripts, CI files, and"
  Write-Host "                    installer metadata under its_magic/ (legacy .its-magic-version"
  Write-Host "                    is also removed when present). Your own source code is never touched."
  Write-Host "  --target <path>   Repo to clean (default: current directory)."
  Write-Host "  --yes             Skip the confirmation prompt."
  Write-Host ""
  Write-Host "Info:"
  Write-Host "  --help            Show this help and exit."
  Write-Host "  --version         Print the installed version and exit."
  Write-Host ""
  Write-Host "Examples:"
  Write-Host "  its-magic --target . --mode missing              Safe first-time setup"
  Write-Host "  its-magic --target . --mode upgrade               Update framework, keep user data"
  Write-Host "  its-magic --target . --mode overwrite --backup    Replace all files, keep backup"
  Write-Host "  its-magic --clean-repo --target . --yes           Remove workflow artifacts silently"
  Write-Host ""
}

$scriptDir = Normalize-PathSafe (Split-Path -Parent $MyInvocation.MyCommand.Path)
$sourceRoot = Join-Path $scriptDir "template"
$repoUrl = "https://github.com/fl0wm0ti0n/its-magic"
$appVersion = Get-AppVersion $scriptDir
$noArgs = $PSBoundParameters.Count -eq 0

if ($Version) {
  Write-Host "its-magic v$appVersion"
  exit 0
}

if ($Help -or $noArgs) {
  Show-ItsMagicHelp -VersionString $appVersion -RepoUrl $repoUrl
  exit 0
}

if (-not (Test-Path $sourceRoot -PathType Container)) {
  Write-Host "[INSTALL_SOURCE_ERROR] template directory is missing. Reinstall its-magic package."
  exit 1
}

$ownershipManifest = Load-InstallerOwnershipManifest -SourceRoot $sourceRoot -ScriptRoot $scriptDir
$includePaths = @($ownershipManifest.install_include_paths)
$cleanPaths = @($ownershipManifest.clean_paths)
$opencodeInstallPaths = @($ownershipManifest.opencode_install_include_paths)
$opencodeCleanPaths = @($ownershipManifest.opencode_clean_paths)
$effectiveIncludePaths = Build-EffectiveIncludePaths -InstallPaths $includePaths -OpencodeInstallPaths $opencodeInstallPaths -HostValue $hostValue
$effectiveCleanPaths = Build-EffectiveCleanPaths -CleanPaths $cleanPaths -OpencodeCleanPaths $opencodeCleanPaths -HostValue $hostValue

if ($CleanRepo) {
  if (-not $Target) { $Target = "." }
  $targetRoot = Normalize-PathSafe $Target
  if (-not (Test-Path $targetRoot -PathType Container)) {
    Write-Host "Target directory does not exist."
    exit 1
  }
  if (-not $Yes) {
    $proceed = Prompt-YesNo "Clean its-magic workflow artifacts in $targetRoot?" $false
    if (-not $proceed) {
      Write-Host "Aborted."
      exit 1
    }
  }
  foreach ($rel in $effectiveCleanPaths) {
    $fullPath = Join-Path $targetRoot $rel
    if (Test-Path $fullPath) {
      if (Test-Path $fullPath -PathType Container) {
        Remove-Item -Path $fullPath -Recurse -Force
      } else {
        Remove-Item -Path $fullPath -Force
      }
      Write-Host "Removed: $rel"
    }
  }
  Write-Host "Clean completed."
  if ($hostValue -ne "both") {
    Emit-HostShrinkDiagnostics -TargetRoot $targetRoot -HostValue $hostValue
  }
  exit 0
}

if (-not $Target) {
  $Target = Read-Host "Target repository path"
}
$targetRoot = Normalize-PathSafe $Target

if (-not (Test-Path $targetRoot -PathType Container)) {
  if ($Create -or (Prompt-YesNo "Target missing. Create?" $false)) {
    New-Item -ItemType Directory -Path $targetRoot -Force | Out-Null
  } else {
    Write-Host "Target directory does not exist."
    exit 1
  }
}

$mode = if ($Mode) { $Mode } else { Choose-Mode }
$backupEnabled = $Backup.IsPresent
if (($mode -eq "overwrite" -or $mode -eq "interactive") -and -not $backupEnabled) {
  $backupEnabled = Prompt-YesNo "Backup existing files before overwrite?" $false
}

$files = List-SourceFiles $sourceRoot $effectiveIncludePaths
if ($files.Count -eq 0) {
  Write-Host "No source files found to install."
  exit 1
}

if ($backupEnabled -and $mode -eq "overwrite") {
  $overwriteCandidates = @()
  foreach ($rel in $files) {
    $dst = Join-Path $targetRoot $rel
    if (Test-Path $dst -PathType Leaf) { $overwriteCandidates += $rel }
  }
  if ($overwriteCandidates.Count -gt 0) {
    $backupRoot = Backup-Files $targetRoot $overwriteCandidates
    Write-Host "Backup created at: $backupRoot"
  }
}

if ($mode -eq "upgrade") {
  $oldVersion = Read-InstalledVersion $targetRoot
  Write-Host ""
  Write-Host "Upgrading from v$oldVersion to v$appVersion" -ForegroundColor Cyan
  Write-Host ""

  if ($backupEnabled) {
    $backupCandidates = @()
    foreach ($rel in $files) {
      $dst = Join-Path $targetRoot $rel
      $cat = Classify-File $rel
      if ($cat -eq 'framework' -and (Test-Path $dst -PathType Leaf)) {
        $backupCandidates += $rel
      }
    }
    if ($backupCandidates.Count -gt 0) {
      $backupRoot = Backup-Files $targetRoot $backupCandidates
      Write-Host "Backup created at: $backupRoot"
    }
  }

  $added = New-Object System.Collections.Generic.List[string]
  $updated = New-Object System.Collections.Generic.List[string]
  $unchanged = 0
  $preserved = 0
  $review = New-Object System.Collections.Generic.List[string]
  $scratchpadExampleRel = '.cursor/scratchpad.local.example.md'
  $scratchpadExampleStatus = 'not-seen'

  foreach ($rel in $files) {
    $src = Join-Path $sourceRoot $rel
    $dst = Join-Path $targetRoot $rel
    $exists = Test-Path $dst -PathType Leaf
    $cat = Classify-File $rel

    if (-not $exists) {
      Ensure-Parent $dst
      Copy-Item -Path $src -Destination $dst -Force
      $added.Add($rel)
      if ($rel -eq $scratchpadExampleRel) { $scratchpadExampleStatus = 'added' }
      continue
    }

    if ($cat -eq 'framework') {
      if (Files-ContentEqual $src $dst) {
        $unchanged++
        if ($rel -eq $scratchpadExampleRel) { $scratchpadExampleStatus = 'unchanged' }
      } else {
        Ensure-Parent $dst
        Copy-Item -Path $src -Destination $dst -Force
        $updated.Add($rel)
        if ($rel -eq $scratchpadExampleRel) { $scratchpadExampleStatus = 'updated' }
      }
      continue
    }

    if ($cat -eq 'user-data') {
      $preserved++
      continue
    }

    if ($cat -eq 'mixed') {
      $preserved++
      if (-not (Files-ContentEqual $src $dst)) {
        $review.Add($rel)
      }
      continue
    }
  }

  Invoke-ScratchpadPostinstall -TargetRoot $targetRoot -Mode "upgrade"
  Invoke-OpencodeModelCatalogHook -TargetRoot $targetRoot
  Invoke-InstallCompletenessValidation -TargetRoot $targetRoot

  if ($hostValue -eq "cursor" -and (Test-Path (Join-Path $targetRoot ".opencode"))) {
    Write-Host "[OPENCODE_STALE_BY_UPGRADE_CURSOR] .opencode/ exists from a prior --host both install; --host cursor upgrade does not refresh it. Run 'its-magic --target <repo> --mode upgrade --host opencode|both' to refresh it."
  }
  if ($hostValue -eq "opencode" -and (Test-Path (Join-Path $targetRoot ".cursor") -PathType Container)) {
    Write-Host "[CURSOR_STALE_BY_UPGRADE_OPENCODE] .cursor/ exists from a prior --host both install; --host opencode upgrade does not refresh it. Run 'its-magic --target <repo> --mode upgrade --host cursor|both' to refresh it."
  }

  Write-InstalledVersion $targetRoot $appVersion
  Sync-RootReadmeToItsMagic $targetRoot (Join-Path $scriptDir "README.md") | Out-Null
  $runbookBootstrap = Invoke-RunbookBootstrap -TargetRoot $targetRoot
  foreach ($note in $runbookBootstrap.notes) { Write-Host $note }
  if (-not $runbookBootstrap.ok) { exit 1 }

  Show-ItsMagicBanner
  Write-Host "Upgrade complete: v$oldVersion -> v$appVersion" -ForegroundColor Green
  Write-Host ""
  if ($added.Count -gt 0) {
    Write-Host "  Added (new):         $($added.Count) files" -ForegroundColor Green
    foreach ($f in $added) { Write-Host "    $f" }
  }
  if ($updated.Count -gt 0) {
    Write-Host "  Updated (framework): $($updated.Count) files" -ForegroundColor Yellow
    foreach ($f in $updated) { Write-Host "    $f" }
  }
  Write-Host "  Unchanged:           $unchanged files"
  Write-Host "  Preserved (user):    $preserved files"
  if ($scratchpadExampleStatus -eq 'not-seen') { $scratchpadExampleStatus = 'not-in-manifest' }
  Write-Host "  Scratchpad example:  $scratchpadExampleStatus (.cursor/scratchpad.local.example.md)"
  Write-Host "  Scratchpad layers:   post-install refreshed example-first, then baseline (see [SCRATCHPAD_LAYER] lines)."
  if (Test-Path (Join-Path $targetRoot '.cursor/scratchpad.local.md') -PathType Leaf) {
    Write-Host "  User local file:     preserved (.cursor/scratchpad.local.md)"
  }
  if ($review.Count -gt 0) {
    Write-Host ""
    Write-Host "  Review recommended:  $($review.Count) files" -ForegroundColor Magenta
    foreach ($f in $review) {
      Write-Host "    $f"
    }
    Write-Host "    Check .cursor/scratchpad.local.example.md for new flags." -ForegroundColor DarkGray
  }
  Write-Host ""
  Write-Host "Repository: $repoUrl"
  Write-Host ""
  exit 0
}

foreach ($rel in $files) {
  $src = Join-Path $sourceRoot $rel
  $dst = Join-Path $targetRoot $rel
  $exists = Test-Path $dst -PathType Leaf

  if ($mode -eq "missing") {
    if ($exists) { continue }
    Ensure-Parent $dst
    Copy-Item -Path $src -Destination $dst -Force
    continue
  }

  if ($mode -eq "overwrite") {
    Ensure-Parent $dst
    Copy-Item -Path $src -Destination $dst -Force
    continue
  }

  if ($mode -eq "interactive") {
    if (-not $exists) {
      Ensure-Parent $dst
      Copy-Item -Path $src -Destination $dst -Force
      continue
    }
    $answer = (Read-Host "File exists: $rel | [o]verwrite [s]kip [q]uit").ToLowerInvariant()
    if ($answer -eq "q") {
      Write-Host "Aborted."
      exit 1
    }
    if ($answer -eq "o") {
      if ($backupEnabled) {
        $backupRoot = Backup-Files $targetRoot @($rel)
        Write-Host "Backed up: $rel -> $backupRoot"
      }
      Ensure-Parent $dst
      Copy-Item -Path $src -Destination $dst -Force
    }
  }
}

Invoke-ScratchpadPostinstall -TargetRoot $targetRoot -Mode $mode
Invoke-OpencodeModelCatalogHook -TargetRoot $targetRoot
Invoke-InstallCompletenessValidation -TargetRoot $targetRoot

Write-InstalledVersion $targetRoot $appVersion
Sync-RootReadmeToItsMagic $targetRoot (Join-Path $scriptDir "README.md") | Out-Null
$runbookBootstrap = Invoke-RunbookBootstrap -TargetRoot $targetRoot
foreach ($note in $runbookBootstrap.notes) { Write-Host $note }
if (-not $runbookBootstrap.ok) { exit 1 }

Show-ItsMagicBanner -IncludeInstallMessage
Write-Host "its-magic v$appVersion"
Write-Host "Repository: $repoUrl"
Write-Host ""
exit 0

