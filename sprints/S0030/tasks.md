# Sprint S0030 Tasks

- Story: `US-0051`
- Sprint: `S0030`

| Task | Status | Description | AC |
|---|---|---|---|
| T-001 | done | Define deterministic intake breadth/risk scoring heuristics and decomposition trigger thresholds | AC-1, AC-5 |
| T-002 | done | Implement multi-story decomposition proposal generation using vertical-slice/workflow-step split strategy | AC-1, AC-2 |
| T-003 | done | Persist split rationale and story boundaries in intake outputs for traceability | AC-3, AC-9 |
| T-004 | done | Add explicit user choice flow to accept, merge, or adjust proposed decomposition before persistence | AC-4 |
| T-005 | done | Enforce single-story default for small/narrow intake with deterministic no-split behavior | AC-5 |
| T-006 | done | Add risk-aware questioning triggers for broad/high-impact intake beyond ambiguity-only checks | AC-6 |
| T-007 | done | Bound adaptive questioning rounds with deterministic stop conditions to prevent unstructured loops | AC-7 |
| T-008 | done | Preserve low-touch `INTAKE_GUIDED_MODE=0` behavior while keeping duplicate/overlap safety mandatory | AC-8 |
| T-009 | done | Update intake artifact contracts (`backlog.md`, `acceptance.md`, `handoffs/po_to_tl.md`) with decomposition/questioning evidence | AC-9 |
| T-010 | done | Align active and `template/` intake/PO guidance for decomposition + adaptive-question behavior | AC-10 |
| T-011 | done | Add regression coverage for split/no-split, user choice flow, risk-aware questions, low-touch mode, and parity guarantees | AC-10 |
