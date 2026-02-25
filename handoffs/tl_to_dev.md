# TL -> Dev Handoff — Sprint S0012 (US-0040 Release Notes Queue)

## Sprint Overview

Sprint S0012 is planned for US-0040: Per-Sprint Release Notes and Release Queue
Tracker.

- Story count: 1 (`US-0040`)
- Planned tasks: 11
- Sizing: within limit (`SPRINT_MAX_TASKS=12`)
- Split decision: not required (single-story sprint remains atomic)
- Milestone activation: not applicable

## Architecture and Decision References

- Story acceptance: `docs/product/backlog.md` (US-0040 AC-1..AC-9)
- Architecture: `docs/engineering/architecture.md` (US-0040 section)
- Decision: `decisions/DEC-0020.md`
- Sprint artifacts: `sprints/S0012/*`

## Execution Order

Execute tasks T-001 through T-011 sequentially.

| Task | Description | Files | AC |
|------|-------------|-------|----|
| T-001 | Define canonical per-sprint immutable release notes path and target-sprint-only write semantics | `.cursor/commands/release.md`, `handoffs/releases/Sxxxx-release-notes.md` | AC-1 |
| T-002 | Define canonical release queue tracker schema and required fields | `.cursor/commands/release.md`, `handoffs/release_queue.md`, `docs/engineering/runbook.md` | AC-2 |
| T-003 | Define deterministic queue transitions (`ready -> unreleased -> released`) for target sprint only | `.cursor/commands/release.md`, `docs/engineering/state.md` | AC-3 |
| T-004 | Define unresolved sprint fail-safe behavior and deterministic reason codes | `.cursor/commands/release.md`, `handoffs/release_queue.md`, `docs/engineering/state.md` | AC-4 |
| T-005 | Define non-destructive legacy migration/backfill for `handoffs/release_notes.md` | `.cursor/commands/release.md`, `handoffs/release_notes.md`, `handoffs/releases/Sxxxx-release-notes.md` | AC-5 |
| T-006 | Define backward-compatible legacy latest-pointer/summary behavior | `handoffs/release_notes.md`, `.cursor/commands/release.md` | AC-6 |
| T-007 | Define queue/notes mismatch fail-safe handling and remediation contract | `.cursor/commands/release.md`, `handoffs/release_queue.md`, `docs/engineering/state.md` | AC-4, AC-7 |
| T-008 | Define unreleased queue visibility in readiness and release reporting | `.cursor/commands/release.md`, `docs/engineering/state.md`, `handoffs/release_notes.md` | AC-7 |
| T-009 | Align ownership/touchpoints across verify-work, release, refresh-context guidance | `.cursor/commands/release.md`, `.cursor/rules/core.mdc`, `.cursor/rules/handoffs.mdc`, `docs/engineering/runbook.md` | AC-8 |
| T-010 | Enforce active/template parity for release queue and per-sprint note semantics | `template/.cursor/commands/release.md`, `template/.cursor/rules/core.mdc`, `template/.cursor/rules/handoffs.mdc`, `template/docs/engineering/runbook.md` | AC-9 |
| T-011 | Plan positive/negative/migration/parity regression matrix in sprint UAT artifacts | `sprints/S0012/uat.md`, `sprints/S0012/uat.json`, `sprints/S0012/plan-verify.json` | AC-1, AC-3, AC-4, AC-5, AC-6, AC-7, AC-9 |

## Critical Requirements to Preserve

1. Release notes must be sprint-scoped and never overwrite another sprint's
   note artifact.
2. Queue transitions must only mutate the target sprint row during one release
   run.
3. Unresolved sprint identity and queue/notes mismatch must fail closed with
   deterministic reason codes and remediation guidance.
4. Legacy `handoffs/release_notes.md` must remain backward-compatible while
   canonical history moves to sprint-scoped files.
5. Migration/backfill must be non-destructive and idempotent.
6. Unreleased queue entries must be visible before release finalization.
7. Active/template guidance must remain behaviorally aligned.

## QA and Validation Focus

Required verification scenarios:
- target-sprint write-only behavior for per-sprint notes
- cross-sprint overwrite prevention
- queue required-field and transition correctness
- unresolved sprint fail-safe behavior with reason codes
- queue/notes mismatch fail-safe behavior
- legacy migration success and unresolved-manual path
- migration idempotency
- backward-compatible legacy pointer behavior
- unreleased queue visibility before finalization
- active/template parity checks

