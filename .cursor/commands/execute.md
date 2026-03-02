---
description: "its-magic execute: implement tasks with artifacts and state updates."
---

# /execute

## Subagents
- dev

## Execution model
- Run `/execute` in a fresh Dev subagent context.
- After writing outputs, stop and hand off to `/qa` in a new subagent/chat.
- When fixing QA findings, each new `/execute` run is a new Dev subagent.

## Isolation evidence write requirement (US-0048 / DEC-0029)

At the end of `/execute`, append an isolation evidence entry to
`docs/engineering/state.md`:

- `phase_id=execute`
- `role=dev`
- `fresh_context_marker=<new marker for this subagent>`
- `timestamp=<ISO UTC>`
- `evidence_ref=<primary output ref>` (recommended: `handoffs/dev_to_qa.md` and the target sprint `sprints/Sxxxx/summary.md`)

In an execute↔QA implementation loop (`AUTO_IMPLEMENTATION_LOOP=1`), each new
`/execute` cycle must have a new `fresh_context_marker` (marker reuse is treated
as stale isolation evidence).

## Inputs
- `sprints/S0001/tasks.md`
- `handoffs/tl_to_dev.md`
- Optional: `handoffs/qa_to_dev.md` when fixing QA findings
- Optional (remote-enabled mode only): `.cursor/remote.json`

## Outputs (artifacts)
- Code changes
- `sprints/S0001/summary.md`
- `docs/engineering/state.md`
- `handoffs/dev_to_qa.md` (if ready)
- Optional (when enabled):
  - `docs/engineering/compatibility-signals.md`
  - `docs/engineering/compatibility-report.md`

## Stop conditions
- Decision gate triggered
- Missing task definition or unclear scope

Release gate semantics (US-0039): mandatory gates (check-in test, QA, UAT) and no-bypass/override contract are enforced at `/release`; see `.cursor/commands/release.md` and `.cursor/commands/qa.md`.

## Canonical status contract (US-0045)

- Story status authority is `docs/product/backlog.md`.
- `docs/product/acceptance.md` and `docs/engineering/state.md` are derived and
  must not be treated as canonical readiness sources when contradictory.
- `/execute` must not start/continue implementation solely based on
  non-canonical status evidence.

## Steps
1. Implement one task at a time.
2. Update summary and engineering state.
3. Handoff to QA when ready.
4. If `AUTO_INSTALL_DEPS=1` in `.cursor/scratchpad.md`, install dependencies
   via the appropriate package manager without prompting.
5. Mode-aware remote-config validation (DEC-0016):
   - If `REMOTE_EXECUTION=0`, skip all remote-config checks (zero overhead).
   - If `REMOTE_EXECUTION=1`, fail fast on `.cursor/remote.json` contract errors
     before remote execution is attempted.
   - Required root fields: `version` (integer), `defaultTarget` (string),
     `targets` (array).
   - Required target fields: `id` (string), `type` (`docker|ssh|vm`),
     `enabled` (boolean), `host` (string), `port` (integer 1..65535),
     `workspaceRoot` (string).
   - Optional target field: `auth` object with `mode` (`none|env`).
   - If `auth.mode=env`, sensitive values must be env-var references only
     (for example `tokenEnv`, `passwordEnv`, `privateKeyPathEnv`).
   - `defaultTarget` must match an existing enabled target `id`.
   - Secret-like inline literals are forbidden in committed config.
6. Remote validation errors must use actionable fail-fast format:
   `[REMOTE_CONFIG_ERROR] <path>: expected <rule>, got <actual>. Fix: <hint>.`
   - Missing file: `.cursor/remote.json` not found.
   - Malformed JSON: parse failure with syntax location.
   - Invalid enum/type/value: include field path and allowed/expected values.
   - Security violation: inline secret-like value detected.
   Use remediation hints that either fix config or disable remote mode
   (`REMOTE_EXECUTION=0`) when remote execution is not needed.
7. If `RUN_TESTS_ON_EDIT=1`, run configured tests after meaningful edits.
8. If `LOOP_UNTIL_GREEN=1`, fix failing tests in small iterations until green,
   or stop and document blockers in `docs/engineering/state.md`.
9. If `AUTO_PAUSE_REQUEST=1` and boundary rules permit, checkpoint via `/pause`.
10. Sync policy evaluation contract (US-0038):
   - Evaluate sync eligibility only at completed phase boundaries.
   - Do not evaluate on partial/intra-phase edits (deterministic boundary-only behavior).
   - If policy mode is `disabled|manual`, keep near-zero overhead and do not
     auto-trigger push behavior.
11. Team-scope guardrails for bulk execute mode (US-0047 / DEC-0024):
   - When `TEAM_MODE=1` and `AUTO_TEAM_SCOPE_ENFORCE=1`, only execute tasks that
     match current member scope (`TEAM_MEMBER`, `ACTIVE_TASK_IDS`).
   - For out-of-scope tasks, do not write code or artifacts; emit deterministic
     reason code and follow configured stop/skip policy.
12. When ready to push, suggest `scripts/validate-and-push` to run the full
    quality chain locally before CI.
13. Optional compatibility observability execution contract (US-0034):
   - If `CROSS_REPO_OBSERVABILITY=0`, skip all compatibility checks (zero
     required overhead).
   - If `CROSS_REPO_OBSERVABILITY=1`, append/update compatibility signals and
     findings in canonical artifacts (`compatibility-signals.md`,
     `compatibility-report.md`) including severity, impacted modules,
     evidence refs, and recommended actions.
14. Optional component-scoped execution guardrails (US-0035):
   - If `COMPONENT_SCOPE_MODE=0`, add zero required scope overhead.
   - If `COMPONENT_SCOPE_MODE=1`, enforce scope-first execution:
     - do not intentionally modify out-of-scope components unless escalation is
       explicitly approved and recorded,
     - any detected unapproved out-of-scope impact must be flagged for decision
       gate handling before release.
15. Optional spec-pack (US-0031):
   - If `SPEC_PACK_MODE=0`, add no required spec-pack steps (zero overhead).
   - If `SPEC_PACK_MODE=1`, update Technical Specification artifact for target
     story at canonical path when implementation details change; see runbook
     for required sections and ownership.
16. Optional user-guide (US-0032):
   - If `USER_GUIDE_MODE=0`, add no required user-guide steps or blocking checks (zero overhead).
   - If `USER_GUIDE_MODE=1`, create or update user guide at
     `docs/user-guides/US-xxxx.md` for target story; see runbook for minimum schema.

