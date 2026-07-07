# QA Findings — US-0119 / S0119 / qa (merged plan-verify + qa + verify-work + UAT)

**story_id**: US-0119 — Autonomous-autonomy presets + configurable hard-stop relaxation
**sprint_id**: S0119
**phase_id**: qa (merged plan-verify + execute QA + verify-work + UAT per ultra_lean)
**role**: qa
**orchestrator_run_id**: auto-20260705-us0119-build-verify
**delivery_mode**: ultra_lean
**macro_phase**: build+verify (qa phase — second canonical phase)
**qa_cycle**: 1
**auto_loop_max_cycles**: 5
**fresh_context_marker**: qa-US0119-build-verify-20260705T212000Z-fresh
**timestamp**: 2026-07-05T21:20:00Z (UTC+2; 19:20:00Z UTC)
**runtime_proof_id**: rp-auto-20260705-us0119-qa-qa-20260705T212000Z-US-0119
**verdict**: **FAIL**

---

## Summary

QA phase cycle 1 independently verified the execute artifacts for US-0119. **Outcome: FAIL. Stop conditions NOT met. Decision gate TRUE. 9 blocking findings require return to `/execute` (dev subagent fresh per BUG-0006 isolation).**

**Key findings**:
- **Critical**: Execute phase appears incomplete — no `sprints/S0119/execute-summary.md` exists, `tests/us0119_autonomy_preset_test.py` MISSING (T-007 entirely skipped), `check_intake_template_parity.py --scope=us-0119` argparse choice missing, `template/docs/engineering/autonomy-stop-matrix.md` MISSING, `template/scripts/validate_autonomy_stop_matrix.py` MISSING.
- **Positive**: `scripts/autonomy_preset_lib.py` + `template/scripts/autonomy_preset_lib.py` both present; `--self-test` 6/6 PASS; scratchpad flags added to both `.cursor/scratchpad.md` and `template/.cursor/scratchpad.local.example.md`; `scripts/data/autonomy_stop_matrix.yaml` + `docs/engineering/autonomy-stop-matrix.md` + `scripts/validate_autonomy_stop_matrix.py` present; `## US-0119` anchor confirmed at architecture.md L1925.
- **Validator bug**: `validate_autonomy_stop_matrix.py --self-test` FAILS with 1316 "orphan code" violations — validator is over-broad, treating every uppercase Python identifier as a potential reason code. This is a dev-authored validator bug that needs fixing before the validator can be trusted.
- **Pre-existing regression (NOT US-0119)**: `tests/scratchpad_example_parity_test.py` 2/4 FAIL (pre-existing BUG-0013 residue — `CAVEMAN_LEVEL=full` / `FRAMEWORK_KIT_REPO=1` / `TOKEN_PROFILE=lean` leak into template). Out of scope for US-0119 regression targets.

---

## Test gate results

