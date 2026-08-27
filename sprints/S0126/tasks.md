# Sprint S0126 - Task checklist (US-0126)

Total tasks: 11 (T-anch + T-001..T-010). SPRINT_MAX_TASKS=12; SPRINT_AUTO_SPLIT=1; no split needed.

## Task execution order

1. T-anch (NO-OP / verification)
2. T-001 (Runbook h2 body `## OpenCode host operator runbook (US-0126)` in `docs/engineering/runbook.md` + `template/docs/engineering/runbook.md` byte-identical — includes T-005 consolidated reason-code table inline)
3. T-002 (README user-visible OpenCode host blurb in `README.md` + `template/its_magic/README.md` byte-identical) - parallel with T-003
4. T-003 (`OPENCODE_ADAPTER_PAIRS` additive extension in `scripts/check_intake_template_parity.py` + template mirror) - parallel with T-002
5. T-004 (NEW `tests/us0126_contract_test.py` + `template/tests/us0126_contract_test.py` byte-identical — 12 markers shell)
6. T-006 (markers 5, 6 — US-0071 sanitization grep tests) - parallel with T-007, T-008, T-009, T-010
7. T-007 (marker 7 — Program DoD static documentation test) - parallel
8. T-008 (markers 8, 9 — default-host reminder + out-of-scope tests) - parallel
9. T-009 (markers 3, 10, 11 — parity + Cursor-docs-not-deleted tests) - parallel
10. T-010 (markers 4, 12 — prior-story marker checklist) - parallel
11. Integration verification

## Task checklist

- [x] **T-anch**: Verify `# US-0126` H1 anchor present in `docs/engineering/architecture.md` (added in /architecture phase per DEC-0076 / BUG-0010; AFTER `# US-0125` L1481 and BEFORE `# US-0089` L2053 per DEC-0073 §11 — verified at L1747); verify DEC-0126 authored Accepted at `decisions/DEC-0126.md` (§1 runbook section, §2 locked operator sentences, §3 consolidated reason-code table, §4 parity scope + layer split, §5 12-marker contract-test list, §6 template parity manifest unchanged, §7 compose-do-not-amend, §8 isolation + runtime proof); verify compose guards 8/8 UNCHANGED baseline (US-0071, US-0113..US-0117, US-0121/DEC-0120, US-0122/DEC-0122, US-0123, US-0124/DEC-0124, US-0125/DEC-0125, US-0102/DEC-0087); verify 12-marker contract-test list locked in architecture AC-4 table; verify runbook h2 placement (immediately after `## OpenCode thin commands + validator bridge (US-0125)` section) + reason-code table (4 `OPENCODE_*` US-0124 + 5 installer `OPENCODE_*`/`CURSOR_*` US-0121 + 3 reused cross-host + raw Python validator codes; NO `OPENCODE_VALIDATOR_FAILED` wrapper per DEC-0125 DQ7) + parity extension (2 new pairs in `OPENCODE_ADAPTER_PAIRS`: `tests/us0126_contract_test.py` ↔ template + `docs/engineering/runbook.md` ↔ template) + DoD/reminder/out-of-scope locked sentences + manifest unchanged lock locked in DEC-0126 §1–§8; verify `docs/engineering/runbook.md` does NOT yet have `## OpenCode host operator runbook (US-0126)` h2; verify `tests/us0126_contract_test.py` + `template/tests/us0126_contract_test.py` do NOT yet exist; verify `OPENCODE_ADAPTER_PAIRS` in `scripts/check_intake_template_parity.py` does NOT yet list the 2 new pairs; verify `README.md` + `template/its_magic/README.md` do NOT yet have the OpenCode host blurb. Record results to `sprints/S0126/t-anch-verification.md`. T-anch is NO-OP / verification only — NO mutation to `docs/engineering/architecture.md` or `decisions/DEC-0126.md` in /execute; T-anch records baseline observations only (mirrors US-0122 / US-0123 / US-0124 / US-0125 T-anch ceremony). (AC-9, AC-10 baseline; NO-OP / verification only)

