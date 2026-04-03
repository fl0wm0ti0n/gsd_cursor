# Architecture archive pack (2026-04-03)

- Rollover trigger: `ARCH_HOT_MAX_LINES=3500, ARCH_HOT_MAX_STORY_SECTIONS=120`
- Source: `docs/engineering/architecture.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 34
- First archived heading: `# US-0038: Phase-Triggered Sync Policy with Guarded Auto-Push`
- Last archived heading: `# US-0038: Phase-Triggered Sync Policy with Guarded Auto-Push`
- Verification tuple (mandatory):
  - archived_body_lines=157
  - preamble_lines=10
  - retained_body_lines=3381

---

# US-0038: Phase-Triggered Sync Policy with Guarded Auto-Push

## Overview

US-0038 defines workflow-level sync policy semantics at phase boundaries. The
goal is deterministic and safe synchronization behavior with zero-overhead
defaults when automation is disabled. This architecture does not implement a
runtime git orchestrator; it defines policy contracts, gates, and artifacts.

## Assumption challenge and alternatives

### Option A: Always auto-push after every phase

Pros:
- Simple to explain.
- Frequent backups to remote.

Cons:
- Violates QA-first safety for feature work.
- High risk of pushing unstable/incomplete changes.
- Conflicts with teams that intentionally stay manual.

### Option B: Manual sync only

Pros:
- Maximum user control and least automation risk.
- Already compatible with existing workflow habits.

Cons:
- No deterministic cadence policy when teams want guarded automation.
- Misses requested phase/milestone trigger model.

### Option C: Policy-driven guarded auto-sync (chosen)

Pros:
- Supports disabled/manual/by-phase/by-milestone/custom modes.
- Enforces mandatory pre-push checks and QA-first restrictions.
- Preserves manual behavior and keeps default non-disruptive.

Cons:
- More policy/evidence fields to maintain in artifacts.

## Minimal architecture

### 1) Sync policy control model

Canonical policy object (stored in workflow artifacts/command context):
- `mode`: `disabled|manual|by_phase|by_milestone|custom_phase_list`
- `custom_phases[]`: canonical phase IDs (used only in `custom_phase_list`)
- `allow_auto_push`: `0|1` (default `0`)
- `auto_push_branch_allowlist[]`: explicit branch names/patterns allowed for
  auto-push
- `optional_checks_enabled`: inferred from runbook command presence

Mode semantics:
- `disabled`: no policy evaluation and no sync attempts.
- `manual`: only user-invoked sync; no auto-triggered sync.
- `by_phase`: evaluate eligibility on every phase-completion boundary.
- `by_milestone`: evaluate only at milestone completion boundary.
- `custom_phase_list`: evaluate only when completed phase matches configured
  list.

Default-safe posture:
- Default mode is non-auto (`manual` or `disabled`).
- If unset/invalid, fail closed to `manual`.

### 2) Guarded auto-push eligibility model

Policy evaluation runs only at phase completion boundaries. A sync attempt is
eligible only when all conditions are true:
1. Boundary trigger matches configured mode.
2. `allow_auto_push=1`.
3. QA-first guard passes for feature work:
   - before QA pass, auto-push is forbidden;
   - manual user-invoked sync is still allowed.
4. No unresolved blocking QA findings / critical unresolved issues.
5. Branch safety guard passes (see below).
6. Mandatory pre-push check chain passes.

If any condition fails, result is deterministic `no_push` with reason code.

### 3) Branch safety constraints

Auto-push branch policy:
- Deny auto-push to protected/default branches by default.
- Allow auto-push only on explicitly allowlisted branches.
- If branch is unknown/unclassified, fail closed (no auto-push).
- Manual push behavior remains unchanged and user-controlled.

### 4) Mandatory pre-push check chain

Pre-push chain order (deterministic):
1. `TEST_COMMAND` (mandatory baseline).
2. `LINT_COMMAND` (if configured and non-empty).
3. `TYPECHECK_COMMAND` (if configured and non-empty).

Rules:
- Missing/blank `TEST_COMMAND` blocks push.
- Test failure/timeout blocks push.
- Optional checks are skipped only when not configured.
- Optional check failures block push when configured.
- Result details must show which checks ran, skipped, passed, or failed.

This aligns with existing `validate-and-push` scripts where tests are already
required before push.

### 5) Observability and evidence artifacts

Canonical sync evidence destination:
- `docs/engineering/state.md` (session status + latest gate verdict)
- `handoffs/dev_to_qa.md` or phase handoff context as needed

Recommended structured entry fields per sync attempt:
- `sync_id` (`SYNC-xxxx`)
- `timestamp`
- `phase_boundary`
- `policy_mode`
- `trigger_source` (`manual|auto`)
- `branch`
- `checks` (`test`, `lint`, `typecheck` with `pass|fail|skipped`)
- `qa_status_snapshot`
- `push_decision` (`pushed|blocked|not_eligible`)
- `reason_code`
- `evidence_refs` (paths to runbook/sprint findings/test reports)

Reason code examples:
- `SYNC_DISABLED`
- `MANUAL_MODE_NO_AUTO`
- `PRE_QA_AUTOPUSH_FORBIDDEN`
- `BLOCKING_QA_FINDINGS`
- `BRANCH_NOT_ALLOWLISTED`
- `TEST_COMMAND_MISSING`
- `TEST_FAILED`
- `OPTIONAL_CHECK_FAILED`
- `SYNC_PUSHED`

### 6) Compatibility constraints

- Keep existing stop conditions and decision gate behavior unchanged.
- Preserve manual mode semantics; no forced push path is introduced.
- Keep optional runbook checks optional; only `TEST_COMMAND` is mandatory.
- Maintain active/template behavioral parity for command/rule/doc updates.

## Sprint-plan readiness (decomposition-ready)

Implementation should split into:
1. Define sync policy schema + defaults in workflow docs/command guidance.
2. Add phase-boundary eligibility evaluation contract and reason codes.
3. Define branch safety deny/allowlist policy for auto-push.
4. Align pre-push check contract with runbook commands and script semantics.
5. Add deterministic sync evidence format to state/handoff artifacts.
6. Add QA scenarios for pre-QA auto-push denial, check failures, and
   disabled/manual zero-overhead behavior.
7. Enforce active + `template/` parity for all touched behavior docs.

---

