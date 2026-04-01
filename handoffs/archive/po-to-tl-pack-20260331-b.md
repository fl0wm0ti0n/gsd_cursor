# PO to TL archive pack (2026-03-31)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 2
- Retained units in hot file: 40
- First archived heading: `## Sprint pointer — BUG-0001 / S0060 (`auto-20260330-01`)`
- Last archived heading: `## Intake Addendum — Non-Overwriting Release Notes + Unreleased Sprint Queue`
- Verification tuple (mandatory):
  - archived_body_lines=55
  - retained_body_lines=769

---

## Sprint pointer — BUG-0001 / S0060 (`auto-20260330-01`)

- **Execute complete** (2026-03-30, dev): **`docs/engineering/state.md`** **Execute checkpoint (2026-03-30) — S0060 / BUG-0001 / auto-20260330-01**; **`handoffs/dev_to_qa.md`**; **`sprints/S0060/summary.md`**. Prior BUG-0001 intake + plan-verify thread: **`handoffs/archive/po-to-tl-pack-20260330.md`**.
- **`BUG-0001`**: **OPEN** until **`/verify-work`**. Next: **`/qa`**.

---

## Intake Addendum — Non-Overwriting Release Notes + Unreleased Sprint Queue

### New intake

User confirmed implementation of prior release-file recommendation:
1. Avoid overwriting single `handoffs/release_notes.md`.
2. Track unreleased sprints explicitly.

### Overlap and duplicate evaluation

- No direct duplicate found in backlog.
- Closest related stories:
  - `US-0038`: sync-policy evidence and push cadence semantics.
  - `US-0039`: release gate ordering and readiness blocking.
- Assessment: related but non-duplicate.
  - Existing stories govern gating and readiness criteria.
  - New request governs release artifact lifecycle/history preservation and queue visibility.
- Decision: create a new focused story to keep lifecycle/migration requirements testable.

### Accepted story

#### US-0040 — Per-Sprint Release Notes and Release Queue Tracker
- Priority: P1
- Status: OPEN
- Intent: preserve release history by sprint and provide deterministic queue state for unreleased/released sprint tracking.

### TL guidance and boundaries

- In scope:
  - Canonical per-sprint release note artifact path and naming contract.
  - Canonical release queue artifact with deterministic state transitions (`unreleased` -> `released`).
  - Safe migration/backfill behavior for existing `handoffs/release_notes.md`.
  - Backward compatibility behavior for workflows still reading `handoffs/release_notes.md`.
  - Command/rule/doc updates plus active/template parity checks.
- Out of scope:
  - Runtime deployment pipeline changes.
  - External release-management platform integration.
  - Redefining QA/UAT evidence model.

### Planning recommendation

1. Define canonical artifact contracts first (per-sprint notes + queue schema + ownership).
2. Define migration/backfill semantics second (resolvable sprint vs unresolved legacy content).
3. Update release command/rules/docs with deterministic transitions and fail-safe behavior.
4. Add QA coverage for overwrite prevention, unresolved sprint context, migration path, and parity checks.

---

