# Sprint S0128 - Sprint Plan (US-0128)

## Metadata

| Field | Value |
|---|---|
| story_id | US-0128 |
| story_title | Convergence smoke surrogate for contract-test and waived-probe UAT slices |
| sprint_id | S0128 |
| delivery_mode | ultra_lean |
| macro_phase | plan (sprint-plan terminal; /plan-verify merged into build+verify under QA per ultra_lean) |
| current_phase | sprint-plan |
| approach | A1 locked (from R-0111 DQ1–DQ8) |
| companion_DEC | none (align with DEC-0110 §10 + DEC-0078; new DEC would duplicate governance per R-0111) |
| research_anchor | R-0111 (DQ1–DQ8 LOCKED) |
| orchestrator_run_id | auto-20260826-01 |
| fresh_context_marker | tl-US0128-sprint-plan-2026-08-26T201100Z-fresh |
| timestamp | 2026-08-26T20:11:00Z (UTC) |
| model_id | cursor-grok-4.6-high (CROSS_MODEL_REVIEW=1 — required on isolation; glm-5.2-high unavailable this spawn) |
| verdict | PASS |
| decision_gate | false |
| SPRINT_MAX_TASKS | 12 |
| SPRINT_AUTO_SPLIT | 1 |
| task_count | 8 (T-anch + T-001..T-007; within 12; no split) |
| COMPONENT_SCOPE_MODE | 0 |
| USER_GUIDE_MODE | 0 |
| plan-verify | ultra_lean — merged into build+verify under QA; plan-verify.json NOT written here |
| backlog_status | OPEN (US-0045 — not mutated; acceptance L156 unchecked) |
| critic_carry_ins | 0 new blocking; 3 architecture critic NBs `a0128arch-*` status=resolved non-blocking — routed as awareness into /execute (below) |

## Scope summary

Ship the convergence-loop drift fix for **US-0128**: add a surrogate evaluation branch to `_eval_smoke_green` in `scripts/sovereign_convergence_lib.py` (L459–470) so ultra_lean/docs/contract-test slices whose active `uat.json` documents all 6 canonical live-runtime probe classes (`browser_smoke`, `api_health`, `process_health`, `cli_smoke`, `build`, `manual_operator`) as `UAT_PROBE_FORBIDDEN` in `waived_probes[]` and emits NO smoke-named step can still satisfy the `smoke_green` conjunct (DEC-0110 §10) when `tests/report.md` Fail:0 + `contract_test_failed=0` + a canonical `convergence_smoke` uat step (or tail `probe_kind=contract_tests_primary` step with `result=pass`) is present. Legacy `_uat_smoke_passes` path unchanged — real smoke-named step PASS still satisfies the conjunct (precedence case 1). `CONVERGENCE_SMOKE_PROBE_FAIL` retained for real smoke step failures and US-0109 deploy smoke. New `CONVERGENCE_SMOKE_SURROGATE_MISSING` for surrogate prerequisites unmet (cases 4–8). US-0109 deploy smoke precedence orthogonal and unchanged (case 9). `ConjunctResult(name="smoke_green", …)` shape unchanged — surrogate is an additional PASS path inside the same conjunct.

Additive `### Convergence smoke surrogate (US-0128)` subsections in `.cursor/commands/qa.md` and `.cursor/commands/verify-work.md` (+ template mirrors) under `## Self-verify UAT probes (US-0092 / DEC-0078)` after `### Browser UAT self-test (US-0093)` before `## Steps`. 11 `test_us0128_*` markers in `tests/us0128_contract_test.py` (+ template mirror). Runbook `### Smoke surrogate for waived-probe UAT slices (US-0128)` subsection after `### Blocking-only conjunct-3 semantics (US-0127)` (L2811) before `### Interpret \`goal_progress\` block` (L2829). `reason_codes.md` `## US-0128` section after US-0127 section (L109–L125) before `## US-0104` (L126). `SOVEREIGN_CONVERGENCE_PAIRS` additive rows for `qa.md` ↔ `template/.cursor/commands/qa.md` and `verify-work.md` ↔ `template/.cursor/commands/verify-work.md`; `--scope=sovereign-convergence` extended automatically via the tuple union.

