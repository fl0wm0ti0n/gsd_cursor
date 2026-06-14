# Sprint S0089

## Metadata

- **sprint_id**: S0089
- **story_refs**: US-0099
- **goal**: Ship **non-destructive dev-environment profile auto-bootstrap** on install/upgrade/postinstall — **`bootstrap_dev_environment_profile()`** + **`--bootstrap`** CLI with four **`DEV_ENV_BOOTSTRAP_*`** reason codes, **`installer.py`** hook after **`run_scratchpad_postinstall`**, **`bin/postinstall.js`** subprocess parity, runbook **customize-after-bootstrap** UX, seven **`test_us0099_*`** contract markers, harness **§26X**, and **`DEV_ENVIRONMENT_PAIRS`** parity verification — per **DEC-0084** amended § bootstrap posture (composes **US-0098** / **US-0018** / **US-0085**; research **R-0086**).
- **status**: planned
- **created_at**: 2026-06-14T18:00:00Z
- **orchestrator_run_id**: auto-20260614-01
- **fresh_context_marker**: tl-S0089-US0099-sprint-plan-20260614T180000Z-fresh

## Scope

- **US-0099**: Auto-bootstrap dev-environment profile on install/upgrade (non-destructive copy-when-missing)
- **Architecture**: `docs/engineering/architecture.md` `# US-0099`
- **Binding decision**: `decisions/DEC-0084.md` (amended § bootstrap posture — no new DEC)
- **Research anchor**: `docs/engineering/research.md` `R-0086`

## Non-goals (hard, from DEC-0084 / architecture `# US-0099`)

- No profile schema v1 change — **US-0098** / **DEC-0084** §2 unchanged.
- No execute step **24** semantic change.
- No overwrite of operator-customized profiles — existence-only skip.
- No auto-enable **`DEV_AUTO_LAUNCH_PROFILE`** — default-off gate unchanged.
- No bootstrap for **`.cursor/remote.json`** — manual seed remains.
- No **`.env`** reads to populate connect fields — **US-0085** inheritance.
- No new **`install_paths`** manifest row for local profile — runtime copy only.
- **Status authority (US-0045)**: US-0099 stays **OPEN** throughout this sprint; closure at `/release`.

## Dependencies

- **Upstream (locked)**: **DEC-0084** amended; architecture `# US-0099`; research **R-0086**
- **Governance stack**: **US-0098** (schema v1 + execute step **24** delivered), **US-0018** (smart upgrade compose), **US-0085** (names-only example), **US-0062** (installer manifest boundary), **US-0017** (template parity), **US-0045** (status authority), **US-0048** / **DEC-0029** (isolation), **US-0056** / **DEC-0038** (strict proof), **DEC-0080** / **DEC-0081** (native chain compose)

## Acceptance criteria coverage (AC-1..AC-8 → T-xxx; surjective, 9 tasks / 8 ACs)

| AC | Description (summary) | Task(s) | Architecture anchor |
|----|-----------------------|---------|---------------------|
| AC-1 | Copy-when-missing on installer **`missing`** + **`upgrade`** | T-001, T-002, T-005 | § Hook placement; § Stdlib helper |
| AC-2 | Never overwrite existing profile | T-002, T-006 | § Path resolution; § Idempotency matrix |
| AC-3 | Path resolution via **`DEV_ENVIRONMENT_CONFIG`** | T-001, T-006 | § Path resolution; § Reason codes |
| AC-4 | npm postinstall parity | T-003 | § Hook placement (**postinstall.js**) |
| AC-5 | Example source contract (names-only; gitignored local) | T-001 | § Overview; § Contrast table |
| AC-6 | Runbook customize-after-bootstrap UX | T-004 | § Runbook operator UX delta |
| AC-7 | Seven **`test_us0099_*`** + parity + harness | T-005, T-006, T-007, T-008, T-009 | § Contract tests + parity |
| AC-8 | Architecture + decision | *(pre-satisfied at `/architecture`)* | **`DEC-0084`** amended; `# US-0099`; plan-verify attestation |

**Multi-AC tasks** (justified by architecture `# US-0099` § Atomic task seeds): **T-001** (AC-1+AC-3+AC-5), **T-002** (AC-1+AC-2), **T-005** (AC-1+AC-7), **T-006** (AC-2+AC-3+AC-7), **T-007** (AC-7). Every AC has ≥1 task or architecture-phase attestation; no `PLAN_AC_COVERAGE_GAP`. **AC-8** pre-satisfied at architecture — no dev task seed per architecture § AC traceability.

## Task count

- **Total**: 9
- **SPRINT_MAX_TASKS**: 12 (from merged scratchpad)
- **Within limit**: yes (9 ≤ 12; `SPRINT_AUTO_SPLIT` not triggered)
- **Coverage**: surjective AC-1..AC-8 coverage; **strict 1:1 task-to-seed** (9 architecture seeds → T-001..T-009); **not** strict AC bijection (multi-AC tasks above; AC-8 architecture-phase only)

