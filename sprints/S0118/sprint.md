# Sprint S0118

## Metadata

- **sprint_id**: S0118
- **story_refs**: US-0118
- **priority**: P2
- **effort**: 1–2 days
- **owner**: dev
- **goal**: Ship the first **code-bearing** story in the new drain — a deterministic per-story **work-kind classifier** `scripts/work_kind_classify_lib.py:classify_work_kind(story_prose, acceptance_criteria, touched_file_hints, component_scope) -> WorkKindClassification` returning `work_kind ∈ {doc, mini, code}` + `recommended_delivery_mode ∈ {standard, ultra_lean, mega_quick}` + `recommended_phase_plan` + `rationale` + `evidence_refs` (+ optional `rule_trace` via `--explain`). Gated by a new default-off `WORK_KIND_ROUTING=0|1` scratchpad flag (zero overhead when off — early-return in `/auto` `resolve_delivery_mode` step 0 + `/intake` step 5 skip when `WORK_KIND_ROUTING != "1"`). Backlog rows gain optional `work_kind` + `recommended_delivery_mode` fields set at intake (operator accept/override; recorded in intake evidence bundle per US-0078/DEC-0060). `/auto` `resolve_delivery_mode` step 0 consumes them when `DELIVERY_MODE`/`AUTO_PHASE_*` are unset (L8 precedence: explicit `DELIVERY_MODE` > explicit `AUTO_PHASE_*` > `WORK_KIND_ROUTING`-derived > current default; `start-from` always wins). `doc` → `[intake, execute, release]`; `mini` → `ultra_lean` or `mega_quick` (US-0096 eligibility); `code` → `standard`. Reuses `scripts/dev_environment_lib.py:classify_touched_files()` tier A/B/C + `TIER_C_SKIP_PREFIXES` — import, do not reinvent (Q9 LOCKED). Deterministic pure-stdlib, no LLM, no network, no `.env` reads (Q3 LOCKED). Four `WORK_KIND_*` reason codes (Q2 LOCKED). 12 `test_us0118_*` contract test markers (Q4 LOCKED). New `### Work-kind routing keys (US-0118)` README sub-block (Q5 LOCKED — 6th sibling; first **6th-story cumulative byte-stability surface** story — prior 5 released blocks US-0113..US-0117 must remain byte-identical; US-0118 adds net-new-keys-only + cross-link-pointers + reason-code-only entries to its own 6th sub-block, never edits prior released blocks) + new `## Work-kind routing (US-0118)` runbook h2 (Q7 LOCKED). Triple-installer parity (Q10/installer manifest). Composes read-only with 6 consumers (US-0096/US-0070/US-0078/US-0051/US-0069/US-0103) — additive only.
- **status**: OPEN (per US-0045 — closure at /release)
- **created_at**: 2026-07-04T23:24:00Z
- **orchestrator_run_id**: auto-20260704-01
- **delivery_mode**: ultra_lean
- **macro_phase**: plan (sprint-plan — third canonical phase)
- **fresh_context_marker**: tl-US0118-sprint-plan-20260704T232400Z-fresh
- **resolved_phase_plan**: `["spec","plan","build+verify","ship"]` (ultra_lean macro — recomputed at story boundary per US-0044 / DEC-0022; `spec` already done via intake+discovery merged; `plan` = research + architecture + sprint-plan all complete; `build+verify` = `/execute` + `/qa` (merges plan-verify + execute QA + verify-work — `plan-verify.json` created by QA within `build+verify`); `ship` = `/release` + `/refresh-context`)

## Scope

- **US-0118**: Work-kind classification + tiered delivery routing per story — first **code-bearing** story in new drain (US-0113..US-0117 were documentation-only)
- **Architecture anchor**: `docs/engineering/architecture.md` `## US-0118 — Work-kind classification + tiered delivery routing per story` (L1713; appended after `## US-0099`; approach_locked=A1)
- **Research anchor**: `docs/engineering/research.md` `## R-0106 - US-0118 Work-kind classification + tiered delivery routing research` (L8754; 10/10 open questions Q1..Q10 closed LOCKED)
- **Companion DEC**: **DEC-0118** (Required → Accepted; authored in architecture phase at `decisions/DEC-0118.md`; mirrors DEC-0082/DEC-0052 precedent — locks work-kind 3-tier enumeration + L8 precedence chain + `dev_environment_lib.classify_touched_files` reuse boundary + zero-overhead-when-off contract)

## DC resolution note

