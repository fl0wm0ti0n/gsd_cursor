# PO to TL archive pack (2026-06-28)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=650, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 2
- Retained units in hot file: 10
- First archived heading: `## Orchestrated architecture handoff — US-0104 / auto-20260628-04`
- Last archived heading: `## Orchestrated research handoff — US-0104 / auto-20260628-04`
- Verification tuple (mandatory):
  - archived_body_lines=140
  - retained_body_lines=635

---

## Orchestrated architecture handoff — US-0104 / auto-20260628-04

### Target

- `story_id=US-0104`
- `orchestrator_run_id=auto-20260628-04`
- phase completed: **`architecture`** (**`tech-lead`**)
- `fresh_context_marker=tl-US0104-architecture-20260628T223000Z-fresh`
- `next_scheduled_phase=sprint-plan`
- `decomposition=single_story` (sovereign-loop batch per intake-sovereign-20260627-01.json)
- `priority=P1`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=7`

### Summary

- **`/architecture`** **PASS** — **`DEC-0104`** ratified; **`# US-0104`** appended; 11 atomic task seeds; eight **`test_us0104_*`** contract markers + compose guards **`test_us0104_us0048_compose_no_base_schema_change`**, **`test_us0104_us0110_critic_path_unchanged`**; **`SOVEREIGN_CRITIC_PAIRS`** parity manifest (5 pairs).
- **Default-off gate**: **`CROSS_MODEL_REVIEW`**: `0`|`1` (default **`0`**); **`CROSS_MODEL_ANTISLOP_THRESHOLD`** default **`6`**; **`CROSS_MODEL_REWORK_MAX`** default **`2`**.
- **Tranche order**: A scratchpad+reason codes → B **`sovereign_critic_lib.py`** → C validator+command → D rework+isolation+degraded → E tests+parity+runbook.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Architecture locks (sprint-plan inputs)

| Lock | Decision |
|------|----------|
| **Binding decision** | **`DEC-0104`** — composes **US-0048** / **US-0069** / **US-0023** / **US-0110** / **US-0103** (additive only) |
| **Task seeds** | 11 seeds (under **`SPRINT_MAX_TASKS=12`** threshold) |
| **Findings path** | **`handoffs/sovereign_critic_findings.jsonl`** (15-field v1; matches **US-0110** `CRITIC_PATH`) |
| **Lenses** | `challenger` \| `architect` \| `subtractor` — all three per invocation |
| **Reconciliation** | `compute_issue_key` → `ik_<sha16>`; ≥2 lenses agree → `confidence=high` |
| **Model selection** | Tier opposition via **`model_tier_lib`**; same slug → degraded single-model-multi-lens |
| **Anti-slop** | 4-item checklist per lens; aggregate `min(lens_scores)`; rework cap → decision gate |
| **Contract tests** | **`test_us0104_scratchpad_keys_literals`**, **`test_us0104_sovereign_critic_command_literals`**, **`test_us0104_three_lens_enum_contract`**, **`test_us0104_findings_jsonl_schema_contract`**, **`test_us0104_reconciliation_agreement_branches`**, **`test_us0104_model_id_isolation_evidence_extension`**, **`test_us0104_antislop_rework_cap_literals`**, **`test_us0104_degraded_fallback_zero_overhead`** |
| **Parity scope** | **`check_intake_template_parity.py --scope=sovereign-critic`** (**`SOVEREIGN_CRITIC_PAIRS`**) |

### AC ↔ task bijection

| AC | Task seeds |
|----|------------|
| AC-1 | T-001, T-002 |
| AC-2 | T-006 |
| AC-3 | T-003, T-006 |
| AC-4 | T-008 |
| AC-5 | T-003, T-004, T-005 |
| AC-6 | T-007 |
| AC-7 | T-009, T-011 |
| AC-8 | T-002, T-005, T-010, T-011 |

### Top risks (carry to /sprint-plan)

- **R1**: Cursor subagent model routing unreliable (**R-0088**) — deterministic degraded fallback required (T-009).
- **R2**: Phase latency/token cost — default-off gate essential (T-001).
- **R3**: Rework oscillation — `CROSS_MODEL_REWORK_MAX` + decision gate (T-007).
- **R4**: Anti-slop subjectivity — lib checklist rubric enforces floor (T-003).
- **R5**: Jury dedup drift — stable `issue_key` algorithm (T-003).
- **R6**: **US-0108** aggregate coupling — frozen `min(lens_scores)`.

### Evidence refs

- `decisions/DEC-0104.md`
- `docs/engineering/architecture.md` (**`# US-0104`**)
- `docs/engineering/research.md` (**`R-0092`**)
- `docs/product/backlog.md` (`## US-0104` — `architecture_notes` appended)
- `handoffs/resume_brief.md` (top pointer → `/sprint-plan`)
- Prior research proof: `tl-US0104-research-20260628T220000Z-fresh`

