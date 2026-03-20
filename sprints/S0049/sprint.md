# Sprint S0049

- Story: `US-0070`
- Goal: implement scratchpad-controlled `/auto` phase plan resolution (single active policy mode), deterministic breadcrumbs before spawn, non-skippable gate reinstatement, `start-from` intersection, continuation parity with backlog-drain/bulk/team modes, and operator-visible diagnostics — aligned with `DEC-0052`, `R-0049`, and `US-0069` / `DEC-0051` (no role substitution when phases are omitted).
- Status: released (`US-0070`; canonical notes `handoffs/releases/S0049-release-notes.md`)

## Scope

- Canonical scratchpad selectors: `AUTO_PHASE_PLAN`, `AUTO_PHASE_EXCLUDE`, `AUTO_PHASE_INCLUDE`, `AUTO_PHASE_PROFILE` with exactly-one active mode and `PHASE_POLICY_CONFLICT` on merge conflict.
- Materialize resolved ordered phase list before first spawn; record selected phases, skipped phases + reasons, and policy metadata in continuation breadcrumbs.
- Validate phase tokens; unknown IDs, empty include, unknown profile → deterministic fail-closed diagnostics.
- Default non-skippable reinstatement (`qa`, `verify-work`, `release`, and evidence-chain prerequisites per `DEC-0052`); named high-risk profiles only with documented ack + registry.
- `start-from=<phase>` intersects with resolved plan; empty intersection fails with resolved plan vs anchor.
- Resume and multi-mode orchestration (`AUTO_BACKLOG_DRAIN`, `AUTO_EXECUTE_BULK`, `TEAM_MODE`) reload merged scratchpad policy and recompute plan; no silent revival of omitted phases.
- Active/template parity for `/auto`, scratchpad examples, runbook, README.
- Regression coverage for default full plan, selective skips (`research`, `sprint-plan`), invalid policy fail-fast, resume consistency.
- Boundary status surfaces enumerate selected/skipped phases and reason codes.
