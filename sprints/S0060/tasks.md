# Sprint S0060 Tasks

- **Bug**: `BUG-0001`
- **Sprint**: `S0060`
- **Governance**: **`DEC-0063`**; **`architecture.md`** **`# BUG-0001`**; **`R-0058`**; **`US-0045`** (bug **`DONE`** post verify-work **`2026-03-30`**); **`US-0018`** / **`US-0030`**

| Task | Status | Description | AC |
|---|---|---|---|
| T-001 | done | Add **`template/scripts/`** copies of **`intake_evidence_validate.py`**, **`intake_evidence_lib.py`**, **`intake_bug_routing_guard.py`** matching repo **`scripts/`** (same PR / documented normalization if any) | AC-1 |
| T-002 | done | Reconcile **`package.json` `files`** with **`DEC-0063`** §2 — ensure **`template/`** delivery covers the trio; add optional explicit **`scripts/intake_*.py`** entries only with enforced lockstep parity | AC-2 |
| T-003 | done | Implement deterministic parity gate (fixture or script + test) for **`scripts/`** ↔ **`template/scripts/`** intake trio; register in **`tests/run-tests.ps1`** / **`tests/run-tests.sh`** as sprint defines | AC-3 |
| T-004 | done | Align **`US-0018`** framework file classification / upgrade paths so new or updated intake modules reach upgraded consumer repos; capture evidence for fresh + upgrade scenarios | AC-4 |
| T-005 | done | Update **`README.md`** and/or **`docs/engineering/runbook.md`** (and **`template/`** mirrors if required) for install layout + intake script location; confirm packaging paths (npm/Choco/Brew) still hydrate from **`template/`** | AC-5 |

## Deterministic AC-to-task mapping

- AC-1 → T-001
- AC-2 → T-002
- AC-3 → T-003
- AC-4 → T-004
- AC-5 → T-005

## Portfolio acceptance

- **`docs/product/acceptance.md`** **`BUG-0001`** checkbox **checked** after **`/verify-work`** (**2026-03-30**) per **`US-0045`** / **`DEC-0061`** §8.
