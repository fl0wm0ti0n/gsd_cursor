# Sprint S0126 - Sprint Plan (US-0126)

## Metadata

| Field | Value |
|---|---|
| story_id | US-0126 |
| story_title | OpenCode host runbook, reason codes, and parity tests — operator runbook + consolidated cross-host reason-code table + `--scope=opencode-adapter` parity extension + 12 static/grep contract markers |
| sprint_id | S0126 |
| delivery_mode | ultra_lean |
| macro_phase | plan (sprint-plan — terminal canonical phase per ultra_lean; /plan-verify runs standalone per orchestrator brief, role=qa) |
| current_phase | sprint-plan |
| approach | A1 locked |
| companion_DEC | DEC-0126 (Accepted) |
| research_anchor | R-0109 (DQ1..DQ8 LOCKED for US-0126; US-0121 Q1..Q12 + US-0122 DQ1..DQ8 + US-0123 DQ1..DQ10 + US-0124 DQ1..DQ8 + US-0125 DQ1..DQ8 locks preserved) |
| orchestrator_run_id | auto-20260825-01 |
| fresh_context_marker | tl-US0126-sprint-plan-20260825T161520Z-fresh |
| timestamp | 2026-08-25T16:15:20Z (UTC) |
| verdict | PASS |
| decision_gate | false |
| SPRINT_MAX_TASKS | 12 |
| SPRINT_AUTO_SPLIT | 1 |
| task_count | 11 (T-anch + T-001..T-010; within 12; no split) |
| CROSS_MODEL_REVIEW | 1 (model_id=glm-5.2-high required) |
| COMPONENT_SCOPE_MODE | 0 |
| USER_GUIDE_MODE | 0 |
| plan-verify | standalone /plan-verify next (role=qa per orchestrator brief); plan-verify.json NOT written in this spawn |
| backlog_status | OPEN (US-0045 — not mutated) |
| ac_checkboxes | unchecked (US-0045 — not mutated) |

## Scope summary

Ship the sixth and final slice of the OpenCode adapter epic (US-0121..US-0126): **Layer 4** — the operator-facing runbook section (`## OpenCode host operator runbook (US-0126)` in `docs/engineering/runbook.md` + `template/docs/engineering/runbook.md` byte-identical), the consolidated cross-host reason-code table, the `--scope=opencode-adapter` parity extension (2 new pairs in `OPENCODE_ADAPTER_PAIRS`), and the 12 `test_us0126_*` contract markers (one-test-per-AC, AC-5 splits into readme + runbook no-dec-leak; static/grep, no live OpenCode probe).

This is an **additive docs + parity + contract-test** change: one new runbook h2 section (mirrored active↔template), one README user-visible OpenCode host blurb (mirrored to `template/its_magic/README.md`), one `OPENCODE_ADAPTER_PAIRS` additive extension (2 new pairs), one new contract test file (`tests/us0126_contract_test.py` — 12 markers, mirrored to `template/tests/us0126_contract_test.py` byte-identical), and the companion DEC-0126. The US-0121 installer-flag h2, the US-0124 stub reason-code h2, and the US-0125 stub reason-code h2 are NOT edited by US-0126 — US-0126 owns the consolidated cross-host table and cross-links to them (compose, do not amend). No Cursor kit docs are deleted (AC-10). No new GUI. No standalone runtime. No OpenCode fork. No VS Code contrib rewrite. No Caveman. No Cursor-browser-as-primary-UAT.

Reason codes: consolidated cross-host table documents 4 `OPENCODE_*` codes from US-0124 + 5 installer `OPENCODE_*`/`CURSOR_*` codes from US-0121 + 3 reused cross-host codes + raw Python validator codes (no `OPENCODE_VALIDATOR_FAILED` wrapper per DEC-0125 DQ7). US-0126 owns the consolidated cross-host view; US-0124/US-0125 stub h2 sections cross-link.