## Constraints

- Keep scope strictly to US-0040 process/artifact behavior.
- Do not introduce deployment runtime changes.
- Keep migration/backfill and mismatch handling non-destructive by default.
- Maintain explicit AC traceability with no plan-verify coverage gaps.

## Done Criteria for Dev Completion

- All 11 tasks in `sprints/S0012/tasks.md` are marked done.
- No uncovered US-0040 acceptance criteria in `sprints/S0012/plan-verify.json`.
- `sprints/S0012/progress.md`, `uat.json`, and `uat.md` are updated with
  execution evidence.
- `docs/engineering/state.md` traceability row advances from `PLANNED` to the
  next lifecycle state with evidence references.

# TL -> Dev Handoff — S0010 + S0011 (US-0038 + US-0039)

## Planning summary

- Sprint split executed per sizing policy (`SPRINT_MAX_TASKS=12`,
  `SPRINT_AUTO_SPLIT=1`):
  - `S0010` for `US-0038` with 11 tasks
  - `S0011` for `US-0039` with 11 tasks
- Split rationale: the combined two-story plan would exceed atomic task design
  once required negative-path testing and template parity work is included.
- Milestone activation check: not applicable for both sprints (no active
  milestone context declared).

## S0010 — US-0038 execution focus

- Goal: deliver policy-driven sync cadence and guarded auto-push semantics.
- Required negative paths:
  - disallowed auto-push on protected/default branch without allowlist
  - disallowed auto-push on failed/missing/timed-out `TEST_COMMAND`
  - disallowed auto-push pre-QA and with unresolved QA blockers
- Mandatory outputs: deterministic sync reason codes and evidence fields in
  state/handoff artifacts.
- Script parity: keep `scripts/validate-and-push.ps1` and
  `scripts/validate-and-push.sh` behaviorally aligned with mandatory
  test-before-push gating.

## S0011 — US-0039 execution focus

- Goal: enforce strict release gate chain:
  `check-in test -> QA -> UAT -> release finalization`.
- Required negative paths:
  - block release on missing/stale/failing test evidence
  - block release on unresolved QA blockers
  - block release on incomplete/placeholder UAT
  - verify no-bypass default behavior
- Override path constraint:
  - only via explicit decision gate with rationale and approver evidence
  - release artifacts must include override evidence pointers when used

## AC traceability readiness

- `S0010`: `sprints/S0010/plan-verify.json` covers `US-0038` AC-1..AC-10 with
  no gaps.
- `S0011`: `sprints/S0011/plan-verify.json` covers `US-0039` AC-1..AC-10 with
  no gaps.
- `docs/engineering/state.md` traceability index includes PLANNED rows for
  `US-0038` and `US-0039`.

## Next execution order

1. Execute `S0010` tasks `T-001..T-011`.
2. Run `/qa` and `/verify-work` for `S0010`.
3. Execute `S0011` tasks `T-001..T-011`.
4. Run `/qa` and `/verify-work` for `S0011`.

## Dev completion note (S0010)

- Dev executed `S0010` task sequence `T-001..T-011` and marked all tasks done.
- US-0038 contract updates are completed across command guidance, runbook/README,
  validate-and-push scripts, regression planning artifacts, and template parity.
- Sprint status is now ready for `/qa` with updated `handoffs/dev_to_qa.md`
  checklist and deterministic sync evidence/reason-code expectations.

# TL -> Dev Handoff — Sprint S0009 (US-0037 Auto Continuation)

## Sprint Overview

Sprint S0009 is planned for US-0037: Mid-Process `/auto` Continuation with
Deterministic Resume Point.

- Story count: 1 (`US-0037`)
- Planned tasks: 9
- Sizing: within limit (`SPRINT_MAX_TASKS=12`)
- Split decision: not required (single sprint)
- Milestone activation: not applicable

## Architecture and Decision References

- Story acceptance: `docs/product/backlog.md` (US-0037 AC-1..AC-9)
- Architecture: `docs/engineering/architecture.md` (US-0037 section)
- Decision: `decisions/DEC-0017.md`
- Sprint artifacts: `sprints/S0009/*`

