# Sprint S0025 Tasks

- Story: `US-0048`
- Sprint: `S0025`

| Task | Status | Description | AC |
|---|---|---|---|
| T-001 | done | Enforce `/auto` orchestrator-only behavior; fail when phase work is executed without spawning a fresh subagent context | AC-1 |
| T-002 | done | Define isolation evidence schema (phase_id, role, fresh_context_marker, timestamp, evidence_ref) and canonical artifact locations | AC-2, AC-6 |
| T-003 | done | Add mandatory phase-transition isolation evidence writing to phase commands/agents | AC-2 |
| T-004 | done | Enforce `/execute` and `/qa` loop fresh-context-per-cycle semantics with deterministic evidence per cycle | AC-3 |
| T-005 | done | Implement fail-safe on missing/invalid isolation evidence (reason codes, stop progression) | AC-4 |
| T-006 | done | Add isolation-compliance gate to `/verify-work`; block finalization on violations | AC-5 |
| T-007 | done | Add isolation-compliance gate to `/release`; enforce gate order (isolation after UAT) | AC-5 |
| T-008 | done | Document reason-code taxonomy (PHASE_CONTEXT_ISOLATION_MISSING, PHASE_CONTEXT_ISOLATION_VIOLATION, ISOLATION_EVIDENCE_STALE, ISOLATION_EVIDENCE_INVALID) and remediation in runbook/commands | AC-7 |
| T-009 | done | Ensure pause/resume provenance; isolation evidence survives pause/resume; deterministic resume requires fresh context and new evidence | AC-9 |
| T-010 | done | Add regression coverage (positive/negative isolation cases); enforce active/template parity for isolation enforcement | AC-8, AC-10 |