Out of scope: implementing the plugin (US-0124), editing `## OpenCode host mode (US-0121)` h2 (compose, do not amend), editing `## OpenCode orchestrator plugin reason codes (US-0124)` h2 (compose, do not amend), editing `## OpenCode thin commands + validator bridge (US-0125)` h2 (compose, do not amend), adding `tests/us0126_contract_test.py` to `[install_include_paths]` (test files NOT installer-shipped per US-0121..US-0125 pattern), resurrecting `OPENCODE_VALIDATOR_FAILED` wrapper (DEC-0125 DQ7 REJECTED), live OpenCode probe in CI (vision D10), frozen pre-US-0126 git snapshot for AC-10 (fragile — deterministic static check used instead), new GUI / standalone runtime / OpenCode fork / VS Code contrib rewrite / Caveman / Cursor-browser-as-primary-UAT (all out of scope per DQ7).

## Acceptance criteria (10) - US-0126 (status OPEN, checkboxes untouched per US-0045)

- **AC-1**: Runbook "OpenCode host" — `docs/engineering/runbook.md` (active + `template/` parity) documents stock OpenCode TUI/desktop/IDE as UI, `--host` opt-in, `/connect` keys, and that kit UX is slash commands + reason codes (no new its-magic GUI). New sibling h2 `## OpenCode host operator runbook (US-0126)`.
- **AC-2**: Reason-code catalog — document `OPENCODE_*` family and reuse/analogue of `NATIVE_CHAIN_UNAVAILABLE`, `AUTO_ORCHESTRATOR_PHASE_EXECUTION`, spawn-isolation failures. Each code has remediation text. Consolidated cross-host table (4 `OPENCODE_*` US-0124 + 5 installer `OPENCODE_*`/`CURSOR_*` US-0121 + 3 reused cross-host + raw Python validator codes; NO `OPENCODE_VALIDATOR_FAILED` wrapper per DEC-0125 DQ7).
- **AC-3**: Parity scope — `check_intake_template_parity.py --scope=opencode-adapter` covers pack, installer host help/manifest, agents/commands/plugin, and runbook surfaces this epic owns. Additive `OPENCODE_ADAPTER_PAIRS` extension (2 new pairs: `tests/us0126_contract_test.py` ↔ template + `docs/engineering/runbook.md` ↔ template). Parity CLI stays byte-only (DQ3 layer split — no grep predicates).
- **AC-4**: Contract tests — `test_us0126_*` (12 markers, one-test-per-AC, AC-5 splits into readme + runbook no-dec-leak; +1 aggregate prior-story marker) fail if the OpenCode pack ships without the documented test markers. Static/grep, no live OpenCode probe (vision D10).
- **AC-5**: README hygiene — user-visible OpenCode host blurb; no leaked DEC in operator sentences (US-0071). UI is OpenCode; kit is the workflow. AC-5 splits: AC-5a = readme no-dec-leak (marker 5), AC-5b = runbook no-dec-leak (marker 6).
- **AC-6**: Program DoD documented — runbook states the epic done-test (intake→release without Cursor; different sessions/providers; validators still block). Locked DoD sentence per DQ5.
- **AC-7**: Default host reminder — docs state cursor-only default until `--host opencode|both`. Locked reminder sentence per DQ6.
- **AC-8**: Out-of-scope list — runbook/README explicitly exclude standalone runtime, OpenCode fork, VS Code contrib rewrite, Caveman, Cursor-browser-as-primary-UAT. Locked out-of-scope list per DQ7.
- **AC-9**: Sanitization + template parity — new doc files mirrored under `template/` where installer-owned. `installer-owned-paths.manifest` unchanged (runbook already covered by `docs`); `tests/us0126_contract_test.py` not installer-shipped.
- **AC-10**: Compose — do not delete Cursor kit docs; OpenCode is additive. Deterministic static check (`.cursor/commands/` + `.cursor/agents/` present with expected file names vs current-kit-inventory baseline, NOT frozen git snapshot).

## Task summaries (11 - T-anch + T-001..T-010)

