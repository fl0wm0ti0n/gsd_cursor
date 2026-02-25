# UAT — Sprint S0008

## Target

- **US-0036**: Official Remote Config Template, Docs, and Fail-Fast Validation
  - AC-1: Canonical `.cursor/remote.json` exists in active and template with aligned defaults/examples
  - AC-2: Remote config schema documented (required/optional fields, types, allowed values, conventions)
  - AC-3: Documentation includes at least two concrete safe target examples
  - AC-4: Validation guidance fails fast when `REMOTE_EXECUTION=1` and config is missing/malformed/invalid
  - AC-5: Validation output uses actionable error messages (path, expected, actual, remediation)
  - AC-6: `REMOTE_EXECUTION=0` mode has zero required remote-config overhead
  - AC-7: Security guidance prohibits committed secrets; env references only
  - AC-8: README and runbook document setup, validation behavior, and mode expectations
  - AC-9: Template parity verified across config references/docs/validation guidance

## Steps

1. **Positive path**: Verify `.cursor/remote.json` exists in active and template
   copies and matches contract shape (root fields + two target examples).
2. **Positive path**: Verify command/rule guidance defines required fields, types,
   allowed enums, and mode-aware behavior for `REMOTE_EXECUTION=0|1`.
3. **Negative path**: Verify missing config guidance exists for
   `REMOTE_EXECUTION=1` with fail-fast remediation.
4. **Negative path**: Verify malformed JSON guidance exists with actionable fix
   instruction.
5. **Negative path**: Verify invalid enum/type/value guidance exists with field
   path + expected + actual + remediation.
6. **Negative path**: Verify secret-like inline value prohibition and env-var-only
   remediation guidance exists.
7. **Disabled mode check**: Verify documentation explicitly states zero-overhead
   behavior when `REMOTE_EXECUTION=0`.
8. **Parity check**: Verify active/template command, rule, README, runbook, and
   remote config references are aligned.

## Dev pre-QA evidence

- Automated validation scripts updated for US-0036 positive/negative paths:
  - `tests/run-tests.ps1`
  - `tests/run-tests.sh`
- Pre-QA run completed in dev phase; final UAT pass/fail remains QA-owned.

## Results

1. Step 1 (AC-1, AC-9) — **PASS**
2. Step 2 (AC-2, AC-4, AC-6) — **PASS**
3. Step 3 (AC-4) — **PASS**
4. Step 4 (AC-4, AC-5) — **PASS**
5. Step 5 (AC-5) — **PASS**
6. Step 6 (AC-7) — **PASS**
7. Step 7 (AC-6) — **PASS**
8. Step 8 (AC-8, AC-9) — **PASS**

## Summary

- Passed: **8**
- Failed: **0**
- Total: **8**
- Count check: `passed + failed = total` (`8 + 0 = 8`) — consistent with `sprints/S0008/uat.json`.

## Acceptance traceability

- AC-1: PASS (Steps 1)
- AC-2: PASS (Step 2)
- AC-3: PASS (Step 1, target examples in contract shape check)
- AC-4: PASS (Steps 2, 3, 4)
- AC-5: PASS (Steps 4, 5)
- AC-6: PASS (Steps 2, 7)
- AC-7: PASS (Step 6)
- AC-8: PASS (Step 8)
- AC-9: PASS (Steps 1, 8)

UAT disposition for `US-0036`: **PASS**.
