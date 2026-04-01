# /auto — full orchestration specification (reference)

> **US-0080 / DEC-0062**: Expanded contract for `/auto`. The slim `.cursor/commands/auto.md` is the default injected surface; load this file when full prose, tables, and step detail are required.

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

## Strict runtime proof enforcement (US-0056 / DEC-0038)

`/auto` must enforce strict runtime attestation in addition to artifact-level
isolation evidence:

- Each completed phase must provide a runtime attestation tuple linked to the
  phase checkpoint evidence:
  - `orchestrator_run_id`
  - `runtime_proof_id`
  - `phase_id`
  - `role`
  - `proof_issued_at` (ISO UTC / RFC3339)
  - `proof_ttl_seconds`
  - `proof_hash`
- `runtime_proof_id` must be unique per phase run; reused proof IDs are invalid.
- Proof freshness must be validated against `proof_issued_at` + TTL policy.
- Proof linkage must be deterministic and auditable to checkpoint evidence refs.
- Fail closed on any strict-proof violation; no silent continuation.

Strict-proof reason codes:
- `RUNTIME_PROOF_MISSING`
- `RUNTIME_PROOF_INVALID`
- `RUNTIME_PROOF_REUSED`
- `RUNTIME_PROOF_STALE`
- `RUNTIME_PROOF_AMBIGUOUS_LINK`

## Strict phase role enforcement (US-0069 / DEC-0051)

`/auto` must enforce a deterministic **phase→role contract** with **preflight
admission** before each phase spawn, **fail-closed checkpoint validation** after
each phase completes, and **aligned strict-proof `role`** values. Post-hoc
isolation markers alone are insufficient.

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

### Alternate-role scratchpad policy (single-valued resolution)

Resolve **exactly one** expected role for phases with alternates using merged
scratchpad (active + `.cursor/scratchpad.local.md`; template parity on install):

- `AUTO_ROLE_RESEARCH`: `po` \| `tech-lead` — when **unset or empty**, default
  `tech-lead`; when set to any other value, fail closed with diagnostics (no
  unrelated-role fallback).
- `AUTO_ROLE_PLAN_VERIFY`: `qa` \| `tech-lead` — when **unset or empty**,
  default `qa`; otherwise only `qa` or `tech-lead` allowed (else fail closed).
- `AUTO_ROLE_REFRESH_CONTEXT`: `curator` \| `po` — when **unset or empty**,
  default `curator`; otherwise only `curator` or `po` allowed (else fail closed).

### Preflight capability gate (before spawn)

Before spawning phase work, `/auto` must:

1. Resolve `phase_id` → expected canonical `role` (matrix + policy keys above).
2. For `execute`, apply **default deny**: expected role is `dev` unless **both**
   `AUTO_EXECUTE_ROLE_OVERRIDE=allowed_non_dev_execute` **and**
   `EXECUTE_OVERRIDE_GOVERNANCE_REF` point to a **parseable** approved exception
   record (for example `DEC-xxxx` or a documented anchor in
   `docs/engineering/state.md`).
3. Evaluate **role capability availability** for that boundary (subagent/tooling
   can satisfy the resolved role).
4. On missing capability: stop with `PHASE_ROLE_CAPABILITY_MISSING` including
   `phase_id`, expected role, observed capability result, and remediation. **Do
   not** spawn under a substitute unrelated role.

### Post-completion boundary validation

When a phase completes, before advancing:

- Isolation evidence `role` must equal the **same** preflight-resolved expected
  role for that `phase_id`. Else stop with `PHASE_ROLE_MISMATCH`.
- Strict-proof tuple `role` must equal isolation `role` and the expected role.
- `proof_hash` must be SHA-256 over canonical sorted-key JSON of
  `orchestrator_run_id`, `runtime_proof_id`, `phase_id`, `role`,
  `proof_issued_at`, `proof_ttl_seconds` (`DEC-0038` / architecture US-0069).

### Resume / `start-from` parity

