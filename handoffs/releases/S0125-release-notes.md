# Release Notes — S0125 / US-0125

- **Sprint**: `S0125`
- **Story**: `US-0125` — OpenCode thin dispatch-only commands + validator bridge (15 command files ≤20 lines; Python CLI SOT; plugin subprocess fail-closed)
- **Release date**: `2026-08-24T21:33:00Z` (UTC)
- **orchestrator_run_id**: `auto-20260824-02`
- **delivery_mode**: `ultra_lean`
- **macro_phase**: `ship` (release is phase 1 of 3: release → closure → refresh-context per DEC-0082)
- **policy_mode**: `confirm` (`RELEASE_PUBLISH_MODE=confirm`; `RELEASE_PUBLISH_AUTO_CONFIRM=0` → no publish execution)
- **trigger_source**: `auto`
- **branch**: `local` (no push; `SYNC_POLICY_MODE=disabled` per DEC-0018)
- **fresh_context_marker**: `rel-US0125-release-20260824T213300Z-fresh`
- **model_id**: `composer-2.5-fast` (CROSS_MODEL_REVIEW=1 — required)
- **runtime_proof_id**: `rp-auto-20260824-02-release-release-20260824T213300Z-US-0125`
- **proof_hash**: `CB1BB92BB263BEA244C382A4A7B3662BB45A00EBD4B41ECC4E8ADB5F26A5E2CC`
- **proof_ttl**: `2026-08-24T22:33:00Z` (UTC)
- **release_version**: (none — workflow-only release; no semver bump per S0121/S0122/S0123/S0124 precedent)

## Verdict

**RELEASE_PASS (1st attempt).** All mandatory release gates (1, 2, 3, 4, 4b) green. Queue row S0125 transitions to `released`. No backlog mutation (closure owns OPEN→DONE + acceptance tick per US-0120 / DEC-0082). No publish (`RELEASE_PUBLISH_MODE=confirm` + `RELEASE_PUBLISH_AUTO_CONFIRM=0` → `PUBLISH_CONFIRMATION_REQUIRED` / deterministic no-op). No sync (`SYNC_POLICY_MODE=disabled` → `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`).

Harness **not re-run** this spawn — accepted `tests/report.md` @ `2026-08-24T21:04:51Z` Pass:845 / Fail:0 per orchestrator gate-1 brief (post execute loop-2 harness refresh; later QA/verify-work/release checkpoints appended `state.md` only as triad oversize process artifact).

## Summary

US-0125 ships **15 dispatch-only OpenCode command files** under `template/.opencode/commands/`:

- Each command ≤20 lines; role-bound frontmatter; STOP after artifact list; no 200-line Cursor clones (clone guard ≤0.30 similarity via `US0125_CLONE_GUARD_STRIP_TOKENS`).
- `/auto`: `agent: auto` + `subtask: false`; dispatch-only — plugin US-0124 remains spawn owner.
- `/closure`: `agent: qa` with prompt `role=qe` (no `qe.md` agent).
- `/ask`: omits `agent`; no `model:` in any command.
- Validator bridge: named CLIs (`intake_evidence_validate.py`, `bug_issue_validate.py`) + generic bridge contract; raw Python reason codes; `OPENCODE_DRIVER_INVOKE_FAILED` only for subprocess throw.
- Contract tests `tests/us0125_contract_test.py` (11 markers) byte-identical to `template/tests/us0125_contract_test.py`.
- Node harness `tests/us0125/bridge_harness.mjs` + `tests/us0125/mock_subprocess.ts` (no live OpenCode runtime per AC-10).
- Runbook stub `## OpenCode thin commands + validator bridge (US-0125)` h2; byte-identical `template/docs/engineering/runbook.md` mirror.
- `OPENCODE_ADAPTER_PAIRS` extended in `scripts/check_intake_template_parity.py` (`--scope=opencode-adapter`).

Execute loop-2 remediated pre-existing B-1 (architecture.md `# US-0090` missing `US-0085` linkage) and B-2 (US-0124 README feature-coverage gap) — not US-0125 product scope; harness refreshed to Pass:845 / Fail:0.

