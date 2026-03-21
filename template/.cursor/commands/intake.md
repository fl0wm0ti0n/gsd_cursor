---
description: "its-magic intake: clarify idea and capture story + acceptance."
---

# /intake

## Subagents
- po

## Execution model
- Run `/intake` in a fresh PO subagent context.
- After writing outputs, stop and hand off to `/discovery` or `/architecture`
  in a new subagent/chat.

## Inputs
- User idea (text or voice transcription)
- Constraints, audience, success criteria

## Outputs (artifacts)
- `docs/product/vision.md`
- `docs/product/backlog.md`
- `docs/product/acceptance.md`
- `handoffs/po_to_tl.md`
- Optional (when enabled): `docs/engineering/compatibility-report.md`
- Optional (when enabled): `docs/engineering/component-scope.md`

## Stop conditions
- Missing acceptance criteria or unclear scope
- Decision gate triggered (see escalation rule)

## Runtime capability and writer-safety guard (US-0059 / DEC-0041)

- `/intake` requires the role-specific `po` subagent capability by default.
- Before any artifact mutation, run capability preflight:
  - if `po` capability is unavailable, fail fast with
    `SUBAGENT_CAPABILITY_UNAVAILABLE`,
  - emit deterministic remediation guidance (for example: enable role-capable
    runtime or explicitly opt in to fallback policy).
- Silent in-band fallback is forbidden unless explicit policy opt-in is
  configured (`INTAKE_SUBAGENT_FALLBACK=allow`).
- For artifact mutations, enforce deterministic single-writer scope:
  - establish writer identity (`writer_id`) and run identity (`intake_run_id`),
  - bind writes to target artifacts (`backlog`, `acceptance`, `vision`,
    `po_to_tl`) for this run.
- Drift guard semantics:
  - self-write changes from the same `(writer_id, intake_run_id)` are valid and
    must not trigger concurrent-writer blockers,
  - external conflicting mutation during active run must fail safe with
    `INTAKE_CONCURRENT_WRITER_DETECTED` and no partial overwrite.

## Mandatory intake question packs and fail-closed persistence gate (US-0068 / DEC-0050)

- Intake must apply one deterministic questionnaire pack before any backlog or
  acceptance persistence:
  - `first-intake-pack` for first/new/broad requests,
  - `small-intake-pack` for narrow follow-up requests.
- Pack selection must be deterministic and auditable:
  - evaluate request breadth (`new capability` vs `bounded refinement`),
  - use known stack/runtime cues when present,
  - unresolved/unknown stack cues must fail closed to `first-intake-pack`
    (never bypass to a smaller pack by default).
- Required topic coverage must be complete before persistence unless bounded
  assumptions are explicitly confirmed:
  - `first-intake-pack` required topics:
    `users_problem`, `runtime_target_environment`, `language_framework_runtime`,
    `architecture_preference`, `ui_design_expectations`,
    `security_compliance`, `non_functional_priorities`, `scope_timeline`.
  - `small-intake-pack` required topics:
    `outcome_success_criteria`, `impacted_components`,
    `constraints_compatibility_risks`, `required_tests_acceptance_checks`,
    `done_definition`.
- Fail-closed deterministic reason codes:
  - `INTAKE_REQUIRED_TOPIC_MISSING`
  - `INTAKE_REQUIRED_PACK_INCOMPLETE`
  - `INTAKE_ASSUMPTION_CONFIRMATION_REQUIRED`
  - `INTAKE_PERSISTENCE_BLOCKED`
- Remediation guidance surface (mandatory on block):
  - list `missing_topics`,
  - request targeted answers for missing required topics,
  - if assumptions are used, require explicit confirmation before write.
- Persistence evidence contract (must be written in intake outputs):
  - `asked_topics`
  - `missing_topics`
  - `assumptions_confirmed`

