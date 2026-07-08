# Release Notes — S0120 / US-0120

- **Sprint**: `S0120`
- **Story**: `US-0120` — Dedicated `/closure` phase with exclusive Story Closure responsibility
- **Release date**: 2026-07-08 (UTC; 2026-07-08T19:45:00Z UTC)
- **orchestrator_run_id**: `auto-20260708-01`
- **delivery_mode**: `ultra_lean`
- **macro_phase**: `ship` (first of three ship phases: release → closure → refresh-context per DEC-0082)
- **policy_mode**: `disabled` (`RELEASE_PUBLISH_MODE=disabled`)
- **trigger_source**: `auto`
- **branch**: `local` (no push; `SYNC_POLICY_MODE=disabled` per DEC-0018)
- **fresh_context_marker**: `release-US0120-release-20260708T194500Z-fresh`
- **runtime_proof_id**: `rp-auto-20260708-01-release-release-20260708T194500Z-US-0120`
- **release_version**: (none — governance-only; no version bump)

## Summary

Ship the dedicated **`/closure`** phase as the second step of the 3-phase ship macro (`[release, closure, refresh-context]` per DEC-0082). US-0120 is governance-only: adds `.cursor/commands/closure.md` (+ template parity), updates DEC-0052 (closure|qe) and DEC-0082 (ship macro), removes backlog reconciliation steps 10–12 from `release.md` (now owned exclusively by `/closure`), adds `scripts/validate_closure_verification.py`, 10 contract tests in `tests/us0120_closure_phase_test.py`, runbook `## Story closure (US-0120)`, and backward-compat drain hook (3-signal detection for in-flight stories). Compose guards 6/6 UNCHANGED.

**US-0120 backlog status intentionally retained OPEN** and acceptance unchecked — Story Closure (OPEN→DONE, `[ ]`→`[x]`) is deferred to `/closure` per US-0120 design.

## ACs satisfied

**12/12 PASS** (QA-verified; release re-ran contract tests):

| AC | Description | Status |
|----|-------------|--------|
| AC-1 | `/closure` command file (active + template) | PASS |
| AC-2 | DEC-0052 phase→role matrix includes closure\|qe | PASS |
| AC-3 | DEC-0082 ship macro [release, closure, refresh-context] | PASS |
| AC-4 | `/auto` phase plan includes closure after release | PASS |
| AC-5 | `release.md` steps 10–12 reconciliation removed | PASS |
| AC-6 | closure-verification.md schema + validator | PASS |
| AC-7 | closure isolation evidence contract | PASS |
| AC-8 | closure runtime proof contract | PASS |
| AC-9 | contract tests (10 markers) | PASS |
| AC-10 | backward-compat drain hook | PASS |
| AC-11 | architecture + runbook + command documentation | PASS |
| AC-12 | compose guards 6/6 UNCHANGED | PASS |

## Files shipped

- `.cursor/commands/closure.md` + `template/.cursor/commands/closure.md` (NEW, byte-identical 8949b)
- `scripts/validate_closure_verification.py` + template mirror (NEW, 9960b PARITY_OK)
- `tests/us0120_closure_phase_test.py` (NEW — 10 markers)
- `decisions/DEC-0052.md`, `decisions/DEC-0082.md` (EDIT — additive)
- `.cursor/commands/auto.md`, `release.md` + templates (EDIT — closure spawn; steps 10–12 removed)
- `scripts/check_intake_template_parity.py` + template (EDIT — `--scope=us-0120`)
- `docs/engineering/context/installer-owned-paths.manifest` (EDIT)
- `docs/engineering/runbook.md` — `## Story closure (US-0120)` L3775

## Test results (release re-run)

```
python -m pytest tests/us0120_closure_phase_test.py -v
  → 10 passed in 0.08s
```

## Validator outputs (release re-run)

