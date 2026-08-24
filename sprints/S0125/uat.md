# Sprint S0125 ? UAT (US-0125, code story) ? populated (verify-work, post qa loop-2 PASS)

- **sprint_id**: S0125
- **story_refs**: US-0125
- **phase**: verify-work (build+verify macro ? third phase per ultra_lean)
- **role**: qa (fresh per BUG-0006; verify-work subagent)
- **orchestrator_run_id**: auto-20260824-02
- **delivery_mode**: ultra_lean
- **macro_phase**: build+verify
- **story_type**: code
- **fresh_context_marker**: `qa-US0125-verify-work-20260824T223500Z-fresh` (NEW ? not reused from qa loop-2 `qa-US0125-qa-20260824T220000Z-fresh`)
- **timestamp**: 2026-08-24T22:35:00Z (UTC)
- **model_id**: glm-5.2-high (CROSS_MODEL_REVIEW=1 ? required)
- **verdict**: **PASS** ? 11/11 UAT steps pass; 11/11 contract-test markers PASS; opencode-adapter parity PASS; README feature coverage PASS (US-0125 correctly absent ? OPEN); triad --check PASS; canonical harness `tests/report.md` Pass:845 / Fail:0 literal @ 2026-08-24T21:04:51Z (not re-run ? no product/tests edits by /verify-work); zero `[FAIL]` rows; no fake browser PASS (non-browser plugin/command contract story).
- **total_steps**: 11 | **passed**: 11 | **failed**: 0
- **story_status**: OPEN (do not mark US-0125 DONE ? US-0045; acceptance L153 unchecked; intake JSON not mutated)

## Target stories + acceptance criteria