- **T-anch** (NO-OP / verification): Verify `# US-0126` H1 anchor in `docs/engineering/architecture.md` AFTER `# US-0125` (L1481) and BEFORE `# US-0089` (L2053) per DEC-0073 §11 / BUG-0010 heading policy (verified at L1747); verify DEC-0126 Accepted at `decisions/DEC-0126.md` (§1–§8); verify compose guards 8/8 UNCHANGED baseline (US-0071, US-0113..US-0117, US-0121/DEC-0120, US-0122/DEC-0122, US-0123, US-0124/DEC-0124, US-0125/DEC-0125, US-0102/DEC-0087); verify 12-marker contract-test list locked in architecture AC-4 table; verify runbook h2 placement (immediately after `## OpenCode thin commands + validator bridge (US-0125)` section) + reason-code table (4+5+3+raw Python; no `OPENCODE_VALIDATOR_FAILED` wrapper) + parity extension (2 new pairs in `OPENCODE_ADAPTER_PAIRS`) + DoD/reminder/out-of-scope locked sentences + manifest unchanged lock locked in DEC-0126 §1–§8; verify `docs/engineering/runbook.md` does NOT yet have `## OpenCode host operator runbook (US-0126)` h2; verify `tests/us0126_contract_test.py` + `template/tests/us0126_contract_test.py` do NOT yet exist; verify `OPENCODE_ADAPTER_PAIRS` in `scripts/check_intake_template_parity.py` does NOT yet list the 2 new pairs; verify `README.md` + `template/its_magic/README.md` do NOT yet have the OpenCode host blurb. Record to `sprints/S0126/t-anch-verification.md`. T-anch is NO-OP / verification only — NO mutation to `architecture.md` or `DEC-0126.md` in /execute (mirrors US-0122 / US-0123 / US-0124 / US-0125 T-anch ceremony). (AC-9, AC-10 baseline; NO-OP / verification only)
- **T-001** (Runbook section body): Ship the new sibling h2 `## OpenCode host operator runbook (US-0126)` body into `docs/engineering/runbook.md` AND `template/docs/engineering/runbook.md` (byte-identical active↔template) per architecture DQ1 + DQ5 + DQ6 + DQ7 + DQ2 LOCKED + DEC-0126 §1, §2. Placement: immediately after the `## OpenCode thin commands + validator bridge (US-0125)` section, before the next non-OpenCode h2. Body contains: locked program DoD sentence (DQ5 — verbatim), locked default-host reminder sentence (DQ6 — verbatim), locked out-of-scope list (DQ7 — verbatim operator prose), Boundaries subsection (runbook only; cross-references to DEC ids allowed here — `docs/product/standalone-runtime-masterplan.md`, `DEC-0055`, `US-0093`), consolidated cross-host reason-code table (DQ2 — 4 `OPENCODE_*` US-0124 + 5 installer `OPENCODE_*`/`CURSOR_*` US-0121 + 3 reused cross-host + raw Python validator codes; each with one-line semantics + fail-closed action + cross-link to owning slice; NO `OPENCODE_VALIDATOR_FAILED` wrapper), parity scope cross-link to `--scope=opencode-adapter` (DQ3). US-0121/US-0124/US-0125 h2 sections untouched (compose, do not amend — cross-link only). MUST keep `docs/engineering/runbook.md` byte-identical with `template/docs/engineering/runbook.md` after edit. Tests: marker 1, 2, 6, 7, 8, 9. (AC-1, AC-2, AC-6, AC-7, AC-8)
- **T-002** (README user-visible OpenCode host blurb): Ship the README user-visible OpenCode host blurb into `README.md` AND `template/its_magic/README.md` (byte-identical active↔template — note: `template/its_magic/README.md` is the installer-shipped README mirror) per architecture DQ6 + DQ7 LOCKED + DEC-0126 §1. Blurb carries: default-host reminder sentence (DQ6 — verbatim operator prose, no DEC ids per US-0071), out-of-scope list (DQ7 — verbatim operator prose, no DEC ids). No Boundaries subsection in README (Boundaries is runbook-only). No reason-code table in README (README blurb is operator pointer, not catalog — runbook owns the table). Additive only — no existing README content rewritten. Tests: marker 5, 8, 9. (AC-5, AC-7, AC-8)
- **T-003** (`OPENCODE_ADAPTER_PAIRS` additive extension): Extend `OPENCODE_ADAPTER_PAIRS` in `scripts/check_intake_template_parity.py` additively with 2 new pairs per architecture DQ3 LOCKED + DEC-0126 §4. New pairs: `tests/us0126_contract_test.py` ↔ `template/tests/us0126_contract_test.py`; `docs/engineering/runbook.md` ↔ `template/docs/engineering/runbook.md`. Existing 8 pairs preserved. **Parity CLI stays byte-only** (DQ3 layer split — critic NB `ik_us0126_dq3_parity_grep_false_pass` closed): `--scope=opencode-adapter` = byte-identical pair check only; reason-code table presence + `test_us0126_*` markers = contract-test grep (in `tests/us0126_contract_test.py`), NOT parity-CLI predicates. Execute must NOT add grep predicates to the parity CLI. Mirror parity script to `template/scripts/check_intake_template_parity.py` byte-identical. Tests: marker 3, 10. (AC-3, AC-9)
- **T-004** (Contract test file `tests/us0126_contract_test.py` — 12 markers): Create `tests/us0126_contract_test.py` with 12 markers per architecture DQ4 LOCKED + DEC-0126 §5. Markers (one-test-per-AC, AC-5 splits into readme + runbook no-dec-leak; +1 aggregate prior-story marker): (1) `test_us0126_runbook_section_present` [AC-1]; (2) `test_us0126_reason_code_catalog_present` [AC-2]; (3) `test_us0126_parity_scope_opencode_adapter` [AC-3]; (4) `test_us0126_test_marker_checklist` [AC-4]; (5) `test_us0126_readme_no_dec_leak` [AC-5a]; (6) `test_us0126_runbook_no_dec_leak` [AC-5b]; (7) `test_us0126_program_dod_documented` [AC-6]; (8) `test_us0126_default_host_reminder` [AC-7]; (9) `test_us0126_out_of_scope_listed` [AC-8]; (10) `test_us0126_template_doc_parity` [AC-9]; (11) `test_us0126_cursor_docs_not_deleted` [AC-10 — deterministic static check vs current-kit-inventory baseline, NOT frozen git snapshot]; (12) `test_us0126_prior_story_markers_present` [AC-4 aggregate]. All markers static/grep-based; no live OpenCode runtime probe (vision D10 lock — DQ4). Mirror to `template/tests/us0126_contract_test.py` byte-identical for parity pairing. Surjective AC coverage: AC-1 (marker 1), AC-2 (marker 2), AC-3 (marker 3 + marker 10), AC-4 (markers 4, 12), AC-5 (markers 5, 6), AC-6 (marker 7), AC-7 (marker 8), AC-8 (marker 9), AC-9 (marker 10), AC-10 (marker 11). Every AC has ≥1 marker. (AC-4)
- **T-005** (Consolidated reason-code table authoring): Author the consolidated cross-host reason-code table inside the runbook h2 body (T-001) per architecture DQ2 LOCKED + DEC-0126 §3. Table documents: 4 `OPENCODE_*` codes from US-0124 (`OPENCODE_PLUGIN_SPAWN_UNSUPPORTED`, `OPENCODE_SUBTASK_IGNORED`, `OPENCODE_HEADLESS_UNSUPPORTED`, `OPENCODE_DRIVER_INVOKE_FAILED`) + 5 installer `OPENCODE_*`/`CURSOR_*` codes from US-0121 (`INSTALL_HOST_INVALID`, `OPENCODE_ORPHANED_BY_CLEAN_CURSOR`, `OPENCODE_STALE_BY_UPGRADE_CURSOR`, `CURSOR_ORPHANED_BY_CLEAN_OPENCODE`, `CURSOR_STALE_BY_UPGRADE_OPENCODE`) + 3 reused cross-host codes (`AUTO_ORCHESTRATOR_PHASE_EXECUTION`, `PHASE_ROLE_MISMATCH`, `NATIVE_CHAIN_UNAVAILABLE`) + raw Python validator codes (`INTAKE_PERSISTENCE_BLOCKED`, `INTAKE_REQUIRED_TOPIC_MISSING`, `BUG_ISSUE_VALIDATION_FAILED` — no `OPENCODE_*` wrapper per DEC-0125 DQ7). Each code has a one-line semantics + fail-closed action + cross-link to owning slice (US-0121/US-0124/US-0125/Python SOT). Table cross-links to US-0124 stub h2 (`## OpenCode orchestrator plugin reason codes (US-0124)`) and US-0125 stub h2 (`## OpenCode thin commands + validator bridge (US-0125)`) for per-slice stub references; US-0126 owns the consolidated cross-host view. NO `OPENCODE_VALIDATOR_FAILED` wrapper (DEC-0125 DQ7 REJECTED — US-0126 must not resurrect it). T-005 is the authoring of the table content inside the runbook h2 body shipped in T-001 — it is NOT a separate file; it is the table block within T-001's h2 body. Tests: marker 2 (`test_us0126_reason_code_catalog_present`) greps runbook for each code + asserts one-line semantics + fail-closed action. (AC-2)
- **T-006** (US-0071 sanitization grep tests): Author `test_us0126_readme_no_dec_leak` (marker 5) + `test_us0126_runbook_no_dec_leak` (marker 6) inside `tests/us0126_contract_test.py` per architecture DQ6/DQ7 + DEC-0126 §5. Marker 5: US-0071 sanitization grep on `README.md` + `template/its_magic/README.md` — assert no `DEC-xxxx` ids in operator-facing sentences (code references in evidence/footnotes allowed; operator prose must not leak DEC ids). Marker 6: US-0071 sanitization grep on `docs/engineering/runbook.md` US-0126 section + template — assert no `DEC-xxxx` ids in operator-facing sentences (cross-references to DEC ids allowed only in the separate "Boundaries/evidence" subsection, not in operator prose). (AC-5)
- **T-007** (Program DoD static documentation test): Author `test_us0126_program_dod_documented` (marker 7) inside `tests/us0126_contract_test.py` per architecture DQ5 LOCKED + DEC-0126 §5. Marker 7 greps runbook for the DoD sentence key phrases (DQ5 lock): "fresh `its-magic --host opencode` install", "distinct sessions", "refuse writes on non-zero exit". Static documentation test (grep for key phrases); NOT a live end-to-end probe (vision D10). (AC-6)
- **T-008** (Default-host reminder + out-of-scope tests): Author `test_us0126_default_host_reminder` (marker 8) + `test_us0126_out_of_scope_listed` (marker 9) inside `tests/us0126_contract_test.py` per architecture DQ6/DQ7 LOCKED + DEC-0126 §5. Marker 8 greps runbook + README for the default-host reminder phrases (DQ6 lock): "Default install is cursor-only", "`--host opencode`", "`--host both`". Marker 9 greps runbook + README for each excluded item name (DQ7 lock): "standalone runtime", "OpenCode fork", "VS Code contrib rewrite", "Caveman", "Cursor browser as primary UAT". (AC-7, AC-8)
- **T-009** (Parity + Cursor-docs-not-deleted tests): Author `test_us0126_parity_scope_opencode_adapter` (marker 3) + `test_us0126_template_doc_parity` (marker 10) + `test_us0126_cursor_docs_not_deleted` (marker 11) inside `tests/us0126_contract_test.py` per architecture DQ3/DQ8 LOCKED + DEC-0126 §5. Marker 3 runs `python scripts/check_intake_template_parity.py --scope=opencode-adapter` and asserts exit 0 (DQ3 lock). Marker 10 asserts `docs/engineering/context/installer-owned-paths.manifest` active↔template byte-identical (DQ8 lock — no new entries) + `docs/engineering/runbook.md` active↔template byte-identical. Marker 11 (AC-10) uses a **deterministic static check** (DQ4 lock — NOT a frozen pre-US-0126 git snapshot, which is fragile): assert `.cursor/commands/` and `.cursor/agents/` directories still exist with expected file names vs current kit inventory (a manifest-style baseline checked into the repo, e.g. a sorted file-name list of `.cursor/commands/*.md` + `.cursor/agents/*.md` captured at execute time and asserted present). No git history dependency. No live OpenCode probe. (AC-3, AC-9, AC-10)
- **T-010** (Prior-story marker checklist): Author `test_us0126_test_marker_checklist` (marker 4) + `test_us0126_prior_story_markers_present` (marker 12) inside `tests/us0126_contract_test.py` per architecture DQ4 LOCKED + DEC-0126 §5. Marker 4 greps `tests/` for `test_us0121_*`..`test_us0125_*` markers (aggregate per-story checklist; one marker per prior epic slice); asserts each prior slice has its documented markers. Marker 12 greps `tests/` for `test_us0121_*`..`test_us0125_*` markers (aggregate prior-story marker presence — kept separate from marker 4 for explicit defense in depth per DQ4 lock; may be merged with marker 4 at execute if redundancy is justified, but architecture locks 12 for clarity). (AC-4 aggregate)

