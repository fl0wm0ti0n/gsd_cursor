# PO to TL archive pack (2026-06-28)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=650, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 10
- First archived heading: `## Orchestrated discovery handoff — US-0105 / auto-20260628-04`
- Last archived heading: `## Orchestrated discovery handoff — US-0105 / auto-20260628-04`
- Verification tuple (mandatory):
  - archived_body_lines=84
  - retained_body_lines=635

---

## Orchestrated discovery handoff — US-0105 / auto-20260628-04

### Target

- `story_id=US-0105`
- `orchestrator_run_id=auto-20260628-04`
- phase completed: **`discovery`** (**`po`**)
- `fresh_context_marker=po-US0105-discovery-20260629T000500Z-fresh`
- `next_scheduled_phase=research`
- `decomposition=single_story` (sovereign-loop batch per intake-sovereign-20260627-01.json)
- `priority=P1`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=6`

### Summary

- **`/discovery`** **PASS** — project-level institutional memory locked: default-off **`SOVEREIGN_MEMORY`** gate; **`docs/engineering/sovereign-memory/`** with four JSONL artifacts + sprint retrospectives; bounded injection (**top-N recent + top-K high-impact + char cap**) via **`sovereign_memory_lib.py`**; curator retrospective after release; dedup on **`decisions-log.jsonl`**; mistake-tagging on failed fix/revert. **Compose do NOT amend** **US-0029** / **US-0080** — external research vs internal learnings remain separate; injection honors **DEC-0062** without changing slim-command contracts. **US-0103** ledger remains per-run audit; **`decisions-log.jsonl`** is distilled cross-run learnings.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Discovery locks (research inputs)

| Lock | Decision |
|------|----------|
| **Scratchpad keys** | `SOVEREIGN_MEMORY=0\|1` (default `0`); `SOVEREIGN_MEMORY_TOP_N` default `5`; `SOVEREIGN_MEMORY_TOP_K` default `3`; `SOVEREIGN_MEMORY_MAX_CHARS` default `2048` |
| **Directory** | `docs/engineering/sovereign-memory/` — `decisions-log.jsonl`, `mistakes.jsonl`, `patterns.jsonl`, `plan-drift-register.jsonl`, `retrospectives/<sprint_id>.md` |
| **Design intent** | **decisions-log** = distilled cross-run decisions (dedup); **mistakes** = anti-patterns; **patterns** = reusable positives; **plan-drift-register** = plan-vs-execution drift; **retrospectives** = curator human-readable sprint summary |
| **Injection** | `build_injection_digest()` — top-N recent + top-K high-impact; dedupe `entry_id`; truncate to char cap; names-only digest |
| **Spawn hook** | Read-only **`sovereign_memory_digest`** block when enabled — additive to **US-0023**, not a new phase role |
| **Curator write** | **`/refresh-context`** after release → `retrospectives/<sprint_id>.md`; optional ledger promotion when `AI_DECISION_LEDGER=1` |
| **Dedup / mistakes** | `decision_key` SHA prefix dedup; mistake tags on `FIX_FAILED` / `REVERT_APPLIED` / fidelity violations |
| **US-0029 compose** | **`research.md`** / `/research` unchanged — internal learnings only; may cite `R-xxxx` as provenance |
| **US-0080 compose** | Server-side digest truncation; no **`TOKEN_PROFILE`** or hot-surface contract changes |
| **US-0103 compose** | 12-field ledger unchanged; optional `promote_from_ledger()` at refresh-context |
| **Growth policy** | JSONL rollover to `sovereign-memory-archive/` — not a triad hot surface (**US-0072**) |

### Acceptance pointers (discovery emphasis)

- **AC-1**: Scratchpad keys + zero-overhead default.
- **AC-2**: Five artifact families + template mirror + v1 schemas.
- **AC-3**: `sovereign_memory_lib.py` bounded injection API.
- **AC-4**: Phase spawn digest integration (US-0023-safe).
- **AC-5**: Curator retrospective + optional ledger promotion.
- **AC-6**: Dedup + mistake-tagging hooks.
- **AC-7**: Eight `test_us0105_*` markers + `--scope=sovereign-memory` parity.
- **AC-8**: Architecture, runbook, compose guards for US-0029/US-0080.

### Top risks (carry to /research)

- **R1**: Token bloat — char cap + lib-side digest mandatory.
- **R2**: Research vs learnings semantic overlap — strict artifact boundary.
- **R3**: Ledger vs decisions-log operator confusion — distinct schemas + docs.
- **R4**: Stale injection — impact_score decay or status field.
- **R5**: Secret leakage in free-text fields.
- **R6**: US-0107 read API coupling — stable lib surface.

### Research asks (new **`R-0093`**)

1. JSONL v1 exact schemas + validator CLI per artifact family.
2. Full `sovereign_memory_lib.py` API + `self_test`.
3. Injection merge algorithm edge cases (ties, empty corpus).
4. Mistake-tagging orchestrator wiring + US-0103 fidelity compose.
5. JSONL rollover/archive line caps vs US-0072.
6. Contract-test inventory + `SOVEREIGN_MEMORY_PAIRS` parity manifest.
7. Companion DEC necessity.

### Evidence refs

- `docs/product/backlog.md` (`## US-0105` — `discovery_notes` with L1–L12 + design-intent table)
- `docs/product/vision.md` (**Discovery Notes — US-0105**)
- `docs/product/acceptance.md` (`US-0105` row — unchecked)
- `docs/engineering/research.md` (**`R-0093`** — discovery stub)
- `handoffs/intake_evidence/intake-sovereign-20260627-01.json`
- Adjacent: **US-0029**, **US-0080**, **DEC-0062**, **US-0103**, **DEC-0103**, **US-0096**, **DEC-0082**, **US-0072**, **US-0107**, **US-0110**

### Next

- **`/research`** (fresh **tech-lead** context) for **`US-0105`** — close **`R-0093`** Q1–Q7; JSONL schemas + helper lib + injection algorithm + contract tests inventory before **`/architecture`**.

### Decision gate

- **None** — discovery satisfied; research readiness explicit.

---