- **US-0125** ? Thin OpenCode commands and Python validator bridge ? dispatch-only named commands, no Cursor command clones, Python CLIs remain fail-closed source of truth, success test (b) `/release` blocked after failing validator, `test_us0125_*` (10 ACs)
  - AC-1: PASS ? markers 1+8+11 PASS; 15 dispatch-only command files; auto.md dispatch-only with agent: auto + subtask: false
  - AC-2: PASS ? marker 2 PASS; line cap <=20 + similarity <=0.30 for all 15 files; US0125_CLONE_GUARD_STRIP_TOKENS locked
  - AC-3: PASS ? marker 3 PASS; named CLIs subprocess; non-zero -> INTAKE_PERSISTENCE_BLOCKED; no reimplementation
  - AC-4: PASS ? marker 4 PASS; success test (b) ? non-zero -> refuse write; throw -> OPENCODE_DRIVER_INVOKE_FAILED; ok -> allowed
  - AC-5: PASS ? marker 5 PASS; raw Python reason codes; no OPENCODE_VALIDATOR_FAILED wrapper; OPENCODE_DRIVER_INVOKE_FAILED only for subprocess throw
  - AC-6: PASS ? marker 6 PASS; zero policy-text fragments in 15 command files
  - AC-7: PASS ? markers 7+8 PASS; deleting quick.md keeps plugin + @auto agent + 14 commands intact
  - AC-8: PASS ? marker 11 PASS + 11/11 contract markers PASS in 0.45s (exit 0); covers all required surfaces
  - AC-9: PASS ? marker 9 PASS; zero US-0125 references in .cursor/commands/*.md; OpenCode commands additive only
  - AC-10: PASS ? marker 10 PASS; package.json zero forbidden runtime deps; command files zero npm install / require(

## Contract test markers (11) ? populated

`python -m pytest tests/us0125_contract_test.py -v` ? **11 passed in 0.45s** (exit 0; independently re-run by /verify-work @ 2026-08-24T22:35:00Z)

1. `test_us0125_command_inventory` (AC-1) ? **PASS**
2. `test_us0125_clone_guard` (AC-2) ? **PASS**
3. `test_us0125_validator_subprocess_fail_closed` (AC-3) ? **PASS**
4. `test_us0125_release_blocked_after_failing_validator` (AC-4) ? **PASS**
5. `test_us0125_reason_code_raw_python` (AC-5) ? **PASS**
6. `test_us0125_no_policy_in_commands` (AC-6) ? **PASS**
7. `test_us0125_missing_command_does_not_disable_plugin` (AC-7) ? **PASS**
8. `test_us0125_auto_command_dispatch_only` (AC-1, AC-7) ? **PASS**
9. `test_us0125_cursor_commands_unchanged` (AC-9) ? **PASS**
10. `test_us0125_no_new_npm_runtime` (AC-10) ? **PASS**
11. `test_us0125_command_frontmatter_shape` (AC-1, AC-8) ? **PASS**

## UAT step results

| Step | AC | Result | Evidence |
|------|----|--------|----------|
| UAT-1 | AC-1 | PASS | test_us0125_command_inventory PASSED; md_files==sorted(expected 15); .gitkeep not exists; marker 11 frontmatter_shape PASSED |
| UAT-2 | AC-2 | PASS | test_us0125_clone_guard PASSED; offenders_line=[]; offenders_sim=[]; US0125_CLONE_GUARD_STRIP_TOKENS at test L61-L88; all 15 files <=20 lines (max 14) |
| UAT-3 | AC-3 | PASS | test_us0125_validator_subprocess_fail_closed PASSED; fixture validator_artifact_mapping.json contains both named CLIs bridge=named; harness release-blocked-nonzero returns allowed=false reasonCode=INTAKE_PERSISTENCE_BLOCKED |
| UAT-4 | AC-4 | PASS | test_us0125_release_blocked_after_failing_validator PASSED; r_nonzero allowed=false reasonCode=INTAKE_PERSISTENCE_BLOCKED calls=1; r_throw allowed=false reasonCode=OPENCODE_DRIVER_INVOKE_FAILED calls=1; r_ok allowed=true |
| UAT-5 | AC-5 | PASS | test_us0125_reason_code_raw_python PASSED; OPENCODE_VALIDATOR_FAILED zero hits across commands+mock_subprocess+bridge_harness; OPENCODE_DRIVER_INVOKE_FAILED present in harness, absent from command files (DQ4) |
| UAT-6 | AC-6 | PASS | test_us0125_no_policy_in_commands PASSED; POLICY_TEXT_FRAGMENTS zero hits across all 15 command files |
| UAT-7 | AC-7 | PASS | test_us0125_missing_command_does_not_disable_plugin PASSED; temp-copy plugins/orchestrator.ts exists; agents/auto.md exists; 14 commands remain after quick.md deletion |
| UAT-8 | AC-1 | PASS | test_us0125_auto_command_dispatch_only PASSED; auto.md <=20 lines; body free of ctx.session.create/Session.create/spawn(= patterns; agent: auto + subtask: false frontmatter |
| UAT-9 | AC-9 | PASS | test_us0125_cursor_commands_unchanged PASSED; 'US-0125' zero hits across .cursor/commands/*.md; OpenCode commands live in template/.opencode/commands/ only |
| UAT-10 | AC-10 | PASS | test_us0125_no_new_npm_runtime PASSED; package.json deps zero forbidden prefixes; 15 command files zero 'npm install' / 'require(' hits |
| UAT-11 | AC-8 | PASS | python -m pytest tests/us0125_contract_test.py -v -> 11 passed in 0.45s (exit 0); covers all 11 markers |

## UAT probes (US-0092 / DEC-0078)

US-0125 is a non-browser plugin/command contract story (dispatch-only commands + validator bridge contract asserted via Node subprocess harness `tests/us0125/bridge_harness.mjs`). No HTTP/UI target resolves; no `browser_smoke` step classifies. Per DEC-0078 fail-closed contract, all steps record `UAT_PROBE_PASS` via live pytest + Node harness (the right probe class for CLI/contract stories). Browser MCP not invoked. **No fake browser PASS.**

- `browser_probe_used`: False
- `browser_probe_reason`: Non-browser plugin/command contract story; no browser_smoke step classifies. Browser MCP not invoked. No fake browser PASS. CLI/contract evidence is the right probe class per DEC-0078.
- `probe_results[]`: 11 entries recorded in `sprints/S0125/uat.json` ? all 11 steps record `UAT_PROBE_PASS` via live pytest (11/11 contract markers in 0.45s, exit 0) + Node subprocess harness scenarios (release-blocked-nonzero, release-blocked-throw, release-allowed).

## Runtime QA autopilot (US-0065 / DEC-0047)

- `runtime_stack_profile`: `node` (harness uses `node --experimental-strip-types` per `tests/us0125/bridge_harness.mjs`).
- `runtime_mode`: local.
- `runtime_startup_command`: `node --experimental-strip-types tests/us0125/bridge_harness.mjs <scenario> (driven via pytest)`.
- `runtime_health_target`: Node subprocess harness exit code + 11/11 contract markers.
- `runtime_health_result`: PASS (exit 0; 11/11 markers in 0.45s).
- `runtime_log_summary`: 0 errors / 0 warnings / 11 pass.
- `runtime_retry_count`: 0 (no transient failures).
- `runtime_retry_ledger`: `[]`.
- `runtime_final_verdict`: pass.
- `runtime_reason_code`: N/A.
- `runtime_evidence_refs`: tests/us0125_contract_test.py pytest output; sprints/S0125/summary.md contract-test block.

No live OpenCode runtime probe (AC-10 boundary). Generated baseline test contract (US-0066) satisfied by the 11 contract-test markers; `generated_test_command` = `python -m pytest tests/us0125_contract_test.py -v`; `generated_test_result` = pass.

## Independent verification commands re-run by /verify-work

| # | Gate | Command | Result |
|---|------|---------|--------|
| 1 | US-0125 contract tests (11 markers) | `python -m pytest tests/us0125_contract_test.py -v` | **PASS** (11/11 in 0.45s, exit 0) |
| 2 | opencode-adapter parity | `python scripts/check_intake_template_parity.py --repo . --scope=opencode-adapter` | **PASS** `[INTAKE_TEMPLATE_PARITY_OK] scope=opencode-adapter` |
| 3 | README feature coverage | `python scripts/validate_readme_feature_coverage.py --repo . --report` | **PASS** ? `{"coverage_missing":[],"coverage_present":["US-0121","US-0122","US-0123","US-0124"],"coverage_total":4,"gaps":[],"status":"PASS"}` (US-0125 correctly absent ? OPEN) |
| 4 | Triad hot-surface | `python scripts/enforce-triad-hot-surface.py --check` | **PASS** (exit 0; no rollover triggered; Active context surface preserved) |
| 5 | Canonical harness report literals | `tests/report.md` @ 2026-08-24T21:04:51Z | **PASS** ? L3 `Timestamp: 2026-08-24T21:04:51Z`; L4 `Pass: 845`; L5 `Fail: 0`; `rg "[FAIL]"` 0 matches (not re-run by /verify-work ? no product/tests edits; per verify-work contract) |

## Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

- `phase_id=verify-work`
- `role=qa`
- `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 ? required)
- `fresh_context_marker=qa-US0125-verify-work-20260824T223500Z-fresh` (NEW ? not reused from qa loop-2)
- `timestamp=2026-08-24T22:35:00Z`
- `evidence_ref=sprints/S0125/uat.json (populated) + sprints/S0125/uat.md (populated) + docs/engineering/state.md (verify-work checkpoint append-bottom) + handoffs/resume_brief.md (verify-work PASS -> /release prepend) + tests/us0125_contract_test.py (11/11 PASS re-run) + tests/report.md (Pass:845 Fail:0 @ 2026-08-24T21:04:51Z ? not re-run)`

Prior lifecycle isolation evidence verified present in `docs/engineering/state.md`:
- `phase_id=execute` (loop-2): `dev-US0125-execute-loop2-20260824T210710Z-fresh` @ 2026-08-24T21:07:10Z
- `phase_id=qa` (loop-2): `qa-US0125-qa-20260824T220000Z-fresh` @ 2026-08-24T22:00:00Z
- `phase_id=verify-work` (this phase): `qa-US0125-verify-work-20260824T223500Z-fresh` @ 2026-08-24T22:35:00Z (appended below)

## Strict runtime proof (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260824-02`
- `runtime_proof_id=rp-auto-20260824-02-verify-work-qa-20260824T223500Z-US-0125` (unique ? distinct from execute loop-2 and qa loop-2 proof ids)
- `phase_id=verify-work`, `role=qa`, `story_id=US-0125`, `sprint_id=S0125`
- `proof_issued_at=2026-08-24T22:35:00Z`
- `proof_ttl_seconds=3600`, `proof_ttl=2026-08-24T23:35:00Z`
- `proof_hash=7278CD174376E4AC82670406BE664DF181D7471F09174DC619B6DC84478F0312`
- Canonical payload (sorted-key JSON per DEC-0038): `{"delivery_mode":"ultra_lean","macro_phase":"build+verify","model_id":"glm-5.2-high","orchestrator_run_id":"auto-20260824-02","phase_id":"verify-work","proof_issued_at":"2026-08-24T22:35:00Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260824-02-verify-work-qa-20260824T223500Z-US-0125","sprint_id":"S0125","story_id":"US-0125"}`

Prior phase proof consumed: `rp-auto-20260824-02-qa-qa-20260824T220000Z-US-0125` (proof_hash=591B6F44D3A311D17083D90AAF1D9A740F45826D63D38C48042FF160139E9AE2, ttl 2026-08-24T23:00:00Z ? consumed before RUNTIME_PROOF_STALE; hash independently recomputed and confirmed match).

## Compose guards (7/7 UNCHANGED)

US-0001, US-0078/DEC-0060, US-0121/DEC-0120, US-0122/DEC-0122, US-0124/DEC-0124, US-0126, US-0102/DEC-0087 ? all read-only consumers; US-0125 additive-only. Backlog US-0125 OPEN (L4329) and acceptance checkboxes (L153) **unchanged** ? US-0045 upheld. Intake evidence JSON not mutated.

## Results summary

- **UAT verdict**: PASS ? 11/11 steps pass; 0 blocking findings; 0 non-blocking findings.
- **Acceptance criteria**: 10/10 PASS (AC-1 through AC-10).
- **Contract tests**: 11/11 PASS (`tests/us0125_contract_test.py`).
- **Parity**: opencode-adapter PASS; readme-feature-coverage PASS (US-0125 absent ? OPEN).
- **Canonical harness**: `tests/report.md` Pass:845 / Fail:0 @ 2026-08-24T21:04:51Z (not re-run ? no product/tests edits by /verify-work).
- **Story status**: OPEN (US-0045 ? not marked DONE; acceptance L153 unchecked; intake JSON not mutated).
- **Next scheduled phase**: `/release` (role=release; fresh subagent per BUG-0006).
- **Stop condition**: STOP after /verify-work. Hand off via artifacts only to /release (role=release). Do NOT spawn /release from this qa subagent. Do NOT mark US-0125 DONE. Do NOT tick acceptance. Do NOT mutate intake JSON.
