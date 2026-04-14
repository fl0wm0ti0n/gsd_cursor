# Sprint S0074 UAT -- US-0086

- **Sprint**: `S0074`
- **Work item**: **US-0086** -- automation-driven remote execution selection
- **Orchestrator run**: **auto-20260405-01**
- **Machine-readable**: `sprints/S0074/uat.json`
- **Status**: **PASS** -- 10/10 UAT steps pass
- **Checked at**: `2026-04-13T22:10:00Z`
- **Checked by**: `qa` (fresh context)
- **Canonical backlog**: **`docs/product/backlog.md`** -- **US-0086** **OPEN** (**US-0045**; transitions at `/release`).

## UAT steps (results)

| Step | AC | Result | Summary |
|------|-----|--------|---------|
| UAT-1 | AC-1 | **pass** | Automation profile keys (`AUTO_REMOTE_AUTOMATION_PROFILE`, `AUTO_REMOTE_ENVIRONMENT_LABEL`) are present in active and template scratchpad surfaces with default-off/manual-safe posture. |
| UAT-2 | AC-2 | **pass** | Runbook and template runbook document manual-vs-automation split and operator-safe defaults. |
| UAT-3 | AC-3 | **pass** | Deterministic routing guidance is explicit in command/reference docs and includes mode-off no-reroute behavior. |
| UAT-4 | AC-4 | **pass** | `start container <target_id>` literal and fail-closed reason codes (`REMOTE_AUTOMATION_MODE_OFF`, `REMOTE_TARGET_UNKNOWN`, `REMOTE_TARGET_DISABLED`, `REMOTE_TARGET_UNROUTABLE`) are present in active and template docs. |
| UAT-5 | AC-5 | **pass** | Names-only routing evidence tuple contract is present in QA/dev handoffs and runbook guidance. |
| UAT-6 | AC-6 | **pass** | Deterministic CI routing recipe is documented for remote-capable execution without changing default manual behavior. |
| UAT-7 | AC-7 | **pass** | Security continuity is preserved (`.env` no-read posture, names-only secret surface evidence). |
| UAT-8 | AC-8 | **pass** | Routing contract regressions pass: `python -m pytest tests/auto_command_contract_test.py -q` -> 19 passed, 94 subtests. |
| UAT-9 | AC-9 | **pass** | Architecture lock and decisions alignment remain consistent for US-0086 contract terms and reason-code vocabulary. |
| UAT-10 | AC-10 | **pass** | Active/template parity is preserved across touched command, docs, rules, scratchpad, and handoff surfaces. |

## Results summary

- **Passed**: 10
- **Failed**: 0
- **Total**: 10
- **Verdict**: **PASS**

### QA gate evidence

- **`/qa`** verdict: **PASS** -- `sprints/S0074/qa-findings.md`
- **TEST_COMMAND**: 788 pass / 6 fail (all pre-existing)
- **Contract tests**: 19 passed, 94 subtests
- **Remote summary tests**: 4 passed
- **Scratchpad parity**: `[SCRATCHPAD_PAIR_OK]`
- **Bug validation**: `[BUG_VALIDATION_OK]`
