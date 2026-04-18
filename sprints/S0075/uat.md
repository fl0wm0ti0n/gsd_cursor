# UAT Matrix — S0075 / US-0089

**Populated at `/verify-work` (qa, fresh context, `auto-20260418-01`, 2026-04-18T18:00:00Z).**

## Orchestration pointer

- **orchestrator_run_id**: `auto-20260418-01`
- **story_id**: **US-0089** -- Cursor Caveman mode (scratchpad-configurable terse responses)
- **sprint_id**: **S0075**
- **uat_completed_at**: `2026-04-18T18:00:00Z`
- **verified_by**: `role=qa`, `orchestrator_run_id=auto-20260418-01`
- **status**: **PASS** (`VERIFY_WORK_UAT_COMPLETE`)
- **decision gate posture**: **none**
- **next phase**: `/release` (fresh release subagent)
- **status authority (US-0045)**: **US-0089** remains **OPEN** in `docs/product/backlog.md` until `/release`.

## UAT steps (AC-1..AC-8 / T-001..T-008)

| Step | AC | Task | Verdict | User-facing description | Evidence |
|------|----|------|---------|-------------------------|----------|
| UAT-1 | AC-1 | T-001 | **PASS** | Operator confirms four locked Caveman scratchpad keys (`CAVEMAN_MODE=0`, `CAVEMAN_LEVEL=`, `CAVEMAN_COMPRESS_INPUT=0`, `CAVEMAN_FILE_SCOPE=`) + `## Caveman mode (US-0089)` comment block are present byte-for-byte in active baseline scratchpad, active example, and template example -- so a fresh install surfaces the contract with default-off semantics. | `.cursor/scratchpad.md` (L234, L246-L249); `.cursor/scratchpad.local.example.md` (L209, L221-L224); `template/.cursor/scratchpad.local.example.md` (L228, L240-L243); subtests `test_caveman_default_off_scratchpad_keys_active` + `test_caveman_default_off_scratchpad_keys_example_parity` PASS (cycle 2). |
| UAT-2 | AC-2 | T-002 | **PASS** | Operator confirms default-off parity: with `CAVEMAN_MODE=0` (or absent), no change to normative command strings, gate ordering, spawn-only language (BUG-0006), `AUTO_QUIET` non-suppressible gate vocabulary, existing contract tokens; no `npx skills add` vendor install leak in runbook or Caveman rule file. | Subtests `test_caveman_default_off_existing_contract_tokens_intact`, `test_caveman_default_off_non_suppressible_gate_vocab_preserved`, `test_caveman_default_off_no_vendor_install_leak` PASS (DEC-0072 §6 items 6-8, cycle 2); `sprints/S0075/qa-findings.md` cycle-2 per-AC table AC-2 PASS. |
| UAT-3 | AC-3 | T-003 | **PASS** | Operator confirms Cursor behavior pack: `.cursor/rules/caveman.mdc` active exists, byte-identical to `template/.cursor/rules/caveman.mdc`, carrying scratchpad gate contract, 9-zone literal-region invariant, AUTO_QUIET non-suppressible gate vocabulary, 5 canonical operator phrases (`caveman on` / `caveman off` / `stop caveman` / `normal mode` / `caveman: lite\|full\|ultra`), non-substitution paragraph, default-off invariant, and DEC-0072 §8 non-goals. | `.cursor/rules/caveman.mdc` + `template/.cursor/rules/caveman.mdc` SHA-256 MATCH `E10EFC32C628E790E69E2393F381108FE0B1F16E0BCDCFFFC162EFF6F91E47DE` (cycle 2); subtest `test_caveman_default_off_rule_file_present_active_template` PASS; `tests/run-tests.ps1` `[PASS] 6 rules exist` confirms rule-file count post cycle-2 patch. |
| UAT-4 | AC-4 | T-004 | **PASS** | Operator confirms `TOKEN_PROFILE` x `CAVEMAN_MODE` non-substitution paragraph is published byte-identically in active + template `docs/engineering/auto-orchestration-reference.md`, so `CAVEMAN_MODE=1` cannot be misread as a lean `TOKEN_PROFILE` equivalent. | `docs/engineering/auto-orchestration-reference.md` L784 + `template/docs/engineering/auto-orchestration-reference.md` L784 (active=template SHA-256 MATCH cycle 2); subtest `test_caveman_default_off_reference_non_substitution_paragraph` PASS. |
| UAT-5 | AC-5 | T-005 | **PASS** | Operator confirms `### Caveman mode (US-0089)` runbook subsection is present byte-identically in active + template `docs/engineering/runbook.md`, with non-substitution paragraph, scratchpad keys table, 5-phrase operator toggle catalog, determinism semantics, and pointer to the 9-zone literal-region invariant. | `docs/engineering/runbook.md` L1330+ + `template/docs/engineering/runbook.md` (active=template SHA-256 MATCH cycle 2); subtest `test_caveman_default_off_runbook_operator_phrases` PASS. |
| UAT-6 | AC-6 | T-006 | **PASS** | Operator confirms regression-lock: `tests/auto_command_contract_test.py` carries all 8 `test_caveman_default_off_*` subtests (items 1-5 from T-006 + items 6-8 from T-002, matching DEC-0072 §6 cardinality) plus the 3 supplemental Caveman subtests (architecture bottom-append + link, template parity sweep, SKILL negative parity). | `python -m pytest tests/auto_command_contract_test.py -q -k caveman` -> **11 passed / 19 deselected / 119 subtests / 0 failed** (cycle 2, unchanged); 8 `test_caveman_default_off_*` all green. |
| UAT-7 | AC-7 | T-007 | **PASS** | Operator confirms `docs/engineering/architecture.md` carries `# US-0089` section bottom-appended (no later `# US-xxxx` / `## US-xxxx` heading follows) and is linked from `docs/product/backlog.md` `## US-0089` and `docs/engineering/decisions.md` DEC-0072 entry + compact index -- preserving append-bottom canonical discipline and full story linkage. | `docs/engineering/architecture.md` L3239 `# US-0089`; `docs/product/backlog.md` `## US-0089` L2227 (architecture_notes pointer); `docs/engineering/decisions.md` DEC-0072 entry L134 + index L307-L316; subtest `test_caveman_architecture_section_bottom_appended_and_linked` PASS. |
| UAT-8 | AC-8 | T-008 | **PASS** | Operator confirms template parity across four US-0089-touched `.cursor/` / `docs/engineering/` surfaces (rule file, reference doc, runbook, scratchpad example for the locked key region) and zero Caveman token leak in `.cursor/skills/its-magic/SKILL.md` negative-parity surface -- per US-0017 + DEC-0072 §7 rows 2-5 + row 8. | SHA-256 active=template MATCH recomputed cycle 2 for `.cursor/rules/caveman.mdc`, `docs/engineering/auto-orchestration-reference.md`, `docs/engineering/runbook.md`; `.cursor/skills/its-magic/SKILL.md` + template mirror zero `CAVEMAN_*` / `US-0089` / operator-phrase tokens; subtests `test_caveman_template_parity_sweep` + `test_caveman_skill_file_negative_parity` PASS. |