## AC -> Task surjective coverage

| AC | Task(s) |
|---|---|
| AC-1 (runbook "OpenCode host" section) | T-001, T-004 (marker 1) |
| AC-2 (reason-code catalog) | T-001, T-005, T-004 (marker 2) |
| AC-3 (parity scope) | T-003, T-004 (marker 3), T-009 (marker 3) |
| AC-4 (contract tests) | T-004 (all 12 markers), T-010 (markers 4, 12) |
| AC-5 (README hygiene) | T-002, T-006 (markers 5, 6) |
| AC-6 (program DoD documented) | T-001, T-007 (marker 7) |
| AC-7 (default host reminder) | T-001, T-002, T-008 (marker 8) |
| AC-8 (out-of-scope list) | T-001, T-002, T-008 (marker 9) |
| AC-9 (sanitization + template parity) | T-003, T-009 (marker 10) |
| AC-10 (compose — Cursor docs not deleted) | T-009 (marker 11) |

**Surjectivity check**: 10/10 ACs covered (each AC has at least 1 task). No `PLAN_AC_COVERAGE_GAP`.

## Compose guards (8/8 UNCHANGED — additive docs + parity + contract-test only)

| Compose target | Verification | Result |
|---|---|---|
| US-0071 (operator-sentence sanitization) | no DEC ids in operator prose; cross-references to runbook h2 / Boundaries subsection only (DQ6/DQ7) | ✅ compose |
| US-0113..US-0117 (operator docs) | add OpenCode host section; do not rewrite Cursor command catalogs | ✅ compose |
| US-0121 / DEC-0120 (installer `--host` flag docs hook — runbook h2) | untouched — US-0126 cross-links to it; does not rewrite the US-0121 h2 | ✅ untouched |
| US-0122 / DEC-0122 (seven role agents) | runbook references seven role agents; does not redefine permissions | ✅ compose |
| US-0123 (per-role slug routing) | runbook references `/connect` keys + per-role slug routing; does not re-list vendor slugs | ✅ compose |
| US-0124 / DEC-0124 (orchestrator plugin + stub reason-code h2) | untouched — US-0126 owns consolidated table; cross-links to US-0124 stub h2; does not reimplement plugin logic | ✅ untouched |
| US-0125 / DEC-0125 (thin commands + validator-bridge stub h2) | untouched — US-0126 owns consolidated table; cross-links to US-0125 stub h2; **DEC-0125 DQ7 raw Python reason codes upheld — `OPENCODE_VALIDATOR_FAILED` wrapper NOT resurrected** | ✅ untouched |
| US-0102 / DEC-0087 (no vendor slugs in `template/`) | no vendor slugs in runbook/README operator prose | ✅ untouched |

