# QA findings — BUG-0016 / S0132 / auto-20260906-bug0016 (qa)

- **phase_id**: qa, **role**: qa, **bug_id**: BUG-0016 (OPEN — not marked DONE per US-0045), **sprint_id**: S0132
- `orchestrator_run_id=auto-20260906-bug0016`, `delivery_mode=ultra_lean`, `macro_phase=build+verify`
- `AUTO_IMPLEMENTATION_LOOP=1`
- `model_id=composer-2.5` (CROSS_MODEL_REVIEW=1 — required on isolation)
- `producer_phase_id=execute`, `producer_role=dev`, `producer_model_id=composer-2.5`
- `critic_phase_id=sovereign-critic` (execute review), `critic_model_id=composer-2.5-fast`, `critic_verdict=PASS`, `anti_slop_aggregate=10`, `open_blocking_findings=0`
- `critic_fresh_context_marker=critic-BUG0016-execute-20260906T191000Z-fresh`
- `fresh_context_marker=qa-BUG0016-qa-20260906T191500Z-fresh` (NEW per US-0048 / BUG-0006; not reused from producer/critic markers)
- `timestamp (UTC)=2026-09-06T19:15:00Z`
- **verdict: QA_PASS**
- `plan_verify_verdict=PASS` (ultra_lean deferred — `sprints/S0132/plan-verify.json`; AC surjective 8/8 + DQ8 via T-007)
- `blocking_count=0`
- `non_blocking_count=3` (execute-critic carry-forwards — informational; not new blockers)
- `story_status=OPEN` (do not mark BUG-0016 DONE; acceptance L181 unchecked; intake JSON not mutated)
- `acceptance_L181=NOT ticked`
- `intake_json=NOT mutated`
- `FRAMEWORK_KIT_REPO=1` / OpenCode Layer-1 permission contract story — no web UI; **no fake browser PASS**
- `SECURITY_REVIEW=0`, `CROSS_REPO_OBSERVABILITY=0`, `COMPONENT_SCOPE_MODE=0`

## Verdict rationale

Fresh QA independently remapped AC-1..AC-8 against architecture `# BUG-0016` + tasks.md, created deferred `plan-verify.json` (PASS / surjective), and re-ran contract + compose gates. All green. Eight agents + test/parity peers byte-identical active↔template. Compose DEC-0124/0125 untouched. Status OPEN preserved. Canonical probe class = `contract_tests_primary` (7 markers). Live OpenCode / browser probes waived (`UAT_PROBE_FORBIDDEN`). `convergence_smoke` surrogate emitted because `contract_test_failed=0`.

## Test plan

| # | Check | Expected |
|---|---|---|
| 1 | Independent AC-1..AC-8 remap vs architecture + tasks | Each AC ≥1 task + marker; DQ8 via T-007 |
| 2 | Create `sprints/S0132/plan-verify.json` (ultra_lean deferred) | PASS / surjective 8/8 |
| 3 | `python -m pytest tests/bug0016_contract_test.py -v` | 7/7 PASS |
| 4 | `python -m pytest tests/us0122_contract_test.py -q` | 8/8 PASS (intentional realign) |
| 5 | `python scripts/check_intake_template_parity.py --scope=bug-0016` | `[INTAKE_TEMPLATE_PARITY_OK]` |
| 6 | `python scripts/enforce-triad-hot-surface.py --check` | exit 0 |
| 7 | `python scripts/check-user-visible-metadata.py --repo . --json` | OK / 0 violations |
| 8 | Active↔template byte identity (8 agents + test peers) | IDENTICAL |
| 9 | Status OPEN; L181 unchecked; BUG-0015 DONE preserved | unchanged |
| 10 | UAT probes | `contract_tests_primary` PASS; live classes waived |
| 11 | Emit `convergence_smoke` when `contract_test_failed=0` | present, `result=pass` |
| 12 | Independent execute proof hash | MATCH `519A7617…` before TTL 20:05:00Z |

## Independent checks (this qa subagent)

