# Sprint S0121 — UAT (US-0121, code story) — verify-work populated/verified (LIVE)

**sprint_id**: S0121
**story_refs**: US-0121
**phase**: verify-work (qa, fresh subagent per BUG-0006)
**role**: qa
**orchestrator_run_id**: auto-20260824-01
**delivery_mode**: ultra_lean
**story_type**: code
**fresh_context_marker**: `qa-US0121-verify-work-20260824T105200Z-fresh`
**timestamp**: 2026-08-24T10:52:00Z (UTC)
**model_id**: glm-5.2-high (CROSS_MODEL_REVIEW=1 — required)
**verdict**: **PASS** (10/10 ACs pass; 14/14 contract-test markers PASSED live; B-1 closed; 0 blocking findings)
**total_steps**: 10 | **passed**: 10 | **failed**: 0
**probe_results**: 1 (cli_smoke pytest — **UAT_PROBE_PASS**, 14/14 live; NB-1 CLOSED for this env)

## Live re-verification evidence (this verify-work run — no rubber-stamp)

- **Live pytest**: `python -m pytest tests/us0121_host_mode_test.py -v` → **14/14 PASSED in 3.43s** (Python 3.12.10 on PATH; pytest 9.1.1; collected 14 items).
- **Canonical harness report**: `tests/report.md` @ 2026-08-24T10:45:36Z → `Pass: 845` / `Fail: 0` (literal zero); zero `[FAIL]` rows (Grep-verified this run).
- **Manifest byte-identity**: active ↔ template SHA-256 = `4AC96FF8A3B9EA2B025A93D787526B0E6343B662BA78BB0C8A72B186697082B5`.
- **Parity script byte-identity**: active ↔ template SHA-256 = `E479211A556543C91972D1E9417A4F31058791A0DA03A9EDE26A67507458B647`.
- **Test pair byte-identity**: active ↔ template SHA-256 = `F3A6075783B87851C6529B0AC8C788449E43E815AE2EEA0511157A55AD6AF83B`.
- **No-secrets re-check**: Grep `apiKey|api_key|sk-|MODEL=` on `template/.opencode` → 0 hits (independently re-verified this run via Grep tool).
- **Prior verify-work proof**: STALE (ttl 2026-08-23T13:00:00Z) — NOT reused. New proof minted this run.

## Acceptance criteria (10) — results

- [x] **AC-1**: `template/.opencode/` tree — valid pack with `agents/`, `commands/`, `plugins/` + gitignore. Empty-but-valid. — **PASS** (UAT-1; Glob 5 files; no repo-root opencode.json; no active mirror)
- [x] **AC-2**: `--host` flag — installer accepts `--host cursor|opencode|both`. Default = `cursor`. Unknown -> `INSTALL_HOST_INVALID`. — **PASS** (UAT-2; live markers 1,5,6,7 PASSED; installer.py L21-34 _HostAction)
- [x] **AC-3**: Install / upgrade / clean — host-scoped; `.cursor/` untouched when `--host opencode`. — **PASS** (UAT-3; live markers 2,3,4,8,9 PASSED; build_effective_* / emit_host_shrink_diagnostics)
- [x] **AC-4**: Cursor coexistence — `--host cursor` byte-identical on `.cursor/` vs pre-US-0121. `--host both` leaves both trees. — **PASS** (UAT-4; live markers 2,3,4 PASSED; host_gates_cursor_row predicate)
- [x] **AC-5**: Manifest + triple-installer — manifest lists `template/.opencode/**`; PS/Bash/Python honor `--host` with same semantics. — **PASS** (UAT-5; live markers 10,11,14 PASSED; manifest byte-identity SHA-256 4AC96FF8...082B5)
- [x] **AC-6**: Parity — `check_intake_template_parity.py --scope=opencode-adapter` fails on drift. — **PASS** (UAT-6; live marker 13 PASSED; parity script byte-identity SHA-256 E479211A...58B647)
- [x] **AC-7**: Contract tests — `test_us0121_*` cover default, each `--host`, upgrade/clean, coexistence, invalid, manifest. — **PASS** (UAT-7; **live pytest 14/14 PASSED**; test pair byte-identity SHA-256 F3A60757...6AF83B; B-1 closed)
- [x] **AC-8**: Compose, do not amend — US-0008 / DEC-0045 / US-0102 / US-0001 / US-0018 unchanged except additive host switch. — **PASS** (UAT-8; compose guards 5/5 UNCHANGED)
- [x] **AC-9**: Docs hook (minimal) — `--help` / runbook mention `--host` + cursor-default lock. — **PASS** (UAT-9; --help docs in JS/PS/sh/py + runbook h2; marker 14 live PASSED)
- [x] **AC-10**: No secrets in template — no API keys, `.env` contents, vendor slugs (US-0102). — **PASS** (UAT-10; **live marker 12 PASSED**; Grep 0 hits independently re-verified; B-1 CLOSED)

