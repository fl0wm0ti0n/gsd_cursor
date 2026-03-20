# Sprint S0045 Tasks

- Story: `US-0066`
- Sprint: `S0045`

| Task | Status | Description | AC |
|---|---|---|---|
| T-001 | done | Define deterministic stack/project detection contract for baseline scaffold selection (Node/Python/Go/Java/.NET minimum) | AC-1 |
| T-002 | done | Generate missing baseline unit/integration/acceptance test files in `/execute` and log generated paths as evidence | AC-2 |
| T-003 | done | Wire deterministic baseline `TEST_COMMAND` update in `docs/engineering/runbook.md` for detected stack | AC-3 |
| T-004 | done | Enforce `/qa` automatic execution of generated baseline tests with pass/fail evidence in `qa-findings` | AC-4 |
| T-005 | done | Add fail-closed unsupported-stack diagnostics and remediation guidance when generation cannot proceed | AC-5 |
| T-006 | done | Preserve user-authored tests and existing commands with deterministic non-destructive merge/precedence rules | AC-6 |
| T-007 | done | Integrate generated-test flow with runtime autopilot gate so non-starting apps cannot PASS QA | AC-7 |
| T-008 | done | Maintain active/template parity for generation rules, command docs, and test guidance surfaces | AC-8 |
| T-009 | done | Add regression coverage for fresh-generation, rerun idempotence, preservation behavior, and unsupported-stack fail-fast | AC-9 |
| T-010 | done | Ensure release/readiness artifacts deterministically reference generated-test evidence | AC-10 |
