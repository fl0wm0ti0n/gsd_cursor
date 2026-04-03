# Sprint S0067

- **Bug**: `BUG-0006`
- **Goal**: Enforce **spawn-only** **`/auto`** process contract (**US-0080**): orchestrator must **not** execute lifecycle phase work or write phase deliverables in orchestrator context; document **`AUTO_ORCHESTRATOR_PHASE_EXECUTION`** alongside existing **`PHASE_CONTEXT_ISOLATION_*`** / **`RUNTIME_PROOF_*`** families; extend static regression per **`R-0065`** / **`docs/engineering/architecture.md`** **`# BUG-0006`**.
- **Status**: **Verify-work PASS** (`2026-04-04T08:30:00Z`, **qa**) — canonical **`BUG-0006`** **DONE** (**US-0045**); UAT **5/5**; **`handoffs/release_queue.md`** **`S0067`** **`ready`**; next **`/release`** (**release**).

## Scope (sprint-local AC themes)

- **AC-1** - **Active command**: **`.cursor/commands/auto.md`** — non-negotiable spawn-only language; explicit forbid orchestrator phase execution / phase deliverable authorship; **`AUTO_ORCHESTRATOR_PHASE_EXECUTION`** in fail-fast / reason-code excerpt with operator remediation (phase→role matrix).
- **AC-2** - **Template parity**: **`template/.cursor/commands/auto.md`** mirrors active **`auto.md`** contract literals and spawn-only obligations (same change set as architecture).
- **AC-3** - **Reference contract**: **`docs/engineering/auto-orchestration-reference.md`** — spawn-only rule aligned with command; cross-link **DEC-0029** (isolation) and **DEC-0038** (strict proof); document **`AUTO_ORCHESTRATOR_PHASE_EXECUTION`** one-line remediation.
- **AC-4** - **Regression tests**: extend **`tests/auto_command_contract_test.py`** — required substrings (spawn phrasing, forbidden in-orchestrator execution), literal **`AUTO_ORCHESTRATOR_PHASE_EXECUTION`**, negative / non-contradiction check vs implied in-process **`architecture`** / **`execute`** / named phases (**R-0065** matrix rows 1–4).
- **AC-5** - **Harness traceability**: confirm **`tests/run-tests.sh`** and **`tests/run-tests.ps1`** still invoke **`tests/auto_command_contract_test.py`** after edits (section paths unchanged or updated deterministically).

## Governance

- `docs/engineering/architecture.md` `# BUG-0006`
- `docs/engineering/research.md` `R-0065`
- Related: `US-0048`, `US-0069`, `US-0080`, `US-0045`, `DEC-0029`, `DEC-0038`, `DEC-0051`, `DEC-0052`
