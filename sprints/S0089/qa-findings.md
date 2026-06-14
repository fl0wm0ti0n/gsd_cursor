# QA Findings — S0089 / US-0099

## Metadata

- **sprint_id**: S0089
- **story_id**: US-0099
- **dec_id**: DEC-0084 (amended § bootstrap posture)
- **research_anchor**: R-0086
- **role**: qa
- **timestamp**: 2026-06-14T22:00:00Z
- **orchestrator_run_id**: auto-20260614-01
- **implementation_loop_index**: 1
- **fresh_context_marker**: qa-S0089-US0099-qa-20260614T220000Z-fresh
- **inputs_reviewed**: `handoffs/dev_to_qa.md` (remediation section), `sprints/S0089/tasks.md`, `sprints/S0089/summary.md`, `sprints/S0089/plan-verify.json`, `docs/product/backlog.md` `## US-0099`, `decisions/DEC-0084.md`, `docs/engineering/architecture.md` `# US-0099`, `docs/engineering/runbook.md`, `scripts/dev_environment_lib.py`, `installer.py`, `bin/postinstall.js`, `scripts/check_intake_template_parity.py`, `tests/auto_command_contract_test.py`

## Overall verdict

**PASS** — All eight story ACs (AC-1..AC-8) satisfied on independent QA re-run after B-001 remediation; seven `test_us0099_*` contract subtests green (10 subtests); `dev_environment_lib.py --self-test` OK; template parity `--scope=dev-environment` OK; `python scripts/check-user-visible-metadata.py` exit **0** (B-001 closed). Story **US-0099** remains **OPEN** per **US-0045** (closure at `/release`).

- `ac_coverage`: AC-1..AC-8 = 8/8 PASS
- `regressions_found`: **none attributable to US-0099**
- `parity_verified`: true (`check_intake_template_parity.py --scope=dev-environment` → `[INTAKE_TEMPLATE_PARITY_OK]`)
- `decision_gate_posture`: none required
- `blocking_findings`: **none** (B-001 remediated and verified)

### Prior blocking finding — closed

| ID | Severity | Reason code | Remediation status | Evidence |
|----|----------|-------------|-------------------|----------|
| B-001 | blocking (closed) | `USER_VISIBLE_INTERNAL_METADATA_DETECTED` | **CLOSED** — `installer.py:378` docstring now neutral prose (`Non-destructive dev-environment profile bootstrap.`); metadata guard exit 0 | `handoffs/dev_to_qa.md` remediation section; QA re-run `check-user-visible-metadata.py` |

## Test plan

| Step | Command / check | Expected | Result |
|------|-----------------|----------|--------|
| 1 | `pytest -k us0099 tests/auto_command_contract_test.py -q` | 7 passed | **PASS** (7 passed, 10 subtests) |
| 2 | `python scripts/dev_environment_lib.py --self-test` | `[DEV_ENVIRONMENT_SELF_TEST_OK]` | **PASS** |
| 3 | `python scripts/check_intake_template_parity.py --scope=dev-environment` | `[INTAKE_TEMPLATE_PARITY_OK]` | **PASS** |
| 4 | `python scripts/check-user-visible-metadata.py` | exit 0 | **PASS** (B-001 closed) |
| 5 | Manual: installer hook order | after `run_scratchpad_postinstall`, before `bootstrap_runbook_commands` on missing + upgrade | **PASS** (`test_us0099_installer_hook_literals`) |
| 6 | Manual: runbook § install-time bootstrap | customize-after-bootstrap UX + `DEV_ENV_BOOTSTRAP_*` troubleshooting | **PASS** |
| 7 | Manual: dev_to_qa evidence tuple | profile off → `DEV_ENV_RELAUNCH_SKIPPED_PROFILE_OFF` | **PASS** |
| 8 | `LINT_COMMAND` | skipped (blank in runbook) | **skipped** |
| 9 | `TYPECHECK_COMMAND` | skipped (blank in runbook) | **skipped** |
| 10 | Bug validator | N/A (story scope, not bug) | **skipped** |

## Per-AC verdicts (AC-1..AC-8)

### AC-1 — Copy-when-missing on installer missing + upgrade — `verdict=PASS`

- **Task**: T-001, T-002, T-005
- **evidence_ref**: `bootstrap_dev_environment_profile` + `bootstrap_dev_environment_profile_installer_hook`; `test_us0099_copy_when_missing`, `test_us0099_installer_hook_literals` green.

### AC-2 — Never overwrite existing profile — `verdict=PASS`

- **Task**: T-002, T-006
- **evidence_ref**: Existence-only skip → `DEV_ENV_BOOTSTRAP_SKIPPED_EXISTS`. `test_us0099_skip_when_exists`, `test_us0099_upgrade_idempotent` green.

