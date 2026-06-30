# Sprint S0111 — Summary (US-0111)

**sprint_id**: S0111
**story_refs**: US-0111
**dec_ref**: DEC-0111
**research_ref**: R-0098
**orchestrator_run_id**: auto-20260628-04
**fresh_context_marker**: curator-S0111-US0111-refresh-context-20260630T200000Z-fresh
**status**: CLOSED (2026-06-30T19:45:00Z)
**closed_at**: 2026-06-30T19:45:00Z
**release_id**: R0111
**release_verdict**: PASS (2026-06-30T20:00:00Z)

## Goal

Release Trigger-Driven Version Changelog Derivation. Dispatch release flow by
trigger source (GitHub webhook, npm publish, Git tag push, manual /release).
Atomic per-version `[Unreleased] → [X.Y.Z]` promotion. Sovereign loop integration
via `version_derivation` ledger events. Nine fail-closed reason codes. Compose
guards: US-0054, US-0100, US-0103, US-0040, US-0008, US-0107, US-0110 unchanged.

## Tasks completed

| Tranche | Task | AC | Deliverable |
|---------|------|----|-------------|
| A | T-001 | AC-1 | `scripts/release_trigger_adapters.py` — TriggerContext dataclass, ReleaseAdapter ABC, 4-entry registry, dispatch_to_adapter(source, env_vars); scratchpad keys `RELEASE_TRIGGER_SOURCE=manual` default. |
| B | T-002 | AC-2 | `GithubReleaseAdapter` — release.tag_name parsing, GitHub API + git ls-remote fallback, GITHUB_TOKEN names-only, fail-closed |
| B | T-003 | AC-3 | `NpmPublishAdapter` — npm_package_version env + npm registry query + package-lock.json fallback, 10s timeout, fail-closed |
| B | T-004 | AC-4 | `GitTagAdapter` — GITHUB_REF + git describe + git for-each-ref semver sort, fail-closed |
| B | T-005 | AC-5 | `ManualReleaseAdapter` — byte-identical to pre-US-0111 /release (previous_version=None) |
| C | T-006 | AC-6 | `compare_versions_from_trigger()` — source-aware routing via release_changelog_lib.normalize_semver (US-0100 compose) |
| C | T-007 | AC-7 | `promote_changelog_version()` — atomic write via os.replace with Windows retry; uses release_changelog_lib.promote_unreleased unchanged |
| C | T-008 | AC-8 | `write_per_version_notes()` — atomic write to `handoffs/releases/v{X.Y.Z}-release-notes.md` |
| C | T-009 | AC-9 | `emit_version_derivation_event()` — `decision_type="version_derivation"` ledger append + release event JSON |
| C | T-010 | AC-10 | 9 fail-closed codes appended to `docs/engineering/reason_codes.md` § US-0111 |
| D | T-011 | AC-11 | 12 contract tests in `tests/us0111_contract_test.py`; template parity scope `release-trigger-adapter` PASS |
| D | T-012 | AC-12 | Runbook section in `docs/engineering/runbook.md` § US-0111; reason_codes already in T-010 |

## Gate results

| Gate | Command | Outcome |
|------|---------|---------|
| Contract tests | `pytest -k us0111 -v` | **12/12 PASS** |
| Template parity | `python scripts/check_intake_template_parity.py --scope=release-trigger-adapter` | `[INTAKE_TEMPLATE_PARITY_OK]` |
| Reason codes inventory | `test_us0111_reason_code_inventory_9_codes` | PASS (9/9 in lib + docs) |
| US-0100 compose guard | `test_us0111_us0100_compose_no_derivation_semantics_change` | PASS |
| US-0054 compose guard | `test_us0111_us0054_compose_no_publish_semantics_change` | PASS |

## Key files

- `scripts/release_trigger_adapters.py` (active + template byte-identical)
- `tests/us0111_contract_test.py` (active + template byte-identical)
- `docs/engineering/reason_codes.md` § US-0111 (9 codes; active + template)
- `docs/engineering/runbook.md` § US-0111 (active + template parity)
- `.cursor/scratchpad.md` (3 new scratchpad keys: RELEASE_TRIGGER_SOURCE/TIMEOUT_SEC/FALLBACK_TO_LOCAL)
- `decisions/DEC-0111.md` (locked)
- `sprints/S0111/{tasks.md, progress.md, sprint.json}`

## Non-goals (honored)

- Did NOT amend compose-guarded files: US-0054 (release-all.sh), US-0103 (decisions.md structure), US-0040 (runbook structure outside additive section), US-0008 (sovereign_convergence_check.py), US-0107 (release_promotion_guard.py), US-0110 (us0109_contract_test.py).
- Did NOT modify US-0100 release_changelog_lib APIs — all reuse is via consumer-only compose.
- Did NOT set US-0111 DONE in backlog — status authority reserved for /release.

## Status authority

**US-0111** remains OPEN in `docs/product/backlog.md` per US-0045 (released at /release).

## QA handoff

See `handoffs/dev_to_qa.md`. Next phase: `/qa` (fresh qa subagent context).