Every `/auto` invocation (explicit `start-from`, `resume_brief`, or conservative
`state.md` fallback) must **recompute** policy resolution and preflight from
scratch; stale continuation artifacts must not bypass the gate.

### Role-enforcement reason codes (deterministic)

- `PHASE_ROLE_CAPABILITY_MISSING`
- `PHASE_ROLE_MISMATCH`

## Configurable phase selection policy (US-0070 / DEC-0052)

`/auto` must treat the **resolved phase plan** as a first-class, fail-closed
schedule: a single ordered subset of canonical phases computed from merged
scratchpad (active + `.cursor/scratchpad.local.md`; template parity on install),
**before** resume/`start-from` intersection and **before** any phase spawn.

### Canonical lifecycle order (baseline `full` plan)

Unless narrowed by policy, the canonical ordered phase list is:

`intake` → `discovery` → `research` → `architecture` → `sprint-plan` →
`plan-verify` → `execute` → `qa` → `verify-work` → `release` →
`refresh-context`

When `SECURITY_REVIEW=1`, insert `/security-review` in **design** mode
immediately after `architecture` and before `sprint-plan`, and in **code** mode
immediately after `execute` and before `qa`, as documented in **Steps** below.
Record these inserts in `resolved_phase_plan` breadcrumbs using the same
deterministic labels the orchestrator already uses for security boundaries.

### Scratchpad selectors (exactly one active policy mode)

At most one of the following may be materially active after merge. If two or
more non-default selectors conflict, fail closed with `PHASE_POLICY_CONFLICT`
and **do not** materialize a plan:

- `AUTO_PHASE_PLAN=full` — full canonical lifecycle (including security-review
  inserts when enabled). Default when unset and no other selector is set.
- `AUTO_PHASE_EXCLUDE=<csv>` — start from `full`, remove listed phase IDs
  (validate each token; unknown id → `PHASE_PLAN_UNKNOWN_PHASE`).
- `AUTO_PHASE_INCLUDE=<csv>` — schedule **only** listed ids, then **re-sort**
  into canonical lifecycle order. Unknown id → `PHASE_PLAN_UNKNOWN_PHASE`.
  Empty result after parsing → `PHASE_PLAN_EMPTY_INCLUDE`.
- `AUTO_PHASE_PROFILE=<name>` — expand a **named profile** from the registry
  below. Unknown profile → `PHASE_PLAN_UNKNOWN_PROFILE`.

**Conflict rule**: `AUTO_PHASE_PLAN` is default-only when it is unset, empty, or
exactly `full`. Any explicit non-`full` `AUTO_PHASE_PLAN` value is invalid
(fail closed with `PHASE_PLAN_INVALID_AUTO_PHASE_PLAN`) — use `INCLUDE` /
`EXCLUDE` / `PROFILE` instead.

### Profile registry (baseline)

- `default` — equivalent to `full` (optional explicit alias; same behavior as
  unset policy).

**High-risk profile sketch** (illustrative; `R-0049`): `profile_high_risk_dev_fast`
may only be selected when **both** hold: `AUTO_PHASE_PROFILE=profile_high_risk_dev_fast`
and `AUTO_PHASE_HIGH_RISK_ACK=<operator_token>` matches the profile spec
version documented in `decisions/DEC-0052.md` / research `R-0049`. Missing ack →
`PHASE_PLAN_HIGH_RISK_ACK_REQUIRED`. High-risk profiles may define **narrower**
reinstatement rules **only** as documented for that profile; default profile
behavior applies otherwise.

### Plan materialization pipeline (evaluation order)

On every `/auto` entry (including resume, backlog-drain, bulk execute, and
team-mode runs), **recompute** from merged scratchpad:

