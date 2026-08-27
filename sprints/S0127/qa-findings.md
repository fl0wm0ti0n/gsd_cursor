# QA findings — US-0127 / S0127 / auto-20260826-01 (qa)

- **phase_id**: qa, **role**: qa, **story_id**: US-0127 (OPEN — not marked DONE per US-0045), **sprint_id**: S0127
- `orchestrator_run_id=auto-20260826-01`, `delivery_mode=ultra_lean`, `macro_phase=build+verify`
- `AUTO_IMPLEMENTATION_LOOP=1`
- `model_id=cursor-grok-4.6-high` (CROSS_MODEL_REVIEW=1 — required on isolation)
- `producer_phase_id=execute`, `producer_role=dev`, `producer_model_id=cursor-grok-4.6-high`
- `critic_phase_id=sovereign-critic` (execute review), `critic_model_id=composer-2.5-fast`, `critic_verdict=PASS`, `anti_slop_aggregate=10`, `open_blocking_findings=0`
- `critic_fresh_context_marker=tl-US0127-sovereign-critic-execute-20260826T184749Z-fresh`
- `fresh_context_marker=qa-US0127-qa-20260826T185256Z-fresh` (NEW per US-0048 / BUG-0006; marker reuse = stale isolation evidence)
- `timestamp (UTC)=2026-08-26T18:52:56Z`
- **verdict: QA_PASS**
- `blocking_count=0`
- `non_blocking_count=1` (NB-1: runbook pair-table prose vs Python `SOVEREIGN_CRITIC_PAIRS` tuple — informational)
- `story_status=OPEN` (do not mark US-0127 DONE per US-0045; acceptance L155 unchecked; intake JSON not mutated; architecture.md not mutated this phase)
- `acceptance_L155=NOT ticked`
- `intake_json=NOT mutated`
- `FRAMEWORK_KIT_REPO=1` (scripts/docs/contract-test slice — no web UI; no fake browser PASS)
- `SECURITY_REVIEW=0`, `CROSS_REPO_OBSERVABILITY=0`, `COMPONENT_SCOPE_MODE=0` (zero overhead)
- `SYNC_POLICY_MODE=disabled` (no push)

## Verdict rationale

Fresh QA independently remapped AC-1..AC-6 against delivered files (not execute summary alone), re-ran the US-0127 contract-test slice (13/13), compose US-0104/US-0110 tests (18/18), `--scope=sovereign-critic` (and related) parity, hygiene `--self-test`, validator `--enforce`, and user-visible metadata guard. All pass green. Compose 8/8 UNCHANGED. Active↔template byte-identical for all eight touched pairs. US-0127 remains OPEN; L155 unchecked; US-0128/0129/0130 and DONE rows US-0108/US-0121..US-0126 untouched. Browser/runtime probes for a generated webapp are **not applicable** and are classified `UAT_PROBE_FORBIDDEN` / waived — not silent PASS.

## Test plan

| # | Check | Expected |
|---|---|---|
| 1 | Independent AC-1..AC-6 remap vs files | Each AC has delivered surface + markers |
| 2 | `python -m pytest tests/us0127_contract_test.py -v` | 13/13 PASS |
| 3 | `python scripts/check_intake_template_parity.py --scope=sovereign-critic` | `[INTAKE_TEMPLATE_PARITY_OK]` |
| 4 | Compose: `pytest tests/us0110_contract_test.py tests/us0104_contract_test.py` | 18/18 PASS |
| 5 | `python scripts/check-user-visible-metadata.py --repo .` | exit 0 |
| 6 | `python scripts/sovereign_critic_hygiene.py --self-test` | `[HYGIENE_SELF_TEST_OK]` |
| 7 | `python scripts/sovereign_critic_validate.py --repo . --enforce` | `[SOVEREIGN_CRITIC_VALIDATION_OK]` (do not amend validator) |
| 8 | Active↔template SHA-256 for touched pairs | IDENTICAL |
| 9 | Compose 8/8 signatures/schema | `read_open_blocking` / `resolve_finding` / findings schema / five-conjunct / US-0107 untouched |
| 10 | Status: US-0127 OPEN; L155 unchecked; siblings + DONE rows | unchanged |
| 11 | UAT probes | `contract_tests_primary` PASS; browser/api/process waived `UAT_PROBE_FORBIDDEN` |

## Independent checks (run in this qa subagent)

