---
description: "its-magic QA: test plan, findings, verify fixes."
---

# /qa

## Subagents
- qa

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
1. Define a test plan and run verification using the runbook commands
   (`TEST_COMMAND`, `LINT_COMMAND`, `TYPECHECK_COMMAND` in `docs/engineering/runbook.md`).
2. Record findings and severity.
3. Update state and handoff to dev if needed.
4. If `AUTO_IMPLEMENTATION_LOOP=1` and blocking issues exist, handoff to dev and
   return to `/execute` automatically (bounded by `AUTO_LOOP_MAX_CYCLES`).
5. Follow with `/verify-work` for user acceptance when blocking issues are closed.
6. If `AUTO_PAUSE_REQUEST=1` at safe boundary, run `/pause` before next phase.
7. Before pushing, suggest running `scripts/validate-and-push` to catch failures
   locally before they reach CI. If CI fails, the auto-fix job in
   `.github/workflows/ci.yml` attempts automatic lint/format fixes and retries.

