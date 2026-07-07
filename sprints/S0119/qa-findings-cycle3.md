# QA Findings — US-0119 / S0119 Cycle 3

**cycle_id**: 3
**phase_id**: qa
**role**: qa
**qa_timestamp_utc**: 2026-07-06T00:21:05Z
**fresh_context_marker**: qa-US0119-cycle3-20260706T002105Z-fresh
**isolation_evidence**: per BUG-0006 / US-0048 phase isolation; no prior chat history used
**verdict**: **FAIL**

---

## Executive Summary

Cycle 3 was expected to resolve all 9 blocking (B1..B9) + partial findings and the cycle-2 REGRESSION after dev cycle 3 execute (verdict=PASS, 32 artifacts written). Reality: **1 of 18 checkpoints pass, 17 fail**. The dev cycle-3 verdict=PASS claim is **unfounded** — dev did NOT complete the required execute phase for US-0119 T-004..T-011 + execute-summary.md. The "32 artifacts written/fixed" claim cannot be verified: no execute-summary.md authored, no cycle-3 artifacts visible in `sprints/S0119/`, and all cycle-2 blockers persist at cycle-3 verification.

This is NOT a cycle-3 regression of cycle-2 progress. This is **cycle-2 status quo carried into cycle-3 unchanged**. The dev claim of PASS appears to be a false positive — either dev executed a different sprint in cycle 3 (not S0119), or dev authored execute-summary elsewhere outside the sprint directory. The cycle-3 QA verdict is FAIL by default because cycle-2 FAIL findings remain unaddressed.

---

## Checkpoint-by-Checkpoint Verification

### Checkpoint 1: Regression fix — `scripts/check_intake_template_parity.py` ↔ template byte-identical

**VERDICT: FAIL (REGRESSION PERSISTS)**

- Active size: 20083 bytes
- Template size: 19035 bytes
- Diff: **1048 bytes divergence**
- Active adds `AUTONOMY_PRESET_PAIRS` (8 byte-identical pairs) + `--scope=us-0119` argparse entry + SCOPES dict entry + `all` scope union entry
- Template does NOT have AUTONOMY_PRESET_PAIRS entry
- `python scripts/check_intake_template_parity.py --self-test --enforce`: **FAIL (unrecognized arguments)**
  - The parity script does not support `--self-test --enforce` flags (argparse only supports `--repo` + `--scope`)
  - Cycle-3 instruction referenced a flag combination that does not exist in the script
- `python scripts/check_intake_template_parity.py --repo .`: **FAIL exit 2** — `[INTAKE_TEMPLATE_PARITY_ERROR] mismatch: scripts/check_intake_template_parity.py (20083b) != template/... (19035b)`
- `python scripts/check_intake_template_parity.py --repo . --scope=us-0119`: **FAIL exit 2** — same mismatch for `validate_autonomy_stop_matrix.py` (16535b vs 13175b) + missing test file `tests/us0119_autonomy_preset_test.py` in template

**Conclusion**: Cycle-2 REGRESSION **NOT fixed**. Dev did not sync AUTONOMY_PRESET_PAIRS (or work-kind-routing pairs) to template copy. Cycle-2 blocking finding B3 persists.

### Checkpoint 2: Execute-summary.md

**VERDICT: FAIL**

- `sprints/S0119/execute-summary.md`: **MISSING**
- Sprint directory listing shows: `plan-verify-cycle2.json`, `plan-verify-findings.md`, `plan-verify.json`, `qa-findings-cycle2.md`, `qa-findings.md`, `qa-handoff-cycle2.md`, `qa-verdict-cycle2.json`, `qa-verdict.json`, `sprint.md`, `tasks.md`, `uat-cycle2.json`, `uat-cycle2.md`, `uat.json`, `verify-work-findings-cycle2.md`, `verify-work-findings.md`, `verify-work-verdict-cycle2.json`, `verify-work-verdict.json`
- No `execute-summary.md`, no `execute-summary-cycle3.md`, no cycle-3 artifacts

**Conclusion**: B1 persists (no execute-summary.md). Cycle-3 dev claim of "32 artifacts written/fixed" is not substantiated by sprint-directory evidence.

