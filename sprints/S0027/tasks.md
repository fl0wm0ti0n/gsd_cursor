# Sprint S0027 Tasks

- Story: `US-0032`
- Sprint: `S0027`

| Task | Status | Description | AC |
|---|---|---|---|
| T-001 | done | Add USER_GUIDE_MODE flag in scratchpad (active + template); default 0 (disabled) | AC-1 |
| T-002 | done | Document that when USER_GUIDE_MODE=0, intake/architecture/sprint/execute/qa/release add no required guide steps or blocking checks | AC-2 |
| T-003 | done | Define canonical location and naming: docs/user-guides/US-xxxx.md per feature story when enabled | AC-3 |
| T-004 | done | Define minimum required guide schema (Purpose, Prerequisites, Usage steps, Example, Limitations, Troubleshooting) and document in runbook | AC-4 |
| T-005 | done | Add validation that reports completeness per guide; fail/release-block only when USER_GUIDE_MODE=1 and required sections missing (USER_GUIDE_INCOMPLETE) | AC-5 |
| T-006 | done | Define story ID → user guide artifact traceability and reference in handoff/release context | AC-6 |
| T-007 | done | Enforce boundaries with US-0031 spec-pack: user guides end-user only; no duplicate ownership/content; document separation in commands/runbook | AC-7 |
| T-008 | done | Align active and template docs/commands/rules for user-guide mode (parity) | AC-8 |
