# Plan-area mapping (US-0081 / DEC-0064)

This index canonicalizes `plan_area_id` → `story_ids` for first-intake and research artifacts.

| `plan_area_id` | Maps to | Title |
|----------------|---------|-------|
| `decision-ledger-jsonl-schema` | **US-0103** | Append-only JSONL schema v1 per orchestrator run |
| `ledger-helper-library` | **US-0103** | `scripts/decision_ledger_lib.py` ledger operations |
| `ledger-validator-cli` | **US-0103** | `scripts/ledger_validate.py` JSONL schema validator |
| `plan-fidelity-deviation-table` | **US-0103** | strict/relaxed/extended deviation classifier |
| `qa-ledger-cross-check` | **US-0103** | QA `ledger_findings` emission contract |
| `ledger-contract-test-inventory` | **US-0103** | Eight `test_us0103_*` markers |
| `ledger-reason-code-inventory` | **US-0103** | `PLAN_FIDELITY_*` (5) + `LEDGER_*` (6) |
| `sovereign-loop-foundation` | **US-0103..US-0110** | Umbrella sovereign-loop foundation layer |

`coverage_complete=true` (for US-0103 research phase).
