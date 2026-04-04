# Decisions

## Current context pack (2026-04-05 — **`US-0084` DONE**; sprint **`S0069` released**; curator **`/refresh-context`** completed on **`auto-20260404-02`**; normative **`DEC-0070`**; **`R-0067`** delivery closed; canonical **bug** rows **`BUG-0001`..`BUG-0007`** all **DONE** (**no OPEN** in range per **`docs/product/backlog.md`**); next work discretionary **`/intake`** (next **US**) or idle until scheduled; prior **`S0068` / `BUG-0007`** (**`auto-20260404-01`**), **`BUG-0006` / `S0067`** (**`auto-20260403-03`**), **`BUG-0005` / `S0066`** (**`auto-20260403-02`**), **`BUG-0004` / `S0065`** (**`auto-20260403-01`**) remain released)

- **`US-0079`** (**DONE**, **`S0058`**, **released**): full lifecycle on **`auto-20260329-01`** — **`/release`** **PASS** **`2026-03-30`**; **`handoffs/release_queue.md`** **`S0058`** **`released`**; **`handoffs/releases/S0058-release-notes.md`**; curator **`/refresh-context`** **PASS** — **`docs/engineering/state.md`** **Refresh-context checkpoint (2026-03-30) — post S0058 / US-0079 (auto-20260329-01)** (`stop_reason=completed`, `next_scheduled_phase=none`); normative **`DEC-0061`**, **`architecture.md`** **`# US-0079`**, **`R-0056`** delivery closed.
- **`US-0078`** (**`S0057`**): **DONE** / **released**; evidence **`sprints/S0057/release-findings.md`**, **`handoffs/releases/S0057-release-notes.md`**, **`handoffs/release_queue.md`** row **`S0057`** **`released`**; **`docs/engineering/state.md`** **Refresh-context checkpoint (2026-03-29) — post S0057 / US-0078 (auto-20260328-01)** (`stop_reason=completed`, `next_scheduled_phase=none`, curator isolation + strict-proof tuple); release traceability **Release checkpoint (2026-03-29) — S0057 / US-0078 / auto-20260328-01**; governance **`DEC-0060`**, **`architecture.md`** **`# US-0078`**.
- **`US-0077`** (**`S0056`**): **DONE** / **released**; evidence **`sprints/S0056/release-findings.md`**, **`handoffs/releases/S0056-release-notes.md`**, **`## Refresh-context checkpoint (2026-03-28) — post S0056 / US-0077 (auto-20260327-02)`** in **`docs/engineering/state.md`** (`orchestrator_run_id=auto-20260327-02`, `stop_reason=completed`, `next_scheduled_phase=none`).
- Migration default: explicit scratchpad keys **`DOC_AUDIENCE_PROFILE`** / **`DOC_DETAIL_LEVEL`** recommended (`both` / `balanced`); **absent keys** on merged scratchpad resolve to **`both`×`balanced`** for resolver/tests per **DEC-0059** §6 until a future cutover mandates explicit keys in CI.
- **`US-0076`** (**`S0055`**): **DONE** / **released**; evidence **`sprints/S0055/release-findings.md`**, **`handoffs/releases/S0055-release-notes.md`**, **`## Refresh-context checkpoint (2026-03-27) — post S0055 / US-0076`** in **`docs/engineering/state.md`** (`orchestrator_run_id=auto-20260327-01`, `stop_reason=completed`).
- **`US-0080`** (**DONE**, **`S0059`**, **released**): full lifecycle on **`auto-20260329-02`** — **`/release`** **PASS** **`2026-03-29`**; **`handoffs/release_queue.md`** **`S0059`** **`released`**; **`handoffs/releases/S0059-release-notes.md`**; curator **`/refresh-context`** **PASS** — **`docs/engineering/state.md`** **Refresh-context checkpoint (2026-03-30) — post S0059 / US-0080 (auto-20260329-02)** (`stop_reason=completed`, `next_scheduled_phase=none`); normative **`DEC-0062`**, **`architecture.md`** **`# US-0080`**, **`R-0057`** delivery closed.
- **`US-0081`** (**DONE**, **`S0061`**, **released**): full lifecycle on **`auto-20260331-01`** — **`/release`** **PASS** **`2026-03-31`**; **`handoffs/release_queue.md`** **`S0061`** **`released`**; **`handoffs/releases/S0061-release-notes.md`**; curator **`/refresh-context`** **PASS** — **`docs/engineering/state.md`** **Refresh-context checkpoint (2026-03-31) — S0061 / US-0081 / auto-20260331-01** (`stop_reason=completed`, `next_scheduled_phase=none`); normative **`DEC-0064`**, **`architecture.md`** **`# US-0081`**, **`R-0059`** delivery closed.
- **`US-0082`** (**DONE**, **`S0062`**, **released**): full lifecycle on **`auto-20260331-02`** — **`/release`** **PASS** **`2026-03-31`**; **`handoffs/release_queue.md`** **`S0062`** **`released`**; **`handoffs/releases/S0062-release-notes.md`**; curator **`/refresh-context`** **PASS** — **`docs/engineering/state.md`** **Refresh-context checkpoint (2026-03-31) — S0062 / US-0082 / auto-20260331-02** (`stop_reason=completed`, `next_scheduled_phase=none`); normative **`DEC-0065`**, **`architecture.md`** **`# US-0082`**, **`R-0060`** delivery closed.
- **`BUG-0001`** (**DONE**, **`S0060`**, **released**): full defect lifecycle on **`auto-20260330-01`** — **`/release`** **PASS** **`2026-03-30`**; **`handoffs/release_queue.md`** **`S0060`** **`released`**; **`handoffs/releases/S0060-release-notes.md`**; curator **`/refresh-context`** **PASS** — **`docs/engineering/state.md`** **Refresh-context checkpoint (2026-03-30) — S0060 / BUG-0001 / auto-20260330-01** (`stop_reason=completed`, `next_scheduled_phase=none`); normative **`DEC-0063`**, **`architecture.md`** **`# BUG-0001`**, **`R-0058`** delivery closed. Sprint artifacts **`sprints/S0060/*`**.
- **`BUG-0003`** (**DONE**, **`S0063`**, **released**): full defect lifecycle on **`auto-20260331-03`** — **`/release`** **PASS** **`2026-03-31`**; **`handoffs/release_queue.md`** **`S0063`** **`released`**; **`handoffs/releases/S0063-release-notes.md`**; curator **`/refresh-context`** closure captured in **`docs/engineering/state.md`** with `stop_reason=completed` and `next_scheduled_phase=none`; normative **`DEC-0066`**, **`architecture.md`** **`# BUG-0003`**, **`R-0061`** delivery closed.
- **`US-0083`** (**DONE**, **`S0064`**, **released**): full lifecycle on **`auto-20260331-04`** — **`/release`** **PASS** **`2026-03-31`**; **`handoffs/release_queue.md`** **`S0064`** **`released`**; **`handoffs/releases/S0064-release-notes.md`**; curator **`/refresh-context`** reconciliation completed (**`2026-04-01T01:15:55Z`**) with closure posture aligned in sprint/research/resume artifacts; normative **`DEC-0067`**, **`docs/engineering/architecture.md`** **`# US-0083`**, **`R-0062`** delivery closed.
- **`BUG-0004`** (**DONE**, **`S0065`**, **released**): full defect lifecycle on **`auto-20260403-01`** — **`/release`** **PASS** **`2026-04-03`**; **`handoffs/release_queue.md`** **`S0065`** **`released`**; **`handoffs/releases/S0065-release-notes.md`**; curator **`/refresh-context`** **PASS** — **`docs/engineering/state.md`** **Refresh-context checkpoint (2026-04-03) — S0065 / BUG-0004 / auto-20260403-01** (`stop_reason=completed`, `next_scheduled_phase=discovery` in auto-stop breadcrumb); normative **`DEC-0068`**, **`architecture.md`** **`# BUG-0004`**, **`R-0063`** delivery closed.
- **`BUG-0005`** (**DONE**, **`S0066`**, **released**): full defect lifecycle on **`auto-20260403-02`** — **`/release`** **PASS** **`2026-04-03T23:30:45Z`**; **`handoffs/release_queue.md`** **`S0066`** **`released`**; **`handoffs/releases/S0066-release-notes.md`**; curator **`/refresh-context`** reconciliation (**`2026-04-03T23:55:00Z`**) closes **`R-0064`** and aligns resume to **`BUG-0006`** / **`discovery`**; normative **`DEC-0069`**, **`architecture.md`** **`# BUG-0005`**, **`R-0064`** delivery closed.
- **`BUG-0006`** (**DONE**, **`S0067`**, **released**): full defect lifecycle on **`auto-20260403-03`** — **`/release`** **PASS** **`2026-04-04T09:00:00Z`**; **`handoffs/release_queue.md`** **`S0067`** **`released`**; **`handoffs/releases/S0067-release-notes.md`**; curator **`/refresh-context`** reconciliation (**`2026-04-04T10:30:00Z`**) closes **`R-0065`** and aligns resume to **`BUG-0007`** / **`discovery`**; normative **`architecture.md`** **`# BUG-0006`**, **`R-0065`** delivery closed (doc + test contract; no standalone **`DEC-00xx`** file).
- **`BUG-0007`** (**DONE**, **`S0068`**, **released**): full defect lifecycle on **`auto-20260404-01`** — **`/release`** **PASS** **`2026-04-05T00:10:00Z`**; **`handoffs/release_queue.md`** **`S0068`** **`released`**; **`handoffs/releases/S0068-release-notes.md`**; curator **`/refresh-context`** reconciliation (**`2026-04-05T01:30:00Z`**) closes **`R-0066`** and aligns **`handoffs/resume_brief.md`** to **`/intake`** (next **US**; portfolio **BUG-0001..BUG-0007** all **DONE**); normative **`architecture.md`** **`# BUG-0007`**, **`R-0066`** delivery closed (**`intake_evidence_lib.py`**, **`intake.md`**, **`tests/intake_evidence_bug0007_r0066_test.py`**; no standalone **`DEC-00xx`** file).
- **`US-0084`** (**DONE**, **`S0069`**, **released**): full lifecycle on **`auto-20260404-02`** — **`/release`** **PASS** **`2026-04-05T00:10:00Z`**; **`handoffs/release_queue.md`** **`S0069`** **`released`**; **`handoffs/releases/S0069-release-notes.md`**; curator **`/refresh-context`** reconciliation (**`2026-04-05T01:30:00Z`**) closes **`R-0067`** and aligns **`handoffs/resume_brief.md`** to **`/intake`** (next **US**; bug portfolio idle **BUG-0001..BUG-0007** **DONE**); normative **`DEC-0070`**, **`architecture.md`** **`# US-0084`**, **`R-0067`** delivery closed (**`guard_installer_publish.py`**, **`remote_config_summary.py`**, **`tests/installer_shell_bug0004_test.py`**, **`tests/remote_config_summary_test.py`**).
- Research: **`R-0053`** (closed with **US-0076**); **`R-0054`** — retained for **US-0077** matrix traceability; normative lock-in **`DEC-0059`** + **`architecture.md`** **`# US-0077`** (delivery closure noted in **`docs/engineering/research.md`**). **`R-0055`** — **US-0078** delivery closed **2026-03-29** with **`S0057`** + **`DEC-0060`** / **`# US-0078`**. **`R-0056`** — **US-0079** delivery closed **2026-03-30** with **`S0058`** + **`DEC-0061`** / **`# US-0079`**. **`R-0057`** — **US-0080** delivery closed **2026-03-30** with **`S0059`** + **`DEC-0062`** / **`# US-0080`**. **`R-0058`** — **BUG-0001** delivery closed **2026-03-30** with **`S0060`** + **`DEC-0063`** / **`# BUG-0001`** (curator **`/refresh-context`** on **`auto-20260330-01`**). **`R-0059`** — **US-0081** delivery closed **2026-03-31** with **`S0061`** + **`DEC-0064`** / **`# US-0081`** (curator **`/refresh-context`** on **`auto-20260331-01`**). **`R-0060`** — **US-0082** delivery closed **2026-03-31** with **`S0062`** + **`DEC-0065`** / **`# US-0082`** (curator **`/refresh-context`** on **`auto-20260331-02`** **`2026-03-31T21:50:00Z`**). **`R-0061`** — **BUG-0003** delivery closed **2026-03-31** with **`S0063`** + **`DEC-0066`** / **`# BUG-0003`** (curator **`/refresh-context`** on **`auto-20260331-03`**). **`R-0062`** — **US-0083** delivery closed **2026-04-01** with **`S0064`** + **`DEC-0067`** / **`# US-0083`** (curator **`/refresh-context`** on **`auto-20260331-04`** **`2026-04-01T01:15:55Z`**). **`R-0063`** — **BUG-0004** delivery closed **2026-04-03** with **`S0065`** + **`DEC-0068`** / **`# BUG-0004`** (curator **`/refresh-context`** on **`auto-20260403-01`**). **`R-0064`** — **BUG-0005** delivery closed **2026-04-03** with **`S0066`** + **`DEC-0069`** / **`# BUG-0005`** (curator **`/refresh-context`** on **`auto-20260403-02`** **`2026-04-03T23:55:00Z`**). **`R-0065`** — **BUG-0006** delivery closed **2026-04-04** with **`S0067`** + **`architecture.md`** **`# BUG-0006`** + **`tests/auto_command_contract_test.py`** (curator **`/refresh-context`** on **`auto-20260403-03`** **`2026-04-04T10:30:00Z`**). **`R-0066`** — **BUG-0007** delivery closed **2026-04-05** with **`S0068`** + **`architecture.md`** **`# BUG-0007`** + **`tests/intake_evidence_bug0007_r0066_test.py`** (curator **`/refresh-context`** on **`auto-20260404-01`** **`2026-04-05T01:30:00Z`**). **`R-0067`** — **US-0084** delivery closed **2026-04-05** with **`S0069`** + **`DEC-0070`** / **`architecture.md`** **`# US-0084`** + **`scripts/guard_installer_publish.py`**, **`scripts/remote_config_summary.py`**, harness **H1–H5** (curator **`/refresh-context`** on **`auto-20260404-02`** **`2026-04-05T01:30:00Z`**).
- Decision: **`DEC-0062`** — **`US-0080`** token-cost metrics, **`run_class_hash`**, **`handoffs/token_cost_runs/`**, parity manifest, AC-10 trade-offs — see **`decisions/DEC-0062.md`** and **`docs/engineering/architecture.md`** **`# US-0080`**.
- Decision: **`DEC-0063`** — **`BUG-0001`** intake gate script ship path (**`template/scripts/`** minimal mirror, **`package.json` `files`**, parity tests, **`US-0018`**) — see **`decisions/DEC-0063.md`** and **`docs/engineering/architecture.md`** **`# BUG-0001`**.
- Decision: **`DEC-0064`** — **`US-0081`** deterministic first-intake full-plan coverage gate (**`plan_area_inventory`**, **`plan_area_coverage`**, fail-closed `INTAKE_PERSISTENCE_BLOCKED` + subcodes, parity/fixture verification) — see **`decisions/DEC-0064.md`** and **`docs/engineering/architecture.md`** **`# US-0081`**.
- Decision: **`DEC-0066`** — **`BUG-0003`** deterministic installer completeness in `missing`/`upgrade` (manifest-authoritative required script inventory, post-install diagnostics, parity/symmetry tests) — see **`decisions/DEC-0066.md`** and **`docs/engineering/architecture.md`** **`# BUG-0003`**.
- Decision: **`DEC-0067`** — **`US-0083`** explicit topic-scoped intake delegation (`satisfied_by=delegation_ref` + bounded delegation fields), deterministic delegation fail codes under `INTAKE_PERSISTENCE_BLOCKED`, guided/low-touch parity, and DEC-0060-compatible `ie:` evidence binding — see **`decisions/DEC-0067.md`** and **`docs/engineering/architecture.md`** **`# US-0083`**.
- Decision: **`DEC-0068`** — **`BUG-0004`** POSIX-safe installer shell startup under Unix CLI `sh` invocation contract (`bin/its-magic.js`), with deterministic `sh` + CLI regression obligations and no forced bash dependency — see **`decisions/DEC-0068.md`** and **`docs/engineering/architecture.md`** **`# BUG-0004`**.
- Decision: **`DEC-0069`** — **`BUG-0005`** deterministic **`handoffs/resume_brief.md`** refresh at successful bug-intake persistence (default **`discovery`** continuation), preserved **`/auto` resume precedence** and fail-fast on stale/unparseable briefs, optional future self-heal gated — see **`decisions/DEC-0069.md`** and **`docs/engineering/architecture.md`** **`# BUG-0005`**.
- Decision: **`DEC-0059`** — profile semantics, **`docs/developer/README.md`** shard, H2 mapping, validator **`scripts/validate_doc_profile.py`**, tiered **AC-8** tests, migration defaults — see **`decisions/DEC-0059.md`** and **`docs/engineering/architecture.md`** **`# US-0077`**.
- Decision: **`DEC-0065`** — **`US-0082`** codebase map bootstrap lifecycle (**`/architecture`** primary gate, optional **`/refresh-context`**, **`/map-codebase`** manual; idempotency; **`CODEBASE_MAP_*`** diagnostics; parity) — see **`decisions/DEC-0065.md`** and **`docs/engineering/architecture.md`** **`# US-0082`**.
- Continuation hygiene: **`handoffs/resume_brief.md`** routes to **`/intake`** (next **US**) after curator **`/refresh-context`** on **`auto-20260404-02`** (**`S0069`** / **`US-0084`**) — canonical **bug** portfolio **`BUG-0001`..`BUG-0007`** **DONE** (**no OPEN** in range); prior released evidence unchanged for **`S0068`** / earlier sprints.
- Latest completed/released stories (high-signal, unchanged):
  - `US-0075` (`S0054`, released), governed by **`DEC-0057`** (scratchpad **example-first**
    upgrade ordering + **`AC-11`** paired baseline ↔ example catalog parity gate;
    **`DEC-0039`** / **`DEC-0055`** alignment).
  - `US-0074` (`S0053`, released), governed by **`DEC-0056`** (baseline version-sync +
    `TEST_COMMAND` bootstrap; npm ↔ Homebrew stable; triple installer + CLI + `template/`
    parity).
  - `US-0073` (`S0052`, released), governed by **`DEC-0055`** (scratchpad Model B).
  - `US-0072` (`S0051`, released), governed by **`DEC-0054`** (triad hot-surface compaction).
  - `US-0071` (`S0050`, released), governed by **`DEC-0053`** (user-visible metadata guard).
  - `US-0070` (`S0049`, released), governed by **`DEC-0052`**.
  - `US-0069` (`S0048`, released), governed by **`DEC-0051`**.