Contract tests `test_us0126_readme_no_dec_leak` (marker 5) + `test_us0126_runbook_no_dec_leak` (marker 6) + `test_us0126_cursor_docs_not_deleted` (marker 11) + `test_us0126_template_doc_parity` (marker 10) enforce at execute boundary.

## Task dependency graph

```
[T-anch] --> [T-001] (runbook h2 body + consolidated reason-code table [T-005 inline]) --> [T-002] (README blurb, parallel with T-003)
                                                                              |
                                                                              v
                                                                          [T-003] (OPENCODE_ADAPTER_PAIRS additive extension, after T-001)
                                                                              |
                                                                              v
                                                                          [T-004] (contract test file with 12 markers — authored in sub-tasks T-006..T-010)
                                                                              |
                                                                              v
                                                                  {T-006, T-007, T-008, T-009, T-010 parallel (markers 5,6 / 7 / 8,9 / 3,10,11 / 4,12)}
                                                                              |
                                                                              v
                                                                  Integration verification
```

**Execution order (deterministic)**: T-anch → T-001 (runbook h2 body with T-005 consolidated table inline) → T-002 (README blurb) parallel with T-003 (OPENCODE_ADAPTER_PAIRS extension) → T-004 (contract test file shell + 12 markers, authored as T-006..T-010 sub-markers) → T-006, T-007, T-008, T-009, T-010 (markers in parallel) → integration verification.

