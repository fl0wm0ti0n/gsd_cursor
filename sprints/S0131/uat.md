# Sprint S0131 — UAT (BUG-0015) — populated at /verify-work (DEC-0009)

- **uat_lifecycle**: populated (verify-work PASS; DEC-0009 placeholder → populated complete)
- **sprint_id**: S0131
- **bug_refs**: BUG-0015
- **phase**: verify-work (build+verify macro)
- **role**: qa (fresh per BUG-0006)
- **orchestrator_run_id**: auto-20260906-bug0015
- **delivery_mode**: ultra_lean
- **macro_phase**: build+verify
- **story_type**: code (OpenCode plugin attach + lifecycle + contract-test slice; FRAMEWORK_KIT_REPO=1)
- **fresh_context_marker**: `qa-BUG0015-verify-work-20260906T150500Z-fresh`
- **timestamp**: 2026-09-06T15:05:00Z (UTC)
- **model_id**: composer-2.5 (CROSS_MODEL_REVIEW=1 — required)
- **producer_phase_id**: qa (role=qa; **QA_PASS**; `blocking_count=0`)
- **critic_phase_id**: sovereign-critic of qa (tech-lead, composer-2.5-fast; PASS; anti_slop=8; marker `critic-BUG0015-qa-20260906T150000Z-fresh`)
- **verdict**: **PASS** (verify-work) — UAT 9/9 pass, 0 fail (AC-1..AC-8 → UAT-1..UAT-8 + canonical `convergence_smoke`); live `pytest tests/bug0015_contract_test.py -v` → **7 passed in 0.71s**; isolation execute+qa+verify-work present
- **total_steps**: 9 (UAT-1..UAT-8 + canonical `convergence_smoke`)
- **passed**: 9 | **failed**: 0
- **bug_status**: OPEN (do not mark BUG-0015 DONE — US-0045; acceptance BUG-0015 L180 unchecked; intake JSON not mutated)
- **blocking_findings**: 0
- **non_blocking_findings**: 3 (NB-1..NB-3 carry-forwards — informational)
- **harness_fail_zero_claimed**: false (slice contract tests are the required evidence)
- **browser_probe_used**: false (no fake browser PASS)

## Probe class — OpenCode plugin contract

BUG-0015 is a plugin/command/contract-test slice. Applicable probe: `contract_tests_primary` (7 markers). No web UI. Six live-runtime classes waived with **`UAT_PROBE_FORBIDDEN`**: `browser_smoke`, `api_health`, `process_health`, `cli_smoke`, `build`, `manual_operator`. **No silent browser PASS.** MCP browser sequence not run.

Canonical surrogate step `id=convergence_smoke` kept `result=pass` because `contract_test_failed=0` (7/7 pytest).

## Target bug + acceptance criteria (architecture `# BUG-0015`)

- **BUG-0015** — OpenCode `/auto` never triggers orchestrator plugin dispatch and stops at command STOP (8 ACs)
  - AC-1: PASS — `/auto` starts plugin spawn loop via host attach (UAT-1; markers 1+2)
  - AC-2: PASS — Missing attach → `OPENCODE_PLUGIN_DISPATCH_ATTACH_UNSUPPORTED` (UAT-2; marker 3)
  - AC-3: PASS — Missing `session.create` → `OPENCODE_PLUGIN_SPAWN_UNSUPPORTED` (UAT-3; marker 4)
  - AC-4: PASS — IsolationEvidence + `OPENCODE_SUBTASK_IGNORED` + state.md SOT (UAT-4; marker 2 + bridge)
  - AC-5: PASS — Concurrent `/auto` → `OPENCODE_AUTO_ALREADY_RUNNING` (UAT-5; marker 5)
  - AC-6: PASS — `auto.md` dispatch-only ≤20 lines, no spawn literals (UAT-6; marker 6)
  - AC-7: PASS — Compose US-0124 spawn API unchanged (UAT-7; marker 7 + us0124 12/12)
  - AC-8: PASS — Seven additive `test_bug0015_*` green (UAT-8; 7/7 live)

## UAT step results (verify-work)

| Step | AC | Result | Evidence |
|------|----|--------|----------|
| UAT-1 | AC-1 | pass | `command.transform` / `editor.add` auto execute → `runAutoLifecycle`; markers 1+2 |
| UAT-2 | AC-2 | pass | marker 3; `OPENCODE_PLUGIN_DISPATCH_ATTACH_UNSUPPORTED` |
| UAT-3 | AC-3 | pass | marker 4; `OPENCODE_PLUGIN_SPAWN_UNSUPPORTED` |
| UAT-4 | AC-4 | pass | marker 2 evidence fields + `opencode_auto_bridge.py`; NB-1 soft-continue non-blocking |
| UAT-5 | AC-5 | pass | marker 5; `OPENCODE_AUTO_ALREADY_RUNNING`; TTL `Date.now()` 7200s |
| UAT-6 | AC-6 | pass | marker 6; `auto.md` ≤20 lines; no spawn literals |
| UAT-7 | AC-7 | pass | marker 7; us0124 12/12; DEC-0124/0125 unchanged |
| UAT-8 | AC-8 | pass | 7/7 `test_bug0015_*` — live `7 passed in 0.71s` |
| convergence_smoke | surrogate | pass | `contract_test_failed=0`; 6 waived probes `UAT_PROBE_FORBIDDEN` |

## Contract test markers (7) — verify-work live re-run

`python -m pytest tests/bug0015_contract_test.py -v` — **7 passed** in 0.71s (2026-09-06T15:05:00Z).

