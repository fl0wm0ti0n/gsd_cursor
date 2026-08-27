# Sprint S0129 - Task checklist (US-0129)

Total tasks: 8 (T-anch + T-001..T-007). SPRINT_MAX_TASKS=12; SPRINT_AUTO_SPLIT=1; no split needed.

**Isolation**: `tl-US0129-sprint-plan-20260827T073646Z-fresh` · `model_id=cursor-grok-4.6-high` · `orchestrator_run_id=auto-20260827-01`

## Task execution order

1. T-anch (NO-OP / verification)
2. T-001 (`scripts/arch_linkage_guard.py` helper + pre-guard no-partial-write + template mirror per DQ2/DQ3)
3. T-002 (`reason_codes.md` `## US-0129` + `ARCH_LINKAGE_ROLLOVER_BLOCKED` + autonomy-stop-matrix `security_hard` row + template mirrors per DQ4/DQ5)
4. T-003 (`ARCH_LINKAGE_AUTO_REPAIR=0` scratchpad comment, no live `=1` + DQ8 stub restore path + template mirrors per DQ1/DQ8)
5. T-004 (`.cursor/commands/refresh-context.md` pre-guard → `--rollover` → post-guard → `--check` + template mirror per DQ3)
6. T-005 (`tests/us0129_contract_test.py` 8 markers + harness **26AB** in `run-tests.ps1` / `run-tests.sh` + template test mirror per DQ6/DQ7)
7. T-006 (runbook h3 under `### Triad hot-surface enforcement (DEC-0054)` + `ARCH_LINKAGE_PAIRS` / `--scope=arch-linkage` + template runbook per D8)
8. T-007 (`installer-owned-paths.manifest` active + template for `scripts/arch_linkage_guard.py`)
9. Integration verification

## Critic NB awareness (execute)

- **T-001** (`a0129ar-challenger-001`): exclude `.tmp*` and non-`docs/engineering/architecture.md` reads so fixture strings (`# US-0067`) and command-file greps do not over-block (R1). Do not pre-seed unrelated stubs if a required heading is already absent (R6) — AC-2 remediation.
- **T-001 / T-003** (`a0129ar-architect-002`): import `split_arch_stories` + the same while-pop predicate — do not copy-fork `rollover_architecture`. Do not add `ARCH_LINKAGE_AUTO_REPAIR` to `AUTONOMY_PRESET`. Stub insert before US-0089/US-0090 tail (R2).
- **T-anch / T-005** (`a0129ar-subtractor-003`): T-anch read-only; no `architecture.md` mutation; do not mark US-0129 DONE; do not tick L157; 8 markers required (not YAGNI); heading-only v1 (R3); do not reopen US-0126/US-0127/US-0128/US-0130.

## Task checklist

- [x] **T-anch**: Verify `# US-0129` H1 present in `docs/engineering/architecture.md` at L1527 (added in /architecture per DEC-0076 / BUG-0010; AFTER `# US-0128` L1383 and BEFORE `# US-0130` L1675); verify approach A1 locked + R-0113 DQ1–DQ8 LOCKED; verify companion **DEC-0129** Accepted at `decisions/DEC-0129.md`; verify compose-do-not-amend 8/8 baseline (DEC-0054, DEC-0073, DEC-0076/US-0089, US-0049, US-0126 B-1 fixture, US-0127/US-0128/US-0130 DONE, DEC-0119, R-0112); verify 8-marker contract-test list locked in architecture; verify `scripts/arch_linkage_guard.py` + `template/scripts/arch_linkage_guard.py` do NOT yet exist; verify `tests/us0129_contract_test.py` + template mirror do NOT yet exist; verify `reason_codes.md` has no `## US-0129` family; verify `ARCH_LINKAGE_ROLLOVER_BLOCKED` is absent from `scripts/data/autonomy_stop_matrix.yaml`; verify no live `ARCH_LINKAGE_AUTO_REPAIR=1` in committed scratchpad; verify `/refresh-context` step 4 is still `--rollover` then `--check` without pre/post guard; verify harness has 26AA but not 26AB; verify `ARCH_LINKAGE_PAIRS` / `--scope=arch-linkage` absent from `check_intake_template_parity.py`; verify installer manifest lacks `scripts/arch_linkage_guard.py`. Record results to `sprints/S0129/t-anch-verification.md`. T-anch is NO-OP / verification only — NO mutation to `docs/engineering/architecture.md` in /execute. (AC-6 baseline; NO-OP / verification only)