| Test gate | Result | Notes |
|-----------|--------|-------|
| `python -m pytest tests/us0119_autonomy_preset_test.py -v` | **FAIL (exit code 4)** | `ERROR: file or directory not found: tests/us0119_autonomy_preset_test.py`. Test file MISSING — T-007 not executed. |
| `python -m pytest tests/scratchpad_example_parity_test.py -v` | **FAIL (exit code 1)** | 2 passed, 2 failed. PRE-EXISTING BUG-0013 residue — `test_bug0013_local_overrides_preserved` (CAVEMAN_LEVEL/FRAMEWORK_KIT_REPO/TOKEN_PROFILE leak into template) + `test_bug0013_active_example_mirror_in_sync` (active template mirror body mismatch). NOT a US-0119 regression target. |
| `python scripts/validate_autonomy_stop_matrix.py --self-test` | **FAIL (exit code 1)** | `[MATRIX_INVALID] 1316 violation(s)` — validator is over-broad, treating every uppercase Python identifier (module constants, class names, etc.) as a potential reason code. Pre-existing files (`_build_caveman_fixtures.py`, `auto_outer_driver.py`, `dev_environment_lib.py`, etc.) contain NO US-0119 autonomy reason codes at all. Dev-authored validator bug needs correction in `/execute` (T-003). |
| `python scripts/autonomy_preset_lib.py --self-test` | **PASS (exit code 0)** | `[PASS] Test 1..6` — `6/6 tests passed`. T-001 properly implemented. |
| `python scripts/check_intake_template_parity.py --repo .` | PASS (exit code 0) | `[INTAKE_TEMPLATE_PARITY_OK] scope=intake` — default scope. |
| `python scripts/check_intake_template_parity.py --repo . --scope=us-0119` | **FAIL (exit code 2)** | `error: argument --scope: invalid choice: 'us-0119'`. Argparse choice not added to parity script. T-008 not executed. |
| `python scripts/validate_readme_feature_coverage.py --repo . --enforce` | PASS (exit code 0) | `{"coverage_missing":[],"coverage_present":[],"coverage_total":0,"status":"PASS"}` — vacuous pass (0 features expected), indicating `check_intake_template_parity.py` or validator lacks a US-0119 feature-coverage manifest entry entirely. |

---

## File existence audit (executed files vs planned files)

### Files created (T-001, T-002, T-003 partial)

| File | Expected (tasks.md) | Actual status |
|------|---------------------|---------------|
| `scripts/autonomy_preset_lib.py` | NEW (T-001) | **EXISTS** — self-test 6/6 PASS |
| `template/scripts/autonomy_preset_lib.py` | NEW byte-identical copy (T-001) | **EXISTS** — byte-identical copy |
| `.cursor/scratchpad.md` (addition) | AUTONOMY_PRESET + AUTONOMY_STOP_POLICY + 12 per-feature flags (T-002) | **MODIFIED** — AUTONOMY_PRESET present at L557/561/564/622 |
| `template/.cursor/scratchpad.local.example.md` (addition) | Mirror of scratchpad additions (T-002) | **MODIFIED** — AUTONOMY_PRESET at L557/561/564/622 |
| `docs/engineering/autonomy-stop-matrix.md` | NEW (T-003) | **EXISTS** |
| `scripts/data/autonomy_stop_matrix.yaml` | NEW machine-readable (T-003) | **EXISTS** |
| `scripts/validate_autonomy_stop_matrix.py` | NEW validator (T-003) | **EXISTS** — but `--self-test` FAILS with 1316 orphan violations (validator bug) |

### Files NOT created (execute incomplete)

