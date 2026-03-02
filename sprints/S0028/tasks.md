# Sprint S0028 Tasks

- Story: `US-0049`
- Sprint: `S0028`

| Task | Status | Description | AC |
|---|---|---|---|
| T-001 | done | Define and document detection rule: legacy drift = backlog DONE and (acceptance unchecked OR traceability/state lacks entry OR release artifacts lack representation) | AC-1 |
| T-002 | done | Implement bounded target-scoped repair: mutate only stories matching legacy-drift rule; no broad rewrite of unrelated artifacts | AC-2 |
| T-003 | done | Define audit report format with required fields (story ID, prior acceptance/traceability state, resolved state, reason code, evidence ref); canonical path `docs/engineering/legacy-drift-audit.md` | AC-3 |
| T-004 | done | Implement reason-code vocabulary and remediation: BACKLOG_DONE_ACCEPTANCE_UNCHECKED, BACKLOG_DONE_TRACEABILITY_MISSING, BACKLOG_DONE_RELEASE_ARTIFACT_MISSING | AC-4 |
| T-005 | done | Implement one-time backfill mode: explicit trigger runs detection and repair once; idempotent when no drift; emit audit report | AC-5 |
| T-006 | done | Implement ongoing guard at release/reconciliation: detect legacy drift; block with reason code or perform target-scoped repair with audit append; documented and deterministic | AC-6 |
| T-007 | done | Align active and template command/rule/docs for backfill guard, audit report location, and reason codes | AC-7 |
| T-008 | done | Add regression coverage: no-drift run, single-drift repair, guard block/repair with reason code | AC-8 |
