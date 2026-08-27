# Release Notes — S0126 / US-0126

- **Sprint**: `S0126`
- **Story**: `US-0126` — OpenCode host operator runbook + consolidated cross-host reason-code catalog + `--scope=opencode-adapter` parity (12 contract-test markers)
- **Release date**: `2026-08-25T17:30:00Z` (UTC)
- **orchestrator_run_id**: `auto-20260825-01`
- **delivery_mode**: `ultra_lean`
- **macro_phase**: `ship` (release is phase 1 of 3: release → closure → refresh-context per DEC-0082)
- **policy_mode**: `confirm` (`RELEASE_PUBLISH_MODE=confirm`; `RELEASE_PUBLISH_AUTO_CONFIRM=0` → no publish execution)
- **trigger_source**: `auto`
- **branch**: `local` (no push; `SYNC_POLICY_MODE=disabled` per DEC-0018)
- **fresh_context_marker**: `rel-US0126-release-20260825T173000Z-fresh`
- **model_id**: `glm-5.2-high` (CROSS_MODEL_REVIEW=1 — required)
- **runtime_proof_id**: `rp-auto-20260825-01-release-release-20260825T173000Z-US-0126`
- **proof_hash**: `7070BE1A0FE9386E67DE72AB2ED35FFE307A1355B49151785BDC728A5BFF6EB3`
- **proof_ttl**: `2026-08-25T18:30:00Z` (UTC)
- **release_version**: (none — workflow-only release; no semver bump per S0121..S0125 precedent)

## Verdict

**RELEASE_PASS (1st attempt).** All mandatory release gates (1, 2, 3, 4, 4b) green. Queue row S0126 transitions to `released`. No backlog mutation (closure owns OPEN→DONE + acceptance tick per US-0120 / DEC-0082). No publish (`RELEASE_PUBLISH_MODE=confirm` + `RELEASE_PUBLISH_AUTO_CONFIRM=0` → `PUBLISH_CONFIRMATION_REQUIRED` / deterministic no-op). No sync (`SYNC_POLICY_MODE=disabled` → `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`).

Harness **not re-run** this spawn — accepted `tests/report.md` @ `2026-08-25T17:13:14Z` Pass:845 / Fail:0 with zero `[FAIL]` rows per orchestrator gate-1 brief (post execute loop-2 harness refresh @ 17:10:00Z; no product/test source files modified after the report timestamp per mtime scan in qa loop-2).

## Summary

US-0126 ships the **OpenCode host operator runbook** and closes the operator-documentation + contract-test gap for the OpenCode adapter:

- `## OpenCode host operator runbook (US-0126)` h2 body in `docs/engineering/runbook.md` + byte-identical `template/docs/engineering/runbook.md` mirror — placed immediately after `## OpenCode thin commands + validator bridge (US-0125)`; carries program DoD sentence, default-host reminder, out-of-scope list, and Boundaries subsection (cross-refs to `docs/product/standalone-runtime-masterplan.md`, `DEC-0055`, `US-0093`).
- Consolidated cross-host reason-code table (15 codes) inline within the runbook h2 body: 4 `OPENCODE_*` US-0124 + 5 installer `OPENCODE_*`/`CURSOR_*` US-0121 + 3 reused cross-host + 3 raw Python validator codes; each with one-line semantics + fail-closed action + cross-link; **NO `OPENCODE_VALIDATOR_FAILED` wrapper** (DEC-0125 DQ7 upheld).
- `### OpenCode host operator runbook (US-0126)` blurb in `README.md` + byte-identical `template/README.md` mirror; same blurb in `its_magic/README.md` + byte-identical `template/its_magic/README.md` mirror (default-host reminder + out-of-scope list; operator prose, no DEC ids per US-0071).
- `OPENCODE_ADAPTER_PAIRS` additive extension in `scripts/check_intake_template_parity.py` (+2 new pairs) + byte-identical `template/scripts/check_intake_template_parity.py` mirror; parity CLI stays byte-only (DQ3 layer split).
- `tests/us0126_contract_test.py` (12 markers) + byte-identical `template/tests/us0126_contract_test.py` mirror — one-test-per-AC, AC-5 splits into readme + runbook no-dec-leak; +1 aggregate prior-story marker; all static/grep, no live OpenCode probe (vision D10).
- AC-10 deterministic static check: `.cursor/commands/` (25 `.md`) + `.cursor/agents/` (7 `.mdc`) present vs current-kit-inventory baseline.

Execute loop-2 remediated pre-existing B-1 (7 architecture-linkage harness failures from rollover) — restored `# US-0091` + `# US-0093` H1 blocks before `# US-0089`, appended `# US-0090` H1 after `# US-0089`, reworded 5 task-table refs, added `**US-0125**` row to `docs/developer/README.md` Architecture notes — not US-0126 product scope; harness refreshed to Pass:845 / Fail:0 @ 2026-08-25T17:13:14Z.

