---
description: "its-magic release: prepare release notes and runbook updates."
---

# /release

## Subagents
- release

## Execution model
- Run `/release` in a fresh Release subagent context.
- After writing outputs, stop and optionally hand off to `/refresh-context` in a
  new subagent/chat.

## Inputs
- `sprints/Sxxxx/summary.md` (target sprint)
- `sprints/Sxxxx/qa-findings.md` (target sprint)
- `sprints/Sxxxx/uat.json`
- `sprints/Sxxxx/uat.md`
- `docs/engineering/runbook.md`
- `docs/engineering/state.md`
- `handoffs/release_notes.md` (legacy compatibility pointer)
- `handoffs/release_queue.md` (canonical queue tracker)

## Outputs (artifacts)
- `handoffs/releases/Sxxxx-release-notes.md` (canonical per-sprint notes)
- `handoffs/release_queue.md` (canonical queue state)
- `handoffs/release_notes.md`
- `docs/engineering/runbook.md`
- `docs/engineering/state.md`

## Stop conditions
- Deploy command missing for requested environment
- Decision gate triggered
- Sprint identity unresolved
- Queue/notes mismatch detected with no safe auto-remediation

## Canonical release artifacts (US-0040 / DEC-0020)

- Canonical release history is sprint-scoped:
  `handoffs/releases/Sxxxx-release-notes.md`.
- Canonical release state tracker is `handoffs/release_queue.md`.
- Legacy compatibility file `handoffs/release_notes.md` remains supported as a
  latest-release pointer/summary (not canonical history storage).
- Never overwrite release notes for non-target sprints.

## Release queue schema contract

Each queue row must include at minimum:
- `sprint_id`
- `story_refs`
- `status` (`planned|ready|unreleased|released|blocked`)
- `last_updated` (ISO timestamp)
- `release_notes_ref` (`handoffs/releases/Sxxxx-release-notes.md`)
- `gate_snapshot` (gate summary or deterministic reason code)
- `release_version` (optional until finalization)

## Deterministic target-sprint-only transition rules

Allowed transitions per target sprint:
- `planned -> ready -> unreleased -> released`
- `blocked` may be set for deterministic failure conditions.

Strict mutation semantics:
- During one `/release` run, only the target sprint row may be created/updated.
- Do not mutate unrelated sprint rows in `handoffs/release_queue.md`.
- Do not write/update `handoffs/releases/Syyyy-release-notes.md` when target is
  `Sxxxx`.

## Steps
1. Resolve target sprint identity from current sprint context.
   - If unresolved, fail closed:
     - do not write any sprint-scoped notes file,
     - do not mutate another sprint queue row,
     - record/update blocked queue row keyed as `UNKNOWN` with reason
       `RELEASE_SPRINT_UNRESOLVED`,
     - include remediation guidance (set explicit sprint context and rerun).
2. Verify sync-policy prerequisite evidence (US-0038):
   - Latest sync verdict must include deterministic evidence fields:
     `phase_boundary`, `policy_mode`, `checks`, `push_decision`, `reason_code`,
     `evidence_refs`.
   - `TEST_COMMAND` baseline evidence is mandatory for any push-eligible path.
   - Optional checks (`LINT_COMMAND`, `TYPECHECK_COMMAND`) are required only when
     configured; missing optional commands must be reported as `skipped`, not fail.
3. Enforce blocker-aware release safety:
   - If unresolved blocking QA findings or unresolved critical issues exist,
     require `no_push` semantics (`BLOCKING_QA_FINDINGS`) and hold release until
     remediation evidence is present.
4. Verify UAT completeness (DEC-0009): confirm all sprint UAT artifacts (`uat.json`,
   `uat.md`) are in populated/verified state per DEC-0009. All steps must have
   recorded results. If any UAT is placeholder or incomplete, block release and
   recommend `/verify-work`.
5. Ensure target queue row exists; set status to `unreleased` before finalization.
   - Create row if missing.
   - Set `release_notes_ref` to target sprint notes path.
   - Keep all non-target rows unchanged.
6. Write/update only target sprint notes at:
   `handoffs/releases/Sxxxx-release-notes.md`.
   - Preserve any existing historical sprint file content unless explicitly
     working on that same sprint.
7. Perform legacy migration/backfill check (one-time, non-destructive):
   - If legacy content exists only in `handoffs/release_notes.md` and target
     sprint can be resolved, backfill target sprint file without deleting legacy.
   - If legacy sprint context is unresolved, keep legacy file unchanged and
     record `LEGACY_NOTES_SPRINT_UNRESOLVED` with manual migration guidance.
   - Migration must be idempotent; do not overwrite existing target sprint notes
     as part of backfill.
8. Run mismatch fail-safe checks before finalization:
   - If queue row missing for resolved sprint: reason `QUEUE_ENTRY_MISSING`.
   - If queue row missing `release_notes_ref`: reason `NOTES_REF_MISSING`.
   - If attempted transition is invalid: reason `STATUS_TRANSITION_INVALID`.
   - For any mismatch: fail closed, preserve existing notes, keep queue in
     `unreleased` or `blocked`, and include remediation guidance.
9. On successful finalization, transition only target sprint:
   `unreleased -> released`.
   - Update `last_updated`, `release_version` (when available), and gate summary.
10. Update backward-compatible legacy file `handoffs/release_notes.md` as
    latest-release pointer and summary:
    - include latest released sprint id,
    - include pointer to canonical sprint-scoped notes file,
    - include visibility section for unreleased queue entries.
11. Update runbook/state readiness and evidence references for release outcome.
12. If `AUTO_RELEASE_NOTES=1` in `.cursor/scratchpad.md`, generation logic must
    still target sprint-scoped notes first and update legacy pointer second.

## Fail-safe reason codes and remediation guidance

Required deterministic reason codes:
- `RELEASE_SPRINT_UNRESOLVED`
- `LEGACY_NOTES_SPRINT_UNRESOLVED`
- `QUEUE_ENTRY_MISSING`
- `NOTES_REF_MISSING`
- `STATUS_TRANSITION_INVALID`

When any reason code is emitted:
- Preserve existing release note artifacts (non-destructive default).
- Do not auto-reconcile by deleting/rebuilding unrelated sprint history.
- Provide actionable remediation steps and require rerun after correction.

