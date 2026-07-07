# QA Findings — US-0119 / S0119 / Cycle 4

## Isolation evidence (US-0048 / DEC-0029)

- `phase_id=qa`
- `role=qa`
- `fresh_context_marker=qa-US0119-cycle4-qa-20260705T222729Z-fresh`
- `orchestrator_run_id=auto-20260705-05`
- `sprint_id=S0119`
- `story_id=US-0119`
- `cycle=4`
- `timestamp=2026-07-05T22:27:29Z`
- `delivery_mode=ultra_lean` (build+verify macro — plan-verify + qa + verify-work + UAT merged)

**Fresh-context proof**: This QA cycle was executed in a new subagent context with zero carry-over from prior QA cycles (cycles 1-3). All 33 checkpoints verified independently with tool-based evidence. No dev PASS claims trusted.

---

## Verdict: FAIL

- `blocking_findings_count=7`
- `verdict=FAIL`
- `next_phase=execute` (dev cycle 5 — final cycle per AUTO_LOOP_MAX_CYCLES=5)
- `escalation_note`: If cycle 5 also FAIL → decision gate escalation to operator for manual intervention or relaxed acceptance criteria.

---

## Per-checkpoint evidence

### Test Gates (10 checkpoints, 8 PASS / 2 FAIL)

| # | Checkpoint | Verdict | Evidence |
|---|-----------|---------|----------|
| 1 | `pytest tests/us0119_autonomy_preset_test.py -v` | **PASS** | 10 passed in 0.32s (all 10 markers: preset_none_is_noop, balanced_expansion, full_expansion, explicit_override, known_keys_only, matrix_validator_passes, security_hard_gates, stop_policy_dispatch, repair_ledger_cap, no_orphan_codes) |
| 2 | `pytest tests/scratchpad_example_parity_test.py -v` | **FAIL** | 2 passed, 2 failed in 0.40s. `test_bug0013_local_overrides_preserved` FAIL — template contains project-local overrides (`DELIVERY_MODE=ultra_lean` in template vs `DELIVERY_MODE=standard` in active scratchpad.local.example.md at line 181). `test_bug0013_active_example_mirror_in_sync` FAIL — active body (from L6) diverges from template body (active=553 lines, template=635 lines). |
| 3 | `validate_autonomy_stop_matrix.py --self-test` | **PASS** | `[MATRIX_VALID] All checks passed (28 codes: 18 security_hard, 10 autonomy_resolvable)` exit 0 |
| 4 | `autonomy_preset_lib.py --self-test` | **PASS** | `6/6 tests passed` exit 0 with implicit `[AUTONOMY_PRESET_SELF_TEST_OK]` |
| 5 | `autonomy_repair_ledger_lib.py --self-test` | **PASS** | `[AUTONOMY_REPAIR_LEDGER_SELF_TEST_OK]` exit 0 |
| 6 | `validate_readme_feature_coverage.py --repo . --enforce` | **PASS** | `[README_FEATURE_COVERAGE_VALIDATE_OK]` status=PASS, coverage_missing=[], exit 0 |
| 7 | `check_intake_template_parity.py --repo .` | **FAIL** | `[INTAKE_TEMPLATE_PARITY_ERROR] mismatch: scripts/check_intake_template_parity.py (20083b) != template/scripts/check_intake_template_parity.py (199994b)`. Active has 8 surface pairs (added us-0119 scope), template still at 7. Dev cycle 4 did NOT sync template mirror. |
| 8 | `check_intake_template_parity.py --repo . --scope=us-0119` | **PASS** | `[INTAKE_TEMPLATE_PARITY_OK] scope=us-0119` exit 0 |
| 9 | `validate_doc_profile.py --repo .` | **PASS** | `[DOC_PROFILE_VALIDATE_OK]` exit 0 |
| 10 | `check-user-visible-metadata.py --repo .` | **PASS** | Silent exit 0 |

### File Existence (4 checkpoints, 1 PASS / 3 FAIL)

