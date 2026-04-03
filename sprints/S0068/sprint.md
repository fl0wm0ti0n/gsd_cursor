# Sprint S0068

- **Bug**: `BUG-0007`
- **Goal**: Fail-closed intake evidence truthfulness for **`asked_topics`** / **`topic_coverage`**: extend **`scripts/intake_evidence_lib.py`** **`validate_intake_evidence`** with duplicate / non-distinct **`answer_ref`** **`quoted_user_text`** guard across required **`small-intake-pack`** topics (exemptions per **DEC-0060** / **DEC-0067** — **`equivalent_evidence_ref`**, **`delegation_ref`**, **`assumption_confirmation_ref`**); surface **`INTAKE_ANSWER_REF_NOT_TOPIC_DISTINCT`** under **`INTAKE_PERSISTENCE_BLOCKED`**; tighten **`.cursor/commands/intake.md`** + **`template/`** mirror; automate **R-0066** regression matrix + **`intake_evidence_validate.py --self-test`** + **`check_intake_template_parity.py`** per **`docs/engineering/architecture.md`** **`# BUG-0007`**.
- **Status**: **Plan verified** — **`sprints/S0068/plan-verify.json`** **PASS** (`2026-04-04T19:15:00Z`, **qa**, `orchestrator_run_id=auto-20260404-01`); next **`/execute`** (**dev**).

## Scope (sprint-local AC themes)

- **AC-1** - **`scripts/intake_evidence_lib.py`**: deterministic duplicate-**`answer_ref`** / shared normalized **`quoted_user_text`** rule across distinct required-topic rows; locked **`INTAKE_ANSWER_REF_NOT_TOPIC_DISTINCT`**; preserve existing delegation / assumption / equivalent-evidence branches (**US-0083** non-regression).
- **AC-2** - **`.cursor/commands/intake.md`**: normative truthfulness — **`asked_topics`** only when user-visible question or allowed alternate; forbid synthetic per-topic **`answer_ref`** echo of one bug blob; cross-link **DEC-0060** / **DEC-0067** / **US-0083**.
- **AC-3** - **`template/.cursor/commands/intake.md`**: literal parity with active **`intake.md`** for all BUG-0007 contract edits.
- **AC-4** - **`tests/`**: new regression module covering **R-0066** matrix rows 1–5 (BUG-0007 exemplar **FAIL**; five distinct answers **PASS**; **`delegation_ref`** **PASS**; **`equivalent_evidence_ref`** **PASS**; **`assumption_confirmation_ref`** **PASS**), prefer **`validate_intake_evidence`** and/or subprocess on **`intake_evidence_validate.py`** as architecture directs.
- **AC-5** - **CLI / harness**: **`python scripts/intake_evidence_validate.py --self-test`** **PASS** after lib change; wire new tests into **`tests/run-tests.sh`** and **`tests/run-tests.ps1`** when a new module is added.
- **AC-6** - **Parity gate**: **`python scripts/check_intake_template_parity.py --repo .`** → **`[INTAKE_TEMPLATE_PARITY_OK]`** after any **`intake.md`** / paired script surface change.

## Governance

- `docs/engineering/architecture.md` `# BUG-0007`
- `docs/engineering/research.md` `R-0066`
- Related: `US-0045`, `US-0068`, `US-0078`, `US-0079`, `US-0083`, `DEC-0060`, `DEC-0067`, `R-0062`