- Hot surface: latest **`/refresh-context` (2026-04-05)** post-**`S0069`** / **`US-0084`** on **`auto-20260404-02`** (decisions/research/sprint summary/resume alignment; **`R-0067`** closed; **`DEC-0070`**). Prior: post-**`S0068`** / **`BUG-0007`** (**`auto-20260404-01`**); post-**`S0067`** / **`BUG-0006`** (**`auto-20260403-03`**); post-**`S0066`** / **`BUG-0005`** (**`auto-20260403-02`**); post-**`S0065`** / **`BUG-0004`** (**`auto-20260403-01`**).
- Traceability (**DEC-0010**):
  - `| US-0082 | S0062 | T-001..T-010 | DONE |` — **`DEC-0065`** + **`# US-0082`**; **`sprints/S0062/*`**;
    **`plan-verify.json`** **PASS**; **`sprints/S0062/uat.json`**, **`sprints/S0062/uat.md`** **PASS**;
    **`sprints/S0062/release-findings.md`**; **`handoffs/releases/S0062-release-notes.md`**;
    orchestrator **`auto-20260331-02`** closed at **`/refresh-context`**; **`handoffs/release_queue.md`** **`S0062`** **`released`**.
  - `| US-0081 | S0061 | T-001..T-010 | DONE |` — **`DEC-0064`** + **`# US-0081`**; **`sprints/S0061/*`**;
    **`plan-verify.json`** **PASS**; **`sprints/S0061/uat.json`**, **`sprints/S0061/uat.md`** **PASS**;
    **`sprints/S0061/release-findings.md`**; **`handoffs/releases/S0061-release-notes.md`**;
    orchestrator **`auto-20260331-01`** closed at **`/refresh-context`**; **`handoffs/release_queue.md`** **`S0061`** **`released`**.
  - `| US-0079 | S0058 | T-001..T-010 | DONE |` — **`DEC-0061`** + **`# US-0079`**; **`sprints/S0058/*`**;
    **`plan-verify.json`** **PASS**; **`sprints/S0058/uat.json`**, **`sprints/S0058/uat.md`** **PASS**;
    **`sprints/S0058/release-findings.md`**; **`handoffs/releases/S0058-release-notes.md`**;
    orchestrator **`auto-20260329-01`** closed at **`/refresh-context`**; **`handoffs/release_queue.md`** **`S0058`** **`released`**.
  - `| US-0080 | S0059 | T-001..T-010 | DONE |` — **`DEC-0062`** + **`# US-0080`**; **`sprints/S0059/*`**;
    **`plan-verify.json`** **PASS**; **`sprints/S0059/uat.json`**, **`sprints/S0059/uat.md`** **PASS**;
    **`sprints/S0059/release-findings.md`**; **`handoffs/releases/S0059-release-notes.md`**;
    orchestrator **`auto-20260329-02`** closed at **`/refresh-context`**; **`handoffs/release_queue.md`** **`S0059`** **`released`**.
  - `| BUG-0001 | S0060 | T-001..T-005 | DONE |` — **`DEC-0063`** + **`architecture.md`** **`# BUG-0001`**; **`sprints/S0060/*`**;
    **`plan-verify.json`** **PASS**; **`sprints/S0060/uat.json`**, **`sprints/S0060/uat.md`** **PASS**;
    **`sprints/S0060/release-findings.md`**; **`handoffs/releases/S0060-release-notes.md`**;
    orchestrator **`auto-20260330-01`** closed at **`/refresh-context`**; **`handoffs/release_queue.md`** **`S0060`** **`released`**.
  - `| BUG-0003 | S0063 | T-001..T-010 | DONE |` — **`DEC-0066`** + **`architecture.md`** **`# BUG-0003`**; **`sprints/S0063/*`**;
    **`plan-verify.json`** **PASS**; **`sprints/S0063/uat.json`**, **`sprints/S0063/uat.md`** **PASS**;
    **`sprints/S0063/release-findings.md`**; **`handoffs/releases/S0063-release-notes.md`**;
    orchestrator **`auto-20260331-03`** closed at **`/refresh-context`**; **`handoffs/release_queue.md`** **`S0063`** **`released`**.
  - `| BUG-0004 | S0065 | T-001..T-008 | DONE |` — **`DEC-0068`** + **`architecture.md`** **`# BUG-0004`**; **`sprints/S0065/*`**;
    **`plan-verify.json`** **PASS**; **`sprints/S0065/uat.json`**, **`sprints/S0065/uat.md`** **PASS**;
    **`sprints/S0065/release-findings.md`**; **`handoffs/releases/S0065-release-notes.md`**;
    orchestrator **`auto-20260403-01`** closed at **`/refresh-context`**; **`handoffs/release_queue.md`** **`S0065`** **`released`**.
  - `| BUG-0005 | S0066 | T-001..T-009 | DONE |` — **`DEC-0069`** + **`architecture.md`** **`# BUG-0005`**; **`sprints/S0066/*`**;
    **`plan-verify.json`** **PASS**; **`sprints/S0066/uat.json`**, **`sprints/S0066/uat.md`** **PASS**;
    **`sprints/S0066/release-findings.md`**; **`handoffs/releases/S0066-release-notes.md`**;
    orchestrator **`auto-20260403-02`** closed at **`/refresh-context`**; **`handoffs/release_queue.md`** **`S0066`** **`released`**.
  - `| BUG-0006 | S0067 | T-001..T-005 | DONE |` — **`architecture.md`** **`# BUG-0006`** + **`R-0065`**; **`sprints/S0067/*`**;
    **`plan-verify.json`** **PASS**; **`sprints/S0067/uat.json`**, **`sprints/S0067/uat.md`** **PASS**;
    **`sprints/S0067/release-findings.md`**; **`handoffs/releases/S0067-release-notes.md`**;
    orchestrator **`auto-20260403-03`** closed at **`/refresh-context`**; **`handoffs/release_queue.md`** **`S0067`** **`released`**.
  - `| BUG-0007 | S0068 | T-001..T-006 | DONE |` — **`architecture.md`** **`# BUG-0007`** + **`R-0066`**; **`sprints/S0068/*`**;
    **`plan-verify.json`** **PASS**; **`sprints/S0068/uat.json`**, **`sprints/S0068/uat.md`** **PASS**;
    **`sprints/S0068/release-findings.md`**; **`handoffs/releases/S0068-release-notes.md`**;
    orchestrator **`auto-20260404-01`** closed at **`/refresh-context`**; **`handoffs/release_queue.md`** **`S0068`** **`released`**.
  - `| US-0084 | S0069 | T-001..T-010 | DONE |` — **`DEC-0070`** + **`architecture.md`** **`# US-0084`** + **`R-0067`**; **`sprints/S0069/*`**;
    **`plan-verify.json`** **PASS**; **`sprints/S0069/uat.json`**, **`sprints/S0069/uat.md`** **PASS**;
    **`sprints/S0069/release-findings.md`**; **`handoffs/releases/S0069-release-notes.md`**;
    orchestrator **`auto-20260404-02`** closed at **`/refresh-context`**; **`handoffs/release_queue.md`** **`S0069`** **`released`**.
  - `| US-0078 | S0057 | T-001..T-010 | DONE |` — **`DEC-0060`** + **`# US-0078`**; **`sprints/S0057/*`**;
    **`plan-verify.json`** **PASS**; **`sprints/S0057/uat.json`**, **`sprints/S0057/uat.md`** **PASS**;
    **`sprints/S0057/release-findings.md`**; **`handoffs/releases/S0057-release-notes.md`**;
    orchestrator **`auto-20260328-01`** closed at **`/refresh-context`**; **`handoffs/release_queue.md`** **`S0057`** **`released`**.
  - `| US-0077 | S0056 | T-001..T-010 | DONE |` — **`DEC-0059`** + **`# US-0077`**; sprint artifacts
    **`sprints/S0056/*`**; **`plan-verify.json`** **PASS**; **`sprints/S0056/release-findings.md`**;
    **`handoffs/releases/S0056-release-notes.md`**; orchestrator **`auto-20260327-02`** closed at **`/refresh-context`**.
  - `| US-0076 | S0055 | T-001..T-010 | DONE |` — evidence in `sprints/S0055/summary.md`,
    `sprints/S0055/qa-findings.md`, `sprints/S0055/uat.json`, `sprints/S0055/uat.md`,
    `sprints/S0055/release-findings.md`, `handoffs/releases/S0055-release-notes.md`,
    `tests/report.md`, `decisions/DEC-0058.md`, `scripts/sync_push_gates.py`,
    `scripts/validate-and-push.ps1`, `scripts/validate-and-push.sh`.
  - `| US-0075 | S0054 | T-001..T-011 | DONE |` — evidence in `sprints/S0054/summary.md`,
    `sprints/S0053/qa-findings.md`, `sprints/S0053/uat.json`, `sprints/S0053/uat.md`,
    `sprints/S0053/release-findings.md`, `handoffs/releases/S0053-release-notes.md`,
    `tests/report.md`, `decisions/DEC-0056.md`, `scripts/enforce-triad-hot-surface.py`.
  - `| US-0073 | S0052 | T-001..T-010 | DONE |` — prior sprint evidence unchanged
    (`sprints/S0052/*`, `handoffs/releases/S0052-release-notes.md`).

