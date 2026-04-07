# QA findings — Sprint S0070 (BUG-0008)

- **Verdict**: **PASS_WITH_DEFERRALS**
- **Orchestrator run (plan segment)**: **`auto-20260404-03`**
- **Latest QA pass**: **`2026-04-05T16:00:00Z`** — operator directive: **skip Debian global install / E2E** for this cycle (**no Debian / SSH / Docker-over-SSH connection method available**); documented as **`DEFERRED_DEBIAN_E2E_NO_RUNTIME`** (not a false PASS of **AC-5** execution — **waiver** for **`/verify-work`** / **`/release`** when product accepts).
- **Prior QA re-validation**: **`2026-04-04T21:00:00Z`** (post **`RELEASE_TEST_FAILED` remediation**)

## Rationale (2026-04-05)

- **In-repo / automated scope for BUG-0008**: **PASS** — guards, **26P2**, **`bug_issue_validate --check-acceptance`**, **`tests/report.md`** **793/0** @ **2026-04-05T20:21:40Z** (**`TEST_COMMAND`** this QA pass), **`enforce-triad-hot-surface.py --check`** after **`state.md`** append + rollover.
- **AC-5 (Debian global E2E)**: **Explicitly not executed** — operator requested skip; no fabricated transcripts. **Waiver path**: **`sprints/S0070/qa-findings.md`** (this file) + operator chat record; follow-on automation selection is **US-0086** (**`docs/product/backlog.md`**). **Do not** claim **`cat -A`** / global **`npm install -g`** was run without real logs.
- **AC-6**: **`RELEASE_PUBLISH_MODE=disabled`** — registry publish not required for **`/release`** publish-target step (**`.cursor/commands/release.md`** §16).
- **US-0045**: **`BUG-0008`** remains **OPEN** until **`/release`** (or backlog edit) marks **DONE**; **`docs/product/acceptance.md`** **BUG-0008** unchecked until then; **`R-0069`** delivery closure only after **DONE** + **`/refresh-context`** per architecture.

## Rationale (2026-04-04, historical)

- **In-repo / automated scope for BUG-0008**: **PASS** — guards, tarball manifest CR scan, regression module, **`bug_issue_validate --check-acceptance`**, triad **`enforce-triad-hot-surface.py --check`** (**PASS** pre-append); post-QA **`state.md`** append triggered **`ARTIFACT_HOT_SURFACE_OVERSIZE`** → **`--rollover`** **`docs/engineering/state-archive/state-pack-20260404-p.md`** → final **`--check`** **PASS** (**DEC-0054**); full Windows harness **`tests/report.md`** now **794** pass / **0** fail — **§26P** (**`installer_shell_bug0004_test`**) **green** after dev **`write_installed_version`** / fixture / report-writer fixes; **§26P2** remains **PASS**.
- **Canonical backlog (US-0045)**: **`BUG-0008` remains OPEN** until release closure.
- **Deferrals (pre-2026-04-05)**: **AC-5** / **AC-6** as originally scoped.

## Test plan (executed, 2026-04-05)

1. **`python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance`**
2. **`python scripts/enforce-triad-hot-surface.py --check`** (pre-**`state.md`** append for this QA block)
3. **`TEST_COMMAND`**: **`powershell -ExecutionPolicy Bypass -File tests/run-tests.ps1`** → **`tests/report.md`** **793** / **0**, **2026-04-05T20:21:40Z**
4. **`python scripts/check-user-visible-metadata.py`** when present (runbook **US-0071**)

## Command outcomes (2026-04-05)

| Command | Outcome | Notes |
|---------|---------|-------|
| `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` | **PASS** | `[BUG_VALIDATION_OK]` |
| `python scripts/enforce-triad-hot-surface.py --check` (pre-state-append) | **PASS** | — |
| `tests/report.md` (after `TEST_COMMAND`) | **PASS** | **793** / **0** @ **2026-04-05T20:21:40Z** |
| `python scripts/check-user-visible-metadata.py` | **run if exists** | see runbook |

## Findings

1. **BUG-0008 mitigations**: **Verified** in-repo (unchanged bar).
2. **Debian E2E**: **Skipped by operator directive** — **`DEFERRED_DEBIAN_E2E_NO_RUNTIME`**; **`/verify-work`** may map **UAT-5** to **pass** with **waiver** + this **`evidence_ref`** only if product accepts; otherwise keep **fail** until real E2E exists.
3. **Next**: **`/release`** when remaining gates green (**`uat.json`** / **`uat.md`** reconciled **2026-04-05** with **UAT-5** waiver + **UAT-7** pre-release notes); optional duplicate **`/verify-work`** if policy requires.

## Evidence refs

- This file — **`DEFERRED_DEBIAN_E2E_NO_RUNTIME`** (**2026-04-05T16:00:00Z**)
- `handoffs/dev_to_qa.md` (S0070 / BUG-0008)
- `sprints/S0070/sprint.md`, `sprints/S0070/tasks.md`, `sprints/S0070/uat.json`, `sprints/S0070/uat.md`
- `package.json`, `its_magic/.its-magic-version`, `README.md`, `template/README.md`
- `handoffs/releases/S0070-release-notes.md`, `handoffs/release_queue.md`
- `tests/report.md` (**2026-04-04T20:25:29Z**)
- `.cursor/scratchpad.md` (**`RELEASE_PUBLISH_MODE=disabled`**)
- `docs/product/backlog.md` — **US-0086** (future remote execution selection)
