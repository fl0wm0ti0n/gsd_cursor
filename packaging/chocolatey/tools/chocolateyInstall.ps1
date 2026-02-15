$ErrorActionPreference = 'Stop'

# --- Config ---
$packageName = 'its-magic'
# UPDATE: url and checksum before each release
$url         = 'https://github.com/fl0wm0ti0n/gsd_cursor/archive/refs/tags/v0.1.1-4.zip'
$checksum    = '8374b8f988e7ef17ef9adfa5cf6a16616a4c0cd23bedbea8356b381a001de51b'
$checksumType= 'sha256'

# --- Download & extract ---
$toolsDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

Install-ChocolateyZipPackage -PackageName $packageName `
    -Url $url `
    -UnzipLocation $toolsDir `
    -Checksum $checksum `
    -ChecksumType $checksumType

# --- Create shim ---
# GitHub release zips extract into repo-tag folders. Resolve bin path dynamically.
$binPath = Get-ChildItem -Path $toolsDir -Recurse -File -Filter "its-magic.js" |
    Where-Object { $_.FullName -match '\\bin\\its-magic\.js$' } |
    Select-Object -First 1 -ExpandProperty FullName
if (Test-Path $binPath) {
    Install-BinFile -Name 'its-magic' -Path "node" -Command "`"$binPath`" `$args"
    Write-Host "its-magic installed. Run: its-magic --help"
} else {
    Write-Warning "bin/its-magic.js not found - run manually: node <extract-path>/bin/its-magic.js"
}










