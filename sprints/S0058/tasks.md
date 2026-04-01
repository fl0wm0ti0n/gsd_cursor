# Sprint S0058 Tasks



- Story: `US-0079`

- Sprint: `S0058`

- Governance: **`DEC-0061`**; **`architecture.md`** **`# US-0079`**; **`R-0056`** (Tier A–D ↔ AC-8); **`US-0045`** / **`US-0030`** parity



| Task | Status | Description | AC |

|---|---|---|---|

| T-001 | done | Implement **`BUG-####`** identity + allocator (next id after highest existing) and canonical **`## Bug issues (canonical)`** region in **`docs/product/backlog.md`** (append-new, stable sort by id) per **`DEC-0061`** §§1–2 | AC-1 |

| T-002 | done | Wire intake **bug routing**: merged scratchpad **`INTAKE_WORK_ITEM_KIND=bug`** and/or documented **`/intake bug`**; fail closed with **`INTAKE_BUG_ROUTING_REQUIRED`** / mismatch family when defect prose lacks signals — **no** silent **`US-xxxx`** allocation (**`DEC-0061`** §5) | AC-2 |

| T-003 | done | Enforce bug status literals **`OPEN`/`DONE`** only in validators and docs; reject illegal states (**`DEC-0061`** §3) | AC-3 |

| T-004 | done | Implement minimum bug schema validation (**environment**, **steps_to_reproduce**, **expected**, **actual**, **evidence_refs** non-empty) + stable **`BUG_VALIDATION_*`** reason codes in runbook; optional link fields per **`DEC-0061`** §4 | AC-4 |

| T-005 | done | Extend sprint templates / **`tasks.md`** conventions so tasks may reference **`BUG-xxxx`** in titles or traceability rows without US conversion (**`DEC-0061`** §7) | AC-5 |

| T-006 | done | Align **`qa-findings`**, **`uat.*`**, **`release-findings`** patterns and examples for **`BUG-xxxx`** alongside **`US-xxxx`** (**US-0042**-style evidence rows) | AC-6 |

| T-007 | done | Extend **`US-0045`** reconciliation tooling: detect **`BUG-`** drift vs **`## Bug acceptance (canonical)`** in **`acceptance.md`**; preserve existing US-only behavior | AC-7 |

| T-008 | done | Extend **`/ask`** + context-pack narrow-read allowlists / regex families for **`BUG-####`** (**`DEC-0061`** §9) | AC-8 |

| T-009 | done | **Active/template parity**: intake commands, core rules, runbook, README, **`template/`** for bug workflow literals and routing (**`US-0030`**) | AC-9 |

| T-010 | done | **AC-10 closure**: ensure **`docs/engineering/decisions.md`** index, operator surfaces, and sprint artifacts explicitly cite **`DEC-0061`** + **`architecture.md`** **`# US-0079`** + migration/grandfather (**`DEC-0061`** §11) | AC-10 |



## Deterministic AC-to-task mapping



- AC-1 → T-001

- AC-2 → T-002

- AC-3 → T-003

- AC-4 → T-004

- AC-5 → T-005

- AC-6 → T-006

- AC-7 → T-007

- AC-8 → T-008

- AC-9 → T-009

- AC-10 → T-010