| Check | Command / method | Result |
|---|---|---|
| Execute proof SHA-256 | Python hashlib sorted-key compact JSON | **MATCH** `519A7617F1ADBEAFD95A940AF28B130F8EB309350F3F787C0AC02152FBEC76BF`; ttl `2026-09-06T20:05:00Z`; consumed_at `2026-09-06T19:15:00Z` |
| BUG-0016 contract tests | `python -m pytest tests/bug0016_contract_test.py -v` | **7 passed** in 0.03s |
| US-0122 compose tests | `python -m pytest tests/us0122_contract_test.py -q` | **8 passed** in 0.03s |
| Parity scope bug-0016 | `python scripts/check_intake_template_parity.py --scope=bug-0016` | **exit 0** — `[INTAKE_TEMPLATE_PARITY_OK]` |
| Triad hot-surface | `python scripts/enforce-triad-hot-surface.py --check` | **exit 0** |
| User-visible metadata | `python scripts/check-user-visible-metadata.py --repo . --json` | **OK** / `violations: []` |
| Full harness `tests/run-tests.ps1` | not re-run this pass | **not claimed** — slice contract tests are the required evidence for this permission-matrix contract story |

## AC remap (independent)

| AC | Delivered surface | Task(s) / markers | Result |
|---|---|---|---|
| AC-1 bash ask po/tl/curator | `bash: ask` on po/tech-lead/curator | T-001, T-002; m1 | **PASS** |
| AC-2 PO intake/resume/state | intake_evidence/** + resume_brief + state.md; `**` deny last | T-001; m2 | **PASS** |
| AC-3 S* sprint globs | `sprints/S*/…` keys; no `Sxxxx` | T-002, T-003; m3 | **PASS** |
| AC-4 release duty paths | release-findings + verify-work-to-release + state + resume_brief + runbook | T-004; m4 | **PASS** (CF2 informational) |
| AC-5 success test (c) | non-dev no production/code allow; deny-last | T-anch, T-005; m5 | **PASS** |
| AC-6 security/auto unchanged | security edit deny + bash ask; auto spawn-only | T-anch; m6 | **PASS** |
| AC-7 active↔template parity | eight agents byte-identical | T-001..T-004; m7 | **PASS** |
| AC-8 DEC-0122 sole SOT | §2 sole matrix; us0122 realign; no DEC-0130 | T-anch, T-005 | **PASS** |
| DQ8 Layer-1 ∩ write-guard | no duty-glob re-deny; DEC-0124/0125 untouched | T-007 | **PASS** |

## Contract marker results (7/7)

| # | Marker | Result |
|---|---|---|
| 1 | `test_bug0016_po_tl_curator_bash_ask` | PASS |
| 2 | `test_bug0016_po_intake_resume_state_allows` | PASS |
| 3 | `test_bug0016_sprint_globs_are_s_star_not_sxxxx` | PASS |
| 4 | `test_bug0016_release_duty_paths` | PASS |
| 5 | `test_bug0016_success_test_c_non_dev_no_production_allow` | PASS |
| 6 | `test_bug0016_security_auto_unchanged` | PASS |
| 7 | `test_bug0016_active_template_agent_parity` | PASS |

## Template byte-identity (touched pairs)

| Pair | Bytes | Result |
|---|---|---|
| `.opencode/agents/po.md` ↔ template | 673b = 673b | IDENTICAL |
| `.opencode/agents/tech-lead.md` ↔ template | 769b = 769b | IDENTICAL |
| `.opencode/agents/curator.md` ↔ template | 733b = 733b | IDENTICAL |
| `.opencode/agents/dev.md` ↔ template | 676b = 676b | IDENTICAL |
| `.opencode/agents/qa.md` ↔ template | 727b = 727b | IDENTICAL |
| `.opencode/agents/release.md` ↔ template | 875b = 875b | IDENTICAL |
| `.opencode/agents/security.md` ↔ template | 417b = 417b | IDENTICAL |
| `.opencode/agents/auto.md` ↔ template | 614b = 614b | IDENTICAL |
| `tests/bug0016_contract_test.py` ↔ template | 9943b = 9943b | IDENTICAL |
| `tests/us0122_contract_test.py` ↔ template | 9813b = 9813b | IDENTICAL |
| `scripts/check_intake_template_parity.py` ↔ template | 27776b = 27776b | IDENTICAL |

## Findings

### Blocking

None. `blocking_count=0`. No `handoffs/qa_to_dev.md`.

### Non-blocking (execute-critic carry-forwards)

- **NB-1** (`b0016ex-challenger-001` / `ik_bug0016_exec_edge_and_proof`): Keep `S*` (not `S[0-9]*`); preserve deny-last + non-dev no production/code allow; T-007 no-double-deny stance holds (QA reconfirmed — no contradiction). plan-verify.json created within ultra_lean QA.
- **NB-2** (`b0016ex-architect-002` / `ik_bug0016_exec_layer_coupling`): DEC-0122 §2 sole SOT; CF2 runbook Layer-1 allow ≠ US-0126 ownership; do not invent DEC-0130 / permissions middleware. Confirmed.
- **NB-3** (`b0016ex-subtractor-003` / `ik_bug0016_exec_scope_minimal`): Do not mark BUG-0016 DONE; do not tick acceptance; do not reopen BUG-0015 / US-0131 / US-0132; no `bash:allow`; no live OpenCode probe; no DEC-0124/0125 amend. Scope held.

## UAT probes (permission-matrix contract — honest classification)

Applicable probe class: **`contract_tests_primary`** (7 markers). No web UI. **No fake browser PASS.** Live-runtime probes **not attempted** (`UAT_PROBE_FORBIDDEN`).

Canonical surrogate step **`convergence_smoke`** emitted (`result=pass`) because `contract_test_failed=0`.

| Probe class | Result | reason_code |
|---|---|---|
| `contract_tests_primary` | PASS (7/7) | `UAT_PROBE_PASS` |
| `browser_smoke` | waived / not applicable | `UAT_PROBE_FORBIDDEN` |
| `api_health` | waived / not applicable | `UAT_PROBE_FORBIDDEN` |
| `process_health` | waived / not applicable | `UAT_PROBE_FORBIDDEN` |
| `cli_smoke` | waived (static harness only; no live OpenCode CLI probe) | `UAT_PROBE_FORBIDDEN` |
| `build` | not applicable | `UAT_PROBE_FORBIDDEN` |
| `manual_operator` | not applicable | `UAT_PROBE_FORBIDDEN` |

**Runtime browser evidence**: none. MCP browser sequence **not run**. No screenshot. No silent browser PASS.

## Runtime QA evidence (US-0065)

- `runtime_stack_profile`: `python` (static agent-frontmatter + DEC-0122 contract harness)
- `runtime_mode`: local
- `runtime_startup_command`: driven via `python -m pytest tests/bug0016_contract_test.py -v`
- `runtime_health_target`: pytest exit + 7/7 markers + us0122 8/8
- `runtime_health_result`: PASS (7 passed in 0.03s; us0122 8 passed in 0.03s)
- `runtime_log_summary`: 0 errors / 0 warnings / 15 pass (7+8)
- `runtime_retry_count`: 0
- `runtime_retry_ledger`: []
- `runtime_final_verdict`: pass
- `runtime_reason_code`: `UAT_PROBE_FORBIDDEN` for live OpenCode/browser; health = contract tests + `convergence_smoke`
- `runtime_evidence_refs`: pytest 7/7; us0122 8/8; parity `--scope=bug-0016`; `sprints/S0132/uat.json` `convergence_smoke`

## Generated-test evidence (US-0066)

- `generated_test_stack_profile`: python
- `generated_test_command`: `python -m pytest tests/bug0016_contract_test.py -v`
- `generated_test_result`: pass
- `generated_test_output_ref`: this file § Independent checks (7 passed in 0.03s)
- `generated_test_paths_ref`: `tests/bug0016_contract_test.py`
- `generated_test_reason_code`: none (pass)

## Status confirmation (US-0045)

- backlog `### BUG-0016` Status: **OPEN** (L4914)
- acceptance L181: **unchecked**
- BUG-0015 remains DONE (not reopened)
- intake JSON not mutated
- architecture.md `# BUG-0016` not mutated this phase
- DEC-0124 / DEC-0125 bodies not mutated
- DEC-0122 §2 sole SOT (no DEC-0130)

