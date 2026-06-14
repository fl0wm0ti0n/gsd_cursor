# Sprint S0088 UAT — US-0098

- **Sprint**: `S0088`
- **Work item**: **US-0098** — Dev environment auto-launch profile (detect, persist, relaunch, connect)
- **Governance**: **DEC-0084** + architecture `# US-0098` + **R-0085**
- **Orchestrator run**: **auto-20260613-01**
- **Machine-readable**: `sprints/S0088/uat.json`
- **Status**: **verified** (release **2026-06-14T12:30:00Z** / `S0088` **released**)
- **Canonical backlog**: **`docs/product/backlog.md`** — **US-0098** **DONE**

## Metadata

- **author**: qa
- **qa_verdict_reference**: `sprints/S0088/qa-findings.md`
- **qa_timestamp**: 2026-06-14T11:00:00Z
- **fresh_context_marker**: qa-S0088-US0098-qa-20260614T110000Z-fresh
- **verify_work_executed_at**: `2026-06-14T12:00:00Z`
- **verify_work_fresh_context_marker**: `qa-S0088-US0098-verify-work-20260614T120000Z-fresh`

## Target acceptance criteria (from backlog `## US-0098`)

- **AC-1**: Default-off scratchpad **`DEV_AUTO_LAUNCH_PROFILE`** gate
- **AC-2**: Dev-environment profile schema v1 + template example; names-only secret refs
- **AC-3**: Four-label detection matrix (`local`, `docker-host-local`, `docker`, `ssh`); fail-closed when unresolved
- **AC-4**: **`/execute`** bounded relaunch + **`dev_to_qa.md`** evidence tuple
- **AC-5**: Operator Connect surface after relaunch (no secret values)
- **AC-6**: Compose with **US-0064**/**US-0085**/**US-0086**/**`DEV_SERVER_*`** — no parallel connectivity schema
- **AC-7**: Explicit **`refresh dev environment`** operator path
- **AC-8**: Bounded retries; **`DEV_ENV_*`** reason codes; no unbounded watch v1
- **AC-9**: Eight **`test_us0098_*`** + **`DEV_ENVIRONMENT_PAIRS`** parity + harness §26W
- **AC-10**: Architecture + runbook operator recipes

## Verdict summary

| Bucket | Count |
|--------|-------|
| PASS | 10 |
| FAIL | 0 |
| SKIP | 0 |
| PENDING | 0 |
| Total | 10 |

## Preconditions

- Python 3.12+ available.
- DEC-0084 execute deliverables merged.
- `scripts/dev_environment_lib.py` (active + template) present.

## UAT steps

### UAT-1 — Scratchpad keys — AC-1 — `verdict=PASS`

`pytest -k us0098_dev_auto_launch_scratchpad` → **`DEV_AUTO_LAUNCH_PROFILE`**, **`DEV_ENVIRONMENT_CONFIG`** documented; default **`off`**.

### UAT-2 — Profile schema — AC-2 — `verdict=PASS`

`pytest -k us0098_dev_environment_schema` → example path + gitignore + schema fields.

### UAT-3 — Detection matrix — AC-3 — `verdict=PASS`

`pytest -k us0098_detection_mode` → four modes + **US-0086** precedence.

### UAT-4 — Execute step 24 — AC-4, AC-7 — `verdict=PASS`

`pytest -k us0098_execute` + refresh phrase test → 24a–24d + evidence tuple + refresh phrase.

### UAT-5 — Connect block — AC-5 — `verdict=PASS`

`pytest -k us0098_connect_block` → mandatory Connect field names.

### UAT-6 — Composition — AC-6 — `verdict=PASS`

`pytest -k us0098_us0086_compose` → **`release-targets.json`** schema unchanged.

### UAT-7 — Reason codes — AC-8 — `verdict=PASS`

`pytest -k us0098_reason_code` → **`DEV_ENV_PROFILE_*`**, **`DEV_ENV_RELAUNCH_*`** inventory.

### UAT-8 — Helper self-test — AC-9 — `verdict=PASS`

`python scripts/dev_environment_lib.py --self-test` → **`[DEV_ENVIRONMENT_SELF_TEST_OK]`**.

### UAT-9 — Template parity — AC-9 — `verdict=PASS`

`python scripts/check_intake_template_parity.py --scope=dev-environment` → **`[INTAKE_TEMPLATE_PARITY_OK]`**.

### UAT-10 — Runbook recipes — AC-10 — `verdict=PASS`

Runbook § dev auto-launch operator recipes present.

## AC ↔ UAT results summary

AC-1..AC-10 verified at verify-work via UAT-1..UAT-10 (all PASS). UAT-10 satisfied via **procedural attestation** per runbook § **Dev environment auto-launch** (live operator E2E not runnable in fresh QA subagent per **BUG-0006**).

## Next

- **`/release`** (fresh **release**) for **`S0088`** / **`US-0098`**.