1. `test_bug0015_command_transform_registers_auto` — PASS
2. `test_bug0015_auto_execute_invokes_spawn_phase` — PASS
3. `test_bug0015_missing_attach_fail_closed` — PASS
4. `test_bug0015_missing_session_create_fail_closed` — PASS
5. `test_bug0015_concurrent_reentry_fail_closed` — PASS
6. `test_bug0015_auto_md_dispatch_only_static` — PASS
7. `test_bug0015_compose_us0124_spawn_api_unchanged` — PASS

## Waived probes (honest live-runtime)

| Probe | reason_code |
|-------|-------------|
| browser_smoke | `UAT_PROBE_FORBIDDEN` (OpenCode plugin contract; no web UI) |
| api_health | `UAT_PROBE_FORBIDDEN` (no runtime HTTP API) |
| process_health | `UAT_PROBE_FORBIDDEN` (no runtime app server) |
| cli_smoke | `UAT_PROBE_FORBIDDEN` (mock-ctx harness only; no live OpenCode CI probe) |
| build | `UAT_PROBE_FORBIDDEN` (no separate build step) |
| manual_operator | `UAT_PROBE_FORBIDDEN` (contract markers cover attach path) |

## Results summary

- **Total**: 9 steps
- **Passed**: 9
- **Failed**: 0
- **Verdict**: PASS
- **Blocking QA findings**: 0 (`sprints/S0131/qa-findings.md` verdict QA_PASS)
- **Acceptance linkage**: AC-1..AC-8 each map to ≥1 UAT step; all PASS. Acceptance checkbox L180 remains unchecked until `/closure` (US-0045).

## Live gate evidence (verify-work)

| Gate | Result |
|------|--------|
| `pytest tests/bug0015_contract_test.py -v` | **7 passed** in 0.71s |
| `pytest tests/us0124_contract_test.py -q` | **12 passed** in 1.46s |
| `check_intake_template_parity.py --scope=bug-0015` | `[INTAKE_TEMPLATE_PARITY_OK]` |
| `enforce-triad-hot-surface.py --check` | exit 0 |
| `check-user-visible-metadata.py --repo . --json` | OK / 0 violations |

## Isolation compliance (US-0048 / DEC-0029)

| Phase | Marker | Present |
|-------|--------|---------|
| execute | `dev-BUG0015-execute-20260906T144000Z-fresh` | yes |
| qa | `qa-BUG0015-qa-20260906T145500Z-fresh` | yes |
| verify-work | `qa-BUG0015-verify-work-20260906T150500Z-fresh` | yes (this phase) |

**Gate verdict**: PASS — no `PHASE_CONTEXT_ISOLATION_MISSING` / `ISOLATION_EVIDENCE_STALE` / `PHASE_CONTEXT_ISOLATION_VIOLATION`.

## Strict runtime proof gate (US-0056 / DEC-0038)

| Phase | runtime_proof_id | proof_hash | Present |
|-------|------------------|------------|---------|
| execute | `rp-auto-20260906-bug0015-execute-dev-20260906T144500Z-BUG-0015` | `1E8BF777…9CB0` | yes |
| qa | `rp-auto-20260906-bug0015-qa-qa-20260906T145500Z-BUG-0015` | `B2924E1E…35FB` | yes |
| verify-work | `rp-auto-20260906-bug0015-verify-work-qa-20260906T150500Z-BUG-0015` | `165F812E…4117` | yes (this phase) |

## Producer proof consumed (qa)

- `runtime_proof_id=rp-auto-20260906-bug0015-qa-qa-20260906T145500Z-BUG-0015`
- Independent SHA-256 MATCH `B2924E1E4F3B1E750491884C7F1226E6DA15F24C9421333914394386AA4E35FB`
- `proof_ttl=2026-09-06T15:55:00Z`; consumed_at `2026-09-06T15:05:00Z` (before RUNTIME_PROOF_STALE)

## Runtime proof (DEC-0038) — verify-work

- `runtime_proof_id=rp-auto-20260906-bug0015-verify-work-qa-20260906T150500Z-BUG-0015`
- Canonical payload: `{"delivery_mode":"ultra_lean","macro_phase":"build+verify","model_id":"composer-2.5","orchestrator_run_id":"auto-20260906-bug0015","phase_id":"verify-work","proof_issued_at":"2026-09-06T15:05:00Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260906-bug0015-verify-work-qa-20260906T150500Z-BUG-0015","sprint_id":"S0131","story_id":"BUG-0015"}`
- `proof_hash=165F812E5357B9DC0BF07AC07628F96D62BB10DFA2056F7EA2C97ADE8C5A4117`
- `proof_issued_at=2026-09-06T15:05:00Z`
- `proof_ttl_seconds=3600`, `proof_ttl=2026-09-06T16:05:00Z`

## Isolation evidence (US-0048 / DEC-0029 / US-0104 v2) — verify-work

- `phase_id=verify-work`, `role=qa`, `model_id=composer-2.5` (CROSS_MODEL_REVIEW=1 — required)
- `fresh_context_marker=qa-BUG0015-verify-work-20260906T150500Z-fresh` (NEW per US-0048 / BUG-0006)
- `timestamp=2026-09-06T15:05:00Z` (UTC)
- `evidence_ref=sprints/S0131/uat.json + sprints/S0131/uat.md`

## Status confirmation (US-0045)

- backlog `### BUG-0015` Status: **OPEN** (L4899) — not flipped DONE
- acceptance L180: **unchecked**
- BUG-0016 remains OPEN / out of scope
- intake JSON not mutated

## Next scheduled phase

- `/release` (role=release; orchestrator-owned fresh subagent per BUG-0006; after sovereign-critic of verify-work if CROSS_MODEL_REVIEW=1)
- STOP after verify-work PASS. Do NOT spawn `/release` from this subagent. Do NOT mark BUG-0015 DONE. Do NOT tick acceptance L180. Do NOT mutate intake JSON. Do NOT solve BUG-0016.