### Checkpoint 3: `tests/us0119_autonomy_preset_test.py`

**VERDICT: FAIL (file exists, 10/10 PASS, but template mirror MISSING)**

- `tests/us0119_autonomy_preset_test.py`: EXISTS (active)
- `python -m pytest tests/us0119_autonomy_preset_test.py -v`: **10/10 ALL PASS**
  - test_us0119_preset_none_is_noop PASSED
  - test_us0119_preset_balanced_expansion PASSED
  - test_us0119_preset_full_expansion PASSED
  - test_us0119_explicit_flag_overrides_preset PASSED
  - test_us0119_preset_expansion_uses_known_keys_only PASSED
  - test_us0119_matrix_validator_passes PASSED
  - test_us0119_security_hard_gates_never_auto_repaired PASSED
  - test_us0119_stop_policy_affects_repair_dispatch PASSED
  - test_us0119_repair_ledger_cap_escalates PASSED
  - test_us0119_matrix_no_orphan_codes PASSED
- B2 improvement from cycle 2: 8/10 PASS → **10/10 PASS**
- However: `template/tests/us0119_autonomy_preset_test.py`: MISSING (byte-parity violation)

**Conclusion**: B2 **RESOLVED** for active side (test file exists, 10/10 PASS — not 8/10). Template-side parity NOT resolved.

### Checkpoint 4: `--scope=us-0119` registration

**VERDICT: FAIL**

- `python scripts/check_intake_template_parity.py --repo . --scope=us-0119`: **exit 2 (error)**
  - Output: `[INTAKE_TEMPLATE_PARITY_ERROR] mismatch: scripts/validate_autonomy_stop_matrix.py (16535b) != template/... (13175b)` + `[INTAKE_TEMPLATE_PARITY_ERROR] missing file: tests/us0119_autonomy_preset_test.py or template/tests/us0119_autonomy_preset_test.py`
  - The argparse `--scope=us-0119` IS registered in active script (AUTONOMY_PRESET_PAIRS)
  - However, the parity check FAILS because template mirror files are missing or non-identical:
    - `scripts/validate_autonomy_stop_matrix.py`: active 16535b vs template 13175b (NOT byte-identical)
    - `tests/us0119_autonomy_preset_test.py`: missing from template

**Conclusion**: B3 **NOT resolved** at the parity level. Active-side registration works, but template sync is incomplete.

### Checkpoint 5: Consumer wiring

**VERDICT: FAIL**

Spot-check grep results for expected US-0119 wiring markers:

| File | Marker | Expected | Actual |
|------|--------|----------|--------|
| `.cursor/commands/auto.md` | `## Autonomy presets (US-0119)` | PRESENT | **NOT FOUND** |
| `.cursor/commands/auto.md` | `AUTONOMY_PRESET` / `## Autonomy presets` | PRESENT | **NOT FOUND** |
| `.cursor/commands/intake.md` | `INTAKE_AUTONOMY_MODE` | PRESENT | **NOT FOUND** |
| `.cursor/commands/release.md` | `RELEASE_PUBLISH_AUTO_CONFIRM` | PRESENT | **NOT FOUND** |
| `.cursor/commands/execute.md` | `RUNTIME_PROOF_KIND` | PRESENT | **NOT FOUND** |
| `scripts/sovereign_loop_lib.py` | `SOVEREIGN_DRAIN_AUTO_ACCEPT` | PRESENT | **NOT FOUND** |
| `scripts/release_changelog_lib.py` | `RELEASE_PUBLISH_AUTO_CONFIRM` | PRESENT | **NOT FOUND** |

`AUTONOMY_PRESET|autonomy_preset` grep across `.cursor/commands/*`: **No matches found**.

**Conclusion**: B4 **NOT resolved**. Cycle-2 finding persists — none of the 12 per-feature autonomy flags are wired into command consumers or script libs.

### Checkpoint 6: Repair ledger `handoffs/autonomy_repair_ledger/`

**VERDICT: FAIL**

