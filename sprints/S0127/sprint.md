# Sprint S0127 - Sprint Plan (US-0127)

## Metadata

| Field | Value |
|---|---|
| story_id | US-0127 |
| story_title | Convergence critic conjunct — blocking-only open findings plus non-blocking auto-resolve at sovereign-critic PASS |
| sprint_id | S0127 |
| delivery_mode | ultra_lean |
| macro_phase | plan (sprint-plan — terminal canonical phase per ultra_lean; /plan-verify runs standalone per orchestrator brief, role=qa) |
| current_phase | sprint-plan |
| approach | A1 locked (from R-0110 DQ1–DQ8) |
| companion_DEC | none (align with DEC-0110 §10 / DEC-0104 §11; new DEC would duplicate governance per R-0110) |
| research_anchor | R-0110 (DQ1–DQ8 LOCKED) |
| orchestrator_run_id | auto-20260825-01 |
| fresh_context_marker | tl-US0127-sprint-plan-20260825T185100Z-fresh |
| timestamp | 2026-08-25T18:51:00Z (UTC) |
| model_id | glm-5.2-high (CROSS_MODEL_REVIEW=1 — required) |
| verdict | PASS |
| decision_gate | false |
| SPRINT_MAX_TASKS | 12 |
| SPRINT_AUTO_SPLIT | 1 |
| task_count | 8 (T-anch + T-001..T-007; within 12; no split) |
| CROSS_MODEL_REVIEW | 1 (model_id=glm-5.2-high required) |
| COMPONENT_SCOPE_MODE | 0 |
| USER_GUIDE_MODE | 0 |
| plan-verify | standalone /plan-verify next (role=qa per orchestrator brief); plan-verify.json NOT written in this spawn |
| backlog_status | OPEN (US-0045 — not mutated) |
| ac_checkboxes | unchecked (US-0045 — not mutated) |
| critic_carry_ins | 0 new (3 architecture critic NBs noted in sovereign-critic of architecture — all non-blocking; routed as awareness into /execute via this sprint plan) |

## Scope summary

Ship the convergence-loop drift fix for **US-0127**: narrow `_critic_jsonl_has_open` in `scripts/sovereign_convergence_lib.py` (lines 318–331) to delegate to `sovereign_critic_lib.read_open_blocking(repo)` so that informational `status=open, blocking=false` PASS concurrence rows no longer block `CONVERGENCE_CROSS_REVIEWER_OPEN` (US-0110 L3 conjunct-3 requires "no open **blocking** cross-reviewer findings"). Add an auto-resolve hook at the end of `/sovereign-critic` (after `reconcile_findings` + JSONL append + isolation evidence, before `## Stop conditions`) that sets `status=resolved` on same-run same-phase non-blocking open rows when `read_open_blocking(repo) == []` (idempotent via `resolve_finding`; audit trail preserved). Ship a new operator-only `scripts/sovereign_critic_hygiene.py` (+ template mirror) with `--report` / `--resolve-nonblocking-for-run <id>` / `--dry-run` / `--confirm` / `--self-test` / `--all-phases` / `--phase-id <id>` and 6 deterministic reason codes. Add 13 `test_us0127_*` markers in `tests/us0127_contract_test.py` (+ template mirror). Add runbook subsections `### Blocking-only conjunct-3 semantics (US-0127)` + `### Hygiene CLI (US-0127)` and a `## US-0127` section in `reason_codes.md` (active + template byte-identical). Extend `SOVEREIGN_CRITIC_PAIRS` additively and extend `check_intake_template_parity.py --scope=sovereign-critic` to cover the hygiene script pair.

This is an **additive code + docs + parity + contract-test** change. It composes read-only with US-0104, US-0110, and US-0107. No new DEC (per R-0110 §Companion DEC recommendation). No backlog Status/AC mutation (US-0045). No intake JSON mutation. No DONE rows US-0108/US-0121..US-0126 reopened.

Out of scope: changing sovereign-critic lens logic; widening `read_open_blocking` signature (A2 rejected); dropping `_critic_jsonl_has_open` entirely (A3 rejected); auto-resolve via background scheduler (A4 rejected); hygiene CLI as a `--scope` on an existing script (A5 rejected); companion DEC-0127 (A6 rejected); reopening US-0126; mutating DONE rows; advisory lock for hygiene CLI (Q3 accepted: no — document operator-only-when-quiet contract).

## Acceptance criteria (6) - US-0127 (status OPEN, checkboxes untouched per US-0045)

