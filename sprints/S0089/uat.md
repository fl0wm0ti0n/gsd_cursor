# Sprint S0089 UAT — US-0099

- **Sprint**: `S0089`
- **Work item**: **US-0099** — Auto-bootstrap dev-environment profile on install/upgrade (non-destructive)
- **Governance**: **DEC-0084** (amended § bootstrap posture) + architecture `# US-0099` + **R-0086**
- **Orchestrator run**: **auto-20260614-01**
- **Implementation loop**: **1**
- **Machine-readable**: `sprints/S0089/uat.json`
- **Status**: **verified** (verify-work **2026-06-14T23:00:00Z** — release pending)
- **Canonical backlog**: **`docs/product/backlog.md`** — **US-0099** **OPEN**

## Metadata

- **author**: qa
- **qa_verdict_reference**: `sprints/S0089/qa-findings.md`
- **qa_timestamp**: 2026-06-14T22:00:00Z
- **fresh_context_marker**: qa-S0089-US0099-qa-20260614T220000Z-fresh
- **verify_work_executed_at**: `2026-06-14T23:00:00Z`
- **verify_work_fresh_context_marker**: `qa-S0089-US0099-verify-work-20260614T230000Z-fresh`
- **verify_work_verdict**: **PASS**

## Verdict summary

| Bucket | Count |
|--------|-------|
| PASS | 8 |
| FAIL | 0 |
| SKIP | 0 |
| PENDING | 0 |
| Total | 8 |

## UAT steps (AC-1..AC-8)

### UAT-1 — AC-1: Copy-when-missing on installer missing + upgrade

- **Command**: `pytest -k us0099_copy_when_missing tests/auto_command_contract_test.py -q`
- **Expected**: Absent profile → bootstrap copies example; installer hook after scratchpad postinstall on missing + upgrade
- **Result**: **PASS**
- **Evidence**: `test_us0099_copy_when_missing`, `test_us0099_installer_hook_literals`

### UAT-2 — AC-2: Never overwrite existing profile

- **Command**: `pytest -k 'us0099_skip or us0099_upgrade' tests/auto_command_contract_test.py -q`
- **Expected**: Pre-seed bytes unchanged; `DEV_ENV_BOOTSTRAP_SKIPPED_EXISTS` on second run
- **Result**: **PASS**
- **Evidence**: `test_us0099_skip_when_exists`, `test_us0099_upgrade_idempotent`

### UAT-3 — AC-3: Path resolution via DEV_ENVIRONMENT_CONFIG

- **Command**: `pytest -k us0099_path_override tests/auto_command_contract_test.py -q`
- **Expected**: Valid override copies; invalid → `DEV_ENV_BOOTSTRAP_PATH_INVALID`, no file
- **Result**: **PASS**
- **Evidence**: `test_us0099_path_override`

### UAT-4 — AC-4: npm postinstall parity

- **Command**: `pytest -k us0099_postinstall tests/auto_command_contract_test.py -q`
- **Expected**: `bin/postinstall.js` spawnSync `--bootstrap`; global skip when no consumer repo
- **Result**: **PASS**
- **Evidence**: `test_us0099_postinstall_parity`

### UAT-5 — AC-5: Example source contract

- **Command**: Manual — confirm `template/.cursor/dev-environment.json.example` source; no `install_paths` row
- **Expected**: Names-only example; local profile gitignored; no `.env` reads
- **Result**: **PASS**
- **Evidence**: architecture `# US-0099` § Contrast table; `installer-owned-paths.manifest` unchanged

### UAT-6 — AC-6: Runbook customize-after-bootstrap UX

- **Command**: Manual — runbook § install-time bootstrap (US-0099)
- **Expected**: Before/after table; customize-after-bootstrap; `DEV_ENV_PROFILE_MISSING` troubleshooting
- **Result**: **PASS**
- **Evidence**: `docs/engineering/runbook.md` + template mirror

### UAT-7 — AC-7: Contract tests + parity + harness

- **Command**: `pytest -k us0099 tests/auto_command_contract_test.py -q` + parity `--scope=dev-environment`
- **Expected**: Seven `test_us0099_*` green; `DEV_ENVIRONMENT_PAIRS` unchanged; harness §26X
- **Result**: **PASS**
- **Evidence**: 7/7 subtests; `[INTAKE_TEMPLATE_PARITY_OK]`; `tests/run-tests.ps1` §26X

### UAT-8 — AC-8: Architecture + decision

- **Command**: Manual — `decisions/DEC-0084.md` + architecture `# US-0099`
- **Expected**: Hook placement, reason codes, idempotency matrix; plan-verify AC-8 attestation
- **Result**: **PASS**
- **Evidence**: `sprints/S0089/plan-verify.json`

## AC ↔ UAT results summary

AC-1..AC-8 verified at verify-work via UAT-1..UAT-8 (all PASS). UAT-5, UAT-6, UAT-8 satisfied via **procedural attestation** (documentation/manifest review in fresh QA subagent per **BUG-0006**).

## Next

- **`/release`** (fresh **release**) for **`S0089`** / **`US-0099`**
