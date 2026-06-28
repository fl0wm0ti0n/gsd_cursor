# PO to TL archive pack (2026-06-28)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=650, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 4
- Retained units in hot file: 10
- First archived heading: `## Orchestrated sprint-plan handoff — US-0110 / auto-20260628-04`
- Last archived heading: `## Orchestrated discovery handoff — US-0110 / auto-20260628-04`
- Verification tuple (mandatory):
  - archived_body_lines=318
  - retained_body_lines=635

---

## Orchestrated sprint-plan handoff — US-0110 / auto-20260628-04

### Target

- `story_id=US-0110`
- `sprint_id=S0110`
- `orchestrator_run_id=auto-20260628-04`
- phase completed: **`sprint-plan`** (**`tech-lead`**)
- `fresh_context_marker=tl-S0110-US0110-sprint-plan-20260628T183000Z-fresh`
- `next_scheduled_phase=plan-verify`
- `decomposition=single_story` (per **US-0051**)
- `priority=P0`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=8`
- `intake_evidence_ref=handoffs/intake_evidence/intake-sovereign-20260627-01.json` (batch — skip re-intake)

### Summary

- **`/sprint-plan`** **PASS** — sprint **`S0110`** materialized from **11 architecture seeds** (T-001..T-011); **AC-1..AC-8 surjective coverage** verified; **`plan-verify.json`** seeded **PENDING**; within **`SPRINT_MAX_TASKS=12`**; **`SPRINT_AUTO_SPLIT`** not triggered. **Compose do NOT amend** US-0088/US-0092/US-0095/US-0044/US-0103.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Sprint-plan locks (plan-verify inputs)

| Lock | Decision |
|------|----------|
| **Binding decision** | **`DEC-0110`** — composes US-0088 / US-0092 / US-0095 / US-0044 / US-0103 (read-only) |
| **Sprint artifacts** | `sprints/S0110/sprint.md`, `tasks.md`, `progress.md`, `plan-verify.json`, `uat.json`, `uat.md` |
| **Task seeds** | T-001..T-011 (strict 1:1 from architecture) |
| **AC bijection** | AC-1→T-001,T-002; AC-2→T-003,T-004,T-006; AC-3→T-005; AC-4→T-007; AC-5→T-008; AC-6→T-009,T-010; AC-7→T-011; AC-8→T-002,T-006,T-010,T-011 |
| **Tranche order** | A keys+reason codes → B lib+derive → C validator → D progress+partial-delivery → E tests+parity+runbook |
| **Contract tests** | 8× `test_us0110_*` in `tests/us0110_contract_test.py` |
| **Parity scope** | `--scope=sovereign-convergence` (`SOVEREIGN_CONVERGENCE_PAIRS`) |
| **Post-edit gates** | `pytest -k us0110`; lib `--self-test`; validator `--self-test`; parity PASS |

### Top risks (carry to /plan-verify)

- **R1**: Predicate cost on large backlogs — line-scoped scan + memoization (T-004).
- **R2**: Upstream artifacts absent — degrade matrix skip semantics (T-004).
- **R3**: Smoke canonical chain — `tests/report.md` + sprint `uat.json` (T-004).
- **R4**: Native-chain interaction — compose regression test (T-011).
- **R5**: Timeout — iteration count; default `0` disabled (T-008).

### Evidence refs

- `sprints/S0110/sprint.md`
- `sprints/S0110/tasks.md`
- `sprints/S0110/plan-verify.json` (PENDING)
- `handoffs/tl_to_dev.md`
- `handoffs/qa_plan_verify.md`
- `docs/product/backlog.md` (`## US-0110` — `sprint_plan_notes`)
- `decisions/DEC-0110.md`
- `docs/engineering/architecture.md` `# US-0110`

### Isolation evidence (TL sprint-plan phase)

| Field | Value |
|-------|-------|
| `phase_id` | `sprint-plan` |
| `role` | `tech-lead` |
| `fresh_context_marker` | `tl-S0110-US0110-sprint-plan-20260628T183000Z-fresh` |
| `timestamp` | `2026-06-28T18:30:00Z` |
| `evidence_ref` | `handoffs/po_to_tl.md` (this handoff) + `sprints/S0110/tasks.md` |

