# Handoff: QA -> Dev (US-0109 / S0109)

- from: qa
- to: dev
- story_id: US-0109
- sprint_id: S0109
- dec_id: DEC-0109
- orchestrator_run_id: auto-20260628-04
- verdict: FAIL
- blocking_findings: 2

## Blocking Issues to Fix

### BF-1: Compose-guard test FAIL (AC-7)

`test_us0109_us0054_compose_no_publish_semantics_change` fails because `scripts/self_healing_deploy_lib.py` contains the token `RELEASE_PUBLISH_OK` in docstrings (lines 6, 308). The compose-guard test treats this as a forbidden token.

**Preferred remediation**: Remove `[RELEASE_PUBLISH_OK]` literal from `self_healing_deploy_lib.py` docstrings. Replace with generic phrasing like "post-publish boundary" or "after successful publish". Also remove from docstring line 308 (`run_smoke_probe_chain` docstring).

After fixing: re-run `pytest tests/us0109_contract_test.py -v` — all 11 must PASS.

### BF-2: Runbook parity FAIL (AC-8)

`docs/engineering/runbook.md` (155699b) != `template/docs/engineering/runbook.md` (145161b). The US-0109 operator remediation section was added to active runbook but not synced to template.

**Remediation**: Copy `docs/engineering/runbook.md` -> `template/docs/engineering/runbook.md`.

After fixing: re-run `python scripts/check_intake_template_parity.py --scope=sovereign-self-healing-deploy` — must exit 0.

## Non-Blocking (FYI)

- NBF-1: Consider narrowing the compose-guard token check to skip docstring/comment lines.

## Resume After Fix

- Re-run `/qa` in a fresh QA subagent. All 11 pytest tests must PASS and all 6 parity pairs must MATCH.
