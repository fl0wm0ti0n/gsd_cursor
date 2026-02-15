$ErrorActionPreference = 'Stop'
Uninstall-BinFile -Name 'its-magic'
$toolsDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$wrapperCmd = Join-Path $toolsDir "its-magic.cmd"
if (Test-Path $wrapperCmd) { Remove-Item $wrapperCmd -Force }
Write-Host "its-magic removed."
