# Sprint S0056 — Dev summary (US-0077)

- **Sprint**: S0056  
- **Story**: US-0077 — Documentation audience profiles and dual README strategy  
- **Governance**: DEC-0059; merge precedence DEC-0055  
- **Plan-verify**: PASS (`orchestrator_run_id=auto-20260327-02`)

## Delivered

1. **Scratchpad**: `DOC_AUDIENCE_PROFILE` and `DOC_DETAIL_LEVEL` on active + template baseline and `.cursor/scratchpad.local.example.md` (default `both` / `balanced`; empty keys resolve per DEC-0059 §6). Invalid enums → `DOC_PROFILE_INVALID`; merge failures surfaced as `DOC_PROFILE_MERGE_ERROR` in `scripts/validate_doc_profile.py`.
2. **Shared library**: `scripts/doc_profile_lib.py` — 9-cell key resolution, H2 literal mapping, budget counting (user H2s only for user/both; Contributing-only count for developer-only), split-layout DEV-forbidden-in-root check, template parity, non-destructive `ensure_doc_surfaces_merged`.
3. **Installer**: `installer.py` `_doc_profile_sync` after successful merged scratchpad validation — idempotent section append; invalid profile fails post-install.
4. **Surfaces**: Root `README.md` + `template/README.md` — normative `USER_*` H2s, `## Contributing` pointer; `docs/developer/README.md` + template mirror — `DEV_*` H2s; renamed legacy `## Workflow` → `## Commands and workflow`, `## Examples` (walkthrough) → `## Walkthrough examples` to avoid collision with DEV H2 literals.
5. **Validator**: `scripts/validate_doc_profile.py` — `--repo`, `--no-template-parity`, `--self-test`; optional-mode stderr hints only when `SPEC_PACK_MODE=1` / `USER_GUIDE_MODE=1` (non-blocking weak crosslink warnings).
6. **Manifest / clean**: `installer-owned-paths.manifest` (active + template) — `scripts/doc_profile_lib.py`, `scripts/validate_doc_profile.py`, `docs/developer` on clean list.
7. **Docs**: `docs/engineering/runbook.md` + template — operator section for doc profile; `.cursor/commands/execute.md` + template — step 21 validator gate.
8. **Tests**: `tests/doc_profile_fixtures_test.py` (Tier A anchors, Tier B resolver assertions, Tier C default merge, invalid profile negative, optional modes off); `tests/run-tests.ps1` / `run-tests.sh` §26j.

## Evidence

- `python scripts/validate_doc_profile.py --self-test` → OK  
- `python scripts/validate_doc_profile.py --repo .` → OK (template parity)  
- `python tests/doc_profile_fixtures_test.py` → OK  
- `python scripts/check-scratchpad-pair-parity.py --repo .` → OK  
- `python scripts/check-user-visible-metadata.py --repo .` → OK  
- Full `tests/run-tests.ps1`: **730 PASS / 2 FAIL** — failures are **pre-existing Homebrew stable formula vs `package.json` version** checks (not introduced by this sprint).

## QA (2026-03-27)

- **Verdict**: **PASS** — `sprints/S0056/qa-findings.md` (all AC-1..AC-10 **PASS**, no blockers).
- **Evidence**: `python scripts/validate_doc_profile.py --repo .`; `python tests/doc_profile_fixtures_test.py`; `python scripts/check-scratchpad-pair-parity.py --repo .`; `python scripts/check-user-visible-metadata.py --repo .` (all exit **0**).
- **Non-blocking**: full PS suite may still show **2 FAIL** on Homebrew vs npm version — baseline packaging drift, not US-0077.

## Verify-work (2026-03-28)

- **Verdict**: **PASS** — `sprints/S0056/uat.json` / `sprints/S0056/uat.md`: **UAT-001..UAT-010** ↔ **AC-1..AC-10**, all **PASS**; traceable to **`sprints/S0056/qa-findings.md`** and command evidence in **`uat.md`**.
- **Canonical backlog**: **`docs/product/backlog.md`** — **`US-0077`** **`DONE`** (per **US-0045** / verify-work closure).
- **Orchestrator**: `orchestrator_run_id=auto-20260327-02`; **`docs/engineering/state.md`** **Refresh-context checkpoint (2026-03-28)** — **`stop_reason=completed`**, **`next_scheduled_phase=none`**.

## Next

- **`/intake`** when new work is prioritized ( **`auto-20260327-02`** closed at **`/refresh-context`**; triad rollover **`state-pack-20260327-q.md`** recorded in **`docs/engineering/state.md`**).