## Compact decision index (bounded summaries)

- `DEC-0067`: **explicit topic-scoped intake delegation (`US-0083`)** — extend `topic_coverage.satisfied_by` with `delegation_ref`; require `delegation_scope`, `delegation_rationale`, `delegation_confidence`, and DEC-0060-compatible `ie:` evidence binding; preserve non-delegated fail-closed path and add deterministic delegation diagnostics (`INTAKE_DELEGATION_EVIDENCE_MISSING`, `INTAKE_DELEGATION_EVIDENCE_INVALID`) under `INTAKE_PERSISTENCE_BLOCKED`; guided/low-touch parity; **`R-0062`** basis; architecture **`# US-0083`**.
- `DEC-0068`: **POSIX-safe installer startup (`BUG-0004`)** — keep Unix CLI invocation via `sh installer.sh`, prohibit unconditional bash-only `set` flags in startup path, and require deterministic direct-`sh` + CLI regression coverage for `missing`/`upgrade` compatibility; **`R-0063`** basis; architecture **`# BUG-0004`**.
- `DEC-0069`: **bug-intake `resume_brief` refresh (`BUG-0005`)** — on successful canonical bug intake persistence, intake writer atomically refreshes **`handoffs/resume_brief.md`** with **`bug_id`**, default **`intended_resume_phase=discovery`**, boundary metadata, and **`US-0045`** alignment; explicit **`start-from`** > parseable brief > **`state.md`** fallback unchanged; **`RESUME_BRIEF_STALE`** / unparseable fail-fast preserved; optional orchestrator self-heal deferred behind strict gates; **`R-0064`** basis; architecture **`# BUG-0005`**.
- **`BUG-0006` (`S0067`)**: **spawn-only `/auto` + `AUTO_ORCHESTRATOR_PHASE_EXECUTION`** — orchestrator must not execute phase work in-process; doc-first contract on active + template **`auto.md`**, **`auto-orchestration-reference.md`**, static regression **`tests/auto_command_contract_test.py`**; normative **`architecture.md`** **`# BUG-0006`**; **`R-0065`** basis (delivery closed **`auto-20260403-03`**).
- **`BUG-0007` (`S0068`)**: **intake evidence asked-vs-covered truthfulness** — **`INTAKE_ANSWER_REF_NOT_TOPIC_DISTINCT`** in **`intake_evidence_lib.py`** (+ **`template/`** parity), active + template **`intake.md`**, **`tests/intake_evidence_bug0007_r0066_test.py`**; normative **`architecture.md`** **`# BUG-0007`**; **`R-0066`** basis (delivery closed **`auto-20260404-01`** curator **`/refresh-context`** **`2026-04-05T01:30:00Z`**).
- **`DEC-0070` / `US-0084` (`S0069`)**: **POSIX npm `installer.sh` + publish guard + remote config helper** — **`.gitattributes`** (**LF** **`*.sh`**), **`scripts/guard_installer_publish.py`**, **`scripts/remote_config_summary.py`** (**`REMOTE_EXECUTION=0`** → exit **0**, stderr skip per **`decisions/DEC-0070.md`**), extended **`tests/installer_shell_bug0004_test.py`**, **`tests/remote_config_summary_test.py`**, harness **H1–H5**; normative **`architecture.md`** **`# US-0084`**; **`R-0067`** basis (delivery closed **`auto-20260404-02`** curator **`/refresh-context`** **`2026-04-05T01:30:00Z`**).
- `DEC-0066`: **installer completeness contract for `missing`/`upgrade` (`BUG-0003`)** — manifest is single required-script source of truth (`installer-owned-paths.manifest`), required inclusion of `scripts/enforce-triad-hot-surface.py`, deterministic post-install checks with `INSTALL_COMPLETENESS_FAILED` / `INSTALL_REQUIRED_SCRIPT_MISSING:<path>`, parity-safe shared validator path across PS1/SH/PY, and positive/negative/symmetry regression scope; **`R-0061`** basis; architecture **`# BUG-0003`**.
- `DEC-0065`: **codebase map bootstrap lifecycle (`US-0082`)** — primary guarantee at **`/architecture`** completion (**tech-lead**); optional policy-gated **`/refresh-context`** refresh; **`/map-codebase`** manual; idempotent regeneration; ownership aligned with map command; deterministic **`CODEBASE_MAP_*`** diagnostics; active/**`template/`** parity + regression matrix; profile containment vs **DEC-0052**; **`R-0060`** basis; architecture **`# US-0082`**.
- `DEC-0064`: **first-intake full-plan coverage gate (`US-0081`)** — normalized **`plan_area_inventory`** + total **`plan_area_id -> story_ids[] | deferred_ref`** mapping required before persistence; fail-closed **`INTAKE_PERSISTENCE_BLOCKED`** family (**`INTAKE_PLAN_COVERAGE_MISSING`**, **`INTAKE_PLAN_AREA_ID_INVALID`**, **`INTAKE_PLAN_COVERAGE_CONTRACT_INVALID`**, **`INTAKE_PLAN_DEFERRED_REF_MISSING`**); guided/low-touch parity and active/**`template/`** fixture checks; **`R-0059`** basis; architecture **`# US-0081`**.
- `DEC-0063`: **intake script ship path (`BUG-0001`)** — three **`intake_*`** files under **`template/scripts/`** mirroring **`scripts/`**; **`package.json` `files`** (**`template/`** primary, optional explicit **`scripts/intake_*.py`**); deterministic parity tests; **`US-0018`** upgrade delivery; **`R-0058`** basis; architecture **`# BUG-0001`**.
- `DEC-0062`: **token-cost metrics + `run_class_hash` + evidence channel (`US-0080`)** — canonical
  fields **`cache_read_tokens`** / **`input_tokens`** / **`output_tokens`** / **`phase_call_count`** (+ optional
  **`cache_creation_tokens`**); **SHA-256** sorted-key JSON **`run_class_hash`** for AC-2 comparability;
  append-only **`handoffs/token_cost_runs/<orchestrator_run_id>.md`** (or **`.jsonl`**) + **`state.md`**
  **`token_cost_evidence_ref`**; parity manifest for **`.cursor/commands/`** / **`.cursor/rules/`** / **`template/`**;
  trade-off table + **`TOKEN_COST_RUN_CLASS_MISMATCH`**; phase boundary **`token_cost_evidence_ref`** (**AC-10**);
  **`R-0057`** basis; architecture **`# US-0080`**.
- `DEC-0061`: **first-class bug issues `BUG-xxxx` + `OPEN`/`DONE` (`US-0079`)** — canonical
  **`## Bug issues (canonical)`** in **`backlog.md`** (optional split per §2); allocator matches
  **`US-xxxx`** policy; minimum schema **environment** / **steps_to_reproduce** / **expected** /
  **actual** / **evidence_refs**; routing via **`INTAKE_WORK_ITEM_KIND`** and/or **`/intake bug`**;
  fail closed **`INTAKE_BUG_ROUTING_REQUIRED`** / mismatch family; **`## Bug acceptance (canonical)`**
  in **`acceptance.md`**; validators **`scripts/bug_issue_validate.py`**, **`scripts/intake_bug_routing_guard.py`**,
  **`tests/bug_issue_fixtures_test.py`**; **`US-0045`** bug-family reconciliation; sprint/QA/release/**`/ask`**
  traceability; optional **`bug_ids`** on **`state.md`** phase boundaries (**US-0070** visibility);
  **`R-0056`** test tiers; architecture **`# US-0079`**.
- `DEC-0060`: **intake question-pack interactive evidence + `ie:` ref binding (`US-0078`)** —
  extends **`DEC-0050`** with mandatory **`topic_coverage`** rows, **`satisfied_by`**, canonical **`ref`**
  (`ie:<intake_run_id>:<turn_index>:<sha256_16>` over sorted-key JSON), asked-vs-covered default
  fail-closed, assumption **`assumption_confirmation_ref`**, mode parity (**guided** / **low-touch**),
  migration grandfather for legacy rows until next intake mutation; reason codes align **`R-0055`**;
  executable validator **`scripts/intake_evidence_validate.py`** + library **`scripts/intake_evidence_lib.py`**
  + **`tests/intake_evidence_fixtures_test.py`** (**AC-8**); architecture **`# US-0078`**;
  linked story **`US-0078`**.
- `DEC-0059`: **documentation audience/depth profiles + dual README developer shard (`US-0077`)** —
  merged scratchpad keys **`DOC_AUDIENCE_PROFILE`** / **`DOC_DETAIL_LEVEL`**; **9-cell**
  semantic keys per **`R-0054`**; root **`README.md`** (**`USER_*`**) + **`docs/developer/README.md`**
  (**`DEV_*`**); normative H2 literals + budgets in **`architecture.md`**; validator
  **`scripts/validate_doc_profile.py`** + tiered **`AC-8`** fixtures; reason codes
  **`DOC_PROFILE_INVALID`**, **`DOC_PROFILE_MERGE_ERROR`**, **`DOC_SECTION_MISSING:<key>`**,
  **`DOC_SECTION_BUDGET_EXCEEDED`**, **`DOC_TEMPLATE_PARITY_FAIL`**; migration defaults per
  **`DEC-0059`** §6; **`US-0030`** / **`US-0031`** / **`US-0032`** / **`US-0071`** boundaries.
- `DEC-0058`: **executable merged-scratchpad wiring for validate-and-push (`US-0076`)** —
  **`validate-and-push.ps1`/`.sh`** read **merged** scratchpad per **`DEC-0055`** for
  **`SYNC_*` / `ALLOW_AUTO_PUSH` / allowlist**; **`runbook.md`** = command keys only;
  **`DEC-0018`** remains policy authority; bounded **`sprints/S*/qa-findings.md`** scan
  (**AC-5**); default **invocation = phase boundary**; optional **`SYNC_PHASE_BOUNDARY`**
  env; linked story **`US-0076`**; research **`R-0053`**.
- `DEC-0057`: **scratchpad example-first upgrade + paired catalog parity (`AC-11`)** —
  example refresh ordered **before or bundled with** materialized baseline refresh so
  example **never lags** template when baseline moves; machine-enforced **`##` + `KEY=`**
  set equality on active + template **baseline ↔ example** pairs (manifest-documented
  local-only exceptions only); diagnostics align with **`DEC-0039`**; merge precedence
  unchanged (**`DEC-0055`**); linked story **`US-0075`**.