## Execution Order

Execute tasks T-001 through T-009 sequentially.

| Task | Description | Files | AC |
|------|-------------|-------|----|
| T-001 | Define explicit `/auto start-from=<phase>` contract and canonical phase IDs | `.cursor/commands/auto.md` | AC-1 |
| T-002 | Define deterministic resolver precedence and precedence test coverage | `.cursor/commands/auto.md`, `sprints/S0009/uat.md` | AC-2 |
| T-003 | Define conflict/staleness/unparseable fail-fast behavior and `[AUTO_RESUME_ERROR]` codes | `.cursor/commands/auto.md`, `.cursor/rules/core.mdc`, `sprints/S0009/uat.md` | AC-3 |
| T-004 | Define one-command continuation through remaining phases | `.cursor/commands/auto.md` | AC-4 |
| T-005 | Preserve decision gates and stop-condition behavior | `.cursor/commands/auto.md`, `.cursor/rules/core.mdc` | AC-5 |
| T-006 | Define breadcrumb logging contract for `state.md` and `resume_brief.md` | `.cursor/commands/auto.md`, `.cursor/commands/pause.md`, `.cursor/commands/resume.md`, `docs/engineering/state.md`, `handoffs/resume_brief.md` | AC-6 |
| T-007 | Preserve backward compatibility and safe defaults | `.cursor/commands/auto.md`, `.cursor/commands/resume.md` | AC-7 |
| T-008 | Align `/pause`, `/resume`, `/auto` guidance and update README/runbook | `.cursor/commands/auto.md`, `.cursor/commands/resume.md`, `.cursor/commands/pause.md`, `README.md`, `docs/engineering/runbook.md` | AC-8 |
| T-009 | Verify and enforce active/template continuation parity | `template/.cursor/commands/auto.md`, `template/.cursor/commands/resume.md`, `template/.cursor/commands/pause.md`, `template/README.md`, `template/docs/engineering/runbook.md` | AC-9 |

## Critical Requirements to Preserve

1. `/auto start-from=<phase>` accepts only canonical phase IDs.
2. Resolver precedence is deterministic and ordered:
   argument > resume brief > state fallback > fail-fast.
3. Stale/conflicting/unparseable resume inputs must fail fast with actionable
   `[AUTO_RESUME_ERROR]` output (no guessing).
4. Continuation must preserve existing stop conditions and decision-gate rules.
5. Breadcrumbs must make continuation source and stop reason inspectable.
6. Manual/interactive workflows must remain unchanged by default.
7. Active/template guidance must remain behaviorally aligned.

## QA and Validation Focus

Required verification scenarios:
- precedence resolution with explicit argument override
- precedence resolution without argument (resume brief then state fallback)
- conflict case (`resume_brief` vs inferred `state` phase) with fail-fast
- stale/unparseable resume brief fail-fast handling
- `[AUTO_RESUME_ERROR]` code contract coverage
- stop-condition preservation in continuation mode
- breadcrumb field coverage in `state.md` and `resume_brief.md`
- active/template parity checks

## Constraints

- Keep scope strictly to US-0037.
- Planning assumptions must not bypass decision gates or input blockers.
- Maintain 1:1 task-to-AC mapping (`T-001`..`T-009` -> `AC-1`..`AC-9`).
- Keep changes deterministic and testable with explicit remediation guidance.

## Done Criteria for Dev Completion

- All 9 tasks in `sprints/S0009/tasks.md` are marked done.
- No uncovered US-0037 acceptance criteria in `sprints/S0009/plan-verify.json`.
- `sprints/S0009/progress.md`, `uat.json`, and `uat.md` are updated with
  execution evidence.
- Traceability row in `docs/engineering/state.md` advances from `PLANNED` to
  post-execution lifecycle state with evidence links.
# TL -> Dev Handoff — Sprint S0009 (US-0037 Auto Continuation)

## Sprint Overview

Sprint S0009 is planned for US-0037: Mid-Process `/auto` Continuation with
Deterministic Resume Point.

- Story count: 1 (`US-0037`)
- Planned tasks: 9
- Sizing: within limit (`SPRINT_MAX_TASKS=12`)
- Split decision: not required (single sprint)
- Milestone activation: not applicable