This is an **additive code + docs + parity + contract-test** change. Composes read-only with US-0109, US-0126, US-0127, US-0110, US-0104, US-0045, US-0048/BUG-0006, US-0056. No new DEC. No backlog Status/AC mutation. No intake JSON mutation. No DONE rows US-0108/US-0121..US-0127 reopened. No US-0129/US-0130 mutation. Do not rewrite `docs/engineering/architecture.md`.

Out of scope: dropping surrogate step requirement (A5 rejected); relaxing `_uat_smoke_passes` to accept any `probe_kind=contract_tests_primary` step (A3 rejected); auto-emitting synthetic smoke step from convergence lib (A4 rejected); using `id=convergence_surrogate` (A2 rejected — loses defense in depth); companion DEC-0128 (A6 rejected — duplicates DEC-0110 §10 / DEC-0078 governance); reopening US-0126; mutating DONE rows; amending US-0104/US-0110/US-0109/US-0127 surfaces.

## Execute awareness (architecture critic NBs — 0 blocking)

Sovereign-critic of architecture PASS (`tl-US0128-sovereign-critic-architecture-20260826T195900Z-fresh`; anti_slop=8; 0 blocking). Route these resolved NBs as execute awareness — do not re-open them as work:

| Finding | Issue key | Execute awareness |
|---|---|---|
| `a0128arch-challenger-001` | `ik_us0128_arch_proof_and_boundary_gaps` | **T-001** must preserve legacy-first ordering (A1): `_uat_smoke_passes` before surrogate branch. `id=convergence_smoke` will also match `_step_is_smoke` (R6 defense-in-depth) — do not invert order. **T-002** must emit explicit `convergence_smoke` on new slices; S0126 `steps[]` lack `probe_kind` so tail fallback cannot satisfy the S0126 fixture as-is (R7; marker 11: reference only). **T-001** fail-closed `CONVERGENCE_SMOKE_SURROGATE_MISSING` when neither top-level `contract_test_failed` nor derived passed==total is present. **T-007** marker 4: partial waivers must not false-pass. |
| `a0128arch-architect-002` | `ik_us0128_arch_layer_compose_boundaries` | Keep layering: T-001 owns lib surrogate only; T-002 owns qa.md/verify-work.md emission; T-003 owns reason_codes; T-004 owns 11 markers; T-005/T-006 own runbook + `SOVEREIGN_CONVERGENCE_PAIRS`. No lib-side `uat.json` synthesis (A4 rejected). Do not touch `_eval_critic_resolved` / `SOVEREIGN_CRITIC_PAIRS` (marker 10). |
| `a0128arch-subtractor-003` | `ik_us0128_arch_scope_discipline` | Do not mark US-0128 DONE; do not tick L156; 11 markers are required (not YAGNI); T-anch is read-only ceremony — no architecture.md mutation in /execute. |

## Acceptance criteria (6) - US-0128 (status OPEN, acceptance L156 unchecked per US-0045)

- **AC-1**: Surrogate eval — Extend `_eval_smoke_green` to accept surrogate when active uat.json has all smoke probe classes waived with `UAT_PROBE_FORBIDDEN` and `contract_test_failed=0`.
- **AC-2**: Canonical uat step — Require uat step `convergence_smoke` (or `probe_kind=contract_tests_primary` tail step) with `result=pass` written by `/verify-work` or `/qa`.
- **AC-3**: Fail closed — Emit `CONVERGENCE_SMOKE_SURROGATE_MISSING` when uat exists, harness Fail>0, or waived_probes incomplete.
- **AC-4**: Command contracts — Update `/qa` and `/verify-work` command contracts to emit convergence smoke step for ultra_lean/docs slices.
- **AC-5**: Contract tests — S0126-style waived uat PASS, missing surrogate FAIL, US-0109 deploy smoke unchanged.
- **AC-6**: Operator docs + parity — Runbook convergence section documents surrogate rules; template parity for convergence lib + command mirrors.

## Task summaries (8 - T-anch + T-001..T-007)

