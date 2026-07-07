# Sprint S0119 — Tasks (US-0119)

**sprint_id**: S0119
**story_refs**: US-0119
**dec_ref**: DEC-0119 (Required → Accepted; authored in architecture phase at `decisions/DEC-0119.md`)
**architecture_ref**: `docs/engineering/architecture.md` `## US-0119 — Autonomous-autonomy presets and configurable hard-stop relaxation` (L1925; approach_locked=A1)
**research_ref**: `docs/engineering/research.md` `## R-0107` (10/10 open questions Q1..Q10 closed LOCKED)
**task_count**: 12 (T-anch + T-001..T-011)
**within_limit**: true (12 ≤ `SPRINT_MAX_TASKS=12`)
**coverage**: AC-1..AC-12 surjective via T-001..T-011 + DC resolution verified via T-anch (12 ACs, 12 tasks; multi-AC tasks T-007 (AC-6+AC-7+AC-10 partial+AC-12 indirect), T-003 (AC-4+AC-7), T-008 (AC-10+AC-11 partial), T-002 (AC-1+AC-3), T-anch (AC-11 partial+AC-12); every AC has ≥1 task; no `PLAN_AC_COVERAGE_GAP`)

---

## Task-to-AC Bijection Table

| Task ID | Title | ACs Satisfied |
|---------|-------|---------------|
| T-anch | **NO-OP / verification** — confirm `## US-0119` h1 anchor already exists in `docs/engineering/architecture.md` (L1925, added in `/architecture` phase per R-0105 Q-2 LOCKED); verify compose-do-not-amend 6/6 | AC-11, AC-12 |
| T-001 | **NEW** `scripts/autonomy_preset_lib.py` — `expand_autonomy_preset(preset, overrides) -> dict` + `--self-test` + `--explain`; pure stdlib; deterministic; `AUTONOMY_PRESET ∈ {none|balanced|full}` expansion into 12 per-feature flags | AC-1, AC-2 |
| T-002 | Add `AUTONOMY_PRESET`, `AUTONOMY_STOP_POLICY`, 12 per-feature flags in `.cursor/scratchpad.md` + `template/.cursor/scratchpad.local.example.md`; merge-precedence note | AC-1, AC-3 |
| T-003 | **NEW** `docs/engineering/autonomy-stop-matrix.md` + `template/docs/engineering/autonomy-stop-matrix.md` + `scripts/data/autonomy_stop_matrix.yaml` + `scripts/validate_autonomy_stop_matrix.py --self-test` | AC-4, AC-7 |
| T-004 | Wire 12 per-feature flags into existing consumers (`/auto`, `/intake`, `/execute`, `/qa`, `/release`) | AC-5 |
| T-005 | **NEW** `handoffs/autonomy_repair_ledger/` + cap logic + `AUTONOMY_REPAIR_CAP_EXHAUSTED` terminal stop reason | AC-8 |
| T-006 | `autonomy_relaxed` breadcrumb in `docs/engineering/state.md` at phase boundary | AC-9 |
| T-007 | **NEW** `tests/us0119_autonomy_preset_test.py` — 10 contract test markers | AC-6, AC-7, AC-10, AC-12 |
| T-008 | `### Autonomy preset keys (US-0119)` README 7th sub-block + `check_intake_template_parity.py --scope=us-0119` + `AUTONOMY_PRESET_PAIRS` | AC-10, AC-11 |
| T-009 | `## Autonomy presets (US-0119)` runbook h2 + `.cursor/commands/auto.md` anchor + template parity | AC-11 |
| T-010 | `installer-owned-paths.manifest` rows for new scripts | AC-10 |
| T-011 | Regression tests `pytest tests/scratchpad_example_parity_test.py -v` 4 passed + `PARITY_OK` byte-stability proof | AC-6, AC-10 |

**Total**: 12 tasks covering 12 ACs (surjective) + DC resolution (T-anch NO-OP / verification).

---

## Execution order

