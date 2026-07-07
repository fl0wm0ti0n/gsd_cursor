# Sprint S0118 — Tasks (US-0118)

**sprint_id**: S0118
**story_refs**: US-0118
**dec_ref**: DEC-0118 (Required → Accepted; authored in architecture phase at `decisions/DEC-0118.md`)
**architecture_ref**: `docs/engineering/architecture.md` `## US-0118 — Work-kind classification + tiered delivery routing per story` (L1713; approach_locked=A1)
**research_ref**: `docs/engineering/research.md` `## R-0106` (L8754; 10/10 open questions Q1..Q10 closed LOCKED)
**task_count**: 10 (T-anch + T-001..T-009)
**within_limit**: true (10 ≤ `SPRINT_MAX_TASKS=12`)
**coverage**: AC-1..AC-12 surjective via T-001..T-009 + DC resolution verified via T-anch (12 ACs, 10 tasks; multi-AC tasks T-007 (AC-1+AC-2), T-008 (AC-4+AC-5+AC-6), T-009 (AC-7+AC-9+AC-12), T-006 (AC-8+AC-9 indirect), T-anch (AC-8+AC-10); every AC has ≥1 task; no `PLAN_AC_COVERAGE_GAP`)

---

## Task-to-AC Bijection Table

| Task ID | Title | ACs Satisfied |
|---------|-------|---------------|
| T-anch | **NO-OP / verification** — confirm `## US-0118 — Work-kind classification + tiered delivery routing per story` h1 anchor already exists in `docs/engineering/architecture.md` (L1713, added in `/architecture` phase per R-0105 Q-2 LOCKED) | AC-8, AC-10 |
| T-001 | Add `### Work-kind routing (US-0118) umbrella section` under `## Commands and workflow` in `its_magic/README.md` | AC-3 |
| T-002 | Add per-feature `#### US-0118` operator subsection under the umbrella + `## Work-kind routing (US-0118)` runbook h2 + `.cursor/commands/intake.md` step-5 hook + `.cursor/commands/auto.md` step-0 precedence clause | AC-3, AC-11 |
| T-003 | Add `### Work-kind routing keys (US-0118)` sub-block under `### Full scratchpad reference (detailed)` in `its_magic/README.md` (net-new keys + reason-code-only entries + cross-link pointers; 6th-story cumulative byte-stability surface) | AC-3 |
| T-004 | Sync `template/its_magic/README.md` byte-identical from `its_magic/README.md` | AC-12 (indirect parity) |
| T-005 | Run validators (`validate_readme_feature_coverage.py --enforce`, `validate_doc_profile.py`, `check-user-visible-metadata.py`, `check_intake_template_parity.py`) and fix any drift | AC-9 (indirect), AC-12 |
| T-006 | Run regression tests (`pytest tests/scratchpad_example_parity_test.py -v`); confirm 4 passed; forbid edits to scratchpad/test files | AC-8, AC-9 |
| T-007 | **NEW** `scripts/work_kind_classify_lib.py` — classifier lib with `classify_work_kind(...)` per R-0106 Q10 signature; pure-stdlib; import `classify_touched_files` + `TIER_C_SKIP_PREFIXES` from `dev_environment_lib` (Q9); 3-tier enum; `--explain` + `--self-test` | AC-1, AC-2 |
| T-008 | `/auto` `resolve_delivery_mode` step-0 integration + `/intake` step-5 hook + `.cursor/scratchpad.md` `WORK_KIND_ROUTING=0` key + intake evidence schema extension (3 optional fields) | AC-4, AC-5, AC-6 |
| T-009 | **NEW** `tests/us0118_contract_test.py` with 12 `test_us0118_*` markers (Q4) + installer manifest rows + `WORK_KIND_ROUTING_PAIRS` parity validator | AC-7, AC-9, AC-12 |

**Total**: 10 tasks covering 12 ACs (surjective) + DC resolution (T-anch NO-OP / verification).

---

## Execution order

