# QA findings — US-0130 / S0130 / auto-20260826-01 (qa)

- **phase_id**: qa, **role**: qa, **story_id**: US-0130 (OPEN — not marked DONE per US-0045), **sprint_id**: S0130
- `orchestrator_run_id=auto-20260826-01`, `delivery_mode=ultra_lean`, `macro_phase=build+verify`
- `AUTO_IMPLEMENTATION_LOOP=1`
- `model_id=cursor-grok-4.6-high` (CROSS_MODEL_REVIEW=1 — required on isolation)
- `producer_phase_id=execute`, `producer_role=dev`, `producer_model_id=cursor-grok-4.6-high`
- `critic_phase_id=sovereign-critic` (execute review), `critic_model_id=composer-2.5-fast`, `critic_verdict=PASS`, `anti_slop_aggregate=10`, `open_blocking_findings=0`
- `critic_fresh_context_marker=tl-US0130-sovereign-critic-execute-20260826T221938Z-fresh`
- `fresh_context_marker=qa-US0130-qa-20260826T222300Z-fresh` (NEW per US-0048 / BUG-0006; marker reuse = stale isolation evidence)
- `timestamp (UTC)=2026-08-26T22:23:00Z`
- **verdict: QA_PASS**
- `blocking_count=0`
- `non_blocking_count=1` (NB-1: full harness `tests/report.md` timestamp precedes execute — informational)
- `story_status=OPEN` (do not mark US-0130 DONE per US-0045; acceptance L158 unchecked; intake JSON not mutated; architecture.md not mutated this phase)
- `acceptance_L158=NOT ticked`
- `intake_json=NOT mutated`
- `model-catalog.local.json=NOT written` (file absent)
- `FRAMEWORK_KIT_REPO=1` (scripts/docs/examples/contract-test slice — no web UI; no fake browser PASS)
- `SECURITY_REVIEW=0`, `CROSS_REPO_OBSERVABILITY=0`, `COMPONENT_SCOPE_MODE=0` (zero overhead)
- `SPEC_PACK_MODE=0`, `USER_GUIDE_MODE=0`, `REMOTE_EXECUTION=0`
- `SYNC_POLICY_MODE=disabled` (no push)

## Verdict rationale

Fresh QA independently remapped AC-1..AC-9 against delivered files (not execute summary alone), re-ran the US-0130 contract-test slice (10/10), compose US-0104 tests (10/10), `--scope=sovereign-critic` and `--scope=model-tier-overrides` parity, and user-visible metadata guard. All pass green. Compose 9/9 UNCHANGED. Active↔template byte-identical for all twelve touched pairs checked. Canonical `convergence_smoke` step emitted in `sprints/S0130/uat.json` because `contract_test_failed=0`. US-0130 remains OPEN; L158 unchecked; US-0129 OPEN untouched; DONE rows US-0108/US-0121..US-0128 preserved. Browser/runtime probes for a generated webapp are **not applicable** and are classified `UAT_PROBE_FORBIDDEN` / waived — not silent PASS. Live-runtime probes were not attempted.

## Test plan

| # | Check | Expected |
|---|---|---|
| 1 | Independent AC-1..AC-9 remap vs files | Each AC has delivered surface + markers |
| 2 | `python -m pytest tests/us0130_contract_test.py -v` | 10/10 PASS |
| 3 | `python -m pytest tests/us0104_contract_test.py -q` | PASS (compose) |
| 4 | `python scripts/check_intake_template_parity.py --scope=sovereign-critic` | `[INTAKE_TEMPLATE_PARITY_OK]` |
| 5 | `python scripts/check_intake_template_parity.py --scope=model-tier-overrides` | `[INTAKE_TEMPLATE_PARITY_OK]` |
| 6 | `python scripts/check-user-visible-metadata.py --repo .` | exit 0 |
| 7 | Active↔template SHA-256/bytes for touched pairs | IDENTICAL |
| 8 | Compose 9/9 (US-0104/US-0102/US-0101/US-0112/US-0127/US-0128/US-0129/US-0123/US-0045) | UNCHANGED |
| 9 | Status: US-0130 OPEN; L158 unchecked; US-0129 OPEN; DONE rows | unchanged |
| 10 | UAT probes | `contract_tests_primary` PASS; 6 live-runtime classes waived `UAT_PROBE_FORBIDDEN` |
| 11 | Emit `convergence_smoke` in S0130 `uat.json` when `contract_test_failed=0` | present, `result=pass` |
| 12 | Independent execute proof hash | MATCH `089947FF…` before TTL 23:14:20Z |
| 13 | Never-write gate | `.cursor/model-catalog.local.json` absent |