```
T-anch (verify `## US-0119` anchor + compose) → T-001 (preset lib) → T-002 (scratchpad flags) →
T-003 (stop matrix + YAML + validator) → T-004 (consumer wiring) → T-005 (repair ledger) →
T-006 (breadcrumb) → T-007 (contract tests) → T-008 (README + parity) → T-009 (docs + runbook + commands) →
T-010 (installer manifest) → T-011 (regression tests)
```

Acyclic. Rationale: T-anch first (NO-OP on architecture.md). T-001→T-002→T-003 core foundation (lib + flags + matrix). T-004→T-005→T-006 consumer integration + audit surface. T-007 tests (depend on lib+matrix+ledger). T-008→T-009→T-010 docs/manifest (depend on finalized surfaces). T-011 regression guard last.

---

## Task Seeds

### T-anch: NO-OP / verification — confirm `## US-0119` h1 anchor + compose-do-not-amend

- [ ] **T-anch** — NO-OP / verification (architecture.md `## US-0119` anchor)
  - **Coverage**: AC-11 (partial — architecture section exists), AC-12
  - **Risk**: LOW
  - **Dependencies**: None (anchor already added in `/architecture` phase)
  - **Files to touch**: None (NO-OP / verification — no execute-phase write to `docs/engineering/architecture.md`)
  - **Files NOT to touch**: `docs/engineering/architecture.md` (no write — read-only verification), all 6 compose targets' architecture sections
  - **Scope**: VERIFY (do NOT write) that `## US-0119 — Autonomous-autonomy presets and configurable hard-stop relaxation` h1 anchor already exists in `docs/engineering/architecture.md` (L1925, added in `/architecture` phase per R-0105 Q-2 LOCKED). Confirm compose-do-not-amend: US-0092/US-0095/US-0056/US-0068/US-0096/BUG-0007 architectural surfaces remain read-only (no edits to their architecture sections). Confirm 23+ compose-guard UNCHANGED set locked.
  - **Verification step**: `rg -c '^## US-0119 ' docs/engineering/architecture.md` returns ≥1; `git diff HEAD -- docs/engineering/architecture.md` shows no execute-phase edits (T-anch is NO-OP).

---

### T-001: `scripts/autonomy_preset_lib.py` — preset expansion lib

- [ ] **T-001** — Preset expansion library
  - **Coverage**: AC-1, AC-2
  - **Risk**: LOW
  - **Dependencies**: T-anch (verification first)
  - **Files to touch**: `scripts/autonomy_preset_lib.py` (NEW); `template/scripts/autonomy_preset_lib.py` (NEW — byte-identical copy)
  - **Files NOT to touch**: `.cursor/commands/*.md` (T-009), `tests/*.py` (T-007)
  - **Scope**: Create `scripts/autonomy_preset_lib.py` exposing `expand_autonomy_preset(preset: str, overrides: dict[str, str] | None = None) -> dict[str, str]`. 3-tier enum: `none → {}`, `balanced → 8 flags per DEC-0119 §7`, `full → all 12 flags per DEC-0119 §7`. Precedence: explicit per-flag value in `overrides` always wins over preset default. Pure stdlib, no LLM, no network, no `.env` reads (Q3 LOCKED from R-0107). Implement `--self-test` mode (exit 0, verify known-key set, verify precedence). Implement `--explain` mode (print expansion dict for a given preset, with source annotations: `preset|explicit|default`). Implement `expand_autonomy_preset` known-keys-only guard (output keys must all be in pre-US-0119 scratchpad schema — AC-12 enforcement at lib level).
  - **Risk**: R5 (precedence — mitigated by explicit precedence chain in lib)
  - **Verification step**: `python scripts/autonomy_preset_lib.py --self-test` exits 0; `python scripts/autonomy_preset_lib.py --explain balanced` prints 8-flag dict; `python scripts/autonomy_preset_lib.py --explain full` prints 12-flag dict; template byte-identical: `fc /b scripts/autonomy_preset_lib.py template/scripts/autonomy_preset_lib.py` shows no differences.

---

### T-002: Add `AUTONOMY_PRESET` + `AUTONOMY_STOP_POLICY` + 12 per-feature flags in scratchpad

