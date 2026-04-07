# Architecture archive pack (2026-04-06)

- Rollover trigger: `ARCH_HOT_MAX_LINES=3500, ARCH_HOT_MAX_STORY_SECTIONS=120`
- Source: `docs/engineering/architecture.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 34
- First archived heading: `# US-0040: Per-Sprint Release Notes and Release Queue Tracker`
- Last archived heading: `# US-0040: Per-Sprint Release Notes and Release Queue Tracker`
- Verification tuple (mandatory):
  - archived_body_lines=169
  - preamble_lines=10
  - retained_body_lines=3408

---

# US-0040: Per-Sprint Release Notes and Release Queue Tracker

## Overview

US-0040 replaces single mutable release notes with sprint-scoped artifacts and a
canonical queue that tracks each sprint's release lifecycle state. The goal is
to prevent overwrite, preserve history, and make unreleased work visible before
release finalization.

Scope remains workflow/process-level only. No deployment runtime changes.

## Assumption challenge and alternatives

### Option A: Keep single mutable `handoffs/release_notes.md`

Pros:
- No new artifacts or migration.

Cons:
- Fails history preservation and non-overwrite requirements.
- Cannot represent multiple unreleased sprint states deterministically.

### Option B: Keep single file with appended history sections

Pros:
- Preserves one-file discoverability.
- Better history than overwrite model.

Cons:
- Queue state remains implicit and harder to validate.
- High risk of inconsistent section formatting and parsing ambiguity.
- Backfill and partial-release state tracking remain brittle.

### Option C: Per-sprint immutable notes + canonical queue index (chosen)

Pros:
- Deterministic per-sprint history with no cross-sprint overwrite.
- Explicit queue model (`planned -> ready -> unreleased -> released`) per sprint.
- Clear migration and failure-safe semantics.

Cons:
- Adds one queue artifact and compatibility pointer rules.

## Minimal architecture

### 1) Canonical artifacts

Release notes:
- `handoffs/releases/Sxxxx-release-notes.md` (primary, sprint-scoped)

Queue index:
- `handoffs/release_queue.md` (canonical release state tracker)

Backward-compatibility pointer file:
- `handoffs/release_notes.md` remains and is updated as "latest release pointer"
  + compatibility summary (no destructive rewrite of historical sprint notes).

### 2) Queue schema and states

Each queue row records at minimum:
- `sprint_id` (for example `S0010`)
- `story_refs` (one or more `US-xxxx`)
- `status` (`planned|ready|unreleased|released|blocked`)
- `last_updated` (ISO timestamp)
- `release_notes_ref` (`handoffs/releases/Sxxxx-release-notes.md`)
- `gate_snapshot` (test/qa/uat summary or reason code)
- `release_version` (optional until final release)

State semantics:
- `planned`: sprint exists but release flow not yet entered.
- `ready`: verify-work complete and release can be attempted.
- `unreleased`: release flow entered; notes created/updated; finalization not done.
- `released`: release finalization succeeded for that sprint.
- `blocked`: deterministic failure (for example unresolved sprint identity or gate
  failure) with remediation guidance.

### 3) Deterministic transition contract

Only the target sprint row may transition during one `/release` run:

1. Resolve sprint ID from current context.
2. If unresolved:
   - do not write any sprint notes file,
   - do not mutate another sprint's queue row,
   - add/update `blocked` queue entry keyed as `UNKNOWN` with reason code
     (`RELEASE_SPRINT_UNRESOLVED`) and remediation.
3. If resolved:
   - ensure queue row exists (create if missing),
   - set row to `unreleased`,
   - write/update only `handoffs/releases/Sxxxx-release-notes.md`,
   - keep other sprint rows untouched.
4. On successful gate completion + finalization:
   - transition same row `unreleased -> released`,
   - update `release_version`/timestamp,
   - refresh compatibility pointer in `handoffs/release_notes.md`.
5. On failure after notes write:
   - keep row in `unreleased` or `blocked` with reason code,
   - never delete or overwrite other sprint note files.

### 4) Backward compatibility contract

`handoffs/release_notes.md` remains supported and becomes:
- latest release summary for the most recently finalized sprint,
- pointer list to recent per-sprint files,
- explicit note that canonical history lives under `handoffs/releases/`.

Existing workflows reading `handoffs/release_notes.md` continue to work for
"latest release" use cases, while full history is preserved per sprint.

### 5) Migration/backfill contract

One-time migration policy for legacy `handoffs/release_notes.md`:

1. Attempt to resolve sprint identity from legacy file content and state context.
2. If resolvable:
   - create `handoffs/releases/Sxxxx-release-notes.md` using legacy content,
   - preserve original legacy file content (append compatibility pointer section).
3. If not resolvable:
   - keep legacy file unchanged,
   - add queue note in `handoffs/release_queue.md` with `blocked` status and
     reason `LEGACY_NOTES_SPRINT_UNRESOLVED`,
   - include manual migration guidance.

Migration is non-destructive and repeat-safe (idempotent by sprint file existence
check).

### 6) Failure-safe behavior for metadata inconsistency

When queue and notes metadata disagree (missing file, wrong status, missing row):
- fail closed for release finalization (no forced `released` transition),
- preserve existing note artifacts as-is,
- write deterministic reason code in queue row:
  - `QUEUE_ENTRY_MISSING`
  - `NOTES_REF_MISSING`
  - `STATUS_TRANSITION_INVALID`
  - `RELEASE_SPRINT_UNRESOLVED`
- provide remediation steps (rebuild row, restore ref, rerun `/release`).

No automatic destructive reconciliation is allowed.

### 7) Ownership and phase touchpoints

- `/verify-work`: marks sprint release-candidate readiness (`ready`) in state
  context.
- `/release`: owns transitions `ready -> unreleased -> released` and note file
  generation/update for target sprint only.
- `/refresh-context`: curates queue readability, keeps stale blocked entries
  visible, and preserves historical integrity.

### 8) Template parity requirements

Implementation must keep active and `template/` guidance aligned for:
- `.cursor/commands/release.md` (new queue + per-sprint notes semantics)
- related rules/handoff guidance where release artifact paths are referenced
- placeholder artifacts for `handoffs/release_queue.md` and
  `handoffs/releases/` conventions.

## Sprint-plan readiness (decomposition-ready)

Implementation tasks should split into:
1. Add canonical artifact contracts and queue schema docs.
2. Add resolver + fail-safe transition semantics in release guidance.
3. Add migration/backfill steps for legacy `handoffs/release_notes.md`.
4. Add backward-compatible pointer behavior in legacy release notes file.
5. Add QA matrix for unresolved sprint, overwrite prevention, queue-note mismatch,
   migration success/failure, and active/template parity.

---

