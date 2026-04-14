# QA Findings -- S0074 / US-0086

- **sprint_id**: S0074
- **story_id**: US-0086
- **qa_phase**: qa
- **qa_role**: qa
- **qa_timestamp**: 2026-04-13T21:22:07Z
- **orchestrator_run_id**: auto-20260405-01
- **verdict**: **PASS**

## Test plan

| Check | Tool / command | Expected | Actual | Result |
|-------|---------------|----------|--------|--------|
| TEST_COMMAND (canonical) | `tests/run-tests.ps1` | no new failures | 788 pass, 6 fail (all pre-existing) | **PASS** |
| Auto command contract | `python -m pytest tests/auto_command_contract_test.py -q` | all pass | 19 passed, 94 subtests passed | **PASS** |
| Remote config summary tests | `python -m pytest tests/remote_config_summary_test.py -q` | all pass | 4 passed | **PASS** |

## Test results summary

- `tests/run-tests.ps1`: 788 pass, 6 fail
- `auto_command_contract_test.py`: 19 passed, 94 subtests passed
- `remote_config_summary_test.py`: 4 passed
- New failures introduced by US-0086 QA run: 0

## Pre-existing failures (not introduced by US-0086)

| Test assertion | Cause | Severity |
|---|---|---|
| Installer runbook TEST_COMMAND present for detectable stack | Pre-existing install fixture stack-detection drift | Low |
| CLI missing install runbook TEST_COMMAND present | Same pre-existing install fixture stack-detection drift | Low |
| auto includes strict-proof boundary step 11b (active) | Pre-existing token expectation drift from compacted step references | Low |
| auto includes strict-proof boundary step 11b (template) | Same pre-existing token expectation drift in template copy | Low |
| triad check passes on repo | Hot surface oversize in `docs/engineering/state.md` (requires rollover in refresh-context) | Low |
| triad check idempotent rerun passes | Same hot surface oversize precondition as above | Low |

## AC verification

| AC | Criterion | Verified | Evidence |
|----|-----------|----------|----------|
| AC-1 | Scratchpad automation-profile keys present in active + template | **PASS** | `.cursor/scratchpad.md`, `template/.cursor/scratchpad.md`, `.cursor/scratchpad.local.example.md`, `template/.cursor/scratchpad.local.example.md` |
| AC-2 | Runbook separates manual vs automation mode in active + template | **PASS** | `docs/engineering/runbook.md`, `template/docs/engineering/runbook.md` |
| AC-3 | Deterministic routing guidance added to commands/rules in active + template | **PASS** | `.cursor/commands/auto.md`, `template/.cursor/commands/auto.md`, `.cursor/rules/coding-standards.mdc`, `template/.cursor/rules/coding-standards.mdc` |
| AC-4 | Deterministic `start container <target_id>` contract + fail-closed reason codes documented | **PASS** | `.cursor/commands/auto.md`, `docs/engineering/auto-orchestration-reference.md`, template counterparts |
| AC-5 | Handoff/state guidance includes names-only routing tuple contract | **PASS** | `handoffs/dev_to_qa.md`, `handoffs/qa_to_verify_work.md`, `docs/engineering/runbook.md` |
| AC-6 | Optional deterministic CI routing recipe documented | **PASS** | `docs/engineering/runbook.md`, `template/docs/engineering/runbook.md`, runtime-connectivity docs |
| AC-7 | Security continuity (`.env` no-read, names-only secret posture) preserved | **PASS** | `coding-standards.mdc` + runbook updates (active/template) |
| AC-8 | Regression coverage for routing contract present and passing | **PASS** | `tests/auto_command_contract_test.py` result 19/19 pass |
| AC-9 | Architecture lock consistency maintained (US-0064/DEC-0070 alignment) | **PASS** | `docs/engineering/architecture.md`, `docs/engineering/decisions.md`, backlog notes |
| AC-10 | Active/template parity sweep complete on touched surfaces | **PASS** | execute summary/handoff + contract test coverage |

## Blocking findings

None.

## QA verdict

**PASS** -- AC-1..AC-10 verified; no new failures introduced by US-0086. Ready for `/verify-work`.