- [ ] **T-002** — Scratchpad flag surface
  - **Coverage**: AC-1, AC-3
  - **Risk**: LOW
  - **Dependencies**: T-001 (lib must exist before documenting flag surface)
  - **Files to touch**: `.cursor/scratchpad.md` (append new autonomy block after sovereign-loop era block); `template/.cursor/scratchpad.local.example.md` (mirror — preserve example-only header)
  - **Files NOT to touch**: `.cursor/scratchpad.local.md` (per DEC-0051 — local is operator territory)
  - **Scope**: Append 14 new scratchpad keys in a new `## Autonomy presets (US-0119)` block (after sovereign-loop block, before publish targets block): `AUTONOMY_PRESET=none`, `AUTONOMY_STOP_POLICY=block`, `INTAKE_AUTONOMY_MODE=0`, `INTAKE_MINIMAL_PACK=0`, `INTAKE_ASSUME_STACK_CONTEXT=0`, `WORK_KIND_AUTO_ACCEPT=0`, `CROSS_MODEL_REWORK_EXHAUSTED_POLICY=block`, `CROSS_MODEL_SKIP_PHASES=`, `RESUME_BRIEF_AUTO_REFRESH=0`, `RUNTIME_PROOF_KIND=strict`, `GOAL_CONVERGENCE_INTERVAL=3`, `SOVEREIGN_DRAIN_AUTO_ACCEPT=0`, `RELEASE_PUBLISH_AUTO_CONFIRM=0`, `AUTONOMY_REPAIR_CAP_OVERRIDE=`. Add merge-precedence note per US-0078 model B: explicit per-flag > preset expansion > scratchpad defaults. Mirror in `template/.cursor/scratchpad.local.example.md` with `example-only` header preserved; no project-local override section copied.
  - **Risk**: R1 (backward-compat — mitigated by default `AUTONOMY_PRESET=none` producing empty expansion)
  - **Verification step**: `rg 'AUTONOMY_PRESET=' .cursor/scratchpad.md` returns match; `rg 'AUTONOMY_STOP_POLICY=' .cursor/scratchpad.md` returns match; 14 new keys visible in scratchpad; template mirror contains same keys with example-only header.

---

### T-003: Stop-matrix manifest + YAML + validator

- [ ] **T-003** — Stop-matrix authority
  - **Coverage**: AC-4, AC-7
  - **Risk**: MEDIUM
  - **Dependencies**: T-001 (lib must exist to reference reason codes)
  - **Files to touch**: `docs/engineering/autonomy-stop-matrix.md` (NEW); `template/docs/engineering/autonomy-stop-matrix.md` (NEW — byte-identical copy); `scripts/data/autonomy_stop_matrix.yaml` (NEW — machine-readable); `scripts/validate_autonomy_stop_matrix.py` (NEW — validator); `template/scripts/validate_autonomy_stop_matrix.py` (NEW — byte-identical copy)
  - **Files NOT to touch**: `docs/engineering/architecture.md` (T-anch NO-OP), `.cursor/commands/*.md` (T-009)
  - **Scope**: Create operator-facing `docs/engineering/autonomy-stop-matrix.md` documenting: (a) 2-tier classification (`security_hard` / `autonomy_resolvable`), (b) 9 `autonomy_resolvable` codes per DEC-0119 §4 R-0107 Q2 mapping, (c) 18+ `security_hard` codes per DEC-0119 §3 (AC-7), (d) column table with `reason_code`, `stop_class`, `auto_repair_kind`, `cap`. Create YAML companion `scripts/data/autonomy_stop_matrix.yaml` (single source of truth). Create `scripts/validate_autonomy_stop_matrix.py --self-test` enforcing: (a) no orphan reason codes in scripts, (b) `security_hard` rows carry `auto_repair_kind=n/a`, (c) `autonomy_resolvable` rows carry finite `cap` (default 3), (d) every reason code in `.cursor/commands/*.md` is in YAML (Q8 LOCKED from R-0107). Byte-identical template copies for both md and py.
  - **Risk**: R2 (security gate bypass — mitigated by validator + contract test), R7 (validator grep fragility — mitigated by explicit YAML manifest not grep-only)
  - **Verification step**: `python scripts/validate_autonomy_stop_matrix.py --self-test` exits 0; `docs/engineering/autonomy-stop-matrix.md` contains both `security_hard` and `autonomy_resolvable` sections; `scripts/data/autonomy_stop_matrix.yaml` validates; template byte-identical: `fc /b docs/engineering/autonomy-stop-matrix.md template/docs/engineering/autonomy-stop-matrix.md` + `fc /b scripts/validate_autonomy_stop_matrix.py template/scripts/validate_autonomy_stop_matrix.py` both show no differences.