## Contract test markers (14) — LIVE status

`python -m pytest tests/us0121_host_mode_test.py -v` — **14/14 PASSED in 3.43s** (Python 3.12.10 on PATH; pytest 9.1.1).

1. `test_us0121_default_host_cursor_when_omitted` (AC-2) — **LIVE PASS**
2. `test_us0121_host_cursor_installs_cursor_and_kernel_no_opencode` (AC-2, AC-3, AC-4) — **LIVE PASS**
3. `test_us0121_host_opencode_skips_cursor_installs_opencode_and_kernel` (AC-2, AC-3, AC-4) — **LIVE PASS**
4. `test_us0121_host_both_installs_both_trees` (AC-2, AC-3, AC-4) — **LIVE PASS**
5. `test_us0121_invalid_host_fails_closed_install_host_invalid` (AC-2) — **LIVE PASS**
6. `test_us0121_host_normalize_case_and_whitespace` (AC-2) — **LIVE PASS**
7. `test_us0121_duplicate_host_argv_fails_closed` (AC-2) — **LIVE PASS**
8. `test_us0121_clean_host_cursor_after_both_emits_orphan_diagnostic` (AC-3, AC-7) — **LIVE PASS**
9. `test_us0121_upgrade_host_cursor_after_both_emits_stale_diagnostic` (AC-3, AC-7) — **LIVE PASS**
10. `test_us0121_mixed_section_cursor_skip_when_host_opencode` (AC-5, AC-7) — **LIVE PASS**
11. `test_us0121_manifest_lists_opencode_pack` (AC-5) — **LIVE PASS**
12. `test_us0121_no_secrets_in_pack` (AC-10) — **LIVE PASS** (B-1 CLOSED: regex assignment-like; Grep 0 hits)
13. `test_us0121_parity_scope_opencode_adapter_registered` (AC-6) — **LIVE PASS**
14. `test_us0121_triple_installer_host_parity` (AC-5, AC-9) — **LIVE PASS**

## UAT step results

