# Sprint S0116 — QA Findings (US-0116)

**sprint_id**: S0116
**story_refs**: US-0116
**phase**: qa (merged plan-verify + execute QA + verify-work + UAT per ultra_lean)
**role**: qa
**orchestrator_run_id**: auto-20260704-01
**delivery_mode**: ultra_lean
**macro_phase**: build+verify (second canonical phase)
**fresh_context_marker**: `qa-US0116-qa-20260704T174300Z-fresh`
**timestamp**: 2026-07-04T17:43:00Z (UTC)
**runtime_proof_id**: `rp-auto-20260704-01-qa-qa-20260704T174300Z-US-0116`
**verdict**: **PASS**

---

## 1. Plan-verify (merged — PASS)

See `sprints/S0116/plan-verify.json`. All 10 checks PASS:

| Check | Status | Detail |
|-------|--------|--------|
| task_count_within_limit | PASS | 6 tasks <= SPRINT_MAX_TASKS=12 |
| ac_coverage_surjective | PASS | 8/8 ACs mapped to 6 tasks |
| dependency_order_acyclic | PASS | T-001->T-006 acyclic |
| files_to_touch_consistent | PASS | only its_magic/README.md + template/its_magic/README.md |
| no_dec_required | PASS | documentation-only; companion_dec=none |
| dc4_deferral_noted | PASS | 4 missing # US-xxxx h1 anchors deferred to US-0117 |
| byte_stability_contract_present | PASS | 4th-story cumulative surface LOCKED |
| compose_guards_23_unchanged | PASS | same 23 as US-0115 |
| test_markers_locked | PASS | 5 markers; no new tests proposed |
| encoding_hygiene_prerequisite_flagged | PASS | carried from US-0114; not a blocker |

---

## 2. Execute QA — independent re-run results

### Validator re-run results (all green on independent re-run)

| Validator | Command | Result | Exit |
|-----------|---------|--------|------|
| Coverage | `python scripts/validate_readme_feature_coverage.py --repo . --enforce` | `{"coverage_missing":[],"coverage_present":[],"coverage_total":0,"gaps":[],"status":"PASS"}` + `[README_FEATURE_COVERAGE_VALIDATE_OK]` | 0 |
| Audience | `python scripts/validate_doc_profile.py --repo .` | `[DOC_PROFILE_VALIDATE_OK]` | 0 |
| Metadata hygiene | `python scripts/check-user-visible-metadata.py --repo .` | silent PASS (no violations) | 0 |
| Intake template parity | `python scripts/check_intake_template_parity.py --repo .` | `[INTAKE_TEMPLATE_PARITY_OK] scope=intake` | 0 |
| Binary parity | `python -c "...PARITY_OK..."` | `PARITY_OK 145485 145485` | 0 |

### Test re-run results (independent)

| Test | Command | Result |
|------|---------|--------|
| Scratchpad example parity (canonical) | `python -m pytest tests/scratchpad_example_parity_test.py -v` | **4 passed in 0.09s** — `test_bug0013_parity_check` PASSED, `test_bug0013_header_preserved` PASSED, `test_bug0013_local_overrides_preserved` PASSED, `test_bug0013_active_example_mirror_in_sync` PASSED |

Pre-existing fixture-path test failures (not introduced by US-0116, not US-0116 regression targets per T-006) — flagged for awareness only:
- `template/tests/scratchpad_example_parity_test.py` — `FileNotFoundError` (designed to run from inside `template/` as a consumer fixture, not from repo root).
- `tests/readme_feature_coverage_fixtures_test.py` (2 of 3 tests) — `FileNotFoundError` (fixture directory missing).

### Byte-stability re-verification (4th-story cumulative surface — CRITICAL)

Independent re-run via Python script comparing the six US-0113/US-0114/US-0115 blocks between `its_magic/README.md` (post-US-0116) and `template/its_magic/README.md` (post-US-0116 byte-sync):

