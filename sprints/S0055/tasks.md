# Sprint S0055 Tasks

- Story: `US-0076`
- Sprint: `S0055`
- Governance: **`DEC-0058`** (executable merged-scratchpad wiring for **validate-and-push**); policy authority **`DEC-0018`** / **`US-0038`**; merge precedence **`DEC-0055`**

| Task | Status | Description | AC |
|---|---|---|---|
| T-001 | done | Implement **default-off** and **disabled/manual** short-circuit: when **`ALLOW_AUTO_PUSH=0`** or **`SYNC_POLICY_MODE`** is **`disabled`** / **`manual`**, **no push**; exit with deterministic **`SYNC_DISABLED`**, **`MANUAL_MODE_NO_AUTO`**, or **`AUTO_PUSH_NOT_ENABLED`** (aligned with **`DEC-0018`**) | AC-1 |
| T-002 | done | Integrate **merged scratchpad** (local → materialized baseline → example per **`DEC-0055`**) for **`SYNC_POLICY_MODE`**, **`SYNC_CUSTOM_PHASES`** (when **`custom_phase_list`**), **`ALLOW_AUTO_PUSH`**, **`AUTO_PUSH_BRANCH_ALLOWLIST`**; **fail closed** on parse/merge errors with **`[SCRATCHPAD_MERGE_ERROR]`**-class remediation; reuse **`installer.py`** merge (or shared helper) — **no** duplicate precedence logic | AC-2 |
| T-003 | done | Enforce **US-0038** check order after policy allows push attempt: **`TEST_COMMAND`** from **`runbook.md`** (required); optional lint/typecheck when set; emit **`TEST_COMMAND_MISSING`**, **`TEST_FAILED`**, **`TEST_TIMEOUT`**, **`OPTIONAL_CHECK_FAILED`** as applicable | AC-3 |
| T-004 | done | **Branch safety**: deterministic allowlist match for current branch; **`BRANCH_NOT_ALLOWLISTED`** and **no push** on mismatch; document match rules in runbook | AC-4 |
| T-005 | done | Implement bounded **QA / blocking scan** per **`DEC-0058`** §6 (glob **`sprints/S*/qa-findings.md`**, blocking markers); emit **`BLOCKING_QA_FINDINGS`**; implement **`PRE_QA_AUTOPUSH_FORBIDDEN`** per runbook-documented bounded **feature / QA-cleared** rule without weakening blocking semantics | AC-5 |
| T-006 | done | Keep **`validate-and-push.ps1`** and **`validate-and-push.sh`** **behaviorally aligned** for scratchpad-driven gates, exit codes, and reason tokens (**cross-platform parity**) | AC-6 |
| T-007 | done | Update **`docs/engineering/runbook.md`**, **`README.md`**, and **`template/`** mirrors: scratchpad **alone** does not push; **run** validate-and-push after eligible boundaries; **`by_phase`** / **`by_milestone`** / **`custom_phase_list`** → operator vs CI scheduling; document optional **`SYNC_PHASE_BOUNDARY`** env (**`DEC-0058`** §4) and **dry-run** flag | AC-7 |
| T-008 | done | Add **regression coverage** in **`tests/run-tests.ps1`** / **`.sh`**: disabled/manual → no push path (dry-run or spy); allowlist mismatch → **`BRANCH_NOT_ALLOWLISTED`**; optional **qa-findings** fixture → **`BLOCKING_QA_FINDINGS`**; **PS1/sh** parity where feasible | AC-8 |
| T-009 | done | Verify **US-0071**: scan new/changed operator-visible strings from scripts for forbidden internal planning-token patterns; fix any violations | AC-9 |
| T-010 | done | **AC-10 closure**: ensure operator docs and sprint/release surfaces **cite `DEC-0058`**, overlap with **`US-0038`**, and **deprecation** of policy-only interpretation for push scripts (per decision §8); cross-link **`DEC-0018`** as policy authority | AC-10 |

## Deterministic AC-to-task mapping

- AC-1 → T-001
- AC-2 → T-002
- AC-3 → T-003
- AC-4 → T-004
- AC-5 → T-005
- AC-6 → T-006
- AC-7 → T-007
- AC-8 → T-008
- AC-9 → T-009
- AC-10 → T-010