- `DEC-0056`: **baseline version-sync + TEST_COMMAND bootstrap** — `package.json`
  `version` canonical for npm/Git tag and Homebrew stable `url` / Ruby `version` /
  `sha256`; installer + CLI runbook bootstrap emits baseline-allowed `TEST_COMMAND`
  (`npm run test` \| `sh tests/run-tests.sh`) with triple-installer + template parity;
  PowerShell runner widening out of scope without explicit follow-up; linked story
  `US-0074`.
- `DEC-0055`: scratchpad **example-only default install (Model B)** with
  **materialized baseline** — canonical merged precedence (local →
  baseline/materialized → example); fail-closed missing required keys with layer
  attribution; upgrade preserves user local + refreshes example per
  **`DEC-0039`**; explicit legacy/migration rules; installer/CLI/`template/`
  parity; linked story `US-0073`.
- `DEC-0054`: **triad hot-surface compaction** — canonical targets `state.md`,
  `handoffs/po_to_tl.md`, `architecture.md`; merged scratchpad thresholds
  (`STATE_HOT_*`, `PO_TO_TL_HOT_*`, `ARCH_HOT_*`); deterministic archive packs
  (`state-archive/`, `handoffs/archive/`, `architecture-archive/`); same-phase
  rollover or fail-closed; mandatory verification tuple (`boundary`, `moved`,
  `retained`, `pack_ref`); phase ownership gates; minimal-read budgets + reason
  codes (`STATE_ARCHIVE_REQUIRED`, `ARTIFACT_HOT_SURFACE_OVERSIZE`,
  `CONTEXT_BUDGET_EXCEEDED`, etc.); linked story `US-0072`.
