# PO to TL archive pack (2026-06-28)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=650, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 2
- Retained units in hot file: 10
- First archived heading: `## Orchestrated architecture handoff — US-0105 / auto-20260628-04`
- Last archived heading: `## Orchestrated research handoff — US-0105 / auto-20260628-04`
- Verification tuple (mandatory):
  - archived_body_lines=124
  - retained_body_lines=635

---

## Orchestrated architecture handoff — US-0105 / auto-20260628-04

### Target

- `story_id=US-0105`
- `orchestrator_run_id=auto-20260628-04`
- phase completed: **`architecture`** (**`tech-lead`**)
- `fresh_context_marker=tl-US0105-architecture-20260629T000700Z-fresh`
- `next_scheduled_phase=sprint-plan`
- `decomposition=single_story` (per **US-0051**)
- `priority=P1`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=6`

### Summary

- **`/architecture`** **PASS** — **`DEC-0105`** locked; **`# US-0105`** appended; 11 atomic task seeds; eight **`test_us0105_*`** contract markers + compose guards **`test_us0105_us0029_*`**, **`test_us0105_us0080_*`**; **`SOVEREIGN_MEMORY_PAIRS`** parity manifest.
- **Default-off gate**: **`SOVEREIGN_MEMORY=0|1`** (default **`0`**); injection via top-N recent + top-K high-impact; char cap **`SOVEREIGN_MEMORY_MAX_CHARS`**.
- **Bootstrap**: create-on-first-write JSONL; **`.gitkeep`** only until first append.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Architecture locks (sprint-plan inputs)

| Lock | Decision |
|------|----------|
| **Binding decision** | **`DEC-0105`** — composes **US-0029** / **US-0080** / **US-0103** / **US-0072** / **US-0096** |
| **Tranche order** | A scratchpad+dir → B lib read/injection → C append/validator → D spawn+hooks → E tests+parity |
| **Task seeds** | 11 seeds (under **`SPRINT_MAX_TASKS=12`** threshold) |
| **JSONL families** | Four v1 schemas + `status` enum + secret scan + **`sovereign_memory_validate.py`** |
| **Injection** | Top-N global recent + top-K high-impact; tail read bound **500** lines/file |
| **Rollover** | **`SOVEREIGN_MEMORY_JSONL_MAX_LINES=500`** → `sovereign-memory-archive/` — **not** triad |
| **Contract tests** | **`test_us0105_scratchpad_keys_literals`**, **`test_us0105_sovereign_memory_directory_contract`**, **`test_us0105_jsonl_schema_contract`**, **`test_us0105_injection_digest_char_cap`**, **`test_us0105_decision_dedup_branch`**, **`test_us0105_mistake_tagging_literals`**, **`test_us0105_zero_overhead_default`**, **`test_us0105_compose_guards`** |
| **Parity scope** | **`check_intake_template_parity.py --scope=sovereign-memory`** (**`SOVEREIGN_MEMORY_PAIRS`**) |

### Top risks (carry to /sprint-plan)

- **R1**: Token bloat — char cap + tail read + lib-side digest mandatory.
- **R2**: Research vs learnings semantic overlap — provenance refs only.
- **R3**: Ledger vs decisions-log operator confusion — distinct schemas + runbook.
- **R4**: Stale injection — `status` supersession field on all entries.
- **R5**: Secret leakage — **`SOVEREIGN_MEMORY_SECRET_DETECTED`** on free-text fields.
- **R6**: **US-0107** read API stability — version via `schema_version`.

### Evidence refs

- `decisions/DEC-0105.md`
- `docs/engineering/architecture.md` (**`# US-0105`**)
- `docs/engineering/research.md` (**`R-0093`**)
- `docs/product/backlog.md` (`## US-0105` — `discovery_notes`)
- `scripts/sovereign_memory_lib.py` (research stub + `[SOVEREIGN_MEMORY_SELF_TEST_OK]`)
- Prior research proof: `tl-US0105-research-20260629T000600Z-fresh`

### Next

