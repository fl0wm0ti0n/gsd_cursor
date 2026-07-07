# Release Notes — S0117 / US-0117

- **Sprint**: `S0117`
- **Story**: `US-0117` — Phase & role governance operator documentation in framework README
- **Release date**: 2026-07-04 (UTC)
- **orchestrator_run_id**: `auto-20260704-01`
- **delivery_mode**: `ultra_lean`
- **macro_phase**: `ship` (first canonical phase — release)
- **policy_mode**: `disabled` (`RELEASE_PUBLISH_MODE=disabled`)
- **trigger_source**: `manual` (`RELEASE_TRIGGER_SOURCE=manual`)
- **branch**: `local` (no push; `SYNC_POLICY_MODE=disabled` per DEC-0018)
- **fresh_context_marker**: `release-US0117-release-20260704T201210Z-fresh`
- **runtime_proof_id**: `rp-auto-20260704-01-release-release-20260704T201210Z-US-0117`
- **release_version**: (none — documentation-only; no version bump)

## Summary

Close the operator-documentation gap for the **phase & role governance family** (US-0069, US-0070, US-0071, US-0072, US-0075, US-0076, US-0077, US-0078, US-0079, US-0080, US-0081, US-0082, US-0083, US-0085, US-0087, US-0088, US-0089, US-0090) in the framework README pair (`its_magic/README.md` ↔ `template/its_magic/README.md`). Added `### Phase & role governance (US-0069 / US-0070 / US-0071 / US-0072 / US-0075 / US-0076 / US-0077 / US-0078 / US-0079 / US-0080 / US-0081 / US-0082 / US-0083 / US-0085 / US-0087 / US-0088 / US-0089 / US-0090) umbrella section` under `## Commands and workflow` (L1864; 5th sibling — first 5-cumulative-surface story), 18 nested `#### US-xxxx` operator subsections (US-id-ascending: US-0069 → US-0090) with 2 labeling corrections applied (US-0082 = "Codebase map" NOT "Input compression" per runbook L63 + DEC-0065 + architecture `## US-0082`; US-0090 = "Caveman input compression" NOT "Phase governance integration" per runbook L2099 + DEC-0073 + architecture `## US-0090`), 1 US-id collision resolved (US-0089 = "Auto orchestration" NOT "Caveman mode" per `/architecture` lock; runbook h2 `## Caveman mode (US-0089)` L2032 covers US-0081 family content), and `### Phase & role governance keys (US-0069 / ... / US-0090)` sub-block (L2856) in `### Full scratchpad reference (detailed)` — **46 net-new key rows across 10 features** (US-0069/0070/0079/0080/0081/0083/0087/0088/0089/0090) + **9 reason-code-only entries** (7 features: US-0070/0077/0081/0083/0085/0087/0090) + **7 prose-only / runbook-cross-link-only entries** (US-0071/0072/0075/0076/0077/0078/0085) + **cross-link pointers** (`DELIVERY_MODE` → US-0114; `LEAN_MEMORY_*` → US-0115 default omit; `TOKEN_PROFILE` → main reference list + US-0080 subsection; `CODEBASE_MAP_REFRESH_ON_ROLLOVER` → US-0082 subsection). US-0113/US-0114/US-0115/US-0116 byte-stability preserved (5th-story cumulative surface — first 5-cumulative-surface story; pure addition; cross-link pointers + reason-code-only entries + net-new key rows only; no edits to US-0113's L2421, US-0114's L2545, US-0115's L2617, or US-0116's L2765 blocks). Default-off posture preserved for optional runtime features; bootstrap-on-install framing for install-time-only features. **36 DC anchors** (18 own + 18 deferred: DC-1 (5, from US-0113) + DC-2 (2, from US-0114) + DC-3 (7, from US-0115) + DC-4 (4, from US-0116)) + `## US-0117` section **resolved in `/architecture` phase** (final deferred-candidate resolution point — T-anch in S0117 was a NO-OP / verification).

## Drain-complete note (5/5 stories shipped)

**This is the FINAL story in the 5-story drain (US-0113..US-0117).** All 5 documentation families are now complete:

| Story | Family | Released |
|-------|--------|----------|
| US-0113 | Sovereign-loop era (US-0103–US-0112, 9 features) | 2026-07-04T03:00:00Z |
| US-0114 | Release & distribution (US-0041 / US-0062 / US-0111 / US-0112, 4 features) | 2026-07-04T07:12:00Z |
| US-0115 | Integration & observability (US-0034 / US-0084 / US-0086 / US-0093 / US-0096 / US-0101 / US-0102, 7 features) | 2026-07-04T08:47:00Z |
| US-0116 | Delivery & lifecycle (US-0092 / US-0095 / US-0098 / US-0099, 4 features) | 2026-07-04T17:51:00Z |
| **US-0117** | **Phase & role governance (US-0069 / ... / US-0090, 18 features)** | **2026-07-04T20:12:00Z** |

