---
description: "its-magic auto: deterministic continuation orchestrator."
---

# /auto

## Subagents
- curator
- tech-lead

## Execution model
- `/auto` is an orchestrator only. It must not execute phase work directly.
- For each phase, spawn a fresh subagent context for that phase role.
- Phase context transfer happens only through artifacts and handoff files.
- Scope is process/workflow orchestration only. Do not claim runtime product
  orchestration changes.

## Per-phase isolation enforcement (US-0048 / DEC-0029)

`/auto` must enforce fresh-context isolation as a fail-closed contract:

- `/auto` must not write phase deliverables itself. If phase work is performed in
  the orchestrator context, stop immediately with reason code
  `PHASE_CONTEXT_ISOLATION_VIOLATION`.
- Each spawned phase must write isolation evidence with required fields
  (`phase_id`, `role`, `fresh_context_marker`, `timestamp`, `evidence_ref`) to
  the canonical evidence store (`docs/engineering/state.md`) before `/auto`
  proceeds to the next phase.
- `/auto` must fail closed when evidence is missing/invalid/stale (see reason
  codes below). No silent continuation.

Reason codes (deterministic):
- `PHASE_CONTEXT_ISOLATION_MISSING`
- `PHASE_CONTEXT_ISOLATION_VIOLATION`
- `ISOLATION_EVIDENCE_STALE`
- `ISOLATION_EVIDENCE_INVALID`

## Inputs
- `AUTO_FLOW_MODE` and `PHASE_MODE` from `.cursor/scratchpad.md`
- `AUTO_IMPLEMENTATION_LOOP`, `AUTO_LOOP_MAX_CYCLES` from `.cursor/scratchpad.md`
- `AUTO_PAUSE_REQUEST`, `AUTO_PAUSE_POLICY` from `.cursor/scratchpad.md`
- `SECURITY_REVIEW`, `COMPLIANCE_PROFILES` from `.cursor/scratchpad.md`
- `AUTO_EXECUTE_BULK`, `AUTO_EXECUTE_MAX_ITEMS`, `AUTO_EXECUTE_ON_BLOCK`,
  `AUTO_EXECUTE_SELECTION`, `AUTO_TEAM_SCOPE_ENFORCE` from `.cursor/scratchpad.md`
- `TEAM_MODE`, `TEAM_MEMBER`, `ACTIVE_TASK_IDS` from merged scratchpad context
- Current product and engineering docs
- Optional explicit argument: `start-from=<phase>`
- Optional explicit argument: `--execute-bulk` (one-run explicit override)
- Resume-source artifacts:
  - `handoffs/resume_brief.md`
  - `docs/engineering/state.md`

## Canonical status contract (US-0045)

- Story status authority is `docs/product/backlog.md` only.
- `docs/product/acceptance.md` and `docs/engineering/state.md` are derived views.
- `/auto` must not infer implementation readiness from non-canonical status
  artifacts when they conflict with backlog status.

## Outputs (artifacts)
- Updated phase artifacts for each step
- `docs/engineering/state.md`
- `handoffs/resume_brief.md` if stopped
- `sprints/S0001/qa-findings.md` and `handoffs/qa_to_dev.md` when loop finds issues
- Deterministic continuation breadcrumbs in relevant artifacts

## Stop conditions
- Decision gate triggered
- Missing critical input
- `AUTO_PAUSE_REQUEST=1` reached at a safe boundary
- `AUTO_LOOP_MAX_CYCLES` reached with unresolved defects

## Optional backlog-drain mode (US-0044 / DEC-0022)

`/auto` supports an optional multi-story backlog-drain mode. Default behavior
remains unchanged unless explicitly enabled.

Canonical controls from `.cursor/scratchpad.md`:
- `AUTO_BACKLOG_DRAIN`: `0|1` (default `0`)
- `AUTO_BACKLOG_MAX_STORIES`: integer `>=1` (default `1`)
- `AUTO_BACKLOG_ON_BLOCK`: `stop|skip` (default `stop`)
- `AUTO_STORY_SELECTION`: `priority_then_backlog_order` (default)

