# Release Notes — S0114 / US-0114

- **Sprint**: `S0114`
- **Story**: `US-0114` — Release & distribution operator documentation in framework README
- **Release date**: 2026-07-04 (UTC)
- **orchestrator_run_id**: `auto-20260704-01`
- **delivery_mode**: `ultra_lean`
- **macro_phase**: `ship` (first canonical phase — release)
- **policy_mode**: `disabled` (`RELEASE_PUBLISH_MODE=disabled`)
- **trigger_source**: `manual` (`RELEASE_TRIGGER_SOURCE=manual`)
- **branch**: `local` (no push; `SYNC_POLICY_MODE=disabled` per DEC-0018)
- **fresh_context_marker**: `release-S0114-US0114-20260704T071200Z-fresh`
- **runtime_proof_id**: `rp-auto-20260704-01-release-release-20260704T071200Z-US-0114`
- **release_version**: (none — documentation-only; no version bump)

## Summary

Close the operator-documentation gap for the **release & distribution family** (US-0041, US-0062, US-0111, US-0112) in the framework README pair (`its_magic/README.md` ↔ `template/its_magic/README.md`). Added `### Release & distribution (US-0041 / US-0062 / US-0111 / US-0112)` umbrella section under `## Commands and workflow` (sibling to US-0113's sovereign-loop umbrella), 4 nested `#### US-xxxx` operator subsections (US-id-ascending: US-0041 → US-0062 → US-0111 → US-0112; release-workflow angle with bidirectional "see US-0113 for sovereign-loop angle" pointers for US-0111/US-0112), and `### Release & distribution keys (US-0041 / US-0062 / US-0111 / US-0112)` sub-block in `### Full scratchpad reference (detailed)` (net-new US-0062 keys only + grouped cross-links + cross-link pointers to US-0113's block for overlap keys). US-0113 byte-stability preserved (pure addition; no edits to US-0113's umbrella or scratchpad keys block). Default-off posture preserved; zero new scratchpad keys introduced.

## ACs satisfied

**8/8 PASS** (independently re-verified by QA; release re-ran all gates):

| AC | Description | Status |
|----|-------------|--------|
| AC-1 | `### Release & distribution umbrella section` under `## Commands and workflow` | PASS |
| AC-2 | Per-feature operator subsections for US-0041/US-0062/US-0111/US-0112 (release-workflow angle) | PASS |
| AC-3 | Full scratchpad reference extension (net-new keys only + cross-link pointers) | PASS |
| AC-4 | Coverage preserved (`validate_readme_feature_coverage.py --enforce` green) | PASS |
| AC-5 | Framework README parity (`its_magic/README.md` ↔ `template/its_magic/README.md` byte-identical) | PASS |
| AC-6 | Audience + metadata hygiene | PASS |
| AC-7 | Runbook cross-links per feature (US-0062 → L171 with note) | PASS |
| AC-8 | Regression tests (coverage parity contract tests green; no test weakenings) | PASS |

## Files shipped

- `its_magic/README.md` — umbrella + 4 subsections + scratchpad reference extension (net-new keys + cross-link pointers)
- `template/its_magic/README.md` — byte-synced one-way copy from `its_magic/README.md` (AC-5)

## Compose guards

**18/18 UNCHANGED** — US-0114 lives entirely outside the compose surface (documentation-only):

US-0091, US-0097, US-0017, US-0040, US-0100, US-0101, US-0102, US-0103, US-0104, US-0105, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112, US-0041, US-0062.

## Test results

- `python -m pytest tests/scratchpad_example_parity_test.py -v` → **4 passed in 0.07s**
  - `test_bug0013_parity_check` PASSED
  - `test_bug0013_header_preserved` PASSED
  - `test_bug0013_local_overrides_preserved` PASSED
  - `test_bug0013_active_example_mirror_in_sync` PASSED
- No test files modified (AC-8 forbids test weakenings).

## Validator outputs (release re-run — all green)

```
python scripts/validate_readme_feature_coverage.py --repo . --enforce
  → {"status":"PASS","coverage_missing":[],"coverage_present":[],"gaps":[]}
  → [README_FEATURE_COVERAGE_VALIDATE_OK]   exit=0   (AC-4)

python scripts/validate_doc_profile.py
  → [DOC_PROFILE_VALIDATE_OK]                exit=0   (AC-6)

python scripts/check_intake_template_parity.py
  → [INTAKE_TEMPLATE_PARITY_OK] scope=intake exit=0   (AC-5)

cmd /c fc /b its_magic\README.md template\its_magic\README.md
  → FC: no differences encountered           exit=0   (AC-5 byte-identical)
```

## US-0113 byte-stability

- `git diff HEAD -- its_magic/README.md` (per QA findings) shows 678 additions + ~1 blank-line removal — pure addition.
- US-0113's `### Sovereign-loop era` umbrella (L940) and `### Sovereign-loop era keys` block (L1427) byte-stability preserved — no content lines removed.
- US-0114 added **cross-link pointers only** to US-0113's block (no edits to US-0113's block content).

