## Dev -> QA Handoff — S0068 / BUG-0007 (`auto-20260404-01`)

### Scope

- Implemented **`docs/engineering/architecture.md`** **`# BUG-0007`** / **`R-0066`**: **`INTAKE_ANSWER_REF_NOT_TOPIC_DISTINCT`** in **`scripts/intake_evidence_lib.py`** (duplicate **`quoted_user_text`** across distinct required **`topic_key`** rows under **`answer_ref`**, with **`equivalent_evidence_ref`**, **`delegation_ref`**, and **`assumption_confirmation_ref`** exemptions); **`template/scripts/intake_evidence_lib.py`** byte parity.
- **`.cursor/commands/intake.md`** + **`template/.cursor/commands/intake.md`**: truthful **`asked_topics`** / **`topic_coverage`**; forbid synthetic echo; **DEC-0060** / **DEC-0067** / **US-0083** cross-links.
- **`tests/intake_evidence_bug0007_r0066_test.py`** (**R-0066** rows **1–5**); **`tests/run-tests.sh`** / **`tests/run-tests.ps1`** section **26R**.

### What changed (verification targets)

- **`scripts/intake_evidence_lib.py`**, **`template/scripts/intake_evidence_lib.py`**
- **`.cursor/commands/intake.md`**, **`template/.cursor/commands/intake.md`**
- **`tests/intake_evidence_bug0007_r0066_test.py`**, **`tests/run-tests.sh`**, **`tests/run-tests.ps1`**

### Evidence pointers

- **`sprints/S0068/summary.md`**, **`sprints/S0068/tasks.md`** (**T-001..T-006** **done**)
- **`docs/product/backlog.md`** (**`execute_notes`** under **`BUG-0007`**)
- **`handoffs/resume_brief.md`** (**`next_scheduled_phase=qa`**)
- **`docs/engineering/state.md`** — execute checkpoint (**DEC-0038** strict proof)

### Tests / checks run (dev)

| Command | Outcome |
|---------|---------|
| `python scripts/intake_evidence_validate.py --self-test` | PASS |
| `python tests/intake_evidence_fixtures_test.py` | PASS |
| `python tests/intake_evidence_bug0007_r0066_test.py` | PASS |
| `python scripts/check_intake_template_parity.py --repo .` | `[INTAKE_TEMPLATE_PARITY_OK]` |

### Next phase

- **`/qa`** for **`S0068`** / **`BUG-0007`** (`next_scheduled_phase=qa`).

---

## Dev -> QA Handoff — S0067 / BUG-0006 (`auto-20260403-03`)

### Scope

- Implemented **`docs/engineering/architecture.md`** **`# BUG-0006`**: spawn-only **`/auto`** contract on **`.cursor/commands/auto.md`** and **`template/.cursor/commands/auto.md`** (**`AUTO_ORCHESTRATOR_PHASE_EXECUTION`**, forbidden orchestrator phase work / phase deliverables); mirrored in **`docs/engineering/auto-orchestration-reference.md`** with **`decisions/DEC-0029.md`** / **`decisions/DEC-0038.md`** cross-links.
- Extended **`tests/auto_command_contract_test.py`** (**R-0065**): required literals, negative phrasing checks, active/template parity, reference substring checks.
- Canonical backlog status remains **OPEN** in **`docs/product/backlog.md`** until QA / verify-work.

### What changed (verification targets)

- **`.cursor/commands/auto.md`**, **`template/.cursor/commands/auto.md`**, **`docs/engineering/auto-orchestration-reference.md`**
- **`tests/auto_command_contract_test.py`** (harness: **`tests/run-tests.sh`** / **`tests/run-tests.ps1`** section **26M** — unchanged wiring)

### Evidence pointers

- **`sprints/S0067/summary.md`**, **`sprints/S0067/tasks.md`** (**T-001..T-005** **done**)
- **`docs/product/backlog.md`** (**`execute_notes`** under **`BUG-0006`**)
- **`handoffs/resume_brief.md`** (**`next_scheduled_phase=qa`**)
- **`docs/engineering/state.md`** — execute checkpoint (**DEC-0038** strict proof)

### Tests / checks run (dev)

| Command | Outcome |
|---------|---------|
| `python tests/auto_command_contract_test.py` | PASS |

### Next phase

- **`/qa`** for **`S0067`** / **`BUG-0006`** (`next_scheduled_phase=qa`).

---

