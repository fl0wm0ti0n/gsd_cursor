# QA findings — US-0129 / S0129 / auto-20260827-01 (qa)

- **phase_id**: qa, **role**: qa, **story_id**: US-0129 (OPEN — not marked DONE per US-0045), **sprint_id**: S0129
- `orchestrator_run_id=auto-20260827-01`, `delivery_mode=ultra_lean`, `macro_phase=build+verify`
- `AUTO_IMPLEMENTATION_LOOP=1`
- `model_id=cursor-grok-4.6-high` (CROSS_MODEL_REVIEW=1 — required on isolation)
- `producer_phase_id=execute`, `producer_role=dev`, `producer_model_id=cursor-grok-4.6-high`
- `critic_phase_id=sovereign-critic` (execute review), `critic_model_id=composer-2.5-fast`, `critic_verdict=PASS`, `anti_slop_aggregate=8`, `open_blocking_findings=0`
- `critic_fresh_context_marker=tl-US0129-sovereign-critic-execute-20260827T081100Z-fresh`
- `fresh_context_marker=qa-US0129-qa-20260827T081557Z-fresh` (NEW per US-0048 / BUG-0006; marker reuse = stale isolation evidence)
- `timestamp (UTC)=2026-08-27T08:15:57Z`
- **verdict: QA_PASS**
- `blocking_count=0`
- `non_blocking_count=1` (NB-1: full harness `tests/report.md` timestamp precedes execute — informational)
- `story_status=OPEN` (do not mark US-0129 DONE per US-0045; acceptance L157 unchecked; intake JSON not mutated; architecture.md not mutated this phase)
- `acceptance_L157=NOT ticked`
- `intake_json=NOT mutated`
- `FRAMEWORK_KIT_REPO=1` (scripts/docs/tests slice — no web UI; no fake browser PASS)
- `SECURITY_REVIEW=0`, `CROSS_REPO_OBSERVABILITY=0`, `COMPONENT_SCOPE_MODE=0` (zero overhead)
- `SPEC_PACK_MODE=0`, `USER_GUIDE_MODE=0`, `REMOTE_EXECUTION=0`
- `SYNC_POLICY_MODE=disabled` (no push)

## Verdict rationale

Fresh QA independently remapped AC-1..AC-6 against delivered files (not execute summary alone), re-ran the US-0129 contract-test slice (8/8), `--scope=arch-linkage` parity, and user-visible metadata guard. All pass green. Compose 8/8 UNCHANGED. Active↔template byte-identical for all ten touched pairs checked. Canonical `convergence_smoke` step emitted in `sprints/S0129/uat.json` because `contract_test_failed=0`. US-0129 remains OPEN; L157 unchecked; DONE rows US-0126/US-0127/US-0128/US-0130 preserved. Browser/runtime probes for a generated webapp are **not applicable** and are classified `UAT_PROBE_FORBIDDEN` / waived — not silent PASS. Live-runtime probes were not attempted. Probe class is **`contract_tests_primary`**.

## Test plan

| # | Check | Expected |
|---|---|---|
| 1 | Independent AC-1..AC-6 remap vs files | Each AC has delivered surface + markers |
| 2 | `python -m pytest tests/us0129_contract_test.py -v` | 8/8 PASS |
| 3 | `python scripts/check_intake_template_parity.py --scope=arch-linkage` | `[INTAKE_TEMPLATE_PARITY_OK]` |
| 4 | `python scripts/check-user-visible-metadata.py --repo .` | exit 0 |
| 5 | Active↔template SHA-256/bytes for touched pairs | IDENTICAL |
| 6 | Compose 8/8 (DEC-0054/DEC-0073/DEC-0076/US-0049/US-0126/US-0127/US-0128/US-0130/DEC-0119/R-0112) | UNCHANGED |
| 7 | Status: US-0129 OPEN; L157 unchecked; DONE rows | unchanged |
| 8 | UAT probes | `contract_tests_primary` PASS; 6 live-runtime classes waived `UAT_PROBE_FORBIDDEN` |
| 9 | Emit `convergence_smoke` in S0129 `uat.json` when `contract_test_failed=0` | present, `result=pass` |
| 10 | Independent execute proof hash | MATCH `CFE682EA…` before TTL 09:04:38Z |
| 11 | No live `ARCH_LINKAGE_AUTO_REPAIR=1`; flag not in `AUTONOMY_PRESET` | PASS |

