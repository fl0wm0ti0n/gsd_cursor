# Release Notes — S0079 / BUG-0010 (triad archiver H2 backward-compat)

- **sprint_id**: S0079
- **bug_refs**: BUG-0010
- **release_name**: `S0079 — BUG-0010 triad archiver dual-level heading fix`
- **release_date**: 2026-06-06T16:36:00Z
- **orchestrator_run_id**: auto-20260606-02
- **verdict**: **PASS**
- **binding_decision**: `DEC-0076` (dual-level archiver H1-wins + diff-gated `ARCH_STORY_HEADING_LEVEL_INVALID`)
- **research_anchor**: `R-0076`

## Summary

Fixes triad hot-surface rollover blindness to legacy `## US-xxxx` story headings. The archiver now recognizes both H1 and H2 story boundaries with deterministic H1-wins precedence, unblocking `/auto` when `architecture.md` exceeds caps in downstream repos. Forward enforcement requires H1 `# US-xxxx` / `# BUG-xxxx` for new architecture writes via diff-gated policy checks, command mandate, contract tests, and harness **§29A**.

## What's new

- **Dual-level archiver (AC-1..AC-3, AC-7)** — `STORY_HEADING_H1` / `STORY_HEADING_H2` patterns; H1-wins `split_arch_stories` (+ template mirror).
- **Diff-gated policy (AC-4)** — `count_h2_story_headings`, `check_arch_heading_policy`, `--check-arch-heading-policy` CLI.
- **Self-test + fixtures (AC-1..AC-3, AC-6)** — Extended `--self-test` (H2-only rollover, mixed, policy delta, inner `##`, BUG H1).
- **Architecture command mandate (AC-4, AC-5)** — `.cursor/commands/architecture.md` H1 mandate + baseline/policy step (+ template).
- **Contract + harness (AC-5, AC-6)** — `test_bug0010_*` in `auto_command_contract_test.py`; harness **§29A** in `run-tests.ps1` / `run-tests.sh`.
- **Fixtures (AC-1, AC-3)** — `tests/fixtures/triad_arch_headings/` (H2-only + mixed).
- **Runbook remediation (AC-8)** — DEC-0076 §7 blurb verbatim (+ template).
- **Architecture linkage (AC-5)** — `test_bug0010_architecture_linkage` assert-only.

## Non-goals (explicit)

- No bulk normalize existing kit `## US-` → `# US-` (operator may remediate manually).
- No standalone validator script (in-place `enforce-triad-hot-surface.py` extension per DEC-0076).
- No new US-0017 parity scope beyond script + command mirrors.

## Run

- **start_command**: `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"`
- **runtime_mode**: `local`
- **runtime_context_ref**: `docs/engineering/runtime-connectivity.md`

## Connect

- **service_url**: N/A (framework/toolkit repository; no running service)
- **service_port**: N/A
- **health_endpoint**: N/A

## Verify

1. `python scripts/enforce-triad-hot-surface.py --self-test`
   → expect exit 0 (dual-level rollover + policy delta cases).
2. `python scripts/enforce-triad-hot-surface.py --check-arch-heading-policy --baseline-h2-count 5`
   → expect exit 0 on kit repo (grandfathered H2 story headings).
3. `python -m pytest tests/auto_command_contract_test.py -q -k bug0010`
   → expect 7 passed.
4. `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance`
   → expect `[BUG_VALIDATION_OK]` (exit 0).
5. Confirm active/template `enforce-triad-hot-surface.py` SHA-256 match (harness §29A).
6. `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"`
   → expect Pass=807 / Fail=14 (14 pre-existing disjoint).
7. Confirm `sprints/S0079/qa-findings.md` PASS and `sprints/S0079/uat.json` 8/8 PASS.
8. Confirm release-queue row `S0079` is `released` and backlog / acceptance show `BUG-0010` = DONE / checked.

- **expected_health_signal**: All artifact checks above pass; `BUG-0010` surfaces as `DONE` in backlog and checked in acceptance.

## Credentials

- Env-reference-only policy in effect. No inline secrets in release artifacts.

## Test evidence summary

- **Canonical `tests/run-tests.ps1`**: Pass=**807** / Fail=**14** (`tests/report.md` Timestamp=2026-06-06T14:31:49Z). +5 pass vs S0078 QA baseline; Fail=14 unchanged (disjoint from DEC-0076).
- **Archiver self-test**: exit 0.
- **Contract subtests**: `pytest -k bug0010` 7 passed.
- **Bug validator**: `[BUG_VALIDATION_OK]` pre- and post-release-write.
- **Harness §29A**: 5/5 assertions PASS.

## Governance references

- **DEC-0076** — dual-level archiver, H1-wins precedence, diff-gated forward enforcement.
- **DEC-0054** — triad hot-surface contract (§2 doc-only amendment).
- **US-0072** / **US-0061** / **US-0058** — triad enforcement + artifact ordering.
- **`docs/engineering/architecture.md`** `# BUG-0010`.
- **`docs/engineering/research.md`** `R-0076`.

## Known Issues

- None blocking release. Pre-existing harness Fail=14 remains for separate triage.
- OPEN bug `BUG-0011` remains on portfolio bug queue.
- Post-S0077 readme feature coverage live `--enforce` drift (`US-0091` `user_visible` metadata + README parity) — disjoint from BUG-0010; see `sprints/S0079/release-findings.md` §Doc gates.

## Release gate summary

| gate | verdict |
|------|---------|
| check-in_test | pass (807/14; 14 pre-existing disjoint) |
| qa | pass (cycle 1) |
| uat | pass (8/8) |
| isolation | pass |
| strict_proof | pass |
| triad_arch_heading | pass |
| readme_feature_coverage_3f | observation (pre-existing drift; S0077 canonical pass) |
| bug_validate | pass |
| finalization | pass |

## Strict proof (release phase)

- `runtime_proof_id=rp-auto-20260606-02-release-release-20260606T163600Z-S0079-BUG0010`
- `proof_hash=185901a6d7b195ae6ab54f9221953ba4311a955d70d62b76c69ca1c351ac4b14`
- `fresh_context_marker=release-S0079-BUG0010-release-20260606T163600Z-fresh`

## Sync / publish

- **Sync**: `SYNC_POLICY_MODE=by_phase`, `ALLOW_AUTO_PUSH=1`, branch `main`; `push_decision=blocked`, `reason_code=TEST_FAILED` (canonical harness Fail=14; disjoint from BUG-0010).
- **Publish**: `RELEASE_PUBLISH_MODE=confirm` → `skipped_pending_operator_confirm`.

## Next phase

- **`/refresh-context`** (fresh **curator** context) for segment closeout, then **`/auto`** for **`BUG-0011`**.
