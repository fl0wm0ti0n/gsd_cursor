# Sprint S0075 Summary

## Metadata

- **sprint_id**: S0075
- **story_refs**: US-0089
- **orchestrator_run_id**: auto-20260418-01
- **planned_at**: 2026-04-18T12:45:00Z (sprint-plan, tech-lead)
- **plan_verified_at**: 2026-04-18T13:00:00Z (plan-verify, qa, PASS)
- **executed_at**: 2026-04-18T14:00:00Z (execute, dev)

## Status

- **execute_complete** — T-001..T-008 delivered; awaiting `/qa` (qa).
- Story **US-0089** remains **OPEN** per US-0045 (closure at `/verify-work`).

## Per-task delivery (T-001..T-008 <-> AC-1..AC-8)

| Task | AC | Status | Evidence |
|------|----|--------|----------|
| T-001 | AC-1 | done | Four locked key lines (`CAVEMAN_MODE=0`, `CAVEMAN_LEVEL=`, `CAVEMAN_COMPRESS_INPUT=0`, `CAVEMAN_FILE_SCOPE=`) + `## Caveman mode (US-0089)` comment block added to `.cursor/scratchpad.md` (baseline active; `template/.cursor/scratchpad.md` n/a per US-0073 / DEC-0055), `.cursor/scratchpad.local.example.md` (active), `template/.cursor/scratchpad.local.example.md` (template parity). Assertions: `test_caveman_default_off_scratchpad_keys_active`, `test_caveman_default_off_scratchpad_keys_example_parity`. |
| T-002 | AC-2 | done | Default-off invariant subtests items **6–8** of DEC-0072 §6 added to `tests/auto_command_contract_test.py`: `test_caveman_default_off_existing_contract_tokens_intact` (pre-US-0089 required tokens preserved in module), `test_caveman_default_off_non_suppressible_gate_vocab_preserved` (AUTO_QUIET gate vocabulary in reference doc), `test_caveman_default_off_no_vendor_install_leak` (no `npx skills add` in runbook or Caveman rule file active/template). |
| T-003 | AC-3 | done | New rule file `.cursor/rules/caveman.mdc` authored + byte-identical `template/.cursor/rules/caveman.mdc`, carrying (i) scratchpad gate contract, (ii) 9-zone literal-region invariant, (iii) AUTO_QUIET non-suppressible gate vocabulary, (iv) five canonical operator toggle phrases (`caveman on`, `caveman off`, `stop caveman`, `normal mode`, `caveman: lite|full|ultra`), (v) non-substitution paragraph, (vi) default-off invariant, (vii) DEC-0072 §8 non-goals. Assertion: `test_caveman_default_off_rule_file_present_active_template`. |
| T-004 | AC-4 | done | `### TOKEN_PROFILE × CAVEMAN_MODE non-substitution (US-0089 / DEC-0072 §1)` subsection inserted after the AUTO_QUIET subsection in `docs/engineering/auto-orchestration-reference.md` (active) + `template/docs/engineering/auto-orchestration-reference.md` (byte-identical). Assertion: `test_caveman_default_off_reference_non_substitution_paragraph`. |
| T-005 | AC-5 | done | `### Caveman mode (US-0089)` subsection appended to `docs/engineering/runbook.md` (active) + `template/docs/engineering/runbook.md`, carrying the non-substitution paragraph, scratchpad keys table, operator toggle phrase catalog, determinism semantics, and a pointer to the 9-zone literal-region invariant. Assertion: `test_caveman_default_off_runbook_operator_phrases`. |
| T-006 | AC-6 | done | Default-off invariant subtests items **1–5** of DEC-0072 §6 added to `tests/auto_command_contract_test.py`: `test_caveman_default_off_scratchpad_keys_active`, `test_caveman_default_off_scratchpad_keys_example_parity`, `test_caveman_default_off_rule_file_present_active_template`, `test_caveman_default_off_reference_non_substitution_paragraph`, `test_caveman_default_off_runbook_operator_phrases`. Combined with T-002 items 6–8, total of **8** Caveman default-off subtests matches DEC-0072 §6 cardinality. |
| T-007 | AC-7 | done | Assertion-only contract test `test_caveman_architecture_section_bottom_appended_and_linked` added: verifies `# US-0089:` heading present in `docs/engineering/architecture.md`, is bottom-appended (no later `# US-xxxx` / `## US-xxxx` heading follows it), and is linked from `docs/product/backlog.md` (US-0089 row) and `docs/engineering/decisions.md` (DEC-0072 entry). No canonical artifact rewrite performed (DEC-0072 §8). |
| T-008 | AC-8 | done | Template parity sweep test `test_caveman_template_parity_sweep` verifies active/template mirrors for the four US-0089-touched file pairs: `.cursor/scratchpad.local.example.md`, `.cursor/rules/caveman.mdc`, `docs/engineering/auto-orchestration-reference.md`, `docs/engineering/runbook.md`. Negative-parity test `test_caveman_skill_file_negative_parity` guards `.cursor/skills/its-magic/SKILL.md` against any `CAVEMAN_*` key, `US-0089` token, or operator phrase (DEC-0072 §8 non-goal). |

