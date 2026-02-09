Param(
  [Parameter(Mandatory = $true)]
  [string]$PromptFile,
  [switch]$Clipboard
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $PromptFile -PathType Leaf)) {
  Write-Host "Prompt file not found: $PromptFile"
  exit 1
}

$raw = Get-Content -Path $PromptFile -Raw
$blocks = $raw -split "(?m)^\s*---\s*$"

$step = 1
foreach ($block in $blocks) {
  $prompt = $block.Trim()
  if (-not $prompt) { continue }
  Write-Host ""
  Write-Host "Step $step:"
  Write-Host $prompt
  if ($Clipboard) {
    $prompt | Set-Clipboard
    Write-Host "Copied to clipboard."
  }
  Read-Host "Press Enter after sending this prompt in Cursor"
  $step++
}

Write-Host "All prompts completed."
exit 0
