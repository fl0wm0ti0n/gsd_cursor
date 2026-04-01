# PO to TL archive pack (2026-03-30)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 35
- First archived heading: `## Intake handoff — BUG-0001 (2026-03-30, PO, `orchestrator_run_id=manual-20260330-BUG0001`)`
- Last archived heading: `## Intake handoff — BUG-0001 (2026-03-30, PO, `orchestrator_run_id=manual-20260330-BUG0001`)`
- Verification tuple (mandatory):
  - archived_body_lines=63
  - retained_body_lines=738

---

## Intake handoff — BUG-0001 (2026-03-30, PO, `orchestrator_run_id=manual-20260330-BUG0001`)

### Work item

- **`BUG-0001`** — **`OPEN`** — Template/install payload omits **`intake_*`** gate scripts (**`docs/product/backlog.md`** **`## Bug issues (canonical)`**).

### Evidence

- **`small-intake-pack`** bundle **`handoffs/intake_evidence/BUG-0001-intake-20260330.json`** — `python scripts/intake_evidence_validate.py --file handoffs/intake_evidence/BUG-0001-intake-20260330.json` → **`[INTAKE_EVIDENCE_VALIDATION_OK]`** (`intake_run_id=manual-20260330-BUG0001-intake`).
- Intake-time research **`R-0058`** — npm **`files`**/`template/` tarball behavior + repo inventory (**`template/scripts/`** lacks **`intake_*.py`**; **`scripts/`** has validators).

### User constraints

- Install **completeness** for **`/intake`** mandatory scripts only — **not** full active/`template/` mirroring.
- Preserve **triple-installer parity** when fixing copy lists or **`template/scripts/`** content.

### Overlap / duplicate check

- Related: **`US-0008`** (installer), **`US-0018`** (upgrade/new-file delivery) — distinct **defect** record for missing **`intake_*`** in shipped template.

### TL next phase

- **`/architecture`** — lock **`BUG-0001`** fix: **`template/scripts/`** intake completeness, **`package.json` `files`**, parity tests / **`US-0018`** (research complete **`auto-20260330-01`**; see **Research Addendum** below).

### Discovery Addendum — BUG-0001 (2026-03-30, PO, `orchestrator_run_id=auto-20260330-01`)

- **Evidence**: **`docs/engineering/state.md`** **Discovery checkpoint (2026-03-30) — BUG-0001 / auto-20260330-01**; repo inventory **`template/scripts/`** vs **`scripts/intake_*.py`**; **`package.json`** **`files`**.
- **Conclusions**: Gap confirmed — **`BUG-0001`** **OPEN**. Template ship path lacks all three intake gate modules; npm manifest does not list **`intake_*`** at repo **`scripts/`** root either (only **`doc_profile_lib.py`** alongside **`template/`**).
- **Research targets**: Frozen minimal file list for **`/intake`** gates; postinstall/copy semantics vs upgrade delivery (**`US-0018`**); parity across npm, Homebrew, Chocolatey; regression tests for validator self-test + bug routing guard in consumer layout.
- **Artifacts**: **`docs/product/backlog.md`**, **`docs/product/vision.md`**, **`handoffs/resume_brief.md`**, **`handoffs/po_to_tl.md`** (this addendum), **`docs/engineering/state.md`**.

### Research Addendum — BUG-0001 (2026-03-30, TL, `orchestrator_run_id=auto-20260330-01`)

- **Evidence**: **`docs/engineering/state.md`** **Research checkpoint (2026-03-30) — BUG-0001 / auto-20260330-01**; **`R-0058`** (extended); **`installer.ps1`** / **`installer.sh`** **`SOURCE_ROOT`→`template/`**; import scan **`scripts/intake_*.py`**.
- **Conclusions**: **Minimal intake payload** = three Python modules (**`intake_evidence_validate.py`**, **`intake_evidence_lib.py`**, **`intake_bug_routing_guard.py`**) — no extra repo-local imports beyond **`intake_evidence_lib`**. **Triple-installer parity** aligns on shipped **`template/`** because installers copy from **`template/`** only; **`BUG-0001`** **OPEN** until **`template/scripts/`** contains those files (+ architecture-owned **`files`**/test policy).
- **Next**: **`/architecture`** (TL) — **`DEC`**/task boundaries, optional pack-time or CI assertions.

### Architecture Addendum — BUG-0001 (2026-03-30, TL, `orchestrator_run_id=auto-20260330-01`)

- **Evidence**: **`docs/engineering/state.md`** **Architecture checkpoint (2026-03-30) — BUG-0001 / auto-20260330-01**; **`decisions/DEC-0063.md`**; **`docs/engineering/architecture.md`** **`# BUG-0001`**.
- **Conclusions**: **`DEC-0063`** — three **`intake_*`** files mirrored under **`template/scripts/`** (parity with **`scripts/`**); **`package.json` `files`** = **`template/`** primary, optional explicit **`scripts/intake_*.py`**; parity tests + **`US-0018`** upgrade delivery required for closure. **`BUG-0001`** **OPEN**.

### Sprint-plan Addendum — BUG-0001 (2026-03-30, TL, `orchestrator_run_id=auto-20260330-01`)

- **Evidence**: **`docs/engineering/state.md`** **Sprint-plan checkpoint (2026-03-30) — BUG-0001 / S0060 / auto-20260330-01**; **`sprints/S0060/sprint.md`**, **`sprints/S0060/tasks.md`**, **`sprints/S0060/plan-verify.json`** (**PENDING**).
- **Conclusions**: Sprint **`S0060`** — **T-001..T-005** ↔ sprint-local **AC-1..AC-5** mapped to **`BUG-0001`** acceptance themes + **`DEC-0063`**. **`BUG-0001`** **OPEN**. Next: **`/plan-verify`** (**QA**).

### Plan-verify Addendum — BUG-0001 / S0060 (2026-03-30, QA, `orchestrator_run_id=auto-20260330-01`)

- **Evidence**: **`docs/engineering/state.md`** **Plan-verify checkpoint (2026-03-30) — S0060 / BUG-0001 / auto-20260330-01**; **`sprints/S0060/plan-verify.json`** (**PASS**).
- **Conclusions**: **PASS** — bijection + governance verified; **`BUG-0001`** **OPEN**; **`acceptance.md`** unchanged. Next: **`/execute`**.

### Execute Addendum — BUG-0001 / S0060 (2026-03-30, dev, `orchestrator_run_id=auto-20260330-01`)

- **Evidence**: **`docs/engineering/state.md`** **Execute checkpoint (2026-03-30) — S0060 / BUG-0001 / auto-20260330-01**; **`sprints/S0060/summary.md`**; **`handoffs/dev_to_qa.md`**.
- **Conclusions**: **`DEC-0063`** delivery landed — **`template/scripts/`** intake trio + **`check_intake_template_parity.py`**; **`package.json` `files`**; **`installer-owned-paths.manifest`** (active + template); **`tests/run-tests.*`** §26N; README/runbook/architecture. **`BUG-0001`** **OPEN** (**US-0045**); **`acceptance.md`** unchanged. Next: **`/qa`**.

### Validator hygiene (same intake run)

- **`scripts/bug_issue_lib.py`**: **`extract_bug_section`** now matches **`## Bug issues (canonical)`** only at **line start** (`re.MULTILINE`), so inline citations in **`US-0079`** notes no longer hijack **`BUG-xxxx`** parsing — **`bug_issue_validate.py --check-acceptance`** green with **`BUG-0001`** present.

---

