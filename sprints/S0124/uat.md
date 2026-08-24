# Sprint S0124 — UAT (US-0124, code story) — populated (verify-work, post qa loop-2 PASS)

- **sprint_id**: S0124
- **story_refs**: US-0124
- **phase**: verify-work (build+verify macro — third phase per ultra_lean)
- **role**: qa (fresh per BUG-0006; verify-work subagent)
- **orchestrator_run_id**: auto-20260824-02
- **delivery_mode**: ultra_lean
- **macro_phase**: build_verify
- **story_type**: code
- **fresh_context_marker**: `qa-US0124-verify-work-20260824T193000Z-fresh` (NEW — not reused from qa loop-2)
- **timestamp**: 2026-08-24T19:30:00Z (UTC)
- **model_id**: glm-5.2-high (CROSS_MODEL_REVIEW=1 — required)
- **verdict**: **PASS** — 11/11 UAT steps pass; 12/12 contract-test markers PASS; opencode-adapter parity PASS; README feature coverage PASS; triad --check PASS post-rollover; metadata guard PASS. Non-browser plugin contract story — no fake browser PASS.
- **total_steps**: 11 | **passed**: 11 | **failed**: 0
- **story_status**: OPEN (do not mark US-0124 DONE — US-0045; acceptance L152 unchecked; intake JSON not mutated)

## Target stories + acceptance criteria

- **US-0124** — OpenCode orchestrator plugin Task-spawns US-0069 roles, never executes phase work in-session (11 ACs)
  - AC-1: PASS — Spawn-only `/auto` — orchestrator plugin/primary agent must not write phase artifacts in its own session; fail-closed `AUTO_ORCHESTRATOR_PHASE_EXECUTION` analogue. (markers 1, 7)
  - AC-2: PASS — US-0069 resolve — next phase maps to the matrix role; wrong-role spawn fails closed `PHASE_ROLE_MISMATCH` analogue. (marker 10)
  - AC-3: PASS — Isolation evidence — each spawned session records `phase_id`, `role`, `fresh_context_marker`, timestamp. (markers 1, 2)
  - AC-4: PASS — Success test (a) — contract/harness proves a prompt-ignoring orchestrator still cannot skip spawn isolation (same-session roleplay is rejected). (marker 2)
  - AC-5: PASS — Success test (d) — `/auto` cannot continue to the next phase without a fresh session for the next role. (markers 2 + 8)
  - AC-6: PASS — Stop matrix — plugin/outer-driver honors US-0092 stop reasons (decision_gate, loop_max, blocked, pause). (T-004 + marker 8)
  - AC-7: PASS — Headless `--invoke-cmd` — US-0092 outer driver can invoke OpenCode non-interactive/session API; `NATIVE_CHAIN_UNAVAILABLE` analogue rather than roleplay. (marker 8)
  - AC-8: PASS — Subtask-ignored fail-closed — fail closed with documented `OPENCODE_*` reason code; no one-chat multi-role. (markers 3, 4, 5)
  - AC-9: PASS — No US-0095 port — `.cursor/commands/auto.md` Cursor Task-chain prose not copied into plugin. (markers 6, 7)
  - AC-10: PASS — Contract tests — `test_us0124_*` cover spawn-only deny, isolation evidence, stop-matrix wiring, `--invoke-cmd` hook, subtask-ignored fail-closed. (all 12 markers)
  - AC-11: PASS — Secrets — plugin logs must not print API keys or `.env` contents. (marker 9)

## Contract test markers (12) — populated

`python -m pytest tests/us0124_contract_test.py -v` → **12 passed in 1.14s** (exit 0; independently re-run by /verify-work @ 2026-08-24T19:28:00Z)

1. `test_us0124_spawn_isolation_static` (AC-1, AC-3) — **PASS**
2. `test_us0124_spawn_isolation_runtime` (AC-3, AC-4, AC-10) — **PASS**
3. `test_us0124_subtask_ignored_null_return` (AC-8) — **PASS**
4. `test_us0124_subtask_ignored_throw` (AC-8; throw-discrimination) — **PASS**
5. `test_us0124_subtask_ignored_identical_id` (AC-8) — **PASS**
6. `test_us0124_no_cursor_auto_clone` (AC-9) — **PASS**
7. `test_us0124_agent_plugin_compose` (AC-1, AC-9; DQ8) — **PASS**
8. `test_us0124_invoke_cmd_hook` (AC-6, AC-7; DQ6 + DQ7) — **PASS**
9. `test_us0124_secrets_no_logging` (AC-11 / US-0085) — **PASS**
10. `test_us0124_phase_role_mismatch` (AC-2; plan-verify carry-forward 10th marker) — **PASS**
11. `test_us0124_no_vendor_slugs_in_plugin` (US-0102 extra guard) — **PASS**
12. `test_us0124_runbook_stub_present` (AC-8 extra guard) — **PASS**

## UAT step results

