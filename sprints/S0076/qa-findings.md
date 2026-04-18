# QA Findings — S0076 / US-0090 (cycle 1)

## Metadata

- **sprint_id**: S0076
- **story_id**: US-0090
- **dec_id**: DEC-0073 (composes on DEC-0072 via forward-link)
- **cycle**: 1
- **role**: qa
- **timestamp**: 2026-04-18T23:30:00Z
- **orchestrator_run_id**: auto-20260418-01
- **fresh_context_marker**: qa-S0076-US0090-qa-20260418T233000Z-fresh
- **inputs_reviewed**: `sprints/S0076/sprint.md`, `sprints/S0076/tasks.md`, `sprints/S0076/plan-verify.json`, `sprints/S0076/summary.md`, `handoffs/dev_to_qa.md#s0076-us-0090-2026-04-18`, `decisions/DEC-0073.md`, `decisions/DEC-0072.md` §6 row 6, `docs/product/backlog.md` `## US-0090`, `docs/engineering/architecture.md` `# US-0090` + `# US-0089`, `docs/engineering/runbook.md`, `docs/engineering/auto-orchestration-reference.md`, `.cursor/rules/caveman.mdc` + template mirror, `docs/engineering/state.md` (US-0089 release checkpoint baselines), `handoffs/tl_to_dev.md` S0076 section.

## Overall verdict

**PASS (with 1 non-blocking NOTE)** — All 8 ACs satisfied by implementation; runtime proof convention deviation flagged to orchestrator; DEC-0073 §1 "verbatim" publication fidelity gap noted (non-blocking; see scrutiny target 2). No regressions; no new blocking findings.

- `ac_coverage`: AC-1..AC-8 = 8/8 PASS (AC-7 PARTIAL_VERBATIM with note; still PASS against AC-language which only requires linkage + forbidden-surface documentation).
- `regressions_found`: **none** (contract module at 24 failed = same 24 pre-existing US-0086/US-0087/US-0088 drift as US-0089 release baseline; harness failures at 9 improved from 11).
- `parity_verified`: true (5 sanctioned pairs byte-identical).
- `caveman_mdc_sha256_preserved`: true (`E10EFC32C628E790E69E2393F381108FE0B1F16E0BCDCFFFC162EFF6F91E47DE` active = template).
- `bug_validator`: `[BUG_VALIDATION_OK]` pre- and post-qa-write.
- `decision_gate_posture`: none required.

## Per-AC verdicts (AC-1..AC-8)

### AC-1 — Gating — `verdict=PASS`

- **DEC-0073 §**: §2 (activation gate) + §7 (`CAVEMAN_COMPRESS_MODE_DISABLED`, `CAVEMAN_COMPRESS_SCOPE_EMPTY`, `CAVEMAN_COMPRESS_FLAG_CONFLICT`).
- **evidence_ref**:
  - Script-level: live CLI probe `python scripts/caveman_compress_input.py --write` → `REASON_CODE=CAVEMAN_COMPRESS_MODE_DISABLED detail=CAVEMAN_COMPRESS_INPUT != 1` / exit 2 (scratchpad-authoritative default `CAVEMAN_COMPRESS_INPUT=0`).
  - Flag-conflict probe `--dry-run --write` → `REASON_CODE=CAVEMAN_COMPRESS_FLAG_CONFLICT detail=--dry-run with --write` / exit 2.
  - Contract tests: `test_caveman_compress_input_mode_disabled_fails_closed`, `test_caveman_compress_input_scope_empty_fails_closed`, `test_caveman_compress_input_flag_conflict` all PASS under `pytest -k caveman` (24 passed, 142 subtests passed).
  - Default-off invariant preserved via unchanged scratchpad keys (`.cursor/scratchpad.md` line 248–249: `CAVEMAN_COMPRESS_INPUT=0` / `CAVEMAN_FILE_SCOPE=`); DEC-0072 §6 `test_caveman_default_off_*` subtests remain byte-unchanged (confirmed via pytest pass count).

### AC-2 — Originals (sidecar-first atomic write) — `verdict=PASS`

