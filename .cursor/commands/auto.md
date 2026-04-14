---
description: "its-magic auto: deterministic continuation orchestrator."
---

# /auto

## Subagents
- curator
- tech-lead

## Execution model
- `/auto` is a **spawn-only orchestrator**: it schedules materialization, spawns
  fresh **phase-role** subagents, and verifies phase boundaries—it **must not**
  execute lifecycle phase work, perform phase-role duties, or author **phase
  deliverables** in the orchestrator context.
- For each phase, **spawn a fresh subagent** for that phase’s canonical role;
  phase output must arrive only via artifacts and handoff files (no in-turn
  orchestrator execution of that phase).
- Phase context transfer happens only through artifacts and handoff files.
- Scope is process/workflow orchestration only. Do not claim runtime product
  orchestration changes.

## Spawn-boundary integrity (BUG-0006)

- **Forbidden**: treating the orchestrator turn as the executor of a lifecycle
  phase (for example running **`architecture`**, **`execute`**, **`qa`**, or any
  other **`phase_id`** in the orchestrator instead of spawning the required
  subagent).
- **Fail fast** with **`AUTO_ORCHESTRATOR_PHASE_EXECUTION`**. **Remediation**:
  stop; spawn a **fresh** subagent for the canonical **`phase_id`** and **`role`**
  per the phase→role matrix (**DEC-0051**); do not merge phase output into
  orchestrator turns. **Distinct from** **`PHASE_CONTEXT_ISOLATION_VIOLATION`**
  (wrong writer / isolation break) and **`RUNTIME_PROOF_*`** / **`PHASE_ROLE_*`**
  families—do not overload those codes for a missing-spawn violation.

## Full specification (US-0080 / DEC-0062)

Long prose, expanded mode semantics, and **Steps 1–13** detail live in
**`docs/engineering/auto-orchestration-reference.md`** (jointly normative). This file
keeps **contract excerpts** required for regression parity and default `/auto` loads.

## Per-phase isolation enforcement (US-0048 / DEC-0029)

- Orchestrator must not write phase deliverables (`PHASE_CONTEXT_ISOLATION_VIOLATION`).
- Each spawned phase appends isolation evidence to `docs/engineering/state.md`
  with `phase_id`, `role`, `fresh_context_marker`, `timestamp`, `evidence_ref`.
- Fail closed on missing/invalid/stale evidence.

Reason codes: `PHASE_CONTEXT_ISOLATION_MISSING`, `PHASE_CONTEXT_ISOLATION_VIOLATION`,
`ISOLATION_EVIDENCE_STALE`, `ISOLATION_EVIDENCE_INVALID`.

## Strict runtime proof enforcement (US-0056 / DEC-0038)

- Each completed phase supplies tuple: `orchestrator_run_id`, `runtime_proof_id`,
  `phase_id`, `role`, `proof_issued_at`, `proof_ttl_seconds`, `proof_hash`
  (hash = SHA-256 sorted-key JSON per **DEC-0038**).
- `runtime_proof_id` unique per phase run; enforce TTL freshness and linkage.

Reason codes: `RUNTIME_PROOF_MISSING`, `RUNTIME_PROOF_INVALID`, `RUNTIME_PROOF_REUSED`,
`RUNTIME_PROOF_STALE`, `RUNTIME_PROOF_AMBIGUOUS_LINK`.

## Strict phase role enforcement (US-0069 / DEC-0051)

Post-hoc markers alone are insufficient: preflight expected role, capability gate,
post-completion match of isolation + strict-proof `role`, execute default deny unless
override governance is satisfied.

### Canonical phase→role matrix (fixed defaults)

| phase_id | Allowed roles | Default when no valid alternate policy |
|----------|-----------------|----------------------------------------|
| `intake` | `po` | `po` |
| `discovery` | `po` | `po` |
| `research` | `po`, `tech-lead` | `tech-lead` |
| `architecture` | `tech-lead` | `tech-lead` |
| `sprint-plan` | `tech-lead` | `tech-lead` |
| `plan-verify` | `qa`, `tech-lead` | `qa` |
| `execute` | `dev` (override path only) | `dev` |
| `qa` | `qa` | `qa` |
| `verify-work` | `qa` | `qa` |
| `release` | `release` | `release` |
| `refresh-context` | `curator`, `po` | `curator` |

Alternate-role keys (merged scratchpad): `AUTO_ROLE_RESEARCH`, `AUTO_ROLE_PLAN_VERIFY`,
`AUTO_ROLE_REFRESH_CONTEXT` — single-valued resolution per **DEC-0051** (see reference).

Execute override: requires `AUTO_EXECUTE_ROLE_OVERRIDE=allowed_non_dev_execute` **and**
parseable `EXECUTE_OVERRIDE_GOVERNANCE_REF`.

Role reason codes: `PHASE_ROLE_CAPABILITY_MISSING`, `PHASE_ROLE_MISMATCH`.

## Configurable phase selection policy (US-0070 / DEC-0052)

Treat **resolved phase plan** as fail-closed schedule from merged scratchpad **before**
resume / `start-from` intersection. Canonical lifecycle:

`intake` → `discovery` → `research` → `architecture` → `sprint-plan` →
`plan-verify` → `execute` → `qa` → `verify-work` → `release` → `refresh-context`

Selectors and reinstatement: see reference. Phase-plan reason codes include
`PHASE_POLICY_CONFLICT`, `PHASE_PLAN_UNKNOWN_PHASE`, `START_FROM_PHASE_PLAN_EMPTY_INTERSECTION`.

