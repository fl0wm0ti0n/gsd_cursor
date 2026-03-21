# Sprint S0051

- Story: `US-0072`
- Goal: enforce deterministic hot/archive compaction for the triad (`docs/engineering/state.md`, `handoffs/po_to_tl.md`, `docs/engineering/architecture.md`) with scratchpad-bound thresholds, same-phase rollover or fail-closed semantics, verification tuples, minimal-read budgets, compact phase-context pointers, and regression coverage — per **`DEC-0054`**, architecture US-0072, **`R-0047`**, and backlog AC-1..AC-10.
- Status: planned (awaiting `/plan-verify`, then `/execute`)

## Scope

- Document and implement hot/archive contracts with explicit pack naming (`state-archive/`, `handoffs/archive/`, `architecture-archive/`) and merged scratchpad keys (`STATE_HOT_*`, `PO_TO_TL_HOT_*`, `ARCH_HOT_*`).
- Same-boundary rollover before phase success or deterministic fail-closed reason codes (no silent oversize hot surfaces).
- Mandatory verification evidence (`boundary`, `moved`, `retained`, `pack_ref`) and idempotent pack writes.
- Archive verification gates for `/refresh-context` and any phase that mutates the triad.
- Per-phase minimal-read policy plus compact hot-summary / pointer artifacts for subagent retrieval.
- Reason-code taxonomy (`STATE_ARCHIVE_REQUIRED`, `ARTIFACT_HOT_SURFACE_OVERSIZE`, `CONTEXT_BUDGET_EXCEEDED`, etc.).
- Preserve auditable history (no destructive loss); active/template parity for commands, scratchpad/runbook/README, and archive README stubs.
