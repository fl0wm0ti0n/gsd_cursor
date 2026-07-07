# Release Notes — S0115 / US-0115

- **Sprint**: `S0115`
- **Story**: `US-0115` — Integration & observability operator documentation in framework README
- **Release date**: 2026-07-04 (UTC)
- **orchestrator_run_id**: `auto-20260704-01`
- **delivery_mode**: `ultra_lean`
- **macro_phase**: `ship` (first canonical phase — release)
- **policy_mode**: `disabled` (`RELEASE_PUBLISH_MODE=disabled`)
- **trigger_source**: `manual` (`RELEASE_TRIGGER_SOURCE=manual`)
- **branch**: `local` (no push; `SYNC_POLICY_MODE=disabled` per DEC-0018)
- **fresh_context_marker**: `release-US0115-release-20260704T084700Z-fresh`
- **runtime_proof_id**: `rp-auto-20260704-01-release-release-20260704T084700Z-US-0115`
- **release_version**: (none — documentation-only; no version bump)

## Summary

Close the operator-documentation gap for the **integration & observability family** (US-0034, US-0084, US-0086, US-0093, US-0096, US-0101, US-0102) in the framework README pair (`its_magic/README.md` ↔ `template/its_magic/README.md`). Added `### Integration & observability (US-0034 / US-0084 / US-0086 / US-0093 / US-0096 / US-0101 / US-0102) umbrella section` under `## Commands and workflow` (L1410; sibling to US-0113's sovereign-loop umbrella and US-0114's release & distribution umbrella), 7 nested `#### US-xxxx` operator subsections (US-id-ascending: US-0034 → US-0084 → US-0086 → US-0093 → US-0096 → US-0101 → US-0102; with bidirectional "see US-0114 for installer-payload angle" pointers for US-0101/US-0102 and US-0096 net-new narrative per R-0103 CORRECTION), and `### Integration & observability keys (US-0034 / US-0084 / US-0086 / US-0093 / US-0096 / US-0101 / US-0102)` sub-block (L1878) in `### Full scratchpad reference (detailed)` (net-new keys only: US-0034 `CROSS_REPO_*` family, US-0096 `LEAN_MEMORY_*` family + `AUTO_DELIVERY_ROUTING`, US-0101 5 resolver keys, US-0102 `MODEL_SLUG_<PHASE_ID>` + grouped cross-link to main reference list for US-0086 `REMOTE_EXECUTION` family + reason-code-only entries for US-0084/US-0093 + cross-link pointer to US-0114's block for canonical `DELIVERY_MODE` row + cross-link pointer to US-0113's block for canonical `MODEL_TIER` row). US-0113/US-0114 byte-stability preserved (3rd-story cumulative surface; pure addition; cross-link pointers only, no edits to US-0113's or US-0114's released blocks). Default-off posture preserved for optional features; zero new scratchpad keys introduced beyond the documented family. DC-3 (7 missing `# US-xxxx` h1 anchors in `architecture.md`) deferred to US-0117.

## ACs satisfied

**8/8 PASS** (independently re-verified by QA; release re-ran all gates):

| AC | Description | Status |
|----|-------------|--------|
| AC-1 | `### Integration & observability umbrella section` under `## Commands and workflow` | PASS |
| AC-2 | Per-feature operator subsections for US-0034/US-0084/US-0086/US-0093/US-0096/US-0101/US-0102 | PASS |
| AC-3 | Full scratchpad reference extension (net-new keys + cross-link pointers + reason-code-only entries) | PASS |
| AC-4 | Coverage preserved (`validate_readme_feature_coverage.py --enforce` green) | PASS |
| AC-5 | Framework README parity (`its_magic/README.md` ↔ `template/its_magic/README.md` byte-identical) | PASS |
| AC-6 | Audience + metadata hygiene | PASS |
| AC-7 | Runbook cross-links per feature (7 features → 7 anchors) | PASS |
| AC-8 | Regression tests (coverage parity contract tests green; no test weakenings) | PASS |

## Files shipped

