# PO to TL archive pack (2026-06-28)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=650, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 10
- First archived heading: `## Orchestrated discovery handoff — US-0104 / auto-20260628-04`
- Last archived heading: `## Orchestrated discovery handoff — US-0104 / auto-20260628-04`
- Verification tuple (mandatory):
  - archived_body_lines=85
  - retained_body_lines=635

---

## Orchestrated discovery handoff — US-0104 / auto-20260628-04

### Target

- `story_id=US-0104`
- `orchestrator_run_id=auto-20260628-04`
- phase completed: **`discovery`** (**`po`**)
- `fresh_context_marker=po-US0104-discovery-20260628T213500Z-fresh`
- `next_scheduled_phase=research`
- `decomposition=single_story` (sovereign-loop batch per intake-sovereign-20260627-01.json)
- `priority=P1`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=7`

### Summary

- **`/discovery`** **PASS** — cross-model adversarial critic locked: default-off **`CROSS_MODEL_REVIEW`** scratchpad gate; per-phase **`/sovereign-critic`** spawn with **different `model_id`** than producer; three-lens evaluation (**Challenger** / **Architect** / **Subtractor**); parallel-jury reconciliation via **`scripts/sovereign_critic_lib.py`**; additive **`model_id`** on **US-0048** isolation evidence; anti-slop scoring with bounded rework loop; degraded **single-model-multi-lens** fallback. **Compose do NOT amend** **US-0048** / **US-0069** / **US-0023** / **US-0110** — populates **`handoffs/sovereign_critic_findings.jsonl`** (US-0110 conjunct 3) and sets **`cross_model_reviewed=true`** on **US-0103** ledger entries.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Discovery locks (research inputs)

| Lock | Decision |
|------|----------|
| **L1 Scratchpad keys** | `CROSS_MODEL_REVIEW=0\|1` (default `0`); `CROSS_MODEL_ANTISLOP_THRESHOLD` int default `6`; `CROSS_MODEL_REWORK_MAX` int default `2`; zero overhead when `0` |
| **L2 Command** | `/sovereign-critic` (`.cursor/commands/sovereign-critic.md` + template); orchestrator hook after producer phase when enabled |
| **L3 Lenses** | `challenger` \| `architect` \| `subtractor` — all three per critic invocation |
| **L4 Findings artifact** | `handoffs/sovereign_critic_findings.jsonl` append-only JSONL v1 (14 fields — see backlog L4) |
| **L5 Reconciliation lib** | `scripts/sovereign_critic_lib.py` + `sovereign_critic_validate.py`; agreement → high confidence; single-finder → medium + flagged |
| **L6 Isolation `model_id`** | Additive US-0048 extension; required when critic enabled; `ISOLATION_EVIDENCE_MODEL_ID_MISSING` fail-closed |
| **L7 Anti-slop + rework** | Per-lens 0–10; aggregate default `min(lens_scores)`; below threshold → rework; cap → decision gate |
| **L8 Degraded fallback** | Single-model-multi-lens when no distinct critic slug; `degraded_mode=true`; informational only |
| **L9 Ledger hook** | `cross_model_reviewed=true` via **US-0103** `decision_ledger_lib` when ledger enabled |
| **L10 Contract tests** | 8× `test_us0104_*` + `--scope=sovereign-critic` (`SOVEREIGN_CRITIC_PAIRS`) |
| **L11 Reason codes** | 10-code `CROSS_MODEL_*` + `ISOLATION_EVIDENCE_MODEL_ID_MISSING` family |
| **L12 Compose** | US-0048/US-0069/US-0023/US-0110 unchanged; US-0101/0102 model resolution consumed read-only |

### Acceptance pointers (discovery emphasis)

- **AC-1**: Scratchpad keys + zero-overhead default-off.
- **AC-2**: `/sovereign-critic` command + orchestrator integration.
- **AC-3**: Three-lens enum + templates; all lenses per invocation.
- **AC-4**: `model_id` in isolation evidence (additive US-0048).
- **AC-5**: Reconciliation library + confidence levels.
- **AC-6**: Anti-slop threshold + bounded rework loop.
- **AC-7**: Degraded single-model-multi-lens fallback.
- **AC-8**: Contract tests, parity, architecture `# US-0104`, runbook, reason codes.

### Top risks (carry to /research)

- **R1**: Model routing reliability (**R-0088** Cursor subagent limitations) — degraded fallback must be deterministic.
- **R2**: Phase latency/token cost — default-off gate essential.
- **R3**: Rework oscillation — cap + decision gate at `CROSS_MODEL_REWORK_MAX`.
- **R4**: Anti-slop determinism — rubric must be lib-checkable, not LLM-subjective only.
- **R5**: Parallel-jury dedup — normalization key affects confidence labels.
- **R6**: **US-0108** consumer — anti-slop aggregate formula must remain stable.

### Research asks (extend **`R-0092`**)

1. Findings JSONL exact schema + validator CLI.
2. Full `sovereign_critic_lib.py` API + issue-normalization key algorithm.
3. `select_critic_model` composing US-0101/0102 — deterministic different-slug selection.
4. Anti-slop rubric + `/auto` rework orchestration + evidence tuple extensions.
5. Isolation evidence `model_id` v2 matrix + regression guards.
6. Contract-test inventory + `SOVEREIGN_CRITIC_PAIRS` parity file list.
7. Companion `DEC-xxxx` necessity.

### Evidence refs

- `docs/product/backlog.md` (`## US-0104` — `discovery_notes`)
- `docs/product/vision.md` (Discovery Notes — US-0104)
- `docs/engineering/research.md` (**`R-0092`** stub)
- `handoffs/intake_evidence/intake-sovereign-20260627-01.json`
- Compose (do not amend): **US-0103** / **DEC-0103**, **US-0110** / **DEC-0110**, **US-0101** / **R-0088**
- Upstream consumer surfaces: `scripts/sovereign_convergence_lib.py` **`CRITIC_PATH`**; `decision_ledger_lib.py` **`cross_model_reviewed`**

### Next

- **`/research`** (fresh **tech-lead** context) for **`US-0104`** — close **`R-0092`** Q1–Q7; lock critic schema, helper lib, model-selection algorithm, contract tests inventory.

### Decision gate

- **None** — discovery satisfied; research readiness explicit.

---