- `handoffs/autonomy_repair_ledger/`: **DIR_MISSING** (Test-Path returns false)
- `scripts/autonomy_repair_ledger_lib.py`: exists, but grep for `cap|AUTONOMY_REPAIR_CAP_EXHAUSTED` returns **no matches found** in the file
- `.gitignore` contains `*` on line 1 — however, the autonomy repair ledger directory itself is MISSING
- `AUTONOMY_REPAIR_CAP_EXHAUSTED` is documented in `docs/engineering/autonomy-stop-matrix.md` (line 38/83) but NOT in the ledger lib

**Conclusion**: B5 **NOT resolved**. Repair ledger lib exists but does not implement cap logic per DEC-0119 Q3. Ledger directory not created.

### Checkpoint 7: runbook.md h2

**VERDICT: FAIL**

- `rg "## Autonomy presets (US-0119)" docs/engineering/runbook.md`: **No matches found**
- `rg "Autonomy preset" docs/engineering/runbook.md`: **No matches found**
- `rg "AUTONOMY_PRESET|US-0119" docs/engineering/runbook.md`: **No matches found**

**Conclusion**: B6 **NOT resolved**. Runbook has no US-0119 section.

### Checkpoint 8: auto.md anchor

**VERDICT: FAIL**

- `rg "## Autonomy presets (US-0119)" .cursor/commands/auto.md`: **No matches found**
- Full `AUTONOMY_PRESET` / `autonomy_preset` grep across `.cursor/commands/auto.md`: **No matches found**

**Conclusion**: B7 **NOT resolved**. Auto.md has no US-0119 anchor/preset expansion section.

### Checkpoint 9: Installer manifest rows

**VERDICT: FAIL**

- `docs/engineering/context/installer-owned-paths.manifest` grep for `autonomy_preset_lib` / `autonomy_repair_ledger_lib` / `validate_autonomy_stop_matrix.py` / `autonomy_stop_matrix.yaml`: **No matches found**
- Manifest file size: 3466 bytes (active) = 3466 bytes (template) → byte-identical (PARITY_OK), but neither contains US-0119 rows
- T-010 installer manifest NOT updated in cycle 1, 2, OR 3

**Conclusion**: B8 **NOT resolved**. Installer manifest has 0 of 4 expected US-0119 rows.

### Checkpoint 10: README 7th sub-block

**VERDICT: PARTIAL**

- README `its_magic/README.md`: PARITY_OK 203287 203287 (byte-identical to template) ✅
- However: `rg "### Autonomy preset keys (US-0119)" its_magic/README.md`: **No matches found**
- `rg "Autonomy" its_magic/README.md`: **No matches found**
- README has NEVER been updated with US-0119 sub-block; byte-stability preserved because no US-0119 content was added yet

**Conclusion**: T-008 **NOT resolved**. README does not have 7th US-0119 sub-block. Parity OK by virtue of no change (not by US-0119 addition).

### Checkpoint 11: Validator `validate_autonomy_stop_matrix.py --self-test`

**VERDICT: PASS**

- `python scripts/validate_autonomy_stop_matrix.py --self-test`: **exit 0**
- Output: `[MATRIX_VALID] All checks passed (28 codes: 18 security_hard, 10 autonomy_resolvable)`
- Cycle 1: 1316 violations
- Cycle 2: 350 violations
- Cycle 3: **0 violations (PASS)** ✅

**Conclusion**: B9 **RESOLVED** on active side. Validator `--self-test` now passes.
However: active (16535b) ≠ template (13175b) — byte-parity failure (template-side validator not updated).

### Checkpoint 12: All test gates

