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
  if sh -c "$condition" >/dev/null 2>&1; then
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
assert_true "22 commands exist" "[ $cmd_count -eq 22 ]"
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
if [ -f "$ROOT/installer.sh" ]; then
  run_with_timeout sh "$ROOT/installer.sh" --target "$TMP" --mode missing --create < /dev/null >/dev/null
  assert_true "Installer (sh) installs commands" "[ -f \"$TMP/.cursor/commands/intake.md\" ]"
else
  assert_true "Installer (sh) exists" "false"
fi

# Upgrade mode test
UPGRADE_TMP="$ROOT/tests/.tmp-upgrade"
rm -rf "$UPGRADE_TMP"
mkdir -p "$UPGRADE_TMP"

if [ -f "$ROOT/installer.sh" ]; then
  run_with_timeout sh "$ROOT/installer.sh" --target "$UPGRADE_TMP" --mode missing --create < /dev/null >/dev/null

  assert_true "Version file written on install" "[ -f \"$UPGRADE_TMP/.its-magic-version\" ]"

  echo "# My Custom Vision" > "$UPGRADE_TMP/docs/product/vision.md"

  echo "modified-framework" > "$UPGRADE_TMP/.cursor/commands/intake.md"

  run_with_timeout sh "$ROOT/installer.sh" --target "$UPGRADE_TMP" --mode upgrade < /dev/null >/dev/null

  assert_true "Upgrade restores framework files" "! grep -q 'modified-framework' \"$UPGRADE_TMP/.cursor/commands/intake.md\""
  assert_true "Upgrade preserves user data" "grep -q 'My Custom Vision' \"$UPGRADE_TMP/docs/product/vision.md\""
  assert_true "Version file updated after upgrade" "[ -f \"$UPGRADE_TMP/.its-magic-version\" ]"
fi

# Clean-repo safety test (direct installer path)
CLEAN_TMP="$ROOT/tests/.tmp-cleanrepo"
rm -rf "$CLEAN_TMP"
mkdir -p "$CLEAN_TMP"
if [ -f "$ROOT/installer.sh" ]; then
  run_with_timeout sh "$ROOT/installer.sh" --target "$CLEAN_TMP" --mode missing --create < /dev/null >/dev/null
  mkdir -p "$CLEAN_TMP/src"
  echo "non-framework marker" > "$CLEAN_TMP/src/keep.txt"
  run_with_timeout sh "$ROOT/installer.sh" --target "$CLEAN_TMP" --clean-repo --yes < /dev/null >/dev/null
  assert_true "Clean-repo removes framework artifacts (installer)" "[ ! -d \"$CLEAN_TMP/.cursor\" ]"
  assert_true "Clean-repo preserves non-framework marker (installer)" "[ -f \"$CLEAN_TMP/src/keep.txt\" ]"
fi

# CLI lifecycle tests (`its-magic` command path)
CLI_ENTRY="$ROOT/bin/its-magic.js"
CLI_TMP="$ROOT/tests/.tmp-cli-lifecycle"
rm -rf "$CLI_TMP"
mkdir -p "$CLI_TMP"
if [ -f "$CLI_ENTRY" ] && command -v node >/dev/null 2>&1; then
  run_with_timeout node "$CLI_ENTRY" --target "$CLI_TMP" --mode missing --create < /dev/null >/dev/null
  assert_true "CLI missing install writes version file" "[ -f \"$CLI_TMP/.its-magic-version\" ]"
  assert_true "CLI missing install writes command file" "[ -f \"$CLI_TMP/.cursor/commands/intake.md\" ]"

  echo "cli-overwrite-marker" > "$CLI_TMP/.cursor/commands/intake.md"
  run_with_timeout node "$CLI_ENTRY" --target "$CLI_TMP" --mode overwrite --backup < /dev/null >/dev/null
  assert_true "CLI overwrite mode creates backup snapshot" "ls \"$CLI_TMP/backups\"/*/.cursor/commands/intake.md >/dev/null 2>&1"

  echo "# CLI User Data Marker" > "$CLI_TMP/docs/product/vision.md"
  echo "cli-upgrade-framework-marker" > "$CLI_TMP/.cursor/commands/intake.md"
  run_with_timeout node "$CLI_ENTRY" --target "$CLI_TMP" --mode upgrade < /dev/null >/dev/null
  assert_true "CLI upgrade restores framework files" "! grep -q 'cli-upgrade-framework-marker' \"$CLI_TMP/.cursor/commands/intake.md\""
  assert_true "CLI upgrade preserves user data" "grep -q 'CLI User Data Marker' \"$CLI_TMP/docs/product/vision.md\""

  mkdir -p "$CLI_TMP/src"
  echo "cli-marker" > "$CLI_TMP/src/keep.txt"
  run_with_timeout node "$CLI_ENTRY" --clean-repo --target "$CLI_TMP" --yes < /dev/null >/dev/null
  assert_true "CLI clean-repo removes framework artifacts" "[ ! -d \"$CLI_TMP/.cursor\" ]"
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

# Auto continuation deterministic contract checks (US-0037)
assert_true "auto includes explicit start-from contract (active)" "file_contains \"$ROOT/.cursor/commands/auto.md\" \"start-from=<phase>\""
assert_true "auto includes explicit start-from contract (template)" "file_contains \"$TPL/.cursor/commands/auto.md\" \"start-from=<phase>\""

assert_true "auto precedence includes argument > resume > state (active)" "file_contains \"$ROOT/.cursor/commands/auto.md\" \"explicit \`/auto start-from=<phase>\`\""
assert_true "auto precedence includes argument > resume > state (template)" "file_contains \"$TPL/.cursor/commands/auto.md\" \"explicit \`/auto start-from=<phase>\`\""

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
assert_true "status normalization report contains baseline row (template)" "file_contains \"$TPL/docs/engineering/status-normalization-report.md\" \"US-0018\""

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
