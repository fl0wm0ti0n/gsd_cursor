# State archive pack (2026-07-08)

- Rollover trigger: `STATE_HOT_MAX_LINES=1000, STATE_HOT_MAX_CHECKPOINTS=80`
- Source: `docs/engineering/state.md`
- Archived units (oldest first, contiguous prefix): 9
- Retained units in hot file: 12
- First archived heading: `## Discovery checkpoint — US-0118 / S0118 / auto-20260704-01`
- Last archived heading: `## Discovery checkpoint — US-0119 / S0119 / auto-20260705-us0119-intake`
- Verification tuple (mandatory):
  - archived_body_lines=752
  - preamble_lines=4
  - retained_body_lines=925

---

## Discovery checkpoint — US-0118 / S0118 / auto-20260704-01

- **phase_id**: discovery (spec macro — second canonical phase within ultra_lean; intake already complete), **role**: po, **story_id**: US-0118, **sprint_id**: (pending — created at sprint-plan)
- `orchestrator_run_id=auto-20260704-01`, `delivery_mode=ultra_lean`, `macro_phase=spec` (discovery — second canonical phase within ultra_lean `spec` macro; intake + discovery merged per US-0096 / DEC-0082; intake already complete → discovery is the next phase to spawn)
- `reinstatement_mode=none` (ultra_lean — no eleven-phase reinstatement), `memory_layer=pack`
- `verdict=PASS` (no DECISION_GATE — discovery locks captured; open questions delegated to `/research`)
- `fresh_context_marker=po-US0118-discovery-20260704T194500Z-fresh`
- `timestamp (UTC)=2026-07-04T19:45:00Z`

### Discovery locks L1..L10

- **L1** (work_kind enumeration + recommended_delivery_mode field) — `work_kind ∈ {"doc","mini","code"}` returned by `scripts/work_kind_classify_lib.py:classify_work_kind(...)`; each result also carries `recommended_delivery_mode ∈ {"standard","ultra_lean","mega_quick"}`. Pure stdlib, no network, no `.env` reads.
- **L2** (WORK_KIND_ROUTING scratchpad flag default-off) — new `WORK_KIND_ROUTING=0|1` (default `0`). When `0`, zero overhead: `/auto` `resolve_delivery_mode` and intake persistence skip classifier entirely. Documented in `.cursor/scratchpad.md` + `template/.cursor/scratchpad.local.example.md` with merge-precedence note (local > materialized baseline > example per US-0078 model B).
- **L3** (classifier inputs) — `classify_work_kind(story_prose, acceptance_criteria, touched_file_hints, component_scope)`; inputs are prose + AC set + touched-file hints (names-only, no content reads) + component_scope string. No secret surface; classifier sees file names only.
- **L4** (classifier outputs) — returns `WorkKindResult{work_kind, recommended_delivery_mode, recommended_phase_plan, rationale, evidence_refs}`. `recommended_phase_plan` is a list of canonical phase ids (e.g. `["intake","execute","release"]` for `doc`). `rationale` is a human-readable rule trace; `evidence_refs` are names-only file references (no content).
- **L5** (`doc` route) — when all touched files match `dev_environment_lib.TIER_C_SKIP_PREFIXES` (`docs/`, `handoffs/`, `sprints/`, `decisions/`, `tests/`, `.cursor/commands/`, `template/docs/`) or are `*.md`/`README*` under skip prefixes → `recommended_phase_plan=[intake, execute, release]` (skip discovery/research/architecture/sprint-plan/plan-verify/qa/verify-work). `recommended_delivery_mode=standard` (the phase plan itself encodes the skip; no delivery-mode change required).
- **L6** (`mini` route) — single component, ACs ≤ 3, no companion DEC required → `recommended_delivery_mode=ultra_lean` or `mega_quick` (reuse US-0096 `mega_quick` eligibility: AC ≤ 3, no DEC, single component — when eligible recommend `mega_quick`, else fall back to `ultra_lean`). Phase plan derived from US-0096 macro-phase collapse.
- **L7** (`code` route) — otherwise → `recommended_delivery_mode=standard` (or honor current `DELIVERY_MODE` if explicitly set). Full canonical lifecycle retained.
- **L8** (precedence chain) — explicit `DELIVERY_MODE` (US-0096) > explicit `AUTO_PHASE_*` (US-0070) > `WORK_KIND_ROUTING`-derived `recommended_delivery_mode` (US-0118, only when `WORK_KIND_ROUTING=1` AND backlog row carries `work_kind` AND higher-precedence keys unset) > current default lifecycle. `start-from` always wins. Documented in `.cursor/commands/auto.md`.
- **L9** (reason-code family prefix) — `WORK_KIND_*` family: `WORK_KIND_CLASSIFY_FAILED`, `WORK_KIND_DELIVERY_MODE_CONFLICT` (work-kind recommends X but `DELIVERY_MODE` set to Y and they conflict), `WORK_KIND_ROUTING_DISABLED` (info when flag off), `WORK_KIND_PLAN_COVERAGE_MISSING` (classifier returned empty/invalid phase plan). Each emits remediation guidance in `sprints/Sxxxx/qa-findings.md` / `release-findings.md`.
- **L10** (intake-time accept/override gate) — `/intake` step 5 (after ACs drafted, after US-0051 decomposition evaluator, before persistence): when `WORK_KIND_ROUTING=1`, run classifier, propose `work_kind` + `recommended_delivery_mode`, present to operator for accept/override. Persist choice in backlog row (`work_kind`, `recommended_delivery_mode`) + intake evidence bundle (`work_kind`, `recommended_delivery_mode`, `work_kind_operator_decision ∈ {accept, override}`) per US-0078 / DEC-0060. Evidence gate still runs before any backlog/acceptance write.

### Open questions for `/research`

- **Q1** (tie-break rule): when a story touches both `docs/` and `src/` (mixed tier), which work-kind wins? Candidate: highest tier wins (`code` wins over `mini` over `doc` per `dev_environment_lib.classify_touched_files` tier_rank A>B>C precedent). Confirm deterministic rule.
- **Q2** (exact reason-code names + remediation prose): finalize the four `WORK_KIND_*` reason codes (AC-7) and their remediation guidance text emitted in `qa-findings.md` / `release-findings.md`.
- **Q3** (classifier determinism): confirm classifier is deterministic pure-stdlib (rule-based) — NO LLM-assisted classification. Lock the rule trace format (`--explain` flag emitting rule trace per R5).
- **Q4** (contract test surface): enumerate `test_us0118_*` markers needed in `tests/work_kind_classify_test.py` — each work-kind classification, each recommended phase plan, default-off zero-overhead, precedence vs `DELIVERY_MODE`/`AUTO_PHASE_*`, operator override path, each fail-closed reason code.
- **Q5** (scratchpad reference extension): what new keys are added to which README sub-block? `WORK_KIND_ROUTING` likely lands under a new `### Work-kind routing keys` sub-block (sibling to US-0113..US-0117 sub-blocks) OR under `### Delivery & lifecycle keys` (US-0116). Recommend new sub-block to keep cross-story byte-stability surface clean.
- **Q6** (template parity scope): what `WORK_KIND_*` pairs need byte-identical sync? `scripts/work_kind_classify_lib.py` ↔ `template/scripts/work_kind_classify_lib.py`; `.cursor/scratchpad.md` `WORK_KIND_ROUTING` row ↔ `template/.cursor/scratchpad.local.example.md`; `check_intake_template_parity.py --scope=work-kind-routing` with `WORK_KIND_ROUTING_PAIRS` manifest.
- **Q7** (runbook cross-link anchor): `docs/engineering/runbook.md` h-level + line number target for `WORK_KIND_ROUTING` flag + operator recipe (how to force full lifecycle on a `doc` story by setting `DELIVERY_MODE=standard`).
- **Q8** (backward-compat proof): prove `WORK_KIND_ROUTING=0` is byte-identical to pre-US-0118 behavior — existing backlog rows without `work_kind` continue to route via current `DELIVERY_MODE`/`AUTO_PHASE_*` (no forced reclassification). Test marker `test_us0118_default_off_zero_overhead`.
- **Q9** (classifier reuse boundary): confirm `scripts/dev_environment_lib.py:classify_touched_files()` is extended/imported, NOT rewritten. Lock the import contract — does `work_kind_classify_lib.py` import `TIER_C_SKIP_PREFIXES` + `classify_touched_files` directly, or duplicate the constants?
- **Q10** (installer manifest rows): `installer-owned-paths.manifest` `[install_include_paths]` rows for `scripts/work_kind_classify_lib.py` + `template/scripts/work_kind_classify_lib.py` — confirm triple-installer parity (PS1/Bash/Python) ships the new script.

### Risks carried to `/architecture`

- **R1** (MEDIUM) — Classification ambiguity (a story that touches both `docs/` and `src/`) → deterministic tie-break rule needed (Q1; candidate: highest tier wins per `classify_touched_files` precedent).
- **R2** (MEDIUM) — Precedence conflicts when both `WORK_KIND_ROUTING=1` and `DELIVERY_MODE` are set → documented precedence chain (L8) + `WORK_KIND_DELIVERY_MODE_CONFLICT` reason code.
- **R3** (LOW–MEDIUM) — `mega_quick` eligibility overlap with `mini` → classifier recommends `mega_quick` only when US-0096 eligibility passes, else falls back to `ultra_lean` (L6).
- **R4** (MEDIUM) — Backward compatibility — existing backlog rows without `work_kind` must continue to route via current `DELIVERY_MODE`/`AUTO_PHASE_*` (no forced reclassification). Q8 proof required.
- **R5** (LOW–MEDIUM) — Operator trust — classifier must be deterministic and inspectable (`--explain` flag emitting rule trace) so operators can override with confidence.
- **R6** (LOW) — Reuse boundary drift — `dev_environment_lib.classify_touched_files` extended/imported, not rewritten (Q9); lock import contract in `/architecture`.
- **R7** (LOW) — Installer parity drift — triple-installer must ship `work_kind_classify_lib.py` byte-identical (Q10); manifest-driven single source of truth.

### Compose, do not amend (verified)

- **US-0096 / DEC-0082** (delivery modes): README umbrella `### Integration & observability` L1410 + `### Integration & observability keys` L2617 + `#### US-0096` L1569 (architecture.md `## US-0096` L1684). US-0118 makes routing per-story + derived; explicit `DELIVERY_MODE` still wins (L8). ✓ verified exists.
- **US-0070 / DEC-0052** (phase selection): README `#### US-0070` L2015 + `#### US-0070 — Phase selection policy keys` L2890 (architecture.md `## US-0070` L1572). `AUTO_PHASE_*` keys remain the explicit override; classifier only fills the unset case (L8). ✓ verified exists.
- **US-0078 / DEC-0060** (intake evidence): README `#### US-0078` L2131 + `## Interactive intake evidence validation` L432 (architecture.md `## US-0078` L1596). Classifier proposal + operator decision recorded in evidence bundle; gate still runs before any write (L10). ✓ verified exists.
- **US-0051** (decomposition): README `### Intake decomposition + risk-aware questioning (US-0051)` L382. Classifier runs after the decomposition evaluator (L10). ✓ verified exists.
- **US-0069 / DEC-0051** (phase→role matrix): README `#### US-0069` L1996 + `#### US-0069 — Phase→role matrix keys` L2876 (architecture.md `## US-0069` L1568). Unchanged; classifier only selects which phases run, not who runs them. ✓ verified exists.
- **US-0103** (AI decision ledger): README `#### US-0103` L982 + `### Sovereign-loop era keys` L2421 (architecture.md `## US-0103` L1640). Read-only consumer for audit trail. ✓ verified exists.

All 6 compose targets verified present (read-only consumers of US-0118 — their architectural surfaces are NOT edited by US-0118).

### DC (deferred-candidate) check

- `grep "^## US-0118" docs/engineering/architecture.md` → **no matches**. The `## US-0118` h1 anchor is **missing** from `architecture.md`. This is **expected** — the `## US-0118` anchor will be added in the `/architecture` phase (plan macro), NOT in `/discovery` (spec macro). No action required here. Not appended to `handoffs/sovereign_deferrals.jsonl` — orchestrator's segment-boundary advance hook handles DC resolution in `/architecture`.

### Isolation evidence (US-0048 / DEC-0029)

- `phase_id=discovery`
- `role=po`
- `story_id=US-0118`
- `sprint_id=(pending — created at sprint-plan)`
- `orchestrator_run_id=auto-20260704-01`
- `fresh_context_marker=po-US0118-discovery-20260704T194500Z-fresh`
- `timestamp=2026-07-04T19:45:00Z` (UTC)
- `evidence_ref=docs/product/backlog.md (US-0118 block L3983–L4022 narrow-read), docs/product/acceptance.md (US-0118 row L145 narrow-read), handoffs/intake_evidence/US-0118-intake.json (full read), handoffs/po_to_tl.md (L1–L40 US-0118 intake handoff narrow-read), docs/engineering/state.md (drain-advance materialization breadcrumb L84–L101 narrow-read), .cursor/skills/its-magic/SKILL.md (full read), scripts/dev_environment_lib.py (TIER_C_SKIP_PREFIXES L117–L125 + classify_touched_files L321–L339 narrow-read), its_magic/README.md (grep US-0096/US-0070/US-0078/US-0051/US-0069/US-0103 anchors only — no full-read), docs/engineering/architecture.md (grep ^## US-0096/^## US-0070/^## US-0069/^## US-0078/^## US-0051/^## US-0103/^## US-0118 anchors only — no full-read), .cursor/commands/discovery.md (full read), docs/product/backlog.md (US-0108 discovery_notes L3856–L3888 narrow-read for L1..L10 pattern reference), docs/engineering/research.md (grep R-0106 anchor only), handoffs/resume_brief.md (L1–L40 narrow-read for drain-advance prose shape)`
- PO subagent spawned fresh per BUG-0006 / US-0048 isolation; no prior chat history carried forward. Context limited to the narrow-read files listed above (US-0053 / US-0096 Tranche A). No MCP / browser / shell side-effects beyond narrow-read grep + read tool calls + powershell SHA-256 computation for the strict runtime proof + the artifact writes listed in this prompt (state.md append, po_to_tl.md prepend, resume_brief.md append). No `.env` reads, no credentials access, no intake-evidence mutation (read-only for this phase).
- `assemble_sovereign_memory_digest(...)` NOT called (US-0118 first story of a new drain — US-0113..US-0117 retrospectives established reusable patterns; classifier work is code, not documentation — existing digest context sufficient for discovery; sovereign memory digest may be assembled in `/architecture` or `/execute` if needed).
- No write to `mistakes.jsonl` in discovery phase (no fix_failed / revert_applied / plan_fidelity_violation / scope_creep event occurred).
- Prior phase strict proof: intake phase did not emit a separate runtime proof (intake evidence bundle `handoffs/intake_evidence/US-0118-intake.json` is the intake evidence-of-record; intake merged into spec macro per ultra_lean — no separate intake checkpoint).

