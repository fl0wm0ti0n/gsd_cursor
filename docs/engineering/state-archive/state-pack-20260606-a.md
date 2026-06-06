# State archive pack (2026-06-06)

- Rollover trigger: `STATE_HOT_MAX_LINES=1200, STATE_HOT_MAX_CHECKPOINTS=80`
- Source: `docs/engineering/state.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 18
- First archived heading: `## QA checkpoint (2026-04-18) -- US-0089 / S0075 / auto-20260418-01`
- Last archived heading: `## QA checkpoint (2026-04-18) -- US-0089 / S0075 / auto-20260418-01`
- Verification tuple (mandatory):
  - archived_body_lines=70
  - preamble_lines=11
  - retained_body_lines=1185

---

## QA checkpoint (2026-04-18) -- US-0089 / S0075 / auto-20260418-01

- **`/qa`** executed in fresh **qa** context for **`S0075`** / **US-0089** (`orchestrator_run_id=auto-20260418-01`, `2026-04-18T15:00:00Z`).
- **Verdict**: **FAIL** -- blocking remediation required before `/verify-work`. AC-1..AC-8 individually **ALL PASS**; failure is driven by a single NEW test-harness assertion regression on the US-0089 surface: `tests/run-tests.ps1` asserts `"5 rules exist"` (`-eq 5`), but US-0089 / **DEC-0072** section 7 row 3 legitimately adds `.cursor/rules/caveman.mdc` + `template/.cursor/rules/caveman.mdc`, raising the count to 6.
- **Test evidence**:
  - Canonical check-in suite: `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` -> exit 1, `tests/report.md` (`Timestamp=2026-04-18T12:09:41Z`, **Pass=782 / Fail=12**). Baseline US-0086 QA: Pass=788 / Fail=6. Delta vs baseline: -6 pass / +6 fail; of the 12 failures, exactly **1 is NEW on US-0089 surface** (rule-count assertion), the remaining **11 are pre-existing drift** (US-0086 / US-0087 / US-0088 `.cursor/commands/auto.md`, scratchpad-pair, triad hot-surface, Homebrew formula, installer TEST_COMMAND).
  - Targeted Caveman pytest: `python -m pytest tests/auto_command_contract_test.py -q -k caveman` -> **11 passed / 19 deselected / 119 subtests / 0 failed** (exit 0).
  - Full contract module: `python -m pytest tests/auto_command_contract_test.py -q` -> **27 passed / 24 failed / 192 subtests** (exit 1; 24 failures pre-existing, disjoint from US-0089 per dev stash-baseline).
  - Full pytest: `python -m pytest -q` -> **66 passed / 24 failed / 4 skipped / 192 subtests** (exit 1; same pre-existing failure set).
  - Remote config regression: `python -m pytest tests/remote_config_summary_test.py -q` -> **4 passed** (exit 0).
  - Bug validator: `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` -> `[BUG_VALIDATION_OK]` (exit 0).
  - User-visible metadata guard (US-0071 / DEC-0053): `python scripts/check-user-visible-metadata.py` -> exit 0 (PASS).
  - Scratchpad pair parity: `python scripts/check-scratchpad-pair-parity.py` -> exit 1 (`SCRATCHPAD_PAIR_ERROR`); `active_pair` drift pre-existing; `template_pair` `CAVEMAN_*` divergence architecturally sanctioned by **DEC-0072 section 7 row 1** / **DEC-0055** (example-only install). Observational only, not blocking US-0089.
- **Per-AC verification**: AC-1 (scratchpad keys + comment block in three files) PASS; AC-2 (default-off invariant, items 6-8) PASS; AC-3 (`.cursor/rules/caveman.mdc` active+template byte-identical SHA-256 `E10EFC32C628E790E69E2393F381108FE0B1F16E0BCDCFFFC162EFF6F91E47DE`) PASS; AC-4 (non-substitution paragraph active+template) PASS; AC-5 (runbook `### Caveman mode (US-0089)` subsection active+template) PASS; AC-6 (8 `test_caveman_default_off_*` subtests green) PASS; AC-7 (`# US-0089` bottom-appended + linked) PASS; AC-8 (template parity sweep + negative parity on `.cursor/skills/its-magic/SKILL.md`) PASS. **AC-1..AC-8 ALL PASS**.
- **Default-off invariant (DEC-0072 section 6)**: UPHELD byte-for-byte -- existing `required` token list intact, AUTO_QUIET non-suppressible gate vocabulary preserved, no vendor install leak.
- **Template parity (DEC-0072 section 7 rows 2-5 + row 8)**: UPHELD -- byte-identical SHA-256 for `.cursor/rules/caveman.mdc`, `docs/engineering/auto-orchestration-reference.md`, `docs/engineering/runbook.md`; negative parity row 8 on `.cursor/skills/its-magic/SKILL.md` (0 CAVEMAN_*, 0 US-0089, 0 operator-phrase tokens).
- **Decision gate posture**: **blocking** -- return to `/execute` (fresh dev) to apply 1-char rule-count bump in `tests/run-tests.ps1` (+ `tests/run-tests.sh` if symmetric assertion present), rerun `tests/run-tests.ps1` + targeted caveman pytest, hand back to `/qa`. No DEC / architecture / backlog AC edit required.
- **Canonical status authority**: `docs/product/backlog.md` **US-0089** stays **OPEN** per **US-0045**; acceptance portfolio row unchanged.

