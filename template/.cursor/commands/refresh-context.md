---
description: "its-magic refresh context: compact state and decisions."
---

# /refresh-context

## Subagents
- curator

## Execution model
- Run `/refresh-context` in a fresh Curator subagent context.
- After writing outputs, stop. Next phase starts in a new subagent/chat.

## Inputs

- **Narrow-read (US-0053 / US-0096 Tranche A)**: Start at docs/engineering/phase-context.md
  and the story section anchor in vision/architecture/decisions when a heading exists; forbid
  full-file reads when a section heading exists.
- Current sprint artifacts
- Decisions and handoffs

## Outputs (artifacts)
- `docs/engineering/state.md`
- `docs/engineering/decisions.md`
- `sprints/S0001/summary.md`

## Stop conditions
- Missing critical artifacts

## Steps
1. Compact state and decisions into a short context pack.
2. Update sprint summary with current status.
3. Ensure handoffs and state are consistent.
3a. Optional codebase map refresh (US-0082 / DEC-0065): when merged scratchpad
    sets `CODEBASE_MAP_REFRESH_ON_ROLLOVER=1`, from repository root run
    `python scripts/materialize_codebase_map.py --trigger refresh-context`.
    Default is **skip** (omit this step) to avoid map churn. On
    `CODEBASE_MAP_BLOCKED:*`, record the token and remediation in the new
    `state.md` checkpoint; do not rewrite operator-authored maps outside the
    bootstrap contract.
4. Enforce **triad** hot-surface rollover when merged scratchpad thresholds are
   exceeded (DEC-0054):
   - read caps from `.cursor/scratchpad.md` + `.cursor/scratchpad.local.md`,
     including `STATE_HOT_MAX_LINES`, `STATE_HOT_MAX_CHECKPOINTS`,
     `PO_TO_TL_HOT_MAX_LINES`, `PO_TO_TL_HOT_MAX_SECTIONS`, `ARCH_HOT_MAX_LINES`,
     and `ARCH_HOT_MAX_STORY_SECTIONS` (see runbook defaults),
   - run `python scripts/enforce-triad-hot-surface.py --rollover` from repo root
     (or `--repo <root>`) so `state.md`, `handoffs/po_to_tl.md`, and
     `docs/engineering/architecture.md` archive oldest contiguous units into
     deterministic packs under `docs/engineering/state-archive/`,
     `handoffs/archive/`, and `docs/engineering/architecture-archive/`,
   - immediately rerun `python scripts/enforce-triad-hot-surface.py --check`;
     on failure stop with `STATE_ARCHIVE_REQUIRED` or
     `ARTIFACT_HOT_SURFACE_OVERSIZE` (no successful phase completion on oversize
     hot files),
   - record verification tuple fields (`boundary`, `moved`, `retained`,
     `pack_ref`) in the new `state.md` checkpoint when any rollover occurred;
     idempotent reruns must not duplicate archived content.
3b. **Goal progress emission (US-0110 / DEC-0110)**: when merged scratchpad
    `SOVEREIGN_GOAL_MODE=goal_convergence` and sovereign loop is active, run from repo root:

    ```bash
    python scripts/sovereign_convergence_lib.py --emit-resume-brief --repo . --orchestrator-run-id <run_id>
    ```

    Writes a fenced JSON block under **`### goal_progress`** in `handoffs/resume_brief.md`.
    Placement: after the latest **`## Latest orchestration pointer`** section, before
    **`## Prior orchestration pointer`**. Skip entirely when `SOVEREIGN_GOAL_MODE=phase_driven`
    (zero overhead). Validate shape with:

    ```bash
    python scripts/sovereign_convergence_validate.py --repo . --enforce
    ```

3c. **Sovereign memory curator retrospective + ledger promotion (US-0105 / DEC-0105)**:
    after release segment close, when merged scratchpad `SOVEREIGN_MEMORY=1`:

    1. `write_retrospective(sprint_id, body)` →
       `docs/engineering/sovereign-memory/retrospectives/<sprint_id>.md` with
       `{sprint_id, story_ids[], release_ref, summary, learnings[], promoted_entry_ids[]}`.
    2. When **also** `AI_DECISION_LEDGER=1`: `promote_from_ledger(orchestrator_run_id, ...)`
       copies subset to `decisions-log.jsonl` with `provenance_ref=ledger:<decision_id>`.
    3. When ledger off or filter empty → informational **`SOVEREIGN_MEMORY_PROMOTION_SKIPPED`**.

    Retrospectives are human audit only — **not injected v1**. Skip entirely when
    `SOVEREIGN_MEMORY=0` (zero overhead). Validate JSONL when files exist:

    ```bash
    python scripts/sovereign_memory_validate.py --repo . --enforce
    ```

## Deterministic artifact ordering contract (US-0058 / DEC-0040)

- Writes must follow `docs/engineering/artifact-ordering-policy.md`.
- `docs/engineering/state.md` refresh checkpoints are append-bottom only.
- `docs/engineering/decisions.md` compact index remains newest-first in bounded
  section while preserving canonical header structure.
- `sprints/S0001/summary.md` context-pack pointer is prepend-top within its
  context section; historical details remain intact.
- Missing/ambiguous anchors fail with `ARTIFACT_ORDERING_ANCHOR_AMBIGUOUS`
  (no partial write).
- Archive write or rollover boundary ambiguity fails with
  `STATE_ARCHIVE_WRITE_FAILED` or `STATE_ARCHIVE_BOUNDARY_AMBIGUOUS`
  (no partial write).
- Archive verification mismatch fails with `STATE_ARCHIVE_VERIFICATION_FAILED`
  (no partial write).

## Cross-phase ownership guard (US-0061 / DEC-0043)

- Refresh-context mutations must comply with
  `docs/engineering/artifact-ownership-policy.md`.
- Only curator-owned compaction scopes may be mutated; non-owned section
  rewrites fail closed with `PHASE_OWNERSHIP_VIOLATION`.

