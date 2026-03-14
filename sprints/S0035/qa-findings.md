# QA Findings — Sprint S0035 (US-0056)

## Summary

- **Sprint:** S0035
- **Story:** US-0056 (Strict Runtime Proof for Per-Phase Subagent Isolation)
- **Outcome:** PASS
- **Blockers:** None
- **Date:** 2026-03-14

## Test evidence

| Check | Result | Evidence |
|-------|--------|----------|
| TEST_COMMAND runbook attempt | WARN (host-limited) | `sh tests/run-tests.sh` unavailable on this Windows host (`sh` command not found) |
| TEST_COMMAND baseline verification (fallback) | PASS | `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` exit code 0 |
| tests/report.md | PASS | Current run shows `Fail: 0` |
| US-0056 regression assertions | PASS | New strict runtime-proof checks in `tests/run-tests.ps1` and `tests/run-tests.sh` pass |
| LINT_COMMAND | SKIPPED | `docs/engineering/runbook.md` value is empty (intentional default) |
| TYPECHECK_COMMAND | SKIPPED | `docs/engineering/runbook.md` value is empty (intentional default) |

## Acceptance criteria verification (US-0056 AC-1..AC-10)

| AC | Contract | Result | Evidence |
|----|----------|--------|----------|
| AC-1 | strict runtime attestation tuple contract defined | PASS | `DEC-0038`, `.cursor/commands/auto.md`, `docs/engineering/runbook.md` |
| AC-2 | `/auto` requires strict-proof and fails closed | PASS | `.cursor/commands/auto.md` strict-proof section + step 11b |
| AC-3 | strict-proof linked to state checkpoint evidence | PASS | runbook strict-proof linkage contract + state checkpoints |
| AC-4 | deterministic strict-proof reason codes | PASS | `RUNTIME_PROOF_*` codes in auto/release/runbook |
| AC-5 | pause/resume provenance continuity | PASS | runbook and resume/state checkpoint contracts |
| AC-6 | verify/release gate consumption | PASS | `.cursor/commands/verify-work.md`, `.cursor/commands/release.md` |
| AC-7 | bounded legacy guidance | PASS | architecture + runbook boundaries |
| AC-8 | operator diagnostics guidance | PASS | runbook + README strict-proof sections |
| AC-9 | regression test coverage | PASS | new test assertions in both test runners |
| AC-10 | active/template parity maintained | PASS | command/runbook/README parity checks |

## Optional-mode checks

- SECURITY_REVIEW=0 -> skipped (zero required security-review overhead).
- CROSS_REPO_OBSERVABILITY=0 -> skipped (zero required compatibility overhead).
- COMPONENT_SCOPE_MODE=0 -> skipped (zero required component-scope overhead).
- SPEC_PACK_MODE=0 -> skipped.
- USER_GUIDE_MODE=0 -> skipped.

## Findings

- **Blocking:** None.
- **Non-blocking:** Shell-based runbook `TEST_COMMAND` remains host-limited on
  Windows; PowerShell fallback was used for mandatory QA evidence.

## Recommendation

- Proceed to **`/verify-work`** for S0035.