- **AC-1**: **Blocking-only check** — Replace `_critic_jsonl_has_open` with blocking-only check matching US-0110 L3 and `read_open_blocking()` semantics.
- **AC-2**: **Auto-resolve non-blocking** — At `/sovereign-critic` PASS with zero blocking findings, auto-set `status=resolved` on same-run non-blocking rows (preserve audit trail).
- **AC-3**: **Hygiene CLI** — Add `scripts/sovereign_critic_hygiene.py` with `--report`, `--resolve-nonblocking-for-run`, `--dry-run` and deterministic reason codes.
- **AC-4**: **Contract tests** — open+blocking=false does not fail convergence; open+blocking=true does; auto-resolve idempotent on re-run.
- **AC-5**: **Operator docs** — Runbook + reason_codes.md document hygiene workflow and convergence conjunct semantics.
- **AC-6**: **Template parity** — `SOVEREIGN_CRITIC_PAIRS`; compose read-only with US-0104/US-0110/US-0107.

## Task summaries (8 - T-anch + T-001..T-007)

- **T-anch** (NO-OP / verification): Verify `# US-0127` H1 anchor in `docs/engineering/architecture.md` at L1852 (after `# US-0126`, before `# US-0091` per DEC-0073 §11); verify approach A1 locked + R-0110 DQ1–DQ8 LOCKED; verify compose-do-not-amend 8/8 baseline (US-0104, US-0110, US-0107, US-0045, US-0048/BUG-0006, US-0053/DEC-0035, US-0103/DEC-0103, US-0056); verify 13-marker contract-test list locked in architecture AC-4 table; verify runbook subsection placement anchors (`### Evaluate convergence` L2792, `### Interpret goal_progress block` L2811, `#### Parity enforcement` L2915, `#### Related artifacts` L2923) + `reason_codes.md` `## US-0110` section at L77–L107; verify `SOVEREIGN_CRITIC_PAIRS` does NOT yet exist in `scripts/check_intake_template_parity.py`; verify `scripts/sovereign_critic_hygiene.py` + template mirror + `tests/us0127_contract_test.py` + template mirror do NOT yet exist; verify `_critic_jsonl_has_open` root cause at `scripts/sovereign_convergence_lib.py` L318–331 still present; verify `read_open_blocking` at `scripts/sovereign_critic_lib.py` L386–400; verify `resolve_finding` at `scripts/sovereign_critic_lib.py` L403. Record to `sprints/S0127/t-anch-verification.md`. T-anch is NO-OP / verification only — NO mutation to `architecture.md` in /execute. (AC-1, AC-2 baseline; NO-OP / verification only)
- **T-001** (AC-1 — Convergence lib fix + DQ6 dispatch): Edit `scripts/sovereign_convergence_lib.py` (+ `template/scripts/sovereign_convergence_lib.py` byte-identical mirror) per architecture DQ1+DQ6 LOCKED. Replace `_critic_jsonl_has_open` body (L318–331) with a delegate to `sovereign_critic_lib.read_open_blocking(repo)` (import; do not redefine — compose read-only on US-0104). Change `_eval_critic_resolved` dispatch (L372–404): when `handoffs/sovereign_critic_findings.jsonl` exists and is non-empty, the JSONL blocking-only predicate is authoritative and `_qa_findings_has_open_critic` is NOT consulted; when JSONL absent, fall back to the unchanged QA-markdown grep heuristic; when neither deployed, informational skip per US-0110 L3 degrade matrix. `_qa_findings_has_open_critic` and `_qa_has_cross_reviewer_section` predicates unchanged. MUST keep active ↔ template byte-identical after edit. Tests: markers 1, 2, 11, 12, 13. (AC-1)
- **T-002** (AC-2 — Auto-resolve hook + helper): Edit `.cursor/commands/sovereign-critic.md` (+ `template/.cursor/commands/sovereign-critic.md` byte-identical mirror) per architecture DQ1 LOCKED. Add a single conditional call at the end of the command after `reconcile_findings` + JSONL append + isolation evidence, before `## Stop conditions`: `if read_open_blocking(repo) == []: auto_resolve_nonblocking_for_run(repo, orchestrator_run_id, phase_id)`. Add `auto_resolve_nonblocking_for_run(repo, orchestrator_run_id, phase_id)` helper to `scripts/sovereign_critic_lib.py` (+ template mirror) — additive; does NOT amend `read_open_blocking`/`resolve_finding` signatures (DQ7 compose read-only). Scope key = `(orchestrator_run_id, phase_id)` pair on the finding row. Idempotent re-run via `resolve_finding` no-op. `SOVEREIGN_CRITIC_AUTORESOLVE_FAILED` is non-blocking informational (PASS verdict stands). MUST keep active ↔ template byte-identical after edit. Tests: markers 3, 4, 5. (AC-2)
- **T-003** (AC-3 — Hygiene CLI + template mirror + 6 reason codes): Create NEW `scripts/sovereign_critic_hygiene.py` (+ `template/scripts/sovereign_critic_hygiene.py` byte-identical mirror) per architecture DQ2+DQ5 LOCKED. Surface inventory: `--report`, `--resolve-nonblocking-for-run <orchestrator_run_id>`, `--dry-run`, `--confirm`, `--self-test`, `--all-phases`, `--phase-id <phase_id>`. 6 reason codes: `HYGIENE_RESOLVE_CONFIRM_REQUIRED` (exit 2), `HYGIENE_RESOLVE_NO_CANDIDATES` (exit 0 info), `HYGIENE_RESOLVE_PARTIAL` (exit 3), `HYGIENE_RESOLVE_FAILED` (exit 4), `HYGIENE_REPORT_EMPTY` (exit 0 info), `HYGIENE_RESOLVE_PHASE_SCOPE_REQUIRED` (exit 2). Operator-only posture — `/auto` orchestrator does NOT call it during a run (document operator-only-when-quiet contract in runbook `### Hygiene CLI (US-0127)` subsection — Q3 accepted: no advisory lock; `/auto` is single-threaded per repo; `resolve_finding` already uses read-all + rewrite-all). MUST keep active ↔ template byte-identical after edit. Tests: markers 6, 7, 8, 9, 10. (AC-3)
- **T-004** (AC-4 — Contract test file `tests/us0127_contract_test.py` — 13 markers): Create `tests/us0127_contract_test.py` with 13 markers per architecture DQ3 LOCKED + R-0110 R2 (marker 13 validator guard). Markers: (1) `test_us0127_open_nonblocking_passes_convergence` [AC-1/AC-4]; (2) `test_us0127_open_blocking_fails_convergence` [AC-1/AC-4]; (3) `test_us0127_autoresolve_idempotent_on_rerun` [AC-2/AC-4]; (4) `test_us0127_autoresolve_preserves_audit_trail` [AC-2/AC-4]; (5) `test_us0127_autoresolve_skips_when_blocking_open` [AC-2/AC-4]; (6) `test_us0127_hygiene_report` [AC-3]; (7) `test_us0127_hygiene_dry_run` [AC-3]; (8) `test_us0127_hygiene_confirm_required` [AC-3]; (9) `test_us0127_hygiene_self_test` [AC-3]; (10) `test_us0127_hygiene_phase_scope_required` [AC-3]; (11) `test_us0127_compose_us0104_read_open_blocking_unchanged` [compose regression guard — DQ7]; (12) `test_us0127_compose_us0110_conjunct3_contract` [compose regression guard — DQ8]; (13) `test_us0127_validate_rejects_missing_blocking` [R2 validator regression guard — confirm `sovereign_critic_validate.py --enforce` rejects missing `blocking`]. All markers static/fixture-based (no live critic spawn). Mirror to `template/tests/us0127_contract_test.py` byte-identical for parity pairing. (AC-4)
- **T-005** (AC-5 — Runbook subsections + reason_codes.md section; active + template byte-identical): Edit `docs/engineering/runbook.md` + `template/docs/engineering/runbook.md` (byte-identical) per architecture DQ4 LOCKED. New `### Blocking-only conjunct-3 semantics (US-0127)` subsection after `### Evaluate convergence` (L2792) and before `### Interpret goal_progress block` (L2811); new `### Hygiene CLI (US-0127)` subsection after `#### Parity enforcement` (L2915) and before `#### Related artifacts` (L2923). Edit `docs/engineering/reason_codes.md` + `template/docs/engineering/reason_codes.md` (byte-identical): new `## US-0127: Convergence critic conjunct hygiene (DEC-0110 §10 / DEC-0104 §11)` section after the US-0110 section (L77–L107) with the 6 hygiene reason codes + `SOVEREIGN_CRITIC_AUTORESOLVE_FAILED` (info) + clarifying note that `CONVERGENCE_CROSS_REVIEWER_OPEN` now requires `blocking=true` (description amendment only; no US-0110 reason-code renumbering). MUST keep active ↔ template byte-identical after edit. (AC-5)
- **T-006** (AC-6 — `SOVEREIGN_CRITIC_PAIRS` additive row + `--scope=sovereign-critic` parity CLI extension): Edit `scripts/check_intake_template_parity.py` (+ `template/scripts/check_intake_template_parity.py` byte-identical mirror) per architecture DQ5 LOCKED. Add NEW `SOVEREIGN_CRITIC_PAIRS` tuple table with the hygiene script pair: `scripts/sovereign_critic_hygiene.py` ↔ `template/scripts/sovereign_critic_hygiene.py`. Add NEW `--scope=sovereign-critic` entry to `SCOPES` dict mapping to `SOVEREIGN_CRITIC_PAIRS`. Add `SOVEREIGN_CRITIC_PAIRS` to the `all` union. Existing scopes unchanged (additive only). `SOVEREIGN_CONVERGENCE_PAIRS` existing rows confirmed (no new row — convergence lib mirror already present per architecture DQ5). MUST keep active ↔ template byte-identical after edit. Tests: marker 11/12 (compose regression guards) + parity CLI exit 0. (AC-6)
- **T-007** (R2 — Validator regression guard marker 13 + confirm `sovereign_critic_validate.py --enforce` rejects missing `blocking`): Author `test_us0127_validate_rejects_missing_blocking` (marker 13) inside `tests/us0127_contract_test.py` per architecture R2 + R-0110 R2 LOCKED. Marker 13 builds a fixture findings JSONL row with `status=open` but NO `blocking` key and asserts `sovereign_critic_validate.py --enforce` rejects it (non-zero exit + clear error). This is the R2 mitigation: prevent a future regression where `blocking` key is absent from a finding row (which would mask the `_critic_jsonl_has_open` narrowing). Mirror to `template/tests/us0127_contract_test.py` byte-identical. (R2 — supports AC-1/AC-4 regression guard)

