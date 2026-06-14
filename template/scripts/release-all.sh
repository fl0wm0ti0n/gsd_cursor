#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────
# Unified release: npm + Chocolatey + Homebrew (all three at once)
# ─────────────────────────────────────────────────────────────────
set -euo pipefail

BUMP="patch"
NPM_TAG="latest"
SKIP_NPM=false
SKIP_CHOCO=false
SKIP_BREW=false
DRY_RUN=false

usage() {
  cat <<EOF
Usage: $0 [options]
  --bump <patch|minor|major|x.y.z>  Version bump (default: patch)
  --npm-tag <tag>                    npm dist-tag (default: latest)
  --skip-npm                         Skip npm publish
  --skip-choco                       Skip Chocolatey push
  --skip-brew                        Skip Homebrew formula update
  --dry-run                          Print actions without executing
  -h|--help                          Show this help
EOF
  exit 0
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --bump)      BUMP="$2"; shift 2;;
    --npm-tag)   NPM_TAG="$2"; shift 2;;
    --skip-npm)  SKIP_NPM=true; shift;;
    --skip-choco)SKIP_CHOCO=true; shift;;
    --skip-brew) SKIP_BREW=true; shift;;
    --dry-run)   DRY_RUN=true; shift;;
    -h|--help)   usage;;
    *) echo "Unknown option: $1"; usage;;
  esac
done

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

# Node 22+: trust OS CA store when TLS inspection adds system CAs (Windows/antivirus/corp proxy).
export NODE_USE_SYSTEM_CA="${NODE_USE_SYSTEM_CA:-1}"

log()  { echo -e "\033[36m[release]\033[0m $1"; }
warn() { echo -e "\033[33m[release]\033[0m $1"; }
err()  { echo -e "\033[31m[release]\033[0m $1"; exit 1; }

# ── 1. Version bump ─────────────────────────────────────────────────
log "Bumping version ($BUMP) ..."
if $DRY_RUN; then
  log "(dry-run) would run: npm version $BUMP --no-git-tag-version"
  NEW_VERSION="0.0.0-dryrun"
else
  npm version "$BUMP" --no-git-tag-version >/dev/null
  NEW_VERSION=$(node -p "require('./package.json').version")
fi
TAG_NAME="v$NEW_VERSION"
log "New version: $NEW_VERSION  (tag: $TAG_NAME)"
CHOCO_VERSION="$NEW_VERSION"
if [[ "$NEW_VERSION" =~ ^([0-9]+\.[0-9]+\.[0-9]+)-([0-9]+)$ ]]; then
  # Old Chocolatey/NuGet rejects numeric-only prerelease labels (e.g. 0.1.1-1).
  # Convert to a compatible label for nuspec only.
  CHOCO_VERSION="${BASH_REMATCH[1]}-beta${BASH_REMATCH[2]}"
fi
if [[ "$CHOCO_VERSION" != "$NEW_VERSION" ]]; then
  log "Chocolatey version normalized: $NEW_VERSION -> $CHOCO_VERSION"
fi

# ── 2. npm publish ──────────────────────────────────────────────────
if ! $SKIP_NPM; then
  log "Publishing to npm (tag=$NPM_TAG) ..."
  if $DRY_RUN; then
    log "(dry-run) would run: npm publish --tag $NPM_TAG"
  else
    npm publish --tag "$NPM_TAG"
    log "npm publish OK"
  fi
else
  warn "Skipping npm"
fi

# ── 3. GitHub release ───────────────────────────────────────────────
ZIP_URL=""
TAR_URL=""

GH_PRERELEASE=""
if [[ "$NEW_VERSION" == *-* ]]; then
  GH_PRERELEASE="--prerelease"
fi

RELEASE_CHANGELOG_ALLOW_GENERATE_NOTES="${RELEASE_CHANGELOG_ALLOW_GENERATE_NOTES:-0}"
VERSION_NOTES="handoffs/releases/${NEW_VERSION}-release-notes.md"