- `DEC-0053`: user-visible **internal metadata sanitization guard** — forbidden
  planning-token patterns (`US|DEC|R` + four digits) in operator/end-user
  software outputs only; explicit allowlist for `docs/**`, `.cursor/**`,
  sprint/handoff/decision artifacts, and code comments; mandatory execute guard +
  QA fail-closed scan + release attestation that checks ran; deterministic
  reason-code vocabulary; active/template parity; linked story `US-0071`.
- `DEC-0052`: scratchpad-controlled `/auto` **phase plan** resolution (single
  active policy mode: `full` / `exclude` / `include` / `profile`), deterministic
  materialization pipeline, default **non-skippable** reinstatement (`qa`,
  `verify-work`, `release` + evidence-chain integrity), `start-from`
  intersection fail-closed semantics, named high-risk profile rules with
  acknowledgment, compatibility with `DEC-0051` (no role substitution via
  skips), and operator-facing breadcrumb/reason-code contract; linked story
  `US-0070`.
- `DEC-0051`: strict `/auto` phase→role mapping with scratchpad-resolved
  alternates (`AUTO_ROLE_RESEARCH`, `AUTO_ROLE_PLAN_VERIFY`,
  `AUTO_ROLE_REFRESH_CONTEXT`), mandatory preflight capability gate,
  fail-closed isolation vs contract validation (`PHASE_ROLE_MISMATCH`),
  `PHASE_ROLE_CAPABILITY_MISSING`, strict-proof `role` alignment with
  isolation, execute default `dev` with rare `AUTO_EXECUTE_ROLE_OVERRIDE` +
  `execute_override_governance_ref`, and resume/start-from preflight parity;
  linked story `US-0069`.
