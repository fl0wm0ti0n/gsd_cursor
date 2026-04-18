# Release Notes — S0075 / US-0089 (Caveman mode)

- **sprint_id**: S0075
- **story_refs**: US-0089
- **release_name**: `S0075 -- US-0089 Cursor Caveman mode`
- **release_date**: 2026-04-18T19:00:00Z
- **orchestrator_run_id**: auto-20260418-01
- **verdict**: **PASS**

## Summary

Ships **Cursor Caveman mode**: a scratchpad-configurable terse response style for
assistant output, default-off, with operator toggle phrases and a strict
non-substitution contract that preserves literal regions and non-suppressible
gate vocabulary.

## What's new

- **Scratchpad controls (AC-1)**: Four new keys in `.cursor/scratchpad.md` and
  `.cursor/scratchpad.local.example.md` (+ template parity):
  `CAVEMAN_MODE=0`, `CAVEMAN_LEVEL=`, `CAVEMAN_COMPRESS_INPUT=0`,
  `CAVEMAN_FILE_SCOPE=`. Default-off invariant guaranteed.
- **Rule contract (AC-3)**: New `.cursor/rules/caveman.mdc` (+ byte-identical
  `template/` copy) defining the scratchpad gate, a 9-zone literal-region
  invariant, non-suppressible AUTO_QUIET gate vocabulary, and five canonical
  operator toggle phrases: `caveman on`, `caveman off`, `stop caveman`,
  `normal mode`, `caveman: lite|full|ultra`.
- **Reference semantics (AC-4)**: `### TOKEN_PROFILE x CAVEMAN_MODE
  non-substitution` subsection added after AUTO_QUIET in
  `docs/engineering/auto-orchestration-reference.md` (+ template parity) —
  clarifies that Caveman does not substitute or re-weight TOKEN_PROFILE /
  US-0080.
- **Operator runbook (AC-5)**: `### Caveman mode (US-0089)` subsection appended
  to `docs/engineering/runbook.md` (+ template parity) with scratchpad key
  table, operator phrase catalog, determinism semantics, and 9-zone literal
  invariant pointer.
- **Default-off invariant tests (AC-2 + AC-6)**: Eight new subtests
  (`test_caveman_default_off_*`) in `tests/auto_command_contract_test.py`
  matching DEC-0072 §6 cardinality: scratchpad keys active + example parity,
  rule file present active+template, reference non-substitution paragraph,
  runbook operator phrases, existing contract tokens intact, gate vocabulary
  preserved, no vendor install leak.
- **Architecture linkage (AC-7)**: Assertion-only
  `test_caveman_architecture_section_bottom_appended_and_linked` verifies
  `# US-0089` heading bottom-appended in `docs/engineering/architecture.md`
  and linked from backlog + decisions.
- **Parity sweep (AC-8)**: `test_caveman_template_parity_sweep` guards the
  four touched active/template pairs; `test_caveman_skill_file_negative_parity`
  forbids any `CAVEMAN_*` / `US-0089` / operator-phrase leakage into
  `.cursor/skills/its-magic/SKILL.md`.

## Non-goals (explicit)

- **No input-side compression**. `CAVEMAN_COMPRESS_INPUT` and
  `CAVEMAN_FILE_SCOPE` remain documented no-ops. Input-side compression is
  deferred to **US-0090**.
- **No TOKEN_PROFILE / US-0080 semantic change** (non-substitution contract).
- **No canonical artifact rewrites** (architecture / decisions are linked, not
  modified).
- **No voice-quality unit tests**, no new runtime dependencies, no
  `npx skills add` token, no edit of `.cursor/skills/its-magic/SKILL.md`.

## Run

- **start_command**: `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"`
- **runtime_mode**: `local`
- **runtime_context_ref**: `docs/engineering/runtime-connectivity.md`

## Connect

- **service_url**: N/A (framework/toolkit repository; no running service)
- **service_port**: N/A
- **health_endpoint**: N/A

## Verify

- **verification_steps**:
  1. Run `python -m pytest tests/auto_command_contract_test.py -k caveman -q` — expect **11 passed**, 19 deselected, 119 subtests passed.
  2. Run `python -m pytest tests/auto_command_contract_test.py -q` — expect **27 passed / 24 failed** (24 pre-existing, disjoint from US-0089).
  3. Run `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` — expect baseline profile Pass=783 / Fail=11 (11 pre-existing disjoint).
  4. Confirm `sprints/S0075/qa-findings.md` cycle 2 is PASS and `sprints/S0075/uat.json` is 8/8.
  5. Confirm release queue row `S0075` is `released` and backlog/acceptance show `US-0089` = DONE / checked.
