# Release Notes — S0082 / US-0093 (Cursor browser-integrated UAT self-test)

- **sprint_id**: S0082
- **story_refs**: US-0093
- **release_name**: `S0082 — US-0093 Cursor browser-integrated UAT self-test (browser_smoke + automatable manual UI)`
- **release_date**: 2026-06-07T01:30:00Z
- **orchestrator_run_id**: auto-20260606-04
- **verdict**: **PASS**
- **binding_decision**: `DEC-0079` (composes on DEC-0078, US-0065, US-0066)
- **research_anchor**: `R-0079`

## Summary

Ships two-tier browser UAT execution for **`/verify-work`**, **`/qa`**, and **`/execute`**: stdlib **`scripts/uat_probe_lib.py`** classifies steps, completes **`process_health`** / **`cli_smoke`** stubs, and routes **`browser_smoke`** / automatable **`manual_operator`** UI steps via **`UAT_BROWSER_PROBE_MODE=cursor|http_fallback|playwright_fallback`** (default **`cursor`**). Agent commands own Cursor browser MCP primary path; HTTP/Playwright subprocess fallback when MCP unavailable. **`browser_evidence_refs`** schema, new **`UAT_BROWSER_*`** reason codes, verb routing table (judgment-deny precedence), and template parity **`--scope=us-0093`**. Composes on **US-0092** / **DEC-0078** without weakening security deny-list or spawn-only (**BUG-0006**).

## What's new

- **Scratchpad keys (AC-1)** — `UAT_BROWSER_PROBE_MODE`, `UAT_BROWSER_FALLBACK_CHAIN`, `UAT_PROCESS_HEALTH_POLL_*`, `DEV_SERVER_PORT`/`DEV_SERVER_COMMAND`; PERMISSION_MODE + runtime-connectivity interaction docs; active + template + local-example parity.
- **browser_smoke two-tier execution (AC-2)** — `execution_tier=agent|stdlib`; cursor mode returns plan + `UAT_PROBE_UNRESOLVED` until agent completes (no fabricated evidence); HTTP/Playwright fallback wired; lib never calls browser MCP directly.
- **Automatable manual_operator routing (AC-3)** — judgment-deny precedence over UI verbs; automatable UI reclassifies to `browser_smoke` when URL resolves.
- **Stub completion (AC-4)** — `process_health` subprocess + readiness poll; `cli_smoke` exit-code assertion; fail-closed reason-code family.
- **Evidence schema (AC-5)** — `browser_evidence_refs` (navigation_url, screenshots[], console/network summary paths); `--merge-result` rejects PASS without refs in cursor mode.
- **New reason codes (AC-6)** — `UAT_BROWSER_UNAVAILABLE`, `UAT_BROWSER_PROBE_FAILED`, `UAT_BROWSER_PROBE_TIMEOUT`; self-test covers MCP-unavailable + timeout fixtures.
- **Security (AC-7)** — `.env`/credential steps → `UAT_PROBE_FORBIDDEN`; DEC-0078 deny-list unchanged.
- **Operator docs (AC-8)** — runbook + auto-orchestration-reference recipes: mode enablement, CI `http_fallback`, evidence paths, `--merge-result`, `@browser` override.
- **Contract tests (AC-9)** — six `test_us0093_*` subtests green; DEC-0078/spawn-only markers not weakened.
- **Template parity (AC-10)** — `check_intake_template_parity.py --scope=us-0093`; architecture `# US-0093` references DEC-0079.

## Non-goals (explicit)

- No bypass of QA/release/isolation/strict-proof gates (**US-0048**, **US-0056**).
- No replacement of all human UAT judgment; visual-regression pixel-diff out of scope.
- No auto-bypass of browser approval in production-like targets without explicit scratchpad opt-in.
- No vendor MCP guarantees beyond documented Cursor browser surface.

## Run