Compose guards 8/8 UNCHANGED (additive only): backlog US-0126 OPEN L4368; acceptance unchecked L154; architecture `# US-0126` anchor (L1747); DEC-0126 Accepted; `.cursor/commands/*.md` unchanged; `.cursor/agents/*.mdc` unchanged; `template/.opencode/{agents,plugins,commands}` unchanged; `installer-owned-paths.manifest` unchanged; mirrors byte-identical.

## ACs satisfied (QA loop-2 + verify-work loop-2, static-contract + UAT 12/12)

**10/10 PASS** (live pytest 12/12 green):

| AC | Description | Status |
|----|-------------|--------|
| AC-1 | Runbook "OpenCode host" section present with AC-1 operator phrases | PASS (marker 1 `test_us0126_runbook_section_present`) |
| AC-2 | Consolidated cross-host reason-code catalog present (15 codes; NO `OPENCODE_VALIDATOR_FAILED` wrapper) | PASS (marker 2 `test_us0126_reason_code_catalog_present`) |
| AC-3 | Parity scope `--scope=opencode-adapter` PASS | PASS (markers 3 + 10) |
| AC-4 | Contract tests `test_us0126_*` PASS | PASS (markers 4 + 12) |
| AC-5 | README hygiene no-dec-leak (root + its_magic + runbook) | PASS (markers 5 + 6) |
| AC-6 | Program DoD documented (key phrases) | PASS (marker 7) |
| AC-7 | Default host reminder (runbook + README) | PASS (marker 8) |
| AC-8 | Out-of-scope list (5 excluded items) | PASS (marker 9) |
| AC-9 | Sanitization + template parity (active↔template byte-identical) | PASS (marker 10) |
| AC-10 | Compose — Cursor docs not deleted (25 commands + 7 agents present vs baseline) | PASS (marker 11) |

## Test results (release 1st attempt — harness NOT re-run)

- **Canonical harness** (`tests/report.md`): timestamp `2026-08-25T17:13:14Z`, `Pass: 845 / Fail: 0` (literal zero at L5). Grep `^\- \[FAIL\]` → 0 matches. Accepted as gate-1 evidence (no product/test source mutations after 17:13:14Z per mtime scan).
- **US-0126 live pytest** (release spawn, 2026-08-25T17:29:37Z): `python -m pytest tests/us0126_contract_test.py -q` → **12 passed in 0.14s**.
- **Parity**: `python scripts/check_intake_template_parity.py --scope=opencode-adapter` → `[INTAKE_TEMPLATE_PARITY_OK] scope=opencode-adapter` (exit 0).
- **README feature coverage**: `python scripts/validate_readme_feature_coverage.py --repo . --report` → `status=PASS`, `coverage_missing=[]`, `coverage_present=["US-0121","US-0122","US-0123","US-0124","US-0125"]` (US-0126 absent — OPEN, not in coverage set; validator excludes OPEN stories).
- **Metadata guard**: `python scripts/check-user-visible-metadata.py --repo .` → exit 0 (silent PASS).
- **Runbook byte-identical**: active ↔ template (204996b = 204996b per execute summary).

## Compose guards

**8/8 UNCHANGED** — US-0071 (operator-sentence sanitization), US-0113..US-0117 (operator docs), US-0121/DEC-0120, US-0122/DEC-0122, US-0123, US-0124/DEC-0124, US-0125/DEC-0125 (`OPENCODE_VALIDATOR_FAILED` wrapper NOT resurrected), US-0102/DEC-0087. Release does not mutate backlog/acceptance/architecture/DEC-0126/orchestrator.ts/.cursor/commands/.cursor/agents/installer-owned-paths.manifest.

## Gate summary

| Gate | Result |
|------|--------|
| check_in_tests | **PASS** (`tests/report.md` @ 2026-08-25T17:13:14Z Pass:845 / Fail:0 literal; zero `[FAIL]` rows; metadata guard exit 0; harness not re-run this release spawn) |
| qa | PASS (`sprints/S0126/qa-findings.md` loop-2; 0 blockers; B-1 CLOSED in execute loop-2) |
| verify_work | PASS (`sprints/S0126/uat.json` verify_work loop-2 verdict=PASS; 12/12 ACs; 12/12 contract live) |
| uat | PASS (12/12 ACs; populated; probe `UAT_PROBE_PASS` per-marker) |
| isolation_evidence | PASS (execute loop-2, qa loop-2, verify-work loop-2 in `docs/engineering/state.md`; distinct `fresh_context_marker`; `model_id=glm-5.2-high` set; phase role alignment OK) |
| strict_runtime_proof | **PASS** (verify-work `rp-auto-20260825-01-verify-work-qa-20260825T172435Z-loop2-US-0126` TTL 2026-08-25T18:24:35Z consumed @ release 17:30:00Z; proof_hash `3B111C163B39BEC1F375CD908BCDAC37749D932892A966388AC29E8852075557` independently recomputed and confirmed match; no reuse) |
| readme_feature_coverage_3f | deferred (US-0126 OPEN — not in coverage set; `coverage_missing=[]`; validator excludes OPEN stories) |
| project_readme_3g | skipped (`FRAMEWORK_KIT_REPO=1` per S0114..S0125 precedent) |
| metadata_guard | PASS (`check-user-visible-metadata.py --repo .` exit 0) |
| triad_regression | PASS (post-release `--rollover` exit 0; `--check` exit 0 post-rollover) |
| backlog_reconciliation | not performed (closure owns per US-0120 / DEC-0082) |
| publish | skipped (`RELEASE_PUBLISH_MODE=confirm`; `RELEASE_PUBLISH_AUTO_CONFIRM=0` → `publish_snapshot=skipped_pending_operator_confirm`) |
| sync | not_eligible (`SYNC_POLICY_MODE=disabled` → `reason_code=SYNC_DISABLED`) |
| finalization | **PASS** (queue row S0126 = `released`) |

