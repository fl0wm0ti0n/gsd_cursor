# Release findings — Sprint S0075 (US-0089)

- **Verdict**: **PASS**
- **Orchestrator run**: **`auto-20260418-01`**
- **Sprint**: **`S0075`**
- **Story**: **`US-0089`** (Cursor Caveman mode)
- **Release date**: `2026-04-18T19:00:00Z`
- **Release agent**: `release`

## Gate audit (US-0039)

| gate | verdict | reason_code | remediation | evidence_refs |
|------|---------|-------------|-------------|---------------|
| check-in_test | pass | - | 11 pre-existing failures confirmed disjoint from US-0089 surface per QA cycle 2; recommend separate triage bug/story. | `sprints/S0075/qa-findings.md` (cycle 2; `tests/run-tests.ps1` Pass=783 / Fail=11); `handoffs/qa_to_release.md` |
| qa | pass | - | None. | `sprints/S0075/qa-findings.md` (cycle 2 PASS) |
| uat | pass | - | None. | `sprints/S0075/uat.json`, `sprints/S0075/uat.md` (8/8 PASS, AC-1..AC-8) |
| isolation | pass | - | None. | `docs/engineering/state.md` (10 distinct `fresh_context_marker` across discovery -> verify-work) |
| strict_proof | pass | - | None. | `docs/engineering/state.md` (10 distinct `runtime_proof_id` per DEC-0038 canonical tuple) |
| scratchpad_pair | pass | - | Observational sanction per DEC-0072 §7 row 1 (pre-existing active/template drift in `.cursor/scratchpad.md` and `.cursor/scratchpad.local.example.md`; US-0089 additions byte-parity clean). | `sprints/S0075/qa-findings.md` (scratchpad_pair snapshot) |
| metadata_guard | pass | - | None. | `sprints/S0075/qa-findings.md` (metadata guard snapshot) |
| bug_validate | pass | - | None. | `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` -> `[BUG_VALIDATION_OK]` |
| finalization | pass | - | None. | `handoffs/releases/S0075-release-notes.md`, `handoffs/release_queue.md`, `handoffs/release_notes.md`, `docs/product/backlog.md`, `docs/product/acceptance.md`, `docs/engineering/status-normalization-report.md`, `docs/engineering/state.md`, `handoffs/resume_brief.md` |

## Delivered acceptance (AC-1..AC-8 per DEC-0072)

- **AC-1**: Four scratchpad keys (`CAVEMAN_MODE=0`, `CAVEMAN_LEVEL=`, `CAVEMAN_COMPRESS_INPUT=0`, `CAVEMAN_FILE_SCOPE=`) + `## Caveman mode (US-0089)` comment block present in `.cursor/scratchpad.md` baseline and `.cursor/scratchpad.local.example.md` active/template pair. Default-off invariant holds.
- **AC-2**: Default-off invariant subtests items 6-8 of DEC-0072 §6 in `tests/auto_command_contract_test.py` (existing contract tokens intact; non-suppressible gate vocabulary preserved; no vendor install leak).
- **AC-3**: New `.cursor/rules/caveman.mdc` + byte-identical `template/.cursor/rules/caveman.mdc` carrying scratchpad gate contract, 9-zone literal-region invariant, AUTO_QUIET non-suppressible gate vocabulary, five canonical operator toggle phrases (`caveman on`, `caveman off`, `stop caveman`, `normal mode`, `caveman: lite|full|ultra`), non-substitution paragraph, default-off invariant, DEC-0072 §8 non-goals.
- **AC-4**: `### TOKEN_PROFILE x CAVEMAN_MODE non-substitution (US-0089 / DEC-0072 §1)` subsection inserted after AUTO_QUIET in `docs/engineering/auto-orchestration-reference.md` (active + `template/`, byte-identical).
- **AC-5**: `### Caveman mode (US-0089)` subsection appended to `docs/engineering/runbook.md` (active + `template/`) carrying non-substitution paragraph, scratchpad key table, operator toggle phrase catalog, determinism semantics, 9-zone literal-region pointer.
- **AC-6**: Default-off invariant subtests items 1-5 of DEC-0072 §6 in `tests/auto_command_contract_test.py`. Combined with AC-2/T-002 items 6-8: 8 total Caveman default-off subtests (matches DEC-0072 §6 cardinality).
- **AC-7**: Assertion-only test `test_caveman_architecture_section_bottom_appended_and_linked` verifies `# US-0089` heading bottom-appended in `docs/engineering/architecture.md`, linked from `docs/product/backlog.md` (US-0089 row) and `docs/engineering/decisions.md` (DEC-0072 entry). No canonical artifact rewrite (DEC-0072 §8).
- **AC-8**: Template parity sweep test `test_caveman_template_parity_sweep` across the four touched active/template pairs + negative-parity test `test_caveman_skill_file_negative_parity` guards `.cursor/skills/its-magic/SKILL.md` against `CAVEMAN_*` keys, `US-0089` tokens, or operator phrases.

