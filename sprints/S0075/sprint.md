# Sprint S0075

## Metadata

- **sprint_id**: S0075
- **story_refs**: US-0089
- **goal**: Deliver response-side Cursor Caveman voice mode, default-off, as a rule-only surface with scratchpad-locked flags, orthogonal to `TOKEN_PROFILE`, and regression-locked via default-off invariant tests — with active + `template/` parity on every touched surface.
- **status**: planned
- **created_at**: 2026-04-18T12:45:00Z
- **orchestrator_run_id**: auto-20260418-01

## Scope

- **US-0089**: Cursor Caveman mode (scratchpad-configurable terse responses)
- **Architecture**: `docs/engineering/architecture.md` `# US-0089`
- **Decision lock**: `decisions/DEC-0072.md` (Accepted) — scratchpad contract, composition surface, default-off invariant
- **Research**: `docs/engineering/research.md` `R-0073` (discovery + research extensions)

## Non-goals (hard, inherited from DEC-0072 §8)

- No input-side file compression (owned by **US-0090**); `CAVEMAN_COMPRESS_INPUT` / `CAVEMAN_FILE_SCOPE` remain documented no-ops.
- No change to `TOKEN_PROFILE` / **US-0080** semantics, context-pack policy, or archive policy.
- No rewrite of canonical artifacts (`docs/product/backlog.md` outside `architecture_notes`/`sprint_plan_notes` appends, `docs/product/acceptance.md`, `docs/engineering/state.md` schema, `handoffs/intake_evidence/*.json`, DEC files).
- No new dependencies (`package.json` untouched); no `npx skills add` token anywhere in normative docs/rules.
- No edit of `.cursor/skills/its-magic/SKILL.md` (row 8 negative-parity assertion).
- No change to spawn-only orchestration (**US-0048** / **DEC-0029** / **BUG-0006**), strict runtime proof (**DEC-0038**), **`AUTO_QUIET`** non-suppressible list (**US-0088**), or **US-0071** visible-metadata rules.
- No unit-test of voice quality under `CAVEMAN_MODE=1`.

## Dependencies

- Upstream (locked): **DEC-0072** (architecture decision), architecture section **`# US-0089`**, research extension **`R-0073`** (2026-04-18).
- Governance stack (unchanged): **US-0017** (template parity), **US-0045** (canonical status), **US-0048 / DEC-0029** (isolation), **US-0056 / DEC-0038** (strict runtime proof), **US-0058 / DEC-0040** (artifact-ordering), **US-0069 / DEC-0051** (phase-role), **US-0080 / DEC-0062** (`TOKEN_PROFILE`), **US-0088** (`AUTO_QUIET` non-suppressible list).
- Downstream: **US-0090** consumes scratchpad vocabulary established here (no code dependency — order-only).

## Acceptance criteria coverage

| AC | Description | Task |
|----|-------------|------|
| AC-1 | Scratchpad contract — new keys in active + `template/` scratchpad surfaces (active `.cursor/scratchpad.md`, active + template `.cursor/scratchpad.local.example.md`) with exact byte-literal lines per **DEC-0072 §3** | T-001 |
| AC-2 | Default-off parity — byte-equivalent normative strings / gate ordering / spawn-only language / existing contract tokens preserved under `CAVEMAN_MODE=0` (additive-only drift) | T-002 |
| AC-3 | Cursor behavior pack — `.cursor/rules/caveman.mdc` (active + `template/`) implements terse voice when enabled; 9-zone literal-region invariant enforced (hard `MUST`) | T-003 |
| AC-4 | `TOKEN_PROFILE` composition — verbatim non-substitution paragraph published in `docs/engineering/auto-orchestration-reference.md` (active + `template/`) | T-004 |
| AC-5 | Operator control — runbook subsection `### Caveman mode (US-0089)` with five canonical phrases + scratchpad-authoritative semantics (active + `template/`) | T-005 |
| AC-6 | Tests — 8 `test_caveman_default_off_*` subtests extending `tests/auto_command_contract_test.py` in place | T-006 |
| AC-7 | `architecture.md` `# US-0089` — linkage / append-bottom integrity confirmed; no rewrite (section already written at `/architecture`) | T-007 |
| AC-8 | Template parity sweep — every touched active surface mirrored per **US-0017**; negative-parity assertion for `.cursor/skills/its-magic/SKILL.md` (no change, row 8) | T-008 |

## Task count

- **Total**: 8
- **SPRINT_MAX_TASKS**: 12
- **Within limit**: yes (8 <= 12; `SPRINT_AUTO_SPLIT` not triggered)
- **task_ac_bijection**: true (T-001..T-008 <-> AC-1..AC-8)

## Governance

