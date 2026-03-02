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

## Steps
1. Determine intake mode from `.cursor/scratchpad.md`:
   - guided mode: `INTAKE_GUIDED_MODE=1` (default)
   - low-touch mode: `INTAKE_GUIDED_MODE=0`
2. Baseline safety (always on in both modes):
   - Check `docs/product/backlog.md` for duplicates/overlap before creating a new
     story.
3. Guided mode behavior (`INTAKE_GUIDED_MODE=1`):
   a. Ask targeted follow-up questions only when ambiguity prevents concrete
      acceptance criteria.
   b. Present at least one viable option/alternative before recommending an
      approach.
   c. Preserve user authority explicitly: PO recommends, user decides.
   d. Perform intake-time web research and persist findings as an R-xxxx entry in
      `docs/engineering/research.md` (auto-increment ID, per DEC-0011); cite
      entry IDs in reasoning and handoff.
4. Low-touch behavior (`INTAKE_GUIDED_MODE=0`):
   - Do not add proactive follow-up/options/research overhead unless the user
     explicitly requests depth.
   - Keep baseline duplicate safety from step 2 active.
5. Persist the story and acceptance in product docs.
6. Write a PO -> TL handoff with scope and risks.
7. Optional cross-repo observability declaration (US-0034):
   - If `CROSS_REPO_OBSERVABILITY=0`, add zero required overhead.
   - If `CROSS_REPO_OBSERVABILITY=1`, capture monitored source list from
     `COMPATIBILITY_SOURCES` (`repo/module/contract/docs`) and include
     compatibility observability intent in handoff context.
8. Optional component scope declaration (US-0035):
   - If `COMPONENT_SCOPE_MODE=0`, add zero required scope overhead.
   - If `COMPONENT_SCOPE_MODE=1`, declare in-scope and out-of-scope components
     in `docs/engineering/component-scope.md` and include references in
     `handoffs/po_to_tl.md`.
9. Optional spec-pack (US-0031):
   - If `SPEC_PACK_MODE=0`, add no required spec-pack steps (zero overhead).
   - If `SPEC_PACK_MODE=1`, ensure CRS artifact for the new story is created or
     updated at canonical path per runbook spec-pack contract; link story ID in
     handoff.
10. Optional user-guide (US-0032):
   - If `USER_GUIDE_MODE=0`, add no required user-guide steps or blocking checks (zero overhead).
   - If `USER_GUIDE_MODE=1`, ensure handoff references canonical user-guide path
     `docs/user-guides/US-xxxx.md` for the new story when applicable; see runbook.