## Execute phase role (per DEC-0051 / US-0069)

| Phase | Role | Isolation |
|---|---|---|
| /plan-verify | qa (fresh per BUG-0006) | {phase_id:plan-verify, role:qa} — standalone per orchestrator brief |
| /execute | dev (fresh per BUG-0006) | {phase_id:execute, role:dev} |
| /qa | qa (fresh) | {phase_id:qa, role:qa} |
| /verify-work | qa (fresh) | {phase_id:verify-work, role:qa} |
| /release | release (fresh) | {phase_id:release, role:release} |
| /closure | qe (fresh) | {phase_id:closure, role:qe} |
| /refresh-context | curator (fresh) | {phase_id:refresh-context, role:curator} |

## Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

| Field | Value |
|---|---|
| phase_id | sprint-plan |
| role | tech-lead |
| story_id | US-0126 |
| sprint_id | S0126 |
| orchestrator_run_id | auto-20260825-01 |
| delivery_mode | ultra_lean |
| macro_phase | plan |
| fresh_context_marker | tl-US0126-sprint-plan-20260825T161520Z-fresh |
| timestamp | 2026-08-25T16:15:20Z (UTC) |
| model_id | glm-5.2-high (CROSS_MODEL_REVIEW=1 — required) |
| evidence_ref | sprints/S0126/sprint.md, sprints/S0126/tasks.md, sprints/S0126/progress.md, sprints/S0126/uat.json, sprints/S0126/uat.md, handoffs/tl_to_dev.md (US-0126 prepend), docs/engineering/state.md (sprint-plan checkpoint append-bottom), docs/engineering/architecture.md # US-0126, decisions/DEC-0126.md |