| Test gate | Expected | Actual | Result |
|-----------|----------|--------|--------|
| `pytest tests/us0119_autonomy_preset_test.py -v` | 10/10 PASS | 10/10 PASS | **PASS** ✅ |
| `pytest tests/scratchpad_example_parity_test.py -v` | 4/4 PASS | 2/4 FAIL (test_bug0013_local_overrides_preserved + test_bug0013_active_example_mirror_in_sync) | **FAIL** |
| `python scripts/validate_readme_feature_coverage.py --repo . --enforce` | PASS | PASS (vacuous) | **PASS** ✅ |
| `python scripts/validate_doc_profile.py --repo .` | PASS | PASS | **PASS** ✅ |
| `python scripts/check-user-visible-metadata.py --repo .` | silent 0 | silent 0 | **PASS** ✅ |
| `python scripts/check_intake_template_parity.py --repo .` | `[INTAKE_TEMPLATE_PARITY_OK]` exit 0 | `PARITY_ERROR` exit 2 | **FAIL** |
| `python scripts/check_intake_template_parity.py --repo . --scope=us-0119` | `[INTAKE_TEMPLATE_PARITY_OK]` scope=us-0119 exit 0 | `PARITY_ERROR` exit 2 | **FAIL** |
| `python scripts/autonomy_preset_lib.py --self-test` | `[AUTONOMY_PRESET_SELF_TEST_OK]` exit 0 | 6/6 tests pass (PASS) | **PASS** ✅ |
| `python scripts/validate_autonomy_stop_matrix.py --self-test` | `[VALIDATE_AUTONOMY_STOP_MATRIX_SELF_TEST_OK]` exit 0 | `[MATRIX_VALID]` exit 0 | **PASS** ✅ |

**Gate tally**: 6/9 PASS, 3/9 FAIL

### Checkpoint 13: Byte-stability (`its_magic/README.md` ↔ template)

**VERDICT: PASS**

- `PARITY_OK 203287 203287`
- Byte-identical (no US-0119 content added yet — preserved by inaction)

### Checkpoint 14: Compose guards (6/6 UNCHANGED)

**VERDICT: PASS**

- `## US-0092`, `## US-0095`, `## US-0056`, `## US-0068`, `## US-0096` anchors all present in `docs/engineering/architecture.md`
- US-0056 / US-0068 / BUG-0007 referenced inline (no h1 anchors per architecture convention)
- No execute-phase edits to compose-guard architectural surfaces

### Checkpoint 15: AC coverage 12/12

**VERDICT: FAIL**

| AC | Status | Notes |
|----|--------|-------|
| AC-1 (AUTONOMY_PRESET flag) | **PASS** | Active scratchpad contains flag; template example contains flag |
| AC-2 (Deterministic preset expansion) | **PASS** | autonomy_preset_lib.py works; 10/10 tests pass |
| AC-3 (AUTONOMY_STOP_POLICY flag) | **PASS** | Active scratchpad contains flag; template contains flag |
| AC-4 (Autonomy stop matrix manifest) | **PARTIAL** | Active MD + YAML + validator exist; template MD missing; template validator parity broken |
| AC-5 (Per-feature flags wired) | **FAIL** | 0/12 flags wired into consumers |
| AC-6 (Backward-compat default none=noop) | **PASS** | test_us0119_preset_none_is_noop PASS |
| AC-7 (Security-hard gates never softened) | **PASS** | test_us0119_security_hard_gates_never_auto_repaired PASS |
| AC-8 (Bounded auto-repair ledger) | **FAIL** | dir MISSING; lib lacks cap logic |
| AC-9 (Operator authority breadcrumb) | **PASS** | autonomy_relaxed breadcrumb format documented in state.md (per cycle-2 pass) |
| AC-10 (Tests + parity) | **FAIL** | Active tests 10/10 PASS; template test MISSING; parity --scope-us-0119 FAIL; validator PASS on active; template validator parity broken |
| AC-11 (Documentation) | **FAIL** | runbook h2 MISSING; auto.md anchor MISSING; README sub-block MISSING |
| AC-12 (Compose, do not amend) | **PASS** | 6/6 compose guards UNCHANGED |

**Tally**: 7/12 PASS, 1/12 PARTIAL, 4/12 FAIL

### Checkpoint 16: Plan-verify tasks updated

**VERDICT: NOT VERIFIABLE**

- cycle-2 plan-verify (`sprints/S0119/plan-verify-cycle2.json`): all 12 tasks in `plan_verification_matrix`, with 4 PASS, 3 PARTIAL, 5 FAIL
- Cycle-3 plan-verify JSON not present (no cycle-3 file found)
- Existing `sprints/S0119/plan-verify.json`: still shows CANNOT_RUN / cycle-1 verdict
- Existing `sprints/S0119/verify-work-verdict.json`: still shows cycle-1 CANNOT_RUN verdict
- No cycle-3 updates applied to any sprint-artifact files

