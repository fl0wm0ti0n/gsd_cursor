# Release Notes — S0089 / US-0099 (dev-environment profile install bootstrap)

- **sprint_id**: S0089
- **story_refs**: US-0099
- **release_name**: `S0089 — US-0099 auto-bootstrap dev-environment profile on install/upgrade`
- **release_date**: 2026-06-14T23:30:00Z
- **orchestrator_run_id**: auto-20260614-01
- **verdict**: **PASS**
- **binding_decision**: `DEC-0084` (amended § bootstrap posture)
- **research_anchor**: `R-0086`

## Summary

Ships **non-destructive auto-bootstrap** for the dev-environment profile: on **`missing`**, **`upgrade`**, and **npm `postinstall`**, copy **`template/.cursor/dev-environment.json.example`** → resolved profile path (**`.cursor/dev-environment.json`** by default, override via **`DEV_ENVIRONMENT_CONFIG`**) **only when absent** — never overwrite operator-customized profiles. Closes the gap after **US-0098** where **`DEV_ENV_PROFILE_MISSING`** blocked **`DEV_AUTO_LAUNCH_PROFILE=deterministic_v1`** until manual seeding.

## What's new

- **Copy-when-missing (AC-1)** — `bootstrap_dev_environment_profile_installer_hook` after scratchpad postinstall on missing + upgrade paths.
- **Never overwrite (AC-2)** — existence-only skip → **`DEV_ENV_BOOTSTRAP_SKIPPED_EXISTS`**; upgrade idempotent.
- **Path resolution (AC-3)** — `resolve_profile_path` + merged scratchpad **`DEV_ENVIRONMENT_CONFIG`**; **`DEV_ENV_BOOTSTRAP_PATH_INVALID`** fail-closed.
- **npm postinstall parity (AC-4)** — `bin/postinstall.js` consumer-repo detection + `spawnSync --bootstrap`.
- **Example source contract (AC-5)** — names-only template example; local profile gitignored (unchanged **DEC-0084** posture).
- **Runbook customize-after-bootstrap (AC-6)** — install-time bootstrap UX + **`DEV_ENV_BOOTSTRAP_*`** troubleshooting family.
- **Contract tests + parity (AC-7)** — seven **`test_us0099_*`** subtests; **`DEV_ENVIRONMENT_PAIRS`**; harness **§26X**.
- **Architecture + decision (AC-8)** — **`DEC-0084`** amended § bootstrap posture; architecture **`# US-0099`**; active + **`template/`** parity.

## Non-goals (explicit)

- No change to **DEC-0084** profile schema v1 or execute step **24** relaunch semantics.
- No default-on **`DEV_AUTO_LAUNCH_PROFILE`**.
- No **`.env`** reads to populate connect fields.

## Run

- **start_command**: `python installer.py upgrade` (or `missing`) — bootstrap runs automatically; manual probe: `python scripts/dev_environment_lib.py --bootstrap --target .cursor/dev-environment.json`
- **runtime_mode**: `local`
- **runtime_context_ref**: `docs/engineering/runbook.md` § **Install-time bootstrap (US-0099)**; `docs/engineering/runtime-connectivity.md` Connect cross-link when profile enabled

## Connect

- **service_url**: N/A at install bootstrap (profile seed only); when **`DEV_AUTO_LAUNCH_PROFILE=deterministic_v1`**, see **US-0098** Connect block after relaunch
- **service_port**: from persisted profile after customize (names-only **`*Env`** refs)
- **health_endpoint**: from profile **`healthPath`** or stack defaults per runbook recipes

## Verify

