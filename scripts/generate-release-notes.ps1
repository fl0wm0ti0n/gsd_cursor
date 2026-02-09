Param(
  [string]$RepoRoot,
  [string]$Version = "v0.0.0",
  [string]$Sprint = "S0001"
)

$ErrorActionPreference = "Stop"

function Resolve-RepoRoot {
  if ($RepoRoot) { return (Resolve-Path $RepoRoot).Path }
  return (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
}

function Read-IfExists($Path) {
  if (Test-Path $Path -PathType Leaf) {
    return Get-Content -Path $Path -Raw
  }
  return ""
}

$root = Resolve-RepoRoot
$summaryPath = Join-Path $root "sprints\$Sprint\summary.md"
$qaPath = Join-Path $root "sprints\$Sprint\qa-findings.md"
$runbookPath = Join-Path $root "docs\engineering\runbook.md"
$outPath = Join-Path $root "handoffs\release_notes.md"

$summary = Read-IfExists $summaryPath
$qa = Read-IfExists $qaPath
$runbook = Read-IfExists $runbookPath

$gitChanges = ""
if (Get-Command git -ErrorAction SilentlyContinue) {
  try {
    $isRepo = git -C $root rev-parse --is-inside-work-tree 2>$null
    if ($isRepo -eq "true") {
      $gitChanges = git -C $root log -n 20 --pretty=format:"- %s"
    }
  } catch {}
}

$timestamp = (Get-Date).ToString("yyyy-MM-dd")

@"
# Release Notes — $Version

**Sprint:** $Sprint
**Date:** $timestamp

---

## Summary

${summary.Trim()}

---

## Changes (last 20 commits)

${gitChanges.Trim()}

---

## QA Findings (from sprint)

${qa.Trim()}

---

## Runbook Notes

${runbook.Trim()}
"@ | Set-Content -Path $outPath

Write-Host "Release notes written to: $outPath"