| File | Expected (tasks.md) | Actual status |
|------|---------------------|---------------|
| `sprints/S0119/execute-summary.md` | NEW (execute output artifact) | **MISSING** — dev did not author execute-summary |
| `tests/us0119_autonomy_preset_test.py` | NEW 10-marker contract tests (T-007) | **MISSING** — file or directory not found |
| `template/docs/engineering/autonomy-stop-matrix.md` | NEW byte-identical copy (T-003) | **MISSING** — no template mirror |
| `template/scripts/validate_autonomy_stop_matrix.py` | NEW byte-identical copy (T-003) | **MISSING** — no template mirror |
| `handoffs/autonomy_repair_ledger/` | NEW directory + gitignore entry (T-005) | **MISSING** |
| `.cursor/commands/auto.md` (addition) | AUTONOMY_PRESET expansion hook (T-004) | **NOT MODIFIED** — grep `AUTONOMY_PRESET\|AUTONOMY_STOP_POLICY` in `.cursor/commands/auto.md` returns 0 matches |
| `.cursor/commands/intake.md` (addition) | INTAKE_AUTONOMY_MODE hook (T-004) | **NOT MODIFIED** — grep `INTAKE_AUTONOMY_MODE` returns 0 matches |
| `.cursor/commands/release.md` (addition) | RELEASE_PUBLISH_AUTO_CONFIRM hook (T-004) | **NOT MODIFIED** — grep `RELEASE_PUBLISH_AUTO_CONFIRM` returns 0 matches |
| `.cursor/commands/execute.md` (addition) | RUNTIME_PROOF_KIND=lightweight hook (T-004) | **NOT MODIFIED** — grep `RUNTIME_PROOF_KIND` returns 0 matches |
| `its_magic/README.md` (addition) | Autonomy preset keys sub-block (T-008) | **NOT MODIFIED** — `git diff --stat HEAD -- its_magic/README.md` shows 0 deletions but also 0 insertions from US-0119 (pure addition not present) |
| `scripts/check_intake_template_parity.py` (addition) | us-0119 scope + AUTONOMY_PRESET_PAIRS (T-008) | **NOT MODIFIED** — argparse choice `us-0119` missing |
| `template/its_magic/README.md` | Byte-identical copy (T-008) | **NOT MODIFIED** — 203287 bytes (matches active README size, but no US-0119 content propagated) |
| `docs/engineering/runbook.md` (addition) | ## Autonomy presets (US-0119) h2 (T-009) | **NOT MODIFIED** — grep `Autonomy presets \(US-0119\)` returns 0 matches |
| `template/docs/engineering/runbook.md` | Byte-identical copy (T-009) | **NOT MODIFIED** |
| `.cursor/commands/auto.md` (addition) | ## Autonomy presets (US-0119) anchor (T-009) | **NOT MODIFIED** |
| `template/.cursor/commands/auto.md` | Byte-identical copy (T-009) | **NOT MODIFIED** |
| `docs/engineering/context/installer-owned-paths.manifest` (addition) | 4 rows for autonomy_preset_lib + validate_autonomy_stop_matrix (T-010) | **NOT MODIFIED** — grep `autonomy_preset_lib\|validate_autonomy_stop_matrix` returns 0 matches |
| `handoffs/autonomy_repair_ledger/.gitignore` | Gitignore entry (T-005) | **MISSING** |

---

## AC coverage verification (AC-1..AC-12)

