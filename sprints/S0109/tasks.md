# Sprint S0109 — US-0109 Self-Healing Deploy Loop — Tasks

## AC-to-task surjective map

| AC | Tasks |
|----|-------|
| AC-1 Scratchpad keys + zero-overhead default | T-001 |
| AC-2 Post-deploy smoke probe + probe_kind | T-002, T-003 |
| AC-3 Bounded retry loop | T-004 |
| AC-4 DEPLOY_DEFERRED state transition (US-0107 `append_deferral`) | T-005 |
| AC-5 Contract tests + backward compat | T-006, T-007 |
| AC-6 Validator CLI + tokens | T-008 |
| AC-7 Compose regression guards | T-009 |
| AC-8 Parity + runbook + reason codes | T-010 |
| AC-9 Execute steps 29-31 wiring | T-011 |

## Tranche order (A->D)

| Tranche | Title | Tasks |
|---------|-------|-------|
| A | Keys + reason codes | T-001 |
| B | Probe lib + target resolution | T-002, T-003 |
| C | Retry + deferral | T-004, T-005 |
| D | Tests + validator + compose + parity + runbook + execute wiring | T-006, T-007, T-008, T-009, T-010, T-011 |

## Tasks

- [x] **T-001** Scratchpad keys + reason codes (AC-1): append `AUTO_SOVEREIGN_SELF_HEALING_DEPLOY=0`, `AUTO_SOVEREIGN_DEPLOY_RETRY_MAX=3`, `AUTO_SOVEREIGN_DEPLOY_SMOKE_TIMEOUT_SEC=30`, `AUTO_SOVEREIGN_DEPLOY_PROBE_KIND=both`, `SOVEREIGN_DEPLOY_ACCEPTANCE_SMOKE_PATH=tests/deploy_smoke/`, `AUTO_SOVEREIGN_DEPLOY_HEALTH_ENDPOINT` (names-only) to `.cursor/scratchpad.md` + template mirror. Reason code inventory: 8 codes (`DEPLOY_HEALING_DISABLED`, `DEPLOY_HEALING_SMOKE_HEALTH_FAIL`, `DEPLOY_HEALING_SMOKE_ACCEPTANCE_FAIL`, `DEPLOY_HEALING_RETRY_ATTEMPT`, `DEPLOY_HEALING_RETRY_CAP_EXHAUSTED`, `DEPLOY_HEALING_DEFERRED`, `DEPLOY_HEALING_PROBE_TARGET_MISSING`, `DEPLOY_HEALING_TIMEOUT`). Dependency: none.

- [x] **T-002** Self-healing deploy lib (AC-2): create `scripts/self_healing_deploy_lib.py` — `run_health_probe(scratchpad)`, `run_acceptance_smoke(scratchpad)`, `run_smoke_probe_chain(scratchpad)` per two-stage chain; names-only URL resolution (US-0085 compose); output schema `{probe_kind, health_status, health_status_code, acceptance_status, acceptance_tests_run, acceptance_tests_failed, overall, reason_code}`. Dependency: T-001.

- [x] **T-003** Probe target resolution (AC-2): `resolve_health_endpoint_url(scratchpad)` — names-only env ref resolution (`os.environ[ref]`); fail-closed `DEPLOY_HEALING_PROBE_TARGET_MISSING` when absent; secret scan. Dependency: T-001.

- [x] **T-004** Bounded retry loop (AC-3): `run_deploy_healing_loop(repo, scratchpad, publish_handler)` — re-enter US-0054 publish PASS on probe FAIL; per-attempt `DEPLOY_HEALING_RETRY_ATTEMPT` reason log; cap at `AUTO_SOVEREIGN_DEPLOY_RETRY_MAX`; idempotency invariant (no duplicated ledger rows); bounded total timeout. Dependency: T-002.

- [x] **T-005** DEPLOY_DEFERRED transition (AC-4): `emit_deploy_deferral(repo, scratchpad, smoke_summary)` calling US-0107 `append_deferral(work_item_kind=deploy, reason_code=DEPLOY_DEFERRED, work_item_ref=<story_id>, source_orchestrator_run_id=<runner>, remediation_hint=<summary truncto512>, blocked_by_phase=release, retry_count=<retry_max>)`. Orchestrator continues per `AUTO_SOVEREIGN_DEFERRAL_POLICY`. Dependency: T-004.

- [x] **T-006** Contract tests (AC-5): create `tests/us0109_contract_test.py` with 8 core markers: `test_us0109_scratchpad_keys_and_defaults`, `test_us0109_probe_health_stage`, `test_us0109_probe_acceptance_stage`, `test_us0109_retry_loop_bounded`, `test_us0109_deferred_after_cap_exhaustion`, `test_us0109_backward_compat_off_path_byte_identical`, `test_us0109_validator_cli_self_test`, `test_us0109_reason_codes_section_present`. Dependency: T-001..T-005.

- [x] **T-007** Backward compat guard (AC-5): `AUTO_SOVEREIGN_SELF_HEALING_DEPLOY=0` byte-identical to US-0054 publish path; no probe, no retry, no deferral, no steps 29-31. Regression test `test_us0109_backward_compat_off_path_byte_identical` (shared with T-006). Dependency: T-002. Compose: US-0054 UNCHANGED.

- [x] **T-008** Validator CLI (AC-6): create `scripts/self_healing_deploy_validate.py` (+ template mirror) with flags `--self-test` (emit `[SELF_HEALING_DEPLOY_VALIDATION_OK]`), `--repo`, `--file`, `--enforce`. Dependency: T-002.

- [x] **T-009** Compose regression guards (AC-7): `test_us0109_us0054_compose_no_publish_semantics_change` + `test_us0109_us0100_compose_no_changelog_change`. Ensure publish targets / confirmation gate / release-notes wiring UNCHANGED; changelog / [Unreleased] / GitHub notes UNCHANGED. Dependency: T-004.

- [x] **T-010** Parity + runbook + reason codes (AC-8): `scripts/check_intake_template_parity.py --scope=sovereign-self-healing-deploy` with `SOVEREIGN_SELF_HEALING_DEPLOY_PAIRS` (6 pairs: scratchpad active+template, validator active+template, lib active+template). Append section to `docs/engineering/runbook.md` "Self-Healing Deploy Loop" operator remediation recipe. Section in `docs/engineering/reason_codes.md` with 8 codes. Dependency: T-008.

- [x] **T-011** Execute steps 29-31 wiring (AC-9): step 29 post-deploy smoke probe; step 30 retry loop on probe FAIL re-enter publish PASS, cap exhaustion -> step 31; step 31 DEPLOY_DEFERRED via `emit_deploy_deferral`. Position: after US-0108 step 28 (merge+cleanup); after US-0047 step 22 + US-0107 step 24; before US-0107 step 24 sovereign-loop advance. Dependency: T-002..T-005.
