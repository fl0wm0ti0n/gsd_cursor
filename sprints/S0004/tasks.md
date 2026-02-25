# Tasks — Sprint S0004

## T-001: Add `/memory-audit` command definition (active + template)
- Story: US-0024
- Status: pending
- Files: `.cursor/commands/memory-audit.md`, `template/.cursor/commands/memory-audit.md`
- Description: Create the command contract with read-only behavior, explicit
  output artifact path, non-blocking execution semantics, and phase usage
  guidance.
- AC covered: AC-1, AC-5

## T-002: Define report format and severity taxonomy in command flow
- Story: US-0024
- Status: pending
- Files: `.cursor/commands/memory-audit.md`, `template/.cursor/commands/memory-audit.md`
- Description: Specify required report sections (timestamp/scope, severity
  summary, findings table, recommended actions) and write contract for
  `docs/engineering/memory-drift-report.md`.
- AC covered: AC-2, AC-5

## T-003: Implement detection coverage guidance and evidence rules
- Story: US-0024
- Status: pending
- Files: `.cursor/commands/memory-audit.md`, `template/.cursor/commands/memory-audit.md`
- Description: Encode minimum checks for (1) changed code without artifact
  updates, (2) unresolved decision TODOs/gates, (3) sprint/story status mismatch
  vs repository signals, with evidence expectations for each finding.
- AC covered: AC-3

## T-004: Enforce US-0024 vs US-0017 scope boundary in output
- Story: US-0024
- Status: pending
- Files: `.cursor/commands/memory-audit.md`, `template/.cursor/commands/memory-audit.md`
- Description: Add explicit report split: "Memory drift findings" (this story)
  and "Template drift findings (reference-only)" with routing note to US-0017.
- AC covered: AC-4

## T-005: Document operator usage in README and runbook (active + template)
- Story: US-0024
- Status: pending
- Files: `README.md`, `template/README.md`, `docs/engineering/runbook.md`, `template/docs/engineering/runbook.md`
- Description: Document when to run `/memory-audit` (pre-handoff, pre-QA,
  pre-release), how to interpret severity/advisory output, and follow-up command
  paths (`/refresh-context`, `/sprint-plan`, `/verify-work`, `/intake`).
- AC covered: AC-6, AC-5

## T-006: Add regression checks for command/doc presence and boundary wording
- Story: US-0024
- Status: pending
- Files: `tests/run-tests.ps1`, `tests/run-tests.sh`
- Description: Extend test scripts with lightweight checks that `/memory-audit`
  command files exist, docs mention usage timing, and template-drift concerns are
  routed to US-0017 wording.
- AC covered: AC-4, AC-6

## Implementation order and constraints
- Execute strictly in task order T-001 -> T-006.
- Keep active and template files aligned in the same task where both exist.
- Do not add US-0017 remediation automation in this sprint; only classify and
  route template drift findings.
- Do not mutate source/workflow/sprint artifacts from within `/memory-audit`
  behavior definition.