| AC | Status | Notes |
|----|--------|-------|
| AC-1 (AUTONOMY_PRESET scratchpad flag) | **PARTIAL PASS** | Flag present in `.cursor/scratchpad.md` (AUTONOMY_PRESET=none at L622) + template mirror. But without consumer wiring (T-004) and contract tests (T-007), the end-to-end AC is not fully verifiable. |
| AC-2 (Deterministic preset expansion) | **PASS** | `scripts/autonomy_preset_lib.py:expand_autonomy_preset()` exists; self-test 6/6 PASS; deterministic; pure stdlib; no LLM/network/env reads. Known-keys-only guard implemented per AC-12 enforcement. |
| AC-3 (AUTONOMY_STOP_POLICY flag) | **PARTIAL PASS** | Flag present in scratchpad + template mirror. But no consumer wiring (T-004) to actually consume it, so end-to-end AC is not verifiable. |
| AC-4 (Autonomy stop matrix manifest) | **PARTIAL PASS** | Active-side `docs/engineering/autonomy-stop-matrix.md` + `scripts/data/autonomy_stop_matrix.yaml` + `scripts/validate_autonomy_stop_matrix.py` exist. But: (a) **template mirror missing** — `template/docs/engineering/autonomy-stop-matrix.md` and `template/scripts/validate_autonomy_stop_matrix.py` absent; (b) **validator --self-test FAILS** — 1316 orphan violations due to over-broad validator bug. AC-4 is partially satisfied but the validator is not trusted. |
| AC-5 (Per-feature autonomy flags wired) | **FAIL** | **No consumer wiring in T-004 files.** 0 grep matches for `AUTONOMY_PRESET`/`AUTONOMY_STOP_POLICY`/`INTAKE_AUTONOMY_MODE`/`RELEASE_PUBLISH_AUTO_CONFIRM` in `.cursor/commands/auto.md`/`intake.md`/`release.md`/`execute.md`. The 12 per-feature flags are documented in scratchpad but NOT consumed anywhere. |
| AC-6 (Backward compatibility default) | **FAIL** | No contract test `test_us0119_preset_none_is_noop` exists. File `tests/us0119_autonomy_preset_test.py` MISSING (pytest exit 4). Cannot verify byte-identical pre-US-0119 behavior. |
| AC-7 (Security-hard gates never softened) | **FAIL** | No contract test `test_us0119_security_hard_gates_never_auto_repaired` exists. Cannot verify matrix `security_hard` rows carry `auto_repair_kind=n/a` programmatically. Validator --self-test FAILS. |
| AC-8 (Bounded auto-repair ledger) | **FAIL** | `handoffs/autonomy_repair_ledger/` directory MISSING. No gitignore entry. No cap logic. No `AUTONOMY_REPAIR_CAP_EXHAUSTED` terminal stop reason code anywhere in codebase. |
| AC-9 (Operator authority breadcrumb) | **PARTIAL PASS** | `autonomy_relaxed` breadcrumb format mentioned at state.md L769 (architecture.md prose reference to L10 — this is the architecture-level description of the breadcrumb, which is the right place for it). But no actual breadcrumb lines emitted in state.md at phase boundaries because no softening ever happened (no consumer wiring for stop-policy). |
| AC-10 (Tests + parity) | **FAIL (3 sub-gates)** | (a) Contract tests MISSING (T-007 skipped); (b) parity script `--scope=us-0119` MISSING (T-008 skipped); (c) `validate_autonomy_stop_matrix.py --self-test` FAILS. Only `autonomy_preset_lib.py --self-test` PASS (partial coverage — T-001 done, T-003/T-007/T-008 skipped). |
| AC-11 (Documentation) | **FAIL (4 sub-gates)** | (a) Runbook `## Autonomy presets (US-0119)` h2 MISSING; (b) `.cursor/commands/auto.md` h2 MISSING; (c) template parities for both MISSING; (d) architecture anchor EXISTS (L1925 — confirmed in this sprint, added in /architecture phase per R-0105 Q-2 LOCKED — T-anch NO-OP is verified at architecture.md grep-level). |
| AC-12 (Compose, do not amend) | **PASS (6/6 unchanged)** | Compose targets (US-0092/US-0095/US-0056/US-0068/US-0096/BUG-0007) UNCHANGED per grep in architecture.md + no edits to consumer files. Contract test `test_us0119_preset_expansion_uses_known_keys_only` MISSING (since T-07 skipped), so programmatic enforcement is absent, but manual inspection confirms 6/6 unchanged. |

**AC coverage tally**: 1 PASS (AC-2), 5 PARTIAL PASS (AC-1, AC-3, AC-4, AC-9, AC-12), 5 FAIL (AC-5, AC-6, AC-7, AC-8, AC-10 + AC-11 composite). **Composite verdict: FAIL**. Decision gate TRUE.

---

## Plan-verify summary (merged into qa per ultra_lean)

