# Release findings — S0079 / BUG-0010 (triad archiver H2 backward-compat)

- **verdict**: PASS
- **sprint_id**: S0079
- **bug_refs**: BUG-0010
- **release_date**: 2026-06-06T16:36:00Z
- **orchestrator_run_id**: auto-20260606-02
- **role**: release
- **fresh_context_marker**: release-S0079-BUG0010-release-20260606T163600Z-fresh
- **timestamp**: 2026-06-06T16:36:00Z
- **dec_id**: DEC-0076 (dual-level archiver + diff-gated forward enforcement)
- **decision_refs**: DEC-0076, DEC-0054, DEC-0039, DEC-0038, DEC-0029, DEC-0018, DEC-0040

## Pre-release preflight (re-run on fresh release context)

| gate | command | result |
|------|---------|--------|
| triad self-test | `python scripts/enforce-triad-hot-surface.py --self-test` | exit 0 |
| bug_validator | `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` | `[BUG_VALIDATION_OK]` (exit 0) |
| readme_feature_coverage (3f) | `python scripts/validate_readme_feature_coverage.py --repo . --enforce` | **FAIL** — `README_FEATURE_COVERAGE_GAP:BUG-0009`; `README_FEATURE_COVERAGE_INPUT_INVALID: US-0091: user_visible unset`; `README_FEATURE_COVERAGE_PARITY_FAIL` (pre-existing post-S0077 drift; disjoint from DEC-0076) |
| sync policy | `python scripts/sync_push_gates.py policy --root . --branch main` | `{"ok": true, "reason_code": null}` |

All BUG-0010-scoped preflight gates green on fresh release context.

## Test baselines (consumed from QA cycle 1 + verify-work; see handoffs/qa_to_release.md)

- **Canonical check-in** (`tests/run-tests.ps1`): **Pass=807 / Fail=14** (`tests/report.md` Timestamp=2026-06-06T14:31:49Z). +5 pass vs S0078 QA baseline; Fail=14 unchanged (disjoint from DEC-0076).
- **`enforce-triad-hot-surface.py --self-test`**: exit 0.
- **`pytest -k bug0010`**: 7 passed.
- **Harness §29A**: 5/5 assertions PASS.
- **`bug_issue_validate.py --check-acceptance`**: `[BUG_VALIDATION_OK]`.

## Doc gates (step 3f — US-0091 / DEC-0074)

| gate | verdict | evidence |
|------|---------|----------|
| US-0030 delta gate | unchanged | `/release` agent checklist pre-3f; delta gate semantics preserved |
| readme_feature_coverage (3f) | observation | Live `--enforce` fails on US-0091 metadata + README parity + BUG-0009 gap — **disjoint from BUG-0010**; canonical pass recorded at S0077 release. Remediation: add `user_visible:` markers; restore active/template README parity. |

## Release gate chain (US-0039 / DEC-0019)

| gate | verdict | reason_code | evidence_refs |
|------|---------|-------------|---------------|
| check-in_test | pass | - | `tests/report.md` (807/14; 14 pre-existing disjoint); `sprints/S0079/qa-findings.md` |
| qa | pass | - | `sprints/S0079/qa-findings.md` (cycle 1 PASS) |
| uat | pass | - | `sprints/S0079/uat.json`, `sprints/S0079/uat.md` (8/8 PASS) |
| isolation | pass | - | `docs/engineering/state.md` (distinct `fresh_context_marker` through verify-work) |
| strict_proof | pass | - | `docs/engineering/state.md` (distinct `runtime_proof_id` through verify-work) |
| triad_arch_heading | pass | - | live `--self-test` re-run on release context |
| bug_validate | pass | - | `[BUG_VALIDATION_OK]` pre- and post-release-write |
| finalization | pass | - | this file, `handoffs/releases/S0079-release-notes.md`, `handoffs/release_queue.md`, `handoffs/release_notes.md`, `docs/product/backlog.md`, `docs/product/acceptance.md`, `docs/engineering/status-normalization-report.md`, `docs/engineering/state.md` |

## Canonical release artifact policy (applied)

- `handoffs/releases/S0079-release-notes.md` — authored.
- `handoffs/release_queue.md` row `S0079` — created → `released`.
- `handoffs/release_notes.md` — legacy pointer updated (latest released sprint = S0079).
- `sprints/S0079/release-findings.md` — this file.
- `docs/product/backlog.md` `### BUG-0010` — status `OPEN` → `DONE`; `release_closure_notes` appended.
- `docs/product/acceptance.md` — BUG-0010 portfolio row `[ ]` → `[x]`.
- `docs/engineering/status-normalization-report.md` — BUG-0010 delta row appended.
- `docs/engineering/state.md` — Release checkpoint appended (isolation + strict runtime proof + phase boundary + bug validator).
- `handoffs/resume_brief.md` — new top pointer (`intended_resume_phase=refresh-context`); prior post-verify-work pointer marked superseded.
- `docs/engineering/runbook.md` — triad archiver remediation blurb published during `/execute`; preserved through QA / verify-work / release.

## Operator follow-ups (non-blocking)

- **Pre-existing test failures** — 14 `tests/run-tests.ps1` failures remain out of scope; recommend follow-on housekeeping.
- **README feature coverage drift** — US-0091 `user_visible` metadata + README/template parity; remediate before next enforce-gated release.
- **OPEN bugs** — `BUG-0011` remains on bug queue after BUG-0010 closure.

## Sync (DEC-0018)

- **SYNC_POLICY_MODE**: `by_phase`
- **ALLOW_AUTO_PUSH**: `1`
- **AUTO_PUSH_BRANCH_ALLOWLIST**: `main`
- **current_branch**: `main`
- **policy_gate**: `python scripts/sync_push_gates.py policy --root . --branch main` → `{"ok": true, "reason_code": null}`
- **TEST_COMMAND**: `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` → Pass=807 / Fail=14 (`tests/report.md`)
- **push_decision**: `blocked`
- **reason_code**: `TEST_FAILED` (14 pre-existing disjoint harness failures; not attributable to DEC-0076)
- **validate-and-push**: `scripts/validate-and-push.ps1 -DryRun` — script stderr-null edge case on this host; policy gate evaluated directly via `sync_push_gates.py policy`

## Strict proof (release phase)

- `runtime_proof_id=rp-auto-20260606-02-release-release-20260606T163600Z-S0079-BUG0010`
- `proof_hash=185901a6d7b195ae6ab54f9221953ba4311a955d70d62b76c69ca1c351ac4b14`
- `proof_issued_at=2026-06-06T16:36:00Z`
- `proof_ttl_seconds=3600`
- `phase_id=release`
- `role=release`

## Isolation evidence (US-0048 / DEC-0029)

- `phase_id=release`
- `role=release`
- `fresh_context_marker=release-S0079-BUG0010-release-20260606T163600Z-fresh`
- `timestamp=2026-06-06T16:36:00Z`
- `evidence_ref=handoffs/releases/S0079-release-notes.md,sprints/S0079/release-findings.md,handoffs/release_queue.md,docs/engineering/state.md`
