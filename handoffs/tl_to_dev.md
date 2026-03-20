## TL -> Dev Handoff — Sprint S0050 (US-0071 User-Visible Internal Metadata Sanitization Guard)

## Planning summary

- **Sprint**: S0050 (new)
- **Story**: US-0071 — User-visible internal metadata sanitization guard
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage intent**: AC-1..AC-10 mapped 1:1 to `T-001..T-010` in `sprints/S0050/tasks.md`

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0071 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0071 section)
- Decision: `decisions/DEC-0053.md`
- Research: `docs/engineering/research.md` (`R-0046`)
- PO -> TL handoff: `handoffs/po_to_tl.md` (Discovery Addendum — US-0071)
- Sprint artifacts: `sprints/S0050/*`

## Focus

1. **Policy + allowlist (T-001..T-002)**: forbidden planning-shaped tokens in user-visible outputs only; explicit internal surfaces + comments-not-strings rule.
2. **Enforcement chain (T-003..T-005)**: `/execute` default guard, `/qa` automated scan with fail-closed diagnostics, structured findings with path evidence and remediation.
3. **Vocabulary + precision (T-006..T-007)**: shared reason codes; no false blocks on allowlisted docs/comments.
4. **Parity + evidence (T-008..T-010)**: active/template alignment, regression matrix (positive/negative/allowlist/idempotence), release attestation that checks ran.

## Execution order