## Steps
1. Determine intake mode from `.cursor/scratchpad.md`:
   - guided mode: `INTAKE_GUIDED_MODE=1` (default)
   - low-touch mode: `INTAKE_GUIDED_MODE=0`
2. Baseline safety (always on in both modes):
   - Check `docs/product/backlog.md` for duplicates/overlap before creating a new
     story.
3. Guided mode behavior (`INTAKE_GUIDED_MODE=1`):
   a. Run a deterministic decomposition evaluator before persistence. Score
      breadth/risk using:
      - feature/workflow-step count,
      - cross-cutting impact surface (multiple components/contracts),
      - expected acceptance set size,
      - risk/unknown dependency surface.
   b. Decomposition trigger:
      - If evaluator indicates broad/high-risk scope, propose a bounded
        multi-story decomposition (typically 2-5 stories).
      - Otherwise default to a single story.
   c. Split strategy requirements:
      - Prefer vertical-slice or workflow-step stories with independent user value.
      - Avoid technical-layer-only splits unless explicitly requested by the user.
   d. Persist split rationale and boundaries:
      - why split (or why not),
      - split axes used (feature/workflow/risk boundary),
      - boundaries between generated stories.
   e. Preserve explicit user authority before final persistence:
      - user can **accept**, **merge**, or **adjust** the proposed split.
   f. Use adaptive questioning:
      - ask when ambiguity blocks concrete acceptance (baseline),
      - also ask additional targeted questions when breadth/risk is high even if
        the request looks concrete.
   g. Keep questioning bounded:
      - use concise, targeted rounds,
      - stop after bounded rounds or when acceptance confidence is sufficient,
      - summarize assumptions for confirmation.
   h. Present at least one viable option/alternative before recommending an
      approach.
   i. Perform intake-time web research and persist findings as an R-xxxx entry in
      `docs/engineering/research.md` (auto-increment ID, per DEC-0011); cite
      entry IDs in reasoning and handoff.
4. Low-touch behavior (`INTAKE_GUIDED_MODE=0`):
   - Keep baseline duplicate safety from step 2 active.
   - Do not add proactive follow-up/options/research overhead unless the user
     explicitly requests depth.
   - Keep single-story default (no forced decomposition), unless the user
     explicitly requests decomposition.
5. Enforce mandatory question-pack coverage before persistence (US-0068):
   - deterministically select one pack (`first-intake-pack` or
     `small-intake-pack`) and record `selected_pack`.
   - ask required questions for the selected pack; adaptive follow-ups remain
     allowed but bounded.
   - before writing backlog/acceptance artifacts, compute required coverage:
     - if complete, proceed to persistence;
     - if incomplete and no explicit assumption confirmation, fail closed with
       deterministic reason code and remediation guidance.
   - persist intake evidence fields (`asked_topics`, `missing_topics`,
     `assumptions_confirmed`) in relevant intake artifacts.
6. Optional fresh-project ID namespace bootstrap (US-0052 / DEC-0034):
   - Read `ID_NAMESPACE_BOOTSTRAP` from `.cursor/scratchpad.md` (`0|1`,
     default `0`).
   - Freshness eligibility is deterministic and auditable:
     - no existing `US-` IDs in `docs/product/backlog.md`,
     - no existing `DEC-` IDs in `docs/engineering/decisions.md` (or
       `decisions/DEC-*.md`),
     - no existing `R-` IDs in `docs/engineering/research.md`.
   - If `ID_NAMESPACE_BOOTSTRAP=1` and freshness checks pass:
     - first newly created story ID starts at `US-0001`.
   - If `ID_NAMESPACE_BOOTSTRAP=0`, or freshness checks fail:
     - continue from highest existing story ID (collision-safe default).
   - Never rewrite or renumber historical IDs.
   - If bootstrap was requested but checks fail, emit deterministic diagnostic:
     `ID_BOOTSTRAP_NOT_FRESH` with brief remediation guidance.
