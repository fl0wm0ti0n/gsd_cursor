# Sprint S0056 Tasks

- Story: `US-0077`
- Sprint: `S0056`
- Governance: **`DEC-0059`** (documentation profiles + dual README shard); merge precedence **`DEC-0055`**; related **`US-0030`** (parity), **`US-0031`** / **`US-0032`** (optional modes), **`US-0071`** (metadata guard)

| Task | Status | Description | AC |
|---|---|---|---|
| T-001 | done | Add **`DOC_AUDIENCE_PROFILE`** and **`DOC_DETAIL_LEVEL`** to **materialized baseline**, **`.cursor/scratchpad.local.example.md`**, and **`template/`** mirrors with documented defaults; parse merged scratchpad; **fail closed** on invalid enums (**`DOC_PROFILE_INVALID`**) and merge failures (**`DOC_PROFILE_MERGE_ERROR`**) per **`DEC-0059`** §§1,6 | AC-1 |
| T-002 | done | Wire profile resolution into **documentation generation/update** entrypoints (installer post-install, CLI, or documented generator hooks) so repeated runs with the same merged inputs yield **deterministic, idempotent** doc mutations (**AC-2**) | AC-2 |
| T-003 | done | Implement **content mapping** to architecture **semantic keys → H2 literals**: populate **`USER_*`** sections in root **`README.md`** and **`DEV_*`** sections in **`docs/developer/README.md`** per resolved cell; enforce plain-language user channel vs developer workflow/guardrails tone (**AC-3**) | AC-3 |
| T-004 | done | Implement **dual README strategy** per **`DEC-0059`** §3: split files, pointer rules for developer-only audience, forbid inlined **`DEV_*`** bodies in root when shard required; explicit **ownership** matrix in docs — **no** contradictory guidance across surfaces (**AC-4**) | AC-4 |
| T-005 | done | Ensure validators and generators **respect `SPEC_PACK_MODE` / `USER_GUIDE_MODE`**: **no** required artifacts or blocking checks when **0**; **profile-aware** depth/cross-links only when **1** (**AC-5**) | AC-5 |
| T-006 | done | Implement **`scripts/validate_doc_profile.py`**: merged scratchpad via **`installer.py`** merge ( **`DEC-0058`** pattern); completeness (**`DOC_SECTION_MISSING:<key>`**), **H2 budgets** (**`DOC_SECTION_BUDGET_EXCEEDED`**), **active/template** path parity (**`DOC_TEMPLATE_PARITY_FAIL`**) | AC-6 |
| T-007 | done | Update **`docs/engineering/runbook.md`**, **README** pointers, **`template/`** mirrors, and **`docs/engineering/context/installer-owned-paths.manifest`** for **`docs/developer/README.md`** + profile operator guidance (**AC-7**) | AC-7 |
| T-008 | done | Add **Tier A/B/C** regression fixtures and **`tests/run-tests.ps1`** / **`.sh`** invocations proving **9-cell** matrix + **non-destructive** doc update behavior (**AC-8**) | AC-8 |
| T-009 | done | Run **US-0071** hygiene on **new/changed** validator stdout, tooling strings, and scanned markdown bodies; extend allowlists only if justified (**AC-9**) | AC-9 |
| T-010 | done | **AC-10 closure**: ensure **operator-facing docs**, sprint surfaces, and **`docs/engineering/decisions.md`** index cite **`DEC-0059`** + **`# US-0077`** migration defaults (explicit keys vs transition **`both`×`balanced`**) | AC-10 |

## Deterministic AC-to-task mapping

- AC-1 → T-001
- AC-2 → T-002
- AC-3 → T-003
- AC-4 → T-004
- AC-5 → T-005
- AC-6 → T-006
- AC-7 → T-007
- AC-8 → T-008
- AC-9 → T-009
- AC-10 → T-010
