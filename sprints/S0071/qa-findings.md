# QA findings — Sprint S0071 (US-0087)

- **Verdict**: **PASS** — mandatory **`TEST_COMMAND`** (**`tests/run-tests.ps1`**) **exit 0** after **DEC-0054** triad hygiene; no blocking findings for in-scope **US-0087** acceptance.
- **Orchestrator run**: **`auto-20260405-01`**
- **Sprint**: **`S0071`**
- **Story**: **`US-0087`** — `/auto` explicit bug targeting (docs + contract tests + template parity); canonical backlog remains **OPEN** (**`US-0045`**) until **`/verify-work`** / release closure.
- **QA executed**: **`2026-04-07T21:07:00Z`** (final harness report timestamp **`tests/report.md`**)

## Prior cycle (historical)

- Initial **`/qa`** **FAIL** (**`2026-04-07T20:30:33Z`**, **790**/4) — **`sprints/S0071/qa-findings.md`** (prior revision), **`handoffs/qa_to_dev.md`**.
- **Dev remediation** — **`handoffs/dev_to_qa.md`** (top block): harness precedence substring, **`RELEASE_PUBLISH_MODE=confirm`**, scratchpad pair parity (**`AUTO_BUG_*`** + US-0087 catalog).

## This pass (post-remediation, fresh `fresh_context_marker`)

### Test plan (runbook)

| Check | Config / command | Result | Notes |
|------|------------------|--------|--------|
| **TEST_COMMAND** | `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` | **PASS** (exit **0**) | Final evidence: **`tests/report.md`** — **Pass: 794**, **Fail: 0** @ **`2026-04-07T20:56:59Z`** |
| **TEST_COMMAND** (first attempt) | same | **FAIL** (exit **1**) | **`2026-04-07T20:55:41Z`** — **792**/2; only **`[FAIL] triad check passes on repo`** + **`idempotent rerun`** — **`STATE_ARCHIVE_REQUIRED`** / **`ARTIFACT_HOT_SURFACE_OVERSIZE`** on **`docs/engineering/state.md`** (**1231**/1200 lines). **Not** a **US-0087** product defect. |
| **Triad rollover (QA, pre-harness)** | `python scripts/enforce-triad-hot-surface.py --rollover` | **PASS** | **`rollover_complete units=1`** → **`docs/engineering/state-archive/state-pack-20260407-b.md`** |
| **Triad check** | `python scripts/enforce-triad-hot-surface.py --check` | **PASS** (exit **0**) | After pre-harness rollover, before final **`TEST_COMMAND`** |
| **Triad rollover (QA, post-state-append)** | `python scripts/enforce-triad-hot-surface.py --rollover` | **PASS** | After **`docs/engineering/state.md`** QA checkpoint + verify-work spawn breadcrumb: **`rollover_complete units=2`** → **`docs/engineering/state-archive/state-pack-20260407-c.md`**; final **`--check`** **PASS** |
| **User-visible metadata** | `python scripts/check-user-visible-metadata.py` | **PASS** (exit **0**) | Fixture **`tests/.tmp-meta-leak/bin/leak-test.js`** still emits detector output during harness; canonical checker on repo roots **PASS** |
| **Scratchpad pair parity** | `python scripts/check-scratchpad-pair-parity.py --repo .` | **PASS** | **`[SCRATCHPAD_PAIR_OK]`** |
| **LINT_COMMAND** | *(blank in runbook)* | **skipped** | Per **`US-0039`** optional-command rules |
| **TYPECHECK_COMMAND** | *(blank in runbook)* | **skipped** | Per **`US-0039`** optional-command rules |
| **SECURITY_REVIEW** | **`SECURITY_REVIEW=0`** (merged scratchpad) | **skipped** | No mandatory **`docs/engineering/security-review.md`** gate |
| **CROSS_REPO_OBSERVABILITY** | **`0`** | **skipped** | Zero required overhead |
| **COMPONENT_SCOPE_MODE** | **`0`** | **skipped** | Zero required overhead |
| **SPEC_PACK_MODE** | **`0`** | **skipped** | Zero required overhead |
| **USER_GUIDE_MODE** | **`0`** | **skipped** | Zero required overhead |

### Targeted regression (story scope)

| Command | Result |
|---------|--------|
| `python -m pytest tests/auto_command_contract_test.py -q` | **PASS** (7 tests, 41 subtests) |

### Remote / environment (**US-0084**)

- **`REMOTE_EXECUTION=1`** on merged scratchpad; **`handoffs/dev_to_qa.md`** (remediation block): **local Windows**, repo root **`c:\flowGit\sonstiges\gsd_cursor`**; **`TEST_COMMAND`** and gates executed **locally** (names-only; no secrets pasted).

### US-0065 / US-0066 (contract)

- **Runtime autopilot (**`US-0065`**)**: **N/A** — no shipped application runtime; schema fields not applicable beyond **`runtime_final_verdict=n/a`**, **`runtime_reason_code=n/a`**, **`runtime_evidence_refs=sprints/S0071/qa-findings.md`**.
- **Generated baseline tests (**`US-0066`**)**: **`generated_test_stack_profile=python`**, **`generated_test_command=TEST_COMMAND`**, **`generated_test_result=pass`**, **`generated_test_output_ref=tests/report.md`**, **`generated_test_paths_ref=tests/`**, **`generated_test_reason_code=(none)`**.

## Severity

| ID | Severity | Blocking | Reason code |
|----|----------|----------|-------------|
| — | — | no | No open blockers |

## Sync policy snapshot (**DEC-0018**)

- **`push_decision=not_eligible|manual`** (operator/CI); **`PRE_QA_AUTOPUSH_FORBIDDEN`** lifted for **QA blockers** — **`TEST_COMMAND`** green; remaining eligibility = branch policy + **`ALLOW_AUTO_PUSH`** + optional lint/typecheck when configured.
- **`reason_code=(none)`** for **BLOCKING_QA_FINDINGS** / **TEST_FAILED** on this pass.

## Next phase

- **`/verify-work`** (fresh **qa** context) — **`next_scheduled_phase=verify-work`**.