## Test evidence

- Targeted: `python -m pytest tests/auto_command_contract_test.py -k caveman --tb=short -q`
  - Result: **11 passed**, 19 deselected, **119 subtests passed**, 0 failed (all US-0089 subtests green).
- Full contract module: `python -m pytest tests/auto_command_contract_test.py --tb=no -q`
  - Result: **24 failed** (pre-existing; all US-0086/US-0087/US-0088 drift unrelated to US-0089 — verified via stash-baseline comparison), **27 passed** (+11 new Caveman passes vs. 16-pass baseline), 192 subtests passed. No new regressions introduced by US-0089.
- Full suite: `python -m pytest -q --tb=no`
  - Result: **24 failed** (pre-existing), **66 passed** (+11 vs. baseline 55), **4 skipped**, 192 subtests passed.
- Bug validator: `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` -> **`[BUG_VALIDATION_OK]`**.

### Pre-existing failures (NOT introduced by US-0089; confirmed via stash-baseline measurement)

- `test_slim_auto_retains_gate_markers` — missing US-0086/US-0087 remote/bug-target tokens in `.cursor/commands/auto.md` (pre-dates US-0089).
- `test_slim_auto_references_step5_and_continuation` — US-0088 Step 5 / continuation vocabulary missing from `.cursor/commands/auto.md`.
- `test_remote_automation_profile_keys_exist_in_scratchpads` — US-0086 remote keys missing from `template/.cursor/scratchpad.local.example.md`.
- `test_template_auto_literal_parity_active`, `test_template_scratchpad_baseline_literal_parity_active`, `test_template_scratchpad_example_literal_parity_active` — pre-existing active↔template drift in `.cursor/commands/auto.md` and scratchpad files (caveat: baseline scratchpad parity test also conflicts with US-0073 / DEC-0055 example-only install policy; out of scope).

None of these failures intersect with Caveman-mode tokens, scratchpad keys, rule file paths, runbook subsection, or reference doc non-substitution paragraph introduced by US-0089.

## Files written / modified

### Active

- `.cursor/scratchpad.md` (T-001)
- `.cursor/scratchpad.local.example.md` (T-001)
- `.cursor/rules/caveman.mdc` (T-003, **new**)
- `docs/engineering/auto-orchestration-reference.md` (T-004)
- `docs/engineering/runbook.md` (T-005)
- `tests/auto_command_contract_test.py` (T-002, T-006, T-007, T-008 — 11 new subtests total)

### Template parity

- `template/.cursor/scratchpad.local.example.md` (T-001)
- `template/.cursor/rules/caveman.mdc` (T-003, **new**)
- `template/docs/engineering/auto-orchestration-reference.md` (T-004)
- `template/docs/engineering/runbook.md` (T-005)

### Explicit non-touches (DEC-0072 §8 non-goals / negative parity)

- `.cursor/skills/its-magic/SKILL.md` — guarded by `test_caveman_skill_file_negative_parity`.
- `decisions/DEC-0072.md` — decision is owned by `/architecture`, not `/execute`.
- `docs/engineering/architecture.md` `# US-0089` — bottom-appended per `/architecture`; assertion-only verification by T-007.
- `docs/product/backlog.md` acceptance rows — unchanged (story OPEN; closure at `/verify-work` per US-0045).
- `.cursor/commands/auto.md` — not part of US-0089 scope (pre-existing US-0086/US-0087/US-0088 drift left untouched).

## Strict runtime proof (DEC-0038)

- `orchestrator_run_id=auto-20260418-01`
- `runtime_proof_id=rp-auto-20260418-01-execute-dev-20260418T140000Z-S0075-US0089`
- `phase_id=execute`
- `role=dev`
- `proof_issued_at=2026-04-18T14:00:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=8a9f9ecc8dce7e31806f5dad53d205e40d9e5e325ecd7ce74b0a64ec42262482`

Canonical payload (sorted-key JSON): `{"orchestrator_run_id":"auto-20260418-01","phase_id":"execute","proof_issued_at":"2026-04-18T14:00:00Z","proof_ttl_seconds":3600,"role":"dev","runtime_proof_id":"rp-auto-20260418-01-execute-dev-20260418T140000Z-S0075-US0089"}`.

## Isolation evidence (US-0048 / DEC-0029)