Execution order: T-anch → T-001 → T-002 → T-003 → T-004 → T-005 → T-006 → T-007 (acyclic; T-001 first since it is the root-cause fix; T-002 depends on T-001's predicate; T-003/T-004 build on T-002; T-005/T-006 are docs/parity; T-007 is the validator regression guard inside T-004's file).

## AC -> Task surjective coverage

| AC | Task(s) |
|---|---|
| AC-1 (Blocking-only check) | T-001, T-004 (markers 1, 2, 11, 12, 13), T-007 (marker 13) |
| AC-2 (Auto-resolve non-blocking) | T-002, T-004 (markers 3, 4, 5) |
| AC-3 (Hygiene CLI) | T-003, T-004 (markers 6, 7, 8, 9, 10) |
| AC-4 (Contract tests) | T-004 (all 13 markers), T-007 (marker 13) |
| AC-5 (Operator docs) | T-005 (runbook subsections + reason_codes.md section) |
| AC-6 (Template parity) | T-006 (SOVEREIGN_CRITIC_PAIRS + --scope=sovereign-critic) |

**Surjectivity check**: 6/6 ACs covered (each AC has at least 1 task). No `PLAN_AC_COVERAGE_GAP`.

## Compose guards (8/8 UNCHANGED — additive code + docs + parity + contract-test only)

