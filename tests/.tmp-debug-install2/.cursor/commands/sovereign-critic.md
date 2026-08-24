---
description: "its-magic sovereign-critic: cross-model adversarial review after producer phase."
---

# /sovereign-critic

## Subagents
- tech-lead (default critic role; fresh context per US-0048 / US-0023)

## Execution model
- Run `/sovereign-critic` in a **fresh critic subagent** context only.
- Invoked by **`/auto`** orchestrator **after** a producer phase completes when
  `CROSS_MODEL_REVIEW=1` (default-off — zero overhead when `0`).
- Orchestrator **must not** execute critic work in-process (**BUG-0006** spawn-only).
- All three lenses run per invocation (parallel jury when distinct critic model;
  sequential fresh spawns in degraded single-model-multi-lens mode).

## Inputs

- `phase_id` — completed producer phase id (DEC-0086 canonical)
- `role` — producer logical role (`po`, `tech-lead`, `dev`, `qa`, …)
- `evidence_ref` — primary artifact refs for the completed phase
- `producer_model_id` — resolved slug or alias (`fast`, `inherit`, vendor slug)
- `artifact_digest` — bounded summary of phase deliverables under review
- `orchestrator_run_id` — partition key for rework counter

## Model selection

Resolve critic via `scripts/sovereign_critic_lib.py`:

```python
select_critic_model(producer_model_id, scratchpad, phase_id)
```

- Tier opposition: producer `strong`/`balanced` → critic `cheap`; producer `cheap` → critic `strong`.
- Same normalized slug → `degraded_mode=true`, reason `CROSS_MODEL_DEGRADED_MODE`.
- Catalog miss → degraded fallback (three sequential lens spawns, same `model_id`).

## Three-lens evaluation (all lenses per invocation)

| Lens | Focus | Checklist (2.5 pts each) |
|------|-------|--------------------------|
| **`challenger`** | Edge cases, races, failure modes, boundaries | edge_case_cited; failure_mode_named; concurrency_considered; input_boundary_tested |
| **`architect`** | Coupling, layering, dependency direction | coupling_named; layer_boundary_stated; dependency_direction_explicit; interface_contract_mentioned |
| **`subtractor`** | Over-engineering, YAGNI, scope creep | unnecessary_abstraction_flagged; yagni_applied; premature_generalization_challenged; scope_creep_identified |

### Lens prompt templates

**Challenger** — Find edge cases, race conditions, failure modes, and boundary violations in the phase artifacts. Cite specific paths. Report checklist hits and propose blocking findings when convergence should halt.

**Architect** — Evaluate coupling, layer boundaries, dependency direction, and interface contracts. Name modules and layers explicitly. Flag violations that block release readiness.

**Subtractor** — Challenge over-engineering, premature abstraction, YAGNI violations, and scope creep. Prefer minimal diffs aligned with task scope.

## Anti-slop scoring

Per lens: `score_lens_antislop(lens, checklist_hits)` → int 0–10.  
Aggregate: `compute_anti_slop_aggregate(lens_scores)` → `min(lens_scores)`.

Agent-reported `anti_slop_score` must be ≤ rubric ceiling (lib clamps down).

## Reconciliation

After all lens findings are collected, run `reconcile_findings(raw_findings)`:

- ≥2 lenses share `issue_key` → `confidence=high`, `single_finder=false`
- Exactly 1 lens → `confidence=medium`, `single_finder=true`

## Outputs (artifacts)

- Append findings to **`handoffs/sovereign_critic_findings.jsonl`** (15-field v1 schema)
- Optional **`cross_reviewer_findings`** block in sprint **`qa-findings.md`** via
  `build_qa_cross_reviewer_block(repo)`
- When `AI_DECISION_LEDGER=1`, call `patch_ledger_cross_model_reviewed(...)` with
  `cross_model_reviewed=True`

## Isolation evidence (US-0048 + US-0104 v2)

At the end of `/sovereign-critic`, append isolation evidence to `docs/engineering/state.md`:

- `phase_id=sovereign-critic`
- `role=tech-lead` (or configured critic role)
- `fresh_context_marker=<new marker for this critic subagent>`
- `timestamp=<ISO UTC>`
- `evidence_ref=<findings path + reviewed artifacts>`
- `model_id=<critic_model_id>` — **required when `CROSS_MODEL_REVIEW=1`**; omit when `0`

Missing `model_id` when critic enabled → fail-closed **`ISOLATION_EVIDENCE_MODEL_ID_MISSING`**.

## Stop conditions

- `CROSS_MODEL_REVIEW=0` → skip entirely (zero overhead)
- `CROSS_MODEL_CRITIC_SPAWN_FAILED` → blocking orchestrator hook failure
- `CROSS_MODEL_FINDINGS_INVALID` → schema validation failure
- `CROSS_MODEL_RECONCILE_FAILED` → jury merge error

## Validator

```bash
python scripts/sovereign_critic_validate.py --repo . --enforce
python scripts/sovereign_critic_validate.py --open-blocking --repo .
```

Success literal: **`[SOVEREIGN_CRITIC_VALIDATION_OK]`**.