## Test evidence summary

- Targeted `python -m pytest tests/auto_command_contract_test.py -k caveman --tb=short -q` -> **11 passed**, 19 deselected, 119 subtests passed, 0 failed (cycle 2 remediation).
- Full `tests/auto_command_contract_test.py` module: **27 passed / 24 failed** (net +11 passes / 0 new failures vs. pre-US-0089 baseline 16 passed / 24 failed).
- Full `python -m pytest -q --tb=no`: **66 passed / 24 failed / 4 skipped**, 192 subtests passed.
- Canonical `tests/run-tests.ps1` check-in suite: **Pass=783 / Fail=11** — all 11 failures pre-existing (US-0086 / US-0087 / US-0088 drift + Homebrew test env) and confirmed disjoint from US-0089 surface per `sprints/S0075/qa-findings.md` cycle 2.
- `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` -> **`[BUG_VALIDATION_OK]`**.

## Known post-release observations

- 11 pre-existing failures remain in `tests/run-tests.ps1` / 24 in full pytest (disjoint from US-0089). Recommended for separate triage as follow-on BUG or small story — scoped to `.cursor/commands/auto.md` slim-auto drift, remote automation profile key presence in scratchpads, active/template auto literal parity, and scratchpad active/template literal parity.
- DEC-0072 §7 row 1 scratchpad active/template drift is explicitly sanctioned as observational; it is not a US-0089 blocker.

## Sync (US-0038 / DEC-0018)

- **SYNC_POLICY_MODE**: `by_phase` (evaluation triggered at release boundary).
- **ALLOW_AUTO_PUSH**: `1`
- **AUTO_PUSH_BRANCH_ALLOWLIST**: `main`
- **current_branch**: `main` (`git rev-parse --abbrev-ref HEAD`).
- **TEST_COMMAND**: `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` (defined in `docs/engineering/runbook.md`).
- **push_decision**: `blocked`
- **reason_code**: `TEST_FAILED` -- canonical `tests/run-tests.ps1` returns non-zero (11 pre-existing failures). Per DEC-0018 the sync-push gate requires a fully-green test command even when release-gate classification tolerates pre-existing disjoint failures. No push performed.
- **evidence_refs**: `sprints/S0075/qa-findings.md` (cycle 2 test snapshot), `docs/engineering/runbook.md` (`TEST_COMMAND` binding), `docs/engineering/decisions.md` (DEC-0018).

## Publish status

- **RELEASE_PUBLISH_MODE**: `confirm`
- **publish_snapshot**: `skipped_pending_operator_confirm`
- No publish scripts executed. Publish remains gated by explicit operator confirmation.
- Deploy commands are explicit in `docs/engineering/runbook.md` (`DEPLOY_STAGING_COMMAND`, `DEPLOY_PROD_COMMAND`) and remain concrete `echo` placeholders pending real targets for this framework/toolkit repository.

## Strict runtime proof (US-0056 / DEC-0038)

- **orchestrator_run_id**: `auto-20260418-01`
- **runtime_proof_id**: `rp-auto-20260418-01-release-release-20260418T190000Z-S0075-US0089`
- **phase_id**: `release`
- **role**: `release`
- **proof_issued_at**: `2026-04-18T19:00:00Z`
- **proof_ttl_seconds**: `3600`
- **proof_hash**: `2f7351477332235595f379aae04d3830a0efc33f9a9cef887822999bcc9839b3`
- **canonical_payload**: `{"orchestrator_run_id":"auto-20260418-01","phase_id":"release","proof_issued_at":"2026-04-18T19:00:00Z","proof_ttl_seconds":3600,"role":"release","runtime_proof_id":"rp-auto-20260418-01-release-release-20260418T190000Z-S0075-US0089"}`

## Status transitions applied

- `docs/product/backlog.md` `## US-0089`: `Status: OPEN` -> `Status: DONE` (US-0045); AC-1..AC-8 checkboxes flipped to `[x]`; appended `release_notes` block.
- `docs/product/acceptance.md`: US-0089 portfolio row flipped unchecked -> checked.
- `handoffs/release_queue.md` row S0075: `planned` -> `released` (2026-04-18).
- `docs/engineering/status-normalization-report.md`: delta row appended for US-0089 -> DONE.
- `handoffs/release_notes.md`: aggregate pointer updated to S0075 / US-0089.
- `handoffs/resume_brief.md`: post-`/release` pointer prepended; prior entry marked superseded.
- `docs/engineering/state.md`: Release checkpoint appended with isolation + strict-proof tuples.

## Next

- **`/refresh-context`** (fresh **curator** context) for US-0089 / S0075 segment close.