## Run

```powershell
# US-0126-specific live contract test (12/12 per release spawn 2026-08-25T17:29:37Z):
python -m pytest tests/us0126_contract_test.py -v
#   Expected: 12 passed in ~0.14s

python scripts/check_intake_template_parity.py --scope=opencode-adapter
#   Expected: [INTAKE_TEMPLATE_PARITY_OK] scope=opencode-adapter

python scripts/validate_readme_feature_coverage.py --repo . --report
#   Expected: status=PASS, coverage_missing=[] (US-0126 absent — OPEN)

python scripts/check-user-visible-metadata.py --repo .
#   Expected: exit 0 (silent PASS)

# Consolidated harness (already Pass:845 / Fail:0 @ 2026-08-25T17:13:14Z — re-run only if product/tests change):
powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"
#   Expected: exit 0; tests/report.md Fail: 0; zero [FAIL] rows
```

Start command for the shipped pack (kit/template story — not a long-running service):

```bash
# Install kit with OpenCode host (commands + agents + plugin ship under template/.opencode/):
its-magic --target <repo> --mode missing --host opencode
# Or both hosts:
its-magic --target <repo> --mode missing --host both
# Operators follow the runbook h2 `## OpenCode host operator runbook (US-0126)` in docs/engineering/runbook.md
```

- **start_command**: `its-magic --target <repo> --mode missing --host opencode` (or `--host both`)
- **runtime_mode**: `local`

## Connect

- **runtime_mode**: `local`
- **service_url**: `n/a` (pack/contract story — no service endpoint)
- **service_port**: `n/a`
- **health_endpoint**: `n/a` (health = contract tests + parity CLI + metadata guard, not HTTP)
- **runtime_context_ref**: kit repo — `docs/engineering/runbook.md` `## OpenCode host operator runbook (US-0126)` h2; `template/.opencode/commands/*.md`; `template/.opencode/agents/*.md`; `template/.opencode/plugins/orchestrator.ts`; `tests/us0126_contract_test.py`

## Verify

1. `python -m pytest tests/us0126_contract_test.py -v` → 12 passed (confirmed per release spawn)
2. `python scripts/check_intake_template_parity.py --scope=opencode-adapter` → `[INTAKE_TEMPLATE_PARITY_OK]`
3. `python scripts/validate_readme_feature_coverage.py --repo . --report` → `status:PASS`, `coverage_missing:[]` (US-0126 absent — OPEN)
4. `python scripts/check-user-visible-metadata.py --repo .` → exit 0
5. `tests/report.md` → `Fail: 0` literal at L5; zero `[FAIL]` rows (timestamp ≥ 2026-08-25T17:13:14Z)
6. `docs/engineering/runbook.md` → `## OpenCode host operator runbook (US-0126)` h2 present + byte-identical `template/docs/engineering/runbook.md` mirror
7. `rg "US-0126" .cursor/commands/*.md` → 0 matches expected for operator prose (AC-5 upheld; US-0126 owns runbook h2, not cursor commands)

**expected_health_signal**: all 12 contract markers PASS; opencode-adapter parity OK; harness Fail:0 when last product-changing execute loop-2 completed; metadata guard exit 0; README coverage PASS (US-0126 absent — OPEN, excluded by validator).

## Credentials

- **credential_source_refs**: `n/a` (API keys via OpenCode `/connect`; never in template or git; runbook h2 + README blurb contain no secret references)
- **expected_value_source**: operator places keys in OpenCode auth store; validator CLIs do not log credentials

## Known Issues

None.

## Evidence refs

- `tests/report.md` (@ 2026-08-25T17:13:14Z)
- `sprints/S0126/qa-findings.md` (loop-2 PASS)
- `sprints/S0126/uat.json`, `sprints/S0126/uat.md` (verify-work loop-2 PASS)
- `sprints/S0126/summary.md`
- `sprints/S0126/release-findings.md`
- `docs/engineering/state.md` (execute loop-2 / qa loop-2 / verify-work loop-2 / sovereign-critic / release checkpoints)
- `decisions/DEC-0126.md`

## Next phase

**`/closure`** (fresh **qe** subagent, ship macro phase 2 per DEC-0082) — backlog OPEN→DONE, acceptance tick, `sprints/S0126/closure-verification.md`. Release does NOT spawn closure.