## Governance

- **DEC-0084** (binding, amended § bootstrap posture) — each task cites governing architecture §(s) and DEC §(s).
- **R-0086** (research anchor).
- **US-0085** inheritance — copied example remains names-only; no secret materialization.
- **US-0045** canonical status authority (US-0099 stays OPEN through this sprint).

## Edit surfaces and parity plan

| # | Active path | Template path | Task | Parity |
|---|-------------|---------------|------|--------|
| 1 | `scripts/dev_environment_lib.py` | `template/scripts/dev_environment_lib.py` | T-001 | Positive |
| 2 | `installer.py` | (active-only — contract literals) | T-002 | N/A |
| 3 | `bin/postinstall.js` | (active-only — contract literals) | T-003 | N/A |
| 4 | `docs/engineering/runbook.md` | `template/docs/engineering/runbook.md` | T-004 | Positive |
| 5 | `tests/auto_command_contract_test.py` | (active-only) | T-005, T-006, T-007 | N/A |
| 6 | `tests/run-tests.ps1` / `tests/run-tests.sh` | (active-only) | T-008 | Harness **§26X** |
| 7 | `scripts/check_intake_template_parity.py` | `template/scripts/check_intake_template_parity.py` | T-009 | Positive |

**NEGATIVE parity (MUST NOT violate)**:

- Do **not** change profile schema v1 or execute step **24** semantics.
- Do **not** overwrite existing profile files on upgrade or re-run.
- Do **not** add local profile to **`install_paths`** manifest.
- Do **not** auto-enable **`DEV_AUTO_LAUNCH_PROFILE`**.
- Do **not** bootstrap **`.cursor/remote.json`**.
- Do **not** read **`.env`** during bootstrap.

## Post-edit gate sequence (architecture § Contract tests)

1. `pytest -k us0099 tests/auto_command_contract_test.py` → all seven subtests green
2. `python scripts/check_intake_template_parity.py --scope=dev-environment` → PASS (**`DEV_ENVIRONMENT_PAIRS`** unchanged)

## Test strategy summary (strategy locked for /execute; no test code in sprint-plan)

### Tranche A — stdlib helper + bootstrap CLI (T-001)

- **`bootstrap_dev_environment_profile`**, **`resolve_profile_path`**, four **`DEV_ENV_BOOTSTRAP_*`** constants
- **`--bootstrap`** / **`--target`** / **`--source-root`** CLI + log tokens

### Tranche B — installer hook (T-002)

- **`bootstrap_dev_environment_profile_installer_hook`** after **`run_scratchpad_postinstall`**, before **`bootstrap_runbook_commands`** on **`missing`** + **`upgrade`**

### Tranche C — postinstall parity (T-003)

- **`bin/postinstall.js`**: repo-root walk + **`spawnSync`** **`--bootstrap`** subprocess

### Tranche D — runbook + tests + harness + parity (T-004..T-009)

- Runbook customize-after-bootstrap + **`DEV_ENV_PROFILE_MISSING`** troubleshooting
- Seven **`test_us0099_*`** contract subtests; harness **§26X**; parity sweep

## Risks and mitigations (architecture § Risks)

| ID | Risk | Sprint guard |
|----|------|--------------|
| R1 | Global-install / wrong cwd | T-003 **`[DEV_ENV_BOOTSTRAP_SKIP]`** path; runbook edge-case note |
| R2 | Accidental overwrite on upgrade | T-001 existence-only skip; T-006 **`test_us0099_skip_when_exists`** + T-005 **`test_us0099_upgrade_idempotent`** |
| R3 | User-visible logs leak planning ids | **DEC-0053** scan on bootstrap tokens in T-001 |
| R4 | Postinstall without merged scratchpad | T-001 helper reads disk layers; default path when unset |

## Definition of done (sprint-plan → plan-verify → execute → qa → verify-work → release)

- All 8 acceptance criteria covered surjectively (AC-8 attested at plan-verify from architecture phase).
- `sprints/S0089/plan-verify.json` reaches **PASS** with `plan_integrity.ac_coverage_surjective=true`, `task_count=9`, `within_limit=true`.
- `pytest -k us0099` green; parity **`--scope=dev-environment`** PASS.
- `docs/product/backlog.md` **`## US-0099`** retains **OPEN** through plan-verify / execute / qa / verify-work; closure at `/release`.

## Next

- **`/plan-verify`** (fresh **qa**) for **`S0089`** / **US-0099** — verify AC-1..AC-8 ↔ T-001..T-009 surjective coverage, task-seed bijection (9 seeds → 9 tasks), task-count bound, governance alignment. Target: `sprints/S0089/plan-verify.json` `status` **`PENDING`** → **`PASS`**.