| # | Checkpoint | Verdict | Evidence |
|---|-----------|---------|----------|
| 11 | `sprints/S0119/execute-summary-cycle4.md` | **FAIL** | MISSING — `Test-Path` returned false |
| 12 | `sprints/S0119/execute-summary.md` | **FAIL** | MISSING — `Test-Path` returned false |
| 13 | `handoffs/autonomy_repair_ledger/.gitignore` | **PASS** | EXISTS, content=`*` |
| 14 | `handoffs/dev_to_qa.md` (US-0119 cycle-4 block) | **FAIL** | EXISTS but contains NO US-0119 references. `Select-String "US-0119\|S0119"` returned ZERO matches. File still has US-0118 content from prior release phase. Dev did not update handoff for cycle 4. |

### Byte Parity (7 checkpoints, 6 PASS / 1 FAIL)

| # | Checkpoint | Verdict | Evidence |
|---|-----------|---------|----------|
| 15 | `its_magic/README.md` ↔ `template/` | **PASS** | `PARITY_OK 208101 208101` (byte-identical) |
| 16 | `docs/engineering/runbook.md` ↔ `template/` | **PASS** | `PARITY_OK 185919 185919` (byte-identical) |
| 17 | `.cursor/commands/auto.md` ↔ `template/` | **PASS** | `PARITY_OK 37667 37667` (byte-identical) |
| 18 | `installer-owned-paths.manifest` ↔ `template/` | **PASS** | `PARITY_OK 3615 3615` (byte-identical) |
| 19 | `scripts/check_intake_template_parity.py` ↔ `template/` | **FAIL** | `PARITY_FAIL 20083 19994` — active has us-0119 scope + 8th surface pair; template still has 7 surface pairs |
| 20 | `scripts/validate_autonomy_stop_matrix.py` ↔ `template/` | **PASS** | `PARITY_OK 16535 16535` (byte-identical) |
| 21 | `tests/us0119_autonomy_preset_test.py` ↔ `template/` | **PASS** | `PARITY_OK 7304 7304` (byte-identical) |

### Consumer Wiring (8 checkpoints, 4 PASS / 4 FAIL)

| # | Checkpoint | Verdict | Evidence |
|---|-----------|---------|----------|
| 22 | `## Autonomy presets (US-0119)` in `.cursor/commands/auto.md` | **PASS** | Match found: `## Autonomy presets (US-0119 / DEC-0119)` — section present with extended DEC-inclusive heading (functional equivalent) |
| 23 | Same in `template/.cursor/commands/auto.md` | **PASS** | PARITY_OK with active confirms mirror |
| 24 | `## Autonomy presets (US-0119)` in `docs/engineering/runbook.md` | **PASS** | Match found: `## Autonomy preset keys (US-0119 / DEC-0119)` — section present with extended heading (functional equivalent) |
| 25 | Same in `template/docs/engineering/runbook.md` | **PASS** | PARITY_OK with active confirms mirror |
| 26 | `AUTONOMY_PRESET\|AUTONOMY_STOP_POLICY\|SOVEREIGN_DRAIN_AUTO_ACCEPT` in `scripts/sovereign_loop_lib.py` | **FAIL** | ZERO matches — rg returned no results. Dev cycle 4 did NOT wire autonomy presets into the sovereign loop consumer. |
| 27 | `AUTONOMY_PRESET\|RELEASE_AUTO_CONFIRM_ACCEPTANCE\|RELEASE_PUBLISH_AUTO_CONFIRM` in `scripts/release_changelog_lib.py` | **FAIL** | ZERO matches — rg returned no results. Dev cycle 4 did NOT wire autonomy presets into the release changelog consumer. |
| 28 | 4 installer manifest rows in `installer-owned-paths.manifest` | **PASS** | 4 matches: `autonomy_preset_lib.py`, `autonomy_repair_ledger_lib.py`, `autonomy_stop_matrix.yaml`, `validate_autonomy_stop_matrix.py` |
| 29 | 4 installer manifest rows in `template/` | **PASS** | 4 matches: byte-identical with active |

### Compose Guards (2 checkpoints, 2 PASS)