- **start_command**: `python scripts/uat_probe_lib.py --repo . --step "run pytest contract tests for us0093" --report`
- **runtime_mode**: `local`
- **runtime_context_ref**: `docs/engineering/runtime-connectivity.md`

## Connect

- **service_url**: N/A (framework/toolkit repository; no running service)
- **service_port**: N/A
- **health_endpoint**: N/A

## Verify

1. `python -m pytest tests/auto_command_contract_test.py -q -k us0093`
   → expect 6 passed.
2. `python scripts/uat_probe_lib.py --self-test`
   → expect `[UAT_PROBE_LIB_SELF_TEST_OK]`.
3. `python scripts/check_intake_template_parity.py --repo . --scope=us-0093`
   → expect `[INTAKE_TEMPLATE_PARITY_OK]`.
4. `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance`
   → expect `[BUG_VALIDATION_OK]`.
5. Confirm `sprints/S0082/qa-findings.md` PASS and `sprints/S0082/uat.json` 10/10 PASS.
6. Confirm release-queue row `S0082` is `released` and backlog / acceptance show `US-0093` = DONE / checked.

- **expected_health_signal**: All artifact checks above pass; `US-0093` surfaces as `DONE` in backlog and checked in acceptance.

## Credentials

- Env-reference-only policy in effect. No inline secrets in release artifacts. Browser probes forbid `.env` reads and credential auto-fill.

## Test evidence summary

- **Canonical `tests/run-tests.ps1`**: Pass=**811** / Fail=**14** (`tests/report.md` Timestamp=2026-06-06T22:04:37Z). Fail=14 pre-existing disjoint.
- **Contract subtests**: `pytest -k us0093` 6 passed (release re-run).
- **UAT probe self-test**: `[UAT_PROBE_LIB_SELF_TEST_OK]`.
- **Bug validator**: `[BUG_VALIDATION_OK]` pre- and post-release-write.
- **Parity**: `[INTAKE_TEMPLATE_PARITY_OK]` scope=us-0093.

## Governance references

- **DEC-0079** — two-tier browser UAT, verb routing, evidence schema, reason codes.
- **DEC-0078** — probe catalog + fail-closed vocabulary (extended, not weakened).
- **US-0065** — runtime QA browser guidance (concrete automation path).
- **`docs/engineering/architecture.md`** `# US-0093`.
- **`docs/engineering/research.md`** `R-0079`.

## Known Issues

- None blocking release. Pre-existing harness Fail=14 remains for separate triage.
- Post-S0077 readme feature coverage live `--enforce` drift (BUG-0009/US-0092 gaps, `user_visible` metadata, README parity) — disjoint from US-0093; observation at release gate 3f.

## Release gate summary

| gate | verdict |
|------|---------|
| check-in_test | pass (811/14; us0093 6/6; 14 pre-existing disjoint) |
| qa | pass (cycle 1) |
| uat | pass (10/10) |
| isolation | pass |
| strict_proof | pass |
| readme_feature_coverage_3f | observation (post-S0077 drift; S0077 canonical pass) |
| bug_validate | pass |
| finalization | pass |

## Strict proof (release phase)

- `runtime_proof_id=rp-auto-20260606-04-release-release-20260607T013000Z-S0082-US0093`
- `proof_hash=57e939f5220447bd9a4697146f6a78fb5fbe6d92005eeafcd354e34c8d7c8ab0`
- `fresh_context_marker=release-S0082-US0093-release-20260607T013000Z-fresh`

## Sync / publish

- **Sync**: `SYNC_POLICY_MODE=by_phase`, `ALLOW_AUTO_PUSH=1`, branch `main`; `push_decision=blocked`, `reason_code=TEST_FAILED` (canonical harness Fail=14; disjoint from US-0093).
- **Publish**: `RELEASE_PUBLISH_MODE=confirm` → `skipped_pending_operator_confirm`.

## Next phase

- **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio **0 OPEN** stories.
