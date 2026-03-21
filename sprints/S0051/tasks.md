# Sprint S0051 Tasks

- Story: `US-0072`
- Sprint: `S0051`

| Task | Status | Description | AC |
|---|---|---|---|
| T-001 | done | Encode deterministic hot/archive contract for `docs/engineering/state.md`, `handoffs/po_to_tl.md`, and `docs/engineering/architecture.md`: merged scratchpad threshold keys, default caps, section/checkpoint definitions, and deterministic pack naming per **`DEC-0054`** | AC-1 |
| T-002 | done | Implement same-phase-boundary rollover semantics: when caps exceeded, complete archive in the mutating phase or fail closed with deterministic reason code (no successful phase completion with oversize hot triad) | AC-2 |
| T-003 | done | Ensure archive execution emits verification tuple (`boundary`, `moved`, `retained`, `pack_ref`) and pack writes are idempotent on rerun | AC-3 |
| T-004 | done | Wire archive verification gates so `/refresh-context` and every phase that mutates triad hot files cannot complete without passing rollover/verification contract | AC-4 |
| T-005 | done | Define and document deterministic minimal-read policy per canonical phase: required files, optional escalation path, bounded line/file budgets | AC-5 |
| T-006 | done | Add compact phase-context artifacts (hot summaries / pointers) so subagents read latest relevant evidence first and expand only when unresolved | AC-6 |
| T-007 | done | Document and enforce deterministic reason-code taxonomy for archive and context-budget failures (minimum set aligned to **`DEC-0054`** / architecture) | AC-7 |
| T-008 | done | Validate traceability: no historical evidence loss; archived slices remain linked and auditable from hot surfaces and packs | AC-8 |
| T-009 | done | Maintain active/template parity for command contracts, scratchpad + runbook + README guidance, and triad archive directory documentation | AC-9 |
| T-010 | done | Add regression coverage: threshold-crossing success path, empty-archive / oversize-hot detection, idempotent rollover, bounded-read enforcement, and fail-safe (fail-closed) behavior | AC-10 |

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
