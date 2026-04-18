# QA Findings -- S0075 / US-0089

## Status

- **verdict**: **FAIL** (blocking).
- **phase**: `/qa` -- fresh **qa** subagent, `orchestrator_run_id=auto-20260418-01`, timestamp `2026-04-18T15:00:00Z`.
- **sprint**: **S0075**; **story**: **US-0089** (remains **OPEN** per **US-0045**).
- **decision-gate posture**: blocking -- return to `/execute` (dev) to remediate one new harness-count assertion introduced by the US-0089 rule-file addition. Pre-existing drift items listed as observational only.
- **handoff**: `handoffs/qa_to_dev.md` (this cycle).

## Verdict rationale (compact)

`/execute` delivered all **T-001..T-008** against **AC-1..AC-8** with **DEC-0072** byte-locked strings preserved and all 11 targeted Caveman pytest subtests green. However, the canonical check-in harness `tests/run-tests.ps1` asserts a fixed rule count (`5 rules exist`) and US-0089 legitimately introduced a sixth rule (`.cursor/rules/caveman.mdc` + `template/` mirror per **DEC-0072 section 7 row 3** / **AC-3**). The assertion was not updated as part of the sprint scope (T-001..T-008 did not enumerate a run-tests.ps1 rule-count bump), so the harness flips from PASS to FAIL on the legitimate additive deliverable. This is strictly a **NEW failure introduced by US-0089** under the task's decision-gate policy and requires remediation before `/verify-work`.

All other `run-tests.ps1` failures (11 of 12) are pre-existing drift carried over from US-0087 / US-0088 (and earlier); they are disjoint from the US-0089 surface and are **observational**, not blocking for US-0089 specifically (separate triage recommended).

## Test evidence (this QA cycle)

### 1. Canonical check-in suite -- `tests/run-tests.ps1`

- Command: `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"`
- Report: `tests/report.md` (`Timestamp=2026-04-18T12:09:41Z`)
- Results: **Pass=782**, **Fail=12**
- Baseline (US-0086 QA, `2026-04-13T21:22:07Z`): **Pass=788**, **Fail=6**
- Delta vs baseline: **-6 pass, +6 fail**.

Classification of the 12 failures:

| # | Test | New vs baseline | US-0089 surface? | Classification |
|---|------|-----------------|------------------|----------------|
| 1 | `5 rules exist` | **NEW** | **YES** -- count asserts `-eq 5`, US-0089 adds `caveman.mdc` bringing `.cursor/rules` + `template/.cursor/rules` to 6 | **BLOCKING** |
| 2 | `Homebrew stable formula URL uses npm version tag` | new (since US-0086) | no | pre-existing drift (release formula) |
| 3 | `Homebrew stable formula version matches npm version` | new (since US-0086) | no | pre-existing drift (release formula) |
| 4 | `Installer runbook TEST_COMMAND present for detectable stack` | pre-existing | no | installer stack-detection drift |
| 5 | `CLI missing install runbook TEST_COMMAND present` | pre-existing | no | installer stack-detection drift |
| 6 | `auto precedence includes argument > resume > state (active)` | new (since US-0086) | no | US-0087 / US-0088 `auto.md` drift |
| 7 | `auto includes strict-proof boundary step 11b (template)` | pre-existing | no | strict-proof step-label drift |
| 8 | `triad check passes on repo` | pre-existing | no | triad hot-surface oversize drift |
| 9 | `triad check idempotent rerun passes` | pre-existing | no | triad hot-surface oversize drift |
| 10 | `scratchpad pair parity check passes on repo` | new (since US-0086) | mixed | predominantly US-0087 / US-0088 `active_pair` drift; additive US-0089 `template_pair` (`CAVEMAN_*` keys in `template/.cursor/scratchpad.local.example.md` not mirrored in `template/.cursor/scratchpad.md`) **architecturally sanctioned** per **DEC-0072 section 7 row 1** / **DEC-0055** (example-only install) |
| 11 | `token-cost active/template parity passes` | new (since US-0086) | no | US-0087 / US-0088 `.cursor/commands/auto.md` drift |
| 12 | `slim auto command contract markers pass` | new (since US-0086) | no | US-0087 / US-0088 `.cursor/commands/auto.md` drift |