Phase boundary visibility (**AC-10**): record `resolved_phase_plan` snapshot,
`skipped_phases`, `phase_boundary`, `next_scheduled_phase` on `state.md`.

## Inputs

Merged scratchpad (**US-0073** / **DEC-0055**), automation flags (`AUTO_*`, `SECURITY_REVIEW`,
`TEAM_*`), phase-plan keys `AUTO_PHASE_PLAN`, `AUTO_PHASE_EXCLUDE`, `AUTO_PHASE_INCLUDE`,
`AUTO_PHASE_PROFILE`, `AUTO_PHASE_HIGH_RISK_ACK`, product/engineering docs,
optional `start-from=<phase>`, optional `--execute-bulk`, `handoffs/resume_brief.md`,
`docs/engineering/state.md`.

## Canonical status contract (US-0045)

Story status authority: `docs/product/backlog.md` only; do not infer readiness from
contradictory derived views.

## Outputs (artifacts)

Phase artifacts, `docs/engineering/state.md`, `handoffs/resume_brief.md` when stopped,
QA loop handoffs when applicable, continuation breadcrumbs including `resolution_source`
(`argument|resume_brief|state_fallback`) and related resume metadata per reference.

## Stop conditions

Decision gate, missing critical input, `AUTO_PAUSE_REQUEST` at safe boundary,
`AUTO_LOOP_MAX_CYCLES` with unresolved defects.

## Optional backlog-drain mode (US-0044 / DEC-0022)

Canonical controls: `AUTO_BACKLOG_DRAIN`, `AUTO_BACKLOG_MAX_STORIES`, `AUTO_BACKLOG_ON_BLOCK`,
`AUTO_STORY_SELECTION`. Reason codes include `BACKLOG_MAX_STORIES_REACHED`. Full semantics:
reference.

## Optional bulk execute mode (US-0047 / DEC-0024)

Explicit `--execute-bulk` or `AUTO_EXECUTE_BULK=1`. Reason codes include
`EXEC_BULK_MAX_ITEMS_REACHED`, `EXEC_TEAM_SCOPE_BLOCKED`, `EXEC_TEAM_SCOPE_SKIPPED`. Full
semantics: reference.

## Sync policy contract (US-0038 / DEC-0018)

Phase-completion boundary evaluation only. **Guarded auto-push eligibility chain**
(checklist in reference). Reason codes include `BRANCH_NOT_ALLOWLISTED`, `TEST_COMMAND_MISSING`,
`SYNC_PUSHED`. Full list: reference.

## Canonical `start-from` phase IDs

`intake`, `discovery`, `research`, `architecture`, `sprint-plan`, `plan-verify`,
`execute`, `qa`, `verify-work`, `release`, `refresh-context` — aliases invalid.

## Deterministic resume-source precedence

Resolve start phase in strict order:

1. Explicit `/auto start-from=<phase>`
2. `handoffs/resume_brief.md`
3. Conservative `docs/engineering/state.md` fallback
4. Fail fast on ambiguity/conflict/unrecoverable inputs

If `resume_brief.md` is present but stale or unparseable, fail fast instead
of silently falling back.

## Fail-fast error code contract

All resume-resolution failures must use:

[AUTO_RESUME_ERROR] <code>: <summary>. Source=<source>. Fix: <action>.

Required codes:
- `INVALID_START_FROM`
- `RESUME_BRIEF_MISSING`
- `RESUME_BRIEF_STALE`
- `RESUME_BRIEF_UNPARSEABLE`
- `RESUME_STATE_CONFLICT`
- `STATE_PHASE_AMBIGUOUS`
- `STATE_PHASE_UNRECOVERABLE`

## Steps (compact; full detail in reference)

1. Read automation flags from merged scratchpad and **materialize the resolved
   phase plan** per **Configurable phase selection policy (US-0070 / DEC-0052)**; append
   plan breadcrumbs to `docs/engineering/state.md` **before** first spawn.
2. Parse `start-from` / `--execute-bulk`; resolve nominal start phase; intersect with plan.
3. Record continuation metadata (`invocation_mode=auto`, `requested_start_from`,
   `resolved_start_phase`, `resolution_source`, `resolution_status`, `timestamp`).
4. Spawn fresh subagents per intersected schedule; enforce **US-0069** preflight/post checks.
5. Implementation loop, pause, stop breadcrumbs (`stop_reason` such as `completed|decision_gate|missing_input|pause_request|loop_max`, `stop_phase`, `timestamp`), `resume_brief` updates — reference.
6. 11a. Isolation evidence verification at each boundary.
7. 11b. At each phase boundary, verify strict runtime attestation tuple exists
   and is valid for the completed phase (`orchestrator_run_id`, `runtime_proof_id`,
   `phase_id`, `role`, `proof_issued_at`, `proof_ttl_seconds`, `proof_hash`).
8. Sync verdict recording when eligible — reference.
9. Backlog-drain / bulk per-item summaries when enabled — reference.

## Backward compatibility

Default manual/interactive unchanged; `/resume` remains valid; deterministic precedence
applies for `/auto` continuation.

## Deterministic artifact ordering guard (US-0058 / DEC-0040)

Follow `docs/engineering/artifact-ordering-policy.md` (`state.md` append-bottom, etc.);
`ARTIFACT_ORDERING_ANCHOR_AMBIGUOUS` fail-closed.