1. Parse merged scratchpad policy inputs for phase selection + `SECURITY_REVIEW`.
2. Detect active policy mode; on conflict → `PHASE_POLICY_CONFLICT` (no plan).
3. Expand mode to a **candidate** ordered phase list in canonical order.
4. Apply **non-skippable reinstatement** for the **default profile** (and for
   any profile that does not explicitly document a narrower exception with ack):
   - **Safety gates**: always reinstate if removed: `qa`, `verify-work`,
     `release`.
   - **Evidence-chain closure**: if the candidate retains any phase from
     `execute` onward (`execute`, optional `security-review-code`, `qa`,
     `verify-work`, `release`, `refresh-context`), reinstate (if removed) the
     contiguous canonical prefix from `intake` through `plan-verify` so later
     gates retain valid upstream isolation + strict-proof chain semantics.
   - When `SECURITY_REVIEW=1`, reinstate the corresponding `security-review-*`
     insert when the adjacent retained phases would otherwise violate the
     documented security boundary contract.
   Record each reinstatement in breadcrumbs with reason `non_skippable_gate`
   (or a more specific documented code).
5. Record **operator-visible plan breadcrumbs** to `docs/engineering/state.md`
   **before** first spawn (append-bottom per `DEC-0040`):
   - `phase_policy_mode` (`full|exclude|include|profile`)
   - `resolved_phase_plan` (ordered `phase_id` list)
   - `skipped_phases` (id + reason: `policy_exclude`, `non_skippable_gate`,
     `default_full_plan`, etc.)
   - `orchestrator_run_id` (when known for this run)
6. **Do not** silently revive phases omitted by policy on continuation: every
   entry re-reads scratchpad bytes and recomputes the plan class.

### `start-from` and resume intersection with the resolved plan

After computing the **resolved phase plan**, resolve the **nominal** start
phase using **Deterministic resume-source precedence** (explicit `start-from`
→ `resume_brief` → `state` fallback → fail-fast).

Then **intersect**:

- Keep phases that appear in the resolved plan **in plan order**, starting at
  the first plan phase whose canonical position is **at or after** the nominal
  anchor phase (canonical order matches the baseline list above, including
  security inserts when enabled).
- If the intersection is empty, fail closed with
  `START_FROM_PHASE_PLAN_EMPTY_INTERSECTION` and diagnostics listing
  `resolved_phase_plan` vs `requested_start_phase` / resume inference.

### Compatibility with `US-0069` / `DEC-0051`

- Role resolution and preflight apply **only** to phases present in the
  intersected schedule. Skipping `research` does **not** change the expected
  role for `architecture` or any other retained phase.
- Skipped phases produce **no** spawn and **no** alternate-role substitution
  for a different phase.

### Phase-plan reason codes (deterministic)

Add to operator diagnostics and breadcrumb records:

- `PHASE_POLICY_CONFLICT`
- `PHASE_PLAN_UNKNOWN_PHASE`
- `PHASE_PLAN_EMPTY_INCLUDE`
- `PHASE_PLAN_UNKNOWN_PROFILE`
- `PHASE_PLAN_INVALID_AUTO_PHASE_PLAN`
- `PHASE_PLAN_HIGH_RISK_ACK_REQUIRED`
- `START_FROM_PHASE_PLAN_EMPTY_INTERSECTION`

### Phase boundary operator visibility (AC-10)

At each phase boundary (after completing a scheduled phase), record a compact
**phase boundary status** entry (for example in `docs/engineering/state.md`
continuation breadcrumbs) including:

- `resolved_phase_plan` snapshot (or stable hash pointer to the run’s plan record)
- `skipped_phases` summary (id + reason code)
- `phase_boundary` (completed `phase_id`)
- `next_scheduled_phase` (or `none` when complete/stopped)

## Inputs
- Merged scratchpad policy (`US-0073` / `DEC-0055`): resolve flags from **local >
  materialized `.cursor/scratchpad.md` > `.cursor/scratchpad.local.example.md`**
  (installers materialize baseline when missing; missing required keys after merge
  must fail closed with `[SCRATCHPAD_MERGE_ERROR]` diagnostics, not silent defaults).
