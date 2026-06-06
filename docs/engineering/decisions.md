# Decisions

## Current context pack (2026-06-07 — **`US-0093`** **DONE** / **`S0082` released** — `auto-20260606-04`, `fresh_context_marker=curator-S0082-US0093-refresh-context-20260607T014500Z-fresh`, `runtime_proof_id=rp-auto-20260606-04-refresh-context-curator-20260607T014500Z-S0082-US0093`, `proof_hash=49953d35dfde952115d49fc5f3e72264b3979fff0d619057c1a700b14a8f9447`; binding **`DEC-0079`** composes on **`DEC-0078`**, **`US-0065`**, **`US-0066`**; research anchor **`R-0079`** **delivered**; **`backlog_drain_stories_remaining_budget=1`**; portfolio **0 OPEN** stories — **`drain_terminated=true`** (`no_open_stories`); next phase **`/intake`**).

- **`US-0093`** (**DONE**, **`S0082`**, **released**): full story lifecycle on **`auto-20260606-04`** — **`/release`** **PASS** **`2026-06-07T01:30:00Z`**; **`handoffs/release_queue.md`** **`S0082`** **`released`**; **`handoffs/releases/S0082-release-notes.md`**; curator **`/refresh-context`** **PASS** (**`2026-06-07T01:45:00Z`**) reconciles **`state.md`**, **`decisions.md`**, **`research.md`** (**`R-0079`** delivered), **`sprints/S0082/summary.md`**, **`handoffs/resume_brief.md`**; normative **`DEC-0079`** — two-tier browser UAT (stdlib **`uat_probe_lib.py`** + agent Cursor browser MCP); **`UAT_BROWSER_PROBE_MODE`**; verb routing; **`browser_evidence_refs`**; stub completion; **`UAT_BROWSER_*`** reason codes; six **`test_us0093_*`** contract subtests; template parity **`--scope=us-0093`**; UAT **10/10**. **Sync**: `push_decision=blocked`, `reason_code=TEST_FAILED` (14 pre-existing harness failures disjoint from US-0093). **Next**: **`/intake`** (portfolio empty).

## Current context pack (2026-06-06 — **`US-0093`** **OPEN** / architecture PASS — superseded for active orchestration by pack above — `auto-20260606-04`, `fresh_context_marker=tl-US0093-architecture-20260606T233000Z-fresh`, `runtime_proof_id=rp-auto-20260606-04-architecture-tl-20260606T233000Z-US0093`, `proof_hash=6a8d66bf42af11654e21aea844bc3eac1127a4b51a258133072e5f64426271de`; binding **`DEC-0079`** composes on **`DEC-0078`**, **`US-0065`**, **`US-0066`**; research anchor **`R-0079`** **closed for `/research`**; **`backlog_drain_stories_remaining_budget=2`**; next phase **`/sprint-plan`**).

