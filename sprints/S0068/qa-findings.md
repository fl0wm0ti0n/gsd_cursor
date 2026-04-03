# QA findings — Sprint S0068 (BUG-0007)

- **Verdict**: **PASS** — proceed to **`/verify-work`** in fresh **qa** context.
- **Orchestrator run**: **`auto-20260404-01`**
- **Scope**: **`INTAKE_ANSWER_REF_NOT_TOPIC_DISTINCT`** in **`scripts/intake_evidence_lib.py`** (+ **`template/scripts/`** parity); truthful **`intake.md`** (active + template); **R-0066** regression **`tests/intake_evidence_bug0007_r0066_test.py`**; harness **26R**; **`intake_evidence_validate.py --self-test`**; **`check_intake_template_parity.py`**; **`tests/intake_evidence_fixtures_test.py`** (US-0083 non-regression).

## Test plan

1. Library self-test and template parity for touched intake surfaces.
2. **R-0066** matrix via **`tests/intake_evidence_bug0007_r0066_test.py`**.
3. Guided/low-touch and delegation paths via **`tests/intake_evidence_fixtures_test.py`**.
4. Exemplar **`handoffs/intake_evidence/BUG-0007-intake-20260403.json`** must **FAIL** validation with **`INTAKE_ANSWER_REF_NOT_TOPIC_DISTINCT`** (deterministic duplicate **`quoted_user_text`** under **`answer_ref`** across required **`topic_key`** values).

## Commands executed

| Command | Outcome |
|---------|---------|
| `python scripts/intake_evidence_validate.py --self-test` | **PASS** (`[INTAKE_EVIDENCE_SELF_TEST_OK]`) |
| `python tests/intake_evidence_bug0007_r0066_test.py` | **PASS** (`[INTAKE_EVIDENCE_VALIDATION_OK]` from fixture assertions) |
| `python tests/intake_evidence_fixtures_test.py` | **PASS** (`[INTAKE_EVIDENCE_FIXTURES_OK]`) |
| `python scripts/check_intake_template_parity.py --repo .` | **PASS** (`[INTAKE_TEMPLATE_PARITY_OK]`) |
| `python scripts/intake_evidence_validate.py --file handoffs/intake_evidence/BUG-0007-intake-20260403.json` | **FAIL (expected)** exit **1**; stderr includes **`primary_codes=INTAKE_ANSWER_REF_NOT_TOPIC_DISTINCT`** (with **`INTAKE_PERSISTENCE_BLOCKED`**) |

## Findings

- **No defects** blocking verify-work: duplicate-**`answer_ref`** guard behaves as specified; exemplar JSON is correctly rejected; regression and fixture suites green; active/template parity OK.

## Artifacts

- **`handoffs/dev_to_qa.md`** — scope consumed.
- **`handoffs/qa_to_verify_work.md`**, **`handoffs/resume_brief.md`** — continuation to **`/verify-work`**.
- **`docs/product/backlog.md`** — **`qa_notes`** under **`### BUG-0007`**.
- **`docs/engineering/state.md`** — QA checkpoint + **DEC-0038** strict proof + **DEC-0054** triad hygiene.
