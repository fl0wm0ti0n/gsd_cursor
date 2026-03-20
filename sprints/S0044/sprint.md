# Sprint S0044

- Story: `US-0065`
- Goal: implement mandatory runtime QA autopilot for generated projects with bounded retries and deterministic evidence.
- Status: execute-complete

## Scope

- Runtime verification pipeline in execute/qa (`startup -> connectivity -> logs -> bounded retries -> verdict`).
- Deterministic runtime reason-code taxonomy and fail-closed behavior.
- Stack-aware runtime profile selection with explicit unresolved-stack handling.
- Webapp/browser verification path when HTTP/UI context applies.
- Remote-runtime compatibility via connectivity contract with sanitized reporting.
- Documentation and regression coverage updates with active/template parity.
