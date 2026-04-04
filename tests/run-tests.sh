#!/usr/bin/env sh
set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TPL="$ROOT/template"
REPORT="$ROOT/tests/report.md"
TMP="$ROOT/tests/.tmp-install"
TIMEOUT_SEC="${TEST_TIMEOUT_SECONDS:-120}"

pass=0
fail=0

run_with_timeout() {
  if command -v timeout >/dev/null 2>&1; then
    timeout "$TIMEOUT_SEC" "$@"
  elif command -v gtimeout >/dev/null 2>&1; then
    gtimeout "$TIMEOUT_SEC" "$@"
  else
    "$@"
  fi
}

add_result() {
  name="$1"
  status="$2"
  detail="$3"
  if [ "$status" = "PASS" ]; then
    pass=$((pass + 1))
  else
    fail=$((fail + 1))
  fi
  if [ -n "$detail" ]; then
    RESULTS="$RESULTS\n- [$status] $name - $detail"
  else
    RESULTS="$RESULTS\n- [$status] $name"
  fi
}

assert_true() {
  name="$1"
  condition="$2"
  detail="$3"
  if eval "$condition" >/dev/null 2>&1; then
    add_result "$name" "PASS" "$detail"
  else
    add_result "$name" "FAIL" "$detail"
  fi
}

file_contains() {
  path="$1"
  text="$2"
  [ -f "$path" ] && grep -q "$text" "$path"
}

write_bootstrap_pkg_json() {
  target_dir="$1"
  cat > "$target_dir/package.json" <<'EOF'
{
  "name": "bootstrap-fixture",
  "version": "1.0.0",
  "scripts": {
    "test": "echo ok",
    "lint": "echo lint",
    "typecheck": "echo typecheck"
  }
}
EOF
}

assert_true "template/ folder exists" "[ -d \"$TPL\" ]"
assert_true "Commands folder exists" "[ -d \"$TPL/.cursor/commands\" ]"
assert_true "Rules folder exists" "[ -d \"$TPL/.cursor/rules\" ]"
assert_true "Skills folder exists" "[ -d \"$TPL/.cursor/skills/its-magic/templates\" ]"
assert_true "Agents folder exists" "[ -d \"$TPL/.cursor/agents\" ]"
assert_true "Hooks config exists" "[ -f \"$TPL/.cursor/hooks.json\" ]"
assert_true "Docs folder exists" "[ -d \"$TPL/docs\" ]"
assert_true "Sprints folder exists" "[ -d \"$TPL/sprints\" ]"
assert_true "Handoffs folder exists" "[ -d \"$TPL/handoffs\" ]"
assert_true "Decisions folder exists" "[ -d \"$TPL/decisions\" ]"
assert_true "Workflows folder exists" "[ -d \"$TPL/.github/workflows\" ]"

