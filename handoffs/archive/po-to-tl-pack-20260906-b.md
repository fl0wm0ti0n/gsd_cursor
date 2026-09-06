# PO to TL archive pack (2026-09-06)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=650, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 8
- First archived heading: `## Discovery handoff Ã¢Â€Â” US-0119 Autonomous-autonomy presets (spec macro)`
- Last archived heading: `## Discovery handoff Ã¢Â€Â” US-0119 Autonomous-autonomy presets (spec macro)`
- Verification tuple (mandatory):
  - archived_body_lines=124
  - retained_body_lines=536

---

## Discovery handoff Ã¢Â€Â” US-0119 Autonomous-autonomy presets (spec macro)

**Phase completed**: discovery
**Phase role**: po
**Story**: US-0119 Autonomous-autonomy presets and configurable hard-stop relaxation
**Verdict**: PASS (no DECISION_GATE)
**Timestamp**: 2026-07-05T21:50:00Z
**Fresh context marker**: po-US0119-discovery-20260705T215000Z-fresh
**Runtime proof**: rp-auto-20260705-us0119-discovery-po-20260705T215000Z-US-0119 (proof_hash=71f1f55775f4d33bdd469f860eddfb7b4361ac462077386d27863f8c22c1cf86, proof_ttl=2026-07-05T22:50:00Z)
**Delivery mode**: ultra_lean (spec+plan merged)
**Macro phase**: spec (intake+discovery merged)

### Summary

AUTONOMY_PRESET={none|balanced|full} scratchpad flag that deterministically expands into twelve per-feature autonomy flags. AUTONOMY_STOP_POLICY={block|auto_repair_then_block|auto_repair_then_skip} flag that classifies every fail-closed reason code as security_hard (never auto-resolved) or autonomy_resolvable (bounded auto-repair with ledger cap). Compose (read-only) with US-0092/US-0095/US-0056/US-0068/US-0096/BUG-0007 Ã¢Â€Â” preset layer is additive only, never rewrites existing semantics.

### Discovery locks (L1..L12)

**L1**: AUTONOMY_PRESET=none|balanced|full (default none) in .cursor/scratchpad.md + template/.cursor/scratchpad.local.example.md. When none, byte-identical pre-US-0119 behavior.

**L2**: scripts/autonomy_preset_lib.py:expand_autonomy_preset(preset, overrides) returns dict. Expansion is deterministic. Explicit per-flag values win over preset expansion.

**L3**: AUTONOMY_STOP_POLICY=block|auto_repair_then_block|auto_repair_then_skip (default block).

**L4**: docs/engineering/autonomy-stop-matrix.md + template/docs/engineering/autonomy-stop-matrix.md (parity). YAML companion scripts/data/autonomy_stop_matrix.yaml + scripts/validate_autonomy_stop_matrix.py.

**L5**: Twelve per-feature flags documented and consumed: INTAKE_AUTONOMY_MODE, INTAKE_MINIMAL_PACK, INTAKE_ASSUME_STACK_CONTEXT, WORK_KIND_AUTO_ACCEPT, CROSS_MODEL_REWORK_EXHAUSTED_POLICY, CROSS_MODEL_SKIP_PHASES, RESUME_BRIEF_AUTO_REFRESH, RUNTIME_PROOF_KIND, GOAL_CONVERGENCE_INTERVAL, SOVEREIGN_DRAIN_AUTO_ACCEPT, RELEASE_PUBLISH_AUTO_CONFIRM, AUTONOMY_STOP_POLICY.

**L6**: Twelve flags do NOT exist yet in scratchpad (grep yields zero matches). US-0119 ADDS these twelve keys net-new.

**L7**: AUTONOMY_PRESET=none produces byte-identical pre-US-0119 orchestrator behavior. Contract test test_us0119_preset_none_is_noop enforces.

**L8**: security_hard gates NEVER softened. Contract test test_us0119_security_hard_gates_never_auto_repaired enforces matrix divergence.

**L9**: Append-only handoffs/autonomy_repair_ledger/<orchestrator_run_id>.jsonl. Cap per (run, reason_code). AUTONOMY_REPAIR_CAP_EXHAUSTED terminal stop reason.

**L10**: autonomy_relaxed breadcrumbs in docs/engineering/state.md.

**L11**: Compose do-not-amend Ã¢Â€Â” US-0092/US-0095/US-0056/US-0068/US-0096/BUG-0007 untouched. Contract test test_us0119_preset_expansion_uses_known_keys_only enforces.

**L12**: Ten contract test markers (test_us0119_*).

### Open questions Q1..Q10 for /research

**Q1** enumerate every autonomy_resolvable reason-code from /auto /intake /execute /qa /release.

