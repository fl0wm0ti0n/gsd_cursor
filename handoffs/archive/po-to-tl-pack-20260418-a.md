# PO to TL archive pack (2026-04-18)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 3
- Retained units in hot file: 42
- First archived heading: `## Research Addendum — US-0076 (tail mirror)`
- Last archived heading: `## Discovery Addendum — US-0077 (tail mirror)`
- Verification tuple (mandatory):
  - archived_body_lines=34
  - retained_body_lines=793

---

## Research Addendum — US-0076 (tail mirror)

> Placement: **tail** hot copy for TL read model (substance aligned with prepended **Research Addendum — US-0076**). `orchestrator_run_id=auto-20260327-01`.

- **Closure**: **`/research`** (TL) complete for **US-0076**; **`R-0053`** extended with implementation anchors + mitigations.
- **Anchors**: **`validate-and-push.ps1`/`.sh`** — merged scratchpad gate before push; prefer **`installer.py`** `merge_scratchpad_layers` / `parse_scratchpad_file`; runbook remains command source only.
- **Boundaries**: **`by_phase`** default = invocation as boundary unless architecture fixes **`state.md`/env/CLI**; **AC-5** = bounded **`qa-findings.md`** scan + sprint path in architecture.
- **Next**: **`/architecture`** — **DEC-0058** (or **DEC-0018** amendment), QA glob, dry-run/exit codes, **AC-8** tests.

---

## Architecture Addendum — US-0076 (tail mirror)

> Placement: **tail** hot copy for TL read model (substance aligned with prepended **Architecture Addendum — US-0076**). `orchestrator_run_id=auto-20260327-01`.

- **Decision**: **`decisions/DEC-0058.md`** accepted — executable scratchpad → **validate-and-push**; **`DEC-0018`** policy authority retained.
- **AC-5**: **`sprints/S*/qa-findings.md`** bounded scan per **DEC-0058** §6.
- **Phase signal**: default **invocation**; optional **`SYNC_PHASE_BOUNDARY`** env.
- **Next**: **`/sprint-plan`**.

---

## Discovery Addendum — US-0077 (tail mirror)

> Placement: **tail** hot copy for TL read model (substance aligned with prepended **Discovery Addendum — US-0077**). `orchestrator_run_id=auto-20260327-02`.

- **Scope**: Documentation audience/depth profiles + dual README strategy; preserve **US-0030** / **US-0031** / **US-0032** / **US-0071**; anchor **R-0054**.
- **Conclusions**: Ownership matrix + bounded sections/split preferred; profile validation with deterministic reason codes; **US-0071** on user-visible outputs.
- **Next**: **`/sprint-plan`** — **`/architecture`** complete (**`DEC-0059`**).
- **Decision gate before research** (historical): **none**.
- **Artifacts**: `docs/product/vision.md`, `docs/product/backlog.md`, `handoffs/po_to_tl.md`, `docs/engineering/state.md`, `docs/engineering/research.md` (**R-0054**).

---

