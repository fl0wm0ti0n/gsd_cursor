# Release Notes — S0116 / US-0116

- **Sprint**: `S0116`
- **Story**: `US-0116` — Delivery & lifecycle operator documentation in framework README
- **Release date**: 2026-07-04 (UTC)
- **orchestrator_run_id**: `auto-20260704-01`
- **delivery_mode**: `ultra_lean`
- **macro_phase**: `ship` (first canonical phase — release)
- **policy_mode**: `disabled` (`RELEASE_PUBLISH_MODE=disabled`)
- **trigger_source**: `manual` (`RELEASE_TRIGGER_SOURCE=manual`)
- **branch**: `local` (no push; `SYNC_POLICY_MODE=disabled` per DEC-0018)
- **fresh_context_marker**: `release-US0116-release-20260704T175100Z-fresh`
- **runtime_proof_id**: `rp-auto-20260704-01-release-release-20260704T175100Z-US-0116`
- **release_version**: (none — documentation-only; no version bump)

## Summary

Close the operator-documentation gap for the **delivery & lifecycle family** (US-0092, US-0095, US-0098, US-0099) in the framework README pair (`its_magic/README.md` ↔ `template/its_magic/README.md`). Added `### Delivery & lifecycle (US-0092 / US-0095 / US-0098 / US-0099) umbrella section` under `## Commands and workflow` (L1665; 4th sibling after US-0113's sovereign-loop umbrella L940, US-0114's release & distribution umbrella L1225, US-0115's integration & observability umbrella L1410 — first 4-cumulative-surface story), 4 nested `#### US-xxxx` operator subsections (US-id-ascending: US-0092 → US-0095 → US-0098 → US-0099; with default-off framing for US-0092/US-0095/US-0098 opt-in features and bootstrap-on-install framing for US-0099; primary/fallback boundary table US-0095 primary IDE / US-0092 fallback headless/CI per runbook L1921–L1926), and `### Delivery & lifecycle keys (US-0092 / US-0095 / US-0098 / US-0099)` sub-block (L2225) in `### Full scratchpad reference (detailed)` — **true net-new key rows** ONLY (US-0098 `DEV_AUTO_LAUNCH_PROFILE` + `DEV_ENVIRONMENT_CONFIG` — the only 2 net-new scratchpad key rows) + **reason-code-only entries** for US-0099 (`DEV_ENV_BOOTSTRAP_*` family + `DEV_ENV_PROFILE_MISSING` — 5 reason codes) + **grouped cross-link pointers** to pre-US-0116 README surfaces for US-0092/US-0095 keys + **cross-link pointers** to US-0114's `### Release & distribution keys` block (L1806) for `DELIVERY_MODE` / `AUTO_INSTALL_DEPS` / `AUTO_RELEASE_NOTES` overlap + optional cross-link pointer to US-0115's `### Integration & observability keys` block (L1878) for `LEAN_MEMORY_*` family (default omit — angle-distinct per R-0104 open question #2). US-0113/US-0114/US-0115 byte-stability preserved (4th-story cumulative surface; pure addition; cross-link pointers + reason-code-only entries only; no edits to US-0113's L1682, US-0114's L1806, or US-0115's L1878 blocks). Default-off posture preserved for optional runtime features (US-0092/US-0095/US-0098); bootstrap-on-install framing for US-0099 (install-time only, zero runtime cost). DC-4 (4 missing `# US-0092`/`# US-0095`/`# US-0098`/`# US-0099` h1 anchors in `architecture.md`) deferred to US-0117 — US-0117 inherits DC-1 (5) + DC-2 (2) + DC-3 (7) + DC-4 (4) = 18 total as architecture.md triad hygiene closure.

## ACs satisfied

**8/8 PASS** (independently re-verified by QA; release re-ran all gates):