- **T-anch** (NO-OP / verification): Verify `# US-0128` H1 anchor in `docs/engineering/architecture.md` at L1671 (after `# US-0127` L1552, before `# US-0091` L1818 per DEC-0073 §11); verify approach A1 + R-0111 DQ1–DQ8 LOCKED; verify compose-do-not-amend 8/8 baseline; verify 11-marker contract-test list locked; verify command/runbook/reason-code/parity placement anchors; verify `tests/us0128_contract_test.py` + template mirror do NOT yet exist; verify `_eval_smoke_green` root cause at L459–470 still present. Record to `sprints/S0128/t-anch-verification.md`. NO mutation to `architecture.md` in /execute.
- **T-001** (AC-1 — Surrogate eval branch + template mirror): Edit `scripts/sovereign_convergence_lib.py` AND template mirror. Legacy path first via `_uat_smoke_passes`; if FAIL, evaluate surrogate prerequisites (6 waived_probes `UAT_PROBE_FORBIDDEN` + `contract_test_failed=0` + surrogate step). Shape of `ConjunctResult(name="smoke_green", …)` unchanged. `_uat_smoke_passes` and `_step_is_smoke` unchanged.
- **T-002** (AC-2+AC-4 — Command contracts + template mirrors): Additive `### Convergence smoke surrogate (US-0128)` subsections in qa.md + verify-work.md (+ mirrors) after `### Browser UAT self-test (US-0093)` before `## Steps`. Emit `convergence_smoke` step for ultra_lean/docs/contract-test slices when all 6 live-runtime classes are waived.
- **T-003** (AC-3 — Fail-closed reason code + template mirror): New `## US-0128` section in `reason_codes.md` with `CONVERGENCE_SMOKE_SURROGATE_MISSING` + clarifying note on US-0110 `CONVERGENCE_SMOKE_PROBE_FAIL` row (description only).
- **T-004** (AC-5 — Contract tests): Create `tests/us0128_contract_test.py` with 11 markers + template mirror (includes T-007 markers 4, 5, 7).
- **T-005** (AC-6 — Runbook subsection + template mirror): New `### Smoke surrogate for waived-probe UAT slices (US-0128)` after US-0127 blocking-only subsection before Interpret `goal_progress` block.
- **T-006** (AC-6 — Parity): Add 2 NEW rows to `SOVEREIGN_CONVERGENCE_PAIRS` for qa.md and verify-work.md command mirrors. `SOVEREIGN_CRITIC_PAIRS` unchanged.
- **T-007** (R1+R3 — Regression guards): Author markers 4, 5, 7 inside T-004 file (partial waivers fail-closed; real smoke pass wins; US-0109 deploy smoke unchanged).

Execution order: T-anch → T-001 → T-002 → T-003 → T-004 (with T-007 markers 4,5,7 authored within) → T-005 → T-006 → integration verification (acyclic; 8 tasks within SPRINT_MAX_TASKS=12; no split).

## AC -> Task surjective coverage

| AC | Task(s) |
|---|---|
| AC-1 (Surrogate eval) | T-001, T-004 (markers 1, 2, 3, 4, 5, 6, 8, 9), T-007 (markers 4, 5) |
| AC-2 (Canonical uat step) | T-002, T-004 (markers 5, 7, 8) |
| AC-3 (Fail closed) | T-003, T-004 (markers 2, 3, 4, 6) |
| AC-4 (Command contracts) | T-002, T-004 (markers 5, 7, 8) |
| AC-5 (Contract tests) | T-004 (all 11 markers), T-007 (markers 4, 5, 7) |
| AC-6 (Operator docs + parity) | T-005 (runbook subsection), T-006 (SOVEREIGN_CONVERGENCE_PAIRS + 2 command rows) |

**Surjectivity check**: 6/6 ACs covered (each AC has at least 1 task). No `PLAN_AC_COVERAGE_GAP`.

## Risks (R1–R7 — accepted from architecture)

| Risk | Severity | Mitigation in this sprint |
|---|---|---|
| R1 surrogate masks real smoke if waived_probes over-broad | HIGH | T-001 legacy-first; T-007 markers 5 + 7 |
| R2 `contract_test_failed` absent in older fixtures | MEDIUM | T-001 derived fallback; fail-closed when neither present; marker 3 |
| R3 partial-waiver ambiguity | MEDIUM | T-001 fail-closed; T-007 marker 4 |
| R4 runbook section-anchor drift | LOW–MEDIUM | T-005 grep by heading text, not line number |
| R5 command-mirror parity gap | LOW | T-006 `SOVEREIGN_CONVERGENCE_PAIRS` +2; marker 8 |
| R6 `id=convergence_smoke` also matches `_step_is_smoke` | LOW | Intentional defense-in-depth; T-001 preserve legacy-first; T-005 documents |
| R7 S0126 steps lack `probe_kind` | LOW | Marker 11: S0126 is waived_probes[] shape reference only; T-002 emits explicit step on new slices |