Prior phase proof consumed: `rp-auto-20260825-01-architecture-tech-lead-20260825T160542Z-US-0126` (proof_hash=EEE667DAEE41839D9695C25D4BBFF2D8FA383CAEF6FDA69BFFEAF1D28B5263A2, ttl 2026-08-25T17:05:42Z — consumed before RUNTIME_PROOF_STALE). Sovereign-critic architecture PASS at 2026-08-25T16:18:02Z (anti_slop_aggregate=8; 0 blocking findings; 3 research critic NBs closed in architecture phase: `ik_us0126_dq3_parity_grep_false_pass`, `ik_us0126_layering_runbook_dec_tests`, `ik_us0126_research_scope_yagni_markers`).

## Runtime proof (DEC-0038)

| Field | Value |
|---|---|
| runtime_proof_id | rp-auto-20260825-01-sprint-plan-tech-lead-20260825T161520Z-US-0126 |
| phase_id | sprint-plan |
| role | tech-lead |
| story_id | US-0126 |
| sprint_id | S0126 |
| orchestrator_run_id | auto-20260825-01 |
| delivery_mode | ultra_lean |
| macro_phase | plan |
| model_id | glm-5.2-high (CROSS_MODEL_REVIEW=1 — required) |
| proof_issued_at | 2026-08-25T16:15:20Z |
| proof_ttl_seconds | 3600 |
| proof_ttl | 2026-08-25T17:15:20Z (UTC) |
| proof_hash | 10E2CAC09DA36BF61FAAC0A3A258C49E2095875703018CAD4102E921704FC2A9 |
| canonical_payload | `{"delivery_mode":"ultra_lean","macro_phase":"plan","model_id":"glm-5.2-high","orchestrator_run_id":"auto-20260825-01","phase_id":"sprint-plan","proof_issued_at":"2026-08-25T16:15:20Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260825-01-sprint-plan-tech-lead-20260825T161520Z-US-0126","sprint_id":"S0126","story_id":"US-0126"}` |

