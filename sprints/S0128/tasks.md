# Sprint S0128 - Task checklist (US-0128)

Total tasks: 8 (T-anch + T-001..T-007). SPRINT_MAX_TASKS=12; SPRINT_AUTO_SPLIT=1; no split needed.

**Isolation**: `tl-US0128-sprint-plan-2026-08-26T201100Z-fresh` · `model_id=cursor-grok-4.6-high` (glm-5.2-high unavailable this spawn) · `orchestrator_run_id=auto-20260826-01`

## Task execution order

1. T-anch (NO-OP / verification)
2. T-001 (Surrogate eval branch `scripts/sovereign_convergence_lib.py` `_eval_smoke_green` + template mirror per DQ1+DQ3+DQ4)
3. T-002 (`.cursor/commands/qa.md` + `.cursor/commands/verify-work.md` additive `### Convergence smoke surrogate (US-0128)` subsections + template mirrors per DQ2+DQ5)
4. T-003 (`docs/engineering/reason_codes.md` `## US-0128` section with `CONVERGENCE_SMOKE_SURROGATE_MISSING` + clarifying note on US-0110 row + template mirror per DQ3+DQ4)
5. T-004 (NEW `tests/us0128_contract_test.py` + `template/tests/us0128_contract_test.py` byte-identical — 11 markers shell, includes T-007 markers 4,5,7)
6. T-005 (runbook `### Smoke surrogate for waived-probe UAT slices (US-0128)` subsection + template mirror per DQ7)
7. T-006 (`SOVEREIGN_CONVERGENCE_PAIRS` additive rows for qa.md + verify-work.md command pairs + template mirror per DQ8)
8. T-007 (R1+R3 regression guards markers 4, 5, 7 authored inside T-004 file)
9. Integration verification

## Critic NB awareness (execute)

- **T-001** (`a0128arch-challenger-001`): preserve **legacy-first** ordering — `_uat_smoke_passes` before surrogate branch. `id=convergence_smoke` will also match `_step_is_smoke` (R6); do not invert. Fail-closed `CONVERGENCE_SMOKE_SURROGATE_MISSING` when neither top-level `contract_test_failed` nor derived `passed==total` is present.
- **T-002** (`a0128arch-challenger-001` R7): emit explicit `convergence_smoke` on new slices. S0126 `steps[]` lack `probe_kind` — do not mutate S0126; tail fallback is for future slices only (marker 11).
- **T-001/T-004/T-007** (`a0128arch-architect-002`): keep layering — lib vs commands vs tests vs docs. No lib-side `uat.json` synthesis (A4 rejected). Do not touch `_eval_critic_resolved` / `SOVEREIGN_CRITIC_PAIRS`.
- **T-anch** (`a0128arch-subtractor-003`): read-only ceremony; no `architecture.md` mutation; do not mark US-0128 DONE; 11 markers are required (not YAGNI).

## Task checklist

- [x] **T-anch**: Verify `# US-0128` H1 anchor present in `docs/engineering/architecture.md` at L1671 (added in /architecture phase per DEC-0073 §11 / BUG-0010 heading policy; AFTER `# US-0127` L1552 and BEFORE `# US-0091` L1818); verify approach A1 locked + R-0111 DQ1–DQ8 LOCKED; verify compose-do-not-amend 8/8 baseline (US-0109, US-0126, US-0127, US-0110, US-0104, US-0045, US-0048/BUG-0006, US-0056); verify 11-marker contract-test list locked in architecture AC-5 table; verify command subsection placement anchors (`## Self-verify UAT probes (US-0092 / DEC-0078)` L55, `### Browser UAT self-test (US-0093)` L66, `## Steps` L92 in qa.md; same anchors in verify-work.md); verify runbook placement anchors (`### Blocking-only conjunct-3 semantics (US-0127)` L2811, `## Goal-Based Convergence (US-0110 / DEC-0110)` L2764, `### Interpret \`goal_progress\` block` L2829); verify `reason_codes.md` `## US-0127` section at L109 and `## US-0104` at L126; verify `SOVEREIGN_CONVERGENCE_PAIRS` exists in `scripts/check_intake_template_parity.py` L538–547 (2 pairs: convergence lib + validate; qa.md/verify-work.md pairs NOT yet present); verify `tests/us0128_contract_test.py` + `template/tests/us0128_contract_test.py` do NOT yet exist; verify `_eval_smoke_green` root cause at `scripts/sovereign_convergence_lib.py` L459–470 still present (PASSes only via `_uat_smoke_passes`); verify `_uat_smoke_passes` at L443–456 and `_step_is_smoke` at L435–440; verify `sprints/S0126/uat.json` `waived_probes[]` reference fixture (6 classes, `UAT_PROBE_FORBIDDEN`). Record results to `sprints/S0128/t-anch-verification.md`. T-anch is NO-OP / verification only — NO mutation to `docs/engineering/architecture.md` in /execute; T-anch records baseline observations only. (AC-1, AC-2 baseline; NO-OP / verification only)

