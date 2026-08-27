# QA findings — US-0128 / S0128 / auto-20260826-01 (qa)

- **phase_id**: qa, **role**: qa, **story_id**: US-0128 (OPEN — not marked DONE per US-0045), **sprint_id**: S0128
- `orchestrator_run_id=auto-20260826-01`, `delivery_mode=ultra_lean`, `macro_phase=build+verify`
- `AUTO_IMPLEMENTATION_LOOP=1`
- `model_id=cursor-grok-4.6-high` (CROSS_MODEL_REVIEW=1 — required on isolation)
- `producer_phase_id=execute`, `producer_role=dev`, `producer_model_id=cursor-grok-4.6-high`
- `critic_phase_id=sovereign-critic` (execute review), `critic_model_id=composer-2.5-fast`, `critic_verdict=PASS`, `anti_slop_aggregate=10`, `open_blocking_findings=0`
- `critic_fresh_context_marker=tl-US0128-sovereign-critic-execute-20260826T203530Z-fresh`
- `fresh_context_marker=qa-US0128-qa-20260826T203743Z-fresh` (NEW per US-0048 / BUG-0006; marker reuse = stale isolation evidence)
- `timestamp (UTC)=2026-08-26T20:37:43Z`
- **verdict: QA_PASS**
- `blocking_count=0`
- `non_blocking_count=1` (NB-1: full harness `tests/report.md` timestamp precedes execute — informational)
- `story_status=OPEN` (do not mark US-0128 DONE per US-0045; acceptance L156 unchecked; intake JSON not mutated; architecture.md not mutated this phase)
- `acceptance_L156=NOT ticked`
- `intake_json=NOT mutated`
- `sprints/S0126/uat.json=NOT mutated` (reference fixture only)
- `FRAMEWORK_KIT_REPO=1` (scripts/docs/contract-test slice — no web UI; no fake browser PASS)
- `SECURITY_REVIEW=0`, `CROSS_REPO_OBSERVABILITY=0`, `COMPONENT_SCOPE_MODE=0` (zero overhead)
- `SYNC_POLICY_MODE=disabled` (no push)

## Verdict rationale

Fresh QA independently remapped AC-1..AC-6 against delivered files (not execute summary alone), re-ran the US-0128 contract-test slice (11/11), compose US-0110/US-0104/US-0127 tests (31/31), `--scope=sovereign-convergence` parity, and user-visible metadata guard. All pass green. Compose 8/8 UNCHANGED. Active↔template byte-identical for all eight touched pairs. Canonical `convergence_smoke` step emitted in `sprints/S0128/uat.json` because `contract_test_failed=0`. US-0128 remains OPEN; L156 unchecked; US-0129/US-0130 and DONE rows US-0108/US-0121..US-0127 untouched. Browser/runtime probes for a generated webapp are **not applicable** and are classified `UAT_PROBE_FORBIDDEN` / waived — not silent PASS.

## Test plan

| # | Check | Expected |
|---|---|---|
| 1 | Independent AC-1..AC-6 remap vs files | Each AC has delivered surface + markers |
| 2 | `python -m pytest tests/us0128_contract_test.py -v` | 11/11 PASS |
| 3 | `python scripts/check_intake_template_parity.py --scope=sovereign-convergence` | `[INTAKE_TEMPLATE_PARITY_OK]` |
| 4 | Compose: `pytest tests/us0110_contract_test.py tests/us0104_contract_test.py tests/us0127_contract_test.py` | 31/31 PASS |
| 5 | `python scripts/check-user-visible-metadata.py --repo .` | exit 0 |
| 6 | Active↔template SHA-256 for touched pairs | IDENTICAL |
| 7 | Compose 8/8 (US-0109/US-0126/US-0127/US-0110/US-0104/US-0045/US-0048/US-0056) | UNCHANGED |
| 8 | Status: US-0128 OPEN; L156 unchecked; siblings + DONE rows | unchanged |
| 9 | UAT probes | `contract_tests_primary` PASS; 6 live-runtime classes waived `UAT_PROBE_FORBIDDEN` |
| 10 | Emit `convergence_smoke` in S0128 `uat.json` when `contract_test_failed=0` | present, `result=pass` (do not mutate S0126 uat) |
| 11 | Independent execute proof hash | MATCH `F0EE260C…` before TTL |

