# Sprint S0120 — Discovery (US-0120)

**story_id**: US-0120
**sprint_id**: S0120
**phase_id**: discovery
**role**: po
**orchestrator_run_id**: auto-20260706-01
**delivery_mode**: ultra_lean
**macro_phase**: spec (intake+discovery merged)
**fresh_context_marker**: po-US0120-discovery-20260706T221400Z-fresh
**timestamp (UTC)**: 2026-07-06T22:14:00Z

---

## Story summary

US-0120 extracts Story Closure (status DONE + acceptance checkbox + state checkpoint) from `/release` step 10–12 into a dedicated `/closure` phase with exclusive responsibility. Motivation: during US-0119, the release subagent claimed closure but did not materialize file changes — the same fidelity gap observed in the 5-cycle execute loop. By giving closure its own phase, the orchestrator can verify it directly and the release subagent can focus on release artifacts only.

---

## Discovery locks D1..D12

**D1 (phase ownership)** — `/closure` is owned by role `qe` (per DEC-0052 phase→role matrix). Fallback: `curator` when `qe` is unavailable. New scratchpad key `AUTO_ROLE_CLOSURE` (default empty = `qe` fallback).

**D2 (phase ordering — ultra_lean ship macro)** — New ship macro: `release → closure → refresh-context` (3 phases, not 2). `/closure` always executes AFTER `/release` PASS (release queue row `released`, release notes written) and BEFORE `/refresh-context`.

**D3 (input prerequisites)** — `/closure` requires: (a) `handoffs/release_queue.md` target sprint row `status=released`, (b) `handoffs/releases/Sxxxx-release-notes.md` exists with gate summary, (c) `sprints/Sxxxx/qa-findings.md` exists and verdict≠FAIL. Missing evidence → block with `CLOSURE_RELEASE_EVIDENCE_MISSING`.

**D4 (output artifacts — 4 mandatory)** — (a) `docs/product/backlog.md` target story `Status: OPEN` → `Status: DONE`, (b) `docs/product/acceptance.md` target checkbox `- [ ]` → `- [x]`, (c) `docs/engineering/state.md` closure checkpoint appended, (d) `sprints/Sxxxx/closure-verification.json` NEW artifact with schema: `story_id`, `closure_date` (ISO UTC), `closure_role`, `pre_closure_status=OPEN`, `post_closure_status=DONE`, `release_evidence_refs[]`, `isolation_evidence{}`, `runtime_proof{}`.

**D5 (compose with US-0043)** — `/closure` is the executor of backlog reconciliation that US-0043 contractually defines. US-0043 contract unchanged; closure implements it as dedicated phase.

**D6 (compose with US-0045)** — `/closure` follows US-0045 canonical status ownership rules: `backlog.md` is canonical owner, `acceptance.md` and `state.md` are derived views. Closure mutates all three — backlog first, acceptance + state derived.

**D7 (compose with US-0040)** — `/closure` operates AFTER release artifacts are written (release queue row, sprint-scoped notes). Closure is the downstream consumer of release evidence.

**D8 (compose with US-0048 isolation evidence)** — `/closure` produces its own isolation evidence appended to `docs/engineering/state.md`: `phase_id=closure`, `role=qe`, `fresh_context_marker=<per-spawn>`, `timestamp`, `evidence_ref=closure-verification.json`. Fresh qe subagent per BUG-0006 / US-0048 isolation.

**D9 (compose with US-0056 strict runtime proof)** — `/closure` emits strict runtime proof: `runtime_proof_id`, `phase_id=closure`, `role=qe`, `story_id`, `sprint_id`, sorted-key JSON payload, SHA-256 proof_hash, proof_ttl=3600s.

**D10 (release.md step 10–12 removal)** — After US-0120 ships: steps 10–12 (backlog status reconciliation + acceptance checkbox reconciliation + state checkpoint for closure + normalization report) of `.cursor/commands/release.md` (active + template mirror) are replaced with a redirect pointer: "Backlog reconciliation is now handled by the dedicated `/closure` phase — see `.cursor/commands/closure.md`."

**D11 (template parity — closure.md)** — New `.cursor/commands/closure.md` must be byte-identical to `template/.cursor/commands/closure.md` per US-0017. `check_intake_template_parity.py --scope=closure-phase` extends parity checker to cover closure command file. Pairs registered in `AUTONOMY_PRESET_PAIRS` or a new `CLOSURE_PHASE_PAIRS` manifest.

**D12 (orchestrator post-closure verification)** — After `/closure` returns, orchestrator runs direct `rg` verification: (a) `rg "^- Status: DONE$" docs/product/backlog.md` must match US-xxxx, (b) `rg "^\*- \[x\] US-xxxx:" docs/product/acceptance.md` must match. Either FAIL → escalate to operator with `CLOSURE_VERIFICATION_FAILED` and handoff to `/qa` → `/execute` re-cycle or manual closure.

