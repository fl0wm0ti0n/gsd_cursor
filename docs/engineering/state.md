# Engineering State

## Execute checkpoint (2026-02-26) — S0012 / US-0040

- Sprint `S0012` (`US-0040`) is DEV COMPLETE.
- `/release` guidance now defines canonical sprint-scoped notes at
  `handoffs/releases/Sxxxx-release-notes.md` with strict target-sprint-only
  write semantics.
- Canonical release queue tracker contract is established at
  `handoffs/release_queue.md` with required schema fields and deterministic
  `ready -> unreleased -> released` transition model.
- Fail-safe reason-code semantics are defined and aligned across release
  command, queue artifact, and runbook:
  `RELEASE_SPRINT_UNRESOLVED`, `LEGACY_NOTES_SPRINT_UNRESOLVED`,
  `QUEUE_ENTRY_MISSING`, `NOTES_REF_MISSING`, `STATUS_TRANSITION_INVALID`.
- Legacy `handoffs/release_notes.md` is preserved as backward-compatible
  latest-pointer/summary, with explicit unreleased queue visibility guidance.
- Active/template parity completed for touched release command, rules, runbook,
  README, and new handoff artifacts.
- Validation evidence: `tests/run-tests.ps1` PASS with `Pass=142`, `Fail=0`
  (`tests/report.md`, timestamp `2026-02-25T23:11:21Z`).

## QA checkpoint (2026-02-26) — S0012 / US-0040

- Sprint `S0012` (`US-0040`) passed `/qa`.
- Fresh automated QA evidence: `tests/run-tests.ps1` exit code `0`,
  `tests/report.md` timestamp `2026-02-25T23:25:52Z` (`Pass=142`, `Fail=0`).
- Acceptance criteria AC-1..AC-9 verified PASS with no contract gaps:
  - non-overwriting sprint-scoped notes path contract
  - canonical release queue existence and deterministic status transitions
  - target-row-only mutation semantics
  - unresolved-sprint and mismatch fail-safe reason-code handling
  - non-destructive/idempotent migration-backfill semantics
  - backward-compatible legacy `handoffs/release_notes.md` pointer behavior
  - active/template parity for release command/rules/handoffs/runbook/readme
- No blocking findings and no non-blocking findings in
  `sprints/S0012/qa-findings.md`.
- Handoff updated in `handoffs/qa_to_dev.md`; next phase is `/verify-work`.

## Verify-work checkpoint (2026-02-26) — S0012 / US-0040

- Sprint `S0012` (`US-0040`) passed `/verify-work`.
- UAT artifacts are finalized and consistent:
  `sprints/S0012/uat.json` and `sprints/S0012/uat.md` (`Passed: 9`, `Failed: 0`,
  `Total: 9`).
- Verify-work outcome: PASS (`US-0040` AC-1..AC-9 each mapped to executed UAT
  steps with PASS results and evidence references).
- Decision gate status: not triggered (no blockers).
- Pre-handoff traceability check: complete; story-to-sprint-to-evidence linkage
  is explicit for `US-0040` across `sprints/S0012/summary.md`,
  `sprints/S0012/qa-findings.md`, `sprints/S0012/uat.json`,
  `sprints/S0012/uat.md`, and `tests/report.md`.

## Release checkpoint (2026-02-26) — S0012 / US-0040

- Sprint `S0012` (`US-0040`) passed `/release` gates and was finalized as
  `released`.
- Canonical sprint-scoped release notes were created first at
  `handoffs/releases/S0012-release-notes.md` (`AUTO_RELEASE_NOTES=1` ordering
  respected), then legacy pointer `handoffs/release_notes.md` was updated.
- Canonical queue row for `S0012` is present in `handoffs/release_queue.md` and
  now set to `released` after deterministic target-row-only transition.
- Existing gates and evidence checks passed:
  - mandatory `TEST_COMMAND` is configured in `docs/engineering/runbook.md`
  - mandatory test evidence is present and passing in `tests/report.md`
  - QA safety check is PASS with no unresolved blockers/criticals
  - UAT completeness/pass is confirmed (`9 passed`, `0 failed`)
- Mismatch fail-safe checks executed with no blocking outcome:
  `RELEASE_SPRINT_UNRESOLVED`, `LEGACY_NOTES_SPRINT_UNRESOLVED`,
  `QUEUE_ENTRY_MISSING`, `NOTES_REF_MISSING`, `STATUS_TRANSITION_INVALID`.

