# QA Findings — S0087 / US-0097

## Metadata

- **sprint_id**: S0087
- **story_id**: US-0097
- **dec_id**: DEC-0083 (amends DEC-0045; reframes DEC-0074 paths)
- **research_anchor**: R-0084
- **role**: qa
- **timestamp**: 2026-06-14T01:00:00Z
- **orchestrator_run_id**: auto-20260613-01
- **fresh_context_marker**: qa-S0087-US0097-qa-20260614T010000Z-fresh
- **inputs_reviewed**: `handoffs/dev_to_qa.md`, `sprints/S0087/tasks.md`, `sprints/S0087/summary.md`, `sprints/S0087/plan-verify.json`, `docs/product/backlog.md` `## US-0097`, `decisions/DEC-0083.md`, `docs/engineering/architecture.md` `# US-0097`, `docs/engineering/runbook.md`, `docs/engineering/context/installer-owned-paths.manifest`, `scripts/project_readme_coverage_lib.py`, `scripts/validate_project_readme_coverage.py`, `scripts/readme_feature_coverage_lib.py`, `scripts/check_intake_template_parity.py`, `tests/auto_command_contract_test.py`, `.cursor/commands/execute.md`, `.cursor/commands/release.md`, `.cursor/scratchpad.md`, `.cursor/scratchpad.local.example.md`.

## Overall verdict

**PASS** — All 10 ACs (AC-1..AC-10) satisfied on independent QA re-run; eight `test_us0097_*` contract subtests green (74 subtests); `validate_project_readme_coverage.py --self-test` OK; template parity `--scope=project-readme` OK; US-0091 regression guard green; installer manifest excludes root `README.md`; scratchpad kit-repo semantics confirmed (`FRAMEWORK_KIT_REPO=1` active, `=0` template example); runbook operator recipes present. Story **US-0097** remains **OPEN** per **US-0045** (closure at `/release`).

- `ac_coverage`: AC-1..AC-10 = 10/10 PASS
- `regressions_found`: **none attributable to US-0097**
- `parity_verified`: true (`check_intake_template_parity.py --scope=project-readme` → `[INTAKE_TEMPLATE_PARITY_OK]`)
- `project_readme_validator`: `[PROJECT_README_COVERAGE_SELF_TEST_OK]`
- `decision_gate_posture`: none required
- `blocking_findings`: **none**

**Full harness note (non-blocking):** `tests/run-tests.ps1` reports 3 pre-existing **BUG-0009** CI-guard failures (`test_bug0009_*`) unrelated to US-0097 scope; US-0097 contract section (§26V) and all story-scoped gates green.

## Test plan

| Step | Command / check | Expected | Result |
|------|-----------------|----------|--------|
| 1 | `pytest -k us0097 tests/auto_command_contract_test.py -v` | 8 passed | **PASS** (8 passed, 74 subtests) |
| 2 | `python scripts/validate_project_readme_coverage.py --self-test` | `[PROJECT_README_COVERAGE_SELF_TEST_OK]` | **PASS** |
| 3 | `python scripts/check_intake_template_parity.py --scope=project-readme` | `[INTAKE_TEMPLATE_PARITY_OK]` | **PASS** |
| 4 | `pytest -k us0097_us0091 tests/auto_command_contract_test.py -v` | US-0091 regression guard green | **PASS** |
| 5 | `python scripts/check-user-visible-metadata.py` | exit 0 | **PASS** |
| 6 | Manual: installer manifest | no root `README.md` in `[install_paths]`; `its_magic` retained | **PASS** |
| 7 | Manual: execute step 23 + release step 3g | 23a/23b/23c literals; 3g after 3f order | **PASS** |
| 8 | Manual: scratchpad keys | `PROJECT_README_ENFORCE=1`; active `FRAMEWORK_KIT_REPO=1`; template example `=0` | **PASS** |
| 9 | Manual: runbook § Project README | S1–S5, M1–M5, operator recipes table | **PASS** |
| 10 | `tests/run-tests.ps1` (baseline) | US-0097 §26V green; note pre-existing BUG-0009 failures | **PASS_WITH_NOTE** (3 unrelated BUG-0009 failures) |

## Per-AC verdicts (AC-1..AC-10)

### AC-1 — Installer ownership — `verdict=PASS`

- **Task**: T-001
- **evidence_ref**: `docs/engineering/context/installer-owned-paths.manifest` — root `README.md` absent from `[install_include_paths]` and `[clean_paths]`; `its_magic` retained. `test_us0097_installer_manifest_no_root_readme` green.

### AC-2 — Non-destructive migration M1–M5 + S1–S5 — `verdict=PASS`

- **Task**: T-002
- **evidence_ref**: `scripts/project_readme_coverage_lib.py` migration + sentinel tables; runbook § Project README coverage validation. `test_us0097_placeholder_sentinel_table` green.

### AC-3 — Project README bootstrap — `verdict=PASS`