---

### T-004: Wire 12 per-feature flags into existing consumers

- [ ] **T-004** — Consumer wiring
  - **Coverage**: AC-5
  - **Risk**: MEDIUM
  - **Dependencies**: T-001 (lib), T-002 (scratchpad flags), T-003 (stop matrix)
  - **Files to touch**: `.cursor/commands/auto.md` (add `AUTONOMY_PRESET` expansion step before phase dispatch — read `AUTONOMY_PRESET` from scratchpad, call `expand_autonomy_preset`, merge into active flag bundle); `.cursor/commands/intake.md` (add `INTAKE_AUTONOMY_MODE` / `INTAKE_MINIMAL_PACK` / `INTAKE_ASSUME_STACK_CONTEXT` consumption — auto-derive answers on known-stack repeat projects per BUG-0007 assumption_confirmation_ref contract); `.cursor/commands/release.md` (add `RELEASE_PUBLISH_AUTO_CONFIRM` consumption — auto-confirm when target in `RELEASE_TARGETS_ALLOWLIST`); `.cursor/commands/execute.md` (add `RUNTIME_PROOF_KIND=lightweight` — counter+ts attestation with TTL=3600s per Q4 LOCKED)
  - **Files NOT to touch**: Compose targets (read-only) — US-0092 outer-driver semantics in `.cursor/commands/auto.md` (additive step only, no rewrite of existing outer-driver logic); US-0095 native auto-chain in `.cursor/commands/qa.md` (NOT touched — consumer wiring only touches the files listed above); US-0056 strict runtime proof semantics (NOT rewritten — `RUNTIME_PROOF_KIND=lightweight` only adds a lighter attestation kind); US-0068 evidence gate logic (NOT bypassed)
  - **Scope**: For each of the 12 per-feature flags in DEC-0119 §7, add a consumption hook in the relevant consumer file. The hook reads the flag value from scratchpad and modifies behaviour ONLY when the flag is set to its autonomy-enabled value (per AC-5 mapping). Default (0/empty/`block`/`strict`) must produce byte-identical pre-US-0119 behaviour. Preserve all existing logic; additive only.
  - **Risk**: R4 (operator confusion — mitigated by breadcrumb T-006 + ledger T-005), R6 (compose drift — mitigated by T-007 `test_us0119_preset_expansion_uses_known_keys_only`)
  - **Verification step**: Each of the 12 flags documented in consumer file; `rg 'AUTONOMY_PRESET' .cursor/commands/auto.md` shows expansion step; `rg 'INTAKE_AUTONOMY_MODE' .cursor/commands/intake.md` shows consumption; default values produce no behaviour change (verified by T-007 test_us0119_preset_none_is_noop).

---

### T-005: Bounded auto-repair ledger