## Decision gate

| Field | Value |
|---|---|
| decision_gate | false |
| stop_conditions_met | yes |
| missing_acceptance_criteria | none (10/10 ACs covered by 12 contract-test markers + compose guards 8/8) |
| compose_guards | 8/8 UNCHANGED (additive docs + parity + contract-test only) |
| dc_check | clean |
| task_count | 11 (within SPRINT_MAX_TASKS=12; SPRINT_AUTO_SPLIT=1 but no split needed) |
| risks_finalized | 6/6 ACCEPTED (R1..R6 from R-0109 US-0126) + 3 research critic NBs closed (ik_us0126_dq3_parity_grep_false_pass; ik_us0126_layering_runbook_dec_tests; ik_us0126_research_scope_yagni_markers) |
| approach | A1 locked |
| Q | DQ1..DQ8 LOCKED for US-0126; US-0121 Q1..Q12 + US-0122 DQ1..DQ8 + US-0123 DQ1..DQ10 + US-0124 DQ1..DQ8 + US-0125 DQ1..DQ8 locks preserved |
| plan-verify readiness | standalone /plan-verify next (role=qa per orchestrator brief); plan-verify.json NOT written in this spawn |
| sovereign_memory_note | `assemble_sovereign_memory_digest(...)` NOT called; no mistakes.jsonl write |

## Definition of done (sprint-plan)

- [x] 11 tasks enumerated (T-anch + T-001..T-010) — within SPRINT_MAX_TASKS=12
- [x] 10/10 ACs covered by 12 contract-test markers + compose guards 8/8 (surjective)
- [x] Task dependency graph documented
- [x] Execute phase role matrix documented (including standalone /plan-verify per orchestrator brief)
- [x] Compose guards 8/8 UNCHANGED (additive docs + parity + contract-test only)
- [x] Critic carry-ins (3 non-blocking from research) explicitly closed in architecture phase; 0 new carry-ins routed to /execute
- [x] Isolation evidence + runtime proof emitted (model_id=glm-5.2-high present)
- [x] Sprint-plan checkpoint appended to `docs/engineering/state.md` (append-bottom; never truncate)
- [x] Sprint-plan handoff prepended to `handoffs/tl_to_dev.md`
- [x] Sprint-plan PASS prepended to `handoffs/resume_brief.md` (→ /plan-verify, role=qa)
- [x] UAT placeholders written (`uat.json` empty steps, `uat.md` ACs no results)
- [x] Traceability row added to `docs/engineering/state.md` (Story=US-0126 | Sprint=S0126 | Tasks=T-anch+T-001..T-010 | Status=PLANNED | Evidence empty)
- [x] Backlog status OPEN (US-0045 — not mutated); AC checkboxes untouched

## Next scheduled phase

| Field | Value |
|---|---|
| next_scheduled_phase | `/plan-verify` (role=qa per orchestrator brief; fresh qa subagent per BUG-0006) |
| next_scheduled_role | qa |
| next_sprint_macro | plan (terminal — /plan-verify is the verification gate before build+verify macro) |
| stop_condition | STOP after sprint-plan completes; hand off via artifacts only to /plan-verify in fresh qa subagent per BUG-0006. Do not spawn /plan-verify from this subagent. |
| artifacts_written | sprints/S0126/sprint.md, sprints/S0126/tasks.md, sprints/S0126/progress.md, sprints/S0126/uat.json, sprints/S0126/uat.md, docs/engineering/state.md (sprint-plan checkpoint append-bottom + traceability row), handoffs/tl_to_dev.md (US-0126 prepend), handoffs/resume_brief.md (sprint-plan PASS prepend → /plan-verify) |




