# QA findings — BUG-0015 / S0131 / auto-20260906-bug0015 (qa)

- **phase_id**: qa, **role**: qa, **bug_id**: BUG-0015 (OPEN — not marked DONE per US-0045), **sprint_id**: S0131
- `orchestrator_run_id=auto-20260906-bug0015`, `delivery_mode=ultra_lean`, `macro_phase=build+verify`
- `AUTO_IMPLEMENTATION_LOOP=1`
- `model_id=composer-2.5` (CROSS_MODEL_REVIEW=1 — required on isolation)
- `producer_phase_id=execute`, `producer_role=dev`, `producer_model_id=composer-2.5`
- `critic_phase_id=sovereign-critic` (execute review), `critic_model_id=composer-2.5-fast`, `critic_verdict=PASS`, `anti_slop_aggregate=8`, `open_blocking_findings=0`
- `critic_fresh_context_marker=critic-BUG0015-execute-20260906T145000Z-fresh`
- `fresh_context_marker=qa-BUG0015-qa-20260906T145500Z-fresh` (NEW per US-0048 / BUG-0006; not reused from producer/critic markers)
- `timestamp (UTC)=2026-09-06T14:55:00Z`
- **verdict: QA_PASS**
- `plan_verify_verdict=PASS` (ultra_lean deferred — `sprints/S0131/plan-verify.json`; AC surjective 8/8)
- `blocking_count=0`
- `non_blocking_count=3` (execute-critic carry-forwards — informational; not new blockers)
- `story_status=OPEN` (do not mark BUG-0015 DONE; acceptance L180 unchecked; intake JSON not mutated)
- `acceptance_L180=NOT ticked`
- `intake_json=NOT mutated`
- `FRAMEWORK_KIT_REPO=1` / OpenCode plugin contract story — no web UI; **no fake browser PASS**
- `SECURITY_REVIEW=0`, `CROSS_REPO_OBSERVABILITY=0`, `COMPONENT_SCOPE_MODE=0`

## Verdict rationale

Fresh QA independently remapped AC-1..AC-8 against architecture `# BUG-0015` + tasks.md, created deferred `plan-verify.json` (PASS / surjective), and re-ran contract + compose gates. All green. Active↔template pairs byte-identical. Compose DEC-0124/0125 untouched. Status OPEN preserved. Canonical probe class = `contract_tests_primary` (7 markers). Live OpenCode / browser probes waived (`UAT_PROBE_FORBIDDEN`). `convergence_smoke` surrogate emitted because `contract_test_failed=0`.

## Test plan

| # | Check | Expected |
|---|---|---|
| 1 | Independent AC-1..AC-8 remap vs architecture + tasks | Each AC ≥1 task + marker |
| 2 | Create `sprints/S0131/plan-verify.json` (ultra_lean deferred) | PASS / surjective 8/8 |
| 3 | `python -m pytest tests/bug0015_contract_test.py -v` | 7/7 PASS |
| 4 | `python -m pytest tests/us0124_contract_test.py -q` | 12/12 PASS (compose) |
| 5 | `python scripts/check_intake_template_parity.py --scope=bug-0015` | `[INTAKE_TEMPLATE_PARITY_OK]` |
| 6 | `python scripts/enforce-triad-hot-surface.py --check` | exit 0 |
| 7 | `python scripts/check-user-visible-metadata.py --repo . --json` | OK / 0 violations |
| 8 | Active↔template byte identity (touched pairs) | IDENTICAL |
| 9 | Status OPEN; L180 unchecked; BUG-0016 untouched | unchanged |
| 10 | UAT probes | `contract_tests_primary` PASS; live classes waived |
| 11 | Emit `convergence_smoke` when `contract_test_failed=0` | present, `result=pass` |
| 12 | Independent execute proof hash | MATCH `1E8BF777…` before TTL 15:45:00Z |

## Independent checks (this qa subagent)

| Check | Command / method | Result |
|---|---|---|
| Execute proof SHA-256 | Python hashlib sorted-key compact JSON | **MATCH** `1E8BF77730FB73CD94657EA5A0287E8F769F31C0CCD2EF81370181AD641D9CB0`; ttl `2026-09-06T15:45:00Z`; consumed_at `2026-09-06T14:55:00Z` |
| BUG-0015 contract tests | `python -m pytest tests/bug0015_contract_test.py -v` | **7 passed** in 0.70s |
| US-0124 compose tests | `python -m pytest tests/us0124_contract_test.py -q` | **12 passed** in 1.37s |
| Parity scope bug-0015 | `python scripts/check_intake_template_parity.py --scope=bug-0015` | **exit 0** — `[INTAKE_TEMPLATE_PARITY_OK]` |
| Triad hot-surface | `python scripts/enforce-triad-hot-surface.py --check` | **exit 0** |
| User-visible metadata | `python scripts/check-user-visible-metadata.py --repo . --json` | **OK** / `violations: []` |
| Full harness `tests/run-tests.ps1` | not re-run this pass | **not claimed** — slice contract tests are the required evidence for this plugin contract story |

## AC remap (independent)