## Independent checks (run in this qa subagent)

| Check | Command | Result |
|---|---|---|
| Execute proof SHA-256 | Python hashlib on sorted-key compact lowercase JSON | **MATCH** `F0EE260C2ADF63821C8C22B7699DFDC0C184BFCD8E32B07C8AB720F78ADBBF32`; ttl `2026-08-26T21:30:23Z`; consumed_at `2026-08-26T20:37:43Z` |
| US-0128 contract tests | `python -m pytest tests/us0128_contract_test.py -v` | **11 passed** in 1.53s (11/11 markers green) |
| sovereign-convergence parity | `python scripts/check_intake_template_parity.py --scope=sovereign-convergence` | **exit 0** — `[INTAKE_TEMPLATE_PARITY_OK] scope=sovereign-convergence` |
| US-0110 + US-0104 + US-0127 compose tests | `python -m pytest tests/us0110_contract_test.py tests/us0104_contract_test.py tests/us0127_contract_test.py -q` | **31 passed** in 0.84s |
| User-visible metadata | `python scripts/check-user-visible-metadata.py --repo .` | **exit 0** |
| LINT_COMMAND | (empty in runbook) | **skipped** |
| TYPECHECK_COMMAND | (empty in runbook) | **skipped** |
| TEST_COMMAND full harness `tests/run-tests.ps1` | not re-run this pass | **not claimed** — `tests/report.md` timestamp `2026-08-26T19:13:17Z` (Pass:845 Fail:0) precedes US-0128 execute (`2026-08-26T20:30:23Z`). Slice tests above are the required evidence for this FRAMEWORK_KIT_REPO=1 story. |
| No-secrets grep | `scripts/sovereign_convergence_lib.py` | zero `api_key` / `apikey` / `sk-` / `auth.json` hits |

## AC remap (independent — files + tests, not execute summary)

| AC | Delivered surface | Markers | Result |
|---|---|---|---|
| AC-1 Surrogate eval | `scripts/sovereign_convergence_lib.py` `_eval_smoke_green`: legacy `_uat_smoke_passes` first; surrogate when 6 `UAT_PROBE_FORBIDDEN` waivers + `contract_test_failed=0` + `convergence_smoke` (or tail `probe_kind=contract_tests_primary`); `_uat_smoke_passes` / `_step_is_smoke` unchanged | m1, m2, m3, m4, m5, m6, m8, m9 | **PASS** |
| AC-2 Canonical uat step | `.cursor/commands/qa.md` + `verify-work.md` `### Convergence smoke surrogate (US-0128)` after Browser UAT, before Steps; this QA pass emits `id=convergence_smoke` in `sprints/S0128/uat.json` | m5, m7, m8 + this-pass emission | **PASS** |
| AC-3 Fail closed | `reason_codes.md` `## US-0128` `CONVERGENCE_SMOKE_SURROGATE_MISSING`; lib fail-closed when no smoke step / incomplete waivers / harness red; `CONVERGENCE_SMOKE_PROBE_FAIL` retained for real smoke fail | m2, m3, m4, m6 | **PASS** |
| AC-4 Command contracts | additive qa.md + verify-work.md subsections (+ template mirrors); emission rule for waived-probe slices | m5, m7, m8 | **PASS** |
| AC-5 Contract tests | `tests/us0128_contract_test.py` 11 `test_us0128_*` markers (static/fixture; no live critic spawn) | all 11 | **PASS** (11/11 this run) |
| AC-6 Operator docs + parity | runbook `### Smoke surrogate for waived-probe UAT slices (US-0128)`; `SOVEREIGN_CONVERGENCE_PAIRS` +2 command rows; `--scope=sovereign-convergence` | m8 + parity CLI | **PASS** |

## Contract marker results (11/11)

