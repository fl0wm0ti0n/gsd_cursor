# QA findings — S0055 / US-0076

- **Sprint**: S0055
- **Story**: US-0076 (executable scratchpad-driven sync / validate-and-push)
- **Governance**: DEC-0058 (DEC-0018 policy authority; DEC-0055 merge)
- **Verdict**: **PASS** (no blocking defects for US-0076 scope)
- **Reviewed**: 2026-03-27 (QA subagent, `orchestrator_run_id=auto-20260327-01`)

## Evidence (commands)

| Check | Command | Result |
|--------|---------|--------|
| Full PS suite | `powershell -ExecutionPolicy Bypass -File tests/run-tests.ps1` | **721 PASS**, **2 FAIL** (Homebrew stable vs npm only; pre-existing **US-0074** baseline per `handoffs/dev_to_qa.md`) |
| US-0076 fixtures (26h) | Same run — `tests/report.md` | All **sync_push_gates** / runbook / invoke asserts **PASS** |
| US-0071 metadata | `python scripts/check-user-visible-metadata.py` | Exit **0** |

**Report**: `tests/report.md` (timestamp **2026-03-27T20:45:00Z**).

## Acceptance criteria

| AC | Verdict | Notes |
|----|---------|--------|
| AC-1 | **PASS** | Policy short-circuit reason codes exercised in **26h** (`SYNC_DISABLED` exit 2); implementation in `scripts/sync_push_gates.py` + wrappers. |
| AC-2 | **PASS** | Merge via installer path only (`sync_push_gates`); **DEC-0055** alignment; fail-closed merge errors documented in runbook. |
| AC-3 | **PASS** | `validate-and-push.*` requires **TEST_COMMAND** from runbook; optional lint/typecheck; reason codes aligned with **US-0038**. |
| AC-4 | **PASS** | **26h** asserts `BRANCH_NOT_ALLOWLISTED` exit 2 on post gate; runbook documents allowlist behavior. |
| AC-5 | **PASS** | Glob `sprints/S*/qa-findings.md` + **DEC-0058** §6 markers; **26h** `BLOCKING_QA_FINDINGS` exit 2; `PRE_QA_AUTOPUSH_FORBIDDEN` per runbook bounded rule. |
| AC-6 | **PASS** | PS1 + bash scripts both invoke `sync_push_gates.py`; tests assert wiring + exit parity where covered. |
| AC-7 | **PASS** | Runbook **Executable validate-and-push wiring (DEC-0058)** + README/template; scheduling + optional `SYNC_PHASE_BOUNDARY` documented. |
| AC-8 | **PASS** | **26h** regression block in `tests/run-tests.ps1` / `.sh` (policy, post, custom_phase_list without boundary). |
| AC-9 | **PASS** | Dedicated metadata script **PASS** on scanned roots; no new forbidden-token violations attributed to this story. |
| AC-10 | **PASS** | **`decisions/DEC-0058.md`** accepted; deprecation of policy-only interpretation §8; **US-0038** cross-linked as policy authority. |

## Non-blocking observations

- **Homebrew vs npm** version asserts remain **FAIL** until packaging alignment (**US-0074**); excluded from US-0076 gate.
- Optional doc hygiene: any remaining `sh scripts/validate-and-push.sh` references elsewhere could be aligned to **bash** (dev follow-up in sprint summary); not required for AC-6 given explicit bash contract in runbook/scripts.

## Sprint task alignment

All **T-001..T-010** marked **done** in `sprints/S0055/tasks.md` — consistent with AC sign-off above.