## Independent checks (run in this qa subagent)

| Check | Command | Result |
|---|---|---|
| Execute proof SHA-256 | Python hashlib on sorted-key compact lowercase JSON | **MATCH** `CFE682EA7A8A7A8EF5A9486F7A9E04FAAC2F9DB6425147CA3D8B7B77F413CE4F`; ttl `2026-08-27T09:04:38Z`; consumed_at `2026-08-27T08:15:57Z` |
| US-0129 contract tests | `python -m pytest tests/us0129_contract_test.py -v` | **8 passed** in 0.57s (8/8 markers green) |
| arch-linkage parity | `python scripts/check_intake_template_parity.py --scope=arch-linkage` | **exit 0** — `[INTAKE_TEMPLATE_PARITY_OK] scope=arch-linkage` |
| User-visible metadata | `python scripts/check-user-visible-metadata.py --repo .` | **exit 0** |
| LINT_COMMAND | (empty in runbook) | **skipped** |
| TYPECHECK_COMMAND | (empty in runbook) | **skipped** |
| TEST_COMMAND full harness `tests/run-tests.ps1` | not re-run this pass | **not claimed** — `tests/report.md` timestamp `2026-08-26T22:41:33Z` (Pass:845 Fail:0) precedes US-0129 execute (`2026-08-27T08:04:38Z`). Slice tests above are the required evidence for this FRAMEWORK_KIT_REPO=1 story. |
| No-secrets grep | `scripts/arch_linkage_guard.py` + `tests/us0129_contract_test.py` | zero `api_key` / `apikey` / `sk-` / `auth.json` hits |
| Live `ARCH_LINKAGE_AUTO_REPAIR=1` | committed scratchpad | **none** (comment `# ARCH_LINKAGE_AUTO_REPAIR: 0\|1 (default=0)` only) |
| `ARCH_LINKAGE_AUTO_REPAIR` in `AUTONOMY_FLAGS` | `scripts/autonomy_preset_lib.py` 12 flags | **absent** (12-flag set unchanged) |

## AC remap (independent — files + tests, not execute summary)

| AC | Delivered surface | Markers | Result |
|---|---|---|---|
| AC-1 Linkage guard script | `scripts/arch_linkage_guard.py` (+ template) imports `split_arch_stories`; `discover_required_arch_headings` stdlib-scans `tests/**/*_test.py` (excludes `tests/.tmp*`); `--pre` / `--post` wrap `--rollover` | m1, m2, m6 | **PASS** |
| AC-2 Fail-closed block | `reason_codes.md` `## US-0129` `ARCH_LINKAGE_ROLLOVER_BLOCKED`; matrix `security_hard` `auto_repair_kind=n/a` `cap=0`; pre-guard emits metadata (story/bug id, missing heading, pack path, remediation) and does not write archive | m2, m3 | **PASS** |
| AC-3 Optional auto-repair | Scratchpad comment default-off; no live `=1`; not in `AUTONOMY_PRESET`; DQ8 H1 stub + pack_ref before US-0089/US-0090 tail; idempotent | m4, m5 | **PASS** |
| AC-4 Rollover wiring | `/refresh-context` step 4: pre-guard → `--rollover` → post-guard → `--check`; runbook h3 under triad; `--scope=arch-linkage` | m6, m7 | **PASS** |
| AC-5 Regression tests | `tests/us0129_contract_test.py` 8 `test_us0129_*` markers; harness **26AB** in `run-tests.ps1` / `run-tests.sh`; B-1 unprotected rollover FAIL | all 8 (esp. m8) | **PASS** (8/8 this run) |
| AC-6 Compose | architecture.md `# US-0129` L1527 not mutated this phase; DEC-0054 split/pack/`ARCH_HOT_MAX_*` import/call only; US-0126 B-1 fixture only; US-0127/US-0128/US-0130 DONE; DEC-0119 12 flags / 9 kinds; L157 unchecked | T-anch + this-pass status | **PASS** |

## Contract marker results (8/8)