## Plan-verify (ultra_lean merged)

- path: `sprints/S0132/plan-verify.json`
- verdict: **PASS**
- coverage_complete: true
- uncovered_acs: []
- plan-verify runtime_proof_id: `rp-auto-20260906-bug0016-plan-verify-qa-20260906T191500Z-BUG-0016`
- plan-verify proof_hash: `B7272F32D7B432CEEDDF2A7C70CFCB633CA6A9AF2B8C5FAADF33DFAF07BF01AB`

## Producer proof consumed (execute)

- `producer_runtime_proof_id=rp-auto-20260906-bug0016-execute-dev-20260906T190500Z-BUG-0016`
- Canonical payload: `{"delivery_mode":"ultra_lean","macro_phase":"build+verify","model_id":"composer-2.5","orchestrator_run_id":"auto-20260906-bug0016","phase_id":"execute","proof_issued_at":"2026-09-06T19:05:00Z","proof_ttl_seconds":3600,"role":"dev","runtime_proof_id":"rp-auto-20260906-bug0016-execute-dev-20260906T190500Z-BUG-0016","sprint_id":"S0132","story_id":"BUG-0016"}`
- `producer_attested_proof_hash=519A7617F1ADBEAFD95A940AF28B130F8EB309350F3F787C0AC02152FBEC76BF`
- Independent SHA-256 recompute: **MATCH**
- `producer_proof_ttl=2026-09-06T20:05:00Z`, `consumed_at=2026-09-06T19:15:00Z` (before RUNTIME_PROOF_STALE)

