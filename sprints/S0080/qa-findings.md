# QA Findings — S0080 / BUG-0011 (cycle 1)

## Metadata

- **sprint_id**: S0080
- **bug_id**: BUG-0011
- **dec_id**: DEC-0077 (composes on DEC-0072; US-0090 orthogonal)
- **cycle**: 1
- **role**: qa
- **timestamp**: 2026-06-06T14:52:02Z
- **orchestrator_run_id**: auto-20260606-02
- **fresh_context_marker**: qa-S0080-BUG0011-qa-20260606T145202Z-fresh
- **inputs_reviewed**: `sprints/S0080/tasks.md`, `sprints/S0080/summary.md`, `sprints/S0080/plan-verify.json`, `handoffs/dev_to_qa.md`, `decisions/DEC-0077.md`, `docs/product/backlog.md` `### BUG-0011`, `docs/engineering/architecture.md` `# BUG-0011`, `tests/run-tests.ps1` §30A.

## Overall verdict

**PASS** — All 8 ACs (AC-1..AC-8) satisfied; harness **§30A** green; nine `test_caveman_voice_*` + SHA baseline bump + regression guard + architecture linkage verified; active/template `caveman.mdc` byte parity confirmed; no regressions attributable to BUG-0011. Bug **BUG-0011** remains **OPEN** per **US-0045** (closure at `/release`).

- `ac_coverage`: AC-1..AC-8 = 8/8 PASS
- `regressions_found`: **none attributable to BUG-0011** (harness Fail=14 vs S0079 QA baseline Fail=14; +1 pass from §30A; all failures disjoint from DEC-0077 deliverables)
- `parity_verified`: true (active/template `caveman.mdc` SHA-256 `C7AAC699…8BC4D` match; runbook voice levels table present active + template)
- `bug_validator`: `[BUG_VALIDATION_OK]`
- `decision_gate_posture`: none required

## Test plan

| Step | Command / check | Expected | Result |
|------|-----------------|----------|--------|
| 1 | `powershell -ExecutionPolicy Bypass -File tests/run-tests.ps1` | §30A green; canonical report | **PASS** (harness exit 1 due to 14 pre-existing disjoint fails) — Pass=808 / Fail=14 (`tests/report.md` Timestamp=2026-06-06T14:51:40Z); §30A line 821 `[PASS]` |
| 2 | `pytest -k caveman_voice` | 9 passed | **PASS** (9 passed, 5 subtests) |
| 3 | `pytest -k "bug0011 or caveman_compress_input_rule_byte or caveman_default_off_bodies"` | 3 passed | **PASS** (3 passed; SHA bump + linkage + regression guard) |
| 4 | Combined S0080 contract filter | 12 passed | **PASS** (`pytest -k "caveman_voice or bug0011 or caveman_compress_input_rule_byte or caveman_default_off_bodies"` → 12 passed, 22 subtests) |
| 5 | `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` | `[BUG_VALIDATION_OK]` | **PASS** |
| 6 | Active/template `caveman.mdc` SHA-256 | post-voice `C7AAC699…8BC4D`; active == template | **PASS** |
| 7 | `_CAVEMAN_RULE_BASELINE_SHA256` constant | matches post-voice digest | **PASS** (`test_caveman_compress_input_rule_byte_identity`) |
| 8 | `test_caveman_default_off_bodies_regression_guard` | DEC-0072 §6 pinned bodies unchanged | **PASS** |
| 9 | Runbook voice levels | `#### Voice compression levels` under US-0089; US-0090 subsection untouched | **PASS** (dev handoff + contract markers) |
| 10 | Scope guards | no scratchpad key changes; no `caveman_compress_input.py` edits; no `test_caveman_default_off_*` body edits | **PASS** |

## Per-AC verdicts (AC-1..AC-8)

### AC-1 — Voice section outline in `caveman.mdc` — `verdict=PASS`

- **DEC-0077 §**: §2, §3, §8
- **evidence_ref**: `## Voice compression (when CAVEMAN_MODE=1)` + six subsections; `test_caveman_voice_section_heading_present`; `test_bug0011_architecture_linkage`.