### Next

- **`/plan-verify`** (fresh **qa** context) for **`S0110`** / **`US-0110`** — AC bijection verification; `plan-verify.json` PENDING → PASS.

### Decision gate

- **None** — sprint-plan satisfied; plan-verify readiness explicit.

---

## Orchestrated architecture handoff — US-0110 / auto-20260628-04

### Target

- `story_id=US-0110`
- `orchestrator_run_id=auto-20260628-04`
- phase completed: **`architecture`** (**`tech-lead`**)
- `fresh_context_marker=tl-US0110-architecture-20260628T180000Z-fresh`
- `next_scheduled_phase=sprint-plan`
- `decomposition=single_story` (per **US-0051**)
- `priority=P0`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=8`
- `intake_evidence_ref=handoffs/intake_evidence/intake-sovereign-20260627-01.json` (batch — skip re-intake)

### Summary

- **`/architecture`** **PASS** — **`# US-0110`** appended to `docs/engineering/architecture.md`; **`DEC-0110`** ratified; **11 task seeds** (T-001..T-011) with surjective AC-1..AC-8 coverage; within **`SPRINT_MAX_TASKS=12`**; **`SPRINT_AUTO_SPLIT`** not triggered. **Compose do NOT amend** US-0088/US-0092/US-0095/US-0044/US-0103.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Architecture locks (sprint-plan inputs)

| Lock | Decision |
|------|----------|
| **Binding decision** | **`DEC-0110`** — composes US-0088 / US-0092 / US-0095 / US-0044 / US-0103 (read-only) |
| **Scratchpad keys** | `SOVEREIGN_GOAL_MODE`, `SOVEREIGN_GOAL`, `SOVEREIGN_GOAL_TOP_N`, `SOVEREIGN_GOAL_MAX_CHARS`, `SOVEREIGN_GOAL_TIMEOUT_MAX` |
| **Schemas** | `ConvergenceResult` v1 + `goal_progress` v1 |
| **Predicate** | Five conjuncts + degrade matrix (skip deferrals/critic when absent; smoke fail-closed; ledger skip when disabled) |
| **Library** | `sovereign_convergence_lib.py` — evaluate/resolve/progress/partial-delivery/timeout |
| **Validator** | `sovereign_convergence_validate.py` — `--convergence-json`, `--goal-progress-json`, `--enforce` |
| **Task seeds** | T-001..T-011 (see architecture § Atomic task seeds) |
| **Contract tests** | 8× `test_us0110_*` in `tests/us0110_contract_test.py` |
| **Parity scope** | `--scope=sovereign-convergence` (`SOVEREIGN_CONVERGENCE_PAIRS`) |
| **Downstream** | **US-0107** consumes predicate for drain-generate + notification |

### Task seed list (T-001..T-011)

| # | Summary | ACs |
|---|---------|-----|
| T-001 | Scratchpad keys `SOVEREIGN_GOAL_*` (active + template) | AC-1 |
| T-002 | Scratchpad comment block + reason codes § US-0110 | AC-1, AC-8 |
| T-003 | `sovereign_convergence_lib.py` schemas + self_test | AC-2 |
| T-004 | `evaluate_convergence` five-conjunct + degrade matrix + memoization | AC-2 |
| T-005 | `resolve_goal` vision auto-derive | AC-3 |
| T-006 | `sovereign_convergence_validate.py` + template mirror | AC-2, AC-8 |
| T-007 | `goal_progress` block + curator `/refresh-context` hook | AC-4 |
| T-008 | Partial delivery report + `check_timeout` | AC-5 |
| T-009 | Eight `test_us0110_*` contract markers | AC-6 |
| T-010 | `SOVEREIGN_CONVERGENCE_PAIRS` parity scope | AC-6, AC-8 |
| T-011 | Runbook + `phase_driven` zero-overhead + compose regression | AC-7, AC-8 |