- **`US-0093`** (**OPEN**, architecture PASS): Cursor browser-integrated UAT self-test on **`auto-20260606-04`** — **`/architecture`** **PASS** **`2026-06-06T23:30:00Z`**; normative **`DEC-0079`** — two-tier execution (stdlib **`uat_probe_lib.py`** + agent Cursor browser MCP); **`UAT_BROWSER_PROBE_MODE`** scratchpad key; verb routing; **`browser_evidence_refs`** evidence schema; stub completion for **`process_health`**/**`cli_smoke`**; reason codes **`UAT_BROWSER_*`**; 10 atomic task seeds; triad hot-surface PASS (`baseline_h2_count=0`). **Next**: **`/sprint-plan`** (fresh **tech-lead**).

- **`US-0092`** (**DONE**, **`S0081`**, **released**): full story lifecycle on **`auto-20260606-03`** — **`/release`** **PASS** **`2026-06-06T22:30:00Z`**; **`handoffs/release_queue.md`** **`S0081`** **`released`**; **`handoffs/releases/S0081-release-notes.md`**; curator **`/refresh-context`** **PASS** (**`2026-06-06T22:45:00Z`**) reconciles **`state.md`**, **`decisions.md`**, **`research.md`** (**`R-0078`** delivery closed), **`sprints/S0081/summary.md`**, **`handoffs/resume_brief.md`**; normative **`DEC-0078`** — opt-in **`AUTO_FLOW_MODE=full_autonomy`** (default-off); stdlib outer driver **`scripts/auto_outer_driver.py`**; UAT probe lib **`scripts/uat_probe_lib.py`**; full_autonomy stop matrix; block-retry ledger **`handoffs/auto_block_retry/<orchestrator_run_id>.jsonl`**; TOKEN_PROFILE orthogonality audit; UAT **10/10**. **Sync**: `push_decision=blocked`, `reason_code=TEST_FAILED` (14 pre-existing harness failures disjoint from US-0092). **Next**: **`/intake`** (portfolio empty).

## Current context pack (2026-06-06 — **`BUG-0011`** **DONE** / **`S0080` released** — superseded for active orchestration by pack above — `auto-20260606-02`, `fresh_context_marker=curator-S0080-BUG0011-refresh-context-20260606T145631Z-fresh`, `runtime_proof_id=rp-auto-20260606-02-refresh-context-curator-20260606T145631Z-S0080-BUG0011`, `proof_hash=95970384cfd1aa7986f234be6fc8b3f88558ea2a8e10b092a3947d9170fba911`; binding **`DEC-0077`** composes on **`DEC-0072`**; research anchor **`R-0077`** **delivered**; **`bug_queue_position=3/3` closed**; **`bug_queue_remaining=0`**; portfolio **0 OPEN** bugs — **`drain_terminated=true`** (`no_open_stories`) prior to **`US-0092`** intake).

- **`BUG-0011`** (**DONE**, **`S0080`**, **released**): full defect lifecycle on **`auto-20260606-02`** — **`/release`** **PASS** **`2026-06-06T17:00:00Z`**; **`handoffs/release_queue.md`** **`S0080`** **`released`**; **`handoffs/releases/S0080-release-notes.md`**; curator **`/refresh-context`** **PASS** (**`2026-06-06T14:56:31Z`**) reconciles **`state.md`**, **`decisions.md`**, **`research.md`** (**`R-0077`** delivery closed), **`sprints/S0080/summary.md`**, **`handoffs/resume_brief.md`**; normative **`DEC-0077`** — voice-section append to `.cursor/rules/caveman.mdc` (`## Voice compression (when CAVEMAN_MODE=1)` + six subsections); dual-layer SHA bump + nine `test_caveman_voice_*` markers; harness **§30A**; runbook compact 2-row level table; `# US-0089` §6 cross-link; **`architecture.md`** **`# BUG-0011`**. **Sync**: `push_decision=blocked`, `reason_code=TEST_FAILED` (14 pre-existing harness failures disjoint from BUG-0011). **Next**: **`/intake`** (portfolio empty).

## Current context pack (2026-06-06 — **`BUG-0011`** **OPEN** / architecture **PASS** — superseded for active orchestration by pack above — `auto-20260606-02`, `fresh_context_marker=tl-BUG0011-architecture-20260606T144123Z-fresh`, `runtime_proof_id=rp-auto-20260606-02-architecture-tl-20260606T144123Z-BUG0011`, `proof_hash=fc34e4003292854f65c2fb5b2e29184250900029979cdbee0c6a2e8bb04a4ad1`; binding **`DEC-0077`** composes on **`DEC-0072`** (no rewrite); research anchor **`R-0077`** **open** (delivery pending); **`bug_queue_position=3/3`**; OPEN bug **`BUG-0011`** — next portfolio **`/sprint-plan`** for **`BUG-0011`** via **`bug-target=BUG-0011`**).

- **`BUG-0011`** (**OPEN**, architecture **PASS**): **`/architecture`** **PASS** **`2026-06-06T14:41:23Z`** on **`auto-20260606-02`**; normative **`DEC-0077`** — voice-section append to `.cursor/rules/caveman.mdc` (`## Voice compression (when CAVEMAN_MODE=1)` outline locked); dual-layer SHA bump + nine `test_caveman_voice_*` markers; harness **§30A**; runbook compact 2-row level table; `# US-0089` §6 cross-link; **`architecture.md`** **`# BUG-0011`** appended. **Next**: **`/sprint-plan`**.

## Current context pack (2026-06-06 — **`BUG-0010`** **DONE** / **`S0079` released** — `auto-20260606-02`, `fresh_context_marker=curator-S0079-BUG0010-refresh-context-20260606T164100Z-fresh`, `runtime_proof_id=rp-auto-20260606-02-refresh-context-curator-20260606T164100Z-S0079-BUG0010`, `proof_hash=2b42915c5f8c0ae364f6f232ef1dc8e1e647fc1932593415d264ffcc8b177ef3`; binding **`DEC-0076`** composes on **`DEC-0054`** + **`DEC-0043`**; research anchor **`R-0076`** **delivered**; **`bug_queue_position=2/3` closed**; **`bug_queue_remaining=1`**; OPEN bug **`BUG-0011`** — next portfolio **`/discovery`** for **`BUG-0011`** via **`bug-target=BUG-0011`**).

- **`BUG-0010`** (**DONE**, **`S0079`**, **released**): full defect lifecycle on **`auto-20260606-02`** — **`/release`** **PASS** **`2026-06-06T16:36:00Z`**; **`handoffs/release_queue.md`** **`S0079`** **`released`**; **`handoffs/releases/S0079-release-notes.md`**; curator **`/refresh-context`** **PASS** (**`2026-06-06T16:41:00Z`**) reconciles **`state.md`**, **`decisions.md`**, **`research.md`** (**`R-0076`** delivery closed), **`sprints/S0079/summary.md`**, **`handoffs/resume_brief.md`**; normative **`DEC-0076`** — dual-level archiver (`STORY_HEADING_H1` + `STORY_HEADING_H2`, H1-wins precedence); diff-gated `ARCH_STORY_HEADING_LEVEL_INVALID` forward enforcement; in-place `enforce-triad-hot-surface.py` extension; harness **§29A**; `test_bug0010_*` contract tests; command + runbook template parity; **`architecture.md`** **`# BUG-0010`**. **Sync**: `push_decision=blocked`, `reason_code=TEST_FAILED` (14 pre-existing harness failures disjoint from BUG-0010). **Next**: **`/discovery`** for **`BUG-0011`**.

## Current context pack (2026-06-06 — **`BUG-0010`** **OPEN** / architecture **PASS** — superseded for active orchestration by pack above — `auto-20260606-02`, `fresh_context_marker=tl-BUG0010-architecture-20260606T142242Z-fresh`, `runtime_proof_id=rp-auto-20260606-02-architecture-tl-20260606T142242Z-BUG0010`, `proof_hash=a3a709c179134f8ac44c89cd05f5b99e132b72f5c06b8224f027131853b48f42`; binding **`DEC-0076`** composes on **`DEC-0054`** + **`DEC-0043`**; research anchor **`R-0076`** **open** (delivery pending); **`bug_queue_position=2/3`**; OPEN bugs **`BUG-0010`**, **`BUG-0011`** — next portfolio **`/sprint-plan`** for **`BUG-0010`** via **`bug-target=BUG-0010`**).

- **`BUG-0010`** (**OPEN**, architecture **PASS**): **`/architecture`** **PASS** **`2026-06-06T14:22:42Z`** on **`auto-20260606-02`**; normative **`DEC-0076`** — dual-level archiver (`STORY_HEADING_H1` + `STORY_HEADING_H2`, H1-wins precedence); diff-gated `ARCH_STORY_HEADING_LEVEL_INVALID` forward enforcement; in-place `enforce-triad-hot-surface.py` extension; harness **§29A**; `test_bug0010_*` contract tests; command + runbook template parity; **`architecture.md`** **`# BUG-0010`** appended. **Next**: **`/sprint-plan`**.

## Current context pack (2026-06-06 — **`BUG-0009`** **DONE** / **`S0078` released** — superseded for active orchestration by pack above — `auto-20260606-02`, `fresh_context_marker=curator-S0078-BUG0009-refresh-context-20260606T162000Z-fresh`, `runtime_proof_id=rp-auto-20260606-02-refresh-context-curator-20260606T162000Z-S0078-BUG0009`, `proof_hash=e095e0efe855f7cfb10e9570c464641acbed1ceb04d4a0a588a256c467523705`; binding **`DEC-0075`**; research anchor **`R-0075`** **delivered**; **`bug_queue_position=1/3` closed**; **`bug_queue_remaining=2`**; OPEN bugs **`BUG-0010`**, **`BUG-0011`** — next portfolio **`/discovery`** for **`BUG-0010`** via **`bug-target=BUG-0010`**).

- **`BUG-0009`** (**DONE**, **`S0078`**, **released**): full defect lifecycle on **`auto-20260606-02`** — **`/release`** **PASS** **`2026-06-06T16:15:00Z`**; **`handoffs/release_queue.md`** **`S0078`** **`released`**; **`handoffs/releases/S0078-release-notes.md`**; curator **`/refresh-context`** **PASS** (**`2026-06-06T16:20:00Z`**) reconciles **`state.md`**, **`decisions.md`**, **`research.md`** (**`R-0075`** delivery closed), **`sprints/S0078/summary.md`**, **`handoffs/resume_brief.md`**; normative **`DEC-0075`** — in-place template `ci.yml` job subtraction (`checks`+`auto-fix` only); active kit retains five packaging jobs; drift guard **`scripts/check_downstream_ci_guard.py`** + **`downstream_ci_guard_lib.py`**; forbidden patterns + reason codes; checks green-by-default; empty template `TEST_COMMAND`; install smoke + harness **§28B**; upgrade remediation docs; template parity **`--scope=downstream-ci-guard`**. **Sync**: `push_decision=blocked`, `reason_code=TEST_FAILED` (14 pre-existing harness failures disjoint from BUG-0009). **Next**: **`/discovery`** for **`BUG-0010`**.

## Current context pack (2026-06-06 — **`BUG-0009`** **OPEN** / **`S0078`** sprint-plan **PASS** — superseded for active orchestration by pack above — `auto-20260606-02`, `fresh_context_marker=tl-S0078-BUG0009-sprint-plan-20260606T140023Z-fresh`, `runtime_proof_id=rp-auto-20260606-02-sprint-plan-tech-lead-20260606T140023Z-S0078-BUG0009`, `proof_hash=8e2050a8b3bbb5993f98d1197ce97e2d1ceccf7be5d62c705058ed396690fcd3`; binding **`DEC-0075`**; research anchor **`R-0075`** **open** (delivery pending); **`bug_queue_position=1/3`**; OPEN bugs **`BUG-0009..BUG-0011`** — next portfolio **`/plan-verify`** for **`S0078`** / **`BUG-0009`**).

- **`BUG-0009`** (**OPEN**, **`S0078`**, sprint-plan **PASS**): **`/sprint-plan`** **PASS** **`2026-06-06T14:00:23Z`** on **`auto-20260606-02`**; sprint **`S0078`** — **T-001..T-010** (AC-1..AC-8 surjective); `plan-verify.json` **PENDING**; harness **§28B**; drift guard + install smoke + operator remediation docs planned per **`DEC-0075`**. **Next**: **`/plan-verify`**.

## Current context pack (2026-06-06 — **`BUG-0009`** **OPEN** / architecture **PASS** — superseded for active orchestration by pack above — `auto-20260606-02`, `fresh_context_marker=tl-BUG0009-architecture-20260606T160000Z-fresh`, `runtime_proof_id=rp-auto-20260606-02-architecture-tl-20260606T160000Z-BUG0009`, `proof_hash=47027c0a605d7150e949cd8d6fc7ad3f30280aca4cbb0462427721e2a57b0805`; binding **`DEC-0075`** composes on **`US-0017`** negative-parity exceptions + **`US-0008`** installer copy; research anchor **`R-0075`** **open** (delivery pending); **`bug_queue_position=1/3`**; OPEN bugs **`BUG-0009..BUG-0011`** — next portfolio **`/sprint-plan`** for **`BUG-0009`** via **`bug-target=BUG-0009`**).

- **`BUG-0009`** (**OPEN**, architecture **PASS**): **`/architecture`** **PASS** **`2026-06-06T16:00:00Z`** on **`auto-20260606-02`**; normative **`DEC-0075`** — in-place template `ci.yml` job subtraction (`checks`+`auto-fix` only); active kit retains five packaging jobs; **`US-0017`** negative-parity table; drift guard **`scripts/check_downstream_ci_guard.py`** + **`downstream_ci_guard_lib.py`**; forbidden patterns + reason codes; checks green-by-default; empty template `TEST_COMMAND`; install smoke + harness **§28B**; upgrade remediation docs; **`architecture.md`** **`# BUG-0009`** appended. **Next**: **`/sprint-plan`**.

## Current context pack (2026-06-06 — **`US-0091`** **DONE** / **`S0077` released** — superseded for active orchestration by pack above — `auto-20260606-01`, `fresh_context_marker=curator-S0077-US0091-refresh-context-20260606T135000Z-fresh`, `runtime_proof_id=rp-auto-20260606-01-refresh-context-curator-20260606T135000Z-S0077-US0091`, `proof_hash=1fe3a39c7fd03d128b3b61e68b9a07593739bd0bd290c7b109f4e23269aff1e9`; binding **`DEC-0074`** composes on **`DEC-0059`** and extends US-0030 release doc-gate family (delta gate unchanged); research anchor **`R-0074`** **delivered**; **`backlog_drain_stories_remaining_budget=3`**; OPEN bugs **`BUG-0009..BUG-0011`** on bug queue — next portfolio **`/discovery`** for **`BUG-0009`** via **`bug-target=BUG-0009`**.

- **`US-0091`** (**DONE**, **`S0077`**, **released**): full lifecycle on **`auto-20260606-01`** — **`/release`** **PASS** **`2026-06-06T13:43:20Z`**; **`handoffs/release_queue.md`** **`S0077`** **`released`**; **`handoffs/releases/S0077-release-notes.md`**; curator **`/refresh-context`** **PASS** (**`2026-06-06T13:50:00Z`**) reconciles **`state.md`**, **`decisions.md`**, **`research.md`** (**`R-0074`** delivery closed), **`sprints/S0077/summary.md`**, **`handoffs/resume_brief.md`**; normative **`DEC-0074`** — predicate Option A (`user_visible:` backlog field + H1–H8 heuristic); stdlib validator **`scripts/validate_readme_feature_coverage.py`** + **`readme_feature_coverage_lib.py`**; three-file README backfill (`coverage_missing=[]`, `coverage_total=98`); release step **3f** composed on US-0030; harness **§27U**; scratchpad **`README_FEATURE_COVERAGE_ENFORCE=1`** post-backfill; template parity **`--scope=readme-feature-coverage`**. **Sync**: `push_decision=blocked`, `reason_code=TEST_FAILED` (9 pre-existing harness failures disjoint from US-0091).

## Current context pack (2026-06-06 — **`US-0091`** **OPEN** / architecture **PASS** — superseded for active orchestration by pack above)

- **`US-0091`** (**OPEN**, architecture **PASS**): **`/architecture`** **PASS** **`2026-06-06T14:30:00Z`** on **`auto-20260606-01`**; normative **`DEC-0074`** — predicate Option A (`user_visible:` backlog field + H1–H8 heuristic when `README_FEATURE_COVERAGE_ENFORCE=0`); validator lib split (`validate_readme_feature_coverage.py` + `readme_feature_coverage_lib.py`); release step **3f** composed on US-0030; grandfathering via `README_FEATURE_COVERAGE_ENFORCE=0|1` (default **0**); section-affinity manifest; reason codes per AC-5; template parity `--scope=readme-feature-coverage`; harness **§27U**; **`architecture.md`** **`# US-0091`** appended. **Next**: **`/sprint-plan`**.

## Current context pack (2026-04-19 — **`US-0090`** **DONE** / **`S0076` released** — superseded for active orchestration by pack above)

- **`US-0090`** (**DONE**, **`S0076`**, **released**): full lifecycle on **`auto-20260418-01`** — **`/release`** **PASS** **`2026-04-19T00:05:00Z`**; **`handoffs/release_queue.md`** **`S0076`** **`released`**; **`handoffs/releases/S0076-release-notes.md`**; curator **`/refresh-context`** **PASS** (**`2026-04-19T00:30:00Z`**) reconciles **`state.md`**, **`decisions.md`**, **`research.md`**, **`sprints/S0076/summary.md`**, **`handoffs/resume_brief.md`**; **`R-0073`** delivery closed for US-0090 surface (anchor now `delivered` for both US-0089 + US-0090); normative **`DEC-0073`** (composes on **`DEC-0072`** via forward-link), **`architecture.md`** **`# US-0090`**, `scripts/caveman_compress_input.py` (active + `template/`) stdlib-only CLI with 4 flags + 9-code reason vocabulary + activation gate + layered deny-list + sidecar-first atomic write + safe-mode idempotent minifier, `docs/engineering/runbook.md` + `docs/engineering/auto-orchestration-reference.md` three-axis companion paragraphs (active + `template/`), `tests/auto_command_contract_test.py` 13 new `test_caveman_compress_input_*` subtests + existing `test_caveman_default_off_*` byte-unchanged, `tests/fixtures/caveman_compress/` 8 classes / 51 fixtures, `tests/installer_completeness_bug0003_test.py` `test_caveman_compress_input_shipped_by_installer`, harness section `26T` (PS1 + SH), installer manifest entry + `check_intake_template_parity.py --scope=caveman-compress` / `--scope=all`.

- **`US-0089`** (**DONE**, **`S0075`**, **released**): full lifecycle on **`auto-20260418-01`** — **`/release`** **PASS** **`2026-04-18T19:00:00Z`**; **`handoffs/release_queue.md`** **`S0075`** **`released`**; **`handoffs/releases/S0075-release-notes.md`**; curator **`/refresh-context`** **PASS** (**`2026-04-18T20:00:00Z`**) reconciles **`state.md`**, **`decisions.md`**, **`research.md`**, **`sprints/S0075/summary.md`**, **`handoffs/resume_brief.md`**; **`R-0073`** delivery closed for US-0089 surface; normative **`DEC-0072`**, **`architecture.md`** **`# US-0089`**, **`.cursor/rules/caveman.mdc`** (active + `template/`), scratchpad keys `CAVEMAN_MODE` / `CAVEMAN_LEVEL` + reserved-for-US-0090 no-ops `CAVEMAN_COMPRESS_INPUT` / `CAVEMAN_FILE_SCOPE`, 9-zone literal-region invariant, 8 `test_caveman_default_off_*` subtests extending `tests/auto_command_contract_test.py` in place, 8-row template parity.

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
- **`BUG-0008`** (**DONE**, **`S0070`**, **released**): full defect lifecycle on **`auto-20260404-03`** — **`/release`** **PASS** **`2026-04-05T22:30:00Z`**; **`handoffs/release_queue.md`** **`S0070`** **`released`**; **`handoffs/releases/S0070-release-notes.md`**; curator **`/refresh-context`** (**`2026-04-05T23:45:00Z`**) reconciles sprint summary + **`handoffs/resume_brief.md`** → **`US-0087`** / **`discovery`**; **`architecture.md`** **`# BUG-0008`**, **`R-0069`** delivery closed (CRLF manifest / **`installer.sh`** / **`guard_installer_publish`** / **26P2**).
- **`US-0084`** (**DONE**, **`S0069`**, **released**): full lifecycle on **`auto-20260404-02`** — **`/release`** **PASS** **`2026-04-05T00:10:00Z`**; **`handoffs/release_queue.md`** **`S0069`** **`released`**; **`handoffs/releases/S0069-release-notes.md`**; curator **`/refresh-context`** reconciliation (**`2026-04-05T01:30:00Z`**) closes **`R-0067`** and aligns **`handoffs/resume_brief.md`** to **`/intake`** (next **US**; bug portfolio idle **BUG-0001..BUG-0007** **DONE**); normative **`DEC-0070`**, **`architecture.md`** **`# US-0084`**, **`R-0067`** delivery closed (**`guard_installer_publish.py`**, **`remote_config_summary.py`**, **`tests/installer_shell_bug0004_test.py`**, **`tests/remote_config_summary_test.py`**).
- **`US-0085`** (**DONE**, **`S0073`**, **released**): full lifecycle on **`auto-20260405-01`** — **`/release`** **PASS** **`2026-04-13T17:00:00Z`**; **`handoffs/release_queue.md`** **`S0073`** **`released`**; **`handoffs/releases/S0073-release-notes.md`**; curator **`/refresh-context`** (**`2026-04-13T18:00:00Z`**) reconciles **`decisions.md`**, **`sprints/S0073/summary.md`**, **`handoffs/resume_brief.md`**; **`R-0072`** delivery closed; normative **`DEC-0071`**, **`architecture.md`** **`# US-0085`**, 4-layer `.env` exclusion contract (`.gitignore` + `.cursorignore` + Cursor rules + operator discipline), `.env.example` 20 names, `scripts/print_remote_env_hint.py`, `tests/test_env_gitignore.py`, 7-touchpoint template parity.
- **`US-0086`** (**DONE**, **`S0074`**, **released**): full lifecycle on **`auto-20260405-01`** — **`/release`** **PASS** **`2026-04-13T22:30:00Z`**; **`handoffs/release_queue.md`** **`S0074`** **`released`**; **`handoffs/releases/S0074-release-notes.md`**; curator **`/refresh-context`** (**`2026-04-13T23:00:00Z`**) reconciles **`state.md`**, **`decisions.md`**, **`research.md`**, **`sprints/S0074/summary.md`**, **`resume_brief.md`**; **`R-0068`** delivery closed; normative **`architecture.md`** **`# US-0086`**, automation routing reason-code contract, and remote-selection evidence tuple.
- **`US-0088`** (**DONE**, **`S0072`**, **released**): full lifecycle on **`auto-20260405-01`** — **`/release`** **PASS** **`2026-04-13T01:15:00Z`**; curator **`/refresh-context`** (**`2026-04-13T01:30:00Z`**); **`R-0071`** delivery closed; normative **`architecture.md`** **`# US-0088`**, **`tests/auto_command_contract_test.py`** (17 tests / 66 subtests), continuous multi-phase + **`AUTO_QUIET`** + drain-advance contract.
- **`US-0087`** (**DONE**, **`S0071`**, **released**): full lifecycle on **`auto-20260405-01`** — **`/release`** **PASS** **`2026-04-12T19:05:00Z`**; curator **`/refresh-context`** (**`2026-04-12T20:35:00Z`**); **`R-0070`** delivery closed; normative **`architecture.md`** **`# US-0087`**, **`tests/auto_command_contract_test.py`**, bug-queue contract.
- Research: **`R-0073`** — shared anchor for **US-0089** + **US-0090**; both scopes now **delivered**. US-0089 delivery closed **2026-04-18T20:00:00Z** with **`S0075`** + **`DEC-0072`** / **`architecture.md`** **`# US-0089`** + **`.cursor/rules/caveman.mdc`** + scratchpad keys + 9-zone literal-region invariant + `test_caveman_default_off_*` subtests. US-0090 delivery closed **2026-04-19T00:30:00Z** with **`S0076`** + **`DEC-0073`** (composes on DEC-0072 via forward-link) / **`architecture.md`** **`# US-0090`** + `scripts/caveman_compress_input.py` (stdlib-only CLI) + `tests/auto_command_contract_test.py` 13 `test_caveman_compress_input_*` subtests + `tests/fixtures/caveman_compress/` (8 classes / 51 fixtures) + harness §26T + installer completeness fixture + `check_intake_template_parity.py --scope=caveman-compress`. **`R-0068`** — **US-0086** delivery closed **2026-04-13** with **`S0074`** / **`architecture.md`** **`# US-0086`** (curator **`/refresh-context`** on **`auto-20260405-01`** **`2026-04-13T23:00:00Z`**). **`R-0072`** — **US-0085** delivery closed **2026-04-13** with **`S0073`** + **`DEC-0071`** / **`architecture.md`** **`# US-0085`** + **`tests/test_env_gitignore.py`** (curator **`2026-04-13T18:00:00Z`**). **`R-0071`** — **US-0088** delivery closed **2026-04-13** with **`S0072`** (curator **`2026-04-13T01:30:00Z`**). Prior closed: **`R-0053`**–**`R-0070`** (all delivered; see archived context packs).
- Decision: **`DEC-0062`** — **`US-0080`** token-cost metrics, **`run_class_hash`**, **`handoffs/token_cost_runs/`**, parity manifest, AC-10 trade-offs — see **`decisions/DEC-0062.md`** and **`docs/engineering/architecture.md`** **`# US-0080`**.
- Decision: **`DEC-0063`** — **`BUG-0001`** intake gate script ship path (**`template/scripts/`** minimal mirror, **`package.json` `files`**, parity tests, **`US-0018`**) — see **`decisions/DEC-0063.md`** and **`docs/engineering/architecture.md`** **`# BUG-0001`**.
- Decision: **`DEC-0064`** — **`US-0081`** deterministic first-intake full-plan coverage gate (**`plan_area_inventory`**, **`plan_area_coverage`**, fail-closed `INTAKE_PERSISTENCE_BLOCKED` + subcodes, parity/fixture verification) — see **`decisions/DEC-0064.md`** and **`docs/engineering/architecture.md`** **`# US-0081`**.
- Decision: **`DEC-0066`** — **`BUG-0003`** deterministic installer completeness in `missing`/`upgrade` (manifest-authoritative required script inventory, post-install diagnostics, parity/symmetry tests) — see **`decisions/DEC-0066.md`** and **`docs/engineering/architecture.md`** **`# BUG-0003`**.
- Decision: **`DEC-0067`** — **`US-0083`** explicit topic-scoped intake delegation (`satisfied_by=delegation_ref` + bounded delegation fields), deterministic delegation fail codes under `INTAKE_PERSISTENCE_BLOCKED`, guided/low-touch parity, and DEC-0060-compatible `ie:` evidence binding — see **`decisions/DEC-0067.md`** and **`docs/engineering/architecture.md`** **`# US-0083`**.
- Decision: **`DEC-0068`** — **`BUG-0004`** POSIX-safe installer shell startup under Unix CLI `sh` invocation contract (`bin/its-magic.js`), with deterministic `sh` + CLI regression obligations and no forced bash dependency — see **`decisions/DEC-0068.md`** and **`docs/engineering/architecture.md`** **`# BUG-0004`**.
- Decision: **`DEC-0069`** — **`BUG-0005`** deterministic **`handoffs/resume_brief.md`** refresh at successful bug-intake persistence (default **`discovery`** continuation), preserved **`/auto` resume precedence** and fail-fast on stale/unparseable briefs, optional future self-heal gated — see **`decisions/DEC-0069.md`** and **`docs/engineering/architecture.md`** **`# BUG-0005`**.
- Decision: **`DEC-0059`** — profile semantics, **`docs/developer/README.md`** shard, H2 mapping, validator **`scripts/validate_doc_profile.py`**, tiered **AC-8** tests, migration defaults — see **`decisions/DEC-0059.md`** and **`docs/engineering/architecture.md`** **`# US-0077`**.
- Decision: **`DEC-0065`** — **`US-0082`** codebase map bootstrap lifecycle (**`/architecture`** primary gate, optional **`/refresh-context`**, **`/map-codebase`** manual; idempotency; **`CODEBASE_MAP_*`** diagnostics; parity) — see **`decisions/DEC-0065.md`** and **`docs/engineering/architecture.md`** **`# US-0082`**.
- Continuation hygiene: **`handoffs/resume_brief.md`** routes to **`/intake`** (portfolio empty; **0 OPEN** stories; **0 OPEN** bugs; **`AUTO_BACKLOG_DRAIN`** budget remaining **1** of **10** unused; **`drain_terminated=true`**; `drain_terminated_reason=no_open_stories`).
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
- Hot surface: latest **`/refresh-context` (2026-06-07T01:45:00Z)** post-**`S0082`** / **`US-0093`** on **`auto-20260606-04`** (**`DEC-0079`** delivered; **`R-0079`** closed; portfolio empty → **`/intake`**; triad rollover **`docs/engineering/state-archive/state-pack-20260606-ag.md`**, **`state-pack-20260606-ah.md`**). Prior: **`/release` (2026-06-07T01:30:00Z)** post-**`S0082`** / **`US-0093`**; **`/refresh-context` (2026-06-06T22:45:00Z)** post-**`S0081`** / **`US-0092`**; **`/refresh-context` (2026-06-06T14:56:31Z)** post-**`S0080`** / **`BUG-0011`**.
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
  - `| US-0085 | S0073 | T-001..T-010 | DONE |` — **`DEC-0071`** + **`architecture.md`** **`# US-0085`** + **`R-0072`** closed; **`sprints/S0073/*`**;
    **`plan-verify.json`** **PASS**; **`sprints/S0073/uat.json`**, **`sprints/S0073/uat.md`** **PASS**;
    **`sprints/S0073/release-findings.md`**; **`handoffs/releases/S0073-release-notes.md`**;
    orchestrator **`auto-20260405-01`** closed at **`/refresh-context`** (**`2026-04-13T18:00:00Z`**); **`handoffs/release_queue.md`** **`S0073`** **`released`**.
  - `| US-0088 | S0072 | T-001..T-007 | DONE |` — **`architecture.md`** **`# US-0088`** + **`R-0071`** closed; **`sprints/S0072/*`**;
    **`plan-verify.json`** **PASS**; **`sprints/S0072/uat.json`**, **`sprints/S0072/uat.md`** **PASS**;
    **`sprints/S0072/release-findings.md`**; **`handoffs/releases/S0072-release-notes.md`**;
    orchestrator **`auto-20260405-01`** closed at **`/refresh-context`** (**`2026-04-13T01:30:00Z`**); **`handoffs/release_queue.md`** **`S0072`** **`released`**.
  - `| US-0087 | S0071 | T-001..T-010 | DONE |` — **`architecture.md`** **`# US-0087`** + **`R-0070`** closed; **`sprints/S0071/*`**;
    **`plan-verify.json`** **PASS**; **`sprints/S0071/uat.json`**, **`sprints/S0071/uat.md`** **PASS**;
    **`sprints/S0071/release-findings.md`**; **`handoffs/releases/S0071-release-notes.md`**;
    orchestrator **`auto-20260405-01`** closed at **`/refresh-context`** (**`2026-04-12T20:35:00Z`**); **`handoffs/release_queue.md`** **`S0071`** **`released`**.
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

- **`DEC-0079` / `US-0093`**: **Cursor browser-integrated UAT self-test — two-tier execution, evidence schema, probe stub completion** — composes on **`DEC-0078`** (probe catalog + fail-closed vocabulary — extends execution, does not weaken); Tier 1 stdlib **`scripts/uat_probe_lib.py`** (classify, subprocess fallbacks, **`process_health`**/**`cli_smoke`** completion, **`--merge-result`**); Tier 2 agent (**`/verify-work`**, **`/qa`**, **`/execute`**) owns Cursor browser MCP when **`UAT_BROWSER_PROBE_MODE=cursor`** (default); scratchpad keys **`UAT_BROWSER_PROBE_MODE`**, **`UAT_BROWSER_FALLBACK_CHAIN`**, poll defaults; **`manual_operator`** verb routing (judgment tokens win); evidence **`browser_evidence_refs`** under **`sprints/Sxxxx/evidence/browser/`**; reason codes **`UAT_BROWSER_UNAVAILABLE`**, **`UAT_BROWSER_PROBE_FAILED`**, **`UAT_BROWSER_PROBE_TIMEOUT`**; security deny-list unchanged; template parity **`--scope=us-0093`** + **`test_us0093_*`**; **`R-0079`** basis; architecture **`# US-0093`**.
- **`DEC-0078` / `US-0092`**: **Full-autonomy flow mode, outer driver, self-verify UAT, and TOKEN_PROFILE orthogonality** — composes on **`US-0088`** (continuous `/auto` + outer-driver equivalence), **`DEC-0062`** (TOKEN_PROFILE = context breadth / token cost only), **`DEC-0047`** (runtime QA autopilot probe extension), **`DEC-0048`** (generated-test probe path); opt-in **`AUTO_FLOW_MODE=full_autonomy`** (default-off); stdlib **`scripts/auto_outer_driver.py`** (argv/exit codes 0–6 + 124, spawn-only loop); **`scripts/uat_probe_lib.py`** shared by **`/verify-work`** + **`/qa`**; seven probe kinds + fail-closed reason codes; block-retry ledger **`handoffs/auto_block_retry/<orchestrator_run_id>.jsonl`**; caps **`AUTO_LOOP_MAX_CYCLES`**, **`AUTO_IMPLEMENTATION_LOOP`**, **`AUTO_BLOCK_RETRY_MAX`** (default **3**); drain-without-pause + **DEC-0069** boundary refresh; TOKEN_PROFILE orthography audit + forbidden-pattern grep; security deny-list (no `.env`, no intake mutation, no auto-publish); template parity per **US-0017**; **`R-0078`** basis; architecture **`# US-0092`**.
- **`DEC-0077` / `BUG-0011`**: **Caveman voice-compression rule append, contract markers, and SHA baseline bump** — composes on **`DEC-0072`** (forward-link, no rewrite); append `## Voice compression (when CAVEMAN_MODE=1)` to `.cursor/rules/caveman.mdc` with six locked subsections; dual-layer SHA bump + nine `test_caveman_voice_*` markers; harness **§30A**; runbook compact 2-row level table; `# US-0089` §6 cross-link; **`R-0077`** basis; architecture **`# BUG-0011`**.
- **`DEC-0076` / `BUG-0010`**: **Dual-level architecture story headings, diff-gated forward enforcement, triad archiver extension** — composes on **`DEC-0054`** (triad hot-surface) + **`DEC-0043`** (history-preserving appends); two-pattern scan (`STORY_HEADING_H1` + `STORY_HEADING_H2`) with H1-wins precedence; in-place **`scripts/enforce-triad-hot-surface.py`** extension (`count_h2_story_headings`, `check_arch_heading_policy`, `ARCH_STORY_HEADING_LEVEL_INVALID`); `/architecture` command H1 mandate (active + `template/`); extended `--self-test` + `test_bug0010_*` + harness **§29A**; runbook legacy `## US-` remediation; **`R-0076`** basis; architecture **`# BUG-0010`**.
- **`DEC-0075` / `BUG-0009`**: **Downstream-safe template CI vs kit-internal active CI and drift guard** — composes on **`US-0017`** (negative-parity exceptions for `ci.yml` + template runbook `TEST_COMMAND:` line); in-place template job subtraction (`checks`+`auto-fix` only); active kit retains five packaging jobs; stdlib guard **`scripts/check_downstream_ci_guard.py`** + **`downstream_ci_guard_lib.py`**; forbidden-pattern list + reason codes (`DOWNSTREAM_CI_FORBIDDEN_PATTERN`, `DOWNSTREAM_CI_JOB_LEAK`, `KIT_CI_PACKAGING_JOBS_MISSING`); checks green-by-default + **`no tests configured yet`** summary; empty template `TEST_COMMAND` bootstrap (**US-0063** preserved); install smoke via **`installer_completeness_bug0003_test.py`**; template parity **`--scope=downstream-ci-guard`** (NOT `ci-downstream` byte parity); harness **§28B**; upgrade remediation docs; **`R-0075`** basis; architecture **`# BUG-0009`**.
- **`DEC-0074` / `US-0091`**: **README feature coverage predicate, validator, release gate composition, grandfathering** — composes on **`DEC-0059`** (dual-README audience); extends US-0030 release doc-gate family (delta gate unchanged); backlog field **`user_visible: true|false`** canonical; migration heuristic H1–H8 when `README_FEATURE_COVERAGE_ENFORCE=0`; stdlib validator **`scripts/validate_readme_feature_coverage.py`** + **`readme_feature_coverage_lib.py`**; release step **3f** in `.cursor/commands/release.md` (active + `template/`); grandfathering scratchpad **`README_FEATURE_COVERAGE_ENFORCE=0|1`** (default **0** until backfill); section-affinity manifest **`readme-section-affinity.json`**; reason codes umbrella **`README_FEATURE_COVERAGE_BLOCKED`** + gap/parity/input/profile sub-codes; template parity **`check_intake_template_parity.py --scope=readme-feature-coverage`**; harness **§27U**; **`R-0074`** basis; architecture **`# US-0091`**.
- `DEC-0067`: **explicit topic-scoped intake delegation (`US-0083`)** — extend `topic_coverage.satisfied_by` with `delegation_ref`; require `delegation_scope`, `delegation_rationale`, `delegation_confidence`, and DEC-0060-compatible `ie:` evidence binding; preserve non-delegated fail-closed path and add deterministic delegation diagnostics (`INTAKE_DELEGATION_EVIDENCE_MISSING`, `INTAKE_DELEGATION_EVIDENCE_INVALID`) under `INTAKE_PERSISTENCE_BLOCKED`; guided/low-touch parity; **`R-0062`** basis; architecture **`# US-0083`**.
- `DEC-0068`: **POSIX-safe installer startup (`BUG-0004`)** — keep Unix CLI invocation via `sh installer.sh`, prohibit unconditional bash-only `set` flags in startup path, and require deterministic direct-`sh` + CLI regression coverage for `missing`/`upgrade` compatibility; **`R-0063`** basis; architecture **`# BUG-0004`**.
- `DEC-0069`: **bug-intake `resume_brief` refresh (`BUG-0005`)** — on successful canonical bug intake persistence, intake writer atomically refreshes **`handoffs/resume_brief.md`** with **`bug_id`**, default **`intended_resume_phase=discovery`**, boundary metadata, and **`US-0045`** alignment; explicit **`start-from`** > parseable brief > **`state.md`** fallback unchanged; **`RESUME_BRIEF_STALE`** / unparseable fail-fast preserved; optional orchestrator self-heal deferred behind strict gates; **`R-0064`** basis; architecture **`# BUG-0005`**.
- **`BUG-0006` (`S0067`)**: **spawn-only `/auto` + `AUTO_ORCHESTRATOR_PHASE_EXECUTION`** — orchestrator must not execute phase work in-process; doc-first contract on active + template **`auto.md`**, **`auto-orchestration-reference.md`**, static regression **`tests/auto_command_contract_test.py`**; normative **`architecture.md`** **`# BUG-0006`**; **`R-0065`** basis (delivery closed **`auto-20260403-03`**).
- **`BUG-0007` (`S0068`)**: **intake evidence asked-vs-covered truthfulness** — **`INTAKE_ANSWER_REF_NOT_TOPIC_DISTINCT`** in **`intake_evidence_lib.py`** (+ **`template/`** parity), active + template **`intake.md`**, **`tests/intake_evidence_bug0007_r0066_test.py`**; normative **`architecture.md`** **`# BUG-0007`**; **`R-0066`** basis (delivery closed **`auto-20260404-01`** curator **`/refresh-context`** **`2026-04-05T01:30:00Z`**).
- **`DEC-0071` / `US-0085`**: **4-layer defense-in-depth `.env` exclusion contract** — `.gitignore` (git tracking) + `.cursorignore` (agent file tools) + Cursor rules (behavioral) + operator discipline; committed `.env.example` (20 `*Env` names only); `scripts/print_remote_env_hint.py` parity helper (names-only, exit 1 `ENV_EXAMPLE_PARITY_MISMATCH`); `tests/test_env_gitignore.py` regression; active + `template/` parity (7 touchpoints); composes with US-0064/DEC-0070/US-0084/US-0086; **`R-0072`** basis; architecture **`# US-0085`**.
- **`DEC-0072` / `US-0089`**: **Caveman mode scratchpad contract, composition surface, and default-off invariant** — Option A orthogonal composition (`TOKEN_PROFILE` owns context breadth, `CAVEMAN_MODE`/`CAVEMAN_LEVEL` own voice; neither substitutes); rule-only surface (`.cursor/rules/caveman.mdc` active + `template/`, no new skill); scratchpad keys `CAVEMAN_MODE=0|1` (default `0`), `CAVEMAN_LEVEL=lite|full|ultra` (default empty, fallback `full` when mode=1; unknown → `CAVEMAN_LEVEL_UNKNOWN`); reserved-for-US-0090 no-ops `CAVEMAN_COMPRESS_INPUT=0|1` (default `0`) and `CAVEMAN_FILE_SCOPE=` (empty); 9-zone literal-region invariant (fenced code, paths, AC checklists, reason codes, IDs, contract markers, strict-proof tuple fields, isolation fields, git refs); canonical operator phrases `caveman on|off`, `stop caveman`, `normal mode`, `caveman: lite|full|ultra`; 8 `test_caveman_default_off_*` subtests extending `tests/auto_command_contract_test.py` in place; US-0090 stays out of scope; **`R-0073`** basis; architecture **`# US-0089`**.
- **`DEC-0073` / `US-0090`**: **Caveman input-side compression — activation gate, sidecar originals, deny/allow contract, CLI, reason-code vocabulary, template + installer parity** — composes on **`DEC-0072`** (forward-link, no rewrite); default-off activation (`CAVEMAN_COMPRESS_INPUT=1` + non-empty `CAVEMAN_FILE_SCOPE` + explicit `--write`; empty scope → `CAVEMAN_COMPRESS_SCOPE_EMPTY`); parallel-tree sidecar originals at `docs/.caveman-originals/<relative/path>/<file>` (single repo-root `.gitignore` anchor + `.gitkeep`); hybrid deny-list source (hard-coded baseline + `.gitignore` secret merge + optional `.cursorignore` overlay; deny always wins; evaluation order deny-hard → ignore-merge → overlay → allow → literal-region scan → write); allow-list grammar profile `docs-prose-only` + raw CSV globs + hybrid form; **safe-mode minifier only in v1** (duplicate-blank collapse + trailing trim + LF normalize + EOF-newline preserve — strictly idempotent by construction); aggressive mode **deferred** (R8 neutralized); LLM-assisted **rejected**; 9-code reason-code vocabulary grouped Gating / Scope / Integrity families (no post-write codes); CLI `scripts/caveman_compress_input.py` with `--dry-run|--write|--verify-originals|--report`; conflict precedence → `CAVEMAN_COMPRESS_FLAG_CONFLICT`; `--purge-orphans` deferred; 9-zone literal-region invariant (DEC-0072 §4) reused verbatim; **no `.cursor/rules/caveman.mdc` subsection in v1** (R10 byte-identity preserved, pre-US-0090 SHA-256 `E10EFC32C628E790E69E2393F381108FE0B1F16E0BCDCFFFC162EFF6F91E47DE`); installer-owned-paths manifest entry mandatory for `template/scripts/caveman_compress_input.py` (R11 mitigation, BUG-0003 class); extend `check_intake_template_parity.py --scope=caveman-compress` + `tests/installer_completeness_bug0003_test.py`; stdlib Python only (no new npm / pip dep); vendor-install ban carried (DEC-0072 §8); three-axis non-substitution paragraph extends DEC-0072 §1 in runbook + auto-orchestration-reference (active + `template/`); **`R-0073`** basis (shared anchor, no new `R-xxxx`); architecture **`# US-0090`**.
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
- Index pattern: `decisions/DEC-0003.md` ... `decisions/DEC-0075.md`.
- Decision: **`DEC-0075`** — **`BUG-0009`** downstream-safe template CI vs kit-internal active CI
  and drift guard (composes on **`US-0017`** negative-parity exceptions + **`US-0008`**
  installer copy). In-place template job subtraction; active five-job positive inventory;
  guard lib split; forbidden-pattern list + reason codes; checks green-by-default; empty
  template `TEST_COMMAND`; install smoke; harness **§28B**; upgrade remediation docs — see
  **`decisions/DEC-0075.md`** and **`docs/engineering/architecture.md`** **`# BUG-0009`**.