Deterministic behavior when enabled (`AUTO_BACKLOG_DRAIN=1`):
- Select next eligible OPEN story via `AUTO_STORY_SELECTION`.
- Run full story lifecycle (`discovery -> ... -> release -> refresh-context`).
- After each story completion, continue to next eligible story until:
  - `AUTO_BACKLOG_MAX_STORIES` limit reached, or
  - no eligible stories remain, or
  - stop condition / decision gate occurs.
- On blocked story:
  - `AUTO_BACKLOG_ON_BLOCK=stop` -> stop immediately.
  - `AUTO_BACKLOG_ON_BLOCK=skip` -> record skip reason and continue.

Default-safe behavior:
- With `AUTO_BACKLOG_DRAIN=0`, preserve existing single-segment continuation.

## Optional bulk execute mode (US-0047 / DEC-0024)

`/auto` supports an explicit bulk execute orchestration mode for continuous
planned-item delivery. Default behavior remains unchanged unless explicitly
enabled.

Canonical controls from `.cursor/scratchpad.md`:
- `AUTO_EXECUTE_BULK`: `0|1` (default `0`)
- `AUTO_EXECUTE_MAX_ITEMS`: integer `>=1` (default `1`)
- `AUTO_EXECUTE_ON_BLOCK`: `stop|skip` (default `stop`)
- `AUTO_EXECUTE_SELECTION`: `planned_then_priority` (default)
- `AUTO_TEAM_SCOPE_ENFORCE`: `0|1` (default `1`)

Explicit activation contract:
- Bulk execute mode is activated when either:
  - explicit argument `--execute-bulk` is present for this run, or
  - `AUTO_EXECUTE_BULK=1` in scratchpad.
- Without explicit activation, preserve current non-bulk continuation behavior.

Deterministic behavior when enabled:
- Select next eligible planned work item via `AUTO_EXECUTE_SELECTION`.
- Process each item with strict isolation:
  - fresh subagent per phase boundary
  - fresh subagent per execute<->QA loop cycle
- Apply bounded stop criteria:
  - stop at `AUTO_EXECUTE_MAX_ITEMS`, or
  - stop/skip on blocked item per policy, or
  - stop when no eligible items remain.

Team mode guardrails (`TEAM_MODE=1`):
- Snapshot and record team context inputs:
  - `TEAM_MODE`, `TEAM_MEMBER`, `ACTIVE_TASK_IDS`
- If `AUTO_TEAM_SCOPE_ENFORCE=1`, only tasks in current member scope are
  executable.
- Out-of-scope tasks must be deterministically handled with no writes:
  - `stop` policy -> `EXEC_TEAM_SCOPE_BLOCKED`
  - `skip` policy -> `EXEC_TEAM_SCOPE_SKIPPED`

## Sync policy contract (US-0038 / DEC-0018)

`/auto` may evaluate sync eligibility only at phase-completion boundaries.
It remains process-level guidance (no runtime git orchestrator changes).

Canonical policy controls from `.cursor/scratchpad.md`:
- `SYNC_POLICY_MODE`:
  `disabled|manual|by_phase|by_milestone|custom_phase_list`
- `SYNC_CUSTOM_PHASES`: comma-separated canonical phase IDs for
  `custom_phase_list` mode
- `ALLOW_AUTO_PUSH`: `0|1`
- `AUTO_PUSH_BRANCH_ALLOWLIST`: comma-separated branches/patterns

Deterministic policy semantics:
- `disabled`: skip sync evaluation entirely (`SYNC_DISABLED`).
- `manual`: no auto-sync attempts (`MANUAL_MODE_NO_AUTO`).
- `by_phase`: evaluate at every phase completion boundary.
- `by_milestone`: evaluate only at milestone completion boundary.
- `custom_phase_list`: evaluate only when completed phase is listed.
- Unset/invalid mode fails closed to `manual`.

Guarded auto-push eligibility chain (all required):
1. Boundary is eligible for configured mode.
2. `ALLOW_AUTO_PUSH=1`.
3. QA-first safety passes (feature work cannot auto-push before QA pass;
   manual user-invoked sync remains allowed).