### Top risks (carry to /sprint-plan)

- **R1**: Predicate cost on large backlogs — line-scoped scan + memoization.
- **R2**: Upstream artifacts absent — degrade matrix skip semantics locked.
- **R3**: Smoke canonical chain — `tests/report.md` + sprint `uat.json` (US-0093).
- **R4**: Native-chain interaction — convergence orthogonal; regression test in T-011.
- **R5**: Timeout — iteration count; default `0` disabled.

### Evidence refs

- `docs/engineering/architecture.md` (`# US-0110`)
- `decisions/DEC-0110.md`
- `docs/product/backlog.md` (`## US-0110` — `architecture_notes`)
- `docs/engineering/research.md` (`R-0091` closed)
- `scripts/sovereign_convergence_lib.py` (research stub)

### Isolation evidence (TL architecture phase)

| Field | Value |
|-------|-------|
| `phase_id` | `architecture` |
| `role` | `tech-lead` |
| `fresh_context_marker` | `tl-US0110-architecture-20260628T180000Z-fresh` |
| `timestamp` | `2026-06-28T18:00:00Z` |
| `evidence_ref` | `handoffs/po_to_tl.md` (this handoff) + `docs/engineering/architecture.md` `# US-0110` |

### Next

- **`/sprint-plan`** (fresh **tech-lead** context) for **`US-0110`** — materialize sprint from 11 seeds; AC bijection check; `sprints/Sxxxx/sprint.md` + `tasks.md`.

### Decision gate

- **None** — architecture satisfied; sprint-plan readiness explicit.

---

## Orchestrated research handoff — US-0110 / auto-20260628-04

### Target

- `story_id=US-0110`
- `orchestrator_run_id=auto-20260628-04`
- phase completed: **`research`** (**`tech-lead`**)
- `fresh_context_marker=tl-US0110-research-20260628T173000Z-fresh`
- `next_scheduled_phase=architecture`
- `decomposition=single_story` (per **US-0051**)
- `priority=P0`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=8`
- `intake_evidence_ref=handoffs/intake_evidence/intake-sovereign-20260627-01.json` (batch — skip re-intake)

### Summary

- **`/research`** **PASS** — **`R-0091`** Q1–Q7 closed; companion **`DEC-0110`** locked. **`scripts/sovereign_convergence_lib.py`** API + schemas + degrade matrix + vision auto-derive + eight **`test_us0110_*`** contract markers + **`SOVEREIGN_CONVERGENCE_PAIRS`** parity manifest. Research stub self-test OK (`[SOVEREIGN_CONVERGENCE_SELF_TEST_OK]`). **Compose do NOT amend** US-0088/US-0092/US-0095/US-0044/US-0103.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Research locks (architecture inputs)

| Lock | Decision |
|------|----------|
| **Binding decision** | **`DEC-0110`** — composes **US-0088** / **US-0092** / **US-0095** / **US-0044** / **US-0103** (read-only) |
| **Scratchpad keys** | `SOVEREIGN_GOAL_MODE`, `SOVEREIGN_GOAL`, `SOVEREIGN_GOAL_TOP_N`, `SOVEREIGN_GOAL_MAX_CHARS`, `SOVEREIGN_GOAL_TIMEOUT_MAX` |
| **Schemas** | `ConvergenceResult` v1 + `goal_progress` v1 (DEC-0110 §2–§3) |
| **Predicate** | Five conjuncts + degrade matrix §4 (skip deferrals/critic when absent; smoke fail-closed; ledger skip when disabled) |
| **Goal derive** | Vision top-N algorithm §5; explicit wins; `SOVEREIGN_GOAL_DERIVE_FAILED` fail-closed |
| **Library** | `sovereign_convergence_lib.py` — evaluate/resolve/progress/partial-delivery/timeout/check |
| **Validator** | `sovereign_convergence_validate.py` — `--convergence-json`, `--goal-progress-json`, `--enforce` |
| **Contract tests** | 8× `test_us0110_*` in `tests/us0110_contract_test.py` |
| **Parity scope** | `--scope=sovereign-convergence` (`SOVEREIGN_CONVERGENCE_PAIRS`) |
| **Performance** | ≤50ms p95; memoization key on input mtimes |
| **Reason codes** | 10 codes (DEC-0110 §10) |
| **Downstream** | **US-0107** consumes predicate for drain-generate + notification |

### Top risks (carry to /architecture)

- **R1**: Predicate cost on large backlogs — line-scoped scan + memoization.
- **R2**: Upstream artifacts absent — degrade matrix skip semantics locked.
- **R3**: Smoke canonical chain — `tests/report.md` + sprint `uat.json` (US-0093); US-0109 orthogonal.
- **R4**: Native-chain interaction — convergence orthogonal; regression test required.
- **R5**: Timeout — iteration count; default `0` disabled.

### Evidence refs

- `decisions/DEC-0110.md`
- `docs/engineering/research.md` (**`R-0091`** closed)
- `scripts/sovereign_convergence_lib.py` (research stub)
- `docs/product/backlog.md` (`## US-0110` — `research_notes`)
- `handoffs/intake_evidence/intake-sovereign-20260627-01.json`
- `decisions/DEC-0103.md` (ledger compose)