- [x] **T-001**: Edit `scripts/sovereign_convergence_lib.py` AND `template/scripts/sovereign_convergence_lib.py` (byte-identical active<->template) per architecture DQ1+DQ3+DQ4 LOCKED. Add a surrogate branch inside `_eval_smoke_green` (L459–470). **Legacy path first** (critic NB): if `_uat_smoke_passes(uat)` returns PASS, return PASS (precedence case 1). If legacy FAIL, evaluate surrogate prerequisites: (a) `tests/report.md` Fail:0 via `_report_passes`; (b) active `uat.json` exists; (c) `waived_probes[]` contains all 6 canonical live-runtime probe classes (`browser_smoke`, `api_health`, `process_health`, `cli_smoke`, `build`, `manual_operator`) with `reason_code=UAT_PROBE_FORBIDDEN`; (d) `contract_test_failed == 0` (top-level authoritative; derived fallback from `contract_test_passed == contract_test_total` when top-level absent; fail closed with `CONVERGENCE_SMOKE_SURROGATE_MISSING` when neither present); (e) surrogate step exists (`id=convergence_smoke` with `result=pass` preferred, OR tail step with `probe_kind=contract_tests_primary` and `result=pass`). If surrogate prerequisites met, return PASS. If unmet, return FAIL with `CONVERGENCE_SMOKE_SURROGATE_MISSING` (no smoke step exists) OR `CONVERGENCE_SMOKE_PROBE_FAIL` (smoke step exists but failed — case 2). `ConjunctResult(name="smoke_green", ...)` shape unchanged. `_uat_smoke_passes` (L443–456) and `_step_is_smoke` (L435–440) unchanged. MUST keep `scripts/sovereign_convergence_lib.py` byte-identical with `template/scripts/sovereign_convergence_lib.py` after edit. Tests: markers 1, 2, 3, 4, 5, 6, 8, 9. (AC-1)

- [x] **T-002**: Edit `.cursor/commands/qa.md` AND `.cursor/commands/verify-work.md` (byte-identical active<->template) per architecture DQ2+DQ5 LOCKED. Add additive `### Convergence smoke surrogate (US-0128)` subsection inside `## Self-verify UAT probes (US-0092 / DEC-0078)`, after `### Browser UAT self-test (US-0093)`, before `## Steps`. Emission rule: for ultra_lean/docs/contract-test slices where all 6 live-runtime probe classes are waived with `UAT_PROBE_FORBIDDEN`, `/qa`/`/verify-work` MUST emit `{"id": "convergence_smoke", "description": "Convergence smoke surrogate — waived-probe slice with green contract-test harness", "result": "pass", "marker": "test_us0128_convergence_smoke_surrogate", "evidence_ref": "tests/report.md Fail:0 + uat.json waived_probes[] (6 classes, UAT_PROBE_FORBIDDEN)", "probe_kind": "contract_tests_primary"}` in `sprints/Sxxxx/uat.json` `steps[]` when `contract_test_failed=0`; emit `result=fail` when `contract_test_failed>0` (convergence lib surfaces `CONVERGENCE_SMOKE_SURROGATE_MISSING`). No change to existing `## Self-verify UAT probes` prose, `### Browser UAT self-test` block, or `## Steps` numbering. Mirror to `template/.cursor/commands/qa.md` + `template/.cursor/commands/verify-work.md` byte-identical. MUST keep active <-> template byte-identical after edit. Do not mutate `sprints/S0126/uat.json` (R7 / marker 11). Tests: markers 5, 7, 8. (AC-2, AC-4)

