# US-0120 Discovery Locks (D1–D12)

## D1: Phase ownership
**LOCKED**: `/closure` phase is owned by the **qe** role (QA engineer). Fresh qe subagent per BUG-0006. When `qe` unavailable, fallback to `curator`. New scratchpad key: `AUTO_ROLE_CLOSURE` (default empty = `qe` fallback).

## D2: Phase ordering
**LOCKED**: `/closure` executes **after** `/release` PASS (release artifacts written, queue updated), **before** `/refresh-context`. Updated lifecycle structure:
- **Standard**: `... → execute → qa → verify-work → release → closure → refresh-context`
- **Ultra-lean**: `release → closure → refresh-context` (ship macro becomes 3 phases)
- **Mega-quick**: `release → closure → refresh-context` (ship macro becomes 3 phases)

## D3: Input prerequisites
**LOCKED**: `/closure` requires:
1. Release queue row status=`released` (source: `handoffs/release_queue.md`)
2. `handoffs/releases/Sxxxx-release-notes.md` exists with PASS verdict
3. `sprints/Sxxxx/qa-findings.md` exists

**Fail-gate**: `CLOSURE_RELEASE_EVIDENCE_MISSING` when prerequisites absent. Remediation: complete `/release` first.

## D4: Output artifacts
**LOCKED**: `/closure` produces (all mandatory):
1. `docs/product/backlog.md` target story status `OPEN` → `DONE`
2. `docs/product/acceptance.md` target checkbox `[ ]` → `[x]`
3. `docs/engineering/state.md` closure checkpoint (phase_id=closure, isolation evidence)
4. `sprints/Sxxxx/closure-verification.md` NEW artifact documenting closure execution (story_id, closure_date, closure_role, pre_closure_status, post_closure_status, release_evidence_refs, isolation_evidence, runtime_proof)

## D5: Compose with US-0043 (backlog reconciliation contract)
**LOCKED**: `/closure` is the **executor** of backlog reconciliation that US-0043 defines. US-0043 contract UNCHANGED; closure implements it as a dedicated phase. Evidence precedence: release queue → release notes → qa-findings → uat → release-findings.

## D6: Compose with US-0045 (canonical status source authority)
**LOCKED**: `/closure` follows US-0045 ownership:
- `backlog.md` is **canonical status owner** (mutated first)
- `acceptance.md` and `state.md` are **derived views** (mutated second, atomically)

Updates all three atomically. Canonical status conflict → `CANONICAL_STATUS_CONFLICT` fail-gate.

## D7: Compose with US-0040 (release artifacts)
**LOCKED**: `/closure` operates **after** release artifacts are written. Release writes release notes + queue; closure writes status/acceptance. **No overlap**. Closure requires release evidence refs (D3) as input.

## D8: Compose with US-0048 (isolation evidence, per-phase)
**LOCKED**: `/closure` produces its own isolation evidence entry in `state.md`:
- phase_id=closure
- role=qe
- fresh_context_marker (per spawn)
- timestamp (ISO UTC)
- evidence_ref=closure-verification.md path

Fresh qe subagent per BUG-0006. Orchestrator can verify closure materialization by reading state.md post-closure.

## D9: Compose with US-0056 (strict runtime proof, per-phase)
**LOCKED**: `/closure` produces its own strict runtime proof tuple:
- runtime_proof_id (per spawn)
- phase_id=closure
- role=qe
- story_id
- sprint_id
- proof_hash (SHA-256 of sorted-key JSON payload)
- proof_ttl=3600s

Per DEC-0038 contract. Proof payload includes closure-specific fields.

## D10: release.md step 10–12 removal
**LOCKED**: After US-0120 ships:
- `.cursor/commands/release.md` steps 10–12 **must be removed**
- Replace with pointer: "Backlog reconciliation is now handled by the dedicated `/closure` phase — see `.cursor/commands/closure.md`"
- Active + `template/` mirror byte-identical
- Release subagent focuses on release artifacts only (gate chain, queue, notes, finalization, legacy, publish targets, connectivity, operator hints, version changelog)

## D11: Template parity
**LOCKED**: New `.cursor/commands/closure.md` must be **byte-identical** to `template/.cursor/commands/closure.md` (active ↔ template mirror). Checked by `check_intake_template_parity.py`.

## D12: Orchestrator post-closure verification
**LOCKED**: After `/closure` returns, orchestrator runs direct `rg` verification:
1. `rg "^- Status: DONE$" docs/product/backlog.md` (target story block)
2. `rg "^\*- \[x\] US-xxxx:" docs/product/acceptance.md` (target row)

If either **FAIL** → escalate to operator with `CLOSURE_VERIFICATION_FAILED`. No auto-repair (fidelity must be enforced at phase boundary).