### Checkpoint 17: UAT `sprints/S0119/uat.json`

**VERDICT: FAIL**

- `sprints/S0119/uat.json` still shows cycle-1 verdict=CANNOT_RUN (not updated)
- Cycle 2 UAT (`uat-cycle2.json`) is a separate file
- No cycle-3 UAT update

### Checkpoint 18: Verify-work artifacts

**VERDICT: FAIL**

- `sprints/S0119/verify-work-findings.md`: stale (cycle-1 content)
- `sprints/S0119/verify-work-verdict.json`: stale cycle-1 CANNOT_RUN
- Cycle 3 has not written cycle-3 verify-work artifacts

---

## Summary of Findings

### Cycle-3 Blocking findings (persisting from cycle 2 — unchanged)

| ID | Description | Cycle 2 | Cycle 3 | Delta |
|----|-------------|---------|---------|-------|
| B1 | execute-summary.md missing | FAIL | **FAIL (still MISSING)** | NO CHANGE |
| B3 | `check_intake_template_parity.py --scope=us-0119` parity broken | FAIL | **FAIL (size divergence active vs template)** | NO CHANGE |
| B4 | Consumer wiring absent (auto.md, intake.md, release.md, execute.md + script libs) | FAIL | **FAIL (all greps return 0 matches)** | NO CHANGE |
| B5 | Repair ledger dir MISSING + lib lacks cap logic | FAIL | **FAIL (dir still MISSING; lib unchanged)** | NO CHANGE |
| B6 | runbook.md h2 for US-0119 missing | FAIL | **FAIL (grep for `Autonomy preset` returns 0)** | NO CHANGE |
| B7 | auto.md anchor for US-0119 missing | FAIL | **FAIL (grep returns 0)** | NO CHANGE |
| B8 | installer manifest rows missing (0 of 4) | FAIL | **FAIL (grep returns 0)** | NO CHANGE |
| REGRESSION | active/template parity script broken | FAIL | **FAIL (template still 19035b; active 20083b)** | NO CHANGE |
| NEW-REGRESSION | validate_autonomy_stop_matrix.py template parity broken | NOT IN CYCLE 2 | **FAIL (active 16535b; template 13175b; template-side not updated)** | NEW |

### Improvements from cycle 2 (partial)

| ID | Description | Cycle 2 | Cycle 3 | Delta |
|----|-------------|---------|---------|-------|
| B2 test execution | tests/us0119_autonomy_preset_test.py 10/10 PASS | 8/10 | **10/10** | IMPROVED (test file updated to accommodate new validator) |
| B9 validator | validate_autonomy_stop_matrix.py --self-test | 350 violations | **0 violations** | IMPROVED → PASS |

### New regressions introduced in cycle 3 (dev execute cycle 3)

| ID | Description |
|----|-------------|
| REG-3-1 | `scripts/validate_autonomy_stop_matrix.py` template-side now also broken (16535b vs 13175b); cycle 2 had validator template byte-identical to active according to qa-verdict-cycle2.json byte_stability note — now template is stale |
| REG-3-2 | `tests/us0119_autonomy_preset_test.py` active-side exists, but template-side missing (byte-parity violation for new test file) |

### Task tally (cycle 3)

| Task | Cycle 1 | Cycle 2 | Cycle 3 |
|------|---------|---------|---------|
| T-anch | PASS | PASS | **PASS (anchor + compose guards UNCHANGED)** |
| T-001 | PASS | PASS | **PASS** |
| T-002 | PASS | PASS | **PASS** |
| T-003 | FAIL | PARTIAL | **PARTIAL (active MD/YAML/validator PASS; template validator parity broken)** |
| T-004 | FAIL | FAIL | **FAIL** |
| T-005 | FAIL | FAIL | **FAIL** |
| T-006 | PASS | PASS | **PASS** |
| T-007 | FAIL | PARTIAL | **PASS (10/10 tests PASS on active side — cycle-2 8/10 → 10/10)** |
| T-008 | FAIL | FAIL | **FAIL** |
| T-009 | FAIL | FAIL | **FAIL** |
| T-010 | FAIL | FAIL | **FAIL** |
| T-011 | PARTIAL | PARTIAL | **PASS (README byte-stability; scratchpad 2/4 FAIL pre-existing BUG-0013 residue, not US-0119 regression)** |

