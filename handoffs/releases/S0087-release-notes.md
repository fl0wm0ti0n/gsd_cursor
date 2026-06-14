# Release Notes — S0087 / US-0097 (project-owned root README bootstrap)

- **sprint_id**: S0087
- **story_refs**: US-0097
- **release_name**: `S0087 — US-0097 project-owned root README bootstrap`
- **release_date**: 2026-06-14T04:30:00Z
- **orchestrator_run_id**: auto-20260613-01
- **verdict**: **PASS**
- **binding_decision**: `DEC-0083` (amends `DEC-0045`; reframes `DEC-0074` paths)
- **research_anchor**: `R-0084`

## Summary

Completes the **US-0062** / **DEC-0045** ownership split: **`its_magic/README.md`** is the only installer-delivered **framework** catalog; **root `README.md`** is **project-owned** with bootstrap on first project story and mandatory per-story/sprint growth. **US-0091** framework coverage validates **`its_magic/`** paths only; new **`validate_project_readme_coverage.py`** + release step **3g** enforce project README coverage (default-on **`PROJECT_README_ENFORCE=1`**). Kit-repo exception via **`FRAMEWORK_KIT_REPO=1`** skips project enforce on the its-magic development repository.

## What's new

- **Installer boundary (AC-1)** — root **`README.md`** removed from installer manifest; framework README ships under **`its_magic/`** only.
- **Migration (AC-2)** — **M1–M5** reason codes + **S1–S5** placeholder sentinels; non-destructive upgrade path documented.
- **Bootstrap scaffold (AC-3)** — execute step **23a** materializes project README from **`docs/product/vision.md`** when missing/placeholder.
- **Per-story delta (AC-4)** — execute **23b** + release **3g** mandatory README growth; **`PROJECT_README_DELTA_SKIPPED`** fail-closed family.
- **Audience structure (AC-5)** — project scaffold `## For users` / `## For developers` / `## Features`; framework catalog confined to **`its_magic/README.md`**.
- **Gate separation (AC-6)** — split validators: framework (**US-0091**) vs project (**US-0097**).
- **Release composition (AC-7)** — release step **3g** after **3f**; scratchpad **`PROJECT_README_ENFORCE`** / **`FRAMEWORK_KIT_REPO`**.
- **Metadata hygiene (AC-8)** — execute **23c** composes **US-0071** guard on project README edits.
- **Contract tests + parity (AC-9)** — eight **`test_us0097_*`** subtests; **`--scope=project-readme`** parity (**`PROJECT_README_PAIRS`**).
- **Architecture + runbook (AC-10)** — **`DEC-0083`**, architecture **`# US-0097`**, runbook operator recipes + troubleshooting.

## Non-goals (explicit)

- No rewrite of **US-0094** framework intro in **`its_magic/README.md`** beyond parity moves.
- No replacement of **`docs/product/`** as canonical backlog.
- No mandatory historical framework catalog regeneration beyond installer boundary completion.

## Run

- **start_command**: `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"`
- **runtime_mode**: `local`
- **runtime_context_ref**: `docs/engineering/runbook.md` § **Project README coverage validation (US-0097 / DEC-0083)**

## Connect

- **service_url**: N/A (framework/toolkit repository; no running service)
- **service_port**: N/A
- **health_endpoint**: N/A

## Verify

1. `pytest -k us0097 tests/auto_command_contract_test.py -v` → expect **8 passed** (74 subtests).
2. `python scripts/validate_project_readme_coverage.py --self-test` → expect `[PROJECT_README_COVERAGE_SELF_TEST_OK]`.
3. `python scripts/check_intake_template_parity.py --scope=project-readme` → expect `[INTAKE_TEMPLATE_PARITY_OK]`.
4. `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` → expect `[BUG_VALIDATION_OK]`.
5. Confirm installer manifest excludes root **`README.md`** and retains **`its_magic`** (`docs/engineering/context/installer-owned-paths.manifest`).
6. Confirm `sprints/S0087/qa-findings.md` **PASS** and `sprints/S0087/uat.json` **10/10 PASS**.
7. Confirm release-queue row **`S0087`** is **`released`** and backlog / acceptance show **`US-0097`** = **DONE** / checked.
8. **Operator E2E (UAT-10)**: follow runbook § **Project README coverage validation** operator recipes table for consumer-repo bootstrap + enforce path (procedural attestation satisfied at verify-work per **BUG-0006**).

- **expected_health_signal**: Contract tests green; **`US-0097`** surfaces as **DONE** in backlog and checked in acceptance; project vs framework README gates separated.

## Credentials

- Env-reference-only policy in effect. No inline secrets in release artifacts.

## Test evidence summary

- **Contract subtests**: `pytest -k us0097` → **8 passed**, 74 subtests (release gate re-run).
- **Project validator**: `[PROJECT_README_COVERAGE_SELF_TEST_OK]`; release **3g** `--enforce` PASS (`kit_repo_skipped=true`).
- **Template parity**: `[INTAKE_TEMPLATE_PARITY_OK]` scope=project-readme.
- **Bug validator**: `[BUG_VALIDATION_OK]` pre- and post-release-write.
- **Metadata guard**: `check-user-visible-metadata.py` exit 0.
- **UAT**: **10/10 PASS** (`sprints/S0087/uat.json`); UAT-10 procedural attestation per runbook.

## Governance references

- **DEC-0083** — project vs framework README ownership + gates.
- **`docs/engineering/architecture.md`** `# US-0097`.
- **`docs/engineering/research.md`** `R-0084`.
- **`decisions/DEC-0083.md`**.

## Known Issues

- None blocking release for in-scope **US-0097** / **DEC-0083** delivery.
- **readme_feature_coverage_3f**: post-**S0077** portfolio drift on **`its_magic/README.md`** family — live `--enforce` reports broad `coverage_missing`; expected during kit-repo transition; classified as observation per **S0085**/**S0086** precedent (disjoint from **US-0097** closure).

## Release gate summary

| gate | verdict |
|------|---------|
| check-in_test | pass (us0097 8/8; metadata guard harness rows) |
| qa | pass (no blockers) |
| uat | pass (10/10; UAT-10 procedural attestation) |
| isolation | pass (execute+qa+verify-work distinct markers; archive ref state-pack-20260613-b) |
| strict_proof | pass |
| parity | pass (scope=project-readme) |
| bug_validate | pass |
| triad_check | pass (rollover units=5) |
| readme_feature_coverage_3f | observation (post-S0077 drift) |
| project_readme_coverage_3g | pass (kit_repo_skipped) |
| finalization | pass |

## Strict proof (release phase)

- `runtime_proof_id=rp-auto-20260613-01-release-release-20260614T043000Z-S0087-US0097`
- `proof_hash=008ad6a2f2d8c6dd7b1ee5c32145936445e9a33627ed3ed90dc545cc5d468530`
- `fresh_context_marker=release-S0087-US0097-release-20260614T043000Z-fresh`

## Sync / publish

- **Sync**: `SYNC_POLICY_MODE=disabled`, `ALLOW_AUTO_PUSH=1`; `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`.
- **Publish**: `RELEASE_PUBLISH_MODE=disabled` → `publish_snapshot=skipped_disabled` (deterministic no-op).

## Next phase

- **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio next OPEN **US-0098**; backlog drain budget **9** remaining.
