# PO to TL archive pack (2026-06-07)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 2
- Retained units in hot file: 13
- First archived heading: `## Intake handoff — BUG-0010 / cursor-20260606-BUG0010-intake`
- Last archived heading: `## Orchestrated discovery handoff — US-0091 / auto-20260606-01`
- Verification tuple (mandatory):
  - archived_body_lines=120
  - retained_body_lines=739

---

## Intake handoff — BUG-0010 / cursor-20260606-BUG0010-intake

### Target

- `bug_id=BUG-0010`
- `intake_run_id=cursor-20260606-BUG0010-intake`
- phase completed: **`intake`** (**`po`**)
- `next_scheduled_phase=discovery`
- `work_item_kind=bug` (`/intake bug`)
- `INTAKE_GUIDED_MODE=1`, `INTAKE_WORK_ITEM_KIND=bug` (argv override), `INTAKE_SUBAGENT_FALLBACK=deny`

### Summary

- **Defect**: Triad archiver (`scripts/enforce-triad-hot-surface.py`) only splits `docs/engineering/architecture.md` on H1 `# US-xxxx` headings. Repos where agents wrote story sections as `## US-xxxx` hit `STATE_ARCHIVE_BOUNDARY_AMBIGUOUS` when the file exceeds `ARCH_HOT_MAX_LINES` — rollover finds zero chunks, `/auto` stops with non-suppressible `blocked` (operator report: discovery PASS on US-0016, then triad gate fail at 3021/3000 lines).
- **Operator fix choice (AskQuestion)**: **both** — (1) extend archiver to recognize `## US-xxxx` as story-section boundaries (backward-compatible rollover); (2) enforce H1 `# US-xxxx` for new `/architecture` writes (validator + command/template parity per **DEC-0054**).
- Distinct from **BUG-0009** (CI template leak). Related governance: **US-0072**, **DEC-0054**, **DEC-0043**.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Proposed fix direction (defer exact design to /architecture)

- Extend `STORY_HEADING` / `split_arch_stories` to treat `## US-xxxx` as archival units (oldest-first, same as `# US-xxxx`).
- Add heading-level validator or contract test; update `.cursor/commands/architecture.md` (+ `template/`) to mandate H1 `# US-xxxx` for new sections.
- Regression: `##`-only fixture rollovers when over cap; `# US-` non-regression; `enforce-triad-hot-surface.py --self-test` extended; runbook operator note for one-time `##`→`#` normalization in existing repos.

### Risks

- **Double-counting** if both `# US-` and `## US-` exist at same id — architecture must define precedence.
- **Nested `##` inside a US block** — archiver must not split on non-story `##` headings.
- **Kit repo mixed headings** — this repo already has 30 `# US-` + 5 `## US-` sections; fix must handle mixed files.

### Intake evidence (US-0078 / DEC-0060)

- `selected_pack=small-intake-pack`; `missing_topics=[]`; `assumptions_confirmed=(none)`
- `outcome_success_criteria` + `constraints_compatibility_risks` = `answer_ref` (operator chat + **both** fix choice); `impacted_components` / `required_tests_acceptance_checks` / `done_definition` = `delegation_ref` per **DEC-0067**
- Validator: `python scripts/intake_evidence_validate.py --file handoffs/intake_evidence/BUG-0010-intake-20260606.json` → **`[INTAKE_EVIDENCE_VALIDATION_OK]`**

### Evidence refs

- `docs/product/backlog.md` (`### BUG-0010`); `docs/product/acceptance.md` (unchecked row)
- `handoffs/intake_evidence/BUG-0010-intake-20260606.json`
- `scripts/enforce-triad-hot-surface.py` (`STORY_HEADING`, `rollover_architecture`); `decisions/DEC-0054.md`
- `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` → **`[BUG_VALIDATION_OK]`**
- `handoffs/resume_brief.md` refreshed: **`[INTAKE_BUG_RESUME_BRIEF_REFRESH_OK]`** (`bug_id=BUG-0010`, `intended_resume_phase=discovery`)

### Next

- **`/discovery`** (fresh PO context) for **BUG-0010** — confirm heading-mix inventory, archiver precedence rules, and enforcement surface for `/architecture`.

---

## Orchestrated discovery handoff — US-0091 / auto-20260606-01

### Target

