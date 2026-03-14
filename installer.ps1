Param(
  [string]$Target,
  [ValidateSet("missing","overwrite","interactive","upgrade")]
  [string]$Mode,
  [switch]$Backup,
  [switch]$Create,
  [switch]$CleanRepo,
  [switch]$Yes,
  [switch]$Help,
  [switch]$Version
)

$ErrorActionPreference = "Stop"

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
    $line = $raw.Trim()
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
    if ($installPaths.Count -eq 0 -or $cleanPaths.Count -eq 0) {
      throw "[INSTALL_MANIFEST_ERROR] $candidate is missing required sections or entries."
    }
    return [PSCustomObject]@{
      install_include_paths = @($installPaths)
      clean_paths = @($cleanPaths)
      manifest_path = $candidate
    }
  }

  throw "[INSTALL_SOURCE_ERROR] installer-owned-paths.manifest not found. Reinstall its-magic to restore template assets."
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

  $mixedFiles = @('.cursor/scratchpad.md', 'README.md')
  if ($mixedFiles -contains $normalized) { return 'mixed' }

  $frameworkPrefixes = @(
    '.cursor/commands/',
    '.cursor/rules/',
    '.cursor/agents/',
    '.cursor/skills/',
    '.cursor/hooks/',
    '.github/workflows/',
    'scripts/validate-and-push',
    'docs/engineering/context/'
  )
  $frameworkExact = @(
    '.cursor/hooks.json',
    '.cursor/scratchpad.local.example.md',
    '.its-magic-version'
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
  $vf = Join-Path $TargetRoot ".its-magic-version"
  if (Test-Path $vf -PathType Leaf) {
    return (Get-Content -Path $vf -Raw).Trim()
  }
  return "unknown"
}

function Write-InstalledVersion($TargetRoot, $Ver) {
  $vf = Join-Path $TargetRoot ".its-magic-version"
  Set-Content -Path $vf -Value $Ver -NoNewline
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
  Write-Host ""
  Write-Host "Clean options:"
  Write-Host "  --clean-repo      Remove all its-magic workflow artifacts from the target repo"
  Write-Host "                    (owned paths from installer manifest, including .cursor,"
  Write-Host "                    docs/product, docs/engineering, docs/user-guides, sprints,"
  Write-Host "                    handoffs, decisions, workflow scripts, CI files, and"
  Write-Host "                    .its-magic-version). Your own source code is never touched."
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
  foreach ($rel in $cleanPaths) {
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

$files = List-SourceFiles $sourceRoot $includePaths
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

  Write-InstalledVersion $targetRoot $appVersion

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

Write-InstalledVersion $targetRoot $appVersion

Show-ItsMagicBanner -IncludeInstallMessage
Write-Host "its-magic v$appVersion"
Write-Host "Repository: $repoUrl"
Write-Host ""
exit 0