---

## AC → Task surjective coverage (12 ACs → 12 tasks)

| Task | ACs covered | Description |
|------|-------------|-------------|
| T-anch | AC-12 | Compose guards UNCHANGED (verify US-0043/US-0045/US-0040/US-0048/US-0056/US-0096 surfaces via grep) |
| T-001 | AC-1 | `.cursor/commands/closure.md` (active + template) with input gates, output artifacts, schema, fail-codes |
| T-002 | AC-2 | DEC-0052 phase→role update + `.cursor/commands/auto.md` phase matrix closure entry + `AUTO_ROLE_CLOSURE` scratchpad key |
| T-003 | AC-3 | DEC-0082 ship macro 2→3 phases + `scripts/work_kind_routing_lib.py` phase plan arrays + `/auto` resolve_delivery_mode |
| T-004 | AC-4 | `/auto` orchestration wiring (release → closure → refresh-context chain) |
| T-005 | AC-5 | Release.md step 10–12 removal (active + template mirror) |
| T-006 | AC-6 | Closure verification artifact schema + validator `scripts/validate_closure_verification.py` |
| T-007 | AC-7 | Closure isolation evidence pattern documented (no new code — closure command instructs subagent) |
| T-008 | AC-8 | Closure runtime proof pattern documented (no new code — closure command instructs subagent) |
| T-009 | AC-9 | Contract tests `tests/us0120_closure_phase_test.py` (10 markers) |
| T-010 | AC-10 | Backward compatibility for in-flight stories detection logic in `/auto` drain-advance hook |
| T-011 | AC-11 | Documentation (`docs/engineering/architecture.md ## US-0120`, `docs/engineering/runbook.md ## Story closure (US-0120)`, `.cursor/commands/auto.md`, README sub-block if needed) |

---

## Test markers (T-009 — 10 markers)

1. `test_us0120_closure_command_file_exists` — `.cursor/commands/closure.md` active + template both exist
2. `test_us0120_dec_0052_includes_closure` — DEC-0052 phase→role matrix includes `closure`
3. `test_us0120_dec_0082_ship_macro_three_phases` — DEC-0082 ship macro = release → closure → refresh-context
4. `test_us0120_auto_phase_plan_includes_closure` — `/auto` command includes closure after release in phase plan
5. `test_us0120_release_md_step_10_12_removed` — release.md does NOT contain old step 10–12 backup
6. `test_us0120_closure_verification_schema_validator` — `validate_closure_verification.py` validates schema
7. `test_us0120_closure_isolation_evidence_pattern` — closure produces isolation evidence in state.md
8. `test_us0120_closure_runtime_proof_pattern` — closure produces runtime proof
9. `test_us0120_all_delivery_modes_include_closure` — standard/ultra_lean/mega_quick phase plans all include closure
10. `test_us0120_compose_guards_unchanged` — 6 compose surfaces untouched (regex-based on compose-target anchors)

---

## Files to touch

- `.cursor/commands/closure.md` (NEW)
- `template/.cursor/commands/closure.md` (NEW mirror)
- `.cursor/commands/auto.md` (closure phase wiring)
- `template/.cursor/commands/auto.md` (mirror)
- `.cursor/commands/release.md` (step 10–12 replacement with redirect pointer)
- `template/.cursor/commands/release.md` (mirror)
- `.cursor/scratchpad.md` (AUTO_ROLE_CLOSURE key)
- `template/.cursor/scratchpad.local.example.md` (mirror)
- `decisions/DEC-0052.md` (phase→role matrix update)
- `decisions/DEC-0082.md` (ship macro phases)
- `scripts/work_kind_routing_lib.py` (phase plan arrays)
- `scripts/validate_closure_verification.py` (NEW)
- `scripts/check_intake_template_parity.py` (--scope=closure-phase)
- `tests/us0120_closure_phase_test.py` (NEW)
- `sprints/S0120/closure-verification.json` (schema template; actual artifact per-sprint)
- `docs/engineering/architecture.md` (`## US-0120` section — T-anch verification)
- `docs/engineering/runbook.md` (`## Story closure (US-0120)` section)
- `its_magic/README.md` (sub-block if new keys added)
- `template/its_magic/README.md` (mirror)

## Files NOT to touch (compose guards)

- US-0043 surface — backlog reconciliation CONTRACT text (no change)
- US-0045 surface — canonical status source text (no change)
- US-0040 surface — canonical release artifacts text (no change)
- US-0048 surface — isolation evidence text (no change)
- US-0056 surface — strict runtime proof text (no change)
- US-0096 surface — delivery modes text (no change)

---

## Risks (R1..R8)

**R1 (MEDIUM)** — Subagent fidelity again. Even with dedicated `/closure` phase, qe subagent may claim closure without materializing. Mitigation: orchestrator post-closure verification (D12).

