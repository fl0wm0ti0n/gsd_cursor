# Sprint S0053 QA Findings

- Story: `US-0074`
- Sprint: `S0053`
- Result: **PASS**

## Test plan

- Consolidated suite: `powershell -ExecutionPolicy Bypass -File tests/run-tests.ps1` (exit `0`).
- User-visible metadata guard: `python scripts/check-user-visible-metadata.py` (exit `0`).
- Triad hot-surface enforcement: `python scripts/enforce-triad-hot-surface.py --check` (exit `0`).
- Validated implementation against **US-0074** AC-1..AC-10, **`DEC-0056`**, **`DEC-0046`**, and sprint tasks **T-001..T-010**.

## Command results

| Command | Exit | Notes |
|--------|------|--------|
| `tests/run-tests.ps1` | 0 | `tests/report.md`: **Pass: 710**, **Fail: 0**, `Timestamp: 2026-03-21T16:04:30Z` |
| `python scripts/check-user-visible-metadata.py` | 0 | No forbidden tokens in scanned operator-visible surfaces (US-0071 guard) |
| `python scripts/enforce-triad-hot-surface.py --check` | 0 | Hot surfaces within policy (**DEC-0054**) |

## AC-7 — Known four-check baseline set (zero failures)

Backlog **US-0074** names four baseline asserts; consolidated runner rows (all **PASS**):

| # | Baseline check (backlog wording) | Report row label | Result |
|---|----------------------------------|------------------|--------|
| 1 | `Homebrew stable formula URL uses npm version tag` | `Homebrew stable formula URL uses npm version tag` | **PASS** |
| 2 | `Homebrew stable formula version matches npm version` | `Homebrew stable formula version matches npm version` | **PASS** |
| 3 | `Installer bootstraps TEST_COMMAND for detectable stack` | `Installer runbook TEST_COMMAND present for detectable stack (npm or sh template default)` | **PASS** |
| 4 | `CLI missing install bootstraps TEST_COMMAND for detectable stack` | `CLI missing install runbook TEST_COMMAND present (npm or sh template default)` | **PASS** |

**Failures in this four-check set: 0.**

## Acceptance validation (US-0074)

- **AC-1**: **PASS** — Root-cause classification and owning paths documented in product backlog discovery notes, **`R-0051`** (post-discovery US-0074), **`DEC-0056`**, architecture **`# US-0074`**, and `handoffs/dev_to_qa.md` / execute checkpoint in `docs/engineering/state.md`.
- **AC-2**: **PASS** — `tests/report.md` Homebrew URL + version rows **PASS**; formula literals aligned with `package.json` per dev handoff (`packaging/homebrew/its-magic.rb`).
- **AC-3**: **PASS** — Installer and CLI missing-install paths materialize runbook `TEST_COMMAND` per detectable stack; evidenced by matching **PASS** rows in `tests/report.md` and **`DEC-0056`** / runbook bootstrap contract.
- **AC-4**: **PASS** — Full green suite (710/0) preserves upgrade/install/scratchpad lifecycle checks (e.g. US-0073 manifest rows, upgrade preserves user data); no ownership-contract regressions observed in runner.
- **AC-5**: **PASS** — Cross-platform bootstrap contract satisfied in tests for PS1/py/sh installer paths and CLI missing-install; parity described in `handoffs/dev_to_qa.md` and **`DEC-0056`**.
- **AC-6**: **PASS** — Assertions remain strict (710 **PASS**, 0 **FAIL**); no masked or skipped baseline rows for the former four failures.
- **AC-7**: **PASS** — See table above: **zero** failures across the four named baseline checks; evidence `tests/report.md` (timestamp as cited).
- **AC-8**: **PASS** — Runner includes active + `template/` parity checks for runbook, commands, and related surfaces; dev handoff lists template/active runbook alignment.
- **AC-9**: **PASS** — Auditable evidence: `tests/report.md` (all four checks **PASS**) and this `sprints/S0053/qa-findings.md`; release-note pointers finalized under **`/verify-work`** / **`/release`** per workflow.
- **AC-10**: **PASS** — Remediation and contract narrative in `decisions/DEC-0056.md`, `docs/engineering/architecture.md` (`# US-0074`), and runbook `TEST_COMMAND` bootstrap note (**DEC-0056**).

## Verdict

- QA verdict for **`S0053`** / **`US-0074`**: **PASS**.
- Blocking in-scope findings: **none**.
- Recommended next phase: **`/verify-work`** (canonical backlog **DONE** transition and acceptance checkboxes).