if command -v gh &>/dev/null; then
  log "Creating GitHub release $TAG_NAME ..."
  if [[ ! -f "$VERSION_NOTES" ]]; then
    log "Version notes missing — deriving via release_changelog_backfill --ensure-version ..."
    if ! $DRY_RUN; then
      python scripts/release_changelog_backfill.py --repo "$REPO_ROOT" --ensure-version "$NEW_VERSION" || true
    fi
  fi
  if $DRY_RUN; then
    if [[ -f "$VERSION_NOTES" ]]; then
      log "(dry-run) would run: python scripts/release_changelog_validate.py --repo . --enforce"
      log "(dry-run) would run: gh release create $TAG_NAME -F $VERSION_NOTES --title $TAG_NAME $GH_PRERELEASE"
    else
      log "(dry-run) would fail-closed: RELEASE_CHANGELOG_VERSION_DOC_MISSING ($VERSION_NOTES)"
    fi
  elif [[ -f "$VERSION_NOTES" ]]; then
    python scripts/release_changelog_validate.py --repo "$REPO_ROOT" --enforce
    gh release create "$TAG_NAME" -F "$VERSION_NOTES" --title "$TAG_NAME" $GH_PRERELEASE || warn "gh release create failed – continuing"
  elif [[ "$RELEASE_CHANGELOG_ALLOW_GENERATE_NOTES" == "1" ]]; then
    warn "RELEASE_CHANGELOG_VERSION_DOC_MISSING: $VERSION_NOTES — falling back to --generate-notes (opt-in)"
    gh release create "$TAG_NAME" --generate-notes --title "$TAG_NAME" $GH_PRERELEASE || warn "gh release create failed – continuing"
  else
    err "RELEASE_CHANGELOG_VERSION_DOC_MISSING: $VERSION_NOTES (set RELEASE_CHANGELOG_ALLOW_GENERATE_NOTES=1 to opt into --generate-notes)"
  fi
  REMOTE_URL=$(git remote get-url origin 2>/dev/null || true)
  if [[ "$REMOTE_URL" =~ github\.com[:/](.+?)(\.git)?$ ]]; then
    REPO_SLUG="${BASH_REMATCH[1]}"
    REPO_SLUG="${REPO_SLUG%.git}"
    ZIP_URL="https://github.com/$REPO_SLUG/archive/refs/tags/$TAG_NAME.zip"
    TAR_URL="https://github.com/$REPO_SLUG/archive/refs/tags/$TAG_NAME.tar.gz"
  fi
else
  warn "gh CLI not found – skipping GitHub release"
  ZIP_URL="https://github.com/USER/its-magic/archive/refs/tags/$TAG_NAME.zip"
  TAR_URL="https://github.com/USER/its-magic/archive/refs/tags/$TAG_NAME.tar.gz"
fi

