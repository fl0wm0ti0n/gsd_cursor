# QA findings — Sprint S0057 / US-0078

- **Story**: US-0078 — Enforced interactive intake question evidence
- **Sprint**: S0057
- **Orchestrator run**: `auto-20260328-01`
- **QA phase**: `/qa` (fresh **qa** context)
- **Overall verdict**: **PASS**
- **Evidence reviewed**: `handoffs/dev_to_qa.md`, `sprints/S0057/tasks.md`, `scripts/intake_evidence_lib.py`, `scripts/intake_evidence_validate.py`, `tests/intake_evidence_fixtures_test.py`, `.cursor/commands/intake.md` (gate ordering), `decisions/DEC-0060.md`, `docs/engineering/architecture.md` (`# US-0078`), `docs/engineering/decisions.md`, `template/` mirrors (spot parity with dev handoff)

## Test plan (executed)

| Step | Command / check | Result |
|------|-------------------|--------|
| Tier A/B matrix | `python tests/intake_evidence_fixtures_test.py` | **PASS** |
| Validator self-test | `python scripts/intake_evidence_validate.py --self-test` | **PASS** |
| Intake gate ordering | Read `.cursor/commands/intake.md` — validate before backlog/acceptance mutation | **PASS** (§ “Interactive intake evidence gate” before persistence) |
| AC-10 traceability | `DEC-0060`, `architecture.md` `# US-0078`, `decisions.md` index | **PASS** |

**Not run (non-blocking)**: Full `tests/run-tests.ps1` — dev noted possible unrelated Homebrew/npm baseline **FAIL**; US-0078 regression surface is §26k equivalents + Python fixtures above (all green).

**Hot surface (DEC-0054)**: After appending the QA checkpoint to **`docs/engineering/state.md`**, **`enforce-triad-hot-surface.py --check`** required **`--rollover`** → **`docs/engineering/state-archive/state-pack-20260328-g.md`**; final **`--check`** **PASS**.

## Per-AC verdicts

| AC | Verdict | Blockers | Non-blockers / notes |
|----|---------|----------|----------------------|
| **AC-1** | **PASS** | — | `validate_intake_evidence` requires each pack key with `topic_coverage` row, valid `satisfied_by`, verifiable `ie:` `ref` (`intake_evidence_lib.py`). |
| **AC-2** | **PASS** | — | Literal `yes` / false confirmations and affirmative `assumptions_confirmed` without `assumption_confirmation_ref` → `INTAKE_ASSUMPTION_CONFIRMATION_REQUIRED` (fixtures P4, P2 positive path). |
| **AC-3** | **PASS** | — | Failures add `INTAKE_PERSISTENCE_BLOCKED` with primary codes preserved; intake command states no backlog/acceptance mutation until validation **PASS**. |
| **AC-4** | **PASS** | — | Bundle contract documents `asked_topics` vs `topic_coverage` / answered evidence and `assumption_confirmation_ref` fields; validator enforces asked-vs-covered alignment (fixtures P5). |
| **AC-5** | **PASS** | — | Same validation rules for guided; no mode branch in validator (`intake_guided_mode` no-op per docstring + `self_test` parity assert). |
| **AC-6** | **PASS** | — | Same pipeline for `intake_guided_mode=0` and `1` in `self_test`; intake.md states parity for low-touch. |
| **AC-7** | **PASS** | — | `missing_topics`, remediation strings, and reason codes on failure paths (`ValidationResult`, `format_blocked_message`). |
| **AC-8** | **PASS** | — | P1–P5 matrix + unknown pack + subprocess `--file` smoke in `tests/intake_evidence_fixtures_test.py`; `run-tests.sh` / `run-tests.ps1` §26k wiring per dev handoff. |
| **AC-9** | **PASS** | — | Dev handoff + grep: active + `template/` intake, runbook, README asserts in test runners; spot-check consistent with **US-0030** parity intent. |
| **AC-10** | **PASS** | — | **`DEC-0060`** + **`architecture.md`** **`# US-0078`** + **`docs/engineering/decisions.md`** index lines cite validator paths and story. |

## Residual risks (informational)

- Full PowerShell runner may still surface **US-0016** / **US-0074** baseline noise unrelated to this story.
- Grandfathered legacy rows: enforcement is on **next** mutation per **DEC-0060** — operators must supply full evidence on write.

## Recommendation

- **`/verify-work`** completed — proceed to **`/release`** for **S0057** / **US-0078** with `next_scheduled_phase=release` (see **`sprints/S0057/uat.json`**, **`sprints/S0057/uat.md`**, **`docs/engineering/state.md`** verify-work checkpoint).