## Dev -> QA Handoff — S0066 / BUG-0005 (`auto-20260403-02`)

### Scope

- Implemented **`DEC-0069`** / **`architecture.md`** **`# BUG-0005`**: deterministic **`handoffs/resume_brief.md`** refresh at successful **`/intake bug`** persistence via **`scripts/intake_bug_resume_brief_refresh.py`** (atomic write, **`discovery`** resume seed, **`US-0045`** guards).
- Canonical backlog status remains **OPEN** in **`docs/product/backlog.md`** until QA / verify-work.

### What changed (verification targets)

- **`scripts/intake_bug_resume_brief_refresh.py`** + **`template/scripts/intake_bug_resume_brief_refresh.py`** (parity via **`check_intake_template_parity.py`**).
- **`.cursor/commands/intake.md`**, **`template/.cursor/commands/intake.md`**: bug persistence checklist + outputs + ownership note for **`resume_brief`**.
- **`docs/engineering/artifact-ownership-policy.md`**, **`template/docs/engineering/artifact-ownership-policy.md`**: **`intake`** allowed for **`resume_brief`** on bug-intake completion (**DEC-0069**).
- **`tests/intake_bug_resume_brief_bug0005_test.py`**: **R-0064** regression matrix; **`run-tests.sh` / `run-tests.ps1`** section **26Q**.

### Evidence pointers

- **`sprints/S0066/summary.md`**, **`sprints/S0066/tasks.md`** (**T-001..T-009** **done**)
- **`docs/product/backlog.md`** (**`execute_notes`** under **`BUG-0005`**)
- **`handoffs/resume_brief.md`** (**`next_scheduled_phase=qa`**)

### Tests / checks run (dev)

| Command | Outcome |
|---------|---------|
| `python tests/intake_bug_resume_brief_bug0005_test.py` | PASS |
| `python scripts/intake_bug_resume_brief_refresh.py --self-test` | PASS |
| `python scripts/check_intake_template_parity.py --repo .` | PASS |
| `python scripts/enforce-triad-hot-surface.py --rollover` then `--check` | PASS (post-`state.md` append) |

### Suggested QA focus

- Confirm intake command documents the refresh step and failure codes (**`INTAKE_RESUME_BRIEF_*`**).
- Spot-check generated **`resume_brief`** latest pointer for **`discovery`** seeds and **`resolution_source=resume_brief`** after a fixture **`/intake bug`** dry run (optional manual).
- Run section **26Q** via full harness if applicable.

### Next phase

- **`/qa`** for **`S0066`** / **`BUG-0005`** (`next_scheduled_phase=qa`).

---

## Dev -> QA Handoff - S0064 / US-0083 (`auto-20260331-04`)

### Scope

- Implemented execute scope for **`US-0083`** per **`DEC-0067`** / **`docs/engineering/architecture.md`** `# US-0083` / `R-0062`.
- Canonical backlog status remains **OPEN** in `docs/product/backlog.md` (**US-0045**), pending QA and verify-work.

### What changed (verification targets)

- **Delegation validator branch (active + template)**:
  - `scripts/intake_evidence_lib.py` and `template/scripts/intake_evidence_lib.py` now accept
    `topic_coverage[].satisfied_by=delegation_ref`.
  - Delegated rows require bounded metadata:
    `delegation_scope`, `delegation_rationale`, `delegation_confidence` (`low|medium|high`).
  - Deterministic fail codes:
    - `INTAKE_DELEGATION_EVIDENCE_MISSING`
    - `INTAKE_DELEGATION_EVIDENCE_INVALID`
  - Non-delegated unresolved required topics remain fail-closed under
    `INTAKE_REQUIRED_TOPIC_MISSING`.
- **Repetitive prompt suppression with accounting**:
  - Added optional row metadata support:
    `evidence_source=equivalent_evidence_ref` + `equivalent_evidence_ref`,
    allowing equivalent pre-captured evidence without forcing repeated asks.
- **Command/guidance updates (active + template parity)**:
  - `.cursor/commands/intake.md`, `.cursor/agents/po.mdc`, and `docs/engineering/runbook.md`
    now document ask-vs-delegate behavior, delegated evidence requirements, and deterministic diagnostics.
- **Regression matrix expansion**:
  - `tests/intake_evidence_fixtures_test.py` now covers:
    - delegated pass (complete evidence),
    - delegated missing/invalid evidence fail,
    - non-delegated unresolved required-topic fail,
    - equivalent-evidence accounting pass,
    - guided/low-touch parity for new delegated paths.

