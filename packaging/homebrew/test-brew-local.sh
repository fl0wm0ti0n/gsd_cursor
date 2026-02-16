#!/usr/bin/env sh
# Test the Homebrew formula locally (no tap upload needed).
# Creates a local tap, installs from the formula, runs a smoke test
# into a temp directory, then uninstalls.
set -e

SKIP_UNINSTALL=false
FORMULA="its-magic"
for arg in "$@"; do
    case "$arg" in
        --skip-uninstall) SKIP_UNINSTALL=true ;;
        --beta) FORMULA="its-magic-beta" ;;
    esac
done

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

log()  { printf "\033[1;36m[test-brew] %s\033[0m\n" "$1"; }
pass() { printf "\033[1;32m[test-brew] PASS - %s\033[0m\n" "$1"; }
fail() { printf "\033[1;31m[test-brew] FAIL - %s\033[0m\n" "$1"; }

# --- Check prerequisites ---
if ! command -v brew >/dev/null 2>&1; then
    fail "brew not found. Install Homebrew first: https://brew.sh"
    exit 1
fi

FORMULA_FILE="$SCRIPT_DIR/${FORMULA}.rb"
if [ ! -f "$FORMULA_FILE" ]; then
    fail "Formula not found: $FORMULA_FILE"
    exit 1
fi
log "Testing formula: $FORMULA_FILE"

# --- Validate formula syntax ---
log "Validating formula syntax ..."
if brew style "$FORMULA_FILE" 2>/dev/null; then
    pass "Formula syntax is valid"
else
    # brew style returns non-zero for warnings too, not always fatal
    log "brew style returned warnings (may be non-fatal)"
fi

# --- Uninstall previous version (if any) ---
if brew list "$FORMULA" >/dev/null 2>&1; then
    log "Removing previous $FORMULA install ..."
    brew uninstall "$FORMULA" 2>/dev/null || true
else
    log "No previous $FORMULA install found (clean slate)"
fi

# --- Install from local formula ---
log "Installing from local formula ..."
brew install --formula "$FORMULA_FILE"
if [ $? -ne 0 ]; then
    fail "brew install failed"
    exit 1
fi
pass "brew install succeeded"

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
if echo "$HELP_OUTPUT" | grep -qiE 'its-magic|Usage|target|install'; then
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

# Cleanup temp dir
rm -rf "$TEST_DIR"

# --- Caveats ---
log "Checking caveats ..."
CAVEATS=$(brew info "$FORMULA" 2>/dev/null | grep -A5 "Caveats" || true)
if [ -n "$CAVEATS" ]; then
    pass "Caveats block present"
else
    log "No caveats found (optional)"
fi

# --- Uninstall ---
if [ "$SKIP_UNINSTALL" = "false" ]; then
    log "Uninstalling ..."
    brew uninstall "$FORMULA"
    pass "Uninstall succeeded"
else
    log "Skipping uninstall (--skip-uninstall flag set)"
fi

# --- Summary ---
echo ""
log "=========================================="
log "  Local Homebrew test complete! ($FORMULA)"
log "=========================================="
