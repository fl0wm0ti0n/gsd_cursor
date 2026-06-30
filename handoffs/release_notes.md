# Release Notes (Legacy Compatibility Pointer)

This file remains backward-compatible for workflows that read
`handoffs/release_notes.md` as the latest release summary.

Canonical sprint history now lives under:
- `handoffs/releases/Sxxxx-release-notes.md`

Canonical queue state now lives under:
- `handoffs/release_queue.md`

---

## Release finalized note (S0112)

- Sprint: `S0112`
- Story: `US-0112` (Ship model-catalog example presets on install/upgrade — DEC-0112)
- Release: **finalized** (`2026-06-30T23:40:00Z`, `orchestrator_run_id=auto-20260628-04`, `fresh_context_marker=release-S0112-US0112-20260630T234000Z-fresh`)
- Queue: **`handoffs/release_queue.md`** row **`S0112`** = **`released`**
- **Run / verify:** `pytest tests/us0112_contract_test.py -v` -> 12 passed; see **`handoffs/releases/S0112-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=disabled`** -- deterministic no-op (`publish_snapshot=skipped_disabled`)
- Sync (**DEC-0018**): **`SYNC_POLICY_MODE=disabled`** -> **`push_decision=not_eligible`**, **`reason_code=SYNC_DISABLED`**
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio **0** OPEN stories remaining

## Release finalized note (S0111)

- Sprint: `S0111`
- Story: `US-0111` (Release Trigger-Driven Version Changelog Derivation — DEC-0111)
- Release: **finalized** (`2026-06-30T19:45:00Z`, `orchestrator_run_id=auto-20260628-04`, `fresh_context_marker=release-S0111-US0111-auto-20260628-04-20260630T194500Z`)
- Queue: **`handoffs/release_queue.md`** row **`S0111`** = **`released`**
- **Run / verify:** `pytest tests/us0111_contract_test.py -v` -> 12 passed; `python scripts/release_trigger_adapters.py --self-test` -> `[RELEASE_TRIGGER_SELF_TEST_OK]`; see **`handoffs/releases/S0111-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=disabled`** -- deterministic no-op (`publish_snapshot=skipped_disabled`)
- Sync (**DEC-0018**): **`SYNC_POLICY_MODE=disabled`** -> **`push_decision=not_eligible`**, **`reason_code=SYNC_DISABLED`**
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio **1** OPEN story remaining (US-0112)

## Release finalized note (S0109)

## Release finalized note (S0109)

- Sprint: `S0109`
- Story: `US-0109` (Self-Healing Deploy Loop -- DEC-0109)
- Release: **finalized** (`2026-06-30T03:00:00Z`, `orchestrator_run_id=auto-20260628-04`, `fresh_context_marker=release-S0109-US0109-auto-20260628-04-20260630T030000Z`)
- Queue: **`handoffs/release_queue.md`** row **`S0109`** = **`released`**
- **Run / verify:** `pytest tests/us0109_contract_test.py -v` -> 11 passed; `python scripts/self_healing_deploy_validate.py --self-test` -> `[SELF_HEALING_DEPLOY_VALIDATION_OK]`; see **`handoffs/releases/S0109-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=disabled`** -- deterministic no-op (`publish_snapshot=skipped_disabled`)
- Sync (**DEC-0018**): **`SYNC_POLICY_MODE=disabled`** -> **`push_decision=not_eligible`**, **`reason_code=SYNC_DISABLED`**
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio **2** OPEN stories remaining (US-0111, US-0112)

## Release finalized note (S0107)

- Sprint: `S0107`
- Story: `US-0107` (Sovereign Loop Mode / AUTO_SOVEREIGN — DEC-0107)
- Release: **finalized** (`2026-06-29T00:23:00Z`, `orchestrator_run_id=auto-20260628-04`, `fresh_context_marker=release-S0107-20260629T002300Z-fresh`)
- Queue: **`handoffs/release_queue.md`** row **`S0107`** = **`released`**
- **Run / verify:** `pytest tests/us0109_contract_test.py -v` → 10 passed; `python scripts/sovereign_loop_lib.py --self-test` → `[SOVEREIGN_LOOP_SELF_TEST_OK]`; see **`handoffs/releases/S0107-release-notes.md`** **## Run** / **## Verify**
- Changelog: step **19** appended **US-0107** under **`CHANGELOG.md`** **`[Unreleased]`** (workflow-only; no semver)
- Publish: **`RELEASE_PUBLISH_MODE=disabled`** — deterministic no-op (`publish_snapshot=skipped_disabled`)
- Sync (**DEC-0018**): **`SYNC_POLICY_MODE=disabled`** → **`push_decision=not_eligible`**, **`reason_code=SYNC_DISABLED`**
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio **5** OPEN stories remaining (US-0106, US-0108, US-0109, US-0111, US-0112)

## Release finalized note (S0092)

