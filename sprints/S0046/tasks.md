# Sprint S0046 Tasks

- Story: `US-0067`
- Sprint: `S0046`

| Task | Status | Description | AC |
|---|---|---|---|
| T-001 | done | Define canonical required `Run/Connect/Verify` section schema for `handoffs/releases/Sxxxx-release-notes.md` with fixed order contract | AC-1 |
| T-002 | done | Enforce required operator field set: startup command(s), runtime mode (`local|remote`), endpoint, expected health signal, and known issues | AC-2 |
| T-003 | done | Add credentials/auth guidance contract for env-variable references only with expected value-source location semantics | AC-3 |
| T-004 | done | Update legacy pointer surface `handoffs/release_notes.md` with concise deterministic latest run/connect summary linking to canonical sprint notes | AC-4 |
| T-005 | done | Add release finalization fail-closed behavior on missing/ambiguous operator fields with deterministic reason codes and remediation guidance | AC-5 |
| T-006 | done | Surface explicit local-vs-remote runtime context and enforce alignment checks with `docs/engineering/runtime-connectivity.md` when present | AC-6 |
| T-007 | done | Require QA/release findings references proving operator guidance validation against real verification evidence | AC-7 |
| T-008 | done | Maintain active/template parity across release command docs/templates and runbook guidance for operator hints contract | AC-8 |
| T-009 | done | Add regression coverage for valid guidance generation, missing-field fail-safe paths, and credentials secret-redaction policy checks | AC-9 |
| T-010 | done | Enforce concise deterministic/idempotent operator-facing output contract across repeated release reruns | AC-10 |