- `phase_id=execute`
- `role=dev`
- `fresh_context_marker=dev-US0089-execute-20260418T140000Z-S0075-fresh`
- `timestamp=2026-04-18T14:00:00Z`
- `evidence_ref=sprints/S0075/summary.md,handoffs/dev_to_qa.md,docs/engineering/state.md,handoffs/resume_brief.md,.cursor/scratchpad.md,.cursor/scratchpad.local.example.md,template/.cursor/scratchpad.local.example.md,.cursor/rules/caveman.mdc,template/.cursor/rules/caveman.mdc,docs/engineering/auto-orchestration-reference.md,template/docs/engineering/auto-orchestration-reference.md,docs/engineering/runbook.md,template/docs/engineering/runbook.md,tests/auto_command_contract_test.py`

## Next

- `/qa` (fresh qa subagent) for S0075 / US-0089. See `handoffs/dev_to_qa.md`.

## QA-loop cycle 2 remediation (2026-04-18)

- **Cycle**: `qa_loop_cycle=2` of `qa_loop_max=5`.
- **Trigger**: Prior `/qa` (`runtime_proof_id=rp-auto-20260418-01-qa-qa-20260418T150000Z-S0075-US0089`, `proof_hash=3bef1259f94c6c5d79cf30a45efbbd28765da263a6ef6ef4918010992fc809ca`, 2026-04-18T15:00:00Z) FAIL with single blocking finding: `tests/run-tests.ps1` rule-count assertion stale (`"5 rules exist"` / `-eq 5`). DEC-0072 §7 row 3 legitimately raised the count to 6.
- **Surgical fix**: bumped the rule-count assertion in both POSIX-parity check-in runners.
  - `tests/run-tests.ps1` line 77: `Assert-True "5 rules exist" ((Count-Files (Join-Path $tpl ".cursor\rules") "*.mdc") -eq 5)` -> `Assert-True "6 rules exist" ((Count-Files (Join-Path $tpl ".cursor\rules") "*.mdc") -eq 6)`.
  - `tests/run-tests.sh` line 87: `assert_true "5 rules exist" "[ $rule_count -eq 5 ]"` -> `assert_true "6 rules exist" "[ $rule_count -eq 6 ]"`.
- **Template parity (US-0017)**: no `template/tests/run-tests.*` mirror exists (test runners are active-only, consistent with row 7 of DEC-0072 §7); no template edit needed.
- **Verified rule-file count**: `.cursor/rules/` contains exactly **6** `.mdc` files (`caveman.mdc`, `coding-standards.mdc`, `core.mdc`, `escalation.mdc`, `handoffs.mdc`, `quality.mdc`). `template/.cursor/rules/` mirrors the same 6 files. Count matches assertion bump.
- **Test evidence (post-fix)**:
  - `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` -> `tests/report.md` `Timestamp=2026-04-18T12:32:24Z`, **Pass=783 / Fail=11** (was Pass=782 / Fail=12 pre-fix; +1 pass / -1 fail; rule-count line now `[PASS] 6 rules exist`). The 11 remaining failures are pre-existing US-0086 / US-0087 / US-0088 drift (observational, disjoint from US-0089 surface), matching QA's stated post-fix expectation.
  - `python -m pytest tests/auto_command_contract_test.py -q -k caveman` -> exit 0, **11 passed / 19 deselected / 119 subtests / 0 failed**. All 11 caveman subtests still green.
  - `python -m pytest tests/auto_command_contract_test.py -q` -> exit 1, **27 passed / 24 failed / 192 subtests** (pre-existing 24-failure baseline preserved -- no new regression introduced).
  - `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` -> `[BUG_VALIDATION_OK]` (exit 0).
- **Files touched (cycle 2)**: `tests/run-tests.ps1`, `tests/run-tests.sh`, `sprints/S0075/summary.md`, `handoffs/dev_to_qa.md`, `handoffs/resume_brief.md`, `docs/engineering/state.md`.
- **Tasks**: T-001..T-008 remain `done`. The remediation is a follow-on assertion patch outside the AC-1..AC-8 surface (test-harness artifact, not a sprint task body); per existing sprint convention no new T-row is added -- the change is recorded here in summary.md.
- **Story status**: `US-0089` remains **OPEN** per US-0045 (closure at `/verify-work`).
- **Strict runtime proof (cycle 2, DEC-0038)**:
  - `orchestrator_run_id=auto-20260418-01`
  - `runtime_proof_id=rp-auto-20260418-01-execute-dev-20260418T160000Z-S0075-US0089-loop2`
  - `phase_id=execute`, `role=dev`
  - `proof_issued_at=2026-04-18T16:00:00Z`, `proof_ttl_seconds=3600`
  - `proof_hash=c43fc4471e31d838f492fcd4054fedd80d11300588290f51801189cb0654e937`
  - Canonical payload: `{"orchestrator_run_id":"auto-20260418-01","phase_id":"execute","proof_issued_at":"2026-04-18T16:00:00Z","proof_ttl_seconds":3600,"role":"dev","runtime_proof_id":"rp-auto-20260418-01-execute-dev-20260418T160000Z-S0075-US0089-loop2"}`.