7. Traceability persistence contract (US-0051):
   - `docs/product/backlog.md`: include decomposition evidence (single-story vs
     split decision, rationale, and boundaries).
   - `docs/product/acceptance.md`: maintain acceptance traceability for resulting
     story set (or single-story decision) with clear scope boundaries.
   - `handoffs/po_to_tl.md`: include split decision summary and adaptive
     questioning evidence (risk/unknown triggers and key assumptions).
8. Persist the story and acceptance in product docs.
9. Write a PO -> TL handoff with scope and risks.
10. Optional cross-repo observability declaration (US-0034):
   - If `CROSS_REPO_OBSERVABILITY=0`, add zero required overhead.
   - If `CROSS_REPO_OBSERVABILITY=1`, capture monitored source list from
     `COMPATIBILITY_SOURCES` (`repo/module/contract/docs`) and include
     compatibility observability intent in handoff context.
11. Optional component scope declaration (US-0035):
   - If `COMPONENT_SCOPE_MODE=0`, add zero required scope overhead.
   - If `COMPONENT_SCOPE_MODE=1`, declare in-scope and out-of-scope components
     in `docs/engineering/component-scope.md` and include references in
     `handoffs/po_to_tl.md`.
12. Optional spec-pack (US-0031):
   - If `SPEC_PACK_MODE=0`, add no required spec-pack steps (zero overhead).
   - If `SPEC_PACK_MODE=1`, ensure CRS artifact for the new story is created or
     updated at canonical path per runbook spec-pack contract; link story ID in
     handoff.
13. Optional user-guide (US-0032):
   - If `USER_GUIDE_MODE=0`, add no required user-guide steps or blocking checks (zero overhead).
   - If `USER_GUIDE_MODE=1`, ensure handoff references canonical user-guide path
     `docs/user-guides/US-xxxx.md` for the new story when applicable; see runbook.
14. Triad hot-surface gate (DEC-0054) when `handoffs/po_to_tl.md` is mutated:
   - run `python scripts/enforce-triad-hot-surface.py --rollover` then `--check`
     from repository root,
   - on failure stop with `STATE_ARCHIVE_REQUIRED` or
     `ARTIFACT_HOT_SURFACE_OVERSIZE` (no successful intake completion with an
     oversize handoff hot file),
   - record the verification tuple (`boundary`, `moved`, `retained`,
     `pack_ref`) in intake outputs when rollover occurred.

## Deterministic artifact ordering contract (US-0058 / DEC-0040)

- Writes to mutable artifacts must follow
  `docs/engineering/artifact-ordering-policy.md`.
- For intake outputs:
  - `docs/product/backlog.md` story blocks must remain sorted-canonical by
    numeric `US-xxxx` ID.
  - `docs/product/acceptance.md` rows must align to canonical backlog order.
  - `handoffs/po_to_tl.md` may prepend the latest handoff section only.
- If the insertion anchor for any target section is missing/ambiguous, fail with
  `ARTIFACT_ORDERING_ANCHOR_AMBIGUOUS` and avoid partial writes.
- If intake appends a `docs/engineering/state.md` checkpoint, enforce UTC
  monotonic timestamp guard (`new >= last`); on violation fail with
  `STATE_TIMESTAMP_NON_MONOTONIC` and avoid partial writes.

## Cross-phase ownership guard (US-0061 / DEC-0043)

- Intake mutations must also comply with
  `docs/engineering/artifact-ownership-policy.md`.
- Intake may mutate only intake-owned scopes (`vision`, `backlog`, `acceptance`,
  `po_to_tl`) for target story context.
- Any attempted delete/rewrite of non-intake-owned sections fails closed with
  `PHASE_OWNERSHIP_VIOLATION`.
- If an override-authorized path is configured for an artifact but required
  override evidence fields are missing, fail with
  `PHASE_OVERRIDE_EVIDENCE_MISSING`.

