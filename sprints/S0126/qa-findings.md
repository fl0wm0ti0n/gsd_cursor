# QA findings — US-0126 / S0126 / auto-20260825-01 (qa, loop-2)

- **phase_id**: qa, **role**: qa, **story_id**: US-0126 (OPEN — not marked DONE per US-0045), **sprint_id**: S0126
- `orchestrator_run_id=auto-20260825-01`, `delivery_mode=ultra_lean`, `macro_phase=build+verify`
- `AUTO_IMPLEMENTATION_LOOP=1` (loop-2 qa after execute loop-2 + sovereign-critic of execute loop-2)
- `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 — required on isolation; this spawn's producer model)
- `producer_phase_id=execute` (loop-2), `producer_role=dev`, `producer_model_id=glm-5.2-high`
- `critic_phase_id=sovereign-critic` (execute loop-2 review), `critic_model_id=composer-2.5-fast`, `critic_verdict=PASS`, `anti_slop_aggregate=8`, `open_blocking_findings=0`
- `critic_fresh_context_marker=tl-US0126-sovereign-critic-execute-loop2-20260825T171502Z-fresh`
- `fresh_context_marker=qa-US0126-qa-20260825T171657Z-fresh-loop2` (NEW per US-0048 / BUG-0006; marker reuse = stale isolation evidence)
- `timestamp (UTC)=2026-08-25T17:16:57Z`
- **verdict: PASS** (qa loop-2 — execute loop-2 B-1 closed)
- `blocking_count=0`
- `non_blocking_count=0` (loop-1 NB-1 US-0125 coverage gap CLOSED in execute loop-2; loop-1 NB-2 AC-10 tuple-in-test drift class remains non-blocking but unchanged)
- `story_status=OPEN` (do not mark US-0126 DONE per US-0045; acceptance L154 unchecked; intake JSON not mutated; architecture.md / DEC-0126.md not mutated)
- `acceptance_L154=NOT ticked`
- `intake_json=NOT mutated`

## Verdict rationale

QA independently re-ran the US-0126 contract-test slice, the opencode-adapter parity check, the README feature coverage check, and re-confirmed the canonical `tests/report.md` Fail=0 evidence on disk in this fresh qa subagent context (Python 3.12). All pass green. The execute loop-2 producer's PASS claim is upheld: execute loop-2 B-1 remediation closed the verify-work loop-1 B-1 FAIL (7 harness Fail) by restoring `# US-0091` + `# US-0093` H1 blocks before `# US-0089`, appending `# US-0090` H1 after `# US-0089` (only `# US-`/`## US-` heading after US-0089), rewording 5 task-table refs `` `# US-0089` ``→`` `US-0089` `` (fixes `test_bug0011_architecture_linkage`), and adding `**US-0125**` row to `docs/developer/README.md` Architecture notes + byte-identical template mirror (closes US-0125 coverage gap). 12/12 `test_us0126_*` contract markers green; opencode-adapter parity OK; compose guards 8/8 UNCHANGED; active↔template byte-identical for all edited pairs; no `OPENCODE_VALIDATOR_FAILED` wrapper resurrected; no DEC-leak in operator prose; `.cursor/` inventory 25 commands + 7 agents matches marker 11 tuple.

## Hard gate — full harness Fail=0 status

**Harness Fail=0 IS claimed (loop-2).** The canonical `tests/report.md` on disk is dated `2026-08-25T17:13:14Z` with `Pass: 845` / `Fail: 0` and zero `[FAIL]` rows — this report is **CURRENT** vs US-0126 + execute loop-2 product edits (execute loop-2 edits landed at `2026-08-25T17:10:00Z`, ~3 minutes BEFORE the report timestamp). Per the QA hard-gate rule, both literals (`Timestamp: 2026-08-25T17:13:14Z` and `Fail: 0`) and the absence of `[FAIL]` rows were independently re-confirmed on disk in this qa subagent. No product/test files (docs/, tests/, scripts/, README.md, its_magic/, template/) were modified after `2026-08-25T17:13:14Z` (verified via filesystem mtime scan — empty result set). The execute loop-2 PASS claim is upheld by current Fail=0 evidence.

## Independent checks (run in this qa subagent)

