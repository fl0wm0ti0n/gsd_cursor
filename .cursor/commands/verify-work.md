---
description: "its-magic verify work: guided user acceptance testing."
---

# /verify-work

## Subagents
- qa

## Execution model
- Run `/verify-work` in a fresh QA subagent context.
- After writing outputs, stop and hand off to `/release` (or back to `/execute`
  if failures require fixes) in a new subagent/chat.

## Inputs
- `docs/product/acceptance.md`
- `sprints/S0001/summary.md`

## Outputs (artifacts)
- `sprints/S0001/uat.json`
- `sprints/S0001/uat.md`
- `docs/engineering/state.md`

## Stop conditions
- Decision gate triggered

## UAT lifecycle rules (DEC-0009)

UAT artifacts transition from **placeholder** (created during `/sprint-plan`) to
**populated** (filled during `/verify-work`) to **verified** (confirmed during
`/release`). QA owns the placeholder → populated transition.

### Minimum UAT content before sprint completion
- `uat.json`: `steps` array is non-empty. Each step has a `description` and
  `result` (`pass` or `fail`). `passed` + `failed` = total steps count.
- `uat.md`: every UAT step is listed with its result. A results summary appears
  at the bottom linking back to story acceptance criteria.
- A sprint **cannot** be marked complete while UAT artifacts remain in
  placeholder state.

## Steps
1. Convert acceptance criteria into testable UAT steps. Derive steps directly from the story's acceptance criteria in `docs/product/acceptance.md`. Each AC should map to at least one UAT step.
2. Populate UAT artifacts: write derived steps into `uat.json` (with description and result per step, accurate pass/fail counts) and `uat.md` (step list with results, summary section). Ensure UAT artifacts are in **populated** state per DEC-0009 — not placeholder.
3. Record results and failures.
4. Update state with pass/fail summary.
5. Update traceability index in `docs/engineering/state.md`: for each story verified in this sprint, set Status to `PASS` or `FAIL` and fill the Evidence column with artifact references (e.g., `S0001/uat.json`, `S0001/summary.md`). Use the DEC-0010 format.
6. Pre-handoff traceability check: confirm no OPEN or DONE story in the current sprint lacks a traceability index entry. If a gap is found, add the missing row before proceeding with the handoff.
7. If `AUTO_IMPLEMENTATION_LOOP=1` and UAT fails, write a handoff to dev/QA and
   continue the fix loop within `AUTO_LOOP_MAX_CYCLES`.