- **expected_health_signal**: Release artifacts complete; canonical status surfaces show `US-0089` as `DONE`.

## Credentials

- Env-reference-only policy in effect; no inline secrets in artifacts.

## Test evidence summary

- **Caveman suite (targeted)**: 11 passed / 0 failed (119 subtests).
- **Full `auto_command_contract_test.py`**: 27 passed / 24 failed (24
  pre-existing; net +11 passes vs. pre-US-0089 baseline; 0 new failures).
- **Full pytest**: 66 passed / 24 failed / 4 skipped (192 subtests).
- **Canonical `tests/run-tests.ps1`**: Pass=783 / Fail=11 (11 pre-existing,
  disjoint from US-0089 — scoped to `.cursor/commands/auto.md` slim-auto
  drift, remote automation profile keys in scratchpads, active/template auto
  literal parity, scratchpad active/template literal parity; recommended for
  separate triage as follow-on BUG or small story).
- **Bug validator**: `[BUG_VALIDATION_OK]`.

## Governance references

- **DEC-0072** — Cursor Caveman mode (scratchpad-configurable terse responses).
- **`docs/engineering/architecture.md`** section `# US-0089`.
- **`docs/engineering/research.md`** research entry **R-0073**.

## Known limitations / follow-on

- `tests/run-tests.ps1` still reports 11 pre-existing failures outside US-0089
  scope — recommend triage under a new follow-on BUG or housekeeping story.
- Input-side compression (`CAVEMAN_COMPRESS_INPUT` / `CAVEMAN_FILE_SCOPE`)
  remains a documented no-op; tracked under **US-0090**.

## Gate audit snapshot (US-0039)

| gate | verdict | reason_code | evidence_refs |
|------|---------|-------------|---------------|
| check-in_test | pass | - | `sprints/S0075/qa-findings.md` (cycle 2; 783/11 pre-existing disjoint) |
| qa | pass | - | `sprints/S0075/qa-findings.md` (cycle 2) |
| uat | pass | - | `sprints/S0075/uat.json`, `sprints/S0075/uat.md` (8/8) |
| isolation | pass | - | `docs/engineering/state.md` (10 distinct fresh_context_marker) |
| strict_proof | pass | - | `docs/engineering/state.md` (10 distinct runtime_proof_id) |
| scratchpad_pair | pass | - | `sprints/S0075/qa-findings.md` (DEC-0072 §7 sanction) |
| metadata_guard | pass | - | `sprints/S0075/qa-findings.md` |
| bug_validate | pass | - | `[BUG_VALIDATION_OK]` |
| finalization | pass | - | this file, `handoffs/release_queue.md`, `handoffs/release_notes.md`, `sprints/S0075/release-findings.md` |

## Publish status

- **RELEASE_PUBLISH_MODE**: `confirm`
- **publish_snapshot**: `skipped_pending_operator_confirm`
- Operator confirmation is required before any publish target execution. No
  publish scripts were run by the release agent.

## Sync (DEC-0018)

- **SYNC_POLICY_MODE**: `by_phase`
- **ALLOW_AUTO_PUSH**: `1`
- **AUTO_PUSH_BRANCH_ALLOWLIST**: `main`
- **current_branch**: `main`
- **push_decision**: `blocked`
- **reason_code**: `TEST_FAILED` — canonical `tests/run-tests.ps1` non-zero
  (11 pre-existing disjoint failures). No push performed.

## Strict runtime proof

- **orchestrator_run_id**: `auto-20260418-01`
- **runtime_proof_id**: `rp-auto-20260418-01-release-release-20260418T190000Z-S0075-US0089`
- **phase_id**: `release`
- **role**: `release`
- **proof_issued_at**: `2026-04-18T19:00:00Z`
- **proof_ttl_seconds**: `3600`
- **proof_hash**: `2f7351477332235595f379aae04d3830a0efc33f9a9cef887822999bcc9839b3`

## Next

- **`/refresh-context`** (fresh **curator** context) for segment closeout.
