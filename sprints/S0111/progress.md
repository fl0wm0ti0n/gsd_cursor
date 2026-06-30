# Sprint S0111 Progress

- sprint_id: S0111
- story_id: US-0111
- story_title: Release Trigger-Driven Version Changelog Derivation
- dec_ref: DEC-0111
- research_ref: R-0098
- status: OPEN
- created_at: 2026-06-30T18:20:00Z
- orchestrator_run_id: auto-20260628-04

## Compose Guards (non-negotiable)

1. US-0054: release-all.sh
2. US-0100: .cursor/scratchpad.md
3. US-0103: docs/engineering/decisions.md
4. US-0040: docs/engineering/runbook.md
5. US-0008: scripts/sovereign_convergence_check.py
6. US-0107: scripts/release_promotion_guard.py
7. US-0110: tests/us0109_contract_test.py

## AC-to-task surjective map

| AC | Tasks | Status |
|----|-------|--------|
| AC-1 | T-001 | DONE |
| AC-2 | T-002 | DONE |
| AC-3 | T-003 | DONE |
| AC-4 | T-004 | DONE |
| AC-5 | T-005 | DONE |
| AC-6 | T-006 | DONE |
| AC-7 | T-007 | DONE |
| AC-8 | T-008 | DONE |
| AC-9 | T-009 | DONE |
| AC-10 | T-010 | DONE |
| AC-11 | T-011 | DONE |
| AC-12 | T-012 | DONE |

## Tranche A — Adapter registry + TriggerContext

- [x] **T-001** AC-1 — Adapter registry (AC-1): TriggerContext dataclass, ReleaseAdapter ABC, dispatch_to_adapter source registry. RELEASE_TRIGGER_SOURCE=manual default + scratchpad key block.

## Tranche B — Four concrete adapters

- [x] **T-002** AC-2 — GitHub webhook adapter: GithubReleaseAdapter parsing release.tag_name, previous resolution via GitHub API + git ls-remote fallback, GITHUB_TOKEN names-only, fail-closed RELEASE_TRIGGER_TAG_MISSING/PREVIOUS_MISSING.
- [x] **T-003** AC-3 — npm publish adapter: NpmPublishAdapter reading npm_package_version env var, registry query with RELEASE_TRIGGER_TIMEOUT_SEC, offline fallback via RELEASE_TRIGGER_FALLBACK_TO_LOCAL=1 → package-lock.json, fail-closed RELEASE_TRIGGER_REGISTRY_UNREACHABLE/PACKAGE_JSON_MISSING.
- [x] **T-004** AC-4 — Git tag push adapter: GitTagAdapter parsing GITHUB_REF env var or git describe --tags --abbrev=0, previous via git for-each-ref --sort=-version:refname refs/tags (semver sort, annotated/lightweight handled), fail-closed RELEASE_TRIGGER_TAG_MISSING/PREVIOUS_MISSING.
- [x] **T-005** AC-5 — Manual backward compatibility adapter: ManualReleaseAdapter returning TriggerContext(source=manual, version=current, previous_version=None); downstream treats as legacy path; byte-identical to pre-US-0111 /release.

## Tranche C — Version compare + promotion + notes + ledger + reason codes

- [x] **T-006** AC-6 — compare_versions integration: compare_versions_from_trigger(trigger) normalizes via release_changelog_lib.normalize_semver; US-0100 compare_versions() signature unchanged (read-only compose); source-aware routing. FAIL_CLOSED RELEASE_TRIGGER_COMPARE_VERSIONS_FAILED.
- [x] **T-007** AC-7 — Atomic promotion: promote_changelog_version() writes atomically via os.replace(temp, target); Windows best-effort retry (PermissionError → 0.1s → retry × 2 → RELEASE_TRIGGER_ATOMIC_PROMOTION_FAILED); promote [Unreleased] → [X.Y.Z] reusing release_changelog_lib.promote_unreleased() unchanged.
- [x] **T-008** AC-8 — Per-version notes generation: write_per_version_notes() atomically via os.replace(temp, target) same Windows best-effort; reuse release_changelog_lib build_version_doc/normalize_semver/derive_work_items/version_fingerprint without modification. FAIL_CLOSED: RELEASE_TRIGGER_NOTES_WRITE_FAILED.
- [x] **T-009** AC-9 — Sovereign loop integration: emit_version_derivation_event() appends (semver, previous_semver, timestamp, derivation_decisions[]) to ledger via decision_ledger_lib.append_entry(decision_type='version_derivation'); ledger schema unchanged (consumer-only compose); writes handoffs/release_events/{iso-timestamp}-{semver}.json. FAIL_CLOSED: RELEASE_TRIGGER_EVENT_EMIT_FAILED.
- [x] **T-010** AC-10 — Fail-closed reason codes (9 codes appended to docs/engineering/reason_codes.md § US-0111): RELEASE_TRIGGER_ADAPTER_FAILED, TAG_MISSING, PREVIOUS_MISSING, PACKAGE_JSON_MISSING, ATOMIC_PROMOTION_FAILED, NOTES_WRITE_FAILED, EVENT_EMIT_FAILED, COMPARE_VERSIONS_FAILED, SOURCE_INVALID. Template mirror updated.

## Tranche D — Contract tests + docs + runbook

- [x] **T-011** AC-11 — Contract tests (tests/us0111_contract_test.py) with 12 markers: test_us0111_adapter_registry_dispatch, github_adapter_success_fail_closed, npm_adapter_success_fail_closed, git_tag_adapter_success_fail_closed, manual_backward_compat_byte_identical, compare_versions_from_trigger_integration, atomic_promotion_temp_rename, per_version_notes_atomic_write, ledger_event_emit_shape, reason_code_inventory_9_codes, us0100_compose_no_derivation_semantics_change, us0054_compose_no_publish_semantics_change. Template parity scope `release-trigger-adapter` via scripts/check_intake_template_parity.py; token `[INTAKE_TEMPLATE_PARITY_OK]`. All 12/12 tests PASS.
- [x] **T-012** AC-12 — Documentation + runbook: docs/engineering/runbook.md § US-0111 (adapter priority, troubleshooting, compose surfaces, parity enforcement). docs/engineering/reason_codes.md § US-0111 (9 codes). Template mirror: runbook + reason_codes byte-identical.

## Gate evidence

| Gate | Command | Outcome |
|------|---------|---------|
| Contract tests | `pytest -k us0111 -v` | **12/12 PASS** |
| Template parity | `python scripts/check_intake_template_parity.py --scope=release-trigger-adapter` | **[INTAKE_TEMPLATE_PARITY_OK]** |
| Reason codes documented | `tests/us0111_contract_test.py::US0111ReasonCodeInventoryTest` | PASS (9 codes in lib + docs) |
| Compose guard US-0100 | `tests/us0111_contract_test.py::US0111US0100ComposeTest` | PASS (API signatures unchanged) |
| Compose guard US-0054 | `tests/us0111_contract_test.py::US0111US0054ComposeTest` | PASS (no publish semantics change) |

## Phase Status

- [x] plan-verify
- [x] execute (dev)
- [ ] qa
- [ ] verify-work
- [ ] release
- [ ] refresh-context
