# Tasks — Sprint S0005

## US-0025: Backlog-to-Sprint Traceability Contract

### T-001: Add traceability index to state.md with historical backfill
- Story: US-0025
- Status: pending
- Files: `docs/engineering/state.md`
- Description: Add a `## Traceability Index` table section per DEC-0010 format
  (Story | Sprint | Tasks | Status | Evidence). Backfill rows for all historical
  sprints (S0001 through S0004) by reviewing each sprint's tasks.md and
  summary.md to reconstruct accurate story-sprint-task mappings.
- AC covered: AC-1, AC-2, AC-3

### T-002: Add traceability index maintenance step to sprint-plan command (active + template)
- Story: US-0025
- Status: pending
- Files: `.cursor/commands/sprint-plan.md`, `template/.cursor/commands/sprint-plan.md`
- Description: Add a step to `/sprint-plan` requiring the Tech Lead to create
  traceability index rows in `state.md` when assigning stories to a sprint.
  New rows use status=PLANNED with empty evidence. Reference DEC-0010 format.
- AC covered: AC-4

### T-003: Add traceability verification step to verify-work command (active + template)
- Story: US-0025
- Status: pending
- Files: `.cursor/commands/verify-work.md`, `template/.cursor/commands/verify-work.md`
- Description: Add a step to `/verify-work` requiring QA to update traceability
  index status (PASS/FAIL) and fill the evidence column with artifact references.
  Add a pre-handoff check: no OPEN/DONE story should lack a traceability entry.
- AC covered: AC-3, AC-5

## US-0027: UAT Artifact Lifecycle and Ownership

### T-004: Add UAT placeholder creation guidance to sprint-plan command (active + template)
- Story: US-0027
- Status: pending
- Files: `.cursor/commands/sprint-plan.md`, `template/.cursor/commands/sprint-plan.md`
- Description: Update `/sprint-plan` to require Tech Lead to create UAT
  placeholder files during planning. `uat.json`: sprint ID + empty steps array.
  `uat.md`: header + target stories and ACs listed, no results. Reference
  DEC-0009 lifecycle taxonomy (placeholder state at this phase).
- AC covered: AC-1, AC-2, AC-5

### T-005: Add UAT population and minimum content rules to verify-work command (active + template)
- Story: US-0027
- Status: pending
- Files: `.cursor/commands/verify-work.md`, `template/.cursor/commands/verify-work.md`
- Description: Update `/verify-work` to reference DEC-0009 lifecycle and minimum
  UAT content requirements. QA must derive UAT steps from acceptance criteria,
  record pass/fail results per step, and ensure `uat.json` has non-empty steps
  array with accurate counts. Sprint cannot be marked complete with placeholder
  UAT.
- AC covered: AC-2, AC-3, AC-4, AC-5

### T-006: Add UAT completeness as release readiness gate (active + template)
- Story: US-0027
- Status: pending
- Files: `.cursor/commands/release.md`, `template/.cursor/commands/release.md`
- Description: Add UAT verification as a release readiness check. Release agent
  confirms UAT artifacts are in populated state (not placeholder) and passing
  before release proceeds. Reference DEC-0009 verified state.
- AC covered: AC-4

## US-0026: Milestone Lifecycle Definition and Exit Criteria

### T-007: Add lifecycle state guidance to milestone-start command (active + template)
- Story: US-0026
- Status: pending
- Files: `.cursor/commands/milestone-start.md`, `template/.cursor/commands/milestone-start.md`
- Description: Add milestone lifecycle states (created → active → in-review →
  completed | cancelled) with entry/exit criteria per DEC-0009. Specify required
  fields for each state. Distinguish placeholder initialization (created state)
  from mandatory real content (active state onwards).
- AC covered: AC-1, AC-2, AC-3, AC-4

### T-008: Add exit criteria checklist to milestone-complete command (active + template)
- Story: US-0026
- Status: pending
- Files: `.cursor/commands/milestone-complete.md`, `template/.cursor/commands/milestone-complete.md`
- Description: Add exit criteria validation checklist: all sprints done, UAT
  passing, progress.md complete, summary.md written with outcomes and lessons.
  Add milestone readiness checks that must pass before completion is allowed.
- AC covered: AC-3, AC-5

### T-009: Add milestone activation check to sprint-plan command (active + template)
- Story: US-0026
- Status: pending
- Files: `.cursor/commands/sprint-plan.md`, `template/.cursor/commands/sprint-plan.md`
- Description: Add a check during sprint planning: if this is the first sprint
  under a milestone, transition milestone to active state. Ensure milestone
  name/goal/scope are populated (not placeholder) before sprint work begins.
- AC covered: AC-2, AC-3

## Implementation order and constraints
- Execute US-0025 tasks first (T-001 → T-003), then US-0027 (T-004 → T-006),
  then US-0026 (T-007 → T-009). This follows PO-recommended sequence.
- Within each story, execute tasks in order.
- Tasks T-002, T-004, and T-009 all modify `sprint-plan.md`. Apply changes
  incrementally — each task adds its section without disrupting prior additions.
- Tasks T-003 and T-005 both modify `verify-work.md`. Same incremental approach.
- Keep active and template files aligned in the same task where both are listed.
- Reference DEC-0009 lifecycle taxonomy in all guidance additions.
- Reference DEC-0010 format for the traceability index.
