# Release Notes — S0106 / US-0106

**Sprint**: S0106  
**Story**: US-0106 — Sovereign Role-Behavior Manifest (P2)  
**Release date**: 2026-06-29  
**Decision**: DEC-0106 (locked)  
**Research**: R-0095 (closed, Q1–Q7 answered)  
**Orchestrator run**: auto-20260628-04  
**Status**: RELEASED

## Summary

Sprint S0106 delivers the sovereign role-behavior manifest capability: a single YAML file (`.cursor/sovereign-role-manifest.yaml`) declaring per-role objective functions, inter-role review obligations as a directed graph, self-override allowances, cross-model policy composition with US-0104, and escalation rules composition with US-0107. Default-off (`SOVEREIGN_ROLE_MANIFEST=0`) for zero overhead when disabled.

## Tasks Delivered (11/11)

| Task | Description | Status |
|------|-------------|--------|
| T-001 | Scratchpad keys + reason codes | DELIVERED |
| T-002 | YAML manifest v1 schema + bootstrap example | DELIVERED |
| T-003 | Validator CLI (`sovereign_role_manifest_validate.py`) + template mirror | DELIVERED |
| T-004 | Objective injection (`build_objective_injection_block`) | DELIVERED |
| T-005 | Review dispatch + `sovereign_role_reviews.jsonl` | DELIVERED |
| T-006 | `cross_model_policy` compose US-0104 | DELIVERED |
| T-007 | Contract tests (8 `test_us0106_*`) + parity scope | DELIVERED |
| T-008 | Architecture `# US-0106` + reason codes | DELIVERED |
| T-009 | Runbook operator recipe | DELIVERED |
| T-010 | Compose regression guards (US-0069, US-0104) | DELIVERED |
| T-011 | Template byte-parity mirrors | DELIVERED |

## Acceptance Criteria (8/8)

| AC | Description | Satisfied |
|----|-------------|-----------|
| AC-1 | Scratchpad keys + zero-overhead default | YES |
| AC-2 | Manifest v1 schema + bootstrap graph | YES |
| AC-3 | Validator CLI + fail-closed | YES |
| AC-4 | Objective injection char-capped | YES |
| AC-5 | Cross-role review dispatch + JSONL | YES |
| AC-6 | `cross_model_policy` compose US-0104 | YES |
| AC-7 | 8 contract tests + parity scope | YES |
| AC-8 | Architecture, runbook, compose guards | YES |

## Gate Chain

- check-in_test: **PASS** (us0106 8/8)
- qa: **PASS** (0 blockers; 8/8 ACs)
- verify-work: **PASS** (8/8 ACs verified)
- uat: **SKIPPED** (verify-work primary gate per DEC-0106)
- isolation: **PASS** (distinct execute + qa + verify-work markers)
- parity: **PASS** (`--scope=sovereign-role-manifest` pairs=4)
- compose_regression: **PASS** (US-0069 matrix unchanged, US-0104 unchanged)
- publish: **SKIPPED** (`RELEASE_PUBLISH_MODE=disabled`)

## Test Evidence

- **Contract tests**: 8/8 PASS (`pytest tests/us0106_contract_test.py -v`)
- **Self-tests**: `[SOVEREIGN_ROLE_MANIFEST_SELF_TEST_OK]`, `[SOVEREIGN_ROLE_MANIFEST_VALIDATION_OK]`
- **Parity**: `[INTAKE_TEMPLATE_PARITY_OK]` scope=sovereign-role-manifest pairs=4

## Release Artifacts

- `.cursor/sovereign-role-manifest.yaml` — manifest YAML (v1 schema)
- `.cursor/rules/sovereign-role-manifest.mdc` — rule enforcing contract
- `scripts/sovereign_role_manifest_lib.py` — lib (load, validate, resolve, dispatch)
- `scripts/sovereign_role_manifest_validate.py` — validator CLI
- `tests/us0106_contract_test.py` — 8 contract tests
- `handoffs/sovereign_role_reviews.jsonl` — review dispatch ledger
- `decisions/DEC-0106.md` — binding decision (locked)
- `docs/engineering/runbook.md` — operator recipe § US-0106

## Compose Guards

- US-0069 phase→role matrix: **unchanged**
- US-0104 critic schema: **unchanged**
- US-0103 ledger schema: **unchanged**
- US-0105 memory schema: **unchanged**
- US-0107 deferral schema: **unchanged**

## Operator Hints

### Run
- `start_command`: manifest is read at subagent spawn when `SOVEREIGN_ROLE_MANIFEST=1`
- `runtime_mode`: local
- `runtime_context_ref`: N/A (framework kit repo)

### Connect
- `service_url`: N/A (framework kit repo)
- `service_port`: N/A
- `health_endpoint`: N/A

### Verify
1. `python scripts/sovereign_role_manifest_validate.py --self-test`
2. `pytest tests/us0106_contract_test.py -v`
3. `python scripts/check_intake_template_parity.py --scope sovereign-role-manifest`

### Credentials
- No credentials required.

### Known Issues
- None.

## Evidence References

- `handoffs/releases/S0106-release-notes.md`
- `sprints/S0106/release-findings.md`
- `sprints/S0106/verify-work-verdict.json`
- `sprints/S0106/qa-verdict.json`
- `decisions/DEC-0106.md`
- `docs/engineering/architecture.md` § US-0106
- `.cursor/sovereign-role-manifest.yaml`
- `scripts/sovereign_role_manifest_lib.py`
- `scripts/sovereign_role_manifest_validate.py`
- `tests/us0106_contract_test.py`
