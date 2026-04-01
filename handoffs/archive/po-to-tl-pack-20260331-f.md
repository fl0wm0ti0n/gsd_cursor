# PO to TL archive pack (2026-03-31)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 42
- First archived heading: `## Intake Addendum — Continuous `/auto` Backlog-Drain Mode`
- Last archived heading: `## Intake Addendum — Continuous `/auto` Backlog-Drain Mode`
- Verification tuple (mandatory):
  - archived_body_lines=47
  - retained_body_lines=763

---

## Intake Addendum — Continuous `/auto` Backlog-Drain Mode

### New intake

User requests that once plans and stories are already defined, `/auto` should
continue working across stories until delivery completion, with configurable
switches to fine-tune stopping behavior.

### Overlap and duplicate evaluation

- Related stories:
  - `US-0037`: deterministic mid-process continuation for one flow.
  - `US-0038`: phase-triggered sync policy and guarded push controls.
  - `US-0043`: deterministic release/backlog reconciliation.
- Assessment:
  - no direct duplicate for **multi-story backlog-drain orchestration mode**.
  - existing stories govern single-flow continuation and safety gates, but not
    deterministic next-story selection + bounded multi-story progression.
- External references reviewed per `R-0008`:
  - deterministic checkpoint/replay orchestration patterns
  - human-approval gate patterns for high-impact operations
- Decision:
  - create `US-0044` as a dedicated orchestration story with explicit switches.

### Accepted story

#### US-0044 — Continuous `/auto` Backlog-Drain Mode with Fine-Tune Switches
- Priority: P1
- Status: OPEN
- Intent: allow optional unattended multi-story progress while preserving current
  safe defaults and decision-gate controls.

### TL guidance and boundaries

- In scope:
  - switch-controlled enable/disable of backlog-drain mode (default off)
  - deterministic next-story selection policy
  - bounded execution controls (max stories per run, stop/skip on blocked story)
  - per-story breadcrumbs and final run summary artifacts
  - active/template parity for command/rule/docs behavior
- Out of scope:
  - bypassing decision gates
  - changing story acceptance ownership/content model
  - runtime product behavior changes unrelated to workflow orchestration

---

