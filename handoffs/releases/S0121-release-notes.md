# Release Notes — S0121 / US-0121

- **Sprint**: `S0121`
- **Story**: `US-0121` — OpenCode host-mode adapter (additive `--host cursor|opencode|both` + empty-but-valid `template/.opencode/` pack + parity scope + 14 contract-test markers)
- **Release date**: `2026-08-24T10:58:00Z` (UTC)
- **orchestrator_run_id**: `auto-20260824-01`
- **delivery_mode**: `ultra_lean`
- **macro_phase**: `ship` (release is phase 1 of 3: release → closure → refresh-context per DEC-0082)
- **policy_mode**: `disabled` (`RELEASE_PUBLISH_MODE=disabled`; `RELEASE_PUBLISH_AUTO_CONFIRM=0`)
- **trigger_source**: `auto`
- **branch**: `local` (no push; `SYNC_POLICY_MODE=disabled` per DEC-0018)
- **fresh_context_marker**: `rel-US0121-release-20260824T105800Z-fresh`
- **model_id**: `glm-5.2-high` (CROSS_MODEL_REVIEW=1 — required)
- **runtime_proof_id**: `rp-auto-20260824-01-release-release-20260824T105800Z-US-0121`
- **proof_hash**: `284BA5148FC227A2DA47A0D10DA126F78E8330423C814D66571BA3264335ABBB`
- **proof_ttl**: `2026-08-24T11:58:00Z` (UTC)
- **release_version**: (none — workflow-only release; no semver bump per S0117/S0118 precedent)

## Verdict

**RELEASE_PASS (3rd attempt).** All mandatory release gates (1, 2, 3, 4, 4b) green. Queue row S0121 transitions `unreleased → released`. No backlog mutation (closure owns OPEN→DONE + acceptance tick per US-0120 / DEC-0082). No publish (`RELEASE_PUBLISH_MODE=disabled` → deterministic no-op). No sync (`SYNC_POLICY_MODE=disabled` per DEC-0018 → `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`).

