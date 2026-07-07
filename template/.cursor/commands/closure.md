# /closure — dedicated story closure phase

## Phase role

- **phase_id**: `closure`
- **role**: `qe`
- **override**: `AUTO_ROLE_CLOSURE` scratchpad key allows `qe` or `curator`; default `qe` when empty (DEC-0052, §2 override, §3 preflight capability gate).

## Phase responsibility

Story Closure holds exclusive responsibility for:

1. Status flip in `docs/product/backlog.md` (canonical status owner per US-0045): `Status: OPEN` → `Status: DONE`
2. Acceptance checkbox in `docs/product/acceptance.md`: `- [ ]` → `- [x]`
3. Closure checkpoint append to `docs/engineering/state.md` (append-bottom per US-0058 / DEC-0040)
4. Creation of per-sprint closure verification artifact: `sprints/Sxxxx/closure-verification.md`

`/closure` runs AFTER `/release` completes with PASS verdict and BEFORE `/refresh-context`.

## Phase ordering (ship macro per DEC-0082)

| Position | Phase | Role |
|----------|-------|------|
| 1 | `/release` | `release` |
| 2 | `/closure` | `qe` |
| 3 | `/refresh-context` | `curator` |

`/closure` is now the **second** phase of the `ship` macro. `/release` no longer performs backlog reconciliation (steps 10-12 removed).

## Inputs

The `/closure` phase consumes the following release artifacts as input evidence (all three are FAIL-gated input prerequisites):

| Artifact | Path | Required |
|----------|------|----------|
| Release queue row | `handoffs/release_queue.md` (target sprint, `status=released`) | YES |
| Release notes | `handoffs/releases/Sxxxx-release-notes.md` (with PASS verdict) | YES |
| QA findings | `sprints/Sxxxx/qa-findings.md` | YES |
| UAT (optional) | `sprints/Sxxxx/uat.json` / `sprints/Sxxxx/uat.md` | OPTIONAL |
| Release findings (optional) | `sprints/Sxxxx/release-findings.md` | OPTIONAL |

## Outputs (artifacts)

`/closure` produces the following artifacts:

| Artifact | Path | Responsibility |
|----------|------|----------------|
| Closure verification | `sprints/Sxxxx/closure-verification.md` | Per-sprint closure execution record |
| Backlog status flip | `docs/product/backlog.md` (target story block only) | `Status: OPEN` → `Status: DONE` |
| Acceptance tick | `docs/product/acceptance.md` (target row only) | `- [ ]` → `- [x]` |
| Closure checkpoint | `docs/engineering/state.md` (append-bottom) | Phase boundary + isolation evidence + runtime proof |

## Stop conditions

- Release evidence missing for target sprint → `CLOSURE_RELEASE_EVIDENCE_MISSING`
- Canonical status source contradictory (release evidence vs backlog state) → `CANONICAL_STATUS_CONFLICT`
- Multiple candidate stories ambiguous for closure → `CLOSURE_AMBIGUOUS_TARGET`
- Target story not found in backlog.md → `CLOSURE_TARGET_NOT_FOUND`

## Input prerequisites (fail-gated)

The following MUST be true before `/closure` can proceed. Fail closed with `CLOSURE_RELEASE_EVIDENCE_MISSING` if any check fails:

1. `handoffs/release_queue.md` contains a row for the target sprint with `status=released`.
2. `handoffs/releases/Sxxxx-release-notes.md` EXISTS and contains PASS verdict.
3. `sprints/Sxxxx/qa-findings.md` EXISTS (QA completion evidence).

If any prerequisite fails:
- Do not mutate backlog.md, acceptance.md, or state.md.
- Append `CLOSURE_RELEASE_EVIDENCE_MISSING` with specific missing-prerequisite list to `sprints/Sxxxx/closure-verification.md` (partial artifact — marks the attempt and the gap).
- Stop and require operator remediation before retry.

## Backlog reconciliation contract (US-0043 / DEC-0021)

`/closure` now holds exclusive responsibility for backlog reconciliation.

Canonical evidence precedence:
1. `handoffs/release_queue.md` target sprint row (`status=released` required)
2. `handoffs/releases/Sxxxx-release-notes.md` gate summary
3. `sprints/Sxxxx/qa-findings.md`
4. `sprints/Sxxxx/uat.json` and `sprints/Sxxxx/uat.md`
5. `sprints/Sxxxx/release-findings.md` (if present)

Deterministic reconciliation behavior:
- Mutate only target sprint story blocks in `docs/product/backlog.md`
- Set target story `Status: DONE` when mandatory release evidence is PASS
- Reconcile target story acceptance checkboxes to checked state in `docs/product/acceptance.md`
- Never mutate unrelated backlog stories

## Canonical status source and global drift guard (US-0045 / DEC-0025)

Canonical ownership:
- Story status (`OPEN|DONE`) is authoritative in `docs/product/backlog.md`.
- `docs/product/acceptance.md` and `docs/engineering/state.md` are derived views.

