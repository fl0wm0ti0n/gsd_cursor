---
description: "GSD QA: test plan, findings, verify fixes."
---

# /gsd-qa

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
1. Define a test plan and run verification.
2. Record findings and severity.
3. Update state and handoff to dev if needed.
4. Follow with `/gsd-verify-work` for user acceptance.

