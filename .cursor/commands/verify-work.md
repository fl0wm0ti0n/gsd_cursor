---
description: "its-magic verify work: guided user acceptance testing."
---

# /verify-work

## Subagents
- qa

## Inputs
- `docs/product/acceptance.md`
- `sprints/S0001/summary.md`

## Outputs (artifacts)
- `sprints/S0001/uat.json`
- `sprints/S0001/uat.md`
- `docs/engineering/state.md`

## Stop conditions
- Decision gate triggered

## Steps
1. Convert acceptance criteria into testable UAT steps.
2. Record results and failures.
3. Update state with pass/fail summary.