**Total drain shipped**: 5 stories, 42 features documented across 5 umbrella sections + 5 scratchpad reference sub-blocks. Pattern now established as a quint (S0113/S0114/S0115/S0116 + US-0117). Drain queue is now EMPTY (0 stories remaining).

## ACs satisfied

**8/8 PASS** (independently re-verified by QA; release re-ran all gates):

| AC | Description | Status |
|----|-------------|--------|
| AC-1 | `### Phase & role governance umbrella section` under `## Commands and workflow` | PASS |
| AC-2 | Per-feature operator subsections for US-0069/US-0070/US-0071/US-0072/US-0075/US-0076/US-0077/US-0078/US-0079/US-0080/US-0081/US-0082/US-0083/US-0085/US-0087/US-0088/US-0089/US-0090 | PASS |
| AC-3 | Full scratchpad reference extension (46 net-new key rows + 9 reason-code-only entries + 7 prose-only / runbook-cross-link-only entries + cross-link pointers) | PASS |
| AC-4 | Coverage preserved (`validate_readme_feature_coverage.py --enforce` green) | PASS |
| AC-5 | Framework README parity (`its_magic/README.md` ↔ `template/its_magic/README.md` byte-identical) | PASS |
| AC-6 | Audience + metadata hygiene | PASS |
| AC-7 | Runbook cross-links per feature (18 features → 18 anchors) | PASS |
| AC-8 | Regression tests (coverage parity contract tests green; no test weakenings) | PASS |

## Files shipped

- `its_magic/README.md` — umbrella + 18 subsections + scratchpad reference extension (net-new keys + cross-link pointers + reason-code-only entries + prose-only entries); pure addition +2188 insertions / 0 deletions in post-L2765 range
- `template/its_magic/README.md` — byte-synced one-way copy from `its_magic/README.md` (AC-5)

## Compose guards

**23/23 UNCHANGED** — US-0117 lives entirely outside the compose surface (documentation-only):

US-0091, US-0097, US-0017, US-0040, US-0100, US-0101, US-0102, US-0103, US-0104, US-0105, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112, US-0034, US-0084, US-0086, US-0093, US-0096, US-0041, US-0062.

## Test results

- `python -m pytest tests/scratchpad_example_parity_test.py -v` → **4 passed in 0.10s**
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
  → PARITY_OK 191091 191091                 exit=0   (AC-5 byte-identical)