- [x] **T-003**: Edit `docs/engineering/reason_codes.md` AND `template/docs/engineering/reason_codes.md` (byte-identical active<->template) per architecture DQ3+DQ4 LOCKED. New `## US-0128: Convergence smoke surrogate (DEC-0110 §10 smoke-green)` section after the US-0127 section (L109–L125) and before `## US-0104` (L126). Add `CONVERGENCE_SMOKE_SURROGATE_MISSING` (blocked_by=yes) — "smoke green — surrogate prerequisites unmet for waived-probe slice (no smoke step + incomplete waivers or harness red)". Add clarifying note on the US-0110 `CONVERGENCE_SMOKE_PROBE_FAIL` row (description only, not a schema change): "reserved for real smoke step failures and US-0109 deploy smoke; surrogate path uses `CONVERGENCE_SMOKE_SURROGATE_MISSING`". `CONVERGENCE_SMOKE_PROBE_FAIL` description unchanged. MUST keep active <-> template byte-identical after edit. Tests: markers 2, 3, 4, 6. (AC-3)

- [x] **T-004**: Create `tests/us0128_contract_test.py` with 11 markers per architecture DQ6 LOCKED + R-0111 Q1 (11 markers — defense in depth on US-0109/US-0110/US-0127 compose; subtractor NB: not YAGNI). Markers:
  1. `test_us0128_surrogate_passes_when_all_six_waived_and_green` — 6 waived_probes (UAT_PROBE_FORBIDDEN) + `contract_test_failed=0` + `convergence_smoke` step `result=pass` + `tests/report.md` Fail:0 -> `_eval_smoke_green` returns `status=pass`, no reason code (AC-1/AC-5).
  2. `test_us0128_surrogate_missing_when_no_step` — 6 waived + green but NO `convergence_smoke` step and no `probe_kind=contract_tests_primary` tail pass -> `status=fail, reason_code=CONVERGENCE_SMOKE_SURROGATE_MISSING` (AC-1/AC-3/AC-5).
  3. `test_us0128_surrogate_missing_when_harness_fail` — 6 waived + `contract_test_failed>0` + no smoke step -> `status=fail, reason_code=CONVERGENCE_SMOKE_SURROGATE_MISSING` (NOT PROBE_FAIL — no smoke step exists) (AC-1/AC-3/AC-5).
  4. `test_us0128_surrogate_missing_when_partial_waivers` — only 3 of 6 waived + no smoke step -> surrogate does NOT activate; `reason_code=CONVERGENCE_SMOKE_SURROGATE_MISSING` (AC-1/AC-3/AC-5).
  5. `test_us0128_real_smoke_step_pass_wins_over_surrogate` — real smoke-named step `result=pass` -> `_eval_smoke_green` PASS via legacy path (surrogate not consulted); waived_probes irrelevant (AC-1/AC-5).
  6. `test_us0128_real_smoke_step_fail_uses_probe_fail_not_surrogate_missing` — real smoke-named step `result=fail` -> `reason_code=CONVERGENCE_SMOKE_PROBE_FAIL` (NOT SURROGATE_MISSING — smoke step exists and failed) (AC-1/AC-3/AC-5).
  7. `test_us0128_compose_us0109_deploy_smoke_unchanged` — US-0109 deploy smoke path semantics unchanged; surrogate branch does not activate when deploy smoke applies (regression guard vs `tests/us0109_contract_test.py`) (AC-5).
  8. `test_us0128_template_parity_convergence_lib_and_commands` — `scripts/sovereign_convergence_lib.py` <-> `template/scripts/sovereign_convergence_lib.py` byte-identical after AC-1 fix; `.cursor/commands/qa.md` <-> `template/.cursor/commands/qa.md` and `.cursor/commands/verify-work.md` <-> `template/.cursor/commands/verify-work.md` byte-identical after DQ5 subsection add (AC-5/AC-6).
  9. `test_us0128_compose_us0110_five_conjunct_unchanged` — `_eval_smoke_green` still emits `ConjunctResult(name="smoke_green", ...)` with the same shape; `tests/us0110_contract_test.py` 8/8 still pass (no conjunct renumbering, no schema change). The surrogate branch is an additional PASS path inside the same conjunct (AC-5).
  10. `test_us0128_compose_us0127_critic_conjunct_unchanged` — `_eval_critic_resolved` (US-0127) unchanged; `tests/us0127_contract_test.py` 13/13 still pass. US-0128 touches `smoke_green` only, not `critic_resolved` (AC-5).
  11. `test_us0128_compose_us0126_waived_probe_fixture_reference_only` — `sprints/S0126/uat.json` is read as a reference fixture for `waived_probes[]` shape; US-0126 DONE product scope and S0126 release artifacts are NOT mutated by US-0128 (regression guard) (AC-5).
  All markers static/fixture-based; no live critic spawn. Mirror to `template/tests/us0128_contract_test.py` byte-identical for parity pairing. (AC-5)

