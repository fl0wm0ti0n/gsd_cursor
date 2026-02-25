#!/usr/bin/env sh
# -------------------------------------------------------------------
# validate-and-push.sh — local test-fix-push loop
#
# Part of the its-magic quality chain:
#   Cursor AI loop  →  validate-and-push  →  CI auto-fix (GitHub)
#
# Reads TEST_COMMAND (and optionally LINT_FIX_COMMAND / FORMAT_COMMAND)
# from docs/engineering/runbook.md, runs them in a loop, and pushes
# only when everything passes.
# -------------------------------------------------------------------
set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MAX_ATTEMPTS="${1:-5}"
BRANCH="${2:-}"
AUTO_COMMIT="${3:-true}"
TIMEOUT_SEC=120

pass_color="\033[1;32m"
fail_color="\033[1;31m"
info_color="\033[1;36m"
warn_color="\033[1;33m"
reset="\033[0m"

log_info()  { printf "${info_color}[info]${reset}  %s\n" "$*"; }
log_pass()  { printf "${pass_color}[pass]${reset}  %s\n" "$*"; }
log_fail()  { printf "${fail_color}[fail]${reset}  %s\n" "$*"; }
log_warn()  { printf "${warn_color}[warn]${reset}  %s\n" "$*"; }

run_with_timeout() {
  if command -v timeout >/dev/null 2>&1; then
    timeout "$TIMEOUT_SEC" "$@"
  elif command -v gtimeout >/dev/null 2>&1; then
    gtimeout "$TIMEOUT_SEC" "$@"
  else
    "$@"
  fi
}

# --- Read commands from runbook ------------------------------------------

RUNBOOK="$ROOT/docs/engineering/runbook.md"

read_runbook_key() {
  key="$1"
  if [ ! -f "$RUNBOOK" ]; then return; fi
  value=$(sed -n "s/^${key}:[[:space:]]*\(.\{1,\}\)$/\1/p" "$RUNBOOK" | head -n 1)
  case "$value" in
    ""|"..."|"<...>"|"TODO") return ;;
  esac
  printf "%s" "$value"
}

TEST_CMD=$(read_runbook_key "TEST_COMMAND")
LINT_CMD=$(read_runbook_key "LINT_COMMAND")
TYPECHECK_CMD=$(read_runbook_key "TYPECHECK_COMMAND")
LINT_FIX_CMD=$(read_runbook_key "LINT_FIX_COMMAND")
FORMAT_CMD=$(read_runbook_key "FORMAT_COMMAND")
TIMEOUT_FROM_RUNBOOK=$(read_runbook_key "TEST_TIMEOUT_SECONDS")
if [ -n "$TIMEOUT_FROM_RUNBOOK" ]; then
  TIMEOUT_SEC="$TIMEOUT_FROM_RUNBOOK"
fi

if [ -z "$TEST_CMD" ]; then
  log_fail "TEST_COMMAND is required by sync policy and cannot be blank."
  log_warn "Reason code: TEST_COMMAND_MISSING"
  log_warn "Set TEST_COMMAND in docs/engineering/runbook.md and re-run."
  exit 1
fi

if [ -z "$BRANCH" ]; then
  BRANCH=$(git -C "$ROOT" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")
fi

log_info "validate-and-push loop"
log_info "Branch: $BRANCH  |  Max attempts: $MAX_ATTEMPTS"
[ -n "$TEST_CMD" ]     && log_info "TEST_COMMAND:     $TEST_CMD"
[ -n "$LINT_CMD" ]     && log_info "LINT_COMMAND:     $LINT_CMD"
[ -n "$TYPECHECK_CMD" ] && log_info "TYPECHECK_COMMAND: $TYPECHECK_CMD"
[ -n "$LINT_FIX_CMD" ] && log_info "LINT_FIX_COMMAND: $LINT_FIX_CMD"
[ -n "$FORMAT_CMD" ]   && log_info "FORMAT_COMMAND:   $FORMAT_CMD"
log_info "TEST_TIMEOUT_SECONDS: $TIMEOUT_SEC"
printf "\n"

run_cmd() {
  cmd="$1"
  if run_with_timeout sh -c "$cmd"; then
    return 0
  fi
  return 1
}

attempt=0
while [ "$attempt" -lt "$MAX_ATTEMPTS" ]; do
  attempt=$((attempt + 1))
  log_info "--- Attempt $attempt / $MAX_ATTEMPTS ---"

  cd "$ROOT"
  all_ok=true

  # 1. Run formatter if available
  if [ -n "$FORMAT_CMD" ]; then
    log_info "Running formatter..."
    if eval "$FORMAT_CMD"; then
      log_pass "Format OK"
    else
      log_warn "Formatter reported issues (non-blocking)"
    fi
  fi

  # 2. Try lint fix if available
  if [ -n "$LINT_FIX_CMD" ]; then
    log_info "Running lint auto-fix..."
    eval "$LINT_FIX_CMD" || true
  fi

  # 2. Mandatory test baseline
  log_info "Running mandatory TEST_COMMAND..."
  if run_cmd "$TEST_CMD"; then
    log_pass "TEST_COMMAND passed"
  else
    log_fail "TEST_COMMAND failed or timed out"
    log_warn "Reason code: TEST_FAILED or TEST_TIMEOUT"
    all_ok=false
  fi

  # 3. Optional lint check
  if [ -n "$LINT_CMD" ]; then
    log_info "Running optional LINT_COMMAND..."
    if run_cmd "$LINT_CMD"; then
      log_pass "Lint OK"
    else
      log_fail "Lint failed"
      log_warn "Reason code: OPTIONAL_CHECK_FAILED"
      all_ok=false
    fi
  else
    log_info "LINT_COMMAND not configured -> skipped"
  fi

  # 4. Optional typecheck check
  if [ -n "$TYPECHECK_CMD" ]; then
    log_info "Running optional TYPECHECK_COMMAND..."
    if run_cmd "$TYPECHECK_CMD"; then
      log_pass "Typecheck OK"
    else
      log_fail "Typecheck failed"
      log_warn "Reason code: OPTIONAL_CHECK_FAILED"
      all_ok=false
    fi
  else
    log_info "TYPECHECK_COMMAND not configured -> skipped"
  fi

  if [ "$all_ok" = "true" ]; then
    log_pass "All checks passed on attempt $attempt."
    break
  fi

  if [ "$attempt" -ge "$MAX_ATTEMPTS" ]; then
    log_fail "Reached max attempts ($MAX_ATTEMPTS). Aborting push."
    printf "\n"
    log_warn "Fix the issues above, then re-run:"
    log_warn "  sh scripts/validate-and-push.sh"
    exit 1
  fi

  printf "\n"
  log_warn "Fix the failing checks, then press Enter to retry (or Ctrl+C to abort)..."
  read -r _unused
done

printf "\n"

if [ "$AUTO_COMMIT" = "true" ]; then
  cd "$ROOT"
  if [ -n "$(git status --porcelain)" ]; then
    log_info "Staging and committing changes..."
    git add -A
    git commit -m "fix: address check failures (validate-and-push)"
  else
    log_info "Working tree clean, nothing to commit."
  fi

  log_info "Pushing to origin/$BRANCH..."
  git push origin "$BRANCH"
  log_pass "Push successful."
else
  log_info "Auto-commit disabled. Push manually when ready."
fi