- Sprint: `S0092`
- Story: `US-0102` (direct per-phase model slug override + role-based catalog presets — DEC-0087 / composes DEC-0086)
- Release: **finalized** (`2026-06-26T00:00:00Z`, `orchestrator_run_id=auto-20260615-02`, strict proof `proof_hash=18d3bed52733e0325eac9068b5aa61f07a97153791217d1e23e4e62663e0b858`)
- Queue: **`handoffs/release_queue.md`** row **`S0092`** = **`released`**
- **Run / verify:** `pytest -k us0102 tests/auto_command_contract_test.py -v` → 8 passed; `python scripts/model_tier_validate.py --repo .` → `[MODEL_TIER_VALIDATION_OK]`; see **`handoffs/releases/S0092-release-notes.md`** **## Run** / **## Verify**
- Changelog: step **19** appended **US-0102** under **`CHANGELOG.md`** **`[Unreleased]`** (workflow-only; no semver)
- Publish: **`RELEASE_PUBLISH_MODE=disabled`** — deterministic no-op (`publish_snapshot=skipped_disabled`)
- Sync (**DEC-0018**): **`SYNC_POLICY_MODE=disabled`** → **`push_decision=not_eligible`**, **`reason_code=SYNC_DISABLED`**
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio **0 OPEN** stories; backlog drain budget **4** remaining

## Release finalized note (S0090)

- Sprint: `S0090`
- Story: `US-0100` (version-scoped release changelog + GitHub `-F` attachment — DEC-0085 / R-0087)
- Release: **finalized** (`2026-06-15T08:00:00Z`, `orchestrator_run_id=auto-20260615-01`, strict proof `proof_hash=92e55de82e4089435f4a6b3229e3233bbc2a4c4fd4aca5675313b8d7638d1d85`)
- Queue: **`handoffs/release_queue.md`** row **`S0090`** = **`released`**
- **Run / verify:** `pytest -k us0100 tests/auto_command_contract_test.py -v` → 10 passed; `python scripts/release_changelog_validate.py --repo .` → exit 0 warn (enforce notes legacy semver rows pending backfill); see **`handoffs/releases/S0090-release-notes.md`** **## Run** / **## Verify**
- Changelog: step **19** appended **US-0100** under **`CHANGELOG.md`** **`[Unreleased]`** (workflow-only; no semver)
- Publish: **`RELEASE_PUBLISH_MODE=disabled`** — deterministic no-op (`publish_snapshot=skipped_disabled`)
- Sync (**DEC-0018**): **`SYNC_POLICY_MODE=disabled`** → **`push_decision=not_eligible`**, **`reason_code=SYNC_DISABLED`**
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio **0 OPEN** stories; backlog drain budget **6** remaining

## Release finalized note (S0089)

- Sprint: `S0089`
- Story: `US-0099` (auto-bootstrap dev-environment profile on install/upgrade — DEC-0084 amended § bootstrap posture / R-0086)
- Release: **finalized** (`2026-06-14T23:30:00Z`, `orchestrator_run_id=auto-20260614-01`, strict proof `proof_hash=907a95ae387d71891aa3d7c86a9c39a164451f3a75966567d61344a3fba22cda`)
- Queue: **`handoffs/release_queue.md`** row **`S0089`** = **`released`**
- **Run / verify:** `pytest -k us0099 tests/auto_command_contract_test.py -v` → 7 passed; `python scripts/dev_environment_lib.py --self-test` → `[DEV_ENVIRONMENT_SELF_TEST_OK]`; see **`handoffs/releases/S0089-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=disabled`** — deterministic no-op (`publish_snapshot=skipped_disabled`)
- Sync (**DEC-0018**): **`SYNC_POLICY_MODE=disabled`** → **`push_decision=not_eligible`**, **`reason_code=SYNC_DISABLED`**
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio **0 OPEN** stories; backlog drain budget **7** remaining

## Release finalized note (S0088)

- Sprint: `S0088`
- Story: `US-0098` (dev environment auto-launch profile — DEC-0084 / R-0085)
- Release: **finalized** (`2026-06-14T12:30:00Z`, `orchestrator_run_id=auto-20260613-01`, strict proof `proof_hash=be1986208496cb2ac1947b34f1b4cea458851f39c88146eb04ba85c8fd009dd5`)
- Queue: **`handoffs/release_queue.md`** row **`S0088`** = **`released`**
- **Run / verify:** `pytest -k us0098 tests/auto_command_contract_test.py -v` → 8 passed; `python scripts/dev_environment_lib.py --self-test` → `[DEV_ENVIRONMENT_SELF_TEST_OK]`; see **`handoffs/releases/S0088-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=disabled`** — deterministic no-op (`publish_snapshot=skipped_disabled`)
- Sync (**DEC-0018**): **`SYNC_POLICY_MODE=disabled`** → **`push_decision=not_eligible`**, **`reason_code=SYNC_DISABLED`**
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio **0 OPEN** stories; backlog drain budget **8** remaining

## Release finalized note (S0087)

- Sprint: `S0087`
- Story: `US-0097` (project-owned root README bootstrap — DEC-0083 / R-0084)
- Release: **finalized** (`2026-06-14T04:30:00Z`, `orchestrator_run_id=auto-20260613-01`, strict proof `proof_hash=008ad6a2f2d8c6dd7b1ee5c32145936445e9a33627ed3ed90dc545cc5d468530`)
- Queue: **`handoffs/release_queue.md`** row **`S0087`** = **`released`**
- **Run / verify:** `pytest -k us0097 tests/auto_command_contract_test.py -v` → 8 passed; `python scripts/validate_project_readme_coverage.py --self-test` → `[PROJECT_README_COVERAGE_SELF_TEST_OK]`; see **`handoffs/releases/S0087-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=disabled`** — deterministic no-op (`publish_snapshot=skipped_disabled`)
- Sync (**DEC-0018**): **`SYNC_POLICY_MODE=disabled`** → **`push_decision=not_eligible`**, **`reason_code=SYNC_DISABLED`**
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio next OPEN **US-0098**; backlog drain budget **9** remaining

