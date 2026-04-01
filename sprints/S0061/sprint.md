# Sprint S0061

- Story: `US-0081`
- Goal: **First-intake full-plan coverage gate** - implement the `DEC-0064` contract so first/new/broad intake persists only when a normalized `plan_area_inventory` is fully accounted for via `plan_area_id -> story_id[] | deferred_ref`, with deterministic fail-closed diagnostics, active/`template/` parity, and regression coverage for pass/fail/defer flows.
- Status: **Execute complete - ready for `/qa`** (`orchestrator_run_id=auto-20260331-01`; `executed_at=2026-03-31T14:20:00Z`)

## Scope

- **AC-1** - Require explicit plan-area inventory derivation before first/new/broad intake persistence.
- **AC-2** - Block persistence when any major plan area is unmapped to story IDs or explicit deferred rationale.
- **AC-3** - Emit complete story-map output that preserves full-plan coverage while allowing phased sequencing.
- **AC-4** - Keep decomposition vertical-slice/workflow oriented; prevent technical-layer-only splits by default.
- **AC-5** - Enforce complete-plan gate in low-touch mode; no bypass path.
- **AC-6** - Persist machine-verifiable coverage-map fields (`plan_area_inventory`, `plan_area_coverage`, `coverage_complete`).
- **AC-7** - Emit deterministic fail codes (`INTAKE_PLAN_COVERAGE_MISSING`) under `INTAKE_PERSISTENCE_BLOCKED`.
- **AC-8** - Update `/ask` and runbook guidance so broad first intake requires complete mapping or justified defer.
- **AC-9** - Preserve active/`template/` parity for intake command, PO guidance, validators, and fixtures.
- **AC-10** - Add regression tests for full-coverage pass, justified defer pass, and missing-mapping block.

## Governance

- `decisions/DEC-0064.md`
- `docs/engineering/architecture.md` `# US-0081`
- `docs/engineering/research.md` `R-0059`
- Related: `US-0051`, `US-0068`, `US-0078`, `US-0045`