Compose guards 7/7 UNCHANGED (additive only): backlog US-0125 OPEN; acceptance unchecked; architecture `# US-0125` anchor; DEC-0125 Accepted; `.cursor/commands/*.md` unchanged; orchestrator.ts unchanged; mirrors byte-identical.

## ACs satisfied (QA loop-2 + verify-work, live + static-contract)

**10/10 PASS** (live pytest 11/11 green):

| AC | Description | Status |
|----|-------------|--------|
| AC-1 | Dispatch-only command inventory + `/auto` | PASS (markers 1, 8, 11) |
| AC-2 | Clone guard ≤20 lines + ≤0.30 similarity | PASS (marker 2) |
| AC-3 | Validator Python CLI SOT + subprocess fail-closed | PASS (marker 3) |
| AC-4 | Success test (b) — release blocked after failing validator | PASS (marker 4) |
| AC-5 | Raw Python reason codes; no wrapper | PASS (marker 5) |
| AC-6 | No policy text in command files | PASS (marker 6) |
| AC-7 | Missing optional command must not disable plugin | PASS (markers 7, 8) |
| AC-8 | Contract tests cover required surfaces | PASS (marker 11 + 11/11 live) |
| AC-9 | Cursor commands unchanged | PASS (marker 9) |
| AC-10 | No new npm runtime | PASS (marker 10) |

## Test results (release 1st attempt — harness NOT re-run)

- **Canonical harness** (`tests/report.md`): timestamp `2026-08-24T21:04:51Z`, `Pass: 845 / Fail: 0` (literal zero at L5). Grep `\[FAIL\]` → 0 matches. Metadata guard coverage rows present (L712–L717). Accepted as gate-1 evidence (execute loop-2 harness refresh; no product/test mutations after 21:04:51Z from qa/verify-work/release phases).
- **US-0125 live pytest** (verify-work, 2026-08-24T22:35:00Z): `python -m pytest tests/us0125_contract_test.py -v` → **11/11 PASSED in 0.45s**.
- **Parity**: `python scripts/check_intake_template_parity.py --repo . --scope=opencode-adapter` → `[INTAKE_TEMPLATE_PARITY_OK]`.
- **README feature coverage**: `validate_readme_feature_coverage --report` → PASS `coverage_missing=[]` (US-0125 absent — OPEN, not in coverage set).
- **Runbook byte-identical**: active ↔ template (per execute summary).

## Compose guards

**7/7 UNCHANGED** — US-0001, US-0078/DEC-0060, US-0121/DEC-0120, US-0122/DEC-0122, US-0124/DEC-0124, US-0126, US-0102/DEC-0087 (release does not mutate backlog/acceptance/architecture/DEC-0125/orchestrator.ts/.cursor/commands).

## Gate summary

| Gate | Result |
|------|--------|
| check_in_tests | **PASS** (`tests/report.md` @ 2026-08-24T21:04:51Z Pass:845 / Fail:0 literal; zero `[FAIL]` rows; metadata guard L712–L717; harness not re-run this release spawn) |
| qa | PASS (`sprints/S0125/qa-findings.md` loop-2; 0 blockers; B-1 + B-2 closed) |
| verify_work | PASS (`sprints/S0125/uat.json` 11/11; verify-work 11/11 contract live) |
| uat | PASS (11/11 ACs; populated; not placeholder) |
| isolation_evidence | PASS (execute loop-2, qa loop-2, verify-work in `docs/engineering/state.md`; distinct `fresh_context_marker`; `model_id` set; phase role alignment OK) |
| strict_runtime_proof | **PASS** (verify-work `rp-auto-20260824-02-verify-work-qa-20260824T223500Z-US-0125` TTL 2026-08-24T23:35:00Z consumed @ release 21:33:00Z; proof_hash `7278CD174376E4AC82670406BE664DF181D7471F09174DC619B6DC84478F0312`; no reuse) |
| readme_feature_coverage_3f | deferred (US-0125 OPEN — not in coverage set; `coverage_missing=[]`) |
| project_readme_3g | skipped (`FRAMEWORK_KIT_REPO=1` per S0114..S0124 precedent) |
| metadata_guard | PASS (`check-user-visible-metadata.py --repo .` exit 0) |
| triad_regression | PASS (`enforce-triad-hot-surface.py --check` exit 0; `--rollover` exit 0 post-release) |
| backlog_reconciliation | not performed (closure owns per US-0120) |
| publish | skipped (`RELEASE_PUBLISH_MODE=confirm`; `RELEASE_PUBLISH_AUTO_CONFIRM=0` → `publish_snapshot=skipped_pending_operator_confirm`) |
| sync | not_eligible (`SYNC_DISABLED`) |
| finalization | **PASS** (queue row S0125 = `released`) |