## Release finalized note (S0086)

- Sprint: `S0086`
- Story: `US-0096` (delivery modes: ultra-lean + mega-quick — DEC-0082 / R-0082)
- Release: **finalized** (`2026-06-13T16:00:00Z`, `orchestrator_run_id=auto-20260612-01`, strict proof `proof_hash=20f59d2ac3731ab4dfdf67925e5b630bf208dc4c20c84892702b537619dc30b1`)
- Queue: **`handoffs/release_queue.md`** row **`S0086`** = **`released`**
- **Run / verify:** `pytest -k "us0096 or us0095 or bug0012" tests/auto_command_contract_test.py -v` → 20 passed; `python scripts/check_intake_template_parity.py --scope=us-0096` → `[INTAKE_TEMPLATE_PARITY_OK]`; see **`handoffs/releases/S0086-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=confirm`** — **no** automated publish without explicit operator confirmation (`publish_snapshot=skipped_pending_operator_confirm`)
- Sync (**DEC-0018**): **`SYNC_POLICY_MODE=disabled`** → **`push_decision=not_eligible`**, **`reason_code=SYNC_DISABLED`**
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio **0 OPEN** stories; backlog drain budget **8** remaining

## Release finalized note (S0085)

- Sprint: `S0085`
- Bug: `BUG-0012` (native-chain drain-advance enforcement — DEC-0081 / R-0083)
- Release: **finalized** (`2026-06-13T01:30:00Z`, `orchestrator_run_id=auto-20260612-01`, strict proof `proof_hash=44b55cf523c1c6721f1b9e359e683a9216379d5b314f401b0a722f667f51afe2`)
- Queue: **`handoffs/release_queue.md`** row **`S0085`** = **`released`**
- **Run / verify:** `pytest -k "bug0012 or us0095" tests/auto_command_contract_test.py -v` → 12 passed; `python scripts/check_intake_template_parity.py --scope=bug-0012` → `[INTAKE_TEMPLATE_PARITY_OK]`; see **`handoffs/releases/S0085-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=confirm`** — **no** automated publish without explicit operator confirmation (`publish_snapshot=skipped_pending_operator_confirm`)
- Sync (**DEC-0018**): **`SYNC_POLICY_MODE=disabled`** → **`push_decision=not_eligible`**, **`reason_code=SYNC_DISABLED`**
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout; bug queue **empty**; portfolio next OPEN **US-0096**

## Release finalized note (S0084)

- Sprint: `S0084`
- Story: `US-0095` (Native in-Cursor `/auto` auto-chaining — DEC-0080 / R-0081)
- Release: **finalized** (`2026-06-07T23:30:00Z`, `orchestrator_run_id=auto-20260607-02`, strict proof `proof_hash=423dead28ffb878335ae77568a29c357fffc185859bf3d2fb98dd23f4fe3202d`)
- Queue: **`handoffs/release_queue.md`** row **`S0084`** = **`released`**
- **Run / verify:** `pytest -k us0095 tests/auto_command_contract_test.py -v` → 7 passed; `python scripts/check_intake_template_parity.py --scope=us-0095` → `[INTAKE_TEMPLATE_PARITY_OK]`; see **`handoffs/releases/S0084-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=confirm`** — **no** automated publish without explicit operator confirmation (`publish_snapshot=skipped_pending_operator_confirm`)
- Sync (**DEC-0018**): **`ALLOW_AUTO_PUSH=1`**, **branch=main**, **`push_decision=blocked`**, **`reason_code=TEST_FAILED`** (14 pre-existing disjoint harness failures)
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio **0 OPEN** stories; backlog drain budget **9** remaining

## Release finalized note (S0083)

- Sprint: `S0083`
- Story: `US-0094` (README visionary intro + tiered feature hierarchy — R-0080)
- Release: **finalized** (`2026-06-07T16:30:00Z`, `orchestrator_run_id=auto-20260607-01`, strict proof `proof_hash=1a245b9025a2d1acf19f5993e4ac7febfb8abc5c1bd75ad88a18e296c7c4dd00`)
- Queue: **`handoffs/release_queue.md`** row **`S0083`** = **`released`**
- **Run / verify:** `python scripts/validate_readme_feature_coverage.py --repo . --enforce` → `[README_FEATURE_COVERAGE_VALIDATE_OK]`; `coverage_missing=[]`, `coverage_total=104`; see **`handoffs/releases/S0083-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=confirm`** — **no** automated publish without explicit operator confirmation (`publish_snapshot=skipped_pending_operator_confirm`)
- Sync (**DEC-0018**): **`ALLOW_AUTO_PUSH=1`**, **branch=main**, **`push_decision=blocked`**, **`reason_code=TEST_FAILED`** (14 pre-existing disjoint harness failures)
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio **0 OPEN** stories

## Release finalized note (S0082)

- Sprint: `S0082`
- Story: `US-0093` (Cursor browser-integrated UAT self-test — DEC-0079)
- Release: **finalized** (`2026-06-07T01:30:00Z`, `orchestrator_run_id=auto-20260606-04`, strict proof `proof_hash=57e939f5220447bd9a4697146f6a78fb5fbe6d92005eeafcd354e34c8d7c8ab0`)
- Queue: **`handoffs/release_queue.md`** row **`S0082`** = **`released`**
- **Run / verify:** `pytest -k us0093` → 6 passed; `python scripts/uat_probe_lib.py --self-test` → `[UAT_PROBE_LIB_SELF_TEST_OK]`; see **`handoffs/releases/S0082-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=confirm`** — **no** automated publish without explicit operator confirmation (`publish_snapshot=skipped_pending_operator_confirm`)
- Sync (**DEC-0018**): **`ALLOW_AUTO_PUSH=1`**, **branch=main**, **`push_decision=blocked`**, **`reason_code=TEST_FAILED`** (14 pre-existing disjoint harness failures)
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio **0 OPEN** stories; backlog drain budget **1** remaining