- [x] **T-001**: Create `scripts/arch_linkage_guard.py` AND `template/scripts/arch_linkage_guard.py` (byte-identical) per architecture DQ2/DQ3 LOCKED. Helper `discover_required_arch_headings(repo) -> frozenset[str]`: stdlib scan of `tests/**/*_test.py`, exclude `tests/.tmp*`; include a token only when the test reads live `docs/engineering/architecture.md` and asserts membership / `find` / `startswith` of a literal `# US-dddd` or `# BUG-dddd`. **No hand-maintained YAML/manifest**. Pre-hook: import/call `split_arch_stories` + the same while-pop predicate as `rollover_architecture` (do **not** copy-fork). If any required heading is in the predicted moved set and `ARCH_LINKAGE_AUTO_REPAIR=0` → emit `ARCH_LINKAGE_ROLLOVER_BLOCKED` (story/bug id, missing heading, predicted pack path, remediation) and **do not write** archive pack or hot file. Stdlib only; no network; no `.env`. MUST keep active ↔ template byte-identical after edit. Tests: markers 1, 2, 3, 6. (AC-1, AC-2)

- [x] **T-002**: Register new `## US-0129 — Architecture hot-surface rollover linkage guard` in `docs/engineering/reason_codes.md` AND template mirror, after the last story family and before `## Other stories`. One-code table `### ARCH_LINKAGE_*` with `ARCH_LINKAGE_ROLLOVER_BLOCKED` (story/bug id, missing heading token, archive pack path predicted or written, remediation: `set ARCH_LINKAGE_AUTO_REPAIR=1` for stub restore, or restore H1s manually, then rerun `--rollover`). Do **not** extend US-0110 / US-0127 / US-0128 / US-0111 tables. `ARCH_LINKAGE_REPAIR_FAILED` is message text under the same code unless execute proves a split. Add `security_hard` row to `scripts/data/autonomy_stop_matrix.yaml` AND `docs/engineering/autonomy-stop-matrix.md` (+ template md mirror): `auto_repair_kind=n/a`, `cap=0`. Never skip — including under `AUTONOMY_STOP_POLICY=auto_repair_then_skip`. MUST keep active ↔ template byte-identical after edit. Tests: marker 3. (AC-2)

- [x] **T-003**: Scratchpad flag + DQ8 stub restore (AC-3). Comment `ARCH_LINKAGE_AUTO_REPAIR=0|1` (default **0**) next to `AUTONOMY_STOP_POLICY` in `.cursor/scratchpad.md` + template mirrors (`template/.cursor/scratchpad.md`, scratchpad.local.example peers). **No live `=1` assignment** in committed scratchpad. Do **not** add the flag to `AUTONOMY_PRESET` expansion (twelve flags unchanged). In `arch_linkage_guard.py` implement repair-on path: when `=1`, allow `--rollover` to archive full bodies, then inject **minimal H1 stubs** into the retained hot file. Stub shape: heading `# US-xxxx — <title from archived block’s first heading line>` (or `# BUG-xxxx — …`) matching `STORY_HEADING_H1` (`[:\u2014\-]` required). Body: exactly one pointer line, e.g. `Archived body in pack_ref: docs/engineering/architecture-archive/architecture-pack-<stamp>.md`. Insertion: into the retained hot surface **before** the US-0089 / US-0090 tail. Idempotent: if stub heading already exists, do not duplicate. Title source: first line of the archived block — do not invent titles. One `state.md` audit row per repair event (append-bottom; no archive rewrite). MUST keep active ↔ template byte-identical after edit. Tests: markers 4, 5. (AC-3)

