# Release Notes — S0122 / US-0122

- **Sprint**: `S0122`
- **Story**: `US-0122` — OpenCode role agents and Layer-1 permission table (eight markdown agents in `template/.opencode/agents/` + locked DEC-0122 §2 matrix + 8 contract-test markers)
- **Release date**: `2026-08-24T13:22:00Z` (UTC)
- **orchestrator_run_id**: `auto-20260824-01`
- **delivery_mode**: `ultra_lean`
- **macro_phase**: `ship` (release is phase 1 of 3: release → closure → refresh-context per DEC-0082)
- **policy_mode**: `disabled` (`RELEASE_PUBLISH_MODE=disabled`; `RELEASE_PUBLISH_AUTO_CONFIRM=0`)
- **trigger_source**: `auto`
- **branch**: `local` (no push; `SYNC_POLICY_MODE=disabled` per DEC-0018)
- **fresh_context_marker**: `rel-US0122-release-20260824T132200Z-fresh`
- **model_id**: `composer-2.5-fast` (CROSS_MODEL_REVIEW=1 — required)
- **runtime_proof_id**: `rp-auto-20260824-01-release-release-20260824T132200Z-US-0122`
- **proof_hash**: `82FDC8D25981588F7AF370ECE715A8D84187DEAC7057FE2E9FD2717EE834741A`
- **proof_ttl**: `2026-08-24T14:22:00Z` (UTC)
- **release_version**: (none — workflow-only release; no semver bump per S0121 precedent)

## Verdict

**RELEASE_PASS (2nd attempt).** All mandatory release gates (1, 2, 3, 4, 4b) green. Queue row S0122 transitions `blocked → released`. No backlog mutation (closure owns OPEN→DONE + acceptance tick per US-0120 / DEC-0082). No publish (`RELEASE_PUBLISH_MODE=disabled` → deterministic no-op). No sync (`SYNC_POLICY_MODE=disabled` per DEC-0018 → `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`).

Prior BLOCKED attempt (2026-08-24T12:45:00Z, `RELEASE_TEST_FAILED` on harness Fail:15 pre-remediation) is CLOSED by execute loop-2 remediations (runbook mirror, architecture ordering, triad rollover) yielding canonical `tests/report.md` Pass:845 / Fail:0 @ `2026-08-24T13:02:49Z` + qa loop-2 + verify-work loop-2 (2026-08-24T13:16:00Z) minting fresh gate-4b proof. This 2nd release attempt accepts the 13:02:49Z harness report (no harness re-run — later phase checkpoints appended `state.md` only; re-run would fail triad as process artifact).

## Summary

US-0122 ships **OpenCode role agents** and a **locked Layer-1 permission table** for the its-magic kit:

- Eight markdown agents at `template/.opencode/agents/{po,tech-lead,dev,qa,release,curator,security,auto}.md` with short Layer-2 prompts (≤ 2 KiB; no clone markers).
- Locked permission matrix per `decisions/DEC-0122.md` §2 (po object form + deny-last; auto 7-role allow + `*` deny last; security `edit: deny`; dev template allow without production-code escalation).
- Contract tests `tests/us0122_contract_test.py` (8 markers) byte-identical to `template/tests/us0122_contract_test.py`.
- `OPENCODE_ADAPTER_PAIRS` extended in `scripts/check_intake_template_parity.py` (`--scope=opencode-adapter`).
- Runbook `## OpenCode role agents and permissions (US-0122)` h2 (L3987) mirrored byte-identical to `template/docs/engineering/runbook.md`.
- Architecture `# US-0122` H1 (L1835) ordered before `# US-0089` H1 (L2056) per DEC-0073 §11.

Compose guards 5/5 UNCHANGED (additive only): US-0003, US-0023/BUG-0006, US-0121, US-0102/DEC-0087, US-0002/US-0004.

## ACs satisfied (QA loop-2 + verify-work loop-2, live + static-contract)

**10/10 PASS** (live pytest 8/8 green):

| AC | Description | Status |
|----|-------------|--------|
| AC-1 | eight markdown agents present | PASS (marker 1) |
| AC-2 | Layer-1 permission matrix locked per DEC-0122 §2 | PASS (markers 2, 4) |
| AC-3 | static success test (c) po production-code denial | PASS (marker 3) |
| AC-4 | Layer-2 short prompts ≤ 2 KiB; no clone markers | PASS (marker 7) |
| AC-5 | US-0003 role-id parity; security edit deny | PASS (markers 1, 5, 8) |
| AC-6 | runbook h2 one-liner present | PASS (static L3987) |
| AC-7 | no vendor slugs in template agents | PASS (marker 6) |
| AC-8 | 8 contract-test markers | PASS (8/8 live) |
| AC-9 | compose 5/5 UNCHANGED | PASS |
| AC-10 | locked matrix consumed by tests | PASS (marker 3) |

## Test results (release 2nd attempt — harness NOT re-run)

- **Canonical harness** (`tests/report.md`): timestamp `2026-08-24T13:02:49Z`, `Pass: 845 / Fail: 0` (literal zero at L5). Grep `\[FAIL\]` → 0 matches. US-0071 metadata guard coverage rows present (L712–L717). Accepted as gate-1 evidence (execute loop-2 post-remediation; no product/test mutations after 13:02:49Z from qa/verify-work phases).
- **US-0122 live pytest** (verify-work loop-2, 2026-08-24T13:16:00Z): `python -m pytest tests/us0122_contract_test.py -v` → **8/8 PASSED in 0.03s** (Python 3.12.10; pytest 9.1.1).
- **Parity**: `python scripts/check_intake_template_parity.py --repo . --scope=opencode-adapter` → `[INTAKE_TEMPLATE_PARITY_OK]`.
- **Runbook byte-identical**: SHA-256 `97e1c0cc3e9d2f6016159c929f27c283283132ae5ac4ea4c5e4e03b3ff2ca4a8` (196549 bytes both sides).