| Compose target | Verification | Result |
|---|---|---|
| US-0104 (sovereign_critic_lib.read_open_blocking / resolve_finding / findings JSONL schema / build_qa_cross_reviewer_block / sovereign_critic_validate.py) | compose read-only — US-0127 consumes read-only; no signature/schema/reconciliation/lens changes (DQ7) | ✅ compose |
| US-0110 (five-conjunct structure / degrade matrix / CONVERGENCE_CROSS_REVIEWER_OPEN reason code) | compose read-only — only `_critic_jsonl_has_open` helper narrows; conjunct name/order/shape unchanged (DQ8) | ✅ compose |
| US-0107 (deferral register / drain-generate / sovereign loop stop matrix) | compose read-only — untouched; `zero_deferrals` conjunct upstream of `critic_resolved` (DQ8) | ✅ compose |
| US-0045 (canonical closure — DONE/acceptance/release) | compose read-only — US-0127 does not mutate backlog Status/ACs | ✅ compose |
| US-0048 / BUG-0006 (fresh-context isolation) | compose read-only — sprint-plan subagent fresh; no prior chat carried | ✅ compose |
| US-0053 / DEC-0035 (narrow-read phase context) | compose read-only — started at phase-context.md + US-0127 anchor; no full-file reads | ✅ compose |
| US-0103 / DEC-0103 (AI Decision Ledger) | compose read-only — sprint-plan phase does not write ledger entries | ✅ compose |
| US-0056 (runtime proof) | compose read-only — sprint-plan issues its own proof; producer proof consumed before TTL | ✅ compose |