## Independent checks (run in this qa subagent)

| Check | Command | Result |
|---|---|---|
| Execute proof SHA-256 | Python hashlib on sorted-key compact lowercase JSON | **MATCH** `089947FF99F92DF799FA3FD51A10E503B3DF26052833DE33EC7942ED7C59DA9C`; ttl `2026-08-26T23:14:20Z`; consumed_at `2026-08-26T22:23:00Z` |
| US-0130 contract tests | `python -m pytest tests/us0130_contract_test.py -v` | **10 passed** in 0.06s (10/10 markers green) |
| US-0104 compose tests | `python -m pytest tests/us0104_contract_test.py -q` | **10 passed** in 0.07s |
| sovereign-critic parity | `python scripts/check_intake_template_parity.py --scope=sovereign-critic` | **exit 0** — `[INTAKE_TEMPLATE_PARITY_OK] scope=sovereign-critic` |
| model-tier-overrides parity | `python scripts/check_intake_template_parity.py --scope=model-tier-overrides` | **exit 0** — `[INTAKE_TEMPLATE_PARITY_OK] scope=model-tier-overrides` |
| User-visible metadata | `python scripts/check-user-visible-metadata.py --repo .` | **exit 0** |
| LINT_COMMAND | (empty in runbook) | **skipped** |
| TYPECHECK_COMMAND | (empty in runbook) | **skipped** |
| TEST_COMMAND full harness `tests/run-tests.ps1` | not re-run this pass | **not claimed** — `tests/report.md` timestamp `2026-08-26T20:57:42Z` (Pass:845 Fail:0) precedes US-0130 execute (`2026-08-26T22:14:20Z`). Slice tests above are the required evidence for this FRAMEWORK_KIT_REPO=1 story. |
| Never-write gate | `.cursor/model-catalog.local.json` | **absent** |
| No-secrets grep | `scripts/sovereign_critic_lib.py` + `tests/us0130_contract_test.py` | zero `api_key` / `apikey` / `sk-` / `auth.json` hits |
| Live `MODEL_SOVEREIGN-CRITIC=` assignment | committed scratchpad | **none** (comment placeholders only) |

## AC remap (independent — files + tests, not execute summary)

| AC | Delivered surface | Markers | Result |
|---|---|---|---|
| AC-1 Scratchpad pin | `.cursor/scratchpad.md` comment `MODEL_SOVEREIGN-CRITIC=<your-critic-model-slug>` (hyphen exact; no underscore alias; vendor slugs in `.cursor/scratchpad.local.md` only); `select_critic_model` consumes pin via `phase_to_model_key("sovereign-critic")`; no live assignment in committed scratchpad | m1, m6 | **PASS** |
| AC-2 Catalog `roles.critic` | `CATALOG_OPTIONAL_ROLE_KEYS = frozenset({"critic"})`; extra-key subtract; missing `critic` not an error; empty-present reuses `MODEL_CATALOG_SCHEMA_V2_INVALID`; `critic` not in `CATALOG_ROLE_KEYS` | m2, m3, m7, m8 | **PASS** |
| AC-3 `select_critic_model` precedence | `_overlay_critic_slug`: pin > `roles.critic` when `role_catalog` > opposition/`dev` via `_resolve_slug_for_tier` UNCHANGED; underscore alias not consumed | m1, m2, m3, m6 | **PASS** |
| AC-4 Collision policy | same-slug comparison after overlay keeps `degraded=True` / `CROSS_MODEL_DEGRADED_MODE` (not a hard stop) | m4 | **PASS** |
| AC-5 One global critic | overlay inside `select_critic_model` only; no per-lens / per-phase critic overrides; `sovereign-critic` not in `PHASE_LOGICAL_ROLE` / `CANONICAL_PHASE_IDS` / `DEFAULT_PHASE_TIER_MATRIX` | m8 + overlay shape | **PASS** |
| AC-6 Contract tests | `tests/us0130_contract_test.py` 10 `test_us0130_*` markers (static/fixture; no live critic spawn) | all 10 | **PASS** (10/10 this run) |
| AC-7 Compose do not amend | US-0104 findings JSONL / three lenses / `CROSS_MODEL_*` keys / anti-slop formula unchanged; US-0101 matrix / US-0102 5-step chain unchanged (`critic` not in required role keys) | m5, m8 + us0104 10/10 | **PASS** |
| AC-8 Examples + installer | cursor_only `critic=composer-2.5-fast` shipped as 9th; generic v2 examples placeholder; installer/manifest never write `model-catalog.local.json` | m9, m10 | **PASS** |
| AC-9 Docs + parity | scratchpad CROSS_MODEL / MODEL comments; runbook `#### Degraded fallback troubleshooting` pin-precedence note; architecture `# US-0130` H1 present at L1815 (not mutated this phase); `--scope=sovereign-critic` + `--scope=model-tier-overrides` OK | m9 + parity CLI | **PASS** |

