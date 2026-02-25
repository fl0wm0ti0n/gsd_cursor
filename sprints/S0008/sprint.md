# Sprint S0008

## Goal

Plan and execute US-0036 (Official Remote Config Template, Docs, and Fail-Fast
Validation) as one atomic sprint that delivers a canonical remote config
artifact, mode-aware validation contract, actionable error guidance, security
constraints, and complete documentation parity across active and template files.

## Scope

- **In scope**: US-0036 (AC-1..AC-9).
- **Out of scope**: Implementing remote transport backends, external secret
  manager integrations, or changing remote protocol semantics.

## Sizing Check

- `SPRINT_MAX_TASKS=12`
- `SPRINT_AUTO_SPLIT=1`
- Planned tasks: 10
- 10 < 12 - within threshold. Single sprint, no split required.

## Milestone Check

- Milestone activation: **not applicable** for this sprint.
- Reason: no active milestone lifecycle is declared for US-0036 in current
  planning context; sprint remains standalone.

## Prerequisites

- S0007 verification complete.
- DEC-0016 accepted (remote config contract and mode-aware validation).
- US-0036 architecture section finalized in `docs/engineering/architecture.md`.

## Key Decisions

- DEC-0016: canonical `.cursor/remote.json` contract with strict validation only
  when `REMOTE_EXECUTION=1`; zero-overhead when `REMOTE_EXECUTION=0`.

## Implementation Order

Execute tasks T-001 through T-010 in sequence. T-001 and T-002 establish the
canonical active/template artifacts. T-003 through T-006 encode validation,
mode gating, error format, and security constraints. T-007 and T-008 finalize
README/runbook guidance. T-009 covers positive and negative QA planning. T-010
completes cross-reference and state updates.

## Risks

| Risk | Mitigation |
|------|------------|
| Contract drift between active and template remote config | Dedicated parity task (T-002) and final cross-reference verification (T-010). |
| False blocking when remote mode is off | Explicit mode-aware guidance task (T-004) and negative-path test planning (T-009). |
| Weak troubleshooting due to vague errors | Enforce actionable error-message format in T-005 and validate in T-009. |
| Secret leakage through config examples | Security constraints task (T-006) plus docs reinforcement in T-007/T-008. |
| Docs mismatch between README and runbook | Separate docs tasks for both files and parity checks in T-010. |

## Definition of Done

- Active and template canonical `.cursor/remote.json` artifacts are defined and
  aligned (AC-1, AC-9).
- Remote config contract/schema guidance is documented with required/optional
  fields, types, enums, and conventions (AC-2).
- At least two safe target examples are documented (AC-3).
- Fail-fast validation behavior is clearly defined for missing/malformed/invalid
  config when `REMOTE_EXECUTION=1` (AC-4).
- Error message contract includes path, expected rule, actual value/type, and
  remediation hint (AC-5).
- `REMOTE_EXECUTION=0` mode explicitly skips remote validation with zero
  required overhead (AC-6).
- Security guidance prohibits committed secrets and prescribes env-var
  references for sensitive values (AC-7).
- README and runbook are updated with setup + mode-specific behavior (AC-8).
- QA coverage plan includes both positive and negative cases, including missing
  file, malformed JSON, invalid fields, and secret-like inline values.