| Check | Command | Result |
|---|---|---|
| US-0126 contract tests | `python -m pytest tests/us0126_contract_test.py -q` | **12 passed** in 0.15s (12/12 markers green) |
| opencode-adapter parity | `python scripts/check_intake_template_parity.py --scope=opencode-adapter` | **exit 0** — `[INTAKE_TEMPLATE_PARITY_OK] scope=opencode-adapter` |
| README feature coverage | `python scripts/validate_readme_feature_coverage.py --repo . --report` | **PASS** — `coverage_missing=[]`, `coverage_present=["US-0121","US-0122","US-0123","US-0124","US-0125"]`, `status=PASS` (US-0125 gap CLOSED in execute loop-2) |
| tests/report.md literals | Read `tests/report.md` lines 1-5 + grep `[FAIL]` | `Timestamp: 2026-08-25T17:13:14Z`, `Pass: 845`, `Fail: 0`, zero `[FAIL]` rows (rg count = 0) |
| Product/test mtime scan | `Get-ChildItem -Recurse -File | Where LastWriteTimeUtc -gt 2026-08-25T17:13:14Z` | **empty** — no product/test files changed after report timestamp |
| Architecture heading order | `rg '^#+ US-\d+' docs/engineering/architecture.md` | US-0126 (L1747) → US-0091 (L2053) → US-0093 (L2068) → US-0089 (L2091) → US-0090 (L2989); US-0090 is the only `# US-`/`## US-` heading after US-0089 (DEC-0073 satisfied) |
| Triad hot-surface | `python scripts/enforce-triad-hot-surface.py --check` | exit 0 (state.md 1200/1200 lines, units within budget — Active context surface preserved at L7) |

## AC → marker → UAT evidence map

| AC | Marker(s) | UAT result | Evidence |
|---|---|---|---|
| AC-1: Runbook "OpenCode host" section present | m1 `test_us0126_runbook_section_present` | PASS | `docs/engineering/runbook.md` `## OpenCode host operator runbook (US-0126)` h2 body with AC-1 operator phrases |
| AC-2: Reason-code catalog present | m2 `test_us0126_reason_code_catalog_present` | PASS | Consolidated cross-host reason-code table (15 codes); NO `OPENCODE_VALIDATOR_FAILED` wrapper |
| AC-3: Parity scope `--scope=opencode-adapter` PASS | m3 `test_us0126_parity_scope_opencode_adapter`, m10 `test_us0126_template_doc_parity` | PASS | `check_intake_template_parity.py --scope=opencode-adapter` exit 0; active↔template byte-identical for all edited pairs |
| AC-4: Contract tests `test_us0126_*` PASS | m4 `test_us0126_test_marker_checklist`, m12 `test_us0126_prior_story_markers_present` | PASS | 12/12 markers green (independent re-run) |
| AC-5: README hygiene no-dec-leak | m5 `test_us0126_readme_no_dec_leak`, m6 `test_us0126_runbook_no_dec_leak` | PASS | No DEC ids in US-0126 README blurb (root + its_magic); no DEC ids in runbook operator prose before Boundaries subsection |
| AC-6: Program DoD documented | m7 `test_us0126_program_dod_documented` | PASS | DoD sentence key phrases present in runbook h2 body |
| AC-7: Default host reminder | m8 `test_us0126_default_host_reminder` | PASS | Default-host phrases in runbook + README blurb (root + its_magic) |
| AC-8: Out-of-scope list | m9 `test_us0126_out_of_scope_listed` | PASS | 5 excluded items in runbook + README blurb (root + its_magic) |
| AC-9: Sanitization + template parity | m10 `test_us0126_template_doc_parity` | PASS | Active↔template byte-identical for manifest, runbook, parity script, contract test, root README, its_magic README |
| AC-10: Compose — Cursor docs not deleted | m11 `test_us0126_cursor_docs_not_deleted` | PASS | `.cursor/commands/` 25 `.md` + `.cursor/agents/` 7 `.mdc` present vs current-kit-inventory baseline |

## Compose guards (8/8 UNCHANGED — read-only verification)

| Compose target | Verification | Result |
|---|---|---|
| US-0071 (operator-sentence sanitization) | no DEC ids in operator prose; cross-references to runbook h2 / Boundaries subsection only (DQ6/DQ7); markers 5 + 6 PASS | UNCHANGED |
| US-0113..US-0117 (operator docs) | additive OpenCode host runbook section; no Cursor command catalog rewrite | UNCHANGED |
| US-0121 / DEC-0120 (installer `--host` flag docs hook) | `## OpenCode host mode (US-0121)` h2 untouched; US-0126 cross-links | UNCHANGED |
| US-0122 / DEC-0122 (seven role agents) | runbook references role agents; does not redefine permissions | UNCHANGED |
| US-0123 (per-role slug routing) | runbook references `/connect` keys + per-role slug routing; does not re-list vendor slugs | UNCHANGED |
| US-0124 / DEC-0124 (orchestrator plugin + stub reason-code h2) | `## OpenCode orchestrator plugin reason codes (US-0124)` h2 untouched; US-0126 owns consolidated table; cross-links | UNCHANGED |
| US-0125 / DEC-0125 (thin commands + validator-bridge stub h2) | `## OpenCode thin commands + validator bridge (US-0125)` h2 untouched; US-0126 owns consolidated table; DEC-0125 DQ7 raw Python reason codes upheld — `OPENCODE_VALIDATOR_FAILED` wrapper NOT resurrected | UNCHANGED |
| US-0102 / DEC-0087 (no vendor slugs in `template/`) | no vendor slugs in runbook/README operator prose | UNCHANGED |