## Contract marker results (10/10)

| # | Marker | AC | Result |
|---|---|---|---|
| 1 | `test_us0130_pin_wins_over_catalog_and_opposition` | AC-1/AC-3/AC-6 | PASS |
| 2 | `test_us0130_catalog_critic_hit_when_pin_absent` | AC-2/AC-3/AC-6 | PASS |
| 3 | `test_us0130_omitted_critic_falls_back_to_opposition` | AC-2/AC-3/AC-6 | PASS |
| 4 | `test_us0130_same_slug_keeps_degraded_mode` | AC-4/AC-6 | PASS |
| 5 | `test_us0130_compose_us0104_findings_schema_unchanged` | AC-7/AC-6 | PASS |
| 6 | `test_us0130_underscore_alias_not_consumed` | AC-1/AC-3/AC-6 | PASS |
| 7 | `test_us0130_extra_critic_allowed_missing_not_error` | AC-2/AC-6 | PASS |
| 8 | `test_us0130_critic_not_in_catalog_role_keys` | AC-2/AC-6 | PASS |
| 9 | `test_us0130_cursor_only_example_ships_critic` | AC-8/AC-6 | PASS |
| 10 | `test_us0130_installer_never_writes_local_catalog` | AC-8/AC-6 | PASS |

## Template byte-identity (touched pairs)

| Pair | Bytes | Result |
|---|---|---|
| `scripts/sovereign_critic_lib.py` ↔ template | 25122b = 25122b | IDENTICAL |
| `scripts/model_tier_lib.py` ↔ template | 24253b = 24253b | IDENTICAL |
| `scripts/model_tier_validate.py` ↔ template | 20986b = 20986b | IDENTICAL |
| `scripts/check_intake_template_parity.py` ↔ template | 24220b = 24220b | IDENTICAL |
| `tests/us0130_contract_test.py` ↔ template | 14101b = 14101b | IDENTICAL |
| `docs/engineering/runbook.md` ↔ template | 209317b = 209317b | IDENTICAL |
| `.cursor/scratchpad.md` ↔ template | 36052b = 36052b | IDENTICAL |
| `.cursor/scratchpad.local.example.md` ↔ template | 35600b = 35600b | IDENTICAL |
| `.cursor/model-catalog.local.example.role-based-balanced_cursor_only.json` ↔ template | 997b = 997b | IDENTICAL |
| `.cursor/model-catalog.local.example.role-based-balanced.json` ↔ template | 764b = 764b | IDENTICAL |
| `.cursor/model-catalog.local.example.role-based-highend.json` ↔ template | 738b = 738b | IDENTICAL |
| `docs/engineering/context/installer-owned-paths.manifest` ↔ template | 4128b = 4128b | IDENTICAL |

## Compose guards (9/9 UNCHANGED)

| Story | Surface | Verification | Result |
|---|---|---|---|
| US-0104 | findings JSONL / lenses / `CROSS_MODEL_*` / anti-slop | marker 5 PASS; us0104 10/10 PASS | UNCHANGED |
| US-0102 | `CATALOG_ROLE_KEYS` required-set / 5-step chain / `PHASE_LOGICAL_ROLE` | marker 8 PASS; `critic` not in required set; `sovereign-critic` not in `PHASE_LOGICAL_ROLE` | UNCHANGED |
| US-0101 | default phase-tier matrix / v1 catalogs | marker 8 PASS; v1 examples not in this-pass touch list | UNCHANGED |
| US-0112 | never-write `model-catalog.local.json` | marker 10 PASS; cursor_only shipped as 9th example; local.json absent | UNCHANGED |
| US-0127 / US-0128 | DONE rows | US-0127 DONE (L4407); US-0128 DONE (L4445); acceptance L155/L156 checked | UNCHANGED |
| US-0129 | sibling OPEN | Status OPEN L4482; acceptance L157 unchecked; not mutated this phase | UNCHANGED |
| US-0123 | OpenCode routing | out of scope; not mixed with Cursor Task slugs | UNCHANGED |
| US-0045 | DONE/acceptance | US-0130 Status OPEN L4516; L158 unchecked | UNCHANGED |
| US-0048 / BUG-0006 | isolation | NEW marker `qa-US0130-qa-20260826T222300Z-fresh` (not reused) | UNCHANGED |
| US-0056 | intake JSON | `handoffs/intake_evidence/US-0130-intake-20260826.json` not mutated this phase | UNCHANGED |