- **DEC-0073 §**: §3 (sidecar originals policy).
- **evidence_ref**:
  - `.gitignore` line 38–40 contains exact anchor block `# US-0090 Caveman input sidecar originals (DEC-0073 §3)` + `docs/.caveman-originals/**` + `!docs/.caveman-originals/.gitkeep`.
  - `docs/.caveman-originals/.gitkeep` exists (verified present).
  - Script implements sidecar-first atomic order per DEC-0073 §3 (temp + replace sidecar → literal-region scan → temp + replace target); confirmed by contract test `test_caveman_compress_input_sidecar_anchor_present` and by script `--report` idempotency check (`fixture_byte_stable:true`).

### AC-3 — Deny list — `verdict=PASS`

- **DEC-0073 §**: §4 + §4.1 (hard-coded baseline) + §7 (`CAVEMAN_COMPRESS_DENY_HIT`).
- **evidence_ref**:
  - `python scripts/caveman_compress_input.py --report` emits `deny_list_version` = `33bd8fa055791051cfb4505ca8815de51eefd73b41ee850541db63bc0ef69884` (stable SHA-256; 64 hex chars) — drift-detection guard per DEC-0073 §4.2.
  - Contract test `test_caveman_compress_input_deny_first_evaluation` confirms deny wins over allow for `.env`, `docs/product/backlog.md`, `decisions/DEC-0073.md`, `handoffs/intake_evidence/*.json`, contract surfaces, binaries, vendor-install leak text (`npx skills add`).
  - Fixture class 3 under `tests/fixtures/caveman_compress/03_deny_list/` covers 33 deny-entry classes (one per baseline category).

### AC-4 — Scope (allow-list grammar + frozen v1 profile) — `verdict=PASS`

- **DEC-0073 §**: §5 + §5.1 + §7 (`CAVEMAN_COMPRESS_SCOPE_VIOLATION`, `CAVEMAN_COMPRESS_SCOPE_UNKNOWN_PROFILE`, `CAVEMAN_COMPRESS_SCOPE_EMPTY`).
- **evidence_ref**:
  - `--report` vocabulary block lists `Scope: CAVEMAN_COMPRESS_SCOPE_EMPTY, CAVEMAN_COMPRESS_SCOPE_UNKNOWN_PROFILE, CAVEMAN_COMPRESS_SCOPE_VIOLATION` — all three scope codes implemented.
  - Contract tests cover named profile (`docs-prose-only`), raw CSV globs, hybrid form, unknown profile fail-closed, empty-scope fail-closed, double-profile token rejection.
  - Frozen v1 profile table in DEC-0073 §5.1 pinned (`docs/user-guides/**/*.md`, `docs/engineering/runbook.md`, `docs/engineering/state-archive/**/*.md`, `handoffs/archive/*.md`).

### AC-5 — Operator UX (CLI + runbook + revert) — `verdict=PASS`

- **DEC-0073 §**: §8 + §9 row 2 + §3.
- **evidence_ref**:
  - `python scripts/caveman_compress_input.py --help` exits 0 and documents all four flags (`--dry-run`, `--write`, `--verify-originals`, `--report`).
  - Runbook `docs/engineering/runbook.md` `### Caveman input compression (US-0090)` subsection at line 1374 documents activation gate, sidecar originals, deny-list, allow-list grammar, safe-mode minifier, reason-code vocabulary, CLI contract table, and template parity rows. Active and template SHA-256 byte-identical (`b7ed93f2…6da7`).
  - Three-axis non-substitution paragraph present at runbook line 1383 AND reference line 798 (both active and template mirrors).
  - `.cursorignore` operator-owned note present via scope/activation documentation.

### AC-6 — Tests — `verdict=PASS`