| Step | AC | Result | Evidence |
|------|----|--------|---------|
| UAT-1 | AC-1 | pass | Glob template/.opencode/** -> 5 files (agents/.gitkeep, commands/.gitkeep, plugins/README.md, .gitignore, README.md); no repo-root opencode.json; no active mirror |
| UAT-2 | AC-2 | pass | Live markers 1,5,6,7 PASSED; --host parser in installer.py/sh/ps + bin/its-magic.js; default cursor; INSTALL_HOST_INVALID fail-closed |
| UAT-3 | AC-3 | pass | Live markers 2,3,4,8,9 PASSED; build_effective_* / emit_host_shrink_diagnostics; host-scoped install/upgrade/clean |
| UAT-4 | AC-4 | pass | Live markers 2,3,4 PASSED; host_gates_cursor_row predicate gates .cursor/ rows; --host cursor excludes .opencode/ rows |
| UAT-5 | AC-5 | pass | Live markers 10,11,14 PASSED; manifest byte-identity SHA-256 4AC96FF8...082B5 (both copies) |
| UAT-6 | AC-6 | pass | Live marker 13 PASSED; opencode-adapter scope registered (L484-497, L521, L543); parity script byte-identity SHA-256 E479211A...58B647 |
| UAT-7 | AC-7 | pass | **Live pytest 14/14 PASSED in 3.43s**; test pair byte-identity SHA-256 F3A60757...6AF83B; B-1 closed |
| UAT-8 | AC-8 | pass | Compose guards 5/5 UNCHANGED (US-0008, DEC-0045, US-0102, US-0001, US-0018) |
| UAT-9 | AC-9 | pass | --help docs in JS/PS/sh/py + runbook ## OpenCode host mode (US-0121) h2; marker 14 live PASSED |
| UAT-10 | AC-10 | pass | **Live marker 12 PASSED**; Grep 0 hits independently re-verified; B-1 CLOSED; tightened regex L248; README rephrased |

## Probe results

| probe_id | type | command | passed | reason_code | ac_mapping |
|----------|------|---------|--------|-------------|------------|
| probe-01-pytest-cli-smoke | cli_smoke | `python -m pytest tests/us0121_host_mode_test.py -v` | **true** | **UAT_PROBE_PASS** | AC-7 |

**Probe notes**: Python 3.12.10 now on PATH. Live pytest executed this verify-work run: 14/14 PASSED in 3.43s. NB-1 CLOSED for this environment. Prior verify-work probe (UAT_PROBE_UNRESOLVED python_not_on_path) superseded honestly — passed=true reflects green live run.

## Canonical harness evidence

- `tests/report.md` @ 2026-08-24T10:45:36Z → `Pass: 845` / `Fail: 0` (literal zero at L5).
- Zero `[FAIL]` rows (Grep-verified this run).
- Harness command: `powershell -ExecutionPolicy Bypass -File tests/run-tests.ps1` → exit 0.

## Non-blocking findings (carried forward; do not block release)

- **NB-1**: CLOSED for this environment (Python 3.12.10 on PATH; live pytest 14/14 green).
- **NB-2**: AC-6 parity scope is grep-only at static layer (marker 13 live-passed but does not subprocess-invoke the parity CLI on a drifted clone; pack files excluded from OPENCODE_ADAPTER_PAIRS). issue_key=ik_us0121_ac6_parity_scope_pack_gap.
- **NB-3**: triple-installer behavioral parity is grep-only at static layer (marker 14). issue_key=ik_us0121_py_only_behavioral_triple_grep.
- **NB-4**: symmetric CURSOR_* shrink diagnostics grep-only (markers 8-9 cover opencode-shrink only; CURSOR_* shrink-to-opencode is grep-only in marker 14).

## Results summary (mapping to ACs)

- **Overall verdict**: **PASS** — 10/10 ACs pass; 14/14 contract-test markers PASSED live; B-1 closed; 0 blocking findings; 0 new product defects.
- **AC-1..AC-10**: all PASS (see table above).
- **B-1 status**: CLOSED (Option C — regex tightened + README rephrased; independently re-verified this verify-work run via Grep → 0 hits; live marker 12 PASSED).
- **Compose guards**: 5/5 UNCHANGED (additive only).
- **Manifest + parity script + test pair byte-identity**: all PARITY_OK (SHA-256 verified this run).
- **Live pytest**: 14/14 PASSED in 3.43s (NB-1 CLOSED for this env).
- **Canonical harness**: Pass:845 / Fail:0 literal; zero [FAIL] rows.
- **Decision gate**: false (no new blocking product defect).
- **Next scheduled phase**: `/release`.
- **Stop condition**: STOP after verify-work; do not spawn `/release` from this QA subagent (BUG-0006). Orchestrator reroutes.

## Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

- `phase_id=verify-work`
- `role=qa`
- `fresh_context_marker=qa-US0121-verify-work-20260824T105200Z-fresh`
- `timestamp=2026-08-24T10:52:00Z`
- `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 — required)
- `evidence_ref=sprints/S0121/uat.json + sprints/S0121/uat.md`
- `next_scheduled_phase=/release`
- `stop_condition=STOP after verify-work; do not spawn /release.`
- QA subagent spawned fresh per BUG-0006 / US-0048 isolation; context limited to verify-work inputs (handoffs/qa_to_verify.md loop-3 PASS, docs/product/acceptance.md US-0121 row, sprints/S0121/uat.json prior placeholder, sprints/S0121/summary.md). No prior chat history carried over.
- Prior verify-work strict proof (STALE): `rp-auto-20260823-01-verify-work-qa-20260823T120000Z-US-0121` (proof_hash=75481ECEAAB2113FB38A61403DB4FC3C342617ECEE9416DD4502B9A834CFD1A2; ttl 2026-08-23T13:00:00Z). NOT reused — expired.
- Prior qa loop-3 strict proof consumed: `rp-auto-20260824-01-qa-qa-loop3-20260824T104600Z-US-0121` (proof_hash=9BF670357BA9AD30AB20EEDEFFECC6A2F3E1700EE1539E6F3F7E600FB7A0DF58). Not reused.

## Strict runtime proof (US-0056 / DEC-0038)

- `runtime_proof_id=rp-auto-20260824-01-verify-work-qa-20260824T105200Z-US-0121` (NEW; not reused)
- `orchestrator_run_id=auto-20260824-01`
- `phase_id=verify-work`, `role=qa`, `story_id=US-0121`, `sprint_id=S0121`
- `delivery_mode=ultra_lean`, `macro_phase=build+verify`
- `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 — required)
- `proof_issued_at=2026-08-24T10:52:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=5DF2AB193AA53A4163418A6808B111CED877195295326ADA326FA0759EA4127D` (SHA-256 of sorted-key JSON payload)
- Canonical payload (sorted-key JSON per DEC-0038): `{"delivery_mode":"ultra_lean","macro_phase":"build+verify","model_id":"glm-5.2-high","orchestrator_run_id":"auto-20260824-01","phase_id":"verify-work","proof_issued_at":"2026-08-24T10:52:00Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260824-01-verify-work-qa-20260824T105200Z-US-0121","sprint_id":"S0121","story_id":"US-0121"}`
- `proof_ttl=2026-08-24T11:52:00Z` (1-hour TTL)

## Stop condition

STOP after verify-work. Do not spawn `/release` from this QA subagent (BUG-0006). Hand off via artifacts only: `sprints/S0121/uat.json` + `sprints/S0121/uat.md` + `docs/engineering/state.md` (verify-work checkpoint + traceability update) + `handoffs/verify_to_release.md` + `handoffs/resume_brief.md` (prepend). The orchestrator reroutes to `/release` in a fresh subagent.