```
T-anch (verify `## US-0118` anchor) → T-007 (classifier lib) → T-008 (/auto + /intake integration) →
T-009 (contract tests + reason codes + installer manifest) → T-001 (README umbrella section) →
T-002 (README per-feature subsection + runbook h2 + command docs) → T-003 (scratchpad ref sub-block) →
T-004 (template byte-sync) → T-005 (validators) → T-006 (regression tests)
```

Acyclic. Rationale for code-first ordering: T-007/T-008/T-009 (code/lib/tests) precede T-001..T-004 (README/doc surfaces) so the README byte-stability surface stays clean — the 6th sub-block documents the already-built classifier. T-anch first since it is a NO-OP on architecture.md.

---

## Task Seeds

### T-anch: NO-OP / verification — confirm `## US-0118` h1 anchor already exists in `docs/engineering/architecture.md`

- [ ] **T-anch** — NO-OP / verification (architecture.md `## US-0118` anchor)
  - **Coverage**: AC-8, AC-10
  - **Risk**: LOW
  - **Dependencies**: None (anchor already added in `/architecture` phase)
  - **Files to touch**: None (NO-OP / verification — no execute-phase write to `docs/engineering/architecture.md`)
  - **Scope**: VERIFY (do NOT write) that `## US-0118 — Work-kind classification + tiered delivery routing per story` h1 anchor already exists in `docs/engineering/architecture.md` (L1713, added in `/architecture` phase per R-0105 Q-2 LOCKED). Confirm compose-do-not-amend: US-0096/US-0070/US-0078/US-0051/US-0069/US-0103 surfaces remain read-only (no edits to their architecture sections). Confirm import-contract lock: `dev_environment_lib.classify_touched_files` + `TIER_C_SKIP_PREFIXES` are import targets (not duplicated).
  - **Verification step**: `rg -c '^## US-0118 ' docs/engineering/architecture.md` returns ≥1; `git diff HEAD -- docs/engineering/architecture.md` shows no execute-phase edits (T-anch is NO-OP).

---

### T-001: Add `### Work-kind routing (US-0118) umbrella section` under `## Commands and workflow`

- [ ] **T-001** — README umbrella section
  - **Coverage**: AC-3
  - **Risk**: LOW
  - **Dependencies**: T-anch (verification first — keeps the README byte-stability surface clean for T-001..T-004)
  - **Files to touch**: `its_magic/README.md` (append new `### Work-kind routing (US-0118) umbrella section` under `## Commands and workflow` after US-0117 umbrella close, before `### Full scratchpad reference (detailed)`)
  - **Scope**: Add `### Work-kind routing (US-0118) umbrella section` containing: `work_kind` enum `{doc, mini, code}` overview + `WORK_KIND_ROUTING` default-off callout + 3 routes summary (`doc`→`[intake,execute,release]`; `mini`→`ultra_lean`/`mega_quick`; `code`→`standard`) + L8 precedence summary + runbook pointer + zero-overhead-when-off contract paragraph.
  - **Verification step**: `its_magic/README.md` contains `### Work-kind routing (US-0118) umbrella section` heading under `## Commands and workflow` after US-0117 umbrella block; `git diff HEAD -- its_magic/README.md` shows pure addition in post-L2856 range (no edits to US-0113..US-0117 blocks).

---

### T-002: Add per-feature `#### US-0118` operator subsection + runbook h2 + command docs

