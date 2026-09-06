# Sprint S0131 - Sprint Plan (BUG-0015)

## Metadata

| Field | Value |
|---|---|
| bug_id | BUG-0015 |
| story_id | (none — bug segment) |
| story_title | OpenCode `/auto` never triggers orchestrator plugin dispatch and stops at command STOP |
| sprint_id | S0131 |
| delivery_mode | ultra_lean |
| macro_phase | plan (sprint-plan terminal; /plan-verify merged into build+verify under QA per ultra_lean) |
| current_phase | sprint-plan |
| approach | A* locked (from R-0114 DQ1–DQ7; CF1–CF7 CLOSED) |
| companion_DEC | none (cite R-0114; compose DEC-0124 / DEC-0125 without amend) |
| research_anchor | R-0114 (DQ1–DQ7 LOCKED) |
| architecture_anchor | docs/engineering/architecture.md # BUG-0015 |
| orchestrator_run_id | auto-20260906-bug0015 |
| fresh_context_marker | tl-BUG0015-sprint-plan-20260906T143000Z-fresh |
| timestamp | 2026-09-06T14:30:00Z (UTC) |
| model_id | composer-2.5 (CROSS_MODEL_REVIEW=1 — required on isolation) |
| verdict | PASS |
| decision_gate | false |
| SPRINT_MAX_TASKS | 12 |
| SPRINT_AUTO_SPLIT | 1 |
| task_count | 7 (T-anch + T-001..T-006; within 12; no split) |
| COMPONENT_SCOPE_MODE | 0 |
| USER_GUIDE_MODE | 0 |
| plan-verify | ultra_lean — merged into build+verify under QA; plan-verify.json NOT written here |
| backlog_status | OPEN (US-0045 — not mutated; acceptance BUG-0015 unchecked) |
| critic_carry_ins | 0 new blocking; 3 architecture critic NBs `b0015ar-*` status=resolved non-blocking — routed as awareness into /execute (below) |

## Scope summary

Close the **interactive `/auto` → plugin spawn linkage gap** on the OpenCode host (compose US-0124/US-0125). US-0124 shipped `spawnPhase` + write-guard + stop-matrix subprocess; US-0125 shipped dispatch-only `.opencode/commands/auto.md`. Runtime defect: `setup()` returns the API and registers only `ctx.tool.hook("execute.before")` — **no host-invoked entry** starts the spawn loop when the operator runs `/auto`.

**Approach A\***: In `setup(ctx)`, register v2 **`ctx.command.transform`** → **`editor.add({ name: "auto", execute })`** as primary host-invoked entry. `execute` calls shared **`runAutoLifecycle`** (in-flight mutex TTL 7200s / clear-on-exit, first-phase via Python kit selectors, `spawnPhase` + `dispatchStopMatrix` loop, IsolationEvidence durable write via Python→state.md). Defense: optional `command.executed` / subscribe — secondary only, mutex-gated. Missing attach → **`OPENCODE_PLUGIN_DISPATCH_ATTACH_UNSUPPORTED`**. Concurrent re-entry → **`OPENCODE_AUTO_ALREADY_RUNNING`**. Thin `auto.md` stays STOP-only. Additive 7 `test_bug0015_*` markers; do not amend `test_us0124_*` / `test_us0125_*`. No companion DEC.

Out of scope: BUG-0016 Layer-1 permissions / DEC-0122 amend; US-0131/US-0132; amending DEC-0124/DEC-0125 bodies; Cursor Task port; TS stop-matrix rewrite; live OpenCode CI probe; marking BUG-0015 DONE; ticking acceptance BUG-0015.

## Execute awareness (architecture critic NBs — 0 blocking)

Sovereign-critic of architecture PASS (`critic-BUG0015-architecture-20260906T142500Z-fresh`; anti_slop=8; 0 blocking). Route these resolved NBs as execute awareness — do not re-open them as work:

