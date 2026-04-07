# Sprint S0071 Tasks

- **Story**: **`US-0087`**
- **Sprint**: **`S0071`**
- **Governance**: `architecture.md` `# US-0087`; `research.md` `R-0070`; `US-0045`

| Task | Status | Description | AC |
|---|---|---|---|
| T-001 | done | Lock **`/auto`** argv literals **`bug-target=BUG-####`** and **`bug-target=all-open`** in **`.cursor/commands/auto.md`** and **`template/`** mirror; document deterministic fail-closed codes (**`AUTO_BUG_QUEUE_EMPTY`**, **`AUTO_BUG_TARGET_UNKNOWN`**, **`AUTO_BUG_TARGET_NOT_OPEN`**) per **`# US-0087`** | AC-1 |
| T-002 | done | Add **`AUTO_BUG_QUEUE`**, **`AUTO_BUG_TARGET`**, **`AUTO_BUG_MAX_ITEMS`**, **`AUTO_BUG_ON_BLOCK`** to **`.cursor/scratchpad.md`** and **`template/.cursor/scratchpad.local.example.md`** with **default-off** semantics | AC-2 |
| T-003 | done | Update **`docs/engineering/auto-orchestration-reference.md`** + active/template **`auto.md`**: bug-target argv precedence vs scratchpad; **`AUTO_SCHEDULER_CONFLICT`** when **`AUTO_BACKLOG_DRAIN=1`** ∧ **`AUTO_BUG_QUEUE=1`** without argv resolution; argv bug-target selects bug scheduler for the run | AC-3 |
| T-004 | done | Document **OPEN**-only queue, **numeric** **`BUG-####`** sort, **`AUTO_BUG_MAX_ITEMS`** cap, and empty-queue fail-closed behavior in normative reference + command; add/extend **contract test** rows as needed | AC-4 |
| T-005 | done | Specify **`resume_brief.md`** + **`state.md`** fields for bug segments (**`bug_id`**, **`bug_queue_position`**, **`bug_queue_remaining`**, **AC-10** tuple) aligned with **`DEC-0069`** (paired refresh at segment boundaries) | AC-5 |
| T-006 | done | Reinforce **spawn-only** orchestrator model for bug-queue mode in **`auto.md`** / **`auto-orchestration-reference.md`** — cross-ref **`BUG-0006`** / **`US-0069`** / **`AUTO_ORCHESTRATOR_PHASE_EXECUTION`** | AC-6 |
| T-007 | done | Extend **`tests/auto_command_contract_test.py`** (and fixtures) for **`bug-target=`** markers, **`AUTO_SCHEDULER_CONFLICT`**, and **template** path parity expectations | AC-7 |
| T-008 | done | Reconcile implementation with **`docs/engineering/architecture.md`** **`# US-0087`** (reason codes, **`AUTO_BUG_*`** names, mutex matrix); fix any drift after doc/test edits | AC-8 |
| T-009 | done | Add **`docs/engineering/runbook.md`** operator subsection **“targeted bug auto drain”** (scratchpad + argv recipe, fail-closed codes, pointer to reference) | AC-9 |
| T-010 | done | **`template/`** byte/literal parity pass for every path touched in **T-001..T-009** (**`auto.md`**, reference, scratchpad examples) — match active repo | AC-10 |

## Deterministic AC-to-task mapping

- AC-1 -> T-001
- AC-2 -> T-002
- AC-3 -> T-003
- AC-4 -> T-004
- AC-5 -> T-005
- AC-6 -> T-006
- AC-7 -> T-007
- AC-8 -> T-008
- AC-9 -> T-009
- AC-10 -> T-010
