# Dev → QA Handoff — S0090 / US-0100

> **2026-06-15T05:00:00Z** — **`/execute`** **PASS** in fresh **dev** context (`orchestrator_run_id=auto-20260615-01`, `fresh_context_marker=dev-S0090-US0100-execute-20260615T050000Z-fresh`, `runtime_proof_id=rp-auto-20260615-01-execute-dev-20260615T050000Z-S0090-US0100`, `proof_hash=5e2e2353bdb546ad3fe86b2476e92a6eb8fe44bcb4da05597df02bb1a9b4313f`). **T-001..T-012** complete. Story **`US-0100`** remains **OPEN** (**US-0045**). Next phase: **`/qa`** (fresh **qa** subagent).

## Sprint anchor

- **Sprint**: `sprints/S0090/sprint.md`
- **Tasks**: `sprints/S0090/tasks.md` (all done)
- **Summary**: `sprints/S0090/summary.md`
- **Plan-verify**: `sprints/S0090/plan-verify.json` (**PASS**)
- **Binding decision**: `decisions/DEC-0085.md`
- **Architecture**: `docs/engineering/architecture.md` `# US-0100`

## Scope delivered

Version-scoped release documentation per **DEC-0085**:

- Cumulative **`CHANGELOG.md`** stub (Keep a Changelog 1.1.0 + `[Unreleased]`)
- **`scripts/release_changelog_lib.py`** — nine API symbols, L4 derivation, coalesce, fingerprint idempotency, queue bind
- **`scripts/release_changelog_validate.py`** — ten fail-closed `RELEASE_CHANGELOG_*` codes + `--enforce`
- **`scripts/release_changelog_backfill.py`** — Tier A/B/C backfill + `--ensure-version` for publish
- **`/release`** step **19** (19a–19d) active + template parity
- **`scripts/release-all.sh`** — `-F` per-version notes, validate preflight, fail-closed `RELEASE_CHANGELOG_VERSION_DOC_MISSING`
- Runbook § **Version-scoped release docs (US-0100)**
- Ten **`test_us0100_*`** contract subtests + harness **§26Y** + **`RELEASE_CHANGELOG_PAIRS`**

## QA verification commands

1. `pytest -k us0100 tests/auto_command_contract_test.py -v` → expect **10 passed**.
2. `python scripts/check_intake_template_parity.py --scope=release-changelog` → `[INTAKE_TEMPLATE_PARITY_OK]`.
3. `python scripts/release_changelog_validate.py --repo .` → `[RELEASE_CHANGELOG_VALIDATE_OK]` (non-enforce on fresh stub).
4. `python scripts/check-user-visible-metadata.py --repo .` → exit 0.
5. Confirm **`US-0100`** still **OPEN** in `docs/product/backlog.md` until **`/release`**.

## Test evidence (execute)

- `pytest -k us0100`: **10 passed**, 26 subtests
- Parity: `[INTAKE_TEMPLATE_PARITY_OK] scope=release-changelog`
- Metadata guard: exit 0
- Triad: rollover + check PASS (pre-append rollover)

## Scope guards (unchanged)

- Do **not** overwrite non-target **`Sxxxx-release-notes.md`** during QA/release.
- Do **not** pass sprint notes to **`gh -F`** — per-version semver file only.
- **`FRAMEWORK_KIT_REPO=1`**: execute step **23** README delta skipped (kit repo).

## Next

- **`/qa`** (fresh **qa**) for **`S0090`** / **US-0100**
