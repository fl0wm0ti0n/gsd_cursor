# Release-to-Dev Handoff — S0122 / US-0122

**date**: 2026-08-24
**from**: release (1st attempt, fresh subagent)
**to**: dev / operator (runbook mirror + triad rollover + harness green)
**orchestrator_run_id**: auto-20260824-01
**release_attempt_marker**: rel-US0122-release-20260824T124500Z-fresh
**model_id**: composer-2.5-fast (CROSS_MODEL_REVIEW=1 — required)

## Blocker

`/release` for `S0122` (US-0122 OpenCode role agents and Layer-1 permission table) fails closed at **gate 1 (check-in test)** with reason code **`RELEASE_TEST_FAILED`**. Queue row S0122 set to `blocked` (NOT `released`). No backlog mutation (closure owns that per US-0120). No publish (disabled).

QA, UAT, isolation, and verify-work strict proof were green at spawn. Gate 4b verify-work proof `rp-auto-20260824-01-verify-work-qa-20260824T123500Z-US-0122` (ttl `2026-08-24T13:35:00Z`) was still fresh — **not** `RUNTIME_PROOF_STALE`.

## Deterministic cause

**`RELEASE_TEST_FAILED`** — Prior `tests/report.md` @ `2026-08-24T10:45:36Z` (`Pass: 845 / Fail: 0`) predates US-0122 execute (`12:15:00Z`) and lacks US-0122 harness rows → stale for this story. Release subagent reran consolidated harness:

```powershell
powershell -ExecutionPolicy Bypass -File tests/run-tests.ps1
```

- Exit code: **1**
- Fresh `tests/report.md` @ `2026-08-24T12:44:49Z`: **`Pass: 830 / Fail: 15`**
- Grep `\[FAIL\]` on report: **15 rows**

Key in-scope failures (US-0122 execute regression surface):

| Failure row | Root cause |
|-------------|------------|
| `slim auto command contract markers pass` | 3 pytest failures in `tests/auto_command_contract_test.py`: architecture `# US-0089` bottom-append violated by later `# US-0122` heading; active/template runbook byte mismatch |
| `check_intake_template_parity --scope=*` (multiple scopes) | `docs/engineering/runbook.md` active (196549b) ≠ template (196286b) — US-0122 h2 added active-only |
| `triad check passes on repo` / `triad check idempotent rerun passes` | `STATE_ARCHIVE_REQUIRED` — state 1845/1200 lines; architecture 3219/3000 lines |

US-0122 contract tests (`tests/us0122_contract_test.py` 8/8) pass in isolation; failure is **parity / triad / consolidated harness** integration.

## QA / verify-work state (informative)

- QA: **PASS** (`sprints/S0122/qa-findings.md`) — 0 blockers; 8/8 contract tests independent re-run.
- Verify-work: **PASS** (`handoffs/verify_to_release.md`, `sprints/S0122/verify-work-findings.md`) — 10/10 UAT; 8/8 live pytest.
- UAT: **PASS** (`sprints/S0122/uat.json` 10/10).
- Isolation: **PASS** — execute, qa, verify-work in `docs/engineering/state.md`.

## Required remediation

1. **Mirror runbook h2** — Copy `## OpenCode role agents and permissions (US-0122)` block from active `docs/engineering/runbook.md` to `template/docs/engineering/runbook.md` so active/template runbook pair is byte-identical (fixes parity scopes + `test_template_runbook_literal_parity_active` + `test_us0095_template_parity_auto_surfaces`).
2. **Architecture bottom-append** — Resolve `test_caveman_architecture_section_bottom_appended_and_linked` failure (`# US-0122` appended after `# US-0089` per DEC-0073 §11). Coordinate with tech-lead if contract update is required; prefer minimal compliant placement.
3. **Triad rollover** — `python scripts/enforce-triad-hot-surface.py --rollover` then `--check` (state + architecture hot-surface oversize).
4. **Refresh harness** — `powershell -ExecutionPolicy Bypass -File tests/run-tests.ps1` → exit 0; `Fail: 0`; zero `[FAIL]` rows.
5. **Rerun `/verify-work`** if gate-4b proof TTL expires before `/release` retry (current ttl `2026-08-24T13:35:00Z`).
6. **Rerun `/release`** in fresh release subagent. On PASS → `/closure` (qe).

## Stop condition

STOP after release handoff. Orchestrator spawns `/execute` (dev) for remediation — release must NOT self-remediate implementation.