| Check | Command | Result |
|---|---|---|
| US-0127 contract tests | `python -m pytest tests/us0127_contract_test.py -v` | **13 passed** in 0.68s (13/13 markers green) |
| sovereign-critic parity | `python scripts/check_intake_template_parity.py --scope=sovereign-critic` | **exit 0** — `[INTAKE_TEMPLATE_PARITY_OK] scope=sovereign-critic` |
| sovereign-convergence parity | `--scope=sovereign-convergence` | **exit 0** — `[INTAKE_TEMPLATE_PARITY_OK]` |
| opencode-adapter parity | `--scope=opencode-adapter` | **exit 0** — `[INTAKE_TEMPLATE_PARITY_OK]` |
| US-0110 + US-0104 compose tests | `python -m pytest tests/us0110_contract_test.py tests/us0104_contract_test.py -q` | **18 passed** in 0.16s |
| User-visible metadata | `python scripts/check-user-visible-metadata.py --repo .` | **exit 0** |
| Hygiene self-test | `python scripts/sovereign_critic_hygiene.py --self-test` | **exit 0** — `[HYGIENE_SELF_TEST_OK]` |
| Validator enforce | `python scripts/sovereign_critic_validate.py --repo . --enforce` | **exit 0** — `[SOVEREIGN_CRITIC_VALIDATION_OK]` |
| LINT_COMMAND | (empty in runbook) | **skipped** |
| TYPECHECK_COMMAND | (empty in runbook) | **skipped** |
| TEST_COMMAND full harness `tests/run-tests.ps1` | not re-run this pass | **not claimed** — `tests/report.md` timestamp `2026-08-25T17:13:14Z` is **stale** vs US-0127 execute (`2026-08-26T18:43:28Z`). Slice tests above are the required evidence for this FRAMEWORK_KIT_REPO=1 story. |
| No-secrets grep | hygiene + us0127 contract test | zero `api_key` / `apikey` / `sk-` / `auth.json` hits |

## AC remap (independent — files + tests, not execute summary)

| AC | Delivered surface | Markers | Result |
|---|---|---|---|
| AC-1 Blocking-only check | `scripts/sovereign_convergence_lib.py` `_critic_jsonl_has_open` delegates to `read_open_blocking`; `_eval_critic_resolved` JSONL-authoritative when non-empty, QA-markdown fallback when JSONL absent, skip when neither | m1, m2, m11, m12, m13 | **PASS** |
| AC-2 Auto-resolve non-blocking | `.cursor/commands/sovereign-critic.md` hook after reconcile+JSONL+isolation, before Stop conditions: `if read_open_blocking(repo) == []: auto_resolve_nonblocking_for_run(...)`; additive helper in `sovereign_critic_lib.py` | m3, m4, m5 | **PASS** |
| AC-3 Hygiene CLI | NEW `scripts/sovereign_critic_hygiene.py` with `--report` / `--resolve-nonblocking-for-run` / `--dry-run` / `--confirm` / `--self-test` / `--all-phases` / `--phase-id` + 6 reason codes | m6, m7, m8, m9, m10 | **PASS** |
| AC-4 Contract tests | `tests/us0127_contract_test.py` 13 `test_us0127_*` markers (static/fixture; no live critic spawn) | all 13 | **PASS** (13/13 this run) |
| AC-5 Operator docs | runbook `### Blocking-only conjunct-3 semantics (US-0127)` + `### Hygiene CLI (US-0127)`; `reason_codes.md` `## US-0127` | grep + byte-identity | **PASS** |
| AC-6 Template parity | `SOVEREIGN_CRITIC_PAIRS` + `--scope=sovereign-critic`; compose read-only US-0104/US-0110/US-0107 | parity CLI + m11/m12 | **PASS** |

## Contract marker results (13/13)

| # | Marker | AC | Result |
|---|---|---|---|
| 1 | `test_us0127_open_nonblocking_passes_convergence` | AC-1/AC-4 | PASS |
| 2 | `test_us0127_open_blocking_fails_convergence` | AC-1/AC-4 | PASS |
| 3 | `test_us0127_autoresolve_idempotent_on_rerun` | AC-2/AC-4 | PASS |
| 4 | `test_us0127_autoresolve_preserves_audit_trail` | AC-2/AC-4 | PASS |
| 5 | `test_us0127_autoresolve_skips_when_blocking_open` | AC-2/AC-4 | PASS |
| 6 | `test_us0127_hygiene_report` | AC-3 | PASS |
| 7 | `test_us0127_hygiene_dry_run` | AC-3 | PASS |
| 8 | `test_us0127_hygiene_confirm_required` | AC-3 | PASS |
| 9 | `test_us0127_hygiene_self_test` | AC-3 | PASS |
| 10 | `test_us0127_hygiene_phase_scope_required` | AC-3 | PASS |
| 11 | `test_us0127_compose_us0104_read_open_blocking_unchanged` | DQ7 | PASS |
| 12 | `test_us0127_compose_us0110_conjunct3_contract` | DQ8 | PASS |
| 13 | `test_us0127_validate_rejects_missing_blocking` | R2 | PASS |