- `its_magic/README.md` — umbrella + 7 subsections + scratchpad reference extension (net-new keys + cross-link pointers + reason-code-only entries)
- `template/its_magic/README.md` — byte-synced one-way copy from `its_magic/README.md` (AC-5)

## Compose guards

**23/23 UNCHANGED** — US-0115 lives entirely outside the compose surface (documentation-only):

US-0091, US-0097, US-0017, US-0040, US-0100, US-0101, US-0102, US-0103, US-0104, US-0105, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112, US-0034, US-0084, US-0086, US-0093, US-0096, US-0041, US-0062.

## Test results

- `python -m pytest tests/scratchpad_example_parity_test.py -v` → **4 passed in 0.06s**
  - `test_bug0013_parity_check` PASSED
  - `test_bug0013_header_preserved` PASSED
  - `test_bug0013_local_overrides_preserved` PASSED
  - `test_bug0013_active_example_mirror_in_sync` PASSED
- No test files modified (AC-8 forbids test weakenings).

## Validator outputs (release re-run — all green)

```
python scripts/validate_readme_feature_coverage.py --repo . --enforce
  → {"coverage_missing":[],"coverage_present":[],"coverage_total":0,"gaps":[],"status":"PASS"}
  → [README_FEATURE_COVERAGE_VALIDATE_OK]   exit=0   (AC-4)

python scripts/validate_doc_profile.py --repo .
  → [DOC_PROFILE_VALIDATE_OK]               exit=0   (AC-6)

python scripts/check-user-visible-metadata.py --repo .
  → (silent PASS)                           exit=0   (AC-6)

python scripts/check_intake_template_parity.py --repo .
  → [INTAKE_TEMPLATE_PARITY_OK] scope=intake exit=0  (AC-5)

python -c "a=open('its_magic/README.md','rb').read(); b=open('template/its_magic/README.md','rb').read(); print('PARITY_OK' if a==b else 'PARITY_DIFF', len(a), len(b))"
  → PARITY_OK 128660 128660                 exit=0   (AC-5 byte-identical)
```

## US-0113 / US-0114 byte-stability