- Decision: **`DEC-0074`** — **`US-0091`** README feature coverage predicate, validator,
  release gate composition, and grandfathering (composes on **`DEC-0059`**; extends US-0030
  doc-gate family). Backlog field **`user_visible:`** canonical; heuristic H1–H8 when
  enforce=0; validator lib split; release step **3f**; **`README_FEATURE_COVERAGE_ENFORCE`**
  scratchpad toggle; section-affinity manifest; reason-code vocabulary per AC-5; template
  parity **`--scope=readme-feature-coverage`**; harness **§27U** — see
  **`decisions/DEC-0074.md`** and **`docs/engineering/architecture.md`** **`# US-0091`**.
- Decision: **`DEC-0073`** — **`US-0090`** Caveman input-side compression
  (composes on **`DEC-0072`** via forward-link, no rewrite). Default-off
  activation gate (`CAVEMAN_COMPRESS_INPUT=1` + non-empty `CAVEMAN_FILE_SCOPE`
  + explicit `--write`; empty scope → `CAVEMAN_COMPRESS_SCOPE_EMPTY`);
  parallel-tree sidecar originals at `docs/.caveman-originals/<relative/path>/<file>`
  (repo-root `.gitignore` anchor + `.gitkeep`); hybrid deny-list (hard-coded
  baseline + `.gitignore` secret merge + optional `.cursorignore` overlay;
  deny wins over allow); allow-list grammar `docs-prose-only` profile + raw
  globs + hybrid form; safe-mode idempotent minifier only in v1
  (duplicate-blank collapse + trailing trim + LF normalize + EOF-newline
  preserve); 9-code reason-code vocabulary (scope / integrity / gating
  families); CLI flags `--dry-run` (default), `--write`, `--verify-originals`,
  `--report`; template + installer parity (`scripts/caveman_compress_input.py`
  active + `template/`, manifest entry, `check_intake_template_parity.py
  --scope=caveman-compress`, `installer_completeness_bug0003_test.py`
  fixture); `.cursor/rules/caveman.mdc` unchanged (SHA-256
  `E10EFC32…E47DE` preserved; negative parity row) — see
  **`decisions/DEC-0073.md`** and **`docs/engineering/architecture.md`**
  **`# US-0090`**.