## Release finalized note (S0081)

- Sprint: `S0081`
- Story: `US-0092` (Full-autonomy `/auto` mode + outer driver + self-verification — DEC-0078)
- Release: **finalized** (`2026-06-06T22:30:00Z`, `orchestrator_run_id=auto-20260606-03`, strict proof `proof_hash=c090713e2791b75a697db7e09c9a874a257e3d79b742436837b6d84d2d1d0c78`)
- Queue: **`handoffs/release_queue.md`** row **`S0081`** = **`released`**
- **Run / verify:** `pytest -k us0092` → 9 passed; `python scripts/auto_outer_driver.py --self-test` → `[AUTO_OUTER_DRIVER_SELF_TEST_OK]`; `python scripts/uat_probe_lib.py --self-test` → `[UAT_PROBE_LIB_SELF_TEST_OK]`; see **`handoffs/releases/S0081-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=confirm`** — **no** automated publish without explicit operator confirmation (`publish_snapshot=skipped_pending_operator_confirm`)
- Sync (**DEC-0018**): **`ALLOW_AUTO_PUSH=1`**, **branch=main**, **`push_decision=blocked`**, **`reason_code=TEST_FAILED`** (14 pre-existing disjoint harness failures)
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio **0 OPEN** stories; backlog drain budget **2** remaining

## Release finalized note (S0080)

- Sprint: `S0080`
- Bug: `BUG-0011` (Caveman voice compression rules — DEC-0077)
- Release: **finalized** (`2026-06-06T17:00:00Z`, `orchestrator_run_id=auto-20260606-02`, strict proof `proof_hash=06b929b4b97c50dfb4012154443764c17e2958c409d4df9d0b16dda5b39825fc`)
- Queue: **`handoffs/release_queue.md`** row **`S0080`** = **`released`**
- **Run / verify:** `pytest -k caveman_voice` → 9 passed; `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` → **`tests/report.md`** (808/14); see **`handoffs/releases/S0080-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=confirm`** — **no** automated publish without explicit operator confirmation (`publish_snapshot=skipped_pending_operator_confirm`)
- Sync (**DEC-0018**): **`ALLOW_AUTO_PUSH=1`**, **branch=main**, **`push_decision=blocked`**, **`reason_code=TEST_FAILED`** (14 pre-existing disjoint harness failures)
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout; bug queue **empty**

## Release finalized note (S0079)

- Sprint: `S0079`
- Bug: `BUG-0010` (triad archiver dual-level heading fix — DEC-0076)
- Release: **finalized** (`2026-06-06T16:36:00Z`, `orchestrator_run_id=auto-20260606-02`, strict proof `proof_hash=185901a6d7b195ae6ab54f9221953ba4311a955d70d62b76c69ca1c351ac4b14`)
- Queue: **`handoffs/release_queue.md`** row **`S0079`** = **`released`**
- **Run / verify:** `python scripts/enforce-triad-hot-surface.py --self-test` → exit 0; `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` → **`tests/report.md`**; see **`handoffs/releases/S0079-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=confirm`** — **no** automated publish without explicit operator confirmation (`publish_snapshot=skipped_pending_operator_confirm`)
- Sync (**DEC-0018**): **`ALLOW_AUTO_PUSH=1`**, **branch=main**, **`push_decision=blocked`**, **`reason_code=TEST_FAILED`** (14 pre-existing disjoint harness failures)
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout, then **`/auto`** for **`BUG-0011`** (bug queue remaining = 1)

## Release finalized note (S0078)

- Sprint: `S0078`
- Bug: `BUG-0009` (downstream CI packaging job leak — DEC-0075)
- Release: **finalized** (`2026-06-06T16:15:00Z`, `orchestrator_run_id=auto-20260606-02`, strict proof `proof_hash=ca36057ca8aff89ceee48d2474bf84c5533f777c9f9cd194a1c18ef8425484bc`)
- Queue: **`handoffs/release_queue.md`** row **`S0078`** = **`released`**
- **Run / verify:** `python scripts/check_downstream_ci_guard.py --repo . --report` → `ok=true`; `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` → **`tests/report.md`**; see **`handoffs/releases/S0078-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=confirm`** — **no** automated publish without explicit operator confirmation (`publish_snapshot=skipped_pending_operator_confirm`)
- Sync (**DEC-0018**): **`ALLOW_AUTO_PUSH=1`**, **branch=main**, **`push_decision=blocked`**, **`reason_code=TEST_FAILED`** (14 pre-existing disjoint harness failures)
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout, then **`/auto`** for **`BUG-0010`** (bug queue remaining = 2)

## Release finalized note (S0077)

