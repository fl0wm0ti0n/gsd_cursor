Param(
  [string]$Target,
  [ValidateSet("missing","overwrite","interactive")]
  [string]$Mode,
  [switch]$Backup,
  [switch]$Create
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
  $backupRoot = Join-Path $TargetRoot ("gsd-backups\" + $timestamp)
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
  $choice = Read-Host "Enter 1, 2, or 3"
  switch ($choice) {
    "1" { return "missing" }
    "2" { return "overwrite" }
    Default { return "interactive" }
  }
}

function Prompt-YesNo($Label, $Default = $false) {
  $suffix = if ($Default) { "Y/n" } else { "y/N" }
  $value = (Read-Host "$Label [$suffix]").ToLowerInvariant()
  if ([string]::IsNullOrWhiteSpace($value)) { return $Default }
  return @("y","yes") -contains $value
}

$sourceRoot = Normalize-PathSafe (Split-Path -Parent $MyInvocation.MyCommand.Path)
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

$includePaths = @(
  ".cursor/commands",
  ".cursor/rules",
  ".cursor/skills",
  ".cursor/agents",
  ".cursor/hooks",
  ".cursor/hooks.json",
  ".cursor/scratchpad.md",
  "docs",
  "sprints",
  "handoffs",
  "decisions",
  ".github/workflows",
  "README.md",
  "gsd-installer.py",
  "gsd-installer.ps1",
  "gsd-installer.sh"
)

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

Write-Host "Install completed."
exit 0

