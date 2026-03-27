# PO to TL archive pack (2026-03-27)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 2
- Retained units in hot file: 25
- First archived heading: `## Architecture Addendum — US-0076`
- Last archived heading: `## Intake Addendum — Multi-Repo Compatibility + Component-Scoped Execution`
- Verification tuple (mandatory):
  - archived_body_lines=68
  - retained_body_lines=750

---

## Architecture Addendum — US-0076

> Placement: **prepend** hot copy. If **DEC-0054** triad rollover archives top sections, use the **tail mirror** at file end for the same substance (`orchestrator_run_id=auto-20260327-01`).

- **Closure**: **`/architecture`** (tech-lead) complete for **US-0076**.
- **Executable contract**: **`decisions/DEC-0058.md`** — merged scratchpad gates **`validate-and-push.ps1`/`.sh`**; **`DEC-0018`** / **`US-0038`** semantics unchanged; **`DEC-0058`** is wiring + QA scan + optional **`SYNC_PHASE_BOUNDARY`**.
- **Design**: **`docs/engineering/architecture.md`** — **# US-0076** (invariants, reason codes, tests, migration).
- **Merge**: Reuse **`installer.py`** merge — no shell duplicate of **`DEC-0055`**.
- **Next**: **`/sprint-plan`**.

## Intake Addendum — Multi-Repo Compatibility + Component-Scoped Execution

### New intake (German source summary)

User asks for:
1. Monitoring across multiple repos/modules for software modules, docs, API descriptions, and API compatibility.
2. A way to work on one component in a repo with multiple components, without breaking others.

This is accepted as workflow/process capability (not runtime application feature behavior).

### Overlap and duplicate evaluation

- No direct duplicate found in current backlog.
- Closest related stories, but distinct scope:
  - `US-0017` template drift guard: parity/sync concern, not compatibility observability.
  - `US-0024` memory drift audit: compares artifacts vs code in one repo, read-only audit; no cross-repo contract focus.
  - `US-0025` traceability contract: links stories and sprint tasks; does not enforce component scoping or compatibility checks.
  - `US-0033` guided intake behavior: interaction mode only, not execution scoping or module compatibility validation.
- Workflow overlap noted with `/intake`, `/architecture`, `/execute`, `/qa`, but no existing story provides these capabilities end-to-end.

### Split decision

- Decision: create **two stories** (`US-0034`, `US-0035`) instead of one merged story.
- Rationale:
  - Different trigger and risk model:
    - `US-0034` is observability + compatibility signal generation and optional release gate behavior.
    - `US-0035` is day-to-day scoped execution safety and out-of-scope impact control.
  - Splitting keeps acceptance tests concrete and avoids mixed pass/fail semantics.

### Accepted stories

#### US-0034 — Multi-Repo and Contract Compatibility Observability
- Priority: P1
- Status: OPEN
- Key intent: optional, flag-driven compatibility visibility across repos/modules/contracts with zero-overhead default when disabled.

#### US-0035 — Component-Scoped Execution Mode with Protection Guards
- Priority: P1
- Status: OPEN
- Key intent: optional, flag-driven component targeting and unaffected-component protection checks with zero-overhead default when disabled.

### TL architecture boundaries

- In scope:
  - Define canonical flags and defaults for both stories.
  - Define canonical artifacts for compatibility findings and scoped-impact evidence.
  - Define decision-gate rules for critical compatibility breakage or unapproved out-of-scope impact.
  - Ensure command/rule/doc updates include active + `template/` parity.
- Out of scope:
  - Runtime service behavior changes.
  - Full cross-repo orchestration platform implementation.
  - Build-system redesign across monorepos.

### Suggested implementation order

1. `US-0035` first to reduce immediate change-risk in multi-component repos.
2. `US-0034` second to add broader compatibility observability and release-time confidence.

