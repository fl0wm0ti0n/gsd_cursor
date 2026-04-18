# PO to TL archive pack (2026-04-18)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 3
- Retained units in hot file: 40
- First archived heading: `## Research Addendum — US-0077 (tail mirror)`
- Last archived heading: `## Discovery Addendum — US-0078 (tail mirror)`
- Verification tuple (mandatory):
  - archived_body_lines=31
  - retained_body_lines=791

---

## Research Addendum — US-0077 (tail mirror)

> Placement: **tail** hot copy for TL read model (substance aligned with prepended **Research Addendum — US-0077**). `orchestrator_run_id=auto-20260327-02`.

- **Closure**: **`/research`** (TL) complete; **`R-0054`** — profile matrix + validation tiers + reason-code draft.
- **Next**: **`/sprint-plan`** — **`/architecture`** complete (**`DEC-0059`**).
- **Decision gate before architecture**: **none** (closed).

---

## Architecture Addendum — US-0077 (tail mirror)

> Placement: **tail** hot copy for TL read model (substance aligned with prepended **Architecture Addendum — US-0077**). `orchestrator_run_id=auto-20260327-02`.

- **Decision**: **`decisions/DEC-0059.md`** — dual README (**`USER_*`** / **`DEV_*`**), validator **`scripts/validate_doc_profile.py`**, tiered **AC-8**, **`US-0030`** parity + manifest path for **`docs/developer/README.md`**.
- **Next**: **`/sprint-plan`**.
- **Decision gate before sprint-plan**: **none**.

---

## Discovery Addendum — US-0078 (tail mirror)

> Placement: **tail** hot copy for TL read model (substance aligned with archived **Discovery Addendum — US-0078** in **`handoffs/archive/po-to-tl-pack-20260328-b.md`**). `orchestrator_run_id=auto-20260328-01`.

- **Scope**: Runtime intake question-pack **evidence** before persistence (**US-0068** / **DEC-0050**); per-topic **`answer_ref`** or explicit assumption-confirmation ref; reject unverifiable **`assumptions_confirmed`**.
- **Conclusions**: Persist **`asked_topics`** vs answered/coverage evidence; **guided** and **low-touch** both **fail closed** without proof; extend **`R-0055`** then **DEC** for schema + migration.
- **Next**: **`/architecture`** for **`US-0078`** (**`/research`** complete; **`R-0055`** refined).
- **Decision gate before research** (historical): **none**.

---

