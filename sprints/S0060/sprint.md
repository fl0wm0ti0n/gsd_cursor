# Sprint S0060

- **Bug**: `BUG-0001`
- **Goal**: **Intake gate script install completeness** — ship the three mandatory **`intake_*`** modules under **`template/scripts/`** in parity with repo **`scripts/`** (**`DEC-0063`** §1), align **`package.json` `files`** with §2, add deterministic parity/regression gates (**§3**, **`US-0030`**), prove **`US-0018`** upgrade delivery for changed intake files (**§4**), and document operator/installer expectations where gaps exist. Canonical portfolio acceptance remains **`docs/product/acceptance.md`** **`BUG-0001`** row (**unchecked** until **`/verify-work`**).
- **Status**: **Verify-work complete — ready for release** — QA **`/qa`** + **`/verify-work`** **`2026-03-30`** (`orchestrator_run_id=auto-20260330-01`); **`sprints/S0060/plan-verify.json`** **PASS**; **`docs/product/acceptance.md`** **`BUG-0001`** **checked**; **`BUG-0001`** **DONE** in backlog (**US-0045**).

## Scope (sprint-local AC themes ↔ backlog **expected**)

- **AC-1** — **Minimal mirror**: **`template/scripts/intake_evidence_validate.py`**, **`intake_evidence_lib.py`**, **`intake_bug_routing_guard.py`** present and match **`scripts/`** counterparts per **`DEC-0063`** §1 (transitive import bar: **`intake_evidence_lib`** only).
- **AC-2** — **`package.json` `files`**: **`template/`** remains primary ship vehicle; optional explicit **`scripts/intake_*.py`** entries only if lockstep parity is enforced (**`DEC-0063`** §2).
- **AC-3** — **Parity CI**: deterministic check (script or test) that the intake trio exists under **`template/scripts/`** and matches **`scripts/`**; wired into **`tests/run-tests.*`** or CI-equivalent per repo convention.
- **AC-4** — **`US-0018` upgrade**: intake files classified for framework upgrade so **`--mode upgrade`** delivers new/changed modules; evidence in sprint QA/UAT matrix or state pointer (**`DEC-0063`** §4).
- **AC-5** — **Operator + triple path**: README/runbook (or packaging notes) states where intake scripts live post-install; spot-check **npm / Chocolatey / Homebrew** surfaces remain consistent with **`template/`**-sourced truth (**`R-0058`**).

## Governance

- **`decisions/DEC-0063.md`**
- **`docs/engineering/architecture.md`** **`# BUG-0001`**
- **`docs/engineering/research.md`** **`R-0058`**
- Related: **`DEC-0061`** (bug schema), **`US-0018`** (upgrade), **`US-0030`** (active/**`template/`** parity)