Prior BLOCKED attempts (2026-08-23T12:48:00Z + 2026-08-23T16:35:00Z) are CLOSED by execute loop-3+4 harness remediation (canonical `tests/report.md` Pass:845 / Fail:0 @ 2026-08-24T10:45:36Z) + fresh verify-work (2026-08-24T10:52:00Z) minting new gate-4b proof. This 3rd release attempt consumes fresh verify-work + qa loop-3 proofs (both within their 1-hour TTL relative to this subagent's `now=2026-08-24T10:58:00Z`).

## Summary

US-0121 ships an additive **OpenCode host-mode adapter** for the its-magic installer kit:

- `template/.opencode/` empty-but-valid pack (agents/.gitkeep, commands/.gitkeep, plugins/README.md, .gitignore with Q10 four groups, README.md) — no repo-root `opencode.json`, no active kit `.opencode/` mirror.
- Additive `--host cursor|opencode|both` flag (default `cursor`) on `bin/its-magic.js` (forwards `-InstallHost <value>` to PowerShell to avoid the `$Host` automatic-variable landmine; `--host <value>` to bash), `installer.ps1` (`-InstallHost`), `installer.sh` (`--host`), `installer.py` (`_HostAction` with duplicate + unknown fail-closed `INSTALL_HOST_INVALID`).
- Manifest additions: `[opencode_install_include_paths]` + `[opencode_clean_paths]` (active + template byte-identical, SHA-256 `4AC96FF8…082B5`).
- Parity scope `opencode-adapter` registered in `scripts/check_intake_template_parity.py` (`OPENCODE_ADAPTER_PAIRS` = manifest, parity script, test file; added to `SCOPES[all]`).
- 14 contract-test markers in `tests/us0121_host_mode_test.py` (mirrored byte-identical to `template/tests/us0121_host_mode_test.py`, SHA-256 `F3A60757…6AF83B`).
- Runbook `## OpenCode host mode (US-0121)` h2 (L3870) covering flag, cursor-default lock, install/clean/upgrade host-scoped semantics, orphan/stale diagnostics, and the PS `-InstallHost` landmine note.

Compose guards 5/5 UNCHANGED (additive only): US-0008, DEC-0045, US-0102, US-0001, US-0018.

## ACs satisfied (QA loop-3 + verify-work, live + static-contract)

**10/10 PASS** (live pytest 14/14 green; B-1 CLOSED):

| AC | Description | Status |
|----|-------------|--------|
| AC-1 | template/.opencode tree valid empty pack | PASS (live markers 11+12) |
| AC-2 | --host flag accepted (default cursor; explicit opencode\|both; unknown fail-closed INSTALL_HOST_INVALID) | PASS (live markers 1,5,6,7) |
| AC-3 | install/upgrade/clean host-scoped semantics | PASS (live markers 2,3,4,8,9) |
| AC-4 | cursor coexistence byte-identity | PASS (live markers 2,3,4) |
| AC-5 | manifest + triple-installer parity | PASS (live markers 10,11,14; manifest byte-identity) |
| AC-6 | parity scope opencode-adapter registered | PASS (live marker 13; NB-2 non-blocking) |
| AC-7 | 14 contract-test markers | PASS (live 14/14 in 3.43s; B-1 closed) |
| AC-8 | compose 5/5 UNCHANGED | PASS |
| AC-9 | docs hook minimal (--help + runbook h2) | PASS |
| AC-10 | no secrets in template/.opencode/** | PASS (B-1 CLOSED; rg 0 hits; tightened regex L248; README rephrased) |

## Test results (release re-run, 3rd attempt)

- **Canonical harness** (`tests/report.md`): timestamp `2026-08-24T10:45:36Z`, `Pass: 845 / Fail: 0` (literal zero at L5). Independent re-verification this release subagent: Grep `\[FAIL\]` → 0 matches. US-0071 metadata guard coverage rows present (L712-L717): positive + leak detection + idempotence.
- **US-0121 live pytest** (verify-work run, 2026-08-24T10:52:00Z): `python -m pytest tests/us0121_host_mode_test.py -v` → **14/14 PASSED in 3.43s** (Python 3.12.10 on PATH; pytest 9.1.1).
- **BUG-0011 architecture linkage**: `python -m pytest tests/auto_command_contract_test.py::AutoCommandContractTest::test_bug0011_architecture_linkage -q` → 1 passed, 9 subtests passed.
- **Metadata guard**: `python scripts/check-user-visible-metadata.py --repo .` → exit 0.
- **Triad hot-surface**: `python scripts/enforce-triad-hot-surface.py --check` → exit 0.

## Compose guards

**5/5 UNCHANGED** — US-0008, DEC-0045, US-0102, US-0001, US-0018 verified read-only (release does not mutate installer surfaces).

## Gate summary

| Gate | Result |
|------|--------|
| check_in_tests | **PASS** (`tests/report.md` @ 2026-08-24T10:45:36Z Pass:845 / Fail:0 literal; zero `[FAIL]` rows; US-0071 metadata guard coverage present) |
| qa | PASS (`sprints/S0121/qa-findings.md` loop-3; 0 blockers; B-1 CLOSED; NB-1 CLOSED for env) |
| verify_work | PASS (`sprints/S0121/uat.json` 10/10; `sprints/S0121/uat.md` 10/10 `[x]`; probe `UAT_PROBE_PASS` live 14/14) |
| uat | PASS (10/10 ACs; live pytest 14/14; not placeholder) |
| isolation_evidence | PASS (execute loop-3 + loop-4, qa loop-3, verify-work, sovereign-critic in `docs/engineering/state.md`; all `model_id` set; phase role alignment OK) |
| strict_runtime_proof | **PASS** (verify-work proof TTL 2026-08-24T11:52:00Z > now 10:58:00Z; qa loop-3 proof TTL 2026-08-24T11:46:00Z > now; execute loop-4 proof TTL 2026-08-24T11:37:29Z > now; all proof IDs unique; no reuse) |
| readme_feature_coverage_3f | deferred (kit/installer story; no new README feature coverage entries; canonical harness rows pass) |
| project_readme_3g | skipped (kit repo; `FRAMEWORK_KIT_REPO=1` per S0114..S0118 precedent) |
| backlog_reconciliation | not performed (closure owns that per US-0120) |
| publish | skipped (`RELEASE_PUBLISH_MODE=disabled`) |
| sync | not_eligible (`SYNC_DISABLED`) |
| finalization | **PASS** (queue row S0121 = `released`) |

## Run

```powershell
# US-0121-specific live contract test (already 14/14 per verify-work 2026-08-24T10:52:00Z):
python -m pytest tests/us0121_host_mode_test.py -v
#   Expected: 14 passed in ~3.4s

# Optional (closes NB-2 subprocess gap):
python scripts/check_intake_template_parity.py --scope=opencode-adapter
#   Expected: [INTAKE_TEMPLATE_PARITY_OK] scope=opencode-adapter

# Refresh consolidated test report (already Pass:845 / Fail:0 @ 2026-08-24T10:45:36Z):
powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"
#   Expected: exit 0; tests/report.md Pass:845 / Fail: 0; zero [FAIL] rows
```

Start command for the shipped adapter (kit/installer story — not a service):

```bash
# End-user invocation (cursor-default; additive --host opt-in for OpenCode)
its-magic --target <repo> --mode missing [--host cursor|opencode|both]
its-magic --target <repo> --mode upgrade [--host cursor|opencode|both]
its-magic --clean-repo --target <repo> --yes [--host cursor|opencode|both]
```

## Connect

- **runtime_mode**: `local`
- **service_url**: `n/a` (kit/installer story — no service endpoint; not a web app)
- **service_port**: `n/a`
- **health_endpoint**: `n/a` (health = contract tests, not a fake HTTP)
- **runtime_context_ref**: kit repo — installer + template pack; no external service endpoint

## Verify

1. `python -m pytest tests/us0121_host_mode_test.py -v` → 14 passed (confirmed green per verify-work 2026-08-24T10:52:00Z)
2. `python scripts/check_intake_template_parity.py --scope=opencode-adapter` → `[INTAKE_TEMPLATE_PARITY_OK]`
3. `rg "apiKey|api_key|sk-|MODEL=" template/.opencode` → 0 hits (B-1 closure; defense-in-depth)
4. Confirm `installer.py --help` documents `--host`; `installer.ps1` uses `-InstallHost` (not `-Host`) internally; `installer.sh --help` documents `--host`; `bin/its-magic.js --help` documents `--host <value>` + cursor-default + diagnostics
5. Confirm `docs/engineering/runbook.md` has `## OpenCode host mode (US-0121)` h2 (L3870)
6. Confirm manifest active ↔ template byte-identical (SHA-256 `4AC96FF8…082B5`)
7. Confirm US-0121 remains **OPEN** in `docs/product/backlog.md` until `/closure` runs (after this release PASS)

**expected_health_signal**: 14/14 contract-test markers pass + parity CLI OK + 0 secret-pattern hits + manifest byte-identity preserved. (Health = contract tests, not HTTP.)

## Credentials

Not applicable (kit/installer story; no external secrets). The `template/.opencode/` pack ships no `opencode.json` and no provider credentials; a consumer repo may add its own `opencode.json` with provider credentials and must not commit it (template `.gitignore` enforces `*.local.json{,c}` ignore per US-0102).

## Known Issues

- **NB-1 (non-blocking, environmental — CLOSED for this env)**: live pytest was not run at execute / qa loop-1/loop-2 / verify-work 2026-08-23 / 1st+2nd release attempts due to python not on PATH. Operator installed python 3.12.10 user-scope; verify-work 2026-08-24T10:52:00Z confirmed 14/14 live. NB-1 is CLOSED at the canonical-harness + live-pytest layer.
- **NB-2 (non-blocking)**: AC-6 parity scope is grep-only (marker 13 does not subprocess-invoke the parity CLI; pack files excluded from `OPENCODE_ADAPTER_PAIRS` per Q9 YAGNI). Closes with a future slice or by adding a subprocess invocation in marker 13.
- **NB-3 (non-blocking)**: triple-installer behavioral parity is grep-only (marker 14 enforces source presence, not PS/sh runtime behavior). Deferred to manual QA runbook (US-0126).
- **NB-4 (non-blocking)**: symmetric `CURSOR_*` shrink diagnostics (shrink both → opencode) are grep-only in marker 14 (L300-309); behavioral markers 8-9 cover only the `OPENCODE_*` shrink direction. Would require markers 15-16 (breaks the locked 14-marker budget). Deferred.
- **No blocking issues.** All gates green.

## Isolation evidence (US-0048 / DEC-0029)

- `phase_id=release`
- `role=release`
- `fresh_context_marker=rel-US0121-release-20260824T105800Z-fresh`
- `timestamp=2026-08-24T10:58:00Z`
- `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 — required)
- `evidence_ref=sprints/S0121/release-findings.md` + `handoffs/releases/S0121-release-notes.md` (this file) + `handoffs/release_queue.md` (S0121 row) + `docs/engineering/state.md` (release checkpoint)
- `next_scheduled_phase=/closure` (fresh qe subagent, ship macro — second canonical phase per DEC-0082)
- `stop_condition=STOP after release; do not spawn /closure, /verify-work, /refresh-context, or any critic from this subagent.`

## Strict runtime proof (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260824-01`
- `runtime_proof_id=rp-auto-20260824-01-release-release-20260824T105800Z-US-0121`
- `phase_id=release`
- `role=release`
- `proof_issued_at=2026-08-24T10:58:00Z`
- `proof_hash=284BA5148FC227A2DA47A0D10DA126F78E8330423C814D66571BA3264335ABBB`
- `proof_ttl_seconds=3600`
- `proof_ttl=2026-08-24T11:58:00Z` (UTC)
- Note: proof attests fresh release subagent context (BUG-0006 / US-0048) AND a release PASS attestation (all gates 1–4b green; queue row S0121 → `released`).

## Next

**PASS.** All mandatory release gates green. Queue row S0121 → `released`. No backlog mutation (closure owns that per US-0120 / DEC-0082).

Next canonical phase: **`/closure`** (fresh **qe** subagent, ship macro — second canonical phase per DEC-0082). Closure owns: backlog OPEN→DONE for US-0121, acceptance tick for US-0121 ACs, `sprints/S0121/closure-verification.md`, closure checkpoint in `docs/engineering/state.md`. After closure PASS → `/refresh-context` (fresh curator subagent, ship macro — third canonical phase).