## Carry-overs preserved

- **DC-2** — `# US-0041` and `# US-0062` h1 anchors missing in `architecture.md`: **DEFERRED to US-0117** (phase & role governance family). US-0114 did not add them.
- **Scratchpad reference extension** — LOCKED = net-new keys + cross-link pointers (per R-0102 open question #1). US-0113's `### Sovereign-loop era keys` block byte-stability preserved; no duplicate key rows.

## Publish / sync / trigger

- **Publish**: `RELEASE_PUBLISH_MODE=disabled` → deterministic no-op (`publish_snapshot=skipped_disabled`)
- **Sync** (DEC-0018): `SYNC_POLICY_MODE=disabled` → `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`
- **Release trigger**: `RELEASE_TRIGGER_SOURCE=manual` (no adapter subprocess)
- **Project README validator** (AC-4 / §3g): `FRAMEWORK_KIT_REPO=1` → root check skipped (kit repo posture)

## Gate chain

| Gate | Result | Evidence |
|------|--------|----------|
| check_in_tests | PASS | 4/4 pytest PASSED in 0.07s |
| qa | QA_PASS | `sprints/S0114/qa-verdict.json` — 8/8 ACs, 0 blockers |
| verify_work | VERIFY_WORK_PASS | `sprints/S0114/verify-work-verdict.json` — ready_for_release=true |
| isolation_evidence | PASS | execute + qa + verify-work runtime_proof_ids present (DEC-0029) |
| compose_guards | 18/18 UNCHANGED | documentation-only — no compose surface touched |
| readme_feature_coverage | PASS | `[README_FEATURE_COVERAGE_VALIDATE_OK]` exit 0 |
| project_readme | skipped | `FRAMEWORK_KIT_REPO=1` → root check skipped |
| doc_profile | PASS | `[DOC_PROFILE_VALIDATE_OK]` exit 0 |
| template_parity | PASS | `[INTAKE_TEMPLATE_PARITY_OK]` + `fc /b` no differences |

## Isolation evidence (US-0048 / DEC-0029)

- `phase_id=release`
- `role=release`
- `fresh_context_marker=release-S0114-US0114-20260704T071200Z-fresh`
- `timestamp=2026-07-04T07:12:00Z`
- `evidence_ref=sprints/S0114/release-findings.md` + `sprints/S0114/release-verdict.json` + this `handoffs/releases/S0114-release-notes.md` (US-0114 only; no other phase or story touched in this spawn)
- `handoff_ref=handoffs/resume_brief.md` (drain-advance block updated to reflect release complete)

## Strict runtime proof tuple (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260704-01`
- `runtime_proof_id=rp-auto-20260704-01-release-release-20260704T071200Z-US-0114`
- `phase_id=release`
- `role=release`
- `proof_issued_at=2026-07-04T07:12:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=release-release-us0114-auto2026070401-20260704T071200Z`

## Verdict

**RELEASE_PASS.** 8/8 ACs satisfied. All gates green. Framework README byte-parity confirmed. US-0113 byte-stability preserved. No test weakenings. No compose-surface changes. Publish skipped (disabled). Sync skipped (disabled). Trigger manual.

## Next

**`/refresh-context`** (fresh **curator** context, ship macro — second canonical phase) for segment closeout. Backlog drain continues with US-0115, US-0116, US-0117 (3 stories remaining).