cmd_count=$(ls "$TPL/.cursor/commands"/*.md 2>/dev/null | wc -l | tr -d ' ')
rule_count=$(ls "$TPL/.cursor/rules"/*.mdc 2>/dev/null | wc -l | tr -d ' ')
agent_count=$(ls "$TPL/.cursor/agents"/*.mdc 2>/dev/null | wc -l | tr -d ' ')
assert_true "23 commands exist" "[ $cmd_count -eq 23 ]"
assert_true "5 rules exist" "[ $rule_count -eq 5 ]"
assert_true "7 agents exist" "[ $agent_count -eq 7 ]"

for file in "$TPL/.cursor/commands"/*.md; do
  name=$(basename "$file")
  ok="true"
  grep -q "## Subagents" "$file" || ok="false"
  grep -q "## Inputs" "$file" || ok="false"
  grep -q "## Outputs" "$file" || ok="false"
  grep -q "## Stop conditions" "$file" || ok="false"
  if [ "$ok" = "true" ]; then
    add_result "Command sections present: $name" "PASS"
  else
    add_result "Command sections present: $name" "FAIL"
  fi
done

runbook="$TPL/docs/engineering/runbook.md"
assert_true "Runbook contains TEST_COMMAND" "file_contains \"$runbook\" \"TEST_COMMAND\""
assert_true "Runbook contains LINT_COMMAND" "file_contains \"$runbook\" \"LINT_COMMAND\""
assert_true "Runbook contains TYPECHECK_COMMAND" "file_contains \"$runbook\" \"TYPECHECK_COMMAND\""
assert_true "Runbook documents OS-aware bootstrap contract (template)" "file_contains \"$runbook\" \"OS-aware runbook command bootstrap (US-0063 / DEC-0046)\""
assert_true "Runbook contains DEPLOY_STAGING_COMMAND" "file_contains \"$runbook\" \"DEPLOY_STAGING_COMMAND\""
assert_true "Runbook contains DEPLOY_PROD_COMMAND" "file_contains \"$runbook\" \"DEPLOY_PROD_COMMAND\""
assert_true "Runbook documents US-0015 intentional empty commands (template)" "file_contains \"$runbook\" \"Intentional empty commands (US-0015)\""

ci="$TPL/.github/workflows/ci.yml"
deploy="$TPL/.github/workflows/deploy.yml"
assert_true "CI workflow references TEST_COMMAND" "file_contains \"$ci\" \"TEST_COMMAND\""
assert_true "CI workflow references LINT_COMMAND" "file_contains \"$ci\" \"LINT_COMMAND\""
assert_true "CI workflow references TYPECHECK_COMMAND" "file_contains \"$ci\" \"TYPECHECK_COMMAND\""
assert_true "Deploy workflow references DEPLOY_STAGING_COMMAND" "file_contains \"$deploy\" \"DEPLOY_STAGING_COMMAND\""
assert_true "Deploy workflow references DEPLOY_PROD_COMMAND" "file_contains \"$deploy\" \"DEPLOY_PROD_COMMAND\""
assert_true "README documents US-0015 intent contract (template)" "file_contains \"$TPL/README.md\" \"US-0015 intent contract\""

# 4b) Homebrew stable formula version sync (US-0016)
PKG_VERSION="$(node -p "require('./package.json').version" 2>/dev/null)"
if [ -n "$PKG_VERSION" ] && [ -f "$ROOT/packaging/homebrew/its-magic.rb" ]; then
  assert_true "Homebrew stable formula URL uses npm version tag" "file_contains \"$ROOT/packaging/homebrew/its-magic.rb\" \"v$PKG_VERSION.tar.gz\""
  assert_true "Homebrew stable formula version matches npm version" "file_contains \"$ROOT/packaging/homebrew/its-magic.rb\" \"version \\\"$PKG_VERSION\\\"\""
else
  assert_true "Homebrew stable formula version sync checks" "false"
fi

rm -rf "$TMP"
mkdir -p "$TMP"
write_bootstrap_pkg_json "$TMP"
if [ -f "$ROOT/installer.sh" ]; then
  run_with_timeout sh "$ROOT/installer.sh" --target "$TMP" --mode missing --create < /dev/null >/dev/null
  assert_true "Installer (sh) installs commands" "[ -f \"$TMP/.cursor/commands/intake.md\" ]"
  assert_true "Installer (sh) installs ownership manifest" "[ -f \"$TMP/docs/engineering/context/installer-owned-paths.manifest\" ]"
  assert_true "Installer ownership manifest includes its_magic boundary" "file_contains \"$TMP/docs/engineering/context/installer-owned-paths.manifest\" \"its_magic\""
  assert_true "Installer manifest omits manifest-copied scratchpad.md (US-0073)" "! file_contains \"$TMP/docs/engineering/context/installer-owned-paths.manifest\" \".cursor/scratchpad.md\""
  assert_true "Fresh install materializes scratchpad baseline (US-0073)" "[ -f \"$TMP/.cursor/scratchpad.md\" ]"
  assert_true "Materialized scratchpad contains MAGIC_CONTEXT_STRICT (US-0073)" "file_contains \"$TMP/.cursor/scratchpad.md\" \"MAGIC_CONTEXT_STRICT=\""
  assert_true "Installer runbook TEST_COMMAND present for detectable stack" "grep -qE '^TEST_COMMAND:[[:space:]]*(npm run test|sh tests/run-tests\\.sh)' \"$TMP/docs/engineering/runbook.md\""
  assert_true "Installer mirrors root README into its_magic README" "file_contains \"$TMP/its_magic/README.md\" \"US-0015 intent contract\""
  assert_true "Fresh install has neutral status-normalization report" "file_contains \"$TMP/docs/engineering/status-normalization-report.md\" \"(none yet)\""
  assert_true "Fresh install has no seeded status-normalization row" "! grep -q 'US-0018' \"$TMP/docs/engineering/status-normalization-report.md\""
  assert_true "Fresh install research has no hardcoded DEC-0011 reference" "! grep -q 'DEC-0011' \"$TMP/docs/engineering/research.md\""
  rm -f "$TMP/.cursor/scratchpad.md"
  if command -v python3 >/dev/null 2>&1; then SPY=python3; elif command -v python >/dev/null 2>&1; then SPY=python; else SPY=""; fi
  assert_true "scratchpad-postinstall recovery exit 0 (US-0073)" "[ -n \"$SPY\" ] && \"$SPY\" \"$ROOT/installer.py\" --scratchpad-postinstall --target \"$TMP\" --mode missing"
  assert_true "scratchpad-postinstall restores materialized baseline (US-0073)" "[ -f \"$TMP/.cursor/scratchpad.md\" ]"
else
  assert_true "Installer (sh) exists" "false"
fi

# Upgrade mode test
UPGRADE_TMP="$ROOT/tests/.tmp-upgrade"
rm -rf "$UPGRADE_TMP"
mkdir -p "$UPGRADE_TMP"
write_bootstrap_pkg_json "$UPGRADE_TMP"

if [ -f "$ROOT/installer.sh" ]; then
  run_with_timeout sh "$ROOT/installer.sh" --target "$UPGRADE_TMP" --mode missing --create < /dev/null >/dev/null

  assert_true "Version file written on install (its_magic)" "[ -f \"$UPGRADE_TMP/its_magic/.its-magic-version\" ]"
  assert_true "Metadata README written on install (its_magic)" "[ -f \"$UPGRADE_TMP/its_magic/README.md\" ]"

  echo "# My Custom Vision" > "$UPGRADE_TMP/docs/product/vision.md"

  echo "modified-framework" > "$UPGRADE_TMP/.cursor/commands/intake.md"
  sed -i.bak 's/^TEST_COMMAND:.*/TEST_COMMAND: custom test command/' "$UPGRADE_TMP/docs/engineering/runbook.md" && rm -f "$UPGRADE_TMP/docs/engineering/runbook.md.bak"
  echo "modified-local-example-marker" > "$UPGRADE_TMP/.cursor/scratchpad.local.example.md"
  echo "user-local-marker=keep" > "$UPGRADE_TMP/.cursor/scratchpad.local.md"

  run_with_timeout sh "$ROOT/installer.sh" --target "$UPGRADE_TMP" --mode upgrade < /dev/null >/dev/null

  assert_true "Upgrade restores framework files" "! grep -q 'modified-framework' \"$UPGRADE_TMP/.cursor/commands/intake.md\""
  assert_true "Upgrade preserves user data" "grep -q 'My Custom Vision' \"$UPGRADE_TMP/docs/product/vision.md\""
  assert_true "Upgrade refreshes scratchpad local example" "! grep -q 'modified-local-example-marker' \"$UPGRADE_TMP/.cursor/scratchpad.local.example.md\" && grep -q 'RELEASE_PUBLISH_MODE=confirm' \"$UPGRADE_TMP/.cursor/scratchpad.local.example.md\""
  assert_true "Upgrade preserves user scratchpad local overrides" "grep -q 'user-local-marker=keep' \"$UPGRADE_TMP/.cursor/scratchpad.local.md\""
  assert_true "Upgrade leaves materialized scratchpad baseline present (US-0073)" "[ -f \"$UPGRADE_TMP/.cursor/scratchpad.md\" ]"
  assert_true "Upgrade baseline still documents AUTO_FLOW_MODE (US-0073)" "file_contains \"$UPGRADE_TMP/.cursor/scratchpad.md\" \"AUTO_FLOW_MODE=\""
  assert_true "Upgrade does not overwrite explicit user TEST_COMMAND" "file_contains \"$UPGRADE_TMP/docs/engineering/runbook.md\" \"TEST_COMMAND: custom test command\""
  assert_true "Version file updated after upgrade (its_magic)" "[ -f \"$UPGRADE_TMP/its_magic/.its-magic-version\" ]"
  assert_true "Legacy top-level version file migrated away on upgrade" "[ ! -f \"$UPGRADE_TMP/.its-magic-version\" ]"
fi

# Clean-repo safety test (direct installer path)
CLEAN_TMP="$ROOT/tests/.tmp-cleanrepo"
rm -rf "$CLEAN_TMP"
mkdir -p "$CLEAN_TMP"
write_bootstrap_pkg_json "$CLEAN_TMP"
if [ -f "$ROOT/installer.sh" ]; then
  run_with_timeout sh "$ROOT/installer.sh" --target "$CLEAN_TMP" --mode missing --create < /dev/null >/dev/null
  mkdir -p "$CLEAN_TMP/src"
  echo "non-framework marker" > "$CLEAN_TMP/src/keep.txt"
  run_with_timeout sh "$ROOT/installer.sh" --target "$CLEAN_TMP" --clean-repo --yes < /dev/null >/dev/null
  assert_true "Clean-repo removes framework artifacts (installer)" "[ ! -d \"$CLEAN_TMP/.cursor\" ] && [ ! -d \"$CLEAN_TMP/docs/engineering\" ] && [ ! -d \"$CLEAN_TMP/docs/user-guides\" ] && [ ! -f \"$CLEAN_TMP/scripts/validate-and-push.ps1\" ] && [ ! -f \"$CLEAN_TMP/scripts/validate-and-push.sh\" ] && [ ! -f \"$CLEAN_TMP/.github/workflows/ci.yml\" ] && [ ! -f \"$CLEAN_TMP/.github/workflows/deploy.yml\" ] && [ ! -d \"$CLEAN_TMP/its_magic\" ] && [ ! -f \"$CLEAN_TMP/.its-magic-version\" ]"
  assert_true "Clean-repo preserves non-framework marker (installer)" "[ -f \"$CLEAN_TMP/src/keep.txt\" ]"
fi

# CLI lifecycle tests (`its-magic` command path)
CLI_ENTRY="$ROOT/bin/its-magic.js"
CLI_TMP="$ROOT/tests/.tmp-cli-lifecycle"
rm -rf "$CLI_TMP"
mkdir -p "$CLI_TMP"
write_bootstrap_pkg_json "$CLI_TMP"
if [ -f "$CLI_ENTRY" ] && command -v node >/dev/null 2>&1; then
  run_with_timeout node "$CLI_ENTRY" --target "$CLI_TMP" --mode missing --create < /dev/null >/dev/null
  assert_true "CLI missing install writes version file (its_magic)" "[ -f \"$CLI_TMP/its_magic/.its-magic-version\" ]"
  assert_true "CLI missing install writes metadata README (its_magic)" "[ -f \"$CLI_TMP/its_magic/README.md\" ]"
  assert_true "CLI missing install runbook TEST_COMMAND present" "grep -qE '^TEST_COMMAND:[[:space:]]*(npm run test|sh tests/run-tests\\.sh)' \"$CLI_TMP/docs/engineering/runbook.md\""
  assert_true "CLI missing install mirrors root README into its_magic README" "file_contains \"$CLI_TMP/its_magic/README.md\" \"US-0015 intent contract\""
  assert_true "CLI missing install writes command file" "[ -f \"$CLI_TMP/.cursor/commands/intake.md\" ]"
  assert_true "CLI missing install materializes scratchpad baseline (US-0073)" "[ -f \"$CLI_TMP/.cursor/scratchpad.md\" ]"
  assert_true "CLI missing install writes ownership manifest" "[ -f \"$CLI_TMP/docs/engineering/context/installer-owned-paths.manifest\" ]"
  assert_true "CLI missing install status-normalization report is neutral" "file_contains \"$CLI_TMP/docs/engineering/status-normalization-report.md\" \"(none yet)\""
  assert_true "CLI missing install research has no DEC-0011 reference" "! grep -q 'DEC-0011' \"$CLI_TMP/docs/engineering/research.md\""

  echo "cli-overwrite-marker" > "$CLI_TMP/.cursor/commands/intake.md"
  run_with_timeout node "$CLI_ENTRY" --target "$CLI_TMP" --mode overwrite --backup < /dev/null >/dev/null
  assert_true "CLI overwrite mode creates backup snapshot" "ls \"$CLI_TMP/backups\"/*/.cursor/commands/intake.md >/dev/null 2>&1"

  echo "# CLI User Data Marker" > "$CLI_TMP/docs/product/vision.md"
  echo "cli-upgrade-framework-marker" > "$CLI_TMP/.cursor/commands/intake.md"
  echo "cli-modified-local-example-marker" > "$CLI_TMP/.cursor/scratchpad.local.example.md"
  echo "cli-local-marker=keep" > "$CLI_TMP/.cursor/scratchpad.local.md"
  run_with_timeout node "$CLI_ENTRY" --target "$CLI_TMP" --mode upgrade < /dev/null >/dev/null
  assert_true "CLI upgrade restores framework files" "! grep -q 'cli-upgrade-framework-marker' \"$CLI_TMP/.cursor/commands/intake.md\""
  assert_true "CLI upgrade preserves user data" "grep -q 'CLI User Data Marker' \"$CLI_TMP/docs/product/vision.md\""
  assert_true "CLI upgrade refreshes scratchpad local example" "! grep -q 'cli-modified-local-example-marker' \"$CLI_TMP/.cursor/scratchpad.local.example.md\" && grep -q 'RELEASE_PUBLISH_MODE=confirm' \"$CLI_TMP/.cursor/scratchpad.local.example.md\""
  assert_true "CLI upgrade preserves user scratchpad local overrides" "grep -q 'cli-local-marker=keep' \"$CLI_TMP/.cursor/scratchpad.local.md\""

  mkdir -p "$CLI_TMP/src"
  echo "cli-marker" > "$CLI_TMP/src/keep.txt"
  run_with_timeout node "$CLI_ENTRY" --clean-repo --target "$CLI_TMP" --yes < /dev/null >/dev/null
  assert_true "CLI clean-repo removes framework artifacts" "[ ! -d \"$CLI_TMP/.cursor\" ] && [ ! -d \"$CLI_TMP/docs/engineering\" ] && [ ! -d \"$CLI_TMP/docs/user-guides\" ] && [ ! -f \"$CLI_TMP/scripts/validate-and-push.ps1\" ] && [ ! -f \"$CLI_TMP/scripts/validate-and-push.sh\" ] && [ ! -f \"$CLI_TMP/.github/workflows/ci.yml\" ] && [ ! -f \"$CLI_TMP/.github/workflows/deploy.yml\" ] && [ ! -d \"$CLI_TMP/its_magic\" ] && [ ! -f \"$CLI_TMP/.its-magic-version\" ]"
  assert_true "CLI clean-repo preserves non-framework marker" "[ -f \"$CLI_TMP/src/keep.txt\" ]"

  set +e
  node "$CLI_ENTRY" --target "$CLI_TMP" --mode invalid-mode >/dev/null 2>&1
  INVALID_EXIT=$?
  set -e
  assert_true "CLI invalid mode fails fast" "[ $INVALID_EXIT -ne 0 ]"
else
  assert_true "CLI lifecycle preconditions (node + bin/its-magic.js)" "false"
fi

rm -rf "$TMP" "$UPGRADE_TMP"
rm -rf "$CLEAN_TMP" "$CLI_TMP"

# Memory-audit command checks (US-0024)
assert_true "memory-audit command exists (active)" "[ -f \"$ROOT/.cursor/commands/memory-audit.md\" ]"
assert_true "memory-audit command exists (template)" "[ -f \"$TPL/.cursor/commands/memory-audit.md\" ]"
assert_true "Runbook documents US-0015 intentional empty commands (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"Intentional empty commands (US-0015)\""
assert_true "Runbook documents OS-aware bootstrap contract (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"OS-aware runbook command bootstrap (US-0063 / DEC-0046)\""
assert_true "README documents US-0015 intent contract (active)" "file_contains \"$ROOT/README.md\" \"US-0015 intent contract\""

assert_true "README mentions memory-audit timing (active)" "file_contains \"$ROOT/README.md\" \"Pre-handoff\""
assert_true "README mentions memory-audit timing (template)" "file_contains \"$TPL/README.md\" \"Pre-handoff\""

assert_true "Runbook mentions memory-audit timing" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"Pre-handoff\""

assert_true "memory-audit routes template drift to US-0017 (active)" "file_contains \"$ROOT/.cursor/commands/memory-audit.md\" \"US-0017\""
assert_true "memory-audit routes template drift to US-0017 (template)" "file_contains \"$TPL/.cursor/commands/memory-audit.md\" \"US-0017\""

assert_true "memory-audit scope boundary section exists (active)" "file_contains \"$ROOT/.cursor/commands/memory-audit.md\" \"Scope boundary: US-0024 vs US-0017\""
assert_true "memory-audit scope boundary section exists (template)" "file_contains \"$TPL/.cursor/commands/memory-audit.md\" \"Scope boundary: US-0024 vs US-0017\""

# Remote config contract checks (US-0036)
assert_true "remote.json exists (active)" "[ -f \"$ROOT/.cursor/remote.json\" ]"
assert_true "remote.json exists (template)" "[ -f \"$TPL/.cursor/remote.json\" ]"

assert_true "remote.json schema includes version (active)" "file_contains \"$ROOT/.cursor/remote.json\" '\"version\"'"
assert_true "remote.json schema includes defaultTarget (active)" "file_contains \"$ROOT/.cursor/remote.json\" '\"defaultTarget\"'"
assert_true "remote.json schema includes targets (active)" "file_contains \"$ROOT/.cursor/remote.json\" '\"targets\"'"
assert_true "remote.json includes local docker example (active)" "file_contains \"$ROOT/.cursor/remote.json\" '\"local-docker\"'"
assert_true "remote.json includes remote vm/ssh example (active)" "file_contains \"$ROOT/.cursor/remote.json\" '\"remote-vm-ssh\"'"

assert_true "remote.json schema includes version (template)" "file_contains \"$TPL/.cursor/remote.json\" '\"version\"'"
assert_true "remote.json schema includes defaultTarget (template)" "file_contains \"$TPL/.cursor/remote.json\" '\"defaultTarget\"'"
assert_true "remote.json schema includes targets (template)" "file_contains \"$TPL/.cursor/remote.json\" '\"targets\"'"

assert_true "README documents remote mode-aware behavior (active)" "file_contains \"$ROOT/README.md\" \"REMOTE_EXECUTION=0\""
assert_true "README documents remote mode-aware behavior (template)" "file_contains \"$TPL/README.md\" \"REMOTE_EXECUTION=0\""
assert_true "Runbook documents remote fail-fast format (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"[REMOTE_CONFIG_ERROR]\""
assert_true "Runbook documents remote fail-fast format (template)" "file_contains \"$TPL/docs/engineering/runbook.md\" \"[REMOTE_CONFIG_ERROR]\""

assert_true "execute command has remote fail-fast guidance (active)" "file_contains \"$ROOT/.cursor/commands/execute.md\" \"REMOTE_CONFIG_ERROR\""
assert_true "execute command has remote fail-fast guidance (template)" "file_contains \"$TPL/.cursor/commands/execute.md\" \"REMOTE_CONFIG_ERROR\""
assert_true "execute command includes disabled-mode skip guidance (active)" "file_contains \"$ROOT/.cursor/commands/execute.md\" \"REMOTE_EXECUTION=0\""
assert_true "execute command includes disabled-mode skip guidance (template)" "file_contains \"$TPL/.cursor/commands/execute.md\" \"REMOTE_EXECUTION=0\""

assert_true "runbook lists negative path: missing config" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"Missing config file\""
assert_true "runbook lists negative path: malformed JSON" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"Malformed JSON\""
assert_true "runbook lists negative path: invalid value or enum" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"Invalid value or enum\""
assert_true "runbook lists negative path: security violation" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"Security violation\""

assert_true "execute command documents runtime autopilot stage chain (active)" "file_contains \"$ROOT/.cursor/commands/execute.md\" \"startup -> readiness/connectivity -> log scan -> bounded retry -> verdict\""
assert_true "execute command documents runtime autopilot stage chain (template)" "file_contains \"$TPL/.cursor/commands/execute.md\" \"startup -> readiness/connectivity -> log scan -> bounded retry -> verdict\""
assert_true "qa command defines RUNTIME_STARTUP_FAILED (active)" "file_contains \"$ROOT/.cursor/commands/qa.md\" \"RUNTIME_STARTUP_FAILED\""
assert_true "qa command defines RUNTIME_RETRY_BUDGET_EXHAUSTED (active)" "file_contains \"$ROOT/.cursor/commands/qa.md\" \"RUNTIME_RETRY_BUDGET_EXHAUSTED\""
assert_true "qa command defines RUNTIME_STACK_PROFILE_UNRESOLVED (template)" "file_contains \"$TPL/.cursor/commands/qa.md\" \"RUNTIME_STACK_PROFILE_UNRESOLVED\""
assert_true "runbook documents runtime QA autopilot contract (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"Runtime QA autopilot contract (US-0065 / DEC-0047)\""
assert_true "runbook documents runtime QA autopilot contract (template)" "file_contains \"$TPL/docs/engineering/runbook.md\" \"Runtime QA autopilot contract (US-0065 / DEC-0047)\""
assert_true "README documents runtime QA autopilot behavior (active)" "file_contains \"$ROOT/README.md\" \"Runtime QA autopilot behavior (US-0065)\""
assert_true "README documents runtime QA autopilot behavior (template)" "file_contains \"$TPL/README.md\" \"Runtime QA autopilot behavior (US-0065)\""
assert_true "quality rule includes runtime deterministic reason codes (active)" "file_contains \"$ROOT/.cursor/rules/quality.mdc\" \"RUNTIME_LOG_CRITICAL_DETECTED\""
assert_true "quality rule includes runtime deterministic reason codes (template)" "file_contains \"$TPL/.cursor/rules/quality.mdc\" \"RUNTIME_LOG_CRITICAL_DETECTED\""
assert_true "execute command documents generated scaffold contract (active)" "file_contains \"$ROOT/.cursor/commands/execute.md\" \"Generated baseline test scaffolding contract (US-0066 / DEC-0048)\""
assert_true "execute command documents generated scaffold contract (template)" "file_contains \"$TPL/.cursor/commands/execute.md\" \"Generated baseline test scaffolding contract (US-0066 / DEC-0048)\""
assert_true "qa command documents generated test auto-run contract (active)" "file_contains \"$ROOT/.cursor/commands/qa.md\" \"Generated baseline test auto-run contract (US-0066 / DEC-0048)\""
assert_true "qa command documents generated test auto-run contract (template)" "file_contains \"$TPL/.cursor/commands/qa.md\" \"Generated baseline test auto-run contract (US-0066 / DEC-0048)\""
assert_true "runbook documents generated test scaffolding contract (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"Generated test scaffolding + auto-run contract (US-0066 / DEC-0048)\""
assert_true "runbook documents generated test scaffolding contract (template)" "file_contains \"$TPL/docs/engineering/runbook.md\" \"Generated test scaffolding + auto-run contract (US-0066 / DEC-0048)\""
assert_true "README documents generated test scaffolding behavior (active)" "file_contains \"$ROOT/README.md\" \"Generated test scaffolding + auto-run behavior (US-0066)\""
assert_true "README documents generated test scaffolding behavior (template)" "file_contains \"$TPL/README.md\" \"Generated test scaffolding + auto-run behavior (US-0066)\""
assert_true "verify-work includes generated-test readiness gate (active)" "file_contains \"$ROOT/.cursor/commands/verify-work.md\" \"Generated-test readiness evidence gate (US-0066 / DEC-0048)\""
assert_true "verify-work includes generated-test readiness gate (template)" "file_contains \"$TPL/.cursor/commands/verify-work.md\" \"Generated-test readiness evidence gate (US-0066 / DEC-0048)\""
assert_true "release includes generated-test evidence prerequisite (active)" "file_contains \"$ROOT/.cursor/commands/release.md\" \"Generated-test evidence prerequisite (US-0066 / DEC-0048)\""
assert_true "release includes generated-test evidence prerequisite (template)" "file_contains \"$TPL/.cursor/commands/release.md\" \"Generated-test evidence prerequisite (US-0066 / DEC-0048)\""
assert_true "release includes scaffold fail code TEST_SCAFFOLD_GENERATION_FAILED (active)" "file_contains \"$ROOT/.cursor/commands/release.md\" \"TEST_SCAFFOLD_GENERATION_FAILED\""
assert_true "release includes scaffold fail code TEST_SCAFFOLD_GENERATION_FAILED (template)" "file_contains \"$TPL/.cursor/commands/release.md\" \"TEST_SCAFFOLD_GENERATION_FAILED\""
assert_true "intake command documents mandatory question packs contract (active)" "file_contains \"$ROOT/.cursor/commands/intake.md\" \"Mandatory intake question packs and fail-closed persistence gate (US-0068 / DEC-0050)\""
assert_true "intake command documents mandatory question packs contract (template)" "file_contains \"$TPL/.cursor/commands/intake.md\" \"Mandatory intake question packs and fail-closed persistence gate (US-0068 / DEC-0050)\""
assert_true "po agent includes first-intake-pack guidance (active)" "file_contains \"$ROOT/.cursor/agents/po.mdc\" \"first-intake-pack\""
assert_true "po agent includes small-intake-pack guidance (template)" "file_contains \"$TPL/.cursor/agents/po.mdc\" \"small-intake-pack\""
assert_true "runbook documents mandatory intake question packs section (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"Mandatory intake question packs and persistence coverage gate (US-0068 / DEC-0050)\""
assert_true "runbook documents mandatory intake question packs section (template)" "file_contains \"$TPL/docs/engineering/runbook.md\" \"Mandatory intake question packs and persistence coverage gate (US-0068 / DEC-0050)\""
assert_true "README documents US-0068 intake pack behavior (active)" "file_contains \"$ROOT/README.md\" \"Mandatory intake question packs (US-0068)\""
assert_true "README documents US-0068 intake pack behavior (template)" "file_contains \"$TPL/README.md\" \"Mandatory intake question packs (US-0068)\""
assert_true "intake command includes deterministic fail code INTAKE_PERSISTENCE_BLOCKED (active)" "file_contains \"$ROOT/.cursor/commands/intake.md\" \"INTAKE_PERSISTENCE_BLOCKED\""
assert_true "intake command includes deterministic evidence field asked_topics (template)" "file_contains \"$TPL/.cursor/commands/intake.md\" \"asked_topics\""
assert_true "intake command documents US-0078 interactive evidence gate (active)" "file_contains \"$ROOT/.cursor/commands/intake.md\" \"Interactive intake evidence gate (US-0078 / DEC-0060 / R-0055)\""
assert_true "intake command documents US-0078 interactive evidence gate (template)" "file_contains \"$TPL/.cursor/commands/intake.md\" \"Interactive intake evidence gate (US-0078 / DEC-0060 / R-0055)\""
assert_true "intake command documents same pre-persistence validation pipeline guided and low-touch (active)" "file_contains \"$ROOT/.cursor/commands/intake.md\" \"same pre-persistence validation pipeline\""
assert_true "intake command documents same pre-persistence validation pipeline guided and low-touch (template)" "file_contains \"$TPL/.cursor/commands/intake.md\" \"same pre-persistence validation pipeline\""
assert_true "intake command documents bug issue routing US-0079 DEC-0061 (active)" "file_contains \"$ROOT/.cursor/commands/intake.md\" \"Bug issue routing (US-0079 / DEC-0061)\""
assert_true "intake command documents bug issue routing US-0079 DEC-0061 (template)" "file_contains \"$TPL/.cursor/commands/intake.md\" \"Bug issue routing (US-0079 / DEC-0061)\""
assert_true "runbook documents interactive intake evidence validation section (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"Interactive intake evidence validation (US-0078 / DEC-0060)\""
assert_true "runbook documents interactive intake evidence validation section (template)" "file_contains \"$TPL/docs/engineering/runbook.md\" \"Interactive intake evidence validation (US-0078 / DEC-0060)\""
assert_true "README documents US-0078 intake evidence validator (active)" "file_contains \"$ROOT/README.md\" \"Interactive intake evidence + validator (US-0078 / DEC-0060)\""
assert_true "README documents US-0078 intake evidence validator (template)" "file_contains \"$TPL/README.md\" \"Interactive intake evidence + validator (US-0078 / DEC-0060)\""
assert_true "README documents bug issues US-0079 DEC-0061 (active)" "file_contains \"$ROOT/README.md\" \"Bug issues + intake routing (US-0079 / DEC-0061)\""
assert_true "README documents bug issues US-0079 DEC-0061 (template)" "file_contains \"$TPL/README.md\" \"Bug issues + intake routing (US-0079 / DEC-0061)\""
assert_true "runbook documents bug issues US-0079 section (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"Bug issues (US-0079 / DEC-0061)\""
assert_true "runbook documents bug issues US-0079 section (template)" "file_contains \"$TPL/docs/engineering/runbook.md\" \"Bug issues (US-0079 / DEC-0061)\""

# Auto continuation deterministic contract checks (US-0037)
assert_true "auto includes explicit start-from contract (active)" "file_contains \"$ROOT/.cursor/commands/auto.md\" \"start-from=<phase>\""
assert_true "auto includes explicit start-from contract (template)" "file_contains \"$TPL/.cursor/commands/auto.md\" \"start-from=<phase>\""

assert_true "auto precedence includes argument > resume > state (active)" "file_contains \"$ROOT/.cursor/commands/auto.md\" \"Resolve start phase in strict order:\""
assert_true "auto precedence includes argument > resume > state (template)" "file_contains \"$TPL/.cursor/commands/auto.md\" \"Resolve start phase in strict order:\""

assert_true "auto requires fail-fast on stale resume brief (active)" "file_contains \"$ROOT/.cursor/commands/auto.md\" \"present but stale or unparseable, fail fast\""
assert_true "auto requires fail-fast on stale resume brief (template)" "file_contains \"$TPL/.cursor/commands/auto.md\" \"present but stale or unparseable, fail fast\""

assert_true "auto includes AUTO_RESUME_ERROR format (active)" "file_contains \"$ROOT/.cursor/commands/auto.md\" \"[AUTO_RESUME_ERROR] <code>: <summary>. Source=<source>. Fix: <action>.\""
assert_true "auto includes AUTO_RESUME_ERROR format (template)" "file_contains \"$TPL/.cursor/commands/auto.md\" \"[AUTO_RESUME_ERROR] <code>: <summary>. Source=<source>. Fix: <action>.\""

assert_true "auto includes required error code INVALID_START_FROM (active)" "file_contains \"$ROOT/.cursor/commands/auto.md\" \"INVALID_START_FROM\""
assert_true "auto includes required error code RESUME_STATE_CONFLICT (active)" "file_contains \"$ROOT/.cursor/commands/auto.md\" \"RESUME_STATE_CONFLICT\""
assert_true "auto includes required error code STATE_PHASE_UNRECOVERABLE (active)" "file_contains \"$ROOT/.cursor/commands/auto.md\" \"STATE_PHASE_UNRECOVERABLE\""
assert_true "auto includes required error code INVALID_START_FROM (template)" "file_contains \"$TPL/.cursor/commands/auto.md\" \"INVALID_START_FROM\""
assert_true "auto includes required error code RESUME_STATE_CONFLICT (template)" "file_contains \"$TPL/.cursor/commands/auto.md\" \"RESUME_STATE_CONFLICT\""
assert_true "auto includes required error code STATE_PHASE_UNRECOVERABLE (template)" "file_contains \"$TPL/.cursor/commands/auto.md\" \"STATE_PHASE_UNRECOVERABLE\""

assert_true "auto includes breadcrumb fields (active)" "file_contains \"$ROOT/.cursor/commands/auto.md\" \"resolution_source\""
assert_true "auto includes breadcrumb stop reason (active)" "file_contains \"$ROOT/.cursor/commands/auto.md\" \"stop_reason\""
assert_true "auto includes breadcrumb fields (template)" "file_contains \"$TPL/.cursor/commands/auto.md\" \"resolution_source\""
assert_true "auto includes breadcrumb stop reason (template)" "file_contains \"$TPL/.cursor/commands/auto.md\" \"stop_reason\""
assert_true "auto documents optional backlog-drain mode (active)" "file_contains \"$ROOT/.cursor/commands/auto.md\" \"Optional backlog-drain mode (US-0044 / DEC-0022)\""
assert_true "auto documents optional backlog-drain mode (template)" "file_contains \"$TPL/.cursor/commands/auto.md\" \"Optional backlog-drain mode (US-0044 / DEC-0022)\""
assert_true "auto includes backlog drain reason BACKLOG_MAX_STORIES_REACHED (active)" "file_contains \"$ROOT/.cursor/commands/auto.md\" \"BACKLOG_MAX_STORIES_REACHED\""
assert_true "auto includes backlog drain reason BACKLOG_MAX_STORIES_REACHED (template)" "file_contains \"$TPL/.cursor/commands/auto.md\" \"BACKLOG_MAX_STORIES_REACHED\""

assert_true "pause references AUTO_RESUME_ERROR contract (active)" "file_contains \"$ROOT/.cursor/commands/pause.md\" \"[AUTO_RESUME_ERROR]\""
assert_true "pause references AUTO_RESUME_ERROR contract (template)" "file_contains \"$TPL/.cursor/commands/pause.md\" \"[AUTO_RESUME_ERROR]\""

assert_true "resume references deterministic precedence guidance (active)" "file_contains \"$ROOT/.cursor/commands/resume.md\" \"argument > resume brief > state fallback\""
assert_true "resume references deterministic precedence guidance (template)" "file_contains \"$TPL/.cursor/commands/resume.md\" \"argument > resume brief > state fallback\""

assert_true "core rule defines DEC-0017 continuation contract (active)" "file_contains \"$ROOT/.cursor/rules/core.mdc\" \"DEC-0017\""
assert_true "core rule defines DEC-0017 continuation contract (template)" "file_contains \"$TPL/.cursor/rules/core.mdc\" \"DEC-0017\""
assert_true "core rule preserves stop conditions in continuation mode (active)" "file_contains \"$ROOT/.cursor/rules/core.mdc\" \"Preserve existing stop/gate controls in continuation mode\""
assert_true "core rule preserves stop conditions in continuation mode (template)" "file_contains \"$TPL/.cursor/rules/core.mdc\" \"Preserve existing stop/gate controls in continuation mode\""

# Sync policy guarded auto-push checks (US-0038)
assert_true "scratchpad includes SYNC_POLICY_MODE (active)" "file_contains \"$ROOT/.cursor/scratchpad.md\" \"SYNC_POLICY_MODE\""
assert_true "scratchpad includes SYNC_POLICY_MODE (template)" "file_contains \"$TPL/.cursor/scratchpad.md\" \"SYNC_POLICY_MODE\""
assert_true "scratchpad includes AUTO_PUSH_BRANCH_ALLOWLIST (active)" "file_contains \"$ROOT/.cursor/scratchpad.md\" \"AUTO_PUSH_BRANCH_ALLOWLIST\""
assert_true "scratchpad includes AUTO_PUSH_BRANCH_ALLOWLIST (template)" "file_contains \"$TPL/.cursor/scratchpad.md\" \"AUTO_PUSH_BRANCH_ALLOWLIST\""
assert_true "scratchpad includes AUTO_BACKLOG_DRAIN (active)" "file_contains \"$ROOT/.cursor/scratchpad.md\" \"AUTO_BACKLOG_DRAIN\""
assert_true "scratchpad includes AUTO_BACKLOG_DRAIN (template)" "file_contains \"$TPL/.cursor/scratchpad.md\" \"AUTO_BACKLOG_DRAIN\""
assert_true "scratchpad includes AUTO_BACKLOG_MAX_STORIES (active)" "file_contains \"$ROOT/.cursor/scratchpad.md\" \"AUTO_BACKLOG_MAX_STORIES\""
assert_true "scratchpad includes AUTO_BACKLOG_MAX_STORIES (template)" "file_contains \"$TPL/.cursor/scratchpad.md\" \"AUTO_BACKLOG_MAX_STORIES\""

assert_true "auto command documents guarded eligibility chain (active)" "file_contains \"$ROOT/.cursor/commands/auto.md\" \"Guarded auto-push eligibility chain\""
assert_true "auto command documents guarded eligibility chain (template)" "file_contains \"$TPL/.cursor/commands/auto.md\" \"Guarded auto-push eligibility chain\""
assert_true "auto command includes BRANCH_NOT_ALLOWLISTED reason code (active)" "file_contains \"$ROOT/.cursor/commands/auto.md\" \"BRANCH_NOT_ALLOWLISTED\""
assert_true "auto command includes BRANCH_NOT_ALLOWLISTED reason code (template)" "file_contains \"$TPL/.cursor/commands/auto.md\" \"BRANCH_NOT_ALLOWLISTED\""
assert_true "runbook documents sync reason code TEST_TIMEOUT (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"TEST_TIMEOUT\""
assert_true "runbook documents sync reason code TEST_TIMEOUT (template)" "file_contains \"$TPL/docs/engineering/runbook.md\" \"TEST_TIMEOUT\""

assert_true "validate-and-push.ps1 requires TEST_COMMAND" "file_contains \"$ROOT/scripts/validate-and-push.ps1\" \"TEST_COMMAND is required by sync policy\""
assert_true "validate-and-push.sh requires TEST_COMMAND" "file_contains \"$ROOT/scripts/validate-and-push.sh\" \"TEST_COMMAND is required by sync policy\""
assert_true "validate-and-push.ps1 supports optional TYPECHECK_COMMAND" "file_contains \"$ROOT/scripts/validate-and-push.ps1\" \"TYPECHECK_COMMAND\""
assert_true "validate-and-push.sh supports optional TYPECHECK_COMMAND" "file_contains \"$ROOT/scripts/validate-and-push.sh\" \"TYPECHECK_COMMAND\""

# 13) Release queue + per-sprint notes contract checks (US-0040)
assert_true "release queue artifact exists (active)" "[ -f \"$ROOT/handoffs/release_queue.md\" ]"
assert_true "release queue artifact exists (template)" "[ -f \"$TPL/handoffs/release_queue.md\" ]"
assert_true "sprint notes template exists (active)" "[ -f \"$ROOT/handoffs/releases/Sxxxx-release-notes.md\" ]"
assert_true "sprint notes template exists (template)" "[ -f \"$TPL/handoffs/releases/Sxxxx-release-notes.md\" ]"

assert_true "release command references sprint-scoped canonical notes path (active)" "file_contains \"$ROOT/.cursor/commands/release.md\" \"handoffs/releases/Sxxxx-release-notes.md\""
assert_true "release command references sprint-scoped canonical notes path (template)" "file_contains \"$TPL/.cursor/commands/release.md\" \"handoffs/releases/Sxxxx-release-notes.md\""
assert_true "release command references canonical queue artifact (active)" "file_contains \"$ROOT/.cursor/commands/release.md\" \"handoffs/release_queue.md\""
assert_true "release command references canonical queue artifact (template)" "file_contains \"$TPL/.cursor/commands/release.md\" \"handoffs/release_queue.md\""

assert_true "release command enforces target sprint only mutation (active)" "file_contains \"$ROOT/.cursor/commands/release.md\" \"only the target sprint row may\""
assert_true "release command enforces target sprint only mutation (template)" "file_contains \"$TPL/.cursor/commands/release.md\" \"only the target sprint row may\""
assert_true "release command defines unresolved sprint fail-safe (active)" "file_contains \"$ROOT/.cursor/commands/release.md\" \"RELEASE_SPRINT_UNRESOLVED\""
assert_true "release command defines unresolved sprint fail-safe (template)" "file_contains \"$TPL/.cursor/commands/release.md\" \"RELEASE_SPRINT_UNRESOLVED\""
assert_true "release command defines mismatch reason code QUEUE_ENTRY_MISSING (active)" "file_contains \"$ROOT/.cursor/commands/release.md\" \"QUEUE_ENTRY_MISSING\""
assert_true "release command defines mismatch reason code NOTES_REF_MISSING (active)" "file_contains \"$ROOT/.cursor/commands/release.md\" \"NOTES_REF_MISSING\""
assert_true "release command defines mismatch reason code STATUS_TRANSITION_INVALID (active)" "file_contains \"$ROOT/.cursor/commands/release.md\" \"STATUS_TRANSITION_INVALID\""
assert_true "release command defines legacy unresolved migration reason code (active)" "file_contains \"$ROOT/.cursor/commands/release.md\" \"LEGACY_NOTES_SPRINT_UNRESOLVED\""
assert_true "release command defines legacy unresolved migration reason code (template)" "file_contains \"$TPL/.cursor/commands/release.md\" \"LEGACY_NOTES_SPRINT_UNRESOLVED\""

assert_true "legacy release notes file documents pointer compatibility (active)" "file_contains \"$ROOT/handoffs/release_notes.md\" \"Legacy Compatibility Pointer\""
assert_true "legacy release notes file references queue visibility (active)" "file_contains \"$ROOT/handoffs/release_notes.md\" \"handoffs/release_queue.md\""
assert_true "legacy release notes file documents pointer compatibility (template)" "file_contains \"$TPL/handoffs/release_notes.md\" \"Legacy Compatibility Pointer\""
assert_true "legacy release notes file references queue visibility (template)" "file_contains \"$TPL/handoffs/release_notes.md\" \"handoffs/release_queue.md\""

assert_true "runbook documents release queue contract (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"Release queue and sprint notes contract\""
assert_true "runbook documents release queue contract (template)" "file_contains \"$TPL/docs/engineering/runbook.md\" \"Release queue and sprint notes contract\""
assert_true "README documents US-0040 release notes model (active)" "file_contains \"$ROOT/README.md\" \"Release notes model (US-0040)\""
assert_true "README documents US-0040 release notes model (template)" "file_contains \"$TPL/README.md\" \"Release notes model (US-0040)\""

# 16) Post-QA release findings workflow checks (US-0042)
assert_true "release command references release findings artifact (active)" "file_contains \"$ROOT/.cursor/commands/release.md\" \"sprints/Sxxxx/release-findings.md\""
assert_true "release command references release findings artifact (template)" "file_contains \"$TPL/.cursor/commands/release.md\" \"sprints/Sxxxx/release-findings.md\""
assert_true "release command references release_to_dev handoff (active)" "file_contains \"$ROOT/.cursor/commands/release.md\" \"handoffs/release_to_dev.md\""
assert_true "release command references release_to_dev handoff (template)" "file_contains \"$TPL/.cursor/commands/release.md\" \"handoffs/release_to_dev.md\""
assert_true "release command includes RELEASE_TEST_FAILED (active)" "file_contains \"$ROOT/.cursor/commands/release.md\" \"RELEASE_TEST_FAILED\""
assert_true "release command includes RELEASE_TEST_FAILED (template)" "file_contains \"$TPL/.cursor/commands/release.md\" \"RELEASE_TEST_FAILED\""
assert_true "release_to_dev handoff exists (active)" "[ -f \"$ROOT/handoffs/release_to_dev.md\" ]"
assert_true "release_to_dev handoff exists (template)" "[ -f \"$TPL/handoffs/release_to_dev.md\" ]"
assert_true "release findings template exists (template)" "[ -f \"$TPL/sprints/S0001/release-findings.md\" ]"
assert_true "runbook documents post-QA release issue workflow (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"Post-QA release issue workflow (US-0042)\""
assert_true "runbook documents post-QA release issue workflow (template)" "file_contains \"$TPL/docs/engineering/runbook.md\" \"Post-QA release issue workflow (US-0042)\""
assert_true "README documents post-QA release issue workflow (active)" "file_contains \"$ROOT/README.md\" \"Post-QA release issue workflow (US-0042)\""
assert_true "README documents post-QA release issue workflow (template)" "file_contains \"$TPL/README.md\" \"Post-QA release issue workflow (US-0042)\""

# 17) Backlog reconciliation invariant checks (US-0043)
assert_true "release command documents backlog reconciliation contract (active)" "file_contains \"$ROOT/.cursor/commands/release.md\" \"Backlog reconciliation contract (US-0043 / DEC-0021)\""
assert_true "release command documents backlog reconciliation contract (template)" "file_contains \"$TPL/.cursor/commands/release.md\" \"Backlog reconciliation contract (US-0043 / DEC-0021)\""
assert_true "release command includes drift reason code BACKLOG_STATUS_DRIFT (active)" "file_contains \"$ROOT/.cursor/commands/release.md\" \"BACKLOG_STATUS_DRIFT\""
assert_true "release command includes drift reason code BACKLOG_STATUS_DRIFT (template)" "file_contains \"$TPL/.cursor/commands/release.md\" \"BACKLOG_STATUS_DRIFT\""
assert_true "runbook documents backlog reconciliation invariant (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"Backlog reconciliation invariant (US-0043)\""
assert_true "runbook documents backlog reconciliation invariant (template)" "file_contains \"$TPL/docs/engineering/runbook.md\" \"Backlog reconciliation invariant (US-0043)\""
assert_true "README documents backlog reconciliation invariant (active)" "file_contains \"$ROOT/README.md\" \"Backlog reconciliation invariant (US-0043)\""
assert_true "README documents backlog reconciliation invariant (template)" "file_contains \"$TPL/README.md\" \"Backlog reconciliation invariant (US-0043)\""
assert_true "runbook documents optional backlog-drain auto mode (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"Optional backlog-drain auto mode (US-0044)\""
assert_true "runbook documents optional backlog-drain auto mode (template)" "file_contains \"$TPL/docs/engineering/runbook.md\" \"Optional backlog-drain auto mode (US-0044)\""
assert_true "README documents optional backlog-drain auto mode (active)" "file_contains \"$ROOT/README.md\" \"backlog-drain mode (US-0044)\""
assert_true "README documents optional backlog-drain auto mode (template)" "file_contains \"$TPL/README.md\" \"backlog-drain mode (US-0044)\""

# 18) Explicit bulk sprint planning checks (US-0046)
assert_true "sprint-plan supports explicit --bulk trigger (active)" "file_contains \"$ROOT/.cursor/commands/sprint-plan.md\" \"--bulk\""
assert_true "sprint-plan supports explicit --bulk trigger (template)" "file_contains \"$TPL/.cursor/commands/sprint-plan.md\" \"--bulk\""
assert_true "sprint-plan documents SPRINT_BULK_MAX_STORIES (active)" "file_contains \"$ROOT/.cursor/commands/sprint-plan.md\" \"SPRINT_BULK_MAX_STORIES\""
assert_true "sprint-plan documents SPRINT_BULK_MAX_STORIES (template)" "file_contains \"$TPL/.cursor/commands/sprint-plan.md\" \"SPRINT_BULK_MAX_STORIES\""
assert_true "sprint-plan includes bounded bulk stop reason (active)" "file_contains \"$ROOT/.cursor/commands/sprint-plan.md\" \"SPRINT_BULK_MAX_SPRINTS_REACHED\""
assert_true "sprint-plan includes bounded bulk stop reason (template)" "file_contains \"$TPL/.cursor/commands/sprint-plan.md\" \"SPRINT_BULK_MAX_SPRINTS_REACHED\""

assert_true "scratchpad includes SPRINT_BULK_MAX_STORIES (active)" "file_contains \"$ROOT/.cursor/scratchpad.md\" \"SPRINT_BULK_MAX_STORIES\""
assert_true "scratchpad includes SPRINT_BULK_MAX_STORIES (template)" "file_contains \"$TPL/.cursor/scratchpad.md\" \"SPRINT_BULK_MAX_STORIES\""
assert_true "scratchpad includes SPRINT_BULK_MAX_SPRINTS (active)" "file_contains \"$ROOT/.cursor/scratchpad.md\" \"SPRINT_BULK_MAX_SPRINTS\""
assert_true "scratchpad includes SPRINT_BULK_MAX_SPRINTS (template)" "file_contains \"$TPL/.cursor/scratchpad.md\" \"SPRINT_BULK_MAX_SPRINTS\""

assert_true "runbook documents explicit bulk sprint planning mode (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"Explicit bulk sprint planning mode (US-0046)\""
assert_true "runbook documents explicit bulk sprint planning mode (template)" "file_contains \"$TPL/docs/engineering/runbook.md\" \"Explicit bulk sprint planning mode (US-0046)\""
assert_true "README documents explicit sprint-plan bulk mode (active)" "file_contains \"$ROOT/README.md\" \"sprint-plan --bulk\""
assert_true "README documents explicit sprint-plan bulk mode (template)" "file_contains \"$TPL/README.md\" \"sprint-plan --bulk\""

# 19) Explicit bulk execute orchestration checks (US-0047)
assert_true "auto command documents explicit --execute-bulk argument (active)" "file_contains \"$ROOT/.cursor/commands/auto.md\" \"--execute-bulk\""
assert_true "auto command documents explicit --execute-bulk argument (template)" "file_contains \"$TPL/.cursor/commands/auto.md\" \"--execute-bulk\""
assert_true "auto command documents AUTO_EXECUTE_BULK control (active)" "file_contains \"$ROOT/.cursor/commands/auto.md\" \"AUTO_EXECUTE_BULK\""
assert_true "auto command documents AUTO_EXECUTE_BULK control (template)" "file_contains \"$TPL/.cursor/commands/auto.md\" \"AUTO_EXECUTE_BULK\""
assert_true "auto command includes EXEC_BULK_MAX_ITEMS_REACHED reason code (active)" "file_contains \"$ROOT/.cursor/commands/auto.md\" \"EXEC_BULK_MAX_ITEMS_REACHED\""
assert_true "auto command includes EXEC_TEAM_SCOPE_BLOCKED reason code (active)" "file_contains \"$ROOT/.cursor/commands/auto.md\" \"EXEC_TEAM_SCOPE_BLOCKED\""
assert_true "auto command includes EXEC_BULK_MAX_ITEMS_REACHED reason code (template)" "file_contains \"$TPL/.cursor/commands/auto.md\" \"EXEC_BULK_MAX_ITEMS_REACHED\""
assert_true "auto command includes EXEC_TEAM_SCOPE_BLOCKED reason code (template)" "file_contains \"$TPL/.cursor/commands/auto.md\" \"EXEC_TEAM_SCOPE_BLOCKED\""

assert_true "scratchpad includes AUTO_EXECUTE_BULK (active)" "file_contains \"$ROOT/.cursor/scratchpad.md\" \"AUTO_EXECUTE_BULK\""
assert_true "scratchpad includes AUTO_EXECUTE_BULK (template)" "file_contains \"$TPL/.cursor/scratchpad.md\" \"AUTO_EXECUTE_BULK\""
assert_true "scratchpad includes AUTO_EXECUTE_MAX_ITEMS (active)" "file_contains \"$ROOT/.cursor/scratchpad.md\" \"AUTO_EXECUTE_MAX_ITEMS\""
assert_true "scratchpad includes AUTO_EXECUTE_MAX_ITEMS (template)" "file_contains \"$TPL/.cursor/scratchpad.md\" \"AUTO_EXECUTE_MAX_ITEMS\""
assert_true "scratchpad includes AUTO_TEAM_SCOPE_ENFORCE (active)" "file_contains \"$ROOT/.cursor/scratchpad.md\" \"AUTO_TEAM_SCOPE_ENFORCE\""
assert_true "scratchpad includes AUTO_TEAM_SCOPE_ENFORCE (template)" "file_contains \"$TPL/.cursor/scratchpad.md\" \"AUTO_TEAM_SCOPE_ENFORCE\""

assert_true "runbook documents explicit bulk execute mode (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"Explicit bulk execute mode (US-0047)\""
assert_true "runbook documents explicit bulk execute mode (template)" "file_contains \"$TPL/docs/engineering/runbook.md\" \"Explicit bulk execute mode (US-0047)\""
assert_true "README documents explicit auto execute bulk mode (active)" "file_contains \"$ROOT/README.md\" \"auto --execute-bulk\""
assert_true "README documents explicit auto execute bulk mode (template)" "file_contains \"$TPL/README.md\" \"auto --execute-bulk\""

assert_true "execute command documents team-scope guardrails (active)" "file_contains \"$ROOT/.cursor/commands/execute.md\" \"Team-scope guardrails for bulk execute mode\""
assert_true "execute command documents team-scope guardrails (template)" "file_contains \"$TPL/.cursor/commands/execute.md\" \"Team-scope guardrails for bulk execute mode\""

# 20) Canonical status + normalization guard checks (US-0045)
assert_true "release command documents canonical status guard section (active)" "file_contains \"$ROOT/.cursor/commands/release.md\" \"Canonical status source and global drift guard (US-0045 / DEC-0025)\""
assert_true "release command documents canonical status guard section (template)" "file_contains \"$TPL/.cursor/commands/release.md\" \"Canonical status source and global drift guard (US-0045 / DEC-0025)\""
assert_true "release command includes CANONICAL_STATUS_CONFLICT reason code (active)" "file_contains \"$ROOT/.cursor/commands/release.md\" \"CANONICAL_STATUS_CONFLICT\""
assert_true "release command includes CANONICAL_STATUS_CONFLICT reason code (template)" "file_contains \"$TPL/.cursor/commands/release.md\" \"CANONICAL_STATUS_CONFLICT\""
assert_true "auto documents canonical status contract (active)" "file_contains \"$ROOT/.cursor/commands/auto.md\" \"Canonical status contract (US-0045)\""
assert_true "auto documents canonical status contract (template)" "file_contains \"$TPL/.cursor/commands/auto.md\" \"Canonical status contract (US-0045)\""
assert_true "execute documents canonical status contract (active)" "file_contains \"$ROOT/.cursor/commands/execute.md\" \"Canonical status contract (US-0045)\""
assert_true "execute documents canonical status contract (template)" "file_contains \"$TPL/.cursor/commands/execute.md\" \"Canonical status contract (US-0045)\""
assert_true "sprint-plan documents planning source clarification (active)" "file_contains \"$ROOT/.cursor/commands/sprint-plan.md\" \"Planning source clarification (US-0045)\""
assert_true "sprint-plan documents planning source clarification (template)" "file_contains \"$TPL/.cursor/commands/sprint-plan.md\" \"Planning source clarification (US-0045)\""
assert_true "runbook documents canonical ownership guard (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"Canonical status ownership and normalization guard (US-0045)\""
assert_true "runbook documents canonical ownership guard (template)" "file_contains \"$TPL/docs/engineering/runbook.md\" \"Canonical status ownership and normalization guard (US-0045)\""
assert_true "README documents canonical story status guard (active)" "file_contains \"$ROOT/README.md\" \"Canonical story status + normalization guard (US-0045)\""
assert_true "README documents canonical story status guard (template)" "file_contains \"$TPL/README.md\" \"Canonical story status + normalization guard (US-0045)\""
assert_true "status normalization report exists (active)" "[ -f \"$ROOT/docs/engineering/status-normalization-report.md\" ]"
assert_true "status normalization report exists (template)" "[ -f \"$TPL/docs/engineering/status-normalization-report.md\" ]"
assert_true "status normalization report contains baseline row (active)" "file_contains \"$ROOT/docs/engineering/status-normalization-report.md\" \"US-0018\""
assert_true "status normalization report template is neutral" "file_contains \"$TPL/docs/engineering/status-normalization-report.md\" \"(none yet)\""

# 21) Guided intake mode checks (US-0033)
assert_true "scratchpad includes INTAKE_GUIDED_MODE (active)" "file_contains \"$ROOT/.cursor/scratchpad.md\" \"INTAKE_GUIDED_MODE\""
assert_true "scratchpad includes INTAKE_GUIDED_MODE (template)" "file_contains \"$TPL/.cursor/scratchpad.md\" \"INTAKE_GUIDED_MODE\""
assert_true "intake command documents guided mode (active)" "file_contains \"$ROOT/.cursor/commands/intake.md\" \"Guided mode behavior\""
assert_true "intake command documents guided mode (template)" "file_contains \"$TPL/.cursor/commands/intake.md\" \"Guided mode behavior\""
assert_true "intake command documents low-touch mode (active)" "file_contains \"$ROOT/.cursor/commands/intake.md\" \"Low-touch behavior\""
assert_true "intake command documents low-touch mode (template)" "file_contains \"$TPL/.cursor/commands/intake.md\" \"Low-touch behavior\""
assert_true "intake low-touch keeps duplicate safety (active)" "file_contains \"$ROOT/.cursor/commands/intake.md\" \"duplicate safety\""
assert_true "intake low-touch keeps duplicate safety (template)" "file_contains \"$TPL/.cursor/commands/intake.md\" \"duplicate safety\""
assert_true "PO agent documents guided intake mode (active)" "file_contains \"$ROOT/.cursor/agents/po.mdc\" \"Guided intake mode\""
assert_true "PO agent documents guided intake mode (template)" "file_contains \"$TPL/.cursor/agents/po.mdc\" \"Guided intake mode\""
assert_true "PO agent documents low-touch mode (active)" "file_contains \"$ROOT/.cursor/agents/po.mdc\" \"Low-touch mode\""
assert_true "PO agent documents low-touch mode (template)" "file_contains \"$TPL/.cursor/agents/po.mdc\" \"Low-touch mode\""
assert_true "runbook documents guided intake mode (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"Guided intake mode (US-0033)\""
assert_true "runbook documents guided intake mode (template)" "file_contains \"$TPL/docs/engineering/runbook.md\" \"Guided intake mode (US-0033)\""
assert_true "README documents guided intake behavior (active)" "file_contains \"$ROOT/README.md\" \"Guided intake behavior (US-0033)\""
assert_true "README documents guided intake behavior (template)" "file_contains \"$TPL/README.md\" \"Guided intake behavior (US-0033)\""

# 21b) Intake decomposition + risk-aware questioning checks (US-0051)
assert_true "intake command documents deterministic decomposition evaluator (active)" "file_contains \"$ROOT/.cursor/commands/intake.md\" \"deterministic decomposition evaluator\""
assert_true "intake command documents deterministic decomposition evaluator (template)" "file_contains \"$TPL/.cursor/commands/intake.md\" \"deterministic decomposition evaluator\""
assert_true "intake command preserves accept/merge/adjust user control (active)" "file_contains \"$ROOT/.cursor/commands/intake.md\" \"accept**, **merge**, or **adjust\""
assert_true "intake command preserves accept/merge/adjust user control (template)" "file_contains \"$TPL/.cursor/commands/intake.md\" \"accept**, **merge**, or **adjust\""
assert_true "intake command documents bounded questioning (active)" "file_contains \"$ROOT/.cursor/commands/intake.md\" \"Keep questioning bounded\""
assert_true "intake command documents bounded questioning (template)" "file_contains \"$TPL/.cursor/commands/intake.md\" \"Keep questioning bounded\""
assert_true "intake low-touch keeps no forced decomposition (active)" "file_contains \"$ROOT/.cursor/commands/intake.md\" \"single-story default (no forced decomposition)\""
assert_true "intake low-touch keeps no forced decomposition (template)" "file_contains \"$TPL/.cursor/commands/intake.md\" \"single-story default (no forced decomposition)\""

assert_true "PO agent documents decomposition evaluator (active)" "file_contains \"$ROOT/.cursor/agents/po.mdc\" \"deterministic decomposition evaluator\""
assert_true "PO agent documents decomposition evaluator (template)" "file_contains \"$TPL/.cursor/agents/po.mdc\" \"deterministic decomposition evaluator\""
assert_true "PO agent documents risk-triggered questioning (active)" "file_contains \"$ROOT/.cursor/agents/po.mdc\" \"breadth/risk is high\""
assert_true "PO agent documents risk-triggered questioning (template)" "file_contains \"$TPL/.cursor/agents/po.mdc\" \"breadth/risk is high\""
assert_true "PO agent keeps low-touch single-story default (active)" "file_contains \"$ROOT/.cursor/agents/po.mdc\" \"single-story default unless user explicitly requests decomposition\""
assert_true "PO agent keeps low-touch single-story default (template)" "file_contains \"$TPL/.cursor/agents/po.mdc\" \"single-story default unless user explicitly requests decomposition\""

assert_true "runbook documents intake decomposition and risk-aware questioning (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"Intake decomposition and risk-aware questioning (US-0051)\""
assert_true "runbook documents intake decomposition and risk-aware questioning (template)" "file_contains \"$TPL/docs/engineering/runbook.md\" \"Intake decomposition and risk-aware questioning (US-0051)\""
assert_true "README documents intake decomposition and risk-aware questioning (active)" "file_contains \"$ROOT/README.md\" \"Intake decomposition + risk-aware questioning (US-0051)\""
assert_true "README documents intake decomposition and risk-aware questioning (template)" "file_contains \"$TPL/README.md\" \"Intake decomposition + risk-aware questioning (US-0051)\""

# 21c) Optional ID namespace bootstrap checks (US-0052)
assert_true "scratchpad includes ID_NAMESPACE_BOOTSTRAP (active)" "file_contains \"$ROOT/.cursor/scratchpad.md\" \"ID_NAMESPACE_BOOTSTRAP\""
assert_true "scratchpad includes ID_NAMESPACE_BOOTSTRAP (template)" "file_contains \"$TPL/.cursor/scratchpad.md\" \"ID_NAMESPACE_BOOTSTRAP\""
assert_true "intake command documents optional ID bootstrap (active)" "file_contains \"$ROOT/.cursor/commands/intake.md\" \"Optional fresh-project ID namespace bootstrap (US-0052 / DEC-0034)\""
assert_true "intake command documents optional ID bootstrap (template)" "file_contains \"$TPL/.cursor/commands/intake.md\" \"Optional fresh-project ID namespace bootstrap (US-0052 / DEC-0034)\""
assert_true "intake command includes ineligible bootstrap diagnostic (active)" "file_contains \"$ROOT/.cursor/commands/intake.md\" \"ID_BOOTSTRAP_NOT_FRESH\""
assert_true "intake command includes ineligible bootstrap diagnostic (template)" "file_contains \"$TPL/.cursor/commands/intake.md\" \"ID_BOOTSTRAP_NOT_FRESH\""
assert_true "research command documents bootstrap-aware ID policy (active)" "file_contains \"$ROOT/.cursor/commands/research.md\" \"ID_NAMESPACE_BOOTSTRAP=1\""
assert_true "research command documents bootstrap-aware ID policy (template)" "file_contains \"$TPL/.cursor/commands/research.md\" \"ID_NAMESPACE_BOOTSTRAP=1\""
assert_true "architecture command documents DEC bootstrap policy (active)" "file_contains \"$ROOT/.cursor/commands/architecture.md\" \"DEC-0001\""
assert_true "architecture command documents DEC bootstrap policy (template)" "file_contains \"$TPL/.cursor/commands/architecture.md\" \"DEC-0001\""
assert_true "PO agent documents story ID bootstrap policy (active)" "file_contains \"$ROOT/.cursor/agents/po.mdc\" \"Story ID policy (US-0052 / DEC-0034)\""
assert_true "PO agent documents story ID bootstrap policy (template)" "file_contains \"$TPL/.cursor/agents/po.mdc\" \"Story ID policy (US-0052 / DEC-0034)\""
assert_true "Tech Lead agent documents decision ID bootstrap policy (active)" "file_contains \"$ROOT/.cursor/agents/tech-lead.mdc\" \"Decision ID policy (US-0052 / DEC-0034)\""
assert_true "Tech Lead agent documents decision ID bootstrap policy (template)" "file_contains \"$TPL/.cursor/agents/tech-lead.mdc\" \"Decision ID policy (US-0052 / DEC-0034)\""
assert_true "runbook documents optional ID namespace bootstrap (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"Optional ID namespace bootstrap (US-0052)\""
assert_true "runbook documents optional ID namespace bootstrap (template)" "file_contains \"$TPL/docs/engineering/runbook.md\" \"Optional ID namespace bootstrap (US-0052)\""
assert_true "README documents optional ID namespace bootstrap (active)" "file_contains \"$ROOT/README.md\" \"Optional ID namespace bootstrap (US-0052)\""
assert_true "README documents optional ID namespace bootstrap (template)" "file_contains \"$TPL/README.md\" \"Optional ID namespace bootstrap (US-0052)\""

# 21d) Context compaction and token profile checks (US-0053)
assert_true "scratchpad includes TOKEN_PROFILE (active)" "file_contains \"$ROOT/.cursor/scratchpad.md\" \"TOKEN_PROFILE=balanced\""
assert_true "scratchpad includes TOKEN_PROFILE (template)" "file_contains \"$TPL/.cursor/scratchpad.md\" \"TOKEN_PROFILE=balanced\""
assert_true "scratchpad documents manual override precedence (active)" "file_contains \"$ROOT/.cursor/scratchpad.md\" \"Manual-override precedence\""
assert_true "scratchpad documents manual override precedence (template)" "file_contains \"$TPL/.cursor/scratchpad.md\" \"Manual-override precedence\""
assert_true "runbook documents context compaction and token profile mode (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"Context compaction and token profile mode (US-0053 / DEC-0035)\""
assert_true "runbook documents context compaction and token profile mode (template)" "file_contains \"$TPL/docs/engineering/runbook.md\" \"Context compaction and token profile mode (US-0053 / DEC-0035)\""
assert_true "README documents context compaction and tiered token profile (active)" "file_contains \"$ROOT/README.md\" \"Context compaction + tiered token profile (US-0053)\""
assert_true "README documents context compaction and tiered token profile (template)" "file_contains \"$TPL/README.md\" \"Context compaction + tiered token profile (US-0053)\""
assert_true "ask command documents narrow-read policy (active)" "file_contains \"$ROOT/.cursor/commands/ask.md\" \"Apply narrow-read retrieval policy (US-0053)\""
assert_true "ask command documents narrow-read policy (template)" "file_contains \"$TPL/.cursor/commands/ask.md\" \"Apply narrow-read retrieval policy (US-0053)\""
assert_true "ask command documents BUG-#### id family (active)" "file_contains \"$ROOT/.cursor/commands/ask.md\" \"BUG-####\""
assert_true "ask command documents BUG-#### id family (template)" "file_contains \"$TPL/.cursor/commands/ask.md\" \"BUG-####\""
assert_true "state documents active context surface policy (active)" "file_contains \"$ROOT/docs/engineering/state.md\" \"Active context surface (US-0053 / DEC-0035)\""
assert_true "state template documents active context surface policy" "file_contains \"$TPL/docs/engineering/state.md\" \"Active context surface (US-0053 / DEC-0035)\""
assert_true "state archive README exists (active)" "[ -f \"$ROOT/docs/engineering/state-archive/README.md\" ]"
assert_true "state archive README exists (template)" "[ -f \"$TPL/docs/engineering/state-archive/README.md\" ]"
assert_true "decisions index is compacted (active)" "file_contains \"$ROOT/docs/engineering/decisions.md\" \"Compact decision index (bounded summaries)\""
assert_true "decisions index includes canonical full records pointer (active)" "file_contains \"$ROOT/docs/engineering/decisions.md\" \"Full records live in decisions/DEC-xxxx.md\""
assert_true "decisions index includes canonical full records pointer (template)" "file_contains \"$TPL/docs/engineering/decisions.md\" \"Full records live in decisions/DEC-xxxx.md\""
assert_true "release gate chain remains documented (active)" "file_contains \"$ROOT/.cursor/commands/release.md\" \"Release gate chain (US-0039 / DEC-0019)\""
assert_true "release gate chain remains documented (template)" "file_contains \"$TPL/.cursor/commands/release.md\" \"Release gate chain (US-0039 / DEC-0019)\""

# 21e) Configurable multi-target publish checks (US-0054)
assert_true "scratchpad includes RELEASE_PUBLISH_MODE (active)" "file_contains \"$ROOT/.cursor/scratchpad.md\" \"RELEASE_PUBLISH_MODE=confirm\""
assert_true "scratchpad includes RELEASE_PUBLISH_MODE (template)" "file_contains \"$TPL/.cursor/scratchpad.md\" \"RELEASE_PUBLISH_MODE=confirm\""
assert_true "scratchpad includes RELEASE_TARGETS_FILE (active)" "file_contains \"$ROOT/.cursor/scratchpad.md\" \"RELEASE_TARGETS_FILE=docs/engineering/release-targets.json\""
assert_true "scratchpad includes RELEASE_TARGETS_FILE (template)" "file_contains \"$TPL/.cursor/scratchpad.md\" \"RELEASE_TARGETS_FILE=docs/engineering/release-targets.json\""
assert_true "runbook documents configurable multi-target publish mode (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"Configurable multi-target publish mode (US-0054 / DEC-0036)\""
assert_true "runbook documents configurable multi-target publish mode (template)" "file_contains \"$TPL/docs/engineering/runbook.md\" \"Configurable multi-target publish mode (US-0054 / DEC-0036)\""
assert_true "README documents configurable multi-target publish mode (active)" "file_contains \"$ROOT/README.md\" \"Configurable multi-target publish + confirmation gate (US-0054)\""
assert_true "README documents configurable multi-target publish mode (template)" "file_contains \"$TPL/README.md\" \"Configurable multi-target publish + confirmation gate (US-0054)\""
assert_true "release command includes configurable publish target section (active)" "file_contains \"$ROOT/.cursor/commands/release.md\" \"Optional configurable publish targets (US-0054 / DEC-0036)\""
assert_true "release command includes configurable publish target section (template)" "file_contains \"$TPL/.cursor/commands/release.md\" \"Optional configurable publish targets (US-0054 / DEC-0036)\""
assert_true "release command includes publish config invalid reason code (active)" "file_contains \"$ROOT/.cursor/commands/release.md\" \"PUBLISH_TARGET_CONFIG_INVALID\""
assert_true "release command includes publish config invalid reason code (template)" "file_contains \"$TPL/.cursor/commands/release.md\" \"PUBLISH_TARGET_CONFIG_INVALID\""
assert_true "release targets schema file exists (active)" "[ -f \"$ROOT/docs/engineering/release-targets.json\" ]"
assert_true "release targets schema file exists (template)" "[ -f \"$TPL/docs/engineering/release-targets.json\" ]"
assert_true "release targets schema includes custom target type (active)" "file_contains \"$ROOT/docs/engineering/release-targets.json\" \"\\\"type\\\": \\\"custom\\\"\""
assert_true "release targets schema includes ssh target type (active)" "file_contains \"$ROOT/docs/engineering/release-targets.json\" \"\\\"type\\\": \\\"ssh\\\"\""
assert_true "release targets schema includes ssh target type (template)" "file_contains \"$TPL/docs/engineering/release-targets.json\" \"\\\"type\\\": \\\"ssh\\\"\""

# 21f) Deterministic status reconciliation checks (US-0055)
assert_true "status-reconcile command exists (active)" "[ -f \"$ROOT/.cursor/commands/status-reconcile.md\" ]"
assert_true "status-reconcile command exists (template)" "[ -f \"$TPL/.cursor/commands/status-reconcile.md\" ]"
assert_true "status-reconcile command defines canonical precedence (active)" "file_contains \"$ROOT/.cursor/commands/status-reconcile.md\" \"Canonical precedence (US-0045 / DEC-0025)\""
assert_true "status-reconcile command defines canonical precedence (template)" "file_contains \"$TPL/.cursor/commands/status-reconcile.md\" \"Canonical precedence (US-0045 / DEC-0025)\""
assert_true "status-reconcile command includes deterministic reason code STATUS_RECONCILE_APPLIED (active)" "file_contains \"$ROOT/.cursor/commands/status-reconcile.md\" \"STATUS_RECONCILE_APPLIED\""
assert_true "status-reconcile command includes deterministic reason code STATUS_RECONCILE_APPLIED (template)" "file_contains \"$TPL/.cursor/commands/status-reconcile.md\" \"STATUS_RECONCILE_APPLIED\""
assert_true "runbook documents deterministic status reconciliation mode (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"Deterministic status reconciliation mode (US-0055 / DEC-0037)\""
assert_true "runbook documents deterministic status reconciliation mode (template)" "file_contains \"$TPL/docs/engineering/runbook.md\" \"Deterministic status reconciliation mode (US-0055 / DEC-0037)\""
assert_true "README documents deterministic status reconciliation command (active)" "file_contains \"$ROOT/README.md\" \"Deterministic status reconciliation command (US-0055)\""
assert_true "README documents deterministic status reconciliation command (template)" "file_contains \"$TPL/README.md\" \"Deterministic status reconciliation command (US-0055)\""

# 21g) Upgrade-safe scratchpad example checks (US-0057)
assert_true "scratchpad local example exists (active)" "[ -f \"$ROOT/.cursor/scratchpad.local.example.md\" ]"
assert_true "scratchpad local example exists (template)" "[ -f \"$TPL/.cursor/scratchpad.local.example.md\" ]"
assert_true "scratchpad local example includes token profile override (active)" "file_contains \"$ROOT/.cursor/scratchpad.local.example.md\" \"TOKEN_PROFILE=balanced\""
assert_true "scratchpad local example includes detailed core behavior descriptions (active)" "file_contains \"$ROOT/.cursor/scratchpad.local.example.md\" \"- MAGIC_CONTEXT_STRICT: 0|1\""
assert_true "scratchpad local example includes detailed automation descriptions (template)" "file_contains \"$TPL/.cursor/scratchpad.local.example.md\" \"- AUTO_FLOW_MODE: manual|auto_until_decision\""
assert_true "scratchpad local example includes release publish mode override (active)" "file_contains \"$ROOT/.cursor/scratchpad.local.example.md\" \"RELEASE_PUBLISH_MODE=confirm\""
assert_true "scratchpad local example includes release publish mode override (template)" "file_contains \"$TPL/.cursor/scratchpad.local.example.md\" \"RELEASE_PUBLISH_MODE=confirm\""
assert_true "runbook documents scratchpad upgrade contract (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"Scratchpad example upgrade contract (US-0057 / DEC-0039 / DEC-0057)\""
assert_true "runbook documents scratchpad upgrade contract (template)" "file_contains \"$TPL/docs/engineering/runbook.md\" \"Scratchpad example upgrade contract (US-0057 / DEC-0039 / DEC-0057)\""
assert_true "README documents scratchpad upgrade behavior (active)" "file_contains \"$ROOT/README.md\" \"Upgrade behavior (US-0057 / DEC-0057):\""
assert_true "README documents scratchpad upgrade behavior (template)" "file_contains \"$TPL/README.md\" \"Upgrade behavior (US-0057 / DEC-0057):\""

# 21h) Deterministic artifact ordering checks (US-0058)
assert_true "artifact ordering policy exists (active)" "[ -f \"$ROOT/docs/engineering/artifact-ordering-policy.md\" ]"
assert_true "artifact ordering policy exists (template)" "[ -f \"$TPL/docs/engineering/artifact-ordering-policy.md\" ]"
assert_true "artifact ordering policy defines state append-bottom (active)" "file_contains \"$ROOT/docs/engineering/artifact-ordering-policy.md\" '`docs/engineering/state.md` | `append-bottom`'"
assert_true "artifact ordering policy defines backlog sorted-canonical (active)" "file_contains \"$ROOT/docs/engineering/artifact-ordering-policy.md\" '`docs/product/backlog.md` | `sorted-canonical`'"
assert_true "artifact ordering policy includes anchor ambiguous reason code (active)" "file_contains \"$ROOT/docs/engineering/artifact-ordering-policy.md\" \"ARTIFACT_ORDERING_ANCHOR_AMBIGUOUS\""
assert_true "auto command includes ordering guard (active)" "file_contains \"$ROOT/.cursor/commands/auto.md\" \"Deterministic artifact ordering guard (US-0058 / DEC-0040)\""
assert_true "auto command includes ordering guard (template)" "file_contains \"$TPL/.cursor/commands/auto.md\" \"Deterministic artifact ordering guard (US-0058 / DEC-0040)\""
assert_true "intake command includes ordering contract (active)" "file_contains \"$ROOT/.cursor/commands/intake.md\" \"Deterministic artifact ordering contract (US-0058 / DEC-0040)\""
assert_true "intake command includes ordering contract (template)" "file_contains \"$TPL/.cursor/commands/intake.md\" \"Deterministic artifact ordering contract (US-0058 / DEC-0040)\""
assert_true "release command includes ordering contract (active)" "file_contains \"$ROOT/.cursor/commands/release.md\" \"Deterministic artifact ordering contract (US-0058 / DEC-0040)\""
assert_true "release command includes ordering contract (template)" "file_contains \"$TPL/.cursor/commands/release.md\" \"Deterministic artifact ordering contract (US-0058 / DEC-0040)\""
assert_true "refresh-context includes ordering contract (active)" "file_contains \"$ROOT/.cursor/commands/refresh-context.md\" \"Deterministic artifact ordering contract (US-0058 / DEC-0040)\""
assert_true "refresh-context includes ordering contract (template)" "file_contains \"$TPL/.cursor/commands/refresh-context.md\" \"Deterministic artifact ordering contract (US-0058 / DEC-0040)\""
assert_true "status-reconcile includes ordering contract (active)" "file_contains \"$ROOT/.cursor/commands/status-reconcile.md\" \"Deterministic artifact ordering contract (US-0058 / DEC-0040)\""
assert_true "status-reconcile includes ordering contract (template)" "file_contains \"$TPL/.cursor/commands/status-reconcile.md\" \"Deterministic artifact ordering contract (US-0058 / DEC-0040)\""
assert_true "runbook documents deterministic artifact ordering mode (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"Deterministic artifact ordering and write discipline (US-0058 / DEC-0040)\""
assert_true "runbook documents deterministic artifact ordering mode (template)" "file_contains \"$TPL/docs/engineering/runbook.md\" \"Deterministic artifact ordering and write discipline (US-0058 / DEC-0040)\""
assert_true "README documents deterministic ordering behavior (active)" "file_contains \"$ROOT/README.md\" \"Deterministic ordering behavior (US-0058):\""
assert_true "README documents deterministic ordering behavior (template)" "file_contains \"$TPL/README.md\" \"Deterministic ordering behavior (US-0058):\""
assert_true "artifact ordering policy includes non-monotonic state timestamp reason code (active)" "file_contains \"$ROOT/docs/engineering/artifact-ordering-policy.md\" \"STATE_TIMESTAMP_NON_MONOTONIC\""
assert_true "artifact ordering policy includes non-monotonic state timestamp reason code (template)" "file_contains \"$TPL/docs/engineering/artifact-ordering-policy.md\" \"STATE_TIMESTAMP_NON_MONOTONIC\""

# 21i) Intake runtime capability and writer-safety checks (US-0059)
assert_true "scratchpad includes INTAKE_SUBAGENT_FALLBACK (active)" "file_contains \"$ROOT/.cursor/scratchpad.md\" \"INTAKE_SUBAGENT_FALLBACK=deny\""
assert_true "scratchpad includes INTAKE_SUBAGENT_FALLBACK (template)" "file_contains \"$TPL/.cursor/scratchpad.md\" \"INTAKE_SUBAGENT_FALLBACK=deny\""
assert_true "scratchpad local example includes INTAKE_SUBAGENT_FALLBACK (active)" "file_contains \"$ROOT/.cursor/scratchpad.local.example.md\" \"INTAKE_SUBAGENT_FALLBACK=deny\""
assert_true "scratchpad local example includes INTAKE_SUBAGENT_FALLBACK (template)" "file_contains \"$TPL/.cursor/scratchpad.local.example.md\" \"INTAKE_SUBAGENT_FALLBACK=deny\""
assert_true "intake command documents capability fail-fast code (active)" "file_contains \"$ROOT/.cursor/commands/intake.md\" \"SUBAGENT_CAPABILITY_UNAVAILABLE\""
assert_true "intake command documents capability fail-fast code (template)" "file_contains \"$TPL/.cursor/commands/intake.md\" \"SUBAGENT_CAPABILITY_UNAVAILABLE\""
assert_true "intake command documents concurrent writer fail-safe code (active)" "file_contains \"$ROOT/.cursor/commands/intake.md\" \"INTAKE_CONCURRENT_WRITER_DETECTED\""
assert_true "intake command documents concurrent writer fail-safe code (template)" "file_contains \"$TPL/.cursor/commands/intake.md\" \"INTAKE_CONCURRENT_WRITER_DETECTED\""
assert_true "runbook documents intake runtime capability and writer safety mode (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"Intake runtime capability and single-writer safety (US-0059 / DEC-0041)\""
assert_true "runbook documents intake runtime capability and writer safety mode (template)" "file_contains \"$TPL/docs/engineering/runbook.md\" \"Intake runtime capability and single-writer safety (US-0059 / DEC-0041)\""
assert_true "README documents intake runtime safety behavior (active)" "file_contains \"$ROOT/README.md\" \"Intake runtime safety behavior (US-0059):\""
assert_true "README documents intake runtime safety behavior (template)" "file_contains \"$TPL/README.md\" \"Intake runtime safety behavior (US-0059):\""

# 21j) Deterministic state rollover enforcement checks (US-0060)
assert_true "scratchpad includes STATE_HOT_MAX_LINES (active)" "file_contains \"$ROOT/.cursor/scratchpad.md\" \"STATE_HOT_MAX_LINES=1200\""
assert_true "scratchpad includes STATE_HOT_MAX_LINES (template)" "file_contains \"$TPL/.cursor/scratchpad.md\" \"STATE_HOT_MAX_LINES=1200\""
assert_true "scratchpad includes STATE_HOT_MAX_CHECKPOINTS (active)" "file_contains \"$ROOT/.cursor/scratchpad.md\" \"STATE_HOT_MAX_CHECKPOINTS=80\""
assert_true "scratchpad includes STATE_HOT_MAX_CHECKPOINTS (template)" "file_contains \"$TPL/.cursor/scratchpad.md\" \"STATE_HOT_MAX_CHECKPOINTS=80\""
assert_true "scratchpad local example includes STATE_HOT_MAX_LINES (active)" "file_contains \"$ROOT/.cursor/scratchpad.local.example.md\" \"STATE_HOT_MAX_LINES=1200\""
assert_true "scratchpad local example includes STATE_HOT_MAX_LINES (template)" "file_contains \"$TPL/.cursor/scratchpad.local.example.md\" \"STATE_HOT_MAX_LINES=1200\""
assert_true "refresh-context command documents rollover thresholds (active)" "file_contains \"$ROOT/.cursor/commands/refresh-context.md\" \"STATE_HOT_MAX_LINES\""
assert_true "refresh-context command documents rollover thresholds (template)" "file_contains \"$TPL/.cursor/commands/refresh-context.md\" \"STATE_HOT_MAX_LINES\""
assert_true "refresh-context includes archive write fail-safe code (active)" "file_contains \"$ROOT/.cursor/commands/refresh-context.md\" \"STATE_ARCHIVE_WRITE_FAILED\""
assert_true "refresh-context includes archive write fail-safe code (template)" "file_contains \"$TPL/.cursor/commands/refresh-context.md\" \"STATE_ARCHIVE_WRITE_FAILED\""
assert_true "artifact ordering policy includes archive fail-safe code (active)" "file_contains \"$ROOT/docs/engineering/artifact-ordering-policy.md\" \"STATE_ARCHIVE_BOUNDARY_AMBIGUOUS\""
assert_true "artifact ordering policy includes archive fail-safe code (template)" "file_contains \"$TPL/docs/engineering/artifact-ordering-policy.md\" \"STATE_ARCHIVE_BOUNDARY_AMBIGUOUS\""
assert_true "runbook documents enforced rollover thresholds (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"Enforced rollover thresholds\""
assert_true "runbook documents enforced rollover thresholds (template)" "file_contains \"$TPL/docs/engineering/runbook.md\" \"Enforced rollover thresholds\""
assert_true "README documents enforced rollover thresholds (active)" "file_contains \"$ROOT/README.md\" \"Enforced rollover thresholds\""
assert_true "README documents enforced rollover thresholds (template)" "file_contains \"$TPL/README.md\" \"Enforced rollover thresholds\""

# 22) Optional cross-repo observability checks (US-0034)
assert_true "scratchpad includes CROSS_REPO_OBSERVABILITY (active)" "file_contains \"$ROOT/.cursor/scratchpad.md\" \"CROSS_REPO_OBSERVABILITY\""
assert_true "scratchpad includes CROSS_REPO_OBSERVABILITY (template)" "file_contains \"$TPL/.cursor/scratchpad.md\" \"CROSS_REPO_OBSERVABILITY\""
assert_true "scratchpad includes COMPATIBILITY_GATE_ON_CRITICAL (active)" "file_contains \"$ROOT/.cursor/scratchpad.md\" \"COMPATIBILITY_GATE_ON_CRITICAL\""
assert_true "scratchpad includes COMPATIBILITY_GATE_ON_CRITICAL (template)" "file_contains \"$TPL/.cursor/scratchpad.md\" \"COMPATIBILITY_GATE_ON_CRITICAL\""
assert_true "scratchpad includes COMPATIBILITY_SOURCES (active)" "file_contains \"$ROOT/.cursor/scratchpad.md\" \"COMPATIBILITY_SOURCES\""
assert_true "scratchpad includes COMPATIBILITY_SOURCES (template)" "file_contains \"$TPL/.cursor/scratchpad.md\" \"COMPATIBILITY_SOURCES\""

assert_true "intake command includes zero-overhead disabled behavior (active)" "file_contains \"$ROOT/.cursor/commands/intake.md\" \"CROSS_REPO_OBSERVABILITY=0\""
assert_true "intake command includes zero-overhead disabled behavior (template)" "file_contains \"$TPL/.cursor/commands/intake.md\" \"CROSS_REPO_OBSERVABILITY=0\""
assert_true "architecture command includes compatibility mode contract (active)" "file_contains \"$ROOT/.cursor/commands/architecture.md\" \"Optional cross-repo observability architecture (US-0034)\""
assert_true "architecture command includes compatibility mode contract (template)" "file_contains \"$TPL/.cursor/commands/architecture.md\" \"Optional cross-repo observability architecture (US-0034)\""
assert_true "execute command includes compatibility mode contract (active)" "file_contains \"$ROOT/.cursor/commands/execute.md\" \"Optional compatibility observability execution contract (US-0034)\""
assert_true "execute command includes compatibility mode contract (template)" "file_contains \"$TPL/.cursor/commands/execute.md\" \"Optional compatibility observability execution contract (US-0034)\""
assert_true "qa command includes compatibility mode checks (active)" "file_contains \"$ROOT/.cursor/commands/qa.md\" \"Optional compatibility observability QA checks (US-0034)\""
assert_true "qa command includes compatibility mode checks (template)" "file_contains \"$TPL/.cursor/commands/qa.md\" \"Optional compatibility observability QA checks (US-0034)\""
assert_true "release command includes compatibility critical reason code (active)" "file_contains \"$ROOT/.cursor/commands/release.md\" \"COMPATIBILITY_CRITICAL_OPEN\""
assert_true "release command includes compatibility critical reason code (template)" "file_contains \"$TPL/.cursor/commands/release.md\" \"COMPATIBILITY_CRITICAL_OPEN\""

assert_true "runbook documents optional cross-repo observability mode (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"Optional cross-repo observability mode (US-0034)\""
assert_true "runbook documents optional cross-repo observability mode (template)" "file_contains \"$TPL/docs/engineering/runbook.md\" \"Optional cross-repo observability mode (US-0034)\""
assert_true "README documents optional cross-repo observability (active)" "file_contains \"$ROOT/README.md\" \"Optional cross-repo observability (US-0034)\""
assert_true "README documents optional cross-repo observability (template)" "file_contains \"$TPL/README.md\" \"Optional cross-repo observability (US-0034)\""

assert_true "compatibility report exists (active)" "[ -f \"$ROOT/docs/engineering/compatibility-report.md\" ]"
assert_true "compatibility report exists (template)" "[ -f \"$TPL/docs/engineering/compatibility-report.md\" ]"
assert_true "compatibility signals exists (active)" "[ -f \"$ROOT/docs/engineering/compatibility-signals.md\" ]"
assert_true "compatibility signals exists (template)" "[ -f \"$TPL/docs/engineering/compatibility-signals.md\" ]"
assert_true "registry manifest exists (active)" "[ -f \"$ROOT/docs/engineering/manifests/registry.manifest.yaml\" ]"
assert_true "registry manifest exists (template)" "[ -f \"$TPL/docs/engineering/manifests/registry.manifest.yaml\" ]"
assert_true "repo manifest exists (active)" "[ -f \"$ROOT/docs/engineering/manifests/repo.manifest.yaml\" ]"
assert_true "repo manifest exists (template)" "[ -f \"$TPL/docs/engineering/manifests/repo.manifest.yaml\" ]"

# 23) Optional component-scoped execution checks (US-0035)
assert_true "scratchpad includes COMPONENT_SCOPE_MODE (active)" "file_contains \"$ROOT/.cursor/scratchpad.md\" \"COMPONENT_SCOPE_MODE\""
assert_true "scratchpad includes COMPONENT_SCOPE_MODE (template)" "file_contains \"$TPL/.cursor/scratchpad.md\" \"COMPONENT_SCOPE_MODE\""
assert_true "scratchpad includes TARGET_COMPONENTS (active)" "file_contains \"$ROOT/.cursor/scratchpad.md\" \"TARGET_COMPONENTS\""
assert_true "scratchpad includes TARGET_COMPONENTS (template)" "file_contains \"$TPL/.cursor/scratchpad.md\" \"TARGET_COMPONENTS\""

assert_true "intake command includes component scope declaration contract (active)" "file_contains \"$ROOT/.cursor/commands/intake.md\" \"Optional component scope declaration (US-0035)\""
assert_true "intake command includes component scope declaration contract (template)" "file_contains \"$TPL/.cursor/commands/intake.md\" \"Optional component scope declaration (US-0035)\""
assert_true "architecture command includes component scope contract (active)" "file_contains \"$ROOT/.cursor/commands/architecture.md\" \"Optional component-scope architecture (US-0035)\""
assert_true "architecture command includes component scope contract (template)" "file_contains \"$TPL/.cursor/commands/architecture.md\" \"Optional component-scope architecture (US-0035)\""
assert_true "sprint-plan includes scoped task metadata contract (active)" "file_contains \"$ROOT/.cursor/commands/sprint-plan.md\" \"Optional component-scoped planning (US-0035)\""
assert_true "sprint-plan includes scoped task metadata contract (template)" "file_contains \"$TPL/.cursor/commands/sprint-plan.md\" \"Optional component-scoped planning (US-0035)\""
assert_true "execute includes component-scope guardrails (active)" "file_contains \"$ROOT/.cursor/commands/execute.md\" \"Optional component-scoped execution guardrails (US-0035)\""
assert_true "execute includes component-scope guardrails (template)" "file_contains \"$TPL/.cursor/commands/execute.md\" \"Optional component-scoped execution guardrails (US-0035)\""
assert_true "qa includes component-scope protection checks (active)" "file_contains \"$ROOT/.cursor/commands/qa.md\" \"Optional component-scope protection checks (US-0035)\""
assert_true "qa includes component-scope protection checks (template)" "file_contains \"$TPL/.cursor/commands/qa.md\" \"Optional component-scope protection checks (US-0035)\""
assert_true "release includes component-scope violation reason code (active)" "file_contains \"$ROOT/.cursor/commands/release.md\" \"COMPONENT_SCOPE_VIOLATION_UNAPPROVED\""
assert_true "release includes component-scope violation reason code (template)" "file_contains \"$TPL/.cursor/commands/release.md\" \"COMPONENT_SCOPE_VIOLATION_UNAPPROVED\""

assert_true "runbook documents optional component-scoped mode (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"Optional component-scoped execution mode (US-0035)\""
assert_true "runbook documents optional component-scoped mode (template)" "file_contains \"$TPL/docs/engineering/runbook.md\" \"Optional component-scoped execution mode (US-0035)\""
assert_true "README documents optional component-scoped execution (active)" "file_contains \"$ROOT/README.md\" \"Optional component-scoped execution (US-0035)\""
assert_true "README documents optional component-scoped execution (template)" "file_contains \"$TPL/README.md\" \"Optional component-scoped execution (US-0035)\""

assert_true "component scope artifact exists (active)" "[ -f \"$ROOT/docs/engineering/component-scope.md\" ]"
assert_true "component scope artifact exists (template)" "[ -f \"$TPL/docs/engineering/component-scope.md\" ]"
assert_true "component scope report exists (active)" "[ -f \"$ROOT/docs/engineering/component-scope-report.md\" ]"
assert_true "component scope report exists (template)" "[ -f \"$TPL/docs/engineering/component-scope-report.md\" ]"

# 24) Optional spec-pack documentation checks (US-0031)
assert_true "scratchpad includes SPEC_PACK_MODE (active)" "file_contains \"$ROOT/.cursor/scratchpad.md\" \"SPEC_PACK_MODE\""
assert_true "scratchpad includes SPEC_PACK_MODE (template)" "file_contains \"$TPL/.cursor/scratchpad.md\" \"SPEC_PACK_MODE\""
assert_true "intake command includes spec-pack zero-overhead when disabled (active)" "file_contains \"$ROOT/.cursor/commands/intake.md\" \"SPEC_PACK_MODE=0\""
assert_true "intake command includes spec-pack zero-overhead when disabled (template)" "file_contains \"$TPL/.cursor/commands/intake.md\" \"SPEC_PACK_MODE=0\""
assert_true "architecture command includes optional spec-pack step (active)" "file_contains \"$ROOT/.cursor/commands/architecture.md\" \"Optional spec-pack (US-0031)\""
assert_true "architecture command includes optional spec-pack step (template)" "file_contains \"$TPL/.cursor/commands/architecture.md\" \"Optional spec-pack (US-0031)\""
assert_true "release command includes spec-pack completeness gate (active)" "file_contains \"$ROOT/.cursor/commands/release.md\" \"SPEC_PACK_INCOMPLETE\""
assert_true "release command includes spec-pack completeness gate (template)" "file_contains \"$TPL/.cursor/commands/release.md\" \"SPEC_PACK_INCOMPLETE\""
assert_true "execute command includes optional spec-pack step (active)" "file_contains \"$ROOT/.cursor/commands/execute.md\" \"Optional spec-pack (US-0031)\""
assert_true "execute command includes optional spec-pack step (template)" "file_contains \"$TPL/.cursor/commands/execute.md\" \"Optional spec-pack (US-0031)\""
assert_true "qa command includes optional spec-pack verification (active)" "file_contains \"$ROOT/.cursor/commands/qa.md\" \"Optional spec-pack verification (US-0031)\""
assert_true "qa command includes optional spec-pack verification (template)" "file_contains \"$TPL/.cursor/commands/qa.md\" \"Optional spec-pack verification (US-0031)\""
assert_true "runbook documents optional spec-pack mode (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"Optional spec-pack documentation mode (US-0031)\""
assert_true "runbook documents optional spec-pack mode (template)" "file_contains \"$TPL/docs/engineering/runbook.md\" \"Optional spec-pack documentation mode (US-0031)\""
assert_true "README documents optional spec-pack documentation (active)" "file_contains \"$ROOT/README.md\" \"Optional spec-pack documentation (US-0031)\""
assert_true "README documents optional spec-pack documentation (template)" "file_contains \"$TPL/README.md\" \"Optional spec-pack documentation (US-0031)\""
assert_true "spec-pack README exists (active)" "[ -f \"$ROOT/docs/engineering/spec-pack/README.md\" ]"
assert_true "spec-pack README exists (template)" "[ -f \"$TPL/docs/engineering/spec-pack/README.md\" ]"

# 24b) Optional user-guide documentation checks (US-0032)
assert_true "scratchpad includes USER_GUIDE_MODE (active)" "file_contains \"$ROOT/.cursor/scratchpad.md\" \"USER_GUIDE_MODE\""
assert_true "scratchpad includes USER_GUIDE_MODE (template)" "file_contains \"$TPL/.cursor/scratchpad.md\" \"USER_GUIDE_MODE\""
assert_true "intake command includes user-guide zero-overhead when disabled (active)" "file_contains \"$ROOT/.cursor/commands/intake.md\" \"USER_GUIDE_MODE=0\""
assert_true "intake command includes user-guide zero-overhead when disabled (template)" "file_contains \"$TPL/.cursor/commands/intake.md\" \"USER_GUIDE_MODE=0\""
assert_true "release command includes user-guide completeness gate (active)" "file_contains \"$ROOT/.cursor/commands/release.md\" \"USER_GUIDE_INCOMPLETE\""
assert_true "release command includes user-guide completeness gate (template)" "file_contains \"$TPL/.cursor/commands/release.md\" \"USER_GUIDE_INCOMPLETE\""
assert_true "runbook documents optional user-guide mode (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"Optional user-guide documentation mode (US-0032)\""
assert_true "runbook documents optional user-guide mode (template)" "file_contains \"$TPL/docs/engineering/runbook.md\" \"Optional user-guide documentation mode (US-0032)\""
assert_true "README documents optional user-guide documentation (active)" "file_contains \"$ROOT/README.md\" \"Optional user-guide documentation (US-0032)\""
assert_true "README documents optional user-guide documentation (template)" "file_contains \"$TPL/README.md\" \"Optional user-guide documentation (US-0032)\""
assert_true "user-guides README exists (active)" "[ -f \"$ROOT/docs/user-guides/README.md\" ]"
assert_true "user-guides README exists (template)" "[ -f \"$TPL/docs/user-guides/README.md\" ]"

# 25) Release gate tightening checks (US-0039)
assert_true "release command defines release gate chain US-0039 (active)" "file_contains \"$ROOT/.cursor/commands/release.md\" \"Release gate chain (US-0039 / DEC-0019)\""
assert_true "release command defines release gate chain US-0039 (template)" "file_contains \"$TPL/.cursor/commands/release.md\" \"Release gate chain (US-0039 / DEC-0019)\""
assert_true "release command defines check-in test evidence validity (active)" "file_contains \"$ROOT/.cursor/commands/release.md\" \"RELEASE_TEST_EVIDENCE_MISSING\""
assert_true "release command defines check-in test evidence validity (template)" "file_contains \"$TPL/.cursor/commands/release.md\" \"RELEASE_TEST_EVIDENCE_MISSING\""
assert_true "release command defines QA completion gate (active)" "file_contains \"$ROOT/.cursor/commands/release.md\" \"QA completion evidence gate (US-0039)\""
assert_true "release command defines QA completion gate (template)" "file_contains \"$TPL/.cursor/commands/release.md\" \"QA completion evidence gate\""
assert_true "release command defines UAT completion gate (active)" "file_contains \"$ROOT/.cursor/commands/release.md\" \"UAT completion gate (US-0039)\""
assert_true "release command defines UAT completion gate (template)" "file_contains \"$TPL/.cursor/commands/release.md\" \"UAT completion gate\""
assert_true "release command defines no-bypass default (active)" "file_contains \"$ROOT/.cursor/commands/release.md\" \"No-bypass default (US-0039)\""
assert_true "release command documents no bypass default (template)" "file_contains \"$TPL/.cursor/commands/release.md\" \"no bypass\""
assert_true "release command defines override evidence contract (active)" "file_contains \"$ROOT/.cursor/commands/release.md\" \"RELEASE_GATE_OVERRIDE_APPROVED\""
assert_true "release command defines override evidence contract (template)" "file_contains \"$TPL/.cursor/commands/release.md\" \"RELEASE_GATE_OVERRIDE_APPROVED\""
assert_true "runbook documents release gate chain US-0039 (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"Release gate chain (US-0039 / DEC-0019)\""
assert_true "runbook documents release gate chain US-0039 (template)" "file_contains \"$TPL/docs/engineering/runbook.md\" \"Release gate chain (US-0039 / DEC-0019)\""
assert_true "runbook documents optional-command compatibility US-0039 (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"Optional-command compatibility (US-0039\""
assert_true "runbook documents optional-command compatibility US-0039 (template)" "file_contains \"$TPL/docs/engineering/runbook.md\" \"Optional-command compatibility (US-0039\""
assert_true "qa command includes release gate prerequisite US-0039 (active)" "file_contains \"$ROOT/.cursor/commands/qa.md\" \"Release gate prerequisite (US-0039)\""
assert_true "qa command includes release gate prerequisite US-0039 (template)" "file_contains \"$TPL/.cursor/commands/qa.md\" \"Release gate prerequisite (US-0039)\""
assert_true "core rule includes release gate no-bypass (active)" "file_contains \"$ROOT/.cursor/rules/core.mdc\" \"Release gate no-bypass (US-0039\""

# 26) Per-phase isolation enforcement checks (US-0048)
assert_true "auto enforces per-phase isolation (active)" "file_contains \"$ROOT/.cursor/commands/auto.md\" \"Per-phase isolation enforcement (US-0048 / DEC-0029)\""
assert_true "auto enforces per-phase isolation (template)" "file_contains \"$TPL/.cursor/commands/auto.md\" \"Per-phase isolation enforcement (US-0048 / DEC-0029)\""
assert_true "auto includes isolation violation reason code (active)" "file_contains \"$ROOT/.cursor/commands/auto.md\" \"PHASE_CONTEXT_ISOLATION_VIOLATION\""
assert_true "auto includes isolation violation reason code (template)" "file_contains \"$TPL/.cursor/commands/auto.md\" \"PHASE_CONTEXT_ISOLATION_VIOLATION\""

assert_true "runbook documents isolation evidence contract (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"Per-phase subagent isolation evidence (US-0048 / DEC-0029)\""
assert_true "runbook documents isolation evidence contract (template)" "file_contains \"$TPL/docs/engineering/runbook.md\" \"Per-phase subagent isolation evidence (US-0048 / DEC-0029)\""
assert_true "runbook includes isolation reason code ISOLATION_EVIDENCE_INVALID (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"ISOLATION_EVIDENCE_INVALID\""
assert_true "runbook includes isolation reason code ISOLATION_EVIDENCE_INVALID (template)" "file_contains \"$TPL/docs/engineering/runbook.md\" \"ISOLATION_EVIDENCE_INVALID\""

assert_true "verify-work includes isolation compliance gate (active)" "file_contains \"$ROOT/.cursor/commands/verify-work.md\" \"Isolation compliance gate (US-0048 / DEC-0029)\""
assert_true "verify-work includes isolation compliance gate (template)" "file_contains \"$TPL/.cursor/commands/verify-work.md\" \"Isolation compliance gate (US-0048 / DEC-0029)\""

assert_true "release includes isolation compliance gate (active)" "file_contains \"$ROOT/.cursor/commands/release.md\" \"Isolation compliance gate\""
assert_true "release includes isolation compliance gate (template)" "file_contains \"$TPL/.cursor/commands/release.md\" \"Isolation compliance gate\""
assert_true "release includes isolation reason code PHASE_CONTEXT_ISOLATION_MISSING (active)" "file_contains \"$ROOT/.cursor/commands/release.md\" \"PHASE_CONTEXT_ISOLATION_MISSING\""
assert_true "release includes isolation reason code PHASE_CONTEXT_ISOLATION_MISSING (template)" "file_contains \"$TPL/.cursor/commands/release.md\" \"PHASE_CONTEXT_ISOLATION_MISSING\""

assert_true "pause records isolation provenance fields (active)" "file_contains \"$ROOT/.cursor/commands/pause.md\" \"isolation_provenance_ref\""
assert_true "pause records isolation provenance fields (template)" "file_contains \"$TPL/.cursor/commands/pause.md\" \"isolation_provenance_ref\""
assert_true "resume validates isolation provenance (active)" "file_contains \"$ROOT/.cursor/commands/resume.md\" \"Validate isolation provenance (US-0048 / DEC-0029)\""
assert_true "resume validates isolation provenance (template)" "file_contains \"$TPL/.cursor/commands/resume.md\" \"Validate isolation provenance (US-0048 / DEC-0029)\""

assert_true "README documents per-phase isolation evidence (active)" "file_contains \"$ROOT/README.md\" \"Per-phase isolation evidence (US-0048 / DEC-0029)\""
assert_true "README documents per-phase isolation evidence (template)" "file_contains \"$TPL/README.md\" \"Per-phase isolation evidence (US-0048 / DEC-0029)\""

assert_true "dev agent documents isolation evidence (active)" "file_contains \"$ROOT/.cursor/agents/dev.mdc\" \"Isolation evidence (US-0048 / DEC-0029)\""
assert_true "dev agent documents isolation evidence (template)" "file_contains \"$TPL/.cursor/agents/dev.mdc\" \"Isolation evidence (US-0048 / DEC-0029)\""

# 26b) Strict runtime proof checks (US-0056)
assert_true "auto documents strict runtime proof section (active)" "file_contains \"$ROOT/.cursor/commands/auto.md\" \"Strict runtime proof enforcement (US-0056 / DEC-0038)\""
assert_true "auto documents strict runtime proof section (template)" "file_contains \"$TPL/.cursor/commands/auto.md\" \"Strict runtime proof enforcement (US-0056 / DEC-0038)\""
assert_true "auto includes runtime proof reason RUNTIME_PROOF_REUSED (active)" "file_contains \"$ROOT/.cursor/commands/auto.md\" \"RUNTIME_PROOF_REUSED\""
assert_true "auto includes runtime proof reason RUNTIME_PROOF_REUSED (template)" "file_contains \"$TPL/.cursor/commands/auto.md\" \"RUNTIME_PROOF_REUSED\""
assert_true "auto includes strict-proof boundary step 11b (active)" "file_contains \"$ROOT/.cursor/commands/auto.md\" \"11b. At each phase boundary, verify strict runtime attestation tuple exists\""
assert_true "auto includes strict-proof boundary step 11b (template)" "file_contains \"$TPL/.cursor/commands/auto.md\" \"11b. At each phase boundary, verify strict runtime attestation tuple exists\""

assert_true "verify-work documents strict runtime proof gate (active)" "file_contains \"$ROOT/.cursor/commands/verify-work.md\" \"Strict runtime proof gate (US-0056 / DEC-0038)\""
assert_true "verify-work documents strict runtime proof gate (template)" "file_contains \"$TPL/.cursor/commands/verify-work.md\" \"Strict runtime proof gate (US-0056 / DEC-0038)\""
assert_true "release includes strict runtime proof gate (active)" "file_contains \"$ROOT/.cursor/commands/release.md\" \"Strict runtime proof gate (US-0056 / DEC-0038)\""
assert_true "release includes strict runtime proof gate (template)" "file_contains \"$TPL/.cursor/commands/release.md\" \"Strict runtime proof gate (US-0056 / DEC-0038)\""
assert_true "release includes runtime proof reason code RUNTIME_PROOF_MISSING (active)" "file_contains \"$ROOT/.cursor/commands/release.md\" \"RUNTIME_PROOF_MISSING\""
assert_true "release includes runtime proof reason code RUNTIME_PROOF_MISSING (template)" "file_contains \"$TPL/.cursor/commands/release.md\" \"RUNTIME_PROOF_MISSING\""

assert_true "runbook documents strict runtime proof contract (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"Strict runtime proof contract (US-0056 / DEC-0038)\""
assert_true "runbook documents strict runtime proof contract (template)" "file_contains \"$TPL/docs/engineering/runbook.md\" \"Strict runtime proof contract (US-0056 / DEC-0038)\""
assert_true "README documents strict runtime proof section (active)" "file_contains \"$ROOT/README.md\" \"Strict runtime proof (US-0056 / DEC-0038)\""
assert_true "README documents strict runtime proof section (template)" "file_contains \"$TPL/README.md\" \"Strict runtime proof (US-0056 / DEC-0038)\""

# 26c) Strict phase role enforcement checks (US-0069 / DEC-0051)
assert_true "auto documents strict phase role enforcement section (active)" "file_contains \"$ROOT/.cursor/commands/auto.md\" \"Strict phase role enforcement (US-0069 / DEC-0051)\""
assert_true "auto documents strict phase role enforcement section (template)" "file_contains \"$TPL/.cursor/commands/auto.md\" \"Strict phase role enforcement (US-0069 / DEC-0051)\""
assert_true "auto includes PHASE_ROLE_CAPABILITY_MISSING (active)" "file_contains \"$ROOT/.cursor/commands/auto.md\" \"PHASE_ROLE_CAPABILITY_MISSING\""
assert_true "auto includes PHASE_ROLE_MISMATCH (active)" "file_contains \"$ROOT/.cursor/commands/auto.md\" \"PHASE_ROLE_MISMATCH\""
assert_true "auto includes AUTO_ROLE_RESEARCH scratchpad input (active)" "file_contains \"$ROOT/.cursor/commands/auto.md\" \"AUTO_ROLE_RESEARCH\""
assert_true "auto includes EXECUTE_OVERRIDE_GOVERNANCE_REF (template)" "file_contains \"$TPL/.cursor/commands/auto.md\" \"EXECUTE_OVERRIDE_GOVERNANCE_REF\""
assert_true "runbook documents phase role enforcement (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"PHASE_ROLE_CAPABILITY_MISSING\""
assert_true "runbook documents phase role enforcement US-0069 header (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"US-0069 / DEC-0051\""
assert_true "runbook documents phase role enforcement (template)" "file_contains \"$TPL/docs/engineering/runbook.md\" \"PHASE_ROLE_CAPABILITY_MISSING\""
assert_true "runbook documents phase role enforcement US-0069 header (template)" "file_contains \"$TPL/docs/engineering/runbook.md\" \"US-0069 / DEC-0051\""
assert_true "README documents phase role enforcement subsection (active)" "file_contains \"$ROOT/README.md\" \"phase→role enforcement (US-0069 / DEC-0051)\""
assert_true "README documents phase role enforcement subsection (template)" "file_contains \"$TPL/README.md\" \"phase→role enforcement (US-0069 / DEC-0051)\""
assert_true "release isolation gate cites phase role alignment (active)" "file_contains \"$ROOT/.cursor/commands/release.md\" \"Phase role alignment (US-0069 / DEC-0051)\""
assert_true "release strict-proof gate cites role alignment (template)" "file_contains \"$TPL/.cursor/commands/release.md\" \"Strict-proof role alignment (US-0069 / DEC-0051)\""
assert_true "active scratchpad documents AUTO_ROLE_RESEARCH (US-0069)" "file_contains \"$ROOT/.cursor/scratchpad.md\" \"AUTO_ROLE_RESEARCH\""
assert_true "template scratchpad documents AUTO_ROLE_RESEARCH (US-0069)" "file_contains \"$TPL/.cursor/scratchpad.md\" \"AUTO_ROLE_RESEARCH\""

# 26d) Configurable phase selection policy checks (US-0070 / DEC-0052)
assert_true "auto documents US-0070 phase selection section (active)" "file_contains \"$ROOT/.cursor/commands/auto.md\" \"Configurable phase selection policy (US-0070 / DEC-0052)\""
assert_true "auto documents US-0070 phase selection section (template)" "file_contains \"$TPL/.cursor/commands/auto.md\" \"Configurable phase selection policy (US-0070 / DEC-0052)\""
assert_true "auto includes PHASE_POLICY_CONFLICT (active)" "file_contains \"$ROOT/.cursor/commands/auto.md\" \"PHASE_POLICY_CONFLICT\""
assert_true "auto includes START_FROM_PHASE_PLAN_EMPTY_INTERSECTION (template)" "file_contains \"$TPL/.cursor/commands/auto.md\" \"START_FROM_PHASE_PLAN_EMPTY_INTERSECTION\""
assert_true "auto steps reference materialize resolved phase plan (active)" "file_contains \"$ROOT/.cursor/commands/auto.md\" \"materialize the resolved\""
assert_true "auto inputs list AUTO_PHASE_EXCLUDE (active)" "file_contains \"$ROOT/.cursor/commands/auto.md\" \"AUTO_PHASE_EXCLUDE\""
assert_true "runbook documents US-0070 phase plan header (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"phase plan (US-0070 / DEC-0052)\""
assert_true "runbook documents US-0070 phase plan header (template)" "file_contains \"$TPL/docs/engineering/runbook.md\" \"phase plan (US-0070 / DEC-0052)\""
assert_true "README documents US-0070 phase selection subsection (active)" "file_contains \"$ROOT/README.md\" \"phase selection policy (US-0070 / DEC-0052)\""
assert_true "README documents US-0070 phase selection subsection (template)" "file_contains \"$TPL/README.md\" \"phase selection policy (US-0070 / DEC-0052)\""
assert_true "active scratchpad documents AUTO_PHASE_INCLUDE (US-0070)" "file_contains \"$ROOT/.cursor/scratchpad.md\" \"AUTO_PHASE_INCLUDE\""
assert_true "template scratchpad documents AUTO_PHASE_INCLUDE (US-0070)" "file_contains \"$TPL/.cursor/scratchpad.md\" \"AUTO_PHASE_INCLUDE\""
assert_true "active scratchpad.local.example documents AUTO_PHASE_PROFILE (US-0070)" "file_contains \"$ROOT/.cursor/scratchpad.local.example.md\" \"AUTO_PHASE_PROFILE\""
assert_true "template scratchpad.local.example documents AUTO_PHASE_PROFILE (US-0070)" "file_contains \"$TPL/.cursor/scratchpad.local.example.md\" \"AUTO_PHASE_PROFILE\""

# 28) Cross-phase ownership guard and archive verification checks (US-0061)
assert_true "artifact ownership policy exists (active)" "[ -f \"$ROOT/docs/engineering/artifact-ownership-policy.md\" ]"
assert_true "artifact ownership policy exists (template)" "[ -f \"$TPL/docs/engineering/artifact-ownership-policy.md\" ]"
assert_true "ownership policy includes phase ownership violation code (active)" "file_contains \"$ROOT/docs/engineering/artifact-ownership-policy.md\" \"PHASE_OWNERSHIP_VIOLATION\""
assert_true "ownership policy includes architecture history deletion code (template)" "file_contains \"$TPL/docs/engineering/artifact-ownership-policy.md\" \"ARCH_HISTORY_DELETION_DETECTED\""
assert_true "refresh-context includes archive verification fail-safe code (active)" "file_contains \"$ROOT/.cursor/commands/refresh-context.md\" \"STATE_ARCHIVE_VERIFICATION_FAILED\""
assert_true "refresh-context includes archive verification fail-safe code (template)" "file_contains \"$TPL/.cursor/commands/refresh-context.md\" \"STATE_ARCHIVE_VERIFICATION_FAILED\""
assert_true "core rule includes cross-phase ownership guard (active)" "file_contains \"$ROOT/.cursor/rules/core.mdc\" \"Cross-phase artifact ownership guard (US-0061 / DEC-0043)\""
assert_true "core rule includes cross-phase ownership guard (template)" "file_contains \"$TPL/.cursor/rules/core.mdc\" \"Cross-phase artifact ownership guard (US-0061 / DEC-0043)\""
assert_true "runbook documents ownership guard mode (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"Cross-phase artifact ownership guard (US-0061 / DEC-0043)\""
assert_true "README documents ownership guard mode (template)" "file_contains \"$TPL/README.md\" \"Cross-phase artifact ownership guard (US-0061)\""

# 29) Remote runtime connectivity contract checks (US-0064)
assert_true "release-targets includes runtime connectivity doc path (active)" "file_contains \"$ROOT/docs/engineering/release-targets.json\" \"runtimeConnectivityDoc\""
assert_true "release-targets includes runtime mode field (template)" "file_contains \"$TPL/docs/engineering/release-targets.json\" \"\\\"mode\\\": \\\"remote\\\"\""
assert_true "release-targets includes traefik metadata (active)" "file_contains \"$ROOT/docs/engineering/release-targets.json\" \"\\\"traefik\\\"\""
assert_true "release-targets includes docker over ssh metadata (template)" "file_contains \"$TPL/docs/engineering/release-targets.json\" \"\\\"dockerOverSsh\\\"\""
assert_true "runtime connectivity doc exists (active)" "[ -f \"$ROOT/docs/engineering/runtime-connectivity.md\" ]"
assert_true "runtime connectivity doc exists (template)" "[ -f \"$TPL/docs/engineering/runtime-connectivity.md\" ]"
assert_true "release command includes remote connectivity invalid reason (active)" "file_contains \"$ROOT/.cursor/commands/release.md\" \"REMOTE_CONNECTIVITY_CONFIG_INVALID\""
assert_true "qa command includes remote runtime QA contract (active)" "file_contains \"$ROOT/.cursor/commands/qa.md\" \"Optional remote runtime QA/debug contract (US-0064)\""
assert_true "execute command includes remote runtime execution context (template)" "file_contains \"$TPL/.cursor/commands/execute.md\" \"Optional remote runtime execution context (US-0064)\""
assert_true "runbook documents runtime connectivity metadata (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"Connectivity metadata (for operator-safe remote/local context)\""
assert_true "README references runtime connectivity doc (template)" "file_contains \"$TPL/README.md\" \"docs/engineering/runtime-connectivity.md\""

# 30) Release operator hints contract checks (US-0067)
assert_true "release notes template includes Run section (active)" "file_contains \"$ROOT/handoffs/releases/Sxxxx-release-notes.md\" \"## Run\""
assert_true "release notes template includes Connect section (template)" "file_contains \"$TPL/handoffs/releases/Sxxxx-release-notes.md\" \"## Connect\""
assert_true "release notes template includes Verify section (active)" "file_contains \"$ROOT/handoffs/releases/Sxxxx-release-notes.md\" \"## Verify\""
assert_true "release notes template includes health endpoint field (template)" "file_contains \"$TPL/handoffs/releases/Sxxxx-release-notes.md\" \"health_endpoint\""
assert_true "release notes template enforces credentials env-ref guidance (active)" "file_contains \"$ROOT/handoffs/releases/Sxxxx-release-notes.md\" \"env names only\""
assert_true "release command includes operator hints contract section (active)" "file_contains \"$ROOT/.cursor/commands/release.md\" \"Release operator Run/Connect/Verify hints contract (US-0067 / DEC-0049)\""
assert_true "release command includes operator hints missing reason code (template)" "file_contains \"$TPL/.cursor/commands/release.md\" \"RELEASE_OPERATOR_HINTS_MISSING\""
assert_true "release command includes operator hints ambiguous reason code (active)" "file_contains \"$ROOT/.cursor/commands/release.md\" \"RELEASE_OPERATOR_HINTS_AMBIGUOUS\""
assert_true "release command includes operator hints secret exposure reason code (template)" "file_contains \"$TPL/.cursor/commands/release.md\" \"RELEASE_OPERATOR_HINTS_SECRET_EXPOSURE\""
assert_true "legacy release notes pointer includes latest operator summary (active)" "file_contains \"$ROOT/handoffs/release_notes.md\" \"Latest operator summary (Run/Connect/Verify)\""
assert_true "legacy release notes pointer includes latest operator summary (template)" "file_contains \"$TPL/handoffs/release_notes.md\" \"Latest operator summary (Run/Connect/Verify)\""
assert_true "runbook documents release operator hints contract (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"Release operator hints contract (US-0067 / DEC-0049)\""
assert_true "core rule documents release operator hints contract (template)" "file_contains \"$TPL/.cursor/rules/core.mdc\" \"Release operator hints contract (US-0067 / DEC-0049)\""

if [ -f "$ROOT/handoffs/release_queue.md" ] && grep -Eq "^\| S0013 \|.*\| released \|" "$ROOT/handoffs/release_queue.md"; then
  us0041_block="$(awk '
    /^## US-0041/ {in_block=1}
    /^## / && in_block==1 && $0 !~ /^## US-0041/ {in_block=0}
    in_block==1 {print}
  ' "$ROOT/docs/product/backlog.md")"
  if printf "%s\n" "$us0041_block" | grep -q -- "- Status: DONE"; then
    add_result "released sprint S0013 has reconciled backlog DONE state for US-0041" "PASS"
  else
    add_result "released sprint S0013 has reconciled backlog DONE state for US-0041" "FAIL"
  fi
fi

# 26e) User-visible internal metadata guard (US-0071 / DEC-0053)
META_SCRIPT="$ROOT/scripts/check-user-visible-metadata.py"
PY=python3
command -v python3 >/dev/null 2>&1 || PY=python
assert_true "metadata guard script exists" "[ -f \"$META_SCRIPT\" ]"
set +e
"$PY" "$META_SCRIPT" --repo "$ROOT"
META_OK=$?
set -e
assert_true "metadata guard clean repo scan passes" "[ \"$META_OK\" -eq 0 ]"
set +e
"$PY" "$META_SCRIPT" --repo "$ROOT"
META_OK2=$?
set -e
assert_true "metadata guard idempotent rerun passes" "[ \"$META_OK2\" -eq 0 ]"
META_LEAK="$ROOT/tests/.tmp-meta-leak"
rm -rf "$META_LEAK"
mkdir -p "$META_LEAK/bin"
printf '%s\n' 'console.log("US-0999");' > "$META_LEAK/bin/leak-test.js"
set +e
"$PY" "$META_SCRIPT" --repo "$META_LEAK"
META_BAD=$?
set -e
assert_true "metadata guard detects leak in user-visible bin" "[ \"$META_BAD\" -eq 1 ]"
rm -rf "$META_LEAK"
META_ALLOW="$ROOT/tests/.tmp-meta-allow"
rm -rf "$META_ALLOW"
mkdir -p "$META_ALLOW/docs" "$META_ALLOW/bin"
printf '%s\n' 'US-0999' > "$META_ALLOW/docs/internal.md"
printf '%s\n' "console.log('ok');" > "$META_ALLOW/bin/ok.js"
set +e
"$PY" "$META_SCRIPT" --repo "$META_ALLOW"
META_ALLOW_RUN=$?
set -e
assert_true "metadata guard passes when only non-scanned tree has tokens" "[ \"$META_ALLOW_RUN\" -eq 0 ]"
rm -rf "$META_ALLOW"
META_JSC="$ROOT/tests/.tmp-meta-jscomment"
rm -rf "$META_JSC"
mkdir -p "$META_JSC/bin"
printf '%s\n' "// US-0999" "console.log('ok');" > "$META_JSC/bin/c.js"
set +e
"$PY" "$META_SCRIPT" --repo "$META_JSC"
META_JSC_RUN=$?
set -e
assert_true "metadata guard allows JS line comment with token shape" "[ \"$META_JSC_RUN\" -eq 0 ]"
rm -rf "$META_JSC"
assert_true "runbook documents user-visible metadata guard (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"User-visible internal metadata guard (US-0071 / DEC-0053)\""
assert_true "runbook documents user-visible metadata guard (template)" "file_contains \"$TPL/docs/engineering/runbook.md\" \"User-visible internal metadata guard (US-0071 / DEC-0053)\""
assert_true "execute command documents metadata guard step (active)" "file_contains \"$ROOT/.cursor/commands/execute.md\" \"User-visible internal metadata guard (US-0071 / DEC-0053)\""
assert_true "execute command documents metadata guard step (template)" "file_contains \"$TPL/.cursor/commands/execute.md\" \"User-visible internal metadata guard (US-0071 / DEC-0053)\""

# 26f) Triad hot-surface enforcement (DEC-0054)
TRIAD_SCRIPT="$ROOT/scripts/enforce-triad-hot-surface.py"
assert_true "triad enforcement script exists" "test -f \"$TRIAD_SCRIPT\""
set +e
"$PY" "$TRIAD_SCRIPT" --self-test
TRI_SELF=$?
set -e
assert_true "triad self-test passes" "[ \"$TRI_SELF\" -eq 0 ]"
set +e
"$PY" "$TRIAD_SCRIPT" --repo "$ROOT" --check
TRI_CHK=$?
set -e
assert_true "triad check passes on repo" "[ \"$TRI_CHK\" -eq 0 ]"
set +e
"$PY" "$TRIAD_SCRIPT" --repo "$ROOT" --check
TRI_CHK2=$?
set -e
assert_true "triad check idempotent rerun passes" "[ \"$TRI_CHK2\" -eq 0 ]"
assert_true "runbook documents triad enforcement (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"scripts/enforce-triad-hot-surface.py\""
assert_true "runbook documents triad enforcement (template)" "file_contains \"$TPL/docs/engineering/runbook.md\" \"scripts/enforce-triad-hot-surface.py\""
assert_true "runbook documents minimal-read phase table (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"Minimal-read defaults by phase\""
assert_true "phase-context pointer file exists (active)" "test -f \"$ROOT/docs/engineering/phase-context.md\""
assert_true "phase-context pointer file exists (template)" "test -f \"$TPL/docs/engineering/phase-context.md\""
assert_true "scratchpad defines PO_TO_TL hot caps (active)" "file_contains \"$ROOT/.cursor/scratchpad.md\" \"PO_TO_TL_HOT_MAX_LINES\""
assert_true "scratchpad defines PO_TO_TL hot caps (template)" "file_contains \"$TPL/.cursor/scratchpad.md\" \"PO_TO_TL_HOT_MAX_LINES\""
assert_true "execute command documents triad gate (active)" "file_contains \"$ROOT/.cursor/commands/execute.md\" \"enforce-triad-hot-surface.py\""
assert_true "execute command documents triad gate (template)" "file_contains \"$TPL/.cursor/commands/execute.md\" \"enforce-triad-hot-surface.py\""
assert_true "refresh-context documents triad rollover (active)" "file_contains \"$ROOT/.cursor/commands/refresh-context.md\" \"enforce-triad-hot-surface.py\""
assert_true "refresh-context documents triad rollover (template)" "file_contains \"$TPL/.cursor/commands/refresh-context.md\" \"enforce-triad-hot-surface.py\""

# 26g) Scratchpad paired catalog parity (US-0075 / DEC-0057 / AC-11)
PARITY_SCRIPT="$ROOT/scripts/check-scratchpad-pair-parity.py"
assert_true "scratchpad pair parity script exists" "[ -f \"$PARITY_SCRIPT\" ]"
set +e
"$PY" "$PARITY_SCRIPT" --repo "$ROOT"
PARITY_OK=$?
set -e
assert_true "scratchpad pair parity check passes on repo" "[ \"$PARITY_OK\" -eq 0 ]"

# 26h) Merged scratchpad sync gates for validate-and-push (US-0076 / DEC-0058)
SG_SCRIPT="$ROOT/scripts/sync_push_gates.py"
assert_true "sync_push_gates.py exists" "[ -f \"$SG_SCRIPT\" ]"
assert_true "validate-and-push.ps1 invokes sync_push_gates" "file_contains \"$ROOT/scripts/validate-and-push.ps1\" \"sync_push_gates.py\""
assert_true "validate-and-push.sh invokes sync_push_gates" "file_contains \"$ROOT/scripts/validate-and-push.sh\" \"sync_push_gates.py\""
assert_true "runbook documents executable validate-and-push wiring (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"Executable validate-and-push wiring (DEC-0058)\""
assert_true "runbook documents executable validate-and-push wiring (template)" "file_contains \"$TPL/docs/engineering/runbook.md\" \"Executable validate-and-push wiring (DEC-0058)\""

new_sync_fixture() {
  fx="$ROOT/tests/.tmp-sync-gate-$$-$RANDOM"
  rm -rf "$fx"
  mkdir -p "$fx/.cursor" "$fx/docs/engineering" "$fx/sprints/S0001"
  cp "$TPL/.cursor/scratchpad.md" "$fx/.cursor/scratchpad.md"
  cp "$TPL/.cursor/scratchpad.local.example.md" "$fx/.cursor/scratchpad.local.example.md"
  printf "%s\n" "$1" > "$fx/.cursor/scratchpad.local.md"
  printf "TEST_COMMAND: echo ok\nTEST_TIMEOUT_SECONDS: 120\n" > "$fx/docs/engineering/runbook.md"
  printf "# q\n" > "$fx/sprints/S0001/qa-findings.md"
  printf "%s\n" "$fx"
}

FXD=$(new_sync_fixture "SYNC_POLICY_MODE=disabled
ALLOW_AUTO_PUSH=1")
set +e
"$PY" "$SG_SCRIPT" policy --root "$FXD" --branch main >/dev/null 2>&1
SGD=$?
set -e
rm -rf "$FXD"
assert_true "sync_push_gates policy SYNC_DISABLED exit 2" "[ \"$SGD\" -eq 2 ]"

FXE=$(new_sync_fixture "SYNC_POLICY_MODE=by_phase
ALLOW_AUTO_PUSH=1
AUTO_PUSH_BRANCH_ALLOWLIST=*")
set +e
"$PY" "$SG_SCRIPT" policy --root "$FXE" --branch main >/dev/null 2>&1
SGE=$?
"$PY" "$SG_SCRIPT" post --root "$FXE" --branch feature-unit >/dev/null 2>&1
SGP=$?
set -e
rm -rf "$FXE"
assert_true "sync_push_gates policy eligible exit 0" "[ \"$SGE\" -eq 0 ]"
assert_true "sync_push_gates post eligible feature branch exit 0" "[ \"$SGP\" -eq 0 ]"

FXB=$(new_sync_fixture "SYNC_POLICY_MODE=by_phase
ALLOW_AUTO_PUSH=1
AUTO_PUSH_BRANCH_ALLOWLIST=main")
set +e
"$PY" "$SG_SCRIPT" post --root "$FXB" --branch wrong-branch >/dev/null 2>&1
SGB=$?
set -e
rm -rf "$FXB"
assert_true "sync_push_gates post BRANCH_NOT_ALLOWLISTED exit 2" "[ \"$SGB\" -eq 2 ]"

FXQ=$(new_sync_fixture "SYNC_POLICY_MODE=by_phase
ALLOW_AUTO_PUSH=1
AUTO_PUSH_BRANCH_ALLOWLIST=*")
printf "## Blocking\n- [ ] item FAIL\n" > "$FXQ/sprints/S0001/qa-findings.md"
set +e
"$PY" "$SG_SCRIPT" post --root "$FXQ" --branch main >/dev/null 2>&1
SGQ=$?
set -e
rm -rf "$FXQ"
assert_true "sync_push_gates post BLOCKING_QA_FINDINGS exit 2" "[ \"$SGQ\" -eq 2 ]"

FXC=$(new_sync_fixture "SYNC_POLICY_MODE=custom_phase_list
ALLOW_AUTO_PUSH=1
SYNC_CUSTOM_PHASES=qa,execute")
set +e
"$PY" "$SG_SCRIPT" policy --root "$FXC" --branch main >/dev/null 2>&1
SGC=$?
set -e
rm -rf "$FXC"
assert_true "sync_push_gates custom_phase_list without SYNC_PHASE_BOUNDARY exit 2" "[ \"$SGC\" -eq 2 ]"

# 26j) Documentation profile validation (US-0077 / DEC-0059)
DOC_PROFILE_SCRIPT="$ROOT/scripts/validate_doc_profile.py"
DOC_PROFILE_FIXTURES="$ROOT/tests/doc_profile_fixtures_test.py"
command -v python3 >/dev/null 2>&1 || true
[ -z "$PY" ] && PY=python3
command -v python3 >/dev/null 2>&1 || PY=python
assert_true "validate_doc_profile.py exists" "[ -f \"$DOC_PROFILE_SCRIPT\" ]"
assert_true "doc_profile_fixtures_test.py exists" "[ -f \"$DOC_PROFILE_FIXTURES\" ]"
assert_true "scratchpad includes DOC_AUDIENCE_PROFILE (active)" "file_contains \"$ROOT/.cursor/scratchpad.md\" \"DOC_AUDIENCE_PROFILE\""
assert_true "scratchpad includes DOC_AUDIENCE_PROFILE (template)" "file_contains \"$TPL/.cursor/scratchpad.md\" \"DOC_AUDIENCE_PROFILE\""
assert_true "runbook documents doc profile validation (active)" "file_contains \"$ROOT/docs/engineering/runbook.md\" \"Documentation profile validation (US-0077 / DEC-0059)\""
assert_true "runbook documents doc profile validation (template)" "file_contains \"$TPL/docs/engineering/runbook.md\" \"Documentation profile validation (US-0077 / DEC-0059)\""
set +e
"$PY" "$DOC_PROFILE_SCRIPT" --self-test >/dev/null 2>&1
DOC_SELF=$?
set -e
assert_true "validate_doc_profile self-test passes" "[ \"$DOC_SELF\" -eq 0 ]"
set +e
"$PY" "$DOC_PROFILE_SCRIPT" --repo "$ROOT" >/dev/null 2>&1
DOC_REPO=$?
set -e
assert_true "validate_doc_profile passes on repo (template parity)" "[ \"$DOC_REPO\" -eq 0 ]"
set +e
"$PY" "$DOC_PROFILE_FIXTURES" >/dev/null 2>&1
DOC_FIX=$?
set -e
assert_true "doc_profile tiered fixtures pass" "[ \"$DOC_FIX\" -eq 0 ]"

# 26k) Intake evidence validation (US-0078 / DEC-0060 / R-0055 AC-8)
INTAKE_LIB="$ROOT/scripts/intake_evidence_lib.py"
INTAKE_VAL="$ROOT/scripts/intake_evidence_validate.py"
INTAKE_FIX="$ROOT/tests/intake_evidence_fixtures_test.py"
assert_true "intake_evidence_lib.py exists" "[ -f \"$INTAKE_LIB\" ]"
assert_true "intake_evidence_validate.py exists" "[ -f \"$INTAKE_VAL\" ]"
assert_true "intake_evidence_fixtures_test.py exists" "[ -f \"$INTAKE_FIX\" ]"
set +e
"$PY" "$INTAKE_VAL" --self-test >/dev/null 2>&1
IE_SELF=$?
set -e
assert_true "intake_evidence_validate self-test passes" "[ \"$IE_SELF\" -eq 0 ]"
set +e
"$PY" "$INTAKE_FIX" >/dev/null 2>&1
IE_FIX=$?
set -e
assert_true "intake_evidence tiered fixtures pass" "[ \"$IE_FIX\" -eq 0 ]"

# 26R) Intake answer_ref topic distinctness (BUG-0007 / R-0066 / S0068)
BUG0007_R0066_TEST="$ROOT/tests/intake_evidence_bug0007_r0066_test.py"
assert_true "intake_evidence_bug0007_r0066_test.py exists" "[ -f \"$BUG0007_R0066_TEST\" ]"
set +e
"$PY" "$BUG0007_R0066_TEST" >/dev/null 2>&1
BUG0007_R0066_PY=$?
set -e
assert_true "intake BUG-0007 R-0066 matrix passes" "[ \"$BUG0007_R0066_PY\" -eq 0 ]"

# 26L) Bug issues + intake routing (US-0079 / DEC-0061 / R-0056)
BUG_LIB="$ROOT/scripts/bug_issue_lib.py"
BUG_VAL="$ROOT/scripts/bug_issue_validate.py"
BUG_GUARD="$ROOT/scripts/intake_bug_routing_guard.py"
BUG_FIX="$ROOT/tests/bug_issue_fixtures_test.py"
assert_true "bug_issue_lib.py exists" "[ -f \"$BUG_LIB\" ]"
assert_true "bug_issue_validate.py exists" "[ -f \"$BUG_VAL\" ]"
assert_true "intake_bug_routing_guard.py exists" "[ -f \"$BUG_GUARD\" ]"
assert_true "bug_issue_fixtures_test.py exists" "[ -f \"$BUG_FIX\" ]"
set +e
"$PY" "$BUG_VAL" --self-test >/dev/null 2>&1
BUG_SELF=$?
set -e
assert_true "bug_issue_validate self-test passes" "[ \"$BUG_SELF\" -eq 0 ]"
set +e
"$PY" "$BUG_VAL" --backlog "$ROOT/docs/product/backlog.md" --acceptance "$ROOT/docs/product/acceptance.md" --check-acceptance >/dev/null 2>&1
BUG_REPO=$?
set -e
assert_true "bug_issue_validate repo + acceptance reconciliation passes" "[ \"$BUG_REPO\" -eq 0 ]"
set +e
"$PY" "$BUG_FIX" >/dev/null 2>&1
BUG_FIX_RUN=$?
set -e
assert_true "bug_issue tiered fixtures pass" "[ \"$BUG_FIX_RUN\" -eq 0 ]"

# 26N) Intake gate active/template parity (BUG-0001 / DEC-0063 / S0060)
INTAKE_PARITY="$ROOT/scripts/check_intake_template_parity.py"
INTAKE_PARITY_TEST="$ROOT/tests/intake_template_parity_fixtures_test.py"
assert_true "check_intake_template_parity.py exists" "[ -f \"$INTAKE_PARITY\" ]"
assert_true "intake_template_parity_fixtures_test.py exists" "[ -f \"$INTAKE_PARITY_TEST\" ]"
set +e
"$PY" "$INTAKE_PARITY" --repo "$ROOT" >/dev/null 2>&1
INTAKE_PARITY_RUN=$?
set -e
assert_true "intake template parity (scripts vs template/scripts) passes" "[ \"$INTAKE_PARITY_RUN\" -eq 0 ]"
set +e
"$PY" "$INTAKE_PARITY_TEST" >/dev/null 2>&1
INTAKE_PARITY_PY=$?
set -e
assert_true "intake_template_parity fixtures pass" "[ \"$INTAKE_PARITY_PY\" -eq 0 ]"

# 26M) Token-cost parity + metrics harness (US-0080 / DEC-0062)
TCP_PARITY="$ROOT/scripts/check_token_cost_parity.py"
TC_LIB="$ROOT/scripts/token_cost_lib.py"
TC_CMP="$ROOT/scripts/token_cost_compare.py"
TC_TEST="$ROOT/tests/token_cost_fixtures_test.py"
AUTO_CMD_TEST="$ROOT/tests/auto_command_contract_test.py"
assert_true "check_token_cost_parity.py exists" "[ -f \"$TCP_PARITY\" ]"
assert_true "token_cost_lib.py exists" "[ -f \"$TC_LIB\" ]"
assert_true "token_cost_compare.py exists" "[ -f \"$TC_CMP\" ]"
assert_true "token_cost_fixtures_test.py exists" "[ -f \"$TC_TEST\" ]"
assert_true "auto_command_contract_test.py exists" "[ -f \"$AUTO_CMD_TEST\" ]"
set +e
"$PY" "$TCP_PARITY" --repo "$ROOT" >/dev/null 2>&1
TCP_RUN=$?
set -e
assert_true "token-cost active/template parity passes" "[ \"$TCP_RUN\" -eq 0 ]"
set +e
"$PY" "$TC_TEST" >/dev/null 2>&1
TC_FIX_RUN=$?
set -e
assert_true "token_cost fixtures + CLI pass" "[ \"$TC_FIX_RUN\" -eq 0 ]"
set +e
"$PY" "$AUTO_CMD_TEST" >/dev/null 2>&1
AUTO_CMD_RUN=$?
set -e
assert_true "slim auto command contract markers pass" "[ \"$AUTO_CMD_RUN\" -eq 0 ]"

# 26N) Codebase map materialize (US-0082 / DEC-0065)
MAP_MAT="$ROOT/scripts/materialize_codebase_map.py"
MAP_MAT_TEST="$ROOT/tests/codebase_map_materialize_test.py"
assert_true "materialize_codebase_map.py exists" "[ -f \"$MAP_MAT\" ]"
assert_true "codebase_map_materialize_test.py exists" "[ -f \"$MAP_MAT_TEST\" ]"
assert_true "architecture command documents map materialize (active)" "grep -q materialize_codebase_map.py \"$ROOT/.cursor/commands/architecture.md\""
assert_true "architecture command documents map materialize (template)" "grep -q materialize_codebase_map.py \"$TPL/.cursor/commands/architecture.md\""
assert_true "runbook documents codebase map bootstrap (active)" "grep -q 'Codebase map bootstrap (US-0082 / DEC-0065)' \"$ROOT/docs/engineering/runbook.md\""
assert_true "runbook documents codebase map bootstrap (template)" "grep -q 'Codebase map bootstrap (US-0082 / DEC-0065)' \"$TPL/docs/engineering/runbook.md\""
set +e
"$PY" "$MAP_MAT_TEST" >/dev/null 2>&1
MAP_MAT_PY=$?
set -e
assert_true "codebase_map_materialize_test passes" "[ \"$MAP_MAT_PY\" -eq 0 ]"

# 26O) Installer completeness deterministic contract (BUG-0003 / DEC-0066)
INSTALLER_COMPLETENESS_TEST="$ROOT/tests/installer_completeness_bug0003_test.py"
assert_true "installer_completeness_bug0003_test.py exists" "[ -f \"$INSTALLER_COMPLETENESS_TEST\" ]"
set +e
"$PY" "$INSTALLER_COMPLETENESS_TEST" >/dev/null 2>&1
INSTALLER_COMPLETENESS_PY=$?
set -e
assert_true "installer completeness BUG-0003 fixtures pass" "[ \"$INSTALLER_COMPLETENESS_PY\" -eq 0 ]"

# 26P) Installer shell startup compatibility contract (BUG-0004 / DEC-0068) — US-0084 **H1**
#     (LF / forbidden set tokens / optional dash-n via Python test module)
INSTALLER_SHELL_TEST="$ROOT/tests/installer_shell_bug0004_test.py"
assert_true "installer_shell_bug0004_test.py exists" "[ -f \"$INSTALLER_SHELL_TEST\" ]"
set +e
"$PY" "$INSTALLER_SHELL_TEST" >/dev/null 2>&1
INSTALLER_SHELL_PY=$?
set -e
assert_true "installer shell BUG-0004 / US-0084 H1 fixtures pass" "[ \"$INSTALLER_SHELL_PY\" -eq 0 ]"

# 26S) US-0084 / AC-10 **H2** — optional dash -n on installer.sh (explicit harness row)
if command -v dash >/dev/null 2>&1; then
  set +e
  dash -n "$ROOT/installer.sh" >/dev/null 2>&1
  DASH_N_EC=$?
  set -e
  assert_true "US-0084 H2 dash -n installer.sh passes" "[ \"$DASH_N_EC\" -eq 0 ]"
else
  assert_true "US-0084 H2 dash -n skipped (dash not on PATH)" "true"
fi

# 26S2) US-0084 / AC-10 **H3–H5** — remote_config_summary.py fixture exit codes
REMOTE_SUMMARY_TEST="$ROOT/tests/remote_config_summary_test.py"
assert_true "remote_config_summary_test.py exists" "[ -f \"$REMOTE_SUMMARY_TEST\" ]"
set +e
"$PY" "$REMOTE_SUMMARY_TEST" >/dev/null 2>&1
REMOTE_SUMMARY_PY=$?
set -e
assert_true "US-0084 H3-H5 remote_config_summary fixtures pass" "[ \"$REMOTE_SUMMARY_PY\" -eq 0 ]"

# 26Q) Bug-intake resume_brief refresh contract (BUG-0005 / DEC-0069)
INTAKE_RESUME_BRIEF_TEST="$ROOT/tests/intake_bug_resume_brief_bug0005_test.py"
assert_true "intake_bug_resume_brief_bug0005_test.py exists" "[ -f \"$INTAKE_RESUME_BRIEF_TEST\" ]"
assert_true "intake documents DEC-0069 resume_brief refresh script (active)" "file_contains \"$ROOT/.cursor/commands/intake.md\" \"intake_bug_resume_brief_refresh.py\""
assert_true "intake documents DEC-0069 resume_brief refresh script (template)" "file_contains \"$TPL/.cursor/commands/intake.md\" \"intake_bug_resume_brief_refresh.py\""
set +e
"$PY" "$INTAKE_RESUME_BRIEF_TEST" >/dev/null 2>&1
INTAKE_RESUME_BRIEF_PY=$?
set -e
assert_true "intake bug resume_brief BUG-0005 fixtures pass" "[ \"$INTAKE_RESUME_BRIEF_PY\" -eq 0 ]"

timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
{
  echo "# its-magic Test Report"
  echo ""
  echo "Timestamp: $timestamp"
  echo "Pass: $pass"
  echo "Fail: $fail"
  echo ""
  echo "## Results"
  printf "%b\n" "$RESULTS"
} > "$REPORT"

echo "Report written to: $REPORT"
if [ "$fail" -gt 0 ]; then
  exit 1
fi
exit 0
