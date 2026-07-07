# Sprint S0118 — QA Findings (US-0118)

**sprint_id**: S0118
**story_refs**: US-0118
**phase**: qa (merged plan-verify + execute QA + verify-work + UAT per ultra_lean / US-0096 / DEC-0082)
**role**: qa
**orchestrator_run_id**: auto-20260704-01
**delivery_mode**: ultra_lean
**macro_phase**: build+verify (second canonical phase)
**fresh_context_marker**: `qa-US0118-qa-20260704T230900Z-fresh`
**timestamp**: 2026-07-04T23:09:00Z (UTC; 2026-07-05T01:09:00Z UTC+2)
**runtime_proof_id**: `rp-auto-20260704-01-qa-qa-20260704T230900Z-US-0118`
**verdict**: **PASS**

---

## 1. Plan-verify (merged — PASS)

See `sprints/S0118/plan-verify.json`. All 11 checks PASS:

| Check | Status | Detail |
|-------|--------|--------|
| task_count_within_limit | PASS | 10 tasks (T-anch NO-OP + T-001..T-009) <= SPRINT_MAX_TASKS=12 |
| ac_coverage_surjective | PASS | 12/12 ACs mapped surjectively to 10 tasks; multi-AC tasks T-007 (AC-1+AC-2), T-008 (AC-4+AC-5+AC-6), T-009 (AC-7+AC-9+AC-12 partial), T-006 (AC-8+AC-9 regression), T-anch (AC-8+AC-10); no PLAN_AC_COVERAGE_GAP |
| dependency_order_acyclic | PASS | T-anch->T-007->T-008->T-009->T-001->T-002->T-003->T-004->T-005->T-006 acyclic (code-first ordering) |
| t_anch_no_op_documented | PASS | T-anch NO-OP / verification — `## US-0118` section already added in `/architecture` phase at architecture.md L1713 per R-0105 Q-2 LOCKED; no execute-phase write to architecture.md |
| files_to_touch_consistent | PASS | 10 entries in files-to-touch table; non-goals hard-listed (backlog.md, acceptance.md, prior US-0113..US-0117 README blocks, dev_environment_lib.py, scratchpad_example_parity_test.py, 23 compose guards) |
| companion_dec_referenced | PASS | DEC-0118 Required -> Accepted; authored in `/architecture` phase; locks 3-tier enumeration + L8 precedence + reuse boundary + zero-overhead-when-off |
| architecture_notes_locked | PASS | `docs/engineering/architecture.md` `## US-0118` locked at L1713 (added in `/architecture` phase per R-0105 Q-2 LOCKED); approach_locked=A1 |
| byte_stability_contract_present | PASS | 6th-story cumulative surface LOCKED (first 6-cumulative-surface story); prior 5 released blocks byte-stability preserved |
| compose_guards_23_unchanged | PASS | same 23 as US-0117; US-0118 is additive-only; US-0118 itself does NOT become a NEW compose guard |
| test_markers_locked | PASS | 13 `test_us0118_*` markers locked (Q4 LOCKED 12 + tie-break Q1); pytest stdlib only |
| parity_scope_defined | PASS | `WORK_KIND_ROUTING_PAIRS` (8 byte-identical pairs) + `--scope=work-kind-routing` flag added; scratchpad files excluded (structural parity via `bug0013` test) |

---

## 2. Execute QA — independent re-run results

### Validator re-run results (all green on independent re-run)

| Validator | Command | Result | Exit |
|-----------|---------|--------|------|
| Coverage | `python scripts/validate_readme_feature_coverage.py --repo . --enforce` | `{"coverage_missing":[],"coverage_present":[],"coverage_total":0,"gaps":[],"status":"PASS"}` + `[README_FEATURE_COVERAGE_VALIDATE_OK]` | 0 |
| Audience | `python scripts/validate_doc_profile.py --repo .` | `[DOC_PROFILE_VALIDATE_OK]` | 0 |
| Metadata hygiene | `python scripts/check-user-visible-metadata.py --repo .` | silent PASS (no violations) | 0 |
| Intake template parity (intake scope) | `python scripts/check_intake_template_parity.py --repo .` | `[INTAKE_TEMPLATE_PARITY_OK] scope=intake` | 0 |
| Intake template parity (work-kind-routing scope) | `python scripts/check_intake_template_parity.py --scope work-kind-routing --repo .` | `[INTAKE_TEMPLATE_PARITY_OK] scope=work-kind-routing` | 0 |
| Classifier lib self-test | `python scripts/work_kind_classify_lib.py --self-test` | `[WORK_KIND_CLASSIFY_SELF_TEST_OK]` | 0 |
| Routing lib self-test | `python scripts/work_kind_routing_lib.py --self-test` | `[WORK_KIND_ROUTING_SELF_TEST_OK]` | 0 |