- [ ] **T-002** — README subsection + runbook + command docs
  - **Coverage**: AC-3, AC-11
  - **Risk**: MEDIUM
  - **Dependencies**: T-001 (umbrella section must exist first to nest under)
  - **Files to touch**: `its_magic/README.md` (add `#### US-0118` subsection under umbrella — single subsection with route table, recommended over split-by-work_kind); `docs/engineering/runbook.md` (append `## Work-kind routing (US-0118)` h2 per Q7 LOCKED); `template/docs/engineering/runbook.md` (parity one-way copy); `.cursor/commands/intake.md` (step-5 classifier hook); `.cursor/commands/auto.md` (`resolve_delivery_mode` step-0 precedence clause); `template/.cursor/commands/intake.md` + `template/.cursor/commands/auto.md` (parity one-way copy)
  - **Scope**: Add per-feature `#### US-0118` operator subsection with route table (doc/mini/code → delivery_mode + phase_plan). Add `## Work-kind routing (US-0118)` runbook h2 with: `WORK_KIND_ROUTING` flag, L8 precedence, operator recipe (force full lifecycle on `doc` story via `DELIVERY_MODE=standard`), `--explain` usage, four `WORK_KIND_*` reason codes. Add `/intake` step-5 hook + `/auto` step-0 precedence clause in command docs.
  - **Verification step**: `its_magic/README.md` contains `#### US-0118` subsection; `docs/engineering/runbook.md` contains `## Work-kind routing (US-0118)` h2; `.cursor/commands/intake.md` documents step-5 hook; `.cursor/commands/auto.md` documents L8 precedence clause; template parities byte-identical.

---

### T-003: Add `### Work-kind routing keys (US-0118)` sub-block under `### Full scratchpad reference (detailed)`

- [ ] **T-003** — README scratchpad ref sub-block (6th sibling)
  - **Coverage**: AC-3
  - **Risk**: MEDIUM (first 6-cumulative-surface story)
  - **Dependencies**: T-001 (umbrella section must exist first)
  - **Files to touch**: `its_magic/README.md` (add `### Work-kind routing keys (US-0118)` sub-block under `### Full scratchpad reference (detailed)` after US-0117 L2856 block, before `### Remote execution config`)
  - **Scope**: Add `### Work-kind routing keys (US-0118)` sub-block — net-new key rows (`WORK_KIND_ROUTING`, `WORK_KIND_TIE_BREAK`, etc. per R-0106 Q5/Q9) + reason-code-only entries (`WORK_KIND_*` family from R-0106 Q2 — `WORK_KIND_CLASSIFY_FAILED`, `WORK_KIND_DELIVERY_MODE_CONFLICT`, `WORK_KIND_ROUTING_DISABLED`, `WORK_KIND_PLAN_COVERAGE_MISSING`) + cross-link pointers (`DELIVERY_MODE` → US-0114; `AUTO_PHASE_*` → US-0070; etc.). 6th-story cumulative byte-stability surface — prior 5 released blocks US-0113..US-0117 byte-stable; US-0118 adds net-new-keys-only + cross-link pointers, never edits prior released blocks.
  - **Verification step**: `its_magic/README.md` contains `### Work-kind routing keys (US-0118)` sub-block after US-0117 block; `git diff HEAD -- its_magic/README.md` shows pure addition (no removals/modifications to US-0113 L2421, US-0114 L2545, US-0115 L2617, US-0116 L2765, or US-0117 L2856 blocks).

---

### T-004: Sync `template/its_magic/README.md` byte-identical from `its_magic/README.md`

- [ ] **T-004** — Template byte-sync
  - **Coverage**: AC-12 (indirect parity)
  - **Risk**: MEDIUM
  - **Dependencies**: T-001, T-002, T-003 (README edits complete first)
  - **Files to touch**: `template/its_magic/README.md` (one-way byte-identical copy from `its_magic/README.md`)
  - **Scope**: Sync `template/its_magic/README.md` byte-identical to `its_magic/README.md`.
  - **Verification step**: `PARITY_OK <size> <size>` (sizes match); `python scripts/check_intake_template_parity.py --repo .` → `[INTAKE_TEMPLATE_PARITY_OK] scope=intake` exit 0.

---

### T-005: Run validators and fix any drift