- [x] **T-001**: Ship the new sibling h2 `## OpenCode host operator runbook (US-0126)` body into `docs/engineering/runbook.md` AND `template/docs/engineering/runbook.md` (byte-identical active↔template) per architecture DQ1 + DQ5 + DQ6 + DQ7 + DQ2 LOCKED + DEC-0126 §1, §2. Placement: immediately after the `## OpenCode thin commands + validator bridge (US-0125)` section, before the next non-OpenCode h2. Body contains: (a) locked program DoD sentence (DQ5 — verbatim): "Program done: with a fresh `its-magic --host opencode` install and `/connect`ed keys, an operator can run `intake → … → release` on stock OpenCode with PO/Dev/QA as distinct sessions (optionally distinct providers per US-0123 role-slug routing), and the Python persistence-blocking validators (`intake_evidence_validate.py`, `bug_issue_validate.py`, and the US-0125 bridge contract set) refuse writes on non-zero exit exactly as on the Cursor host."; (b) locked default-host reminder sentence (DQ6 — verbatim): "Default install is cursor-only. Pass `--host opencode` or `--host both` to install the OpenCode host adapter; without it, `.opencode/` is not installed. See `## OpenCode host mode (US-0121)` for the installer flag reference."; (c) locked out-of-scope list (DQ7 — verbatim operator prose, no DEC ids): "Out of scope for the OpenCode host adapter: standalone runtime, OpenCode fork, VS Code contrib rewrite, Caveman mode, Cursor browser as primary UAT."; (d) Boundaries subsection (runbook only; cross-references to DEC ids allowed here — NOT operator prose): "standalone runtime — see `docs/product/standalone-runtime-masterplan.md`.", "OpenCode fork — out of scope; the adapter uses stock OpenCode plugins/agents/commands only.", "VS Code contrib rewrite — out of scope; the adapter does not modify VS Code or its contrib extensions.", "Caveman mode — see `DEC-0055`.", "Cursor browser as primary UAT — out of scope; browser UAT remains a secondary surface (US-0093)."; (e) consolidated cross-host reason-code table (T-005 inline — DQ2: 4 `OPENCODE_*` US-0124 + 5 installer `OPENCODE_*`/`CURSOR_*` US-0121 + 3 reused cross-host + raw Python validator codes; each with one-line semantics + fail-closed action + cross-link to owning slice; NO `OPENCODE_VALIDATOR_FAILED` wrapper per DEC-0125 DQ7); (f) parity scope cross-link to `--scope=opencode-adapter` (DQ3). US-0121/US-0124/US-0125 h2 sections untouched (compose, do not amend — cross-link only). **MUST keep `docs/engineering/runbook.md` byte-identical with `template/docs/engineering/runbook.md` after edit** — edit both files identically. Tests: marker 1, 2, 6, 7, 8, 9. (AC-1, AC-2, AC-6, AC-7, AC-8)

- [x] **T-002**: Ship the README user-visible OpenCode host blurb into `README.md` AND `template/its_magic/README.md` (byte-identical active↔template — note: `template/its_magic/README.md` is the installer-shipped README mirror) per architecture DQ6 + DQ7 LOCKED + DEC-0126 §1. Blurb carries: (a) default-host reminder sentence (DQ6 — verbatim operator prose, no DEC ids per US-0071): "Default install is cursor-only. Pass `--host opencode` or `--host both` to install the OpenCode host adapter; without it, `.opencode/` is not installed. See `## OpenCode host mode (US-0121)` for the installer flag reference."; (b) out-of-scope list (DQ7 — verbatim operator prose, no DEC ids): "Out of scope for the OpenCode host adapter: standalone runtime, OpenCode fork, VS Code contrib rewrite, Caveman mode, Cursor browser as primary UAT." No Boundaries subsection in README (Boundaries is runbook-only). No reason-code table in README (README blurb is operator pointer, not catalog — runbook owns the table). Additive only — no existing README content rewritten. Tests: marker 5, 8, 9. (AC-5, AC-7, AC-8)