## Sprint-plan checkpoint (2026-02-26)

- Sprint `S0012` is planned for `US-0040` (Per-Sprint Release Notes and Release
  Queue Tracker).
- Sizing policy check:
  - `SPRINT_MAX_TASKS=12`
  - `SPRINT_AUTO_SPLIT=1`
  - Planned tasks: 11 (`<= 12`)
  - Split decision: not required (single-story sprint remains atomic with
    migration and negative-path coverage included).
- Milestone activation check: not applicable (no active milestone lifecycle
  context declared for `US-0040`).
- Planning artifacts are created and ready for `/execute` handoff:
  `sprints/S0012/sprint.md`, `tasks.md`, `progress.md`, `uat.json`, `uat.md`,
  `plan-verify.json`.
- Plan-verify result: PASS with explicit AC-1..AC-9 coverage and no gaps in
  `sprints/S0012/plan-verify.json`.

## Sprint-plan checkpoint (2026-02-25)

- Planned sequential sprints for `US-0038` and `US-0039`:
  - `S0010` -> `US-0038` (Phase-Triggered Sync Policy with Guarded Auto-Push)
  - `S0011` -> `US-0039` (Release Gate Tightening for Check-In Tests and QA/UAT Completion)
- Split rationale: combined scope would exceed atomic, testable planning under
  `SPRINT_MAX_TASKS=12` once mandatory negative-path coverage and template parity
  tasks are included.
- `S0010` task count: 11 (`<= 12`), milestone activation check: not applicable.
- `S0011` task count: 11 (`<= 12`), milestone activation check: not applicable.
- Both sprint plans pass plan-verify with explicit AC mapping and no coverage
  gaps in `sprints/S0010/plan-verify.json` and `sprints/S0011/plan-verify.json`.

## Execute checkpoint (2026-02-25) — S0010 / US-0038

- Sprint `S0010` (`US-0038`) is DEV COMPLETE.
- Canonical sync policy contract delivered with default-safe settings:
  `SYNC_POLICY_MODE=manual`, `ALLOW_AUTO_PUSH=0`.
- Guarded auto-push semantics documented and aligned:
  phase-boundary-only evaluation, QA-first denial, blocker-aware denial, branch
  deny-by-default + explicit allowlist.
- Mandatory pre-push gate implemented in both validate scripts:
  `TEST_COMMAND` required; missing/failing/timed-out test blocks push.
- Optional check behavior clarified: `LINT_COMMAND` and `TYPECHECK_COMMAND` run
  only when configured; otherwise deterministic `skipped` reporting.
- Sync reason-code/evidence schema is documented in runbook, command guidance,
  and QA handoff artifacts.
- Active/template parity completed for all touched guidance/config files.

## QA checkpoint (2026-02-25) — S0010 / US-0038

- Sprint `S0010` (`US-0038`) passed `/qa`.
- Automated QA evidence: `tests/run-tests.ps1` exit code `0`,
  `tests/report.md` timestamp `2026-02-25T21:59:17Z` (`Pass=117`, `Fail=0`).
- Acceptance criteria AC-1..AC-10 verified PASS with no contract gaps:
  policy modes/default-safe behavior, guarded auto-push prerequisites,
  QA-first/blocker constraints, branch allowlist safety, mandatory test baseline,
  optional lint/typecheck semantics, reason-code/evidence observability, and
  active/template parity.
- No blocking findings and no non-blocking findings in
  `sprints/S0010/qa-findings.md`.
- Handoff updated in `handoffs/qa_to_dev.md`; next phase is `/verify-work`.

## Verify-work checkpoint (2026-02-25) — S0010 / US-0038

- Sprint `S0010` (`US-0038`) passed `/verify-work`.
- UAT evidence is populated and consistent in `sprints/S0010/uat.json` and
  `sprints/S0010/uat.md` (`Passed: 10`, `Failed: 0`, `Total: 10`).
- Verify-work outcome: PASS (`US-0038` AC-1..AC-10 mapped to executed UAT steps
  with PASS results and evidence references).
- Decision gate status: not triggered (no blockers).
- Pre-handoff traceability check: complete; story-to-sprint-to-evidence linkage
  is explicit for `US-0038` across `summary.md`, `qa-findings.md`, `uat.json`,
  `uat.md`, and `tests/report.md`.
- Handoff is ready for `/release` via `handoffs/release_notes.md`.

