# Sprint S0111 - US-0111 Release Trigger Derivation - Tasks

## AC-to-task surjective map

| AC | Tasks |
|----|-------|
| AC-1 Trigger adapter registry | T-001 |
| AC-2 GitHub webhook adapter | T-002 |
| AC-3 npm publish trigger | T-003 |
| AC-4 Git tag push trigger | T-004 |
| AC-5 Manual backward compatibility | T-005 |
| AC-6 Version comparison logic | T-006 |
| AC-7 Atomic promotion | T-007 |
| AC-8 Per-version notes generation | T-008 |
| AC-9 Sovereign loop integration | T-009 |
| AC-10 Fail-closed reason codes | T-010 |
| AC-11 Contract tests + template parity | T-011 |
| AC-12 Documentation + runbook updates | T-012 |

## Tranche order (A->D)

| Tranche | Title | Tasks |
|---------|-------|-------|
| A | Adapter registry + TriggerContext | T-001 |
| B | Four concrete adapters | T-002, T-003, T-004, T-005 |
| C | Version compare + promotion + notes + ledger + reason codes | T-006, T-007, T-008, T-009, T-010 |
| D | Contract tests + docs + runbook | T-011, T-012 |

## Tasks

- [ ] **T-001** Trigger adapter registry (AC-1): Create `scripts/release_trigger_adapters.py` with `TriggerContext` dataclass (`version: str, previous_version: Optional[str], source: str, metadata: dict`), abstract `ReleaseAdapter` base class with `detect(env_vars) -> Optional[TriggerContext]` and `get_version_info() -> TriggerContext_with_version_and_previous`, and `dispatch_to_adapter(source, env_vars)` registry. Template mirror. Append scratchpad key `RELEASE_TRIGGER_SOURCE=manual` (default manual = zero behavior change). Dependency: none.

- [ ] **T-002** GitHub webhook adapter (AC-2): `GithubReleaseAdapter` in `release_trigger_adapters.py` — parse webhook payload `release.tag_name`; query GitHub API `GET /repos/{owner}/{repo}/releases` sorted by `created_at` desc to find previous tag (skip current); fallback via `git ls-remote --tags origin` filtered for semver sorted desc; use `GITHUB_TOKEN` names-only env ref; fail-closed `RELEASE_TRIGGER_TAG_MISSING` / `RELEASE_TRIGGER_PREVIOUS_MISSING`. Wire into registry. Dependency: T-001.

- [ ] **T-003** npm publish adapter (AC-3): `NpmPublishAdapter` in `release_trigger_adapters.py` — read `npm_package_version` env var; query npm registry `npm view {pkg} versions --json` with 10s timeout (`RELEASE_TRIGGER_TIMEOUT_SEC`); offline fallback via `RELEASE_TRIGGER_FALLBACK_TO_LOCAL=1` → `package-lock.json`; fail-closed `RELEASE_TRIGGER_REGISTRY_UNREACHABLE`. Wire into registry. Dependency: T-001.

- [ ] **T-004** Git tag push adapter (AC-4): `GitTagAdapter` in `release_trigger_adapters.py` — parse `GITHUB_REF` env var (CI) or local `git describe --tags --abbrev=0`; compute `previous_version` via `git for-each-ref --sort=-version:refname refs/tags` filtered for semver (annotated vs lightweight handled by semver sort, NOT date); fail-closed `RELEASE_TRIGGER_TAG_MISSING` / `RELEASE_TRIGGER_PREVIOUS_MISSING`. Wire into registry. Dependency: T-001.

- [ ] **T-005** Manual backward compatibility (AC-5): `ManualReleaseAdapter` in `release_trigger_adapters.py` — `/release` command dispatch returns `TriggerContext(source=manual, version=current, previous_version=None)`; downstream treats as legacy path; byte-identical to pre-US-0111 `/release` behavior. Regression guard `test_us0111_manual_backward_compat_byte_identical`. Wire into registry. Dependency: T-001.