### Isolation evidence (TL research phase)

| Field | Value |
|-------|-------|
| `phase_id` | `research` |
| `role` | `tech-lead` |
| `fresh_context_marker` | `tl-US0110-research-20260628T173000Z-fresh` |
| `timestamp` | `2026-06-28T17:30:00Z` |
| `evidence_ref` | `handoffs/po_to_tl.md` (this handoff) + `decisions/DEC-0110.md` |

### Next

- **`/architecture`** (fresh **tech-lead** context) for **`US-0110`** — append `# US-0110`, task seeds, runbook hooks.

### Decision gate

- **None** — research satisfied; architecture readiness explicit.

---

## Orchestrated discovery handoff — US-0110 / auto-20260628-04

### Target

- `story_id=US-0110`
- `orchestrator_run_id=auto-20260628-04`
- phase completed: **`discovery`** (**`po`**)
- `fresh_context_marker=po-US0110-discovery-20260628T170000Z-fresh`
- `next_scheduled_phase=research`
- `decomposition=single_story` (per **US-0051**)
- `priority=P0`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=8`
- `intake_evidence_ref=handoffs/intake_evidence/intake-sovereign-20260627-01.json` (batch — skip re-intake)

### Summary

- **`/discovery`** **PASS** — goal-based convergence predicate locked as sovereign-loop terminal condition. **`scripts/sovereign_convergence_lib.py`** exposes **`evaluate_convergence(repo, scratchpad) -> {converged, unmet_conditions[], blocked_by[]}`**. Five-conjunct predicate: all OPEN stories DONE + zero deferrals + cross-reviewer findings resolved + smoke probe green + ledger no unapproved extensions. Scratchpad: **`SOVEREIGN_GOAL_MODE=phase_driven|goal_convergence`** (default **`phase_driven`**), **`SOVEREIGN_GOAL`**, **`SOVEREIGN_GOAL_TOP_N`**, **`SOVEREIGN_GOAL_TIMEOUT_MAX`**. Mid-loop **`goal_progress`** block in curator **`/refresh-context`** → **`handoffs/resume_brief.md`**. Timeout → **`SOVEREIGN_GOAL_TIMEOUT`** + **`handoffs/sovereign_partial_delivery.md`**. **Compose do NOT amend** US-0088/US-0092/US-0095/US-0044/US-0103.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Discovery locks (research inputs)

| Lock | Decision |
|------|----------|
| **L1 Scratchpad keys** | `SOVEREIGN_GOAL_MODE` ∈ {`phase_driven`, `goal_convergence`}, default `phase_driven`; `SOVEREIGN_GOAL` optional; `SOVEREIGN_GOAL_TOP_N` default `3`; `SOVEREIGN_GOAL_TIMEOUT_MAX` default `0` (disabled) |
| **L2 Evaluator library** | `scripts/sovereign_convergence_lib.py` — `evaluate_convergence`, `resolve_goal`, `build_goal_progress_block`, `write_partial_delivery_report`, `is_goal_convergence_enabled`, `self_test` |
| **L3 Convergence predicate** | Five conjuncts: backlog OPEN=0, deferrals=0, critic findings resolved, smoke green, ledger extensions approved |
| **L4 Goal authoring** | Explicit `SOVEREIGN_GOAL` wins; else vision top-N auto-derive; `SOVEREIGN_GOAL_DERIVE_FAILED` fail-closed |
| **L5 Mid-loop progress** | Curator `goal_progress` JSON block in `resume_brief.md` when `goal_convergence` active |
| **L6 Partial delivery** | `SOVEREIGN_GOAL_TIMEOUT` + `handoffs/sovereign_partial_delivery.md` (Goal, Unmet, Blocked, Completed/Open stories, Deferrals, Remediation) |
| **L7 Backward compat** | `phase_driven` = zero overhead; US-0088/0092/0095/0044 stop matrix unchanged |
| **L8 Contract tests** | 8× `test_us0110_*` markers; parity `--scope=sovereign-convergence` (`SOVEREIGN_CONVERGENCE_PAIRS`) |
| **L9 Reason codes** | 10 codes: `CONVERGENCE_*` (5) + `SOVEREIGN_GOAL_*` (4) + `CONVERGENCE_EVAL_FAILED` |
| **L10 Compose (read-only)** | Backlog, `sovereign_deferrals.jsonl`, QA/critic findings, `tests/report.md`+`uat.json`, sovereign ledger |
| **L11 Performance** | Line-scoped backlog scan; ledger `last_n=100`; drain-loop cache strategy (research Q6) |
| **L12 Downstream** | **US-0107** consumes predicate for drain-generate + notification |

### Research asks (extend R-0091)

1. **Q1**: `ConvergenceResult` + `goal_progress` JSON schemas + validator CLI.
2. **Q2**: Full helper library API + CLI surface.
3. **Q3**: Degrade matrix when US-0104/US-0107 artifacts absent.
4. **Q4**: Vision auto-derive algorithm.
5. **Q5**: Contract-test inventory + parity file list.
6. **Q6**: Performance budget + memoization for drain loops.
7. **Q7**: Companion DEC necessity.

### Top risks (carry to /research)

- **R1**: Predicate evaluation cost on large backlogs.
- **R2**: Upstream artifacts (US-0104 critic, US-0107 deferrals) not yet deployed — degrade semantics.
- **R3**: Smoke probe canonical source (US-0093 UAT vs US-0109 deploy).
- **R4**: `goal_convergence` must not bypass US-0095 native-chain segment boundaries.
- **R5**: Timeout semantics — iteration vs wall-clock; default disabled safe path.

### Evidence refs

- `docs/product/backlog.md` (`## US-0110` — `discovery_notes`)
- `docs/product/vision.md` (Discovery Notes — US-0110)
- `docs/engineering/research.md` (**`R-0091`**)
- `handoffs/intake_evidence/intake-sovereign-20260627-01.json`
- `docs/engineering/architecture.md` (compose constraints: US-0088, US-0092, US-0095, US-0044, US-0103 — do not amend)
- `decisions/DEC-0103.md` (ledger extension check compose)

### Isolation evidence (PO discovery phase)

| Field | Value |
|-------|-------|
| `phase_id` | `discovery` |
| `role` | `po` |
| `fresh_context_marker` | `po-US0110-discovery-20260628T170000Z-fresh` |
| `timestamp` | `2026-06-28T17:00:00Z` |
| `evidence_ref` | `handoffs/po_to_tl.md` (this handoff) + `docs/product/backlog.md` § US-0110 `discovery_notes` |

### Next

- **`/research`** (fresh **tech-lead** context) for **`US-0110`** — close **`R-0091`** Q1–Q7; companion DEC decision if Q7 affirms.

### Decision gate

- **None** — discovery satisfied; research readiness explicit.

---

