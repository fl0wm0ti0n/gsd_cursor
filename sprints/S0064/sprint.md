# Sprint S0064

- Story: `US-0083`
- Goal: **Explicit delegable intake topics without weakening fail-closed semantics** - implement `DEC-0067` so intake supports topic-scoped `satisfied_by=delegation_ref` with deterministic evidence fields and DEC-0060-compatible `ie:` binding, preserves strict fail-closed behavior for non-delegated unresolved required topics, keeps guided/low-touch parity, updates docs and command guidance, and ships regression and parity coverage for delegated pass and block scenarios.
- Status: **Execute complete - awaiting `/qa`** (`orchestrator_run_id=auto-20260331-04`; `planned_at=2026-04-01T01:20:00Z`; `executed_at=2026-04-01T09:30:00Z`; `fresh_context_marker=dev-US0083-execute-20260401T093000Z-fresh`)

## Scope

- **AC-1** - Intake questioning adapts to request context and avoids fixed repetitive prompt sequences when equivalent information is already available.
- **AC-2** - Users can explicitly delegate unresolved intake decisions to the agent (clear opt-in phrase/field), and this delegation is persisted as auditable evidence.
- **AC-3** - Explicit delegation provides a non-blocking persistence path for unresolved topics that would otherwise fail as missing, while preserving deterministic validation semantics.
- **AC-4** - Non-delegated unresolved required topics continue to fail closed with existing deterministic reason codes and remediation.
- **AC-5** - Delegated assumptions include bounded scope/rationale and confidence notes so downstream phases can revisit or confirm if needed.
- **AC-6** - Guided and low-touch modes both support delegation consistently, without silent bypasses.
- **AC-7** - `/intake` command, PO agent guidance, and runbook documentation explain when to ask, when to delegate, and how evidence is recorded.
- **AC-8** - Intake evidence schema/validator supports delegated-topic representation with machine-verifiable refs compatible with DEC-0060 conventions.
- **AC-9** - Active/template parity is maintained for command/rule/docs/tests implementing delegation behavior.
- **AC-10** - Regression coverage includes delegated pass cases, non-delegated block cases, and deterministic diagnostics.

## Governance

- `decisions/DEC-0067.md`
- `docs/engineering/architecture.md` `# US-0083`
- `docs/engineering/research.md` `R-0062`
- Related: `US-0068`, `US-0078`, `US-0045`, `DEC-0050`, `DEC-0060`