| Finding | Issue key | Execute awareness |
|---|---|---|
| `b0015ar-challenger-001` | `ik_bug0015_arch_edge_and_proof` | **T-002 / T-005**: Prove mutex gate on dual-fire / secondary `command.executed` after STOP (marker 5). Document mutex TTL clock source + clear-on-fail-closed paths (R1/R3 residuals). |
| `b0015ar-architect-002` | `ik_bug0015_arch_layer_coupling` | **T-003**: IsolationEvidence + first-phase via Python bridge only (no OpenCode-only resolver). **T-006**: runbook h3 stub only (US-0126 owns full table). Keep active+template parity for `orchestrator.ts` / `auto.md` / `bug0015_contract_test`. |
| `b0015ar-subtractor-003` | `ik_bug0015_arch_scope_minimal` | **T-anch** ceremony overlap acceptable. Do not expand to BUG-0016 / live OpenCode probe / DEC amend. Do not mark BUG-0015 DONE. 7 markers required (not YAGNI). |

## Acceptance criteria (8) - BUG-0015 (status OPEN, acceptance unchecked per US-0045)

- **AC-1**: `/auto` starts plugin spawn loop via host attach (`command.transform` / `editor.add({ name: "auto", execute })` → `runAutoLifecycle` → `spawnPhase`).
- **AC-2**: Missing attach fail-closed `OPENCODE_PLUGIN_DISPATCH_ATTACH_UNSUPPORTED`.
- **AC-3**: Missing `session.create` → `OPENCODE_PLUGIN_SPAWN_UNSUPPORTED` (compose DEC-0124).
- **AC-4**: IsolationEvidence minimum fields + `OPENCODE_SUBTASK_IGNORED` on null/throw/identical-id; durable write to state.md SOT via Python bridge.
- **AC-5**: Concurrent/re-entrant `/auto` → `OPENCODE_AUTO_ALREADY_RUNNING` (mutex TTL 7200s / clear-on-exit).
- **AC-6**: `auto.md` remains dispatch-only (≤20 lines, no spawn literals) — active + template.
- **AC-7**: Compose US-0124 spawn API unchanged (no DEC-0124/0125 body amend; exported `spawnPhase` / reason codes present).
- **AC-8**: Seven additive `test_bug0015_*` green (mock-ctx; no live OpenCode probe).

## Task summaries (7 - T-anch + T-001..T-006)

- **T-anch** (NO-OP / verification): Verify `# BUG-0015` H1 + approach A* + R-0114 DQ1–DQ7 + CF1–CF7 closed + no DEC-0124/0125 body amend. Record to `sprints/S0131/t-anch-verification.md`. NO mutation to `architecture.md` in /execute.
- **T-001** (AC-1, AC-2): Register `command.transform` / `editor.add({ name: "auto", execute })`; missing attach → `OPENCODE_PLUGIN_DISPATCH_ATTACH_UNSUPPORTED`; secondary event optional + mutex.
- **T-002** (AC-1, AC-3, AC-5): Implement `runAutoLifecycle` + in-flight mutex (TTL 7200s / clear-on-exit) + `spawnPhase` / `dispatchStopMatrix` loop; wire headless compose path.
- **T-003** (AC-4): IsolationEvidence durable write via Python bridge to state.md; first-phase selection via Python (argv → resume_brief → scratchpad → US-0087).
- **T-004** (AC-6): Keep `auto.md` STOP-only (active + template); no spawn literals.
- **T-005** (AC-2..AC-8): Add 7 `test_bug0015_*` markers + mock-ctx harness extension; do not amend us0124/us0125 tests.
- **T-006** (AC-2, AC-5): Runbook h3 stub for two new reason codes; cross-link US-0126; optional parity scope `bug-0015`.

Execution order: T-anch → T-001 → T-002 → T-003 → T-004 → T-005 → T-006 (acyclic; attach first, then lifecycle/mutex, then bridges, then static assert, then tests, then runbook).

## AC -> Task surjective coverage

| AC | Task(s) |
|---|---|
| AC-1 (`/auto` starts spawn via attach) | T-001, T-002, T-005 (markers 1, 2) |
| AC-2 (missing attach fail-closed) | T-001, T-005 (marker 3), T-006 |
| AC-3 (missing session.create) | T-002, T-005 (marker 4) |
| AC-4 (IsolationEvidence + state.md) | T-003, T-005 |
| AC-5 (concurrent `/auto` mutex) | T-002, T-005 (marker 5), T-006 |
| AC-6 (`auto.md` dispatch-only) | T-004, T-005 (marker 6) |
| AC-7 (compose US-0124 spawn API) | T-anch, T-005 (marker 7) |
| AC-8 (seven additive markers) | T-005 (all 7 markers) |

