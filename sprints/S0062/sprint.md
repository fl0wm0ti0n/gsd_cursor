# Sprint S0062

- Story: `US-0082`
- Goal: **Agent-driven codebase map bootstrap** — implement **`DEC-0065`** so `docs/engineering/codebase-map.md` is guaranteed at the **`/architecture`** lifecycle boundary (with optional policy-gated **`/refresh-context`** refresh), **`/map-codebase`** remains explicit/manual, idempotent generation respects ownership, **`CODEBASE_MAP_*`** diagnostics + operator guidance ship, active/`template/` parity holds, regressions cover fresh/rerun/failure paths, existing maps stay compatible, and **`BUG-0002`** is closed as expectation mismatch with traceability.
- Status: **Verify-work complete — ready for `/release`** (`orchestrator_run_id=auto-20260331-02`; `planned_at=2026-03-31T20:05:00Z`; `plan_verified_at=2026-03-31T20:20:00Z`; `executed_at=2026-03-31T20:40:00Z`; `verified_at=2026-03-31T21:20:00Z`)

## Scope

- **AC-1** — Deterministic lifecycle point(s) where TL/Dev path ensures `docs/engineering/codebase-map.md` exists in fresh repos (primary: **`/architecture`** exit per **`DEC-0065`**).
- **AC-2** — Keep **`/map-codebase`** as explicit/manual command; document when auto/bootstrap runs vs operator-invoked runs.
- **AC-3** — Idempotent map refresh (reruns safe; no unstable churn).
- **AC-4** — Respect artifact ownership policy when generation is triggered outside intake.
- **AC-5** — Deterministic diagnostics when map generation is skipped/blocked (`CODEBASE_MAP_*` family + remediation).
- **AC-6** — Runbook and **`/ask`** guidance naming where map responsibility lives.
- **AC-7** — Active and `template/` parity for commands/rules/docs/tests implementing this behavior.
- **AC-8** — Regression tests: fresh bootstrap, rerun, failure-path diagnostics.
- **AC-9** — Backward compatibility for repos with pre-existing map files.
- **AC-10** — Story owns closure/reclassification of **`BUG-0002`** (no duplicate tracking).

## Governance

- `decisions/DEC-0065.md`
- `docs/engineering/architecture.md` `# US-0082`
- `docs/engineering/research.md` `R-0060`
- Related: `US-0001`, `BUG-0002`, `DEC-0052`, `US-0045`
