# Tasks — Sprint S0008

## US-0036: Official Remote Config Template, Docs, and Fail-Fast Validation

### T-001: Add canonical active remote config template
- Story: US-0036
- Status: done
- Files: `.cursor/remote.json`
- Description: Create canonical active `.cursor/remote.json` with non-secret
  placeholder values, required root/target fields, and safe defaults aligned to
  DEC-0016 and architecture contract. Include at least two placeholder targets
  (local network/docker-like and remote VM/SSH-like) without embedded secrets.
- AC covered: AC-1, AC-3

### T-002: Add template parity remote config file
- Story: US-0036
- Status: done
- Files: `template/.cursor/remote.json`
- Description: Add template counterpart for `.cursor/remote.json` with the same
  contract shape, safe placeholder semantics, and target examples as active
  copy. Verify parity and behavioral alignment.
- AC covered: AC-1, AC-9
- Depends on: T-001

### T-003: Define remote config schema and contract guidance
- Story: US-0036
- Status: done
- Files: `.cursor/commands/execute.md`, `.cursor/rules/core.mdc`
- Description: Encode contract guidance in command/rule touchpoints: required
  vs optional fields, data types, allowed values, and path/host conventions for
  remote targets. Ensure contract is deterministic and references DEC-0016.
- AC covered: AC-2
- Depends on: T-001

### T-004: Add mode-aware validation behavior guidance
- Story: US-0036
- Status: done
- Files: `.cursor/commands/execute.md`, `.cursor/rules/core.mdc`
- Description: Define validation trigger behavior so checks run only when
  `REMOTE_EXECUTION=1`. Explicitly skip remote-config validation when
  `REMOTE_EXECUTION=0` to preserve zero-overhead default path.
- AC covered: AC-4, AC-6
- Depends on: T-003

### T-005: Define actionable fail-fast error messaging format
- Story: US-0036
- Status: done
- Files: `.cursor/commands/execute.md`, `.cursor/rules/quality.mdc`
- Description: Add standardized error output contract for remote validation
  failures: include failing path, expected rule, actual value/type, and clear
  remediation hint. Include examples for missing file, invalid enum/type, and
  malformed JSON.
- AC covered: AC-5, AC-4
- Depends on: T-004

### T-006: Add security constraints for remote config handling
- Story: US-0036
- Status: done
- Files: `.cursor/rules/coding-standards.mdc`, `.cursor/commands/execute.md`
- Description: Add explicit security guardrails for remote config: no committed
  secrets/tokens/keys in `.cursor/remote.json`; sensitive values must use env
  variable references only. Include violation/remediation guidance.
- AC covered: AC-7
- Depends on: T-003

### T-007: Update README remote setup documentation
- Story: US-0036
- Status: done
- Files: `README.md`
- Description: Document remote setup workflow, schema summary, two safe example
  target configurations, mode behavior (`REMOTE_EXECUTION=0|1`), and fail-fast
  expectations with actionable troubleshooting pointers.
- AC covered: AC-3, AC-8
- Depends on: T-001, T-004, T-005, T-006

### T-008: Update runbook remote validation guidance
- Story: US-0036
- Status: done
- Files: `docs/engineering/runbook.md`
- Description: Add operator-oriented remote execution runbook guidance:
  preconditions, validation classes, fail-fast semantics when enabled,
  zero-overhead behavior when disabled, error interpretation, and remediation.
- AC covered: AC-4, AC-5, AC-6, AC-8
- Depends on: T-003, T-004, T-005, T-006

### T-009: Plan and add positive/negative QA coverage
- Story: US-0036
- Status: done
- Files: `tests/run-tests.ps1`, `tests/run-tests.sh`, `sprints/S0008/uat.md`
- Description: Add/adjust verification planning for remote config behavior with
  positive and negative paths. Negative-path coverage must include: missing
  remote config when enabled, malformed JSON, invalid fields/values, and
  secret-like inline values. Confirm disabled-mode non-blocking behavior.
- AC covered: AC-4, AC-5, AC-6, AC-7, AC-8, AC-9
- Depends on: T-002, T-004, T-005, T-006, T-008

### T-010: Final cross-reference and sprint/state updates
- Story: US-0036
- Status: done
- Files: `docs/engineering/state.md`, `handoffs/tl_to_dev.md`
- Description: Update state and handoff artifacts for S0008, including
  traceability index row for US-0036 with PLANNED status and evidence to be
  filled during verify-work. Confirm AC-to-task mapping remains complete.
- AC covered: AC-9
- Depends on: T-001 through T-009

## Implementation Order and Constraints

- Execute in sequence T-001 -> T-010.
- Keep sprint atomic to US-0036 only; do not mix unrelated stories.
- Respect mode-aware behavior: remote validation applies only when
  `REMOTE_EXECUTION=1`.
- Preserve zero-overhead default path for `REMOTE_EXECUTION=0`.
- Enforce active/template parity for remote config and related guidance.