- [x] **T-005**: Edit `docs/engineering/runbook.md` AND `template/docs/engineering/runbook.md` (byte-identical active<->template) per architecture DQ7 LOCKED. New `### Smoke surrogate for waived-probe UAT slices (US-0128)` subsection inside `## Goal-Based Convergence (US-0110 / DEC-0110)` (L2764), after `### Blocking-only conjunct-3 semantics (US-0127)` (L2811), before `### Interpret \`goal_progress\` block` (L2829). Document: (a) surrogate eligibility (all 6 live-runtime probe classes waived with `UAT_PROBE_FORBIDDEN`); (b) surrogate step contract (`convergence_smoke` id preferred, or `probe_kind=contract_tests_primary` tail with `result=pass`); (c) `contract_test_failed=0` requirement (top-level authoritative, derived fallback); (d) precedence (real smoke step wins; deploy smoke US-0109 unchanged; partial waivers fail closed); (e) remediation for `CONVERGENCE_SMOKE_SURROGATE_MISSING` (emit `convergence_smoke` step in `/qa`/`/verify-work`; ensure 6 waived_probes; fix failing contract tests); (f) R6 — surrogate step IS a smoke step and the surrogate branch is the documented waived_probes + contract_test_failed gate. MUST keep active <-> template byte-identical after edit. (AC-6)

- [x] **T-006**: Edit `scripts/check_intake_template_parity.py` AND `template/scripts/check_intake_template_parity.py` (byte-identical active<->template) per architecture DQ8 LOCKED. Add 2 NEW rows to `SOVEREIGN_CONVERGENCE_PAIRS` (L538–547): `(".cursor/commands/qa.md", "template/.cursor/commands/qa.md")` and `(".cursor/commands/verify-work.md", "template/.cursor/commands/verify-work.md")`. Existing rows (convergence lib + validate) unchanged. `SCOPES["sovereign-convergence"]` already maps to `SOVEREIGN_CONVERGENCE_PAIRS` (L573) — extension is automatic via the tuple union. `SCOPES["all"]` already includes `SOVEREIGN_CONVERGENCE_PAIRS` (L597) — auto-extended. `SOVEREIGN_CRITIC_PAIRS` unchanged (no critic surface touched by US-0128). MUST keep `scripts/check_intake_template_parity.py` byte-identical with `template/scripts/check_intake_template_parity.py` after edit. Tests: marker 8 (`test_us0128_template_parity_convergence_lib_and_commands`) + `python scripts/check_intake_template_parity.py --scope=sovereign-convergence` exit 0. (AC-6)

- [x] **T-007**: Author markers 4 (`test_us0128_surrogate_missing_when_partial_waivers`), 5 (`test_us0128_real_smoke_step_pass_wins_over_surrogate`), 7 (`test_us0128_compose_us0109_deploy_smoke_unchanged`) inside `tests/us0128_contract_test.py` per architecture R1+R3 LOCKED. Marker 5 guards "real smoke step pass wins over surrogate" (defense in depth — a webapp slice with a real smoke step uses the legacy path; surrogate not consulted). Marker 7 guards "US-0109 deploy smoke unchanged" (regression guard vs `tests/us0109_contract_test.py`). Marker 4 guards "partial waivers fail closed" (R3 / challenger NB — only 3 of 6 waived does NOT activate surrogate). Mirror to `template/tests/us0128_contract_test.py` byte-identical (covered by T-004 mirror). (R1+R3 — supports AC-5 regression guards)

## Integration verification (post T-006 + T-004)

- [x] Test gate: `python -m pytest tests/us0128_contract_test.py -v` -> 11/11 PASS
- [x] Parity gate: `check_intake_template_parity.py --scope=sovereign-convergence` PASS (now includes qa.md + verify-work.md command pairs)
- [x] Parity gate: active + template sovereign_convergence_lib.py byte-identical
- [x] Parity gate: active + template qa.md byte-identical
- [x] Parity gate: active + template verify-work.md byte-identical
- [x] Parity gate: active + template runbook.md byte-identical
- [x] Parity gate: active + template reason_codes.md byte-identical
- [x] Parity gate: active + template check_intake_template_parity.py byte-identical
- [x] Parity gate: active + template us0128_contract_test.py byte-identical
- [x] Compose gate: 8/8 UNCHANGED (US-0109/US-0126/US-0127/US-0110/US-0104/US-0045/US-0048/US-0056)
- [x] Compose gate: `pytest tests/us0110_contract_test.py tests/us0104_contract_test.py tests/us0127_contract_test.py -q` PASS (markers 9, 10 + compose regression)
- [x] No-secrets gate: `api_key`/`apikey`/`sk-`/`auth.json`/`.env` grep zero hits on edited files