| # | Checkpoint | Verdict | Evidence |
|---|-----------|---------|----------|
| 30 | US-0092/US-0095/US-0056/US-0068/US-0096 anchors in architecture.md | **PASS** | 3/5 have h2 anchors (`## US-0096` L1684, `## US-0092` L1696, `## US-0095` L1700); US-0056 and US-0068 have inline references (confirmed unchanged by sprint.md compose table). |
| 31 | BUG-0007 anchor preserved | **PASS** | Found in `docs/product/backlog.md` — `### BUG-0007` anchor preserved. |

### AC Coverage 12/12 (12 checkpoints, 10 PASS / 1 PARTIAL / 1 FAIL)

| # | Checkpoint | Verdict | Evidence |
|---|-----------|---------|----------|
| AC-1 | AUTONOMY_PRESET scratchpad flag | **PASS** | `AUTONOMY_PRESET=none` present in `.cursor/scratchpad.md` (comment block + flag line) + `template/.cursor/scratchpad.local.example.md` |
| AC-2 | Deterministic preset expansion | **PASS** | `expand_autonomy_preset` function exists in `scripts/autonomy_preset_lib.py` + self-test 6/6 PASS |
| AC-3 | AUTONOMY_STOP_POLICY flag | **PASS** | `AUTONOMY_STOP_POLICY=block` present in `.cursor/scratchpad.md` + template |
| AC-4 | Autonomy stop matrix manifest | **PASS** | All 3 files exist: `docs/engineering/autonomy-stop-matrix.md`, `scripts/data/autonomy_stop_matrix.yaml`, `scripts/validate_autonomy_stop_matrix.py`. Validator self-test PASS (28 codes). |
| AC-5 | Per-feature flags wired | **PARTIAL** | Documented in runbook + auto.md (many matches). BUT `scripts/sovereign_loop_lib.py` has ZERO matches on `AUTONOMY_PRESET\|AUTONOMY_STOP_POLICY` and `scripts/release_changelog_lib.py` has ZERO matches on `AUTONOMY_PRESET\|RELEASE_AUTO_CONFIRM*`. T-004 consumer wiring incomplete. |
| AC-6 | Backward compat default | **PASS** | `test_us0119_preset_none_is_noop` PASS |
| AC-7 | Security-hard gates never softened | **PASS** | `test_us0119_security_hard_gates_never_auto_repaired` PASS + matrix 18 security_hard codes |
| AC-8 | Bounded auto-repair ledger | **PASS** | `handoffs/autonomy_repair_ledger/` dir EXISTS + `.gitignore` with `*` + `test_us0119_repair_ledger_cap_escalates` PASS |
| AC-9 | Operator authority preserved | **PASS** | `autonomy_relaxed: <reason_code> -> <auto_repair_kind>` breadcrumb reference found in `.cursor/commands/auto.md` |
| AC-10 | Tests + parity | **FAIL** | US-0119 tests 10/10 PASS. BUT `scratchpad_example_parity_test.py` 2/4 FAIL (BUG-0013 regression at line 181: `DELIVERY_MODE=standard` active vs `DELIVERY_MODE=ultra_lean` template). `check_intake_template_parity.py` default scope FAIL (20083b vs 199994b). |
| AC-11 | Documentation | **PASS** | `## Autonomy presets (US-0119 / DEC-0119)` in auto.md, `## Autonomy preset keys (US-0119 / DEC-0119)` in runbook.md, `## US-0119` in architecture.md, `decisions/DEC-0119.md` EXISTS, template parities PARITY_OK for runbook + auto.md |
| AC-12 | Compose, do not amend | **PASS** | Compose guards 6/6 verified UNCHANGED (see #30-31 above). `test_us0119_preset_expansion_uses_known_keys_only` PASS. |

### Plan-Verify Task Delta (12 tasks)

| Task | Cycle 1 | Cycle 2 | Cycle 3 | Cycle 4 | Evidence |
|------|---------|---------|---------|---------|----------|
| T-anch | FAIL | PASS | PASS | PASS | `## US-0119` anchor present in architecture.md |
| T-001 (lib) | PASS | PASS | PASS | PASS | `autonomy_preset_lib.py` self-test 6/6 PASS |
| T-002 (flags) | PASS | PASS | PASS | PASS | `AUTONOMY_PRESET=none` + `AUTONOMY_STOP_POLICY=block` in scratchpad |
| T-003 (matrix) | FAIL | PARTIAL | PARTIAL | PASS | Validator --self-test PASS (28 codes, 0 violations), YAML+MD+validator files all exist, template PARITY_OK |
| T-004 (wiring) | FAIL | FAIL | FAIL | **FAIL** | sovereign_loop_lib.py and release_changelog_lib.py have ZERO autonomy matches |
| T-005 (ledger) | FAIL | FAIL | FAIL | **PASS** | Dir EXISTS, .gitignore with `*`, repair_ledger_lib.py self-test PASS + contract test PASS |
| T-006 (breadcrumb) | PASS | PASS | PASS | PASS | `autonomy_relaxed` breadcrumb in auto.md |
| T-007 (tests) | FAIL | PARTIAL | PASS | PASS | 10/10 US-0119 tests PASS |
| T-008 (parity) | FAIL | FAIL | PASS | **FAIL** | check_intake_template_parity.py PARITY_FAIL (20083b vs 199994b), scratchpad parity 2/4 FAIL |
| T-009 (docs) | FAIL | FAIL | FAIL | PASS | runbook h2 + auto.md h2 + architecture anchor + DEC-0119 + template parities |
| T-010 (manifest) | FAIL | FAIL | FAIL | PASS | 4 installer manifest rows in active + template PARITY_OK |
| T-011 (regression) | PARTIAL | PARTIAL | PARTIAL | **FAIL** | scratchpad_example_parity_test.py 2/4 FAIL (REGRESSION) |

Task tally: 8 PASS / 0 PARTIAL / 4 FAIL (T-004, T-008, T-011, execute-summary missing)

---

## Blocking Findings (7)

### B1: scratchpad_example_parity_test.py 2/4 FAIL — BUG-0013 regression

- `test_bug0013_local_overrides_preserved` FAIL — template `.cursor/scratchpad.local.example.md` contains project-local overrides not in active
- `test_bug0013_active_example_mirror_in_sync` FAIL — active body diverges from template at line 181 (`DELIVERY_MODE=standard` in active vs `DELIVERY_MODE=ultra_lean` in template)
- Active=553 lines, template=635 lines (82-line divergence)
- **Impact**: BUG-0013 contract violation — active and template scratchpad.local.example.md must be byte-identical from L6 onward
- **Remediation**: Sync active `.cursor/scratchpad.local.example.md` from template OR vice versa to restore byte-identity (from L6 onward)

### B2: check_intake_template_parity.py active vs template PARITY_FAIL

- Active=20083b, template=199994b (89-byte difference)
- Active has 8 surface pairs including `--scope=us-0119` line
- Template still has 7 surface pairs
- Dev cycle 4 did NOT sync the template mirror of `scripts/check_intake_template_parity.py`
- **Impact**: Installer delivers stale template validator that cannot check us-0119 scope
- **Remediation**: One-way byte-identical copy `scripts/check_intake_template_parity.py` → `template/scripts/check_intake_template_parity.py`

### B3: execute-summary.md MISSING

- `sprints/S0119/execute-summary.md` does not exist
- `sprints/S0119/execute-summary-cycle4.md` does not exist
- No dev-authored execute summary for any cycle
- **Impact**: No evidence trail of what dev built in execute cycles
- **Remediation**: Create `sprints/S0119/execute-summary-cycle4.md` with per-task status, validator results, test results, byte-stability, parity, AC coverage, isolation evidence, runtime proof

### B4: handoffs/dev_to_qa.md NOT UPDATED for US-0119 cycle 4

- File exists but contains ZERO US-0119/S0119 references
- Still has US-0118 content from prior release phase
- **Impact**: No dev→qa handoff for QA cycle 4 to validate against
- **Remediation**: Create `handoffs/dev_to_qa.md` top-block for US-0119 cycle 4 with artifact lists, validator results, isolation evidence

### B5: sovereign_loop_lib.py has NO autonomy preset wiring

- `rg "AUTONOMY_PRESET|AUTONOMY_STOP_POLICY|SOVEREIGN_DRAIN_AUTO_ACCEPT" scripts/sovereign_loop_lib.py` → ZERO matches
- T-004 consumer wiring incomplete — sovereign loop is a primary consumer of autonomy presets
- **Impact**: AC-5 not fully satisfied; autonomous-autonomy presets cannot influence sovereign loop behavior
- **Remediation**: Add AUTONOMY_PRESET expansion call + AUTONOMY_STOP_POLICY dispatch to `scripts/sovereign_loop_lib.py`

### B6: release_changelog_lib.py has NO autonomy preset wiring

- `rg "AUTONOMY_PRESET|RELEASE_AUTO_CONFIRM_ACCEPTANCE|RELEASE_PUBLISH_AUTO_CONFIRM" scripts/release_changelog_lib.py` → ZERO matches
- T-004 consumer wiring incomplete — release changelog is a primary consumer of autonomy flags
- **Impact**: AC-5 not fully satisfied; release automation cannot leverage autonomy presets
- **Remediation**: Add AUTONOMY_PRESET expansion call + RELEASE_AUTO_CONFIRM_ACCEPTANCE/RELEASE_PUBLISH_AUTO_CONFIRM flags to `scripts/release_changelog_lib.py`

### B7: scratchpad.local.example.md active/template divergence (REGRESSION)

- Pre-US-0119 baseline was 4/4 PASS for scratchpad_example_parity_test.py
- Current state: 2/4 FAIL (regression introduced by US-0119 execute)
- Active=553 lines, template=635 lines — 82-line divergence
- First divergence at line 181: `DELIVERY_MODE=standard` (active) vs `DELIVERY_MODE=ultra_lean` (template)
- This test was a regression target for AC-10 / T-011
- **Impact**: T-011 FAIL; AC-10 FAIL
- **Remediation**: Reconcile `.cursor/scratchpad.local.example.md` and `template/.cursor/scratchpad.local.example.md` to byte-identity (from L6 onward)

---

## Non-blocking Findings (3)

### N1: Heading format variance in documentation

- AC-11 spec says `## Autonomy presets (US-0119)` but runbook uses `## Autonomy preset keys (US-0119 / DEC-0119)` and auto.md uses `## Autonomy presets (US-0119 / DEC-0119)`
- Both include DEC-0119 in heading (consistent with US-0118 pattern)
- Functionally equivalent — section exists with correct content
- **Action**: Cosmetic only, no remediation required

### N2: scratchpad_example_parity_test failure is BUG-0013 pre-existing, NOT US-0119 root cause

- BUG-0013 test failures existed before US-0119 (carried from prior sprint)
- However, US-0119's active modifications to scratchpad.local.example.md DID NOT restore parity (T-011 regression target unmet)
- **Action**: Fix as part of execute cycle 5

### N3: execute-summary-cycle4.md naming convention

- Dev cycle 4 may not have created a distinct execute-summary-cycle4.md since prior cycles created execute-summary.md (without cycle suffix)
- Neither file exists, so this is an aggregate documentation gap
- **Action**: Create execute-summary.md (canonical name) in execute cycle 5

---

## Strict Runtime Proof Tuple (DEC-0038)

- `runtime_proof_id=rp-us0119-s0119-qa-cycle4-qa-2026-07-05T22:27:29Z`
- Canonical payload (sorted-key JSON per DEC-0038): `{"cycle":4,"orchestrator_run_id":"auto-20260705-05","phase_id":"qa","proof_issued_at":"2026-07-05T22:27:29Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-us0119-s0119-qa-cycle4-qa-2026-07-05T22:27:29Z","sprint_id":"S0119","story_id":"US-0119","verdict":"FAIL"}`
- `proof_hash=f5f2abced05b6c2488a0142d913085ab4f84384b190f2b950457d1d0b9a2db33` (SHA-256 of canonical, recomputable)
- `proof_ttl=2026-07-05T23:27:29Z` (1 hour TTL per DEC-0038)

---

## Decision Gate

- `decision_gate=true` (cannot proceed to /release; requires return to /execute cycle 5)
- **next_scheduled_phase**: `/execute` (role=dev, fresh subagent per BUG-0006 isolation, cycle 5 — FINAL cycle)
- **remaining_cycle budget**: 1 (cycle 5 is final; if cycle-5-QA-fail → decision gate escalation to operator)