- **DEC-0072**: scratchpad contract, composition surface, default-off invariant, 9-zone literal-region list, operator phrases, 8-row template parity inventory.
- **R-0073** (2026-04-18 research extension): TOKEN_PROFILE × CAVEMAN precedence, rule-only vs rule+skill, default-off test strategy, operator toggle vocabulary, 9-zone invariants, external pattern portability, scratchpad key naming, template parity inventory.
- **US-0088**: `AUTO_QUIET` non-suppressible gate vocabulary preserved (contract subtest #7).
- **US-0071**: user-visible metadata sanitization unchanged (no hidden-ID resurrection via terse voice).
- **US-0021**: decision-gate, errors, evidence contracts non-suppressible under `CAVEMAN_MODE=1`.
- **US-0085 / DEC-0071**: no `.env` reads; no secrets in output; names-only evidence posture (unchanged).

## Template parity plan (8-row inventory — DEC-0072 §7)

| # | Active path | Template path | Action | Task |
|---|-------------|---------------|--------|------|
| 1 | `.cursor/scratchpad.md` | n/a (example-only install, **DEC-0055**) | Add 4 Caveman key lines + `## Caveman mode (US-0089)` comment block | T-001 |
| 2 | `.cursor/scratchpad.local.example.md` | `template/.cursor/scratchpad.local.example.md` | Same 4 key lines + comment block, byte-identical active/template | T-001 |
| 3 | `.cursor/rules/caveman.mdc` (**new**) | `template/.cursor/rules/caveman.mdc` (**new**) | Create rule with `CAVEMAN_MODE` gate, 9-zone literal-region invariant, 5 canonical phrases, non-suppressible gate list | T-003 |
| 4 | `docs/engineering/auto-orchestration-reference.md` | `template/docs/engineering/auto-orchestration-reference.md` | Insert verbatim non-substitution paragraph (orthogonal axes) | T-004 |
| 5 | `docs/engineering/runbook.md` | `template/docs/engineering/runbook.md` | Add `### Caveman mode (US-0089)` subsection: key table + phrase catalog + non-substitution paragraph | T-005 |
| 6 | `docs/engineering/architecture.md` `# US-0089` | active-only | Already written at `/architecture` — verify linkage/append-bottom integrity | T-007 |
| 7 | `tests/auto_command_contract_test.py` | active-only | Extend in place with 8 `test_caveman_default_off_*` subtests | T-006 |
| 8 | `.cursor/skills/its-magic/SKILL.md` | `template/.cursor/skills/its-magic/SKILL.md` | **No change** — negative-parity assertion (row 8) | T-008 |

## Risk notes

- **R1 — Voice drift into literal regions**: A subagent under `CAVEMAN_MODE=1` might abbreviate reason codes, AC wording, IDs, or strict-proof tuple fields. Mitigation: `.cursor/rules/caveman.mdc` states the 9-zone invariant as hard `MUST`; contract subtest #3 asserts the nine literal-region tokens are present in both active + template rule bodies.
- **R2 — Silent substitution with `TOKEN_PROFILE`**: Operators may read `CAVEMAN_MODE=1` as equivalent to a leaner `TOKEN_PROFILE`. Mitigation: verbatim non-substitution paragraph in reference + runbook (active + template); contract subtest #4 asserts literal sentence presence.
- **R3 — Non-suppressible gate drift**: Terse voice could mask `decision_gate`, `[BUG_VALIDATION_OK]`, `[INTAKE_EVIDENCE_VALIDATION_OK]`, `blocked`, `missing input`, or **US-0088** `AUTO_QUIET` gate vocabulary. Mitigation: rule body lists non-suppressible items; contract subtest #7 asserts gate vocabulary intact.
- **R4 — Vendor install leak**: External reference repo (`JuliusBrussee/caveman`, MIT) documents `npx skills add`; that token must not land in kit docs/rules. Mitigation: contract subtest #8 asserts absence of `npx skills add` anywhere.
- **R5 — Template parity slip**: Active-only edit of a surface with a template mirror would break **US-0017**. Mitigation: T-008 sweep + contract subtests #2 / #3 / #4 / #5 assert byte-parity where required; dev must edit both surfaces in the same commit (see handoff).
- **R6 — Default-off regression**: Any change to existing `required` token list that drops/renames a token would regress **US-0045** / **US-0088** contracts. Mitigation: contract subtest #6 asserts existing token list is intact (only additive).
- **R7 — Cross-spawn toggle drift**: Session phrases that bypass scratchpad could desync state across subagent spawns. Mitigation: DEC-0072 §5 and rule text declare scratchpad authoritative; session phrases are next-turn overlays only.
- **R8 — `CAVEMAN_LEVEL` unknown value**: Non-enum values (e.g. typos) must fail-closed. Mitigation: DEC-0072 §3 locks `CAVEMAN_LEVEL_UNKNOWN` semantics; rule preserves literal prose when level is unrecognized.

## Definition of done

- All 8 acceptance criteria covered by their mapped tasks (T-001..T-008 -> AC-1..AC-8).
- `tests/auto_command_contract_test.py` gains 8 passing `test_caveman_default_off_*` subtests (default-off invariants + literal token / file-presence assertions).
- No drift in normative command strings / gate ordering / spawn-only language; existing `required` token list extended only by addition.
- Template parity verified across rows 2, 3, 4, 5 of the DEC-0072 §7 inventory; rows 1 (example-only install), 6 (active-only architecture), 7 (active-only tests) follow their documented non-parity pattern; row 8 negative-parity confirmed (file untouched).
- `docs/product/backlog.md` **`## US-0089`** retains `OPEN` status (**US-0045**) through plan-verify; closure happens at `/verify-work`.
- `sprints/S0075/plan-verify.json` reaches **PASS** with `plan_integrity.task_ac_bijection=true`.