## Run

```powershell
# US-0125-specific live contract test (11/11 per verify-work 2026-08-24T22:35:00Z):
python -m pytest tests/us0125_contract_test.py -v
#   Expected: 11 passed in ~0.45s

python scripts/check_intake_template_parity.py --repo . --scope=opencode-adapter
#   Expected: [INTAKE_TEMPLATE_PARITY_OK] scope=opencode-adapter

# Node bridge harness smoke (marker 3/4 scenarios):
node --experimental-strip-types tests/us0125/bridge_harness.mjs release-blocked-nonzero
#   Expected: allowed=false reasonCode=INTAKE_PERSISTENCE_BLOCKED

# Consolidated harness (already Pass:845 / Fail:0 @ 2026-08-24T21:04:51Z — re-run only if product/tests change):
powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"
#   Expected: exit 0; tests/report.md Fail: 0; zero [FAIL] rows
```

Start command for the shipped pack (kit/template story — not a long-running service):

```bash
# Install kit with OpenCode host (commands ship under template/.opencode/commands/):
its-magic --target <repo> --mode missing --host opencode
# Or both hosts:
its-magic --target <repo> --mode missing --host both
# Commands compose with template/.opencode/agents/*.md and plugin orchestrator.ts (US-0124)
```

- **start_command**: `its-magic --target <repo> --mode missing --host opencode` (or `--host both`)
- **runtime_mode**: `local`

## Connect

- **runtime_mode**: `local`
- **service_url**: `n/a` (pack/contract story — no service endpoint)
- **service_port**: `n/a`
- **health_endpoint**: `n/a` (health = contract tests + Node harness, not HTTP)
- **runtime_context_ref**: kit repo — `template/.opencode/commands/*.md`; `template/.opencode/plugins/orchestrator.ts`; bridge harness `tests/us0125/bridge_harness.mjs`

## Verify

1. `python -m pytest tests/us0125_contract_test.py -v` → 11 passed (confirmed per verify-work)
2. `python scripts/check_intake_template_parity.py --repo . --scope=opencode-adapter` → `[INTAKE_TEMPLATE_PARITY_OK]`
3. `python scripts/validate_readme_feature_coverage.py --repo . --report` → `status:PASS`, `coverage_missing:[]` (US-0125 absent — OPEN)
4. `tests/report.md` → `Fail: 0` literal at L5; zero `[FAIL]` rows (timestamp ≥ 2026-08-24T21:04:51Z)
5. `docs/engineering/runbook.md` → `## OpenCode thin commands + validator bridge (US-0125)` h2 present + byte-identical mirror
6. `rg "US-0125" .cursor/commands/*.md` → 0 matches (AC-9 upheld)

**expected_health_signal**: all 11 contract markers PASS; opencode-adapter parity OK; harness Fail:0 when last product-changing execute loop-2 completed; dispatch-only commands with raw Python validator reason codes.

## Credentials

- **credential_source_refs**: `n/a` (API keys via OpenCode `/connect`; never in template or git; command files contain no secret references)
- **expected_value_source**: operator places keys in OpenCode auth store; validator CLIs do not log credentials

## Known Issues

None.

## Evidence refs

- `tests/report.md` (@ 2026-08-24T21:04:51Z)
- `sprints/S0125/qa-findings.md` (loop-2 PASS)
- `sprints/S0125/uat.json`, `sprints/S0125/uat.md`
- `sprints/S0125/summary.md`
- `sprints/S0125/release-findings.md`
- `docs/engineering/state.md` (execute loop-2 / qa loop-2 / verify-work / release checkpoints)
- `decisions/DEC-0125.md`

## Next phase

**`/closure`** (fresh **qe** subagent, ship macro phase 2 per DEC-0082) — backlog OPEN→DONE, acceptance tick, `sprints/S0125/closure-verification.md`. Release does NOT spawn closure.
