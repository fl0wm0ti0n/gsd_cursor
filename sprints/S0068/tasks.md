# Sprint S0068 Tasks

- **Bug**: `BUG-0007`
- **Sprint**: `S0068`
- **Governance**: `architecture.md` `# BUG-0007`; `R-0066`; `US-0045`

| Task | Status | Description | AC |
|---|---|---|---|
| T-001 | done | Implement **`validate_intake_evidence`** guard in **`scripts/intake_evidence_lib.py`**: non-distinct **`quoted_user_text`** across **`satisfied_by=answer_ref`** rows for distinct required **`topic_key`** values (normalized per existing lib rules); emit **`INTAKE_ANSWER_REF_NOT_TOPIC_DISTINCT`**; exempt **`delegation_ref`**, **`equivalent_evidence_ref`** / **`evidence_source`**, **`assumption_confirmation_ref`** paths; tune so **`handoffs/intake_evidence/BUG-0007-intake-20260403.json`** **FAIL**s and five-distinct-answers case **PASS**es | AC-1 |
| T-002 | done | Update **`.cursor/commands/intake.md`**: truthful **`asked_topics`** / **`topic_coverage`** authoring; forbid echoing one user blob across all keys as fake **`answer_ref`**; cross-link **DEC-0060** / **DEC-0067** / **US-0083** | AC-2 |
| T-003 | done | Mirror **`T-002`** contract edits in **`template/.cursor/commands/intake.md`** | AC-3 |
| T-004 | done | Add **`tests/`** regression coverage for **R-0066** table rows **1–5** (exemplar-style **FAIL** with **`INTAKE_ANSWER_REF_NOT_TOPIC_DISTINCT`**; distinct short answers; **`delegation_ref`**; **`equivalent_evidence_ref`**; **`assumption_confirmation_ref`**) — fixtures or minimal JSON builders as appropriate | AC-4 |
| T-005 | done | Confirm **`python scripts/intake_evidence_validate.py --self-test`** **PASS**; register new test module in **`tests/run-tests.sh`** and **`tests/run-tests.ps1`** (section placement consistent with existing intake/evidence tests) | AC-5 |
| T-006 | done | Run **`python scripts/check_intake_template_parity.py --repo .`** → **`[INTAKE_TEMPLATE_PARITY_OK]`**; fix any **`template/`** drift introduced by **`T-002`–`T-003`** | AC-6 |

## Deterministic AC-to-task mapping

- AC-1 -> T-001
- AC-2 -> T-002
- AC-3 -> T-003
- AC-4 -> T-004
- AC-5 -> T-005
- AC-6 -> T-006