- [ ] **T-005** — Validators
  - **Coverage**: AC-9 (indirect), AC-12
  - **Risk**: LOW
  - **Dependencies**: T-001, T-002, T-003, T-004 (README + template edits complete first)
  - **Files to touch**: validators are read-only gates, not edit targets (fix prose drift if any)
  - **Scope**: Run `python scripts/validate_readme_feature_coverage.py --repo . --enforce` → `[README_FEATURE_COVERAGE_VALIDATE_OK]` with `coverage_missing=["US-0118"]` baseline (US-0118 not in catalog surface). Run `python scripts/validate_doc_profile.py --repo .` + `python scripts/check-user-visible-metadata.py --repo .` + `python scripts/check_intake_template_parity.py --repo .` → expect PASS. Fix any narrative prose leaking internal IDs.
  - **Verification step**: All 4 validators exit 0; no internal IDs in operator-visible prose.

---

### T-006: Run regression tests

- [ ] **T-006** — Regression tests
  - **Coverage**: AC-8, AC-9
  - **Risk**: LOW–MEDIUM
  - **Dependencies**: T-001..T-005 (all README/template edits complete first)
  - **Files to touch**: None (forbid edits to `.cursor/scratchpad.md`, `template/.cursor/scratchpad.local.example.md`, `tests/scratchpad_example_parity_test.py`)
  - **Scope**: Run `python -m pytest tests/scratchpad_example_parity_test.py -v` → 4 passed. Forbid edits to scratchpad/test files.
  - **Verification step**: `4 passed` (BUG-0013 parity baseline green; not weakened).

---

### T-007: NEW `scripts/work_kind_classify_lib.py` — classifier lib

- [ ] **T-007** — Classifier library (NEW)
  - **Coverage**: AC-1, AC-2
  - **Risk**: MEDIUM
  - **Dependencies**: T-anch (import-contract lock verified first)
  - **Files to touch**: `scripts/work_kind_classify_lib.py` (NEW); `template/scripts/work_kind_classify_lib.py` (NEW parity one-way copy)
  - **Scope**: Create `scripts/work_kind_classify_lib.py` exposing `classify_work_kind(story_prose, acceptance_criteria, touched_file_hints, component_scope) -> WorkKindClassification` per R-0106 Q10 signature. Pure-stdlib (Q3 LOCKED); import `TIER_C_SKIP_PREFIXES` + `classify_touched_files` from `dev_environment_lib` (Q9 LOCKED import contract — no duplication). 3-tier enum `WorkKind.DOC / MINI / CODE`. Implement doc/mini/code rules per AC-2 + Q1 tie-break (highest tier wins). Derive `recommended_delivery_mode` + `recommended_phase_plan`. `--explain` flag emits `rule_trace` (Q3). `--self-test` exits 0 (AC-12). Reason-code family `WORK_KIND_*` (Q2).
  - **Verification step**: `python scripts/work_kind_classify_lib.py --self-test` exits 0; `python -c "from work_kind_classify_lib import classify_work_kind, WorkKind; print(classify_work_kind('test', ['AC-1'], ['docs/foo.md'], None))"` returns a `WorkKindClassification` with `work_kind=doc`.

---

### T-008: `/auto` + `/intake` integration + scratchpad key + intake evidence schema