## Target summary

- **pass / fail / total**: **8 / 0 / 8**
- **ratio**: **8/8 PASS**
- **story_status_after_verify_work**: **OPEN** (closure at `/release` per US-0045).

## Isolation compliance (US-0048 / DEC-0029)

**Verdict: PASS.** All 10 completed phases for US-0089 / S0075 carry valid, distinct isolation evidence in `docs/engineering/state.md`.

| # | phase_id | role | fresh_context_marker | runtime_proof_id |
|---|----------|------|----------------------|------------------|
| 1 | `discovery` | `po` | `po-US0089-discovery-20260418T120500Z-fresh` | `rp-auto-20260418-01-discovery-po-20260418T120500Z-US0089` |
| 2 | `research` | `tech-lead` | `tl-US0089-research-20260418T121500Z-fresh` | `rp-auto-20260418-01-research-tech-lead-20260418T121500Z-US0089` |
| 3 | `architecture` | `tech-lead` | `tl-US0089-architecture-20260418T123000Z-fresh` | `rp-auto-20260418-01-architecture-tech-lead-20260418T123000Z-US0089` |
| 4 | `sprint-plan` | `tech-lead` | `tl-US0089-sprint-plan-20260418T124500Z-fresh` | `rp-auto-20260418-01-sprint-plan-tech-lead-20260418T124500Z-US0089-S0075` |
| 5 | `plan-verify` | `qa` | `qa-S0075-US0089-plan-verify-20260418T130000Z-fresh` | `rp-auto-20260418-01-plan-verify-qa-20260418T130000Z-S0075-US0089` |
| 6 | `execute` (cycle 1) | `dev` | `dev-US0089-execute-20260418T140000Z-S0075-fresh` | `rp-auto-20260418-01-execute-dev-20260418T140000Z-S0075-US0089` |
| 7 | `qa` (cycle 1) | `qa` | `qa-S0075-US0089-qa-20260418T150000Z-fresh` | `rp-auto-20260418-01-qa-qa-20260418T150000Z-S0075-US0089` |
| 8 | `execute` (cycle 2) | `dev` | `dev-US0089-execute-20260418T160000Z-S0075-loop2-fresh` | `rp-auto-20260418-01-execute-dev-20260418T160000Z-S0075-US0089-loop2` |
| 9 | `qa` (cycle 2) | `qa` | `qa-S0075-US0089-qa-20260418T170000Z-loop2-fresh` | `rp-auto-20260418-01-qa-qa-20260418T170000Z-S0075-US0089-loop2` |
| 10 | `verify-work` | `qa` | `qa-S0075-US0089-verify-work-20260418T180000Z-fresh` | `rp-auto-20260418-01-verify-work-qa-20260418T180000Z-S0075-US0089` |