4. No unresolved blocking QA findings / critical unresolved issues.
5. Branch safety passes: protected/default branches are denied by default unless
   explicitly allowlisted.
6. Mandatory pre-push checks pass:
   - `TEST_COMMAND` is required
   - optional `LINT_COMMAND` / `TYPECHECK_COMMAND` run only when configured
   - failures or timeout result in `no_push`

If any condition fails, verdict is deterministic `no_push` with reason code.

Reason-code baseline:
- `SYNC_DISABLED`
- `MANUAL_MODE_NO_AUTO`
- `SYNC_TRIGGER_NOT_ELIGIBLE`
- `AUTO_PUSH_NOT_ENABLED`
- `PRE_QA_AUTOPUSH_FORBIDDEN`
- `BLOCKING_QA_FINDINGS`
- `BRANCH_NOT_ALLOWLISTED`
- `TEST_COMMAND_MISSING`
- `TEST_FAILED`
- `TEST_TIMEOUT`
- `OPTIONAL_CHECK_FAILED`
- `SYNC_PUSHED`
- `BACKLOG_DRAIN_DISABLED`
- `BACKLOG_STORY_BLOCKED_STOP`
- `BACKLOG_STORY_BLOCKED_SKIPPED`
- `BACKLOG_MAX_STORIES_REACHED`
- `BACKLOG_NO_ELIGIBLE_STORIES`
- `EXEC_BULK_DISABLED`
- `EXEC_BULK_ITEM_BLOCKED_STOP`
- `EXEC_BULK_ITEM_BLOCKED_SKIPPED`
- `EXEC_BULK_MAX_ITEMS_REACHED`
- `EXEC_BULK_NO_ELIGIBLE_ITEMS`
- `EXEC_TEAM_SCOPE_BLOCKED`
- `EXEC_TEAM_SCOPE_SKIPPED`

## Canonical `start-from` contract

- Accepted canonical phase IDs:
  - `intake`
  - `discovery`
  - `research`
  - `architecture`
  - `sprint-plan`
  - `plan-verify`
  - `execute`
  - `qa`
  - `verify-work`
  - `release`
  - `refresh-context`
- Only canonical IDs are accepted. Alias values (for example `sprint_plan`,
  `verifywork`) are invalid and must fail fast.

## Deterministic resume-source precedence

Resolve start phase in strict order:

1. Explicit `/auto start-from=<phase>`
2. `handoffs/resume_brief.md`
3. Conservative `docs/engineering/state.md` fallback
4. Fail fast on ambiguity/conflict/unrecoverable inputs

Deterministic precedence behavior:
- If explicit `start-from` is valid, it wins and lower-priority sources do not
  affect selected start phase.
- `state.md` fallback is used only when `resume_brief.md` is absent.
- If `resume_brief.md` is present but stale or unparseable, fail fast instead
  of silently falling back.

## Conflict and stale/unparseable policy

- Explicit valid override always wins and is logged as override.
- No override + `resume_brief` conflicts with `state` inference: fail fast.
- `resume_brief` exists but stale: fail fast.
- `resume_brief` exists but unparseable: fail fast.
- `state` fallback yields multiple candidate phases: fail fast.
- `state` fallback yields no trustworthy boundary: fail fast.

## Fail-fast error code contract

All resume-resolution failures must use:

`[AUTO_RESUME_ERROR] <code>: <summary>. Source=<source>. Fix: <action>.`

Required codes:
- `INVALID_START_FROM`
- `RESUME_BRIEF_MISSING`
- `RESUME_BRIEF_STALE`
- `RESUME_BRIEF_UNPARSEABLE`
- `RESUME_STATE_CONFLICT`
- `STATE_PHASE_AMBIGUOUS`
- `STATE_PHASE_UNRECOVERABLE`

## Steps
1. Read automation flags from scratchpad.
2. Parse optional `start-from=<phase>` and validate canonical phase ID rules.
   Parse optional `--execute-bulk` and treat it as explicit one-run override.
3. Resolve start phase using deterministic precedence:
   - explicit argument -> resume brief -> state fallback -> fail-fast.
   - Emit `[AUTO_RESUME_ERROR] ...` message on resolver failure.