- `DEC-0050`: mandatory deterministic intake question packs (`first-intake-pack`
  and `small-intake-pack`) with machine-verifiable topic IDs,
  required/optional classification, fail-closed persistence gating on missing
  required coverage, bounded assumptions confirmation path, and mandatory
  intake coverage evidence fields (`asked_topics`, `missing_topics`,
  `assumptions_confirmed`); linked story `US-0068`.
- `DEC-0049`: deterministic release operator hints contract for sprint release
  artifacts with fixed `Run -> Connect -> Verify -> Credentials(env-ref only) ->
  Known Issues` ordering, fail-closed required-field validation, explicit
  `local|remote` runtime context alignment, and concise latest-pointer parity;
  linked story `US-0067`.
- `DEC-0048`: deterministic generated-test scaffolding + auto-run contract for
  generated app projects, including supported stack baseline profiles
  (Node/Python/Go/Java/.NET), fail-closed unresolved/unsupported diagnostics,
  non-destructive precedence (`user-authored assets` > `generated missing
  assets`), rerun idempotence, and mandatory QA evidence linkage; linked story
  `US-0066`.
- `DEC-0047`: mandatory runtime QA autopilot contract for generated projects:
  startup/readiness/log validation chain, bounded selective retries, deterministic
  runtime reason-code families, stack-aware profile fail-safe, and mandatory
  runtime evidence schema; linked story `US-0065`.