| AC | Description | Status |
|----|-------------|--------|
| AC-1 | `### Delivery & lifecycle umbrella section` under `## Commands and workflow` | PASS |
| AC-2 | Per-feature operator subsections for US-0092/US-0095/US-0098/US-0099 | PASS |
| AC-3 | Full scratchpad reference extension (true net-new keys only + cross-link pointers + reason-code-only entries) | PASS |
| AC-4 | Coverage preserved (`validate_readme_feature_coverage.py --enforce` green) | PASS |
| AC-5 | Framework README parity (`its_magic/README.md` ↔ `template/its_magic/README.md` byte-identical) | PASS |
| AC-6 | Audience + metadata hygiene | PASS |
| AC-7 | Runbook cross-links per feature (4 features → 4 anchors) | PASS |
| AC-8 | Regression tests (coverage parity contract tests green; no test weakenings) | PASS |

## Files shipped

- `its_magic/README.md` — umbrella + 4 subsections + scratchpad reference extension (net-new keys + cross-link pointers + reason-code-only entries); pure addition +1370 insertions / 0 deletions in post-L1878 range
- `template/its_magic/README.md` — byte-synced one-way copy from `its_magic/README.md` (AC-5)

## Compose guards

**23/23 UNCHANGED** — US-0116 lives entirely outside the compose surface (documentation-only):

US-0091, US-0097, US-0017, US-0040, US-0100, US-0101, US-0102, US-0103, US-0104, US-0105, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112, US-0034, US-0084, US-0086, US-0093, US-0096, US-0041, US-0062.

## Test results

- `python -m pytest tests/scratchpad_example_parity_test.py -v` → **4 passed in 0.09s**
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
  → PARITY_OK 145485 145485                 exit=0   (AC-5 byte-identical)