```
python scripts/validate_closure_verification.py --self-test
  → [VALIDATE_CLOSURE_VERIFICATION_SELF_TEST_OK]  exit 0

python scripts/check_intake_template_parity.py --repo . --scope=us-0120
  → [INTAKE_TEMPLATE_PARITY_OK] scope=us-0120  exit 0

python scripts/validate_readme_feature_coverage.py --repo . --enforce
  → [README_FEATURE_COVERAGE_VALIDATE_OK]  exit 0

python scripts/validate_project_readme_coverage.py --repo . --enforce
  → kit_repo_skipped (FRAMEWORK_KIT_REPO=1)  exit 0

python scripts/validate_doc_profile.py --repo .
  → [DOC_PROFILE_VALIDATE_OK]  exit 0

python scripts/check-user-visible-metadata.py --repo .
  → silent PASS  exit 0
```

## Compose guards

**6/6 UNCHANGED** — US-0043, US-0045, US-0040, US-0048, US-0056, US-0096 verified read-only.

## Gate summary

| Gate | Result |
|------|--------|
| check_in_tests | PASS (10/10 us0120_closure_phase_test) |
| qa | QA_PASS (`sprints/S0120/qa-findings.md`) |
| verify_work | PASS (`sprints/S0120/verify-work-findings.md`) |
| uat | PASS (12/12 `sprints/S0120/uat.json`) |
| isolation_evidence | PASS (execute + qa in state.md) |
| strict_runtime_proof | PASS (execute + qa tuples consumed) |
| readme_feature_coverage_3f | PASS |
| project_readme_3g | PASS (kit_repo_skipped) |
| backlog_reconciliation | **deferred** to `/closure` |
| publish | skipped (`RELEASE_PUBLISH_MODE=disabled`) |
| sync | not_eligible (`SYNC_DISABLED`) |

## Run

```powershell
python -m pytest tests/us0120_closure_phase_test.py -v
python scripts/validate_closure_verification.py --self-test
```

Expected: 10 passed, `[VALIDATE_CLOSURE_VERIFICATION_SELF_TEST_OK]`

## Connect

- **runtime_mode**: `local`
- **runtime_context_ref**: governance repo — no external service endpoint
- Ship macro position: phase 1 of 3 (`release` → `closure` → `refresh-context`)

## Verify

1. `python -m pytest tests/us0120_closure_phase_test.py -v` → 10 passed
2. `python scripts/validate_closure_verification.py --self-test` → exit 0
3. Confirm `release.md` step 10 points to `/closure` (steps 10–12 reconciliation removed)
4. Confirm `auto.md` ship macro includes `closure` after `release`
5. Confirm US-0120 remains **OPEN** in `docs/product/backlog.md` until `/closure` runs

## Credentials

Not applicable (governance-only; no external secrets).

## Known Issues

None blocking. Non-blocking: pre-existing triad oversize on `state.md` (not US-0120 regression).

## Isolation evidence (US-0048 / DEC-0029)

- `phase_id=release`
- `role=release`
- `fresh_context_marker=release-US0120-release-20260708T194500Z-fresh`
- `timestamp=2026-07-08T19:45:00Z`
- `evidence_ref=sprints/S0120/release-findings.md` + `sprints/S0120/release-verdict.json` + this file

## Strict runtime proof (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260708-01`
- `runtime_proof_id=rp-auto-20260708-01-release-release-20260708T194500Z-US-0120`
- `phase_id=release`
- `role=release`
- `proof_issued_at=2026-07-08T19:45:00Z`
- `proof_hash=982f4a5fe047111a689d57bb562caf410b6cb98df99fd49aa575072ec49b1c17`
- `proof_ttl_seconds=3600`
- `proof_ttl=2026-07-08T20:45:00Z` (UTC)

## Verdict

**RELEASE_PASS.** 12/12 ACs satisfied. All gates green. Backlog reconciliation **deferred** to `/closure` (US-0120 design). Story remains OPEN; acceptance unchecked. Publish skipped (disabled). Sync skipped (disabled).

## Next

**`/closure`** (fresh **qe** subagent, ship macro — second canonical phase per DEC-0082). Closure owns: backlog OPEN→DONE, acceptance tick, `sprints/S0120/closure-verification.md`, closure checkpoint in state.md.