- [x] **T-003**: Extend `OPENCODE_ADAPTER_PAIRS` in `scripts/check_intake_template_parity.py` additively with 2 new pairs per architecture DQ3 LOCKED + DEC-0126 §4. New pairs: `tests/us0126_contract_test.py` ↔ `template/tests/us0126_contract_test.py`; `docs/engineering/runbook.md` ↔ `template/docs/engineering/runbook.md`. Existing 8 pairs preserved (installer-owned-paths.manifest ↔ template, check_intake_template_parity.py ↔ template, tests/us0121_host_mode_test.py ↔ template, tests/us0122_contract_test.py ↔ template, tests/us0123_contract_test.py ↔ template, tests/us0124_contract_test.py ↔ template, tests/us0125_contract_test.py ↔ template, model_tier_validate.py ↔ template). **Parity CLI stays byte-only** (DQ3 layer split — critic NB `ik_us0126_dq3_parity_grep_false_pass` closed): `--scope=opencode-adapter` = byte-identical pair check only (file content hash match + non-empty existence); reason-code table presence + `test_us0126_*` markers = contract-test grep (in `tests/us0126_contract_test.py`), NOT parity-CLI predicates. Execute must NOT add grep predicates to the parity CLI; the parity CLI stays byte-only. Mirror parity script to `template/scripts/check_intake_template_parity.py` byte-identical. Tests: marker 3, 10. (AC-3, AC-9)

- [x] **T-004**: Create `tests/us0126_contract_test.py` with 12 markers per architecture DQ4 LOCKED + DEC-0126 §5. Markers (one-test-per-AC, AC-5 splits into readme + runbook no-dec-leak; +1 aggregate prior-story marker):
  1. `test_us0126_runbook_section_present` — grep `docs/engineering/runbook.md` + `template/docs/engineering/runbook.md` for `## OpenCode host operator runbook (US-0126)` h2 (DQ1 lock) (AC-1).
  2. `test_us0126_reason_code_catalog_present` — grep runbook for each code in the consolidated table (DQ2 lock): 4 `OPENCODE_*` (US-0124) + 5 installer `OPENCODE_*`/`CURSOR_*` (US-0121) + 3 reused cross-host + raw Python validator codes; assert each code has a one-line semantics + fail-closed action (AC-2).
  3. `test_us0126_parity_scope_opencode_adapter` — run `python scripts/check_intake_template_parity.py --scope=opencode-adapter` and assert exit 0 (DQ3 lock) (AC-3).
  4. `test_us0126_test_marker_checklist` — grep `tests/` for `test_us0121_*`..`test_us0125_*` markers (aggregate per-story checklist; one marker per prior epic slice); assert each prior slice has its documented markers (AC-4).
  5. `test_us0126_readme_no_dec_leak` — US-0071 sanitization grep on `README.md` + `template/its_magic/README.md`: assert no `DEC-xxxx` ids in operator-facing sentences (code references in evidence/footnotes allowed; operator prose must not leak DEC ids) (AC-5a).
  6. `test_us0126_runbook_no_dec_leak` — US-0071 sanitization grep on `docs/engineering/runbook.md` US-0126 section + template: assert no `DEC-xxxx` ids in operator-facing sentences (cross-references to DEC ids allowed only in a separate "Boundaries/evidence" subsection, not in operator prose) (AC-5b).
  7. `test_us0126_program_dod_documented` — grep runbook for the DoD sentence key phrases (DQ5 lock): "fresh `its-magic --host opencode` install", "distinct sessions", "refuse writes on non-zero exit" (AC-6).
  8. `test_us0126_default_host_reminder` — grep runbook + README for the default-host reminder phrases (DQ6 lock): "Default install is cursor-only", "`--host opencode`", "`--host both`" (AC-7).
  9. `test_us0126_out_of_scope_listed` — grep runbook + README for each excluded item name (DQ7 lock): "standalone runtime", "OpenCode fork", "VS Code contrib rewrite", "Caveman", "Cursor browser as primary UAT" (AC-8).
  10. `test_us0126_template_doc_parity` — assert `docs/engineering/context/installer-owned-paths.manifest` active↔template byte-identical (DQ8 lock — no new entries) + `docs/engineering/runbook.md` active↔template byte-identical (AC-9).
  11. `test_us0126_cursor_docs_not_deleted` — **deterministic static check** (DQ4 lock — NOT a frozen pre-US-0126 git snapshot, which is fragile): assert `.cursor/commands/` and `.cursor/agents/` directories still exist with expected file names vs current kit inventory (a sorted file-name list of `.cursor/commands/*.md` + `.cursor/agents/*.md` captured at execute time and asserted present — manifest-style baseline checked into the repo). No git history dependency. No live OpenCode probe (AC-10).
  12. `test_us0126_prior_story_markers_present` — grep `tests/` for `test_us0121_*`..`test_us0125_*` markers (aggregate prior-story marker presence — kept separate from marker 4 for explicit defense in depth per DQ4 lock; may be merged with marker 4 at execute if redundancy is justified, but architecture locks 12 for clarity) (AC-4 aggregate).
  All markers static/grep-based; no live OpenCode runtime probe (vision D10 lock — DQ4). Mirror to `template/tests/us0126_contract_test.py` byte-identical for parity pairing. Surjective AC coverage: AC-1 (marker 1), AC-2 (marker 2), AC-3 (marker 3 + marker 10), AC-4 (markers 4, 12), AC-5 (markers 5, 6), AC-6 (marker 7), AC-7 (marker 8), AC-8 (marker 9), AC-9 (marker 10), AC-10 (marker 11). Every AC has ≥1 marker. (AC-4)

