# QA findings — S0056 / US-0077

- **Sprint**: S0056
- **Story**: US-0077 (documentation audience profiles + dual README strategy)
- **Governance**: DEC-0059 (DEC-0055 merge; US-0030 parity; US-0031/US-0032 optional modes; US-0071 hygiene)
- **Verdict**: **PASS** (no blocking defects for US-0077 scope)
- **Reviewed**: 2026-03-27 (QA subagent, `orchestrator_run_id=auto-20260327-02`)

## Evidence (commands)

| Check | Command | Result |
|--------|---------|--------|
| Doc profile validator (active + template parity) | `python scripts/validate_doc_profile.py --repo .` | Exit **0** — `[DOC_PROFILE_VALIDATE_OK]` |
| Tiered fixtures (AC-8) | `python tests/doc_profile_fixtures_test.py` | Exit **0** — `[DOC_PROFILE_FIXTURES_OK]` |
| Scratchpad pair parity | `python scripts/check-scratchpad-pair-parity.py --repo .` | Exit **0** — `[SCRATCHPAD_PAIR_OK]` |
| US-0071 metadata guard | `python scripts/check-user-visible-metadata.py --repo .` | Exit **0** |
| Validator self-test | `python scripts/validate_doc_profile.py --self-test` | Exit **0** — `[DOC_PROFILE_SELF_TEST_OK]` |

**Handoff**: `handoffs/dev_to_qa.md` (scope + artifact list).

## Acceptance criteria

| AC | Verdict | Notes |
|----|---------|--------|
| AC-1 | **PASS** | `DOC_AUDIENCE_PROFILE` / `DOC_DETAIL_LEVEL` on active + template baseline and `.cursor/scratchpad.local.example.md`; invalid profile → `[DOC_PROFILE_INVALID]` with remediation (fixture + `scripts/doc_profile_lib.py`); merge errors → `DOC_PROFILE_MERGE_ERROR` path per DEC-0059. |
| AC-2 | **PASS** | `scripts/doc_profile_lib.py` `ensure_doc_surfaces_merged` + installer `installer.py` `_doc_profile_sync` — idempotent merged-scratchpad-driven doc surface updates; same inputs → deterministic validation outcome. |
| AC-3 | **PASS** | Root `README.md` + `docs/developer/README.md` (and template mirrors) follow USER_* vs DEV_* split per architecture `# US-0077`; user channel plain-language H2s vs developer guardrails. |
| AC-4 | **PASS** | Dual-file split (root README + `docs/developer/README.md`); ownership table in `decisions/DEC-0059.md` + architecture; Contributing pointer pattern; no contradictory body rules observed in validator scope. |
| AC-5 | **PASS** | Validator optional-mode behavior: `SPEC_PACK_MODE` / `USER_GUIDE_MODE` off — fixtures in `tests/doc_profile_fixtures_test.py` confirm no requirement for spec-pack/user-guide files; stderr hints only when modes on (per dev summary). |
| AC-6 | **PASS** | `scripts/validate_doc_profile.py` enforces required sections, budgets, template parity; reason codes `DOC_SECTION_MISSING:<key>`, `DOC_SECTION_BUDGET_EXCEEDED`, `DOC_TEMPLATE_PARITY_FAIL` per DEC-0059 / architecture. |
| AC-7 | **PASS** | `docs/engineering/runbook.md` **Documentation profile validation (US-0077 / DEC-0059)**; `.cursor/commands/execute.md` step **21**; `template/` mirrors; manifest lists doc profile scripts + `docs/developer`. |
| AC-8 | **PASS** | Tiered coverage in `tests/doc_profile_fixtures_test.py` (invalid profile, user×concise, developer×balanced, both×technical-deep, default merge, optional modes off); `tests/run-tests.ps1` / `run-tests.sh` §26j wiring asserts. |
| AC-9 | **PASS** | `check-user-visible-metadata.py` exit **0** on repo; installer docstring hygiene per handoff (no new forbidden planning tokens in scanned operator paths). |
| AC-10 | **PASS** | **`decisions/DEC-0059.md`** (Accepted) + `docs/engineering/architecture.md` `# US-0077` — semantics, artifact boundaries, migration defaults §6. |

## Non-blocking observations

- **Full `tests/run-tests.ps1`**: dev handoff notes **730 PASS / 2 FAIL** on **Homebrew stable formula vs npm `package.json` version** — same class as historical baseline drift (**US-0016** / **US-0074** narrative); **out of scope** for US-0077 gate. Tiered doc-profile checks and §26j are the authoritative US-0077 regression surface for this QA cycle.
- Triad/state hot-surface enforcement not re-run in this QA subagent turn; prior **`/plan-verify`** / execute checkpoints recorded **`enforce-triad-hot-surface.py --check` PASS** where applicable in `docs/engineering/state.md`.

## Sprint task alignment

- **`sprints/S0056/tasks.md`**: T-001..T-010 marked **done** — consistent with AC-1..AC-10 coverage above.