**Q2** per-reason-code auto_repair_kind taxonomy.

**Q3** matrix cap defaults Ã¢Â€Â” uniform 3 or per-code tuning?

**Q4** RUNTIME_PROOF_KIND=lightweight TTL same as strict_hash?

**Q5** SOVEREIGN_DRAIN_RISK_THRESHOLD low|medium|high criteria per tier.

**Q6** RELEASE_PUBLISH_AUTO_CONFIRM allowlist only or includes previously-confirmed?

**Q7** INTAKE_MINIMAL_PACK threshold for "established project".

**Q8** matrix validator grep commands vs explicit manifest.

**Q9** AUTONOMY_REPAIR_CAP_EXHAUSTED new code vs extension of BLOCK_RETRY_CAP_EXHAUSTED.

**Q10** breadcrumb format in state.md Ã¢Â€Â” one-line per soft-stop or aggregated per phase?

### Risks R1..R6 carried to /architecture

**R1** (MEDIUM) backward-compat regression Ã¢Â€Â” test_us0119_preset_none_is_noop.

**R2** (MEDIUM) security gate bypass matrix Ã¢Â€Â” test_us0119_security_hard_gates_never_auto_repaired.

**R3** (LOW) repair ledger growth Ã¢Â€Â” per-run cap + gitignore.

**R4** (MEDIUM) operator confusion Ã¢Â€Â” breadcrumb + ledger audit surface.

**R5** (LOW-MEDIUM) preset-expansion vs explicit-key precedence Ã¢Â€Â” LOCKED: explicit > preset > defaults.

**R6** (LOW) compose-do-not-amend drift Ã¢Â€Â” test_us0119_preset_expansion_uses_known_keys_only.

### Compose do-not-amend (verified)

- US-0092: Ã¢ÂœÂ“ exists Ã¢Â€Â” delivery confirmation gate unchanged
- US-0095: Ã¢ÂœÂ“ exists Ã¢Â€Â” native auto-chain unchanged
- US-0056: Ã¢ÂœÂ“ exists as inline reference Ã¢Â€Â” strict runtime proof semantics UNCHANGED
- US-0068: Ã¢ÂœÂ“ exists as intake evidence gate Ã¢Â€Â” NEVER bypassed
- US-0096: Ã¢ÂœÂ“ exists Ã¢Â€Â” delivery modes unchanged
- BUG-0007: Ã¢ÂœÂ“ exists as anti-echo truthfulness rule Ã¢Â€Â” assumption_confirmation_ref contract preserved

### DC check

grep "^## US-0119" docs/engineering/architecture.md Ã¢Â†Â’ no matches. Expected (anchor added in /architecture phase). Not appended to sovereign_deferrals.jsonl.

### Validator gates

- validate_readme_feature_coverage.py PASS
- scratchpad_example_parity_test.py 4 passed

### Isolation evidence

- phase_id=discovery, role=po, story_id=US-0119, sprint_id=(pending)
- orchestrator_run_id=auto-20260705-us0119-intake
- fresh_context_marker=po-US0119-discovery-20260705T215000Z-fresh
- timestamp=2026-07-05T21:50:00Z (UTC)
- evidence_ref=docs/product/backlog.md (## US-0119 L4028-4070), handoffs/intake_evidence/US-0119-intake-20260705.json, handoffs/po_to_tl.md, handoffs/resume_brief.md, docs/engineering/research.md (R-0107 stub L8907-8928), docs/engineering/architecture.md (grep ^## US-0119 + compose targets), .cursor/scratchpad.md (grep autonomy keys Ã¢Â€Â” zero matches confirming L6), docs/product/acceptance.md (US-0119 row L146)
- assemble_sovereign_memory_digest(...) NOT called
- No write to mistakes.jsonl

### Decision gate

decision_gate=false (no DECISION_GATE)
stop_conditions_met=yes

### Next scheduled phase

next_scheduled_phase=/research
next_scheduled_role=tech-lead
next_scheduled_sprint_macro=plan
stop_condition=STOP after discovery completes; hand off to /research in fresh tech-lead subagent

---

# PO-to-TL handoffs

<!-- Archive pointer: US-0117 lifecycle handoffs (sprint-plan, architecture, research, spec) rolled over to `handoffs/archive/po-to-tl-pack-20260704-c.md` on 2026-07-04 by curator (US-0117 refresh-context terminal - final story in 5-story drain). US-0113/US-0114/US-0115 lifecycles in po-to-tl-pack-20260704-a/b.md; US-0116 lifecycle handoffs lost in git checkout HEAD recovery event (authoritative record in sprints/S0116/). Drain queue EMPTY - no next-story handoff to retain. -->

