# QA Findings — Sprint S0029 (US-0050)

## Summary

- **Sprint:** S0029
- **Story:** US-0050 (Clean Install Hygiene and Complete Clean-Repo Coverage)
- **Outcome:** PASS
- **Blockers:** None
- **Date:** 2026-03-11

## Test evidence

| Check | Result | Evidence |
|-------|--------|----------|
| TEST_COMMAND baseline verification | PASS | `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` exit code 0 |
| tests/report.md | PASS | Timestamp: 2026-03-11T22:12:04Z, Pass: 404, Fail: 0 |
| Homebrew stable formula sync checks | PASS | `Homebrew stable formula URL uses npm version tag`; `Homebrew stable formula version matches npm version` |
| US-0050 lifecycle/install-clean assertions | PASS | Ownership manifest, neutral starter artifacts, and clean completeness checks are all passing |
| LINT_COMMAND | SKIPPED | `docs/engineering/runbook.md` value is empty (intentional default) |
| TYPECHECK_COMMAND | SKIPPED | `docs/engineering/runbook.md` value is empty (intentional default) |

## Acceptance criteria verification (US-0050 AC-1..AC-9)

| AC | Contract | Result | Evidence |
|----|----------|--------|----------|
| AC-1 | clean-repo removes ownership-complete installer-managed artifacts | PASS | `docs/engineering/context/installer-owned-paths.manifest`; lifecycle assertions in `tests/report.md` |
| AC-2 | one ownership source consumed by ps1/sh/py installers | PASS | `installer.ps1`, `installer.sh`, `installer.py` manifest-loading logic |
| AC-3 | non-framework cleanup safety is explicit and tested | PASS | clean safety assertions in `tests/run-tests.ps1` and `tests/run-tests.sh` |
| AC-4 | template engineering starter artifacts are neutralized | PASS | `template/docs/engineering/status-normalization-report.md`, `compatibility-*.md`, `component-scope*.md` |
| AC-5 | no hardcoded runtime ID refs in starter docs (or intentional baseline) | PASS | `template/docs/engineering/research.md` header no longer references `DEC-0011` |
| AC-6 | fresh missing install yields neutral baseline artifacts | PASS | fresh-install assertions in test runners and passing report rows |
| AC-7 | US-0018 upgrade behavior remains intact | PASS | upgrade assertions in lifecycle tests remain passing |
| AC-8 | regression coverage across fresh install/clean/reinstall/parity | PASS | both test runners include expanded checks and are passing |
| AC-9 | active/template install-clean contract parity maintained | PASS | parity of manifest + README/help contract text in active and template copies |

## Optional-mode checks

- SECURITY_REVIEW=0 -> skipped (zero required security-review overhead).
- CROSS_REPO_OBSERVABILITY=0 -> skipped (zero required compatibility overhead).
- COMPONENT_SCOPE_MODE=0 -> skipped (zero required component-scope overhead).
- SPEC_PACK_MODE=0 -> skipped.
- USER_GUIDE_MODE=0 -> skipped.

## Findings

- **Blocking:** None.
- **Non-blocking:** Runbook `TEST_COMMAND` currently references `sh tests/run-tests.sh`; on this host, PowerShell baseline command was used successfully for mandatory QA evidence.

## Sync-policy reason code guidance

- `PRE_QA_AUTOPUSH_FORBIDDEN` cleared for this sprint after QA pass.
- `BLOCKING_QA_FINDINGS` not applicable (no open blockers).
- `SYNC_PUSHED` may be eligible only when policy/branch safety checks pass (current mode remains manual).

## Recommendation

- Proceed to **`/verify-work`** for S0029.
