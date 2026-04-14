# PO to TL archive pack (2026-04-14)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 44
- First archived heading: `## PO → TL Handoff — US-0089 / US-0090 (Intake)`
- Last archived heading: `## PO → TL Handoff — US-0089 / US-0090 (Intake)`
- Verification tuple (mandatory):
  - archived_body_lines=30
  - retained_body_lines=799

---

## PO → TL Handoff — US-0089 / US-0090 (Intake)

> Placement: prepended per **US-0058** / **DEC-0054** hot-surface discipline; older handoffs remain below.

### New intake

Operator wants **Caveman-style** terse communication (**JuliusBrussee/caveman**-like) in **Cursor**, **scratchpad-configurable**, **default off**, **without losing** existing **its-magic** features. **Split stories**: **US-0089** (response style + scratchpad + rules/skill + tests) then **US-0090** (optional **input-side** file compression with **original preserved** and **hard deny** for canonical/evidence paths).

### Evidence

- **`handoffs/intake_evidence/US-0089-intake-20260414.json`** — **`first-intake-pack`**, **`[INTAKE_EVIDENCE_VALIDATION_OK]`** (`intake_run_id=cursor-20260414-caveman-intake`).
- **`docs/product/backlog.md`** — **`## US-0089`**, **`## US-0090`**; **`docs/product/acceptance.md`** portfolio rows; **`docs/product/vision.md`** value + intake notes; **`docs/engineering/research.md`** **`R-0073`** stub.

### Decomposition (US-0051)

- **US-0089**: Caveman **output** mode + **`.cursor/scratchpad.md`** keys + **rules/skill** + **`architecture.md`** **`# US-0089`** + contract tests (**default-off** invariant).
- **US-0090**: Optional **compress**-like path for **scoped** files only; **gates** on **`CAVEMAN_MODE`** + explicit compress policy; **deny** intake evidence, backlog, acceptance, **state.md**, **`.env`**; **template/** parity.

### TL scope / risks

- **Composition with `TOKEN_PROFILE` / US-0080** must be explicit (**orthogonal** vs precedence matrix — pick one in architecture).
- **Loss risk** on **US-0090**: architecture must lock **sidecar original** pattern and **immutable deny-list** defaults; no silent rewrite of **US-0078** bundles.
- **Parity**: any **`.cursor/`** change mirrored in **`template/`** (**US-0017**).

### Recommendation

**`/discovery`** (**US-0089** first) → **`/research`** (extend **`R-0073`**) → **`/architecture`** → **`/sprint-plan`** (order **US-0089** before **US-0090**).

---