- Sprint: `S0077`
- Story: `US-0091` (README feature coverage backfill + blocking drift gate — DEC-0074)
- Release: **finalized** (`2026-06-06T13:43:20Z`, `orchestrator_run_id=auto-20260606-01`, strict proof `proof_hash=cbfc031254b549dfef27f12c4a6d5acb51b528835180b60252e54b44d238bd47`)
- Queue: **`handoffs/release_queue.md`** row **`S0077`** = **`released`**
- **Run / verify:** `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` -> **`tests/report.md`**; `python scripts/validate_readme_feature_coverage.py --repo . --enforce` -> **`[README_FEATURE_COVERAGE_VALIDATE_OK]`**; see **`handoffs/releases/S0077-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=confirm`** - **no** automated publish without explicit operator confirmation (`publish_snapshot=skipped_pending_operator_confirm`)
- Sync (**DEC-0018**): **`ALLOW_AUTO_PUSH=1`**, **branch=main**, **`push_decision=blocked`**, **`reason_code=TEST_FAILED`** (9 pre-existing disjoint harness failures)
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout, then **`/auto`** / portfolio (backlog drain budget remaining = 3; OPEN bugs `BUG-0009..BUG-0011` on bug queue)

## Release finalized note (S0076)

- Sprint: `S0076`
- Story: `US-0090` (Caveman input compression — operator-gated, sidecar-first, default-off CLI + installer surface; DEC-0073)
- Release: **finalized** (`2026-04-19T00:05:00Z`, `orchestrator_run_id=auto-20260418-01`, strict proof `proof_hash=0126c54efd3cc8158d9d0a687a66e9bce8f4eeefb89522993bb5ce805bb87e40`)
- Queue: **`handoffs/release_queue.md`** row **`S0076`** = **`released`**
- **Run / verify:** `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` -> **`tests/report.md`**; see **`handoffs/releases/S0076-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=confirm`** - **no** automated publish without explicit operator confirmation (`publish_snapshot=skipped_pending_operator_confirm`)
- Sync (**DEC-0018**): **`ALLOW_AUTO_PUSH=1`**, **branch=main**, **`push_decision=blocked`**, **`reason_code=TEST_FAILED`** (9 pre-existing disjoint failures block push gate even though release-gate classification tolerates them)
- Carried-forward non-blocking observations: (1) `PARTIAL_VERBATIM` on DEC-0073 §1 publication (architecture verbatim; reference + runbook paraphrase; DEC-0072 §6 row 6 pinned test preserved byte-unchanged); (2) UAT-3 `--dry-run` vs `--write` narration variance (AC-4 fail-closed intent satisfied via `--write` evidence).
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout, then **`/auto`** / portfolio (next OPEN story per backlog drain; budget remaining = 4)

## Release finalized note (S0075)

- Sprint: `S0075`
- Story: `US-0089` (Cursor Caveman mode — scratchpad-configurable terse responses)
- Release: **finalized** (`2026-04-18T19:00:00Z`, `orchestrator_run_id=auto-20260418-01`, strict proof `proof_hash=2f7351477332235595f379aae04d3830a0efc33f9a9cef887822999bcc9839b3`)
- Queue: **`handoffs/release_queue.md`** row **`S0075`** = **`released`**
- **Run / verify:** `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` -> **`tests/report.md`**; see **`handoffs/releases/S0075-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=confirm`** - **no** automated publish without explicit operator confirmation (`publish_snapshot=skipped_pending_operator_confirm`)
- Sync (**DEC-0018**): **`ALLOW_AUTO_PUSH=1`**, **branch=main**, **`push_decision=blocked`**, **`reason_code=TEST_FAILED`** (11 pre-existing disjoint failures block push gate even though release-gate classification tolerates them)
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout, then **`/auto`** / portfolio (next OPEN story per backlog drain)

## Release finalized note (S0074)

- Sprint: `S0074`
- Story: `US-0086` (automation-driven remote execution selection)
- Release: **finalized** (`2026-04-13T22:30:00Z`, `orchestrator_run_id=auto-20260405-01`, strict proof `proof_hash=3bc64c2345bb8861075d957ae665280da80f41d0ce21ba4caa6e55e865b96153`)
- Queue: **`handoffs/release_queue.md`** row **`S0074`** = **`released`**
- **Run / verify:** `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` -> **`tests/report.md`**; see **`handoffs/releases/S0074-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=confirm`** - **no** automated publish without explicit operator confirmation
- Sync (**DEC-0018**): **`ALLOW_AUTO_PUSH=0`** -> **`push_decision=not_eligible`**, **`reason_code=MANUAL_MODE_NO_AUTO`** (unless scratchpad overrides)
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout, then **`/auto`** / portfolio (next OPEN story per backlog drain)

## Release finalized note (S0073)

- Sprint: `S0073`
- Story: `US-0085` (Gitignored `.env` for remote and release connectivity — no AI read)
- Release: **finalized** (`2026-04-13T17:00:00Z`, `orchestrator_run_id=auto-20260405-01`, strict proof `proof_hash=201375708766b544b12a336534d09e5a8c69369bf18e10c8ea8ac76717dcfb75`)
- Queue: **`handoffs/release_queue.md`** row **`S0073`** = **`released`**
- **Run / verify:** `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` → **`tests/report.md`**; see **`handoffs/releases/S0073-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=confirm`** — **no** automated publish without explicit operator confirmation
- Sync (**DEC-0018**): **`ALLOW_AUTO_PUSH=0`** → **`push_decision=not_eligible`**, **`reason_code=MANUAL_MODE_NO_AUTO`** (unless scratchpad overrides)
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout, then **`/auto`** / portfolio (next OPEN story per backlog drain)

## Release finalized note (S0072)