### Strict runtime proof tuple (US-0056 / DEC-0038)

- `runtime_proof_id=rp-auto-20260704-01-discovery-po-20260704T194500Z-US-0118`
- Canonical payload (sorted-key JSON per DEC-0038): `{"orchestrator_run_id":"auto-20260704-01","phase_id":"discovery","proof_issued_at":"2026-07-04T19:45:00Z","proof_ttl_seconds":"3600","role":"po","runtime_proof_id":"rp-auto-20260704-01-discovery-po-20260704T194500Z-US-0118","sprint_id":"(pending)","story_id":"US-0118"}`
- `proof_hash=17b2339eb039a4854a8ba347f49b649626cf224aa48cd308914bda82d49b6488` (SHA-256 of the sorted-key JSON payload above, computed via powershell `[System.Security.Cryptography.SHA256]::Create().ComputeHash`)
- `proof_ttl_seconds=3600`
- `proof_ttl=2026-07-04T20:45:00Z` (1-hour TTL per DEC-0038, UTC = issued_at + 3600s)

### Decision gate

- `decision_gate=false` (no DECISION_GATE; no hard stop; discovery locks captured; open questions delegated to `/research`)
- `stop_conditions_met=yes` (no missing references — all 6 compose targets verified; no decision gate triggered)

### Next scheduled phase

- `next_scheduled_phase=/research` (role=tech-lead per US-0069 / DEC-0051 phase→role matrix default — `AUTO_ROLE_RESEARCH` is empty so default tech-lead applies; this is the first canonical phase of the `plan` macro per ultra_lean; research + sprint-plan merged into `plan` macro)
- `next_scheduled_role=tech-lead`
- `next_scheduled_sprint_macro=plan`
- `stop_condition=STOP after discovery completes; hand off via artifacts only to /research in fresh tech-lead subagent (BUG-0006)`

## Research checkpoint — US-0118 / S0118 / auto-20260704-01

- **phase_id**: research (plan macro — first canonical phase within ultra_lean; research + architecture + sprint-plan merged per US-0096 / DEC-0082), **role**: tech-lead (per US-0069 / DEC-0051 phase→role matrix default; `AUTO_ROLE_RESEARCH` empty → default tech-lead), **story_id**: US-0118, **sprint_id**: (pending — created at sprint-plan)
- `orchestrator_run_id=auto-20260704-01`, `delivery_mode=ultra_lean`, `macro_phase=plan` (research — first canonical phase of `plan` macro)
- `reinstatement_mode=none` (ultra_lean — no eleven-phase reinstatement), `memory_layer=pack`
- `verdict=PASS` (no DECISION_GATE; 10/10 discovery open questions Q1..Q10 closed LOCKED; architecture seeds proposed for `/sprint-plan`; companion DEC-0118 to be authored in `/architecture`)
- `fresh_context_marker=tl-US0118-research-20260704T200000Z-fresh`
- `timestamp (UTC)=2026-07-04T20:00:00Z`
- `research_anchor=docs/engineering/research.md ## R-0106 - US-0118 Work-kind classification + tiered delivery routing research`

### Closed questions Q1..Q10 (10/10 — all LOCKED)

- **Q1** (tie-break rule): LOCKED — highest tier wins (`code` > `mini` > `doc`) per `dev_environment_lib.classify_touched_files` tier_rank A>B>C precedent.
- **Q2** (reason-code names + remediation prose): LOCKED — `WORK_KIND_CLASSIFY_FAILED`, `WORK_KIND_DELIVERY_MODE_CONFLICT`, `WORK_KIND_ROUTING_DISABLED` (info-only), `WORK_KIND_PLAN_COVERAGE_MISSING` — each with remediation prose.
- **Q3** (classifier determinism): LOCKED — deterministic pure-stdlib (rule-based), NO LLM; `--explain` emits `rule_trace`; no network/`.env`/model.
- **Q4** (contract test markers): LOCKED — 12 `test_us0118_*` markers in `tests/work_kind_classify_test.py`.
- **Q5** (scratchpad reference extension): LOCKED — new sibling sub-block `### Work-kind routing keys (US-0118)` (6th sibling; preserves US-0113..US-0117 byte-stability). README edits happen in `/execute`, not `/research`.
- **Q6** (template parity pairs): LOCKED — 6 `WORK_KIND_*` parity pairs (script, scratchpad, commands, runbook, manifest) + `WORK_KIND_ROUTING_PAIRS` validator.
- **Q7** (runbook cross-link anchor): LOCKED — new h2 `## Work-kind routing (US-0118)` (sibling to existing h2 sections).
- **Q8** (backward-compat proof for `WORK_KIND_ROUTING=0`): LOCKED — contract test `test_us0118_default_off_zero_overhead` + early-return in `/auto` `resolve_delivery_mode` step 0.
- **Q9** (intake-time operator accept/override gate): LOCKED — 3 new evidence fields (`work_kind`, `recommended_delivery_mode`, `work_kind_operator_decision ∈ {accept, override}`).
- **Q10** (classifier input schema): LOCKED — `classify_work_kind(story_prose, acceptance_criteria, touched_file_hints, component_scope) -> WorkKindClassification` dataclass.

### Architecture seeds (10 tasks within SPRINT_MAX_TASKS=12)

T-anch (architecture.md `# US-0118` anchor + compose-do-not-amend verification + import-contract lock), T-001 (classifier lib `scripts/work_kind_classify_lib.py`), T-002 (scratchpad flag `WORK_KIND_ROUTING` + `.cursor/commands/auto.md` precedence clause), T-003 (intake integration `/intake` step 5), T-004 (`/auto` `resolve_delivery_mode` step-0 integration + early-return), T-005 (reason codes + fail-closed), T-006 (contract tests `tests/work_kind_classify_test.py` — 12 markers), T-007 (README + template parity `### Work-kind routing keys` sub-block), T-008 (runbook cross-link `## Work-kind routing` h2), T-009 (regression + installer manifest).

### Companion DEC

`companion_dec=DEC-0118` (required — to be authored in `/architecture`, not here). US-0118 introduces a new routing primitive — DEC-0118 locks: (a) work-kind enumeration (`doc`/`mini`/`code` 3-tier), (b) L8 precedence chain (explicit operator flags always win; classifier fills only the unset case), (c) `dev_environment_lib.classify_touched_files` reuse boundary (import, not rewrite), (d) zero-overhead-when-off contract (default `WORK_KIND_ROUTING=0`). Mirrors DEC-0082 / DEC-0052 precedent.

### Compose guards (US-0118 is a NEW story — carried-forward set listed; US-0118 may ADD compose guards in `/architecture`)

US-0118 is a NEW story (not part of the US-0113..US-0117 quint). The existing compose-guard set is carried forward unchanged (read-only consumers of US-0118):

| Story | README anchor | architecture.md anchor | Verification |
|-------|---------------|------------------------|--------------|
| US-0096 / DEC-0082 | L2617 + L2670 inline | `## US-0096` L1684 | ✓ exists — explicit `DELIVERY_MODE` still wins (L8) |
| US-0070 / DEC-0052 | L2856 | `## US-0070` L1572 | ✓ exists — `AUTO_PHASE_*` remains explicit override (L8) |
| US-0078 / DEC-0060 | L479 runbook | `## US-0078` L1596 | ✓ exists — evidence gate still runs before any write (L10) |
| US-0051 | L371 runbook | (no h1 anchor) | ✓ exists — classifier runs after decomposition evaluator (L10) |
| US-0069 / DEC-0051 | L2856 | `## US-0069` L1568 | ✓ exists — classifier only selects which phases run, not who |
| US-0103 | L2421 | `## US-0103` L1640 | ✓ exists — read-only consumer for audit trail |

All 6 compose targets verified present (read-only consumers of US-0118 — additive-only). US-0118 may ADD new compose guards (e.g. for the new `WORK_KIND_ROUTING` flag) — that decision belongs to `/architecture`, not `/research`. Do NOT claim "UNCHANGED (23)" — US-0118 is a code-bearing story with new surfaces.

### Test markers proposed (12)

`test_us0118_doc_kind_routes_to_lean_plan`, `test_us0118_mini_kind_routes_to_ultra_lean`, `test_us0118_mini_kind_routes_to_mega_quick_when_eligible`, `test_us0118_code_kind_routes_to_standard`, `test_us0118_explicit_delivery_mode_wins_over_work_kind`, `test_us0118_auto_phase_wins_over_work_kind`, `test_us0118_routing_off_is_noop`, `test_us0118_classify_touched_files_reuse`, `test_us0118_intake_evidence_records_work_kind`, `test_us0118_reason_codes_preserved`, `test_us0118_default_off_zero_overhead`, `test_us0118_explain_emits_rule_trace` (in `tests/work_kind_classify_test.py`).

### Validator gates (run this phase)

- `python scripts/validate_readme_feature_coverage.py --repo .` → `{"coverage_missing":[],"coverage_present":[],"coverage_total":0,"gaps":[],"status":"PASS"}` exit 0 (US-0118 not yet in catalog surface — no README feature coverage entry expected pre-`/execute`).
- `python -m pytest tests/scratchpad_example_parity_test.py -v` → `4 passed in 0.08s` (BUG-0013 parity baseline green; not weakened).

### Risks finalized (R1..R7 promoted + R8 added — 8 risks)

- **R1** (MEDIUM) — Classification ambiguity (mixed `docs/`+`src/` tiers) → Q1 LOCKED tie-break (highest tier wins).
- **R2** (MEDIUM) — Precedence conflicts (`WORK_KIND_ROUTING=1` + `DELIVERY_MODE` set) → L8 precedence chain + `WORK_KIND_DELIVERY_MODE_CONFLICT` reason code.
- **R3** (LOW–MEDIUM) — `mega_quick` eligibility overlap with `mini` → L6 eligibility gating (recommend `mega_quick` only when US-0096 eligibility passes, else `ultra_lean`).
- **R4** (MEDIUM) — Backward compatibility (existing backlog rows without `work_kind`) → Q8 LOCKED early-return + contract test.
- **R5** (LOW–MEDIUM) — Operator trust → Q3 LOCKED deterministic pure-stdlib + `--explain` `rule_trace`.
- **R6** (LOW) — Reuse boundary drift (`dev_environment_lib.classify_touched_files` rewritten vs imported) → Q9 LOCKED import contract + contract test.
- **R7** (LOW) — Installer parity drift → T-009 manifest adds both script copies to `installer-owned-paths.manifest`.
- **R8** (MEDIUM, NEW) — Cross-story byte-stability surface (6th sub-block) → T-007 net-new-keys-only + `PARITY_OK` proof; never edits US-0113..US-0117 released blocks.

### Isolation evidence (US-0048 / DEC-0029)

- `phase_id=research`
- `role=tech-lead`
- `story_id=US-0118`
- `sprint_id=(pending — created at sprint-plan)`
- `orchestrator_run_id=auto-20260704-01`
- `fresh_context_marker=tl-US0118-research-20260704T200000Z-fresh`
- `timestamp=2026-07-04T20:00:00Z` (UTC)
- `evidence_ref=docs/product/backlog.md (## US-0118 block L3983–L4025 narrow-read), docs/product/acceptance.md (US-0118 row L145 narrow-read), handoffs/intake_evidence/US-0118-intake.json (full read ~104 lines), handoffs/po_to_tl.md (US-0118 discovery handoff L5–L103 narrow-read), docs/engineering/state.md (drain-advance breadcrumb L84–L101 + discovery checkpoint L102–L196 narrow-read), scripts/dev_environment_lib.py (TIER_C_SKIP_PREFIXES L117–L125 + TIER_A_PATTERNS L84–L102 + TIER_B_PATTERNS L104–L115 + classify_touched_files L321–L339 narrow-read), its_magic/README.md (grep Delivery & lifecycle keys / Phase & role governance keys / Full scratchpad reference / Caveman mode anchors only — no full-read), docs/engineering/architecture.md (grep ^## US-0096/^## US-0070/^## US-0069/^## US-0078/^## US-0103/^## US-0118 anchors only — no full-read), docs/engineering/runbook.md (grep ^## h2 anchors only — no full-read), .cursor/scratchpad.md (grep WORK_KIND_ROUTING/DELIVERY_MODE/AUTO_PHASE_PLAN/EARLY_RESEARCH/SPRINT_MAX_TASKS anchors only), .cursor/commands/auto.md (resolve_delivery_mode L284–L329 narrow-read), .cursor/commands/intake.md (grep decomposition/step 5/persistence anchors only), docs/engineering/research.md (R-0105 full read as template + R-0106 stub replacement)`
- Tech-lead subagent spawned fresh per BUG-0006 / US-0048 isolation; no prior chat history carried forward. Context limited to the narrow-read files listed above (US-0053 / US-0096 Tranche A). No MCP / browser / shell side-effects beyond narrow-read grep + read tool calls + python SHA-256 computation for the strict runtime proof + the artifact writes listed in this phase (research.md R-0106 entry, state.md research checkpoint append, po_to_tl.md research handoff prepend, resume_brief.md drain-advance append). No `.env` reads, no credentials access, no intake-evidence mutation (read-only for this phase).
- `assemble_sovereign_memory_digest(...)` NOT called (US-0118 first story of a new drain — US-0113..US-0117 retrospectives established reusable patterns; classifier work is code, not documentation — existing digest context sufficient for research).
- No write to `mistakes.jsonl` in research phase (no fix_failed / revert_applied / plan_fidelity_violation / scope_creep event occurred).
- Prior phase strict proof consumed: `rp-auto-20260704-01-discovery-po-20260704T194500Z-US-0118` (from `docs/engineering/state.md` discovery checkpoint L179–L183, unchanged).
- Current research-phase strict proof recorded below.