**R2 (LOW)** — Release subagent scope confusion during transition (in-flight stories). Mitigation: T-010 detection logic.

**R3 (LOW)** — Template parity drift for closure.md. Mitigation: T-001 (active + template both new; byte-identical by construction).

**R4 (LOW-MEDIUM)** — DEC update scope. DEC-0052 + DEC-0082 must be edited precisely (not rewritten). Mitigation: T-002 + T-003 scoped edits only; no rewrite.

**R5 (LOW)** — Phase plan arrays in work_kind_routing_lib.py. Mitigation: T-003 + T-009 contract test `test_us0120_all_delivery_modes_include_closure`.

**R6 (LOW)** — Compose-guard accidental edit. Mitigation: T-anch + T-009 contract test `test_us0120_compose_guards_unchanged`.

**R7 (LOW)** — Closure verification schema rigidity (future stories may need extensions). Mitigation: schema allows optional fields; validator only checks required fields.

**R8 (LOW)** — Backward compat for already-released S0119. Mitigation: detection logic in T-010 — S0119 already closed (status DONE) so closure is a no-op for it.

---

## Compose, do not amend (verified)

- US-0043 (backlog reconciliation contract): UNCHANGED — closure EXECUTES US-0043, does not amend
- US-0045 (canonical status source): UNCHANGED — closure FOLLOWS US-0045, does not amend
- US-0040 (release artifacts): UNCHANGED — closure operates after US-0040, does not amend
- US-0048 (isolation evidence): UNCHANGED — closure produces own isolation evidence per US-0048
- US-0056 (strict runtime proof): UNCHANGED — closure produces own runtime proof per US-0056
- US-0096 (delivery modes): UNCHANGED — closure added to phase plans, does not amend delivery modes

All 6 compose targets verified present (read-only consumers of US-0120 — their architectural surfaces are NOT edited by US-0120).

---

## DC (deferred-candidate) check

- `grep "^## US-0120" docs/engineering/architecture.md` → no matches expected (will be added in /architecture phase per R-0105 Q-2 LOCKED pattern).
- T-anch in /execute verifies anchor at architecture.md without writing it.

---

## Isolation evidence

- `phase_id=discovery`
- `role=po`
- `story_id=US-0120`
- `sprint_id=S0120`
- `orchestrator_run_id=auto-20260706-01`
- `fresh_context_marker=po-US0120-discovery-20260706T221400Z-fresh`
- `timestamp=2026-07-06T22:14:00Z` (UTC)
- `evidence_ref=handoffs/intake_evidence/US-0120-intake-20260706.json, docs/product/backlog.md (## US-0120 L4072-L4111), docs/product/acceptance.md (US-0120 row L147)`
- PO subagent spawned fresh per BUG-0006 / US-0048 isolation; no prior chat history carried forward
- `assemble_sovereign_memory_digest(...)` NOT called (existing context sufficient; US-0120 lifecycle-governance angle not in prior digests but discoverable via narrow-read)
- No write to `mistakes.jsonl` in discovery (no fix_failed / revert_applied / plan_fidelity_violation / scope_creep)

---

## Strict runtime proof tuple

- `runtime_proof_id=rp-auto-20260706-01-discovery-po-20260706T221400Z-US-0120`
- Canonical payload (sorted-key JSON per DEC-0038):
  ```json
  {
    "delivery_mode": "ultra_lean",
    "macro_phase": "spec",
    "orchestrator_run_id": "auto-20260706-01",
    "phase_id": "discovery",
    "proof_issued_at": "2026-07-06T22:14:00Z",
    "proof_ttl_seconds": 3600,
    "role": "po",
    "runtime_proof_id": "rp-auto-20260706-01-discovery-po-20260706T221400Z-US-0120",
    "sprint_id": "S0120",
    "story_id": "US-0120"
  }
  ```
- `proof_hash=447f401d9ca72415e0f3d607829eaced5fb14cbbffd71a48a336de48a9d040dd` (SHA-256 of canonical payload; computed by orchestrator post-write per DEC-0038)
- `proof_ttl=2026-07-06T23:14:00Z` (1-hour TTL)

---

## Decision gate

- `decision_gate=false`
- `stop_conditions_met=yes`
- All 12 ACs well-formed surjective coverage 12 tasks
- All 6 compose targets UNCHANGED
- No DC candidates
- Companion DEC: none (modifies DEC-0052 + DEC-0082 directly, no new DEC)

---

## Next scheduled phase

- `next_scheduled_phase=/research` (plan macro, first canonical phase per ultra_lean; research + architecture + sprint-plan merged)
- `next_scheduled_role=tech-lead`
- `next_scheduled_sprint_macro=plan`
- `stop_condition=STOP after discovery completes; hand off via artifacts only to /research in fresh tech-lead subagent`