Isolation evidence (**US-0048** / **DEC-0029**):

- `phase_id=qa`
- `role=qa`
- `fresh_context_marker=qa-S0075-US0089-qa-20260418T150000Z-fresh`
- `timestamp=2026-04-18T15:00:00Z`
- `evidence_ref=sprints/S0075/qa-findings.md,handoffs/qa_to_dev.md,handoffs/resume_brief.md,docs/engineering/state.md,tests/report.md`

Strict runtime proof (**US-0056** / **DEC-0038**): canonical tuple hashed as **SHA-256** of **sorted-key JSON** over (`orchestrator_run_id`, `runtime_proof_id`, `phase_id`, `role`, `proof_issued_at`, `proof_ttl_seconds`). **`proof_ttl_seconds`** is a JSON **integer**.

- `orchestrator_run_id=auto-20260418-01`
- `runtime_proof_id=rp-auto-20260418-01-qa-qa-20260418T150000Z-S0075-US0089`
- `phase_id=qa`
- `role=qa`
- `proof_issued_at=2026-04-18T15:00:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=3bef1259f94c6c5d79cf30a45efbbd28765da263a6ef6ef4918010992fc809ca`

Canonical payload: `{"orchestrator_run_id":"auto-20260418-01","phase_id":"qa","proof_issued_at":"2026-04-18T15:00:00Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260418-01-qa-qa-20260418T150000Z-S0075-US0089"}`.

Traceability index (**DEC-0010**):

| Story | Sprint | Tasks | Status | Evidence |
|-------|--------|-------|--------|----------|
| US-0089 | S0075 | T-001..T-008 | QA FAIL (blocking; harness rule-count assertion) | sprints/S0075/qa-findings.md, handoffs/qa_to_dev.md, handoffs/resume_brief.md, docs/engineering/state.md, tests/report.md |

## Phase boundary status (post-qa, US-0089 / S0075 / auto-20260418-01)

- `phase_boundary=qa`
- `next_scheduled_phase=execute`
- `segment_work_item_kind=story`
- `active_bug_id=(none)`
- `bug_queue_position=(none)`
- `bug_queue_remaining=(none)`
- `backlog_drain_active=true`
- `bug_queue_active=false`
- `backlog_drain_stories_remaining_budget=6`
- `bug_id=(none)`
- `story_id=US-0089`
- `sprint_id=S0075`
- `orchestrator_run_id=auto-20260418-01`

**Phase boundary operator visibility (AC-10)** -- compact status: `phase_boundary=qa`; `next_scheduled_phase=execute`; `segment_work_item_kind=story`; `active_bug_id=(none)`; `bug_queue_position=(none)`; `bug_queue_remaining=(none)`; `backlog_drain_active=true`; `bug_queue_active=false`; `backlog_drain_stories_remaining_budget=6`; `story_id=US-0089`; `sprint_id=S0075`; `orchestrator_run_id=auto-20260418-01`.

**Boundary verification (qa complete)**: isolation `phase_id=qa` / `role=qa` + strict proof `runtime_proof_id=rp-auto-20260418-01-qa-qa-20260418T150000Z-S0075-US0089` / `proof_hash=3bef1259f94c6c5d79cf30a45efbbd28765da263a6ef6ef4918010992fc809ca` recorded above.

**Preflight for next phase (US-0069 / DEC-0051)**: spawn `phase_id=execute`, `role=dev` (canonical default per DEC-0051 phase->role matrix; FAIL returns to dev for remediation). Execute must apply the 1-char rule-count bump in `tests/run-tests.ps1` (line 77: `"5 rules exist"` / `-eq 5` -> `"6 rules exist"` / `-eq 6`) and symmetric change in `tests/run-tests.sh` if present; rerun `tests/run-tests.ps1` (expect **Pass=783 / Fail=11** post-fix) + targeted caveman pytest (expect 11/0), then hand back to `/qa` for re-verification. Decision gate posture: **blocking** -- do not run `/verify-work` until fix lands. No DEC / architecture / backlog AC change required.

**Bug validator (US-0088 / DEC-0069)**: `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` -> `[BUG_VALIDATION_OK]`. Bug issue format + acceptance rows intact post-qa artifact writes.


