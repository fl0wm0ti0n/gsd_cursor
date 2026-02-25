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

## Stop conditions
- Decision gate triggered
- Missing task definition or unclear scope

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
11. When ready to push, suggest `scripts/validate-and-push` to run the full
    quality chain locally before CI.

