# Sprint S0047 Tasks

- Story: `US-0068`
- Sprint: `S0047`

| Task | Status | Description | AC |
|---|---|---|---|
| T-001 | done | Define canonical `first-intake-pack` schema and required topic IDs for users/problem, runtime target/environment, stack/runtime, architecture preference, UI/design expectations, security/compliance, NFR priorities, and scope/timeline | AC-1 |
| T-002 | done | Define canonical `small-intake-pack` schema and required topic IDs for outcome/success criteria, impacted components, constraints/compatibility risk, required tests/acceptance checks, and done definition | AC-2 |
| T-003 | done | Implement deterministic required/optional classification and machine-verifiable coverage evaluation for both packs | AC-1, AC-2 |
| T-004 | done | Add fail-closed intake persistence gate that blocks backlog/acceptance writes until required pack coverage is satisfied or bounded assumptions are explicitly confirmed | AC-3 |
| T-005 | done | Preserve guided-mode adaptive follow-ups with bounded rounds while enforcing minimum pack coverage | AC-4 |
| T-006 | done | Preserve low-touch mode but enforce critical minimum safety questions when required fields are missing | AC-5 |
| T-007 | done | Persist intake questioning evidence (`asked_topics`, `missing_topics`, unresolved assumptions, confirmations) in canonical backlog/acceptance/handoff artifacts | AC-6 |
| T-008 | done | Define deterministic intake-block reason-code taxonomy and remediation output for missing required answers | AC-7 |
| T-009 | done | Maintain active/template parity for intake command, PO agent guidance, runbook, and README surfaces touched by question-pack enforcement | AC-8 |
| T-010 | done | Add regression coverage for first-intake flow, small-intake flow, low-touch compatibility, and blocked-on-missing-answer behavior | AC-9 |
| T-011 | done | Enforce language/project-aware question-pack selection with deterministic unknown-stack fallback behavior | AC-10 |

## Deterministic AC-to-task mapping (one-to-many)

- AC-1 -> T-001, T-003
- AC-2 -> T-002, T-003
- AC-3 -> T-004
- AC-4 -> T-005
- AC-5 -> T-006
- AC-6 -> T-007
- AC-7 -> T-008
- AC-8 -> T-009
- AC-9 -> T-010
- AC-10 -> T-011