- [x] **T-005**: Author the consolidated cross-host reason-code table inside the runbook h2 body (T-001) per architecture DQ2 LOCKED + DEC-0126 §3. Table documents: 4 `OPENCODE_*` codes from US-0124 (`OPENCODE_PLUGIN_SPAWN_UNSUPPORTED`, `OPENCODE_SUBTASK_IGNORED`, `OPENCODE_HEADLESS_UNSUPPORTED`, `OPENCODE_DRIVER_INVOKE_FAILED`) + 5 installer `OPENCODE_*`/`CURSOR_*` codes from US-0121 (`INSTALL_HOST_INVALID`, `OPENCODE_ORPHANED_BY_CLEAN_CURSOR`, `OPENCODE_STALE_BY_UPGRADE_CURSOR`, `CURSOR_ORPHANED_BY_CLEAN_OPENCODE`, `CURSOR_STALE_BY_UPGRADE_OPENCODE`) + 3 reused cross-host codes (`AUTO_ORCHESTRATOR_PHASE_EXECUTION`, `PHASE_ROLE_MISMATCH`, `NATIVE_CHAIN_UNAVAILABLE`) + raw Python validator codes (`INTAKE_PERSISTENCE_BLOCKED`, `INTAKE_REQUIRED_TOPIC_MISSING`, `BUG_ISSUE_VALIDATION_FAILED` — no `OPENCODE_*` wrapper per DEC-0125 DQ7). Each code has a one-line semantics + fail-closed action + cross-link to owning slice (US-0121/US-0124/US-0125/Python SOT). Table cross-links to US-0124 stub h2 (`## OpenCode orchestrator plugin reason codes (US-0124)`) and US-0125 stub h2 (`## OpenCode thin commands + validator bridge (US-0125)`) for per-slice stub references; US-0126 owns the consolidated cross-host view. NO `OPENCODE_VALIDATOR_FAILED` wrapper (DEC-0125 DQ7 REJECTED — US-0126 must not resurrect it). T-005 is the authoring of the table content inside the runbook h2 body shipped in T-001 — it is NOT a separate file; it is the table block within T-001's h2 body. Tests: marker 2 (`test_us0126_reason_code_catalog_present`) greps runbook for each code + asserts one-line semantics + fail-closed action. (AC-2)

