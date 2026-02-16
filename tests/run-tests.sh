#!/usr/bin/env sh
set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPORT="$ROOT/tests/report.md"
TMP="$ROOT/tests/.tmp-install"

pass=0
fail=0

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
  if sh -c "$condition"; then
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

assert_true "Commands folder exists" "[ -d \"$ROOT/.cursor/commands\" ]"
assert_true "Rules folder exists" "[ -d \"$ROOT/.cursor/rules\" ]"
assert_true "Skills folder exists" "[ -d \"$ROOT/.cursor/skills/team/templates\" ]"
assert_true "Agents folder exists" "[ -d \"$ROOT/.cursor/agents\" ]"
assert_true "Hooks config exists" "[ -f \"$ROOT/.cursor/hooks.json\" ]"
assert_true "Docs folder exists" "[ -d \"$ROOT/docs\" ]"
assert_true "Sprints folder exists" "[ -d \"$ROOT/sprints\" ]"
assert_true "Handoffs folder exists" "[ -d \"$ROOT/handoffs\" ]"
assert_true "Decisions folder exists" "[ -d \"$ROOT/decisions\" ]"
assert_true "Workflows folder exists" "[ -d \"$ROOT/.github/workflows\" ]"

cmd_count=$(ls "$ROOT/.cursor/commands"/*.md 2>/dev/null | wc -l | tr -d ' ')
rule_count=$(ls "$ROOT/.cursor/rules"/*.mdc 2>/dev/null | wc -l | tr -d ' ')
agent_count=$(ls "$ROOT/.cursor/agents"/*.mdc 2>/dev/null | wc -l | tr -d ' ')
assert_true "10 commands exist" "[ $cmd_count -eq 10 ]"
assert_true "4 rules exist" "[ $rule_count -eq 4 ]"
assert_true "6 agents exist" "[ $agent_count -eq 6 ]"

for file in "$ROOT/.cursor/commands"/*.md; do
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

runbook="$ROOT/docs/engineering/runbook.md"
assert_true "Runbook contains TEST_COMMAND" "file_contains \"$runbook\" \"TEST_COMMAND\""
assert_true "Runbook contains LINT_COMMAND" "file_contains \"$runbook\" \"LINT_COMMAND\""
assert_true "Runbook contains TYPECHECK_COMMAND" "file_contains \"$runbook\" \"TYPECHECK_COMMAND\""
assert_true "Runbook contains DEPLOY_STAGING_COMMAND" "file_contains \"$runbook\" \"DEPLOY_STAGING_COMMAND\""
assert_true "Runbook contains DEPLOY_PROD_COMMAND" "file_contains \"$runbook\" \"DEPLOY_PROD_COMMAND\""

ci="$ROOT/.github/workflows/ci.yml"
deploy="$ROOT/.github/workflows/deploy.yml"
assert_true "CI workflow references TEST_COMMAND" "file_contains \"$ci\" \"TEST_COMMAND\""
assert_true "CI workflow references LINT_COMMAND" "file_contains \"$ci\" \"LINT_COMMAND\""
assert_true "CI workflow references TYPECHECK_COMMAND" "file_contains \"$ci\" \"TYPECHECK_COMMAND\""
assert_true "Deploy workflow references DEPLOY_STAGING_COMMAND" "file_contains \"$deploy\" \"DEPLOY_STAGING_COMMAND\""
assert_true "Deploy workflow references DEPLOY_PROD_COMMAND" "file_contains \"$deploy\" \"DEPLOY_PROD_COMMAND\""

rm -rf "$TMP"
mkdir -p "$TMP"
if [ -f "$ROOT/installer.sh" ]; then
  sh "$ROOT/installer.sh" --target "$TMP" --mode missing --create >/dev/null
  assert_true "Installer (sh) installs commands" "[ -f \"$TMP/.cursor/commands/intake.md\" ]"
else
  assert_true "Installer (sh) exists" "false"
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