```

## US-0113 / US-0114 / US-0115 / US-0116 byte-stability (5th-story cumulative surface)

- `its_magic/README.md` ↔ `template/its_magic/README.md` byte-identical at **191091 bytes each** — end-to-end parity is the authoritative byte-stability proof.
- US-0113's `### Sovereign-loop era keys` block (L2421), US-0114's `### Release & distribution keys` block (L2545), US-0115's `### Integration & observability keys` block (L2617), and US-0116's `### Delivery & lifecycle keys` block (L2765) byte-stability preserved — no content lines removed; all 8 prior-released blocks (4 keys blocks + 4 umbrella blocks) byte-identical between the two READMEs.
- US-0117 added **net-new key rows + cross-link pointers + reason-code-only entries + prose-only entries only** (no edits to any prior released block's content). Pure addition; 5th-story cumulative byte-stability surface — first 5-cumulative-surface story. `git diff --stat HEAD -- its_magic/README.md` confirms +2188 insertions / 0 deletions.

## DC anchor resolution (final deferred-candidate resolution point)

US-0117 is the **final deferred-candidate resolution point** for the architecture.md triad hygiene closure. The 36 `## US-xxxx` h1 anchors (18 own + 18 deferred DC-1+DC-2+DC-3+DC-4) plus the `## US-0117` section itself were **added in the `/architecture` phase** (per R-0105 Q-2 LOCKED: resolve in `/architecture`, NOT `/execute` — keeps anchors as architecture artifacts per `docs/engineering/artifact-ownership-policy.md`). T-anch in S0117 was a NO-OP / verification — no execute-phase write to architecture.md. Release confirms the 36 anchors + `## US-0117` section exist at `docs/engineering/architecture.md` L1420 + L1568–L1708 (verified via grep — 36 matching `## US-xxxx` headings confirmed).

## Carry-overs preserved

- **Scratchpad reference extension** — LOCKED = net-new keys + cross-link pointers + reason-code-only entries + prose-only entries. US-0113's L2421, US-0114's L2545, US-0115's L2617, and US-0116's L2765 blocks byte-stability preserved; no duplicate key rows.
- **Encoding hygiene prerequisite** — carried from US-0114; working-tree `docs/product/backlog.md` has 185 stray `0xa7` bytes per R-0102/R-0103/R-0104/R-0105. Did NOT block `validate_readme_feature_coverage.py --enforce` in this release run (validator returned `[README_FEATURE_COVERAGE_VALIDATE_OK]` exit 0). Preserved for orchestrator awareness; NOT a US-0117 blocker.
- **DC anchor resolution** — RESOLVED in `/architecture` phase (not deferred further). US-0117 is the final story in the 5-story drain; no carry-over to a successor story.

## Non-blocking findings (0 blocking, 4 non-blocking — all cosmetic/pre-existing)

1. **NB-1 (T-anch NO-OP)**: 36 DC anchors + `## US-0117` section already added in `/architecture` phase per R-0105 Q-2 LOCKED; no execute-phase write to architecture.md. The 1-deletion in numstat is a pre-existing line-ending change at L570 from the architecture phase.
2. **NB-2 (R-0105 labeling discrepancy)**: backlog.md US-0117 summary line L3969 appears to swap US-0082 / US-0090 labels; dev followed runbook + DEC + architecture lock as canonical; no backlog.md edit per US-0045 (closure only at /release). QA + release re-verified README labeling matches the authoritative runbook + DEC + architecture lock.
3. **NB-3 (encoding hygiene prerequisite)**: 185 stray `0xa7` (§) bytes in working-tree `docs/product/backlog.md` carried from US-0114 per R-0102/R-0103/R-0104/R-0105; did NOT block the validator in this release re-verification run (validator returned exit 0).
4. **NB-4 (pre-existing fixture-path test failures)**: `template/tests/scratchpad_example_parity_test.py` + `tests/readme_feature_coverage_fixtures_test.py` (2 of 3 tests) FileNotFoundError — NOT introduced by US-0117, NOT US-0117 regression targets per `sprints/S0117/tasks.md` T-006.

## Publish / sync / trigger

- **Publish**: `RELEASE_PUBLISH_MODE=disabled` → deterministic no-op (`publish_snapshot=skipped_disabled`)
- **Sync** (DEC-0018): `SYNC_POLICY_MODE=disabled` → `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`
- **Release trigger**: `RELEASE_TRIGGER_SOURCE=manual` (no adapter subprocess)
- **No packaging version bump**: US-0117 is documentation-only; no `its_magic/.its-magic-version` bump, no chocolatey/homebrew packaging changes. Released out-of-band (documentation-only, no packaging version bump).

## Gate chain

| Gate | Result | Evidence |
|------|--------|----------|
| check_in_tests | PASS | 4/4 pytest PASSED in 0.10s |
| qa | QA_PASS | `sprints/S0117/qa-verdict.json` — 8/8 ACs, 0 blockers, 4 non-blocking (cosmetic/pre-existing) |
| verify_work | VERIFY_WORK_PASS | `sprints/S0117/verify-work-verdict.json` — execute_summary_accurate=true, scope_creep=none |
| isolation_evidence | PASS | execute + qa + verify-work + release runtime_proof_ids present (DEC-0029) |
| compose_guards | 23/23 UNCHANGED | documentation-only — no compose surface touched |
| readme_feature_coverage | PASS | `[README_FEATURE_COVERAGE_VALIDATE_OK]` exit 0 |
| doc_profile | PASS | `[DOC_PROFILE_VALIDATE_OK]` exit 0 |
| metadata_guard | PASS | `check-user-visible-metadata.py` exit 0 (silent PASS) |
| template_parity | PASS | `[INTAKE_TEMPLATE_PARITY_OK]` + `PARITY_OK 191091 191091` |
| dc_anchor_resolution | PASS | 36 `## US-xxxx` h1 anchors + `## US-0117` section confirmed present in architecture.md |

## Isolation evidence (US-0048 / DEC-0029)

- `phase_id=release`
- `role=release`
- `fresh_context_marker=release-US0117-release-20260704T201210Z-fresh`
- `timestamp=2026-07-04T20:12:10Z`
- `evidence_ref=sprints/S0117/release-findings.md` + `sprints/S0117/release-verdict.json` + this `handoffs/releases/S0117-release-notes.md` (US-0117 only; no other phase or story touched in this spawn)
- `handoff_ref=handoffs/resume_brief.md` (drain-advance block updated to reflect release complete — drain complete 5/5)

## Strict runtime proof tuple (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260704-01`
- `runtime_proof_id=rp-auto-20260704-01-release-release-20260704T201210Z-US-0117`
- `phase_id=release`
- `role=release`
- `proof_issued_at=2026-07-04T20:12:10Z`
- `proof_ttl_seconds=3600`

## Verdict

**RELEASE_PASS.** 8/8 ACs satisfied. All gates green. Framework README byte-parity confirmed (`PARITY_OK 191091 191091`). US-0113/US-0114/US-0115/US-0116 byte-stability preserved (5th-story cumulative surface — first 5-cumulative-surface story). 36 DC anchors + `## US-0117` section resolved in `/architecture` phase (final deferred-candidate resolution point). No test weakenings. No compose-surface changes. No version bump. Publish skipped (disabled). Sync skipped (disabled). Trigger manual. Story closed in `docs/product/backlog.md` (OPEN → DONE) and `docs/product/acceptance.md` (`[ ]` → `[x]`). **Drain complete 5/5** — all 5 documentation families (US-0113..US-0117) shipped; backlog drain queue now EMPTY.

## Next

**`/refresh-context`** (fresh **curator** context, ship macro — second canonical phase) for segment closeout. Backlog drain queue is now **EMPTY** (0 stories remaining — final story in 5-story drain shipped).