## Template byte-identity (touched pairs)

| Pair | Bytes | Result |
|---|---|---|
| `scripts/sovereign_critic_hygiene.py` ↔ template | 10970b = 10970b | IDENTICAL |
| `tests/us0127_contract_test.py` ↔ template | 14899b = 14899b | IDENTICAL |
| `scripts/sovereign_convergence_lib.py` ↔ template | 37058b = 37058b | IDENTICAL |
| `scripts/sovereign_critic_lib.py` ↔ template | 23206b = 23206b | IDENTICAL |
| `.cursor/commands/sovereign-critic.md` ↔ template | 5266b = 5266b | IDENTICAL |
| `docs/engineering/runbook.md` ↔ template | 207169b = 207169b | IDENTICAL |
| `docs/engineering/reason_codes.md` ↔ template | 31481b = 31481b | IDENTICAL |
| `scripts/check_intake_template_parity.py` ↔ template | 23708b = 23708b | IDENTICAL |

## Compose guards (8/8 UNCHANGED)

| Story | Surface | Verification | Result |
|---|---|---|---|
| US-0104 | `read_open_blocking(repo) -> List[dict]` | inspect signature + predicate `obj.get("blocking") and obj.get("status") == "open"` | UNCHANGED |
| US-0104 | `resolve_finding(path, finding_id, status) -> bool` | inspect signature; read-all + rewrite-all | UNCHANGED |
| US-0104 | findings JSONL schema | `FINDING_REQUIRED_FIELDS` 15 fields incl. `blocking`/`status` | UNCHANGED |
| US-0104 | `sovereign_critic_validate.py` | `--enforce` OK; git last touch is US-0104-era commit; **not amended** | UNCHANGED |
| US-0110 | five-conjunct identity | `('backlog_clear','zero_deferrals','critic_resolved','smoke_green','ledger_clean')` | UNCHANGED |
| US-0110 | `CONVERGENCE_CROSS_REVIEWER_OPEN` | reason-code name unchanged; description-only note in US-0127 reason_codes section | UNCHANGED |
| US-0107 | deferral / drain-generate / stop matrix | `reason_codes.md` `## US-0107` present; not in execute touch list | UNCHANGED |
| US-0045 | DONE/acceptance | US-0127 Status OPEN; L155 unchecked; US-0128/0129/0130 OPEN unchecked; US-0108/US-0121..US-0126 DONE preserved | UNCHANGED |

## Findings

### Blocking

None. `blocking_count=0`.

### Non-blocking

- **NB-1** (informational): runbook `#### Parity enforcement` prose still lists `SOVEREIGN_CRITIC_PAIRS` as "lib, validator, command, scratchpad, `DEC-0104.md`" plus an additive hygiene row, while `scripts/check_intake_template_parity.py` `SOVEREIGN_CRITIC_PAIRS` contains **only** the hygiene script pair. `--scope=sovereign-critic` PASS and AC-6 are satisfied. No code/test failure. Optional later docs tidy; not a QA blocker.

## UAT probes (FRAMEWORK_KIT_REPO=1 — honest classification)

Applicable probe class: **`contract_tests_primary`** (13 markers). No web UI. Hygiene CLI is operator-only (not invoked by `/auto`).

| Probe class | Result | reason_code |
|---|---|---|
| `contract_tests_primary` | PASS (13/13) | `UAT_PROBE_PASS` |
| `browser_smoke` | waived / not applicable | `UAT_PROBE_FORBIDDEN` |
| `api_health` | waived / not applicable | `UAT_PROBE_FORBIDDEN` |
| `process_health` | waived / not applicable | `UAT_PROBE_FORBIDDEN` |
| `cli_smoke` | covered by hygiene `--self-test` + markers 6–10; no new binary | `UAT_PROBE_FORBIDDEN` (no live operator CLI against production JSONL) |
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
- `runtime_reason_code`: `UAT_PROBE_FORBIDDEN` for browser/runtime-app probes; slice health is contract tests
- `runtime_evidence_refs`: pytest 13/13; parity CLI; hygiene `--self-test`; validator `--enforce`

## Generated-test evidence (US-0066)

- `generated_test_stack_profile`: python
- `generated_test_command`: `python -m pytest tests/us0127_contract_test.py -v`
- `generated_test_result`: pass
- `generated_test_output_ref`: this file § Independent checks (13 passed in 0.68s)
- `generated_test_paths_ref`: `tests/us0127_contract_test.py`
- `generated_test_reason_code`: none (pass)

## Status confirmation (US-0045)