No `PHASE_CONTEXT_ISOLATION_MISSING` / `PHASE_CONTEXT_ISOLATION_VIOLATION` / `ISOLATION_EVIDENCE_STALE` / `ISOLATION_EVIDENCE_INVALID` observed. Every `fresh_context_marker` is distinct.

## Strict runtime proof compliance (US-0056 / DEC-0038)

**Verdict: PASS.** **10 distinct** `runtime_proof_id` values across 10 completed phases; each hashed as SHA-256 of sorted-key JSON over the canonical tuple. No reuse, no missing, no invalid, no ambiguous linkage.

| # | phase_id (cycle) | runtime_proof_id | proof_hash |
|---|------------------|------------------|------------|
| 1 | `discovery` | `rp-auto-20260418-01-discovery-po-20260418T120500Z-US0089` | `d9cddea7b36a663a10dcebc9c25b1aed5db8509fce47f31d5fa573efc210d40c` |
| 2 | `research` | `rp-auto-20260418-01-research-tech-lead-20260418T121500Z-US0089` | `bf62cc661618dd6c6ad12b5d1af3888d5b9efa1e92f71592906066208987e8d5` |
| 3 | `architecture` | `rp-auto-20260418-01-architecture-tech-lead-20260418T123000Z-US0089` | `3fad7c97b67e3014806b8e712ce4f024597c11a9f9e717dab7b5050c4468cc82` |
| 4 | `sprint-plan` | `rp-auto-20260418-01-sprint-plan-tech-lead-20260418T124500Z-US0089-S0075` | `9837d899f11b198de97b16b07497000dcb1603f9104ba799c501d8d8c9e158d7` |
| 5 | `plan-verify` | `rp-auto-20260418-01-plan-verify-qa-20260418T130000Z-S0075-US0089` | `454a90ed6117490ccdb6e7a9ce603681c68e5cf36fef89c94947c3d7649bf480` |
| 6 | `execute` cycle 1 | `rp-auto-20260418-01-execute-dev-20260418T140000Z-S0075-US0089` | `8a9f9ecc8dce7e31806f5dad53d205e40d9e5e325ecd7ce74b0a64ec42262482` |
| 7 | `qa` cycle 1 | `rp-auto-20260418-01-qa-qa-20260418T150000Z-S0075-US0089` | `3bef1259f94c6c5d79cf30a45efbbd28765da263a6ef6ef4918010992fc809ca` |
| 8 | `execute` cycle 2 | `rp-auto-20260418-01-execute-dev-20260418T160000Z-S0075-US0089-loop2` | `c43fc4471e31d838f492fcd4054fedd80d11300588290f51801189cb0654e937` |
| 9 | `qa` cycle 2 | `rp-auto-20260418-01-qa-qa-20260418T170000Z-S0075-US0089-loop2` | `5910d19fa6c14b94089b378d1c4552263c377b02ff9d18a0dea2511de9cebc05` |
| 10 | `verify-work` | `rp-auto-20260418-01-verify-work-qa-20260418T180000Z-S0075-US0089` | `e1f0d305b11cbbe68b2487a1ffe2b6d20d7ca6900c08ff460ea1d23c831e7a6a` |