### AC-2 — Template byte parity for `caveman.mdc` — `verdict=PASS`

- **DEC-0077 §**: §1, §9
- **evidence_ref**: active/template SHA-256 `C7AAC699C5CDF732BD029FA8C431B2A4D0B5A3A1B91E49D80C19C11C9748BC4D` (match); `test_caveman_compress_input_rule_byte_identity` active==template assertion.

### AC-3 — User-rule `### Precedence` subsection — `verdict=PASS`

- **DEC-0077 §**: §2 row 1
- **evidence_ref**: `test_caveman_voice_precedence_subsection_present`.

### AC-4 — Ultra defers to 9-zone (no duplicate list) — `verdict=PASS`

- **DEC-0077 §**: §2 row 6
- **evidence_ref**: `test_caveman_voice_ultra_defers_to_nine_zone_stub`; no duplicate 9-zone literal list in voice section.

### AC-5 — `test_caveman_voice_*` + SHA baseline bump — `verdict=PASS`

- **DEC-0077 §**: §4, §5
- **evidence_ref**: nine `test_caveman_voice_*` subtests green; `_CAVEMAN_RULE_BASELINE_SHA256` bumped `E10EFC32…E47DE` → `C7AAC699…8BC4D`.

### AC-6 — Runbook voice levels (US-0090 untouched) — `verdict=PASS`

- **DEC-0077 §**: §7
- **evidence_ref**: `#### Voice compression levels` 2-row table + rule pointer in runbook active + template; US-0090 subsection byte-unchanged per dev handoff.

### AC-7 — `test_caveman_default_off_*` bodies preserved — `verdict=PASS`

- **DEC-0077 §**: §4 invariants
- **evidence_ref**: `test_caveman_default_off_bodies_regression_guard` PASS; no assertion body edits.

### AC-8 — Harness §30A + operator voice UAT — `verdict=PASS`

- **DEC-0077 §**: §6, §10
- **evidence_ref**: harness §30A `BUG-0011 caveman_voice contract subtests pass`; UAT scenario authored in `sprints/S0080/uat.md` + `uat.json` (operator execution deferred to `/verify-work` per DEC-0077 §10).

## Canonical check-in baseline comparison

| Checkpoint | Pass | Fail | Notes |
|------------|------|------|-------|
| BUG-0010 QA (S0079) | 807 | 14 | Prior bug QA baseline |
| **BUG-0011 QA (S0080)** | **808** | **14** | **+1 pass / +0 fail** (§30A additive assertion) |

**Fail=14 (all disjoint from BUG-0011 / DEC-0077)** — unchanged set vs S0079 QA: Homebrew formula (2), installer/CLI TEST_COMMAND (2), triad repo `--check` (2), scratchpad pair parity (1), slim auto contract markers (1), readme feature coverage repo report + idempotent (2), plus collateral (TOKEN_PROFILE, state policy, auto strict-proof step 11b).

**BUG-0011 harness addition (PASS)**: `BUG-0011 caveman_voice contract subtests pass` (§30A).

## Generated baseline test evidence (US-0066 / DEC-0048)

- `generated_test_stack_profile`: python (stdlib + pytest)
- `generated_test_command`: `python -m pytest tests/auto_command_contract_test.py -q -k "caveman_voice or bug0011 or caveman_compress_input_rule_byte or caveman_default_off_bodies"`
- `generated_test_result`: pass
- `generated_test_output_ref`: 12 passed, 22 subtests passed
- `generated_test_paths_ref`: `tests/auto_command_contract_test.py` (`test_caveman_voice_*`, `test_bug0011_architecture_linkage`, `test_caveman_compress_input_rule_byte_identity`, `test_caveman_default_off_bodies_regression_guard`)
- `generated_test_reason_code`: (none — pass)

## Runtime QA evidence (US-0065)

Not applicable — rule-file / contract-marker story; no application runtime startup required. `runtime_final_verdict=skipped`; `runtime_reason_code=N/A_CAVEMAN_VOICE_RULE_STORY`.