## Loop-1 → loop-2 remediation status

| Loop-1 finding | Class | Loop-2 status |
|---|---|---|
| NB-1: US-0125 README feature coverage gap (`coverage_missing=["US-0125"]`) | non-blocking | **CLOSED** — `**US-0125**` row added to `docs/developer/README.md` Architecture notes + byte-identical `template/docs/developer/README.md` mirror in execute loop-2; `validate_readme_feature_coverage --repo . --report` now returns `coverage_missing=[]` `status=PASS` (independently re-confirmed in this qa loop-2) |
| NB-2: AC-10 tuple-in-test surplus-file drift class | non-blocking | UNCHANGED — known drift class, non-blocking for US-0126 (current inventory 25+7 matches tuple); no action required |
| Verify-work B-1: 7 harness Fail (architecture.md heading linkage + US-0125 coverage) | blocking (verify-work loop-1) | **CLOSED** — execute loop-2 restored US-0091/US-0093/US-0090 H1 blocks + reworded 5 task-table refs; full harness Pass:845 Fail:0 @ 2026-08-25T17:13:14Z (independently re-confirmed on disk in this qa loop-2) |

## Hard constraints upheld (qa loop-2 verification)

1. Runbook h2 placed immediately after `## OpenCode thin commands + validator bridge (US-0125)` section; US-0121/US-0124/US-0125 h2 sections untouched. PASS
2. Locked operator sentences (DoD + default-host reminder + out-of-scope list) shipped verbatim into runbook h2 body + README blurb; no DEC ids in operator prose (US-0071). PASS
3. Boundaries subsection (runbook only) carries cross-references to `docs/product/standalone-runtime-masterplan.md`, `DEC-0055`, `US-0093`. PASS
4. Consolidated reason-code table: 15 codes; each with one-line semantics + fail-closed action + cross-link; NO `OPENCODE_VALIDATOR_FAILED` wrapper. PASS
5. `OPENCODE_ADAPTER_PAIRS` additive extension (2 new pairs); existing 8 pairs preserved; parity CLI stays byte-only (DQ3 layer split — no grep predicates added). PASS
6. 12 contract markers (one-test-per-AC, AC-5 splits into readme + runbook no-dec-leak; +1 aggregate prior-story marker); all static/grep, no live OpenCode probe (vision D10). PASS
7. AC-10 deterministic static check: `.cursor/commands/` (25 `.md` files) + `.cursor/agents/` (7 `.mdc` files) present vs current-kit-inventory baseline. PASS
8. `installer-owned-paths.manifest` UNCHANGED (DQ8). PASS
9. Active ↔ template byte-identical for all edited pairs. PASS
10. T-anch NO-OP only — no `architecture.md` / `DEC-0126.md` mutation in /execute (loop-2 architecture.md edits were B-1 remediation scope, not T-anch scope; heading policy check PASS). PASS
11. Backlog US-0126 OPEN; acceptance L154 unchecked; intake JSON not mutated; US-0121..US-0125 not reopened. PASS
12. Execute loop-2 proof_hash `C4D6532B2D9658461294FA4DD05618961A9DDE594DA8BCE945AB86497690FA5A` consumed (provided by orchestrator; ttl 2026-08-25T18:10:00Z — consumed at 2026-08-25T17:16:57Z before RUNTIME_PROOF_STALE). PASS

## Producer proof consumed (execute loop-2)

- `producer_runtime_proof_id=rp-auto-20260825-01-execute-dev-20260825T171000Z-loop2-US-0126`
- `producer_attested_proof_hash=C4D6532B2D9658461294FA4DD05618961A9DDE594DA8BCE945AB86497690FA5A`
- `producer_proof_ttl=2026-08-25T18:10:00Z`, `consumed_at=2026-08-25T17:16:57Z` (before RUNTIME_PROOF_STALE)
- `producer_ttl_stale=false`