| # | Marker | AC | Result |
|---|---|---|---|
| 1 | `test_us0129_guard_discovers_contract_heading_set` | AC-1 | PASS |
| 2 | `test_us0129_pre_rollover_blocks_before_archive_write` | AC-1 / AC-2 | PASS |
| 3 | `test_us0129_block_emits_arch_linkage_rollover_blocked_metadata` | AC-2 | PASS |
| 4 | `test_us0129_auto_repair_default_off` | AC-3 | PASS |
| 5 | `test_us0129_auto_repair_restores_h1_stub_idempotent` | AC-3 | PASS |
| 6 | `test_us0129_post_rollover_verifies_active_linkage` | AC-1 / AC-4 | PASS |
| 7 | `test_us0129_refresh_context_wires_pre_post_guard` | AC-4 | PASS |
| 8 | `test_us0129_b1_regression_unprotected_rollover_fails` | AC-5 | PASS |

## Template byte-identity (touched pairs)

| Pair | Bytes | Result |
|---|---|---|
| `scripts/arch_linkage_guard.py` ↔ template | 16243b = 16243b | IDENTICAL |
| `.cursor/commands/refresh-context.md` ↔ template | 5793b = 5793b | IDENTICAL |
| `tests/us0129_contract_test.py` ↔ template | 13138b = 13138b | IDENTICAL |
| `docs/engineering/reason_codes.md` ↔ template | 34061b = 34061b | IDENTICAL |
| `docs/engineering/runbook.md` ↔ template | 210676b = 210676b | IDENTICAL |
| `.cursor/scratchpad.md` ↔ template | 36350b = 36350b | IDENTICAL |
| `.cursor/scratchpad.local.example.md` ↔ template | 35898b = 35898b | IDENTICAL |
| `docs/engineering/autonomy-stop-matrix.md` ↔ template | 6133b = 6133b | IDENTICAL |
| `docs/engineering/context/installer-owned-paths.manifest` ↔ template | 4218b = 4218b | IDENTICAL |
| `scripts/check_intake_template_parity.py` ↔ template | 25072b = 25072b | IDENTICAL |

`--scope=arch-linkage` covers the first six pairs. Extra execute-touched pairs independently hashed IDENTICAL.

## Compose guards (8/8 UNCHANGED)

| Story | Surface | Verification | Result |
|---|---|---|---|
| DEC-0054 | `rollover_architecture` split/pack/`ARCH_HOT_MAX_*` | import/call only; marker 2 folds “archiver unchanged” | UNCHANGED |
| DEC-0073 | H1 heading policy | architecture.md not mutated this phase; `# US-0129` L1527 retained | UNCHANGED |
| DEC-0076 / US-0089 | US-0089/US-0090 tail | DQ8 stubs insert before tail; marker 5 | UNCHANGED |
| US-0049 | state archive contract | this QA pass appends state.md only; no pack rewrite of prior archives | UNCHANGED |
| US-0126 | B-1 fixture only | marker 8 PASS; US-0126 Status DONE L4368; L154 checked | UNCHANGED |
| US-0127 / US-0128 / US-0130 | DONE rows | US-0127 DONE L4407; US-0128 DONE L4445; US-0130 DONE L4522; L155/L156/L158 checked | UNCHANGED |
| DEC-0119 | 9 `auto_repair_kind` + 12 preset flags | `ARCH_LINKAGE_AUTO_REPAIR` not in `AUTONOMY_FLAGS`; matrix `auto_repair_kind=n/a` | UNCHANGED |
| R-0112 | US-0130 overlay | not extended this story | UNCHANGED |
| US-0045 | DONE/acceptance | US-0129 Status OPEN L4482; L157 unchecked | UNCHANGED |
| US-0048 / BUG-0006 | isolation | NEW marker `qa-US0129-qa-20260827T081557Z-fresh` (not reused) | UNCHANGED |
| US-0056 | intake JSON | `handoffs/intake_evidence/US-0129-intake-20260825.json` not mutated this phase | UNCHANGED |

## Findings

### Blocking

None. `blocking_count=0`.

### Non-blocking