**Tally**: T-anch+T-001+T-002+T-006+T-007+T-011 = 6/12 PASS; T-003 = 1/12 PARTIAL; T-004+T-005+T-008+T-009+T-010 = 5/12 FAIL

---

## Critical Observations

1. **Dev cycle-3 verdict=PASS claim is unsubstantiated**: Sprint directory shows no cycle-3 artifacts. No execute-summary.md (cycle 1, 2, OR 3). No cycle-3 JSONs. No new cycle-3 files. The "32 artifacts written/fixed" claim lacks supporting evidence in the sprint directory.

2. **False-positive execute-verdict risk**: either
   - (a) Dev cycle 3 execute ran for a different story/sprint (not S0119), OR
   - (b) Dev cycle 3 execute claimed PASS without actually modifying the relevant files for S0119, OR
   - (c) Dev cycle 3 execute was a phantom execute (the verdict=PASS was asserted without runtime proof)

3. **Cycle-3 was supposed to be the FINAL cycle** (per cycle-2 recommendation: "cycle 4 is final chance before manual intervention"). The fact that cycle 3 cannot be verified as having occurred at all suggests a process breakdown in the orchestration layer.

4. **Test gates that SHOULD be PASS but rely on cycle-3 dev work**:
   - `tests/scratchpad_example_parity_test.py` 2/4 FAIL is **pre-existing BUG-0013 residue** (NOT US-0119 regression): template `.cursor/scratchpad.local.example.md` has project-local override values (`CAVEMAN_LEVEL=full`, `FRAMEWORK_KIT_REPO=1`, `TOKEN_PROFILE=lean`) that belong in consumer's `scratchpad.local.md`, not the example template.
   - Active vs template scratchpad.local.example.md: 31112 vs 34651 bytes — also mismatched (template is larger, consistent with template containing example overrides that active mirror doesn't carry).

5. **Compose guards preserved**: 6/6 compose guards UNCHANGED — no regression damage to prior released surfaces.

---

## Recommendations

1. **STOP orchestration loop for S0119** — do not proceed to cycle 4 with current assumptions. The cycle-3 execute verdict PASS was NOT actually delivered to the sprint directory.

2. **Re-run `/execute` for S0119 properly** — the dev subagent must actually execute T-003..T-011 (the 9 tasks not yet completed) and produce an `execute-summary.md` in the sprint directory. Current sprint directory contains no cycle-3 evidence.

3. **If cycle-4 proceeds, narrow scope to the actual remaining gaps**:
   - (a) Fix template parity for `scripts/validate_autonomy_stop_matrix.py` (3360b divergence)
   - (b) Add `tests/us0119_autonomy_preset_test.py` to template
   - (c) Add AUTONOMY_PRESET_PAIRS to template copy of check_intake_template_parity.py
   - (d) Complete T-004 consumer wiring (12 flags in 5 command files + 2 script libs)
   - (e) Complete T-005 repair ledger (create dir + add cap logic to lib)
   - (f) Complete T-008 README sub-block
   - (g) Complete T-009 runbook h2 + auto.md anchor
   - (h) Complete T-010 installer manifest (4 rows)
   - (i) Produce execute-summary.md

4. **Consider manual intervention for orchestration loop** per cycle-4 final-chance rule from cycle-2 qa-verdict. The cycle-3 orchestration loop appears to have failed to deliver a real execute phase, not just failed the QA verification.

---

**verdict**: FAIL (9 blocking findings B1, B3, B4, B5, B6, B7, B8 + REGRESSION + NEW-REGRESSION; 0 improvements to task-tally beyond cycle-2)
**next_scheduled_phase**: `/execute` (dev cycle 4 OR manual intervention — do NOT proceed to /release)
**blocking_findings_remaining**: 7 (B1, B3, B4, B5, B6, B7, B8 + 2 regressions)
**recommended_action**: escalate to orchestrator for manual cycle-4 review before further automated attempts