| Step | AC | Result | Evidence |
|------|----|--------|----------|
| UAT-1 | AC-1 | PASS | marker 1 (spawn_isolation_static) + marker 7 (agent_plugin_compose) PASS; plugin source ctx.session.create + parentID + agent + ctx.tool.hook('execute.before') + AUTO_ORCHESTRATOR_PHASE_EXECUTION |
| UAT-2 | AC-2 | PASS | marker 10 (phase_role_mismatch) PASS; unknown phase_id -> PHASE_ROLE_MISMATCH fail-closed with zero session.create calls |
| UAT-3 | AC-3 | PASS | marker 1 + marker 2 (spawn_isolation_runtime) PASS; isolation evidence dict with parentID, sessionID, role, phase_id, timestamp, fresh_context_marker |
| UAT-4 | AC-4 | PASS | marker 2 PASS; sessionID !== parentID enforced (orchestrator-session-0 vs fresh uuid); prompt-ignoring orchestrator cannot skip spawn isolation |
| UAT-5 | AC-5 | PASS | marker 2 + marker 8 PASS; dispatch-stop-matrix-ok returns action=spawn_next next_phase=qa; fresh session required before next phase |
| UAT-6 | AC-6 | PASS | T-004 + marker 8 PASS; auto_outer_driver.py additive argv -> JSON {action:spawn_next, phase, role}; legacy byte-identical when flags absent |
| UAT-7 | AC-7 | PASS | marker 8 PASS; headless argv ['opencode','run','--agent','auto','--format','json','--auto',<prompt>]; OPENCODE_HEADLESS_UNSUPPORTED when opencode missing; JSON events parsed on success |
| UAT-8 | AC-8 | PASS | markers 3, 4, 5 PASS; null/throw/identical-id all -> OPENCODE_SUBTASK_IGNORED; missing-primitive -> OPENCODE_PLUGIN_SPAWN_UNSUPPORTED; no one-chat multi-role |
| UAT-9 | AC-9 | PASS | markers 6, 7 PASS; zero Cursor-clone phrases in plugin; both auto.md + orchestrator.ts exist with no permission-array leak |
| UAT-10 | AC-10 | PASS | 12/12 contract markers PASS in 1.14s (exit 0); covers spawn-only deny, isolation evidence, stop-matrix wiring, --invoke-cmd hook, subtask-ignored fail-closed, secrets, phase-role mismatch, vendor slugs, runbook stub |
| UAT-11 | AC-11 | PASS | marker 9 PASS; zero secret patterns (api_key|apikey|sk-|auth.json|.env) in plugin/harness source; zero vendor model slugs in plugin |

## UAT probes (US-0092 / DEC-0078)

US-0124 is a non-browser TypeScript plugin contract story. No HTTP/UI target resolves; no `browser_smoke` step classifies. Per DEC-0078 fail-closed contract, unresolvable steps record `UAT_PROBE_UNRESOLVED` (not a silent PASS). Browser MCP not invoked. **No fake browser PASS.**

- `browser_probe_used`: false
- `browser_probe_reason`: Non-browser TypeScript plugin contract story; no browser_smoke step classifies. Browser MCP not invoked. No fake browser PASS.
- `probe_results[]`: 11 entries recorded in `sprints/S0124/uat.json` — UAT-6/UAT-7 (cli_smoke) and UAT-10 (test) record `UAT_PROBE_PASS` via live driver/pytest; remaining 8 steps record `UAT_PROBE_UNRESOLVED` with contract-test/harness/static-grep evidence basis (legitimate per DEC-0078 for non-browser stories).

## Runtime QA autopilot (US-0065 / DEC-0047)

- `runtime_stack_profile`: `node` (plugin is TypeScript; harness uses `node --experimental-strip-types` per `tests/us0124/run_harness.mjs`).
- `runtime_mode`: local.
- `runtime_startup_command`: `node --experimental-strip-types tests/us0124/run_harness.mjs` (driven via pytest).
- `runtime_health_target`: Node subprocess harness exit code + 12/12 contract markers.
- `runtime_health_result`: PASS (exit 0; 12/12 markers in 1.14s).
- `runtime_log_summary`: 0 errors / 0 warnings / 12 pass (pytest captured; no critical signals).
- `runtime_retry_count`: 0 (no transient failures).
- `runtime_retry_ledger`: `[]`.
- `runtime_final_verdict`: pass (contract-harness runtime; no live OpenCode probe required per AC-10).
- `runtime_reason_code`: N/A.
- `runtime_evidence_refs`: `tests/us0124_contract_test.py` pytest output above; `sprints/S0124/summary.md` contract-test block.

No live OpenCode runtime probe (AC-10 boundary). Generated baseline test contract (US-0066) satisfied by the 12 contract-test markers; `generated_test_command` = `python -m pytest tests/us0124_contract_test.py -v`; `generated_test_result` = pass.

## Independent verification commands re-run by /verify-work

