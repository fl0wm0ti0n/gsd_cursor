# Sprint S0111 UAT — US-0111

- **Sprint**: `S0111`
- **Work item**: **US-0111** — Release Trigger-Driven Version Changelog Derivation
- **Governance**: **DEC-0111** + architecture `# US-0111` + **R-0098**
- **Orchestrator run**: **auto-20260628-04**
- **Machine-readable**: `sprints/S0111/uat.json`
- **Status**: **verified** (verify-work **2026-06-30T19:45:00Z**)
- **Canonical backlog**: **`docs/product/backlog.md`** — **US-0111** **OPEN** (closure at `/release` per **US-0045**)

## Metadata

- **author**: qa
- **qa_verdict_reference**: `sprints/S0111/qa-findings.md`
- **qa_timestamp**: `2026-06-30T19:30:00Z`
- **qa_verdict**: `PASS`
- **verify_work_executed_at**: `2026-06-30T19:45:00Z`
- **verify_work_role**: qa
- **verify_work_fresh_context_marker**: `qa-S0111-US0111-verify-work-20260630T194500Z-fresh`
- **verify_work_verdict**: `PASS`

## Target acceptance criteria (from architecture `# US-0111`)

- **AC-1**: Default-off `RELEASE_TRIGGER_SOURCE=manual` scratchpad gate + related keys
- **AC-2**: Four adapter types (github webhook, npm registry, git tag, manual `/release`)
- **AC-3**: GitHub webhook adapter parses payload + queries previous tag
- **AC-4**: npm registry adapter queries versions + computes previous via semver
- **AC-5**: Git tag adapter parses `git describe --tags` + handles annotated/lightweight tags
- **AC-6**: Manual adapter backward-compatible (byte-identical to pre-US-0111)
- **AC-7**: `TriggerContext` data structure abstraction consumed by `release_changelog_lib`
- **AC-8**: Ledger integration via `append_event` (decision_type=version_derivation)
- **AC-9**: Release notes generation (atomic write via US-0040)
- **AC-10**: 12 `test_us0111_*` contract markers + `RELEASE_TRIGGERS_PAIRS` parity
- **AC-11**: Runbook § Release Triggers (operator recipe)
- **AC-12**: Reason codes § US-0111 (9 fail-closed codes) + template byte-parity

## Verdict summary

| Bucket | Count |
|--------|-------|
| PASS | 12 |
| FAIL | 0 |
| SKIP | 0 |
| PENDING | 0 |
| Total | 12 |

## Preconditions

- Python 3.12+ available.
- DEC-0111 execute deliverables merged.
- `scripts/release_trigger_adapters.py` + template mirrors present.
- `tests/us0111_contract_test.py` with 12 test markers present.
- Reason codes documented in `docs/engineering/reason_codes.md` § US-0111.

## UAT steps

### UAT-1 — Scratchpad keys — AC-1 — `verdict=PASS`

`pytest -k test_us0111_scratchpad_keys_literals` → three `RELEASE_TRIGGER_*` keys + defaults (`RELEASE_TRIGGER_SOURCE=manual`, `RELEASE_TRIGGER_TIMEOUT_SEC=10`, `RELEASE_TRIGGER_FALLBACK_TO_LOCAL=0`).

### UAT-2 — Adapter registration — AC-2 — `verdict=PASS`

`pytest -k test_us0111_adapter_registry_dispatch` → four adapter types registered and dispatched correctly.

### UAT-3 — GitHub webhook adapter — AC-3 — `verdict=PASS`

`pytest -k test_us0111_github_webhook_adapter` → `GitHubReleaseAdapter` parses webhook payload and computes `previous_version`.

### UAT-4 — npm registry adapter — AC-4 — `verdict=PASS`

`pytest -k test_us0111_npm_registry_adapter` → `NpmRegistryAdapter` queries `npm view {pkg} versions --json` and computes `previous_version` via semver.

### UAT-5 — Git tag adapter — AC-5 — `verdict=PASS`

`pytest -k test_us0111_git_tag_adapter` → `GitTagAdapter` parses `git describe --tags` and handles annotated vs lightweight tag sorting.

### UAT-6 — Manual backward compatibility — AC-6 — `verdict=PASS`

`pytest -k test_us0111_manual_adapter_backward_compatible` → `ManualReleaseAdapter` byte-identical behavior; `RELEASE_TRIGGER_SOURCE=manual` path unchanged.

### UAT-7 — TriggerContext abstraction — AC-7 — `verdict=PASS`

`pytest -k test_us0111_trigger_context_shape` → `TriggerContext` dataclass with version, previous_version, source, metadata fields. Compose guard US-0100 honors `release_changelog_lib.compare_versions()` signature.

### UAT-8 — Ledger integration — AC-8 — `verdict=PASS`

`pytest -k test_us0111_ledger_integration` → `append_event` with `decision_type=version_derivation`; JSON event emitted; US-0103 composition correct.

### UAT-9 — Release notes generation — AC-9 — `verdict=PASS`

`pytest -k test_us0111_release_notes_generation` → `handoffs/releases/<version>-notes.md` generated atomically; US-0040 compose guard honored.

### UAT-10 — Contract tests — AC-10 — `verdict=PASS`

`pytest -k us0111` → **12/12** `test_us0111_*` markers PASS.

### UAT-11 — Parity + self-test — AC-10, AC-12 — `verdict=PASS`

`python scripts/check_intake_template_parity.py --scope=release-triggers` → `[INTAKE_TEMPLATE_PARITY_OK]` pairs=2. Lib self-test `[RELEASE_TRIGGER_SELF_TEST_OK]`.

### UAT-12 — Reason codes + runbook — AC-11, AC-12 — `verdict=PASS`

`python scripts/release_trigger_adapters.py --self-test` → lib self-test green. `docs/engineering/reason_codes.md` § US-0111 present with 9 codes: `ADAPTER_FAILED`, `INVALID_SOURCE`, `PARSE_PAYLOAD_FAILED`, `MISSING_TAG`, `MISSING_PREVIOUS`, `RATE_LIMITED`, `VERSION_FORMAT_INVALID`, `UNKNOWN_ADAPTER`, `COMPOSE_GUARD_VIOLATION`. Runbook § Release Triggers (US-0111) present (operator recipe procedural attestation).

## AC ↔ UAT results summary

AC-1..AC-12 verified at verify-work via UAT-1..UAT-12 (all PASS). UAT-12 satisfies AC-11 (runbook) and AC-12 (reason codes) via **procedural attestation** per runbook § Release Triggers.

## Next

- **`/release`** for **`S0111`** / **`US-0111`**.
- UAT artifacts now correctly reflect US-0111 deliverables (release trigger adapters), not US-0110 sovereign convergence artifacts.