## Compose guards (8/8 UNCHANGED — additive code + docs + parity + contract-test only)

| Compose target | Verification | Result |
|---|---|---|
| US-0109 (deploy smoke / `DEPLOY_SMOKE_*`) | surrogate path is `/qa`/`/verify-work` UAT only; marker 7 | compose |
| US-0126 (`sprints/S0126/uat.json` fixture) | reference fixture only; marker 11; DONE not reopened | compose |
| US-0127 (`_eval_critic_resolved` / hygiene / `SOVEREIGN_CRITIC_PAIRS`) | US-0128 touches `smoke_green` only; marker 10 | compose |
| US-0110 (five-conjunct / `CONVERGENCE_SMOKE_PROBE_FAIL`) | additional PASS path inside same conjunct; marker 9 | compose |
| US-0104 (critic findings JSONL) | not touched | compose |
| US-0045 (canonical closure) | backlog Status/ACs not mutated | compose |
| US-0048 / BUG-0006 | this subagent fresh; no prior chat | compose |
| US-0056 (runtime proof) | this phase issues its own proof; architecture proof consumed MATCH | compose |

## Execute phase role (per DEC-0051 / US-0069)

| Phase | Role | Isolation |
|---|---|---|
| /execute | dev (fresh per BUG-0006) | {phase_id:execute, role:dev} |
| /qa | qa (fresh) | {phase_id:qa, role:qa} — creates plan-verify.json within build+verify per ultra_lean |
| /verify-work | qa (fresh) | {phase_id:verify-work, role:qa} |
| /release | release (fresh) | {phase_id:release, role:release} |
| /closure | qe (fresh) | {phase_id:closure, role:qe} |
| /refresh-context | curator (fresh) | {phase_id:refresh-context, role:curator} |

## Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

| Field | Value |
|---|---|
| phase_id | sprint-plan |
| role | tech-lead |
| story_id | US-0128 |
| sprint_id | S0128 |
| orchestrator_run_id | auto-20260826-01 |
| delivery_mode | ultra_lean |
| macro_phase | plan |
| fresh_context_marker | tl-US0128-sprint-plan-2026-08-26T201100Z-fresh |
| timestamp | 2026-08-26T20:11:00Z (UTC) |
| model_id | cursor-grok-4.6-high (CROSS_MODEL_REVIEW=1 — required; glm-5.2-high unavailable this spawn) |
| evidence_ref | sprints/S0128/sprint.md, sprints/S0128/tasks.md, sprints/S0128/progress.md, sprints/S0128/uat.json, sprints/S0128/uat.md, handoffs/tl_to_dev.md (US-0128 prepend), docs/engineering/state.md (sprint-plan checkpoint append-bottom + traceability row), docs/engineering/architecture.md # US-0128 (L1671 — not mutated), handoffs/resume_brief.md |

Prior phase proof consumed: `rp-auto-20260826-01-architecture-tech-lead-2026-08-26T195500Z-US-0128` (proof_hash=FF499010B78C4FB7855E9D6F4482227AD7B258230671D67E4E2B42571A68A969, ttl 2026-08-26T20:55:00Z — independent SHA-256 MATCH; consumed at 2026-08-26T20:11:00Z before RUNTIME_PROOF_STALE). Sovereign-critic architecture PASS at 2026-08-26T19:59:00Z (anti_slop_aggregate=8; 0 blocking findings; 3 NBs `a0128arch-*` status=resolved).

## Runtime proof (DEC-0038)

