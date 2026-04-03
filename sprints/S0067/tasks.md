# Sprint S0067 Tasks

- **Bug**: `BUG-0006`
- **Sprint**: `S0067`
- **Governance**: `architecture.md` `# BUG-0006`; `R-0065`; `US-0045`

| Task | Status | Description | AC |
|---|---|---|---|
| T-001 | done | Update **`.cursor/commands/auto.md`**: spawn-only / orchestrator-scope boundaries; forbid direct orchestrator phase work and phase deliverable writes; add **`AUTO_ORCHESTRATOR_PHASE_EXECUTION`** to documented fail-fast vocabulary with remediation | AC-1 |
| T-002 | done | Update **`template/.cursor/commands/auto.md`** for literal parity with active **`auto.md`** on BUG-0006 contract surfaces | AC-2 |
| T-003 | done | Update **`docs/engineering/auto-orchestration-reference.md`**: mirror spawn-only rule; cross-link **DEC-0029** / **DEC-0038**; document **`AUTO_ORCHESTRATOR_PHASE_EXECUTION`** | AC-3 |
| T-004 | done | Extend **`tests/auto_command_contract_test.py`**: required contract strings, reason-code literal, negative non-contradiction vs in-orchestrator phase execution (**R-0065**) | AC-4 |
| T-005 | done | Verify **`tests/run-tests.sh`** / **`tests/run-tests.ps1`** still reference and run **`tests/auto_command_contract_test.py`**; adjust sections only if paths or invocation contract changes | AC-5 |

## Deterministic AC-to-task mapping

- AC-1 -> T-001
- AC-2 -> T-002
- AC-3 -> T-003
- AC-4 -> T-004
- AC-5 -> T-005