- backlog `## US-0127` Status: **OPEN** (L4407)
- acceptance L155: **unchecked**
- US-0128 Status OPEN (L4445); L156 unchecked
- US-0129 Status OPEN (L4479); L157 unchecked
- US-0130 Status OPEN (L4513); L158 unchecked
- US-0108 DONE (L3568); US-0121..US-0126 DONE (L4127..L4368)
- intake JSON not mutated this phase

## Producer proof consumed (execute)

- `producer_runtime_proof_id=rp-auto-20260826-01-execute-dev-20260826T184328Z-US-0127`
- Canonical payload independently hashed: `{"delivery_mode":"ultra_lean","macro_phase":"build+verify","model_id":"cursor-grok-4.6-high","orchestrator_run_id":"auto-20260826-01","phase_id":"execute","proof_issued_at":"2026-08-26T18:43:28Z","proof_ttl_seconds":3600,"role":"dev","runtime_proof_id":"rp-auto-20260826-01-execute-dev-20260826T184328Z-US-0127","sprint_id":"S0127","story_id":"US-0127"}`
- `producer_attested_proof_hash=F42BBB6F51CD57EE2B5D7EC04630F5EFB38F93B89B38AEE4C38418C28616BBFE`
- Independent SHA-256 recompute: **MATCH**
- `producer_proof_ttl=2026-08-26T19:43:28Z`, `consumed_at=2026-08-26T18:52:56Z` (before RUNTIME_PROOF_STALE)
- `producer_ttl_stale=false`

## Strict runtime proof (DEC-0038) — qa

- `orchestrator_run_id=auto-20260826-01`
- `runtime_proof_id=rp-auto-20260826-01-qa-qa-20260826T185256Z-US-0127` (NEW — distinct from execute `...184328Z...`; no proof_id reuse)
- `phase_id=qa`, `role=qa`, `story_id=US-0127`, `sprint_id=S0127`
- `delivery_mode=ultra_lean`, `macro_phase=build+verify`, `model_id=cursor-grok-4.6-high`
- `proof_issued_at=2026-08-26T18:52:56Z`
- `proof_ttl_seconds=3600`, `proof_ttl=2026-08-26T19:52:56Z` (UTC = issued_at + 3600s)
- `proof_hash=ADF5500EBF02220B1A3A14FB9B1EE6941A59F5382755A754C9D7ED62468C6E98` (SHA-256 of sorted-key compact lowercase-keys JSON payload, UTF-8 bytes via Python 3.12 hashlib; independently recomputed MATCH before return)
- Canonical payload: `{"delivery_mode":"ultra_lean","macro_phase":"build+verify","model_id":"cursor-grok-4.6-high","orchestrator_run_id":"auto-20260826-01","phase_id":"qa","proof_issued_at":"2026-08-26T18:52:56Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260826-01-qa-qa-20260826T185256Z-US-0127","sprint_id":"S0127","story_id":"US-0127"}`

## Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

- `phase_id=qa`, `role=qa`, `model_id=cursor-grok-4.6-high` (CROSS_MODEL_REVIEW=1 — required)
- `fresh_context_marker=qa-US0127-qa-20260826T185256Z-fresh` (NEW per US-0048 / BUG-0006)
- `timestamp=2026-08-26T18:52:56Z` (UTC)
- `evidence_ref=sprints/S0127/qa-findings.md`
- Fresh qa subagent per BUG-0006 / US-0048 isolation; no prior chat history carried forward. Context limited to narrow-read (US-0053). No `.env` reads, no credentials access, no intake-evidence mutation, no backlog Status/AC mutation, no acceptance.md mutation, no architecture.md mutation, no DONE-row mutation, no US-0128/US-0129/US-0130 mutation, no `/execute` or `/verify-work` spawn from this subagent.

## Next scheduled phase

- `next_scheduled_phase=/verify-work` (role=qa per US-0069 / DEC-0051; fresh qa subagent per BUG-0006 — orchestrator-owned spawn; after sovereign-critic of qa if CROSS_MODEL_REVIEW=1)
- `next_scheduled_role=qa`
- `stop_condition=STOP after qa PASS. Orchestrator spawns sovereign-critic of qa (CROSS_MODEL_REVIEW=1), then /verify-work in a fresh qa subagent (BUG-0006). Do NOT spawn /verify-work or /execute from this subagent. Do NOT mark US-0127 DONE. Do NOT tick acceptance L155. Do NOT mutate intake JSON. Do NOT amend US-0104/US-0110/US-0107 surfaces.`
- `artifacts_written=sprints/S0127/qa-findings.md, sprints/S0127/uat.json, sprints/S0127/uat.md, docs/engineering/state.md (qa checkpoint append), handoffs/resume_brief.md (qa PASS prepend → /verify-work)`
- `handoffs/qa_to_dev.md=NOT written` (no blocking findings; AUTO_IMPLEMENTATION_LOOP does not return to /execute)