## Architecture and Decision References

- Story acceptance: `docs/product/backlog.md` (US-0037 AC-1..AC-9)
- Architecture: `docs/engineering/architecture.md` (US-0037 section)
- Decision: `decisions/DEC-0017.md`
- Sprint artifacts: `sprints/S0009/*`

## Execution Order

Execute tasks T-001 through T-009 sequentially.

| Task | Description | Files | AC |
|------|-------------|-------|----|
| T-001 | Define explicit `/auto start-from=<phase>` contract and canonical phase IDs | `.cursor/commands/auto.md` | AC-1 |
| T-002 | Define deterministic resolver precedence and precedence test coverage | `.cursor/commands/auto.md`, `sprints/S0009/uat.md` | AC-2 |
| T-003 | Define conflict/staleness/unparseable fail-fast behavior and `[AUTO_RESUME_ERROR]` codes | `.cursor/commands/auto.md`, `.cursor/rules/core.mdc`, `sprints/S0009/uat.md` | AC-3 |
| T-004 | Define one-command continuation through remaining phases | `.cursor/commands/auto.md` | AC-4 |
| T-005 | Preserve decision gates and stop-condition behavior | `.cursor/commands/auto.md`, `.cursor/rules/core.mdc` | AC-5 |
| T-006 | Define breadcrumb logging contract for `state.md` and `resume_brief.md` | `.cursor/commands/auto.md`, `.cursor/commands/pause.md`, `.cursor/commands/resume.md`, `docs/engineering/state.md`, `handoffs/resume_brief.md` | AC-6 |
| T-007 | Preserve backward compatibility and safe defaults | `.cursor/commands/auto.md`, `.cursor/commands/resume.md` | AC-7 |
| T-008 | Align `/pause`, `/resume`, `/auto` guidance and update README/runbook | `.cursor/commands/auto.md`, `.cursor/commands/resume.md`, `.cursor/commands/pause.md`, `README.md`, `docs/engineering/runbook.md` | AC-8 |
| T-009 | Verify and enforce active/template continuation parity | `template/.cursor/commands/auto.md`, `template/.cursor/commands/resume.md`, `template/.cursor/commands/pause.md`, `template/README.md`, `template/docs/engineering/runbook.md` | AC-9 |

## Critical Requirements to Preserve

1. `/auto start-from=<phase>` accepts only canonical phase IDs.
2. Resolver precedence is deterministic and ordered:
   argument > resume brief > state fallback > fail-fast.
3. Stale/conflicting/unparseable resume inputs must fail fast with actionable
   `[AUTO_RESUME_ERROR]` output (no guessing).
4. Continuation must preserve existing stop conditions and decision-gate rules.
5. Breadcrumbs must make continuation source and stop reason inspectable.
6. Manual/interactive workflows must remain unchanged by default.
7. Active/template guidance must remain behaviorally aligned.

## QA and Validation Focus

Required verification scenarios:
- precedence resolution with explicit argument override
- precedence resolution without argument (resume brief then state fallback)
- conflict case (`resume_brief` vs inferred `state` phase) with fail-fast
- stale/unparseable resume brief fail-fast handling
- `[AUTO_RESUME_ERROR]` code contract coverage
- stop-condition preservation in continuation mode
- breadcrumb field coverage in `state.md` and `resume_brief.md`
- active/template parity checks

## Constraints

- Keep scope strictly to US-0037.
- Planning assumptions must not bypass decision gates or input blockers.
- Maintain 1:1 task-to-AC mapping (`T-001`..`T-009` -> `AC-1`..`AC-9`).
- Keep changes deterministic and testable with explicit remediation guidance.

## Done Criteria for Dev Completion

- All 9 tasks in `sprints/S0009/tasks.md` are marked done.
- No uncovered US-0037 acceptance criteria in `sprints/S0009/plan-verify.json`.
- `sprints/S0009/progress.md`, `uat.json`, and `uat.md` are updated with
  execution evidence.
- Traceability row in `docs/engineering/state.md` advances from `PLANNED` to
  post-execution lifecycle state with evidence links.
# TL -> Dev Handoff — Sprint S0008 (US-0036 Remote Config Contract)