- **NB-1** (informational): `tests/report.md` Timestamp `2026-08-26T22:41:33Z` (Pass:845 Fail:0) precedes US-0129 execute `2026-08-27T08:04:38Z`. This QA pass did not re-run `tests/run-tests.ps1`. Slice pytest 8/8 is the required FRAMEWORK_KIT_REPO=1 evidence. Canonical `convergence_smoke.evidence_ref` still uses the contracted token `tests/report.md Fail:0 + uat.json waived_probes[] (6 classes, UAT_PROBE_FORBIDDEN)`. Do not claim a live full-harness Fail:0 from this pass.

Critic NB awareness (not new QA findings): `a0129ex-challenger-001`; `a0129ex-architect-002`; `a0129ex-subtractor-003` (informational concurrence from execute critic PASS, anti_slop=8, 0 blocking).

## UAT probes (FRAMEWORK_KIT_REPO=1 — honest classification)

Applicable probe class: **`contract_tests_primary`** (8 markers). No web UI. No fake browser PASS. Live-runtime probes **not attempted** (`UAT_PROBE_FORBIDDEN` if attempted).

Canonical surrogate step **`convergence_smoke`** emitted this pass (`result=pass`) because `contract_test_failed=0`.

| Probe class | Result | reason_code |
|---|---|---|
| `contract_tests_primary` | PASS (8/8) | `UAT_PROBE_PASS` |
| `browser_smoke` | waived / not applicable | `UAT_PROBE_FORBIDDEN` |
| `api_health` | waived / not applicable | `UAT_PROBE_FORBIDDEN` |
| `process_health` | waived / not applicable | `UAT_PROBE_FORBIDDEN` |
| `cli_smoke` | not applicable (lib + commands; verified via contract tests) | `UAT_PROBE_FORBIDDEN` |
| `build` | not applicable | `UAT_PROBE_FORBIDDEN` |
| `manual_operator` | not applicable | `UAT_PROBE_FORBIDDEN` |

**Runtime browser evidence**: none. MCP browser sequence **not run**. No screenshot. No silent browser PASS.

## Runtime QA evidence (US-0065) — kit slice, not generated webapp

- `runtime_startup_command`: n/a (FRAMEWORK_KIT_REPO=1; no app server)
- `runtime_stack_profile`: python (scripts/docs/tests kit)
- `runtime_mode`: local
- `runtime_health_target`: n/a — no process/endpoint
- `runtime_health_result`: not_applicable
- `runtime_log_summary`: n/a (no app logs)
- `runtime_retry_count`: 0
- `runtime_retry_ledger`: []
- `runtime_final_verdict`: pass
- `runtime_reason_code`: `UAT_PROBE_FORBIDDEN` for browser/runtime-app probes; slice health is contract tests + `convergence_smoke` surrogate
- `runtime_evidence_refs`: pytest 8/8; parity CLI `--scope=arch-linkage`; `sprints/S0129/uat.json` `convergence_smoke`

## Generated-test evidence (US-0066)

- `generated_test_stack_profile`: python
- `generated_test_command`: `python -m pytest tests/us0129_contract_test.py -v`
- `generated_test_result`: pass
- `generated_test_output_ref`: this file § Independent checks (8 passed in 0.57s)
- `generated_test_paths_ref`: `tests/us0129_contract_test.py`
- `generated_test_reason_code`: none (pass)

## Status confirmation (US-0045)

- backlog `## US-0129` Status: **OPEN** (L4482)
- acceptance L157: **unchecked**
- US-0130 DONE (acceptance L158 checked)
- US-0128 DONE (acceptance L156 checked)
- US-0127 DONE (acceptance L155 checked)
- US-0126 DONE (acceptance L154 checked)
- US-0108 DONE; US-0121..US-0125 DONE
- intake JSON not mutated this phase
- architecture.md `# US-0129` L1527 not mutated this phase

## Producer proof consumed (execute)

