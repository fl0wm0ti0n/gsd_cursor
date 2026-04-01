# PO to TL archive pack (2026-03-28)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 29
- First archived heading: `## Discovery Addendum — US-0078`
- Last archived heading: `## Discovery Addendum — US-0078`
- Verification tuple (mandatory):
  - archived_body_lines=27
  - retained_body_lines=800

---

## Discovery Addendum — US-0078

> Placement: prepended; triad **`--rollover`** may archive this block to `handoffs/archive/`.
> `orchestrator_run_id=auto-20260328-01`.

- **Scope**: Runtime enforcement that **US-0068** / **DEC-0050** mandatory question-pack coverage and
  assumption confirmations are **evidence-backed** before backlog/acceptance mutation; complements
  **US-0051** / **US-0059** without changing decomposition heuristics.
- **Anchors**: **`R-0055`** (current) — minimal model: per-topic **`answer_ref`** or confirmed-assumption ref;
  block persistence when any required topic lacks one; reject inferred **`assumptions_confirmed`** without
  explicit confirmation evidence.
- **Conclusions**: Policy text alone is insufficient — implement deterministic **interaction/evidence**
  fields (**`asked_topics`** vs **`answered_topics`** or equivalent) and fail-closed diagnostics
  (**`INTAKE_REQUIRED_TOPIC_MISSING`**, **`INTAKE_REQUIRED_PACK_INCOMPLETE`**,
  **`INTAKE_ASSUMPTION_CONFIRMATION_REQUIRED`**). **Guided** and **low-touch** both gate persistence;
  low-touch reduces follow-up depth, not proof requirements.
- **Research handoff**: Extend **`R-0055`** with schema literals, confirmation-event detection contract,
  bounded remediation prompt rules, and **AC-8** positive/negative test matrix; then **`/architecture`**
  (**new DEC** or **DEC-0050** amendment) for authoritative intake-evidence model + migration of legacy
  persisted rows.
- **Next**: **`/research`** for **`US-0078`** (default role **`tech-lead`** per **`AUTO_ROLE_RESEARCH`** unless
  scratchpad overrides).
- **Decision gate before research**: **none** — single-story scope and **`R-0055`** draft already bound the
  problem; remaining work is schema and enforcement detail.

---

