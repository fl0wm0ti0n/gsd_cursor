# Sprint S0070 UAT — BUG-0008 (CRLF installer manifest)

- **Sprint**: `S0070`
- **Work item**: **`BUG-0008`** — Global Linux install / empty `install_include_paths` when manifest is CRLF
- **Product acceptance row**: `docs/product/acceptance.md` — BUG-0008 (**unchecked** until **US-0045** closure via **`/release`**)
- **State**: **populated** (**DEC-0009**) — reconciled **`2026-04-05T16:00:00Z`** (QA operator skip **AC-5** + honest **UAT-7** notes)
- **Machine-readable**: `sprints/S0070/uat.json`
- **Orchestrator (plan segment)**: `auto-20260404-03`

## Results summary

| Metric | Value |
|--------|-------|
| **Total steps** | 7 |
| **Passed** | 7 |
| **Failed** | 0 |
| **Overall UAT result** | **pass** |

## Steps (maps to `sprints/S0070/sprint.md` AC-1..AC-7)

| Step | AC | Result | Notes |
|------|-----|--------|--------|
| UAT-1 | AC-1 | pass | Semver **0.1.2-41** in `package.json` + `its_magic/.its-magic-version`; no lockfile. |
| UAT-2 | AC-2 | pass | `npm pack`, `prepublishOnly`, `guard_installer_publish`; tarball template manifest no `\r`. |
| UAT-3 | AC-3 | pass | README + template/README operator subsection (CRLF / upgrade). |
| UAT-4 | AC-4 | pass | `installer_manifest_crlf_bug0008_test.py` + section 26P2 (awk on PATH for non-skip). |
| UAT-5 | AC-5 | pass | **Waiver** — **`DEFERRED_DEBIAN_E2E_NO_RUNTIME`**: operator directed skip (no Debian/SSH/docker-over-SSH); **`sprints/S0070/qa-findings.md`** **2026-04-05T16:00:00Z**. Does **not** assert global Debian install was run. |
| UAT-6 | AC-6 | pass | **`RELEASE_PUBLISH_MODE=disabled`** in **`.cursor/scratchpad.md`** — **`/release`** skips publish targets (no-op) per **`.cursor/commands/release.md`** (**US-0054** / **DEC-0036**). Draft **`handoffs/releases/S0070-release-notes.md`**; **`handoffs/release_queue.md`** **S0070** re-evaluated at **`/release`**. |
| UAT-7 | AC-7 | pass | **Pre-release validation** — **`bug_issue_validate --check-acceptance`** OK; **`tests/report.md`** **793/0** @ **2026-04-05T20:21:40Z**; **`qa-findings.md`** **PASS_WITH_DEFERRALS**. **BUG-0008** still **OPEN**; **`acceptance.md`** unchecked until **`/release`** / **DONE**. **R-0069** delivery closure and final **`release-findings`** posture remain **post-`/release`** + **`/refresh-context`** — not claimed here. |

## Acceptance criteria traceability

- Sprint AC themes: **`docs/engineering/architecture.md`** **`# BUG-0008`**, **`sprints/S0070/sprint.md`**.
- Canonical bug status: **`docs/product/backlog.md`** **`### BUG-0008`** (**OPEN** until closure workflow).
- **AC-5**: **Waiver** documented; full Debian E2E still recommended when a runtime is available (**US-0086**).

## Readiness / next actions

1. **`/release`** when remaining release gates allow — **`BUG-0008`** / **`acceptance.md`** / **`R-0069`** per **US-0045** after publish path (if any) and closure.
2. **Optional**: run **Debian global E2E** when connection exists; add **`evidence_refs`** and refresh UAT if stricter evidence is required.
3. **`tests/report.md`**: **793/0** @ **2026-04-05T20:21:40Z** — latest **`TEST_COMMAND`** evidence this QA cycle.

## Governance refs

- `docs/engineering/architecture.md` (`# BUG-0008`)
- `docs/engineering/research.md` (`R-0069`)
- `sprints/S0070/release-findings.md` (re-run **`/release`** per current queue posture)
- `sprints/S0070/qa-findings.md` (**`DEFERRED_DEBIAN_E2E_NO_RUNTIME`**)
