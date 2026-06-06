# PO to TL archive pack (2026-06-06)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 14
- First archived heading: `## Orchestrated research handoff — BUG-0009 / auto-20260606-02`
- Last archived heading: `## Orchestrated research handoff — BUG-0009 / auto-20260606-02`
- Verification tuple (mandatory):
  - archived_body_lines=52
  - retained_body_lines=766

---

## Orchestrated research handoff — BUG-0009 / auto-20260606-02

### Target

- `bug_id=BUG-0009`
- `orchestrator_run_id=auto-20260606-02`
- phase completed: **`research`** (**`tech-lead`**)
- `fresh_context_marker=tl-BUG0009-research-20260606T155605Z-fresh`
- `next_scheduled_phase=architecture`
- `segment_work_item_kind=bug`
- `bug_queue_position=1` / `bug_queue_remaining=3`

### Summary

- **`/research`** **PASS** — extended **`R-0075`** with Q1–Q6 resolution. **Template CI**: in-place job subtraction in `template/.github/workflows/ci.yml` (retain `checks` + `auto-fix`; remove packaging jobs); keep `ci.yml` filename and installer manifest unchanged. **Drift guard**: new `scripts/check_downstream_ci_guard.py` (template forbidden-pattern scan + active five-job positive inventory) + contract-test markers + harness **§28B**; no byte-parity scope on `check_intake_template_parity.py`. **Runbook**: empty `TEST_COMMAND` in shipped template runbook (US-0063 bootstrap fills); checks workflow "no tests configured yet" summary; active kit runbook keeps harness. **Install smoke**: extend `installer_completeness_bug0003_test.py` for post-install/upgrade job inventory. **Docs**: upgrade remediation blurb for stale pre-fix repos.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Key findings (architecture inputs)

1. **CI split shape (Q1)**: Option A in-place subtraction — reject separate filename and cross-repo reusable workflow (EARLY_RESEARCH: template-copy model per US-0008).
2. **Guard contract (Q2)**: Forbidden patterns (`npm-test`, `brew-test`, `choco-test`, `npm pack`, `its-magic-*.tgz`, `installer.sh`, `packaging/chocolatey`, `packaging/homebrew`); reason codes `DOWNSTREAM_CI_FORBIDDEN_PATTERN`, `DOWNSTREAM_CI_JOB_LEAK`, `KIT_CI_PACKAGING_JOBS_MISSING`.
3. **Green-by-default (Q3)**: Template `TEST_COMMAND` empty on ship; US-0063 writes baseline when unset; fail only on configured command failure.
4. **US-0017 negative parity (Q4)**: `ci.yml` intentional active ≠ template; optional runbook `TEST_COMMAND` line exception — architecture locks companion DEC.
5. **Install smoke (Q5)**: Job-inventory tests on `missing` + `upgrade` modes.
6. **Remediation copy (Q6)**: `its-magic --mode upgrade` refreshes broken `ci.yml`.

### Evidence refs

- `docs/engineering/research.md` (**`R-0075`** research extension)
- `docs/product/backlog.md` (`### BUG-0009` — `research_notes`)
- `docs/product/acceptance.md` (`BUG-0009` row — unchecked)
- `handoffs/intake_evidence/BUG-0009-intake-20260606.json`
- `template/.github/workflows/ci.yml`, `.github/workflows/ci.yml`, `docs/engineering/context/installer-owned-paths.manifest`
- `docs/engineering/state.md` (Research checkpoint — this run)
- `handoffs/resume_brief.md` (architecture pointer)

### Architecture asks (companion DEC-xxxx)

1. Lock US-0017 negative-parity exception table (`ci.yml` + optional runbook `TEST_COMMAND` line).
2. Author `docs/engineering/architecture.md` **`# BUG-0009`** with guard script contract, forbidden-pattern list, checks semantics, template parity inventory.
3. Confirm lib split (`downstream_ci_guard_lib.py` vs monolithic script) and harness section id (**§28B** candidate).

### Next

- **`/architecture`** (fresh **tech-lead** context) for **`BUG-0009`** — lock companion DEC + architecture section before **`/sprint-plan`**.

### Decision gate

- **None** — research satisfied; bug **OPEN**.

---