- [ ] **T-008** — Integration (auto + intake + scratchpad + evidence schema)
  - **Coverage**: AC-4, AC-5, AC-6
  - **Risk**: MEDIUM
  - **Dependencies**: T-007 (classifier lib must exist first)
  - **Files to touch**: `.cursor/commands/auto.md` (`resolve_delivery_mode` step-0 precedence clause — minimal hook, early-return when `WORK_KIND_ROUTING != "1"`); `.cursor/commands/intake.md` (step-5 classifier hook — after ACs + after US-0051 decomposition evaluator, before persistence); `.cursor/scratchpad.md` (NEW `WORK_KIND_ROUTING=0` key with merge-precedence note); `template/.cursor/scratchpad.local.example.md` (mirror `WORK_KIND_ROUTING` row); `handoffs/intake_evidence/*.json` (schema extension: 3 new optional fields `work_kind`, `recommended_delivery_mode`, `work_kind_operator_decision ∈ {accept, override}`); `template/.cursor/commands/auto.md` + `template/.cursor/commands/intake.md` (parity one-way copy)
  - **Scope**: `/auto` `resolve_delivery_mode` step-0 minimal hook (early-return when `WORK_KIND_ROUTING != "1"`; precedence chain L8: explicit `DELIVERY_MODE` > `AUTO_PHASE_*` > `WORK_KIND_ROUTING` derived > current default; `start-from` always wins; `WORK_KIND_DELIVERY_MODE_CONFLICT` reason code when both set). `/intake` step-5 hook (run classifier after ACs + after US-0051 decomposition evaluator, before persistence; present `work_kind` + `recommended_delivery_mode` to operator for accept/override; persist choice in backlog row + intake evidence bundle). Add `WORK_KIND_ROUTING=0` to `.cursor/scratchpad.md` + `template/.cursor/scratchpad.local.example.md` with merge-precedence note (US-0078 model B: local > materialized baseline > example). Extend `handoffs/intake_evidence/*.json` schema with 3 optional fields. US-0078 evidence gate still runs before any backlog/acceptance write.
  - **Verification step**: `.cursor/commands/auto.md` documents L8 precedence clause; `.cursor/commands/intake.md` documents step-5 hook; `.cursor/scratchpad.md` contains `WORK_KIND_ROUTING=0`; intake evidence schema extended with 3 optional fields.

---

### T-009: NEW `tests/us0118_contract_test.py` + installer manifest + parity validator

- [ ] **T-009** — Contract tests + installer manifest + parity validator (NEW)
  - **Coverage**: AC-7, AC-9, AC-12
  - **Risk**: MEDIUM
  - **Dependencies**: T-007 (classifier lib must exist first), T-008 (integration must exist first)
  - **Files to touch**: `tests/us0118_contract_test.py` (NEW — 12 `test_us0118_*` markers per Q4 LOCKED); `template/tests/us0118_contract_test.py` (NEW parity); `installer-owned-paths.manifest` (add `scripts/work_kind_classify_lib.py` + `template/scripts/work_kind_classify_lib.py` to `[install_include_paths]`); `scripts/check_intake_template_parity.py` (add `WORK_KIND_ROUTING_PAIRS` manifest constant + `--scope=work-kind-routing` flag per Q6 LOCKED); `template/scripts/check_intake_template_parity.py` (parity one-way copy)
  - **Scope**: Create `tests/us0118_contract_test.py` with 12 `test_us0118_*` markers (Q4 LOCKED): `test_us0118_doc_kind_routes_to_lean_plan`, `test_us0118_mini_kind_routes_to_ultra_lean`, `test_us0118_mini_kind_routes_to_mega_quick_when_eligible`, `test_us0118_code_kind_routes_to_standard`, `test_us0118_explicit_delivery_mode_wins_over_work_kind`, `test_us0118_auto_phase_wins_over_work_kind`, `test_us0118_routing_off_is_noop`, `test_us0118_classify_touched_files_reuse`, `test_us0118_intake_evidence_records_work_kind`, `test_us0118_reason_codes_preserved`, `test_us0118_default_off_zero_overhead`, `test_us0118_explain_emits_rule_trace`. Add `scripts/work_kind_classify_lib.py` + `template/scripts/work_kind_classify_lib.py` to `installer-owned-paths.manifest` `[install_include_paths]` (Q10/installer parity — triple-installer PS1/Bash/Python ships the new script). Add `WORK_KIND_ROUTING_PAIRS` to `scripts/check_intake_template_parity.py` + `--scope=work-kind-routing` flag (Q6). Active + `template/` parity for new script + scratchpad lines.
  - **Verification step**: `python -m pytest tests/us0118_contract_test.py -v` → 12 passed; `installer-owned-paths.manifest` contains both script paths; `python scripts/check_intake_template_parity.py --scope=work-kind-routing --repo .` → PASS.
