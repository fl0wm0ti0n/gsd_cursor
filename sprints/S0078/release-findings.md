# Release findings — S0078 / BUG-0009 (downstream CI packaging leak)

- **verdict**: PASS
- **sprint_id**: S0078
- **bug_refs**: BUG-0009
- **release_date**: 2026-06-06T16:15:00Z
- **orchestrator_run_id**: auto-20260606-02
- **role**: release
- **fresh_context_marker**: release-S0078-BUG0009-release-20260606T161500Z-fresh
- **timestamp**: 2026-06-06T16:15:00Z
- **dec_id**: DEC-0075 (US-0017 negative-parity exceptions)
- **decision_refs**: DEC-0075, DEC-0039, DEC-0038, DEC-0029, DEC-0018, DEC-0040

## Pre-release preflight (re-run on fresh release context)

| gate | command | result |
|------|---------|--------|
| downstream_ci_guard | `python scripts/check_downstream_ci_guard.py --self-test` | `[DOWNSTREAM_CI_GUARD_SELF_TEST_OK]` (exit 0) |
| downstream_ci_guard report | `python scripts/check_downstream_ci_guard.py --repo . --report` | `ok=true`; `template_job_keys=[checks,auto-fix]`; active five jobs; `forbidden_hits=[]` |
| parity (downstream-ci-guard) | `python scripts/check_intake_template_parity.py --scope=downstream-ci-guard` | `[INTAKE_TEMPLATE_PARITY_OK]` (exit 0) |
| bug_validator | `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` | `[BUG_VALIDATION_OK]` (exit 0) |
| readme_feature_coverage (3f) | `python scripts/validate_readme_feature_coverage.py --repo . --enforce` | **FAIL** — `README_FEATURE_COVERAGE_INPUT_INVALID: US-0091: user_visible unset`; `README_FEATURE_COVERAGE_PARITY_FAIL: README.md != template/README.md` (pre-existing post-S0077 drift; disjoint from DEC-0075) |
| sync policy | `python scripts/sync_push_gates.py policy --root . --branch main` | `{"ok": true, "reason_code": null}` |

All BUG-0009-scoped preflight gates green on fresh release context.

## Test baselines (consumed from QA cycle 1 + verify-work; see handoffs/qa_to_release.md)

- **Canonical check-in** (`tests/run-tests.ps1`): **Pass=802 / Fail=14** (`tests/report.md` Timestamp=2026-06-06T14:08:25Z). +5 fail vs S0077 QA baseline Fail=9; disjoint from DEC-0075 deliverables.
- **`check_downstream_ci_guard.py`**: self-test OK; `--report` `ok=true`.
- **`pytest -k bug0009`**: 6 passed.
- **`pytest -k downstream_ci`**: 2 passed.
- **`bug_issue_validate.py --check-acceptance`**: `[BUG_VALIDATION_OK]`.

## Doc gates (step 3f — US-0091 / DEC-0074)

| gate | verdict | evidence |
|------|---------|----------|
| US-0030 delta gate | unchanged | `/release` agent checklist pre-3f; delta gate semantics preserved |
| readme_feature_coverage (3f) | observation | Live `--enforce` fails on US-0091 metadata + README parity — **disjoint from BUG-0009**; canonical pass recorded at S0077 release (`sprints/S0077/release-findings.md` §Doc gates, `2026-06-06T13:43:20Z`). Remediation: add `user_visible:` to US-0091 backlog block; restore active/template README parity. |

## Release gate chain (US-0039 / DEC-0019)

| gate | verdict | reason_code | evidence_refs |
|------|---------|-------------|---------------|
| check-in_test | pass | - | `tests/report.md` (802/14; 14 pre-existing disjoint); `sprints/S0078/qa-findings.md` |
| qa | pass | - | `sprints/S0078/qa-findings.md` (cycle 1 PASS) |
| uat | pass | - | `sprints/S0078/uat.json`, `sprints/S0078/uat.md` (8/8 PASS) |
| isolation | pass | - | `docs/engineering/state.md` (distinct `fresh_context_marker` through verify-work) |
| strict_proof | pass | - | `docs/engineering/state.md` (distinct `runtime_proof_id` through verify-work) |
| downstream_ci_guard | pass | - | live self-test + `--report` re-run on release context |
| bug_validate | pass | - | `[BUG_VALIDATION_OK]` pre- and post-release-write |
| finalization | pass | - | this file, `handoffs/releases/S0078-release-notes.md`, `handoffs/release_queue.md`, `handoffs/release_notes.md`, `docs/product/backlog.md`, `docs/product/acceptance.md`, `docs/engineering/status-normalization-report.md`, `docs/engineering/state.md` |