- `producer_runtime_proof_id=rp-auto-20260827-01-execute-dev-20260827T080438Z-US-0129`
- Canonical payload independently hashed: `{"delivery_mode":"ultra_lean","macro_phase":"build+verify","model_id":"cursor-grok-4.6-high","orchestrator_run_id":"auto-20260827-01","phase_id":"execute","proof_issued_at":"2026-08-27T08:04:38Z","proof_ttl_seconds":3600,"role":"dev","runtime_proof_id":"rp-auto-20260827-01-execute-dev-20260827T080438Z-US-0129","sprint_id":"S0129","story_id":"US-0129"}`
- `producer_attested_proof_hash=CFE682EA7A8A7A8EF5A9486F7A9E04FAAC2F9DB6425147CA3D8B7B77F413CE4F`
- Independent SHA-256 recompute: **MATCH**
- `producer_proof_ttl=2026-08-27T09:04:38Z`, `consumed_at=2026-08-27T08:15:57Z` (before RUNTIME_PROOF_STALE)
- `producer_ttl_stale=false`

## Strict runtime proof (DEC-0038) — qa

- `orchestrator_run_id=auto-20260827-01`
- `runtime_proof_id=rp-auto-20260827-01-qa-qa-20260827T081557Z-US-0129` (NEW — distinct from execute `...080438Z...`; no proof_id reuse)
- `phase_id=qa`, `role=qa`, `story_id=US-0129`, `sprint_id=S0129`
- `delivery_mode=ultra_lean`, `macro_phase=build+verify`, `model_id=cursor-grok-4.6-high`
- `proof_issued_at=2026-08-27T08:15:57Z`
- `proof_ttl_seconds=3600`, `proof_ttl=2026-08-27T09:15:57Z` (UTC = issued_at + 3600s)
- `proof_hash=EF77672C5F3DD2F99EABDB9D93D8F2B1445C4943234FE08BC1BDE436CCF6E0D3` (SHA-256 of sorted-key compact lowercase-keys JSON payload, UTF-8 bytes via Python 3.12 hashlib; independently recomputed MATCH before return)
- Canonical payload: `{"delivery_mode":"ultra_lean","macro_phase":"build+verify","model_id":"cursor-grok-4.6-high","orchestrator_run_id":"auto-20260827-01","phase_id":"qa","proof_issued_at":"2026-08-27T08:15:57Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260827-01-qa-qa-20260827T081557Z-US-0129","sprint_id":"S0129","story_id":"US-0129"}`

## Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

- `phase_id=qa`, `role=qa`, `model_id=cursor-grok-4.6-high` (CROSS_MODEL_REVIEW=1 — required)
- `fresh_context_marker=qa-US0129-qa-20260827T081557Z-fresh` (NEW per US-0048 / BUG-0006)
- `timestamp=2026-08-27T08:15:57Z` (UTC)
- `evidence_ref=sprints/S0129/qa-findings.md`
- Fresh qa subagent per BUG-0006 / US-0048 isolation; no prior chat history carried forward. Context limited to narrow-read (US-0053). No `.env` reads, no credentials access, no intake-evidence mutation, no backlog Status/AC mutation, no acceptance.md mutation, no architecture.md mutation, no DONE-row mutation, no `/execute` or `/verify-work` spawn from this subagent.

## Next scheduled phase

- `next_scheduled_phase=/verify-work` (role=qa per US-0069 / DEC-0051; fresh qa subagent per BUG-0006 — orchestrator-owned spawn; after sovereign-critic of qa if CROSS_MODEL_REVIEW=1)
- `next_scheduled_role=qa`
- `stop_condition=STOP after qa PASS. Orchestrator spawns sovereign-critic of qa (CROSS_MODEL_REVIEW=1), then /verify-work in a fresh qa subagent (BUG-0006). Do NOT spawn /verify-work or /execute from this subagent. Do NOT mark US-0129 DONE. Do NOT tick acceptance L157. Do NOT mutate intake JSON. Do NOT mutate architecture.md. Do NOT reopen US-0126/US-0127/US-0128/US-0130. Do NOT add ARCH_LINKAGE_AUTO_REPAIR to AUTONOMY_PRESET.`
- `artifacts_written=sprints/S0129/qa-findings.md, sprints/S0129/uat.json, sprints/S0129/uat.md, docs/engineering/state.md (qa checkpoint append), handoffs/resume_brief.md (qa PASS prepend → /verify-work)`
- `handoffs/qa_to_dev.md=NOT written` (no blocking findings; AUTO_IMPLEMENTATION_LOOP does not return to /execute)