Contract tests `test_us0127_compose_us0104_read_open_blocking_unchanged` (marker 11) + `test_us0127_compose_us0110_conjunct3_contract` (marker 12) + `test_us0127_validate_rejects_missing_blocking` (marker 13) enforce at execute boundary.

## Task dependency graph

```
[T-anch] --> [T-001] (convergence lib fix + DQ6 dispatch) --> [T-002] (auto-resolve hook + helper)
                                                        |
                                                        v
                                                    [T-003] (hygiene CLI + 6 reason codes, parallel with T-004)
                                                        |
                                                        v
                                                    [T-004] (contract test file with 13 markers — authored incl. T-007 marker 13)
                                                        |
                                                        v
                                                    [T-005] (runbook subsections + reason_codes.md section)
                                                        |
                                                        v
                                                    [T-006] (SOVEREIGN_CRITIC_PAIRS + --scope=sovereign-critic parity CLI)
                                                        |
                                                        v
                                                    [T-007] (validator regression guard marker 13 — authored inside T-004 file)
                                                        |
                                                        v
                                                    Integration verification
```

**Execution order (deterministic)**: T-anch → T-001 → T-002 → T-003 → T-004 (shell + 13 markers, with T-007 marker 13 authored within) → T-005 → T-006 → integration verification.

## Execute phase role (per DEC-0051 / US-0069)

| Phase | Role | Isolation |
|---|---|---|
| /plan-verify | qa (fresh per BUG-0006) | {phase_id:plan-verify, role:qa} — standalone per orchestrator brief |
| /execute | dev (fresh per BUG-0006) | {phase_id:execute, role:dev} |
| /qa | qa (fresh) | {phase_id:qa, role:qa} |
| /verify-work | qa (fresh) | {phase_id:verify-work, role:qa} |
| /release | release (fresh) | {phase_id:release, role:release} |
| /closure | qe (fresh) | {phase_id:closure, role:qe} |
| /refresh-context | curator (fresh) | {phase_id:refresh-context, role:curator} |

## Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

| Field | Value |
|---|---|
| phase_id | sprint-plan |
| role | tech-lead |
| story_id | US-0127 |
| sprint_id | S0127 |
| orchestrator_run_id | auto-20260825-01 |
| delivery_mode | ultra_lean |
| macro_phase | plan |
| fresh_context_marker | tl-US0127-sprint-plan-20260825T185100Z-fresh |
| timestamp | 2026-08-25T18:51:00Z (UTC) |
| model_id | glm-5.2-high (CROSS_MODEL_REVIEW=1 — required) |
| evidence_ref | sprints/S0127/sprint.md, sprints/S0127/tasks.md, sprints/S0127/progress.md, sprints/S0127/uat.json, sprints/S0127/uat.md, handoffs/tl_to_dev.md (US-0127 prepend), docs/engineering/state.md (sprint-plan checkpoint append-bottom + traceability row), docs/engineering/architecture.md # US-0127 (L1852 — not mutated), handoffs/resume_brief.md |

Prior phase proof consumed: `rp-auto-20260825-01-architecture-tech-lead-20260825T184100Z-US-0127` (proof_hash=DF773DDFBA1021C5DBD44F0470469BD76A909C1373FC528BAEA65070CB9A179C, ttl 2026-08-25T19:41:00Z — consumed before RUNTIME_PROOF_STALE). Sovereign-critic architecture PASS at 2026-08-25T18:48:02Z (anti_slop_aggregate=8; 0 blocking findings; 3 architecture critic NBs noted — all non-blocking).

## Runtime proof (DEC-0038)