## Release checkpoint (2026-02-25) — S0010 / US-0038

- Sprint `S0010` (`US-0038`) passed `/release` gates and is release-ready.
- Deterministic gate order verified:
  1) check-in test baseline, 2) QA completion, 3) UAT completeness, 4) release
  finalization.
- Mandatory test evidence is present and passing:
  `tests/report.md` (`Timestamp: 2026-02-25T21:59:17Z`, `Pass=117`, `Fail=0`).
- QA safety gate is clear:
  `sprints/S0010/qa-findings.md` reports `PASS` with no blocking findings.
- UAT completeness gate is clear:
  `sprints/S0010/uat.json` + `sprints/S0010/uat.md` are populated and consistent
  (`10/10` pass, `0` fail).
- US-0038 sync-policy prerequisite evidence fields are confirmed in release
  context (`phase_boundary`, `policy_mode`, `checks`, `push_decision`,
  `reason_code`, `evidence_refs`) via `docs/engineering/runbook.md`.
- Release notes finalized in `handoffs/release_notes.md`.

## Sprint-plan checkpoint (2026-02-25)

- Sprint `S0009` is planned for `US-0037` (Mid-Process `/auto` Continuation with
  Deterministic Resume Point).
- Task plan includes 9 tasks with explicit AC-1..AC-9 mapping and no coverage
  gaps in `sprints/S0009/plan-verify.json`.
- Milestone check was executed and marked not applicable for this sprint.
- Planning artifacts are created and ready for `/execute` handoff.

## Execute checkpoint (2026-02-25)

- Sprint `S0009` (`US-0037`) implementation completed in process-contract scope.
- `/auto` now defines canonical `start-from=<phase>` and deterministic precedence:
  argument > `resume_brief` > conservative `state` fallback > fail-fast.
- Conflict, stale, unparseable, and ambiguous resume handling now uses
  `[AUTO_RESUME_ERROR]` code contract with explicit remediation guidance.
- `/pause`, `/resume`, and `/auto` guidance is aligned for continuation
  semantics and breadcrumb observability.
- Existing stop conditions and decision gates are preserved in continuation mode.
- Active/template parity updated for affected command/rule/doc files.

## Verify-work checkpoint (2026-02-25)

- Sprint `S0009` (`US-0037`) passed `/verify-work`.
- UAT evidence is populated and consistent in `sprints/S0009/uat.json` and
  `sprints/S0009/uat.md` (`Passed: 9`, `Failed: 0`, `Total: 9`).
- Verify-work outcome: PASS (`US-0037` AC-1..AC-9 mapped to executed UAT steps
  with PASS results and evidence references).
- Decision gate status: not triggered (no blockers).
- Pre-handoff traceability check: complete; story-to-sprint-to-evidence linkage
  is explicit for `US-0037` across `summary.md`, `qa-findings.md`, `uat.json`,
  `uat.md`, and `tests/report.md`.
- Handoff is ready for `/release` via `handoffs/release_notes.md`.

## QA checkpoint (2026-02-25)

- Sprint `S0008` (`US-0036`) passed `/qa`.
- QA evidence is recorded in `sprints/S0008/qa-findings.md` and `tests/report.md`
  (`Pass: 77`, `Fail: 0`).
- No blockers found; handoff to `/verify-work` is ready.

## Pause checkpoint (2026-02-25)

- Workflow paused cleanly after S0008 dev completion.
- Active sprint is `S0008` (`US-0036`): all tasks T-001..T-010 are done and
  evidence artifacts are updated.
- Current boundary is handoff-ready for `/qa`; no additional execute-phase work
  is required before QA verification starts.

## Session status

S0010 release gates PASS for US-0038; sprint is release-ready with finalized
notes. S0011 remains PLANNED for US-0039. S0009 verify-work remains PASS for
US-0037 and ready for `/release`.
- Validation evidence: `tests/run-tests.ps1` passed with `Pass=117`, `Fail=0`
  (`tests/report.md`, timestamp `2026-02-25T21:59:17Z`).

Planning outcomes:
- Deterministic continuation semantics are decomposed into sprint tasks with
  explicit AC coverage (`T-001`..`T-009`).
- Resolver precedence, conflict/staleness fail-fast policy, and
  `[AUTO_RESUME_ERROR]` contract are included as planning scope.
- UAT planning explicitly covers precedence ordering, stale/conflict handling,
  and fail-fast error-code verification for resume resolution.