### AC-3 — Path resolution via DEV_ENVIRONMENT_CONFIG — `verdict=PASS`

- **Task**: T-001, T-006
- **evidence_ref**: `resolve_profile_path` + override validation. `test_us0099_path_override` green (valid copy + invalid → `PATH_INVALID`).

### AC-4 — npm postinstall parity — `verdict=PASS`

- **Task**: T-003
- **evidence_ref**: `bin/postinstall.js` `--bootstrap` + `spawnSync` + `dev_environment_lib.py` literals + global skip token. `test_us0099_postinstall_parity` green.

### AC-5 — Example source contract (names-only; gitignored local) — `verdict=PASS`

- **Task**: T-001
- **evidence_ref**: Source `template/.cursor/dev-environment.json.example` only; local profile not in `install_paths` manifest; contrast table in architecture § AC-5. No `.env` reads in bootstrap path.

### AC-6 — Runbook customize-after-bootstrap UX — `verdict=PASS`

- **Task**: T-004
- **evidence_ref**: Runbook § install-time bootstrap (US-0099): before/after table, customize-after-bootstrap, `DEV_ENV_PROFILE_MISSING` troubleshooting, `DEV_ENV_BOOTSTRAP_*` reason codes. Active + template mirror parity OK.

### AC-7 — Seven test_us0099_* + parity + harness §26X — `verdict=PASS`

- **Task**: T-005, T-006, T-007, T-008, T-009
- **evidence_ref**: Seven `test_us0099_*` subtests green; four `DEV_ENV_BOOTSTRAP_*` inventory; harness **§26X** in `tests/run-tests.ps1` / `tests/run-tests.sh`; `DEV_ENVIRONMENT_PAIRS` rows 1–8 unchanged.

### AC-8 — Architecture + decision — `verdict=PASS`

- **Task**: *(pre-satisfied at `/architecture`)*
- **evidence_ref**: `decisions/DEC-0084.md` amended § bootstrap posture; `docs/engineering/architecture.md` `# US-0099`; `sprints/S0089/plan-verify.json` AC-8 attestation.

## Dev environment relaunch evidence (step 24 — profile off this phase)

| Field | Value |
|-------|-------|
| `dev_auto_launch_profile` | `off` |
| `runtime_mode` | `(skipped)` |
| `relaunch_tier` | `(none)` |
| `relaunch_outcome` | `skipped` |
| `retry_count` | `0` |
| `reason_code` | `DEV_ENV_RELAUNCH_SKIPPED_PROFILE_OFF` |

## Generated baseline test evidence (US-0066 / DEC-0048)

- `generated_test_stack_profile`: python
- `generated_test_command`: `pytest -k us0099 tests/auto_command_contract_test.py -q`
- `generated_test_result`: pass
- `generated_test_output_ref`: 7 passed, 10 subtests (QA independent re-run post-remediation)
- `generated_test_paths_ref`: `tests/auto_command_contract_test.py` (`test_us0099_*`)
- `generated_test_reason_code`: (none)

## Runtime QA evidence (US-0065 — N/A for bootstrap-only story)

- `runtime_startup_command`: (N/A — install-time bootstrap; no app runtime)
- `runtime_stack_profile`: python
- `runtime_mode`: local
- `runtime_health_target`: (N/A)
- `runtime_health_result`: (skipped — bootstrap contract only)
- `runtime_log_summary`: (N/A)
- `runtime_retry_count`: 0
- `runtime_retry_ledger`: []
- `runtime_final_verdict`: pass (contract scope)
- `runtime_reason_code`: (none)
- `runtime_evidence_refs`: `handoffs/dev_to_qa.md` (DEV_ENV_RELAUNCH_SKIPPED_PROFILE_OFF)

## Runtime proof (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260614-01`
- `runtime_proof_id=rp-auto-20260614-01-qa-qa-20260614T220000Z-S0089-US0099`
- `phase_id=qa`
- `role=qa`
- `proof_issued_at=2026-06-14T22:00:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=b1b36e6effff9026c0b837908758a63bc53ccb92e13606aae70b0d6fde94014c`
- `fresh_context_marker=qa-S0089-US0099-qa-20260614T220000Z-fresh`

Canonical payload: `{"orchestrator_run_id":"auto-20260614-01","phase_id":"qa","proof_issued_at":"2026-06-14T22:00:00Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260614-01-qa-qa-20260614T220000Z-S0089-US0099"}`.

## Next

- **`/verify-work`** (fresh **qa**) for **`S0089`** / **`US-0099`** — independent UAT re-run and closure preflight.
