# PO to TL archive pack (2026-06-06)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 2
- Retained units in hot file: 14
- First archived heading: `## Intake handoff — BUG-0009 / cursor-20260606-BUG0009-intake`
- Last archived heading: `## Orchestrated discovery handoff — BUG-0009 / auto-20260606-02`
- Verification tuple (mandatory):
  - archived_body_lines=115
  - retained_body_lines=767

---

## Intake handoff — BUG-0009 / cursor-20260606-BUG0009-intake

### Target

- `bug_id=BUG-0009`
- `intake_run_id=cursor-20260606-BUG0009-intake`
- phase completed: **`intake`** (**`po`**)
- `next_scheduled_phase=discovery`
- `work_item_kind=bug` (`/intake bug`)
- `INTAKE_GUIDED_MODE=1`, `INTAKE_WORK_ITEM_KIND=bug` (argv override), `INTAKE_SUBAGENT_FALLBACK=deny`

### Summary

- **Defect**: its-magic copies its **own** repo CI (`.github/workflows/ci.yml`) into every generated/installed project via the byte-identical `template/.github/workflows/ci.yml`. That workflow contains its-magic-only self-packaging jobs — `npm-test` (`npm pack` → `its-magic-*.tgz` / `package.json`), `brew-test` (`sh installer.sh`), `choco-test` (`packaging/chocolatey` choco pack) — none of which exist in a downstream repo, so CI fails in **every** its-magic-created project (example: `finance_goblin`, exits 254 / 127 / 1).
- **Operator-confirmed scope (AskQuestion 2026-06-06)**:
  - `existing_repos=new_only` — fix new installs/upgrades; existing broken repos heal on their next its-magic `upgrade`/`clean` (re-copies corrected `ci.yml`).
  - `checks_failure=include` — also harden the generic `checks` job so it is tolerant/clear when a fresh project has no real tests/lint yet (avoid the `Tests or lint failed` hard-fail on empty projects).
- **Root-cause hypothesis (confirm in `/discovery`)**: active-repo CI and downstream-template CI were kept identical; no guard enforces `template/.github/workflows/ci.yml == .github/workflows/ci.yml` (only intake-script parity is guarded), so the template CI can be safely decoupled.
- Status authority: **OPEN** in `docs/product/backlog.md` per `US-0045`; closure flips at `/release`.

### Proposed fix direction (defer exact design to /architecture)

- Split CI: a **downstream-safe** `template/.github/workflows/ci.yml` (generic runbook-driven `checks` + `auto-fix` only, no self-packaging jobs) vs its-magic's **own internal** `.github/workflows/ci.yml` (keep `npm-test`/`brew-test`/`choco-test` for self-distribution).
- Add a **regression/drift guard** (test wired into `tests/run-tests.{sh,ps1}`) that fails if the template CI references its-magic self-packaging paths (`npm pack its-magic`, `installer.sh`, `packaging/chocolatey`, `packaging/homebrew`).
- Harden the generic `checks` job for empty fresh projects (clear "no real tests configured" path instead of a hard failure).
- Verify installer copy parity across `installer.ps1` / `installer.sh` / `installer.py` and `docs/engineering/context/installer-owned-paths.manifest`.

### Risks (carry to /discovery and /research)

- **Self-CI loss** if the split accidentally strips packaging jobs from the *active* repo CI — mitigation: drift guard must target only the template file, and its-magic's own CI must retain self-packaging coverage.
- **Stale broken repos** remain red until the operator upgrades — accepted per `new_only` scope; call out the upgrade remediation in release notes/docs.
- **Runbook-driven false fails** for downstream repos with placeholder commands — addressed by the `checks`-job hardening facet.

### Intake evidence (US-0078 / DEC-0060)

- `selected_pack=small-intake-pack`
- `asked_topics=outcome_success_criteria, impacted_components, constraints_compatibility_risks, required_tests_acceptance_checks, done_definition`
- `missing_topics=[]`; `assumptions_confirmed=(none)`
- Truthful satisfaction mix: `outcome_success_criteria` / `constraints_compatibility_risks` / `done_definition` = `answer_ref` (distinct quoted operator answers from the 2 AskQuestion rounds + original request); `impacted_components` / `required_tests_acceptance_checks` = `delegation_ref` (PO scoped from operator-supplied CI logs, not fabricated questions) per `BUG-0007` / `DEC-0067`.
- Validator: `python scripts/intake_evidence_validate.py --file handoffs/intake_evidence/BUG-0009-intake-20260606.json` → **`[INTAKE_EVIDENCE_VALIDATION_OK]`**.

### Evidence refs

