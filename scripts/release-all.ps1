<#
.SYNOPSIS
  Unified release: npm + Chocolatey + Homebrew (all three at once).
.DESCRIPTION
  1. Bumps version in package.json (patch|minor|major|explicit)
  2. Publishes to npm
  3. Creates a GitHub release with a source zip (for Homebrew/Chocolatey URLs)
  4. Updates Chocolatey nuspec + pushes to chocolatey.org
  5. Updates Homebrew formula with new URL + sha256
.PARAMETER Bump
  Version bump type: patch, minor, major, or an explicit semver (e.g. 1.2.3).
  Default: patch
.PARAMETER NpmTag
  npm dist-tag (e.g. latest, beta, rc). Default: latest
.PARAMETER SkipNpm
  Skip npm publish.
.PARAMETER SkipChoco
  Skip Chocolatey push.
.PARAMETER SkipBrew
  Skip Homebrew formula update.
.PARAMETER DryRun
  Print what would happen without executing.
#>
param(
    [string]$Bump = "patch",
    [string]$NpmTag = "latest",
    [switch]$SkipNpm,
    [switch]$SkipChoco,
    [switch]$SkipBrew,
    [switch]$DryRun,
    [switch]$SkipBrewPush,
    [string]$BrewTapRepo = "",
    [string]$BrewTapBranch = "main",
    [string]$BrewTapDir = "",
    [bool]$CreateBrewTapIfMissing = $true
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
if (-not (Test-Path (Join-Path $repoRoot 'package.json'))) {
    $repoRoot = Split-Path -Parent $PSScriptRoot
}
Push-Location $repoRoot

# ── Helpers ──────────────────────────────────────────────────────────
function Log($msg) { Write-Host "[release] $msg" -ForegroundColor Cyan }
function Warn($msg){ Write-Host "[release] $msg" -ForegroundColor Yellow }
function Err($msg) { Write-Host "[release] $msg" -ForegroundColor Red; Pop-Location; exit 1 }

# Quote char for building regex patterns (avoids PS 5.1 parser issues)
$DQ = [char]34
$chocoFailed = $false
$brewTapFailed = $false
$brewTapPushed = $false

# ── 1. Version bump ─────────────────────────────────────────────────
Log "Bumping version ($Bump) ..."
if ($DryRun) {
    Log "(dry-run) would run: npm version $Bump --no-git-tag-version"
    $newVersion = "0.0.0-dryrun"
} else {
    npm version $Bump --no-git-tag-version | Out-Null
    $pkg = Get-Content package.json -Raw | ConvertFrom-Json
    $newVersion = $pkg.version
}
Log "New version: $newVersion"

# ── 2. npm publish ───────────────────────────────────────────────────
if (-not $SkipNpm) {
    Log "Publishing to npm (tag=$NpmTag) ..."
    if ($DryRun) {
        Log "(dry-run) would run: npm publish --tag $NpmTag"
    } else {
        npm publish --tag $NpmTag
        if ($LASTEXITCODE -ne 0) { Err "npm publish failed" }
        Log "npm publish OK"
    }
} else {
    Warn "Skipping npm"
}

# ── 3. GitHub release (needed by Homebrew + Chocolatey) ──────────────
$ghAvailable = $null -ne (Get-Command gh -ErrorAction SilentlyContinue)
$tagName = "v$newVersion"
$zipUrl  = ""
$tarUrl  = ""

$isPrerelease = $newVersion -match '-'
$chocoVersion = $newVersion
if ($newVersion -match '^(\d+\.\d+\.\d+)-(\d+)$') {
    # Old Chocolatey/NuGet rejects numeric-only prerelease labels (e.g. 0.1.1-1).
    # Convert to a compatible label for nuspec only.
    $chocoVersion = "$($Matches[1])-beta$($Matches[2])"
}
if ($chocoVersion -ne $newVersion) {
    Log "Chocolatey version normalized: $newVersion -> $chocoVersion"
}

if ($ghAvailable) {
    Log "Creating GitHub release $tagName ..."
    if ($DryRun) {
        Log "(dry-run) would run: gh release create $tagName --generate-notes"
        $zipUrl = "https://github.com/USER/its-magic/archive/refs/tags/$tagName.zip"
        $tarUrl = "https://github.com/USER/its-magic/archive/refs/tags/$tagName.tar.gz"
    } else {
        $ghArgs = @("release", "create", $tagName, "--generate-notes", "--title", $tagName)
        if ($isPrerelease) { $ghArgs += "--prerelease" }
        & gh @ghArgs
        if ($LASTEXITCODE -ne 0) { Warn "gh release create failed - continuing anyway" }
        # Derive archive URL from current remote
        $remoteUrl = git remote get-url origin 2>$null
        if ($remoteUrl -match 'github\.com[:/](.+?)(\.git)?$') {
            $repoSlug = $Matches[1]
            $zipUrl = "https://github.com/$repoSlug/archive/refs/tags/$tagName.zip"
            $tarUrl = "https://github.com/$repoSlug/archive/refs/tags/$tagName.tar.gz"
        }
        Log "GitHub release created: $tagName"
    }
} else {
    Warn "gh CLI not found - skipping GitHub release"
    $zipUrl = "https://github.com/USER/its-magic/archive/refs/tags/$tagName.zip"
    $tarUrl = "https://github.com/USER/its-magic/archive/refs/tags/$tagName.tar.gz"
}

# ── 4. Chocolatey ───────────────────────────────────────────────────
if (-not $SkipChoco) {
    $chocoDir = Join-Path $repoRoot 'packaging\chocolatey'
    $nuspec   = Join-Path $chocoDir 'its-magic.nuspec'
    $chocoInstall = Join-Path $chocoDir 'tools\chocolateyInstall.ps1'

    if (Test-Path $nuspec) {
        Log "Updating Chocolatey nuspec to $chocoVersion ..."
        if (-not $DryRun) {
            # Update version in nuspec
            $xml = [xml](Get-Content $nuspec -Raw)
            $xml.package.metadata.version = $chocoVersion
            $xml.Save($nuspec)

            # Update URL in install script
            $installContent = Get-Content $chocoInstall -Raw
            if ($zipUrl) {
                $installContent = $installContent -replace "\`$url\s*=\s*'[^']+'", "`$url         = '$zipUrl'"
            }
            Set-Content -Path $chocoInstall -Value $installContent
        }

        # Compute checksum if we have the zip
        if ($zipUrl -and -not $DryRun) {
            Log "Downloading zip for checksum ..."
            $tmpZip = Join-Path $env:TEMP "gsd-$tagName.zip"
            try {
                Invoke-WebRequest -Uri $zipUrl -OutFile $tmpZip -UseBasicParsing
                $sha = (Get-FileHash -Path $tmpZip -Algorithm SHA256).Hash.ToLower()
                $installContent = Get-Content $chocoInstall -Raw
                $installContent = $installContent -replace "\`$checksum\s*=\s*'[^']+'", "`$checksum    = '$sha'"
                Set-Content -Path $chocoInstall -Value $installContent
                Remove-Item $tmpZip -Force
                Log "Checksum: $sha"
            } catch {
                Warn "Could not download zip for checksum - set PLACEHOLDER manually"
            }
        }

        $chocoAvailable = $null -ne (Get-Command choco -ErrorAction SilentlyContinue)
        if ($chocoAvailable) {
            Log "Packing + pushing Chocolatey package ..."
            if ($DryRun) {
                Log "(dry-run) would run: choco pack + choco push"
            } else {
                Push-Location $chocoDir
                choco pack
                if ($LASTEXITCODE -ne 0) {
                    $chocoFailed = $true
                    Warn "choco pack failed"
                } else {
                    $nupkg = Get-ChildItem "*.nupkg" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
                    if ($nupkg) {
                        choco push $nupkg.Name --source https://push.chocolatey.org/
                        if ($LASTEXITCODE -ne 0) {
                            $chocoFailed = $true
                            Warn "choco push failed"
                        }
                        else { Log "Chocolatey push OK" }
                    } else {
                        $chocoFailed = $true
                        Warn "No .nupkg created by choco pack"
                    }
                }
                Pop-Location
            }
        } else {
            $chocoFailed = $true
            Warn "choco not found - nuspec updated but not pushed. Run choco pack and choco push manually."
        }
    } else {
        $chocoFailed = $true
        Warn "nuspec not found at $nuspec - skipping Chocolatey"
    }
} else {
    Warn "Skipping Chocolatey"
}

# ── 5. Homebrew ─────────────────────────────────────────────────────
if (-not $SkipBrew) {
    # Detect pre-release: anything with a hyphen
    if ($isPrerelease) {
        $formulaPath = Join-Path $repoRoot 'packaging\homebrew\its-magic-beta.rb'
        Log "Pre-release detected - using beta formula"
    } else {
        $formulaPath = Join-Path $repoRoot 'packaging\homebrew\its-magic.rb'
    }

    if (Test-Path $formulaPath) {
        $formulaName = Split-Path -Leaf $formulaPath
        Log "Updating Homebrew formula ($formulaName) to $newVersion ..."
        if (-not $DryRun) {
            $formula = Get-Content $formulaPath -Raw

            # Update version in URL
            if ($tarUrl) {
                $urlPattern = 'url ' + $DQ + 'https://github\.com/[^' + $DQ + ']+\.tar\.gz' + $DQ
                $urlReplace = 'url ' + $DQ + $tarUrl + $DQ
                $formula = $formula -replace $urlPattern, $urlReplace
            } else {
                $formula = $formula -replace 'vVERSION', $tagName
            }

            # Update explicit version line for beta formula
            if ($isPrerelease) {
                $verPattern = 'version ' + $DQ + '[^' + $DQ + ']*' + $DQ
                $verReplace = 'version ' + $DQ + $newVersion + $DQ
                $formula = $formula -replace $verPattern, $verReplace
            }

            # Compute tar.gz sha256 if possible
            if ($tarUrl) {
                $tmpTar = Join-Path $env:TEMP "gsd-$tagName.tar.gz"
                try {
                    Invoke-WebRequest -Uri $tarUrl -OutFile $tmpTar -UseBasicParsing
                    $sha = (Get-FileHash -Path $tmpTar -Algorithm SHA256).Hash.ToLower()
                    $shaPattern = 'sha256 ' + $DQ + '[^' + $DQ + ']*' + $DQ
                    $shaReplace = 'sha256 ' + $DQ + $sha + $DQ
                    $formula = $formula -replace $shaPattern, $shaReplace
                    Remove-Item $tmpTar -Force
                    Log "Homebrew sha256: $sha"
                } catch {
                    Warn "Could not download tar.gz - set sha256 manually in the formula"
                }
            }

            Set-Content -Path $formulaPath -Value $formula
            Log "Homebrew formula updated: $formulaName"
            if ($isPrerelease) {
                Log "Users install beta with: brew install USER/tap/its-magic-beta"
            } else {
                Log "Users install stable with: brew install USER/tap/its-magic"
            }
        } else {
            $formulaName = Split-Path -Leaf $formulaPath
            Log "(dry-run) would update $formulaName"
        }
    } else {
        Warn "Formula not found at $formulaPath - skipping Homebrew"
    }

    # Optional: publish formulas to Homebrew tap repository
    if (-not $SkipBrewPush) {
        if ($DryRun) {
            Log "(dry-run) would publish formulas to Homebrew tap"
        } else {
            $gitAvailable = $null -ne (Get-Command git -ErrorAction SilentlyContinue)
            $ghAvailableForTap = $null -ne (Get-Command gh -ErrorAction SilentlyContinue)
            if (-not $gitAvailable) {
                $brewTapFailed = $true
                Warn "git not found - cannot push Homebrew formulas to tap"
            } else {
                if (-not $BrewTapRepo) {
                    $originUrl = git remote get-url origin 2>$null
                    if ($originUrl -match 'github\.com[:/](.+?)/(.+?)(\.git)?$') {
                        $owner = $Matches[1]
                        $BrewTapRepo = "$owner/homebrew-tap"
                    }
                }

                if (-not $BrewTapRepo) {
                    $brewTapFailed = $true
                    Warn "Could not infer Homebrew tap repo. Pass -BrewTapRepo owner/homebrew-tap"
                } else {
                    if (-not $BrewTapDir) {
                        $safeTap = ($BrewTapRepo -replace '[^a-zA-Z0-9_-]', '-')
                        $BrewTapDir = Join-Path $env:TEMP "its-magic-$safeTap"
                    }

                    Log "Publishing formulas to tap $BrewTapRepo (branch: $BrewTapBranch) ..."

                    # Use a child scope with relaxed error handling for git commands
                    # that write to stderr even on success (e.g. empty repo warnings).
                    $tapReady = $true
                    $prevEAP = $ErrorActionPreference
                    $ErrorActionPreference = 'Continue'

                    # ── Step A: Ensure we have a local clone ──
                    $tapGitDir = Join-Path $BrewTapDir ".git"

                    # Clean up non-git directory leftovers
                    if ((Test-Path $BrewTapDir) -and -not (Test-Path $tapGitDir)) {
                        Warn "Tap directory exists but is not a git repo. Removing: $BrewTapDir"
                        Remove-Item -Recurse -Force $BrewTapDir
                    }

                    if (Test-Path $tapGitDir) {
                        # Already cloned - fetch latest
                        git -C $BrewTapDir fetch origin 2>&1 | Out-Null
                    } else {
                        # Clone (try gh first, then git)
                        $cloneOk = $false
                        if ($ghAvailableForTap) {
                            & gh repo clone $BrewTapRepo $BrewTapDir 2>&1 | Out-Null
                            if ($LASTEXITCODE -eq 0) { $cloneOk = $true }
                        }
                        if (-not $cloneOk) {
                            git clone "https://github.com/$BrewTapRepo.git" $BrewTapDir 2>&1 | Out-Null
                            if ($LASTEXITCODE -eq 0) { $cloneOk = $true }
                        }
                        if (-not $cloneOk -and $CreateBrewTapIfMissing -and $ghAvailableForTap) {
                            Warn "Tap repo not found. Creating $BrewTapRepo on GitHub ..."
                            & gh repo create $BrewTapRepo --public --description "Homebrew tap for its-magic" 2>&1 | Out-Null
                            if ($LASTEXITCODE -eq 0) {
                                Log "Tap repo created: https://github.com/$BrewTapRepo"
                                if (Test-Path $BrewTapDir) { Remove-Item -Recurse -Force $BrewTapDir }
                                & gh repo clone $BrewTapRepo $BrewTapDir 2>&1 | Out-Null
                                if ($LASTEXITCODE -eq 0) { $cloneOk = $true }
                            }
                        }
                        if (-not $cloneOk) {
                            $tapReady = $false; $brewTapFailed = $true
                            Warn "Failed to clone/create tap repo $BrewTapRepo"
                        }
                    }

                    # ── Step B: Ensure branch exists ──
                    if ($tapReady) {
                        # Check if repo has any commits at all
                        $hasCommits = $false
                        git -C $BrewTapDir log --oneline -1 2>&1 | Out-Null
                        if ($LASTEXITCODE -eq 0) { $hasCommits = $true }

                        if ($hasCommits) {
                            git -C $BrewTapDir checkout $BrewTapBranch 2>&1 | Out-Null
                            if ($LASTEXITCODE -ne 0) {
                                git -C $BrewTapDir checkout -b $BrewTapBranch 2>&1 | Out-Null
                            }
                            # Try to pull if remote branch exists
                            git -C $BrewTapDir pull origin $BrewTapBranch 2>&1 | Out-Null
                        } else {
                            Log "Empty tap repo detected - creating initial branch $BrewTapBranch"
                            git -C $BrewTapDir checkout --orphan $BrewTapBranch 2>&1 | Out-Null
                        }
                    }

                    # ── Step C: Copy formulas, commit, push ──
                    if ($tapReady) {
                        $tapFormulaDir = Join-Path $BrewTapDir "Formula"
                        if (-not (Test-Path $tapFormulaDir)) {
                            New-Item -ItemType Directory -Path $tapFormulaDir -Force | Out-Null
                        }

                        Copy-Item (Join-Path $repoRoot "packaging\homebrew\its-magic.rb") (Join-Path $tapFormulaDir "its-magic.rb") -Force
                        Copy-Item (Join-Path $repoRoot "packaging\homebrew\its-magic-beta.rb") (Join-Path $tapFormulaDir "its-magic-beta.rb") -Force

                        git -C $BrewTapDir add Formula/its-magic.rb Formula/its-magic-beta.rb

                        $tapChanges = git -C $BrewTapDir status --porcelain
                        if ($tapChanges) {
                            git -C $BrewTapDir commit -m "chore: update its-magic formulas for $newVersion" 2>&1 | Out-Null
                            if ($LASTEXITCODE -ne 0) {
                                $brewTapFailed = $true
                                Warn "Failed to commit Homebrew tap changes"
                            } else {
                                git -C $BrewTapDir push -u origin $BrewTapBranch 2>&1 | Out-Null
                                if ($LASTEXITCODE -ne 0) {
                                    $brewTapFailed = $true
                                    Warn "Failed to push Homebrew tap changes"
                                } else {
                                    $brewTapPushed = $true
                                    Log "Homebrew tap updated: https://github.com/$BrewTapRepo"
                                }
                            }
                        } else {
                            Log "No Homebrew formula changes to push"
                        }
                    }

                    $ErrorActionPreference = $prevEAP
                }
            }
        }
    } else {
        Warn "Skipping Homebrew tap push"
    }
} else {
    Warn "Skipping Homebrew"
}

# ── Done ─────────────────────────────────────────────────────────────
Pop-Location
$npmStatus = "OK"
if ($SkipNpm) { $npmStatus = "SKIPPED" }
$chocoStatus = "OK"
if ($SkipChoco) { $chocoStatus = "SKIPPED" }
elseif ($DryRun) { $chocoStatus = "DRY-RUN" }
elseif ($chocoFailed) { $chocoStatus = "FAILED - check log" }
$brewStatus = "OK - formula updated"
if ($SkipBrew) { $brewStatus = "SKIPPED" }
elseif ($brewTapFailed) { $brewStatus = "FORMULA OK - TAP PUSH FAILED" }
elseif ($brewTapPushed) { $brewStatus = "OK - formula updated + tap pushed" }

Log "=========================================="
Log "Release $newVersion complete!"
Log "  npm:         $npmStatus"
Log "  Chocolatey:  $chocoStatus"
Log "  Homebrew:    $brewStatus"
Log "=========================================="