- `story_id=US-0091`
- `orchestrator_run_id=auto-20260606-01`
- phase completed: **`discovery`** (**`po`**)
- `next_scheduled_phase=research`
- `fresh_context_marker=po-US0091-discovery-20260606T132027Z-fresh`
- `decomposition=single_story` (operator explicit; per `US-0051`)
- `priority=P1`
- `backlog_drain_active=true`

### Summary

- **Static-coverage gap**: `US-0030` (DONE) blocks README/runbook **deltas** when commands/flags change; it does **not** assert that every DONE user-visible feature already has a blurb. `US-0091` closes that gap with audit + backfill + a **second blocking check** in the `/release` doc-gate surface.
- **Three-file target** (audience + parity): root `README.md` (operator blurbs), `template/README.md` (byte parity per `US-0017`), `docs/developer/README.md` (`DEV_*` traceability rows per `DEC-0059`).
- **Discovery-locked predicate**: backlog block field **`user_visible: true|false`** is canonical validator input; optional acceptance row `(user_visible)` suffix is human-scan only. In-scope = **DONE** + `user_visible: true` (explicit) or migration-heuristic pass for unset fields; out-of-scope = `user_visible: false` or pure-internal surfaces. Ambiguous → `README_FEATURE_COVERAGE_INPUT_INVALID`.
- **Section placement**: backfill adds **bullets/sub-entries within existing H2s** — no new H2s; affinity map in vision/backlog discovery notes; `validate_doc_profile.py` section budgets unchanged.
- **Grandfathering**: blocking gate activates in the **same sprint/commit** as backfill — no retroactive `/release` block before catalog is populated (**AC-10**).
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Acceptance pointers (discovery emphasis)

- **AC-1**: predicate + `user_visible` marker contract (backlog field canonical).
- **AC-2**: deterministic audit report (`coverage_total` / gaps list).
- **AC-3–AC-4**: three-file backfill + audience/profile compliance.
- **AC-5–AC-7**: validator script, `/release` composition on `US-0030`, idempotent `--report`.
- **AC-8–AC-9**: `US-0071` hygiene + `US-0017` template parity for new script/content.
- **AC-10**: companion `DEC-xxxx` with grandfathering + composition semantics.

### Top risks (carry to /research)

- **R1** False positives without bounded predicate — mitigation: explicit `user_visible` markers + fail-closed ambiguous.
- **R2** README bloat across ~90 DONE stories — mitigation: 1–2 sentence blurbs, existing section budgets.
- **R3** Three-file parity drift — mitigation: compose with `US-0017`, extend parity tests not duplicate logic.
- **R4** Retroactive release lock-in — mitigation: same-sprint atomic delivery + grandfathering toggle.
- **R5** `US-0071` token leakage in backfilled prose — mitigation: existing scanner stays green.
- **R6** Migration heuristic ambiguity for unset `user_visible` — mitigation: research locks deterministic rules table.

### Research asks (extend **`R-0074`**)

1. Validator placement and CLI grammar — candidate `scripts/validate_readme_feature_coverage.py` with `--self-test`, `--report`, stable JSON (`coverage_total` / `coverage_present` / `coverage_missing`).
2. Release-gate wiring point — where `/release` / `validate-and-push` invokes the second check (active + `template/`).
3. Migration heuristic table — deterministic rules for unset `user_visible` during one-time backfill pass.
4. Section-affinity manifest — `US-xxxx`/`BUG-xxxx` → root H2 + DEV H2 anchor (no new headings).
5. Grandfathering / first-activation toggle — report-only vs blocking enablement contract.
6. Template parity inventory — extend `check_intake_template_parity.py` or sibling test for new validator script paths.

### Evidence refs

- `docs/product/backlog.md` (`## US-0091` — discovery_notes appended)
- `docs/product/vision.md` (**Discovery Notes — US-0091**)
- `docs/product/acceptance.md` (`US-0091` row — unchecked)
- `handoffs/intake_evidence/US-0091-intake-20260510.json`
- `docs/engineering/research.md` (**`R-0074`** — discovery extension appended)
- `docs/engineering/state.md` (Discovery checkpoint — this run)
- `handoffs/resume_brief.md` (top pointer → `/research`)
- Adjacent: `US-0030`, `US-0077`/`DEC-0059`, `US-0017`, `US-0071`, `DEC-0040`

### Next

- **`/research`** (fresh **tech-lead** context) for **`US-0091`** — deepen **`R-0074`**, lock validator/release wiring, migration heuristic, and grandfathering before **`/architecture`**.

### Decision gate

- **None** — discovery satisfied; research readiness explicit.

---

