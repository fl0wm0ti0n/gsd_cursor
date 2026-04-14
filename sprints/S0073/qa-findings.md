# QA Findings -- S0073 / US-0085

- **sprint_id**: S0073
- **story_id**: US-0085
- **qa_phase**: qa
- **qa_role**: qa
- **qa_timestamp**: 2026-04-13T15:00:00Z
- **orchestrator_run_id**: auto-20260405-01
- **verdict**: **PASS**

## Test plan

| Check | Tool / command | Expected | Actual | Result |
|-------|---------------|----------|--------|--------|
| TEST_COMMAND (canonical) | `tests/run-tests.ps1` | 0 new failures | 790 pass, 4 fail (all pre-existing) | **PASS** |
| Full pytest suite | `python -m pytest tests/ -q` | 0 failures | 56 passed, 4 skipped, 66 subtests | **PASS** |
| Scratchpad pair parity | `check-scratchpad-pair-parity.py` | SCRATCHPAD_PAIR_OK | SCRATCHPAD_PAIR_OK | **PASS** |
| User-visible metadata | `check-user-visible-metadata.py` | exit 0 | exit 0 | **PASS** |
| Bug issue validation | `bug_issue_validate.py --check-acceptance` | BUG_VALIDATION_OK | BUG_VALIDATION_OK | **PASS** |
| Auto command contract | `auto_command_contract_test.py` | 17 pass | 17 passed, 66 subtests | **PASS** |
| Parity helper (AC-8) | `print_remote_env_hint.py` | Parity PASS | Parity PASS (20/20), exit 0 | **PASS** |
| Env gitignore tests (AC-9) | `test_env_gitignore.py -v` | 4 pass | 4 passed | **PASS** |
| Remote config summary (AC-10) | `remote_config_summary.py` | exit 0 | exit 0 (skip mode) | **PASS** |
| Triad hot surface | `enforce-triad-hot-surface.py --check` | PASS | PASS (exit 0) | **PASS** |

## Test results summary

- **pytest**: 56 passed, 4 skipped, 0 failed
- **run-tests.ps1**: 790 pass, 4 fail (all pre-existing)
- **Contract tests**: 17 passed, 66 subtests
- **New tests (AC-9)**: 4 passed
- **Total new failures introduced by US-0085**: **0**

## Pre-existing failures (not introduced by US-0085)

| Test assertion | Cause | Severity |
|---|---|---|
| Installer runbook TEST_COMMAND present for detectable stack | Stack detection not finding test command in tmp-install sandbox; pre-existing | Low |
| CLI missing install runbook TEST_COMMAND present | Same root cause for CLI install path; pre-existing | Low |
| auto includes strict-proof boundary step 11b (active) | US-0088 renumbered compact steps; test expects old literal; pre-existing from S0072 | Low |
| auto includes strict-proof boundary step 11b (template) | Same for template copy; pre-existing from S0072 | Low |

All 4 failures documented in `sprints/S0072/qa-findings.md` as pre-existing.

## AC verification

| AC | Criterion | Verified | Evidence |
|----|-----------|----------|----------|
| AC-1 | `.gitignore` + `template/.gitignore` list `.env` patterns with negation | **PASS** | Both files contain correct patterns; git check-ignore validates |
| AC-2 | `.cursorignore` + `template/.cursorignore` exclude `.env*` from agent context | **PASS** | Both files exist with correct patterns referencing DEC-0071 |
| AC-3 | `.env.example` + `template/.env.example` with 20 names only, no values | **PASS** | 20 names grouped by source; no secret values; section comments |
| AC-4 | `runbook.md` + template has `.env` copy/source recipe and guidance | **PASS** | Section present in both with Bash + PowerShell source commands |
| AC-5 | `runtime-connectivity.md` + template references `.env` sourcing | **PASS** | Sourcing paragraph present in both active and template |
| AC-6 | `us-0084-remote-e2e.md` + template references `.env` in Path B/C | **PASS** | Path B/C both reference `.env.example` copy and `.env` sourcing |
| AC-7 | `coding-standards.mdc` + template has `.env` exclusion rule | **PASS** | Exclusion bullet present after DEC-0016 bullet in both |
| AC-8 | `print_remote_env_hint.py` prints names only with parity check | **PASS** | 20 names printed alphabetically; Parity PASS 20/20; exit 0 |
| AC-9 | `test_env_gitignore.py` regression tests pass | **PASS** | 4/4 tests pass |
| AC-10 | `remote_config_summary.py` + existing tests remain PASS | **PASS** | Script exit 0; full suite 56/0 pass/fail; no regression |

## Observations (non-blocking)

1. Template `.gitignore` is minimal (only `.env*` patterns) -- intentional for new projects.
2. `!.env.example` negation added to both `.gitignore` and `.cursorignore` -- correct behavior.
3. `print_remote_env_hint.py` outputs parity line to stderr (cosmetic in PowerShell).

## Blocking findings

None.

## QA verdict

**PASS** -- All 10 ACs verified; no new test failures; no blocking findings. Ready for `/verify-work`.
