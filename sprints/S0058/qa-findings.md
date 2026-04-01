# Sprint S0058 — QA findings

- **Story**: `US-0079` — First-class bug issue workflow (`BUG-####`, `OPEN`/`DONE`)
- **Sprint**: `S0058`
- **Orchestrator run**: `orchestrator_run_id=auto-20260329-01`
- **QA phase**: `/qa` (fresh **qa** context)
- **Overall verdict**: **PASS**
- **Evidence reviewed**: `handoffs/dev_to_qa.md`, `sprints/S0058/tasks.md`, `sprints/S0058/sprint.md`, `decisions/DEC-0061.md`, `docs/engineering/architecture.md` (`# US-0079`), `docs/engineering/research.md` (`R-0056`), `scripts/bug_issue_lib.py`, `scripts/bug_issue_validate.py`, `scripts/intake_bug_routing_guard.py`, `.cursor/commands/intake.md` / `ask.md` (bug routing + narrow-read), `docs/product/backlog.md` (`## Bug issues (canonical)`), `docs/product/acceptance.md` (`## Bug acceptance (canonical)`), `template/` parity (spot vs dev handoff)

## Traceability convention (US-0042 / DEC-0061)

When recording defects found during QA, reference **`BUG-xxxx`** (canonical bug issues) or **`US-xxxx`** (feature stories) with explicit evidence pointers — example row shape:

| Finding | Severity | IDs | Evidence |
|---------|----------|-----|----------|
| (none) | — | — | — |

## Test plan (executed)

| Step | Command / check | Result |
|------|-----------------|--------|
| Validator self-test | `python scripts/bug_issue_validate.py --self-test` | **PASS** (`[BUG_VALIDATION_OK]`) |
| Backlog + acceptance reconcile | `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` | **PASS** (`[BUG_VALIDATION_OK]`) |
| Fixture / Tier matrix | `python tests/bug_issue_fixtures_test.py` | **PASS** (`[BUG_ISSUE_FIXTURES_OK]`) |
| Full harness | `powershell -ExecutionPolicy Bypass -File tests/run-tests.ps1` | **Exit 1** — see non-blocking baseline below |

**Non-blocking (out of scope for US-0079)**: `tests/report.md` (**2026-03-29T20:23:46Z**) reports **758 pass / 2 fail** — both failures are **Homebrew stable formula** URL/version vs **npm** tag checks, unrelated to bug-issue validators or §26L. All **§26L** / **BUG_** / **INTAKE_BUG_ROUTING** paths in the run output are **PASS** (mirrors **S0057** QA treatment of unrelated baseline noise).

## Per-AC verdicts

| AC | Verdict | Notes |
|----|---------|-------|
| **AC-1** | **PASS** | Canonical `## Bug issues (canonical)` + allocator (`bug_issue_validate.py --print-next-id`); `BUG-####` distinct from `US-xxxx`. |
| **AC-2** | **PASS** | `INTAKE_WORK_ITEM_KIND`, `/intake bug`, `intake_bug_routing_guard.py` — fail-closed `INTAKE_BUG_ROUTING_REQUIRED`; no silent US allocation. |
| **AC-3** | **PASS** | Validators + docs enforce `OPEN`/`DONE` only (`BUG_VALIDATION_STATUS_INVALID` family). |
| **AC-4** | **PASS** | Required fields + non-empty `evidence_refs`; deterministic `BUG_VALIDATION_*` / reconcile codes. |
| **AC-5** | **PASS** | `tasks.md` / sprint surfaces reference `BUG-xxxx` traceability without US conversion. |
| **AC-6** | **PASS** | This file + `summary.md` document `BUG-xxxx` alongside `US-xxxx` for QA/release-style rows. |
| **AC-7** | **PASS** | `--check-acceptance` reconciles bug family vs `## Bug acceptance (canonical)`; US-only reconciliation preserved. |
| **AC-8** | **PASS** | `ask.md` narrow-read includes `BUG-####` under canonical bug region. |
| **AC-9** | **PASS** | Dev handoff list + spot-check: active + `template/` commands/rules/runbook/README/scratchpad parity. |
| **AC-10** | **PASS** | **`DEC-0061`**, **`architecture.md`** **`# US-0079`**, **`decisions.md`** index — traceability and policy closure. |

## Verdict

- **PASS** — no blocking findings; **`next_scheduled_phase=verify-work`** at QA write time (per **US-0045** / **US-0078** precedent: portfolio **`acceptance.md`** **US-0079** checked at **`/verify-work`** — see **`sprints/S0058/uat.md`**).
