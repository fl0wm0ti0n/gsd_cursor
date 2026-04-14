# Release notes — Sprint S0071 / US-0087 (finalized)

**In-repo package version**: `its-magic@0.1.2-41` (unchanged from prior release; this sprint is **documentation/orchestration contract** delivery).

**Release finalization**: `2026-04-12T19:05:00Z` (`orchestrator_run_id=auto-20260405-01`, strict proof `proof_hash=b453b8901b083fb927dc73cfea54655f4e4ea1a703c4f1ea3e5cb420e6c4b215`)

## Summary

Ships **explicit bug-targeting** for **`/auto`**: canonical argv literals **`bug-target=BUG-####`** and **`bug-target=all-open`**, scratchpad **`AUTO_BUG_*`** keys (default-off), scheduler mutex **`AUTO_SCHEDULER_CONFLICT`** vs **`AUTO_BACKLOG_DRAIN`**, fail-closed resume codes, **AC-10** segment fields (**`segment_work_item_kind`**, **`active_bug_id`**, queue cursors), and contract tests plus **active/`template/`** parity.

## Operator-visible changes

- **`.cursor/commands/auto.md`** + **`template/.cursor/commands/auto.md`**: bug-queue semantics, spawn-only cross-refs (**`BUG-0006`**, **`US-0069`**).
- **`docs/engineering/auto-orchestration-reference.md`** (+ template mirror): normative **Optional bug-queue mode (US-0087)**.
- **`docs/engineering/architecture.md`**: **`# US-0087`** interaction matrix.
- **`docs/engineering/runbook.md`**: **Targeted bug auto drain (US-0087)** operator subsection.
- **`.cursor/scratchpad.md`** / **`template/`** examples: **`AUTO_BUG_*`** catalog; materialized baseline retains **`RELEASE_PUBLISH_MODE=confirm`**.
- **Tests**: **`tests/auto_command_contract_test.py`** markers and parity checks.

## Gate summary (US-0039)

- **Check-in test**: **PASS** — **`tests/report.md`** **794**/0 @ **2026-04-12T18:54:35Z**; **`python scripts/check-scratchpad-pair-parity.py --repo .`** → **`[SCRATCHPAD_PAIR_OK]`**; **`python scripts/check-user-visible-metadata.py`** **PASS**.
- **QA**: **PASS** — **`sprints/S0071/qa-findings.md`**; no blocking findings at release boundary.
- **UAT**: **PASS** — **`sprints/S0071/uat.json`** / **`uat.md`** **10**/10 **`pass`** (verify-work **2026-04-12**).
- **Isolation / strict proof**: **PASS** — lifecycle isolation + **DEC-0038** tuples through **verify-work**; **release** tuple in **`docs/engineering/state.md`**.
- **Publish**: **skipped** — **`RELEASE_PUBLISH_MODE=confirm`** requires explicit operator approval before any **`RELEASE_TARGETS_FILE`** execution (**US-0054** / **DEC-0036**); no registry publish this boundary.

## Run

- `start_command`: `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` (canonical **`TEST_COMMAND`** from `docs/engineering/runbook.md`).
- `runtime_mode`: `local` (docs + CLI installer repo; no long-running app service).
- `runtime_context_ref`: `docs/engineering/runbook.md`

## Connect

- `service_url`: `n/a`
- `service_port`: `n/a`
- `health_endpoint`: `n/a`

## Verify

1. `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` → **`tests/report.md`** green.
2. `python -m pytest tests/auto_command_contract_test.py -q` — contract markers for **US-0087** / argv literals / scheduler conflict.
3. `python scripts/check-scratchpad-pair-parity.py --repo .` → **`[SCRATCHPAD_PAIR_OK]`**.
4. `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` → **`[BUG_VALIDATION_OK]`**.
5. `python scripts/enforce-triad-hot-surface.py --check` — **PASS** after **`state.md`** checkpoint append (rollover if required).

`expected_health_signal`: Harness **PASS**; parity and bug-acceptance validators **OK**.

## Credentials

- `credential_source_refs`: **No** inline secrets. Publish targets (if ever run) use env-referenced fields per **`docs/engineering/release-targets.json`** and **`RELEASE_PUBLISH_MODE`**.

## Known Issues

- **Behavioral orchestrator** in Cursor still interprets these docs; tests lock **literals and parity**, not live scheduling.
- **Registry publish**: not executed; set **`RELEASE_PUBLISH_MODE=auto`** only with explicit governance if automating.

## Deploy (staging / production)

- **Staging / production**: per `docs/engineering/runbook.md` **`DEPLOY_*`** — placeholder echo commands for this repository.
- **npm**: **`npm publish`** only after operator confirmation when **`RELEASE_PUBLISH_MODE`** allows, **`npm run prepublishOnly`** **PASS**, and registry auth via env/CI secrets only.