Deterministic reconciliation precedence:
1. `docs/product/backlog.md` story status (canonical status owner)
2. Target sprint release evidence
3. Derived-view updates (`docs/product/acceptance.md`, `docs/engineering/state.md`)

## Orchestrator post-closure verification protocol

After `/closure` subagent returns, the orchestrator runs direct `rg` verification (materialization fidelity check):

1. `rg "^- Status: DONE$" docs/product/backlog.md` constrained to target story block
2. `rg "^\- \[x\] US-xxxx:" docs/product/acceptance.md` targeted row
3. State.md: `rg "phase_id=closure" docs/engineering/state.md` combined with `rg "story_id=US-xxxx"`
4. `rg "story_id.*US-xxxx" sprints/Sxxxx/closure-verification.md`

If ANY check fails → escalate `CLOSURE_VERIFICATION_FAILED` with specific check that failed.

## closure-verification.md schema

Required fields (in `sprints/Sxxxx/closure-verification.md`):
- `story_id` (US-xxxx)
- `closure_date` (ISO-8601 UTC)
- `closure_role` (qe|curator)
- `pre_closure_status` (OPEN)
- `post_closure_status` (DONE)
- `release_evidence_refs[]` (array of paths)
- `isolation_evidence{}` (object per US-0048 / DEC-0029)
- `runtime_proof{}` (object per US-0056 / DEC-0038)

Optional fields:
- `normalization_notes` — edge cases
- `backward_compat_note` — for in-flight story closure

Validate with: `python scripts/validate_closure_verification.py --file sprints/Sxxxx/closure-verification.md`

## Artifact ordering contract (US-0058 / DEC-0040)

`/closure` mutations follow strict ordering:
1. `docs/product/backlog.md` (status flip — canonical status owner)
2. `docs/product/acceptance.md` (checkbox tick — derived view)
3. `docs/engineering/state.md` (closure checkpoint append — append-bottom only)
4. `sprints/Sxxxx/closure-verification.md` (new artifact)

## Cross-phase ownership guard (US-0061 / DEC-0043)

`/closure` owns ONLY:
- Status flip in `docs/product/backlog.md` (target story block)
- Checkbox tick in `docs/product/acceptance.md` (target row)
- Closure checkpoint append in `docs/engineering/state.md`
- `sprints/Sxxxx/closure-verification.md` creation

`/closure` must NOT touch:
- Release artifacts (`handoffs/releases/Sxxxx-release-notes.md`, `handoffs/release_queue.md`)
- QA artifacts (`sprints/Sxxxx/qa-findings.md`, `handoffs/qa_to_dev.md`)
- Execute artifacts (`sprints/Sxxxx/summary.md`, code changes)

## Drain hook backward compatibility (AC-10)

For in-flight stories at US-0120 ship boundary (stories that completed `/release` before `/closure` existed):
- 3-signal detection: (i) release_queue row `status=released`, (ii) backlog.md `Status: OPEN`, (iii) acceptance.md `[ ]` unchecked → closure SKIPPED → orchestrator spawn `/closure` backfill.
- For `Status: DONE` stories: SKIP (already closed).
- Pre-US-0120 stories with all three signals: emit `CLOSURE_LEGACY_DRIFT` + manual reconciliation guidance.

## Fail-safe reason codes and remediation guidance

| Reason code | Condition | Remediation |
|---|---|---|
| `CLOSURE_RELEASE_EVIDENCE_MISSING` | Input prerequisite not met | Complete `/release` first |
| `CLOSURE_VERIFICATION_FAILED` | Orchestrator post-verification rg check failed | Re-run `/closure` |
| `CANONICAL_STATUS_CONFLICT` | Backlog status contradicts release evidence | Resolve contradiction manually |
| `BACKLOG_STATUS_DRIFT` | Backlog not reconciled after closure | Re-run `/closure` |
| `PHASE_OWNERSHIP_VIOLATION` | `/closure` tried to mutate non-owned artifact | Check cross-phase ownership guard |
| `PHASE_OVERRIDE_EVIDENCE_MISSING` | Override path configured but evidence missing | Provide override evidence or disable override |
| `CLOSURE_LEGACY_DRIFT` | Pre-US-0120 story with released+OPEN | Manual reconciliation or backfill closure |

## Strict runtime proof (DEC-0038)

Each `/closure` execution must produce own strict runtime proof with unique `runtime_proof_id`:
- runtime_proof_id (unique per closure run)
- proof_hash (SHA-256 of canonical payload)
- proof_ttl_seconds (3600)
- proof_issued_at (ISO-8601 UTC)

## Isolation evidence (US-0048 / DEC-0029)

Each `/closure` execution must produce own isolation evidence:
- phase_id=closure, role=qe (or curator)
- fresh_context_marker (unique per run per BUG-0006)
- timestamp (ISO-8601 UTC)
- evidence_ref (sprints/Sxxxx/closure-verification.md)