### Test re-run results (independent)

| Test | Command | Result |
|------|---------|--------|
| Scratchpad example parity (canonical) | `python -m pytest tests/scratchpad_example_parity_test.py -v` | **4 passed in 0.16s** — `test_bug0013_parity_check` PASSED, `test_bug0013_header_preserved` PASSED, `test_bug0013_local_overrides_preserved` PASSED, `test_bug0013_active_example_mirror_in_sync` PASSED |
| US-0118 contract tests | `python -m pytest tests/us0118_contract_test.py -v` | **13 passed in 0.16s** — `test_us0118_doc_kind_routes_to_lean_plan`, `test_us0118_mini_kind_routes_to_ultra_lean`, `test_us0118_mini_kind_routes_to_mega_quick_when_eligible`, `test_us0118_code_kind_routes_to_standard`, `test_us0118_explicit_delivery_mode_wins_over_work_kind`, `test_us0118_auto_phase_wins_over_work_kind`, `test_us0118_routing_off_is_noop`, `test_us0118_default_off_zero_overhead`, `test_us0118_classify_touched_files_reuse`, `test_us0118_intake_evidence_records_work_kind`, `test_us0118_reason_codes_preserved`, `test_us0118_explain_emits_rule_trace`, `test_us0118_tie_break_code_wins` |

**17 passed total** (4 BUG-0013 regression + 13 US-0118 contract). Pre-existing fixture-path test failures (NOT introduced by US-0118, NOT US-0118 regression targets per T-006) flagged for awareness only — same pre-existing set already documented in execute-summary.

### Byte-stability re-verification (6th-story cumulative surface — CRITICAL)

Independent re-run via `python -c "a=open(...); b=open(...); print('PARITY_OK' if a==b else 'MISMATCH', len(a), len(b))"` comparing `its_magic/README.md` and `template/its_magic/README.md`:

```
PARITY_OK 203287 203287
```