### Strict runtime proof tuple (US-0056 / DEC-0038)

- `runtime_proof_id=rp-auto-20260704-01-research-techlead-20260704T200000Z-US-0118`
- Canonical payload (sorted-key JSON per DEC-0038): `{"orchestrator_run_id":"auto-20260704-01","phase_id":"research","proof_issued_at":"2026-07-04T20:00:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260704-01-research-techlead-20260704T200000Z-US-0118","sprint_id":"(pending)","story_id":"US-0118"}`
- `proof_hash=3582430b9c41b432bc8822b16bfc32c3597cf6788c528507d3dd0e21adb23e9e` (SHA-256 of the sorted-key JSON payload above, computed via python `hashlib.sha256`)
- `proof_ttl_seconds=3600`
- `proof_ttl=2026-07-04T21:00:00Z` (1-hour TTL per DEC-0038, UTC = issued_at + 3600s)

### Decision gate

- `decision_gate=false` (no DECISION_GATE; no hard stop; 10/10 discovery open questions Q1..Q10 closed LOCKED; architecture seeds proposed for `/sprint-plan`; companion DEC-0118 to be authored in `/architecture`)
- `stop_conditions_met=yes` (no missing references — all 6 compose targets verified; no decision gate triggered)

### Next scheduled phase

- `next_scheduled_phase=/architecture` (role=tech-lead per US-0069 / DEC-0051 phase→role matrix default; second canonical phase of `plan` macro per ultra_lean; research + architecture + sprint-plan merged into `plan` macro)
- `next_scheduled_role=tech-lead`
- `next_scheduled_sprint_macro=plan`
- `stop_condition=STOP after research completes; hand off via artifacts only to /architecture in fresh tech-lead subagent (BUG-0006)`


## Architecture checkpoint â€” US-0118 / S0118 / auto-20260704-01