- Decision: **`DEC-0072`** — **`US-0089`** Caveman mode scratchpad contract,
  composition surface, and default-off invariant (Option A orthogonal
  composition with `TOKEN_PROFILE`; rule-only `.cursor/rules/caveman.mdc`
  active + `template/`; locked scratchpad keys `CAVEMAN_MODE` / `CAVEMAN_LEVEL`
  plus US-0090 reserved no-ops `CAVEMAN_COMPRESS_INPUT` / `CAVEMAN_FILE_SCOPE`;
  9-zone literal-region invariant; canonical operator phrase catalog;
  8 `test_caveman_default_off_*` subtests extending
  `tests/auto_command_contract_test.py` in place) — see
  **`decisions/DEC-0072.md`** and **`docs/engineering/architecture.md`** **`# US-0089`**.
- Decision: **`DEC-0071`** — 4-layer defense-in-depth **`.env`** exclusion
  contract (`.gitignore` + `.cursorignore` + Cursor rules + operator discipline);
  committed **`.env.example`** (20 names); parity helper + regression test — see
  **`decisions/DEC-0071.md`** and **`docs/engineering/architecture.md`** **`# US-0085`**.
- Decision: **`DEC-0070`** — **`remote_config_summary.py`** when **`REMOTE_EXECUTION=0`**
  exits **0** (skip, stderr reason) — see **`decisions/DEC-0070.md`** and
  **`docs/engineering/architecture.md`** **`# US-0084`**.