# ── 4. Chocolatey ───────────────────────────────────────────────────
if ! $SKIP_CHOCO; then
  NUSPEC="$REPO_ROOT/packaging/chocolatey/its-magic.nuspec"
  CHOCO_INSTALL="$REPO_ROOT/packaging/chocolatey/tools/chocolateyInstall.ps1"

  if [[ -f "$NUSPEC" ]]; then
    log "Updating Chocolatey nuspec to $CHOCO_VERSION ..."
    if ! $DRY_RUN; then
      # Update version in nuspec (simple sed)
      sed -i.bak "s|<version>[^<]*</version>|<version>$CHOCO_VERSION</version>|" "$NUSPEC"
      rm -f "${NUSPEC}.bak"

      # Update URL in install script
      if [[ -n "$ZIP_URL" ]]; then
        sed -i.bak "s|^\\$url[[:space:]]*=.*$|\\$url         = '$ZIP_URL'|" "$CHOCO_INSTALL"
        rm -f "${CHOCO_INSTALL}.bak"
      fi

      # Compute checksum
      if [[ -n "$ZIP_URL" ]]; then
        TMP_ZIP="/tmp/its-magic-$TAG_NAME.zip"
        if curl -fsSL "$ZIP_URL" -o "$TMP_ZIP" 2>/dev/null; then
          SHA=$(shasum -a 256 "$TMP_ZIP" | awk '{print $1}')
          sed -i.bak "s|^\\$checksum[[:space:]]*=.*$|\\$checksum    = '$SHA'|" "$CHOCO_INSTALL"
          rm -f "${CHOCO_INSTALL}.bak" "$TMP_ZIP"
          log "Chocolatey checksum: $SHA"
        else
          warn "Could not download zip for checksum – set PLACEHOLDER manually"
        fi
      fi
    fi

    if command -v choco &>/dev/null; then
      log "Packing + pushing Chocolatey package ..."
      if ! $DRY_RUN; then
        (cd "$REPO_ROOT/packaging/chocolatey" && choco pack && \
         NUPKG=$(ls -1t *.nupkg 2>/dev/null | head -1) && \
         choco push "$NUPKG" --source https://push.chocolatey.org/ || warn "choco push failed")
      fi
    else
      warn "choco not found – nuspec updated but not pushed"
    fi
  else
    warn "nuspec not found – skipping Chocolatey"
  fi
else
  warn "Skipping Chocolatey"
fi

# ── 5. Homebrew ─────────────────────────────────────────────────────
if ! $SKIP_BREW; then
  # Detect pre-release: anything with a hyphen (e.g. 0.2.0-beta.1, 1.0.0-rc.1)
  IS_PRERELEASE=false
  if [[ "$NEW_VERSION" == *-* ]]; then
    IS_PRERELEASE=true
  fi

  if $IS_PRERELEASE; then
    FORMULA="$REPO_ROOT/packaging/homebrew/its-magic-beta.rb"
    log "Pre-release detected – using beta formula"
  else
    FORMULA="$REPO_ROOT/packaging/homebrew/its-magic.rb"
  fi

  if [[ -f "$FORMULA" ]]; then
    FORMULA_NAME=$(basename "$FORMULA")
    log "Updating Homebrew formula ($FORMULA_NAME) to $NEW_VERSION ..."
    if ! $DRY_RUN; then
      if [[ -n "$TAR_URL" ]]; then
        sed -i.bak "s|url \"https://github.com/[^\"]*\.tar\.gz\"|url \"$TAR_URL\"|" "$FORMULA"
        rm -f "${FORMULA}.bak"
      else
        sed -i.bak "s|vVERSION|$TAG_NAME|g" "$FORMULA"
        rm -f "${FORMULA}.bak"
      fi

      # Update explicit version line for beta formula
      if $IS_PRERELEASE; then
        sed -i.bak "s|version \"[^\"]*\"|version \"$NEW_VERSION\"|" "$FORMULA"
        rm -f "${FORMULA}.bak"
      fi

      # Compute sha256
      if [[ -n "$TAR_URL" ]]; then
        TMP_TAR="/tmp/its-magic-$TAG_NAME.tar.gz"
        if curl -fsSL "$TAR_URL" -o "$TMP_TAR" 2>/dev/null; then
          SHA=$(shasum -a 256 "$TMP_TAR" | awk '{print $1}')
          # Replace both PLACEHOLDER and any previous sha256 value
          sed -i.bak "s|sha256 \"[^\"]*\"|sha256 \"$SHA\"|" "$FORMULA"
          rm -f "${FORMULA}.bak" "$TMP_TAR"
          log "Homebrew sha256: $SHA"
        else
          warn "Could not download tar.gz – set sha256 manually"
        fi
      fi
      log "Homebrew formula updated: $FORMULA_NAME"
      if $IS_PRERELEASE; then
        log "Users install beta with: brew install USER/tap/its-magic-beta"
      else
        log "Users install stable with: brew install USER/tap/its-magic"
      fi
    fi
  else
    warn "Formula not found – skipping Homebrew"
  fi
else
  warn "Skipping Homebrew"
fi

# ── Done ─────────────────────────────────────────────────────────────
log "=========================================="
log "Release $NEW_VERSION complete!"
log "  npm:         $(if $SKIP_NPM; then echo 'SKIPPED'; else echo 'OK'; fi)"
log "  Chocolatey:  $(if $SKIP_CHOCO; then echo 'SKIPPED'; else echo 'OK (check warnings)'; fi)"
log "  Homebrew:    $(if $SKIP_BREW; then echo 'SKIPPED'; else echo 'OK (formula updated)'; fi)"
log "=========================================="
