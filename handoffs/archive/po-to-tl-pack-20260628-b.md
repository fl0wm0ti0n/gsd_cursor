# PO to TL archive pack (2026-06-28)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=650, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 10
- First archived heading: `## PO intake handoff — US-0112 / cursor-20260628-US0112-intake`
- Last archived heading: `## PO intake handoff — US-0112 / cursor-20260628-US0112-intake`
- Verification tuple (mandatory):
  - archived_body_lines=64
  - retained_body_lines=635

---

## PO intake handoff — US-0112 / cursor-20260628-US0112-intake

### Target

- `story_id=US-0112`
- `intake_run_id=cursor-20260628-US0112-intake`
- `selected_pack=small-intake-pack`
- `priority=P2`
- `decomposition=single_story` (per **US-0051**)
- `next_scheduled_phase=architecture`

### Summary

Operator **`/ask`** → **`/intake`**: the eight **`model-catalog.local.example*.json`** presets (**US-0101**/**US-0102**) should ship into consumer repos on its-magic **install/upgrade**. Repo survey: files exist under **`template/.cursor/`** but **`installer-owned-paths.manifest`** omits them — **`missing`**/**`upgrade`** never copies them to **`.cursor/`**.

### Scope (8 ACs)

1. Manifest lists all eight example paths in **`[install_include_paths]`**.
2. **`missing`** mode adds absent examples.
3. **`upgrade`** refreshes examples as **framework** files (like **`scratchpad.local.example.md`**).
4. **Never** touch gitignored **`model-catalog.local.json`**.
5. Triple installer parity (PS1 / Bash / Python).
6. Runbook preset-selection recipe.
7. **`test_us0112_*`** + **`--scope=model-catalog-examples`** parity.
8. Architecture **`# US-0112`**.

### Alternative considered

- **US-0099-style** auto-copy one preset → **`model-catalog.local.json`** — **rejected at intake**: eight presets imply operator choice; auto-bootstrap would pick an arbitrary default.

### Overlap / duplicate check

- **US-0101** / **US-0102** (DONE) — **completes delivery**; does not amend tier matrix or catalog schema.
- **US-0099** (DONE) — **distinct**: dev profile is gitignored local file; examples are committed framework files.
- **US-0075** (DONE) — **compose**: same framework example refresh semantics.

### Intake evidence

- `handoffs/intake_evidence/US-0112-intake-20260628.json` → **`[INTAKE_EVIDENCE_VALIDATION_OK]`**
- `asked_topics`: all five small-pack keys covered
- `missing_topics`: (none)
- `assumptions_confirmed`: (none)

### Risks (PO)

- **R1**: Accidental overwrite of **`model-catalog.local.json`** — mitigate with manifest exclusion + contract test guard.
- **R2**: Stale examples after upgrade if not classified as framework — explicit **`Classify-File`** or default-framework fallback in architecture.
- **R3**: Manifest drift when new presets added — parity scope + manifest completeness test.

### Research anchor

- **`R-0090`** — extend in **`/architecture`** (manifest rows, classification, parity manifest, contract tests).

### Status authority

- **OPEN** per **US-0045** until QA/release closure chain.
- **Next**: **`/architecture`** (fresh **tech-lead**) for **`US-0112`** — **`/discovery`** skipped (clear scope, strong **US-0099**/**US-0075** precedents).

### Decision gate

- **None** — intake satisfied.

---