### Evidence pointers

- `sprints/S0064/summary.md`
- `sprints/S0064/tasks.md` (T-001..T-010 **done**)
- `docs/product/backlog.md` (`US-0083` execute notes)
- `handoffs/resume_brief.md` (next scheduled phase `qa`)

### Tests / checks run (dev)

| Command | Outcome |
|---------|---------|
| `python tests/intake_evidence_fixtures_test.py` | PASS |
| `python scripts/intake_evidence_validate.py --self-test` | PASS |
| `python scripts/check_intake_template_parity.py --repo .` | PASS |

### Suggested QA focus

- Validate delegated required-topic pass path and deterministic blocked diagnostics for missing/invalid delegation evidence.
- Confirm non-delegated unresolved required topics still fail with `INTAKE_REQUIRED_TOPIC_MISSING` + `INTAKE_PERSISTENCE_BLOCKED`.
- Verify guided/low-touch parity for delegated and non-delegated matrices.
- Spot-check active/template parity for all touched intake command/guidance/script surfaces.

### Next phase

- **`/qa`** for **`S0064`** / **`US-0083`** (`next_scheduled_phase=qa`).

---

## Dev → QA Handoff — S0063 / BUG-0003 (`auto-20260331-03`)

### Scope

- Implemented execute scope for **`BUG-0003`** per **`DEC-0066`** / **`docs/engineering/architecture.md`** `# BUG-0003`.
- Canonical backlog status remains **OPEN** in `docs/product/backlog.md` (**US-0045**), pending QA and verify-work.

### What changed (verification targets)

- **Manifest contract** (active + template): `docs/engineering/context/installer-owned-paths.manifest` now includes:
  - `scripts/enforce-triad-hot-surface.py` in `install_include_paths`,
  - matching clean ownership in `clean_paths`,
  - explicit `[required_install_script_paths]` inventory (single required-script source).
- **Installer completeness invariant**:
  - `installer.py` now performs deterministic post-install required-script validation for `missing` and `upgrade`,
  - deterministic diagnostics: `INSTALL_COMPLETENESS_FAILED`, `INSTALL_REQUIRED_SCRIPT_MISSING:<path>`,
  - remediation text points to manifest parity + rerun guidance,
  - hidden helper paths for parity wiring: `--validate-install-completeness`, `--source-root` (test fixture use).
- **Wrapper parity**:
  - `installer.ps1`, `installer.sh` now delegate completeness validation to Python (`installer.py --validate-install-completeness`) for identical reason-code semantics.
- **Template parity**:
  - added `template/scripts/enforce-triad-hot-surface.py` mirror (required script now shipped by installer source tree).
- **Runbook remediation** (active + template):
  - `docs/engineering/runbook.md` updated with BUG-0003 completeness gate, fail codes, and remediation workflow.
- **Regression coverage**:
  - new `tests/installer_completeness_bug0003_test.py` (positive missing/upgrade, deterministic negative staged omission, active/template parity, install/clean symmetry),
  - integrated into `tests/run-tests.ps1` and `tests/run-tests.sh`.

### Evidence pointers

- `sprints/S0063/summary.md`
- `sprints/S0063/tasks.md` (T-001..T-010 **done**)
- `docs/engineering/state.md` (execute checkpoint + phase boundary + strict proof + triad hygiene)
- `handoffs/resume_brief.md` (next scheduled phase moved to `qa`)

### Tests / checks run (dev)

| Command | Outcome |
|---------|---------|
| `python tests/installer_completeness_bug0003_test.py` | PASS |
| `python installer.py --validate-install-completeness --target .` | PASS |
| `powershell -ExecutionPolicy Bypass -File tests/run-tests.ps1` | PARTIAL — BUG-0003 additions pass (including new installer completeness fixtures); suite exit `1` from pre-existing Homebrew stable formula vs npm version assertions (`tests/report.md`) |

### Suggested QA focus

- Confirm `missing` and `upgrade` both fail closed with deterministic diagnostics when a required script path is absent from staged source.
- Verify active/template manifest + required script parity and install/clean symmetry (`[required_install_script_paths]` subset of both install and clean sections).
- Spot-check wrapper parity: `installer.ps1` / `installer.sh` reason-code outputs match Python contract for completeness failures.

### Next phase

- **`/qa`** for **`S0063`** / **`BUG-0003`** (`next_scheduled_phase=qa`).