- Sprint: `S0072`
- Story: `US-0088` (`/auto` continuous multi-phase loop + quiet backlog drain)
- Release: **finalized** (`2026-04-13T01:15:00Z`, `orchestrator_run_id=auto-20260405-01`, strict proof `proof_hash=a1c18a2b7e8a8f83687ca47ad29c0764b0a5867e4098e8e1c1a20314ffe68bbd`)
- Queue: **`handoffs/release_queue.md`** row **`S0072`** = **`released`**
- **Run / verify:** `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` → **`tests/report.md`**; see **`handoffs/releases/S0072-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=confirm`** — **no** automated publish without explicit operator confirmation
- Sync (**DEC-0018**): **`ALLOW_AUTO_PUSH=0`** → **`push_decision=not_eligible`**, **`reason_code=MANUAL_MODE_NO_AUTO`** (unless scratchpad overrides)
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout, then **`/auto`** / portfolio (next OPEN story per backlog drain)

## Release finalized note (S0071)

- Sprint: `S0071`
- Story: `US-0087` (**`/auto`** explicit bug targeting / bug-queue mode)
- Release: **finalized** (`2026-04-12T19:05:00Z`, `orchestrator_run_id=auto-20260405-01`, strict proof `proof_hash=b453b8901b083fb927dc73cfea54655f4e4ea1a703c4f1ea3e5cb420e6c4b215`)
- Queue: **`handoffs/release_queue.md`** row **`S0071`** = **`released`**
- **Run / verify:** `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` → **`tests/report.md`**; see **`handoffs/releases/S0071-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=confirm`** — **no** automated publish without explicit operator confirmation
- Sync (**DEC-0018**): **`ALLOW_AUTO_PUSH=0`** → **`push_decision=not_eligible`**, **`reason_code=MANUAL_MODE_NO_AUTO`** (unless scratchpad overrides)
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout, then **`/auto`** / portfolio (**US-0088** intake already in **`resume_brief`**)

## Release finalized note (S0070)

- Sprint: `S0070`
- Bug: `BUG-0008` (CRLF **`installer-owned-paths.manifest`** / **`R-0069`**)
- Release: **finalized** (`2026-04-05T22:30:00Z`, `orchestrator_run_id=auto-20260404-03`, strict proof `proof_hash=29228ef7c322aa74d21b8a354adf4c45bbb8d4c64c967ee9dd3d58f7e9b2bf02`)
- Queue: **`handoffs/release_queue.md`** row **`S0070`** = **`released`**
- **Run / verify:** `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` → **`tests/report.md`**; see **`handoffs/releases/S0070-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=disabled`** — **no** **`npm publish`** this boundary (deterministic no-op)
- Sync (**DEC-0018**): **`ALLOW_AUTO_PUSH=0`** → **`push_decision=not_eligible`**, **`reason_code=MANUAL_MODE_NO_AUTO`** (unless scratchpad overrides)
- **Next**: **`/refresh-context`** (fresh **curator** context)

## Release finalized note (S0069)

- Sprint: `S0069`
- Story: `US-0084` (POSIX npm installer + Linux remote test targets; **US-0064** alignment; **DEC-0070** remote-config helper skip policy)
- Release: **finalized** (`2026-04-05T00:10:00Z`, `orchestrator_run_id=auto-20260404-02`, strict proof `proof_hash=418cbee2c8f7508880e1cbcae744d67877c08e68c91432b3de38f0e1773b07fc`)
- Queue: **`handoffs/release_queue.md`** row **`S0069`** = **`released`**
- Publish posture: **`RELEASE_PUBLISH_MODE=confirm`** — no auto-publish without confirmation
- Sync (**DEC-0018**): **`ALLOW_AUTO_PUSH=0`** → **`push_decision=not_eligible`**, **`reason_code=MANUAL_MODE_NO_AUTO`** (no auto-push this boundary)
- **Next**: **`/refresh-context`** (fresh **curator** context)

## Release finalized note (S0068) (historical)

- Sprint: `S0068`
- Bug: `BUG-0007` (**R-0066** / **`INTAKE_ANSWER_REF_NOT_TOPIC_DISTINCT`**)
- Release: **finalized** (`2026-04-05T00:10:00Z`, `orchestrator_run_id=auto-20260404-01`, strict proof `proof_hash=6c824be4c8dfb3ecb25de8e8ca90910789436a2c916489fb15a935baf3c64202`)
- Queue: **`handoffs/release_queue.md`** row **`S0068`** = **`released`**
- Sync (**DEC-0018**): **`ALLOW_AUTO_PUSH=0`** → **`push_decision=not_eligible`**, **`reason_code=MANUAL_MODE_NO_AUTO`** (no auto-push this boundary)
- Portfolio: **`docs/product/backlog.md`** — canonical **bug** rows **BUG-0001..BUG-0007** all **DONE**; **next OPEN bug:** **(none)**
- **Next**: **`/refresh-context`** (fresh **curator** context) — **superseded** by **S0069** pointer above

## Release readiness note (S0068) (historical)

- Pre-release verify-work **PASS** (`2026-04-04T23:45:00Z`); superseded by **Release finalized note (S0068)** above.

## Release readiness note (S0067)

- Sprint: `S0067`
- Bug: `BUG-0006` (**spawn-only `/auto`**, **`AUTO_ORCHESTRATOR_PHASE_EXECUTION`**, **R-0065**)
- Release: **finalized** — queue row **`released`**; canonical notes `handoffs/releases/S0067-release-notes.md` (`2026-04-04T09:00:00Z`, `orchestrator_run_id=auto-20260403-03`); **`/refresh-context`** **complete** — successor track **`S0068`** / **`BUG-0007`** **released** (`2026-04-05`).