- [x] **T-004**: Edit `.cursor/commands/refresh-context.md` AND `template/.cursor/commands/refresh-context.md` (byte-identical) per architecture DQ3 LOCKED. After cap read, wire **pre-guard → `--rollover` → post-guard → existing `--check`**. Do not change `rollover_architecture` heading-split semantics or pack naming. MUST keep active ↔ template byte-identical after edit. Tests: markers 6, 7. (AC-4)

- [x] **T-005**: Create `tests/us0129_contract_test.py` with 8 markers per architecture Q1 + R-0113 inventory (AC-5). Synthetic mini-architecture fixtures in temp dirs — **do not** replay `architecture-pack-20260825.md`. Do not weaken existing linkage consumers. Markers:
  1. `test_us0129_guard_discovers_contract_heading_set` — AC-1 / DQ2
  2. `test_us0129_pre_rollover_blocks_before_archive_write` — AC-1 / AC-2 / DQ3 (also folds “archiver unchanged”: no `split_arch_stories` / pack-header format change)
  3. `test_us0129_block_emits_arch_linkage_rollover_blocked_metadata` — AC-2
  4. `test_us0129_auto_repair_default_off` — AC-3 / DQ1
  5. `test_us0129_auto_repair_restores_h1_stub_idempotent` — AC-3 / DQ8 (fixture includes US-0089 tail)
  6. `test_us0129_post_rollover_verifies_active_linkage` — AC-1 / AC-4 / DQ3
  7. `test_us0129_refresh_context_wires_pre_post_guard` — AC-4
  8. `test_us0129_b1_regression_unprotected_rollover_fails` — AC-5
  Add harness section **26AB** after 26AA US-0102 in `tests/run-tests.ps1` **and** `tests/run-tests.sh`. Do not rename 26M rows. Do not call the section “B-1”. Mirror tests to `template/tests/us0129_contract_test.py` byte-identical. All markers static/fixture-based. (AC-5)

- [x] **T-006**: Edit `docs/engineering/runbook.md` AND `template/docs/engineering/runbook.md` (byte-identical). New **h3** under `### Triad hot-surface enforcement (DEC-0054)` (~L871), not a new sibling h2. Operator troubleshooting + cross-link to reason_codes.md. Edit `scripts/check_intake_template_parity.py` AND template mirror: new `ARCH_LINKAGE_PAIRS` + `--scope=arch-linkage` in `SCOPES` (and `all`): `scripts/arch_linkage_guard.py`, `.cursor/commands/refresh-context.md`, `tests/us0129_contract_test.py` (plus scratchpad comment / runbook / reason_codes if not already covered). MUST keep active ↔ template byte-identical after edit. Tests: marker 7 + `python scripts/check_intake_template_parity.py --scope=arch-linkage` exit 0. (AC-4 / D8)

- [x] **T-007**: Add `scripts/arch_linkage_guard.py` to `docs/engineering/context/installer-owned-paths.manifest` (active + template) in every section that already lists `scripts/enforce-triad-hot-surface.py` (`[install_include_paths]`, `[clean_paths]`, `[required_install_script_paths]` as applicable). Matching placement next to the triad-enforcer row. MUST keep active ↔ template byte-identical after edit. (D8)

## Integration verification (post T-007)

- [x] Test gate: `python -m pytest tests/us0129_contract_test.py -v` -> 8/8 PASS
- [x] Parity gate: `check_intake_template_parity.py --scope=arch-linkage` PASS
- [x] Parity gate: active + template `arch_linkage_guard.py` byte-identical
- [x] Parity gate: active + template `refresh-context.md` byte-identical
- [x] Parity gate: active + template `us0129_contract_test.py` byte-identical
- [x] Parity gate: active + template reason_codes.md / runbook.md / scratchpad.md byte-identical
- [x] Compose gate: 8/8 UNCHANGED (DEC-0054/DEC-0073/DEC-0076/US-0049/US-0126/US-0127/US-0128/US-0130/DEC-0119)
- [x] Compose gate: `ARCH_HOT_MAX_*` numbers unchanged; `rollover_architecture` heading-split unchanged
- [x] No-secrets gate: `api_key`/`apikey`/`sk-`/`auth.json`/`.env` grep zero hits on edited files
- [x] No-DONE gate: US-0129 Status stays OPEN; acceptance L157 unchecked; US-0126/US-0127/US-0128/US-0130 not reopened

