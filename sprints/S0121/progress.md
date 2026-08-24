# Sprint S0121 — Progress (US-0121)

**sprint_id**: S0121
**story_id**: US-0121
**phase**: execute (build+verify macro — first canonical phase per ultra_lean)
**role**: dev (fresh per BUG-0006)
**orchestrator_run_id**: auto-20260823-01
**delivery_mode**: ultra_lean
**fresh_context_marker**: dev-US0121-execute-20260823T113000Z-fresh
**timestamp**: 2026-08-23T11:30:00Z (UTC)
**status**: IMPLEMENTED (T-anch + T-001..T-009 complete; 14 markers authored; awaiting /qa)

## Task progress

| Task | Status | Notes |
|---|---|---|
| T-anch | PASS | NO-OP verification note at sprints/S0121/t-anch-verification.md |
| T-001 | PASS | template/.opencode/ pack created (5 files; Q10 four gitignore groups; no slugs/secrets) |
| T-002 | PASS | manifest opencode sections added (active+template byte-identical) |
| T-003 | PASS | bin/its-magic.js --host parser + --help doc + forward to PS -InstallHost / sh --host |
| T-004 | PASS | installer.ps1 -InstallHost + Host-GatesCursorRow + diagnostics (PS syntax OK) |
| T-005 | PASS | installer.sh --host + host_gates_cursor_row + diagnostics |
| T-006 | PASS | installer.py --host (_HostAction) + host_gates_cursor_row + diagnostics (manifest authority) |
| T-007 | PASS | tests/us0121_host_mode_test.py (14 markers) + template mirror byte-identical |
| T-008 | PASS | opencode-adapter scope registered in both parity scripts (byte-identical) |
| T-009 | PASS | runbook ## OpenCode host mode (US-0121) h2 appended |

## Execute cycles

| Cycle | Phase | Role | Fresh marker | Verdict | Notes |
|------|-------|------|---------------|---------|-------|
| 1 | execute | dev | dev-US0121-execute-20260823T113000Z-fresh | PASS | T-anch + T-001..T-009 implemented in a single dev spawn (ultra_lean). 14 contract-test markers authored. Compose guards 5/5 UNCHANGED. Manifest + parity script + test file active/template byte-identical. `tests_not_run=python_not_on_path`. |
| 2 | execute | dev | dev-US0121-execute-loop2-20260823T115000Z-fresh | PASS | B-1 closed via Option C (test regex tightened + README L45 rephrased). `tests/us0121_host_mode_test.py` ↔ `template/tests/us0121_host_mode_test.py` byte-identical (SHA-256 F3A607…AF83B both). `rg "apiKey\|api_key\|sk-\|MODEL=" template/.opencode` → 0 hits. NB-2..NB-4 deliberately not addressed. `tests_not_run=python_not_on_path` (NB-1 persists). |

## Findings / blockers

- **NB-1 (non-blocking)**: `python` / `py` / `python3` / `node` not on PATH on this Windows host. Live pytest not run; recorded as `tests_not_run=python_not_on_path`. PS syntax verified via `[System.Management.Automation.Language.Parser]::ParseFile`. Manual review of installer.py / installer.sh / bin/its-magic.js performed. QA subagent should run pytest if python is available in its environment.
- **NB-2 (non-blocking)**: `docs/engineering/runbook.md` active vs `template/docs/engineering/runbook.md` were already drifting pre-US-0121 (pre-existing condition; not introduced by this story). US-0121 scope (`opencode-adapter`) does NOT include the runbook pair, so this drift does not affect the US-0121 parity gate. Left for the runbook-parity owner to reconcile.
- **NB-3 (non-blocking)**: PowerShell `-InstallHost` (not `-Host`) used internally to avoid the `$Host` automatic-variable landmine. JS exposes `--host` to end users and forwards `-InstallHost <value>` to PS. Documented in runbook + dev_to_qa handoff.
