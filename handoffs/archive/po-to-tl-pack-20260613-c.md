# PO to TL archive pack (2026-06-13)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=650, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 10
- First archived heading: `## Orchestrated discovery handoff — US-0100 / auto-20260615-01`
- Last archived heading: `## Orchestrated discovery handoff — US-0100 / auto-20260615-01`
- Verification tuple (mandatory):
  - archived_body_lines=74
  - retained_body_lines=635

---

## Orchestrated discovery handoff — US-0100 / auto-20260615-01

### Target

- `story_id=US-0100`
- `orchestrator_run_id=auto-20260615-01`
- phase completed: **`discovery`** (**`po`**)
- `fresh_context_marker=po-US0100-discovery-20260615T010000Z-fresh`
- `next_scheduled_phase=research`
- `decomposition=single_story` (per **US-0051**)
- `priority=P1`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=7`

### Summary

- **`/discovery`** **PASS** — version-scoped release documentation locked: cumulative **`CHANGELOG.md`** (Keep a Changelog 1.1.0) + per-version **`handoffs/releases/vX.Y.Z-release-notes.md`**; sprint **`Sxxxx`** notes unchanged (**US-0040**); **`release-all.sh`** must switch from **`--generate-notes`** to **`-F`** canonical body when version doc exists; **`/release`** derivation hook + queue **`release_version`** binding; backfill from **~79** released sprint notes.
- **Repo gap confirmed**: no **`CHANGELOG.md`**; queue **`release_version`** mostly empty; **`gh release create --generate-notes`** at **`scripts/release-all.sh:99`**.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Discovery locks (research/architecture inputs)

| Lock | Decision |
|------|----------|
| **L1 Cumulative path** | Repo-root **`CHANGELOG.md`** (Keep a Changelog 1.1.0, **`[Unreleased]`** + semver sections) |
| **L2 Per-version path** | **`handoffs/releases/vX.Y.Z-release-notes.md`** |
| **L3 Sprint layer** | **`handoffs/releases/Sxxxx-release-notes.md`** unchanged — compose only |
| **L4 Derivation precedence** | Sprint notes (**What's new**, **`story_refs`**) → backlog title/summary → queue **`story_refs`** |
| **L5 GitHub body SOT** | Per-version file; **`gh release create … -F`**; no **`--generate-notes`** when file exists |
| **L6 Version binding** | Queue **`release_version`** on **`/release`** finalization; **`release-all.sh`** uses post-**`npm version`** semver |
| **L7 Idempotency** | Re-run must not duplicate version sections |
| **L8 Backfill** | Idempotent script from **`released`** rows + sprint notes; remediation for ambiguous semver |
| **L9 Multi-sprint coalesce** | **Open — Q1/Q4 in research** |
| **L10 US-0067 compose** | Run/Connect/Verify stay in sprint notes; version docs link only |
| **L11 US-0054 compose** | Docs may write under **`RELEASE_PUBLISH_MODE=disabled`**; publish attach still gated |
| **L12 Workflow paths** | Document **`/release`** vs **`release-all.sh`** vs CI tag touchpoints |
| **L13 Reason codes** | **`RELEASE_CHANGELOG_*`** family + documented **`gh`/file fallbacks |
| **L14 Validator** | **`scripts/release_changelog_validate.py`** |

### Top risks (carry to /research)

- **R1**: Backfill semver ambiguity — most queue rows lack **`release_version`**; need deterministic grouping without falsifying history.
- **R2**: Multi-sprint single npm publish — coalesce must not drop sprint cross-links or duplicate work items.
- **R3**: Workflow-only release vs npm publish — clarify **`[Unreleased]`** vs semver-bound sections (**Q3**).

### Research open questions (`R-0087`)

- **Q1**: Backfill semver assignment when **`release_version`** blank.
- **Q2**: Keep a Changelog category mapping vs flat US/BUG list.
- **Q3**: Workflow-only **`/release`** without npm bump — **`[Unreleased]`** posture.
- **Q4**: Coalesce when **`release-all.sh`** covers multiple sprints since last tag.
- **Q5**: Template parity surfaces.

### Evidence refs

- `handoffs/intake_evidence/US-0100-intake-20260615.json`
- `docs/product/vision.md` (**Discovery Notes — US-0100**)
- `docs/product/backlog.md` (`## US-0100` — `discovery_notes`)
- `docs/engineering/research.md` (**`R-0087`** stub — extend at research)
- `scripts/release-all.sh` (lines 85–112 GitHub step)
- `handoffs/release_queue.md`, `handoffs/releases/S0089-release-notes.md` (exemplar)
- `docs/engineering/state.md` (Discovery checkpoint — this run)
- `handoffs/resume_brief.md` (top pointer → `/research`)

### Next

- **`/research`** (fresh **tech-lead** context) for **`US-0100`** — close **`R-0087`** Q1–Q5; repo survey closure; backfill algorithm sketch.

### Decision gate

- **None** — discovery satisfied; research readiness explicit on Q1–Q5 and L9 coalesce.

---