US-0118 is the first story of a new drain (post-US-0117 drain completion). `grep "^## US-0118" docs/engineering/architecture.md` prior to the `/architecture` phase → no matches. The `## US-0118` h1 anchor was **added in the `/architecture` phase** (per R-0105 Q-2 LOCKED pattern — architecture artifacts live in `architecture.md`, not `/execute`). US-0117 was the **final deferred-candidate resolution point** (36 anchors added in US-0117's architecture phase). US-0118 inherits a clean deferral register; no DC candidates created or carried. **Consequence for this sprint**: **T-anch is a NO-OP / verification task** — the `## US-0118` anchor already exists at architecture.md L1713; T-anch verifies it remains present and that `git diff HEAD -- docs/engineering/architecture.md` shows no execute-phase edits to architecture.md.

## Acceptance criteria (US-0118 — 12 ACs verbatim from `docs/product/backlog.md` `## US-0118`)

| AC | Description (verbatim) |
|----|-------------|
| AC-1 | **Classifier library** — `scripts/work_kind_classify_lib.py` exposes `classify_work_kind(story_prose, acceptance_criteria, touched_file_hints, component_scope) -> WorkKindResult` returning `work_kind ∈ {"doc","mini","code"}`, `recommended_delivery_mode` (`standard`\|`ultra_lean`\|`mega_quick`), `recommended_phase_plan` (list of canonical phase ids), `rationale` (string), and `evidence_refs` (names-only). Pure stdlib, no network, no `.env` reads. |
| AC-2 | **Classification rules** — `doc` when all touched files match `dev_environment_lib.TIER_C_SKIP_PREFIXES` or are `*.md`/`README*` under skip prefixes → phase plan `[intake, execute, release]` (skip discovery/research/architecture/sprint-plan/plan-verify/qa/verify-work). `mini` when single component, ACs <= 3, no companion DEC required → `ultra_lean` or `mega_quick` (reuse US-0096 `mega_quick` eligibility). `code` otherwise → `standard` (or current `DELIVERY_MODE`). |
| AC-3 | **Scratchpad flag** — new `WORK_KIND_ROUTING=0\|1` (default `0`). When `0`, zero overhead: `/auto` `resolve_delivery_mode` and intake persistence skip classifier entirely. When `1`, classifier runs at intake (after ACs) and at `/auto` step 0. Documented in `.cursor/scratchpad.md` + `template/.cursor/scratchpad.local.example.md` with merge-precedence note. |
| AC-4 | **Backlog row fields** — `docs/product/backlog.md` story blocks support optional `- work_kind: doc\|mini\|code` and `- recommended_delivery_mode: standard\|ultra_lean\|mega_quick` rows. Intake writes them when `WORK_KIND_ROUTING=1` and operator accepts; absence is valid (classifier not run). Acceptance traceability updated. |
| AC-5 | **Intake integration** — `/intake` step 5 (after ACs drafted, after decomposition evaluator, before persistence): when `WORK_KIND_ROUTING=1`, run classifier, propose `work_kind` + `recommended_delivery_mode`, present to operator for accept/override. Persist choice in backlog row + intake evidence bundle (`work_kind`, `recommended_delivery_mode`, `work_kind_operator_decision` ∈ {accept, override}). US-0078 evidence gate still runs before any backlog/acceptance write. |
| AC-6 | **`/auto` integration** — `/auto` `resolve_delivery_mode` (step 0) gains precedence clause: when `WORK_KIND_ROUTING=1` **and** backlog row carries `work_kind` **and** `DELIVERY_MODE` scratchpad key is unset **and** `AUTO_PHASE_*` keys are unset, derive `resolved_phase_plan` from `recommended_delivery_mode`. Explicit `DELIVERY_MODE` / `AUTO_PHASE_*` / `start-from` always win. Precedence order documented in `.cursor/commands/auto.md`. |
| AC-7 | **Fail-closed reason codes** — `WORK_KIND_CLASSIFY_FAILED`, `WORK_KIND_DELIVERY_MODE_CONFLICT` (work-kind recommends mode X but `DELIVERY_MODE` set to Y and they conflict), `WORK_KIND_ROUTING_DISABLED` (info when flag off), `WORK_KIND_PLAN_COVERAGE_MISSING` (classifier returned an empty/invalid phase plan). Each emits remediation guidance in `sprints/Sxxxx/qa-findings.md` / `release-findings.md`. |
| AC-8 | **Compose, do not amend** — US-0096 (delivery modes), US-0070 (phase selection), US-0078 (intake evidence), US-0051 (decomposition), US-0069 (phase→role matrix), US-0103 (AI decision ledger — read-only consumer) all unchanged. Additive only: new flag, new lib, new row fields, new precedence clause. |
| AC-9 | **Contract tests + parity** — `tests/work_kind_classify_test.py` with `test_us0118_*` markers covering: each work-kind classification, each recommended phase plan, default-off zero-overhead, precedence vs `DELIVERY_MODE`/`AUTO_PHASE_*`, operator override path, each fail-closed reason code. `check_intake_template_parity.py --scope=work-kind-routing` when intake/scratchpad surfaces touched. Active + `template/` parity for new script + scratchpad lines. |
| AC-10 | **Architecture notes** — `docs/engineering/architecture.md` `# US-0118` documents classifier contract, work-kind enumeration, precedence chain, fail-closed codes, composition with US-0096/US-0070/US-0078/US-0051/US-0069, and the `dev_environment_lib.classify_touched_files` reuse anchor. Active + `template/` parity. |
| AC-11 | **Runbook + command docs** — `docs/engineering/runbook.md` documents `WORK_KIND_ROUTING` flag + operator recipe (how to force full lifecycle on a `doc` story by setting `DELIVERY_MODE=standard`). `.cursor/commands/intake.md` + `.cursor/commands/auto.md` document the classifier hook + precedence. `template/` parity. |
| AC-12 | **Self-test + installer delivery** — `python scripts/work_kind_classify_lib.py --self-test` exits 0; `installer-owned-paths.manifest` `[install_include_paths]` lists `scripts/work_kind_classify_lib.py` + `template/scripts/work_kind_classify_lib.py`; triple-installer parity (PS1/Bash/Python) ships the new script. |

## AC → task surjective coverage (10 tasks, 12 ACs)

| AC | Task(s) | Architecture anchor |
|----|---------|---------------------|
| AC-1 (Classifier library) | T-007 | § Sprint seeds T-007 |
| AC-2 (Classification rules) | T-007 | § Sprint seeds T-007 |
| AC-3 (Scratchpad flag) | T-001, T-003 | § Sprint seeds T-001 / T-003 |
| AC-4 (Backlog row fields) | T-008 | § Sprint seeds T-008 |
| AC-5 (Intake integration) | T-008 | § Sprint seeds T-008 |
| AC-6 (`/auto` integration) | T-008 | § Sprint seeds T-008 |
| AC-7 (Fail-closed reason codes) | T-009 | § Sprint seeds T-009 |
| AC-8 (Compose, do not amend) | T-anch, T-006 | § Sprint seeds T-anch / T-006 |
| AC-9 (Contract tests + parity) | T-009, T-006 | § Sprint seeds T-009 / T-006 |
| AC-10 (Architecture notes) | T-anch | § Sprint seeds T-anch (NO-OP / verification — `## US-0118` already added in `/architecture`) |
| AC-11 (Runbook + command docs) | T-002 | § Sprint seeds T-002 |
| AC-12 (Self-test + installer delivery) | T-005, T-009 | § Sprint seeds T-005 / T-009 |

**Surjectivity check**: AC-1..AC-12 all covered (12/12) + DC resolution verified (T-anch). Multi-AC tasks: **T-007** (AC-1+AC-2), **T-008** (AC-4+AC-5+AC-6), **T-009** (AC-7+AC-9+AC-12 partial), **T-006** (AC-8+AC-9 indirect regression), **T-anch** (AC-8 compose verification + AC-10 architecture verification). Every AC has ≥1 task. No `PLAN_AC_COVERAGE_GAP`.

## Task count

- **Total**: 10 (T-anch + T-001..T-009)
- **SPRINT_MAX_TASKS**: 12 (from `.cursor/scratchpad.md`)
- **Within limit**: yes (10 ≤ 12; `SPRINT_AUTO_SPLIT` not triggered)
- **SPRINT_AUTO_SPLIT_TRIGGERED**: false

## Sprint seeds (T-anch + T-001..T-009 — refined from architecture section)

Execution order (per architecture dependency chain, refined for code-first ordering):

```
T-anch (verify `## US-0118` anchor) → T-007 (classifier lib) → T-008 (/auto + /intake integration) →
T-009 (contract tests + reason codes + installer manifest) → T-001 (README umbrella section) →
T-002 (README per-feature subsection + runbook h2 + command docs) → T-003 (scratchpad ref sub-block) →
T-004 (template byte-sync) → T-005 (validators) → T-006 (regression tests)
```

**Rationale for code-first ordering**: T-007/T-008/T-009 (code/lib/tests) precede T-001..T-004 (README/doc surfaces) so that the README byte-stability surface stays clean — the 6th sub-block documents the already-built classifier. T-anch first since it is a NO-OP on architecture.md.

| ID | Title | ACs | Tranche | Risk |
|----|-------|-----|:--------|:-----|
| T-anch | **NO-OP / verification** — confirm `## US-0118 — Work-kind classification + tiered delivery routing per story` h1 anchor already exists in `docs/engineering/architecture.md` (L1713, added in `/architecture` phase per R-0105 Q-2 LOCKED). No new write. Verify `git diff HEAD -- docs/engineering/architecture.md` shows no execute-phase edits to architecture.md. Compose-do-not-amend: confirm 6 read-only consumers (US-0096/US-0070/US-0078/US-0051/US-0069/US-0103) remain unedited. Import-contract lock: confirm `dev_environment_lib.classify_touched_files` + `TIER_C_SKIP_PREFIXES` are import targets (not duplicated). | AC-8, AC-10 | A | LOW |
| T-001 | Add `### Work-kind routing (US-0118) umbrella section` under `## Commands and workflow` in `its_magic/README.md` after US-0117 umbrella close, before `### Full scratchpad reference (detailed)`. Contains: `work_kind` enum `{doc, mini, code}` overview + `WORK_KIND_ROUTING` default-off callout + 3 routes summary (`doc`→`[intake,execute,release]`; `mini`→`ultra_lean`/`mega_quick`; `code`→`standard`) + L8 precedence summary + runbook pointer + zero-overhead-when-off contract paragraph. | AC-3 | A | LOW |
| T-002 | Add per-feature `#### US-0118` operator subsection(s) under the umbrella (single US-0118 subsection with route table — recommended over split-by-work_kind) + `## Work-kind routing (US-0118)` h2 in `docs/engineering/runbook.md` (Q7 LOCKED) + `template/docs/engineering/runbook.md` parity. Runbook content: `WORK_KIND_ROUTING` flag, L8 precedence, operator recipe (force full lifecycle on `doc` story via `DELIVERY_MODE=standard`), `--explain` usage, four `WORK_KIND_*` reason codes. `.cursor/commands/intake.md` step-5 hook + `.cursor/commands/auto.md` `resolve_delivery_mode` step-0 precedence clause. `template/.cursor/commands/` parity. | AC-3, AC-11 | A | MEDIUM |
| T-003 | Add `### Work-kind routing keys (US-0118)` sub-block under `### Full scratchpad reference (detailed)` in `its_magic/README.md` after US-0117 block (L2856), before `### Remote execution config`. Net-new key rows (`WORK_KIND_ROUTING`, `WORK_KIND_TIE_BREAK`, etc. per R-0106 Q5/Q9) + reason-code-only entries (`WORK_KIND_*` family from R-0106 Q2) + cross-link pointers (`DELIVERY_MODE` → US-0114; `AUTO_PHASE_*` → US-0070; etc.). **6th-story cumulative byte-stability surface** — prior 5 released blocks US-0113..US-0117 byte-stable; US-0118 adds net-new-keys-only + cross-link pointers, never edits prior released blocks. | AC-3 | A | MEDIUM (first 6-cumulative-surface story) |
| T-004 | Sync `template/its_magic/README.md` byte-identical to `its_magic/README.md` (one-way copy). Verify `PARITY_OK <size> <size>` + `[INTAKE_TEMPLATE_PARITY_OK] scope=intake`. | AC-12 (indirect parity) | B | MEDIUM |
| T-005 | Run validators: `python scripts/validate_readme_feature_coverage.py --repo . --enforce` → `[README_FEATURE_COVERAGE_VALIDATE_OK]` with `coverage_missing=["US-0118"]` baseline (US-0118 not in catalog surface). `python scripts/validate_doc_profile.py --repo .` + `python scripts/check-user-visible-metadata.py --repo .` + `python scripts/check_intake_template_parity.py --repo .` → expect PASS. Fix any narrative prose leaking internal IDs. | AC-9 (indirect), AC-12 | B | LOW |
| T-006 | Run regression tests: `python -m pytest tests/scratchpad_example_parity_test.py -v` → 4 passed. Forbid edits to `.cursor/scratchpad.md`, `template/.cursor/scratchpad.local.example.md`, `tests/scratchpad_example_parity_test.py`. | AC-8, AC-9 | B | LOW–MEDIUM |
| T-007 | **NEW** `scripts/work_kind_classify_lib.py` — classifier lib exposing `classify_work_kind(story_prose, acceptance_criteria, touched_file_hints, component_scope) -> WorkKindClassification` per R-0106 Q10 signature. Pure-stdlib (Q3 LOCKED); import `TIER_C_SKIP_PREFIXES` + `classify_touched_files` from `dev_environment_lib` (Q9 LOCKED import contract — no duplication). 3-tier enum `WorkKind.DOC / MINI / CODE`. Implement doc/mini/code rules per AC-2 + Q1 tie-break (highest tier wins). Derive `recommended_delivery_mode` + `recommended_phase_plan`. `--explain` flag emits `rule_trace` (Q3). `--self-test` exits 0 (AC-12). Reason-code family `WORK_KIND_*` (Q2). | AC-1, AC-2 | B | MEDIUM |
| T-008 | `/auto` `resolve_delivery_mode` step-0 integration — minimal hook in `.cursor/commands/auto.md` prose (or lib function `scripts/work_kind_routing_lib.py` if needed). Early-return when `WORK_KIND_ROUTING != "1"` (zero-overhead-when-off; Q8). Precedence chain L8 (explicit `DELIVERY_MODE` > `AUTO_PHASE_*` > `WORK_KIND_ROUTING` derived > current default; `start-from` always wins). `WORK_KIND_DELIVERY_MODE_CONFLICT` reason code when both set. `/intake` step-5 hook: run classifier after ACs + after US-0051 decomposition evaluator, before persistence; present `work_kind` + `recommended_delivery_mode` to operator for accept/override; persist choice in backlog row (`- work_kind`, `- recommended_delivery_mode`) + intake evidence bundle (`work_kind`, `recommended_delivery_mode`, `work_kind_operator_decision`). US-0078 evidence gate still runs before any backlog/acceptance write. Add `WORK_KIND_ROUTING=0` to `.cursor/scratchpad.md` + `template/.cursor/scratchpad.local.example.md` with merge-precedence note. Extend `handoffs/intake_evidence/*.json` schema with 3 optional fields. | AC-4, AC-5, AC-6 | B | MEDIUM |
| T-009 | **NEW** `tests/us0118_contract_test.py` (or `tests/work_kind_classify_test.py` per R-0106) with 12 `test_us0118_*` markers (Q4 LOCKED): `test_us0118_doc_kind_routes_to_lean_plan`, `test_us0118_mini_kind_routes_to_ultra_lean`, `test_us0118_mini_kind_routes_to_mega_quick_when_eligible`, `test_us0118_code_kind_routes_to_standard`, `test_us0118_explicit_delivery_mode_wins_over_work_kind`, `test_us0118_auto_phase_wins_over_work_kind`, `test_us0118_routing_off_is_noop`, `test_us0118_classify_touched_files_reuse`, `test_us0118_intake_evidence_records_work_kind`, `test_us0118_reason_codes_preserved`, `test_us0118_default_off_zero_overhead`, `test_us0118_explain_emits_rule_trace`. Add `scripts/work_kind_classify_lib.py` + `template/scripts/work_kind_classify_lib.py` to `installer-owned-paths.manifest` `[install_include_paths]` (Q10/installer parity — triple-installer PS1/Bash/Python ships the new script). Add `WORK_KIND_ROUTING_PAIRS` to `scripts/check_intake_template_parity.py` + `--scope=work-kind-routing` flag (Q6). Active + `template/` parity for new script + scratchpad lines. | AC-7, AC-9, AC-12 | B | MEDIUM |

**Total task seeds: 10 (T-anch + T-001..T-009) — within `SPRINT_MAX_TASKS=12`.**

## Test markers (12 `test_us0118_*` from R-0106 Q4 LOCKED)

| Marker | File | ACs covered | Notes |
|--------|------|-------------|-------|
| `test_us0118_doc_kind_routes_to_lean_plan` | `tests/us0118_contract_test.py` | AC-1, AC-2 | doc kind → `[intake, execute, release]` |
| `test_us0118_mini_kind_routes_to_ultra_lean` | `tests/us0118_contract_test.py` | AC-1, AC-2 | mini kind → ultra_lean (mega_quick ineligible) |
| `test_us0118_mini_kind_routes_to_mega_quick_when_eligible` | `tests/us0118_contract_test.py` | AC-1, AC-2 | mini kind + US-0096 eligibility → mega_quick |
| `test_us0118_code_kind_routes_to_standard` | `tests/us0118_contract_test.py` | AC-1, AC-2 | code kind → standard |
| `test_us0118_explicit_delivery_mode_wins_over_work_kind` | `tests/us0118_contract_test.py` | AC-6 | L8 precedence — explicit DELIVERY_MODE wins |
| `test_us0118_auto_phase_wins_over_work_kind` | `tests/us0118_contract_test.py` | AC-6 | L8 precedence — AUTO_PHASE_* wins over derived |
| `test_us0118_routing_off_is_noop` | `tests/us0118_contract_test.py` | AC-3 | WORK_KIND_ROUTING=0 → zero overhead |
| `test_us0118_classify_touched_files_reuse` | `tests/us0118_contract_test.py` | AC-8 | import boundary — no duplication |
| `test_us0118_intake_evidence_records_work_kind` | `tests/us0118_contract_test.py` | AC-5 | evidence bundle schema extension |
| `test_us0118_reason_codes_preserved` | `tests/us0118_contract_test.py` | AC-7 | four WORK_KIND_* reason codes |
| `test_us0118_default_off_zero_overhead` | `tests/us0118_contract_test.py` | AC-3, AC-8 | backward compat — byte-identical to pre-US-0118 |
| `test_us0118_explain_emits_rule_trace` | `tests/us0118_contract_test.py` | AC-1 | `--explain` flag emits rule_trace |

Plus the regression baseline marker: `tests/scratchpad_example_parity_test.py` (4 tests — BUG-0013 parity baseline; do not weaken).

## Files to touch

| # | Active path | Template path | Task | Parity |
|---|-------------|---------------|------|--------|
| 1 | `scripts/work_kind_classify_lib.py` | `template/scripts/work_kind_classify_lib.py` | T-007, T-009 | One-way copy via T-009 installer manifest |
| 2 | `tests/us0118_contract_test.py` | `template/tests/us0118_contract_test.py` | T-009 | Active + template parity |
| 3 | `its_magic/README.md` | `template/its_magic/README.md` | T-001, T-002, T-003, T-004 | Byte-identical via T-004 one-way copy |
| 4 | `docs/engineering/runbook.md` | `template/docs/engineering/runbook.md` | T-002 | One-way copy |
| 5 | `.cursor/commands/auto.md` | `template/.cursor/commands/auto.md` | T-008 | One-way copy |
| 6 | `.cursor/commands/intake.md` | `template/.cursor/commands/intake.md` | T-008 | One-way copy |
| 7 | `.cursor/scratchpad.md` | `template/.cursor/scratchpad.local.example.md` | T-008 | Merge-precedence (US-0078 model B) |
| 8 | `installer-owned-paths.manifest` | — | T-009 | Manifest single source of truth |
| 9 | `scripts/check_intake_template_parity.py` | `template/scripts/check_intake_template_parity.py` | T-009 | `WORK_KIND_ROUTING_PAIRS` + `--scope=work-kind-routing` |
| 10 | _(verification only)_ `docs/engineering/architecture.md` | — | T-anch (NO-OP / verification — no execute-phase write) | N/A |

## Files NOT to touch (non-goals — hard)

- `docs/product/backlog.md` — US-0045 status authority; release-only. US-0118 remains OPEN until `/release`. Backlog row fields `work_kind` / `recommended_delivery_mode` are added per-story at intake time only when `WORK_KIND_ROUTING=1` and operator accepts — this is a schema extension, NOT a bulk edit of existing rows. No forced reclassification of existing rows.
- `docs/product/acceptance.md` — release-only.
- Prior-released US-0113..US-0117 README blocks (`### Sovereign-loop era` L940 + `### Sovereign-loop era keys` L2421 / `### Release & distribution` L1225 + `### Release & distribution keys` L2545 / `### Integration & observability` L1410 + `### Integration & observability keys` L2617 / `### Delivery & lifecycle` L1665 + `### Delivery & lifecycle keys` L2765 / `### Phase & role governance` + `### Phase & role governance keys` L2856) in `its_magic/README.md` — **byte-stability contract** (all 5 already released in S0113..S0117). US-0118 adds cross-link pointers to these blocks from its own 6th sub-block; it never edits them. Execute-phase must verify `git diff HEAD -- its_magic/README.md` shows pure addition in the post-L2856 range (no removals/modifications to US-0113's L2421, US-0114's L2545, US-0115's L2617, US-0116's L2765, or US-0117's L2856 blocks).
- `scripts/sovereign_loop_lib.py` — compose-do-not-amend (US-0103 read-only consumer).
- `scripts/sovereign_convergence_lib.py` — compose-do-not-amend (US-0105 read-only consumer).
- `scripts/dev_environment_lib.py` — **REUSE only — do not modify**. Import `classify_touched_files` + `TIER_C_SKIP_PREFIXES` from `dev_environment_lib` (Q9 LOCKED import contract). Contract test `test_us0118_classify_touched_files_reuse` enforces the import boundary.
- `tests/scratchpad_example_parity_test.py` — AC-8 regression baseline; forbid edits.
- Compose-guard stories (23 — US-0091, US-0097, US-0017, US-0040, US-0100..US-0112, US-0034, US-0084, US-0086, US-0093, US-0096, US-0041, US-0062) — read-only consumers; additive-only.
- `docs/engineering/architecture.md` — **other than the `## US-0118` section already appended in `/architecture` phase, NO execute-phase edits**. T-anch is a NO-OP / verification task.

## Compose guards UNCHANGED (23 cumulative — same 23 as US-0117)

US-0118 is a code-bearing story but lives entirely **additive** to the compose surface — it adds a new flag (`WORK_KIND_ROUTING`), a new lib (`work_kind_classify_lib.py`), new backlog row fields, a new precedence clause, a new README sub-block, and a new runbook h2. It does **not** amend any existing compose-surface feature. The 23 compose guards (cumulative across all prior stories — US-0118 adds no new family-internal guards because US-0118 is itself a single-feature story, not a family umbrella) remain UNCHANGED:

US-0091, US-0097, US-0017, US-0040, US-0100, US-0101, US-0102, US-0103, US-0104, US-0105, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112, US-0034, US-0084, US-0086, US-0093, US-0096, US-0041, US-0062.

**Does US-0118 itself become a NEW compose guard?** **NO.** US-0118 is a **routing primitive**, not a compose-surface guard. The 6 read-only compose consumers (US-0096 / US-0070 / US-0078 / US-0051 / US-0069 / US-0103) consume US-0118's output; they are not amended by it. Adding US-0118 to the compose-guard list would conflate a routing primitive with a guard — rejected. US-0118's contract is enforced by its own 12 `test_us0118_*` markers + the `WORK_KIND_ROUTING=0` zero-overhead-when-off contract (test `test_us0118_default_off_zero_overhead`).

## 6th-story cumulative byte-stability surface note

US-0118 is the **first 6-cumulative-surface story**. Prior 5 released blocks (US-0113 L2421, US-0114 L2545, US-0115 L2617, US-0116 L2765, US-0117 L2856) must remain byte-identical between `its_magic/README.md` and `template/its_magic/README.md`. US-0118 adds net-new-keys-only + cross-link-pointers + reason-code-only entries to its own 6th sub-block (`### Work-kind routing keys (US-0118)`), never edits prior released blocks. `PARITY_OK <size> <size>` is the authoritative end-to-end byte-stability proof. The cross-story byte-stability contract pattern now scales from quint (S0113/S0114/S0115/S0116 + US-0117) to sextet (adds US-0118) — the contract generalizes to any N-cumulative-surface story.

## Plan-verify readiness ultra_lean merge note

`plan-verify` is **MERGED into `qa`** within the `build+verify` macro per ultra_lean (US-0096 / DEC-0082). QA will create `plan-verify.json` within `build+verify`. This sprint-plan phase does **NOT** create a separate plan-verify sprint task. The `build+verify` macro = `/execute` (first canonical phase, role=dev) + `/qa` (second canonical phase, role=qa — merges plan-verify + execute QA + verify-work).

## Decision gate

- `decision_gate=false` (no DECISION_GATE; no hard stop; companion DEC-0118 authored Accepted in architecture phase; approach A1 locked; sprint seeds T-anch + T-001..T-009 within SPRINT_MAX_TASKS=12; risks R1..R8 finalized; DC check clean; compose-do-not-amend verified 6/6)
- `stop_conditions_met=yes` (no missing references — all 6 compose targets verified; no decision gate triggered; AC baselines green: `validate_readme_feature_coverage.py` PASS + `pytest tests/scratchpad_example_parity_test.py` 4 passed)

## Sovereign memory note

`assemble_sovereign_memory_digest(...)` NOT called (US-0118 documentation+code so far — sprint-plan phase writes sprint artifacts only; existing digest context sufficient per R-0106 — S0113..S0117 retrospectives established reusable patterns; cross-link pointer pattern + angle-distinct narrative pattern + byte-stability contract now scale from quint to sextet; the routing-primitive angle is distinct from prior 5 documentation-family angles). No write to `mistakes.jsonl` in sprint-plan phase.

## Risks finalized (R1..R8 — promoted from R-0106)

| Risk | Severity | Mitigation |
|------|----------|------------|
| **R1** Classification ambiguity (mixed `docs/` + `src/` tiers) | **MEDIUM** | Q1 LOCKED: highest tier wins (`code` > `mini` > `doc`) per `classify_touched_files` tier_rank A>B>C. Single-pass deterministic. Contract test `test_us0118_code_kind_routes_to_standard` covers the mixed-tier case. |
| **R2** Precedence conflicts (`WORK_KIND_ROUTING=1` + `DELIVERY_MODE` set) | **MEDIUM** | L8 precedence chain LOCKED + `WORK_KIND_DELIVERY_MODE_CONFLICT` reason code (Q2). Explicit operator flags always win; classifier fills only the unset case. Contract test `test_us0118_explicit_delivery_mode_wins_over_work_kind` + `test_us0118_auto_phase_wins_over_work_kind`. |
| **R3** `mega_quick` eligibility overlap with `mini` | **LOW–MEDIUM** | L6 LOCKED: classifier recommends `mega_quick` only when US-0096 eligibility passes (AC≤3, no DEC, single component), else falls back to `ultra_lean`. Contract test `test_us0118_mini_kind_routes_to_mega_quick_when_eligible` + `test_us0118_mini_kind_routes_to_ultra_lean`. |
| **R4** Backward compatibility (existing backlog rows without `work_kind`) | **MEDIUM** | Q8 LOCKED: `WORK_KIND_ROUTING=0` default-off + early-return in `/auto` step 0 + `/intake` step 5 skip. No forced reclassification, no schema-migration. Contract test `test_us0118_default_off_zero_overhead`. |
| **R5** Operator trust (deterministic + inspectable) | **LOW–MEDIUM** | Q3 LOCKED: deterministic pure-stdlib + `--explain` flag emitting `rule_trace` (Q10). Contract test `test_us0118_explain_emits_rule_trace`. Operators can override with confidence. |
| **R6** Reuse boundary drift (`dev_environment_lib.classify_touched_files` rewritten vs imported) | **LOW** | Q9 LOCKED (in T-007): `work_kind_classify_lib.py` imports `TIER_C_SKIP_PREFIXES` + `classify_touched_files` from `dev_environment_lib` — no duplication. Contract test `test_us0118_classify_touched_files_reuse`. |
| **R7** Installer parity drift (triple-installer must ship new script) | **LOW** | T-009 adds both `scripts/work_kind_classify_lib.py` + `template/scripts/work_kind_classify_lib.py` to `installer-owned-paths.manifest` `[install_include_paths]`. Manifest-driven single source of truth. |
| **R8** Cross-story byte-stability surface (6th sub-block) — US-0118 is the first NEW story after the US-0113..US-0117 quint; it adds a 6th sub-block to `### Full scratchpad reference (detailed)`. Risk of accidentally editing a prior released block. | **MEDIUM** | T-003 mandates net-new-keys-only + cross-link-pointer + reason-code-only shape; never edits prior released blocks. Execute-phase verifies `git diff HEAD -- its_magic/README.md` shows pure addition in the post-L2856 range. QA re-verifies. `PARITY_OK <size> <size>` authoritative end-to-end proof. Pattern now scales from quint to 6th story. |

## Definition of done

- All 12 ACs RELEASED in `/release` phase (12/12 satisfied — QA_PASS + VERIFY_WORK_PASS + RELEASE_PASS).
- 23/23 compose guards UNCHANGED (additive-only).
- `PARITY_OK <size> <size>` green (framework README pair byte-identical).
- `python -m pytest tests/scratchpad_example_parity_test.py -v` → 4 passed.
- `python -m pytest tests/us0118_contract_test.py` → all 12 `test_us0118_*` passed.
- `python scripts/validate_readme_feature_coverage.py --repo . --enforce` → exit 0.
- `python scripts/work_kind_classify_lib.py --self-test` → exit 0.
- Story CLOSED in `docs/product/backlog.md` (OPEN → DONE) per US-0045.
- `docs/product/acceptance.md` US-0118 row `[ ]` → `[x]`.

## Next phase

- `next_scheduled_phase=/execute` (role=dev per US-0069 / DEC-0051 phase→role matrix default; first canonical phase of `build+verify` macro per ultra_lean)
- `next_scheduled_role=dev`
- `next_scheduled_sprint_macro=build+verify`
- `stop_condition=STOP after sprint-plan completes; hand off via artifacts only to /execute in fresh dev subagent (BUG-0006)`

## Isolation evidence (US-0048 / DEC-0029)

- `phase_id=sprint-plan`
- `role=tech-lead`
- `story_id=US-0118`
- `sprint_id=S0118`
- `orchestrator_run_id=auto-20260704-01`
- `delivery_mode=ultra_lean`, `macro_phase=plan` (sprint-plan — third canonical phase of `plan` macro per US-0096 / DEC-0082; research + architecture + sprint-plan merged)
- `fresh_context_marker=tl-US0118-sprint-plan-20260704T232400Z-fresh`
- `timestamp=2026-07-04T23:24:00Z` (UTC)
- `evidence_ref=docs/engineering/state.md (architecture checkpoint L300–L372 narrow-read — phase_id/role/story_id/orchestrator_run_id/delivery_mode/macro_phase/fresh_context_marker/timestamp/architecture_anchor/companion_dec/approach_locked/sprint_seeds/compose_guards/test_markers/risks_finalized/stop_conditions_met + isolation evidence + strict runtime proof + decision gate + next scheduled phase), docs/engineering/architecture.md (## US-0118 section L1713–L1923 full read — Overview + Companion DEC + Approach A1 + Files to touch + Files NOT to touch + Sprint seeds T-anch+T-001..T-009 + Test markers + Compose guards UNCHANGED + DC resolution + Compose-do-not-amend + Risks finalized + Stop conditions met + Sovereign memory note + Consequences + Evidence references + Isolation evidence + Strict runtime proof + Decision gate + Next scheduled phase), handoffs/po_to_tl.md (US-0118 architecture handoff L5–L74 narrow-read — summary + architecture anchor + approach A1 + companion DEC + sprint seeds preview + DC resolution + risks + compose guards + isolation evidence + strict runtime proof + decision gate + next scheduled phase), docs/product/backlog.md (## US-0118 block L3983–L4025 narrow-read — 12 ACs verbatim + boundaries + related_us + intake_notes), docs/product/acceptance.md (US-0118 row L145 narrow-read — 12 ACs OPEN), sprints/S0117/sprint.md (full read as ultra_lean template — metadata + scope + AC table + AC→task surjective coverage + task count + tasks + test markers + files to touch + files NOT to touch + compose guards + byte-stability surface note + plan-verify readiness ultra_lean merge note + decision gate + sovereign memory note + risks + definition of done + next phase + isolation evidence + strict runtime proof), sprints/S0117/tasks.md (first ~120 lines read as ultra_lean tasks template — Task-to-AC Bijection Table + Task Seeds shape), handoffs/resume_brief.md (top ~30 lines narrow-read for drain-advance prose shape)`
- Tech-lead subagent spawned fresh per BUG-0006 / US-0048 isolation; no prior chat history carried forward. Context limited to the narrow-read files listed above (US-0053 / US-0096 Tranche A). No MCP / browser / shell side-effects beyond narrow-read grep + read tool calls + python SHA-256 computation for the strict runtime proof + powershell line-count computations + the artifact writes listed in this phase (sprints/S0118/sprint.md NEW, sprints/S0118/tasks.md NEW, handoffs/po_to_tl.md sprint-plan handoff prepend, docs/engineering/state.md sprint-plan checkpoint append, handoffs/resume_brief.md drain-advance append). No `.env` reads, no credentials access, no intake-evidence mutation.
- `assemble_sovereign_memory_digest(...)` NOT called (US-0118 documentation+code so far — sprint-plan phase writes sprint artifacts only; existing digest context sufficient per R-0106).
- No write to `mistakes.jsonl` in sprint-plan phase (no fix_failed / revert_applied / plan_fidelity_violation / scope_creep event occurred).
- Prior phase strict proof consumed: `rp-auto-20260704-01-architecture-techlead-20260704T203000Z-US-0118` (from `docs/engineering/state.md` architecture checkpoint, unchanged).
- Current sprint-plan-phase strict proof recorded below.

## Strict runtime proof (US-0056 / DEC-0038)

- `runtime_proof_id=rp-auto-20260704-01-sprint-plan-techlead-20260704T232400Z-US-0118`
- Canonical payload (sorted-key JSON per DEC-0038): `{"orchestrator_run_id":"auto-20260704-01","phase_id":"sprint-plan","proof_issued_at":"2026-07-04T23:24:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260704-01-sprint-plan-techlead-20260704T232400Z-US-0118","sprint_id":"S0118","story_id":"US-0118"}`
- `proof_hash=4a6b5b6125848f4cbb209ad5ea7623f715e3aea8572ce087850069e0a7da29e7` (SHA-256 of the sorted-key JSON payload above, computed via python `hashlib.sha256`)
- `proof_ttl_seconds=3600`
- `proof_ttl=2026-07-05T00:24:00Z` (1-hour TTL per DEC-0038, UTC = issued_at + 3600s)

## Validator gates (run this phase)

- `python scripts/validate_readme_feature_coverage.py --repo .` → `{"coverage_missing":[],"coverage_present":[],"coverage_total":0,"gaps":[],"repo_root":".","report_schema_version":1,"status":"PASS"}` exit 0 (US-0118 not yet in catalog surface — no README feature coverage entry expected pre-`/execute`).
- `python -m pytest tests/scratchpad_example_parity_test.py -v` → `4 passed in 0.08s` (BUG-0013 parity baseline green; not weakened).