- **`/sprint-plan`** (fresh **tech-lead** context) for **`US-0105`** — materialize sprint from 11 architecture seeds; AC-1..AC-8 bijection check.

### Decision gate

- **None** — architecture satisfied; sprint-plan readiness explicit.

---

## Orchestrated research handoff — US-0105 / auto-20260628-04

### Target

- `story_id=US-0105`
- `orchestrator_run_id=auto-20260628-04`
- phase completed: **`research`** (**`tech-lead`**)
- `fresh_context_marker=tl-US0105-research-20260629T000600Z-fresh`
- `next_scheduled_phase=architecture`
- `decomposition=single_story` (per **US-0051**)
- `priority=P1`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=6`

### Summary

- **`/research`** **PASS** — **`R-0093`** Q1–Q7 closed; architecture-ready locks on JSONL v1 schemas, **`sovereign_memory_lib.py`** API, injection merge algorithm, mistake-tagging wiring, JSONL rollover vs **US-0072**, contract-test inventory, and companion **`DEC-0105`** recommendation.
- **Bootstrap**: create-on-first-write JSONL; directory **`.gitkeep`** only until first append.
- **Injection**: global top-N recent + top-K high-impact from `patterns`/`mistakes`; char cap **`SOVEREIGN_MEMORY_MAX_CHARS`**; zero overhead when **`SOVEREIGN_MEMORY=0`**.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Research locks (architecture inputs)

| Lock | Decision |
|------|----------|
| **Binding decision** | **`DEC-0105`** (to author) — composes **US-0029** / **US-0080** / **US-0103** / **US-0072** / **US-0096** |
| **JSONL schemas** | Four v1 families + shared base; `status` enum; secret scan; **`sovereign_memory_validate.py`** CLI |
| **Lib API** | **`scripts/sovereign_memory_lib.py`** — injection, append, dedup, promote, retrospective, rollover hooks |
| **Injection** | Top-N global recent (`ts` desc) + top-K high-impact (`impact_score` desc); tail read bound **500** lines/file |
| **Mistake hooks** | `fix_failed`, `revert_applied`, `plan_fidelity_violation` (+ optional `test_regression`, `scope_creep`) |
| **Rollover** | **`SOVEREIGN_MEMORY_JSONL_MAX_LINES=500`** → `sovereign-memory-archive/` — **not** triad |
| **Contract tests** | Eight **`test_us0105_*`** + compose guards **`test_us0105_us0029_*`**, **`test_us0105_us0080_*`** |
| **Parity scope** | **`check_intake_template_parity.py --scope=sovereign-memory`** (**`SOVEREIGN_MEMORY_PAIRS`**) |

### Top risks (carry to /architecture)

- **R1**: Token bloat — char cap + tail read + lib-side digest mandatory.
- **R2**: Research vs learnings semantic overlap — provenance refs only.
- **R3**: Ledger vs decisions-log operator confusion — distinct schemas + runbook.
- **R4**: Stale injection — `status` supersession field on all entries.
- **R5**: Secret leakage — **`SOVEREIGN_MEMORY_SECRET_DETECTED`** on free-text fields.
- **R6**: **US-0107** read API stability — version via `schema_version`.

### Evidence refs

- `docs/engineering/research.md` (**`R-0093`** — research extension)
- `scripts/sovereign_memory_lib.py` (research stub + `[SOVEREIGN_MEMORY_SELF_TEST_OK]`)
- `docs/product/backlog.md` (`## US-0105` — `discovery_notes`)
- `handoffs/archive/po-to-tl-pack-20260628-f.md` (discovery handoff)
- `handoffs/intake_evidence/intake-sovereign-20260627-01.json`
- Prior discovery proof: `po-US0105-discovery-20260629T000500Z-fresh`

### Next

- **`/architecture`** (fresh **tech-lead** context) for **`US-0105`** — author **`# US-0105`**, companion **`DEC-0105`**, atomic task seeds, **`test_us0105_*`** literals, runbook operator recipes.

### Decision gate

- **None** — research satisfied; architecture readiness explicit.

---