## Canonical release artifact policy (applied)

- `handoffs/releases/S0078-release-notes.md` — authored.
- `handoffs/release_queue.md` row `S0078` — `ready` → `released`.
- `handoffs/release_notes.md` — legacy pointer updated (latest released sprint = S0078).
- `sprints/S0078/release-findings.md` — this file.
- `docs/product/backlog.md` `### BUG-0009` — status `OPEN` → `DONE`; `release_closure_notes` appended.
- `docs/product/acceptance.md` — BUG-0009 portfolio row `[ ]` → `[x]`.
- `docs/engineering/status-normalization-report.md` — BUG-0009 delta row appended.
- `docs/engineering/state.md` — Release checkpoint prepended (isolation + strict runtime proof + phase boundary + bug validator).
- `handoffs/resume_brief.md` — new top pointer (`intended_resume_phase=refresh-context`); prior post-verify-work pointer marked superseded.
- `docs/engineering/runbook.md` — downstream CI remediation subsection published during `/execute`; preserved through QA / verify-work / release.

## Operator follow-ups (non-blocking)

- **Pre-existing test failures** — 14 `tests/run-tests.ps1` failures remain out of scope; recommend follow-on housekeeping.
- **README feature coverage drift** — US-0091 `user_visible` metadata + README/template parity; remediate before next enforce-gated release.
- **OPEN bugs** — `BUG-0010`, `BUG-0011` remain on bug queue after BUG-0009 closure.

## Sync (DEC-0018)

- **SYNC_POLICY_MODE**: `by_phase`
- **ALLOW_AUTO_PUSH**: `1`
- **AUTO_PUSH_BRANCH_ALLOWLIST**: `main`
- **current_branch**: `main`
- **policy_gate**: `python scripts/sync_push_gates.py policy --root . --branch main` → `{"ok": true, "reason_code": null}`
- **post_test_gate**: not executed (uncommitted local release artifacts; canonical harness exit non-zero on 14 pre-existing failures)
- **push_decision**: `blocked`
- **reason_code**: `TEST_FAILED` (canonical `tests/run-tests.ps1` reports Fail=14 at `tests/report.md` Timestamp=2026-06-06T14:08:25Z; failures disjoint from BUG-0009 surface)
- **remediation**: operator may commit release artifacts and re-run `scripts/validate-and-push.ps1` after triaging pre-existing harness failures, or accept local-only release finalization per prior sprint precedent.

## Publish (RELEASE_PUBLISH_MODE=confirm)

- **publish_snapshot**: `skipped_pending_operator_confirm`
- No publish scripts were executed by the release agent. Operator confirmation is required before any publish target.

## Isolation evidence (US-0048 / DEC-0029)

- `phase_id=release`
- `role=release`
- `fresh_context_marker=release-S0078-BUG0009-release-20260606T161500Z-fresh`
- `timestamp=2026-06-06T16:15:00Z`
- `evidence_ref=[sprints/S0078/release-findings.md, handoffs/releases/S0078-release-notes.md]`

## Strict runtime proof (US-0056 / DEC-0038)

- `runtime_proof_id=rp-auto-20260606-02-release-release-20260606T161500Z-S0078-BUG0009`
- canonical JSON tuple = `{"orchestrator_run_id":"auto-20260606-02","phase_id":"release","proof_issued_at":"2026-06-06T16:15:00Z","proof_ttl_seconds":3600,"role":"release","runtime_proof_id":"rp-auto-20260606-02-release-release-20260606T161500Z-S0078-BUG0009"}`
- `proof_hash=ca36057ca8aff89ceee48d2474bf84c5533f777c9f9cd194a1c18ef8425484bc` (SHA-256 of sorted-key JSON)
- Linkage to prior verify-work proof `rp-auto-20260606-02-verify-work-qa-20260606T161030Z-S0078-BUG0009` via shared `orchestrator_run_id=auto-20260606-02`