- [x] **T-006**: Author `test_us0126_readme_no_dec_leak` (marker 5) + `test_us0126_runbook_no_dec_leak` (marker 6) inside `tests/us0126_contract_test.py` per architecture DQ6/DQ7 + DEC-0126 §5. Marker 5: US-0071 sanitization grep on `README.md` + `template/its_magic/README.md` — assert no `DEC-xxxx` ids in operator-facing sentences (code references in evidence/footnotes allowed; operator prose must not leak DEC ids). Marker 6: US-0071 sanitization grep on `docs/engineering/runbook.md` US-0126 section + template — assert no `DEC-xxxx` ids in operator-facing sentences (cross-references to DEC ids allowed only in the separate "Boundaries/evidence" subsection, not in operator prose). (AC-5)

- [x] **T-007**: Author `test_us0126_program_dod_documented` (marker 7) inside `tests/us0126_contract_test.py` per architecture DQ5 LOCKED + DEC-0126 §5. Marker 7 greps runbook for the DoD sentence key phrases (DQ5 lock): "fresh `its-magic --host opencode` install", "distinct sessions", "refuse writes on non-zero exit". Static documentation test (grep for key phrases); NOT a live end-to-end probe (vision D10). (AC-6)

- [x] **T-008**: Author `test_us0126_default_host_reminder` (marker 8) + `test_us0126_out_of_scope_listed` (marker 9) inside `tests/us0126_contract_test.py` per architecture DQ6/DQ7 LOCKED + DEC-0126 §5. Marker 8 greps runbook + README for the default-host reminder phrases (DQ6 lock): "Default install is cursor-only", "`--host opencode`", "`--host both`". Marker 9 greps runbook + README for each excluded item name (DQ7 lock): "standalone runtime", "OpenCode fork", "VS Code contrib rewrite", "Caveman", "Cursor browser as primary UAT". (AC-7, AC-8)

- [x] **T-009**: Author `test_us0126_parity_scope_opencode_adapter` (marker 3) + `test_us0126_template_doc_parity` (marker 10) + `test_us0126_cursor_docs_not_deleted` (marker 11) inside `tests/us0126_contract_test.py` per architecture DQ3/DQ8 LOCKED + DEC-0126 §5. Marker 3 runs `python scripts/check_intake_template_parity.py --scope=opencode-adapter` and asserts exit 0 (DQ3 lock). Marker 10 asserts `docs/engineering/context/installer-owned-paths.manifest` active↔template byte-identical (DQ8 lock — no new entries) + `docs/engineering/runbook.md` active↔template byte-identical. Marker 11 (AC-10) uses a **deterministic static check** (DQ4 lock — NOT a frozen pre-US-0126 git snapshot, which is fragile): assert `.cursor/commands/` and `.cursor/agents/` directories still exist with expected file names vs current kit inventory (a manifest-style baseline checked into the repo at execute time). No git history dependency. No live OpenCode probe. (AC-3, AC-9, AC-10)

- [x] **T-010**: Author `test_us0126_test_marker_checklist` (marker 4) + `test_us0126_prior_story_markers_present` (marker 12) inside `tests/us0126_contract_test.py` per architecture DQ4 LOCKED + DEC-0126 §5. Marker 4 greps `tests/` for `test_us0121_*`..`test_us0125_*` markers (aggregate per-story checklist; one marker per prior epic slice); asserts each prior slice has its documented markers. Marker 12 greps `tests/` for `test_us0121_*`..`test_us0125_*` markers (aggregate prior-story marker presence — kept separate from marker 4 for explicit defense in depth per DQ4 lock; may be merged with marker 4 at execute if redundancy is justified, but architecture locks 12 for clarity). (AC-4 aggregate)