Blocking count: **1** (item #1). Observational / pre-existing: **11**.

### 2. Targeted US-0089 subtests -- pytest `-k caveman`

- Command: `python -m pytest tests/auto_command_contract_test.py -q -k caveman --tb=short`
- Result: **11 passed**, **19 deselected**, **119 subtests passed**, **0 failed**, **0 skipped**. Exit 0.
- Subtests green (exhaustive):
  1. `test_caveman_default_off_scratchpad_keys_active`
  2. `test_caveman_default_off_scratchpad_keys_example_parity`
  3. `test_caveman_default_off_rule_file_present_active_template`
  4. `test_caveman_default_off_reference_non_substitution_paragraph`
  5. `test_caveman_default_off_runbook_operator_phrases`
  6. `test_caveman_default_off_existing_contract_tokens_intact`
  7. `test_caveman_default_off_non_suppressible_gate_vocab_preserved`
  8. `test_caveman_default_off_no_vendor_install_leak`
  9. `test_caveman_architecture_section_bottom_appended_and_linked`
  10. `test_caveman_template_parity_sweep`
  11. `test_caveman_skill_file_negative_parity`

### 3. Full contract module -- pytest `tests/auto_command_contract_test.py`

- Command: `python -m pytest tests/auto_command_contract_test.py -q --tb=no`
- Result: **27 passed**, **24 failed**, **192 subtests passed**. Exit 1.
- Failing tests (all pre-existing, disjoint from US-0089 surface per dev stash-baseline measurement):
  - `test_slim_auto_retains_gate_markers` (US-0086 / US-0087 token drift)
  - `test_slim_auto_references_step5_and_continuation` (US-0088 Step 5 / continuation vocabulary missing from `.cursor/commands/auto.md`)
  - `test_remote_automation_profile_keys_exist_in_scratchpads` (US-0086 remote keys missing from `template/.cursor/scratchpad.local.example.md`)
  - `test_template_auto_literal_parity_active`
  - `test_template_scratchpad_baseline_literal_parity_active`
  - `test_template_scratchpad_example_literal_parity_active`
- Dev-reported stash baseline (independently reproducible): removing US-0089 changes yields **16 passed / 24 failed**; adding US-0089 yields **27 passed / 24 failed**. Net change from US-0089: **+11 passes, 0 new failures** inside this module.

### 4. Full repository pytest suite

- Command: `python -m pytest -q --tb=no`
- Result: **66 passed**, **24 failed**, **4 skipped**, **192 subtests passed**. Exit 1.
- Same 24 pre-existing failures as section 3. Skips: 4 (pre-existing).

### 5. Remote config summary regression -- pytest

- Command: `python -m pytest tests/remote_config_summary_test.py -q`
- Result: **4 passed**, 0 failed. Exit 0.

### 6. Bug issue validator

- Command: `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance`
- Output: `[BUG_VALIDATION_OK]`. Exit 0.

### 7. User-visible metadata guard (US-0071 / DEC-0053)

- Command: `python scripts/check-user-visible-metadata.py`
- Result: empty stdout, exit 0 -> **PASS** (no `USER_VISIBLE_INTERNAL_METADATA_DETECTED`).

### 8. Scratchpad pair parity -- `python scripts/check-scratchpad-pair-parity.py`

- Exit 1 -- `SCRATCHPAD_PAIR_ERROR` (multi-cause):
  - `active_pair`: keys only_in_baseline `['AUTO_BUG_MAX_ITEMS', 'AUTO_BUG_ON_BLOCK', 'AUTO_BUG_QUEUE', 'AUTO_BUG_TARGET', 'AUTO_QUIET', 'AUTO_REMOTE_AUTOMATION_PROFILE', 'AUTO_REMOTE_ENVIRONMENT_LABEL']` -- pre-existing US-0087 / US-0088 / US-0086 drift (`.cursor/scratchpad.md` vs `.cursor/scratchpad.local.example.md`); not US-0089.
  - `template_pair`: keys only_in_example `['CAVEMAN_COMPRESS_INPUT', 'CAVEMAN_FILE_SCOPE', 'CAVEMAN_LEVEL', 'CAVEMAN_MODE']` -- additive under **DEC-0072 section 7 row 1** / **DEC-0055** (example-only install; baseline scratchpad `n/a`). Architecturally sanctioned by the story decision; script lacks the carveout.
- Result: **`[SCRATCHPAD_PAIR_ERROR]`** -- observational-only for US-0089 scope (the new drift component is explicitly sanctioned; the pre-existing drift is out of story scope). Classification for this sprint: **not blocking US-0089**. Separate triage needed for the overall script state (recommend a dedicated bug issue or an explicit whitelist update that encodes DEC-0055).

## Per-AC verification table (AC-1..AC-8 vs DEC-0072)

| AC | Verdict | Evidence |
|----|---------|----------|
| AC-1 | **PASS** | Four locked key lines (`CAVEMAN_MODE=0`, `CAVEMAN_LEVEL=`, `CAVEMAN_COMPRESS_INPUT=0`, `CAVEMAN_FILE_SCOPE=`) + `## Caveman mode (US-0089)` comment block present in `.cursor/scratchpad.md` (L246-L249, L234), `.cursor/scratchpad.local.example.md` (L221-L224, L209), and `template/.cursor/scratchpad.local.example.md` (L240-L243, L228). Subtests `test_caveman_default_off_scratchpad_keys_active` + `test_caveman_default_off_scratchpad_keys_example_parity` PASS. |
| AC-2 | **PASS** | DEC-0072 section 6 items 6-8 subtests PASS (`test_caveman_default_off_existing_contract_tokens_intact`, `test_caveman_default_off_non_suppressible_gate_vocab_preserved`, `test_caveman_default_off_no_vendor_install_leak`). Byte-for-byte default-off invariant held in `required` token list, `AUTO_QUIET` non-suppressible gate vocabulary, and vendor-install-leak guard (no `npx skills add` token in `.cursor/rules/caveman.mdc` or `docs/engineering/runbook.md`). |
| AC-3 | **PASS** | `.cursor/rules/caveman.mdc` and `template/.cursor/rules/caveman.mdc` exist, byte-identical (SHA-256 `E10EFC32C628E790E69E2393F381108FE0B1F16E0BCDCFFFC162EFF6F91E47DE`), containing `CAVEMAN_MODE`, `literal`, all five operator phrases (`caveman on`, `caveman off`, `stop caveman`, `normal mode`, `caveman: lite|full|ultra`), 9-zone literal-region invariant, non-suppressible gate list, single-line JuliusBrussee/caveman attribution with no `npx skills add` leak. Subtest `test_caveman_default_off_rule_file_present_active_template` PASS. |
| AC-4 | **PASS** | `TOKEN_PROFILE` x `CAVEMAN_MODE` non-substitution paragraph present byte-identical in `docs/engineering/auto-orchestration-reference.md` (L784) and `template/docs/engineering/auto-orchestration-reference.md` (L784). Active-template SHA-256 MATCH. Subtest `test_caveman_default_off_reference_non_substitution_paragraph` PASS. |
| AC-5 | **PASS** | `### Caveman mode (US-0089)` subsection present in `docs/engineering/runbook.md` (L1330+) with non-substitution paragraph + 5-phrase table + key catalog + determinism semantics; `template/docs/engineering/runbook.md` byte-identical (SHA-256 MATCH). Subtest `test_caveman_default_off_runbook_operator_phrases` PASS. |
| AC-6 | **PASS** | 8 `test_caveman_default_off_*` subtests (items 1-5 from T-006 + items 6-8 from T-002) all green in targeted run. File extension in place in `tests/auto_command_contract_test.py` (no new module). |
| AC-7 | **PASS** | `# US-0089` heading present in `docs/engineering/architecture.md` (L3239) as the last `# US-####` heading (no later `# US-####` / `## US-####` follows); linked from `docs/product/backlog.md` (`## US-0089`, L2227) and `docs/engineering/decisions.md` (DEC-0072 entry at L134 + index pointer at L307-L316). Subtest `test_caveman_architecture_section_bottom_appended_and_linked` PASS. |
| AC-8 | **PASS** | Byte-identical active-template SHA-256 confirmed for `.cursor/rules/caveman.mdc`, `docs/engineering/auto-orchestration-reference.md`, `docs/engineering/runbook.md`. Negative parity: `.cursor/skills/its-magic/SKILL.md` + `template/.cursor/skills/its-magic/SKILL.md` contain **zero** `CAVEMAN_*`, `US-0089`, or operator-phrase tokens (grep hits = 0). Subtests `test_caveman_template_parity_sweep` + `test_caveman_skill_file_negative_parity` PASS. |

**Per-AC result**: **AC-1..AC-8 ALL PASS**. The FAIL verdict is driven exclusively by the **`run-tests.ps1` rule-count assertion drift (finding #1 above)**, which is an out-of-task-surface test-authoring gap rather than an AC regression.

## Default-off invariant confirmation (DEC-0072 section 6 byte-for-byte baseline)

Under `CAVEMAN_MODE=0` or absent:

- Existing `required` token list in `tests/auto_command_contract_test.py` is intact -- assertion `test_caveman_default_off_existing_contract_tokens_intact` PASS (no removed / renamed tokens).
- `AUTO_QUIET` non-suppressible gate vocabulary (`decision_gate`, `missing input`, `pause`, `loop_max`, `blocked`, `[BUG_VALIDATION_OK]`, `[INTAKE_EVIDENCE_VALIDATION_OK]`) preserved in `.cursor/commands/auto.md` + `docs/engineering/auto-orchestration-reference.md` -- subtest `test_caveman_default_off_non_suppressible_gate_vocab_preserved` PASS.
- No vendor install leak -- subtest `test_caveman_default_off_no_vendor_install_leak` PASS; independent grep confirms `npx skills add` absent from `.cursor/rules/caveman.mdc`, `docs/engineering/runbook.md`, and template mirrors.
- Spawn-only / strict-proof / isolation-evidence / user-visible-metadata / bug-issue contracts unchanged (no edits to their canonical files this story).

Default-off invariant **UPHELD byte-for-byte**.

## Template parity confirmation (DEC-0072 section 7 rows 2-5 + row 8)

SHA-256 active-template MATCH (byte-identical) for:

- `.cursor/rules/caveman.mdc` vs `template/.cursor/rules/caveman.mdc` -- **MATCH**
- `docs/engineering/auto-orchestration-reference.md` vs `template/docs/engineering/auto-orchestration-reference.md` -- **MATCH**
- `docs/engineering/runbook.md` vs `template/docs/engineering/runbook.md` -- **MATCH**
- `.cursor/skills/its-magic/SKILL.md` vs `template/.cursor/skills/its-magic/SKILL.md` -- **MATCH** (negative parity row 8; unchanged by US-0089; zero CAVEMAN tokens).

`.cursor/scratchpad.local.example.md` vs `template/.cursor/scratchpad.local.example.md` overall hashes **DIFFER** (existing divergence from historical operator-local example content pre-dating US-0089), but the four locked Caveman key lines + `## Caveman mode (US-0089)` comment block are byte-identical across the pair -- confirmed by `test_caveman_default_off_scratchpad_keys_example_parity` PASS. Row 2 parity requirement is for the locked Caveman strings, not the entire file; DEC-0072 section 7 row 2 is satisfied.

Template parity **UPHELD** for all US-0089-touched rows.

## Contract-gate results

| Gate | Result |
|------|--------|
| `[BUG_VALIDATION_OK]` | **PASS** -- `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` exit 0 |
| User-visible metadata guard (US-0071 / DEC-0053) | **PASS** -- `python scripts/check-user-visible-metadata.py` exit 0 |
| `[SCRATCHPAD_PAIR_OK]` | **FAIL -> observational** -- predominantly pre-existing US-0087 / US-0088 drift; additive US-0089 template_pair component is architecturally sanctioned by DEC-0072 section 7 row 1 / DEC-0055. **Not blocking US-0089** -- recommend dedicated BUG issue to encode the DEC-0055 carveout into the pair-parity script |

## Observations (non-blocking)

- **Pre-existing drift in `.cursor/commands/auto.md`** (US-0087 / US-0088) surfaces as 6+ `run-tests.ps1` failures and 3+ pytest-module failures. Not US-0089 scope; recommend a dedicated drift-repair story or bug issue.
- **Template baseline scratchpad drift** (US-0086 remote keys) surfaces as `test_remote_automation_profile_keys_exist_in_scratchpads` pre-existing failure. Not US-0089 scope.
- **Homebrew formula version drift** (items 2-3 of `run-tests.ps1` failures) surfaces as 2 NEW-since-US-0086 failures from a release metadata update; not US-0089 scope.
- `CAVEMAN_COMPRESS_INPUT` / `CAVEMAN_FILE_SCOPE` are reserved for **US-0090** and remain documented no-ops; T-007 assertion-only test confirms architecture.md bottom-append discipline honored.
- No DEC authored this cycle (decision rights stay with `/architecture`; DEC-0072 already locked).
- No canonical artifact rewrites observed beyond additive rows (backlog `## US-0089` architecture_notes, decisions.md index + context pack).

## Required remediation (1 blocking)

1. **Update `tests/run-tests.ps1` rule-count assertion** (file `tests/run-tests.ps1`, line 77):
   - From: `Assert-True "5 rules exist" ((Count-Files (Join-Path $tpl ".cursor\rules") "*.mdc") -eq 5)`
   - To: `Assert-True "6 rules exist" ((Count-Files (Join-Path $tpl ".cursor\rules") "*.mdc") -eq 6)`
   - Rationale: US-0089 / DEC-0072 section 7 row 3 legitimately adds `.cursor/rules/caveman.mdc` + `template/.cursor/rules/caveman.mdc`, raising the rule count from 5 to 6. The assertion was not updated in T-003; this causes `run-tests.ps1` to flip PASS -> FAIL on the rule-count sanity check. Minimal 1-char fix.
   - After remediation expectation: `run-tests.ps1` baseline becomes **Pass=783 / Fail=11** -- all 11 remaining failures are pre-existing drift unrelated to US-0089 (treat as separate triage).
   - Also verify parallel `tests/run-tests.sh` (POSIX harness) for analogous rule-count assertion; if present, bump symmetrically to keep Linux / POSIX check-in parity with PowerShell.

Pre-existing drift failures (items 2-12 in section 1 table) are **NOT** required to be fixed as part of this remediation; they should be triaged separately (likely candidates for dedicated drift-repair / BUG issues).

## Runtime QA / generated-test contracts

- **Runtime mode**: `runtime_mode=local` (no `REMOTE_EXECUTION=1`; remote runtime QA autopilot contract is zero-overhead skip for this story).
- **Runtime stack profile**: `runtime_stack_profile=python` (for repo test harness); `runtime_startup_command=powershell -ExecutionPolicy Bypass -File tests/run-tests.ps1`.
- **Runtime final verdict**: `runtime_final_verdict=fail` (harness exit 1, driven by rule-count assertion).
- **Runtime reason code**: not applicable to US-0089 product surface (not a runtime failure; harness-assertion failure).
- **Generated-test contract (US-0066 / DEC-0048)**: N/A -- US-0089 is a framework-metadata story, not a generated-project story.

## Strict runtime proof (DEC-0038)

- `orchestrator_run_id=auto-20260418-01`
- `runtime_proof_id=rp-auto-20260418-01-qa-qa-20260418T150000Z-S0075-US0089`
- `phase_id=qa`
- `role=qa`
- `proof_issued_at=2026-04-18T15:00:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=3bef1259f94c6c5d79cf30a45efbbd28765da263a6ef6ef4918010992fc809ca`

Canonical sorted-key JSON: `{"orchestrator_run_id":"auto-20260418-01","phase_id":"qa","proof_issued_at":"2026-04-18T15:00:00Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260418-01-qa-qa-20260418T150000Z-S0075-US0089"}`

## Isolation evidence (US-0048 / DEC-0029)

- `phase_id=qa`
- `role=qa`
- `fresh_context_marker=qa-S0075-US0089-qa-20260418T150000Z-fresh`
- `timestamp=2026-04-18T15:00:00Z`
- `evidence_ref=sprints/S0075/qa-findings.md,handoffs/qa_to_dev.md,handoffs/resume_brief.md,docs/engineering/state.md,tests/report.md`

## Next

- **`/execute`** (fresh **dev**) for **`S0075`** / **US-0089** -- apply the single blocking remediation in **`tests/run-tests.ps1`** (rule-count assertion `5 -> 6`; also update parallel `tests/run-tests.sh` if an analogous assertion exists), rerun `run-tests.ps1` + targeted caveman pytest, and hand back to `/qa`. Story remains **OPEN** per **US-0045**.
- Decision gate posture: **blocking** -- single clear remediation; no architecture / DEC change required; no `/verify-work` or `/release` should run until fix lands and QA re-verifies.

---

## QA-loop cycle 2 re-verification (2026-04-18)

### Status (cycle 2)

- **verdict**: **PASS**.
- **phase**: `/qa` -- fresh **qa** subagent, `orchestrator_run_id=auto-20260418-01`, timestamp `2026-04-18T17:00:00Z`, **qa_loop_cycle=2** of **qa_loop_max=5**.
- **sprint**: **S0075**; **story**: **US-0089** (remains **OPEN** per **US-0045**; closure at `/verify-work`).
- **decision-gate posture**: none -- prior blocking finding cleared; ready for `/verify-work`.
- **handoff**: `handoffs/qa_to_verify_work.md` (this cycle).
- **cycle-1 section above preserved unchanged (history).**

### Verdict rationale (cycle 2)

The single blocking finding from cycle 1 -- the stale `"5 rules exist"` assertion in the canonical check-in runner `tests/run-tests.ps1` (line 77) -- is cleared. Dev bumped both POSIX-parity runners (`tests/run-tests.ps1` line 77 and `tests/run-tests.sh` line 87) from `-eq 5` / `"5 rules exist"` to `-eq 6` / `"6 rules exist"`, matching the legitimate additive deliverable under DEC-0072 §7 row 3 (`.cursor/rules/caveman.mdc` + `template/` mirror). `.cursor/rules/` is independently verified to contain exactly 6 `.mdc` files (`caveman.mdc`, `coding-standards.mdc`, `core.mdc`, `escalation.mdc`, `handoffs.mdc`, `quality.mdc`); `template/.cursor/rules/` mirrors the same six. Report now shows `[PASS] 6 rules exist`.

AC-1..AC-8 surface, default-off invariant (DEC-0072 §6 items 1-8), template parity (DEC-0072 §7 rows 2-5 + row 8 negative parity), and all contract gates remain intact byte-for-byte -- the fix was strictly a test-harness count bump outside the AC surface. The 11 remaining `run-tests.ps1` failures are all pre-existing (US-0086 / US-0087 / US-0088 drift) and all disjoint from US-0089.

### Test evidence (cycle 2, independently re-run by QA)

#### 1. Canonical check-in suite -- `tests/run-tests.ps1`

- Command: `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"`
- Report: `tests/report.md` (`Timestamp=2026-04-18T12:38:03Z`)
- Results: **Pass=783, Fail=11**
- Baseline comparison:
  - US-0086 QA baseline (2026-04-13T21:22:07Z): Pass=788 / Fail=6.
  - Cycle 1 (pre-fix): Pass=782 / Fail=12.
  - Cycle 2 dev-reported (post-fix): Pass=783 / Fail=11.
  - Cycle 2 QA-observed: **Pass=783 / Fail=11** -- exact match to dev-reported, +1 pass / -1 fail vs cycle 1.
- Key line: `- [PASS] 6 rules exist` (line 21 of report) -- prior blocking `[FAIL] 5 rules exist` gone.

Classification of the 11 remaining failures (all identical to cycle-1 items 2-12; all pre-existing, all disjoint from US-0089 surface):

| # | Test | Pre-existing? | US-0089 surface? | Classification |
|---|------|---------------|------------------|----------------|
| 1 | `Homebrew stable formula URL uses npm version tag` | pre-existing (pre-dates US-0089; appeared new since US-0086) | no | release formula drift |
| 2 | `Homebrew stable formula version matches npm version` | pre-existing (pre-dates US-0089) | no | release formula drift |
| 3 | `Installer runbook TEST_COMMAND present for detectable stack (npm or sh template default)` | pre-existing | no | installer stack-detection drift |
| 4 | `CLI missing install runbook TEST_COMMAND present (npm or sh template default)` | pre-existing | no | installer stack-detection drift |
| 5 | `auto precedence includes argument > resume > state (active)` | pre-existing (US-0087 / US-0088) | no | `.cursor/commands/auto.md` drift |
| 6 | `auto includes strict-proof boundary step 11b (template)` | pre-existing | no | strict-proof step-label drift in template |
| 7 | `triad check passes on repo` | pre-existing | no | triad hot-surface oversize drift |
| 8 | `triad check idempotent rerun passes` | pre-existing | no | triad hot-surface oversize drift |
| 9 | `scratchpad pair parity check passes on repo` | pre-existing (mixed: US-0086/US-0087/US-0088 active_pair drift; additive US-0089 template_pair component **architecturally sanctioned** per DEC-0072 §7 row 1 / DEC-0055) | no (sanctioned) | pair-parity script lacks DEC-0055 carveout |
| 10 | `token-cost active/template parity passes` | pre-existing (US-0087 / US-0088) | no | `.cursor/commands/auto.md` drift |
| 11 | `slim auto command contract markers pass` | pre-existing (US-0087 / US-0088) | no | `.cursor/commands/auto.md` drift |

**All 11 pre-existing, all disjoint from US-0089.** No new failure introduced by the cycle-2 harness patch. Recommend separate triage (drift-repair / BUG issues) -- out of US-0089 scope.

#### 2. Targeted US-0089 subtests -- pytest `-k caveman`

- Command: `python -m pytest tests/auto_command_contract_test.py -q -k caveman`
- Result: **11 passed, 19 deselected, 119 subtests passed, 0 failed**. Exit 0. Unchanged from cycle 1.
- All 11 Caveman subtests (default-off invariant 1-5, default-off invariant 6-8, architecture bottom-append + link, template parity sweep, skill negative parity) remain green.

#### 3. Full contract module -- pytest `tests/auto_command_contract_test.py`

- Command: `python -m pytest tests/auto_command_contract_test.py -q`
- Result: **27 passed, 24 failed, 192 subtests passed**. Exit 1.
- 24-failure pre-existing baseline preserved byte-for-byte (identical set to cycle 1: `test_slim_auto_retains_gate_markers`, `test_slim_auto_references_step5_and_continuation`, `test_remote_automation_profile_keys_exist_in_scratchpads`, `test_template_auto_literal_parity_active`, `test_template_scratchpad_baseline_literal_parity_active`, `test_template_scratchpad_example_literal_parity_active`, etc.). No new regression introduced by cycle-2 patch.

#### 4. Remote config summary -- pytest

- Command: `python -m pytest tests/remote_config_summary_test.py -q`
- Result: **4 passed**, 0 failed. Exit 0. Unchanged.

#### 5. Bug issue validator

- Command: `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance`
- Output: `[BUG_VALIDATION_OK]`. Exit 0.

#### 6. User-visible metadata guard (US-0071 / DEC-0053)

- Command: `python scripts/check-user-visible-metadata.py`
- Exit 0 -- **PASS** (no `USER_VISIBLE_INTERNAL_METADATA_DETECTED`).

### Per-AC re-verification (AC-1..AC-8 vs DEC-0072; cycle 2)

| AC | Cycle-1 verdict | Cycle-2 verdict | Evidence (unchanged from cycle 1; no code edit on AC surface this cycle) |
|----|-----------------|-----------------|---------------------------------------------------------------------------|
| AC-1 | PASS | **PASS (reaffirmed)** | Four locked key lines + `## Caveman mode (US-0089)` comment block intact in `.cursor/scratchpad.md`, `.cursor/scratchpad.local.example.md`, `template/.cursor/scratchpad.local.example.md`. Subtests `test_caveman_default_off_scratchpad_keys_active` + `test_caveman_default_off_scratchpad_keys_example_parity` PASS. |
| AC-2 | PASS | **PASS (reaffirmed)** | DEC-0072 §6 items 6-8 subtests PASS (`test_caveman_default_off_existing_contract_tokens_intact`, `test_caveman_default_off_non_suppressible_gate_vocab_preserved`, `test_caveman_default_off_no_vendor_install_leak`). |
| AC-3 | PASS | **PASS (reaffirmed)** | `.cursor/rules/caveman.mdc` + `template/.cursor/rules/caveman.mdc` byte-identical (SHA-256 active=template MATCH, independently recomputed). Subtest `test_caveman_default_off_rule_file_present_active_template` PASS. |
| AC-4 | PASS | **PASS (reaffirmed)** | `TOKEN_PROFILE x CAVEMAN_MODE` non-substitution paragraph present byte-identical in `docs/engineering/auto-orchestration-reference.md` + `template/`. Active=template SHA-256 MATCH recomputed. Subtest `test_caveman_default_off_reference_non_substitution_paragraph` PASS. |
| AC-5 | PASS | **PASS (reaffirmed)** | `### Caveman mode (US-0089)` subsection in `docs/engineering/runbook.md` + `template/` byte-identical. Active=template SHA-256 MATCH recomputed. Subtest `test_caveman_default_off_runbook_operator_phrases` PASS. |
| AC-6 | PASS | **PASS (reaffirmed)** | All 8 `test_caveman_default_off_*` subtests green (cycle 2). |
| AC-7 | PASS | **PASS (reaffirmed)** | `# US-0089` heading bottom-appended in `docs/engineering/architecture.md` and linked from `docs/product/backlog.md` + `docs/engineering/decisions.md`. Subtest `test_caveman_architecture_section_bottom_appended_and_linked` PASS. |
| AC-8 | PASS | **PASS (reaffirmed)** | Active=template SHA-256 MATCH for all three US-0089-touched pairs; negative parity `.cursor/skills/its-magic/SKILL.md` zero Caveman tokens. Subtests `test_caveman_template_parity_sweep` + `test_caveman_skill_file_negative_parity` PASS. |

**Cycle-2 per-AC result**: **AC-1..AC-8 ALL PASS reaffirmed**. No regression observed. The cycle-2 harness patch touched only `tests/run-tests.ps1` line 77 and `tests/run-tests.sh` line 87 -- entirely outside the AC-1..AC-8 product/test surface.

### Default-off invariant (cycle 2)

Under `CAVEMAN_MODE=0` or absent: UPHELD byte-for-byte. All 8 default-off subtests green. No `npx skills add` leak. AUTO_QUIET non-suppressible gate vocabulary preserved. Existing contract tokens intact. Independent verification via targeted caveman pytest (11/0) and full contract module (27 passed; caveman portion unchanged). No byte drift introduced by the cycle-2 patch (the touched files -- `tests/run-tests.ps1`, `tests/run-tests.sh` -- are not part of the default-off invariant surface).

### Template parity (cycle 2)

All four US-0089-touched active-template pairs with byte-identical content requirement hold:

- `.cursor/rules/caveman.mdc` vs `template/.cursor/rules/caveman.mdc`: **MATCH** (SHA-256 recomputed this cycle).
- `docs/engineering/auto-orchestration-reference.md` vs `template/docs/engineering/auto-orchestration-reference.md`: **MATCH**.
- `docs/engineering/runbook.md` vs `template/docs/engineering/runbook.md`: **MATCH**.
- `.cursor/skills/its-magic/SKILL.md` vs `template/.cursor/skills/its-magic/SKILL.md`: **MATCH** (negative parity row 8; zero Caveman tokens -- unchanged).

Cycle-2 patch on `tests/run-tests.*`: no `template/tests/run-tests.*` mirror exists (test runners are active-only, consistent with row 7 of DEC-0072 §7 which lists no template runner row). **No parity drift introduced.** Template parity **UPHELD** -- confirmed symmetric to cycle 1.

### Contract-gate results (cycle 2)

| Gate | Cycle-2 Result |
|------|----------------|
| `[BUG_VALIDATION_OK]` | **PASS** -- exit 0 |
| User-visible metadata guard (US-0071 / DEC-0053) | **PASS** -- exit 0 |
| `[SCRATCHPAD_PAIR_OK]` | **FAIL -> observational** -- same root cause as cycle 1 (pre-existing US-0086/US-0087/US-0088 `active_pair` drift + sanctioned US-0089 `template_pair` CAVEMAN_* keys per DEC-0072 §7 row 1 / DEC-0055). **Not blocking US-0089.** Separate triage still recommended (BUG issue or script carveout). |

### Observations (non-blocking, cycle 2)

- Pre-existing `.cursor/commands/auto.md` drift (US-0087 / US-0088) continues to surface as 6 pytest-module failures and several `run-tests.ps1` failures. Out of US-0089 scope.
- Pre-existing `template/.cursor/scratchpad.md` remote-key drift (US-0086) continues to surface as `test_remote_automation_profile_keys_exist_in_scratchpads`. Out of US-0089 scope.
- Pre-existing triad hot-surface oversize drift continues to surface twice in `run-tests.ps1`. Out of US-0089 scope.
- Pre-existing Homebrew formula version drift continues (2 `run-tests.ps1` failures). Out of US-0089 scope.
- `CAVEMAN_COMPRESS_INPUT` / `CAVEMAN_FILE_SCOPE` remain reserved for US-0090; no-ops confirmed.

### Runtime QA / generated-test contracts (cycle 2)

- **Runtime mode**: `runtime_mode=local` (no `REMOTE_EXECUTION=1`; zero-overhead skip).
- **Runtime stack profile**: `runtime_stack_profile=python`; `runtime_startup_command=powershell -ExecutionPolicy Bypass -File tests/run-tests.ps1`.
- **Runtime final verdict**: `runtime_final_verdict=pass` (from QA's US-0089-scoped lens: the blocking assertion clears; remaining 11 failures are pre-existing observational drift; the decision-gate-relevant runtime surface for US-0089 is PASS).
- **Generated-test contract (US-0066 / DEC-0048)**: N/A -- US-0089 is a framework-metadata story.

### Decision-gate posture (cycle 2)

**None.** The single cycle-1 blocking finding is cleared with a minimal surgical patch that introduced zero new failures. AC-1..AC-8 reaffirmed PASS. Default-off invariant and template parity UPHELD. Contract gates pass (`[BUG_VALIDATION_OK]`, metadata guard PASS). QA-loop terminates cleanly at cycle 2 (well inside `AUTO_LOOP_MAX_CYCLES=5`). Ready for `/verify-work`.

### Strict runtime proof (cycle 2, DEC-0038)

- `orchestrator_run_id=auto-20260418-01`
- `runtime_proof_id=rp-auto-20260418-01-qa-qa-20260418T170000Z-S0075-US0089-loop2`
- `phase_id=qa`
- `role=qa`
- `proof_issued_at=2026-04-18T17:00:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=5910d19fa6c14b94089b378d1c4552263c377b02ff9d18a0dea2511de9cebc05`

Canonical sorted-key JSON: `{"orchestrator_run_id":"auto-20260418-01","phase_id":"qa","proof_issued_at":"2026-04-18T17:00:00Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260418-01-qa-qa-20260418T170000Z-S0075-US0089-loop2"}`.

### Isolation evidence (cycle 2, US-0048 / DEC-0029)

- `phase_id=qa`
- `role=qa`
- `fresh_context_marker=qa-S0075-US0089-qa-20260418T170000Z-loop2-fresh`
- `timestamp=2026-04-18T17:00:00Z`
- `evidence_ref=sprints/S0075/qa-findings.md,handoffs/qa_to_verify_work.md,handoffs/resume_brief.md,docs/engineering/state.md,tests/report.md`

### Next (cycle 2)

- **`/verify-work`** (fresh **qa** context) for **`S0075`** / **US-0089** -- QA-loop cycle-2 PASS unblocks verify-work. Per DEC-0051 phase->role matrix, canonical role is `qa`.
- Decision gate posture: **none expected**.
- Story remains **OPEN** per **US-0045** (closure at `/verify-work` or `/release`).