- **Isolation evidence (cycle 2, US-0048 / DEC-0029)**: `phase_id=execute`, `role=dev`, `fresh_context_marker=dev-US0089-execute-20260418T160000Z-S0075-loop2-fresh`, `timestamp=2026-04-18T16:00:00Z`, `evidence_ref=tests/run-tests.ps1,tests/run-tests.sh,sprints/S0075/summary.md,handoffs/dev_to_qa.md,handoffs/resume_brief.md,docs/engineering/state.md,tests/report.md`.
- **Next**: `/qa` (fresh qa subagent) for S0075 / US-0089 -- QA-loop cycle 2 re-verification.

## Refresh-context checkpoint (2026-04-18) -- segment close for US-0089 / S0075

- **Curator `/refresh-context`** executed in fresh curator context (`orchestrator_run_id=auto-20260418-01`, `timestamp=2026-04-18T20:00:00Z`, `fresh_context_marker=curator-S0075-US0089-refresh-context-20260418T200000Z-fresh`).
- **Verdict**: **PASS** -- US-0089 segment closed; context pack reconciled.
- **Final status**: **`US-0089`** = **DONE** (`docs/product/backlog.md`); AC-1..AC-8 `[x]`; acceptance portfolio row checked in **`docs/product/acceptance.md`**; sprint **`S0075`** = **released** (`handoffs/release_queue.md`, `2026-04-18T19:00:00Z`); release notes **`handoffs/releases/S0075-release-notes.md`**; release findings **`sprints/S0075/release-findings.md`** (verdict PASS).
- **Upstream release proof consumed (DEC-0038)**: `runtime_proof_id=rp-auto-20260418-01-release-release-20260418T190000Z-S0075-US0089`; `proof_hash=2f7351477332235595f379aae04d3830a0efc33f9a9cef887822999bcc9839b3`; `proof_issued_at=2026-04-18T19:00:00Z`; `proof_ttl_seconds=3600`.
- **Refresh-context strict runtime proof (DEC-0038)**: `runtime_proof_id=rp-auto-20260418-01-refresh-context-curator-20260418T200000Z-S0075-US0089`; `proof_hash=f91b4f46aa8f50981971495d7fbfd7728a2729bb5c3e488757216a4b11a4a6b8`; `proof_issued_at=2026-04-18T20:00:00Z`; `proof_ttl_seconds=3600`; canonical payload `{"orchestrator_run_id":"auto-20260418-01","phase_id":"refresh-context","proof_issued_at":"2026-04-18T20:00:00Z","proof_ttl_seconds":3600,"role":"curator","runtime_proof_id":"rp-auto-20260418-01-refresh-context-curator-20260418T200000Z-S0075-US0089"}`.
- **Artifacts touched**: **`docs/engineering/state.md`** (refresh-context checkpoint appended; two triad rollovers performed per DEC-0054 -> `docs/engineering/state-archive/state-pack-20260418-c.md` + `docs/engineering/state-archive/state-pack-20260418-d.md`), **`docs/engineering/decisions.md`** (`## Current context pack` anchor refreshed to US-0089 / S0075 / DEC-0072; DEC-0072 retained in index + full records), **`docs/engineering/research.md`** (**R-0073** delivery-closure note appended; marked delivered for US-0089 surface; remains shared anchor for US-0090 extension), **`sprints/S0075/summary.md`** (this section), **`handoffs/resume_brief.md`** (new top pointer; prior post-`/release` pointer superseded).
- **Backlog drain**: `backlog_drain_stories_remaining_budget` decremented **6 -> 5**; next candidate OPEN story **`US-0090`** (input-side Caveman compression; depends on US-0089 -> now unblocked).
- **Consistency checks**: `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` -> `[BUG_VALIDATION_OK]`; `handoffs/release_queue.md` `S0075` row `status=released`; no OPEN story blocked by US-0089 anymore.
- **Stop metadata**: `stop_reason=completed`; `stop_phase=refresh-context`; `backlog_drain_segment_complete=1`.
- **Phase boundary**: `phase_boundary=refresh-context`; `next_scheduled_phase=discovery` (US-0090; US-0090 intake coverage bundled in `handoffs/intake_evidence/US-0089-intake-20260414.json` `plan_area_coverage`).
- **Next command**: `/discovery` (fresh **po** context) for **US-0090**, or `/auto start-from=discovery`. Decision-gate posture: **none expected**.