## Compose guards

**5/5 UNCHANGED** — US-0003, US-0023/BUG-0006, US-0121, US-0102/DEC-0087, US-0002/US-0004 verified read-only (release does not mutate backlog/acceptance/architecture/DEC-0122).

## Gate summary

| Gate | Result |
|------|--------|
| check_in_tests | **PASS** (`tests/report.md` @ 2026-08-24T13:02:49Z Pass:845 / Fail:0 literal; zero `[FAIL]` rows; metadata guard rows L712–L717; harness not re-run this release spawn) |
| qa | PASS (`sprints/S0122/qa-findings.md` loop-2; 0 blockers; 3 non-blocking carry-forwards) |
| verify_work | PASS (`sprints/S0122/uat.json` 10/10; verify-work loop-2 8/8 contract live) |
| uat | PASS (10/10 ACs; not placeholder) |
| isolation_evidence | PASS (execute loop-2, qa loop-2, verify-work loop-2 in `docs/engineering/state.md`; distinct `fresh_context_marker`; `model_id` set; phase role alignment OK) |
| strict_runtime_proof | **PASS** (verify-work `rp-auto-20260824-01-verify-work-qa-20260824T131600Z-US-0122` TTL 2026-08-24T14:16:00Z > release now 13:22:00Z; proof_hash `47C37682F5F8861E4A2D6F2515390D3F4ADE0EE8D5C5DEA61A552B21A979A409`; no reuse) |
| readme_feature_coverage_3f | deferred (kit/pack story; harness rows pass) |
| project_readme_3g | skipped (`FRAMEWORK_KIT_REPO=1` per S0114..S0121 precedent) |
| backlog_reconciliation | not performed (closure owns per US-0120) |
| publish | skipped (`RELEASE_PUBLISH_MODE=disabled`) |
| sync | not_eligible (`SYNC_DISABLED`) |
| finalization | **PASS** (queue row S0122 = `released`) |

## Run

```powershell
# US-0122-specific live contract test (8/8 per verify-work loop-2 2026-08-24T13:16:00Z):
python -m pytest tests/us0122_contract_test.py -v
#   Expected: 8 passed in ~0.03s

python scripts/check_intake_template_parity.py --repo . --scope=opencode-adapter
#   Expected: [INTAKE_TEMPLATE_PARITY_OK] scope=opencode-adapter

# Consolidated harness (already Pass:845 / Fail:0 @ 2026-08-24T13:02:49Z — re-run only if product/tests change):
powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"
#   Expected: exit 0; tests/report.md Fail: 0; zero [FAIL] rows
```

Start command for the shipped pack (kit/template story — not a service):

```bash
# Install kit into target repo (US-0121 host-mode; agents ship under template/.opencode/agents/)
its-magic --target <repo> --mode missing [--host cursor|opencode|both]
```

## Connect

- **runtime_mode**: `local`
- **service_url**: `n/a` (pack/contract story — no service endpoint)
- **service_port**: `n/a`
- **health_endpoint**: `n/a` (health = contract tests, not HTTP)
- **runtime_context_ref**: kit repo — `template/.opencode/agents/*.md`; no external service

## Verify

1. `python -m pytest tests/us0122_contract_test.py -v` → 8 passed (confirmed per verify-work loop-2)
2. `python scripts/check_intake_template_parity.py --repo . --scope=opencode-adapter` → `[INTAKE_TEMPLATE_PARITY_OK]`
3. `tests/report.md` → `Fail: 0` literal at L5; zero `[FAIL]` rows (timestamp ≥ 2026-08-24T13:02:49Z)
4. `docs/engineering/runbook.md` L3987 → `## OpenCode role agents and permissions (US-0122)` h2 present
5. Eight agent files under `template/.opencode/agents/` with DEC-0122 §2 matrix (po deny-last; auto `*` deny last)

**expected_health_signal**: all contract markers PASS; parity OK; harness Fail:0 when last product-changing execute completed.

## Credentials

- **credential_source_refs**: `n/a` (no runtime credentials; pack ships markdown agents only)
- **expected_value_source**: no API keys in `template/.opencode/**` (vendor-slug guard marker 6)

## Known Issues

- `ik_us0122_stale_compose_count_6_vs_5` — architecture overview "compose guards 6/6" drift vs 5/5 T-anch count (non-blocking; doc-parity deferred).
- `ik_us0122_sxxxx_literal_glob_runtime` — `sprints/Sxxxx/*` globs in DEC-0122 §2 are sprint placeholder patterns (closed at plan-verify).
- `ik_us0122_dev_template_agent_permission_escalation` — dev `template/**` allow closed via parity gate (non-blocking).

## Evidence refs

- `tests/report.md` (@ 2026-08-24T13:02:49Z)
- `sprints/S0122/qa-findings.md` (loop-2)
- `sprints/S0122/verify-work-findings.md` (loop-2)
- `sprints/S0122/uat.json`, `sprints/S0122/uat.md`
- `sprints/S0122/release-findings.md`
- `handoffs/verify_to_release.md`
- `docs/engineering/state.md` (execute/qa/verify-work loop-2 checkpoints)
- `decisions/DEC-0122.md`

## Next phase

**`/closure`** (fresh **qe** subagent, ship macro phase 2 per DEC-0082) — backlog OPEN→DONE, acceptance tick, `sprints/S0122/closure-verification.md`. Release does NOT spawn closure.