## Files to touch (scope)

### New (create)

- `scripts/arch_linkage_guard.py`
- `template/scripts/arch_linkage_guard.py` (byte-identical mirror for parity)
- `tests/us0129_contract_test.py`
- `template/tests/us0129_contract_test.py` (byte-identical mirror for parity)
- `sprints/S0129/t-anch-verification.md`

### Edit (scoped, additive only)

- `docs/engineering/reason_codes.md` + `template/docs/engineering/reason_codes.md` (`## US-0129` family)
- `scripts/data/autonomy_stop_matrix.yaml` (`security_hard` row)
- `docs/engineering/autonomy-stop-matrix.md` + `template/docs/engineering/autonomy-stop-matrix.md`
- `.cursor/scratchpad.md` + `template/.cursor/scratchpad.md` (comment next to `AUTONOMY_STOP_POLICY`; no live `=1`)
- `.cursor/scratchpad.local.example.md` + `template/.cursor/scratchpad.local.example.md` (same comment)
- `.cursor/commands/refresh-context.md` + `template/.cursor/commands/refresh-context.md`
- `tests/run-tests.ps1` + `tests/run-tests.sh` (harness **26AB** after 26AA)
- `docs/engineering/runbook.md` + `template/docs/engineering/runbook.md` (h3 under triad)
- `scripts/check_intake_template_parity.py` + template mirror (`ARCH_LINKAGE_PAIRS` + `--scope=arch-linkage`)
- `docs/engineering/context/installer-owned-paths.manifest` + template mirror

### Verify read-only (no mutation)

- `docs/engineering/architecture.md # US-0129` (T-anch NO-OP; DQ1..DQ8 locks + 8-marker table are the locked source of truth)
- `decisions/DEC-0129.md` (already Accepted — do not rewrite)
- `docs/product/backlog.md ## US-0129` (read-only Status/ACs — US-0045; sprint-plan notes already written this phase)
- `docs/product/acceptance.md` US-0129 row L157 (read-only — US-0045 derived view)
- `handoffs/intake_evidence/US-0129-intake-20260825.json` (read-only — never mutate prior intake evidence)

### Compose-guard UNCHANGED (DO NOT TOUCH)

| File | Reason |
|---|---|
| `docs/product/backlog.md` Status/ACs | US-0045 canonical status — `/closure` mutates ONLY at execution time |
| `docs/product/acceptance.md` | US-0045 derived view — same |
| `docs/engineering/architecture.md` | Do not rewrite; T-anch is verification only |
| `scripts/enforce-triad-hot-surface.py` `rollover_architecture` split/pack/`ARCH_HOT_MAX_*` | DEC-0054 compose — import/call only |
| `AUTONOMY_PRESET` expansion / 9 `auto_repair_kind` values | DEC-0119 compose — no 13th flag, no 10th kind |
| US-0126 DONE row / acceptance L154 | B-1 fixture only — do not reopen |
| US-0127 / US-0128 / US-0130 DONE rows | do not reopen |
| `docs/engineering/research.md` `## R-0112` | US-0130 overlay — do not extend |
| `handoffs/intake_evidence/US-0129-intake-20260825.json` | never mutate prior intake evidence |

## AC -> Task surjective coverage

| AC | Task(s) |
|---|---|
| AC-1 (Linkage guard script) | T-001, T-005 (markers 1, 2, 6) |
| AC-2 (Fail-closed block) | T-001, T-002, T-005 (markers 2, 3) |
| AC-3 (Optional auto-repair) | T-003, T-005 (markers 4, 5) |
| AC-4 (Rollover wiring) | T-004, T-006, T-005 (markers 6, 7) |
| AC-5 (Regression tests) | T-005 (all 8 markers) |
| AC-6 (Compose) | T-anch |

**Surjectivity check**: 6/6 ACs covered (AC-1..AC-6 each have at least 1 task). No `PLAN_AC_COVERAGE_GAP`.