| Field | Value |
|---|---|
| runtime_proof_id | rp-auto-20260826-01-sprint-plan-tech-lead-2026-08-26T201100Z-US-0128 |
| phase_id | sprint-plan |
| role | tech-lead |
| story_id | US-0128 |
| sprint_id | S0128 |
| orchestrator_run_id | auto-20260826-01 |
| delivery_mode | ultra_lean |
| macro_phase | plan |
| model_id | cursor-grok-4.6-high (CROSS_MODEL_REVIEW=1 — required; glm-5.2-high unavailable this spawn) |
| proof_issued_at | 2026-08-26T20:11:00Z |
| proof_ttl_seconds | 3600 |
| proof_ttl | 2026-08-26T21:11:00Z (UTC) |
| proof_hash | C911D7C5CAA2939EC6F65ED07C717E9CBB00E80B551DCBFECA097D39F26878F4 |
| canonical_payload | `{"delivery_mode":"ultra_lean","macro_phase":"plan","model_id":"cursor-grok-4.6-high","orchestrator_run_id":"auto-20260826-01","phase_id":"sprint-plan","proof_issued_at":"2026-08-26T20:11:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260826-01-sprint-plan-tech-lead-2026-08-26T201100Z-US-0128","sprint_id":"S0128","story_id":"US-0128"}` |

## Decision gate

| Field | Value |
|---|---|
| decision_gate | false |
| stop_conditions_met | yes |
| missing_acceptance_criteria | none (6/6 ACs covered; 11 contract-test markers; compose guards 8/8) |
| compose_guards | 8/8 UNCHANGED |
| dc_check | clean (`# US-0128` H1 already added in /architecture at L1671) |
| task_count | 8 (within SPRINT_MAX_TASKS=12; SPRINT_AUTO_SPLIT=1 but no split needed) |
| risks_finalized | 7/7 ACCEPTED (R1..R7) |
| approach | A1 locked |
| companion_DEC | none |
| plan-verify readiness | ultra_lean — /plan-verify merged into build+verify under QA; plan-verify.json NOT written in this spawn |
| sovereign_memory_note | `assemble_sovereign_memory_digest(...)` NOT called; no mistakes.jsonl write |

## Definition of done (sprint-plan)

- [x] 8 tasks enumerated (T-anch + T-001..T-007) — within SPRINT_MAX_TASKS=12
- [x] 6/6 ACs covered by 11 contract-test markers + compose guards 8/8 (surjective)
- [x] Task dependency graph documented
- [x] Execute phase role matrix documented (ultra_lean — /plan-verify merged into build+verify under QA)
- [x] Compose guards 8/8 UNCHANGED
- [x] Critic carry-ins (3 non-blocking from architecture sovereign-critic) routed as execute awareness
- [x] Isolation evidence + runtime proof emitted (model_id=cursor-grok-4.6-high present)
- [x] Sprint-plan checkpoint appended to `docs/engineering/state.md`
- [x] Sprint-plan handoff prepended to `handoffs/tl_to_dev.md`
- [x] Sprint-plan PASS prepended to `handoffs/resume_brief.md` (-> /execute)
- [x] UAT placeholders written (`uat.json` empty steps, `uat.md` ACs no results)
- [x] Traceability row added to `docs/engineering/state.md` (Story=US-0128 | Sprint=S0128 | Tasks=T-anch+T-001..T-007 | Status=PLANNED | Evidence empty)
- [x] Backlog status OPEN (US-0045 — not mutated); AC checkboxes untouched

## Next scheduled phase

| Field | Value |
|---|---|
| next_scheduled_phase | `/execute` (role=dev per US-0069 / DEC-0051; fresh dev subagent per BUG-0006; first canonical phase of `build+verify` macro per ultra_lean; /plan-verify merged into qa per ultra_lean — qa creates plan-verify.json within build+verify) |
| next_scheduled_role | dev |
| next_sprint_macro | build+verify (ultra_lean — plan-verify merged into qa) |
| stop_condition | STOP after sprint-plan completes; hand off via artifacts only to /execute in fresh dev subagent per BUG-0006. Do not spawn /execute from this subagent. |
| artifacts_written | sprints/S0128/ (sprint.md, tasks.md, progress.md, uat.json, uat.md), docs/engineering/state.md (sprint-plan checkpoint append-bottom + traceability row), handoffs/tl_to_dev.md (US-0128 prepend), handoffs/resume_brief.md (sprint-plan PASS prepend -> /execute) |
