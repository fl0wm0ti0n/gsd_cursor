# QA → Verify-Work Handoff

## Remote evidence tuple (US-0086 / AC-5)

When routing verify-work to remote or container targets, emit names-only evidence:

- `target_id`
- `environment_label`
- `automation_profile`
- `routing_source`
- `secret_surface=names_only`

See `docs/engineering/runbook.md` for operator examples.

---

# QA → Verify-Work Handoff — S0108 / US-0108 (QA PASS, next `/verify-work` fresh qa subagent)

**Sprint**: S0108
**Story**: US-0108 — Parallel Instance Arbitrage for dev phase
**QA role**: qa
**Timestamp**: 2026-06-29T21:45:00Z
**Orchestrator run ID**: auto-20260628-04
**Fresh context marker**: qa-verify-work-S0108-US0108-auto-20260628-04-20260629T214500Z-fresh
**Plan-verify verdict**: **PASS**

## Summary

Plan-verify for US-0108 / S0108 completed. AC-1..AC-8 surjective map to T-001..T-011 confirmed. 11 tasks ≤ SPRINT_MAX_TASKS=12. Compose guards (US-0047/US-0092/US-0103/US-0104/US-0107) verified — no modifications required. DEC-0108 locked (Accepted). R-0096 referenced (delivered, Q1–Q10 CLOSED). No blocking findings.

## Verification criteria

- [x] AC-1..AC-8 surjective map confirmed in sprint artifacts
- [x] 11 tasks T-001..T-011 within SPRINT_MAX_TASKS=12
- [x] Compose guards verified (no US-0047/US-0092/US-0103/US-0104/US-0107 modifications required)
- [x] DEC-0108 locked and referenced
- [x] R-0096 referenced as research anchor

## Artifacts

- `sprints/S0108/plan-verify-findings.md` — verification results
- `sprints/S0108/plan-verify-verdict.json` — structured PASS verdict
- `sprints/S0108/sprint.md`, `tasks.md`, `progress.md`, `sprint.json`, `plan-verify.json`

## Next phase

Spawn fresh **dev** subagent for **`/execute`** on **S0108 / US-0108**.

---

# QA → Verify-Work Handoff — S0107 / US-0107

**Sprint**: S0107  
**Story**: US-0107 — Sovereign Loop Mode (AUTO_SOVEREIGN)  
**QA role**: qa  
**Timestamp**: 2026-06-29T00:21:00Z  
**Orchestrator run ID**: auto-20260628-04  
**Fresh context marker**: qa-S0107-US0107-20260629T002100Z-fresh  
**QA verdict**: **PASS**

## Summary

QA verification of US-0107 execute deliverables completed successfully. All 10 contract tests pass (8 core + 2 compose guards). Lib and validator self-tests green. Template parity scope `sovereign-loop` (6 pairs) PASS. All AC-1..AC-8 satisfied. No blocking findings. **US-0107 remains OPEN** per US-0045. **`docs/engineering/state.md` not modified.**

## Evidence

| Gate | Result |
|------|--------|
| Contract tests | 10/10 PASS (`pytest -k us0107 -v`) |
| Lib self-test | `[SOVEREIGN_LOOP_SELF_TEST_OK]` exit 0 |
| Validator self-test | `[SOVEREIGN_LOOP_VALIDATION_OK]` exit 0 |
| Parity | `[INTAKE_TEMPLATE_PARITY_OK] scope=sovereign-loop pairs=6` |
| Scratchpad keys | Nine `AUTO_SOVEREIGN_*` + `SOVEREIGN_NOTIFY_*` keys in active + template scratchpad |
| Deferral bootstrap | `handoffs/sovereign_deferrals/.gitkeep` (+ template mirror) |
| Reason codes | 12 codes § US-0107 in `docs/engineering/reason_codes.md` |
| Runbook | § Sovereign Loop Mode (US-0107) + US-0109 `DEPLOY_DEFERRED` integration declaration |
| `/auto` orchestrator | Sovereign loop advance hook, spawn-only PO drain-generate, mandatory per-candidate decision gate |
| US-0110 compose | `list_open_deferrals()` wired into `zero_deferrals` conjunct — no DEC-0110 amendment |
| Zero-overhead default | `AUTO_SOVEREIGN=0` → noop advance, no deferral reads/writes |
| Goal-mode coupling | Fail-closed `SOVEREIGN_LOOP_GOAL_MODE_REQUIRED` when sovereign on without `goal_convergence` |
| Compose regression | US-0088/US-0092/US-0095 stop matrix unchanged; US-0095 spawn-only preserved for drain-generate |

## AC coverage

| AC | Verdict | Primary evidence |
|----|---------|------------------|
| AC-1 | PASS | Scratchpad keys + zero-overhead default + goal-mode fail-closed |
| AC-2 | PASS | Deferral JSONL v1 schema, CRUD API, validator CLI, `.gitkeep` bootstrap |
| AC-3 | PASS | `advance_sovereign_loop` policy branches (stop/skip/resolve_first) + terminal paths |
| AC-4 | PASS | Drain-generate 3-candidate cap, spawn-only PO, mandatory decision gate in `/auto` |
| AC-5 | PASS | Notification fail-open (ntfy/hook); email deferred; local-only secret config |
| AC-6 | PASS | US-0110 `zero_deferrals` import + US-0109 `DEPLOY_DEFERRED` integration declaration |
| AC-7 | PASS | Eight contract tests + parity `--scope=sovereign-loop` |
| AC-8 | PASS | Reason codes, runbook, compose-no-stop-matrix guards |

## Artifacts for verify-work

- `sprints/S0107/summary.md` — execute summary
- `sprints/S0107/execute-findings.md` — execute gate evidence
- `sprints/S0107/qa-findings.md` — this turn's findings
- `sprints/S0107/qa-verdict.json` — structured PASS verdict
- `tests/us0107_contract_test.py` — 10 contract tests
- `scripts/sovereign_loop_lib.py` — deferral register, advance, drain-generate, notifications
- `scripts/sovereign_loop_validate.py` — JSONL validator CLI
- `decisions/DEC-0107.md` — binding decision (+ template mirror)
- Hook prose: `.cursor/commands/auto.md`, `docs/engineering/auto-orchestration-reference.md`

## Status authority

Do **not** flip US-0107 to DONE or check acceptance boxes — closure at `/release` only. Do **not** modify `docs/engineering/state.md` during verify-work unless isolation evidence append is explicitly in scope for a live orchestrator run.

## Next phase

Spawn fresh **qa** subagent for **`/verify-work`** on **S0107** / **US-0107** (spawn-only per BUG-0006; native chain per DEC-0080 / DEC-0081).