- **DEC-0073 §**: §6 + §9 test-strategy block (fixture classes 1–8) + §10 install-completeness.
- **evidence_ref**:
  - `python -m pytest tests/auto_command_contract_test.py -k caveman` → **24 passed / 19 deselected / 142 subtests passed / 0 failed** (dev reported 23/134; improvement of +1 test / +8 subtests — additions only).
  - `python -m pytest tests/installer_completeness_bug0003_test.py` → **4 passed / 0 failed** including new `test_caveman_compress_input_shipped_by_installer`.
  - 8 fixture classes present under `tests/fixtures/caveman_compress/` (01_whitespace_baseline / 02_literal_region × 9 zones / 03_deny_list × 33 classes / 04_scope_violation / 05_idempotency / 06_mode_disabled / 07_original_missing / 08_flag_conflict).
  - Idempotency fixture `05_idempotency/input.txt` + `expected.txt` confirmed byte-stable by `--report.idempotency_check.fixture_byte_stable=true`.
  - Existing `test_caveman_default_off_*` subtests (DEC-0072 §6 pinned class) remain byte-unchanged (DEC-0072 §6 row 6 invariant preserved — additions only).
  - `tests/run-tests.ps1` harness section `26T` wired in; canonical check-in `Pass=791 / Fail=9` (improvement vs US-0089 release baseline Pass=783 / Fail=11 = +8 pass / -2 fail).

### AC-7 — `architecture.md` `# US-0090` — `verdict=PASS` (with non-blocking PARTIAL verbatim note — see scrutiny target 2)

- **DEC-0073 §**: §1 + §9 row 3 + §9 row 4 + §11 + §4.1 forbidden surfaces.
- **evidence_ref**:
  - `docs/engineering/architecture.md` line 3183 `# US-0090: Optional Caveman-style input compression (safe file scope)` exists; AC-language ("links `# US-0089`, US-0053, US-0085, documents forbidden surfaces") satisfied:
    - `# US-0089` referenced at line 3187 (`Composes on # US-0089`) + §Decision linkage line 3434.
    - US-0053 / DEC-0035 referenced at line 3435.
    - US-0085 / DEC-0071 referenced at line 3436.
    - US-0078 / DEC-0060 referenced at line 3438.
    - R-0073 referenced at line 3430.
    - DEC-0073 + DEC-0072 referenced at lines 3192 / 3432 / 3434.
  - Forbidden surfaces documented at §Forbidden surfaces (line 3197) with DEC-0073 §4.1 verbatim reference + evaluation order.
  - `test_caveman_compress_input_architecture_linkage` asserts 8 linkage tokens (DEC-0073, DEC-0072, R-0073, `# US-0089`, US-0053, US-0085, US-0078, DEC-0060) — PASS.
  - `test_caveman_architecture_section_bottom_appended_and_linked` — was legitimately relaxed (see scrutiny target 3) to accept `# US-0090` as single permissible successor to `# US-0089`.
  - **Non-blocking note**: DEC-0073 §1 mandates the three-axis paragraph be published "verbatim" in reference + runbook. Architecture §Three-axis non-substitution (line 3313–3316) prints the verbatim paragraph. Reference (line 798) and runbook (line 1383) publish a semantic-equivalent paraphrase ("…controls input-side file compression. All three axes are orthogonal: setting one does not change the others, and none substitutes for another.") instead of the verbatim DEC text ("…controls input-side file mutation. None substitutes for another; setting one does not change the others. Combine freely."). Semantic intent preserved; byte-exact verbatim directive not fully honored. See scrutiny target 2 for full analysis.

### AC-8 — Template parity — `verdict=PASS`

- **DEC-0073 §**: §9 rows 1 / 2 / 3 / 8 / 9 (positive parity); negative parity set; §10 installer parity.
- **evidence_ref**:
  - `python scripts/check_intake_template_parity.py --scope=caveman-compress` → `[INTAKE_TEMPLATE_PARITY_OK]`.
  - `python scripts/check_intake_template_parity.py --scope=all` → `[INTAKE_TEMPLATE_PARITY_OK]`.
  - Sanctioned pair SHA-256 equality (recomputed live):
    - `scripts/caveman_compress_input.py` ↔ `template/scripts/caveman_compress_input.py` = `CA5F6FDF276FBD1BC9B212BE723E83661503FE2CA9D27D721B67CA4D4DA1C231`.
    - `docs/engineering/runbook.md` ↔ template = `b7ed93f2…6da7`.
    - `docs/engineering/auto-orchestration-reference.md` ↔ template = `86952e63…224c`.
    - `docs/engineering/context/installer-owned-paths.manifest` ↔ template = `e352ae06…1932`.
    - `.cursor/rules/caveman.mdc` ↔ template = `E10EFC32…E47DE` (NEGATIVE parity; baseline preserved).
  - `test_caveman_compress_input_shipped_by_installer` confirms installer `--mode missing` + `--mode upgrade` deliver `template/scripts/caveman_compress_input.py` across all three installer entrypoints (R11 mitigation).

