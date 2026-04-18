# PO to TL archive pack (2026-04-18)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 5
- Retained units in hot file: 36
- First archived heading: `## Research Addendum — US-0078 (tail mirror)`
- Last archived heading: `## PO → TL Handoff — US-0080 (Research)`
- Verification tuple (mandatory):
  - archived_body_lines=63
  - retained_body_lines=791

---

## Research Addendum — US-0078 (tail mirror)

> Placement: **tail** hot copy for TL read model (substance aligned with prepended **Research Addendum — US-0078**, archived to **`handoffs/archive/po-to-tl-pack-20260328-d.md`** on post-research triad rollover). `orchestrator_run_id=auto-20260328-01`.

- **Closure**: **`/research`** (**tech-lead**) complete; **`R-0055`** — schema, rules, **AC-8** tiers.
- **Next**: **`/architecture`** — **DEC-0050** / DEC for **`ref`** format + migration.
- **Decision gate before architecture**: **none**.

---

## Architecture Addendum — US-0078 (tail mirror)

> Placement: **tail** hot copy for TL read model (substance aligned with prepended **Architecture Addendum — US-0078**). `orchestrator_run_id=auto-20260328-01`.

- **Decision**: **`decisions/DEC-0060.md`** — **`ie:`** **`ref`** binding; extends **`DEC-0050`**; grandfather migration until next intake mutation.
- **Architecture**: **`docs/engineering/architecture.md`** **`# US-0078`**.
- **Next**: **`/sprint-plan`**.
- **Decision gate before sprint-plan**: **none**.

---

## PO → TL Handoff — US-0080 (Intake)

- **Orchestrator**: **`auto-20260329-02`** — intake complete in fresh **PO** context.
- **Evidence**: **`handoffs/intake_evidence/US-0080-intake-20260329.json`** — **`[INTAKE_EVIDENCE_VALIDATION_OK]`** (`small-intake-pack`, **`ie:`** per **DEC-0060**).
- **Research anchor**: **`R-0057`** (current) — structural levers (command/context slimming, comparable-run measurement); **`TOKEN_PROFILE=lean`** alone insufficient.
- **Alternatives**: **(1)** status quo pricing tolerance — rejected; **(2)** profile-only — rejected; **(3)** slimming + bounded phase-context + auditable metrics — **recommended** (aligned with backlog).
- **Artifacts**: **`docs/product/backlog.md`** (US-0080 intake closure + topic_coverage), **`docs/product/vision.md`** (intake closure line), **`handoffs/resume_brief.md`** → **`/discovery`**, **`docs/engineering/state.md`** (isolation + strict proof + phase boundary; triad rollover **`docs/engineering/state-archive/state-pack-20260329-m.md`**).
- **Next**: **`/discovery`** for **`US-0080`**, then **`/research`** / **`/architecture`** to lock metric definitions and **DEC** for **AC-10** trade-offs.
- **Decision gate before discovery**: **none** (intake evidence satisfied).

---

## PO → TL Handoff — US-0080 (Discovery)

- **Orchestrator**: **`auto-20260329-02`** — discovery complete in fresh **PO** context.
- **Evidence**: **`docs/product/backlog.md`** (US-0080 discovery notes), **`docs/product/vision.md`** (**Discovery Notes — US-0080**), **`docs/engineering/state.md`** (Discovery checkpoint + strict proof); research anchor remains **`R-0057`** (current).
- **Findings**: Dominant lever is **structural** — reduce repeated large command/policy prefixes and tighten **per-phase context packs** while preserving mandatory gates; **`TOKEN_PROFILE=lean`** alone insufficient.
- **Research asks**: Deterministic **run-class/baseline** for AC-1/AC-2; **metric/evidence** placement contract; **active/template** parity list for slimmed orchestration surfaces.
- **Risks**: Over-slimming obscuring policy; baseline drift enabling metric gaming; template divergence.
- **Artifacts**: **`handoffs/resume_brief.md`** → **`/research`** for **`US-0080`**.
- **Next**: **`/research`** (then **`/architecture`**) to lock metric definitions and **DEC** for **AC-10** trade-offs.
- **Decision gate before research**: **none** (discovery satisfied).

---

## PO → TL Handoff — US-0080 (Research)

- **Orchestrator**: **`auto-20260329-02`** — research complete in fresh **tech-lead** context.
- **Evidence**: **`docs/engineering/research.md`** **`R-0057`** (extension + research closure line);
  **`docs/product/backlog.md`** / **`docs/product/vision.md`** (research closure notes);
  **`docs/engineering/state.md`** (Research checkpoint + strict proof; triad rollover
  **`docs/engineering/state-archive/state-pack-20260329-o.md`**).
- **Findings**: **Run-class tuple** frozen for AC-1/AC-2 comparability; **append-only in-repo metric
  records** + **`state.md`** pointer for AC-6; **explicit parity manifest** for `.cursor/commands/`,
  `.cursor/rules/`, `template/` mirrors (AC-3/AC-9); vendor **`cache_read_input_tokens`** semantics
  as conceptual anchor for metric naming in upcoming **DEC**.
- **Artifacts**: **`handoffs/resume_brief.md`** → **`/architecture`** for **`US-0080`**.
- **Next**: **`/architecture`** to lock **`architecture.md`** story section + **DEC** for AC-10.
- **Decision gate before architecture**: **none** (research satisfied; story **OPEN**).

---

