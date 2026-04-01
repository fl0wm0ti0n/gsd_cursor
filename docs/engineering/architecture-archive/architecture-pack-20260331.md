# Architecture archive pack (2026-03-31)

- Rollover trigger: `ARCH_HOT_MAX_LINES=3500, ARCH_HOT_MAX_STORY_SECTIONS=120`
- Source: `docs/engineering/architecture.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 34
- First archived heading: `# US-0037: Mid-Process `/auto` Continuation with Deterministic Resume Point`
- Last archived heading: `# US-0037: Mid-Process `/auto` Continuation with Deterministic Resume Point`
- Verification tuple (mandatory):
  - archived_body_lines=187
  - preamble_lines=10
  - retained_body_lines=3341

---

# US-0037: Mid-Process `/auto` Continuation with Deterministic Resume Point

## Overview

US-0037 adds deterministic continuation semantics for `/auto` so teams can
restart from mid-process with one command and continue remaining phases without
manual phase triggers. The design is workflow-level orchestration only. It does
not change phase deliverables, decision gates, or runtime product behavior.

## Assumption challenge and alternatives

### Option A: Keep implicit behavior only

Pros:
- No command contract changes.
- Lowest immediate implementation effort.

Cons:
- Resume behavior stays inference-heavy and non-deterministic.
- Ambiguous source resolution can silently choose the wrong phase.
- Does not satisfy ACs for explicit `start-from`, fail-fast conflicts, and
  inspectable breadcrumbs.

### Option B: Resume-only continuation (no `/auto start-from`)

Pros:
- Simpler than full unification.
- Reuses `resume_brief.md` as primary source.

Cons:
- No explicit operator override for urgent/manual recovery cases.
- Still weak when resume brief is stale/missing and state fallback is needed.
- Splits semantics across `/resume` and `/auto` instead of one deterministic
  control model.

### Option C: Unified deterministic model (chosen)

Pros:
- Explicit `/auto start-from=<phase>` override for intentional control.
- Deterministic source precedence when no override.
- Fail-fast on ambiguity/staleness/conflict rather than guessing.
- One-command continuation through remaining phases with existing stop rules.

Cons:
- Slightly more command/rule documentation work.
- Requires explicit conflict/error contract and breadcrumb schema.

## Minimal architecture

### 1) Canonical phase IDs and validation

Accepted canonical IDs for `start-from`:
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

Validation policy:
- Unknown/non-canonical phase -> fail fast.
- Alias forms are not accepted in v1 (`sprint_plan`, `verifywork`, etc.) to
  keep behavior deterministic.

### 2) Deterministic resume-source precedence

When `/auto` is invoked, resolve start phase in strict order:

1. **Explicit override**: command argument `start-from=<phase>`.
2. **Resume brief source**: `handoffs/resume_brief.md` intended resume phase.
3. **State fallback source**: infer next phase from `docs/engineering/state.md`.
4. **Fail-fast**: if unresolved, ambiguous, conflicting, or stale.

Deterministic rule:
- Once a higher-priority source resolves validly, lower sources are ignored for
  phase selection (but can still be used for consistency checks and warnings).

### 3) Conflict and staleness policy

Resolver outcomes:
- `resolved`: exactly one valid phase source selected by precedence.
- `conflict`: sources disagree and no explicit override exists.
- `stale`: source exists but points to an invalid/outdated context.
- `missing`: required data not present.
- `ambiguous`: multiple possible phases inferred from same source.

Policy:
- If explicit `start-from` is valid, proceed and record that it overrides other
  sources.
- If no explicit override and `resume_brief` conflicts with `state` inference:
  fail fast with actionable remediation.
- If `resume_brief` exists but is stale/unparseable, do not silently skip to
  state; fail fast and request cleanup or explicit override.
- Use `state` fallback only when `resume_brief` is genuinely absent.
- If state inference is ambiguous/unrecoverable, fail fast.

### 4) Error messaging contract (fail-fast)

All resolver failures must return a structured message contract:

`[AUTO_RESUME_ERROR] <code>: <summary>. Source=<source>. Fix: <action>.`

Required codes:
- `INVALID_START_FROM`
- `RESUME_BRIEF_MISSING`
- `RESUME_BRIEF_STALE`
- `RESUME_BRIEF_UNPARSEABLE`
- `RESUME_STATE_CONFLICT`
- `STATE_PHASE_AMBIGUOUS`
- `STATE_PHASE_UNRECOVERABLE`

Examples:
- `[AUTO_RESUME_ERROR] INVALID_START_FROM: "planverify" is not a canonical phase. Source=argument. Fix: use one of [intake..refresh-context].`
- `[AUTO_RESUME_ERROR] RESUME_STATE_CONFLICT: resume_brief=qa, state_inferred=verify-work. Source=resolver. Fix: run /resume to reconcile artifacts or rerun /auto start-from=<phase>.`

### 5) State fallback inference contract

`docs/engineering/state.md` fallback is intentionally conservative:
- Infer from latest explicit boundary/checkpoint statements that indicate
  "ready for <phase>" or "paused at <phase>".
- If multiple candidate phases are present in latest state slice, mark
  ambiguous and fail.
- If no trustworthy boundary phrase exists, mark unrecoverable and fail.

This keeps inference deterministic and avoids hidden heuristics.

### 6) One-command continuation flow (remaining phases only)

After phase resolution, `/auto` executes remaining phases in canonical order,
starting at resolved phase, preserving existing behavior:
- Fresh subagent per phase.
- Existing execute/QA loop behavior when `AUTO_IMPLEMENTATION_LOOP=1`.
- Existing optional security review steps when `SECURITY_REVIEW=1`.
- Existing stop conditions remain unchanged:
  - decision gate
  - missing critical input
  - pause request (`AUTO_PAUSE_REQUEST=1` at safe boundary)
  - loop max cycles reached

No gate bypass is allowed in continuation mode.

### 7) Observability and breadcrumb contract

Continuation must write deterministic breadcrumbs to artifacts so behavior is
auditable.

Minimum breadcrumb fields:
- `invocation_mode` (`auto`)
- `requested_start_from` (value or `none`)
- `resolved_start_phase`
- `resolution_source` (`argument|resume_brief|state_fallback`)
- `resolution_status` (`resolved|fail-fast`)
- `stop_reason` (`completed|decision_gate|missing_input|pause_request|loop_max`)
- `stop_phase`
- `timestamp`

Artifact update targets:
- `docs/engineering/state.md`: append a concise continuation checkpoint summary.
- `handoffs/resume_brief.md` (when stopped before completion): update intended
  resume phase plus stop reason and last completed phase.

### 8) Backward compatibility and safe defaults

- Existing manual workflows remain unchanged.
- `/resume` continues to work for context loading and status reporting.
- `/auto` gains explicit deterministic continuation behavior only when invoked.
- If no explicit `start-from` is provided, legacy users still get automatic
  continuation — now with deterministic source policy and fail-fast safety.

## Sprint-plan readiness (decomposition-ready)

Implementation tasks should split into:
1. Define parser/validator for `start-from` canonical phase IDs.
2. Implement precedence resolver with strict conflict/staleness outcomes.
3. Implement fail-fast error message contract and user remediation text.
4. Implement conservative `state.md` inference helper with ambiguity handling.
5. Wire continuation flow to existing stop conditions (no behavior bypass).
6. Add breadcrumb writing contract to `state.md` and `resume_brief.md`.
7. Align `/auto`, `/resume`, `/pause` command guidance and template parity.

---

