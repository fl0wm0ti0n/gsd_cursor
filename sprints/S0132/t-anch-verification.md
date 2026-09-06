# T-anch verification — BUG-0016 / S0132 (NO-OP)

**sprint_id**: S0132  
**bug_id**: BUG-0016  
**task**: T-anch  
**phase_id**: execute  
**role**: dev  
**orchestrator_run_id**: auto-20260906-bug0016  
**fresh_context_marker**: `dev-BUG0016-execute-20260906T190500Z-fresh`  
**timestamp**: 2026-09-06T19:05:00Z (UTC)  
**model_id**: composer-2.5 (CROSS_MODEL_REVIEW=1)  
**verdict**: PASS (baseline confirmed; NO mutation to architecture.md / DEC-0122 body)

## Checks

| Check | Result | Evidence |
|---|---|---|
| `# BUG-0016` H1 in `docs/engineering/architecture.md` | PASS | L2712 `# BUG-0016 — OpenCode Layer-1 permissions vs kit duties (amend DEC-0122 §2)` |
| Approach A* locked | PASS | architecture § Approach locked (A* — from R-0115 DQ1–DQ8) |
| R-0115 DQ1–DQ8 LOCKED | PASS | `docs/engineering/research.md` `## R-0115`; architecture cites DQ1–DQ8 |
| CF1–CF5 CLOSED | PASS | architecture critic NB closures table CF1..CF5 LOCKED |
| Companion DEC none (DEC-0130 rejected) | PASS | no `decisions/DEC-0130.md`; architecture/DEC reject A3 / CF4 |
| `decisions/DEC-0122.md` §2 already amended (sole SOT) | PASS | Amended banner + matrix uses `bash: ask`, PO duty paths, `sprints/S*/`, release duty paths; security/auto unchanged |
| Success test (c) prose intact | PASS | DEC-0122 §2 Ordering contract + §3 static harness; no production/code allow for non-dev |
| 7-marker contract-test list locked | PASS | architecture DQ7 table markers 1–7 named |
| Compose guards | PASS | no US-0131/US-0132 reopen; no bash:allow; no live probe; security/auto unchanged in matrix |
| Pre-execute agent gap | PASS | active+template agents still show `bash: deny` (po/tl/curator), `sprints/Sxxxx/`, release missing duty paths |
| `tests/bug0016_contract_test.py` absent (baseline) | PASS | file does not exist pre-T-006 |
| No architecture.md / DEC-0122 body mutation this task | PASS | read-only verification only |

## Pre-execute gap snapshot (confirm)

- po / tech-lead / curator: `bash: deny`
- tech-lead / dev / qa: permission keys use literal `sprints/Sxxxx/…`
- release: missing `release-findings`, `verify-work-to-release`, `state.md`, `resume_brief.md`, `runbook.md`
- security / auto: match amended matrix already (unchanged targets)

## Next

T-001 → amend `po.md` active+template.
