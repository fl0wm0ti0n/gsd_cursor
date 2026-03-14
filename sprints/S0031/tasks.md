# Sprint S0031 Tasks

- Story: `US-0052`
- Sprint: `S0031`

| Task | Status | Description | AC |
|---|---|---|---|
| T-001 | done | Define explicit bootstrap control contract (flag/config/help) with default-off behavior | AC-1, AC-6 |
| T-002 | done | Implement deterministic freshness detection over canonical `US-`, `DEC-`, and `R-` artifact surfaces | AC-2, AC-4 |
| T-003 | done | Implement bootstrap-start behavior for eligible fresh repos to begin at `US-0001`/`DEC-0001`/`R-0001` | AC-2 |
| T-004 | done | Preserve non-fresh highest-existing-ID continuation and enforce no historical ID rewrite | AC-3 |
| T-005 | done | Add deterministic diagnostics when bootstrap is requested but freshness criteria fail | AC-4, AC-6 |
| T-006 | done | Harden collision-safety rules across story/decision/research ID generation in normal sequential flow | AC-5 |
| T-007 | done | Update operator guidance in README/runbook/command help for bootstrap behavior, constraints, and caveats | AC-6 |
| T-008 | done | Add regression tests for fresh-repo bootstrap-enabled and fresh-repo bootstrap-disabled paths | AC-7 |
| T-009 | done | Add regression tests for non-fresh continuation and mixed-artifact edge cases | AC-7 |
| T-010 | done | Align active and `template/` contracts/docs/tests for namespace-bootstrap behavior parity | AC-8 |
