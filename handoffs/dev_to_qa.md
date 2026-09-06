# Dev → QA handoff — BUG-0016 / S0132 / execute PASS

- sprint_id: S0132
- bug_id: BUG-0016 (Status OPEN — authority docs/product/backlog.md; do NOT mark DONE)
- story_id: (none — bug segment)
- phase_id: execute
- role: dev
- orchestrator_run_id: auto-20260906-bug0016
- delivery_mode: ultra_lean
- macro_phase: build+verify
- fresh_context_marker: dev-BUG0016-execute-20260906T190500Z-fresh
- timestamp: 2026-09-06T19:05:00Z (UTC)
- model_id: composer-2.5 (CROSS_MODEL_REVIEW=1 — required on isolation)
- execute_verdict: PASS
- approach: A* — DEC-0122 §2 sole SOT + agent frontmatter parity; bash ask po/tl/curator; PO duty paths; S* sprint globs; release duty paths; 7× test_bug0016_*; success test (c) preserved
- companion_DEC: none (DEC-0130 rejected; DEC-0122 §2 already amended in architecture)

## What shipped

1. Active + template `.opencode/agents/{po,tech-lead,dev,qa,release,curator}.md` frontmatter aligned to amended DEC-0122 §2
2. po/tech-lead/curator: `bash: ask` (not deny/allow)
3. PO edit: +`handoffs/intake_evidence/**` +`handoffs/resume_brief.md` +`docs/engineering/state.md`; `**` deny last
4. tech-lead/dev/qa/release: `sprints/Sxxxx/…` → `sprints/S*/…`
5. release: +release-findings +verify-work-to-release +state.md +resume_brief.md +runbook.md (keep verify_to_release)
6. security.md / auto.md UNCHANGED
7. `tests/us0122_contract_test.py` intentional realign + `tests/bug0016_contract_test.py` (7 markers) + template mirrors
8. Parity scope `bug-0016` (+ agent pairs on `opencode-adapter`)
9. T-007: write-guard does not re-deny duty globs — DEC-0124/0125 untouched

## Test evidence

| Gate | Result |
|---|---|
| `pytest tests/bug0016_contract_test.py -v` | 7/7 PASS |
| `pytest tests/us0122_contract_test.py -q` | 8/8 PASS (intentional realign) |
| `check_intake_template_parity.py --scope=bug-0016` | OK |
| `enforce-triad-hot-surface.py --check` | exit 0 |
| `check-user-visible-metadata.py --repo . --json` | OK / 0 violations |

## Files changed (execute)

- `.opencode/agents/{po,tech-lead,curator,dev,qa,release}.md` + `template/.opencode/agents/` peers
- `tests/us0122_contract_test.py` + `template/tests/us0122_contract_test.py`
- `tests/bug0016_contract_test.py` + `template/tests/bug0016_contract_test.py` (NEW)
- `scripts/check_intake_template_parity.py` + template (`bug-0016` scope + agent pairs)
- `sprints/S0132/{t-anch-verification.md,summary.md,progress.md,tasks.md}`
- `docs/engineering/state.md` (execute checkpoint)
- `handoffs/resume_brief.md` (execute PASS → qa)
- `handoffs/dev_to_qa.md` (this file)

## Compose / scope guards for QA

- Do NOT invent DEC-0130 / second matrix SOT
- Do NOT use `bash: allow`
- Do NOT amend DEC-0124 / DEC-0125 bodies (T-007: no double-deny proven)
- Do NOT reopen US-0131 / US-0132
- Do NOT reopen BUG-0015 (DONE compose-note only)
- Do NOT mark BUG-0016 DONE; do NOT tick acceptance BUG-0016
- Do NOT mutate intake JSON
- Do NOT rewrite architecture.md
- CF2: release runbook Layer-1 allow ≠ US-0126 prose ownership transfer
- plan-verify.json: create within QA per ultra_lean (merged into build+verify)

## Runtime proof (producer)

- runtime_proof_id: `rp-auto-20260906-bug0016-execute-dev-20260906T190500Z-BUG-0016`
- proof_hash: `519A7617F1ADBEAFD95A940AF28B130F8EB309350F3F787C0AC02152FBEC76BF`
- proof_ttl: 2026-09-06T20:05:00Z
- prior_consumed: `rp-auto-20260906-bug0016-sprint-plan-techlead-20260906T185500Z-BUG-0016` (F6892B96789FF471D7A97B40F80BBE59E725FB5A5DD573515D0ABC663B0A997F)

## critic_evidence (CROSS_MODEL_REVIEW=1 — producer evidence; critic runs after)

```yaml
critic_evidence:
  producer_phase_id: execute
  producer_role: dev
  producer_model_id: composer-2.5
  orchestrator_run_id: auto-20260906-bug0016
  sprint_id: S0132
  story_id: BUG-0016
  bug_id: BUG-0016
  fresh_context_marker: dev-BUG0016-execute-20260906T190500Z-fresh
  runtime_proof_id: rp-auto-20260906-bug0016-execute-dev-20260906T190500Z-BUG-0016
  proof_hash: 519A7617F1ADBEAFD95A940AF28B130F8EB309350F3F787C0AC02152FBEC76BF
  proof_issued_at: 2026-09-06T19:05:00Z
  proof_ttl: 2026-09-06T20:05:00Z
  canonical_payload: '{"delivery_mode":"ultra_lean","macro_phase":"build+verify","model_id":"composer-2.5","orchestrator_run_id":"auto-20260906-bug0016","phase_id":"execute","proof_issued_at":"2026-09-06T19:05:00Z","proof_ttl_seconds":3600,"role":"dev","runtime_proof_id":"rp-auto-20260906-bug0016-execute-dev-20260906T190500Z-BUG-0016","sprint_id":"S0132","story_id":"BUG-0016"}'
  evidence_refs:
    - sprints/S0132/summary.md
    - sprints/S0132/tasks.md
    - sprints/S0132/progress.md
    - sprints/S0132/t-anch-verification.md
    - tests/bug0016_contract_test.py
    - tests/us0122_contract_test.py
    - .opencode/agents/po.md
    - .opencode/agents/release.md
    - decisions/DEC-0122.md
    - docs/engineering/state.md
  nb_awareness_closed_in_execute:
    - b0016ar-challenger-001 / ik_bug0016_arch_edge_and_proof (T-007 write-guard verify; S* kept; parity + us0122 realign)
    - b0016ar-architect-002 / ik_bug0016_arch_layer_coupling (T-anch..T-007 1:1; DEC-0122 sole SOT; CF2 runbook allow ≠ US-0126 ownership)
    - b0016ar-subtractor-003 / ik_bug0016_arch_scope_minimal (no DONE / no DEC-0130 / no bash:allow / no live probe / 7 markers)
  ready_for_sovereign_critic: true
```

## Stop condition

STOP after execute. Orchestrator owns sovereign-critic of execute then `/qa` in fresh qa subagent (BUG-0006). Do not spawn QA from this subagent. Do not mark BUG-0016 DONE. Do not tick acceptance. Do not reopen BUG-0015.