- [ ] **T-005** — Repair ledger + cap logic
  - **Coverage**: AC-8
  - **Risk**: LOW
  - **Dependencies**: T-003 (stop matrix — cap taken from matrix)
  - **Files to touch**: `handoffs/autonomy_repair_ledger/` (NEW directory — gitignored at per-run path); ledger append logic integrated into T-004 consumer wiring (in `.cursor/commands/auto.md` stop-dispatch step)
  - **Files NOT to touch**: `.cursor/commands/execute.md` (repair ledger is an auto/phase-boundary concern, not execute), `.cursor/commands/qa.md` (compose target UNCHANGED)
  - **Scope**: Create `handoffs/autonomy_repair_ledger/` directory (gitignored at `handoffs/autonomy_repair_ledger/*.jsonl`). Implement append-only ledger write: per (orchestrator_run_id, reason_code) pair, append `{"reason_code": "<code>", "auto_repair_kind": "<kind>", "attempt": <int>, "outcome": "success|failure", "evidence_ref": "<path>"}` line. Cap per (run, reason_code) = 3 (from matrix default per Q3 LOCKED); operator override via optional `AUTONOMY_REPAIR_CAP_OVERRIDE=<int>` scratchpad key. Cap exhaustion → emit new terminal `AUTONOMY_REPAIR_CAP_EXHAUSTED` stop reason (distinct from `BLOCK_RETRY_CAP_EXHAUSTED` per Q9 LOCKED — run-level vs story-level). Gitignore at `handoffs/autonomy_repair_ledger/*.jsonl`.
  - **Risk**: R3 (ledger growth — mitigated by per-run cap + gitignore)
  - **Verification step**: `git status` shows `handoffs/autonomy_repair_ledger/` in gitignore; cap logic tested by T-007 `test_us0119_repair_ledger_cap_escalates`; `test_us0119_matrix_no_orphan_codes` passes.

---

### T-006: `autonomy_relaxed` breadcrumb in state.md

- [ ] **T-006** — State.md breadcrumb
  - **Coverage**: AC-9
  - **Risk**: LOW
  - **Dependencies**: T-004 (consumer wiring — breadcrumb emitted when stop is actually softened), T-005 (ledger — breadcrumb references repair attempt)
  - **Files to touch**: `docs/engineering/state.md` (append breadcrumb format description — actual breadcrumb lines appended dynamically at phase boundaries during execute)
  - **Files NOT to touch**: `docs/engineering/architecture.md` (T-anch NO-OP), prior sprint checkpoint blocks in state.md (additive only)
  - **Scope**: Document breadcrumb format in state.md sprint-plan section (or new `### Autonomy breadcrumb format` sub-section): `autonomy_relaxed: <reason_code> -> <auto_repair_kind>` per soft-stop (one-line per soft-stop per Q10 LOCKED from R-0107 — not aggregated per phase). The actual breadcrumb lines are emitted at runtime by the orchestrator at phase boundaries after a stop has been softened. The format is: one line per soft-stop, emitted after phase completes, before next phase starts.
  - **Risk**: R8 (breadcrumb granularity — mitigated by Q10 LOCKED one-line per soft-stop)
  - **Verification step**: `rg 'autonomy_relaxed' docs/engineering/state.md` shows breadcrumb format description; execute-phase will emit actual breadcrumb lines dynamically.

---

### T-007: Contract tests (10 markers)

- [ ] **T-007** — `tests/us0119_autonomy_preset_test.py`
  - **Coverage**: AC-6, AC-7, AC-10, AC-12
  - **Risk**: MEDIUM
  - **Dependencies**: T-001 (lib), T-002 (scratchpad flags), T-003 (stop matrix), T-005 (ledger)
  - **Files to touch**: `tests/us0119_autonomy_preset_test.py` (NEW — 10 contract test markers)
  - **Files NOT to touch**: `tests/scratchpad_example_parity_test.py` (T-011 regression — separate file), `tests/us0118_contract_test.py` (compose UNCHANGED)
  - **Scope**: Create `tests/us0119_autonomy_preset_test.py` with 10 `test_us0119_*` markers per DEC-0119 §9:
    1. `test_us0119_preset_none_is_noop` (AC-6) — `AUTONOMY_PRESET=none` produces byte-identical pre-US-0119 behaviour (empty expansion dict)
    2. `test_us0119_preset_balanced_expansion` (AC-2) — balanced expands into documented 8 flags per DEC-0119 §7
    3. `test_us0119_preset_full_expansion` (AC-2) — full expands into documented 12 flags per DEC-0119 §7
    4. `test_us0119_explicit_flag_overrides_preset` (AC-2) — explicit per-flag > preset expansion
    5. `test_us0119_preset_expansion_uses_known_keys_only` (AC-12) — expansion output contains only keys in pre-US-0119 scratchpad schema (compose guard)
    6. `test_us0119_matrix_validator_passes` (AC-4) — `scripts/validate_autonomy_stop_matrix.py --self-test` exits 0
    7. `test_us0119_security_hard_gates_never_auto_repaired` (AC-7) — matrix `security_hard` rows all carry `auto_repair_kind=n/a`
    8. `test_us0119_stop_policy_affects_repair_dispatch` (AC-3) — `auto_repair_then_block` vs `auto_repair_then_skip` dispatch correctly
    9. `test_us0119_repair_ledger_cap_escalates` (AC-8) — cap exhaustion → `AUTONOMY_REPAIR_CAP_EXHAUSTED` terminal stop
    10. `test_us0119_matrix_no_orphan_codes` (AC-4) — no orphan reason codes outside YAML manifest
  - **Risk**: R1 (none/noop regression — mitigated by marker 1), R2 (security gate bypass — mitigated by marker 7), R6 (compose drift — mitigated by marker 5)
  - **Verification step**: `pytest tests/us0119_autonomy_preset_test.py -v` returns 10 passed; all 10 markers enumerated in test file docstring.

