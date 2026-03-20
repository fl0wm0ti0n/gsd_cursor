# Sprint S0045

- Story: `US-0066`
- Goal: implement deterministic generated-test scaffolding and automatic QA test execution for app projects.
- Status: execute-complete

## Scope

- Stack/project detection for Node, Python, Go, Java, and .NET baseline scaffold selection.
- Non-destructive generation of missing unit/integration/acceptance test assets with evidence capture.
- Deterministic `TEST_COMMAND` runbook wiring for detected stacks.
- Mandatory `/qa` auto-execution of generated baseline tests with auditable pass/fail output.
- Fail-closed diagnostics for unsupported/unresolvable stacks.
- Integration boundary with runtime autopilot contract (`US-0065`) and active/template parity.