## Sprint Overview

Sprint S0008 is planned for US-0036: Official Remote Config Template, Docs, and
Fail-Fast Validation.

- Story count: 1 (`US-0036`)
- Planned tasks: 10
- Sizing: within limit (`SPRINT_MAX_TASKS=12`)
- Split decision: not required (single sprint)
- Milestone activation: not applicable

## Architecture and Decision References

- Story acceptance: `docs/product/backlog.md` (US-0036 AC-1..AC-9)
- Architecture: `docs/engineering/architecture.md` (US-0036 section)
- Decision: `decisions/DEC-0016.md`
- Sprint artifacts: `sprints/S0008/*`

## Execution Order

Execute tasks T-001 through T-010 sequentially.

| Task | Description | Files | ACs |
|------|-------------|-------|-----|
| T-001 | Add canonical active remote config template | `.cursor/remote.json` | AC-1, AC-3 |
| T-002 | Add template remote config parity | `template/.cursor/remote.json` | AC-1, AC-9 |
| T-003 | Define schema/contract guidance | `.cursor/commands/execute.md`, `.cursor/rules/core.mdc` | AC-2 |
| T-004 | Define mode-aware validation trigger behavior | `.cursor/commands/execute.md`, `.cursor/rules/core.mdc` | AC-4, AC-6 |
| T-005 | Define actionable fail-fast error format | `.cursor/commands/execute.md`, `.cursor/rules/quality.mdc` | AC-5, AC-4 |
| T-006 | Add security constraints for remote config | `.cursor/rules/coding-standards.mdc`, `.cursor/commands/execute.md` | AC-7 |
| T-007 | Update README remote setup and behavior docs | `README.md` | AC-3, AC-8 |
| T-008 | Update runbook validation guidance | `docs/engineering/runbook.md` | AC-4, AC-5, AC-6, AC-8 |
| T-009 | Plan/add positive + negative QA coverage | `tests/run-tests.ps1`, `tests/run-tests.sh`, `sprints/S0008/uat.md` | AC-4, AC-5, AC-6, AC-7, AC-8, AC-9 |
| T-010 | Final state/traceability and handoff cross-reference update | `docs/engineering/state.md`, `handoffs/tl_to_dev.md` | AC-9 |

## Critical Requirements to Preserve

1. Mode-aware behavior:
   - Validate remote config only when `REMOTE_EXECUTION=1`.
   - Skip remote validation entirely when `REMOTE_EXECUTION=0`.
2. Fail-fast requirement:
   - Missing, malformed, semantically invalid, or insecure config must fail fast
     in remote-enabled mode.
3. Error message contract:
   - Include field/path, expected rule, actual value/type, and remediation hint.
4. Security posture:
   - No committed secrets in `.cursor/remote.json`.
   - Use environment variable references for sensitive values.
5. Parity:
   - Active and `template/` copies must stay behaviorally aligned.
   - README and runbook guidance must not contradict each other.

## QA and Validation Focus

Negative-path coverage is mandatory in this sprint. Ensure test planning includes:
- missing `.cursor/remote.json` with `REMOTE_EXECUTION=1`
- malformed JSON syntax
- invalid enum/type/semantic values (e.g., bad target type, missing required field)
- secret-like inline values in config
- confirmation that `REMOTE_EXECUTION=0` avoids false-fail checks

Positive-path coverage should confirm:
- valid config passes in remote-enabled mode
- example targets and docs references remain consistent across active/template

## Constraints

- Keep scope strictly to US-0036.
- Do not implement remote transport backends or external secret manager logic.
- Keep edits atomic and testable with explicit AC mapping.
- Maintain template parity as a first-class requirement, not a follow-up.

## Done Criteria for Dev Completion

- All 10 tasks in `sprints/S0008/tasks.md` moved from pending to done.
- No uncovered US-0036 acceptance criteria.
- `sprints/S0008/progress.md`, `uat.json`, and `uat.md` updated with execution evidence.
- Traceability row in `docs/engineering/state.md` advanced from `PLANNED` to the
  next lifecycle status with evidence links.

## Dev completion note

Dev execution completed for S0008. All T-001..T-010 tasks are marked done and
the sprint is handed off via `handoffs/dev_to_qa.md` for QA verification.