| Field | Value |
|---|---|
| runtime_proof_id | rp-auto-20260825-01-sprint-plan-tech-lead-20260825T185100Z-US-0127 |
| phase_id | sprint-plan |
| role | tech-lead |
| story_id | US-0127 |
| sprint_id | S0127 |
| orchestrator_run_id | auto-20260825-01 |
| delivery_mode | ultra_lean |
| macro_phase | plan |
| model_id | glm-5.2-high (CROSS_MODEL_REVIEW=1 — required) |
| proof_issued_at | 2026-08-25T18:51:00Z |
| proof_ttl_seconds | 3600 |
| proof_ttl | 2026-08-25T19:51:00Z (UTC) |
| proof_hash | DE343C909809932C3EA4B83A0D8B5F23FF8535954F05512C5D33A3EB3DE65723 |
| canonical_payload | `{"delivery_mode":"ultra_lean","macro_phase":"plan","model_id":"glm-5.2-high","orchestrator_run_id":"auto-20260825-01","phase_id":"sprint-plan","proof_issued_at":"2026-08-25T18:51:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260825-01-sprint-plan-tech-lead-20260825T185100Z-US-0127","sprint_id":"S0127","story_id":"US-0127"}` |

## Decision gate

| Field | Value |
|---|---|
| decision_gate | false |
| stop_conditions_met | yes |
| missing_acceptance_criteria | none (6/6 ACs covered by 13 contract-test markers + compose guards 8/8) |
| compose_guards | 8/8 UNCHANGED (additive code + docs + parity + contract-test only) |
| dc_check | clean (T-anch verifies # US-0127 H1 anchor already added in /architecture phase at L1852) |
| task_count | 8 (within SPRINT_MAX_TASKS=12; SPRINT_AUTO_SPLIT=1 but no split needed) |
| risks_finalized | 6/6 ACCEPTED (R1..R6 from R-0110 / architecture) |
| approach | A1 locked |
| Q | DQ1..DQ8 LOCKED for US-0127; Q1/Q2/Q3 accepted per research recommendations: 13 markers / yes `--all-phases` + `HYGIENE_RESOLVE_PHASE_SCOPE_REQUIRED` / no advisory lock (document operator-only-when-quiet contract) |
| plan-verify readiness | standalone /plan-verify next (role=qa per orchestrator brief); plan-verify.json NOT written in this spawn |
| sovereign_memory_note | `assemble_sovereign_memory_digest(...)` NOT called; no mistakes.jsonl write |

## Definition of done (sprint-plan)

- [x] 8 tasks enumerated (T-anch + T-001..T-007) — within SPRINT_MAX_TASKS=12
- [x] 6/6 ACs covered by 13 contract-test markers + compose guards 8/8 (surjective)
- [x] Task dependency graph documented
- [x] Execute phase role matrix documented (including standalone /plan-verify per orchestrator brief)
- [x] Compose guards 8/8 UNCHANGED (additive code + docs + parity + contract-test only)
- [x] Critic carry-ins (3 non-blocking from architecture sovereign-critic) explicitly noted; 0 new carry-ins routed to /execute
- [x] Isolation evidence + runtime proof emitted (model_id=glm-5.2-high present)
- [x] Sprint-plan checkpoint appended to `docs/engineering/state.md` (append-bottom; never truncate)
- [x] Sprint-plan handoff prepended to `handoffs/tl_to_dev.md`
- [x] Sprint-plan PASS prepended to `handoffs/resume_brief.md` (→ /plan-verify, role=qa)
- [x] UAT placeholders written (`uat.json` empty steps, `uat.md` ACs no results)
- [x] Traceability row added to `docs/engineering/state.md` (Story=US-0127 | Sprint=S0127 | Tasks=T-anch+T-001..T-007 | Status=PLANNED | Evidence empty)
- [x] Backlog status OPEN (US-0045 — not mutated); AC checkboxes untouched

## Next scheduled phase

| Field | Value |
|---|---|
| next_scheduled_phase | `/plan-verify` (role=qa per orchestrator brief; fresh qa subagent per BUG-0006) |
| next_scheduled_role | qa |
| next_sprint_macro | plan (terminal — /plan-verify is the verification gate before build+verify macro) |
| stop_condition | STOP after sprint-plan completes; hand off via artifacts only to /plan-verify in fresh qa subagent per BUG-0006. Do not spawn /plan-verify from this subagent. |
| artifacts_written | sprints/S0127/sprint.md, sprints/S0127/tasks.md, sprints/S0127/progress.md, sprints/S0127/uat.json, sprints/S0127/uat.md, docs/engineering/state.md (sprint-plan checkpoint append-bottom + traceability row), handoffs/tl_to_dev.md (US-0127 prepend), handoffs/resume_brief.md (sprint-plan PASS prepend → /plan-verify) |