- [ ] **T-006** Version comparison logic (AC-6): Integrate TriggerContext into `release_changelog_lib.compare_versions(target_version)`. When source != manual, compare_versions computes semver diff. US-0100 `compare_versions()` function signature UNCHANGED (read-only compose). Source-aware routing in adapter dispatch. Dependency: T-002, T-003, T-004, T-005.

- [ ] **T-007** Atomic promotion (AC-7): Generate `CHANGELOG-vX.Y.Z.md` atomically via `os.replace(temp, target)` (best-effort on Windows: catch `PermissionError`, retry 0.1s, then `RELEASE_TRIGGER_ATOMIC_PROMOTION_FAILED`); promote `[Unreleased]` → `[X.Y.Z]` in `CHANGELOG.md`; reuse `release_changelog_lib.promote_unreleased()` without modification (US-0100 compose). Dependency: T-006.

- [ ] **T-008** Per-version notes generation (AC-8): Emit `handoffs/releases/vX.Y.Z-release-notes.md` atomically via `os.replace(temp, target)` (same Windows best-effort); reuse `release_changelog_lib` notes APIs without modification. Dependency: T-006.

- [ ] **T-009** Sovereign loop integration (AC-9): Emit `(semver, previous_semver, timestamp, derivation_decisions[])` event to US-0103 ledger via `append_entry(decision_type=version_derivation, payload={semver, previous_semver, timestamp_iso, derivation_decisions})` — ledger schema unchanged (consumer-only append compose). Write `handoffs/release_events/{iso-timestamp}-{semver}.json` (create dir if missing). Dependency: T-007, T-008.

- [ ] **T-010** Fail-closed reason codes (AC-10): Add **9 codes** to `docs/engineering/reason_codes.md` under § US-0111: `RELEASE_TRIGGER_ADAPTER_FAILED`, `RELEASE_TRIGGER_TAG_MISSING`, `RELEASE_TRIGGER_PREVIOUS_MISSING`, `RELEASE_TRIGGER_PACKAGE_JSON_MISSING`, `RELEASE_TRIGGER_ATOMIC_PROMOTION_FAILED`, `RELEASE_TRIGGER_NOTES_WRITE_FAILED`, `RELEASE_TRIGGER_EVENT_EMIT_FAILED`, `RELEASE_TRIGGER_COMPARE_VERSIONS_FAILED`, `RELEASE_TRIGGER_SOURCE_INVALID`. Template mirror. Dependency: none.

- [ ] **T-011** Contract tests + template parity (AC-11): Create `tests/us0111_contract_test.py` with 12 markers: `test_us0111_adapter_registry_dispatch`, `test_us0111_github_adapter_success_fail_closed`, `test_us0111_npm_adapter_success_fail_closed`, `test_us0111_git_tag_adapter_success_fail_closed`, `test_us0111_manual_backward_compat_byte_identical`, `test_us0111_compare_versions_from_trigger_integration`, `test_us0111_atomic_promotion_temp_rename`, `test_us0111_per_version_notes_atomic_write`, `test_us0111_ledger_event_emit_shape`, `test_us0111_reason_code_inventory_9_codes`, `test_us0111_us0100_compose_no_derivation_semantics_change`, `test_us0111_us0054_compose_no_publish_semantics_change`. Add `check_intake_template_parity.py --scope=release-triggers` (mirror `scripts/release_trigger_adapters.py` ↔ `template/scripts/release_trigger_adapters.py`). Template parity token `[RELEASE_TRIGGER_SELF_TEST_OK]`. Dependency: T-001..T-010.

- [ ] **T-012** Documentation + runbook updates (AC-12): Append section "US-0111 — Release Trigger Derivation" to `docs/engineering/runbook.md` (operator recipe: adapter priority, troubleshooting). Append reason code family to `docs/engineering/reason_codes.md` § US-0111. Template mirror for runbook + reason codes. Dependency: T-010, T-011.