## Release readiness note (S0066)

- Sprint: `S0066`
- Bug: `BUG-0005` (**DEC-0069**)
- Release: **finalized** — queue row **`released`**; canonical notes `handoffs/releases/S0066-release-notes.md`; **`/refresh-context`** **complete** (`auto-20260403-02`, **`2026-04-03T23:55:00Z`**) — superseded by **`S0067`** closure track; portfolio now advances via **`BUG-0007`** after **`S0067`** **`/refresh-context`**.

## Release readiness note (S0065)

- Sprint: `S0065`
- Bug: `BUG-0004`
- Release: **finalized** - queue row **`released`**; canonical notes `handoffs/releases/S0065-release-notes.md`; next **`/refresh-context`** completed.

## Release readiness note (S0064)

- Sprint: `S0064`
- Story: `US-0083`
- Release: **finalized** - queue row **`released`**; canonical notes `handoffs/releases/S0064-release-notes.md`; next **`/refresh-context`** (see `docs/engineering/state.md`).

## Release readiness note (S0063)

- Sprint: `S0063`
- Bug: `BUG-0003`
- Release: **finalized** — queue row **`released`**; canonical notes `handoffs/releases/S0063-release-notes.md`; next **`/refresh-context`** (see `docs/engineering/state.md`).

## Release readiness note (S0062)

- Sprint: `S0062`
- Story: `US-0082`
- Release: **finalized** — queue row **`released`**; canonical notes `handoffs/releases/S0062-release-notes.md`; next **`/refresh-context`** (see `docs/engineering/state.md`).

## Release readiness note (S0061)

- Sprint: `S0061`
- Story: `US-0081`
- Release: **finalized** — queue row **`released`**; canonical notes `handoffs/releases/S0061-release-notes.md`; next **`/refresh-context`** (see `docs/engineering/state.md`).

## Release readiness note (S0060)

- Sprint: `S0060`
- Bug: `BUG-0001`
- Release: **finalized** — queue row **`released`**; canonical notes `handoffs/releases/S0060-release-notes.md`; next **`/refresh-context`** (see `docs/engineering/state.md`).

## Release readiness note (S0059)

- Sprint: `S0059`
- Story: `US-0080`
- Release: **finalized** — queue row **`released`**; canonical notes `handoffs/releases/S0059-release-notes.md`; next **`/refresh-context`** (see `docs/engineering/state.md`).

## Release readiness note (S0058)

- Sprint: `S0058`
- Story: `US-0079`
- Release: **finalized** — queue row **`released`**; canonical notes `handoffs/releases/S0058-release-notes.md`; next **`/refresh-context`** (see `docs/engineering/state.md`).

## Unreleased queue visibility

Check `handoffs/release_queue.md` for all pending entries where `status=unreleased`
or `status=blocked` before finalization.

