# Sprint S0049 QA Findings

- Story: `US-0070`
- Sprint: `S0049`
- Result: PASS

## Test plan

- Execute baseline regression command and collect report evidence:
  `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"`.
- Validate execute outputs against `US-0070` acceptance criteria across sprint
  artifacts, `/auto` phase-selection contract (DEC-0052), runbook/README,
  scratchpad parity, and regression section **26d** in both test runners (per
  `handoffs/dev_to_qa.md`).

## Findings

- Baseline command executed:
  `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` (exit code `1`).
- Evidence: `tests/report.md` (`Timestamp: 2026-03-20T21:19:34Z`, `Pass: 673`,
  `Fail: 4`).
- In-scope US-0070 regression checks (**26d**) are **PASS** in `tests/report.md`:
  - `Configurable phase selection policy (US-0070 / DEC-0052)` in `auto.md`
    (active/template)
  - US-0070 phase plan header in runbook (active/template)
  - US-0070 phase selection subsection in README (active/template)
  - `AUTO_PHASE_INCLUDE` / `AUTO_PHASE_PROFILE` in scratchpad examples
    (active/template)
- Contract surface validation PASS (spot-check + dev handoff list):
  - `.cursor/commands/auto.md` + template: phase policy modes, plan
    materialization, non-skippable reinstatement, `start-from` intersection,
    fail-closed reason codes, backlog-drain/bulk boundary reload, boundary status.
  - Scratchpad + `scratchpad.local.example` + template: `AUTO_PHASE_*` contract.
  - `docs/engineering/runbook.md` + template: phase plan operator guidance.
  - `README.md` + template: phase selection policy pointers.
  - `tests/run-tests.ps1`, `tests/run-tests.sh`: **26d** assertions present and green.
- Sprint execute artifacts reviewed: `sprints/S0049/sprint.md`,
  `sprints/S0049/tasks.md`, `sprints/S0049/progress.md`, `handoffs/dev_to_qa.md` —
  consistent with delivered scope (`T-001..T-010` done).
- Out-of-scope baseline failures (not treated as `US-0070` blockers):
  - `Homebrew stable formula URL uses npm version tag`
  - `Homebrew stable formula version matches npm version`
  - `Installer bootstraps TEST_COMMAND for detectable stack`
  - `CLI missing install bootstraps TEST_COMMAND for detectable stack`

## Acceptance validation (US-0070)

- AC-1: PASS — canonical scratchpad phase policy (`AUTO_PHASE_PLAN` /
  `EXCLUDE` / `INCLUDE` / `PROFILE`) with single active mode and conflict
  fail-closed in `/auto` + examples.
- AC-2: PASS — resolved plan + breadcrumbs before spawn documented in `/auto`.
- AC-3: PASS — unknown/invalid tokens and related fail-fast codes documented.
- AC-4: PASS — non-skippable gates and reinstatement semantics documented.
- AC-5: PASS — `start-from` intersection and empty-intersection fail-closed
  documented.
- AC-6: PASS — backlog-drain / bulk / team paths aligned with policy reload in
  `/auto` steps.
- AC-7: PASS — resume / continuation parity with phase policy recomputation
  documented.
- AC-8: PASS — active/template parity for listed surfaces (tests + spot-check).
- AC-9: PASS — section **26d** assertions PASS in `tests/report.md`.
- AC-10: PASS — phase boundary operator-visible status contract in `/auto`.

## Verdict

- QA verdict for `S0049` / `US-0070`: **PASS**.
- Blocking findings in-scope: **none**.
- Deterministic blocker reason code: **not applicable** (no in-scope blockers).
- Recommended next phase: **`/verify-work`**.