No `RUNTIME_PROOF_MISSING` / `RUNTIME_PROOF_INVALID` / `RUNTIME_PROOF_REUSED` / `RUNTIME_PROOF_STALE` / `RUNTIME_PROOF_AMBIGUOUS_LINK` observed.

## This verify-work strict proof (DEC-0038)

- `orchestrator_run_id=auto-20260418-01`
- `runtime_proof_id=rp-auto-20260418-01-verify-work-qa-20260418T180000Z-S0075-US0089`
- `phase_id=verify-work`
- `role=qa`
- `proof_issued_at=2026-04-18T18:00:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=e1f0d305b11cbbe68b2487a1ffe2b6d20d7ca6900c08ff460ea1d23c831e7a6a`

Canonical sorted-key JSON: `{"orchestrator_run_id":"auto-20260418-01","phase_id":"verify-work","proof_issued_at":"2026-04-18T18:00:00Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260418-01-verify-work-qa-20260418T180000Z-S0075-US0089"}`

## This verify-work isolation evidence (US-0048 / DEC-0029)

- `phase_id=verify-work`
- `role=qa`
- `fresh_context_marker=qa-S0075-US0089-verify-work-20260418T180000Z-fresh`
- `timestamp=2026-04-18T18:00:00Z`
- `evidence_ref=sprints/S0075/uat.json,sprints/S0075/uat.md,handoffs/qa_to_release.md,docs/product/backlog.md,handoffs/resume_brief.md,docs/engineering/state.md`

## Notes

- No code, test, DEC, architecture, backlog AC, or qa-findings text modified by this phase -- `/verify-work` is strictly assertion + UAT population + traceability + handoff.
- Pre-existing 24 `auto_command_contract_test.py` failures and 11 `tests/run-tests.ps1` failures remain out of US-0089 scope (US-0086 / US-0087 / US-0088 drift; Homebrew formula drift; triad hot-surface drift; `SCRATCHPAD_PAIR_ERROR` sanctioned per DEC-0072 §7 row 1 / DEC-0055 + pre-existing drift) -- recommend separate triage as dedicated drift-repair / BUG issues after release.
- `CAVEMAN_COMPRESS_INPUT` / `CAVEMAN_FILE_SCOPE` remain reserved-for-US-0090 documented no-ops; no behavior change in US-0089.
- `[BUG_VALIDATION_OK]` + user-visible metadata guard (US-0071 / DEC-0053) remained PASS throughout the lifecycle.

## Next

- **`/release`** (fresh **release** subagent) for **`S0075`** / **US-0089**. Or **`/auto start-from=release`**. Decision gate posture: **none expected**. Expected outcome: story flip `OPEN -> DONE` per US-0045; acceptance checklist check-off; sprint release queue advanced.