| # | Marker | AC | Result |
|---|---|---|---|
| 1 | `test_us0128_surrogate_passes_when_all_six_waived_and_green` | AC-1/AC-5 | PASS |
| 2 | `test_us0128_surrogate_missing_when_no_step` | AC-1/AC-3/AC-5 | PASS |
| 3 | `test_us0128_surrogate_missing_when_harness_fail` | AC-1/AC-3/AC-5 | PASS |
| 4 | `test_us0128_surrogate_missing_when_partial_waivers` | AC-1/AC-3/AC-5 | PASS |
| 5 | `test_us0128_real_smoke_step_pass_wins_over_surrogate` | AC-1/AC-5 | PASS |
| 6 | `test_us0128_real_smoke_step_fail_uses_probe_fail_not_surrogate_missing` | AC-1/AC-3/AC-5 | PASS |
| 7 | `test_us0128_compose_us0109_deploy_smoke_unchanged` | AC-5 | PASS |
| 8 | `test_us0128_template_parity_convergence_lib_and_commands` | AC-5/AC-6 | PASS |
| 9 | `test_us0128_compose_us0110_five_conjunct_unchanged` | AC-5 | PASS |
| 10 | `test_us0128_compose_us0127_critic_conjunct_unchanged` | AC-5 | PASS |
| 11 | `test_us0128_compose_us0126_waived_probe_fixture_reference_only` | AC-5 | PASS |

## Template byte-identity (touched pairs)

| Pair | Bytes | Result |
|---|---|---|
| `scripts/sovereign_convergence_lib.py` ↔ template | 40493b = 40493b | IDENTICAL |
| `scripts/sovereign_convergence_validate.py` ↔ template | 6800b = 6800b | IDENTICAL |
| `.cursor/commands/qa.md` ↔ template | 13453b = 13453b | IDENTICAL |
| `.cursor/commands/verify-work.md` ↔ template | 9257b = 9257b | IDENTICAL |
| `docs/engineering/runbook.md` ↔ template | 209033b = 209033b | IDENTICAL |
| `docs/engineering/reason_codes.md` ↔ template | 32578b = 32578b | IDENTICAL |
| `scripts/check_intake_template_parity.py` ↔ template | 23914b = 23914b | IDENTICAL |
| `tests/us0128_contract_test.py` ↔ template | 15677b = 15677b | IDENTICAL |

## Compose guards (8/8 UNCHANGED)

| Story | Surface | Verification | Result |
|---|---|---|---|
| US-0109 | deploy smoke path | marker 7 PASS; surrogate does not activate when deploy smoke applies | UNCHANGED |
| US-0126 | `sprints/S0126/uat.json` waived-probe fixture | marker 11 PASS; this QA pass did not mutate S0126 uat | UNCHANGED |
| US-0127 | `_eval_critic_resolved` / `SOVEREIGN_CRITIC_PAIRS` | marker 10 PASS; `SOVEREIGN_CRITIC_PAIRS` still hygiene-only | UNCHANGED |
| US-0110 | five-conjunct identity | `CONVERGENCE_CONJUNCTS = (backlog_clear, zero_deferrals, critic_resolved, smoke_green, ledger_clean)`; `REASON_CODES` still 10; `CONVERGENCE_SMOKE_SURROGATE_MISSING` additive outside that inventory | UNCHANGED |
| US-0104 | critic findings / `read_open_blocking` | compose tests 31/31 include us0104; not in execute touch list | UNCHANGED |
| US-0045 | DONE/acceptance | US-0128 Status OPEN L4445; L156 unchecked; US-0129/US-0130 OPEN unchecked; US-0127 DONE (L155 checked); US-0108/US-0121..US-0126 DONE preserved | UNCHANGED |
| US-0048 / BUG-0006 | isolation | NEW marker `qa-US0128-qa-20260826T203743Z-fresh` (not reused) | UNCHANGED |
| US-0056 | intake JSON | `handoffs/intake_evidence/US-0128-intake-20260825.json` not mutated this phase | UNCHANGED |

## Findings

### Blocking

None. `blocking_count=0`.

### Non-blocking

