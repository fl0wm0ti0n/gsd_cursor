# Sprint S0062 Tasks

- Story: `US-0082`
- Sprint: `S0062`
- Governance: `DEC-0065`; `architecture.md` `# US-0082`; `R-0060`; `US-0045`

| Task | Status | Description | AC |
|---|---|---|---|
| T-001 | done | Wire primary lifecycle guarantee at **`/architecture`** completion (tech-lead path): invoke map materialization or deterministic block before **`/sprint-plan`** handoff; align with **`DEC-0065`** §primary gate | AC-1 |
| T-002 | done | Document auto/bootstrap vs explicit **`/map-codebase`** in command surfaces, runbook, and cross-links (**AC-2**) | AC-2 |
| T-003 | done | Implement idempotent map generation/refresh (stable ordering; avoid no-op file churn) | AC-3 |
| T-004 | done | Enforce artifact ownership / write-surface policy for non-intake triggers (same surfaces as **`/map-codebase`**; preserve **`state.md`** append-only discipline) | AC-4 |
| T-005 | done | Emit deterministic **`CODEBASE_MAP_*`** diagnostics (skip/block reasons + remediation) per architecture fail-code vocabulary | AC-5 |
| T-006 | done | Update **`docs/engineering/runbook.md`** and **`.cursor/commands/ask.md`** (active + template) so operators/agents know responsibility locus | AC-6 |
| T-007 | done | Maintain active/`template/` parity for commands, rules, docs, and tests touched by map bootstrap behavior | AC-7 |
| T-008 | done | Add regression coverage for fresh-repo bootstrap, idempotent rerun, and failure-path diagnostics | AC-8 |
| T-009 | done | Ensure non-destructive / compatible behavior when `codebase-map.md` already exists (no silent data loss) | AC-9 |
| T-010 | done | Close/reclassify **`BUG-0002`** as expectation mismatch with backlog/docs traceability to **`US-0082`** | AC-10 |

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