| AC | Delivered surface | Task(s) / markers | Result |
|---|---|---|---|
| AC-1 `/auto` starts spawn via attach | `command.transform` → `editor.add({ name: "auto", execute })` → `runAutoLifecycle` | T-001, T-002; m1, m2 | **PASS** |
| AC-2 Missing attach fail-closed | `OPENCODE_PLUGIN_DISPATCH_ATTACH_UNSUPPORTED` + runbook stub | T-001, T-006; m3 | **PASS** |
| AC-3 Missing `session.create` | `OPENCODE_PLUGIN_SPAWN_UNSUPPORTED` | T-002; m4 | **PASS** |
| AC-4 IsolationEvidence + state.md | Python `opencode_auto_bridge.py`; marker 2 evidence fields | T-003; m2 | **PASS** (see NB-1 soft-continue residual) |
| AC-5 Concurrent `/auto` mutex | `OPENCODE_AUTO_ALREADY_RUNNING`; TTL `Date.now()` 7200s; clear-on-exit | T-002, T-006; m5 | **PASS** |
| AC-6 `auto.md` dispatch-only | ≤20 lines; no spawn literals; active+template | T-004; m6 | **PASS** |
| AC-7 Compose US-0124 spawn API | marker 7; DEC-0124/0125 bodies unchanged | T-anch; m7 | **PASS** |
| AC-8 Seven additive markers | `tests/bug0015_contract_test.py` 7/7 | T-005 | **PASS** |

## Contract marker results (7/7)

| # | Marker | Result |
|---|---|---|
| 1 | `test_bug0015_command_transform_registers_auto` | PASS |
| 2 | `test_bug0015_auto_execute_invokes_spawn_phase` | PASS |
| 3 | `test_bug0015_missing_attach_fail_closed` | PASS |
| 4 | `test_bug0015_missing_session_create_fail_closed` | PASS |
| 5 | `test_bug0015_concurrent_reentry_fail_closed` | PASS |
| 6 | `test_bug0015_auto_md_dispatch_only_static` | PASS |
| 7 | `test_bug0015_compose_us0124_spawn_api_unchanged` | PASS |

## Template byte-identity (touched pairs)

| Pair | Bytes | Result |
|---|---|---|
| `.opencode/plugins/orchestrator.ts` ↔ template | 23832b = 23832b | IDENTICAL |
| `.opencode/commands/auto.md` ↔ template | 225b = 225b | IDENTICAL |
| `tests/bug0015_contract_test.py` ↔ template | 6736b = 6736b | IDENTICAL |
| `docs/engineering/runbook.md` ↔ template | 211430b = 211430b | IDENTICAL |
| `scripts/opencode_auto_bridge.py` ↔ template | 8096b = 8096b | IDENTICAL |
| `scripts/check_intake_template_parity.py` ↔ template | 25902b = 25902b | IDENTICAL |

## Findings

### Blocking

None. `blocking_count=0`. No `handoffs/qa_to_dev.md`.

### Non-blocking (execute-critic carry-forwards)

- **NB-1** (`b0015ex-challenger-001` / `ik_bug0015_execute_edge_and_proof`): First-phase Python bridge miss soft-falls to `phase_id=execute`; `persistIsolationViaPython` `DRIVER_INVOKE_FAILED` does not fail-close lifecycle (only `OPENCODE_SUBTASK_IGNORED` does). Documented in plan-verify AC-4 check; not a coverage gap; no 8th marker required (architecture DQ6 locked at 7).
- **NB-2** (`b0015ex-architect-002` / `ik_bug0015_execute_layer_coupling`): `event.subscribe` alone can set `attachSupported` when transform missing — intended CF1/CF6 secondary defense; primary remains `command.transform` execute. Confirmed intended; not blocking.
- **NB-3** (`b0015ex-subtractor-003` / `ik_bug0015_execute_scope_minimal`): Scope discipline held — no BUG-0016 / live OpenCode probe / DEC amend / DONE flip. Informational.

## UAT probes (plugin contract — honest classification)

Applicable probe class: **`contract_tests_primary`** (7 markers). No web UI. **No fake browser PASS.** Live-runtime probes **not attempted** (`UAT_PROBE_FORBIDDEN`).

Canonical surrogate step **`convergence_smoke`** emitted (`result=pass`) because `contract_test_failed=0`.

| Probe class | Result | reason_code |
|---|---|---|
| `contract_tests_primary` | PASS (7/7) | `UAT_PROBE_PASS` |
| `browser_smoke` | waived / not applicable | `UAT_PROBE_FORBIDDEN` |
| `api_health` | waived / not applicable | `UAT_PROBE_FORBIDDEN` |
| `process_health` | waived / not applicable | `UAT_PROBE_FORBIDDEN` |
| `cli_smoke` | waived (mock-ctx harness only; no live OpenCode CLI probe) | `UAT_PROBE_FORBIDDEN` |
| `build` | not applicable | `UAT_PROBE_FORBIDDEN` |
| `manual_operator` | not applicable | `UAT_PROBE_FORBIDDEN` |

**Runtime browser evidence**: none. MCP browser sequence **not run**. No screenshot. No silent browser PASS.

## Runtime QA evidence (US-0065)