Run tasks `T-001`..`T-010` in sequence (see `sprints/S0050/tasks.md`).

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0050/tasks.md` marked done.
- `sprints/S0050/plan-verify.json` confirms AC-1..AC-10 coverage with no gaps (**PASS** after `/plan-verify`).
- `sprints/S0050/progress.md`, `sprints/S0050/uat.json`, and `sprints/S0050/uat.md` updated with implementation evidence.
- `docs/engineering/state.md` includes lifecycle checkpoint traceability for `US-0071`.

## Next phase

Plan-verify **PASS** for **`S0050`** (`sprints/S0050/plan-verify.json`). Proceed to **`/execute`** for **`S0050`** (`US-0071`).

---

## TL -> Dev Handoff — Sprint S0049 (US-0070 Configurable Auto Phase Selection Policy)

## Planning summary

- **Sprint**: S0049 (new)
- **Story**: US-0070 — Scratchpad-controlled `/auto` phase selection policy
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage intent**: AC-1..AC-10 mapped 1:1 to `T-001..T-010` in `sprints/S0049/tasks.md`

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0070 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0070 section)
- Decision: `decisions/DEC-0052.md`
- Research: `docs/engineering/research.md` (`R-0049`)
- PO -> TL handoff: `handoffs/po_to_tl.md` (Discovery Addendum — US-0070)
- Sprint artifacts: `sprints/S0049/*`

## Focus

1. **Policy contract + conflict gate (T-001)**: single active selector (`AUTO_PHASE_PLAN` / `EXCLUDE` / `INCLUDE` / `PROFILE`) and `PHASE_POLICY_CONFLICT` per `DEC-0052`.
2. **Plan materialization + breadcrumbs (T-002..T-005)**: ordered canonical plan, non-skippable reinstatement, `start-from` intersection, fail-closed invalid tokens.
3. **Continuation + modes (T-006..T-007)**: backlog-drain, bulk execute, team paths, and resume parity — reload policy, recompute plan, no silent phase revival.
4. **Parity + regression + operator UX (T-008..T-010)**: active/template docs, test coverage, boundary status with selected/skipped + reason codes.

## Execution order

Run tasks `T-001`..`T-010` in sequence (see `sprints/S0049/tasks.md`).

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0049/tasks.md` marked done.
- `sprints/S0049/plan-verify.json` confirms AC-1..AC-10 coverage with no gaps (**PASS** after `/plan-verify`).
- `sprints/S0049/progress.md`, `sprints/S0049/uat.json`, and `sprints/S0049/uat.md` updated with implementation evidence.
- `docs/engineering/state.md` includes lifecycle checkpoint traceability for `US-0070`.

## Next phase

Proceed to **`/execute`** for `S0049` (`US-0070`). Plan-verify: **PASS** (`sprints/S0049/plan-verify.json`).

---

## TL -> Dev Handoff — Sprint S0048 (US-0069 Strict Phase Role Enforcement in /auto)

## Planning summary

- **Sprint**: S0048 (new)
- **Story**: US-0069 — Strict phase role enforcement in `/auto` orchestration
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage intent**: AC-1..AC-10 mapped 1:1 to `T-001..T-010` in `sprints/S0048/tasks.md`

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0069 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0069 section)
- Decision: `decisions/DEC-0051.md`
- Research: `docs/engineering/research.md` (`R-0048`)
- PO -> TL handoff: `handoffs/po_to_tl.md` (Discovery Addendum — US-0069)
- Sprint artifacts: `sprints/S0048/*`

## Focus

1. **Contract + single-valued roles (T-001)**: canonical phase→role matrix and scratchpad alternate resolution per `DEC-0051`.
2. **Preflight + fail-closed spawn (T-002..T-004)**: `PHASE_ROLE_CAPABILITY_MISSING`, checkpoint `PHASE_ROLE_MISMATCH`, and full diagnostics.
3. **Execute default deny + resume parity (T-005..T-006)**: override governance ref path; no stale resume bypass.
4. **Parity + regression + vocabulary + release evidence (T-007..T-010)**: active/template docs, tests, reason-code docs, readiness citations.

## Execution order

Run tasks `T-001`..`T-010` in sequence (see `sprints/S0048/tasks.md`).

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0048/tasks.md` marked done.
- `sprints/S0048/plan-verify.json` confirms AC-1..AC-10 coverage with no gaps (**PASS**; recorded 2026-03-20).
- `sprints/S0048/progress.md`, `sprints/S0048/uat.json`, and `sprints/S0048/uat.md` updated with implementation evidence.
- `docs/engineering/state.md` includes lifecycle checkpoint traceability for `US-0069`.

## Next phase

Proceed to **`/execute`** for `S0048` (`US-0069`).

---

## TL -> Dev Handoff — Sprint S0047 (US-0068 Mandatory Intake Question Packs)

## Planning summary

- **Sprint**: S0047 (new)
- **Story**: US-0068 — Mandatory intake question packs for first and small intakes
- **Task count**: 11 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage intent**: AC-1..AC-10 mapped in `sprints/S0047/tasks.md` (remediation applied for AC-8/AC-9/AC-10)

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0068 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0068 section)
- Decision: `decisions/DEC-0050.md`
- Research: `docs/engineering/research.md` (`R-0045`, baseline `R-0041`)
- PO -> TL handoff: `handoffs/po_to_tl.md` (US-0068 discovery addendum)
- Sprint artifacts: `sprints/S0047/*`

## Focus

1. **Deterministic pack schemas (T-001..T-003)**: define machine-verifiable first/small intake topic coverage with required/optional classification.
2. **Fail-closed persistence policy (T-004..T-008)**: block writes on missing required coverage, allow explicit bounded assumptions, and emit deterministic reason codes.
3. **Parity + regression + fallback (T-009..T-011)**: cover active/template parity (AC-8), explicit regression matrix (AC-9), and deterministic unknown-stack fallback (AC-10).

## Execution order

Run tasks `T-001`..`T-011` in sequence (see `sprints/S0047/tasks.md`).

## Done criteria for Dev completion

- All 11 tasks in `sprints/S0047/tasks.md` marked done.
- `sprints/S0047/plan-verify.json` confirms AC-1..AC-10 coverage with no gaps.
- `sprints/S0047/progress.md`, `sprints/S0047/uat.json`, and `sprints/S0047/uat.md` updated with implementation evidence.
- `docs/engineering/state.md` includes lifecycle checkpoint traceability for `US-0068`.

## Next phase

Proceed to **`/execute`** for `S0047` (`US-0068`) after `/plan-verify`.

---

## TL -> Dev Handoff — Sprint S0046 (US-0067 Release Operator Run/Connect/Verify Hints Contract)

## Planning summary

- **Sprint**: S0046 (new)
- **Story**: US-0067 — Release operator Run/Connect/Verify hints contract
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage**: AC-1..AC-10 verified PASS in `sprints/S0046/plan-verify.json`

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0067 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0067 section)
- Decision: `decisions/DEC-0049.md`
- Research: `docs/engineering/research.md` (`R-0044`, baseline `R-0041`)
- PO -> TL handoff: `handoffs/po_to_tl.md` (US-0067 discovery addendum)
- Sprint artifacts: `sprints/S0046/*`

## Focus

1. **Canonical schema + required fields (T-001..T-003)**: fixed-order `Run -> Connect -> Verify -> Credentials(env-ref only) -> Known Issues` contract with required operator fields and credentials safety boundary.
2. **Fail-closed release and context alignment (T-004..T-007)**: deterministic latest-pointer parity, missing/ambiguous field blocking, runtime context (`local|remote`) explicitness, and QA/release evidence linkage.
3. **Parity + deterministic reruns (T-008..T-010)**: active/template parity, regression coverage, and idempotent concise operator-facing release output.

## Execution order

Run tasks `T-001`..`T-010` in sequence (see `sprints/S0046/tasks.md`).

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0046/tasks.md` marked done.
- `sprints/S0046/plan-verify.json` confirms AC-1..AC-10 coverage with no gaps.
- `sprints/S0046/progress.md`, `sprints/S0046/uat.json`, and `sprints/S0046/uat.md` updated with implementation evidence.
- `docs/engineering/state.md` includes lifecycle checkpoint traceability for `US-0067`.

## Next phase

Proceed to **`/execute`** for `S0046` (`US-0067`) after `/plan-verify`.

---

## TL -> Dev Handoff — Sprint S0045 (US-0066 Generated Test Scaffolding + Auto-Run)

## Planning summary

- **Sprint**: S0045 (new)
- **Story**: US-0066 — Generated test scaffolding + auto-run contract for app projects
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage intent**: AC-1..AC-10 mapped in `sprints/S0045/tasks.md`

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0066 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0066 section)
- Decision: `decisions/DEC-0048.md`
- Research: `docs/engineering/research.md` (`R-0043`, baseline `R-0041`)
- PO -> TL handoff: `handoffs/po_to_tl.md` (US-0066 section/addendum)
- Sprint artifacts: `sprints/S0045/*`

## Focus

1. **Scaffold generation contract (T-001..T-003)**: stack detection, missing-asset generation, and deterministic baseline `TEST_COMMAND` runbook wiring.
2. **QA and fail-safe behavior (T-004..T-007)**: automatic generated-test execution, unsupported-stack diagnostics, non-destructive merge precedence, and runtime-autopilot integration boundary.
3. **Parity + evidence (T-008..T-010)**: active/template parity, regression coverage, and deterministic release/readiness evidence references.

## Execution order

Run tasks `T-001`..`T-010` in sequence (see `sprints/S0045/tasks.md`).

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0045/tasks.md` marked done.
- `sprints/S0045/plan-verify.json` confirms AC-1..AC-10 coverage with no gaps.
- `sprints/S0045/progress.md`, `sprints/S0045/uat.json`, and `sprints/S0045/uat.md` updated with implementation evidence.
- `docs/engineering/state.md` includes lifecycle checkpoint traceability for `US-0066`.

## Next phase

Proceed to **`/execute`** for `S0045` (`US-0066`) after `/plan-verify`.

---

## TL -> Dev Handoff — Sprint S0044 (US-0065 Runtime QA Autopilot)

## Planning summary

- **Sprint**: S0044 (new)
- **Story**: US-0065 — Runtime QA Autopilot for generated projects (startup/connectivity/logs/bounded debug retries)
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage intent**: AC-1..AC-10 mapped in `sprints/S0044/tasks.md`

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0065 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0065 section)
- Decision: `decisions/DEC-0047.md`
- Research: `docs/engineering/research.md` (`R-0042`, baseline `R-0041`)
- PO -> TL handoff: `handoffs/po_to_tl.md` (US-0065 section/addendum)
- Sprint artifacts: `sprints/S0044/*`

## Focus

1. **Mandatory runtime truth path (T-001..T-004)**: startup, connectivity, log scan, bounded retries, and auditable evidence schema.
2. **Deterministic runtime policy (T-005..T-008)**: stack-profile resolution, webapp/browser checks, debug escalation, and remote-runtime compatibility.
3. **Parity + verification (T-009..T-010)**: active/template contract parity and deterministic regression paths.

## Execution order

Run tasks `T-001`..`T-010` in sequence (see `sprints/S0044/tasks.md`).

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0044/tasks.md` marked done.
- `sprints/S0044/plan-verify.json` confirms AC-1..AC-10 coverage with no gaps.
- `sprints/S0044/progress.md`, `sprints/S0044/uat.json`, and `sprints/S0044/uat.md` updated with implementation evidence.
- `docs/engineering/state.md` includes lifecycle checkpoint traceability for `US-0065`.

## Next phase

Proceed to **`/execute`** for `S0044` (`US-0065`) after `/plan-verify`.

---

# TL -> Dev Handoff — Sprint S0043 (US-0063 OS-Aware Runbook Bootstrap)

## Planning summary

- **Sprint**: S0043 (new)
- **Story**: US-0063 — OS-aware runbook command auto-bootstrap with verified
  quality gates
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage**: AC-1..AC-10 verified PASS in `sprints/S0043/plan-verify.json`.

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0063 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0063 section)
- Decision: `decisions/DEC-0046.md`
- Research: `docs/engineering/research.md` (`R-0039`)
- PO -> TL handoff: `handoffs/po_to_tl.md` (US-0063 section)
- Sprint artifacts: `sprints/S0043/*`

## Focus

1. **Bootstrap contract + detection (T-001..T-004)**: precedence model, OS/stack
   detection, and deterministic validation diagnostics.
2. **Gate and safety behavior (T-005..T-007)**: keep mandatory baseline command
   policy and preserve user overrides on reruns.
3. **Parity + verification (T-008..T-010)**: active/template parity with
   installer/CLI/docs/tests updates.

## Execution order

Run tasks `T-001`..`T-010` in sequence (see `sprints/S0043/tasks.md`).

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0043/tasks.md` marked done.
- `sprints/S0043/plan-verify.json` confirms AC-1..AC-10 coverage with no gaps.
- `sprints/S0043/progress.md`, `sprints/S0043/uat.json`, and
  `sprints/S0043/uat.md` updated with implementation evidence.
- `docs/engineering/state.md` includes checkpoint traceability for `US-0063`.

## Next phase

Proceed to **`/execute`** for `S0043` (`US-0063`).

---

# TL -> Dev Handoff — Sprint S0041 (US-0064 Remote Connectivity Contract)

## Planning summary

- **Sprint**: S0041 (new)
- **Story**: US-0064 — Remote runtime connectivity contract for QA/release/publish
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage**: AC-1..AC-10 verified PASS in `sprints/S0041/plan-verify.json`.

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0064 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0064 section)
- Decision: `decisions/DEC-0044.md`
- Research: `docs/engineering/research.md` (`R-0040`)
- PO -> TL handoff: `handoffs/po_to_tl.md` (US-0064 section)
- Sprint artifacts: `sprints/S0041/*`

## Focus

1. **Schema + validation (T-001..T-004)**: connectivity metadata + docker-over-ssh
   support and deterministic validation diagnostics.
2. **Phase integration (T-005..T-007)**: remote-aware release/qa/execute behavior
   and canonical operator connectivity doc.
3. **Parity + verification (T-008..T-010)**: active/template parity, tests, and docs.

## Execution order

Run tasks `T-001`..`T-010` in sequence (see `sprints/S0041/tasks.md`).

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0041/tasks.md` marked done.
- `sprints/S0041/plan-verify.json` confirms AC-1..AC-10 coverage with no gaps.
- `sprints/S0041/progress.md`, `sprints/S0041/uat.json`, and
  `sprints/S0041/uat.md` updated with implementation evidence.
- `docs/engineering/state.md` includes checkpoint traceability for `US-0064`.

## Next phase

Proceed to **`/execute`** for `S0041` (`US-0064`).

---

# TL -> Dev Handoff — Sprint S0040 (US-0061 Ownership Guard + Archive Control)

## Planning summary

- **Sprint**: S0040 (new)
- **Story**: US-0061 — Cross-phase artifact ownership guard and deterministic
  archive control
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage**: AC-1..AC-10 verified PASS in `sprints/S0040/plan-verify.json`.

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0061 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0061 section)
- Decision: `decisions/DEC-0043.md`
- Research: `docs/engineering/research.md` (`R-0037`)
- PO -> TL handoff: `handoffs/po_to_tl.md` (US-0061 section/addendum)
- Sprint artifacts: `sprints/S0040/*`

## Focus

1. **Ownership matrix + fail-safe (T-001..T-004)**: define phase ownership,
   non-destructive mutation rules, and override evidence requirements.
2. **Archive verification control (T-005..T-006)**: deterministic archive
   verification outputs and fail-safe mismatch behavior.
3. **Parity + validation (T-007..T-010)**: preserve existing canonical
   contracts and add regression/test/doc updates.

## Execution order

Run tasks `T-001`..`T-010` in sequence (see `sprints/S0040/tasks.md`).

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0040/tasks.md` marked done.
- `sprints/S0040/plan-verify.json` confirms AC-1..AC-10 coverage with no gaps.
- `sprints/S0040/progress.md`, `sprints/S0040/uat.json`, and
  `sprints/S0040/uat.md` updated with implementation evidence.
- `docs/engineering/state.md` includes checkpoint traceability for `US-0061`.

## Next phase

Proceed to **`/execute`** for `S0040` (`US-0061`).

---

# TL -> Dev Handoff — Sprint S0039 (US-0060 State Rollover Enforcement)

## Planning summary

- **Sprint**: S0039 (new)
- **Story**: US-0060 — Deterministic state hot-surface rollover and archive enforcement
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage**: AC-1..AC-10 verified PASS in `sprints/S0039/plan-verify.json`.

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0060 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0060 section)
- Decision: `decisions/DEC-0042.md`
- Research: `docs/engineering/research.md` (`R-0036`)
- PO -> TL handoff: `handoffs/po_to_tl.md` (US-0060 section/addendum)
- Sprint artifacts: `sprints/S0039/*`

## Focus

1. **Threshold contract (T-001..T-003)**: deterministic rollover triggers and
   refresh-context enforcement.
2. **Archive safety (T-004..T-006)**: non-destructive history retention,
   idempotent partitioning, and fail-safe diagnostics.
3. **Parity + validation (T-007..T-010)**: ordering compatibility, docs, tests,
   and release traceability.

## Execution order

Run tasks `T-001`..`T-010` in sequence (see `sprints/S0039/tasks.md`).

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0039/tasks.md` marked done.
- `sprints/S0039/plan-verify.json` confirms AC-1..AC-10 coverage with no gaps.
- `sprints/S0039/progress.md`, `sprints/S0039/uat.json`, and
  `sprints/S0039/uat.md` updated with implementation evidence.
- `docs/engineering/state.md` includes checkpoint traceability for `US-0060`.

## Next phase

Proceed to **`/execute`** for `S0039` (`US-0060`).

---

# TL -> Dev Handoff — Sprint S0038 (US-0059 Intake Capability Guard + Drift Safety)

## Planning summary

- **Sprint**: S0038 (new)
- **Story**: US-0059 — Deterministic intake runtime capability guard and
  single-writer drift safety
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage**: AC-1..AC-10 verified PASS in `sprints/S0038/plan-verify.json`.

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0059 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0059 section)
- Decision: `decisions/DEC-0041.md`
- Research: `docs/engineering/research.md` (`R-0035`)
- PO -> TL handoff: `handoffs/po_to_tl.md` (US-0059 section/addendum)
- Sprint artifacts: `sprints/S0038/*`

## Focus

1. **Capability fail-fast (T-001..T-003)**: deterministic preflight and explicit
   fallback policy.
2. **Single-writer drift safety (T-004..T-006)**: self-write-aware drift
   semantics and fail-safe external conflict behavior.
3. **Parity + validation (T-007..T-010)**: active/template parity, tests, docs,
   and release traceability.

## Execution order

Run tasks `T-001`..`T-010` in sequence (see `sprints/S0038/tasks.md`).

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0038/tasks.md` marked done.
- `sprints/S0038/plan-verify.json` confirms AC-1..AC-10 coverage with no gaps.
- `sprints/S0038/progress.md`, `sprints/S0038/uat.json`, and
  `sprints/S0038/uat.md` updated with implementation evidence.
- `docs/engineering/state.md` includes checkpoint traceability for `US-0059`.

## Next phase

Proceed to **`/execute`** for `S0038` (`US-0059`).

---

# TL -> Dev Handoff — Sprint S0037 (US-0058 Deterministic Artifact Ordering)

## Planning summary

- **Sprint**: S0037 (new)
- **Story**: US-0058 — Deterministic artifact ordering and write discipline
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage**: AC-1..AC-10 verified PASS in `sprints/S0037/plan-verify.json`.

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0058 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0058 section)
- Decision: `decisions/DEC-0040.md`
- Research: `docs/engineering/research.md` (`R-0033`)
- PO -> TL handoff: `handoffs/po_to_tl.md` (US-0058 section)
- Sprint artifacts: `sprints/S0037/*`

## Focus

1. **Ordering matrix + fail-safe (T-001..T-005)**: define canonical policy and
   command-level fail-safe anchor behavior.
2. **Idempotence + guarantees (T-006..T-008)**: preserve canonical ownership
   contracts while enforcing deterministic ordering.
3. **Validation + docs (T-009..T-010)**: regression coverage and operator docs.

## Execution order

Run tasks `T-001`..`T-010` in sequence (see `sprints/S0037/tasks.md`).

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0037/tasks.md` marked done.
- `sprints/S0037/plan-verify.json` confirms AC-1..AC-10 coverage with no gaps.
- `sprints/S0037/progress.md`, `sprints/S0037/uat.json`, and
  `sprints/S0037/uat.md` updated with implementation evidence.
- `docs/engineering/state.md` includes checkpoint traceability for `US-0058`.

## Next phase

Proceed to **`/execute`** for `S0037` (`US-0058`).

---

# TL -> Dev Handoff — Sprint S0036 (US-0057 Upgrade-Safe Scratchpad Example Refresh)

## Planning summary

- **Sprint**: S0036 (new)
- **Story**: US-0057 — Upgrade-safe scratchpad local example refresh and parity
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage**: AC-1..AC-10 verified PASS in `sprints/S0036/plan-verify.json`.

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0057 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0057 section)
- Decision: `decisions/DEC-0039.md`
- Research: `docs/engineering/research.md` (`R-0032`)
- PO -> TL handoff: `handoffs/po_to_tl.md` (US-0057 section)
- Sprint artifacts: `sprints/S0036/*`

## Focus

1. **Ownership + refresh semantics (T-001..T-004)**: enforce framework-owned
   example refresh with deterministic diagnostics while preserving user-local
   scratchpad values.
2. **Parity + drift prevention (T-005..T-008)**: keep active/template and
   installer parity so new flags appear in refreshed example surfaces.
3. **Validation + docs (T-009..T-010)**: regression coverage and operator-facing
   README/runbook guidance.

## Execution order

Run tasks `T-001`..`T-010` in sequence (see `sprints/S0036/tasks.md`).

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0036/tasks.md` marked done.
- `sprints/S0036/plan-verify.json` confirms AC-1..AC-10 coverage with no gaps.
- `sprints/S0036/progress.md`, `sprints/S0036/uat.json`, and
  `sprints/S0036/uat.md` updated with implementation evidence.
- `docs/engineering/state.md` traceability/checkpoints updated for `US-0057`.

## Execution guardrails

- Preserve user ownership for `.cursor/scratchpad.local.md`.
- Keep framework refresh deterministic for `.cursor/scratchpad.local.example.md`.
- Maintain parity across installer scripts and template docs/files.

## Next phase

Proceed to **`/execute`** for `S0036` (`US-0057`).

---

# TL -> Dev Handoff — Sprint S0035 (US-0056 Strict Runtime Proof for Per-Phase Isolation)

## Planning summary

- **Sprint**: S0035 (new)
- **Story**: US-0056 — Strict Runtime Proof for Per-Phase Subagent Isolation
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage**: AC-1..AC-10 verified PASS in `sprints/S0035/plan-verify.json`.

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0056 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0056 section)
- Decision: `decisions/DEC-0038.md`
- Research: `docs/engineering/research.md` (`R-0034`)
- PO -> TL handoff: `handoffs/po_to_tl.md` (US-0056 section/addendum)
- Sprint artifacts: `sprints/S0035/*`

## Focus

1. **Strict tuple contract (T-001..T-004)**: require deterministic runtime
   attestation fields and fail-closed reason-code taxonomy.
2. **Boundary integration (T-005..T-006)**: enforce strict-proof checks in
   `/auto`, `/verify-work`, and `/release` contracts.
3. **Operator + compatibility guidance (T-007..T-010)**: bounded legacy handling,
   diagnostics, tests, and active/template parity.

## Execution order

Run tasks `T-001`..`T-010` in sequence (see `sprints/S0035/tasks.md`).

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0035/tasks.md` marked done.
- `sprints/S0035/plan-verify.json` confirms AC-1..AC-10 coverage with no gaps.
- `sprints/S0035/progress.md`, `sprints/S0035/uat.json`, and
  `sprints/S0035/uat.md` updated with implementation evidence.
- `docs/engineering/state.md` traceability/checkpoints updated for `US-0056`.

## Execution guardrails

- Keep `/auto` orchestration-only semantics.
- Preserve existing mandatory release gate chain order.
- Maintain active/template parity for all strict-proof contracts.

## Next phase

Proceed to **`/execute`** for `S0035` (`US-0056`).

---

# TL -> Dev Handoff — Sprint S0034 (US-0055 Deterministic Status Reconciliation Command)

## Planning summary

- **Sprint**: S0034 (new)
- **Story**: US-0055 — Deterministic Status Reconciliation Command
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage**: AC-1..AC-10 verified PASS in `sprints/S0034/plan-verify.json`.

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0055 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0055 section)
- Decision: `decisions/DEC-0037.md`
- Research: `docs/engineering/research.md` (`R-0031`)
- PO -> TL handoff: `handoffs/po_to_tl.md` (US-0055 section)
- Sprint artifacts: `sprints/S0034/*`

## Focus

1. **Reconciliation command contract (T-001..T-003)**: define deterministic
   read/repair behavior with canonical precedence and conflict handling.
2. **Normalization behavior (T-004..T-007)**: reconcile DONE+unchecked and
   acceptance/resume drift with bounded target scope and auditable evidence.
3. **Deterministic diagnostics + parity (T-008..T-010)**: reason codes,
   regression coverage, and active/template alignment.

## Execution order

Run tasks `T-001`..`T-010` in sequence (see `sprints/S0034/tasks.md`).

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0034/tasks.md` marked done.
- `sprints/S0034/plan-verify.json` confirms AC-1..AC-10 coverage with no gaps.
- `sprints/S0034/progress.md`, `sprints/S0034/uat.json`, and
  `sprints/S0034/uat.md` updated with implementation evidence.
- `docs/engineering/state.md` traceability row for US-0055 advances from
  `PLANNED` with evidence references.

## Execution guardrails

- Preserve canonical status ownership (`docs/product/backlog.md`).
- Reconciliation writes must be target-scoped and non-destructive.
- Keep mandatory release gate chain behavior unchanged.

## Next phase

Proceed to **`/execute`** for `S0034` (`US-0055`).

---

# TL -> Dev Handoff — Sprint S0033 (US-0054 Configurable Multi-Target Release Publish with Confirmation Gate)

## Planning summary

- **Sprint**: S0033 (new)
- **Story**: US-0054 — Configurable Multi-Target Release Publish with Confirmation Gate
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage**: AC-1..AC-10 verified PASS in `sprints/S0033/plan-verify.json`.

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0054 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0054 section)
- Decision: `decisions/DEC-0036.md`
- Research: `docs/engineering/research.md` (`R-0029`, `R-0030`)
- PO -> TL handoff: `handoffs/po_to_tl.md` (US-0054 section)
- Sprint artifacts: `sprints/S0033/*`

## Focus

1. **Target schema + taxonomy (T-001..T-003)**: implement deterministic
   configurable target schema with built-in target classes and first-class
   `custom` + `ssh` support.
2. **Safety contract (T-004, T-006, T-007)**: enforce confirmation default,
   fail-fast validation, and env-reference-only secret handling.
3. **Run semantics (T-005)**: deterministic target ordering, selection, and
   skip behavior for disabled targets.
4. **Parity + guardrails (T-008..T-010)**: align active/template contract and
   preserve mandatory release gate invariants.

## Execution order

Run tasks `T-001`..`T-010` in sequence (see `sprints/S0033/tasks.md`).

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0033/tasks.md` marked done.
- `sprints/S0033/plan-verify.json` confirms AC-1..AC-10 coverage with no gaps.
- `sprints/S0033/progress.md`, `sprints/S0033/uat.json`, and
  `sprints/S0033/uat.md` updated with implementation evidence.
- `docs/engineering/state.md` traceability row for US-0054 advances from
  `PLANNED` with evidence references.

## Execution guardrails

- Mandatory release quality gates remain unchanged (`/qa`, `/verify-work`, `/release`).
- No inline credentials in committed target configuration.
- Keep active/template parity for all publish-target contracts.

## Next phase

Proceed to **`/execute`** for `S0033` (`US-0054`).

---

# TL -> Dev Handoff — Sprint S0032 (US-0053 Context Compaction and Tiered Token-Cost Optimization Mode)

## Planning summary

- **Sprint**: S0032 (new)
- **Story**: US-0053 — Context Compaction and Tiered Token-Cost Optimization Mode
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage**: AC-1..AC-10 verified PASS in `sprints/S0032/plan-verify.json`.

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0053 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0053 section)
- Decision: `decisions/DEC-0035.md`
- Research: `docs/engineering/research.md` (`R-0027`, `R-0028`)
- PO -> TL handoff: `handoffs/po_to_tl.md` (US-0053 section)
- Sprint artifacts: `sprints/S0032/*`

## Focus

1. **Profile policy (T-001..T-003)**: implement deterministic
   `TOKEN_PROFILE=lean|balanced|full` behavior, mapping table, and explicit
   override precedence.
2. **Context compaction (T-004, T-005)**: implement bounded active-context
   contracts for `state.md` and compact decisions index policy with archive/link
   safety.
3. **Retrieval strategy (T-006)**: enforce narrow-read `/ask` policy
   (targeted-first, bounded expansion, explicit not-found behavior).
4. **Parity and guardrails (T-007..T-009)**: keep active/template contracts
   aligned and lock mandatory QA/UAT/release invariants in regression checks.
5. **Operator guidance + integrity (T-010)**: document profile tradeoffs and
   verify no destructive impact to ID/release-history semantics.

## Execution order

Run tasks `T-001`..`T-010` in sequence (see `sprints/S0032/tasks.md`).

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0032/tasks.md` marked done.
- `sprints/S0032/plan-verify.json` confirms AC-1..AC-10 coverage with no gaps.
- `sprints/S0032/progress.md`, `sprints/S0032/uat.json`, and
  `sprints/S0032/uat.md` updated with implementation evidence.
- `docs/engineering/state.md` traceability row for US-0053 advances from
  `PLANNED` with evidence references.

## Execution guardrails

- Mandatory safety gates remain intact (`/qa`, `/verify-work`, `/release`).
- No destructive rewrite of historical release or ID artifacts.
- Keep active/template parity for all token-profile and compaction contracts.

## Next phase

Proceed to **`/execute`** for `S0032` (`US-0053`).

---

# TL -> Dev Handoff — Sprint S0031 (US-0052 Optional Fresh-Project ID Namespace Bootstrap)

## Planning summary

- **Sprint**: S0031 (new)
- **Story**: US-0052 — Optional Fresh-Project ID Namespace Bootstrap
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage**: AC-1..AC-8 verified PASS in `sprints/S0031/plan-verify.json`.

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0052 AC-1..AC-8)
- Architecture: `docs/engineering/architecture.md` (US-0052 section)
- Decisions: `decisions/DEC-0034.md`
- Research: `docs/engineering/research.md` (`R-0024`, `R-0025`)
- PO->TL handoff: `handoffs/po_to_tl.md` (Install Hygiene + Smart Intake + Bootstrap IDs section)
- Sprint artifacts: `sprints/S0031/*`

## Focus

1. **Bootstrap control contract (T-001)**: define explicit optional bootstrap control with default-off behavior and clear operator interface.
2. **Deterministic freshness eligibility (T-002, T-005)**: detect fresh vs non-fresh repo state using canonical ID surfaces and emit actionable diagnostics when bootstrap request is ineligible.
3. **ID generation behavior (T-003, T-004, T-006)**: start at `0001` only for eligible bootstrap; otherwise continue from highest existing IDs without rewriting historical artifacts and with collision safety.
4. **Operator guidance (T-007)**: document bootstrap constraints, compatibility behavior, and migration caveats in runbook/README/help paths.
5. **Regression and parity (T-008..T-010)**: cover fresh/non-fresh/mixed-edge cases and keep active/template contracts aligned.

## Execution order

Execute tasks `T-001`..`T-010` in sequence (see `sprints/S0031/tasks.md`).

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0031/tasks.md` are marked done.
- No uncovered US-0052 acceptance criteria after `sprints/S0031/plan-verify.json` is PASS.
- `sprints/S0031/progress.md`, `uat.json`, and `uat.md` updated with execution evidence.
- `docs/engineering/state.md` traceability row for US-0052 advanced from `PLANNED` with evidence references.

## Execution guardrails

- Preserve backward compatibility for non-fresh repositories (highest-ID continuation).
- Never renumber or rewrite historical IDs.
- Keep optional behavior explicit and default-off; no hidden bootstrap side effects.
- Maintain active/template parity for command, docs, and test contracts.

## Next phase

Proceed to **`/execute`** for `S0031` (`US-0052`).

---

# TL -> Dev Handoff — Sprint S0030 (US-0051 Intelligent Intake Decomposition and Risk-Aware PO Questioning)

## Planning summary

- **Sprint**: S0030 (new)
- **Story**: US-0051 — Intelligent Intake Decomposition and Risk-Aware PO Questioning
- **Task count**: 11 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage**: AC-1..AC-10 verified PASS in `sprints/S0030/plan-verify.json`.

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0051 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0051 section)
- Decisions: `decisions/DEC-0033.md`
- Research: `docs/engineering/research.md` (`R-0024`, `R-0025`)
- PO->TL handoff: `handoffs/po_to_tl.md` (Install Hygiene + Smart Intake + Bootstrap IDs section)
- Sprint artifacts: `sprints/S0030/*`

## Focus

1. **Decomposition trigger model (T-001, T-005)**: add deterministic breadth/risk heuristics with safe single-story default for narrow intake.
2. **Split quality and persistence (T-002, T-003)**: generate vertical-slice/workflow-step split proposals and persist explicit split rationale/boundaries.
3. **User authority controls (T-004)**: require accept/merge/adjust confirmation before decomposed persistence.
4. **Risk-aware questioning (T-006, T-007)**: escalate follow-ups for broad/high-risk intake while keeping bounded rounds.
5. **Low-touch compatibility (T-008)**: preserve `INTAKE_GUIDED_MODE=0` minimal-overhead behavior with duplicate safety intact.
6. **Traceability + parity + regression (T-009..T-011)**: ensure artifact evidence, active/template alignment, and tests for split/no-split/questioning paths.

## Execution order

Execute tasks `T-001`..`T-011` in sequence (see `sprints/S0030/tasks.md`).

## Done criteria for Dev completion

- All 11 tasks in `sprints/S0030/tasks.md` are marked done.
- No uncovered US-0051 acceptance criteria after `sprints/S0030/plan-verify.json` is PASS.
- `sprints/S0030/progress.md`, `uat.json`, and `uat.md` updated with execution evidence.
- `docs/engineering/state.md` traceability row for US-0051 advanced from `PLANNED` with evidence references.

## Execution guardrails

- Process/workflow/docs/tests only; no runtime product feature behavior changes.
- Decomposition must remain bounded and user-controlled (no forced uncontrolled splitting).
- Preserve low-touch compatibility and active/template parity for intake semantics.

## Next phase

Proceed to **`/execute`** for `S0030` (`US-0051`).

---

# TL -> Dev Handoff — Sprint S0029 (US-0050 Clean Install Hygiene and Complete Clean-Repo Coverage)

## Planning summary

- **Sprint**: S0029 (new)
- **Story**: US-0050 — Clean Install Hygiene and Complete Clean-Repo Coverage
- **Task count**: 10 (within `SPRINT_MAX_TASKS=12`)
- **AC coverage**: AC-1..AC-9 verified PASS in `sprints/S0029/plan-verify.json`.

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0050 AC-1..AC-9)
- Architecture: `docs/engineering/architecture.md` (US-0050 section)
- Decisions: `decisions/DEC-0032.md`
- Research: `docs/engineering/research.md` (`R-0024`, `R-0025`)
- PO->TL handoff: `handoffs/po_to_tl.md` (Install Hygiene + Smart Intake + Bootstrap IDs section)
- Sprint artifacts: `sprints/S0029/*`

## Focus

1. **Ownership source of truth (T-001)**: define canonical installer-owned path contract used by all installers.
2. **Cross-installer parity (T-002..T-004)**: ensure `installer.ps1`, `installer.sh`, `installer.py` consume same ownership rules for install/clean.
3. **Cleanup safety (T-005)**: enforce explicit non-destructive boundaries for non-framework files.
4. **Template neutrality (T-006, T-007)**: remove seeded operational history and neutralize hardcoded runtime ID refs unless intentionally baseline-backed.
5. **Lifecycle regression (T-008, T-009)**: prove fresh install -> clean-repo -> reinstall behavior and full cleanup coverage.
6. **Compatibility/parity hardening (T-010)**: preserve US-0018 upgrade behavior and active/template alignment.

## Execution order

Execute tasks `T-001`..`T-010` in sequence (see `sprints/S0029/tasks.md`).

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0029/tasks.md` are marked done.
- No uncovered US-0050 acceptance criteria; `sprints/S0029/plan-verify.json` PASS after `/plan-verify`.
- `sprints/S0029/progress.md`, `uat.json`, and `uat.md` updated with execution evidence.
- `docs/engineering/state.md` traceability row for US-0050 advanced from `PLANNED` with evidence references.

## Execution guardrails

- Process/workflow/docs/tests only; no runtime product feature behavior changes.
- Keep cleanup operations ownership-scoped and non-destructive.
- Maintain active/template parity for installer and starter-artifact contract behavior.

## Next phase

Proceed to **`/execute`** for `S0029` (`US-0050`).

---

# TL -> Dev Handoff — Sprint S0028 (US-0049 Legacy DONE-Story Acceptance/Traceability Backfill Guard)

## Planning summary

- **Sprint**: S0028 (new)
- **Story**: US-0049 — Legacy DONE-Story Acceptance/Traceability Backfill Guard
- **Task count**: 8 (within SPRINT_MAX_TASKS=12)
- **AC coverage**: AC-1..AC-8 explicit in `sprints/S0028/plan-verify.json`; run `/plan-verify` to confirm.

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0049 AC-1..AC-8)
- Architecture: `docs/engineering/architecture.md` (US-0049 section)
- Decision: `decisions/DEC-0031.md`
- Research: `docs/engineering/research.md` (R-0023)
- PO→TL handoff: `handoffs/po_to_tl.md` (US-0049 discovery addendum)
- Sprint artifacts: `sprints/S0028/*`

## Focus

1. **Detection rule (T-001)**: Legacy drift = backlog DONE and (acceptance unchecked OR traceability/state lacks entry OR release artifacts lack representation).
2. **Target-scoped repair (T-002)**: Mutate only stories matching the rule; no broad rewrite.
3. **Audit report (T-003)**: Canonical path `docs/engineering/legacy-drift-audit.md`; required fields: story ID, prior acceptance/traceability state, resolved state, reason code, evidence ref.
4. **Reason codes (T-004)**: `BACKLOG_DONE_ACCEPTANCE_UNCHECKED`, `BACKLOG_DONE_TRACEABILITY_MISSING`, `BACKLOG_DONE_RELEASE_ARTIFACT_MISSING` with remediation.
5. **One-time backfill (T-005)**: Explicit trigger; idempotent when no drift; emit audit report.
6. **Ongoing guard (T-006)**: At release/reconciliation or dedicated check; block or repair with audit append; documented, deterministic.
7. **Template parity (T-007)**: Active and `template/` command/rule/docs for backfill and guard aligned.
8. **Regression (T-008)**: No-drift run, single-drift repair, guard block/repair with reason code.

## Execution order

Execute tasks `T-001`..`T-008` in sequence (see `sprints/S0028/tasks.md`).

## Done criteria for Dev completion

- All 8 tasks in `sprints/S0028/tasks.md` are marked done.
- No uncovered US-0049 acceptance criteria; `sprints/S0028/plan-verify.json` satisfied (run `/plan-verify` to confirm).
- `sprints/S0028/progress.md`, `uat.json`, and `uat.md` updated with execution evidence.
- `docs/engineering/state.md` traceability row for US-0049 advanced from PLANNED with evidence references.

## Execution guardrails

- Process/workflow/docs only; no runtime product feature changes.
- Maintain active/template parity for backfill guard, audit report location, reason codes.
- Regression: no-drift, single-drift repair, guard block/repair with reason code.

## Next phase

Run **`/plan-verify`** for S0028; then proceed to execute and `/qa` when ready.

---

# TL -> Sprint-Plan Handoff — US-0049 (Legacy DONE-Story Acceptance/Traceability Backfill Guard) [COMPLETED]

## Architecture summary

- **Story**: US-0049 — Legacy DONE-Story Acceptance/Traceability Backfill Guard (OPEN)
- **Scope**: Detection rule (backlog DONE and acceptance unchecked or traceability/release missing), target-scoped repair only, canonical audit report, reason-code vocabulary, one-time backfill mode, ongoing guard at release/reconciliation.
- **Out of scope**: Changing US-0045 canonical status ownership or US-0043 broad reconciliation semantics.

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0049 AC-1..AC-8)
- Architecture: `docs/engineering/architecture.md` (US-0049 section)
- Decision: `decisions/DEC-0031.md`
- Research: `docs/engineering/research.md` (R-0023)
- PO→TL handoff: `handoffs/po_to_tl.md` (US-0049 discovery addendum)

## Focus for `/sprint-plan`

1. **Detection rule**: Document and implement detection for legacy drift (backlog DONE and acceptance unchecked or traceability missing or release artifact missing).
2. **Audit report**: Canonical path `docs/engineering/legacy-drift-audit.md`; required fields per entry (story ID, prior acceptance/traceability state, resolved state, reason code, evidence ref).
3. **Reason codes**: `BACKLOG_DONE_ACCEPTANCE_UNCHECKED`, `BACKLOG_DONE_TRACEABILITY_MISSING`, `BACKLOG_DONE_RELEASE_ARTIFACT_MISSING` with remediation guidance.
4. **One-time backfill**: Explicit trigger; target-scoped repair; idempotent when no drift; append audit report.
5. **Ongoing guard**: At release or reconciliation (or dedicated check); block with reason code or repair with audit append; deterministic, documented.
6. **Template parity**: Active and `template/` command/rule/docs for backfill and guard aligned.
7. **Regression**: No-drift run (no changes), single-drift repair (audit entry), guard block/repair with reason code.

## Next phase

Sprint **S0028** created. Run **`/plan-verify`** for S0028; then `/execute` handoff.

---

# TL -> Dev Handoff — Sprint S0027 (US-0032 Optional Feature User Guide Generation)

## Planning summary

- **Sprint**: S0027 (new)
- **Story**: US-0032 — Optional Feature User Guide Generation
- **Task count**: 8 (within SPRINT_MAX_TASKS=12)
- **AC coverage**: AC-1..AC-8 explicit in `sprints/S0027/plan-verify.json`; no gaps

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0032 AC-1..AC-8)
- Architecture: `docs/engineering/architecture.md` (US-0032 section)
- Decision: `decisions/DEC-0030.md`
- Sprint artifacts: `sprints/S0027/*`

## Focus

1. **USER_GUIDE_MODE** flag (default 0); when disabled, zero required steps or blocking checks in any phase.
2. Canonical location: `docs/user-guides/US-xxxx.md` per feature story when enabled.
3. Minimum guide schema: Purpose, Prerequisites, Usage steps, Example, Limitations, Troubleshooting (structural validation only).
4. Validation reports completeness; release blocks with `USER_GUIDE_INCOMPLETE` only when enabled and required sections missing.
5. Traceability: story ID → user guide artifact; referenced in handoff/release context.
6. Boundaries with US-0031: user guides end-user only; no duplicate spec-pack content; document separation.
7. Template parity: active and `template/` docs/commands/rules aligned for user-guide mode.

## Execution order

Execute tasks `T-001`..`T-008` in sequence (see `sprints/S0027/tasks.md`).

## Done criteria for Dev completion

- All 8 tasks in `sprints/S0027/tasks.md` are marked done.
- No uncovered US-0032 acceptance criteria; `sprints/S0027/plan-verify.json` remains satisfied.
- `sprints/S0027/progress.md`, `uat.json`, and `uat.md` updated with execution evidence.
- `docs/engineering/state.md` traceability row for US-0032 advanced from PLANNED with evidence references.

## Execution guardrails

- Process/workflow/docs only; no runtime product feature changes.
- Maintain active/template parity for intake, architecture, sprint-plan, execute, qa, release, runbook, README.
- Regression: positive/negative and USER_GUIDE_MODE=0 zero-overhead coverage in test runners.

## Next phase

After execute: run `/plan-verify` for S0027 if not already run; then `/qa` and `/verify-work` when ready.

---

# TL -> Dev Handoff — Sprint S0011 (US-0039 Release Gate Tightening)

## Planning summary

- **Sprint**: S0011 (reused; plan valid per 2026-03-02 refresh)
- **Story**: US-0039 — Release Gate Tightening for Check-In Tests and QA/UAT Completion
- **Task count**: 11 (within SPRINT_MAX_TASKS=12)
- **AC coverage**: AC-1..AC-10 explicit in `sprints/S0011/plan-verify.json`; no gaps

## Rationale for reusing S0011

- Existing S0011 plan already covers US-0039 AC-1..AC-10 with 11 atomic tasks.
- Scope and architecture unchanged; backlog/acceptance criteria match.
- Sizing and gate-order semantics remain correct; no stale/incompatible content.

## Architecture and decision references

- Story acceptance: `docs/product/backlog.md` (US-0039 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0039 section)
- Decision: `decisions/DEC-0019.md` (gate order, no-bypass, override evidence)
- Sprint artifacts: `sprints/S0011/*`

## Focus

1. **Gate order**: check-in test → QA → UAT → release finalization (mandatory, deterministic).
2. **Check-in test gate**: verify latest test result passing; block on missing/stale/failing with reason codes.
3. **QA gate**: require no unresolved blocking findings before release.
4. **UAT gate**: block on placeholder, incomplete, or unresolved-fail UAT state.
5. **Evidence**: per-gate pass/fail and evidence pointers in handoff/state for audit.
6. **No bypass**: default path has no bypass; override only via decision gate + rationale.
7. **Template parity**: align `template/` release, qa, execute, runbook for gate semantics.
8. **Regression**: positive/negative/stale-evidence cases per gate; optional lint/typecheck keys do not false-fail.

## Execution order

Execute tasks `T-001`..`T-011` in sequence (see `sprints/S0011/tasks.md`).

## Done criteria for Dev completion

- All 11 tasks in `sprints/S0011/tasks.md` are marked done.
- No uncovered US-0039 acceptance criteria; `sprints/S0011/plan-verify.json` remains satisfied.
- `sprints/S0011/progress.md`, `uat.json`, and `uat.md` updated with execution evidence.
- `docs/engineering/state.md` traceability row for US-0039 advanced from PLANNED with evidence references.

## Execution guardrails (release gate tightening)

- Process/workflow/docs/tests only; no runtime product feature changes.
- Maintain active/template parity for release, qa, execute, runbook, README.
- Regression: positive/negative/stale-evidence and no-bypass coverage in test runners.

## Next phase

After execute/QA/verify-work: run `/plan-verify` for S0011 if not already run; then `/release` when gates pass.

---

# TL -> Dev Handoff — Sprint S0026 (US-0031 Optional Documentation Pack)

## Sprint Overview

Sprint `S0026` is planned for `US-0031`.

- Story count: 1 (`US-0031`)
- Planned tasks: 8
- Sizing: within limit (`SPRINT_MAX_TASKS=12`)

## Architecture and Decision References

- Story acceptance: `docs/product/backlog.md` (US-0031 AC-1..AC-8)
- Sprint artifacts: `sprints/S0026/*`

## Focus

1. Add single enable flag/config for spec-pack mode; default disabled.
2. When disabled: no extra required steps in intake/architecture/release.
3. When enabled: create/update Design Concept, CRS, Technical Specification at canonical locations.
4. Define minimum required sections/fields per artifact; validation blocks only when enabled and incomplete.
5. Define traceability from backlog story IDs to spec-pack artifacts; document ownership (role/phase per document).
6. Maintain active/template parity for spec-pack mode references.

## Execution order

Execute tasks `T-001`..`T-008` in sequence.

## Done criteria for Dev completion

- All 8 tasks in `sprints/S0026/tasks.md` are marked done.
- No uncovered US-0031 acceptance criteria in `sprints/S0026/plan-verify.json`.
- `sprints/S0026/progress.md`, `uat.json`, and `uat.md` updated with execution evidence.
- `docs/engineering/state.md` traceability row advanced from `PLANNED` with evidence references.

---

# TL -> Dev Handoff — Sprint S0025 (US-0048 Per-Phase Subagent Isolation)

## Sprint Overview

Sprint `S0025` is planned for `US-0048`.

- Story count: 1 (`US-0048`)
- Planned tasks: 10
- Sizing: within limit (`SPRINT_MAX_TASKS=12`)
- Next phase: **`/plan-verify`** for `S0025`

## Architecture and Decision References

- Story acceptance: `docs/product/backlog.md` (US-0048 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0048 section)
- Research: `docs/engineering/research.md` (`R-0018`, `R-0019`)
- Decision: `decisions/DEC-0029.md`
- Sprint artifacts: `sprints/S0025/*`

## Focus

1. Enforce `/auto` orchestrator-only behavior; fail when phase work runs without fresh subagent.
2. Define and write isolation evidence schema and canonical locations; document in runbook/commands.
3. Add isolation-compliance gates to `/verify-work` and `/release`; enforce gate order.
4. Implement reason-code taxonomy and remediation; ensure pause/resume provenance.
5. Add regression coverage and active/template parity for isolation enforcement.

## Execution order

Execute tasks `T-001`..`T-010` in sequence.

## Critical constraints

- Isolation evidence schema: phase_id, role, fresh_context_marker, timestamp, evidence_ref.
- Fail-closed on missing/invalid evidence; no silent continuation.
- Gate order at release: check-in test → QA → UAT → isolation compliance → release finalization.
- Evidence must survive pause/resume; resume requires fresh context and new evidence.

## Done criteria for Dev completion

- All 10 tasks in `sprints/S0025/tasks.md` are marked done.
- No uncovered US-0048 acceptance criteria in `sprints/S0025/plan-verify.json`.
- `sprints/S0025/progress.md`, `uat.json`, and `uat.md` updated with execution evidence.
- `docs/engineering/state.md` traceability row advanced from `PLANNED` with evidence references.

---

# TL -> Dev Handoff — Sprint S0024 (US-0035 Component-Scoped Mode)

## Sprint Overview

Sprint `S0024` is planned for `US-0035`.

- Story count: 1 (`US-0035`)
- Planned tasks: 8
- Sizing: within limit (`SPRINT_MAX_TASKS=12`)

## Focus

1. Add component scope controls with default-off behavior.
2. Add explicit scope declaration and scoped task metadata contracts.
3. Add execute/qa/release guardrails for unapproved out-of-scope impact.
4. Maintain active/template parity and regression coverage.

## Dev completion note

- Sprint `S0024` implementation is complete.
- All tasks `T-001..T-008` are done with regression evidence in `tests/report.md`.
- Sprint is ready for QA/verify/release gates with complete artifacts.

---

# TL -> Dev Handoff — Sprint S0023 (US-0034 Cross-Repo Observability)

## Sprint Overview

Sprint `S0023` is planned for `US-0034`.

- Story count: 1 (`US-0034`)
- Planned tasks: 8
- Sizing: within limit (`SPRINT_MAX_TASKS=12`)

## Focus

1. Add optional compatibility observability mode controls (default off).
2. Add source declaration contract and canonical compatibility artifacts.
3. Add critical compatibility gate behavior for release.
4. Preserve active/template parity and regression coverage.

## Dev completion note

- Sprint `S0023` implementation is complete.
- All tasks `T-001..T-008` are done with regression evidence in `tests/report.md`.
- Sprint is ready for QA/verify/release gates with complete artifacts.

---

# TL -> Dev Handoff — Sprint S0022 (US-0033 Guided Intake Mode)

## Sprint Overview

Sprint `S0022` is planned for `US-0033`.

- Story count: 1 (`US-0033`)
- Planned tasks: 9
- Sizing: within limit (`SPRINT_MAX_TASKS=12`)

## Focus

1. Add one explicit intake behavior switch (`INTAKE_GUIDED_MODE`).
2. Define guided mode and low-touch mode behavior contracts.
3. Keep duplicate-check baseline safety in both modes.
4. Preserve active/template parity and regression coverage.

## Dev completion note

- Sprint `S0022` implementation is complete.
- All tasks `T-001..T-009` are done with regression evidence in `tests/report.md`.
- Sprint is ready for QA/verify/release gates with complete artifacts.

---

# TL -> Dev Handoff — Sprint S0021 (US-0045 Canonical Status Guard)

## Sprint Overview

Sprint `S0021` is planned for `US-0045`.

- Story count: 1 (`US-0045`)
- Planned tasks: 10
- Sizing: within limit (`SPRINT_MAX_TASKS=12`)

## Focus

1. Make `docs/product/backlog.md` the canonical story-status source.
2. Define deterministic reconciliation precedence and target-scoped mutation.
3. Add one-time normalization baseline report with auditable row details.
4. Add fail-safe contradiction reason code and active/template parity checks.

## Dev completion note

- Sprint `S0021` implementation is complete.
- All tasks `T-001..T-010` are done with regression evidence in `tests/report.md`.
- Sprint is ready for QA/verify/release gates with complete artifacts.

---

# TL -> Dev Handoff — Sprint S0020 (US-0047 Explicit Bulk Execute Orchestration)

## Sprint Overview

Sprint `S0020` is planned for `US-0047`.

- Story count: 1 (`US-0047`)
- Planned tasks: 10
- Sizing: within limit (`SPRINT_MAX_TASKS=12`)

## Focus

1. Define explicit bulk execute activation semantics for `/auto`.
2. Define deterministic selection, bounded controls, and reason-code outcomes.
3. Enforce team-scoped no-write guardrails (`TEAM_MEMBER` + `ACTIVE_TASK_IDS`).
4. Maintain strict fresh-context isolation and active/template parity.

## Dev completion note

- Sprint `S0020` implementation is complete.
- All tasks `T-001..T-010` are done with regression evidence in `tests/report.md`.
- Sprint is ready for QA/verify/release gates with complete artifacts.

---

# TL -> Dev Handoff — Sprint S0019 (US-0046 Explicit Bulk Sprint Planning)

## Sprint Overview

Sprint `S0019` is planned for `US-0046`.

- Story count: 1 (`US-0046`)
- Planned tasks: 10
- Sizing: within limit (`SPRINT_MAX_TASKS=12`)

## Focus

1. Define explicit `/sprint-plan --bulk` trigger semantics with default-safe fallback.
2. Define deterministic selection/grouping and bounded stop behavior.
3. Preserve sizing safety and planning artifact completeness for each generated sprint.
4. Maintain traceability consistency and active/template parity.

## Dev completion note

- Sprint `S0019` implementation is complete.
- All tasks `T-001..T-010` are done with regression evidence in `tests/report.md`.
- Sprint is ready for QA/verify/release gates with complete artifacts.

---

# TL -> Dev Handoff — Sprint S0018 (US-0016 Homebrew Sync)

## Sprint Overview

Sprint `S0018` is planned for `US-0016`.

- Story count: 1 (`US-0016`)
- Planned tasks: 3
- Sizing: within limit (`SPRINT_MAX_TASKS=12`)

## Focus

1. Align stable Homebrew formula tag/version with npm package version.
2. Add regression checks in both test runners for alignment.
3. Reconcile product acceptance state and release artifacts.

---

# TL -> Dev Handoff — Sprint S0017 (US-0044 Backlog-Drain Auto Mode)

## Sprint Overview

Sprint `S0017` is planned for `US-0044`.

- Story count: 1 (`US-0044`)
- Planned tasks: 10
- Sizing: within limit (`SPRINT_MAX_TASKS=12`)

## Focus

1. Add optional multi-story backlog-drain behavior contract for `/auto`.
2. Add fine-tune scratchpad switches with default-safe off behavior.
3. Add deterministic reason codes and per-story breadcrumb contract.
4. Maintain active/template parity and regression coverage.

---

# TL -> Dev Handoff — Sprint S0016 (US-0015 Runbook Completion)

## Sprint Overview

Sprint `S0016` is planned for `US-0015`.

- Story count: 1 (`US-0015`)
- Planned tasks: 4
- Sizing: within limit (`SPRINT_MAX_TASKS=12`)

## Execution order

Execute tasks `T-001..T-004`.

## Focus

1. Document intentional empty optional runbook commands.
2. Keep active/template parity for runbook + README.
3. Add regression tests to protect the documentation contract.

---

# TL -> Dev Handoff — Sprint S0015 (US-0043 Backlog Reconciliation Gate)

## Sprint Overview

Sprint `S0015` is planned for `US-0043`: Backlog Reconciliation Gate for
Released Sprints.

- Story count: 1 (`US-0043`)
- Planned tasks: 10
- Sizing: within limit (`SPRINT_MAX_TASKS=12`)
- Split decision: not required
- Milestone activation: not applicable

## Architecture and Decision References

- Story acceptance: `docs/product/backlog.md` (US-0043 AC-1..AC-10)
- Architecture: `docs/engineering/architecture.md` (US-0043 section)
- Research: `docs/engineering/research.md` (`R-0007`)
- Decision: `decisions/DEC-0021.md`
- Sprint artifacts: `sprints/S0015/*`

## Execution order

Execute tasks `T-001..T-010` in sequence.

## Priority focus

1. Implement deterministic release-boundary backlog reconciliation for the
   target sprint story only.
2. Add fail-safe contradiction handling with `BACKLOG_STATUS_DRIFT`.
3. Add regression coverage for stale mismatch and positive auto-reconcile.
4. Maintain active/template parity for command/rule/doc behavior.

## Critical constraints

- No mutation of unrelated backlog stories.
- No pre-release `DONE` transitions.
- Keep behavior deterministic and evidence-driven from canonical artifacts.
- Preserve manual-mode safe defaults and existing decision-gate boundaries.

---

# TL -> Dev Handoff — Sprint S0014 (US-0042 Release Findings Workflow)

## Sprint Overview

Sprint `S0014` is planned for `US-0042` and is implementation-complete.

## Scope delivered

1. Added canonical post-QA release findings artifact contract:
   `sprints/Sxxxx/release-findings.md`.
2. Added canonical blocked-release handoff:
   `handoffs/release_to_dev.md`.
3. Updated release command and release reason-code contract for blocked post-QA
   scenarios.
4. Updated runbook/README boundary guidance for QA findings vs release findings.
5. Added active/template parity updates and regression checks in both test
   runners.
6. Captured real blocked-release evidence for `S0013`.

---

# TL -> Dev Handoff — Sprint S0013 (US-0041 Lifecycle QA Expansion)

## Sprint Overview

Sprint S0013 is planned for US-0041: End-to-End Lifecycle QA for `its-magic`
Install/Upgrade/Clean.

- Story count: 1 (`US-0041`)
- Planned tasks: 11
- Sizing: within limit (`SPRINT_MAX_TASKS=12`)
- Split decision: not required (single-story sprint)
- Milestone activation: not applicable

## Execution Order

Execute tasks `T-001` through `T-011` in sequence.

## Priority focus for this sprint

1. Add clean-repo safety lifecycle checks in PowerShell + shell tests.
2. Add CLI lifecycle tests (`its-magic` path) for `missing`, `overwrite --backup`,
   `upgrade`, and `--clean-repo`.
3. Add invalid-mode negative-path checks with deterministic non-zero behavior.
4. Extend npm local package tests and CI lifecycle subset checks.
5. Update README/runbook lifecycle QA matrix and maintain template parity.

## Critical constraints

- Use temp directories only for lifecycle tests.
- Ensure cleanup runs even after failed assertions.
- Verify non-framework markers survive clean-repo checks.
- Keep active/template docs aligned for new lifecycle QA references.

---

# TL -> Dev Handoff — Sprint S0012 (US-0040 Release Notes Queue)

## Sprint Overview

Sprint S0012 is planned for US-0040: Per-Sprint Release Notes and Release Queue
Tracker.

- Story count: 1 (`US-0040`)
- Planned tasks: 11
- Sizing: within limit (`SPRINT_MAX_TASKS=12`)
- Split decision: not required (single-story sprint remains atomic)
- Milestone activation: not applicable

## Architecture and Decision References

- Story acceptance: `docs/product/backlog.md` (US-0040 AC-1..AC-9)
- Architecture: `docs/engineering/architecture.md` (US-0040 section)
- Decision: `decisions/DEC-0020.md`
- Sprint artifacts: `sprints/S0012/*`

## Execution Order

Execute tasks T-001 through T-011 sequentially.

| Task | Description | Files | AC |
|------|-------------|-------|----|
| T-001 | Define canonical per-sprint immutable release notes path and target-sprint-only write semantics | `.cursor/commands/release.md`, `handoffs/releases/Sxxxx-release-notes.md` | AC-1 |
| T-002 | Define canonical release queue tracker schema and required fields | `.cursor/commands/release.md`, `handoffs/release_queue.md`, `docs/engineering/runbook.md` | AC-2 |
| T-003 | Define deterministic queue transitions (`ready -> unreleased -> released`) for target sprint only | `.cursor/commands/release.md`, `docs/engineering/state.md` | AC-3 |
| T-004 | Define unresolved sprint fail-safe behavior and deterministic reason codes | `.cursor/commands/release.md`, `handoffs/release_queue.md`, `docs/engineering/state.md` | AC-4 |
| T-005 | Define non-destructive legacy migration/backfill for `handoffs/release_notes.md` | `.cursor/commands/release.md`, `handoffs/release_notes.md`, `handoffs/releases/Sxxxx-release-notes.md` | AC-5 |
| T-006 | Define backward-compatible legacy latest-pointer/summary behavior | `handoffs/release_notes.md`, `.cursor/commands/release.md` | AC-6 |
| T-007 | Define queue/notes mismatch fail-safe handling and remediation contract | `.cursor/commands/release.md`, `handoffs/release_queue.md`, `docs/engineering/state.md` | AC-4, AC-7 |
| T-008 | Define unreleased queue visibility in readiness and release reporting | `.cursor/commands/release.md`, `docs/engineering/state.md`, `handoffs/release_notes.md` | AC-7 |
| T-009 | Align ownership/touchpoints across verify-work, release, refresh-context guidance | `.cursor/commands/release.md`, `.cursor/rules/core.mdc`, `.cursor/rules/handoffs.mdc`, `docs/engineering/runbook.md` | AC-8 |
| T-010 | Enforce active/template parity for release queue and per-sprint note semantics | `template/.cursor/commands/release.md`, `template/.cursor/rules/core.mdc`, `template/.cursor/rules/handoffs.mdc`, `template/docs/engineering/runbook.md` | AC-9 |
| T-011 | Plan positive/negative/migration/parity regression matrix in sprint UAT artifacts | `sprints/S0012/uat.md`, `sprints/S0012/uat.json`, `sprints/S0012/plan-verify.json` | AC-1, AC-3, AC-4, AC-5, AC-6, AC-7, AC-9 |

## Critical Requirements to Preserve

1. Release notes must be sprint-scoped and never overwrite another sprint's
   note artifact.
2. Queue transitions must only mutate the target sprint row during one release
   run.
3. Unresolved sprint identity and queue/notes mismatch must fail closed with
   deterministic reason codes and remediation guidance.
4. Legacy `handoffs/release_notes.md` must remain backward-compatible while
   canonical history moves to sprint-scoped files.
5. Migration/backfill must be non-destructive and idempotent.
6. Unreleased queue entries must be visible before release finalization.
7. Active/template guidance must remain behaviorally aligned.

## QA and Validation Focus

Required verification scenarios:
- target-sprint write-only behavior for per-sprint notes
- cross-sprint overwrite prevention
- queue required-field and transition correctness
- unresolved sprint fail-safe behavior with reason codes
- queue/notes mismatch fail-safe behavior
- legacy migration success and unresolved-manual path
- migration idempotency
- backward-compatible legacy pointer behavior
- unreleased queue visibility before finalization
- active/template parity checks

## Constraints

- Keep scope strictly to US-0040 process/artifact behavior.
- Do not introduce deployment runtime changes.
- Keep migration/backfill and mismatch handling non-destructive by default.
- Maintain explicit AC traceability with no plan-verify coverage gaps.

## Done Criteria for Dev Completion

- All 11 tasks in `sprints/S0012/tasks.md` are marked done.
- No uncovered US-0040 acceptance criteria in `sprints/S0012/plan-verify.json`.
- `sprints/S0012/progress.md`, `uat.json`, and `uat.md` are updated with
  execution evidence.
- `docs/engineering/state.md` traceability row advances from `PLANNED` to the
  next lifecycle state with evidence references.

# TL -> Dev Handoff — S0010 + S0011 (US-0038 + US-0039)

## Planning summary

- Sprint split executed per sizing policy (`SPRINT_MAX_TASKS=12`,
  `SPRINT_AUTO_SPLIT=1`):
  - `S0010` for `US-0038` with 11 tasks
  - `S0011` for `US-0039` with 11 tasks
- Split rationale: the combined two-story plan would exceed atomic task design
  once required negative-path testing and template parity work is included.
- Milestone activation check: not applicable for both sprints (no active
  milestone context declared).

## S0010 — US-0038 execution focus

- Goal: deliver policy-driven sync cadence and guarded auto-push semantics.
- Required negative paths:
  - disallowed auto-push on protected/default branch without allowlist
  - disallowed auto-push on failed/missing/timed-out `TEST_COMMAND`
  - disallowed auto-push pre-QA and with unresolved QA blockers
- Mandatory outputs: deterministic sync reason codes and evidence fields in
  state/handoff artifacts.
- Script parity: keep `scripts/validate-and-push.ps1` and
  `scripts/validate-and-push.sh` behaviorally aligned with mandatory
  test-before-push gating.

## S0011 — US-0039 execution focus

- Goal: enforce strict release gate chain:
  `check-in test -> QA -> UAT -> release finalization`.
- Required negative paths:
  - block release on missing/stale/failing test evidence
  - block release on unresolved QA blockers
  - block release on incomplete/placeholder UAT
  - verify no-bypass default behavior
- Override path constraint:
  - only via explicit decision gate with rationale and approver evidence
  - release artifacts must include override evidence pointers when used

## AC traceability readiness

- `S0010`: `sprints/S0010/plan-verify.json` covers `US-0038` AC-1..AC-10 with
  no gaps.
- `S0011`: `sprints/S0011/plan-verify.json` covers `US-0039` AC-1..AC-10 with
  no gaps.
- `docs/engineering/state.md` traceability index includes PLANNED rows for
  `US-0038` and `US-0039`.

## Next execution order

1. Execute `S0010` tasks `T-001..T-011`.
2. Run `/qa` and `/verify-work` for `S0010`.
3. Execute `S0011` tasks `T-001..T-011`.
4. Run `/qa` and `/verify-work` for `S0011`.

## Dev completion note (S0010)

- Dev executed `S0010` task sequence `T-001..T-011` and marked all tasks done.
- US-0038 contract updates are completed across command guidance, runbook/README,
  validate-and-push scripts, regression planning artifacts, and template parity.
- Sprint status is now ready for `/qa` with updated `handoffs/dev_to_qa.md`
  checklist and deterministic sync evidence/reason-code expectations.

# TL -> Dev Handoff — Sprint S0009 (US-0037 Auto Continuation)

## Sprint Overview

Sprint S0009 is planned for US-0037: Mid-Process `/auto` Continuation with
Deterministic Resume Point.

- Story count: 1 (`US-0037`)
- Planned tasks: 9
- Sizing: within limit (`SPRINT_MAX_TASKS=12`)
- Split decision: not required (single sprint)
- Milestone activation: not applicable

## Architecture and Decision References

- Story acceptance: `docs/product/backlog.md` (US-0037 AC-1..AC-9)
- Architecture: `docs/engineering/architecture.md` (US-0037 section)
- Decision: `decisions/DEC-0017.md`
- Sprint artifacts: `sprints/S0009/*`

## Execution Order

Execute tasks T-001 through T-009 sequentially.

| Task | Description | Files | AC |
|------|-------------|-------|----|
| T-001 | Define explicit `/auto start-from=<phase>` contract and canonical phase IDs | `.cursor/commands/auto.md` | AC-1 |
| T-002 | Define deterministic resolver precedence and precedence test coverage | `.cursor/commands/auto.md`, `sprints/S0009/uat.md` | AC-2 |
| T-003 | Define conflict/staleness/unparseable fail-fast behavior and `[AUTO_RESUME_ERROR]` codes | `.cursor/commands/auto.md`, `.cursor/rules/core.mdc`, `sprints/S0009/uat.md` | AC-3 |
| T-004 | Define one-command continuation through remaining phases | `.cursor/commands/auto.md` | AC-4 |
| T-005 | Preserve decision gates and stop-condition behavior | `.cursor/commands/auto.md`, `.cursor/rules/core.mdc` | AC-5 |
| T-006 | Define breadcrumb logging contract for `state.md` and `resume_brief.md` | `.cursor/commands/auto.md`, `.cursor/commands/pause.md`, `.cursor/commands/resume.md`, `docs/engineering/state.md`, `handoffs/resume_brief.md` | AC-6 |
| T-007 | Preserve backward compatibility and safe defaults | `.cursor/commands/auto.md`, `.cursor/commands/resume.md` | AC-7 |
| T-008 | Align `/pause`, `/resume`, `/auto` guidance and update README/runbook | `.cursor/commands/auto.md`, `.cursor/commands/resume.md`, `.cursor/commands/pause.md`, `README.md`, `docs/engineering/runbook.md` | AC-8 |
| T-009 | Verify and enforce active/template continuation parity | `template/.cursor/commands/auto.md`, `template/.cursor/commands/resume.md`, `template/.cursor/commands/pause.md`, `template/README.md`, `template/docs/engineering/runbook.md` | AC-9 |

## Critical Requirements to Preserve

1. `/auto start-from=<phase>` accepts only canonical phase IDs.
2. Resolver precedence is deterministic and ordered:
   argument > resume brief > state fallback > fail-fast.
3. Stale/conflicting/unparseable resume inputs must fail fast with actionable
   `[AUTO_RESUME_ERROR]` output (no guessing).
4. Continuation must preserve existing stop conditions and decision-gate rules.
5. Breadcrumbs must make continuation source and stop reason inspectable.
6. Manual/interactive workflows must remain unchanged by default.
7. Active/template guidance must remain behaviorally aligned.

## QA and Validation Focus

Required verification scenarios:
- precedence resolution with explicit argument override
- precedence resolution without argument (resume brief then state fallback)
- conflict case (`resume_brief` vs inferred `state` phase) with fail-fast
- stale/unparseable resume brief fail-fast handling
- `[AUTO_RESUME_ERROR]` code contract coverage
- stop-condition preservation in continuation mode
- breadcrumb field coverage in `state.md` and `resume_brief.md`
- active/template parity checks

## Constraints

- Keep scope strictly to US-0037.
- Planning assumptions must not bypass decision gates or input blockers.
- Maintain 1:1 task-to-AC mapping (`T-001`..`T-009` -> `AC-1`..`AC-9`).
- Keep changes deterministic and testable with explicit remediation guidance.

## Done Criteria for Dev Completion

- All 9 tasks in `sprints/S0009/tasks.md` are marked done.
- No uncovered US-0037 acceptance criteria in `sprints/S0009/plan-verify.json`.
- `sprints/S0009/progress.md`, `uat.json`, and `uat.md` are updated with
  execution evidence.
- Traceability row in `docs/engineering/state.md` advances from `PLANNED` to
  post-execution lifecycle state with evidence links.
# TL -> Dev Handoff — Sprint S0009 (US-0037 Auto Continuation)

## Sprint Overview

Sprint S0009 is planned for US-0037: Mid-Process `/auto` Continuation with
Deterministic Resume Point.

- Story count: 1 (`US-0037`)
- Planned tasks: 9
- Sizing: within limit (`SPRINT_MAX_TASKS=12`)
- Split decision: not required (single sprint)
- Milestone activation: not applicable

## Architecture and Decision References

- Story acceptance: `docs/product/backlog.md` (US-0037 AC-1..AC-9)
- Architecture: `docs/engineering/architecture.md` (US-0037 section)
- Decision: `decisions/DEC-0017.md`
- Sprint artifacts: `sprints/S0009/*`

## Execution Order

Execute tasks T-001 through T-009 sequentially.

| Task | Description | Files | AC |
|------|-------------|-------|----|
| T-001 | Define explicit `/auto start-from=<phase>` contract and canonical phase IDs | `.cursor/commands/auto.md` | AC-1 |
| T-002 | Define deterministic resolver precedence and precedence test coverage | `.cursor/commands/auto.md`, `sprints/S0009/uat.md` | AC-2 |
| T-003 | Define conflict/staleness/unparseable fail-fast behavior and `[AUTO_RESUME_ERROR]` codes | `.cursor/commands/auto.md`, `.cursor/rules/core.mdc`, `sprints/S0009/uat.md` | AC-3 |
| T-004 | Define one-command continuation through remaining phases | `.cursor/commands/auto.md` | AC-4 |
| T-005 | Preserve decision gates and stop-condition behavior | `.cursor/commands/auto.md`, `.cursor/rules/core.mdc` | AC-5 |
| T-006 | Define breadcrumb logging contract for `state.md` and `resume_brief.md` | `.cursor/commands/auto.md`, `.cursor/commands/pause.md`, `.cursor/commands/resume.md`, `docs/engineering/state.md`, `handoffs/resume_brief.md` | AC-6 |
| T-007 | Preserve backward compatibility and safe defaults | `.cursor/commands/auto.md`, `.cursor/commands/resume.md` | AC-7 |
| T-008 | Align `/pause`, `/resume`, `/auto` guidance and update README/runbook | `.cursor/commands/auto.md`, `.cursor/commands/resume.md`, `.cursor/commands/pause.md`, `README.md`, `docs/engineering/runbook.md` | AC-8 |
| T-009 | Verify and enforce active/template continuation parity | `template/.cursor/commands/auto.md`, `template/.cursor/commands/resume.md`, `template/.cursor/commands/pause.md`, `template/README.md`, `template/docs/engineering/runbook.md` | AC-9 |

## Critical Requirements to Preserve

1. `/auto start-from=<phase>` accepts only canonical phase IDs.
2. Resolver precedence is deterministic and ordered:
   argument > resume brief > state fallback > fail-fast.
3. Stale/conflicting/unparseable resume inputs must fail fast with actionable
   `[AUTO_RESUME_ERROR]` output (no guessing).
4. Continuation must preserve existing stop conditions and decision-gate rules.
5. Breadcrumbs must make continuation source and stop reason inspectable.
6. Manual/interactive workflows must remain unchanged by default.
7. Active/template guidance must remain behaviorally aligned.

## QA and Validation Focus

Required verification scenarios:
- precedence resolution with explicit argument override
- precedence resolution without argument (resume brief then state fallback)
- conflict case (`resume_brief` vs inferred `state` phase) with fail-fast
- stale/unparseable resume brief fail-fast handling
- `[AUTO_RESUME_ERROR]` code contract coverage
- stop-condition preservation in continuation mode
- breadcrumb field coverage in `state.md` and `resume_brief.md`
- active/template parity checks

## Constraints

- Keep scope strictly to US-0037.
- Planning assumptions must not bypass decision gates or input blockers.
- Maintain 1:1 task-to-AC mapping (`T-001`..`T-009` -> `AC-1`..`AC-9`).
- Keep changes deterministic and testable with explicit remediation guidance.

## Done Criteria for Dev Completion

- All 9 tasks in `sprints/S0009/tasks.md` are marked done.
- No uncovered US-0037 acceptance criteria in `sprints/S0009/plan-verify.json`.
- `sprints/S0009/progress.md`, `uat.json`, and `uat.md` are updated with
  execution evidence.
- Traceability row in `docs/engineering/state.md` advances from `PLANNED` to
  post-execution lifecycle state with evidence links.
# TL -> Dev Handoff — Sprint S0008 (US-0036 Remote Config Contract)

## Sprint Overview

Sprint S0008 is planned for US-0036: Official Remote Config Template, Docs, and
Fail-Fast Validation.

- Story count: 1 (`US-0036`)
- Planned tasks: 10
- Sizing: within limit (`SPRINT_MAX_TASKS=12`)
- Split decision: not required (single sprint)
- Milestone activation: not applicable

## Architecture and Decision References

- Story acceptance: `docs/product/backlog.md` (US-0036 AC-1..AC-9)
- Architecture: `docs/engineering/architecture.md` (US-0036 section)
- Decision: `decisions/DEC-0016.md`
- Sprint artifacts: `sprints/S0008/*`

## Execution Order

Execute tasks T-001 through T-010 sequentially.

| Task | Description | Files | ACs |
|------|-------------|-------|-----|
| T-001 | Add canonical active remote config template | `.cursor/remote.json` | AC-1, AC-3 |
| T-002 | Add template remote config parity | `template/.cursor/remote.json` | AC-1, AC-9 |
| T-003 | Define schema/contract guidance | `.cursor/commands/execute.md`, `.cursor/rules/core.mdc` | AC-2 |
| T-004 | Define mode-aware validation trigger behavior | `.cursor/commands/execute.md`, `.cursor/rules/core.mdc` | AC-4, AC-6 |
| T-005 | Define actionable fail-fast error format | `.cursor/commands/execute.md`, `.cursor/rules/quality.mdc` | AC-5, AC-4 |
| T-006 | Add security constraints for remote config | `.cursor/rules/coding-standards.mdc`, `.cursor/commands/execute.md` | AC-7 |
| T-007 | Update README remote setup and behavior docs | `README.md` | AC-3, AC-8 |
| T-008 | Update runbook validation guidance | `docs/engineering/runbook.md` | AC-4, AC-5, AC-6, AC-8 |
| T-009 | Plan/add positive + negative QA coverage | `tests/run-tests.ps1`, `tests/run-tests.sh`, `sprints/S0008/uat.md` | AC-4, AC-5, AC-6, AC-7, AC-8, AC-9 |
| T-010 | Final state/traceability and handoff cross-reference update | `docs/engineering/state.md`, `handoffs/tl_to_dev.md` | AC-9 |

## Critical Requirements to Preserve

1. Mode-aware behavior:
   - Validate remote config only when `REMOTE_EXECUTION=1`.
   - Skip remote validation entirely when `REMOTE_EXECUTION=0`.
2. Fail-fast requirement:
   - Missing, malformed, semantically invalid, or insecure config must fail fast
     in remote-enabled mode.
3. Error message contract:
   - Include field/path, expected rule, actual value/type, and remediation hint.
4. Security posture:
   - No committed secrets in `.cursor/remote.json`.
   - Use environment variable references for sensitive values.
5. Parity:
   - Active and `template/` copies must stay behaviorally aligned.
   - README and runbook guidance must not contradict each other.

## QA and Validation Focus

Negative-path coverage is mandatory in this sprint. Ensure test planning includes:
- missing `.cursor/remote.json` with `REMOTE_EXECUTION=1`
- malformed JSON syntax
- invalid enum/type/semantic values (e.g., bad target type, missing required field)
- secret-like inline values in config
- confirmation that `REMOTE_EXECUTION=0` avoids false-fail checks

Positive-path coverage should confirm:
- valid config passes in remote-enabled mode
- example targets and docs references remain consistent across active/template

## Constraints

- Keep scope strictly to US-0036.
- Do not implement remote transport backends or external secret manager logic.
- Keep edits atomic and testable with explicit AC mapping.
- Maintain template parity as a first-class requirement, not a follow-up.

## Done Criteria for Dev Completion

- All 10 tasks in `sprints/S0008/tasks.md` moved from pending to done.
- No uncovered US-0036 acceptance criteria.
- `sprints/S0008/progress.md`, `uat.json`, and `uat.md` updated with execution evidence.
- Traceability row in `docs/engineering/state.md` advanced from `PLANNED` to the
  next lifecycle status with evidence links.

## Dev completion note

Dev execution completed for S0008. All T-001..T-010 tasks are marked done and
the sprint is handed off via `handoffs/dev_to_qa.md` for QA verification.