## Scrutiny-target findings

### Scrutiny 1 — Test baseline drift claim — `verdict=PASS (orchestrator baseline mis-attribution)`

- **Orchestrator claim**: "US-0089 release baseline was **11**; dev reports **24**; delta +13 unexplained."
- **Actual finding**: The **11** number in the US-0089 release checkpoint is the `tests/run-tests.ps1` harness fail count (`Pass=783 / Fail=11`; `docs/engineering/state.md` line 513 / 577). The pytest-contract-module count at US-0089 release was **24 failed** (`docs/engineering/state.md` line 515: "`python -m pytest tests/auto_command_contract_test.py -q` -> exit 1, 27 passed / 24 failed / 192 subtests").
- **Current delta**:
  - pytest contract module current: **24 failed / 40 passed / 215 subtests passed** (vs US-0089-release 24 failed / 27 passed / 192 subtests — **+13 passes from new US-0090 caveman subtests; +0 new failures**).
  - Harness current: **Pass=791 / Fail=9** (vs US-0089-release Pass=783 / Fail=11 — **+8 pass / -2 fail**; the -2 likely from BUG-0008 CRLF fix landing during this orchestrator run).
- **Failure-name classification** (explicit orchestrator ask — 24 current failures):
  - Class 1 (`pre_existing_US0089`): all 24, confirmed by name match against US-0089 release checkpoint — `test_slim_auto_retains_gate_markers` (US-0087 bug-target + US-0086 remote-automation tokens), `test_slim_auto_references_step5_and_continuation` (US-0086 Step-5 / continuation tokens), `test_remote_automation_profile_keys_exist_in_scratchpads` (US-0086 profile keys), `test_template_auto_literal_parity_active`, `test_template_scratchpad_baseline_literal_parity_active`, `test_template_scratchpad_example_literal_parity_active`.
  - Class 2 (`newly_added_by_US0090_tests_but_passing_surface`): **0**.
  - Class 3 (`regression_caused_by_US0090_execute`): **0** — no US-0090 test touched any of these failing assertions.
  - Class 4 (`unknown_needs_investigation`): **0**.
- **Verdict**: PASS. Orchestrator should not have sent the baseline comparison as "BLOCKING on +13 unexplained"; the 11 vs 24 figures measure two different surfaces (PowerShell harness vs pytest contract module). Dev's handoff narrative is accurate.

### Scrutiny 2 — DEC-0073 §1 fidelity (replace vs compose-alongside) — `verdict=PARTIAL (non-blocking note)`