---

### T-008: README 7th sub-block + parity scope + manifest

- [ ] **T-008** — README sub-block + parity
  - **Coverage**: AC-10, AC-11
  - **Risk**: MEDIUM
  - **Dependencies**: T-002 (scratchpad flags), T-008 (lib + flags finalized before README docs)
  - **Files to touch**: `its_magic/README.md` (add `### Autonomy preset keys (US-0119)` 7th sub-block under `### Full scratchpad reference (detailed)`; net-new keys only + reason-code-only entries + cross-link pointers; preserves cross-story byte-stability surface); `scripts/check_intake_template_parity.py` (add `us-0119` scope + `AUTONOMY_PRESET_PAIRS` file-pair list); `template/its_magic/README.md` (byte-identical sync); `template/scripts/check_intake_template_parity.py` (byte-identical sync)
  - **Files NOT to touch**: Prior 6 sub-blocks in README (byte-stability surface — US-0113..US-0118)
  - **Scope**: Add 7th cumulative byte-stability sub-block `### Autonomy preset keys (US-0119)` documenting: 14 new scratchpad keys (AUTONOMY_PRESET + AUTONOMY_STOP_POLICY + 12 per-feature flags) + stop-class enumeration (security_hard/autonomy_resolvable) + 9 auto_repair_kind values + AUTONOMY_REPAIR_CAP_EXHAUSTED terminal stop reason + cross-link pointers to architecture.md `## US-0119` + DEC-0119 + runbook h2 + stop-matrix manifest. Add `us-0119` scope to `check_intake_template_parity.py` with `AUTONOMY_PRESET_PAIRS` listing all 7 file-pair tuples for US-0119 surfaces. Sync template byte-identical.
  - **Risk**: R4 (operator confusion — mitigated by comprehensive README sub-block)
  - **Verification step**: `its_magic/README.md` contains `### Autonomy preset keys (US-0119)` sub-block; `python scripts/check_intake_template_parity.py --scope=us-0119` lists all 7 file-pair tuples; template byte-identical: `fc /b its_magic/README.md template/its_magic/README.md` + `fc /b scripts/check_intake_template_parity.py template/scripts/check_intake_template_parity.py`.

---

### T-009: Runbook + command docs + template parity