## Strict runtime proof (DEC-0038) — qa loop-2

- `orchestrator_run_id=auto-20260825-01`
- `runtime_proof_id=rp-auto-20260825-01-qa-qa-20260825T171657Z-loop2-US-0126` (NEW — distinct from producer execute loop-2 proof `...20260825T171000Z...` and from loop-1 qa proof `...20260825T164330Z...`; no proof_id reuse)
- `phase_id=qa`, `role=qa`, `story_id=US-0126`, `sprint_id=S0126`
- `delivery_mode=ultra_lean`, `macro_phase=build+verify`, `model_id=glm-5.2-high`
- `proof_issued_at=2026-08-25T17:16:57Z`
- `proof_ttl_seconds=3600`, `proof_ttl=2026-08-25T18:16:57Z` (UTC = issued_at + 3600s)
- `proof_hash=15325E5A724C3B0692BC0DFA3F1742F8FB7C5BD4407C65D732D4BA09CAD3D88F` (SHA-256 of sorted-key compact JSON payload, UTF-8 bytes via Python 3.12 hashlib; independently recomputed and confirmed match BEFORE returning)
- Canonical payload: `{"delivery_mode":"ultra_lean","macro_phase":"build+verify","model_id":"glm-5.2-high","orchestrator_run_id":"auto-20260825-01","phase_id":"qa","proof_issued_at":"2026-08-25T17:16:57Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260825-01-qa-qa-20260825T171657Z-loop2-US-0126","sprint_id":"S0126","story_id":"US-0126"}`

## Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

- `phase_id=qa`, `role=qa`, `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 — required)
- `fresh_context_marker=qa-US0126-qa-20260825T171657Z-fresh-loop2` (NEW per US-0048 / BUG-0006; marker reuse = stale isolation evidence)
- `timestamp=2026-08-25T17:16:57Z` (UTC)
- Fresh qa subagent per BUG-0006 / US-0048 isolation; no prior chat history carried forward. Context limited to narrow-read: `handoffs/dev_to_qa.md`, `sprints/S0126/summary.md`, `docs/product/acceptance.md` US-0126 row (read-only), `tests/us0126_contract_test.py` (read-only run), `scripts/check_intake_template_parity.py` (read-only run), `scripts/validate_readme_feature_coverage.py` (read-only run), `scripts/enforce-triad-hot-surface.py` (read-only run), `tests/report.md` (read-only literal re-confirmation). No `.env` reads, no credentials access, no intake-evidence mutation, no backlog status/AC mutation, no acceptance.md mutation, no architecture.md mutation, no DEC-0126 mutation, no /verify-work or /execute spawn.
- Producer proof consumed: `rp-auto-20260825-01-execute-dev-20260825T171000Z-loop2-US-0126` (`proof_hash=C4D6532B2D9658461294FA4DD05618961A9DDE594DA8BCE945AB86497690FA5A` — RUNTIME_PROOF_VALID; consumed at 2026-08-25T17:16:57Z before RUNTIME_PROOF_STALE ttl 2026-08-25T18:10:00Z).

## Next scheduled phase

- `next_scheduled_phase=/verify-work` (loop-2, role=qa per US-0069 / DEC-0051 phase→role matrix; fresh qa subagent per BUG-0006 — orchestrator-owned spawn; after sovereign-critic of qa loop-2 per CROSS_MODEL_REVIEW=1)
- `next_scheduled_role=qa`
- `stop_condition=STOP after qa loop-2 PASS. Orchestrator spawns sovereign-critic of qa loop-2 (if CROSS_MODEL_REVIEW=1), then /verify-work loop-2 in fresh qa subagent per BUG-0006. Do NOT spawn /verify-work or /execute from this subagent. Do NOT mark US-0126 DONE. Do NOT tick acceptance L154. Do NOT mutate intake JSON. Do NOT mutate architecture.md or DEC-0126.md. Do NOT reopen US-0121..US-0125.`
- `artifacts_written=sprints/S0126/qa-findings.md (loop-2 PASS overwrite), docs/engineering/state.md (qa loop-2 checkpoint append-bottom — never truncate; triad check PASS at 1200/1200 pre-append; Active context surface preserved at L7), handoffs/resume_brief.md (qa loop-2 PASS prepend -> sovereign-critic of qa loop-2, then /verify-work loop-2)`
- `triad=enforce-triad-hot-surface.py --check exit 0 (state.md 1200/1200 lines, units within budget — Active context surface preserved at L7)`