**Surjectivity check**: 8/8 ACs covered (each AC has at least 1 task). No `PLAN_AC_COVERAGE_GAP`.

## Risks (R1–R5 — accepted from architecture)

| Risk | Severity | Mitigation in this sprint |
|---|---|---|
| R1 markdown vs transform dual-fire | MEDIUM → LOW | CF1 + mutex; T-002/T-005 marker 5; T-004/marker 6 |
| R2 `command.executed` after STOP race | MEDIUM → LOW | CF6 primary = transform execute; secondary mutex-gated |
| R3 mutex false-positive after crash | LOW | CF5 clear-on-exit + 7200s TTL; challenger NB awareness |
| R4 reason-code stub drift vs US-0126 | LOW | T-006 stub + cross-link only |
| R5 BUG-0016 still blocks validators post-fix | LOW | expected; out of scope |

## Compose guards (UNCHANGED — additive attach + lifecycle + bridge + tests + runbook stub only)

| Compose target | Verification | Result |
|---|---|---|
| DEC-0124 / US-0124 | spawn API / write-guard / stop-matrix subprocess UNCHANGED; attach additive; marker 7 | compose |
| DEC-0125 / US-0125 | `auto.md` STOP-only ≤20 lines; no spawn literals; marker 6 | compose |
| DEC-0122 | Layer-1 matrix NOT amended (BUG-0016) | compose |
| US-0131 / US-0132 | config/model parity NOT reopened | compose |
| US-0126 | full reason-code table ownership UNCHANGED; T-006 stub only | compose |
| US-0045 / US-0048 / US-0056 | Status stays OPEN; fresh isolation; this phase mints its own proof | compose |

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
| bug_id | BUG-0015 |
| story_id | BUG-0015 |
| sprint_id | S0131 |
| orchestrator_run_id | auto-20260906-bug0015 |
| delivery_mode | ultra_lean |
| macro_phase | plan |
| fresh_context_marker | tl-BUG0015-sprint-plan-20260906T143000Z-fresh |
| timestamp | 2026-09-06T14:30:00Z (UTC) |
| model_id | composer-2.5 (CROSS_MODEL_REVIEW=1 — required) |
| evidence_ref | sprints/S0131/sprint.md, sprints/S0131/tasks.md, sprints/S0131/progress.md, sprints/S0131/uat.json, sprints/S0131/uat.md, handoffs/tl_to_dev.md (BUG-0015 prepend), docs/engineering/state.md (sprint-plan checkpoint prepend + traceability row), docs/engineering/architecture.md # BUG-0015 (not mutated), handoffs/resume_brief.md |

Prior phase proof consumed: `rp-auto-20260906-bug0015-architecture-techlead-20260906T142000Z-BUG-0015` (proof_hash=DBEB0F5D44E6801D5E1DEEA686A95CB32090B75A1FA1DCCF5621C1E1FD017440, ttl 2026-09-06T15:20:00Z — independent SHA-256 MATCH via critic; consumed at 2026-09-06T14:30:00Z before RUNTIME_PROOF_STALE). Sovereign-critic architecture PASS at 2026-09-06T14:25:00Z (anti_slop_aggregate=8; 0 blocking findings; 3 NBs `b0015ar-*` status=resolved).

## Runtime proof (DEC-0038)

