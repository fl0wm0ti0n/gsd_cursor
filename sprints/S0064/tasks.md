# Sprint S0064 Tasks

- Story: `US-0083`
- Sprint: `S0064`
- Governance: `DEC-0067`; `architecture.md` `# US-0083`; `R-0062`; `US-0045`

| Task | Status | Description | AC |
|---|---|---|---|
| T-001 | done | Refine intake question-selection flow so previously captured equivalent evidence suppresses repetitive required-topic prompts while preserving mandatory topic accounting | AC-1 |
| T-002 | done | Extend intake capture surfaces to support explicit topic-scoped delegation opt-in and persist auditable delegation evidence entries | AC-2 |
| T-003 | done | Implement validator branch where required topics marked `satisfied_by=delegation_ref` pass persistence only when complete delegation evidence is present | AC-3 |
| T-004 | done | Preserve and verify unchanged fail-closed behavior for unresolved required topics that are not explicitly delegated (`INTAKE_REQUIRED_TOPIC_MISSING` path) | AC-4 |
| T-005 | done | Enforce bounded delegation metadata contract (`delegation_scope`, `delegation_rationale`, `delegation_confidence`) and propagate to downstream artifacts for revisit | AC-5 |
| T-006 | done | Ensure guided and low-touch intake modes share identical delegation validation semantics with no mode-specific bypass path | AC-6 |
| T-007 | done | Update `/intake` command docs, PO guidance, and runbook sections for ask-vs-delegate behavior and deterministic evidence recording expectations | AC-7 |
| T-008 | done | Update intake evidence schema and validator for delegated-topic representation with DEC-0060-compatible machine-verifiable `ie:` references | AC-8 |
| T-009 | done | Maintain active/template parity for every touched command/rule/docs/test surface implementing delegation behavior | AC-9 |
| T-010 | done | Add regression matrix for delegated pass, delegated invalid/missing evidence fail, and non-delegated required-topic fail with deterministic diagnostics | AC-10 |

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
