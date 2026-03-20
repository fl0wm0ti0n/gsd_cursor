# Release Notes - S0044 (`US-0065`)

## What shipped

- Added mandatory runtime QA autopilot stage chain for generated projects:
  `startup -> readiness/connectivity -> log scan -> bounded retry -> verdict`.
- Added deterministic runtime failure reason-code taxonomy and fail-closed
  behavior for startup failure, endpoint unreachable, critical runtime logs,
  retry-budget exhaustion, and unresolved stack profile.
- Added bounded retry semantics and required per-attempt runtime evidence
  ledger fields for execute/qa runtime workflows.
- Added canonical runtime QA evidence schema requirements, including startup
  command, mode/profile context, health result, log summary, retry ledger,
  and final verdict fields.
- Added stack-aware runtime profile expectations for Node/Python/Go/Java/.NET
  plus deterministic unresolved-profile fallback.
- Added webapp runtime verification guidance (browser load + console/network
  signals) and bounded optional debug escalation path.
- Preserved remote-runtime compatibility via sanitized endpoint/auth-reference
  reporting constraints.
- Kept active/template parity and added US-0065 regression assertions.

## Gate summary

- Check-in test gate: PASS (US-0065 runtime-autopilot contract checks passed).
- QA completion gate: PASS (`sprints/S0044/qa-findings.md`).
- UAT completion gate: PASS (`10/10`, `0` failed).
- Isolation gate: PASS (execute/qa/verify-work evidence + strict proofs present).
- Release finalization: PASS (queue released + backlog/acceptance reconciled).