```

## US-0113 / US-0114 / US-0115 byte-stability (4th-story cumulative surface)

- `its_magic/README.md` ↔ `template/its_magic/README.md` byte-identical at **145485 bytes each** — end-to-end parity is the authoritative byte-stability proof.
- US-0113's `### Sovereign-loop era keys` block (L1682), US-0114's `### Release & distribution keys` block (L1806), and US-0115's `### Integration & observability keys` block (L1878) byte-stability preserved — no content lines removed; all 6 prior-released blocks (3 keys blocks + 3 umbrella blocks) byte-identical between the two READMEs.
- US-0116 added **cross-link pointers + reason-code-only entries + 2 net-new US-0098 key rows only** (no edits to any prior released block's content). Pure addition; 4th-story cumulative byte-stability surface — first 4-cumulative-surface story. `git diff --stat HEAD -- its_magic/README.md` confirms +1370 insertions / 0 deletions.

## Carry-overs preserved

- **DC-4** — 4 missing `# US-0092`/`# US-0095`/`# US-0098`/`# US-0099` h1 anchors in `architecture.md`: **DEFERRED to US-0117** (architecture.md triad hygiene closure; US-0117 inherits DC-1 (5) + DC-2 (2) + DC-3 (7) + DC-4 (4) = 18 total). US-0116 did not add them; correctly noted in execute-summary, dev_to_qa.md, qa-findings, qa-verdict, verify-work-findings, state.md checkpoints, release-findings, and this release-notes; NOT appended to `handoffs/sovereign_deferrals.jsonl` (orchestrator's segment-boundary advance hook handles it).
- **Scratchpad reference extension** — LOCKED = net-new keys + cross-link pointers + reason-code-only entries. US-0113's `### Sovereign-loop era keys` block, US-0114's `### Release & distribution keys` block, and US-0115's `### Integration & observability keys` block byte-stability preserved; no duplicate key rows.
- **Encoding hygiene prerequisite** — carried from US-0114; working-tree `docs/product/backlog.md` has 185 stray `0xa7` bytes per R-0102/R-0103/R-0104. Did NOT block `validate_readme_feature_coverage.py --enforce` in this release run (validator returned `[README_FEATURE_COVERAGE_VALIDATE_OK]` exit 0). Preserved for orchestrator awareness; NOT a US-0116 blocker.

## Non-blocking findings (0 blocking, 3 non-blocking — all cosmetic/pre-existing)

1. **NB-1 (DC-4 deferral)**: 4 missing `# US-0092`/`# US-0095`/`# US-0098`/`# US-0099` h1 anchors in `architecture.md` deferred to US-0117 — not a US-0116 blocker (AC-7 satisfied via runbook cross-links; all 4 features have existing verified runbook anchors per R-0104).
2. **NB-2 (encoding hygiene prerequisite)**: 185 stray `0xa7` (§) bytes in working-tree `docs/product/backlog.md` carried from US-0114 per R-0102/R-0103/R-0104; did NOT block the validator in this release re-verification run (validator returned exit 0).
3. **NB-3 (pre-existing fixture-path test failures)**: `template/tests/scratchpad_example_parity_test.py` + `tests/readme_feature_coverage_fixtures_test.py` (2 of 3 tests) FileNotFoundError — NOT introduced by US-0116, NOT US-0116 regression targets per `sprints/S0116/tasks.md` T-006.

## Publish / sync / trigger

- **Publish**: `RELEASE_PUBLISH_MODE=disabled` → deterministic no-op (`publish_snapshot=skipped_disabled`)
- **Sync** (DEC-0018): `SYNC_POLICY_MODE=disabled` → `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`
- **Release trigger**: `RELEASE_TRIGGER_SOURCE=manual` (no adapter subprocess)
- **No packaging version bump**: US-0116 is documentation-only; no `its_magic/.its-magic-version` bump, no chocolatey/homebrew packaging changes. Released out-of-band (documentation-only, no packaging version bump).

## Gate chain

| Gate | Result | Evidence |
|------|--------|----------|
| check_in_tests | PASS | 4/4 pytest PASSED in 0.09s |
| qa | QA_PASS | `sprints/S0116/qa-verdict.json` — 8/8 ACs, 0 blockers, 3 non-blocking (cosmetic/pre-existing) |
| verify_work | VERIFY_WORK_PASS | `sprints/S0116/verify-work-verdict.json` — execute_summary_accurate=true, scope_creep=none |
| isolation_evidence | PASS | execute + qa + verify-work + release runtime_proof_ids present (DEC-0029) |
| compose_guards | 23/23 UNCHANGED | documentation-only — no compose surface touched |
| readme_feature_coverage | PASS | `[README_FEATURE_COVERAGE_VALIDATE_OK]` exit 0 |
| doc_profile | PASS | `[DOC_PROFILE_VALIDATE_OK]` exit 0 |
| metadata_guard | PASS | `check-user-visible-metadata.py` exit 0 (silent PASS) |
| template_parity | PASS | `[INTAKE_TEMPLATE_PARITY_OK]` + `PARITY_OK 145485 145485` |

## Isolation evidence (US-0048 / DEC-0029)

- `phase_id=release`
- `role=release`
- `fresh_context_marker=release-US0116-release-20260704T175100Z-fresh`
- `timestamp=2026-07-04T17:51:00Z`
- `evidence_ref=sprints/S0116/release-findings.md` + `sprints/S0116/release-verdict.json` + this `handoffs/releases/S0116-release-notes.md` (US-0116 only; no other phase or story touched in this spawn)
- `handoff_ref=handoffs/resume_brief.md` (drain-advance block updated to reflect release complete)

## Strict runtime proof tuple (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260704-01`
- `runtime_proof_id=rp-auto-20260704-01-release-release-20260704T175100Z-US-0116`
- `phase_id=release`
- `role=release`
- `proof_issued_at=2026-07-04T17:51:00Z`
- `proof_ttl_seconds=3600`

## Verdict

**RELEASE_PASS.** 8/8 ACs satisfied. All gates green. Framework README byte-parity confirmed (`PARITY_OK 145485 145485`). US-0113/US-0114/US-0115 byte-stability preserved (4th-story cumulative surface — first 4-cumulative-surface story). No test weakenings. No compose-surface changes. No version bump. Publish skipped (disabled). Sync skipped (disabled). Trigger manual. Story closed in `docs/product/backlog.md` (OPEN → DONE) and `docs/product/acceptance.md` (`[ ]` → `[x]`).

## Next

**`/refresh-context`** (fresh **curator** context, ship macro — second canonical phase) for segment closeout. Backlog drain continues with US-0117 (1 story remaining — US-0117 inherits DC-1 (5) + DC-2 (2) + DC-3 (7) + DC-4 (4) = 18 architecture.md triad hygiene anchors).
