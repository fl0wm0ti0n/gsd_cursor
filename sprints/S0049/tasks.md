# Sprint S0049 Tasks

- Story: `US-0070`
- Sprint: `S0049`

| Task | Status | Description | AC |
|---|---|---|---|
| T-001 | done | Encode canonical scratchpad phase-selection contract (`AUTO_PHASE_PLAN`, `AUTO_PHASE_EXCLUDE`, `AUTO_PHASE_INCLUDE`, `AUTO_PHASE_PROFILE`) with exactly-one active mode, conflict fail-closed (`PHASE_POLICY_CONFLICT`), and precedence per `DEC-0052` in `/auto` + scratchpad examples (active + template) | AC-1 |
| T-002 | done | Implement deterministic plan materialization: expand policy mode to candidate ordered canonical phase list, apply non-skippable reinstatement, intersect `start-from` when present, and write selected/skipped phases + reasons to continuation breadcrumbs **before** first phase spawn | AC-2 |
| T-003 | done | Fail closed on unknown/invalid phase identifiers, empty include result, unknown profile, and related parse errors with deterministic diagnostics and reason codes (no silent ignore or partial schedule) | AC-3 |
| T-004 | done | Enforce default non-skippable phase set (safety gates + evidence-chain integrity per `DEC-0052`); record reinstatements in breadcrumbs (`non_skippable_gate`, etc.); no silent bypass of mandatory gates in default profile | AC-4 |
| T-005 | done | Document and implement deterministic `start-from=<phase>` intersection with resolved plan; empty intersection stops with listing of resolved plan vs requested anchor | AC-5 |
| T-006 | done | Align backlog-drain, bulk execute, and team-scope enforcement paths with phase-policy reload + plan recompute; preserve bounded stop semantics and deterministic block/skip reason codes | AC-6 |
| T-007 | done | Ensure resume, `resume_brief`, and state-fallback entry paths persist phase-policy inputs in breadcrumbs and recompute the same effective plan class (no silent reintroduction of skipped phases) | AC-7 |
| T-008 | done | Maintain active/template parity for `/auto`, scratchpad + `scratchpad.local.example`, runbook, and README for all new keys, profiles sketch, and failure taxonomy | AC-8 |
| T-009 | done | Add regression coverage: default full plan parity with pre-US-0070 behavior, selective skip examples (`research`, `sprint-plan`) with reinstatement checks, invalid config fail-fast paths, and resume/plan consistency | AC-9 |
| T-010 | done | Emit operator-visible status at phase boundaries listing selected phases, skipped phases with reason codes (`policy_exclude`, `non_skippable_gate`, `default_full_plan`, fail-fast codes), aligned with breadcrumb contract | AC-10 |

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