- `docs/product/backlog.md` (`### BUG-0009` block — environment / steps / expected / actual / evidence_refs / intake_notes)
- `docs/product/acceptance.md` (`## Bug acceptance (canonical)` `BUG-0009` row — unchecked)
- `handoffs/intake_evidence/BUG-0009-intake-20260606.json` (canonical `ie:` refs per `DEC-0060`)
- `template/.github/workflows/ci.yml` + `.github/workflows/ci.yml` (identical source — leak origin); `docs/engineering/context/installer-owned-paths.manifest`; `installer.ps1` / `installer.sh` / `installer.py`
- `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` → **`[BUG_VALIDATION_OK]`**
- `handoffs/resume_brief.md` refreshed (DEC-0069): `python scripts/intake_bug_resume_brief_refresh.py --bug-id BUG-0009 ...` → **`[INTAKE_BUG_RESUME_BRIEF_REFRESH_OK]`**

### Next

- **`/discovery`** (fresh PO context) for `BUG-0009` — confirm leak root cause, the exact template-vs-active CI decoupling boundary, and the empty-project `checks` hardening behavior.

---

## Orchestrated discovery handoff — BUG-0009 / auto-20260606-02

### Target

- `bug_id=BUG-0009`
- `orchestrator_run_id=auto-20260606-02`
- phase completed: **`discovery`** (**`po`**)
- `next_scheduled_phase=research`
- `fresh_context_marker=po-BUG0009-discovery-20260606T141500Z-fresh`
- `segment_work_item_kind=bug`
- `bug_queue_position=1` / `bug_queue_remaining=3` (queue: BUG-0009→0010→0011)

### Summary

- **Defect confirmed**: byte-identical `template/.github/workflows/ci.yml` ↔ `.github/workflows/ci.yml` (SHA-256 `e51d2cb1…`, 11404 bytes) copies five jobs into every downstream repo via **US-0008** installer manifest (`.github/workflows` directory). Self-packaging jobs (`npm-test`, `brew-test`, `choco-test`) reference kit-only paths and fail in consumer repos (operator example: `finance_goblin`).
- **Discovery-locked decoupling**: template CI → `checks` + `auto-fix` only; active CI → retain all five jobs for kit self-distribution (**US-0007** / **US-0009**). **`US-0017` parity exception** for `ci.yml` (intentional active ≠ template).
- **checks hardening**: pass with explicit `no tests configured yet` when all runbook commands empty/skipped; fail only on actual configured-command failure.
- **Operator scope**: new installs/upgrades only; **US-0018** upgrade/clean heals existing broken repos.
- **Drift guard**: regression must block re-leak of forbidden self-packaging patterns in template CI.
- **`deploy.yml`**: already downstream-safe — no change.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Research asks (extend **`R-0075`**)

1. Template CI YAML shape (in-place job subtraction vs separate filename + manifest impact).
2. Drift-guard mechanism and harness section wiring.
3. Fresh-project `TEST_COMMAND` / **US-0063** bootstrap vs green-by-default `checks`.
4. **`US-0017`** negative-parity policy and `check_intake_template_parity.py` scope extension.
5. Install/upgrade smoke for post-copy `ci.yml` job inventory.
6. Release-note upgrade remediation wording.

### Top risks

- **R1**: Strip packaging jobs from active CI — guard must be template-scoped; active CI contract asserts five jobs remain.
- **R2**: Stale broken repos until upgrade — accepted; document remediation.
- **R3**: Installer copies wrong workflow — install-completeness fixture (**BUG-0003** class).

### Evidence refs

- `docs/product/backlog.md` (`### BUG-0009` — discovery_notes)
- `docs/product/vision.md` (**Intake notes — BUG-0009**, **Discovery Notes — BUG-0009**)
- `docs/product/acceptance.md` (`BUG-0009` row — unchecked)
- `handoffs/intake_evidence/BUG-0009-intake-20260606.json`
- `docs/engineering/research.md` (**`R-0075`** discovery extension)
- `template/.github/workflows/ci.yml`, `.github/workflows/ci.yml`, `docs/engineering/context/installer-owned-paths.manifest`
- `docs/engineering/state.md` (Discovery checkpoint — this run)
- `handoffs/resume_brief.md` (top pointer → `/research`)
- Related: **US-0007**, **US-0008**, **US-0017**, **US-0018**, **US-0063**

### Next

- **`/research`** (fresh **tech-lead** context) for **`BUG-0009`** — resolve **`R-0075`** Q1–Q6 before **`/architecture`**.

### Decision gate

- **None** — discovery satisfied; bug **OPEN**.

---

