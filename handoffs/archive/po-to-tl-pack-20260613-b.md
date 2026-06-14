# PO to TL archive pack (2026-06-13)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=650, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 10
- First archived heading: `## Orchestrated intake handoff — US-0100 / cursor-20260615-US0100-intake`
- Last archived heading: `## Orchestrated intake handoff — US-0100 / cursor-20260615-US0100-intake`
- Verification tuple (mandatory):
  - archived_body_lines=63
  - retained_body_lines=635

---

## Orchestrated intake handoff — US-0100 / cursor-20260615-US0100-intake

### Target

- `story_id=US-0100`
- `intake_run_id=cursor-20260615-US0100-intake`
- phase completed: **`intake`** (**`po`**)
- `fresh_context_marker=po-US0100-intake-20260615T120000Z-fresh`
- `next_scheduled_phase=discovery`
- `decomposition=single_story` (per **US-0051**)
- `priority=P1`
- `INTAKE_GUIDED_MODE=1`
- `INTAKE_WORK_ITEM_KIND=story`

### Summary

- **`/intake`** **PASS** — operator request: cumulative version changelog + per-release docs listing **US-xxxx** / **BUG-xxxx** with short descriptions; GitHub/git publish should attach canonical release notes per best practices; compose with **US-0040** sprint notes, **`release_queue`**, **US-0054** **`RELEASE_PUBLISH_MODE`**, and **`release-all.sh`**.
- **Intake pack**: **`first-intake-pack`** — 8/8 topics + 7 plan areas → **`US-0100`**; **`coverage_complete=true`**; validator **`[INTAKE_EVIDENCE_VALIDATION_OK]`** on **`handoffs/intake_evidence/US-0100-intake-20260615.json`**.
- **Decomposition evaluator**: **single story** — version docs, `/release` derivation, GitHub attach, backfill, and validators are one integrated contract.
- **Research stub**: **`R-0087`** (Keep a Changelog + **`gh release create -F`** survey; semver/backfill questions open).
- Status authority: **OPEN** per **US-0045**; closure at **`/release`**.

### Scope locks (discovery inputs)

| Lock | Intake decision |
|------|-----------------|
| **Cumulative artifact** | Growing **`CHANGELOG.md`** (Keep a Changelog 1.1.0 shape) — version → US/BUG one-liners |
| **Per-version docs** | **`handoffs/releases/vX.Y.Z-release-notes.md`** (or architecture-locked equivalent) |
| **Sprint layer** | **`handoffs/releases/Sxxxx-release-notes.md`** unchanged (**US-0040**) |
| **Derivation** | **`/release`** finalization derives version docs from sprint notes + backlog + queue |
| **Publish** | **`gh release create -F <version-notes>`** replaces **`--generate-notes`** when docs exist; **`RELEASE_PUBLISH_MODE`** gates unchanged |
| **Backfill** | Idempotent seed from existing **`released`** queue rows + sprint notes |

### Overlap / non-goals

- **Not replacing** **US-0040** sprint-scoped notes or queue semantics.
- **Not auto-bumping** semver without operator/`release-all.sh` intent.
- **Out of scope v1**: **`.github/release.yml`** PR-label taxonomy (optional future).

### Top risks (carry to /discovery)

- **R1**: Ambiguous semver when historical queue rows lack **`release_version`** — backfill must fail-safe with remediation.
- **R2**: Duplicate changelog sections on idempotent **`/release`** re-run — require deterministic upsert semantics.
- **R3**: Publish path divergence between **`/release`** and **`release-all.sh`** — shared helper recommended.

### Evidence refs

- `handoffs/intake_evidence/US-0100-intake-20260615.json`
- `docs/product/backlog.md` (`## US-0100`)
- `docs/product/acceptance.md` (portfolio row **US-0100** unchecked)
- `docs/product/vision.md` (**`## Intake Notes — US-0100`**)
- `docs/engineering/research.md` (**`R-0087`** stub)

### Next

- **`/discovery`** (fresh **PO** context) for **`US-0100`**.

### Decision gate

- **None** — intake satisfied; discovery readiness explicit.

---