- **Task**: T-003
- **evidence_ref**: Bootstrap scaffold materializer + vision H1/purpose sourcing. `test_us0097_execute_step23_literals` covers 23a bootstrap branch.

### AC-4 — Per-story/sprint delta — `verdict=PASS`

- **Task**: T-004, T-005
- **evidence_ref**: Execute step **23b** mandatory delta + release step **3g**; reason codes `PROJECT_README_DELTA_SKIPPED`. `test_us0097_execute_step23_literals` + `test_us0097_release_step3g_literals` green.

### AC-5 — Audience structure — `verdict=PASS`

- **Task**: T-003, T-007
- **evidence_ref**: Scaffold `## For users` / `## For developers` / `## Features` + `<!-- project-readme-feature-catalog -->`; framework catalog confined to `its_magic/README.md`. `readme_feature_coverage_lib.py` reframed to `its_magic/README.md`.

### AC-6 — Gate separation — `verdict=PASS`

- **Task**: T-007, T-008
- **evidence_ref**: `validate_readme_feature_coverage.py` → framework paths only; `validate_project_readme_coverage.py` → project root; `--report` schema v1. `test_us0097_framework_validator_paths_reframed` + `test_us0097_project_readme_coverage_validator_contract` green.

### AC-7 — Release composition + scratchpad — `verdict=PASS`

- **Task**: T-005, T-006
- **evidence_ref**: Release **3g** after **3f**; `PROJECT_README_ENFORCE` / `FRAMEWORK_KIT_REPO` in scratchpad surfaces. Active scratchpad `FRAMEWORK_KIT_REPO=1` (kit repo); template example `FRAMEWORK_KIT_REPO=0`. `test_us0097_project_readme_enforce_scratchpad_keys` + `test_us0097_release_step3g_literals` green.

### AC-8 — Metadata hygiene (US-0071) — `verdict=PASS`

- **Task**: T-004
- **evidence_ref**: Execute step **23c** composes `check-user-visible-metadata.py`; checker exit 0 on QA run.

### AC-9 — Contract tests + template parity — `verdict=PASS`

- **Task**: T-009, T-010
- **evidence_ref**: Eight `test_us0097_*` subtests green (74 subtests); `check_intake_template_parity.py --scope=project-readme` → `[INTAKE_TEMPLATE_PARITY_OK]`; harness §26V registered; `PROJECT_README_PAIRS` (8 pairs).

### AC-10 — Architecture + runbook — `verdict=PASS`

- **Task**: T-011
- **evidence_ref**: `decisions/DEC-0083.md` + `docs/engineering/architecture.md` `# US-0097`; runbook § **Project README coverage validation (US-0097 / DEC-0083)** operator recipes table + troubleshooting.

## Generated baseline test evidence (US-0066 / DEC-0048)

- `generated_test_stack_profile`: python
- `generated_test_command`: `pytest -k us0097 tests/auto_command_contract_test.py -v`
- `generated_test_result`: pass
- `generated_test_output_ref`: 8 passed, 74 subtests (QA independent re-run)
- `generated_test_paths_ref`: `tests/auto_command_contract_test.py` (`test_us0097_*`)
- `generated_test_reason_code`: (none)

## Runtime proof (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260613-01`
- `runtime_proof_id=rp-auto-20260613-01-qa-qa-20260614T010000Z-S0087-US0097`
- `phase_id=qa`
- `role=qa`
- `proof_issued_at=2026-06-14T01:00:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=f6f5bff4992c8cd60c6126d7dc296dfefdbcd589009669bd28764bd3de09aea6`
- `fresh_context_marker=qa-S0087-US0097-qa-20260614T010000Z-fresh`
- Linkage to prior execute proof `rp-auto-20260613-01-execute-dev-20260614T000000Z-S0087-US0097` / `proof_hash=316906689073204289aecd65c0e6e71cb7efd4a42479b334b7727908c4f81ee9` via shared `orchestrator_run_id`, `story_id`, `sprint_id`.

Canonical payload: `{"orchestrator_run_id":"auto-20260613-01","phase_id":"qa","proof_issued_at":"2026-06-14T01:00:00Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260613-01-qa-qa-20260614T010000Z-S0087-US0097"}`.

## Isolation evidence (US-0048 / DEC-0029)

- `phase_id=qa`
- `role=qa`
- `fresh_context_marker=qa-S0087-US0097-qa-20260614T010000Z-fresh`
- `timestamp=2026-06-14T01:00:00Z`
- `evidence_ref=sprints/S0087/qa-findings.md,handoffs/qa_to_verify_work.md,handoffs/dev_to_qa.md,handoffs/resume_brief.md,docs/engineering/state.md,sprints/S0087/uat.json,sprints/S0087/uat.md,docs/product/backlog.md`

## Next phase

- **`/verify-work`** (fresh **qa**) for **`S0087`** / **`US-0097`**.