- `DEC-0046`: runbook command bootstrap contract with precedence
  (`user override > detected defaults > fail-fast diagnostics`), stack/OS-aware
  detection, mandatory baseline validation, and non-destructive reruns; linked
  story `US-0063`.
- `DEC-0045`: installer-owned canonical metadata boundary at `its_magic/` with
  upgrade migration from legacy root marker, clean/install ownership manifest
  updates, and non-destructive backward compatibility; linked story `US-0062`.
- `DEC-0043`: cross-phase ownership matrix with non-destructive mutation
  enforcement (`PHASE_OWNERSHIP_VIOLATION`,
  `PHASE_OVERRIDE_EVIDENCE_MISSING`, `ARCH_HISTORY_DELETION_DETECTED`) and
  deterministic archive verification fail-safe
  (`STATE_ARCHIVE_VERIFICATION_FAILED`); linked story `US-0061`.
- `DEC-0044`: release-target runtime connectivity contract (`runtime.mode`,
  endpoint metadata, Traefik fields, docker-over-ssh) with remote-aware
  release/qa/execute behavior and deterministic diagnostics
  (`REMOTE_CONNECTIVITY_CONFIG_INVALID`,
  `RUNTIME_CONNECTIVITY_DOC_WRITE_FAILED`); linked story `US-0064`.