1. `pytest -k us0099 tests/auto_command_contract_test.py -v` → expect **7 passed** (10 subtests).
2. `python scripts/dev_environment_lib.py --self-test` → expect `[DEV_ENVIRONMENT_SELF_TEST_OK]`.
3. `python scripts/check_intake_template_parity.py --scope=dev-environment` → expect `[INTAKE_TEMPLATE_PARITY_OK]`.
4. `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` → expect `[BUG_VALIDATION_OK]`.
5. `python scripts/check-user-visible-metadata.py` → exit 0.
6. Confirm runbook § **Install-time bootstrap (US-0099)** in active + template mirrors.
7. Confirm `sprints/S0089/qa-findings.md` **PASS** and `sprints/S0089/uat.json` **8/8 PASS**.
8. Confirm release-queue row **`S0089`** is **`released`** and backlog / acceptance show **`US-0099`** = **DONE** / checked.
9. **Operator E2E (UAT-5/UAT-6/UAT-8)**: procedural attestation satisfied at verify-work per **BUG-0006** (manifest/runbook/architecture review).

- **expected_health_signal**: Contract tests green; helper self-test OK; **`US-0099`** surfaces as **DONE** in backlog and checked in acceptance.

## Credentials

- Env-reference-only policy in effect. Bootstrap copies names-only example JSON; no inline secrets in git-tracked artifacts.

## Test evidence summary

- **Contract subtests**: `pytest -k us0099` → **7 passed**, 10 subtests (release gate re-run).
- **Helper self-test**: `[DEV_ENVIRONMENT_SELF_TEST_OK]`.
- **Template parity**: `[INTAKE_TEMPLATE_PARITY_OK]` scope=dev-environment.
- **Bug validator**: `[BUG_VALIDATION_OK]` pre- and post-release-write.
- **Metadata guard**: `check-user-visible-metadata.py` exit 0 (B-001 closed).
- **UAT**: **8/8 PASS** (`sprints/S0089/uat.json`); UAT-5/UAT-6/UAT-8 procedural attestation per runbook.

## Governance references

- **DEC-0084** — amended § bootstrap posture + **`DEV_ENV_BOOTSTRAP_*`** reason family.
- **`docs/engineering/architecture.md`** `# US-0099`.
- **`docs/engineering/research.md`** `R-0086`.
- **`decisions/DEC-0084.md`**.

## Known Issues

- None blocking release for in-scope **US-0099** / **DEC-0084** bootstrap delivery.
- **readme_feature_coverage_3f**: post-**S0077** portfolio drift on **`its_magic/README.md`** family — live `--enforce` reports broad `coverage_missing`; kit-repo observation per **S0085**/**S0086**/**S0087**/**S0088** precedent (disjoint from **US-0099** closure).
- **Full harness**: 25 pre-existing failures in `tests/run-tests.ps1` (809/25 baseline @ `tests/report.md` Timestamp=2026-06-13T10:33:17Z; non-blocking per QA/verify-work).

## Release gate summary

| gate | verdict |
|------|---------|
| check-in_test | pass (us0099 7/7; metadata guard harness rows PASS) |
| qa | pass (no blockers; B-001 closed) |
| uat | pass (8/8; UAT-5/6/8 procedural attestation) |
| isolation | pass (execute+qa+verify-work distinct markers) |
| strict_proof | pass |
| parity | pass (scope=dev-environment) |
| bug_validate | pass |
| readme_feature_coverage_3f | observation (post-S0077 drift; kit-repo) |
| project_readme_coverage_3g | pass (kit_repo_skipped) |
| metadata_guard | pass |
| publish | skipped (RELEASE_PUBLISH_MODE=disabled) |
| finalization | pass |

## Strict proof (release phase)

- `runtime_proof_id=rp-auto-20260614-01-release-release-20260614T233000Z-S0089-US0099`
- `proof_hash=907a95ae387d71891aa3d7c86a9c39a164451f3a75966567d61344a3fba22cda`
- `fresh_context_marker=release-S0089-US0099-release-20260614T233000Z-fresh`

## Sync / publish

- **Sync**: `SYNC_POLICY_MODE=disabled`, `ALLOW_AUTO_PUSH=1`; `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`.
- **Publish**: `RELEASE_PUBLISH_MODE=disabled` → `publish_snapshot=skipped_disabled` (deterministic no-op).

## Next phase

- **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio **0 OPEN** stories; backlog drain budget **7** remaining.