## Strict runtime proof (DEC-0038) — qa

- `orchestrator_run_id=auto-20260906-bug0016`
- `runtime_proof_id=rp-auto-20260906-bug0016-qa-qa-20260906T191500Z-BUG-0016`
- `phase_id=qa`, `role=qa`, `story_id=BUG-0016`, `sprint_id=S0132`
- `proof_issued_at=2026-09-06T19:15:00Z`
- `proof_ttl_seconds=3600`, `proof_ttl=2026-09-06T20:15:00Z`
- `proof_hash=2258AE43B09997167501DD437B38DBA1A01356D1D09991707C1098EBC8D5523D`
- Canonical payload: `{"delivery_mode":"ultra_lean","macro_phase":"build+verify","model_id":"composer-2.5","orchestrator_run_id":"auto-20260906-bug0016","phase_id":"qa","proof_issued_at":"2026-09-06T19:15:00Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260906-bug0016-qa-qa-20260906T191500Z-BUG-0016","sprint_id":"S0132","story_id":"BUG-0016"}`

## Isolation evidence (US-0048 / DEC-0029)

- `phase_id=qa`
- `role=qa`
- `model_id=composer-2.5` (CROSS_MODEL_REVIEW=1)
- `fresh_context_marker=qa-BUG0016-qa-20260906T191500Z-fresh`
- `timestamp=2026-09-06T19:15:00Z`
- `evidence_ref=sprints/S0132/qa-findings.md + sprints/S0132/plan-verify.json + sprints/S0132/uat.json + handoffs/qa_to_verify.md + handoffs/resume_brief.md + docs/engineering/state.md`

## Next phase

- **PASS → `/verify-work`** (fresh qa subagent per BUG-0006). Do NOT mark BUG-0016 DONE. Do NOT tick acceptance L181. Do NOT mutate intake JSON. Do NOT reopen BUG-0015. Do NOT spawn `/verify-work` from this qa subagent.