- Breadcrumb observability and stop-condition preservation are explicitly
  planned.
- `/pause`, `/resume`, and `/auto` alignment plus README/runbook updates are
  planned to cover user-facing behavior changes.
- Active/template parity is included as a first-class sprint deliverable.

## Progress snapshot

- US-0018 (Smart Upgrade Mode): implemented, S0001 complete
- US-0015 (Document empty runbook commands): done in README
- US-0019 (Clean placeholder content): done
- US-0020 (/ask command): implemented, S0002 complete
- US-0021 (Critical evaluation): implemented, S0002 complete
- US-0022 (Sprint sizing + scratchpad config): implemented, S0002 complete
- US-0023 (fresh subagent context per phase + /auto orchestration): implemented,
  S0003 QA complete (pass)
- US-0024 (Memory Drift Audit Command): implemented, S0004 QA pass
- US-0025 (Backlog-to-Sprint Traceability Contract): implemented, S0005 dev complete
- US-0026 (Milestone Lifecycle Definition and Exit Criteria): implemented, S0005 dev complete
- US-0027 (UAT Artifact Lifecycle and Ownership): implemented, S0005 dev complete
- US-0028 (Security & Compliance Review Agent): implemented, S0007 verify-work PASS

## Architecture decisions (this cycle)

- DEC-0011: Research entry format — semi-structured R-xxxx IDs with minimal
  required fields (id, date, topic). Optional enrichment (sources, confidence,
  linked stories, status). Knowledge base in research.md.
- DEC-0012: Security review as dedicated 7th agent role (security.mdc), not
  augmented behavior on existing agents. Flag-controlled, zero overhead when
  disabled.

## Architecture approach summary

- **US-0029**: Early web research integrated as optional sub-step in `/intake`
  (PO) and `/architecture` (TL), controlled by `EARLY_RESEARCH=1` flag.
  `/research` command output restructured to R-xxxx entries. research.md
  migrated to structured format. Curator scope expanded for knowledge base
  maintenance (freshness, dedup, pruning). 16 files affected (8 active + 8
  template copies).
- **US-0028**: New 7th agent role (`security.mdc`) with `/security-review`
  command (two modes: design review post-architecture, code review post-execute).
  `SECURITY_REVIEW=0` and `COMPLIANCE_PROFILES=` scratchpad flags. Compliance
  profiles are prompt-embedded checklists (GDPR, SOC2, HIPAA, PCI-DSS,
  ISO27001). Critical findings create DEC-xxxx records and trigger decision
  gates. 13 files affected (7 active + 6 template copies).

## Traceability Index

Per DEC-0010, this table maps every story to its sprint, tasks, status, and evidence.

| Story | Sprint | Tasks | Status | Evidence |
|-------|--------|-------|--------|----------|
| US-0018 | S0001 | T-001..T-011 | DONE | S0001/summary.md, S0001/uat.json |
| US-0015 | S0001 | T-011 | DONE | S0001/summary.md |
| US-0020 | S0002 | T-001..T-002 | DONE | S0002/summary.md |
| US-0021 | S0002 | T-003..T-006 | DONE | S0002/summary.md |
| US-0022 | S0002 | T-004, T-007..T-008 | DONE | S0002/summary.md |
| US-0023 | S0003 | T-001..T-006 | DONE | S0003/summary.md |
| US-0024 | S0004 | T-001..T-006 | DONE | S0004/summary.md, S0004/qa-findings.md |
| US-0025 | S0005 | T-001..T-003 | DONE | S0005/summary.md |
| US-0027 | S0005 | T-004..T-006 | DONE | S0005/summary.md |
| US-0026 | S0005 | T-007..T-009 | DONE | S0005/summary.md |
| US-0029 | S0006 | T-001..T-010 | DONE | S0006/summary.md |
| US-0028 | S0007 | T-001..T-010 | PASS | S0007/uat.json, S0007/uat.md, S0007/summary.md, S0007/qa-findings.md |
| US-0036 | S0008 | T-001..T-010 | PASS | S0008/summary.md, S0008/qa-findings.md, S0008/uat.json, S0008/uat.md |
| US-0037 | S0009 | T-001..T-009 | PASS | S0009/summary.md, S0009/qa-findings.md, S0009/uat.json, S0009/uat.md, tests/report.md |
| US-0038 | S0010 | T-001..T-011 | PASS | S0010/summary.md, S0010/qa-findings.md, S0010/uat.json, S0010/uat.md, tests/report.md |
| US-0039 | S0011 | T-001..T-011 | PLANNED | S0011/sprint.md, S0011/tasks.md, S0011/plan-verify.json |
| US-0040 | S0012 | T-001..T-011 | PASS | S0012/summary.md, S0012/qa-findings.md, S0012/uat.json, S0012/uat.md, tests/report.md |

