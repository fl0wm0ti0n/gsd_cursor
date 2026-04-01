# PO to TL archive pack (2026-03-29)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 32
- First archived heading: `## Intake Addendum — Mid-Process Full Automation Continuation`
- Last archived heading: `## Intake Addendum — Mid-Process Full Automation Continuation`
- Verification tuple (mandatory):
  - archived_body_lines=49
  - retained_body_lines=756

---

## Intake Addendum — Mid-Process Full Automation Continuation

### New intake

User asks for a way to start full automation from mid-process:
- pause/resume plus scratchpad `PHASE_MODE=auto` still feels step-by-step with manual prompts
- expectation is one command that continues the remaining workflow automatically from the correct point

### Overlap and duplicate evaluation

- Existing overlap:
  - `US-0023` (DONE): defines fresh subagent context per phase and `/auto` orchestration model.
  - Existing commands `.cursor/commands/auto.md`, `.cursor/commands/resume.md`, `.cursor/commands/pause.md` describe pieces of the behavior.
- Gap identified:
  - No explicit `/auto` mid-process resume-point input contract (`start-from` style).
  - No deterministic precedence contract for resume source resolution (resume brief vs state fallback) with conflict handling.
  - No single, testable "continue remaining phases without manual phase triggers" acceptance contract.
- Decision:
  - Create a new focused story (`US-0037`) instead of reopening `US-0023`, so implementation scope stays concrete and regression-safe.

### Accepted story

#### US-0037 — Mid-Process `/auto` Continuation with Deterministic Resume Point
- Priority: P1
- Status: OPEN
- Intent: make `/auto` continuation behavior explicit, deterministic, and testable while preserving current safe defaults and decision gates.

### TL guidance and boundaries

- In scope:
  - Add explicit `/auto` `start-from` phase support.
  - Define deterministic resume-source precedence (`handoffs/resume_brief.md` first, then `docs/engineering/state.md` fallback).
  - Define safe failure behavior for missing/stale/conflicting resume inputs.
  - Require one-command continuation through remaining phases with existing stop conditions.
  - Add continuation breadcrumbs/logging to artifacts for inspectability.
  - Align `/pause`, `/resume`, `/auto` semantics and keep active + `template/` parity.
- Out of scope:
  - Bypassing decision gates or missing-input blockers.
  - Changing phase deliverables or introducing unrelated runtime features.

### Suggested implementation order

1. Define canonical phase IDs and `start-from` validation contract.
2. Implement deterministic resume-source resolver and conflict policy.
3. Update `/auto`, `/resume`, `/pause` docs/rules for semantic alignment.
4. Add QA cases for explicit start, implicit resume, conflict, missing source, and stop-reason logging.

---

