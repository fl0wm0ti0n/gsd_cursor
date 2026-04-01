# Sprint S0061 Tasks

- Story: `US-0081`
- Sprint: `S0061`
- Governance: `DEC-0064`; `architecture.md` `# US-0081`; `R-0059`; `US-0045`

| Task | Status | Description | AC |
|---|---|---|---|
| T-001 | done | Add deterministic first/new/broad trigger flow that always derives normalized `plan_area_inventory` before any intake persistence path | AC-1 |
| T-002 | done | Enforce total coverage invariant: every major `plan_area_id` must map to `story_id[]` or `deferred_ref`; block persistence on gaps | AC-2 |
| T-003 | done | Implement canonical story-map output that renders complete coverage while allowing phased sequencing of resulting stories | AC-3 |
| T-004 | done | Apply decomposition guardrails so mapping logic rejects technical-layer-only split proposals unless explicitly justified by policy | AC-4 |
| T-005 | done | Wire the same complete-plan gate into low-touch intake execution path; remove bypass behavior | AC-5 |
| T-006 | done | Persist and validate machine-readable coverage fields (`plan_area_inventory`, `plan_area_coverage`, `coverage_complete`) in intake evidence and storage | AC-6 |
| T-007 | done | Emit deterministic diagnostics for coverage gaps using `INTAKE_PERSISTENCE_BLOCKED` + `INTAKE_PLAN_COVERAGE_MISSING` with remediation text | AC-7 |
| T-008 | done | Update `/ask` guidance and `docs/engineering/runbook.md` with complete-coverage policy and deferred-rationale expectations | AC-8 |
| T-009 | done | Apply active/`template/` parity updates for command/rules/docs/validators and add parity checks where required | AC-9 |
| T-010 | done | Add regression suite for coverage pass, justified defer pass, and missing-map fail-closed behavior across guided and low-touch modes | AC-10 |

## Deterministic AC-to-task mapping

- AC-1 -> T-001
- AC-2 -> T-002
- AC-3 -> T-003
- AC-4 -> T-004
- AC-5 -> T-005
- AC-6 -> T-006
- AC-7 -> T-007
- AC-8 -> T-008
- AC-9 -> T-009
- AC-10 -> T-010