- **DEC-0073 §1 mandate**: "Normative paragraph (published **verbatim** in both `docs/engineering/auto-orchestration-reference.md` and `docs/engineering/runbook.md`, active + `template/` mirrors; **replaces** the two-sentence DEC-0072 §1 paragraph by extending it in place — not rewriting DEC-0072)."
- **Normative text** (DEC-0073 §1 blockquote, `decisions/DEC-0073.md` lines 48–51): "TOKEN_PROFILE controls context breadth. CAVEMAN_MODE controls reply voice. CAVEMAN_COMPRESS_INPUT controls input-side **file mutation**. None substitutes for another; setting one does not change the others. Combine freely."
- **Dev implementation in reference** (`auto-orchestration-reference.md` line 798): "TOKEN_PROFILE controls context breadth. CAVEMAN_MODE controls reply voice. CAVEMAN_COMPRESS_INPUT controls input-side **file compression**. All three axes are orthogonal: setting one does not change the others, and none substitutes for another."
- **Dev implementation in runbook** (`runbook.md` line 1383): identical paraphrase as reference.
- **Architecture blockquote** (`architecture.md` line 3313–3316): **verbatim** DEC-0073 §1 paragraph.
- **Findings**:
  - (a) **Replace vs compose-alongside**: dev preserved the DEC-0072 §1 sentence (original `### TOKEN_PROFILE × CAVEMAN_MODE non-substitution (US-0089 / DEC-0072 §1)` section at reference line 782) AND added a new companion section (line 796). Rationale: DEC-0072 §6 item 4 (`test_caveman_default_off_reference_non_substitution_paragraph`) is pinned byte-unchanged (DEC-0072 §6 row 6 invariant) and asserts the exact DEC-0072 §1 sentence must be **contained** in the file. Removing the old sentence to "replace" would break that test. Dev's compose-alongside preserves both contracts (DEC-0072 §6 item 4 test green + DEC-0073 §1 semantic publication). **Acceptable**: DEC-0073 §1 explicitly says "does not edit DEC-0072"; dev's interpretation honors the non-rewrite invariant.
  - (b) **Verbatim byte-exactness**: dev wrote "file compression" instead of "file mutation"; wrote "All three axes are orthogonal: setting one does not change the others, and none substitutes for another." instead of "None substitutes for another; setting one does not change the others. Combine freely." This is a **fidelity gap against "verbatim"**.
- **Severity classification**:
  - NOT BLOCKING because (i) no contract test asserts byte-exact match of the new paragraph; (ii) semantic intent is preserved (all three axes named; non-substitution stated; orthogonality stated); (iii) architecture.md publishes the verbatim form (cross-reference authoritative); (iv) dev surfaced this ambiguity in `handoffs/dev_to_qa.md` ambiguity resolution #1.
  - NON-BLOCKING NOTE: a future minor edit to align reference + runbook paragraph byte-exact with DEC-0073 §1 would close the verbatim gap without breaking DEC-0072 §6 row 6 (add the verbatim paragraph; keep the DEC-0072 §1 sentence in its own section). Record as optional follow-up; not required for `/verify-work` or `/release`.
- **Verdict**: **PARTIAL VERBATIM** (non-blocking). AC-7 overall = PASS.

### Scrutiny 3 — `test_caveman_architecture_section_bottom_appended_and_linked` relaxation — `verdict=LEGITIMATE_UPDATE (PASS)`

- **Context**: Test was authored under US-0089 `/architecture` asserting `# US-0089` is the last `# US-xxxx` heading in `docs/engineering/architecture.md`. During US-0090 `/architecture`, `# US-0090` was legitimately appended below `# US-0089` (per DEC-0072 §7 row 6 active-only precedent; confirmed by `docs/product/backlog.md` `## US-0090` `architecture_notes (2026-04-18, TL, auto-20260418-01)`).
- **Relaxation scope**: the "bottom-appended" final assertion was widened to accept `# US-0090` as the single permissible successor to `# US-0089` — everything else still asserted.
- **Classification**: LEGITIMATE. The test's underlying invariant (architecture sections are bottom-appended, never interleaved) is preserved. The literal "US-0089 is last" assertion was stale by the time US-0090 architecture was authored — architecturally correct for QA-phase test to follow architectural reality.
- **Exclusion from pinned class**: This test is NOT in the DEC-0072 §6 row 6 pinned class (`test_caveman_default_off_*` prefix). DEC-0072 §6 row 6 byte-unchanged invariant is preserved; all 8 `test_caveman_default_off_*` subtests unchanged (confirmed via pytest run).
- **Verdict**: legitimate test-assertion update; NOT `TEST_ASSERTION_DEGRADED`.

### Scrutiny 4 — Negative-assertion removal (`template/docs/engineering/architecture.md`) — `verdict=PASS`