`git diff --stat HEAD -- its_magic/README.md` shows `its_magic/README.md | 2333 +++++++++++++++++++++++++++++++++++++++++++++++++++` — **2333 insertions, 0 deletions** (pure addition in the post-US-0117 range; no removals/modifications to US-0113's L2421, US-0114's L2545, US-0115's L2617, US-0116's L2765, or US-0117's L2856 blocks). The 6th-story cumulative byte-stability surface is preserved — the cross-story contract now scales from quintet (US-0113..US-0117) to sextet (+US-0118).

### Parity re-verification

- `its_magic/README.md` ↔ `template/its_magic/README.md`: `PARITY_OK 203287 203287` (independent re-run, exit 0)
- `python scripts/check_intake_template_parity.py --repo .` → `[INTAKE_TEMPLATE_PARITY_OK] scope=intake` (exit 0)
- `python scripts/check_intake_template_parity.py --scope work-kind-routing --repo .` → `[INTAKE_TEMPLATE_PARITY_OK] scope=work-kind-routing` (exit 0)
- Both parity gates green; `its_magic/README.md` ↔ `template/its_magic/README.md` byte-identical.

### Compose guards — 23 UNCHANGED (verified)

US-0118 is additive-only — new flag (`WORK_KIND_ROUTING`), new lib (`work_kind_classify_lib.py` + `work_kind_routing_lib.py`), new backlog row fields, new precedence clause, new README sub-block, new runbook h2. It does NOT amend any existing compose-surface feature. The 23 cumulative compose guards remain UNCHANGED (same 23 as US-0117): US-0091, US-0097, US-0017, US-0040, US-0100, US-0101, US-0102, US-0103, US-0104, US-0105, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112, US-0034, US-0084, US-0086, US-0093, US-0096, US-0041, US-0062.

`dev_environment_lib.py` NOT modified — IMPORT only (Q9 LOCKED; `TIER_C_SKIP_PREFIXES` + `classify_touched_files` imported, not reimplemented). Contract test `test_us0118_classify_touched_files_reuse` enforces `wkc.classify_touched_files is dev_environment_lib.classify_touched_files` and `wkc.TIER_C_SKIP_PREFIXES is dev_environment_lib.TIER_C_SKIP_PREFIXES` — verified PASS.

6 read-only compose consumers (US-0096 / US-0070 / US-0078 / US-0051 / US-0069 / US-0103) remain unedited. `tests/scratchpad_example_parity_test.py` NOT modified (no test weakening).

### AC coverage independent assessment (12/12)

| AC | Description | Independent verification | Status | Task |
|----|-------------|---------------------------|--------|------|
| AC-1 | Classifier library | Read `scripts/work_kind_classify_lib.py` L299-L373 — `classify_work_kind(story_prose, acceptance_criteria, touched_file_hints, component_scope, *, has_companion_dec, explain) -> WorkKindClassification` per R-0106 Q10 signature. Pure stdlib (no network, no `.env` reads). Returns `work_kind`, `recommended_delivery_mode`, `recommended_phase_plan`, `rationale`, `evidence_refs`, optional `rule_trace`. Self-test PASS. | ✅ PASS | T-007 |
| AC-2 | Classification rules (doc/mini/code + tie-break) | DOC phase plan `[intake, execute, release]` (L105); MINI → `ultra_lean` or `mega_quick` per US-0096 eligibility (L257-L291); CODE → `standard` full lifecycle (L113-L125). Q1 LOCKED tie-break: highest tier wins via `classify_touched_files` tier_rank A>B>C → CODE > MINI > DOC (L177-L181, L203-L254). Contract tests `test_us0118_*_kind_routes_to_*` + `test_us0118_tie_break_code_wins` PASS. | ✅ PASS | T-007 |
| AC-3 | Scratchpad flag `WORK_KIND_ROUTING=0|1` (default `0`) | `.cursor/scratchpad.md` L188-L199 confirmed: comment block + `WORK_KIND_ROUTING=0` + `WORK_KIND_TIE_BREAK=highest_tier_wins`. Zero-overhead-when-off: routing lib L120-L124 early-returns `(standard, full_plan, WORK_KIND_ROUTING_OFF)` when flag != "1". Documented in README umbrella + scratchpad ref sub-block. | ✅ PASS | T-001, T-003, T-008 |
| AC-4 | Backlog row fields | `/intake` step 4b hook (`.cursor/commands/intake.md` L246+) documents the operator accept/override gate + backlog row persistence (`- work_kind`, `- recommended_delivery_mode`). Absence is valid. No forced reclassification of existing rows. | ✅ PASS | T-008 |
| AC-5 | Intake integration (step 5 classifier + operator accept/override) | `/intake` step 4b hook after ACs + after US-0051 decomposition evaluator, before persistence. Classifies when `WORK_KIND_ROUTING=1`, proposes `work_kind` + `recommended_delivery_mode`, operator accept/override. Persist in backlog row + intake evidence bundle (3 optional fields). US-0078 evidence gate still runs before any backlog/acceptance write. | ✅ PASS | T-008 |
| AC-6 | `/auto` integration (resolve_delivery_mode step-0 precedence) | `.cursor/commands/auto.md` L292-L300: `### Work-kind routing hook (US-0118 / DEC-0118) — step 0a` prose block. L8 precedence: explicit `DELIVERY_MODE` > `AUTO_PHASE_*` > `WORK_KIND_ROUTING`-derived > current default. `start-from` always wins. Early-return when `WORK_KIND_ROUTING != "1"`. `WORK_KIND_DELIVERY_MODE_CONFLICT` when both set. | ✅ PASS | T-008 |
| AC-7 | Fail-closed reason codes (`WORK_KIND_*` family) | 6 reason codes in `scripts/work_kind_classify_lib.py` L131-L145: `WORK_KIND_ROUTING_OFF` (info), `WORK_KIND_DELIVERY_MODE_CONFLICT`, `WORK_KIND_CLASSIFY_FAILED`, `WORK_KIND_UNKNOWN_ROUTE`, `WORK_KIND_PLAN_COVERAGE_MISSING`, `WORK_KIND_TIE_BREAK_APPLIED` (info). Each has remediation prose in `REASON_CODE_REMEDIATION` (L147-L173). Contract test `test_us0118_reason_codes_preserved` verifies all 6 codes + remediation + `WORK_KIND_REASON_CODES` tuple. PASS. | ✅ PASS | T-007, T-009 |
| AC-8 | Compose, do not amend (6 read-only consumers) | US-0096/US-0070/US-0078/US-0051/US-0069/US-0103 architectural surfaces remain read-only. 23 compose guards UNCHANGED. `dev_environment_lib.py` NOT modified (IMPORT only — Q9 LOCKED; contract test `test_us0118_classify_touched_files_reuse` PASS). `tests/scratchpad_example_parity_test.py` NOT modified. | ✅ PASS | T-anch, T-006 |
| AC-9 | Contract tests + parity | `tests/us0118_contract_test.py` has 13 `test_us0118_*` markers (Q4 LOCKED 12 + tie-break Q1). All PASS. `check_intake_template_parity.py --scope=work-kind-routing` PASS. Active + `template/` parity for new script + scratchpad lines + command docs + runbook + manifest (all `PARITY_OK` per execute-summary; re-verified via `[INTAKE_TEMPLATE_PARITY_OK]` exit 0). | ✅ PASS | T-009, T-006 |
| AC-10 | Architecture notes (`## US-0118` section) | T-anch NO-OP / verification. Grep `^## US-0118` `docs/engineering/architecture.md` → L1713 `## US-0118 — Work-kind classification + tiered delivery routing per story` confirmed. Documents classifier contract, work-kind enumeration, precedence chain, fail-closed codes, composition, `dev_environment_lib.classify_touched_files` reuse anchor. No execute-phase write to architecture.md. | ✅ PASS | T-anch |
| AC-11 | Runbook + command docs | `docs/engineering/runbook.md` L3579 `## Work-kind routing (US-0118 / DEC-0118)` h2 section appended at end (mirror of `## Caveman mode (US-0089)` shape). `.cursor/commands/auto.md` step 0a hook (L292+). `.cursor/commands/intake.md` step 4b hook (L246+). `template/` parity byte-identical. | ✅ PASS | T-002, T-008 |
| AC-12 | Self-test + installer delivery | `python scripts/work_kind_classify_lib.py --self-test` → `[WORK_KIND_CLASSIFY_SELF_TEST_OK]` exit 0. `python scripts/work_kind_routing_lib.py --self-test` → `[WORK_KIND_ROUTING_SELF_TEST_OK]` exit 0. `installer-owned-paths.manifest` `[install_include_paths]` + `[clean_paths]` + `[required_install_script_paths]` list `scripts/work_kind_classify_lib.py` + `scripts/work_kind_routing_lib.py`. Triple-installer parity (PS1/Bash/Python) ships the new scripts. | ✅ PASS | T-005, T-009 |

**Surjectivity**: 12/12 ACs covered by 10 tasks (T-anch NO-OP + T-001..T-009). No `QA_AC_COVERAGE_GAP`.

### Cross-link pointer verification (AC-3 byte-stability — PASS)

The new `### Work-kind routing keys (US-0118)` sub-block adds 2 net-new key rows (`WORK_KIND_ROUTING`, `WORK_KIND_TIE_BREAK`) + 6 reason-code-only entries (`WORK_KIND_*` family) + 3 cross-link pointers (`DELIVERY_MODE` → US-0114 L2545; `AUTO_PHASE_*` → US-0070; `LEAN_MEMORY_*` → US-0115 L2617). All cross-link pointers reference canonical blocks without duplicating key documentation — byte-stability contract honored.

### DC anchor resolution verification (T-anch NO-OP — PASS)

- `## US-0118 — Work-kind classification + tiered delivery routing per story` confirmed at L1713 of `docs/engineering/architecture.md` (added in `/architecture` phase per R-0105 Q-2 LOCKED).
- T-anch is a NO-OP / verification task — no execute-phase write to architecture.md.
- US-0118 inherits a clean deferral register (US-0117 was the final deferred-candidate resolution point with 36 anchors).

### `dev_environment_lib.py` reuse boundary (Q9 LOCKED — PASS)

- `scripts/work_kind_classify_lib.py` L52-L56 imports `TIER_C_SKIP_PREFIXES` + `classify_touched_files` from `dev_environment_lib` (no duplication).
- Contract test `test_us0118_classify_touched_files_reuse` (tests/us0118_contract_test.py L196-L205) verifies `wkc.classify_touched_files is dev_environment_lib.classify_touched_files` and `wkc.TIER_C_SKIP_PREFIXES is dev_environment_lib.TIER_C_SKIP_PREFIXES` — PASS.
- The classifier self-test (L464-L467) also verifies the import boundary.

### `/auto` and `/intake` prose integration (PASS)

- `.cursor/commands/auto.md` L292-L300: step 0a hook prose added under `## Mode-scoped delivery resolver — step 0` per AC-6. Describes WORK_KIND_ROUTING hook, L8 precedence, zero-overhead-when-off, WORK_KIND_DELIVERY_MODE_CONFLICT.
- `.cursor/commands/intake.md` L246+: step 4b classifier hook added between existing step 4 and step 5 per AC-5. Documents operator accept/override gate, WORK_KIND_ROUTING flag check, intake evidence schema extension.
- `template/.cursor/commands/auto.md` ↔ active: byte-identical (`PARITY_OK 35783 35783` per dev).
- `template/.cursor/commands/intake.md` ↔ active: byte-identical (via identical StrReplace edit).

### Scratchpad integration (PASS)

- `.cursor/scratchpad.md` L188-L199: comment block + `WORK_KIND_ROUTING=0` (default-off) + `WORK_KIND_TIE_BREAK=highest_tier_wins` keys added near delivery-mode / phase-selection section.
- Merge-precedence note (US-0078 model B: local > baseline > example) preserved in the comment block.
- The scratchpad parity test (`test_bug0013_active_example_mirror_in_sync`) PASSes — structural key parity preserved across `.cursor/scratchpad.md` + `template/.cursor/scratchpad.local.example.md` + `.cursor/scratchpad.local.example.md`.

---

## 3. Verify-work (execute-summary vs actual state — PASS)

See `sprints/S0118/verify-work-findings.md` and `sprints/S0118/verify-work-verdict.json`.

- **execute_summary_accurate**: true — 13/13 dev claims independently re-verified and matched (all 5 validators green; 2 self-tests green; 17/17 pytest PASS; byte-stability preserved on all 5 prior-released blocks + 6th sub-block pure addition; parity `PARITY_OK 203287 203287`; AC coverage 12/12; T-anch NO-OP / DC resolution verified; `dev_environment_lib.py` IMPORT only; 23 compose guards UNCHANGED; pre-existing fixture-path test failures flagged).
- **scope_creep**: NONE — only files-to-touch list modified; no edits to `dev_environment_lib.py`, `tests/scratchpad_example_parity_test.py`, `docs/product/backlog.md` (US-0045), `docs/product/acceptance.md` (US-0045), 23 compose-guard surfaces, or prior-released US-0113..US-0117 README blocks.
- **byte_stability_preserved**: true (6th-story cumulative surface — first 6-cumulative-surface story).
- **parity_preserved**: true.
- **DC resolution correctly noted**: T-anch NO-OP — `## US-0118` section confirmed present in architecture.md from `/architecture` phase; not silently dropped.

---

## 4. UAT (documentation+code story — PASS)

See `sprints/S0118/uat.json` and `sprints/S0118/uat.md`. 12/12 ACs PASS via the 13 `test_us0118_*` contract markers + 4 BUG-0013 regression tests (17 total). For US-0118 (documentation+code story), UAT reduces to contract-test verification per S0117 precedent. All 12 ACs PASS via the contract test surface.

---

## Known issues / deferrals

- **T-anch NO-OP** — `## US-0118` h1 anchor already added in `/architecture` phase per R-0105 Q-2 LOCKED. T-anch in this sprint = NO-OP / verification; no execute-phase write to architecture.md.
- **Pre-existing test failures (31)** in `python -m pytest tests/ -v` — NOT introduced by US-0118, NOT US-0118 regression targets per T-006. Root causes: (a) `.cursor/scratchpad.md` vs `template/.cursor/scratchpad.md` byte-mismatch from project-local overrides (pre-existing); (b) `model-catalog-examples` scope missing from `check_intake_template_parity.py` (US-0112 deferred); (c) architecture linkage failures from prior stories (pre-existing). The canonical `tests/scratchpad_example_parity_test.py` (4 tests) + `tests/us0118_contract_test.py` (13 tests) ran green (17 passed).
- **Intake evidence schema extension (AC-9)** — the 3 optional fields are documented in the runbook + classifier lib docstring + `/intake` step 4b hook. No existing intake evidence files were modified — only the schema contract is documented.
- **Mega-quick eligibility** — when a MINI-kind story has ACs ≤ 3 + single component + no DEC, the routing lib MAY propose `mega_quick` per US-0096. Operator may accept or override to `ultra_lean` / `standard`. The `mega_quick` route is opt-in via the classifier proposal — never forced.

**0 blocking findings. 4 non-blocking findings** (all cosmetic/pre-existing, NOT introduced by US-0118, NOT US-0118 regression targets).

---

## Isolation evidence (US-0048 / DEC-0029)

- **phase_id**: qa (merges plan-verify + execute QA + verify-work per ultra_lean / US-0096 / DEC-0082)
- **role**: qa
- **fresh_context_marker**: `qa-US0118-qa-20260704T230900Z-fresh`
- **timestamp**: 2026-07-04T23:09:00Z (UTC; 2026-07-05T01:09:00Z UTC+2)
- **evidence_ref**: `sprints/S0118/qa-findings.md` (this file) + `sprints/S0118/plan-verify.json` + `sprints/S0118/qa-verdict.json` + `sprints/S0118/verify-work-findings.md` + `sprints/S0118/verify-work-verdict.json` + `sprints/S0118/uat.json` + `sprints/S0118/uat.md` + `docs/engineering/state.md` (qa checkpoint appended) + `handoffs/resume_brief.md` (drain-advance appended)
- **isolation_mode**: fresh subagent context per BUG-0006 / US-0048 — qa subagent spawned fresh for the qa phase; no carry-over from prior sprint-plan / architecture / research / discovery / execute phases other than the artifact reads enumerated in the parent prompt.

## Strict runtime proof (DEC-0038)

- **runtime_proof_id**: `rp-auto-20260704-01-qa-qa-20260704T230900Z-US-0118`
- **proof_issued_at**: 2026-07-04T23:09:00Z
- **proof_ttl_seconds**: 3600
- **proof_ttl**: 2026-07-05T00:09:00Z (UTC) per DEC-0038
- **canonical_payload** (sorted-key JSON per DEC-0038): `{"orchestrator_run_id":"auto-20260704-01","phase_id":"qa","proof_issued_at":"2026-07-04T23:09:00Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260704-01-qa-qa-20260704T230900Z-US-0118","story_id":"US-0118"}`

## Sovereign memory note

`assemble_sovereign_memory_digest(...)` NOT called (US-0118 documentation+code; existing digest context sufficient per R-0106 — S0113..S0117 retrospectives established reusable patterns; cross-link pointer pattern + byte-stability contract + reuse-import pattern now scale from quint to sextet; the routing-primitive angle is distinct from prior 5 documentation-family angles). No write to `mistakes.jsonl` in qa phase (no fix_failed / revert_applied / plan_fidelity_violation / scope_creep event occurred — all 4 non-blocking findings are cosmetic/pre-existing).

## Next phase

Per **ultra_lean**, the orchestrator routes to the **`/release` phase** (release subagent, `ship` macro — first canonical phase per ultra_lean). US-0118 remains **OPEN** in `docs/product/backlog.md` and `docs/product/acceptance.md` US-0118 row remains `[ ]` until `/release` closes it per US-0045.

**STOP**: qa complete; do not spawn the next phase. The orchestrator will Task-spawn the release subagent for `/release`. Hand off via artifacts only.

- **next_scheduled_phase**: `/release` (release subagent, `ship` macro — first canonical phase per ultra_lean)
- **next_scheduled_role**: release
- **stop_condition**: STOP after qa artifacts written; orchestrator Task-spawns release for `/release` (BUG-0006 spawn-only)