- `runtime_stack_profile`: `node` (plugin TypeScript; harness via pytest → `tests/bug0015/run_harness.mjs`)
- `runtime_mode`: local
- `runtime_startup_command`: driven via `python -m pytest tests/bug0015_contract_test.py -v`
- `runtime_health_target`: Node mock-ctx harness exit + 7/7 markers
- `runtime_health_result`: PASS (7 passed in 0.70s)
- `runtime_log_summary`: 0 errors / 0 warnings / 7 pass
- `runtime_retry_count`: 0
- `runtime_retry_ledger`: []
- `runtime_final_verdict`: pass
- `runtime_reason_code`: `UAT_PROBE_FORBIDDEN` for live OpenCode/browser; health = contract tests + `convergence_smoke`
- `runtime_evidence_refs`: pytest 7/7; us0124 12/12; parity `--scope=bug-0015`; `sprints/S0131/uat.json` `convergence_smoke`

## Generated-test evidence (US-0066)

- `generated_test_stack_profile`: python
- `generated_test_command`: `python -m pytest tests/bug0015_contract_test.py -v`
- `generated_test_result`: pass
- `generated_test_output_ref`: this file § Independent checks (7 passed in 0.70s)
- `generated_test_paths_ref`: `tests/bug0015_contract_test.py`
- `generated_test_reason_code`: none (pass)

## Status confirmation (US-0045)

- backlog `### BUG-0015` Status: **OPEN** (L4899)
- acceptance L180: **unchecked**
- BUG-0016 remains OPEN / out of scope
- intake JSON not mutated
- architecture.md `# BUG-0015` not mutated this phase
- DEC-0124 / DEC-0125 bodies not mutated

## Plan-verify (ultra_lean merged)

- path: `sprints/S0131/plan-verify.json`
- verdict: **PASS**
- coverage_complete: true
- uncovered_acs: []
- plan-verify runtime_proof_id: `rp-auto-20260906-bug0015-plan-verify-qa-20260906T145500Z-BUG-0015`
- plan-verify proof_hash: `B9462F769BD5CBB61D3FD41769BA1B669ACF44296A5724861F87D9F208226BC5`

## Producer proof consumed (execute)

- `producer_runtime_proof_id=rp-auto-20260906-bug0015-execute-dev-20260906T144500Z-BUG-0015`
- Canonical payload: `{"delivery_mode":"ultra_lean","macro_phase":"build+verify","model_id":"composer-2.5","orchestrator_run_id":"auto-20260906-bug0015","phase_id":"execute","proof_issued_at":"2026-09-06T14:45:00Z","proof_ttl_seconds":3600,"role":"dev","runtime_proof_id":"rp-auto-20260906-bug0015-execute-dev-20260906T144500Z-BUG-0015","sprint_id":"S0131","story_id":"BUG-0015"}`
- `producer_attested_proof_hash=1E8BF77730FB73CD94657EA5A0287E8F769F31C0CCD2EF81370181AD641D9CB0`
- Independent SHA-256 recompute: **MATCH**
- `producer_proof_ttl=2026-09-06T15:45:00Z`, `consumed_at=2026-09-06T14:55:00Z` (before RUNTIME_PROOF_STALE)

## Strict runtime proof (DEC-0038) — qa

- `orchestrator_run_id=auto-20260906-bug0015`
- `runtime_proof_id=rp-auto-20260906-bug0015-qa-qa-20260906T145500Z-BUG-0015`
- `phase_id=qa`, `role=qa`, `story_id=BUG-0015`, `sprint_id=S0131`
- `proof_issued_at=2026-09-06T14:55:00Z`
- `proof_ttl_seconds=3600`, `proof_ttl=2026-09-06T15:55:00Z`
- `proof_hash=B2924E1E4F3B1E750491884C7F1226E6DA15F24C9421333914394386AA4E35FB`
- Canonical payload: `{"delivery_mode":"ultra_lean","macro_phase":"build+verify","model_id":"composer-2.5","orchestrator_run_id":"auto-20260906-bug0015","phase_id":"qa","proof_issued_at":"2026-09-06T14:55:00Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260906-bug0015-qa-qa-20260906T145500Z-BUG-0015","sprint_id":"S0131","story_id":"BUG-0015"}`

## Isolation evidence (US-0048 / DEC-0029)

- `phase_id=qa`
- `role=qa`
- `model_id=composer-2.5` (CROSS_MODEL_REVIEW=1)
- `fresh_context_marker=qa-BUG0015-qa-20260906T145500Z-fresh`
- `timestamp=2026-09-06T14:55:00Z`
- `evidence_ref=sprints/S0131/qa-findings.md + sprints/S0131/plan-verify.json + sprints/S0131/uat.json + handoffs/qa_to_verify.md + handoffs/resume_brief.md + docs/engineering/state.md`

## Next phase

- **PASS → `/verify-work`** (fresh qa subagent per BUG-0006). Do NOT mark BUG-0015 DONE. Do NOT tick acceptance L180. Do NOT mutate intake JSON. Do NOT solve BUG-0016. Do NOT spawn `/verify-work` from this qa subagent.
