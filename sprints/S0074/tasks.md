# Tasks — S0074 / US-0086

## T-001 — Add automation profile keys in scratchpad (active + template) — AC-1

- **AC**: AC-1
- **Description**: Add architecture-locked automation-profile keys to `.cursor/scratchpad.md` and `template/.cursor/scratchpad.md` (plus local example if touched), default-off, with explicit manual-mode unchanged behavior.
- **Files**: `.cursor/scratchpad.md`, `template/.cursor/scratchpad.md`, `.cursor/scratchpad.local.example.md`, `template/.cursor/scratchpad.local.example.md`
- **Status**: done
- **Acceptance**: Keys and defaults are present in active + template and preserve manual local default path.

## T-002 — Document manual vs automation mode in runbook (active + template) — AC-2

- **AC**: AC-2
- **Description**: Update runbook sections to clearly separate manual workflows (no remote config dependency) from automation workflows (may route remote when profile enabled).
- **Files**: `docs/engineering/runbook.md`, `template/docs/engineering/runbook.md`
- **Status**: done
- **Acceptance**: Runbook has explicit two-mode contract and references US-0085 names-only env posture.

## T-003 — Add deterministic routing guidance to rules/commands (active + template) — AC-3

- **AC**: AC-3
- **Description**: Update command/rule guidance so mode-on follows deterministic routing policy and mode-off never silently reroutes TEST_COMMAND to remote.
- **Files**: `.cursor/commands/auto.md`, `template/.cursor/commands/auto.md`, `.cursor/rules/coding-standards.mdc`, `template/.cursor/rules/coding-standards.mdc`
- **Status**: done
- **Acceptance**: Mode-on/off behavior appears in active + template with no ambiguous fallback.

## T-004 — Implement NL target intent resolution contract docs/tests — AC-4

- **AC**: AC-4
- **Description**: Add deterministic parsing contract for `start container <target_id>` and fail-closed outputs for unknown/disabled targets with locked reason codes.
- **Files**: `.cursor/commands/auto.md`, `docs/engineering/auto-orchestration-reference.md`, `template/.cursor/commands/auto.md`, `template/docs/engineering/auto-orchestration-reference.md`
- **Status**: done
- **Acceptance**: Explicit phrase contract and fail-closed reason-code path are documented in active + template.

## T-005 — Add handoff/state evidence tuple fields for remote routing — AC-5

- **AC**: AC-5
- **Description**: Define and wire execute/qa handoff evidence expectations for `target_id`, `environment_label`, `automation_profile`, `routing_source`, and names-only secret posture.
- **Files**: `handoffs/dev_to_qa.md`, `handoffs/qa_to_verify_work.md`, `docs/engineering/state.md` (contract references only), `docs/engineering/runbook.md`
- **Status**: done
- **Acceptance**: Handoff templates/guidance require tuple fields when remote routing is used.

## T-006 — Add optional deterministic CI recipe docs — AC-6

- **AC**: AC-6
- **Description**: Provide copy-pasteable optional CI routing recipe using deterministic path filters/matrix hints for Linux/container-sensitive changes.
- **Files**: `docs/engineering/runbook.md`, `template/docs/engineering/runbook.md`, `docs/engineering/runtime-connectivity.md`, `template/docs/engineering/runtime-connectivity.md`
- **Status**: done
- **Acceptance**: CI recipe is documented as optional and deterministic without claiming unsupported vendor magic.

## T-007 — Enforce security continuity (no `.env` reads, no secrets) — AC-7

- **AC**: AC-7
- **Description**: Ensure remote automation docs/rules and command contract explicitly prohibit `.env` reads and secret value output, preserving names-only evidence format.
- **Files**: `.cursor/rules/coding-standards.mdc`, `template/.cursor/rules/coding-standards.mdc`, `docs/engineering/runbook.md`, `template/docs/engineering/runbook.md`
- **Status**: done
- **Acceptance**: Security constraints are explicit and consistent with US-0085/DEC-0071.

## T-008 — Add/extend target resolution regression tests — AC-8

- **AC**: AC-8
- **Description**: Add tests or contract assertions that validate explicit target resolution success/failure and verify existing remote summary behavior remains stable when automation profile is off.
- **Files**: `tests/auto_command_contract_test.py`, `tests/test_remote_config_summary.py` (if needed), `scripts/remote_config_summary.py` (no behavior drift expected)
- **Status**: done
- **Acceptance**: Tests cover pass/fail target resolution cases and mode-off non-regression.

## T-009 — Reconcile architecture lock consistency — AC-9

- **AC**: AC-9
- **Description**: Verify delivery matches `architecture.md` `# US-0086` reason-code vocabulary, key names, and compatibility boundaries with US-0064/DEC-0070.
- **Files**: `docs/engineering/architecture.md`, `docs/engineering/decisions.md`, `docs/product/backlog.md` (notes only if required)
- **Status**: done
- **Acceptance**: No drift between implementation surfaces and locked architecture contracts.

## T-010 — Perform active/template parity sweep — AC-10

- **AC**: AC-10
- **Description**: Execute final parity pass across all touched command/rule/scratchpad/doc surfaces to keep active/template behavior aligned.
- **Files**: active + `template/` counterparts for touched US-0086 surfaces
- **Status**: done
- **Acceptance**: Parity checks pass and no touched active path lacks template equivalent where applicable.
