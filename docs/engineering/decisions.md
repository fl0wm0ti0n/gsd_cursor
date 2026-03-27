# Decisions

## Current context pack (2026-03-28 — post-refresh-context US-0077 / S0056 / auto-20260327-02 closed)

- **`US-0077`** (**`S0056`**): **DONE** / **released**; evidence **`sprints/S0056/release-findings.md`**, **`handoffs/releases/S0056-release-notes.md`**, **`## Refresh-context checkpoint (2026-03-28) — post S0056 / US-0077 (auto-20260327-02)`** in **`docs/engineering/state.md`** (`orchestrator_run_id=auto-20260327-02`, `stop_reason=completed`, `next_scheduled_phase=none`).
- Migration default: explicit scratchpad keys **`DOC_AUDIENCE_PROFILE`** / **`DOC_DETAIL_LEVEL`** recommended (`both` / `balanced`); **absent keys** on merged scratchpad resolve to **`both`×`balanced`** for resolver/tests per **DEC-0059** §6 until a future cutover mandates explicit keys in CI.
- **`US-0076`** (**`S0055`**): **DONE** / **released**; evidence **`sprints/S0055/release-findings.md`**, **`handoffs/releases/S0055-release-notes.md`**, **`## Refresh-context checkpoint (2026-03-27) — post S0055 / US-0076`** in **`docs/engineering/state.md`** (`orchestrator_run_id=auto-20260327-01`, `stop_reason=completed`).
- Active workflow target: **`/intake`** when new work is prioritized (no scheduled auto phase; queue idle).
- Research: **`R-0053`** (closed with **US-0076**); **`R-0054`** — retained for **US-0077** matrix traceability; normative lock-in **`DEC-0059`** + **`architecture.md`** **`# US-0077`** (delivery closure noted in **`docs/engineering/research.md`**).
- Decision: **`DEC-0059`** — profile semantics, **`docs/developer/README.md`** shard, H2 mapping, validator **`scripts/validate_doc_profile.py`**, tiered **AC-8** tests, migration defaults — see **`decisions/DEC-0059.md`** and **`docs/engineering/architecture.md`** **`# US-0077`**.
- Continuation hygiene: **`handoffs/resume_brief.md`** → **`none`** + **`/intake`**.
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
- Hot surface: at **`/refresh-context` (2026-03-28)**, post-append **`state.md`** oversize → **`rollover_complete units=1`** → **`docs/engineering/state-archive/state-pack-20260327-q.md`**; final triad **`--check`** **PASS** (see **`## Refresh-context checkpoint (2026-03-28) — post S0056 / US-0077 (auto-20260327-02)`**).
- Traceability (**DEC-0010**):
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
- Index pattern: `decisions/DEC-0003.md` ... `decisions/DEC-0059.md`.
