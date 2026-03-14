# Sprint S0032 Tasks

- Story: `US-0053`
- Sprint: `S0032`

| Task | Status | Description | AC |
|---|---|---|---|
| T-001 | done | Define `TOKEN_PROFILE=lean|balanced|full` contract and deterministic profile-to-flag mapping table | AC-1 |
| T-002 | done | Implement lean-profile defaults for lower-overhead loops/research/automation while preserving mandatory gates | AC-2 |
| T-003 | done | Define balanced/full behavior and explicit manual-override precedence contract | AC-3 |
| T-004 | done | Implement hot-vs-archive compaction policy for `docs/engineering/state.md` with non-destructive archive references | AC-4 |
| T-005 | done | Implement compact index policy for `docs/engineering/decisions.md` with canonical DEC linkouts | AC-5 |
| T-006 | done | Update `/ask` contract to narrow-read retrieval (targeted first, bounded expansion, explicit not-found) | AC-6 |
| T-007 | done | Align active and `template/` command/agent/runbook/README/scratchpad contracts for token-profile and compaction semantics | AC-7 |
| T-008 | done | Add regression tests for profile mapping behavior, override precedence, and mandatory-gate invariants | AC-8 |
| T-009 | done | Add regression tests for compact-context and `/ask` narrow-read policy with active/template parity assertions | AC-8, AC-7 |
| T-010 | done | Update operator guidance and verify no ID/release-history semantics are rewritten by compaction changes | AC-9, AC-10 |