- **NB-1** (informational): `tests/report.md` Timestamp `2026-08-26T19:13:17Z` (Pass:845 Fail:0) precedes US-0128 execute `2026-08-26T20:30:23Z`. This QA pass did not re-run `tests/run-tests.ps1`. Slice pytest 11/11 is the required FRAMEWORK_KIT_REPO=1 evidence. Canonical T-002 `convergence_smoke.evidence_ref` still uses the contracted token `tests/report.md Fail:0 + uat.json waived_probes[] (6 classes, UAT_PROBE_FORBIDDEN)`. Do not claim a live full-harness Fail:0 from this pass.

Critic NB awareness (not new QA findings): `a0128ex-challenger-001` (legacy-first `_eval_smoke_green`; `id=convergence_smoke` also matches `_step_is_smoke`); `a0128ex-architect-002` (layering; no lib-side uat synthesis); `a0128ex-subtractor-003` (T-anch ceremony; T-007/T-004 overlap doc-only).

## UAT probes (FRAMEWORK_KIT_REPO=1 — honest classification)

Applicable probe class: **`contract_tests_primary`** (11 markers). No web UI. No fake browser PASS.

Canonical surrogate step **`convergence_smoke`** emitted this pass (`result=pass`) because `contract_test_failed=0`.

| Probe class | Result | reason_code |
|---|---|---|
| `contract_tests_primary` | PASS (11/11) | `UAT_PROBE_PASS` |
| `browser_smoke` | waived / not applicable | `UAT_PROBE_FORBIDDEN` |
| `api_health` | waived / not applicable | `UAT_PROBE_FORBIDDEN` |
| `process_health` | waived / not applicable | `UAT_PROBE_FORBIDDEN` |
| `cli_smoke` | not applicable (lib + commands; verified via contract tests) | `UAT_PROBE_FORBIDDEN` |
| `build` | not applicable | `UAT_PROBE_FORBIDDEN` |
| `manual_operator` | not applicable | `UAT_PROBE_FORBIDDEN` |

**Runtime browser evidence**: none. MCP browser sequence **not run**. No screenshot. No silent browser PASS.

## Runtime QA evidence (US-0065) — kit slice, not generated webapp

- `runtime_startup_command`: n/a (FRAMEWORK_KIT_REPO=1; no app server)
- `runtime_stack_profile`: python (scripts/docs kit)
- `runtime_mode`: local
- `runtime_health_target`: n/a — no process/endpoint
- `runtime_health_result`: not_applicable
- `runtime_log_summary`: n/a (no app logs)
- `runtime_retry_count`: 0
- `runtime_retry_ledger`: []
- `runtime_final_verdict`: pass
- `runtime_reason_code`: `UAT_PROBE_FORBIDDEN` for browser/runtime-app probes; slice health is contract tests + `convergence_smoke` surrogate
- `runtime_evidence_refs`: pytest 11/11; parity CLI `--scope=sovereign-convergence`; compose 31/31; `sprints/S0128/uat.json` `convergence_smoke`

## Generated-test evidence (US-0066)

- `generated_test_stack_profile`: python
- `generated_test_command`: `python -m pytest tests/us0128_contract_test.py -v`
- `generated_test_result`: pass
- `generated_test_output_ref`: this file § Independent checks (11 passed in 1.53s)
- `generated_test_paths_ref`: `tests/us0128_contract_test.py`
- `generated_test_reason_code`: none (pass)

## Status confirmation (US-0045)

- backlog `## US-0128` Status: **OPEN** (L4445)
- acceptance L156: **unchecked**
- US-0129 Status OPEN (L4482); L157 unchecked
- US-0130 Status OPEN (L4514); L158 unchecked
- US-0127 DONE (acceptance L155 checked)
- US-0108 DONE; US-0121..US-0126 DONE
- intake JSON not mutated this phase
- architecture.md `# US-0128` not mutated this phase
- `sprints/S0126/uat.json` not mutated this phase

## Producer proof consumed (execute)