- `DEC-0042`: deterministic state hot-surface rollover with explicit thresholds
  (`STATE_HOT_MAX_LINES`, `STATE_HOT_MAX_CHECKPOINTS`), non-destructive archive
  packs, and fail-safe diagnostics
  (`STATE_ARCHIVE_BOUNDARY_AMBIGUOUS`, `STATE_ARCHIVE_WRITE_FAILED`); linked
  story `US-0060`.
- `DEC-0041`: deterministic intake capability preflight with fail-fast
  `SUBAGENT_CAPABILITY_UNAVAILABLE`, explicit fallback policy, and
  single-writer self-write-aware drift safety
  (`INTAKE_CONCURRENT_WRITER_DETECTED` for external conflicts); linked story
  `US-0059`.
- `DEC-0040`: canonical artifact ordering matrix (`append-bottom`,
  `prepend-top`, `sorted-canonical`) plus fail-safe anchor handling and
  idempotent rerun contract; linked story `US-0058`.
- `DEC-0039`: Upgrade-safe scratchpad example refresh contract with explicit
  ownership boundaries (`.cursor/scratchpad.local.example.md` framework-owned,
  `.cursor/scratchpad.local.md` user-owned), deterministic diagnostics, and
  installer parity checks; linked story `US-0057`.
- `DEC-0038`: strict runtime attestation envelope and boundary
  validator for `/auto` with deterministic fail-closed reason codes and
  pause/resume provenance integration; linked story `US-0056`.
- `DEC-0037`: Deterministic status reconciliation command with canonical
  precedence, bounded repair, auditable normalization evidence, and resume
  readiness update; linked story `US-0055`.
- `DEC-0036`: Configurable multi-target publish contract with default
  confirmation boundary, schema validation, and first-class `custom` + `ssh`
  target support; linked story `US-0054`.
- `DEC-0035`: Tiered token profile (`lean|balanced|full`), compact
  active-context/archive policy, compact decisions index, and `/ask`
  narrow-read retrieval; linked story `US-0053`.
- `DEC-0034`: Optional fresh-project ID namespace bootstrap with deterministic
  freshness checks; linked story `US-0052`.
- `DEC-0033`: Intake decomposition + risk-aware PO questioning with bounded
  split heuristics and explicit user authority; linked story `US-0051`.
- `DEC-0032`: Installer-owned manifest controls install/clean ownership with
  clean-starter hygiene and lifecycle parity checks; linked story `US-0050`.
- `DEC-0029`: Per-phase fresh-context isolation evidence is mandatory at phase
  boundaries; linked story `US-0048`.
- `DEC-0025`: Canonical story status source is `docs/product/backlog.md`, with
  target-scoped derived reconciliation in acceptance/state.

## Canonical full records

- Full records live in decisions/DEC-xxxx.md.
- Index pattern: `decisions/DEC-0003.md` ... `decisions/DEC-0070.md`.
- Decision: **`DEC-0070`** — **`remote_config_summary.py`** when **`REMOTE_EXECUTION=0`**
  exits **0** (skip, stderr reason) — see **`decisions/DEC-0070.md`** and
  **`docs/engineering/architecture.md`** **`# US-0084`**.