- `AUTO_FLOW_MODE` and `PHASE_MODE` from merged scratchpad
- `AUTO_IMPLEMENTATION_LOOP`, `AUTO_LOOP_MAX_CYCLES` from merged scratchpad
- `AUTO_PAUSE_REQUEST`, `AUTO_PAUSE_POLICY` from merged scratchpad
- `SECURITY_REVIEW`, `COMPLIANCE_PROFILES` from merged scratchpad
- `AUTO_EXECUTE_BULK`, `AUTO_EXECUTE_MAX_ITEMS`, `AUTO_EXECUTE_ON_BLOCK`,
  `AUTO_EXECUTE_SELECTION`, `AUTO_TEAM_SCOPE_ENFORCE` from merged scratchpad
- `AUTO_ROLE_RESEARCH`, `AUTO_ROLE_PLAN_VERIFY`, `AUTO_ROLE_REFRESH_CONTEXT`,
  `AUTO_EXECUTE_ROLE_OVERRIDE`, `EXECUTE_OVERRIDE_GOVERNANCE_REF` from merged
  scratchpad (US-0069 / DEC-0051)
- `AUTO_PHASE_PLAN`, `AUTO_PHASE_EXCLUDE`, `AUTO_PHASE_INCLUDE`,
  `AUTO_PHASE_PROFILE`, `AUTO_PHASE_HIGH_RISK_ACK` from merged scratchpad
  (US-0070 / DEC-0052)
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
- `RUNTIME_PROOF_MISSING`
- `RUNTIME_PROOF_INVALID`
- `RUNTIME_PROOF_REUSED`
- `RUNTIME_PROOF_STALE`
- `RUNTIME_PROOF_AMBIGUOUS_LINK`
- `PHASE_ROLE_CAPABILITY_MISSING`
- `PHASE_ROLE_MISMATCH`
- `PHASE_POLICY_CONFLICT`
- `PHASE_PLAN_UNKNOWN_PHASE`
- `PHASE_PLAN_EMPTY_INCLUDE`
- `PHASE_PLAN_UNKNOWN_PROFILE`
- `PHASE_PLAN_INVALID_AUTO_PHASE_PLAN`
- `PHASE_PLAN_HIGH_RISK_ACK_REQUIRED`
- `START_FROM_PHASE_PLAN_EMPTY_INTERSECTION`

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
1. Read automation flags from merged scratchpad and **materialize the resolved
   phase plan** per **Configurable phase selection policy (US-0070 / DEC-0052)**:
   detect exactly-one policy mode, expand, apply non-skippable reinstatement,
   validate tokens/profile/ack requirements, and append plan breadcrumbs
   (`phase_policy_mode`, `resolved_phase_plan`, `skipped_phases` + reasons) to
   `docs/engineering/state.md` **before** any phase spawn. On failure, emit
   deterministic phase-plan reason codes and stop (no partial schedule).
2. Parse optional `start-from=<phase>` and validate canonical phase ID rules.
   Parse optional `--execute-bulk` and treat it as explicit one-run override.
3. Resolve **nominal** start phase using deterministic precedence:
   - explicit argument -> resume brief -> state fallback -> fail-fast.
   - Emit `[AUTO_RESUME_ERROR] ...` message on resolver failure.
3a. **Intersect** the nominal start anchor with the resolved phase plan (plan
   order preserved; drop scheduled phases strictly before the anchor in canonical
   order). **Empty intersection** → fail fast with
   `START_FROM_PHASE_PLAN_EMPTY_INTERSECTION` and diagnostics listing
   `resolved_phase_plan` vs `requested_start_phase` / inferred resume anchor.
   Set the executable schedule to this intersection.
4. Record continuation breadcrumb metadata in `docs/engineering/state.md`:
   - `invocation_mode=auto`
   - `requested_start_from`
   - `resolved_start_phase` (first phase of the intersected schedule)
   - `resolution_source` (`argument|resume_brief|state_fallback`)
   - `resolution_status` (`resolved|fail-fast`)
   - `timestamp`