## Integration verification (post T-010 + T-004)

- [x] Test gate: `python -m pytest tests/us0126_contract_test.py -v` → 12/12 PASS
- [x] Parity gate: `check_intake_template_parity.py --scope=opencode-adapter` PASS
- [x] Parity gate: active + template manifest byte-identical
- [x] Parity gate: active + template runbook byte-identical
- [x] Parity gate: active + template parity script byte-identical
- [x] Parity gate: active + template contract test byte-identical
- [x] Compose gate: 8/8 UNCHANGED
- [x] No-secrets gate: `api_key`/`apikey`/`sk-`/`auth.json`/`.env` grep zero hits on runbook/README/contract test
- [x] No-DEC-leak gate: marker 5 + marker 6 PASS (operator prose clean)
- [x] Cursor-docs-not-deleted gate: marker 11 PASS (`.cursor/commands/` + `.cursor/agents/` present)
- [x] No-`OPENCODE_VALIDATOR_FAILED`-wrapper gate: marker 2 asserts raw Python codes only

## Files to touch (scope)

### New (create)

- `tests/us0126_contract_test.py`
- `template/tests/us0126_contract_test.py` (byte-identical mirror for parity)
- `sprints/S0126/t-anch-verification.md`

### Edit (scoped, additive only)

- `docs/engineering/runbook.md` (append `## OpenCode host operator runbook (US-0126)` h2 body — program DoD + default-host reminder + out-of-scope + Boundaries subsection + consolidated reason-code table + parity scope cross-link)
- `template/docs/engineering/runbook.md` (byte-identical mirror)
- `README.md` (add user-visible OpenCode host blurb — default-host reminder + out-of-scope list; additive)
- `template/its_magic/README.md` (byte-identical mirror)
- `scripts/check_intake_template_parity.py` (extend `OPENCODE_ADAPTER_PAIRS` additively with 2 new pairs)
- `template/scripts/check_intake_template_parity.py` (byte-identical mirror)

### Verify read-only (no mutation)

- `docs/engineering/architecture.md # US-0126` (T-anch NO-OP; DQ1..DQ8 locks + 12-marker table + reason-code table are the locked source of truth — execute ships the runbook body, NOT architecture.md)
- `decisions/DEC-0126.md` (T-anch NO-OP)
- `docs/engineering/context/installer-owned-paths.manifest` (DQ8 lock — UNCHANGED; runbook already covered by `docs` in `[install_include_paths]`; `tests/us0126_contract_test.py` NOT installer-shipped per US-0121..US-0125 pattern)
- `template/docs/engineering/context/installer-owned-paths.manifest` (byte-identical mirror — UNCHANGED)
- `template/.opencode/agents/*.md` (US-0122 — agent files unchanged)
- `template/.opencode/plugins/orchestrator.ts` (US-0124 — plugin unchanged)
- `template/.opencode/commands/*.md` (US-0125 — command files unchanged)
- `.cursor/commands/*.md` + `.cursor/agents/*.md` (read-only compose for AC-10 baseline; `test_us0126_cursor_docs_not_deleted` marker 11 enforces presence)

### Compose-guard UNCHANGED (DO NOT TOUCH)

| File | Reason |
|---|---|
| `docs/product/backlog.md` | US-0045 canonical status — `/closure` mutates ONLY at execution time |
| `docs/product/acceptance.md` | US-0045 derived view — same |
| Compose-guard story surfaces (US-0071, US-0113..US-0117, US-0121/DEC-0120, US-0122/DEC-0122, US-0123, US-0124/DEC-0124, US-0125/DEC-0125, US-0102/DEC-0087) | 8/8 UNCHANGED — US-0126 adds additive docs + parity + contract-test only |

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

**Surjectivity check**: 10/10 ACs covered (AC-1..AC-10 each have at least 1 task). No `PLAN_AC_COVERAGE_GAP`.