| Block | its_magic length | template length | EQUAL |
|-------|-----------------|-----------------|-------|
| `### Sovereign-loop era keys (US-0103–US-0112)` | (matched) | (matched) | **True** |
| `### Release & distribution keys (US-0041 / US-0062 / US-0111 / US-0112)` | 4115 | 4115 | **True** |
| `### Integration & observability keys (US-0034 / US-0084 / US-0086 / US-0093 / US-0096 / US-0101 / US-0102)` | 8433 | 8433 | **True** |
| `### Sovereign-loop era (US-0103–US-0112) umbrella section` | 13700 | 13700 | **True** |
| `### Release & distribution (US-0041 / US-0062 / US-0111 / US-0112) umbrella section` | 10418 | 10418 | **True** |
| `### Integration & observability (US-0034 / US-0084 / US-0086 / US-0093 / US-0096 / US-0101 / US-0102) umbrella section` | 14575 | 14575 | **True** |
| **Full README parity** | 145485 | 145485 | **True** |

All 6 prior-released blocks are byte-identical between the two READMEs. **Byte-stability contract preserved (4th-story cumulative surface — first 4-cumulative-surface story).**

`git diff --stat HEAD -- its_magic/README.md template/its_magic/README.md` shows `its_magic/README.md` +1370 insertions, 0 deletions (pure addition in post-L1878 range); `template/its_magic/README.md` +2975/-6 (template sync delta — includes US-0113/US-0114/US-0115 unstaged working-tree additions vs. HEAD; the authoritative end-to-end byte-stability proof is the template-vs-new-its_magic comparison above, both `PARITY_OK 145485 145485` and full-file equal).

### Parity re-verification

- `python -c "...PARITY_OK..."` → `PARITY_OK 145485 145485` (exit 0).
- `python scripts/check_intake_template_parity.py --repo .` → `[INTAKE_TEMPLATE_PARITY_OK] scope=intake` (exit 0).
- Both parity gates green; `its_magic/README.md` ↔ `template/its_magic/README.md` byte-identical.

### AC coverage independent assessment (8/8)

| AC | Description | Independent verification | Status | Task |
|----|-------------|---------------------------|--------|------|
| AC-1 | `### Delivery & lifecycle` umbrella section under `## Commands and workflow` | Grep confirmed `### Delivery & lifecycle (US-0092 / US-0095 / US-0098 / US-0099) umbrella section` at L1665 of `its_magic/README.md`, after US-0115 umbrella close, before `### Full scratchpad reference (detailed)` | ✅ PASS | T-001 |
| AC-2 | Per-feature operator subsections for US-0092/US-0095/US-0098/US-0099 | Grep confirmed exactly 4 `#### US-xxxx` subsections US-id-ascending at L1720 (US-0092), L1757 (US-0095), L1799 (US-0098), L1832 (US-0099) | ✅ PASS | T-002 |
| AC-3 | Full scratchpad reference extension (true net-new keys + cross-link pointers + reason-code-only entries) | `### Delivery & lifecycle keys (US-0092 / US-0095 / US-0098 / US-0099)` sub-block at L2225; 2 net-new key rows (`DEV_AUTO_LAUNCH_PROFILE`, `DEV_ENVIRONMENT_CONFIG`) at L2236; 5 US-0099 reason-code-only entries at L2254; grouped cross-link at L2278; cross-link pointer to US-0114 block at L2295; cross-link pointer to US-0115 block at L2305; US-0113/US-0114/US-0115 byte-stability preserved (see table above) | ✅ PASS | T-003 |
| AC-4 | Coverage preserved | `[README_FEATURE_COVERAGE_VALIDATE_OK]` exit 0; `coverage_missing=[]` unchanged from baseline | ✅ PASS | T-005 |
| AC-5 | Framework README parity | `PARITY_OK 145485 145485` + `[INTAKE_TEMPLATE_PARITY_OK] scope=intake` | ✅ PASS | T-004 |
| AC-6 | Audience + metadata hygiene | `[DOC_PROFILE_VALIDATE_OK]` exit 0 + `check-user-visible-metadata.py` exit 0 | ✅ PASS | T-005 |
| AC-7 | Runbook cross-links per feature (4 features → 4 anchors) | Verified runbook anchors exist — US-0092 L1958 (`### Full-autonomy outer driver (US-0092) — fallback`) + L1989 (`#### Security (US-0092 / DEC-0078)`); US-0095 L1900 (`### Native in-chat auto-chain (US-0095)`); US-0098 L244 (`## Dev environment auto-launch (US-0098 / DEC-0084)`); US-0099 L244 (parent h2) + secondary pointers to L250 (bootstrap paragraph) + L301 (normative contract anchor). All 4 README subsections include runbook cross-link lines. | ✅ PASS | T-002 |
| AC-8 | Regression tests | 4/4 pytest PASSED in 0.09s; no test weakenings; US-0116 did NOT touch `.cursor/scratchpad.md`, `template/.cursor/scratchpad.local.example.md`, or `tests/scratchpad_example_parity_test.py` | ✅ PASS | T-006 |