## Findings

### Blocking

None. `blocking_count=0`.

### Non-blocking

- **NB-1** (informational): `tests/report.md` Timestamp `2026-08-26T20:57:42Z` (Pass:845 Fail:0) precedes US-0130 execute `2026-08-26T22:14:20Z`. This QA pass did not re-run `tests/run-tests.ps1`. Slice pytest 10/10 is the required FRAMEWORK_KIT_REPO=1 evidence. Canonical `convergence_smoke.evidence_ref` still uses the contracted token `tests/report.md Fail:0 + uat.json waived_probes[] (6 classes, UAT_PROBE_FORBIDDEN)`. Do not claim a live full-harness Fail:0 from this pass.

Critic NB awareness (not new QA findings): `a0130ex-challenger-001`; `a0130ex-architect-002`; `a0130ex-subtractor-003` (informational concurrence from execute critic PASS, anti_slop=10, 0 blocking).

## UAT probes (FRAMEWORK_KIT_REPO=1 — honest classification)

Applicable probe class: **`contract_tests_primary`** (10 markers). No web UI. No fake browser PASS. Live-runtime probes **not attempted** (`UAT_PROBE_FORBIDDEN` if attempted).

Canonical surrogate step **`convergence_smoke`** emitted this pass (`result=pass`) because `contract_test_failed=0`.

| Probe class | Result | reason_code |
|---|---|---|
| `contract_tests_primary` | PASS (10/10) | `UAT_PROBE_PASS` |
| `browser_smoke` | waived / not applicable | `UAT_PROBE_FORBIDDEN` |
| `api_health` | waived / not applicable | `UAT_PROBE_FORBIDDEN` |
| `process_health` | waived / not applicable | `UAT_PROBE_FORBIDDEN` |
| `cli_smoke` | not applicable (lib + examples; verified via contract tests) | `UAT_PROBE_FORBIDDEN` |
| `build` | not applicable | `UAT_PROBE_FORBIDDEN` |
| `manual_operator` | not applicable | `UAT_PROBE_FORBIDDEN` |

**Runtime browser evidence**: none. MCP browser sequence **not run**. No screenshot. No silent browser PASS.

## Runtime QA evidence (US-0065) — kit slice, not generated webapp

- `runtime_startup_command`: n/a (FRAMEWORK_KIT_REPO=1; no app server)
- `runtime_stack_profile`: python (scripts/docs/examples kit)
- `runtime_mode`: local
- `runtime_health_target`: n/a — no process/endpoint
- `runtime_health_result`: not_applicable
- `runtime_log_summary`: n/a (no app logs)
- `runtime_retry_count`: 0
- `runtime_retry_ledger`: []
- `runtime_final_verdict`: pass
- `runtime_reason_code`: `UAT_PROBE_FORBIDDEN` for browser/runtime-app probes; slice health is contract tests + `convergence_smoke` surrogate
- `runtime_evidence_refs`: pytest 10/10; us0104 10/10; parity CLI `--scope=sovereign-critic` + `--scope=model-tier-overrides`; `sprints/S0130/uat.json` `convergence_smoke`

## Generated-test evidence (US-0066)

- `generated_test_stack_profile`: python
- `generated_test_command`: `python -m pytest tests/us0130_contract_test.py -v`
- `generated_test_result`: pass
- `generated_test_output_ref`: this file § Independent checks (10 passed in 0.06s)
- `generated_test_paths_ref`: `tests/us0130_contract_test.py`
- `generated_test_reason_code`: none (pass)

## Status confirmation (US-0045)

- backlog `## US-0130` Status: **OPEN** (L4516)
- acceptance L158: **unchecked**
- US-0129 Status OPEN (L4482); L157 unchecked
- US-0128 DONE (acceptance L156 checked)
- US-0127 DONE (acceptance L155 checked)
- US-0108 DONE; US-0121..US-0126 DONE
- intake JSON not mutated this phase
- architecture.md `# US-0130` L1815 not mutated this phase
- `.cursor/model-catalog.local.json` not written this phase

## Producer proof consumed (execute)