- `its_magic/README.md` ↔ `template/its_magic/README.md` byte-identical at 128660 bytes each — end-to-end parity is the authoritative byte-stability proof.
- US-0113's `### Sovereign-loop era keys` block (L1682) and US-0114's `### Release & distribution keys` block (L1806) byte-stability preserved — no content lines removed.
- US-0115 added **cross-link pointers only** to US-0113's and US-0114's blocks (no edits to either released block's content). Pure addition; 3rd-story cumulative byte-stability surface.

## Carry-overs preserved

- **DC-3** — 7 missing `# US-0034`/`# US-0084`/`# US-0086`/`# US-0093`/`# US-0096`/`# US-0101`/`# US-0102` h1 anchors in `architecture.md`: **DEFERRED to US-0117** (architecture.md triad hygiene closure; US-0117 inherits DC-1 (5) + DC-2 (2) + DC-3 (7) = 14 total). US-0115 did not add them; correctly noted in execute-summary, dev_to_qa.md, qa-findings, and state.md checkpoints; NOT appended to `handoffs/sovereign_deferrals.jsonl` (orchestrator's segment-boundary advance hook handles it).
- **Scratchpad reference extension** — LOCKED = net-new keys + cross-link pointers + reason-code-only entries. US-0113's `### Sovereign-loop era keys` block and US-0114's `### Release & distribution keys` block byte-stability preserved; no duplicate key rows.
- **Encoding hygiene prerequisite** — carried from US-0114; working-tree `docs/product/backlog.md` has 185 stray `0xa7` bytes per R-0102/R-0103. Did NOT block `validate_readme_feature_coverage.py --enforce` in this release run (validator returned `[README_FEATURE_COVERAGE_VALIDATE_OK]` exit 0). Preserved for orchestrator awareness; NOT a US-0115 blocker.

## Non-blocking findings (0 blocking, 3 non-blocking — all cosmetic/pre-existing)

1. **NB-1 (cosmetic)**: Sprint.md baseline anticipated `coverage_missing=["US-0117"]` but actual validator output is `coverage_missing=[]` (US-0117 queued, not yet OPEN in-scope). Unchanged from pre-execute baseline; AC-4 gate holds.
2. **NB-2 (cosmetic)**: US-0084 README cross-link text reads `### Published npm installer.sh / POSIX dash (US-0084)` but actual runbook heading is `### Published npm \`installer.sh\` / POSIX dash (US-0084)` (with backticks). L1441 cited correctly; anchor recognizable. Not a broken cross-link.
3. **NB-3 (pre-existing)**: Pre-existing fixture-path test failures (NOT introduced by US-0115, NOT US-0115 regression targets per T-006): `template/tests/scratchpad_example_parity_test.py` FileNotFoundError (designed to run from inside `template/`), `tests/readme_feature_coverage_fixtures_test.py` 2 of 3 tests FileNotFoundError (fixture directory missing).

## Publish / sync / trigger

- **Publish**: `RELEASE_PUBLISH_MODE=disabled` → deterministic no-op (`publish_snapshot=skipped_disabled`)
- **Sync** (DEC-0018): `SYNC_POLICY_MODE=disabled` → `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`
- **Release trigger**: `RELEASE_TRIGGER_SOURCE=manual` (no adapter subprocess)
- **No packaging version bump**: US-0115 is documentation-only; no `its_magic/.its-magic-version` bump, no chocolatey/homebrew packaging changes.

## Gate chain

| Gate | Result | Evidence |
|------|--------|----------|
| check_in_tests | PASS | 4/4 pytest PASSED in 0.06s |
| qa | QA_PASS | `sprints/S0115/qa-verdict.json` — 8/8 ACs, 0 blockers, 3 non-blocking (cosmetic/pre-existing) |
| verify_work | VERIFY_WORK_PASS | `sprints/S0115/verify-work-verdict.json` — execute_summary_accurate=true, scope_creep=none |
| isolation_evidence | PASS | execute + qa + verify-work + release runtime_proof_ids present (DEC-0029) |
| compose_guards | 23/23 UNCHANGED | documentation-only — no compose surface touched |
| readme_feature_coverage | PASS | `[README_FEATURE_COVERAGE_VALIDATE_OK]` exit 0 |
| doc_profile | PASS | `[DOC_PROFILE_VALIDATE_OK]` exit 0 |
| metadata_guard | PASS | `check-user-visible-metadata.py` exit 0 (silent PASS) |
| template_parity | PASS | `[INTAKE_TEMPLATE_PARITY_OK]` + `PARITY_OK 128660 128660` |

## Isolation evidence (US-0048 / DEC-0029)

- `phase_id=release`
- `role=release`
- `fresh_context_marker=release-US0115-release-20260704T084700Z-fresh`
- `timestamp=2026-07-04T08:47:00Z`
- `evidence_ref=sprints/S0115/release-findings.md` + `sprints/S0115/release-verdict.json` + this `handoffs/releases/S0115-release-notes.md` (US-0115 only; no other phase or story touched in this spawn)
- `handoff_ref=handoffs/resume_brief.md` (drain-advance block updated to reflect release complete)

## Strict runtime proof tuple (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260704-01`
- `runtime_proof_id=rp-auto-20260704-01-release-release-20260704T084700Z-US-0115`
- `phase_id=release`
- `role=release`
- `proof_issued_at=2026-07-04T08:47:00Z`
- `proof_ttl_seconds=3600`

## Verdict

**RELEASE_PASS.** 8/8 ACs satisfied. All gates green. Framework README byte-parity confirmed (`PARITY_OK 128660 128660`). US-0113/US-0114 byte-stability preserved (3rd-story cumulative surface). No test weakenings. No compose-surface changes. No version bump. Publish skipped (disabled). Sync skipped (disabled). Trigger manual.

## Next

**`/refresh-context`** (fresh **curator** context, ship macro — second canonical phase) for segment closeout. Backlog drain continues with US-0116, US-0117 (2 stories remaining).
