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

## Inputs
- `AUTO_FLOW_MODE` and `PHASE_MODE` from `.cursor/scratchpad.md`
- `AUTO_IMPLEMENTATION_LOOP`, `AUTO_LOOP_MAX_CYCLES` from `.cursor/scratchpad.md`
- `AUTO_PAUSE_REQUEST`, `AUTO_PAUSE_POLICY` from `.cursor/scratchpad.md`
- `SECURITY_REVIEW`, `COMPLIANCE_PROFILES` from `.cursor/scratchpad.md`
- Current product and engineering docs
- Optional explicit argument: `start-from=<phase>`
- Resume-source artifacts:
  - `handoffs/resume_brief.md`
  - `docs/engineering/state.md`

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
6. Pass only the phase input files and current objective to each spawned
   subagent. Do not pass prior conversational reasoning as phase context.
7. If `AUTO_IMPLEMENTATION_LOOP=1`, alternate fresh subagents for execute and QA
   (`dev`, then `qa`, then new `dev`, then new `qa`) until no blocking findings
   or `AUTO_LOOP_MAX_CYCLES` is reached.
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

## Backward compatibility

- Manual and interactive workflows remain unchanged by default.
- `/resume` remains valid for context loading and guided continuation.
- Deterministic precedence and fail-fast behavior apply when `/auto` continuation
  is invoked.
