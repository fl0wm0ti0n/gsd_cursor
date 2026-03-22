# PO to TL archive pack (2026-03-21)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 3
- Retained units in hot file: 23
- First archived heading: `## Discovery Addendum — US-0075 (2026-03-26)`
- Last archived heading: `## PO → TL Handoff — US-0075 (Intake)`
- Verification tuple (mandatory):
  - archived_body_lines=111
  - retained_body_lines=768

---

## Discovery Addendum — US-0075 (2026-03-26)

### Discovery focus

- Close the **example-lags-baseline** class: **`.cursor/scratchpad.local.example.md`**
  must refresh on every install/upgrade path that touches scratchpad layers, **before or
  with** materialized **`.cursor/scratchpad.md`** refresh (**AC-1**, **AC-3**).
- Implement **AC-11** as a **machine-verifiable** paired-file inventory (sections +
  **`KEY=`** lines) for active + **`template/`** pairs; default **no** “keys only in one
  file” without a documented manifest exception.

### Discovery conclusions for TL

- **Single behavioral contract**: Ordering + parity are one story — installers, manifest,
  and tests must enforce both; splitting would re-open drift.
- **Operator story**: Example is the **copy-from** catalog; materialized baseline is
  **DEC-0055** merge input; local is **user-owned** — diagnostics must name which surface
  was touched (**AC-5**).
- **Regression posture**: Simulate **stale example + fresh template** upgrade and assert
  post-run **byte/template alignment** for example paths (**AC-6**, **AC-9**).

### Research handoff targets (**`R-0052`**)

1. Map **deterministic refresh sequence** across **`installer.ps1`**, **`installer.sh`**,
   **`installer.py`**, **`bin/its-magic.js`**, and **`docs/engineering/context/installer-owned-paths.manifest`**
   (+ `template/` mirror).
2. Specify the **parity check algorithm** (normalization rules for comments/blank lines,
   what qualifies as a framework **`KEY=`**, handling of intentional value-only differences).
3. Confirm interaction with **DEC-0055** / **DEC-0039** / **US-0057** — amendment only if
   ordering needs a normative DEC sentence beyond current text.

### Recommendation

- Proceed **`/research`** for **`US-0075`** (extend **`R-0052`**), then **`/architecture`**
  if a **DEC** tweak is required to lock ordering next to **DEC-0055**.

---

## PO → TL Handoff — US-0075 (Intake refinement 2026-03-25)

### Refinement

User requires **all settings in both** scratchpad files (materialized
**`.cursor/scratchpad.md`** and **`.cursor/scratchpad.local.example.md`**, plus
**`template/`** mirrors). Concrete gap: **Team** section exists in **example** but
not in **materialized** `scratchpad.md`; **`AUTO_ROLE_*`**, **`AUTO_PHASE_*`**,
and **triad** **`PO_TO_TL_*` / `ARCH_*`** keys exist in **materialized** but not in
**example**.

### PO decision

- Extend **US-0075** with **AC-11** (**complete settings catalog parity**) and a
  **deterministic check** (test or script) so drift cannot recur silently.
- Discovery/research should record canonical **key set** source (template pair as
  gold master after fix).

### Intake pack (refinement)

- selected_pack=`small-intake-pack`
- asked_topics=`outcome_success_criteria`,`impacted_components`,`constraints_compatibility_risks`,`required_tests_acceptance_checks`,`done_definition`,`paired_scratchpad_full_key_parity`
- missing_topics=`(none)`
- assumptions_confirmed=`(none)`

---

## PO → TL Handoff — US-0075 (Intake)

### New intake (operator report)

User reports upgrade/install refreshes **`.cursor/scratchpad.md`** but **does not** update
**`.cursor/scratchpad.local.example.md`**, while they expect the **example** file to be the
one that receives framework updates so they can copy keys into **`.cursor/scratchpad.local.md`**
(or defaults).

### Overlap and duplicate evaluation

- **US-0057** (DONE): upgrade-safe **example** refresh — **treat as regression** if behavior
  diverges (example stale while baseline updates).
- **US-0073** / **DEC-0055**: Model B materialization of `scratchpad.md` — ordering must ensure
  **example catalog** is not older than template when baseline is refreshed.
- **DEC-0039**: framework-owned example — reaffirm; no user-data classification on example.

### Decomposition decision

- **Single story** **US-0075**: one contract for **example-first** / **non-lagging** example
  refresh across installers, CLI, manifest, template parity, diagnostics, and tests.

### Intake pack evidence

- selected_pack=`small-intake-pack`
- asked_topics=`outcome_success_criteria`,`impacted_components`,`constraints_compatibility_risks`,`required_tests_acceptance_checks`,`done_definition`
- missing_topics=`(none)`
- assumptions_confirmed=`(none)`

### Scope for TL / discovery

- Define deterministic **refresh ordering** and manifest ownership for:
  - `template/.cursor/scratchpad.local.example.md` → installed `.cursor/scratchpad.local.example.md`
  - vs `template/.cursor/scratchpad.md` → materialized `.cursor/scratchpad.md`
- Ensure **upgrade** and **install** paths cannot refresh baseline without refreshing example.
- Add **regression tests** and **operator diagnostics** per backlog ACs.
- Research anchor: **`R-0052`**.

### Recommendation

- Proceed **`/discovery`** then **`/research`** (extend **R-0052** with file-level evidence from
  current `installer.py` / manifest), then **`/architecture`** if a **DEC** amendment or new
  **DEC** is needed to lock ordering beyond **DEC-0055**.

---