## Files to touch (scope)

### New (create)

- `tests/us0128_contract_test.py`
- `template/tests/us0128_contract_test.py` (byte-identical mirror for parity)
- `sprints/S0128/t-anch-verification.md`

### Edit (scoped, additive only)

- `scripts/sovereign_convergence_lib.py` (add surrogate branch inside `_eval_smoke_green` per DQ1+DQ3+DQ4)
- `template/scripts/sovereign_convergence_lib.py` (byte-identical mirror)
- `.cursor/commands/qa.md` (additive `### Convergence smoke surrogate (US-0128)` subsection per DQ2+DQ5)
- `template/.cursor/commands/qa.md` (byte-identical mirror)
- `.cursor/commands/verify-work.md` (additive `### Convergence smoke surrogate (US-0128)` subsection per DQ2+DQ5)
- `template/.cursor/commands/verify-work.md` (byte-identical mirror)
- `docs/engineering/reason_codes.md` (append `## US-0128` section per DQ3+DQ4)
- `template/docs/engineering/reason_codes.md` (byte-identical mirror)
- `docs/engineering/runbook.md` (append `### Smoke surrogate for waived-probe UAT slices (US-0128)` subsection per DQ7)
- `template/docs/engineering/runbook.md` (byte-identical mirror)
- `scripts/check_intake_template_parity.py` (add 2 rows to `SOVEREIGN_CONVERGENCE_PAIRS` per DQ8)
- `template/scripts/check_intake_template_parity.py` (byte-identical mirror)

### Verify read-only (no mutation)

- `docs/engineering/architecture.md # US-0128` (T-anch NO-OP; DQ1..DQ8 locks + 11-marker table are the locked source of truth — execute ships the runbook/reason_codes body, NOT architecture.md)
- `docs/product/backlog.md ## US-0128` (read-only — US-0045 canonical status)
- `docs/product/acceptance.md` US-0128 row (read-only — US-0045 derived view)
- `handoffs/intake_evidence/US-0128-intake-20260825.json` (read-only — never mutate prior intake evidence)
- `sprints/S0126/uat.json` (read-only — reference fixture for `waived_probes[]` shape; marker 11 guards non-mutation)

### Compose-guard UNCHANGED (DO NOT TOUCH)

| File | Reason |
|---|---|
| `docs/product/backlog.md` | US-0045 canonical status — `/closure` mutates ONLY at execution time |
| `docs/product/acceptance.md` | US-0045 derived view — same |
| `docs/engineering/architecture.md` | Do not rewrite; T-anch is verification only |
| `decisions/` | No new DEC (per R-0111 §Companion DEC recommendation) |
| US-0109 surfaces (deploy smoke post-publish path / `DEPLOY_SMOKE_*` reason codes) | compose read-only — marker 7 regression guard |
| US-0126 surfaces (`sprints/S0126/uat.json` waived-probe fixture / S0126 release artifacts) | compose read-only — marker 11 regression guard |
| US-0127 surfaces (`_eval_critic_resolved` / `read_open_blocking` / hygiene CLI / `SOVEREIGN_CRITIC_PAIRS`) | compose read-only — marker 10 regression guard |
| US-0110 surfaces (five-conjunct structure / degrade matrix / `CONVERGENCE_SMOKE_PROBE_FAIL` reason code) | compose read-only — marker 9 regression guard |
| US-0104 surfaces (critic findings JSONL / `read_open_blocking` / `resolve_finding`) | compose read-only |
| US-0121..US-0127 DONE rows | do not reopen |

## AC -> Task surjective coverage

| AC | Task(s) |
|---|---|
| AC-1 (Surrogate eval) | T-001, T-004 (markers 1, 2, 3, 4, 5, 6, 8, 9), T-007 (markers 4, 5) |
| AC-2 (Canonical uat step) | T-002, T-004 (markers 5, 7, 8) |
| AC-3 (Fail closed) | T-003, T-004 (markers 2, 3, 4, 6) |
| AC-4 (Command contracts) | T-002, T-004 (markers 5, 7, 8) |
| AC-5 (Contract tests) | T-004 (all 11 markers), T-007 (markers 4, 5, 7) |
| AC-6 (Operator docs + parity) | T-005 (runbook subsection), T-006 (SOVEREIGN_CONVERGENCE_PAIRS + 2 command rows) |

**Surjectivity check**: 6/6 ACs covered (AC-1..AC-6 each have at least 1 task). No `PLAN_AC_COVERAGE_GAP`.
