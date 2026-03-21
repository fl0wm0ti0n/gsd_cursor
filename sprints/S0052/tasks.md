# Sprint S0052 Tasks

- Story: `US-0073`
- Sprint: `S0052`
- Governance: **`DEC-0055`** (Model B example-only + materialized baseline; merge precedence; parity; fail-closed diagnostics)

| Task | Status | Description | AC |
|---|---|---|---|
| T-001 | done | Encode and document **canonical installer delivery policy** for scratchpad artifacts per **`DEC-0055`**: Model B default, when materialized baseline is required, and deterministic rationale vs legacy Model A | AC-1 |
| T-002 | done | Ensure `/auto` and phase command loaders resolve required scratchpad flags after merge **without silent missing-config fallback**; fail closed with diagnostics when required keys absent/invalid | AC-2 |
| T-003 | done | Implement **`its-magic --mode upgrade`** behavior: preserve **user-owned** `.cursor/scratchpad.local.md`; refresh framework-owned example; apply selected delivery policy consistently with **`DEC-0039`** | AC-3 |
| T-004 | done | Missing/invalid baseline or merge state **fails closed** with deterministic operator diagnostics, layer attribution (`local`, `baseline|materialized`, `example`), and remediation guidance | AC-4 |
| T-005 | done | Make **ownership boundaries** explicit and enforced: framework vs user scratchpad paths; clean-repo and install paths never overwrite user local | AC-5 |
| T-006 | done | Maintain **installer parity** across `installer.ps1`, `installer.sh`, `installer.py`, and CLI entrypoints for Model B delivery + merge semantics | AC-6 |
| T-007 | done | Update **README + runbook**: chosen model (**`DEC-0055`**), migration from legacy dual committed files, materialization steps, and operator actions | AC-7 |
| T-008 | done | Preserve **active/template parity** for scratchpad-related contracts, examples, and installer-adjacent docs | AC-8 |
| T-009 | done | Add **regression coverage**: fresh install, upgrade from legacy, missing-file recovery, local override preservation (tests or scripted checks as established in repo) | AC-9 |
| T-010 | done | Document **decision/traceability overlap** with **`US-0018`**, **`US-0057`**, **`DEC-0039`**, **`R-0050`**; confirm no regression in automation **fail-closed** safety defaults | AC-10 |

## Deterministic AC-to-task mapping

- AC-1 → T-001
- AC-2 → T-002
- AC-3 → T-003
- AC-4 → T-004
- AC-5 → T-005
- AC-6 → T-006
- AC-7 → T-007
- AC-8 → T-008
- AC-9 → T-009
- AC-10 → T-010
