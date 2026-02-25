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
  if eval "$condition"; then
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

ci="$TPL/.github/workflows/ci.yml"
deploy="$TPL/.github/workflows/deploy.yml"
assert_true "CI workflow references TEST_COMMAND" "file_contains \"$ci\" \"TEST_COMMAND\""
assert_true "CI workflow references LINT_COMMAND" "file_contains \"$ci\" \"LINT_COMMAND\""
assert_true "CI workflow references TYPECHECK_COMMAND" "file_contains \"$ci\" \"TYPECHECK_COMMAND\""
assert_true "Deploy workflow references DEPLOY_STAGING_COMMAND" "file_contains \"$deploy\" \"DEPLOY_STAGING_COMMAND\""
assert_true "Deploy workflow references DEPLOY_PROD_COMMAND" "file_contains \"$deploy\" \"DEPLOY_PROD_COMMAND\""

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

rm -rf "$TMP" "$UPGRADE_TMP"

# Memory-audit command checks (US-0024)
assert_true "memory-audit command exists (active)" "[ -f \"$ROOT/.cursor/commands/memory-audit.md\" ]"
assert_true "memory-audit command exists (template)" "[ -f \"$TPL/.cursor/commands/memory-audit.md\" ]"

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