- [ ] **T-009** — Documentation + runbook + command anchor
  - **Coverage**: AC-11
  - **Risk**: LOW
  - **Dependencies**: T-008 (README sub-block — docs reference sub-block content)
  - **Files to touch**: `docs/engineering/runbook.md` (add `## Autonomy presets (US-0119)` h2); `template/docs/engineering/runbook.md` (byte-identical mirror); `.cursor/commands/auto.md` (add `## Autonomy presets (US-0119)` anchor); `template/.cursor/commands/auto.md` (byte-identical mirror)
  - **Files NOT to touch**: `.cursor/commands/execute.md` (US-0092 UNCHANGED — compose target), `.cursor/commands/qa.md` (US-0095 UNCHANGED — compose target)
  - **Scope**: Add `## Autonomy presets (US-0119)` h2 in runbook with: `AUTONOMY_PRESET` enum + `AUTONOMY_STOP_POLICY` enum + 12 per-feature flag reference table + operator recipe (set `AUTONOMY_PRESET=balanced` for moderate autonomy; set `AUTONOMY_PRESET=full` for maximum autonomy; set `AUTONOMY_STOP_POLICY=auto_repair_then_block` for repair+block vs `auto_repair_then_skip` for repair+skip). Add `## Autonomy presets (US-0119)` anchor in `.cursor/commands/auto.md` documenting preset expansion step + stop-policy dispatch. Byte-identical template parities for both files.
  - **Risk**: LOW (documentation only)
  - **Verification step**: `docs/engineering/runbook.md` contains `## Autonomy presets (US-0119)` h2; `.cursor/commands/auto.md` contains `## Autonomy presets (US-0119)` anchor; template parities byte-identical: `fc /b docs/engineering/runbook.md template/docs/engineering/runbook.md` + `fc /b .cursor/commands/auto.md template/.cursor/commands/auto.md`.

---

### T-010: Installer manifest rows

- [ ] **T-010** — Installer manifest
  - **Coverage**: AC-10
  - **Risk**: LOW
  - **Dependencies**: T-001 (lib), T-003 (validator script)
  - **Files to touch**: `docs/engineering/context/installer-owned-paths.manifest` (add rows under `[install_include_paths]`)
  - **Files NOT to touch**: `.cursor/scratchpad.md` (T-002), `its_magic/README.md` (T-008)
  - **Scope**: Add 4 rows to `docs/engineering/context/installer-owned-paths.manifest` under `[install_include_paths]`:
    1. `scripts/autonomy_preset_lib.py`
    2. `template/scripts/autonomy_preset_lib.py`
    3. `scripts/validate_autonomy_stop_matrix.py`
    4. `template/scripts/validate_autonomy_stop_matrix.py`
  - **Risk**: LOW (manifest rows only)
  - **Verification step**: `installer-owned-paths.manifest` contains all 4 rows; `rg 'autonomy_preset_lib' docs/engineering/context/installer-owned-paths.manifest` returns 2 matches; `rg 'validate_autonomy_stop_matrix' docs/engineering/context/installer-owned-paths.manifest` returns 2 matches.

---

### T-011: Regression tests + byte-stability proof

- [ ] **T-011** — Regression guard
  - **Coverage**: AC-6, AC-10
  - **Risk**: LOW
  - **Dependencies**: T-002 (scratchpad flags — byte-parity against template), T-008 (README sub-block — template byte-sync), T-009 (docs template parity)
  - **Files to touch**: None (regression test execution — no file modifications)
  - **Files NOT to touch**: `tests/scratchpad_example_parity_test.py` (existing regression test — MUST NOT be edited; only executed to prove byte-stability preserved)
  - **Scope**: Run `pytest tests/scratchpad_example_parity_test.py -v` and confirm 4 passed (byte-stability against pre-US-0119 baseline). Run `python scripts/check_intake_template_parity.py --scope=us-0119` and confirm `[INTAKE_TEMPLATE_PARITY_OK]`. Run `python scripts/validate_autonomy_stop_matrix.py --self-test` and confirm exit 0. Emit `PARITY_OK <active_size> <template_size>` byte-stability proof tuple for all US-0119 surface pairs.
  - **Risk**: LOW (read-only execution)
  - **Verification step**: All 3 commands return exit 0; `PARITY_OK` tuple emitted; prior regression baseline (`scratchpad_example_parity_test.py 4 passed`) preserved.

---

## Summary

- **12 tasks** exactly filling `SPRINT_MAX_TASKS=12`
- **12 ACs** covered surjectively (every AC has ≥1 task)
- **T-anch NO-OP** verifies architecture anchor + compose-do-not-amend
- **6/6 compose guards** verified UNCHANGED
- **DC check clean** (no deferred-candidate carry-over)
- **10 contract test markers** in T-007 covering AC-6/AC-7/AC-10/AC-12
- **8 risks** finalized (R1..R8) with mitigations per DEC-0119 / R-0107
