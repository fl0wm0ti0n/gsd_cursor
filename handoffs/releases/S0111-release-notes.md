# Release Notes — Sprint S0111

**Sprint**: S0111
**Story**: US-0111 — Release Trigger-Driven Version Changelog Derivation
**Decision**: DEC-0111
**Research**: R-0098
**Release Date**: 2026-06-30T19:45:00Z
**Orchestrator Run**: auto-20260628-04
**Verdict**: PASS
**Trigger Source**: manual (manual /release)
**Publish Mode**: disabled (skipped)

## Summary

Extended US-0100 version-scoped changelog with trigger-agnostic entry points for GitHub webhook, npm registry, git tag, and manual release sources. Added atomically generated per-version release notes, sovereign ledger `append_event` integration with `decision_type=version_derivation`, and nine fail-closed `RELEASE_TRIGGER_*` reason codes. Composition preserved: seven compose guard stories untouched.

## Deliverables

| Artifact | Scope | Compose Status |
| --- | --- | --- |
| `scripts/release_trigger_adapters.py` | Trigger adapter library with `TriggerContext` dataclass, `ReleaseAdapter` ABC, 4 concrete adapters, registry dispatcher | New file |
| `tests/us0111_contract_test.py` | 12 contract test markers | New file |
| `template/scripts/release_trigger_adapters.py` | Byte-parity mirror | New file (template) |
| `template/tests/us0111_contract_test.py` | Byte-parity mirror | New file (template) |
| `docs/engineering/reason_codes.md` § US-0111 | 9 RELEASE_TRIGGER_* codes | Additive section (template mirror) |
| `docs/engineering/runbook.md` § US-0111 | Operator recipe | Additive section (template parity) |
| `.cursor/scratchpad.md` | 3 new keys: `RELEASE_TRIGGER_SOURCE=manual`, `RELEASE_TRIGGER_TIMEOUT_SEC=10`, `RELEASE_TRIGGER_FALLBACK_TO_LOCAL=0` | Additive keys (template mirror) |

## Trigger Adapter System

Four adapter types registered in the adapter registry:

| Adapter | Source Value | Implementation |
| --- | --- | --- |
| GitHub webhook | `github` | `GitHubReleaseAdapter` — parses `release.tag_name`, queries GitHub API, fails closed on missing tag |
| npm registry | `npm` | `NpmRegistryAdapter` — queries `npm view <pkg> versions --json`, computes `previous_version` via semver |
| Git tag | `git_tag` | `GitTagAdapter` — parses `git describe --tags`, handles annotated/lightweight tags |
| Manual `/release` | `manual` | `ManualReleaseAdapter` — byte-identical to pre-US-0111 behavior |

## Contract Test Results

```
pytest -k us0111 -v → 12/12 PASS
```

## Compose Guards

| Guard | File | Status |
| --- | --- | --- |
| US-0008 | `scripts/sovereign_convergence_check.py` | Unchanged |
| US-0040 | `docs/engineering/runbook.md` | Additive-section-only |
| US-0054 | `scripts/release-all.sh` | Unchanged |
| US-0100 | `scripts/release_changelog_lib.py` + `.cursor/scratchpad.md` | Unchanged-lib; additive-keys in scratchpad |
| US-0103 | `scripts/decision_ledger_lib.py` | Consumer-only-append |
| US-0107 | `scripts/release_promotion_guard.py` | Unchanged |
| US-0110 | `tests/us0109_contract_test.py` | Unchanged |

All 7/7 guards PASS — no regressions detected.

## Reason Codes (9 RELEASE_TRIGGER_*)

| Code | Description |
| --- | --- |
| `RELEASE_TRIGGER_ADAPTER_FAILED` | Adapter dispatch failed |
| `RELEASE_TRIGGER_TAG_MISSING` | Missing tag in adapter response |
| `RELEASE_TRIGGER_PREVIOUS_MISSING` | Missing previous_version |
| `RELEASE_TRIGGER_PACKAGE_JSON_MISSING` | Missing package.json for npm adapter |
| `RELEASE_TRIGGER_ATOMIC_PROMOTION_FAILED` | Atomic promotion failed |
| `RELEASE_TRIGGER_NOTES_WRITE_FAILED` | Release notes write failed |
| `RELEASE_TRIGGER_EVENT_EMIT_FAILED` | Ledger event emit failed |
| `RELEASE_TRIGGER_COMPARE_VERSIONS_FAILED` | Version comparison failed |
| `RELEASE_TRIGGER_SOURCE_INVALID` | Unknown trigger source |

## Gate Verification

| Gate | Verdict | Evidence |
| --- | --- | --- |
| Check-in test gate | PASS | 12/12 US-0111 contract tests |
| QA completion gate | PASS | QA PASS, 0 blockers |
| UAT completion gate | PASS | 12/12 verified UAT steps (uat.json + uat.md) |
| Isolation compliance gate | PASS | Distinct fresh context markers per phase |
| Compose regression guard | PASS | 7/7 unchanged |
| Template parity | PASS | `--scope=release-trigger-adapter`, 2 pairs |

## Run

```powershell
pytest tests/us0111_contract_test.py -v
python scripts/release_trigger_adapters.py --self-test
```

Expected: 12 passed, `[RELEASE_TRIGGER_SELF_TEST_OK]`

## Connect

- Trigger source: controlled by scratchpad key `RELEASE_TRIGGER_SOURCE` (default `manual`)
- Integration: `compare_versions_from_trigger(trigger_context)` wraps `release_changelog_lib.compare_versions()`
- Event path: `handoffs/release_events/{timestamp}-{semver}.json` (when available)

## Verify

1. `pytest tests/us0111_contract_test.py -v` → 12 passed
2. `python scripts/release_trigger_adapters.py --self-test` → `[RELEASE_TRIGGER_SELF_TEST_OK]`
3. Confirm reason code inventory: 9 codes documented in `docs/engineering/reason_codes.md` § US-0111
4. Confirm runbook recipe: § Release Triggers (US-0111) present in `docs/engineering/runbook.md`

## Known Issues

None

## Credentials

Not applicable (no external secrets required; all adapters operate against local state or configurable environment variables).

## Queue Entry

`handoffs/release_queue.md` row `S0111` = `released` (2026-06-30).