4. Record continuation breadcrumb metadata in `docs/engineering/state.md`:
   - `invocation_mode=auto`
   - `requested_start_from`
   - `resolved_start_phase`
   - `resolution_source` (`argument|resume_brief|state_fallback`)
   - `resolution_status` (`resolved|fail-fast`)
   - `timestamp`
5. Spawn a fresh subagent for each remaining phase in canonical order, starting
   at the resolved phase:
   intake -> discovery -> research -> architecture -> sprint plan ->
   plan verify -> execute -> QA -> verify work -> release -> refresh context.
   If `SECURITY_REVIEW=1`, run `/security-review` in a fresh security subagent:
   - in `design` mode immediately after architecture and before sprint plan,
   - in `code` mode immediately after execute and before QA.
   If `SECURITY_REVIEW=0` (default), skip both checks with zero overhead.
   - If `AUTO_BACKLOG_DRAIN=1`, repeat story lifecycle for next eligible OPEN
     story using deterministic selection policy until bounded stop criteria.
   - If bulk execute mode is active (`--execute-bulk` or
     `AUTO_EXECUTE_BULK=1`), iterate eligible planned items using
     `AUTO_EXECUTE_SELECTION` with bounded item count
     (`AUTO_EXECUTE_MAX_ITEMS`) and deterministic block/skip semantics.
   - In team mode with enforcement enabled, run pre-mutation scope checks against
     `TEAM_MEMBER` and `ACTIVE_TASK_IDS`; out-of-scope tasks produce deterministic
     reason codes and no writes.
6. Pass only the phase input files and current objective to each spawned
   subagent. Do not pass prior conversational reasoning as phase context.
7. If `AUTO_IMPLEMENTATION_LOOP=1`, alternate fresh subagents for execute and QA
   (`dev`, then `qa`, then new `dev`, then new `qa`) until no blocking findings
   or `AUTO_LOOP_MAX_CYCLES` is reached.
   - After each cycle, verify that both phases wrote new isolation evidence
     entries (distinct `fresh_context_marker` per phase per cycle).
8. If `AUTO_PAUSE_REQUEST=1`, stop at the next safe boundary
   (`AUTO_PAUSE_POLICY`) and spawn `/pause` in a fresh curator subagent.
9. Preserve existing stop conditions and gates without bypass:
   - decision gate
   - missing critical input
   - pause request at safe boundary
   - loop max cycles reached
10. On stop (or completion), write breadcrumbs:
   - `stop_reason` (`completed|decision_gate|missing_input|pause_request|loop_max`)
   - `stop_phase`
   - `timestamp`
11. If stopped before completion, update `handoffs/resume_brief.md` with the
    intended next phase and stop metadata.
11a. At each phase boundary, verify isolation evidence exists for the completed
    phase in `docs/engineering/state.md` and includes all required fields. If
    missing/invalid/stale, stop with the appropriate reason code and remediation
    guidance (run the phase again in a fresh subagent context and write new
    evidence).
12. At each phase boundary, evaluate sync policy only when mode requires it and
    record a deterministic sync verdict entry with:
    - `phase_boundary`
    - `policy_mode`
    - `trigger_source` (`manual|auto`)
    - `branch`
    - `checks` (`test|lint|typecheck`: `pass|fail|skipped`)
    - `qa_status_snapshot`
    - `push_decision` (`pushed|blocked|not_eligible`)
    - `reason_code`
    - `evidence_refs`
13. When backlog-drain mode or bulk execute mode is enabled, append per-item run
    summary entries:
    - `item_id`
    - `item_kind` (`story|sprint`)
    - `story_id`
    - `sprint_id`
    - `story_start_phase`
    - `story_stop_phase`
    - `story_outcome` (`released|blocked|skipped`)
    - `story_reason_code`
    - `team_context_snapshot` (`TEAM_MODE`, `TEAM_MEMBER`, `ACTIVE_TASK_IDS`)
    - `timestamp`

## Backward compatibility

- Manual and interactive workflows remain unchanged by default.
- `/resume` remains valid for context loading and guided continuation.
- Deterministic precedence and fail-fast behavior apply when `/auto` continuation
  is invoked.