- `producer_runtime_proof_id=rp-auto-20260826-01-execute-dev-20260826T203023Z-US-0128`
- Canonical payload independently hashed: `{"delivery_mode":"ultra_lean","macro_phase":"build+verify","model_id":"cursor-grok-4.6-high","orchestrator_run_id":"auto-20260826-01","phase_id":"execute","proof_issued_at":"2026-08-26T20:30:23Z","proof_ttl_seconds":3600,"role":"dev","runtime_proof_id":"rp-auto-20260826-01-execute-dev-20260826T203023Z-US-0128","sprint_id":"S0128","story_id":"US-0128"}`
- `producer_attested_proof_hash=F0EE260C2ADF63821C8C22B7699DFDC0C184BFCD8E32B07C8AB720F78ADBBF32`
- Independent SHA-256 recompute: **MATCH**
- `producer_proof_ttl=2026-08-26T21:30:23Z`, `consumed_at=2026-08-26T20:37:43Z` (before RUNTIME_PROOF_STALE)
- `producer_ttl_stale=false`

## Strict runtime proof (DEC-0038) — qa

- `orchestrator_run_id=auto-20260826-01`
- `runtime_proof_id=rp-auto-20260826-01-qa-qa-20260826T203743Z-US-0128` (NEW — distinct from execute `...203023Z...`; no proof_id reuse)
- `phase_id=qa`, `role=qa`, `story_id=US-0128`, `sprint_id=S0128`
- `delivery_mode=ultra_lean`, `macro_phase=build+verify`, `model_id=cursor-grok-4.6-high`
- `proof_issued_at=2026-08-26T20:37:43Z`
- `proof_ttl_seconds=3600`, `proof_ttl=2026-08-26T21:37:43Z` (UTC = issued_at + 3600s)
- `proof_hash=CE9A73B8CC6EA0E8CEB1FBC02459F1B3CFACB420B6716814244D619B414861BC` (SHA-256 of sorted-key compact lowercase-keys JSON payload, UTF-8 bytes via Python 3.12 hashlib; independently recomputed MATCH before return)
- Canonical payload: `{"delivery_mode":"ultra_lean","macro_phase":"build+verify","model_id":"cursor-grok-4.6-high","orchestrator_run_id":"auto-20260826-01","phase_id":"qa","proof_issued_at":"2026-08-26T20:37:43Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260826-01-qa-qa-20260826T203743Z-US-0128","sprint_id":"S0128","story_id":"US-0128"}`

## Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

- `phase_id=qa`, `role=qa`, `model_id=cursor-grok-4.6-high` (CROSS_MODEL_REVIEW=1 — required)
- `fresh_context_marker=qa-US0128-qa-20260826T203743Z-fresh` (NEW per US-0048 / BUG-0006)
- `timestamp=2026-08-26T20:37:43Z` (UTC)
- `evidence_ref=sprints/S0128/qa-findings.md`
- Fresh qa subagent per BUG-0006 / US-0048 isolation; no prior chat history carried forward. Context limited to narrow-read (US-0053). No `.env` reads, no credentials access, no intake-evidence mutation, no backlog Status/AC mutation, no acceptance.md mutation, no architecture.md mutation, no DONE-row mutation, no US-0129/US-0130 mutation, no S0126 uat mutation, no `/execute` or `/verify-work` spawn from this subagent.

## Next scheduled phase

- `next_scheduled_phase=/verify-work` (role=qa per US-0069 / DEC-0051; fresh qa subagent per BUG-0006 — orchestrator-owned spawn; after sovereign-critic of qa if CROSS_MODEL_REVIEW=1)
- `next_scheduled_role=qa`
- `stop_condition=STOP after qa PASS. Orchestrator spawns sovereign-critic of qa (CROSS_MODEL_REVIEW=1), then /verify-work in a fresh qa subagent (BUG-0006). Do NOT spawn /verify-work or /execute from this subagent. Do NOT mark US-0128 DONE. Do NOT tick acceptance L156. Do NOT mutate intake JSON. Do NOT amend US-0104/US-0110/US-0109/US-0126/US-0127 surfaces. Do NOT mutate US-0129/US-0130. Do NOT mutate sprints/S0126/uat.json.`
- `artifacts_written=sprints/S0128/qa-findings.md, sprints/S0128/uat.json, sprints/S0128/uat.md, docs/engineering/state.md (qa checkpoint append), handoffs/resume_brief.md (qa PASS prepend → /verify-work)`
- `handoffs/qa_to_dev.md=NOT written` (no blocking findings; AUTO_IMPLEMENTATION_LOOP does not return to /execute)
