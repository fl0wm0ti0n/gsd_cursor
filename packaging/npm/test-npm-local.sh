#!/usr/bin/env sh
# Test the npm package locally (no upload needed).
# Packs with npm pack, installs globally from the tarball, runs a smoke test
# into a temp directory, then uninstalls.
set -e

SKIP_UNINSTALL=false
for arg in "$@"; do
    case "$arg" in
        --skip-uninstall) SKIP_UNINSTALL=true ;;
    esac
done

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
if [ ! -f "$REPO_ROOT/package.json" ]; then
    REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
fi

log()  { printf "\033[1;36m[test-npm] %s\033[0m\n" "$1"; }
pass() { printf "\033[1;32m[test-npm] PASS - %s\033[0m\n" "$1"; }
fail() { printf "\033[1;31m[test-npm] FAIL - %s\033[0m\n" "$1"; }

# --- Check prerequisites ---
if ! command -v npm >/dev/null 2>&1; then
    fail "npm not found. Install Node.js first."
    exit 1
fi
if ! command -v node >/dev/null 2>&1; then
    fail "node not found. Install Node.js first."
    exit 1
fi

cd "$REPO_ROOT"

# --- Clean old tarballs ---
log "Cleaning old tarballs ..."
rm -f its-magic-*.tgz

# --- Pack ---
log "Running npm pack ..."
npm pack
TGZ=$(ls -t its-magic-*.tgz 2>/dev/null | head -1)
if [ -z "$TGZ" ]; then
    fail "npm pack did not create a .tgz file"
    exit 1
fi
pass "Package created: $TGZ"

# --- Uninstall previous global install (if any) ---
log "Removing previous global its-magic (if any) ..."
npm uninstall -g its-magic 2>/dev/null || true

# --- Install globally from local tarball ---
log "Installing globally from local tarball ..."
npm install -g "$TGZ"
pass "npm install -g succeeded"

# --- Smoke test: check the command exists ---
log "Running smoke tests ..."
if command -v its-magic >/dev/null 2>&1; then
    pass "Command found: $(command -v its-magic)"
else
    fail "its-magic command not found in PATH"
fi

# --- Smoke test: run its-magic --help ---
log "Testing 'its-magic --help' ..."
HELP_OUTPUT=$(its-magic --help 2>&1 || true)
if echo "$HELP_OUTPUT" | grep -qiE 'its-magic|Usage|target'; then
    pass "its-magic --help works"
    printf "\033[1;30m%s\033[0m\n" "$HELP_OUTPUT"
else
    fail "its-magic --help did not return expected output"
    echo "$HELP_OUTPUT"
fi

# --- Smoke test: install into a temp directory ---
TEST_DIR=$(mktemp -d)
log "Testing install into temp dir: $TEST_DIR ..."
its-magic --target "$TEST_DIR" --mode missing --create 2>/dev/null || true

ALL_FOUND=true
for f in \
    ".cursor/commands/intake.md" \
    ".cursor/rules/core.mdc" \
    ".cursor/hooks.json" \
    ".cursor/scratchpad.md" \
    "docs/engineering/runbook.md"
do
    if [ -f "$TEST_DIR/$f" ]; then
        pass "File installed: $f"
    else
        fail "File missing: $f"
        ALL_FOUND=false
    fi
done

# --- Smoke test: upgrade mode in temp directory ---
echo "npm-cli-upgrade-marker" > "$TEST_DIR/.cursor/commands/intake.md"
its-magic --target "$TEST_DIR" --mode upgrade 2>/dev/null || true
if ! grep -q "npm-cli-upgrade-marker" "$TEST_DIR/.cursor/commands/intake.md"; then
    pass "Upgrade restores framework file in temp repo"
else
    fail "Upgrade did not restore framework file in temp repo"
fi

# --- Smoke test: clean-repo safety in temp directory ---
mkdir -p "$TEST_DIR/src"
echo "npm-cli-marker" > "$TEST_DIR/src/keep.txt"
its-magic --clean-repo --target "$TEST_DIR" --yes 2>/dev/null || true
if [ ! -d "$TEST_DIR/.cursor" ]; then
    pass "Clean-repo removed framework artifacts"
else
    fail "Clean-repo did not remove framework artifacts"
fi
if [ -f "$TEST_DIR/src/keep.txt" ]; then
    pass "Clean-repo preserved non-framework marker file"
else
    fail "Clean-repo removed non-framework marker file"
fi

# Cleanup temp dir
rm -rf "$TEST_DIR"

# --- Clean tarball ---
rm -f "$TGZ"

# --- Uninstall ---
if [ "$SKIP_UNINSTALL" = "false" ]; then
    log "Uninstalling ..."
    npm uninstall -g its-magic
    pass "Uninstall succeeded"
else
    log "Skipping uninstall (--skip-uninstall flag set)"
fi

# --- Summary ---
echo ""
log "=========================================="
log "  Local npm test complete!"
log "=========================================="
