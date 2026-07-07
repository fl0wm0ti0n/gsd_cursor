# PO to TL archive pack (2026-07-03)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=650, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 10
- First archived heading: `## Intake handoff — US-0113 / cursor-20260703-US0113-intake`
- Last archived heading: `## Intake handoff — US-0113 / cursor-20260703-US0113-intake`
- Verification tuple (mandatory):
  - archived_body_lines=61
  - retained_body_lines=597

---

## Intake handoff — US-0113 / cursor-20260703-US0113-intake

### Target

- `story_id=US-0113`
- `intake_run_id=cursor-20260703-US0113-intake`
- phase completed: **`intake`** (**`po`**)
- `next_scheduled_phase=discovery`
- `decomposition=single_story` (per **US-0051**)
- `priority=P1`
- `selected_pack=small-intake-pack`
- `intake_evidence_ref=handoffs/intake_evidence/US-0113-intake-20260703.json`

### Summary

- **`/intake`** **PASS** — operator documentation gap after **BUG-0014**: sovereign-loop features (**US-0103–US-0112**) have **US-0091 catalog rows** in `its_magic/README.md` but lack operator prose (what / when / how) and **Full scratchpad reference** entries. Request: extend **`template/its_magic/README.md`** (and active **`its_magic/README.md`**) with feature guides and scratchpad key documentation comparable to **Automation modes** / **Sync policy** depth.
- **Distinct from BUG-0014** (traceability index) and **US-0094** (intro hierarchy). **Distinct from US-0032** (optional separate user-guide files — default-off).
- Status authority: **OPEN** per **US-0045**; closure at **`/release`**.

### Scope locks (discovery inputs)

| Lock | Decision |
|------|----------|
| **Primary surfaces** | `its_magic/README.md` + `template/its_magic/README.md` (byte-identical per **US-0097**) |
| **Section pattern** | New **`### Sovereign loop`** umbrella + per-feature **`####`** blocks under **`## Commands and workflow`**; extend **`### Full scratchpad reference (detailed)`** |
| **Features in scope** | **US-0103**, **US-0104**, **US-0105**, **US-0106**, **US-0107**, **US-0108**, **US-0109**, **US-0110**, **US-0111**, **US-0112** |
| **Per-feature content** | What it is; when to enable; minimal recipe (flags + commands); master enable flag default **`0`**; related scratchpad keys (one-line each) |
| **Catalog immutability** | Three **`<!-- readme-feature-coverage-catalog -->`** blocks — anchors preserved (**DEC-0074** affinity); post-edit **`validate_readme_feature_coverage.py --enforce`** mandatory |
| **Deep dive** | Link to matching **`docs/engineering/runbook.md`** § per US — do not duplicate full runbook in README |
| **Audience** | **DEC-0059** USER_* H2 vocabulary; no new top-level audience H2s |
| **Out of scope** | Runtime behavior changes; **`docs/user-guides/`** generation unless explicitly opted in later; **`docs/developer/README.md`** body rewrite |

### Acceptance pointers (intake emphasis)

- **AC-1**: Sovereign stack umbrella + recommended enable order + default-off posture.
- **AC-2**: Ten per-feature operator subsections (**US-0103..US-0112**).
- **AC-3**: Full scratchpad reference sovereign key blocks (mirror **`scratchpad.local.example.md`**).
- **AC-4**: Coverage validator green; **`coverage_missing=[]`**.
- **AC-5**: Framework README byte parity.
- **AC-6**: Doc profile + metadata hygiene gates.
- **AC-7**: Runbook cross-links per feature.
- **AC-8**: Regression / template parity guards.

### Top risks (carry to /discovery)

- **R1**: README bloat — use concise operator recipes; defer depth to runbook links.
- **R2**: Catalog affinity break — forbid cross-H2 moves of **`US-xxxx`** anchor lines.
- **R3**: Misleading command slugs in existing catalog rows — discovery may lock corrected operator-facing command names in narrative (catalog row text optional fix if coverage-safe).
- **R4**: Scratchpad reference drift vs example file — narrative must match **`scratchpad.local.example.md`** key names/defaults.

### Alternatives considered

- **Enable US-0032** and generate **`docs/user-guides/US-0103.md`** etc. — rejected as primary path (extra mode flag; operator asked for README/scratchpad clarity in-framework).
- **Bug reopen BUG-0014** — rejected (ACs were catalog-only; this is new capability documentation scope).

### Next

- **`/discovery`** (fresh **PO** subagent) for **`US-0113`**.

---