## Known issues

- AC-6 (upgrade from pre-version repos) deferred — repos without
  `.its-magic-version` show "upgrading from vunknown"

## Key risks

- US-0021 AC-7 behavioral: evaluation is constructive per rule text, but only
  testable by running /intake with a weak/duplicate idea
- US-0022 AC-4 advisory: new idea routing is guidance in the command, not
  programmatically enforced
- US-0023 behavioral: fresh-context model is defined in artifacts and role
  contracts; real isolation still depends on executing commands with fresh
  subagent sessions
- US-0024: detection checks are guidance-based; actual drift detection quality
  depends on agent thoroughness when running `/memory-audit`
- US-0025/0026/0027: all three stories are guidance/documentation changes, not
  hard enforcement. Effectiveness depends on AI reading and following the
  updated command steps and lifecycle rules.

## Next actions

1. Run `/release` for `S0009` (`US-0037`) using finalized verify-work evidence.
2. Keep `tests/report.md` green as continuation semantics evolve.
3. Maintain active/template parity as continuation guidance evolves.

---

## Session status (US-0034 and US-0035 architecture)

- `/architecture` completed for `US-0034` and `US-0035` with concrete, optional
  workflow-level design.
- Manifest topology finalized as hybrid model (global registry + local repo and
  component manifests) with compatibility links and contract-change signals.
- Component-scoped mode finalized with declarative target/non-target scope,
  protection checks, and explicit decision-gate triggers.
- Decision records created: `DEC-0013`, `DEC-0014`, `DEC-0015`.
- Defaults remain non-blocking/off unless enabled (`CROSS_REPO_OBSERVABILITY=0`,
  `COMPONENT_SCOPE_MODE=0`).

## Next actions (for sprint planning readiness)

1. Run `/sprint-plan` for `US-0034` and create tasks for:
   manifest artifacts, compatibility signal/report artifacts, and gate checks.
2. Run `/sprint-plan` for `US-0035` and create tasks for:
   component scope declaration artifacts, task tagging contract, QA protection
   checklist, and out-of-scope gate flow.
3. Add required scratchpad flags and command/rule references in active +
   `template/` copies during implementation to satisfy parity ACs.

---

## Session status (US-0036 architecture)

- `/architecture` completed for `US-0036` with a concrete process-level design.
- Canonical remote config contract defined at `.cursor/remote.json` with parity
  requirement for `template/.cursor/remote.json`.
- Mode-aware validation finalized: fail-fast checks apply only when
  `REMOTE_EXECUTION=1`; remote-disabled mode remains zero-overhead.
- Actionable error message contract defined (path, expected, actual, fix).
- Security model finalized: no committed secrets in config, environment-variable
  references for sensitive values only.
- Decision record created: `DEC-0016`.

## Next actions (US-0036 sprint-plan readiness)

1. Create active + template `.cursor/remote.json` artifacts with safe placeholder
   examples (at least local docker + remote VM/SSH target).
2. Update `README.md` and `docs/engineering/runbook.md` with schema, setup, and
   mode-specific behavior (`REMOTE_EXECUTION=0|1`).
3. Implement validation guidance in command/rule touchpoints with fail-fast
   semantics only for remote-enabled mode.
4. Define/verify error messages for missing file, malformed JSON, invalid field
   values, and secret-like inline values.
5. Run parity verification across active/template references and documentation.

---

## Session status (US-0037 architecture)

- `/architecture` completed for `US-0037` with a concrete, minimal
  continuation-control model.
- Deterministic start-phase precedence finalized:
  1) explicit `/auto start-from=<phase>`
  2) `handoffs/resume_brief.md`
  3) conservative `docs/engineering/state.md` fallback
  4) fail-fast on ambiguity/conflict/unrecoverable inputs.
- Conflict/staleness policy defined: no silent guessing, structured
  `[AUTO_RESUME_ERROR]` contract with remediation guidance.
- One-command continuation defined across remaining phases with existing stop
  conditions preserved (decision gate, missing input, pause request, loop max).