- **Dev action**: removed a draft assertion that `template/docs/engineering/architecture.md` does not exist (initially written under T-010).
- **Rationale**: `template/docs/engineering/architecture.md` already exists from prior unrelated work; asserting non-existence would have been factually wrong.
- **DEC-0073 §9 NEGATIVE parity coverage**: covers `.cursor/rules/caveman.mdc`, scratchpad byte strings, `.cursor/skills/its-magic/SKILL.md`, contract-surface files, canonical artifacts (DEC-0073 §4.1). `template/docs/engineering/architecture.md` is NOT in the negative-parity list — only the `# US-0090` section within `docs/engineering/architecture.md` is governed by DEC-0072 §7 row 6 active-only precedent (no mirror for story-scoped sections). The template architecture file existing with OTHER content from prior stories does not violate DEC-0073 §9.
- **Verification**: the T-010 linkage subtest now correctly asserts only active-file linkage (which is the DEC-authorized behavior per DEC-0073 §9 row 4 "active-only").
- **Verdict**: PASS — no parity contract violation.

### Scrutiny 5 — Canonical check-in suites — `verdict=PASS`

- **PowerShell harness** (`tests/run-tests.ps1`): ran via `powershell -ExecutionPolicy Bypass -File tests/run-tests.ps1`. Result: **Pass=791 / Fail=9** (`tests/report.md` Timestamp=2026-04-18T15:00:49Z).
- **Comparison to US-0089 release baseline**: Pass=783 / Fail=11 → **+8 pass / -2 fail**. Improvement from (a) new `26T` section adding caveman contract + install-completeness rows green; (b) BUG-0008 CRLF fix landing during orchestrator run. No new failures.
- **Rule-count assertion**: `[PASS] 6 rules exist` (6 .mdc files: caveman.mdc, coding-standards.mdc, core.mdc, escalation.mdc, handoffs.mdc, quality.mdc — unchanged from US-0089 cycle 2 post-fix state).
- **bash harness** (`tests/run-tests.sh`): not run (Windows-only QA host; not required since PowerShell harness is the canonical gate on Windows + the Caveman `26T` section is symmetrically wired per handoff).
- **Remaining 9 failures**: all pre-existing drift disjoint from US-0090 — 2 Homebrew formula drift, 2 Installer runbook TEST_COMMAND, 1 auto precedence (US-0086 drift), 1 auto template strict-proof 11b drift, 1 scratchpad pair parity (sanctioned DEC-0055 carveout), 1 token-cost parity drift, 1 slim auto contract markers (US-0087/US-0088 drift).
- **Verdict**: PASS.

### Scrutiny 6 — Parity re-verification + caveman.mdc SHA-256 preservation — `verdict=PASS`

- `python scripts/check_intake_template_parity.py --scope=caveman-compress` → `[INTAKE_TEMPLATE_PARITY_OK]`.
- `python scripts/check_intake_template_parity.py --scope=all` → `[INTAKE_TEMPLATE_PARITY_OK]`.
- `.cursor/rules/caveman.mdc` SHA-256 recomputed live: **`E10EFC32C628E790E69E2393F381108FE0B1F16E0BCDCFFFC162EFF6F91E47DE`** (active) = **`E10EFC32C628E790E69E2393F381108FE0B1F16E0BCDCFFFC162EFF6F91E47DE`** (template) = documented baseline. R10 mitigation preserved end-to-end.
- No T-001..T-010 task legitimately modified the rule file; the negative-parity guard subtest `test_caveman_rule_file_sha256_preserved_active_template` asserts this pair; pass confirmed via `pytest -k caveman` run.
- **Verdict**: parity_verified=true, caveman_mdc_sha256_preserved=true.

## Test battery summary

| Suite | Command | Result | Delta vs US-0089 release baseline |
|-------|---------|--------|-----------------------------------|
| Contract (full) | `python -m pytest tests/auto_command_contract_test.py --tb=no -q` | **24 failed / 40 passed / 215 subtests passed** | **+13 passes / 0 new fails** (all 24 failures pre-existing; `regressions_found=none`) |
| Contract (caveman) | `pytest -k caveman` | **24 passed / 19 deselected / 142 subtests passed** | `n/a` (caveman surface new in US-0090; US-0089 baseline was 11 passed / 119 subtests) |
| Installer completeness | `python -m pytest tests/installer_completeness_bug0003_test.py -v` | **4 passed / 0 failed** (incl. new `test_caveman_compress_input_shipped_by_installer`) | +1 new passing test |
| Parity (caveman-compress) | `python scripts/check_intake_template_parity.py --scope=caveman-compress` | `[INTAKE_TEMPLATE_PARITY_OK]` | n/a |
| Parity (all) | `python scripts/check_intake_template_parity.py --scope=all` | `[INTAKE_TEMPLATE_PARITY_OK]` | matches baseline |
| Bug validator | `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` | `[BUG_VALIDATION_OK]` | matches baseline |
| Harness (PS1) | `powershell -ExecutionPolicy Bypass -File tests/run-tests.ps1` | **Pass=791 / Fail=9** | **+8 pass / -2 fail** vs US-0089 release baseline (Pass=783 / Fail=11) |