| Task | Plan state | Actual state | Match? |
|------|------------|--------------|--------|
| T-anch | NO-OP / verification — confirm `## US-0119` anchor + compose 6/6 | Anchor confirmed at L1925; compose 6/6 UNCHANGED | **PASS** (no execute-phase write attempted) |
| T-001 | NEW scripts/autonomy_preset_lib.py + template mirror | EXIST; self-test 6/6 PASS | **PASS** |
| T-002 | Scratchpad flags (AUTONOMY_PRESET + AUTONOMY_STOP_POLICY + 12 per-feature) | PRESENT in both scratchpad.md + template | **PASS** (flag addition only — consumer wiring not yet executed, that's T-004) |
| T-003 | Stop-matrix + YAML + validator + template parities | ACTIVE EXISTS; **template parities MISSING**; **validator --self-test FAILS 1316 violations** | **FAIL** (2 of 5 sub-artifacts missing; validator bug) |
| T-004 | Consumer wiring in auto.md / intake.md / release.md / execute.md | **NOT EXECUTED** — 0 grep matches | **FAIL** |
| T-005 | handoffs/autonomy_repair_ledger/ + gitignore + cap logic | **NOT EXECUTED** — directory missing | **FAIL** |
| T-006 | autonomy_relaxed breadcrumb in state.md | Architecture reference at state.md L769 (design-level) — OK; no runtime breadcrumbs emitted | **PASS** (design only; runtime emission depends on consumer wiring) |
| T-007 | tests/us0119_autonomy_preset_test.py (10 markers) | **NOT EXECUTED** — file missing | **FAIL** |
| T-008 | README sub-block + parity --scope=us-0119 + template mirror | **NOT EXECUTED** — 0 README insertions, 0 argparse scope additions | **FAIL** |
| T-009 | Runbook h2 + auto.md anchor + template parities | **NOT EXECUTED** | **FAIL** |
| T-010 | Installer-manifest rows (4) | **NOT EXECUTED** — 0 matches | **FAIL** |
| T-011 | Regression tests + PARITY_OK byte-stability proof | README byte-stable (PARITY_OK 203287 203287 — by inaction since T-008 skipped); **scratchpad_example_parity_test.py 2/4 FAIL pre-existing** | **PARTIAL PASS** (byte-stable but no new byte-stability to prove; legacy parities FAIL is pre-existing) |

**Plan-verify tally**: 4 PASS (T-anch, T-001, T-002, T-006), 1 PARTIAL PASS (T-003, T-011), 7 FAIL (T-003 validator + template parity missing, T-004, T-005, T-007, T-008, T-009, T-010). **Composite plan-verify verdict: FAIL**.

---

## Verify-work summary (merged into qa per ultra_lean)

**execute-summary.md**: MISSING — dev did not author a sprint execute summary. Verify-work cannot be performed without an execute-summary to cross-check.

---

## UAT summary (merged into qa per ultra_lean)

Cannot perform UAT on a FAIL verdict. UAT is gated on `qa-verdict.json` PASS + `verify-work-verdict.json` PASS. Both FAIL.

---

## Byte-stability verification

- `git diff --stat HEAD -- its_magic/README.md`:
  ```
  its_magic/README.md | 2333 +++++++++++++++++++++++++++++++++++++++++++++++++++
  1 file changed, 2333 insertions(+)
  ```
  **Pure-addition confirmed**: 0 deletions, 2333 insertions (README diff is entirely additive — no US-0113..US-0118 regression). BUT wait — 2333 insertions suggests this diff includes prior stories (US-0113..US-0118 and US-0119 additions combined), NOT a US-0119-only delta. The diff is `HEAD -- its_magic/README.md` — HEAD is the last commit, and its_magic/README.md has uncommitted working-tree changes from ALL post-last-commit additions. The US-0119-specific delta is indistinguishable from this stat alone.
- `its_magic/README.md` active size: 203287 bytes; `template/its_magic/README.md` template size: 203287 bytes — **PARITY_OK 203287 203287** (byte-identical framework README pair).
- BUT this byte-identity is by inaction (T-008 skipped). The US-0119 feature keys were not added to README. Parity check passes trivially (both sides are pre-US-0119). For US-011's contribution to be byte-stability-proven, T-008 must execute and establish the 7th cumulative sub-block.

---

## Compose verification (6/6 compose targets UNCHANGED)

| Compose target | Status | Evidence |
|---------------|--------|----------|
| US-0092 (full-autonomy outer driver) | UNCHANGED | `docs/engineering/architecture.md` L197 `| **US-0092** | Full autonomy outer driver unchanged` — pre-existing reference, not edited |
| US-0095 (native in-chat auto-chain) | UNCHANGED | `docs/engineering/architecture.md` `## US-0095` section present + unchanged |
| US-0056 (strict runtime proof) | UNCHANGED | No edits to US-0056 architecture section in working tree |
| US-0068 (evidence gate) | UNCHANGED | No edits to US-0068 architecture section in working tree |
| US-0096 (delivery modes / ultra_lean) | UNCHANGED | No edits to US-0096 architecture section in working tree |
| BUG-0007 (assumption_confirmation_ref) | UNCHANGED | No edits to BUG-0007 in working tree |

All 6/6 compose targets UNCHANGED — confirmed by grep + task-seed audit.

---

## T-anch NO-OP verification (architecture.md `## US-0119` anchor)

- `rg -c '^## US-0119 ' docs/engineering/architecture.md` → 1 match at L1925. Anchor present.
- Anchor added in `/architecture` phase (per R-0105 Q-2 LOCKED pattern).
- No execute-phase write to architecture.md confirmed (grep for execute-only artifacts in architecture.md returns no execute-specific content).

**T-anch NO-OP properly verified**: no architecture.md writes attempted during execute phase. Compose 6/6 UNCHANGED.

---

## Root cause analysis

Execute phase appears to have stopped partway through the sprint seed. Likely root causes:
1. **Dev subagent did not produce `execute-summary.md`** — suggests the execute phase itself may not have fully completed, or the handoff protocol for the merged ultra_lean flow was not correctly followed.
2. **T-003 validator bug** — ` validate_autonomy_stop_matrix.py --self-test` treats every ALL_CAPS identifier as a reason code, which means it's scanning ALL Python files (dev_environment_lib.py, auto_outer_driver.py, bug_issue_lib.py, etc.) rather than just US-0119-relevant files. This is a classic grep-over-broad bug. Fix: scope the validator to only check US-0119-defined reason codes (those in the YAML manifest) + explicit US-0119 consumer files, not arbitrary Python files.
3. **T-004..T-011 skipped** — dev likely stopped after T-001/T-002/T-003 (the foundation triad) without continuing through the execution order chain. The execution order is `T-anch → T-001 → T-002 → T-003 → T-004 → T-005 → T-006 → T-007 → T-008 → T-009 → T-010 → T-011`; skipping T-004..T-011 breaks the chain.

---

## Decision gate

**DECISION_GATE = TRUE**. Cannot proceed to `/release`. Requires return to `/execute` (dev subagent, fresh per BUG-0006) for a second cycle.

---

## Strict runtime proof tuple (DEC-0038)

- `runtime_proof_id`: `rp-auto-20260705-us0119-qa-qa-20260705T212000Z-US-0119`
- `proof_hash`: `8b2e3d4c5a6f789012345678abcdef0987654321fedcba9876543210abcdef09` (SHA-256 placeholder — orchestrator recomputes canonical_payload sorted-key JSON at flush time)
- `proof_ttl`: `2026-07-05T22:20:00Z UTC`
- `canonical_payload`: `{"delivery_mode":"ultra_lean","macro_phase":"build+verify","orchestrator_run_id":"auto-20260705-us0119-build-verify","phase_id":"qa","proof_issued_at":"2026-07-05T19:20:00Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260705-us0119-qa-qa-20260705T212000Z-US-0119","sprint_id":"S0119","story_id":"US-0119","verdict":"FAIL"}`

---

## Next actions

1. **Dev subagent (cycle 2 of `AUTO_IMPLEMENTATION_LOOP=1`)**: fresh Task-spawned per BUG-0006 isolation. Must complete T-003 validator bug fix + T-003 template parity + T-004 (consumer wiring) + T-005 (repair ledger) + T-007 (contract tests) + T-008 (README sub-block + parity --scope) + T-009 (runbook + auto.md + template parities) + T-010 (installer manifest rows) + T-011 (regression tests + byte-stability PARITY_OK proof) + `execute-summary.md`.
2. After dev cycle 2 completes with execute-summary.md, orchestrator Task-spawns fresh QA subagent for `/qa` cycle 2 to re-run the merged plan-verify + qa + verify-work + UAT.
3. If cycle 2 passes, proceed to `/release`.
