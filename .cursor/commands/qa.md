---
description: "its-magic QA: test plan, findings, verify fixes."
---

# /qa

## Subagents
- qa

## Execution model
- Run `/qa` in a fresh QA subagent context.
- After writing outputs, stop and hand off to `/execute` (if issues) or
  `/verify-work` (if clear) in a new subagent/chat.
- Each QA pass in the implementation loop must be a new QA subagent.

## Inputs
- `handoffs/dev_to_qa.md`
- `sprints/S0001/summary.md`

## Outputs (artifacts)
- `sprints/S0001/qa-findings.md`
- `handoffs/qa_to_dev.md` (if issues)
- `docs/engineering/state.md`

## Stop conditions
- Critical defects require decision
- Missing test plan coverage

## Steps
0. If `SECURITY_REVIEW=1`, verify `docs/engineering/security-review.md` exists
   and has no unresolved `critical` findings before proceeding. If unresolved
   critical findings exist, stop at a decision gate.
1. Define a test plan and run verification using the runbook commands
   (`TEST_COMMAND`, `LINT_COMMAND`, `TYPECHECK_COMMAND` in `docs/engineering/runbook.md`).
   - `TEST_COMMAND` is mandatory baseline evidence for push eligibility.
   - Optional checks run only when configured and should be reported as
     `pass|fail|skipped` deterministically.
2. Record findings and severity.
   - Explicitly classify blockers that must prevent auto-push:
     unresolved blocking QA findings and unresolved critical issues.
3. Update state and handoff to dev if needed.
   - For sync-policy evidence, include deterministic `reason_code` guidance:
     - `PRE_QA_AUTOPUSH_FORBIDDEN` (feature work before QA completion)
     - `BLOCKING_QA_FINDINGS` (open blockers/criticals)
     - `SYNC_PUSHED` (eligible + checks passed + branch safe)
4. If `AUTO_IMPLEMENTATION_LOOP=1` and blocking issues exist, handoff to dev and
   return to `/execute` automatically (bounded by `AUTO_LOOP_MAX_CYCLES`).
5. Follow with `/verify-work` for user acceptance when blocking issues are closed.
6. If `AUTO_PAUSE_REQUEST=1` at safe boundary, run `/pause` before next phase.
7. Before pushing, suggest running `scripts/validate-and-push` to catch failures
   locally before they reach CI. If CI fails, the auto-fix job in
   `.github/workflows/ci.yml` attempts automatic lint/format fixes and retries.

