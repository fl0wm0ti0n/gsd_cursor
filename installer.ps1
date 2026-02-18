Param(
  [string]$Target,
  [ValidateSet("missing","overwrite","interactive")]
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
  Write-Host "  --backup          Before overwriting, save existing files to backups/<timestamp>/."
  Write-Host "                    Ignored when mode is 'missing' (nothing gets replaced)."
  Write-Host "  --create          Create the target directory if it does not exist."
  Write-Host ""
  Write-Host "Clean options:"
  Write-Host "  --clean-repo      Remove all its-magic workflow artifacts from the target repo"
  Write-Host "                    (.cursor, docs/product, docs/engineering, sprints, handoffs,"
  Write-Host "                    decisions). Your own source code is never touched."
  Write-Host "  --target <path>   Repo to clean (default: current directory)."
  Write-Host "  --yes             Skip the confirmation prompt."
  Write-Host ""
  Write-Host "Info:"
  Write-Host "  --help            Show this help and exit."
  Write-Host "  --version         Print the installed version and exit."
  Write-Host ""
  Write-Host "Examples:"
  Write-Host "  its-magic --target . --mode missing            Safe first-time setup"
  Write-Host "  its-magic --target . --mode overwrite --backup   Update all files, keep backup"
  Write-Host "  its-magic --clean-repo --target . --yes        Remove workflow artifacts silently"
  Write-Host ""
}

$sourceRoot = Normalize-PathSafe (Split-Path -Parent $MyInvocation.MyCommand.Path)
$repoUrl = "https://github.com/fl0wm0ti0n/its-magic"
$appVersion = Get-AppVersion $sourceRoot
$noArgs = $PSBoundParameters.Count -eq 0

if ($Version) {
  Write-Host "its-magic v$appVersion"
  exit 0
}

if ($Help -or $noArgs) {
  Show-ItsMagicHelp -VersionString $appVersion -RepoUrl $repoUrl
  exit 0
}

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
  $cleanPaths = @(
    ".cursor",
    "docs\product",
    "docs\engineering",
    "sprints",
    "handoffs",
    "decisions"
  )
  foreach ($rel in $cleanPaths) {
    $fullPath = Join-Path $targetRoot $rel
    if (Test-Path $fullPath) {
      Remove-Item -Path $fullPath -Recurse -Force
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

$includePaths = @(
  ".cursor/commands",
  ".cursor/rules",
  ".cursor/skills",
  ".cursor/agents",
  ".cursor/hooks",
  ".cursor/hooks.json",
  ".cursor/scratchpad.md",
  ".cursor/scratchpad.local.example.md",
  "docs",
  "sprints",
  "handoffs",
  "decisions",
  ".github/workflows",
  "README.md"
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

Show-ItsMagicBanner -IncludeInstallMessage
Write-Host "its-magic v$appVersion"
Write-Host "Repository: $repoUrl"
Write-Host ""
exit 0