- Breadcrumb observability contract defined for start source, resolved phase,
  and stop reason in `state.md` and `resume_brief.md`.
- Decision record created: `DEC-0017`.

## Next actions (US-0037 sprint-plan readiness)

1. Break implementation into resolver/validation, conflict policy, breadcrumb
   writing, and command-alignment tasks.
2. Update `/auto`, `/resume`, and `/pause` guidance to apply one deterministic
   continuation semantics contract.
3. Add QA scenarios for explicit override, resume-brief precedence, state
   fallback, stale/conflict fail-fast, and stop-reason breadcrumb verification.
4. Include active + `template/` parity tasks in sprint scope.

---

## Session status (US-0038 and US-0039 architecture)

- `/architecture` completed for `US-0038` and `US-0039` with concrete,
  workflow-level safety defaults and deterministic gate contracts.
- `US-0038` finalized:
  - sync control model (`disabled|manual|by_phase|by_milestone|custom_phase_list`)
  - phase-boundary-only eligibility evaluation
  - guarded auto-push semantics (QA-first, branch safety deny-by-default,
    mandatory `TEST_COMMAND` pre-push baseline)
  - deterministic sync reason-code + evidence format.
- `US-0039` finalized:
  - deterministic release gate order:
    check-in tests -> QA completion -> UAT completion -> release finalization
  - mandatory evidence prerequisites per gate
  - no default bypass; explicit decision-gate override path only.
- Decision records created: `DEC-0018` and `DEC-0019`.

## Architecture readiness

- Ready for immediate `/sprint-plan` decomposition.
- Scope remains process/workflow-level (no runtime orchestrator change).
- Existing stop conditions and decision gates are preserved by design.
- Manual mode behavior is preserved and remains non-disruptive by default.
- Template parity remains a mandatory implementation requirement.

## Next actions (US-0038/US-0039 sprint-plan readiness)

1. Create sprint tasks for sync-policy schema, branch safety constraints,
   pre-push check-chain semantics, and sync evidence reason codes.
2. Create sprint tasks for release gate ordering, evidence freshness checks,
   QA/UAT prerequisite validation, and explicit override-path documentation.
3. Align command/docs artifacts (`/execute`, `/qa`, `/release`, `/auto`,
   runbook notes, validate-and-push scripts) to a single gate vocabulary.
4. Add QA regression matrix covering positive/negative/stale-evidence cases
   for sync and release gates.
5. Include active + `template/` parity checks as explicit done criteria.

---

## Session status (US-0040 architecture)

- `/architecture` completed for `US-0040` with concrete, minimal process-level
  design.
- Release notes model finalized as sprint-scoped immutable artifacts at
  `handoffs/releases/Sxxxx-release-notes.md` to prevent cross-sprint overwrite.
- Canonical release queue model finalized at `handoffs/release_queue.md` with
  deterministic statuses:
  `planned|ready|unreleased|released|blocked`.
- Deterministic transition contract finalized:
  target sprint only, with `ready -> unreleased -> released` progression and
  fail-closed behavior when sprint resolution or metadata consistency fails.
- Backward compatibility finalized:
  `handoffs/release_notes.md` remains supported as latest-release pointer/summary.
- Non-destructive migration/backfill finalized for legacy
  `handoffs/release_notes.md` with resolvable vs unresolved sprint handling.
- Decision record created: `DEC-0020`.

## Architecture readiness

- Ready for immediate `/sprint-plan` decomposition.
- Scope remains workflow/process-level only; no deployment-system rewrite.
- Defaults remain safe and non-destructive:
  unresolved sprint context cannot overwrite historical notes.
- Queue/notes inconsistency policy is fail-safe by design with explicit reason
  codes and remediation guidance.
- Template parity remains mandatory for all release guidance and artifact
  conventions.

## Next actions (US-0040 sprint-plan readiness)

1. Add sprint tasks for queue artifact contract, state transitions, and
   target-sprint-only mutation guarantees.
2. Add sprint tasks for per-sprint release note pathing and overwrite-prevention
   behavior.
3. Add sprint tasks for legacy migration/backfill logic and unresolved-legacy
   manual guidance path.
4. Update release command/rules/docs for backward-compatible
   `handoffs/release_notes.md` pointer behavior.
5. Add QA matrix for unresolved sprint identity, partial failure after notes
   write, queue/notes mismatch recovery, migration idempotency, and
   active/template parity.