| # | Gate | Command | Result |
|---|------|---------|--------|
| 1 | US-0124 contract tests (12 markers) | `python -m pytest tests/us0124_contract_test.py -v` | **PASS** (12/12 in 1.14s, exit 0) |
| 2 | opencode-adapter parity | `python scripts/check_intake_template_parity.py --repo . --scope opencode-adapter` | **PASS** `[INTAKE_TEMPLATE_PARITY_OK] scope=opencode-adapter` |
| 3 | README feature coverage | `python scripts/validate_readme_feature_coverage.py --repo . --report` | **PASS** — `{"coverage_missing":[],"coverage_present":["US-0121","US-0122","US-0123"],"coverage_total":3,"gaps":[],"status":"PASS"}` |
| 4 | Triad hot-surface (post-rollover) | `python scripts/enforce-triad-hot-surface.py --check` | **PASS** (exit 0; --rollover archived 1 unit prior) |
| 5 | User-visible metadata guard | `python scripts/check-user-visible-metadata.py --repo .` | **PASS** (exit 0) |
| 6 | Canonical harness report literals | `tests/report.md` @ 2026-08-24T19:17:58Z | **PASS** — L3 `Timestamp: 2026-08-24T19:17:58Z`; L4 `Pass: 845`; L5 `Fail: 0`; `rg "\[FAIL\]"` 0 matches (not re-run by /verify-work — no product/tests edits; per verify-work contract) |

## Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

- `phase_id=verify-work`
- `role=qa`
- `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 — required)
- `fresh_context_marker=qa-US0124-verify-work-20260824T193000Z-fresh` (NEW — not reused from qa loop-2)
- `timestamp=2026-08-24T19:30:00Z`
- `evidence_ref=sprints/S0124/uat.json (populated) + sprints/S0124/uat.md (populated) + docs/engineering/state.md (verify-work checkpoint append-bottom) + handoffs/resume_brief.md (verify-work PASS -> /release prepend) + tests/us0124_contract_test.py (12/12 PASS re-run) + tests/report.md (Pass:845 Fail:0 @ 2026-08-24T19:17:58Z — not re-run)`

Prior lifecycle isolation evidence verified present in `docs/engineering/state.md`:
- `phase_id=execute` (loop-2): `dev-US0124-execute-loop2-20260824T192000Z-fresh` @ 2026-08-24T19:20:00Z
- `phase_id=qa` (loop-2): `qa-US0124-qa-20260824T192500Z-fresh` @ 2026-08-24T19:25:00Z
- `phase_id=verify-work` (this phase): `qa-US0124-verify-work-20260824T193000Z-fresh` @ 2026-08-24T19:30:00Z (appended below)

## Strict runtime proof (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260824-02`
- `runtime_proof_id=rp-auto-20260824-02-verify-work-qa-20260824T193000Z-US-0124` (unique — distinct from execute loop-2 and qa loop-2 proof ids)
- `phase_id=verify-work`, `role=qa`, `story_id=US-0124`, `sprint_id=S0124`
- `proof_issued_at=2026-08-24T19:30:00Z`
- `proof_ttl_seconds=3600`, `proof_ttl=2026-08-24T20:30:00Z`
- `proof_hash=C1453A18FFF838E5ADAB069E930F82F9B87C7CAC176C4D7DAAC7F8E77FB24B89`
- Canonical payload (sorted-key JSON per DEC-0038): `{"delivery_mode":"ultra_lean","macro_phase":"build_verify","model_id":"glm-5.2-high","orchestrator_run_id":"auto-20260824-02","phase_id":"verify-work","proof_issued_at":"2026-08-24T19:30:00Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260824-02-verify-work-qa-20260824T193000Z-US-0124","sprint_id":"S0124","story_id":"US-0124"}`

## Compose guards (9/9 UNCHANGED)

US-0069/DEC-0051, US-0092/DEC-0078, US-0095/DEC-0080, US-0023/US-0048/BUG-0006, US-0005, US-0122/DEC-0122, US-0121/DEC-0120, US-0125, US-0102/DEC-0087 — all read-only consumers; US-0124 additive-only. Backlog L4287 (US-0124 OPEN) and acceptance checkboxes (L152) **unchanged** — US-0045 upheld. Intake evidence JSON not mutated.

## Results summary

- **UAT verdict**: PASS — 11/11 steps pass; 0 blocking findings; 0 non-blocking findings.
- **Acceptance criteria**: 11/11 PASS (AC-1 through AC-11).
- **Contract tests**: 12/12 PASS (`tests/us0124_contract_test.py`).
- **Parity**: opencode-adapter PASS; readme-feature-coverage PASS.
- **Canonical harness**: `tests/report.md` Pass:845 / Fail:0 @ 2026-08-24T19:17:58Z (not re-run — no product/tests edits by /verify-work).
- **Story status**: OPEN (US-0045 — not marked DONE; acceptance L152 unchecked; intake JSON not mutated).
- **Next scheduled phase**: `/release` (role=release; fresh subagent per BUG-0006).
- **Stop condition**: STOP after /verify-work. Hand off via artifacts only to `/release`. Do NOT spawn /release from this qa subagent. Do NOT mark US-0124 DONE. Do NOT tick acceptance. Do NOT mutate intake JSON.