- `producer_runtime_proof_id=rp-auto-20260826-01-execute-dev-20260826T221420Z-US-0130`
- Canonical payload independently hashed: `{"delivery_mode":"ultra_lean","macro_phase":"build+verify","model_id":"cursor-grok-4.6-high","orchestrator_run_id":"auto-20260826-01","phase_id":"execute","proof_issued_at":"2026-08-26T22:14:20Z","proof_ttl_seconds":3600,"role":"dev","runtime_proof_id":"rp-auto-20260826-01-execute-dev-20260826T221420Z-US-0130","sprint_id":"S0130","story_id":"US-0130"}`
- `producer_attested_proof_hash=089947FF99F92DF799FA3FD51A10E503B3DF26052833DE33EC7942ED7C59DA9C`
- Independent SHA-256 recompute: **MATCH**
- `producer_proof_ttl=2026-08-26T23:14:20Z`, `consumed_at=2026-08-26T22:23:00Z` (before RUNTIME_PROOF_STALE)
- `producer_ttl_stale=false`

## Strict runtime proof (DEC-0038) — qa

- `orchestrator_run_id=auto-20260826-01`
- `runtime_proof_id=rp-auto-20260826-01-qa-qa-20260826T222300Z-US-0130` (NEW — distinct from execute `...221420Z...`; no proof_id reuse)
- `phase_id=qa`, `role=qa`, `story_id=US-0130`, `sprint_id=S0130`
- `delivery_mode=ultra_lean`, `macro_phase=build+verify`, `model_id=cursor-grok-4.6-high`
- `proof_issued_at=2026-08-26T22:23:00Z`
- `proof_ttl_seconds=3600`, `proof_ttl=2026-08-26T23:23:00Z` (UTC = issued_at + 3600s)
- `proof_hash=7DCD83D45E1188B5102B46BCDE05EB43CC2A052EAF430647604C5B7BB3A46557` (SHA-256 of sorted-key compact lowercase-keys JSON payload, UTF-8 bytes via Python 3.12 hashlib; independently recomputed MATCH before return)
- Canonical payload: `{"delivery_mode":"ultra_lean","macro_phase":"build+verify","model_id":"cursor-grok-4.6-high","orchestrator_run_id":"auto-20260826-01","phase_id":"qa","proof_issued_at":"2026-08-26T22:23:00Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260826-01-qa-qa-20260826T222300Z-US-0130","sprint_id":"S0130","story_id":"US-0130"}`

## Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

- `phase_id=qa`, `role=qa`, `model_id=cursor-grok-4.6-high` (CROSS_MODEL_REVIEW=1 — required)
- `fresh_context_marker=qa-US0130-qa-20260826T222300Z-fresh` (NEW per US-0048 / BUG-0006)
- `timestamp=2026-08-26T22:23:00Z` (UTC)
- `evidence_ref=sprints/S0130/qa-findings.md`
- Fresh qa subagent per BUG-0006 / US-0048 isolation; no prior chat history carried forward. Context limited to narrow-read (US-0053). No `.env` reads, no credentials access, no intake-evidence mutation, no backlog Status/AC mutation, no acceptance.md mutation, no architecture.md mutation, no DONE-row mutation, no US-0129 mutation, no `model-catalog.local.json` write, no `/execute` or `/verify-work` spawn from this subagent.

## Next scheduled phase

- `next_scheduled_phase=/verify-work` (role=qa per US-0069 / DEC-0051; fresh qa subagent per BUG-0006 — orchestrator-owned spawn; after sovereign-critic of qa if CROSS_MODEL_REVIEW=1)
- `next_scheduled_role=qa`
- `stop_condition=STOP after qa PASS. Orchestrator spawns sovereign-critic of qa (CROSS_MODEL_REVIEW=1), then /verify-work in a fresh qa subagent (BUG-0006). Do NOT spawn /verify-work or /execute from this subagent. Do NOT mark US-0130 DONE. Do NOT tick acceptance L158. Do NOT mutate intake JSON. Do NOT mutate US-0129. Do NOT reopen US-0127/US-0128. Do NOT amend US-0104/US-0102/US-0101 surfaces. Do NOT write model-catalog.local.json. Do NOT author DEC-0130.`
- `artifacts_written=sprints/S0130/qa-findings.md, sprints/S0130/uat.json, sprints/S0130/uat.md, docs/engineering/state.md (qa checkpoint append), handoffs/resume_brief.md (qa PASS prepend → /verify-work)`
- `handoffs/qa_to_dev.md=NOT written` (no blocking findings; AUTO_IMPLEMENTATION_LOOP does not return to /execute)