### Next

- **`/sprint-plan`** (fresh **tech-lead** context) for **`US-0104`** — materialize sprint from 11 architecture seeds; AC-1..AC-8 bijection check.

### Decision gate

- **None** — architecture satisfied; sprint-plan readiness explicit.

---

## Orchestrated research handoff — US-0104 / auto-20260628-04

### Target

- `story_id=US-0104`
- `orchestrator_run_id=auto-20260628-04`
- phase completed: **`research`** (**`tech-lead`**)
- `fresh_context_marker=tl-US0104-research-20260628T220000Z-fresh`
- `next_scheduled_phase=architecture`
- `decomposition=single_story` (sovereign-loop batch per intake-sovereign-20260627-01.json)
- `priority=P1`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=7`

### Summary

- **`/research`** **PASS** — **`R-0092`** Q1–Q7 closed; **`DEC-0104`** locked; architecture-ready on default-off cross-model adversarial critic: three-lens parallel jury, `ik_<sha16>` reconciliation, tier-opposition `select_critic_model`, anti-slop `min(lens_scores)` + bounded rework, degraded single-model-multi-lens fallback, additive `model_id` on **US-0048** isolation evidence. Populates **`handoffs/sovereign_critic_findings.jsonl`** for **US-0110** conjunct 3; sets **`cross_model_reviewed=true`** on **US-0103** ledger when enabled.
- Research stub **`scripts/sovereign_critic_lib.py`** self-test **`[SOVEREIGN_CRITIC_SELF_TEST_OK]`**; full spawn orchestration deferred to execute.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Research locks (architecture inputs)

| Lock | Decision |
|------|----------|
| **Binding decision** | **`DEC-0104`** — composes **US-0048** / **US-0069** / **US-0023** / **US-0110** / **US-0103** (read-only / additive only) |
| **Scratchpad keys** | `CROSS_MODEL_REVIEW=0\|1` (default `0`); `CROSS_MODEL_ANTISLOP_THRESHOLD` default `6`; `CROSS_MODEL_REWORK_MAX` default `2` |
| **Findings schema** | `handoffs/sovereign_critic_findings.jsonl` v1 — 15 required fields; optional `issue_key`, `single_finder`, `rework_generation` |
| **Lenses** | `challenger` \| `architect` \| `subtractor` — all three per invocation |
| **Reconciliation** | `compute_issue_key` → SHA-256 prefix; ≥2 lenses agree → `confidence=high` |
| **Model selection** | Tier opposition via **`model_tier_lib`**; same slug → `CROSS_MODEL_DEGRADED_MODE` |
| **Anti-slop** | 4-item checklist per lens; aggregate `min(lens_scores)`; rework cap → decision gate |
| **Isolation v2** | Additive `model_id` on **US-0048** evidence when critic enabled |
| **Contract tests** | Eight `test_us0104_*` + compose guards `test_us0104_us0048_compose_no_base_schema_change`, `test_us0104_us0110_critic_path_unchanged` |
| **Parity scope** | `check_intake_template_parity.py --scope=sovereign-critic` (**`SOVEREIGN_CRITIC_PAIRS`**, 5 pairs) |

### Top risks (carry to /architecture)

- **R1**: Cursor subagent model routing unreliable (**R-0088**) — deterministic degraded fallback required.
- **R2**: Phase latency/token cost — default-off gate essential.
- **R3**: Rework oscillation — `CROSS_MODEL_REWORK_MAX` + decision gate.
- **R4**: Anti-slop subjectivity — lib checklist rubric enforces floor.
- **R5**: Jury dedup drift — stable `issue_key` algorithm.
- **R6**: **US-0108** aggregate coupling — frozen `min(lens_scores)`.

### Evidence refs

- `decisions/DEC-0104.md`
- `docs/engineering/research.md` (**`R-0092`** — delivered)
- `scripts/sovereign_critic_lib.py` (research stub)
- `docs/product/backlog.md` (`## US-0104` — `research_notes` appended)
- `handoffs/resume_brief.md` (top pointer → `/architecture`)
- `handoffs/intake_evidence/intake-sovereign-20260627-01.json`
- Prior discovery proof: `po-US0104-discovery-20260628T213500Z-fresh`

### Next

- **`/architecture`** (fresh **tech-lead** context) for **`US-0104`** — author **`# US-0104`**, atomic task seeds, eight `test_us0104_*` literals, runbook operator recipes.

### Decision gate

- **None** — research satisfied; architecture readiness explicit.

---