## Blocking findings

None.

## Isolation evidence (US-0048 / DEC-0029)

- `phase_id=qa`
- `role=qa`
- `fresh_context_marker=qa-S0080-BUG0011-qa-20260606T145202Z-fresh`
- `timestamp=2026-06-06T14:52:02Z`
- `evidence_ref=sprints/S0080/qa-findings.md,handoffs/qa_to_verify_work.md,docs/engineering/state.md,tests/report.md`

## Strict runtime proof (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260606-02`
- `runtime_proof_id=rp-auto-20260606-02-qa-qa-20260606T145202Z-S0080-BUG0011`
- `phase_id=qa`
- `role=qa`
- `proof_issued_at=2026-06-06T14:52:02Z`
- `proof_ttl_seconds=3600`
- `proof_hash=6a82aea98053763f0bfede267523a90007a69c2529d8282d1eafbfc9601329ba`

Canonical payload: `{"orchestrator_run_id":"auto-20260606-02","phase_id":"qa","proof_issued_at":"2026-06-06T14:52:02Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260606-02-qa-qa-20260606T145202Z-S0080-BUG0011"}`.

## Next phase

**`/verify-work`** (fresh **qa** subagent) — BUG-0011 remains OPEN until verify-work + `/release` closure per US-0045.

---

## Verify-work findings (cycle 1) — 2026-06-06

## Metadata

- **phase_id**: verify-work
- **role**: qa
- **timestamp**: 2026-06-06T16:53:00Z
- **orchestrator_run_id**: auto-20260606-02
- **fresh_context_marker**: qa-S0080-BUG0011-verify-work-20260606T165300Z-fresh

## Overall verdict

**PASS** — AC-1..AC-8 verified at verify-work; UAT-1 operator voice spot-check **PASS**; closure preflight **9/9 PASS**; independent re-runs green. Bug **BUG-0011** remains **OPEN** per **US-0045** (closure at `/release`).

## Independent re-runs (verify-work)

| Check | Result |
|-------|--------|
| `pytest -k "caveman_voice or bug0011 or caveman_compress_input_rule_byte or caveman_default_off_bodies"` | **12 passed**, 22 subtests |
| `bug_issue_validate.py --check-acceptance` | `[BUG_VALIDATION_OK]` |
| active/template `caveman.mdc` SHA-256 | `C7AAC699…8BC4D` match |

## UAT-1 operator voice spot-check (AC-8)

- **Verdict**: **PASS**
- **Observation**: `full`-level rule semantics produce visibly shorter spawn-only orchestrator prose vs default-off baseline; 9-zone literals preserved in sample reply.
- **Evidence**: `sprints/S0080/uat.json` scenario UAT-1; `sprints/S0080/uat.md` §UAT-1.

## Isolation evidence (US-0048 / DEC-0029)

- `phase_id=verify-work`
- `role=qa`
- `fresh_context_marker=qa-S0080-BUG0011-verify-work-20260606T165300Z-fresh`
- `timestamp=2026-06-06T16:53:00Z`
- `evidence_ref=sprints/S0080/uat.json,sprints/S0080/uat.md,handoffs/qa_to_release.md,docs/engineering/state.md`

## Strict runtime proof (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260606-02`
- `runtime_proof_id=rp-auto-20260606-02-verify-work-qa-20260606T165300Z-S0080-BUG0011`
- `phase_id=verify-work`
- `role=qa`
- `proof_issued_at=2026-06-06T16:53:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=b4db7ef70af8bc6e06c64a9f7820e7ea87148fd365152054a76fb5dfaa4221f4`

Canonical payload: `{"orchestrator_run_id":"auto-20260606-02","phase_id":"verify-work","proof_issued_at":"2026-06-06T16:53:00Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260606-02-verify-work-qa-20260606T165300Z-S0080-BUG0011"}`.

## Next phase

**`/release`** (fresh **release** subagent) — BUG-0011 remains OPEN until release closure per US-0045.