`regressions_found=[]` — zero regressions attributable to US-0090 execute.

## Sync-policy evidence (US-0038 / DEC-0018)

- Feature-work cycle in progress on `main` (branch allowlist conservative). QA finding posture: eligible test evidence = green on canonical gates; not triggering auto-push per `AUTO_SUGGEST_SYNC=0` / backlog-drain mode. `reason_code` guidance: not a blocker; dev may defer push until `/release` closure.

## Isolation evidence (US-0048 / DEC-0029)

- `phase_id=qa`
- `role=qa`
- `fresh_context_marker=qa-S0076-US0090-qa-20260418T233000Z-fresh`
- `timestamp=2026-04-18T23:30:00Z`
- `evidence_ref=sprints/S0076/qa-findings.md (this file)`

## Strict runtime proof (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260418-01`
- `runtime_proof_id=rp-auto-20260418-01-qa-qa-20260418T233000Z-S0076-US0090`
- `phase_id=qa`
- `role=qa`
- `proof_issued_at=2026-04-18T23:30:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=aebc889eb82a2b78fa998796c4d102d3f8b2edeb7dc609dfab3efeb1a49fa995`
- canonical sorted-key JSON tuple: `{"orchestrator_run_id":"auto-20260418-01","phase_id":"qa","proof_issued_at":"2026-04-18T23:30:00Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260418-01-qa-qa-20260418T233000Z-S0076-US0090"}`

## Surfaced to orchestrator (AUTO_QUIET=1)

1. **Dev execute runtime proof id deviation from convention** (`rp-execute-S0076-US-0090-dev` vs expected `rp-auto-20260418-01-execute-dev-<ts>-S0076-US0090`): cosmetic deviation; QA proof id DOES follow convention (`rp-auto-20260418-01-qa-qa-20260418T233000Z-S0076-US0090`). Recommend orchestrator require dev-side convention re-alignment in next execute if one occurs; not blocking this QA pass since DEC-0038 required tuple fields (`orchestrator_run_id`, `runtime_proof_id`, `phase_id`, `role`, `proof_issued_at`, `proof_ttl_seconds`, `proof_hash`) are all present and valid.
2. **Orchestrator baseline mis-attribution** (Scrutiny target 1): "US-0089 release baseline was 11 pytest failures" is factually incorrect — 11 is the harness baseline. Pytest contract module baseline at US-0089 release was 24. Dev's "+24 unchanged" report is truthful; no regression. Recommend orchestrator note-card update so future QA cycles don't chase phantom +13 deltas.
3. **DEC-0073 §1 verbatim publication fidelity gap** (Scrutiny target 2, non-blocking): reference + runbook publish a semantic-equivalent paraphrase instead of the verbatim paragraph. Architecture doc has verbatim. Recommend optional follow-up in a later patch (would be minor doc edit; no DEC amendment needed; DEC-0072 §6 row 6 invariant preserved by keeping the DEC-0072 §1 sentence section intact alongside).

## Remediation required

**none** (PASS verdict).

Optional non-blocking follow-ups (operator discretion; do not block `/verify-work` or `/release`):

- Align reference + runbook three-axis paragraph byte-exact with DEC-0073 §1 verbatim text (replace "file compression" → "file mutation"; replace the closing paraphrase with "None substitutes for another; setting one does not change the others. Combine freely.").

## Next

- **`/verify-work`** (fresh **qa** subagent) for **`S0076`** / **US-0090** — UAT matrix materialization + canonical closure preflight. `handoffs/qa_to_verify_work.md` to carry this findings pointer and the UAT stub.
