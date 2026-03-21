# Decisions

## Current context pack (2026-03-24 — post-release S0053 / US-0074)

- Latest completed/released stories (high-signal):
  - `US-0074` (`S0053`, released), governed by **`DEC-0056`** (baseline version-sync +
    `TEST_COMMAND` bootstrap; npm ↔ Homebrew stable; triple installer + CLI + `template/`
    parity).
  - `US-0073` (`S0052`, released), governed by **`DEC-0055`** (scratchpad Model B).
  - `US-0072` (`S0051`, released), governed by **`DEC-0054`** (triad hot-surface compaction).
  - `US-0071` (`S0050`, released), governed by **`DEC-0053`** (user-visible metadata guard).
  - `US-0070` (`S0049`, released), governed by **`DEC-0052`**.
  - `US-0069` (`S0048`, released), governed by **`DEC-0051`**.
- Hot surface: **`/refresh-context`** after **`S0053`** — triad
  `scripts/enforce-triad-hot-surface.py`: post-checkpoint-append **`--check`** →
  **`ARTIFACT_HOT_SURFACE_OVERSIZE`** on `state.md` → **`--rollover`** (**`units=4`**) →
  `docs/engineering/state-archive/state-pack-20260321-k.md` → final **`--check` PASS**
  (see `## Refresh-context checkpoint (2026-03-24) — post S0053 / US-0074` in `state.md`).
- Next prioritized open story: **none** — `docs/product/backlog.md` has **no** `Status: OPEN`
  rows after **`US-0074`** **DONE**; next work enters via **`/intake`** when prioritized.
- Active workflow target: operator **`none`** or **`/intake`** for net-new backlog items.
- Continuation hygiene: `handoffs/resume_brief.md` aligned post-refresh-context
  (`intended_resume_phase=none` unless operator selects new work).
- Traceability (**DEC-0010**):
  - `| US-0074 | S0053 | T-001..T-010 | DONE |` — evidence in `sprints/S0053/summary.md`,
    `sprints/S0053/qa-findings.md`, `sprints/S0053/uat.json`, `sprints/S0053/uat.md`,
    `sprints/S0053/release-findings.md`, `handoffs/releases/S0053-release-notes.md`,
    `tests/report.md`, `decisions/DEC-0056.md`, `scripts/enforce-triad-hot-surface.py`.
  - `| US-0073 | S0052 | T-001..T-010 | DONE |` — prior sprint evidence unchanged
    (`sprints/S0052/*`, `handoffs/releases/S0052-release-notes.md`).
- No open decision gate at this boundary.

## Compact decision index (bounded summaries)

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
- Index pattern: `decisions/DEC-0003.md` ... `decisions/DEC-0056.md`.
