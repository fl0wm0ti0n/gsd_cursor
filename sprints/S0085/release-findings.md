# Release Findings — S0085 / BUG-0012

## Metadata

- **sprint_id**: S0085
- **bug_id**: BUG-0012
- **dec_id**: DEC-0081
- **research_anchor**: R-0083
- **role**: release
- **timestamp**: 2026-06-13T01:30:00Z
- **orchestrator_run_id**: auto-20260612-01
- **fresh_context_marker**: release-S0085-BUG0012-release-20260613T013000Z-fresh

## Gate status

**PASS** — All mandatory release gates green; **BUG-0012** closed **DONE** per **US-0045**.

## Per-gate audit verdict (US-0039)

| gate | verdict | reason_code | remediation | evidence_refs |
|------|---------|-------------|-------------|---------------|
| check-in_test | pass | (none) | — | `pytest -k "bug0012 or us0095"` 12 passed |
| qa | pass | (none) | — | `sprints/S0085/qa-findings.md` |
| uat | pass | (none) | — | `sprints/S0085/uat.json` 8/8; UAT-8 procedural attestation |
| isolation | pass | (none) | — | `docs/engineering/state.md` execute/qa/verify-work markers |
| strict_proof | pass | (none) | — | verify-work `proof_hash=ea5744b4…`; release proof below |
| readme_feature_coverage_3f | observation | README_FEATURE_COVERAGE_BLOCKED | post-S0077 drift; not in-scope blocker | `validate_readme_feature_coverage.py --enforce` |
| bug_validate | pass | (none) | — | `[BUG_VALIDATION_OK]` post-closure |
| finalization | pass | (none) | — | this file, `handoffs/releases/S0085-release-notes.md`, queue row |

## Blocking findings

**None**

## Non-blocking observations

- **readme_feature_coverage_3f**: live `--enforce` reports broad `coverage_missing` (106 DONE items without ID markers in README family). Pre-existing post-**S0077** drift; prior releases (**S0080**, **S0078**, **S0081**) classified as observation, not blocker. **BUG-0012** (`user_visible: true`) not in enforce set until closure; README backfill deferred to portfolio hygiene sprint.

## Release gate chain evidence

| Check | Result |
|-------|--------|
| `pytest -k "bug0012 or us0095" tests/auto_command_contract_test.py` | **12 passed**, 50 subtests |
| `python scripts/check_intake_template_parity.py --scope=bug-0012` | `[INTAKE_TEMPLATE_PARITY_OK]` |
| `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` | `[BUG_VALIDATION_OK]` (post-closure) |
| UAT | **8/8 PASS** |
| Plan-verify | **PASS** (`sprints/S0085/plan-verify.json`) |
| Isolation | **PASS** (distinct `fresh_context_marker` per phase) |

## Strict proof (release phase)

- `orchestrator_run_id=auto-20260612-01`
- `runtime_proof_id=rp-auto-20260612-01-release-release-20260613T013000Z-S0085-BUG0012`
- `phase_id=release`
- `role=release`
- `proof_issued_at=2026-06-13T01:30:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=44b55cf523c1c6721f1b9e359e683a9216379d5b314f401b0a722f667f51afe2`

Canonical payload: `{"orchestrator_run_id":"auto-20260612-01","phase_id":"release","proof_issued_at":"2026-06-13T01:30:00Z","proof_ttl_seconds":3600,"role":"release","runtime_proof_id":"rp-auto-20260612-01-release-release-20260613T013000Z-S0085-BUG0012"}`.

**Boundary verification (release boundary; upstream verify-work consumed)**: prior verify-work checkpoint `qa-S0085-BUG0012-verify-work-20260613T001500Z-fresh` / `proof_hash=ea5744b4ba3b6643b80ea0aeb296898894276c7e8f9e276f6de8ca27a1844375`.

## Backlog reconciliation (US-0043 / US-0045)

- **BUG-0012**: `OPEN` → **DONE** in `docs/product/backlog.md`
- **acceptance**: `docs/product/acceptance.md` **BUG-0012** row checked
- **release_queue**: **S0085** → **`released`**

## Publish / sync snapshot

- `RELEASE_PUBLISH_MODE=confirm` → `publish_snapshot=skipped_pending_operator_confirm`
- `SYNC_POLICY_MODE=disabled` → `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`

## Next phase

- **`/refresh-context`** (fresh **curator**)