- **`S0070` / `BUG-0008`**: **`blocked`** (`2026-04-04T23:30:00Z`) — **`RELEASE_TEST_FAILED`**, **`RELEASE_UAT_INCOMPLETE`**, deferred **publish**/**E2E**; canonical notes `handoffs/releases/S0070-release-notes.md`; do **not** treat **`S0069`** pointer as superseding this track until **`S0070`** **`released`** or row cleared.

## Release readiness note (S0057)

- Sprint: `S0057`
- Story: `US-0078`
- Release: **finalized** — queue row **`released`**; canonical notes `handoffs/releases/S0057-release-notes.md`; next **`/refresh-context`** (see `docs/engineering/state.md`).

## Release readiness note (S0056)

- Sprint: `S0056`
- Story: `US-0077`
- Release: **finalized** — queue row **`released`**; canonical notes `handoffs/releases/S0056-release-notes.md`; next **`/refresh-context`** (see `docs/engineering/state.md`).

## Release readiness note (S0055)

- Sprint: `S0055`
- Story: `US-0076`
- Verify-work: PASS
- UAT status: PASS (`10/10`, `0` failed)
- QA findings: PASS with no in-scope blockers (`sprints/S0055/qa-findings.md`)
- Release readiness: Finalized as `released` in `handoffs/release_queue.md`
  with canonical sprint-scoped notes.

## Latest operator summary (Run/Connect/Verify)

- **Start command:** Last finalized sprint **`S0109`**: `pytest tests/us0109_contract_test.py -v` — refer to `## Run` in
  `handoffs/releases/S0109-release-notes.md`.
- **Endpoint + port:** N/A (release documentation layer) — refer to `## Connect` in
  `handoffs/releases/S0109-release-notes.md`.
- **Verification steps + health signal:** Refer to `## Verify` in
  `handoffs/releases/S0109-release-notes.md`.
- **Credentials source refs (sanitized):** Refer to `## Credentials` in
  `handoffs/releases/S0107-release-notes.md` (env-ref only).
- **Known issues:** Refer to `## Known Issues` in
  `handoffs/releases/S0109-release-notes.md`.

## Historical references

- `S0075`: `handoffs/releases/S0075-release-notes.md`
- `S0074`: `handoffs/releases/S0074-release-notes.md`
- `S0073`: `handoffs/releases/S0073-release-notes.md`
- `S0072`: `handoffs/releases/S0072-release-notes.md`
- `S0071`: `handoffs/releases/S0071-release-notes.md`
- `S0070`: `handoffs/releases/S0070-release-notes.md`
- `S0069`: `handoffs/releases/S0069-release-notes.md`
- `S0068`: `handoffs/releases/S0068-release-notes.md`
- `S0067`: `handoffs/releases/S0067-release-notes.md`
- `S0066`: `handoffs/releases/S0066-release-notes.md`
- `S0065`: `handoffs/releases/S0065-release-notes.md`
- `S0064`: `handoffs/releases/S0064-release-notes.md`
- `S0063`: `handoffs/releases/S0063-release-notes.md`
- `S0062`: `handoffs/releases/S0062-release-notes.md`
- `S0061`: `handoffs/releases/S0061-release-notes.md`
- `S0060`: `handoffs/releases/S0060-release-notes.md`
- `S0059`: `handoffs/releases/S0059-release-notes.md`
- `S0058`: `handoffs/releases/S0058-release-notes.md`
- `S0057`: `handoffs/releases/S0057-release-notes.md`
- `S0056`: `handoffs/releases/S0056-release-notes.md`
- `S0055`: `handoffs/releases/S0055-release-notes.md`
- `S0054`: `handoffs/releases/S0054-release-notes.md`
- `S0053`: `handoffs/releases/S0053-release-notes.md`
- `S0052`: `handoffs/releases/S0052-release-notes.md`
- `S0051`: `handoffs/releases/S0051-release-notes.md`
- `S0050`: `handoffs/releases/S0050-release-notes.md`
- `S0049`: `handoffs/releases/S0049-release-notes.md`
- `S0048`: `handoffs/releases/S0048-release-notes.md`
- `S0047`: `handoffs/releases/S0047-release-notes.md`
- `S0046`: `handoffs/releases/S0046-release-notes.md`
- `S0045`: `handoffs/releases/S0045-release-notes.md`
- `S0044`: `handoffs/releases/S0044-release-notes.md`
- `S0043`: `handoffs/releases/S0043-release-notes.md`
- `S0042`: `handoffs/releases/S0042-release-notes.md`
- `S0041`: `handoffs/releases/S0041-release-notes.md`
- `S0040`: `handoffs/releases/S0040-release-notes.md`
- `S0039`: `handoffs/releases/S0039-release-notes.md`
- `S0038`: `handoffs/releases/S0038-release-notes.md`
- `S0037`: `handoffs/releases/S0037-release-notes.md`
- `S0036`: `handoffs/releases/S0036-release-notes.md`
- `S0035`: `handoffs/releases/S0035-release-notes.md`
- `S0034`: `handoffs/releases/S0034-release-notes.md`
- `S0033`: `handoffs/releases/S0033-release-notes.md`
- `S0032`: `handoffs/releases/S0032-release-notes.md`
- `S0031`: `handoffs/releases/S0031-release-notes.md`
- `S0030`: `handoffs/releases/S0030-release-notes.md`
- `S0029`: `handoffs/releases/S0029-release-notes.md`
- `S0011`: `handoffs/releases/S0011-release-notes.md`
- `S0025`: `handoffs/releases/S0025-release-notes.md`
- `S0026`: `handoffs/releases/S0026-release-notes.md`
- `S0027`: `handoffs/releases/S0027-release-notes.md`
- `S0028`: `handoffs/releases/S0028-release-notes.md`
- `S0024`: `handoffs/releases/S0024-release-notes.md`
- `S0023`: `handoffs/releases/S0023-release-notes.md`
- `S0022`: `handoffs/releases/S0022-release-notes.md`
- `S0021`: `handoffs/releases/S0021-release-notes.md`
- `S0020`: `handoffs/releases/S0020-release-notes.md`
- `S0019`: `handoffs/releases/S0019-release-notes.md`
- `S0018`: `handoffs/releases/S0018-release-notes.md`
- `S0017`: `handoffs/releases/S0017-release-notes.md`
- `S0016`: `handoffs/releases/S0016-release-notes.md`
- `S0015`: `handoffs/releases/S0015-release-notes.md`
- `S0013`: `handoffs/releases/S0013-release-notes.md`
- `S0012`: `handoffs/releases/S0012-release-notes.md`
- `S0010`: `handoffs/releases/S0010-release-notes.md`

---

## Per-gate audit verdict (US-0039)

When `/release` runs, each gate (check-in test, QA, UAT, finalization) is recorded with:
- **verdict**: pass | fail | override
- **reason_code**: e.g. RELEASE_TEST_FAILED, RELEASE_QA_BLOCKERS_OPEN, RELEASE_UAT_INCOMPLETE, RELEASE_GATE_OVERRIDE_APPROVED
- **remediation**: short steps when not pass
- **evidence_refs**: paths to tests/report.md, qa-findings.md, uat.json, release-findings.md, DEC-xxxx

Canonical per-run gate snapshot lives in `sprints/Sxxxx/release-findings.md` and queue row `gate_snapshot`; TL/QA audit from those artifacts and `docs/engineering/state.md` checkpoints.

**Override path (US-0039)**: When a gate is overridden, record decision record ref (DEC-xxxx), rationale, approver, and risk acceptance in release-findings and gate_snapshot; use reason code `RELEASE_GATE_OVERRIDE_APPROVED`.

## Compatibility behavior contract

- Keep this file as a pointer/summary; do not treat it as canonical historical
  storage.
- `/release` must update sprint-scoped notes first, then refresh this pointer.
- Never delete or destructively rewrite historical sprint-scoped note files
  through this legacy path.
