# Release Notes — S0088 / US-0098 (dev environment auto-launch profile)

- **sprint_id**: S0088
- **story_refs**: US-0098
- **release_name**: `S0088 — US-0098 dev environment auto-launch profile`
- **release_date**: 2026-06-14T12:30:00Z
- **orchestrator_run_id**: auto-20260613-01
- **verdict**: **PASS**
- **binding_decision**: `DEC-0084` (composes US-0085 / US-0064 / US-0086 / US-0093)
- **research_anchor**: `R-0085`

## Summary

Ships a **default-off** scratchpad-gated dev auto-launch profile so **`/execute`** can detect dev runtime mode, persist an operator-seeded profile, run bounded rebuild/relaunch after implementation changes, and surface **Connect** blocks with names-only secret refs — composing with **US-0064**, **US-0085**, **US-0086**, and **US-0093** without reading **`.env`**.

## What's new

- **Default-off gate (AC-1)** — scratchpad **`DEV_AUTO_LAUNCH_PROFILE`** + **`DEV_ENVIRONMENT_CONFIG`**; zero overhead when **`off`**.
- **Profile schema v1 (AC-2)** — `template/.cursor/dev-environment.json.example`; gitignore/cursorignore for **`.cursor/dev-environment.json`**.
- **Detection matrix (AC-3)** — `local`, `docker-host-local`, `docker`, `ssh`; **US-0086** remote precedence over **docker-host-local**.
- **Execute step 24 (AC-4, AC-7)** — bounded relaunch **24a–24d** + **`refresh dev environment`** operator path; evidence tuple in **`dev_to_qa.md`**.
- **Connect surface (AC-5)** — `format_connect_block` mandatory fields; no inline secrets.
- **Composition (AC-6)** — **`release-targets.json`** schema unchanged; no **`.env`** reads.
- **Bounded safety (AC-8)** — **`DEV_ENV_PROFILE_*`** / **`DEV_ENV_RELAUNCH_*`** reason codes; retry caps.
- **Contract tests + parity (AC-9)** — eight **`test_us0098_*`** subtests; **`DEV_ENVIRONMENT_PAIRS`**; harness **§26W**.
- **Architecture + runbook (AC-10)** — **`DEC-0084`**, architecture **`# US-0098`**, runbook § **Dev environment auto-launch**.

## Non-goals (explicit)

- No replacement of **US-0064** connectivity schema or production deploy orchestration.
- No unbounded file-watch daemon in v1.
- No mandatory relaunch overhead when profile is **off**.

## Run

- **start_command**: `python scripts/dev_environment_lib.py --self-test` (profile off) or enable **`DEV_AUTO_LAUNCH_PROFILE=deterministic_v1`** per runbook
- **runtime_mode**: `local` (default kit-repo); `docker-host-local` / `docker` / `ssh` when profile enabled and detected
- **runtime_context_ref**: `docs/engineering/runbook.md` § **Dev environment auto-launch (US-0098 / DEC-0084)**; `docs/engineering/runtime-connectivity.md` Connect cross-link

## Connect

- **service_url**: from **`format_connect_block`** after successful relaunch (profile on); N/A when profile **off**
- **service_port**: from persisted profile / detection (names-only **`*Env`** refs)
- **health_endpoint**: from profile **`healthPath`** or stack defaults per runbook recipes

## Verify

1. `pytest -k us0098 tests/auto_command_contract_test.py -v` → expect **8 passed** (91 subtests).
2. `python scripts/dev_environment_lib.py --self-test` → expect `[DEV_ENVIRONMENT_SELF_TEST_OK]`.
3. `python scripts/check_intake_template_parity.py --scope=dev-environment` → expect `[INTAKE_TEMPLATE_PARITY_OK]`.
4. `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` → expect `[BUG_VALIDATION_OK]`.
5. Confirm execute step **24** literals in `.cursor/commands/execute.md` (active + template).
6. Confirm `sprints/S0088/qa-findings.md` **PASS** and `sprints/S0088/uat.json` **10/10 PASS**.
7. Confirm release-queue row **`S0088`** is **`released`** and backlog / acceptance show **`US-0098`** = **DONE** / checked.
8. **Operator E2E (UAT-10)**: follow runbook § **Dev environment auto-launch** operator recipes table (procedural attestation satisfied at verify-work per **BUG-0006**).

- **expected_health_signal**: Contract tests green; helper self-test OK; **`US-0098`** surfaces as **DONE** in backlog and checked in acceptance.

## Credentials

- Env-reference-only policy in effect. Profile JSON uses **`*Env`** name fields only; no inline secrets in git-tracked artifacts.

## Test evidence summary

- **Contract subtests**: `pytest -k us0098` → **8 passed**, 91 subtests (release gate re-run).
- **Helper self-test**: `[DEV_ENVIRONMENT_SELF_TEST_OK]`.
- **Template parity**: `[INTAKE_TEMPLATE_PARITY_OK]` scope=dev-environment.
- **Bug validator**: `[BUG_VALIDATION_OK]` pre- and post-release-write.
- **Metadata guard**: `check-user-visible-metadata.py` exit 0.
- **UAT**: **10/10 PASS** (`sprints/S0088/uat.json`); UAT-10 procedural attestation per runbook.

## Governance references

- **DEC-0084** — dev auto-launch profile, detection, execute relaunch, Connect surfacing.
- **`docs/engineering/architecture.md`** `# US-0098`.
- **`docs/engineering/research.md`** `R-0085`.
- **`decisions/DEC-0084.md`**.

## Known Issues

- None blocking release for in-scope **US-0098** / **DEC-0084** delivery.
- **readme_feature_coverage_3f**: post-**S0077** portfolio drift on **`its_magic/README.md`** family — live `--enforce` reports broad `coverage_missing`; kit-repo observation per **S0085**/**S0086**/**S0087** precedent (disjoint from **US-0098** closure).
- **Full harness**: 3 pre-existing **BUG-0009** CI-guard failures in `tests/run-tests.ps1` (809/25 baseline; non-blocking per QA/verify-work).

## Release gate summary

| gate | verdict |
|------|---------|
| check-in_test | pass (us0098 8/8; metadata guard harness rows) |
| qa | pass (no blockers) |
| uat | pass (10/10; UAT-10 procedural attestation) |
| isolation | pass (execute+qa+verify-work distinct markers; archive ref state-pack-20260613-h) |
| strict_proof | pass |
| parity | pass (scope=dev-environment) |
| bug_validate | pass |
| triad_check | pass (rollover units=6 pre-append) |
| readme_feature_coverage_3f | observation (post-S0077 drift) |
| project_readme_coverage_3g | pass (kit_repo_skipped) |
| publish | skipped (RELEASE_PUBLISH_MODE=disabled) |
| finalization | pass |

## Strict proof (release phase)

- `runtime_proof_id=rp-auto-20260613-01-release-release-20260614T123000Z-S0088-US0098`
- `proof_hash=be1986208496cb2ac1947b34f1b4cea458851f39c88146eb04ba85c8fd009dd5`
- `fresh_context_marker=release-S0088-US0098-release-20260614T123000Z-fresh`

## Sync / publish

- **Sync**: `SYNC_POLICY_MODE=disabled`, `ALLOW_AUTO_PUSH=1`; `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`.
- **Publish**: `RELEASE_PUBLISH_MODE=disabled` → `publish_snapshot=skipped_disabled` (deterministic no-op).

## Next phase

- **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio **0 OPEN** stories; backlog drain budget **8** remaining.