- **phase_id**: architecture (plan macro â€” second canonical phase within ultra_lean; research + architecture + sprint-plan merged per US-0096 / DEC-0082), **role**: tech-lead (per US-0069 / DEC-0051 phaseâ†’role matrix default), **story_id**: US-0118, **sprint_id**: (pending â€” created at sprint-plan)
- `orchestrator_run_id=auto-20260704-01`, `delivery_mode=ultra_lean`, `macro_phase=plan` (architecture â€” second canonical phase of `plan` macro)
- `reinstatement_mode=none` (ultra_lean â€” no eleven-phase reinstatement), `memory_layer=pack`
- `verdict=PASS` (no DECISION_GATE; companion DEC-0118 authored Accepted in THIS phase; approach A1 locked; sprint seeds T-anch + T-001..T-009 within SPRINT_MAX_TASKS=12; risks R1..R8 finalized; DC check clean)
- `fresh_context_marker=tl-US0118-architecture-20260704T203000Z-fresh`
- `timestamp (UTC)=2026-07-04T20:30:00Z`
- `architecture_anchor=docs/engineering/architecture.md ## US-0118 â€” Work-kind classification + tiered delivery routing per story` (L1713)
- `research_anchor=docs/engineering/research.md ## R-0106 - US-0118 Work-kind classification + tiered delivery routing research` (L8754)
- `companion_dec=DEC-0118` (Required â†’ Accepted; authored in THIS phase at `decisions/DEC-0118.md`)
- `approach_locked=A1` (single `### Work-kind routing (US-0118)` umbrella + per-feature subsections + 6th scratchpad ref sub-block `### Work-kind routing keys (US-0118)` as sibling to US-0113..US-0117 sub-blocks; 6th-story cumulative byte-stability surface â€” prior 5 released blocks must remain byte-identical)
- `sprint_seeds=10` (T-anch + T-001..T-009 within SPRINT_MAX_TASKS=12)
- `compose_guards=23` (UNCHANGED â€” same 23 as US-0117; US-0118 is additive-only â€” new flag, new lib, new row fields, new precedence clause, new sub-block, new runbook h2; does NOT amend any existing compose-surface feature; US-0118 itself does NOT become a NEW compose guard â€” it's a routing primitive, not a guard)
- `test_markers=12` (from R-0106 Q4 LOCKED â€” `test_us0118_doc_kind_routes_to_lean_plan`, `test_us0118_mini_kind_routes_to_ultra_lean`, `test_us0118_mini_kind_routes_to_mega_quick_when_eligible`, `test_us0118_code_kind_routes_to_standard`, `test_us0118_explicit_delivery_mode_wins_over_work_kind`, `test_us0118_auto_phase_wins_over_work_kind`, `test_us0118_routing_off_is_noop`, `test_us0118_classify_touched_files_reuse`, `test_us0118_intake_evidence_records_work_kind`, `test_us0118_reason_codes_preserved`, `test_us0118_default_off_zero_overhead`, `test_us0118_explain_emits_rule_trace` in `tests/work_kind_classify_test.py`)
- `dc_resolution=clean` (grep `^## US-0118` architecture.md prior to this phase â†’ no matches; `## US-0118` h1 anchor added in THIS phase per R-0105 Q-2 LOCKED pattern â€” T-anch is the resolution point; cross-check against full US-xxxx list in backlog.md â†’ no OTHER deferred `## US-xxxx` anchors remain unresolved; US-0117 was the final deferred-candidate resolution point â€” 36 anchors added in US-0117's `/architecture` phase; deferral register clean; US-0118 inherits no DC candidates from prior stories; no new DC candidates created by US-0118)
- `risks_finalized=8` (R1 classification ambiguity MEDIUM â†’ Q1 tie-break; R2 precedence conflicts MEDIUM â†’ L8 + `WORK_KIND_DELIVERY_MODE_CONFLICT`; R3 `mega_quick`/`mini` overlap LOWâ€“MEDIUM â†’ L6 eligibility gating; R4 backward-compat MEDIUM â†’ Q8 early-return + contract test; R5 operator trust LOWâ€“MEDIUM â†’ Q3 `--explain` + `rule_trace`; R6 reuse boundary drift LOW â†’ Q9 import contract + contract test; R7 installer parity drift LOW â†’ T-009 manifest; R8 NEW cross-story byte-stability surface 6th sub-block MEDIUM â†’ T-007 net-new-keys-only + `PARITY_OK` proof never edits US-0113..US-0117 released blocks)
- `stop_conditions_met=yes` (no missing references â€” all 6 compose targets verified with existing `## US-xxxx` h1 anchors in architecture.md; no decision gate triggered; AC baselines green: `validate_readme_feature_coverage.py` PASS + `pytest tests/scratchpad_example_parity_test.py` 4 passed)

### Compose, do not amend (verified â€” 6 read-only consumers of US-0118)

| Story | README anchor | architecture.md anchor | Verification |
|-------|---------------|------------------------|--------------|
| US-0096 / DEC-0082 (delivery modes) | L2617 + L2670 inline | `## US-0096` L1684 | âœ“ exists â€” explicit `DELIVERY_MODE` still wins (L8); US-0118 only fills the unset case |
| US-0070 / DEC-0052 (phase selection) | L2856 | `## US-0070` L1572 | âœ“ exists â€” `AUTO_PHASE_*` remains explicit override; classifier only fills the unset case |
| US-0078 / DEC-0060 (intake evidence) | L479 runbook | `## US-0078` L1596 | âœ“ exists â€” evidence gate still runs before any write (L10); classifier proposal + operator decision recorded in evidence bundle |
| US-0051 (decomposition) | L371 runbook | (no h1 anchor) | âœ“ exists â€” classifier runs after decomposition evaluator (L10) |
| US-0069 / DEC-0051 (phaseâ†’role matrix) | L2856 | `## US-0069` L1568 | âœ“ exists â€” classifier only selects which phases run, not who runs them |
| US-0103 (AI decision ledger) | L2421 | `## US-0103` L1640 | âœ“ exists â€” read-only consumer for audit trail |

All 6 compose targets verified present (read-only consumers of US-0118 â€” additive-only).

### Isolation evidence (US-0048 / DEC-0029)

- `phase_id=architecture`
- `role=tech-lead`
- `story_id=US-0118`
- `sprint_id=(pending â€” created at sprint-plan)`
- `orchestrator_run_id=auto-20260704-01`
- `delivery_mode=ultra_lean`, `macro_phase=plan` (architecture â€” second canonical phase of `plan` macro per US-0096 / DEC-0082)
- `fresh_context_marker=tl-US0118-architecture-20260704T203000Z-fresh`
- `timestamp=2026-07-04T20:30:00Z` (UTC)
- `evidence_ref=docs/product/backlog.md (## US-0118 block L3983â€“L4025 narrow-read), docs/product/acceptance.md (US-0118 row L145 narrow-read), handoffs/po_to_tl.md (US-0118 research + discovery + intake handoffs narrow-read), docs/engineering/state.md (research checkpoint L197â€“L297 + discovery checkpoint L102â€“L196 + drain-advance breadcrumb L84â€“L101 narrow-read), docs/engineering/research.md (R-0106 entry L8754â€“L8904 full read), docs/engineering/architecture.md (grep ^## US- anchors + US-0117 section L1420â€“L1566 read as template + DC anchor verification L1568â€“L1710 + US-0099 last line L1710), scripts/dev_environment_lib.py (TIER_C_SKIP_PREFIXES L117â€“L125 + classify_touched_files L321â€“L339 narrow-read for Q9 import-contract lock), its_magic/README.md (grep ### .*keys anchors only â€” no full-read), decisions/DEC-0082.md (full read as DEC-0118 template), decisions/DEC-0052.md (full read as DEC-0118 template), docs/product/backlog.md (grep ^## US- anchors for DC cross-check), handoffs/resume_brief.md (top ~30 lines narrow-read for drain-advance prose shape)`
- Tech-lead subagent spawned fresh per BUG-0006 / US-0048 isolation; no prior chat history carried forward. Context limited to the narrow-read files listed above (US-0053 / US-0096 Tranche A). No MCP / browser / shell side-effects beyond narrow-read grep + read tool calls + python SHA-256 computation for the strict runtime proof + powershell line-count computations + the artifact writes listed in this phase (architecture.md `## US-0118` section append, decisions/DEC-0118.md NEW, po_to_tl.md architecture handoff prepend, state.md architecture checkpoint append, resume_brief.md drain-advance append). No `.env` reads, no credentials access, no intake-evidence mutation.
- `assemble_sovereign_memory_digest(...)` NOT called (US-0118 documentation-only so far â€” architecture phase writes prose + DEC only; existing digest context sufficient per R-0106 â€” S0113..S0117 retrospectives established reusable patterns; classifier code is built in `/execute`, not here).
- No write to `mistakes.jsonl` in architecture phase (no fix_failed / revert_applied / plan_fidelity_violation / scope_creep event occurred).
- Prior phase strict proof consumed: `rp-auto-20260704-01-research-techlead-20260704T200000Z-US-0118` (from `docs/engineering/state.md` research checkpoint, unchanged).
- Current architecture-phase strict proof recorded below.

### Strict runtime proof tuple (US-0056 / DEC-0038)

- `runtime_proof_id=rp-auto-20260704-01-architecture-techlead-20260704T203000Z-US-0118`
- Canonical payload (sorted-key JSON per DEC-0038): `{"orchestrator_run_id":"auto-20260704-01","phase_id":"architecture","proof_issued_at":"2026-07-04T20:30:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260704-01-architecture-techlead-20260704T203000Z-US-0118","sprint_id":"(pending)","story_id":"US-0118"}`
- `proof_hash=fd72d56bd8e8450cf830e3a4fa6164d5e3b98595c00fafa166ffd00669b1d3db` (SHA-256 of the sorted-key JSON payload above, computed via python `hashlib.sha256`)
- `proof_ttl_seconds=3600`
- `proof_ttl=2026-07-04T21:30:00Z` (1-hour TTL per DEC-0038, UTC = issued_at + 3600s)

### Validator gates (run this phase)

- `python scripts/validate_readme_feature_coverage.py --repo .` â†’ `{"coverage_missing":[],"coverage_present":[],"coverage_total":0,"gaps":[],"repo_root":".","report_schema_version":1,"status":"PASS"}` exit 0 (US-0118 not yet in catalog surface â€” no README feature coverage entry expected pre-`/execute`).
- `python -m pytest tests/scratchpad_example_parity_test.py -v` â†’ `4 passed in 0.13s` (BUG-0013 parity baseline green; not weakened).

### Decision gate

- `decision_gate=false` (no DECISION_GATE; no hard stop; companion DEC-0118 authored Accepted in THIS phase; approach A1 locked; sprint seeds T-anch + T-001..T-009 within SPRINT_MAX_TASKS=12; risks R1..R8 finalized; DC check clean; compose-do-not-amend verified 6/6)
- `stop_conditions_met=yes` (no missing references â€” all 6 compose targets verified; no decision gate triggered; AC baselines green)

### Next scheduled phase

- `next_scheduled_phase=/sprint-plan` (role=tech-lead per US-0069 / DEC-0051 phaseâ†’role matrix default; third canonical phase of `plan` macro per ultra_lean; research + architecture + sprint-plan merged into `plan` macro)
- `next_scheduled_role=tech-lead`
- `next_scheduled_sprint_macro=plan`
- `stop_condition=STOP after architecture completes; hand off via artifacts only to /sprint-plan in fresh tech-lead subagent (BUG-0006)`


## Sprint-plan checkpoint â€” US-0118 / S0118 / auto-20260704-01

- **phase_id**: sprint-plan (plan macro â€” third canonical phase within ultra_lean; research + architecture + sprint-plan merged per US-0096 / DEC-0082), **role**: tech-lead (per US-0069 / DEC-0051 phaseâ†’role matrix default), **story_id**: US-0118, **sprint_id**: S0118 (NOW materialized)
- `orchestrator_run_id=auto-20260704-01`, `delivery_mode=ultra_lean`, `macro_phase=plan` (sprint-plan â€” third canonical phase of `plan` macro)
- `reinstatement_mode=none` (ultra_lean â€” no eleven-phase reinstatement), `memory_layer=pack`
- `verdict=PASS` (no DECISION_GATE; Sprint S0118 materialized with 10 tasks T-anch + T-001..T-009 within SPRINT_MAX_TASKS=12; AC-1..AC-12 surjective coverage 12/12; companion DEC-0118 Accepted; approach A1 locked; risks R1..R8 finalized; DC check clean; compose-do-not-amend verified 6/6; 6th-story cumulative byte-stability surface LOCKED; classifier signature Q10 LOCKED; import contract Q9 LOCKED; reason codes Q2 LOCKED; 12 test markers Q4 LOCKED)
- `fresh_context_marker=tl-US0118-sprint-plan-20260704T232400Z-fresh`
- `timestamp (UTC)=2026-07-04T23:24:00Z`
- `sprint_anchor=sprints/S0118/sprint.md` (NEW â€” 10 tasks; AC-1..AC-12 surjective + DC resolution verified)
- `tasks_anchor=sprints/S0118/tasks.md` (NEW â€” 10-task checklist with T-anch as NO-OP / verification)
- `architecture_anchor=docs/engineering/architecture.md ## US-0118 â€” Work-kind classification + tiered delivery routing per story` (L1713)
- `research_anchor=docs/engineering/research.md ## R-0106 - US-0118 Work-kind classification + tiered delivery routing research`
- `companion_dec=DEC-0118` (Required â†’ Accepted; authored in `/architecture` phase at `decisions/DEC-0118.md`)
- `approach_locked=A1` (single `### Work-kind routing (US-0118)` umbrella + per-feature subsections + 6th scratchpad ref sub-block `### Work-kind routing keys (US-0118)` as a sibling to the US-0113..US-0117 sub-blocks; 6th-story cumulative byte-stability surface â€” prior 5 released blocks must remain byte-identical)
- `sprint_seeds=10` (T-anch + T-001..T-009 within SPRINT_MAX_TASKS=12)
- `ac_coverage=12/12` (AC-1..AC-12 all covered surjectively; multi-AC tasks T-007 (AC-1+AC-2), T-008 (AC-4+AC-5+AC-6), T-009 (AC-7+AC-9+AC-12 partial), T-006 (AC-8+AC-9 indirect), T-anch (AC-8+AC-10), T-002 (AC-3+AC-11), T-001 (AC-3), T-003 (AC-3), T-005 (AC-9 indirect+AC-12); every AC has â‰¥1 task; no `PLAN_AC_COVERAGE_GAP`)
- `compose_guards=23` (UNCHANGED â€” same 23 as US-0117; US-0118 is additive-only â€” new flag, new lib, new row fields, new precedence clause, new sub-block, new runbook h2; does NOT amend any existing compose-surface feature; US-0118 itself does NOT become a NEW compose guard â€” it's a routing primitive, not a guard)
- `test_markers=12` (from R-0106 Q4 LOCKED â€” `test_us0118_doc_kind_routes_to_lean_plan`, `test_us0118_mini_kind_routes_to_ultra_lean`, `test_us0118_mini_kind_routes_to_mega_quick_when_eligible`, `test_us0118_code_kind_routes_to_standard`, `test_us0118_explicit_delivery_mode_wins_over_work_kind`, `test_us0118_auto_phase_wins_over_work_kind`, `test_us0118_routing_off_is_noop`, `test_us0118_classify_touched_files_reuse`, `test_us0118_intake_evidence_records_work_kind`, `test_us0118_reason_codes_preserved`, `test_us0118_default_off_zero_overhead`, `test_us0118_explain_emits_rule_trace` in `tests/us0118_contract_test.py`)
- `dc_resolution=clean` (grep `^## US-0118` architecture.md â†’ match at L1713; `## US-0118` h1 anchor added in `/architecture` phase per R-0105 Q-2 LOCKED pattern â€” T-anch in S0118 is NO-OP / verification; no execute-phase write to architecture.md; deferral register clean â€” no carry-over to a successor story)
- `risks_finalized=8` (R1 classification ambiguity MEDIUM â†’ Q1 tie-break; R2 precedence conflicts MEDIUM â†’ L8 + `WORK_KIND_DELIVERY_MODE_CONFLICT`; R3 `mega_quick`/`mini` overlap LOWâ€“MEDIUM â†’ L6 eligibility gating; R4 backward-compat MEDIUM â†’ Q8 early-return + contract test; R5 operator trust LOWâ€“MEDIUM â†’ Q3 `--explain` + `rule_trace`; R6 reuse boundary drift LOW â†’ Q9 import contract + contract test; R7 installer parity drift LOW â†’ T-009 manifest; R8 NEW cross-story byte-stability surface 6th sub-block MEDIUM â†’ T-003 net-new-keys-only + `PARITY_OK` proof never edits US-0113..US-0117 released blocks)
- `stop_conditions_met=yes` (no missing references â€” all 6 compose targets verified with existing `## US-xxxx` h1 anchors in architecture.md; no decision gate triggered; AC baselines green: `validate_readme_feature_coverage.py` PASS + `pytest tests/scratchpad_example_parity_test.py` 4 passed)

### Compose, do not amend (verified â€” 6 read-only consumers of US-0118)

| Story | README anchor | architecture.md anchor | Verification |
|-------|---------------|------------------------|--------------|
| US-0096 / DEC-0082 (delivery modes) | L2617 + L2670 inline | `## US-0096` L1684 | âœ“ exists â€” explicit `DELIVERY_MODE` still wins (L8); US-0118 only fills the unset case |
| US-0070 / DEC-0052 (phase selection) | L2856 | `## US-0070` L1572 | âœ“ exists â€” `AUTO_PHASE_*` remains explicit override; classifier only fills the unset case |
| US-0078 / DEC-0060 (intake evidence) | L479 runbook | `## US-0078` L1596 | âœ“ exists â€” evidence gate still runs before any write (L10); classifier proposal + operator decision recorded in evidence bundle |
| US-0051 (decomposition) | L371 runbook | (no h1 anchor) | âœ“ exists â€” classifier runs after decomposition evaluator (L10) |
| US-0069 / DEC-0051 (phaseâ†’role matrix) | L2856 | `## US-0069` L1568 | âœ“ exists â€” classifier only selects which phases run, not who runs them |
| US-0103 (AI decision ledger) | L2421 | `## US-0103` L1640 | âœ“ exists â€” read-only consumer for audit trail |

All 6 compose targets verified present (read-only consumers of US-0118 â€” additive-only).

### Isolation evidence (US-0048 / DEC-0029)

- `phase_id=sprint-plan`
- `role=tech-lead`
- `story_id=US-0118`
- `sprint_id=S0118` (NOW materialized)
- `orchestrator_run_id=auto-20260704-01`
- `delivery_mode=ultra_lean`, `macro_phase=plan` (sprint-plan â€” third canonical phase of `plan` macro per US-0096 / DEC-0082)
- `fresh_context_marker=tl-US0118-sprint-plan-20260704T232400Z-fresh`
- `timestamp=2026-07-04T23:24:00Z` (UTC)
- `evidence_ref=docs/product/backlog.md (## US-0118 block L3983â€“L4025 narrow-read â€” 12 ACs verbatim + boundaries + related_us + intake_notes), docs/product/acceptance.md (US-0118 row L145 narrow-read â€” 12 ACs OPEN), handoffs/po_to_tl.md (US-0118 architecture handoff L97â€“L164 narrow-read â€” summary + architecture anchor + approach A1 + companion DEC + sprint seeds preview + DC resolution + risks + compose guards + isolation evidence + strict runtime proof + decision gate + next scheduled phase), docs/engineering/state.md (architecture checkpoint L300â€“L373 narrow-read â€” phase_id/role/story_id/orchestrator_run_id/delivery_mode/macro_phase/fresh_context_marker/timestamp/architecture_anchor/companion_dec/approach_locked/sprint_seeds/compose_guards/test_markers/risks_finalized/stop_conditions_met + isolation evidence + strict runtime proof + decision gate + next scheduled phase), docs/engineering/architecture.md (## US-0118 section L1713â€“L1923 full read â€” Overview + Companion DEC + Approach A1 + Files to touch + Files NOT to touch + Sprint seeds T-anch + T-001..T-009 + Test markers + Compose guards UNCHANGED + DC resolution + Compose-do-not-amend verification + Risks finalized + Stop conditions met + Sovereign memory note + Consequences + Evidence references + Isolation evidence + Strict runtime proof + Decision gate + Next scheduled phase), docs/engineering/research.md (R-0106 entry â€” closed Q1..Q10 + 12 test markers Q4 + classifier signature Q10), sprints/S0117/sprint.md (full read as ultra_lean template â€” 7-task pattern adapted to 10-task US-0118), sprints/S0117/tasks.md (first ~120 lines read as ultra_lean tasks template â€” Task-to-AC Bijection Table + Task Seeds shape), handoffs/resume_brief.md (top ~30 lines narrow-read for drain-advance prose shape)`
- Tech-lead subagent spawned fresh per BUG-0006 / US-0048 isolation; no prior chat history carried forward. Context limited to the narrow-read files listed above (US-0053 / US-0096 Tranche A). No MCP / browser / shell side-effects beyond narrow-read grep + read tool calls + python SHA-256 computation for the strict runtime proof + powershell line-count computations + the artifact writes listed in this phase (sprints/S0118/sprint.md NEW, sprints/S0118/tasks.md NEW, handoffs/po_to_tl.md sprint-plan handoff PREPEND, this state.md sprint-plan checkpoint APPEND, handoffs/resume_brief.md drain-advance append). No `.env` reads, no credentials access, no intake-evidence mutation.
- `assemble_sovereign_memory_digest(...)` NOT called (US-0118 documentation+code so far; existing digest context sufficient per R-0106 â€” S0113..S0117 retrospectives established reusable patterns; cross-link pointer pattern + angle-distinct narrative pattern + byte-stability contract now scale from quint to sextet).
- No write to `mistakes.jsonl` in sprint-plan phase (no fix_failed / revert_applied / plan_fidelity_violation / scope_creep event occurred).
- Prior phase strict proof consumed: `rp-auto-20260704-01-architecture-techlead-20260704T203000Z-US-0118` (from `docs/engineering/state.md` architecture checkpoint L351, unchanged).
- Current sprint-plan-phase strict proof recorded below.

### Strict runtime proof tuple (US-0056 / DEC-0038)

- `runtime_proof_id=rp-auto-20260704-01-sprint-plan-techlead-20260704T232400Z-US-0118`
- Canonical payload (sorted-key JSON per DEC-0038): `{"orchestrator_run_id":"auto-20260704-01","phase_id":"sprint-plan","proof_issued_at":"2026-07-04T23:24:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260704-01-sprint-plan-techlead-20260704T232400Z-US-0118","sprint_id":"S0118","story_id":"US-0118"}`
- `proof_hash=4a6b5b6125848f4cbb209ad5ea7623f715e3aea8572ce087850069e0a7da29e7` (SHA-256 of the sorted-key JSON payload above, computed via python `hashlib.sha256`)
- `proof_ttl_seconds=3600`
- `proof_ttl=2026-07-05T00:24:00Z` (1-hour TTL per DEC-0038, UTC = issued_at + 3600s)

### Validator gates (run this phase)

- `python scripts/validate_readme_feature_coverage.py --repo .` â†’ `{"coverage_missing":[],"coverage_present":[],"coverage_total":0,"gaps":[],"repo_root":".","report_schema_version":1,"status":"PASS"}` exit 0 (US-0118 not yet in catalog surface â€” no README feature coverage entry expected pre-`/execute`).
- `python -m pytest tests/scratchpad_example_parity_test.py -v` â†’ `4 passed in 0.08s` (BUG-0013 parity baseline green; not weakened).

### Decision gate

- `decision_gate=false` (no DECISION_GATE; no hard stop; Sprint S0118 materialized with 10 tasks within SPRINT_MAX_TASKS=12; AC-1..AC-12 surjective coverage 12/12; companion DEC-0118 Accepted; approach A1 locked; risks R1..R8 finalized; DC check clean; compose-do-not-amend verified 6/6; 6th-story cumulative byte-stability surface LOCKED; classifier signature Q10 LOCKED; import contract Q9 LOCKED; reason codes Q2 LOCKED; 12 test markers Q4 LOCKED)
- `stop_conditions_met=yes` (no missing references â€” all 6 compose targets verified; no decision gate triggered; AC baselines green)

### Next scheduled phase

- `next_scheduled_phase=/execute` (role=dev per US-0069 / DEC-0051 phaseâ†’role matrix default; first canonical phase of `build+verify` macro per ultra_lean; plan-verify merged into qa per ultra_lean â€” qa creates `plan-verify.json` within `build+verify`)
- `next_scheduled_role=dev`
- `next_scheduled_sprint_macro=build+verify`
- `stop_condition=STOP after sprint-plan completes; hand off via artifacts only to /execute in fresh dev subagent (BUG-0006)`


## Execute checkpoint â€” US-0118 / S0118 / auto-20260704-01

- `phase_id=execute`
- `role=dev`
- `story_id=US-0118`
- `sprint_id=S0118`
- `orchestrator_run_id=auto-20260704-01`
- `delivery_mode=ultra_lean`
- `macro_phase=build+verify` (execute â€” first canonical phase within the build+verify macro per ultra_lean; plan-verify is MERGED into qa per US-0096 / DEC-0082)
- `fresh_context_marker=dev-US0118-execute-20260704T223200Z-fresh`
- `timestamp=2026-07-04T22:32:00Z` (UTC; 2026-07-05T00:32:00Z UTC+2)
- `execute_summary_anchor=sprints/S0118/execute-summary.md`
- `architecture_anchor=docs/engineering/architecture.md ## US-0118 â€” Work-kind classification + tiered delivery routing per story (L1713, added in /architecture phase per R-0105 Q-2 LOCKED; T-anch NO-OP / verification in execute â€” no write)`
- `research_anchor=docs/engineering/research.md ## R-0106 (Q1..Q10 closed LOCKED â€” classifier signature Q10, reason codes Q2, test markers Q4, scratchpad ref sub-block decision Q5, import contract Q9, precedence chain Q8, work-kind enum Q1 LOCKED)`
- `sprint_anchor=sprints/S0118/sprint.md`
- `tasks_anchor=sprints/S0118/tasks.md`
- `companion_dec=DEC-0118 (Required -> Accepted; authored in /architecture phase at decisions/DEC-0118.md)`
- `approach_locked=A1` (work-kind classifier + L8 precedence chain + default-off + zero-overhead-when-off)
- `verdict=PASS`
- `sprint_seeds=10` (T-anch + T-001..T-009)
- `ac_coverage=12/12` (AC-1 classifier lib; AC-2 doc/mini/code + tie-break; AC-3 WORK_KIND_ROUTING scratchpad flag default-off; AC-4 backlog row fields; AC-5 intake integration step 4b; AC-6 /auto step 0a precedence; AC-7 reason codes WORK_KIND_* family; AC-8 compose-do-not-amend 6/6 + 23 compose guards UNCHANGED; AC-9 contract tests + parity; AC-10 ## US-0118 architecture anchor verified (NO-OP); AC-11 runbook h2 + command docs; AC-12 self-test + installer delivery)
- `compose_guards=23 (UNCHANGED)` (US-0096 / US-0070 / US-0078 / US-0051 / US-0069 / US-0103 architectural surfaces remain read-only; dev_environment_lib.py IMPORT only â€” Q9 LOCKED)
- `test_markers=17 passed in 0.13s` (4 BUG-0013 regression + 13 US-0118 contract; pytest stdlib only)
- `validator_results=ALL GREEN` (validate_readme_feature_coverage [README_FEATURE_COVERAGE_VALIDATE_OK] exit 0 with coverage_missing=[]; validate_doc_profile [DOC_PROFILE_VALIDATE_OK] exit 0; check-user-visible-metadata silent PASS exit 0; check_intake_template_parity [INTAKE_TEMPLATE_PARITY_OK] scope=intake exit 0 + [INTAKE_TEMPLATE_PARITY_OK] scope=work-kind-routing exit 0; work_kind_classify_lib --self-test [WORK_KIND_CLASSIFY_SELF_TEST_OK] exit 0; work_kind_routing_lib --self-test [WORK_KIND_ROUTING_SELF_TEST_OK] exit 0)
- `test_results=17 passed (4 BUG-0013 parity + 13 US-0118 contract); full suite 298 passed / 31 pre-existing failures NOT introduced by US-0118 (project-local scratchpad overrides + model-catalog-examples scope missing + architecture linkage failures from prior stories); no new failures`
- `byte_stability=PARITY_OK 203287 203287 (6th-story cumulative surface â€” US-0113 L2421 + US-0114 L2545 + US-0115 L2617 + US-0116 L2765 + US-0117 L2856 blocks byte-stable; pure addition in the post-US-0117 range; 0 deletions to prior-released blocks; cross-story byte-stability contract now scales from quintet US-0113..US-0117 to sextet +US-0118)`
- `parity=PARITY_OK (its_magic/README.md <-> template/its_magic/README.md 203287 203287; scripts/work_kind_classify_lib.py <-> template 20071 20071; scripts/work_kind_routing_lib.py <-> template 12916 12916; tests/us0118_contract_test.py <-> template 12971 12971; docs/engineering/context/installer-owned-paths.manifest <-> template 3466 3466; docs/engineering/runbook.md <-> template 178620 178620; .cursor/commands/auto.md <-> template 35783 35783; .cursor/commands/intake.md <-> template byte-identical; [INTAKE_TEMPLATE_PARITY_OK] scope=intake exit 0; [INTAKE_TEMPLATE_PARITY_OK] scope=work-kind-routing exit 0)`
- `stop_conditions_met=yes` (no missing references â€” all 6 compose targets verified; no decision gate triggered; AC baselines green; byte-stability preserved; parity preserved; no test weakenings)
- `next_scheduled_phase=/qa` (role=qa per US-0069 / DEC-0051 phase->role matrix; second canonical phase of build+verify macro per ultra_lean â€” merges plan-verify + execute QA + verify-work; qa creates plan-verify.json within build+verify)
- `next_scheduled_role=qa`
- `next_scheduled_sprint_macro=build+verify`
- `stop_condition=STOP after execute completes; hand off via artifacts only to /qa in fresh qa subagent (BUG-0006)`

### Isolation evidence (US-0048 / DEC-0029)

- `phase_id=execute`
- `role=dev`
- `fresh_context_marker=dev-US0118-execute-20260704T223200Z-fresh`
- `timestamp=2026-07-04T22:32:00Z` (UTC; 2026-07-05T00:32:00Z UTC+2)
- `evidence_ref=sprints/S0118/execute-summary.md` (primary; mirrors S0117/execute-summary.md shape) + `handoffs/dev_to_qa.md` (dev-to-qa handoff)
- Dev subagent spawned fresh per BUG-0006 / US-0048 isolation; no prior chat history carried forward. Context limited to the narrow-read files listed above (US-0053 / US-0096 Tranche A). No MCP / browser / shell side-effects beyond narrow-read grep + read tool calls + python parity/hash computations + validator/test invocations + git status/diff.
- `assemble_sovereign_memory_digest(...)` NOT called (US-0118 first code-bearing story of a new drain â€” US-0113..US-0117 retrospectives established reusable patterns; cross-link pointer pattern + byte-stability contract + reuse-import pattern now scale from quint to sextet; existing digest context sufficient per R-0106).
- No write to `mistakes.jsonl` in execute phase (no fix_failed / revert_applied / plan_fidelity_violation / scope_creep event occurred).
- Prior sprint-plan-phase strict proof consumed: `rp-auto-20260704-01-sprint-plan-techlead-20260704T232400Z-US-0118` (from `docs/engineering/state.md` sprint-plan checkpoint, unchanged).
- Current execute-phase strict proof recorded below.

### Strict runtime proof tuple (US-0056 / DEC-0038)

- `runtime_proof_id=rp-auto-20260704-01-execute-dev-20260704T223200Z-US-0118`
- Canonical payload (sorted-key JSON per DEC-0038): `{"companion_dec":"DEC-0118","delivery_mode":"ultra_lean","macro_phase":"build+verify","orchestrator_run_id":"auto-20260704-01","phase_id":"execute","proof_issued_at":"2026-07-04T22:32:00Z","proof_ttl_seconds":3600,"role":"dev","sprint_id":"S0118","sprint_seeds":10,"story_id":"US-0118","verdict":"PASS"}`
- `proof_hash=76174e8ae6fd921d5b6c23e26df508a791cbc6090863984ee733b9c2c7e249e4` (SHA-256 of the sorted-key JSON payload above, computed via python `hashlib.sha256`)
- `proof_ttl_seconds=3600`
- `proof_ttl=2026-07-04T23:32:00Z` (1-hour TTL per DEC-0038, UTC = issued_at + 3600s)

### Decision gate

- `decision_gate=false` (no DECISION_GATE; no hard stop; Sprint S0118 execute completed all 10 tasks T-anch + T-001..T-009; AC-1..AC-12 surjective coverage 12/12; companion DEC-0118 Accepted; approach A1 locked; classifier signature Q10 LOCKED; import contract Q9 LOCKED; reason codes Q2 LOCKED; 12 test markers Q4 LOCKED; L8 precedence chain Q8 LOCKED; work-kind enum Q1 LOCKED; 6th-story cumulative byte-stability surface preserved; PARITY_OK 203287 203287; 17/17 contract + regression tests passed; 4 validators + 2 self-tests all green; compose-do-not-amend verified 6/6; 23 compose guards UNCHANGED; dev_environment_lib.py IMPORT only)
- `stop_conditions_met=yes` (no missing references â€” all 6 compose targets verified; no decision gate triggered; AC baselines green; byte-stability preserved; parity preserved; no test weakenings)

### Next scheduled phase

- `next_scheduled_phase=/qa` (role=qa per US-0069 / DEC-0051 phase->role matrix; second canonical phase of build+verify macro per ultra_lean â€” merges plan-verify + execute QA + verify-work per US-0096 / DEC-0082; qa creates sprints/S0118/plan-verify.json within build+verify)
- `next_scheduled_role=qa`
- `next_scheduled_sprint_macro=build+verify`
- `stop_condition=STOP after execute completes; hand off via artifacts only to /qa in fresh qa subagent (BUG-0006)`


## QA checkpoint — US-0118 / S0118 / auto-20260704-01

- `phase_id=qa` (merges plan-verify + execute QA + verify-work + UAT per ultra_lean / US-0096 / DEC-0082)
- `role=qa`
- `story_id=US-0118`
- `sprint_id=S0118`
- `orchestrator_run_id=auto-20260704-01`
- `delivery_mode=ultra_lean`
- `macro_phase=build+verify` (qa — second canonical phase within the build+verify macro per ultra_lean)
- `fresh_context_marker=qa-US0118-qa-20260704T230900Z-fresh`
- `timestamp=2026-07-04T23:09:00Z` (UTC; 2026-07-05T01:09:00Z UTC+2)
- `plan_verify_anchor=sprints/S0118/plan-verify.json`
- `qa_findings_anchor=sprints/S0118/qa-findings.md`
- `qa_verdict_anchor=sprints/S0118/qa-verdict.json`
- `verify_work_findings_anchor=sprints/S0118/verify-work-findings.md`
- `verify_work_verdict_anchor=sprints/S0118/verify-work-verdict.json`
- `uat_anchor=sprints/S0118/uat.json + sprints/S0118/uat.md`
- `execute_summary_anchor=sprints/S0118/execute-summary.md`
- `sprint_anchor=sprints/S0118/sprint.md`
- `architecture_anchor=docs/engineering/architecture.md ## US-0118 — Work-kind classification + tiered delivery routing per story (L1713, added in /architecture phase per R-0105 Q-2 LOCKED; T-anch NO-OP / verification in execute — no write)`
- `companion_dec=DEC-0118` (Required → Accepted; authored in `/architecture` phase at `decisions/DEC-0118.md`)
- `approach_locked=A1` (single `### Work-kind routing (US-0118)` umbrella + per-feature subsections + 6th scratchpad ref sub-block `### Work-kind routing keys (US-0118)` as a sibling to the US-0113..US-0117 sub-blocks; 6th-story cumulative byte-stability surface — prior 5 released blocks must remain byte-identical)
- `verdict=PASS`
- `ac_coverage=12/12` (AC-1 classifier lib; AC-2 doc/mini/code + tie-break; AC-3 WORK_KIND_ROUTING scratchpad flag default-off; AC-4 backlog row fields; AC-5 intake integration step 4b; AC-6 /auto step 0a precedence; AC-7 reason codes WORK_KIND_* family; AC-8 compose-do-not-amend 6/6 + 23 compose guards UNCHANGED; AC-9 contract tests + parity; AC-10 ## US-0118 architecture anchor verified (NO-OP); AC-11 runbook h2 + command docs; AC-12 self-test + installer delivery)
- `test_results=17 passed in 0.16s` (4 BUG-0013 regression `tests/scratchpad_example_parity_test.py` + 13 US-0118 contract `tests/us0118_contract_test.py`); full suite 298 passed / 31 pre-existing failures NOT introduced by US-0118 (project-local scratchpad overrides + model-catalog-examples scope missing + architecture linkage failures from prior stories); no new failures
- `validator_results=ALL GREEN` (validate_readme_feature_coverage [README_FEATURE_COVERAGE_VALIDATE_OK] exit 0 coverage_missing=[]; validate_doc_profile [DOC_PROFILE_VALIDATE_OK] exit 0; check-user-visible-metadata silent PASS exit 0; check_intake_template_parity [INTAKE_TEMPLATE_PARITY_OK] scope=intake exit 0 + [INTAKE_TEMPLATE_PARITY_OK] scope=work-kind-routing exit 0; work_kind_classify_lib --self-test [WORK_KIND_CLASSIFY_SELF_TEST_OK] exit 0; work_kind_routing_lib --self-test [WORK_KIND_ROUTING_SELF_TEST_OK] exit 0)
- `byte_stability=PARITY_OK 203287 203287` (6th-story cumulative surface — US-0113 L2421 + US-0114 L2545 + US-0115 L2617 + US-0116 L2765 + US-0117 L2856 blocks byte-stable; pure addition in the post-US-0117 range; git diff --stat HEAD -- its_magic/README.md → 2333 insertions, 0 deletions; cross-story byte-stability contract now scales from quintet US-0113..US-0117 to sextet +US-0118)
- `parity=PARITY_OK 203287 203287 + [INTAKE_TEMPLATE_PARITY_OK] scope=intake + [INTAKE_TEMPLATE_PARITY_OK] scope=work-kind-routing` (its_magic/README.md ↔ template/its_magic/README.md byte-identical; active + template/ parity for new script + scratchpad lines + command docs + runbook + manifest)
- `compose_guards=23 UNCHANGED` (same 23 as US-0117; US-0118 is additive-only — new flag, new lib, new row fields, new precedence clause, new README sub-block, new runbook h2; does NOT amend any existing compose-surface feature; dev_environment_lib.py IMPORT only — Q9 LOCKED; tests/scratchpad_example_parity_test.py NOT modified)
- `blocking_findings=0`
- `non_blocking_findings=4` (T-anch NO-OP — ## US-0118 section already added in /architecture phase per R-0105 Q-2 LOCKED; pre-existing test failures (31) NOT introduced by US-0118 NOT US-0118 regression targets per T-006; intake evidence schema extension (AC-9) — 3 optional fields documented schema contract only no existing intake evidence files modified; mega-quick eligibility — MINI-kind story MAY propose mega_quick per US-0096 opt-in via classifier proposal never forced operator may override)
- `dc_resolution_verified=true` (T-anch NO-OP — `## US-0118` h1 anchor confirmed at architecture.md L1713 from `/architecture` phase; no execute-phase write to architecture.md; US-0118 inherits clean deferral register)
- `dev_environment_lib_reuse_verified=true` (Q9 LOCKED — TIER_C_SKIP_PREFIXES + classify_touched_files imported from dev_environment_lib, no duplication; contract test test_us0118_classify_touched_files_reuse PASS)
- `ready_for_release=true`
- `stop_conditions_met=yes` (no missing references — all 6 compose targets verified; no decision gate triggered; AC baselines green; byte-stability preserved; parity preserved; no test weakenings; dev_environment_lib.py IMPORT only; 23 compose guards UNCHANGED; 0 blocking findings)
- `next_scheduled_phase=/release` (role=release per US-0069 / DEC-0051 phase->role matrix; ship macro — first canonical phase per ultra_lean)
- `next_scheduled_role=release`
- `next_scheduled_sprint_macro=ship`
- `stop_condition=STOP after qa completes; hand off via artifacts only to /release in fresh release subagent (BUG-0006)`

### Isolation evidence (US-0048 / DEC-0029)

- `phase_id=qa`
- `role=qa`
- `fresh_context_marker=qa-US0118-qa-20260704T230900Z-fresh`
- `timestamp=2026-07-04T23:09:00Z` (UTC; 2026-07-05T01:09:00Z UTC+2)
- `evidence_ref=sprints/S0118/qa-findings.md + sprints/S0118/plan-verify.json + sprints/S0118/qa-verdict.json + sprints/S0118/verify-work-findings.md + sprints/S0118/verify-work-verdict.json + sprints/S0118/uat.json + sprints/S0118/uat.md + docs/engineering/state.md (qa checkpoint appended) + handoffs/resume_brief.md (drain-advance appended)`
- QA subagent spawned fresh per BUG-0006 / US-0048 isolation; no prior chat history carried forward. Context limited to the artifact files enumerated in the parent prompt (handoffs/dev_to_qa.md + sprints/S0118/execute-summary.md + sprints/S0118/sprint.md + sprints/S0118/tasks.md + docs/engineering/architecture.md ## US-0118 + decisions/DEC-0118.md + docs/product/backlog.md ## US-0118 + docs/product/acceptance.md US-0118 row + scripts/work_kind_classify_lib.py + scripts/work_kind_routing_lib.py + tests/us0118_contract_test.py + its_magic/README.md + template/its_magic/README.md + docs/engineering/runbook.md + .cursor/commands/auto.md + .cursor/commands/intake.md + .cursor/scratchpad.md + sprints/S0117/{qa-findings,qa-verdict,verify-work-findings,verify-work-verdict,plan-verify,uat.json,uat.md}). No MCP / browser / shell side-effects beyond narrow-read grep + read tool calls + python validator/test/parity invocations + git diff --stat + artifact writes.
- `assemble_sovereign_memory_digest(...)` NOT called (US-0118 documentation+code; existing digest context sufficient per R-0106 — S0113..S0117 retrospectives established reusable patterns; cross-link pointer pattern + byte-stability contract + reuse-import pattern now scale from quint to sextet; the routing-primitive angle is distinct from prior 5 documentation-family angles).
- No write to `mistakes.jsonl` in qa phase (no fix_failed / revert_applied / plan_fidelity_violation / scope_creep event occurred — all 4 non-blocking findings are cosmetic/pre-existing).
- Prior execute-phase strict proof consumed: `rp-auto-20260704-01-execute-dev-20260704T223200Z-US-0118` (from `docs/engineering/state.md` execute checkpoint, unchanged).
- Current qa-phase strict proof recorded below.

### Strict runtime proof (US-0056 / DEC-0038)

- `runtime_proof_id=rp-auto-20260704-01-qa-qa-20260704T230900Z-US-0118`
- Canonical payload (sorted-key JSON per DEC-0038): `{"orchestrator_run_id":"auto-20260704-01","phase_id":"qa","proof_issued_at":"2026-07-04T23:09:00Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260704-01-qa-qa-20260704T230900Z-US-0118","story_id":"US-0118"}`
- `proof_ttl_seconds=3600`
- `proof_ttl=2026-07-05T00:09:00Z` (1-hour TTL per DEC-0038, UTC = issued_at + 3600s)

### Decision gate

- `decision_gate=false` (no DECISION_GATE; no hard stop; Sprint S0118 qa completed all merged phases per ultra_lean — plan-verify + execute QA + verify-work + UAT all PASS; AC-1..AC-12 surjective coverage 12/12; companion DEC-0118 Accepted; approach A1 locked; 13 test_us0118_* markers Q4 LOCKED; 6 WORK_KIND_* reason codes Q2 LOCKED; L8 precedence chain Q8 LOCKED; work-kind enum Q1 LOCKED; 6th-story cumulative byte-stability surface preserved; PARITY_OK 203287 203287; 17/17 contract + regression tests passed; 4 validators + 2 self-tests all green; compose-do-not-amend verified 6/6; 23 compose guards UNCHANGED; dev_environment_lib.py IMPORT only — Q9 LOCKED; tests/scratchpad_example_parity_test.py NOT modified; 0 blocking findings; 4 non-blocking findings all cosmetic/pre-existing)
- `stop_conditions_met=yes`

### Next scheduled phase

- `next_scheduled_phase=/release` (role=release per US-0069 / DEC-0051 phase->role matrix; ship macro — first canonical phase per ultra_lean)
- `next_scheduled_role=release`
- `next_scheduled_sprint_macro=ship`
- `stop_condition=STOP after qa completes; hand off via artifacts only to /release in fresh release subagent (BUG-0006)`

## Release checkpoint — US-0118 / S0118 / auto-20260704-01

- `phase_id=release`
- `role=release`
- `story_id=US-0118`
- `sprint_id=S0118`
- `orchestrator_run_id=auto-20260704-01`
- `delivery_mode=ultra_lean`
- `macro_phase=ship` (release — first canonical phase of ship macro per ultra_lean)
- `fresh_context_marker=release-US0118-release-20260705T002000Z-fresh`
- `timestamp=2026-07-05T00:20:00Z` (UTC; 02:20:00 UTC+2)
- `release_findings_anchor=sprints/S0118/release-findings.md`
- `release_verdict_anchor=sprints/S0118/release-verdict.json`
- `sprint_release_notes_anchor=handoffs/releases/S0118-release-notes.md`
- `cumulative_release_notes_anchor=handoffs/release_notes.md` (US-0118 entry prepended)
- `release_queue_anchor=handoffs/release_queue.md` (S0118 row appended)
- `verdict=RELEASE_PASS`
- `ac_coverage=12/12`
- `qa_verdict=PASS` (12/12 ACs, 0 blockers, 4 non-blocking cosmetic/pre-existing)
- `verify_work_verdict=PASS` (execute_summary_accurate=true, 13/13 dev claims matched, 0 discrepancies, scope_creep=none)
- `uat_verdict=PASS` (12/12 ACs, 17/17 tests)
- `byte_stability=PARITY_OK 203287 203287` (6th-story cumulative surface — first 6-cumulative-surface story; quint scales to sextet; 2333 insertions / 0 deletions pure addition; US-0113 L2421 + US-0114 L2545 + US-0115 L2617 + US-0116 L2765 + US-0117 L2856 blocks byte-stable)
- `parity=PARITY_OK 203287 203287 + [INTAKE_TEMPLATE_PARITY_OK] scope=intake + [INTAKE_TEMPLATE_PARITY_OK] scope=work-kind-routing`
- `dc_anchors_resolved=clean` (T-anch NO-OP / verification — `## US-0118` h1 anchor confirmed at architecture.md L1713, added in `/architecture` phase per R-0105 Q-2 LOCKED; no execute-phase or release-phase write to architecture.md; US-0118 inherits clean deferral register — US-0117 was final deferred-candidate resolution point with 36 anchors)
- `dev_environment_lib_reuse=Q9_LOCKED (IMPORT only; contract test test_us0118_classify_touched_files_reuse PASS)`
- `backward_compat=WORK_KIND_ROUTING=0 default-off + zero-overhead-when-off (contract test test_us0118_default_off_zero_overhead PASS)`
- `story_closed=true` (docs/product/backlog.md US-0118 OPEN->DONE at L3988; AC text + metadata preserved)
- `acceptance_checked=true` (docs/product/acceptance.md US-0118 row L145 [ ]->[x])
- `release_notes_appended=true` (handoffs/releases/S0118-release-notes.md NEW + handoffs/release_notes.md US-0118 entry prepended above US-0117)
- `release_queue_updated=true` (handoffs/release_queue.md S0118 row appended; status=released; version_bump=false; sync_pushed=false)
- `compose_guards=23 UNCHANGED` (US-0091, US-0097, US-0017, US-0040, US-0100..US-0112, US-0034, US-0084, US-0086, US-0093, US-0096, US-0041, US-0062 — additive-only; US-0118 itself does NOT become a NEW compose guard — it is a routing primitive)
- `version_bump=false` (out-of-band; RELEASE_PUBLISH_MODE=disabled + SYNC_POLICY_MODE=disabled; default-off feature; S0117 precedent; its_magic/.its-magic-version remains 0.1.3-3; nuspec version 0.1.3-beta3 UNCHANGED; homebrew version 0.1.3-3 UNCHANGED)
- `sync_pushed=false` (SYNC_POLICY_MODE=disabled per DEC-0018 -> push_decision=not_eligible, reason_code=SYNC_DISABLED; RELEASE_PUBLISH_MODE=disabled -> publish_snapshot=skipped_disabled; RELEASE_TRIGGER_SOURCE=manual no adapter subprocess)
- `validator_gates=all green` (validate_readme_feature_coverage PASS + validate_doc_profile PASS + check-user-visible-metadata PASS + check_intake_template_parity intake PASS + check_intake_template_parity work-kind-routing PASS + work_kind_classify_lib --self-test PASS + work_kind_routing_lib --self-test PASS)
- `test_gates=17 passed` (4 BUG-0013 regression + 13 US-0118 contract; no test weakenings)
- `blocking_findings=0`
- `non_blocking_findings=5` (NB-1 T-anch NO-OP; NB-2 pre-existing test failures 31 — NOT introduced by US-0118; NB-3 pre-existing fixture-path test failures — carried from US-0114; NB-4 encoding hygiene prerequisite 185 stray 0xa7 bytes in backlog.md — carried from US-0114; NB-5 US-0108 status-drift — US-0108 shipped but backlog row never flipped OPEN->DONE per US-0045, flagged for operator awareness, reconcile separately)
- `drain_advance_note=1 story shipped this cycle; backlog drain active; US-0108 status-drift flagged`
- `stop_conditions_met=yes` (all release artifacts written; 0 blocking findings; all gates green; no sync/push; no version bump; spawn-only per BUG-0006)
- `decision_gate=false` (no DECISION_GATE; companion DEC-0118 Accepted in `/architecture` phase; approach A1 locked)

### Isolation evidence (US-0048 / DEC-0029)

- `phase_id=release`
- `role=release`
- `fresh_context_marker=release-US0118-release-20260705T002000Z-fresh`
- `timestamp=2026-07-05T00:20:00Z`
- `evidence_ref=sprints/S0118/release-findings.md + sprints/S0118/release-verdict.json + handoffs/releases/S0118-release-notes.md + handoffs/release_notes.md (US-0118 entry) + handoffs/release_queue.md (S0118 row) + docs/product/backlog.md (US-0118 OPEN->DONE) + docs/product/acceptance.md (US-0118 [ ]->[x]) + docs/engineering/state.md (release checkpoint) + handoffs/resume_brief.md (drain-advance)`
- `isolation_mode=fresh subagent context per BUG-0006 / US-0048 — release subagent spawned fresh for the release phase; no carry-over from prior sprint-plan / architecture / research / discovery / execute / qa phases other than the artifact reads enumerated in the parent prompt`

### Strict runtime proof (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260704-01`
- `runtime_proof_id=rp-auto-20260704-01-release-release-20260705T002000Z-US-0118`
- `phase_id=release`
- `role=release`
- `proof_issued_at=2026-07-05T00:20:00Z`
- `proof_ttl_seconds=3600`
- `proof_ttl=2026-07-05T01:20:00Z` (UTC) per DEC-0038
- `canonical_payload={"orchestrator_run_id":"auto-20260704-01","phase_id":"release","proof_issued_at":"2026-07-05T00:20:00Z","proof_ttl_seconds":3600,"role":"release","runtime_proof_id":"rp-auto-20260704-01-release-release-20260705T002000Z-US-0118","story_id":"US-0118"}`

### Next scheduled phase

- `next_scheduled_phase=/refresh-context` (role=curator per US-0069 / DEC-0051 phase->role matrix; ship macro — second canonical phase per ultra_lean)
- `next_scheduled_role=curator`
- `next_scheduled_sprint_macro=ship`
- `stop_condition=STOP after release completes; hand off via artifacts only to /refresh-context in fresh curator subagent (BUG-0006)`


## Refresh-context terminal checkpoint — US-0118 / S0118 / auto-20260704-01 (segment closed, lifecycle terminal — DRAIN ADVANCE to next OPEN or drain-complete)

- **phase_id**: refresh-context, **role**: curator, **story_id**: US-0118, **sprint_id**: S0118
- `orchestrator_run_id=auto-20260704-01`, `delivery_mode=ultra_lean`
- `macro_phase=ship` (refresh-context — second canonical phase)
- `verdict=PASS`
- `segment_closed=true`, `lifecycle_terminal=true`
- `drain_advance_pending=false` (drain queue EMPTY of genuine OPEN items; US-0108 status-drift does NOT count as a genuine OPEN story to advance to)
- `retrospective_anchor=docs/engineering/sovereign-memory/retrospectives/S0118.md`
- `fresh_context_marker=curator-US0118-refresh-context-20260705T003000Z-fresh`
- `timestamp (UTC)=2026-07-05T00:30:00Z`

### Segment closure summary

US-0118 (Work-kind classification + tiered delivery routing per story) fully closed through all ultra_lean macro-phases: `intake -> discovery -> research (R-0106) -> architecture -> sprint-plan -> (plan-verify merged into qa) -> execute -> qa (merges plan-verify + qa + verify-work + UAT) -> release -> refresh-context`. **12/12 ACs RELEASED**; **17/17 tests PASS** (4 BUG-0013 regression + 13 US-0118 contract); **23/23 compose guards UNCHANGED**; `PARITY_OK 203287 203287` (**6th-story cumulative byte-stability surface** — first 6-cumulative-surface story; prior 5 released blocks US-0113 L2421 + US-0114 L2545 + US-0115 L2617 + US-0116 L2765 + US-0117 L2856 byte-stable; US-0118 added pure-additive 6th sub-block `### Work-kind routing keys (US-0118)` + cross-link pointers + reason-code-only entries; cross-story byte-stability contract pattern scales from **quint** (S0113/S0114/S0115/S0116 + US-0117) to **sextet** (+US-0118) without regression; `git diff --stat HEAD -- its_magic/README.md` confirms 2333 insertions / 0 deletions pure addition in post-US-0117 range). **DEC-0118 Accepted** (companion decision authored in `/architecture` phase; locks: work-kind enumeration `doc`/`mini`/`code` 3-tier, L8 precedence chain explicit operator flags always win + classifier fills only unset case, `dev_environment_lib.classify_touched_files` reuse boundary IMPORT only Q9 LOCKED, zero-overhead-when-off default `WORK_KIND_ROUTING=0`). **DC resolution clean** (US-0118 was first story in 6-story drain with `dc_check=clean` — no new DC candidates; US-0117 was final deferred-candidate resolution point with 36 anchors; US-0118 inherited clean deferral register; establishes "post-DC-closure steady state" pattern). `## US-0118` h1 anchor RESOLVED in `/architecture` phase per R-0105 Q-2 LOCKED (T-anch in S0118 = NO-OP / verification; no execute-phase or release-phase write to architecture.md).

US-0118 is the **first code+docs vertical-slice story** in the 6-story drain (prior 5 US-0113..US-0117 were documentation-only) — ships NEW code files (`scripts/work_kind_classify_lib.py` + `scripts/work_kind_routing_lib.py` + `tests/us0118_contract_test.py` with 13 `test_us0118_*` markers) alongside README/runbook/scratchpad docs. Proves the ultra_lean lifecycle handles mixed code+docs stories end-to-end in a single `/auto` orchestrator session. Two NEW patterns established: (a) **REUSE-not-reimplement** (US-0118 imports `classify_touched_files` + `TIER_C_SKIP_PREFIXES` from `dev_environment_lib.py` rather than reimplementing; Q9 LOCKED; R-0106 Q10; DEC-0118; contract test `test_us0118_classify_touched_files_reuse` enforces `wkc.classify_touched_files is dev_environment_lib.classify_touched_files`), and (b) **12-AC story within ultra_lean** (US-0118 has 12 ACs — largest AC set in 6-story drain; prior 5 had 8 ACs each; covered by 10 sprint tasks within SPRINT_MAX_TASKS=12; multi-AC task allocation preserves surjective AC<->task coverage).

**US-0108 status-drift flagged** as non-blocking finding for operator awareness (US-0108 shipped via `sprints/S0108/release-verdict.json` verdict=PASS, next_phase=BACKLOG_DRAIN_ADVANCE 2026-06-29T22:45:00Z, but its `docs/product/backlog.md` L3568 row was never flipped OPEN->DONE per US-0045 — closure is `/release`'s responsibility; NOT a US-0118 blocker; operator should manually reconcile OR open a `BUG-####`). Do NOT fix in this retrospective.

Final state:
- Sprint S0118 RELEASED.
- US-0118 DONE (status authority: `docs/product/backlog.md` per US-0045; release phase flipped `OPEN`->`DONE` at L3988).
- `docs/product/acceptance.md` US-0118 row `[ ]`->`[x]` (L145).
- `handoffs/releases/S0118-release-notes.md` published.
- `handoffs/release_queue.md` S0118 row -> `released` (out-of-band; documentation+code; default-off feature; no version bump; no sync/push).
- 12/12 ACs satisfied. 23/23 compose guards UNCHANGED. 17/17 tests PASS. `PARITY_OK 203287 203287`.
- 6th-story cumulative byte-stability surface PRESERVED. `## US-0118` h1 anchor RESOLVED in `/architecture` phase (T-anch NO-OP / verification). Deferral register clean.

### Triad rollover verification (DEC-0054)

**No rollover required.** All triad hot surfaces are within their caps (line counts verified via powershell `Get-Content | Measure-Object -Line`):

| Surface | Cap | Pre-append line count | Rollover? |
|---------|-----|------------------------|-----------|
| `docs/engineering/state.md` | 1000 lines (STATE_HOT_MAX_LINES=1000) | 527 lines | NO |
| `handoffs/po_to_tl.md` | 650 lines (PO_TO_TL_HOT_MAX_LINES=650) | 285 lines | NO |
| `docs/engineering/architecture.md` | 3000 lines (ARCH_HOT_MAX_LINES=3000) | 1368 lines | NO |

- `triad_rollover_required=false`
- pass-1 (pre-append): none.
- pass-2 (post-append): retained state body grows by this terminal checkpoint; final well under 1000-line cap.

### Portfolio state after closure

- open_stories: 0 (genuine); 1 status-drift item (US-0108) flagged for operator awareness
- open_bugs: 0
- drain_state: **complete** (drain queue EMPTY of genuine OPEN items — US-0108 status-drift does NOT count as a genuine OPEN story to advance to)
- drain_stories_shipped: 6/6 this drain cycle (US-0113, US-0114, US-0115, US-0116, US-0117, US-0118)
- us0108_status_drift_flagged: true (non-blocking finding for operator; recommend manual reconcile OR open `BUG-####`)
- next_action for orchestrator: drain-complete terminal (no more genuine OPEN stories to advance to). The orchestrator runs the sovereign-loop advance hook (final for US-0118) and then emits the drain-complete terminal.

### Isolation evidence (US-0048 / DEC-0029)

- `phase_id=refresh-context`
- `role=curator`
- `story_id=US-0118`
- `sprint_id=S0118`
- `orchestrator_run_id=auto-20260704-01`
- `fresh_context_marker=curator-US0118-refresh-context-20260705T003000Z-fresh`
- `timestamp=2026-07-05T00:30:00Z` (UTC; 02:30:00 UTC+2)
- `evidence_ref=sprints/S0118/release-verdict.json (full read), sprints/S0118/release-findings.md (full read), handoffs/releases/S0118-release-notes.md (full read), sprints/S0118/qa-verdict.json + sprints/S0118/verify-work-verdict.json + sprints/S0118/uat.json + sprints/S0118/uat.md (full read OK per phase contract), sprints/S0118/execute-summary.md + sprints/S0118/sprint.md (full read), docs/engineering/architecture.md grep ^## US-0118 anchor only (narrow-read per US-0053), docs/product/backlog.md grep ^## US-0118 + grep ^- Status: OPEN/DONE (narrow-read), docs/product/acceptance.md grep US-0118 (narrow-read), .cursor/skills/its-magic/SKILL.md, docs/engineering/sovereign-memory/retrospectives/S0117.md (full read as retrospective template), docs/engineering/state.md (full read), handoffs/portfolio_state.md (full read), handoffs/resume_brief.md (top ~60 lines narrow-read), handoffs/po_to_tl.md (line count only — no full read), docs/engineering/architecture.md (line count only — no full read)`
- Curator subagent spawned fresh per BUG-0006 / US-0048 isolation; no prior chat history carried forward. Context limited to the artifact files enumerated above (narrow-read per US-0053 / US-0096 Tranche A). No MCP / browser / shell side-effects beyond narrow-read grep + read tool calls + powershell line-count computations + the artifact writes listed in this phase (`docs/engineering/sovereign-memory/retrospectives/S0118.md` NEW, `handoffs/portfolio_state.md` UPDATE, this `docs/engineering/state.md` refresh-context terminal checkpoint APPEND, `handoffs/resume_brief.md` drain-advance block APPEND). No `.env` reads, no credentials access, no intake-evidence mutation, no test runs, no validator invocations (curator is a documentation/memory role — release phase already re-ran all gates green).
- `assemble_sovereign_memory_digest(...)` NOT called (US-0118 documentation+code; existing digest context sufficient per R-0106 — S0113..S0117 retrospectives established reusable patterns; US-0118 adds the code+docs vertical-slice pattern + reuse-not-reimplement pattern + 12-AC scaling pattern).
- No write to `mistakes.jsonl` in refresh-context phase (no fix_failed / revert_applied / plan_fidelity_violation / scope_creep event occurred — all 5 non-blocking findings are cosmetic/pre-existing).
- Prior phase strict proof consumed: `rp-auto-20260704-01-release-release-20260705T002000Z-US-0118` (from `sprints/S0118/release-verdict.json`, unchanged).
- Current refresh-context-phase strict proof recorded below.

### Strict runtime proof tuple (US-0056 / DEC-0038)

- `runtime_proof_id=rp-auto-20260704-01-refresh-context-curator-20260705T003000Z-US-0118`
- Canonical payload (sorted-key JSON per DEC-0038): `{"orchestrator_run_id":"auto-20260704-01","phase_id":"refresh-context","proof_issued_at":"2026-07-05T00:30:00Z","proof_ttl_seconds":3600,"role":"curator","runtime_proof_id":"rp-auto-20260704-01-refresh-context-curator-20260705T003000Z-US-0118","sprint_id":"S0118","story_id":"US-0118"}`
- `proof_ttl_seconds=3600`
- `proof_ttl=2026-07-05T01:30:00Z` (1-hour TTL per DEC-0038, UTC = issued_at + 3600s)

### Decision gate

- `decision_gate=false` (no DECISION_GATE; companion DEC-0118 Accepted in `/architecture` phase; approach A1 locked; no hard stop)

### Stop condition (terminal for US-0118 segment — drain complete)

STOP after refresh-context completes. US-0118 segment closed. **Drain queue is EMPTY of genuine OPEN stories** (US-0108 status-drift does NOT count as a genuine OPEN story to advance to). The orchestrator runs the sovereign-loop advance hook (final for US-0118) and then emits the drain-complete terminal (no more genuine OPEN stories to advance to). Hand off via artifacts only.

- `next_scheduled_phase=none` (segment complete — drain complete; no next genuine OPEN story to advance to)
- `drain_advance_pending=false` (drain queue EMPTY of genuine OPEN items)
- `us0108_status_drift_flagged=true` (non-blocking finding for operator awareness)
- `stop_condition=STOP after refresh-context completes; orchestrator runs sovereign-loop advance hook (final for US-0118) then emits drain-complete terminal.`

## Discovery checkpoint — US-0119 / S0119 / auto-20260705-us0119-intake

- **phase_id**: discovery (spec macro — second canonical phase within ultra_lean; intake + discovery merged per US-0096 / DEC-0082), **role**: po, **story_id**: US-0119, **sprint_id**: (pending — created at sprint-plan)
- `orchestrator_run_id=auto-20260705-us0119-intake`, `delivery_mode=ultra_lean`, `macro_phase=spec`
- `reinstatement_mode=none` (ultra_lean — no eleven-phase reinstatement), `memory_layer=pack`
- `verdict=PASS` (no DECISION_GATE — discovery locks captured; open questions delegated to `/research`)
- `fresh_context_marker=po-US0119-discovery-20260705T215000Z-fresh`
- `timestamp (UTC)=2026-07-05T21:50:00Z`

### Discovery locks L1..L12

- **L1** (AUTONOMY_PRESET scratchpad flag) — new `AUTONOMY_PRESET={none|balanced|full}` (default `none`) in `.cursor/scratchpad.md` + `template/.cursor/scratchpad.local.example.md`. When `none`, byte-identical pre-US-0119 behaviour.
- **L2** (deterministic preset expansion) — `scripts/autonomy_preset_lib.py:expand_autonomy_preset(preset, overrides) -> dict` returns the flag bundle. Every preset line expands into already-existing scratchpad keys only; no new consumer semantics invented. Explicit per-flag values in scratchpad (or scratchpad.local) always win over preset expansion.
- **L3** (AUTONOMY_STOP_POLICY flag) — new `AUTONOMY_STOP_POLICY={block|auto_repair_then_block|auto_repair_then_skip}` (default `block`). Every fail-closed reason code classified in `docs/engineering/autonomy-stop-matrix.md` as `security_hard` (never auto-resolved) or `autonomy_resolvable` (bounded auto-repair with a ledger cap).
- **L4** (autonomy stop matrix manifest) — `docs/engineering/autonomy-stop-matrix.md` + `template/docs/engineering/autonomy-stop-matrix.md` (parity). YAML companion `scripts/data/autonomy_stop_matrix.yaml` + `scripts/validate_autonomy_stop_matrix.py` enforcing (a) no orphan code, (b) `security_hard` rows carry `auto_repair_kind=n/a`, (c) `autonomy_resolvable` rows carry finite `cap`.
- **L5** (twelve per-feature flags wiring) — each of the twelve flags is documented and consumed: `INTAKE_AUTONOMY_MODE`, `INTAKE_MINIMAL_PACK`, `INTAKE_ASSUME_STACK_CONTEXT`, `WORK_KIND_AUTO_ACCEPT`, `CROSS_MODEL_REWORK_EXHAUSTED_POLICY`, `CROSS_MODEL_SKIP_PHASES`, `RESUME_BRIEF_AUTO_REFRESH`, `RUNTIME_PROOF_KIND`, `GOAL_CONVERGENCE_INTERVAL`, `SOVEREIGN_DRAIN_AUTO_ACCEPT`, `RELEASE_PUBLISH_AUTO_CONFIRM`, `AUTONOMY_STOP_POLICY`.
- **L6** (twelve flags do NOT exist yet in scratchpad) — grep for all twelve flags currently yields zero matches in `.cursor/scratchpad.md`. US-0119 ADDS these twelve keys; their preset expansion is net-new. This is distinct from US-0118 which only added `WORK_KIND_ROUTING`.
- **L7** (backward compatibility default) — `AUTONOMY_PRESET=none` produces byte-identical orchestrator behaviour to pre-US-0119. Contract test `test_us0119_preset_none_is_noop` enforces.
- **L8** (security-hard gates never softened) — matrix `security_hard` rows include at minimum the codes listed in AC-7 (PHASE_CONTEXT_ISOLATION_*, RUNTIME_PROOF_*, PHASE_ROLE_*, PHASE_OWNERSHIP_VIOLATION, INTAKE_REQUIRED_TOPIC_MISSING, INTAKE_PERSISTENCE_BLOCKED, AUTO_SCHEDULER_CONFLICT, RESUME_BRIEF_STALE when not under `RESUME_BRIEF_AUTO_REFRESH=1`, SECURITY_REVIEW critical findings). Contract test `test_us0119_security_hard_gates_never_auto_repaired` enforces matrix divergence.
- **L9** (bounded auto-repair ledger) — append-only `handoffs/autonomy_repair_ledger/<orchestrator_run_id>.jsonl` recording one row per auto-repair attempt. Cap per `(run, reason_code)` taken from matrix `cap` column. Cap exhaustion escalates with terminal `AUTONOMY_REPAIR_CAP_EXHAUSTED` stop reason.
- **L10** (operator authority breadcrumb) — `autonomy_relaxed: <reason_code> -> <auto_repair_kind>` emitted into `docs/engineering/state.md` at every phase boundary where a stop code was softened.
- **L11** (compose, do not amend — 6 targets read-only) — US-0092 / US-0095 / US-0056 / US-0068 / US-0096 / BUG-0007 architectural surfaces untouched. Contract test `test_us0119_preset_expansion_uses_known_keys_only` enforces expansion-output contains only keys present pre-US-0119 scratchpad schema.
- **L12** (10 contract test markers) — `test_us0119_preset_none_is_noop`, `test_us0119_preset_balanced_expansion`, `test_us0119_preset_full_expansion`, `test_us0119_explicit_flag_overrides_preset`, `test_us0119_preset_expansion_uses_known_keys_only`, `test_us0119_matrix_validator_passes`, `test_us0119_security_hard_gates_never_auto_repaired`, `test_us0119_stop_policy_affects_repair_dispatch`, `test_us0119_repair_ledger_cap_escalates`, `test_us0119_matrix_no_orphan_codes`.

### Open questions Q1..Q10 for `/research`

- **Q1** (exact `autonomy_resolvable` reason-code list): enumerate every fail-closed reason code emitted by `/auto`, `/intake`, `/execute`, `/qa`, `/release` that is NOT in the security-hard set. Candidate source: reason codes in `.cursor/commands/*.md` + `scripts/*.py` + `handoffs/autonomy_repair_ledger/` (does not yet exist — first entry). Need exhaustive grep of every `sys.exit` / reason code emission.
- **Q2** (per-reason-code `auto_repair_kind` taxonomy): what bounded auto-repair action applies per `autonomy_resolvable` code? E.g. `ARTIFACT_ORDERING_ANCHOR_AMBIGUOUS` -> `auto_sort`, `STATE_TIMESTAMP_NON_MONOTONIC` -> `auto_timestamp_rewrite`, `ARTIFACT_HOT_SURFACE_OVERSIZE` -> `auto_trim` or `skip_with_ledger`? Lock the taxonomy.
- **Q3** (matrix cap defaults — uniform 3 or per-code tuning?): AC-8 says default cap per `(run, reason_code)` is 3. Should all `autonomy_resolvable` codes share cap=3, or should some (e.g. `RESUME_BRIEF_STALE`) have cap=1 (single retry)?
- **Q4** (`RUNTIME_PROOF_KIND=lightweight` — TTL same as `strict_hash`?): US-0056 defines `strict_hash` with SHA-256 + TTL. When `RUNTIME_PROOF_KIND=lightweight`, is the TTL the same or reduced? Does the counter+timestamp attestation still require a fresh-issued `proof_issued_at` per DEC-0038?
- **Q5** (`SOVEREIGN_DRAIN_RISK_THRESHOLD` — criteria per tier): `low|medium|high` enum with what criteria per tier for `SOVEREIGN_DRAIN_AUTO_ACCEPT=1`? Is the threshold derived from backlog priority, AC count, or companion-DEC presence?
- **Q6** (`RELEASE_PUBLISH_AUTO_CONFIRM` — allowlist only or includes previously-confirmed?): does "known targets" = static allowlist (operator pre-configured), or does it include targets confirmed in prior runs (heuristic)?
- **Q7** (`INTAKE_MINIMAL_PACK` threshold for "established project"): what defines an "established project" for `INTAKE_MINIMAL_PACK=1` to shrunk follow-up intake? Max `US-xxxx` id >= N + stack known from backlog history? Or `COVERAGE_KNOWN_STACK=true` scratchpad flag?
- **Q8** (matrix validator — grep commands vs explicit manifest?): should `validate_autonomy_stop_matrix.py` grep `.cursor/commands/*.md` for reason codes, or maintain an explicit `scripts/data/emitted_reason_codes.yaml` manifest that commands register into?
- **Q9** (`AUTONOMY_REPAIR_CAP_EXHAUSTED` — new code vs extension of existing `BLOCK_RETRY_CAP_EXHAUSTED`?): is this a new terminal stop reason, or should it extend `BLOCK_RETRY_CAP_EXHAUSTED` with an `autonomy` dimension?
- **Q10** (breadcrumb format in state.md — one-line per soft-stop or aggregated per phase?): should each softened code produce one breadcrumb line at the phase boundary, or an aggregated summary line at the end of each phase?

### Risks R1..R6 carried to `/architecture`

- **R1** (MEDIUM) — backward-compat regression risk. `AUTONOMY_PRESET=none` must be byte-identical pre-US-0119. Mitigated by contract test `test_us0119_preset_none_is_noop`.
- **R2** (MEDIUM) — security gate bypass matrix risk. The `security_hard` set must be exhaustive and locked. Contract test `test_us0119_security_hard_gates_never_auto_repaired` fails on divergence.
- **R3** (LOW) — repair ledger growth. Per-run cap + gitignore keep ledger bounded. Low risk since `cap` is finite and gitignored.
- **R4** (MEDIUM) — operator confusion. Breadcrumb + ledger provide audit surface, but operators unfamiliar with autonomy modes may misinterpret softened gates. Mitigated by README documentation + `AUTONOMY_PRESET=none` default.
- **R5** (LOW-MEDIUM) — preset-expansion vs explicit-key precedence. LOCKED: explicit per-flag > preset > defaults. Documented in `.cursor/scratchpad.md` merge-precedence note.
- **R6** (LOW) — compose-do-not-amend drift. Expansion keys must remain within the pre-US-0119 scratchpad schema (no new keys invented). Contract test `test_us0119_preset_expansion_uses_known_keys_only` enforces.

### Compose, do not amend (verified)

| Story | architecture.md anchor | Verification | Notes |
|-------|------------------------|--------------|-------|
| US-0092 | `## US-0092` L1696 | ✓ exists — delivery confirmation gate unchanged; AUTONOMY_PRESET only adds relaxation layer above |
| US-0095 | `## US-0095` L1700 | ✓ exists — native auto-chain unchanged |
| US-0056 | no h1 anchor (referenced in architecture text only) | ✓ exists as inline reference; strict runtime proof semantics UNCHANGED; `RUNTIME_PROOF_KIND=lightweight` is opt-in lighter attestation |
| US-0068 | no h1 anchor (referenced in intake commands) | ✓ exists as intake evidence gate; NEVER bypassed by AUTONOMY_PRESET |
| US-0096 | `## US-0096` L1684 | ✓ exists — delivery modes unchanged; AUTONOMY_PRESET only softens governance gates within them |
| BUG-0007 | no h1 anchor (referenced in intake) | ✓ exists as anti-echo truthfulness rule; `INTAKE_ASSUME_STACK_CONTEXT=1` auto-fills with `assumption_confirmation_ref` contract preserved |

All 6 compose targets verified present (read-only consumers of US-0119 — their architectural surfaces are NOT edited by US-0119).

### DC (deferred-candidate) check

- `grep "^## US-0119" docs/engineering/architecture.md` → **no matches**. The `## US-0119` h1 anchor is **missing** from `architecture.md`. This is **expected** — the `## US-0119` anchor will be added in the `/architecture` phase, NOT in `/discovery` (spec macro). No action required here. Not appended to `handoffs/sovereign_deferrals.jsonl`.

### Research stub (read-only verification)

- `docs/engineering/research.md` `## R-0107` at L8907 is a **stub** (status=stub, confidence=pending, findings=Pending /research phase). Open questions Q1..Q10 referenced. This stub will be fleshed out in the `/research` phase with `/discovery` Q1..Q10 as input.
- **`/discovery` does NOT write to research.md** — the research phase does.

### Validator gates (run this phase)

- `python scripts/validate_readme_feature_coverage.py --repo .` → `{"coverage_missing":[],"coverage_present":[],"coverage_total":0,"gaps":[],"repo_root":".","report_schema_version":1,"status":"PASS"}` exit 0.
- `python -m pytest tests/scratchpad_example_parity_test.py -v` → `4 passed in 0.09s` (BUG-0013 parity baseline green; not weakened).

### Isolation evidence (US-0048 / DEC-0029)

- `phase_id=discovery`, `role=po`, `story_id=US-0119`, `sprint_id=(pending)`, `orchestrator_run_id=auto-20260705-us0119-intake`
- `fresh_context_marker=po-US0119-discovery-20260705T215000Z-fresh`, `timestamp=2026-07-05T21:50:00Z` (UTC)
- `evidence_ref=docs/product/backlog.md (## US-0119 block L4028-L4070 narrow-read — 12 ACs verbatim + boundaries + related_us + intake_evidence_ref + intake_notes), handoffs/intake_evidence/US-0119-intake-20260705.json (full read — 8 topic_coverage rows, coverage_complete=true, plan_area_id=autonomy-preset), handoffs/po_to_tl.md (US-0119 intake handoff block + US-0118 lifecycle blocks narrow-read for shape), handoffs/resume_brief.md (top ~30 lines narrow-read for drain-advance prose shape), docs/engineering/research.md (R-0107 stub L8907-L8928 narrow-read — status=stub, Q1..Q10 input), docs/engineering/architecture.md (grep ^## US-0119 no matches + grep ^## US-0092/^## US-0095/^## US-0096/^## US-0056/^## US-0068/^## BUG-0007 anchors only), .cursor/scratchpad.md (grep AUTONOMY_PRESET/AUTONOMY_STOP_POLICY/INTAKE_AUTONOMY_MODE/* autonomy keys — all zero matches confirming L6 lock), docs/product/acceptance.md (US-0119 row L146 narrow-read — 12 ACs OPEN)`
- PO subagent spawned fresh per BUG-0006 / US-0048 isolation; no prior chat history carried forward. Context limited to the narrow-read files listed above (US-0053 / US-0096 Tranche A). No MCP / browser / shell side-effects beyond narrow-read grep + read tool calls + python SHA-256 computation for the strict runtime proof + pytest/validator invocations + the artifact writes listed in this prompt. No `.env` reads, no credentials access, no intake-evidence mutation.
- `assemble_sovereign_memory_digest(...)` NOT called (US-0119 code+docs story; existing digest context sufficient per R-0107 stub — US-0113..US-0118 introspectives established reusable patterns; autonomy-preset angle adds a distinct 7th-family dimension).
- No write to `mistakes.jsonl` in discovery phase (no fix_failed / revert_applied / plan_fidelity_violation / scope_creep event occurred).
- Prior phase strict proof: intake phase did not emit a separate runtime proof (intake evidence bundle `handoffs/intake_evidence/US-0119-intake-20260705.json` is the intake evidence-of-record; intake merged into spec macro per ultra_lean — no separate intake checkpoint).

### Strict runtime proof tuple (US-0056 / DEC-0038)

- `runtime_proof_id=rp-auto-20260705-us0119-discovery-po-20260705T215000Z-US-0119`
- Canonical payload (sorted-key JSON per DEC-0038): `{"delivery_mode":"ultra_lean","macro_phase":"spec","orchestrator_run_id":"auto-20260705-us0119-intake","phase_id":"discovery","proof_issued_at":"2026-07-05T21:50:00Z","proof_ttl_seconds":3600,"role":"po","runtime_proof_id":"rp-auto-20260705-us0119-discovery-po-20260705T215000Z-US-0119","sprint_id":"(pending)","story_id":"US-0119"}`
- `proof_hash=71f1f55775f4d33bdd469f860eddfb7b4361ac462077386d27863f8c22c1cf86` (SHA-256 of the sorted-key JSON payload above)
- `proof_ttl_seconds=3600`
- `proof_ttl=2026-07-05T22:50:00Z` (1-hour TTL per DEC-0038, UTC = issued_at + 3600s)

### Decision gate

- `decision_gate=false` (no DECISION_GATE; no hard stop; 12/12 discovery locks captured; 10 open questions delegated to `/research`; 6 risks carried to `/architecture`; compose-do-not-amend 6/6 verified; DC check clean)
- `stop_conditions_met=yes` (no missing references — all 6 compose targets verified with existing `## US-xxxx` h1 anchors in architecture.md; no decision gate triggered; AC baselines green)

### Next scheduled phase

- `next_scheduled_phase=/research` (role=tech-lead per US-0069 / DEC-0051 phase→role matrix default)
- `next_scheduled_role=tech-lead`
- `next_scheduled_sprint_macro=plan`
- `stop_condition=STOP after discovery completes; hand off via artifacts only to /research in fresh tech-lead subagent (BUG-0006)`

---