| Field | Value |
|---|---|
| runtime_proof_id | rp-auto-20260906-bug0015-sprint-plan-techlead-20260906T143000Z-BUG-0015 |
| phase_id | sprint-plan |
| role | tech-lead |
| story_id | BUG-0015 |
| sprint_id | S0131 |
| orchestrator_run_id | auto-20260906-bug0015 |
| delivery_mode | ultra_lean |
| macro_phase | plan |
| model_id | composer-2.5 (CROSS_MODEL_REVIEW=1 — required) |
| proof_issued_at | 2026-09-06T14:30:00Z |
| proof_ttl_seconds | 3600 |
| proof_ttl | 2026-09-06T15:30:00Z (UTC) |
| proof_hash | 628D489A395FD783DE7E84A5D8AAC82823AA35843A4FE498638DEB0A5175E43E |
| canonical_payload | `{"delivery_mode":"ultra_lean","macro_phase":"plan","model_id":"composer-2.5","orchestrator_run_id":"auto-20260906-bug0015","phase_id":"sprint-plan","proof_issued_at":"2026-09-06T14:30:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260906-bug0015-sprint-plan-techlead-20260906T143000Z-BUG-0015","sprint_id":"S0131","story_id":"BUG-0015"}` |

## Decision gate

| Field | Value |
|---|---|
| decision_gate | false |
| stop_conditions_met | yes |
| missing_acceptance_criteria | none (8/8 ACs covered; 7 contract-test markers; compose guards UNCHANGED) |
| compose_guards | DEC-0124/0125/0122 + US-0131/0132/0126/0045 UNCHANGED |
| dc_check | clean (`# BUG-0015` H1 already added in /architecture) |
| task_count | 7 (within SPRINT_MAX_TASKS=12; SPRINT_AUTO_SPLIT=1 but no split needed) |
| risks_finalized | 5/5 ACCEPTED (R1..R5) |
| approach | A* locked |
| companion_DEC | none |
| plan-verify readiness | ultra_lean — /plan-verify merged into build+verify under QA; plan-verify.json NOT written in this spawn |
| sovereign_memory_note | `assemble_sovereign_memory_digest(...)` NOT called; no mistakes.jsonl write |

## Definition of done (sprint-plan)

- [x] 7 tasks enumerated (T-anch + T-001..T-006) — within SPRINT_MAX_TASKS=12
- [x] 8/8 ACs covered by 7 contract-test markers + compose guards (surjective)
- [x] Task dependency graph documented
- [x] Execute phase role matrix documented (ultra_lean — /plan-verify merged into build+verify under QA)
- [x] Compose guards UNCHANGED
- [x] Critic carry-ins (3 non-blocking from architecture sovereign-critic) routed as execute awareness
- [x] Isolation evidence + runtime proof emitted (model_id=composer-2.5 present)
- [x] Sprint-plan checkpoint prepended to `docs/engineering/state.md`
- [x] Sprint-plan handoff prepended to `handoffs/tl_to_dev.md`
- [x] Sprint-plan PASS prepended to `handoffs/resume_brief.md` (-> /execute)
- [x] UAT placeholders written (`uat.json` empty/pending steps, `uat.md` ACs no results)
- [x] Traceability row added to `docs/engineering/state.md` (Story=BUG-0015 | Sprint=S0131 | Tasks=T-anch+T-001..T-006 | Status=PLANNED | Evidence empty)
- [x] Backlog status OPEN (US-0045 — not mutated); AC checkboxes untouched; sprint_plan_notes appended

## Next scheduled phase

| Field | Value |
|---|---|
| next_scheduled_phase | `/execute` (role=dev per US-0069 / DEC-0051; fresh dev subagent per BUG-0006; first canonical phase of `build+verify` macro per ultra_lean; /plan-verify merged into qa per ultra_lean — qa creates plan-verify.json within build+verify). Orchestrator runs sovereign-critic of sprint-plan first (CROSS_MODEL_REVIEW=1). Do not mandate outer driver. |
| next_scheduled_role | dev |
| next_sprint_macro | build+verify (ultra_lean — plan-verify merged into qa) |
| stop_condition | STOP after sprint-plan completes; hand off via artifacts only. Orchestrator owns critic of sprint-plan then `/execute` in fresh dev subagent per BUG-0006. Do not spawn /execute or /plan-verify from this subagent. |
| artifacts_written | sprints/S0131/ (sprint.md, tasks.md, progress.md, uat.json, uat.md), docs/engineering/state.md (sprint-plan checkpoint + traceability), handoffs/tl_to_dev.md (BUG-0015 prepend), handoffs/resume_brief.md (sprint-plan PASS prepend -> /execute), docs/product/backlog.md (sprint_plan_notes append; Status OPEN) |