5. Spawn a fresh subagent for each remaining phase in **the intersected
   resolved schedule order** (not the full canonical list when phases are
   omitted), starting at `resolved_start_phase`:
   default full path:
   intake -> discovery -> research -> architecture -> sprint plan ->
   plan verify -> execute -> QA -> verify work -> release -> refresh context.
   If `SECURITY_REVIEW=1`, run `/security-review` in a fresh security subagent:
   - in `design` mode immediately after architecture and before sprint plan,
   - in `code` mode immediately after execute and before QA.
   If `SECURITY_REVIEW=0` (default), skip both checks with zero overhead.
   - If `AUTO_BACKLOG_DRAIN=1`, repeat story lifecycle for next eligible OPEN
     story using deterministic selection policy until bounded stop criteria.
     **Reload merged scratchpad phase-selection inputs and recompute the phase
     plan at each story boundary** (same policy class as single-segment runs).
   - If bulk execute mode is active (`--execute-bulk` or
     `AUTO_EXECUTE_BULK=1`), iterate eligible planned items using
     `AUTO_EXECUTE_SELECTION` with bounded item count
     (`AUTO_EXECUTE_MAX_ITEMS`) and deterministic block/skip semantics.
     **Reload merged scratchpad phase-selection inputs and recompute the phase
     plan at each item boundary** (no silent revival of omitted phases).
   - In team mode with enforcement enabled, run pre-mutation scope checks against
     `TEAM_MEMBER` and `ACTIVE_TASK_IDS`; out-of-scope tasks produce deterministic
     reason codes and no writes.
   - **US-0069 / DEC-0051**: Before each phase spawn, resolve the single-valued
     expected role (matrix + `AUTO_ROLE_RESEARCH`, `AUTO_ROLE_PLAN_VERIFY`,
     `AUTO_ROLE_REFRESH_CONTEXT`), enforce execute default deny / override
     contract, and run the preflight capability gate; on failure stop with
     `PHASE_ROLE_CAPABILITY_MISSING` (no unrelated-role spawn).
   - **US-0069 / DEC-0051**: After each phase completes, validate isolation
     `role` and strict-proof `role` against the preflight-resolved expected
     role; on conflict stop with `PHASE_ROLE_MISMATCH`.
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
    evidence). Append **phase boundary status** per **Configurable phase
    selection policy (US-0070 / DEC-0052)** (selected/skipped summary + next
    scheduled phase).
11b. At each phase boundary, verify strict runtime attestation tuple exists and
    is valid for the completed phase (`orchestrator_run_id`,
    `runtime_proof_id`, `phase_id`, `role`, `proof_issued_at`,
    `proof_ttl_seconds`, `proof_hash`).
    - Missing tuple: `RUNTIME_PROOF_MISSING`
    - Invalid schema/hash/linkage: `RUNTIME_PROOF_INVALID`
    - Reused `runtime_proof_id`: `RUNTIME_PROOF_REUSED`
    - Expired proof TTL / stale proof: `RUNTIME_PROOF_STALE`
    - Ambiguous proof-to-checkpoint linkage: `RUNTIME_PROOF_AMBIGUOUS_LINK`
    - Remediation: rerun affected phase in fresh subagent context, write new
      strict-proof tuple + checkpoint evidence, then continue.
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

## Deterministic artifact ordering guard (US-0058 / DEC-0040)

- When `/auto` coordinates phases that write mutable artifacts, each phase must
  follow `docs/engineering/artifact-ordering-policy.md`.
- Ordering policies are mandatory:
  - `state.md`: append-bottom
  - `backlog.md` / `acceptance.md`: sorted-canonical
  - release/handoff surfaces: policy-specific (prepend/append) as documented.
- If a required placement anchor is missing or ambiguous, fail closed with
  `ARTIFACT_ORDERING_ANCHOR_AMBIGUOUS` and do not continue.