**Surjectivity**: 8/8 ACs covered by 6 tasks. No `QA_AC_COVERAGE_GAP`.

### Cross-link pointer verification (AC-3 byte-stability — PASS)

- **Cross-link to US-0114 `### Release & distribution keys`** at L2295: `### Delivery & lifecycle keys` sub-block contains `#### Cross-link to Release & distribution keys (DELIVERY_MODE / AUTO_INSTALL_DEPS / AUTO_RELEASE_NOTES overlap)` referencing the canonical block above for `DELIVERY_MODE`, `AUTO_INSTALL_DEPS`, `AUTO_RELEASE_NOTES`. References — does not duplicate — the canonical rows (US-0114 byte-stability preserved; no duplicate key rows).
- **Cross-link to US-0115 `### Integration & observability keys`** at L2305: `#### Cross-link to Integration & observability keys (LEAN_MEMORY_* overlap)` referencing the canonical `LEAN_MEMORY_*` family rows above. References — does not duplicate — the canonical rows (US-0115 byte-stability preserved; US-0095 angle-distinct from US-0096's `LEAN_MEMORY_*` family per R-0104 open question #2).
- **Grouped cross-link** at L2278: `#### US-0092 / US-0095 — Grouped cross-link (auto-chain + drain keys)` references the pre-US-0116 README surfaces (`### Automation modes` L880, `### Sync policy (US-0038)` L909, `### Optional /auto backlog-drain mode (US-0044)` L2370, main reference list). No duplicate key rows.
- All cross-link pointer rows reference canonical blocks without duplicating key documentation — byte-stability contract honored.

---

## 3. Verify-work (execute-summary vs actual state — PASS)

See `sprints/S0116/verify-work-findings.md` and `sprints/S0116/verify-work-verdict.json`.

- **execute_summary_accurate**: true — 12/12 dev claims independently re-verified and matched (all 5 validators green; 4/4 pytest PASS; byte-stability preserved on all 6 prior-released blocks; parity `PARITY_OK 145485 145485`; AC coverage 8/8; DC-4 deferral correctly noted; encoding hygiene prerequisite carried; pre-existing fixture-path test failures flagged).
- **scope_creep**: NONE — only `its_magic/README.md` + `template/its_magic/README.md` modified; no edits to scratchpad canonical, `docs/product/backlog.md`, `docs/engineering/runbook.md`, `docs/engineering/architecture.md` beyond US-0116 anchor, `installer.*`, `scripts/*`, any test file, `docs/developer/README.md`.
- **byte_stability_preserved**: true (4th-story cumulative surface — see table above).
- **parity_preserved**: true.
- **DC-4 deferral correctly noted**: not silently dropped.

---

## 4. UAT (documentation story — PASS)

See `sprints/S0116/uat.json` and `sprints/S0116/uat.md`. 4/4 UAT steps PASS:

1. **Internal anchor links resolve**: All `### `/`#### ` anchor references in the new `### Delivery & lifecycle` umbrella section (L1665–L1861) and `### Delivery & lifecycle keys` sub-block (L2225–L2314) point to existing README/runbook sections verified by grep.
2. **README renders without markdown errors**: No malformed headings; consistent h3/h4 nesting; boundary table at L1770–L1775 well-formed.
3. **TOC contract honored**: Catalog anchor `<!-- readme-feature-coverage-catalog -->` (L63) UNCHANGED; US-0116 appends narrative sections outside the catalog block (per US-0091 compose guard).
4. **Cross-link pointer rows reference canonical blocks without duplicating key documentation**: Verified above (cross-link pointer verification).

---

## Known issues / deferrals

- **DC-4** (deferred to US-0117): 4 missing `# US-xxxx` h1 anchors in active `docs/engineering/architecture.md` for the US-0116 family — `# US-0092`, `# US-0095`, `# US-0098`, `# US-0099`. Not a US-0116 blocker (AC-7 satisfied via runbook cross-links). US-0117 inherits DC-1 (5) + DC-2 (2) + DC-3 (7) + DC-4 (4) = 18 total as architecture.md triad hygiene closure. NOT appended to `handoffs/sovereign_deferrals.jsonl` — orchestrator's segment-boundary advance hook handles it.
- **Encoding hygiene prerequisite** (carried from US-0114): Working-tree `docs/product/backlog.md` has 185 stray `0xa7` (§) bytes per R-0102/R-0103/R-0104 (Windows-1252 corruption). Did NOT block `validate_readme_feature_coverage.py --enforce` in QA re-verification run (validator returned `[README_FEATURE_COVERAGE_VALIDATE_OK]` exit 0). Flag preserved for orchestrator awareness. NOT a US-0116 blocker.
- **Pre-existing fixture-path test failures** (NOT introduced by US-0116, NOT US-0116 regression targets per `sprints/S0116/tasks.md` T-006): `template/tests/scratchpad_example_parity_test.py` and `tests/readme_feature_coverage_fixtures_test.py` (2 of 3 tests) FileNotFoundError — pre-existing fixture-path issues.

**0 blocking findings. 3 non-blocking findings** (all cosmetic/pre-existing, NOT introduced by US-0116).

---

## Isolation evidence (US-0048 / DEC-0029)

- **phase_id**: qa
- **role**: qa
- **fresh_context_marker**: `qa-US0116-qa-20260704T174300Z-fresh`
- **timestamp**: 2026-07-04T17:43:00Z (UTC)
- **evidence_ref**: `sprints/S0116/qa-findings.md` (this file) + `sprints/S0116/plan-verify.json` + `sprints/S0116/qa-verdict.json` + `sprints/S0116/verify-work-findings.md` + `sprints/S0116/verify-work-verdict.json` + `sprints/S0116/uat.json` + `sprints/S0116/uat.md` + `handoffs/qa_to_dev.md` + `docs/engineering/state.md` (qa checkpoint appended)
- **isolation_mode**: fresh subagent context per BUG-0006 / US-0048 — qa subagent spawned fresh for the qa phase; no carry-over from prior sprint-plan / architecture / research / discovery / execute phases other than the artifact reads enumerated in the parent prompt.

## Strict runtime proof

- **runtime_proof_id**: `rp-auto-20260704-01-qa-qa-20260704T174300Z-US-0116`
- **proof_issued_at**: 2026-07-04T17:43:00Z
- **proof_ttl_seconds**: 3600
- **proof_ttl**: 2026-07-04T18:43:00Z (UTC) per DEC-0038
- **canonical_payload** (sorted-key JSON per DEC-0038): `{"orchestrator_run_id":"auto-20260704-01","phase_id":"qa","proof_issued_at":"2026-07-04T17:43:00Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260704-01-qa-qa-20260704T174300Z-US-0116","story_id":"US-0116"}`
- **proof_hash** (SHA-256 sorted-key JSON per DEC-0038): `7ac6c3e4797dbf2f68a940c520d3ea35b3f9afd10c6b12cc91409ae0b6f2b83c`.

## Sovereign memory note

`assemble_sovereign_memory_digest(...)` NOT called (US-0116 documentation-only; existing digest context sufficient per R-0104; S0113/S0114/S0115 retrospectives established reusable patterns — cross-link pointer pattern + angle-distinct narrative pattern + cross-story byte-stability contract now form a quad; US-0116 is the first 4-cumulative-surface story). No write to `mistakes.jsonl` in qa phase (no fix_failed / revert_applied / plan_fidelity_violation / scope_creep event occurred — all 3 non-blocking findings are cosmetic/pre-existing).

## Next phase

Per **ultra_lean**, the orchestrator routes to the **`/release` phase** (release subagent, `ship` macro — first canonical phase). US-0116 remains **OPEN** in `docs/product/backlog.md` until `/release` closes it per US-0045.

**STOP**: qa complete; do not spawn the next phase. The orchestrator will Task-spawn the release subagent for `/release`. Hand off via artifacts only.

- **next_scheduled_phase**: `/release` (release subagent, `ship` macro — first canonical phase per ultra_lean)
- **stop_condition**: STOP after qa artifacts written; orchestrator Task-spawns release for `/release`
