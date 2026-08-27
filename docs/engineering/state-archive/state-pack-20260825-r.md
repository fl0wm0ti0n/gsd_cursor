# State archive pack (2026-08-25)

- Rollover trigger: `STATE_HOT_MAX_LINES=1200, STATE_HOT_MAX_CHECKPOINTS=80`
- Source: `docs/engineering/state.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 25
- First archived heading: `## Research checkpoint — US-0126 / auto-20260825-01`
- Last archived heading: `## Research checkpoint — US-0126 / auto-20260825-01`
- Verification tuple (mandatory):
  - archived_body_lines=48
  - preamble_lines=15
  - retained_body_lines=1160

---

## Research checkpoint — US-0126 / auto-20260825-01

- **phase_id**: research, **role**: tech-lead, **story_id**: US-0126, **sprint_id**: (pending)
- `orchestrator_run_id=auto-20260825-01`
- `delivery_mode=ultra_lean`, `macro_phase=plan` (research — first canonical phase of `plan` macro per US-0096 / DEC-0082)
- `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 — required)
- `fresh_context_marker=tl-US0126-research-20260825T155615Z-fresh`, `timestamp=2026-08-25T15:56:15Z` (UTC)
- `verdict=PASS` (no DECISION_GATE; 8/8 discovery open questions DQ1..DQ8 closed LOCKED for `/architecture`; architecture seeds proposed; companion DEC-0126 optional)
- `status=OPEN` (US-0045; US-0126 NOT marked DONE; acceptance L154 NOT ticked; intake JSON NOT mutated; vision D1–D10 NOT rewritten; prior R-0109 locks NOT wiped; `# US-0126` NOT added to architecture.md — `/architecture` owns that H1 per DEC-0073 after `# US-0125` and before `# US-0089`)

### Research summary (US-0126 — R-0109 US-0126 deepened findings)

- **R-0109 US-0126 subsection appended** at `docs/engineering/research.md` L9940 (`### Deepened findings — US-0126`). R-0109 remains the epic anchor; **no new R-id allocated**. US-0121 Q1..Q12 + US-0122 DQ1..DQ8 + US-0123 DQ1..DQ10 + US-0124 DQ1..DQ8 + US-0125 DQ1..DQ8 locks **PRESERVED** (not wiped).
- **DQ1 LOCKED**: new sibling h2 `## OpenCode host operator runbook (US-0126)` in `docs/engineering/runbook.md` + `template/docs/engineering/runbook.md` (active↔template byte-identical); anchor `opencode-host-operator-runbook-us-0126`; placed after `## OpenCode thin commands + validator bridge (US-0125)` (L4009). US-0121 `## OpenCode host mode (US-0121)` (L3870 — installer `--host` flag docs hook), US-0124 stub reason-code h2 (L3995), US-0125 stub reason-code h2 (L4009) stay **untouched** (compose, do not amend); US-0126 cross-links to them.
- **DQ2 LOCKED**: consolidated cross-host reason-code table = 4 `OPENCODE_*` (US-0124: `OPENCODE_PLUGIN_SPAWN_UNSUPPORTED`, `OPENCODE_SUBTASK_IGNORED`, `OPENCODE_HEADLESS_UNSUPPORTED`, `OPENCODE_DRIVER_INVOKE_FAILED`) + 5 installer `OPENCODE_*`/`CURSOR_*` (US-0121: `INSTALL_HOST_INVALID`, `OPENCODE_ORPHANED_BY_CLEAN_CURSOR`, `OPENCODE_STALE_BY_UPGRADE_CURSOR`, `CURSOR_ORPHANED_BY_CLEAN_OPENCODE`, `CURSOR_STALE_BY_UPGRADE_OPENCODE`) + 3 reused cross-host (`AUTO_ORCHESTRATOR_PHASE_EXECUTION`, `PHASE_ROLE_MISMATCH`, `NATIVE_CHAIN_UNAVAILABLE`) + raw Python validator codes (`INTAKE_PERSISTENCE_BLOCKED`, `INTAKE_REQUIRED_TOPIC_MISSING`, `BUG_ISSUE_VALIDATION_FAILED`, ...). **NO `OPENCODE_VALIDATOR_FAILED` wrapper** (rejected by DEC-0125 DQ7 — D2 discovery listing was STALE; US-0126 must not resurrect it). Each code: one-line semantics + fail-closed action + cross-link to owning slice.
- **DQ3 LOCKED**: extend `OPENCODE_ADAPTER_PAIRS` additively in `scripts/check_intake_template_parity.py` (L484–L517) with 2 new pairs: `tests/us0126_contract_test.py` ↔ template + `docs/engineering/runbook.md` ↔ template. Do NOT invent a sibling script or sibling scope. `--scope=opencode-adapter` (L541) validates the whole epic surface in one invocation. Pass/fail = byte-identical pair + surface file presence + reason-code table presence + test marker presence; exit 0 = `[INTAKE_TEMPLATE_PARITY_OK] scope=opencode-adapter`, non-zero = `INTAKE_TEMPLATE_PARITY_FAILED`.
- **DQ4 LOCKED**: 12 `test_us0126_*` markers (one-test-per-AC; AC-5 splits into readme + runbook no-dec-leak; +1 aggregate prior-story marker `test_us0126_prior_story_markers_present` / `test_us0126_test_marker_checklist`). All static/grep-based, no live OpenCode probe (vision D10 lock). Tests live in `tests/us0126_contract_test.py` ↔ `template/tests/us0126_contract_test.py` byte-identical.
- **DQ5 LOCKED**: program DoD = static documentation test (grep for locked sentence key phrases); no live end-to-end probe. "without Cursor" = no `.cursor/` directory loaded for this project (installer `--host opencode` skips `.cursor/` rows per US-0121; kernel paths still install); NOT "no Cursor IDE process on the operator machine". "different sessions/providers" = distinct OpenCode sessions for PO/Dev/QA; optionally distinct providers via US-0123. "validators still block" = Python persistence-blocking validators (`intake_evidence_validate.py`, `bug_issue_validate.py`, US-0125 bridge contract set) refuse writes on non-zero exit exactly as on Cursor; US-0124 plugin `ctx.tool.hook("execute.before")` enforces.
- **DQ6 LOCKED**: default-host reminder sentence = "Default install is cursor-only. Pass `--host opencode` or `--host both` to install the OpenCode host adapter; without it, `.opencode/` is not installed. See `## OpenCode host mode (US-0121)` for the installer flag reference." Appears in runbook US-0126 section + README. No DEC ids in operator prose (US-0071); cross-reference is to US-0121 runbook h2 (not `DEC-0120`).
- **DQ7 LOCKED**: out-of-scope list = 5 items named by surface in operator prose: "standalone runtime, OpenCode fork, VS Code contrib rewrite, Caveman mode, Cursor browser as primary UAT." Cross-references to owning masterplans/DECs in a separate Boundaries subsection (runbook only; not operator prose). US-0071 sanitization enforced.
- **DQ8 LOCKED**: no new `installer-owned-paths.manifest` entries (active + template byte-identical unchanged). Runbook is already installer-owned via `docs` in `[install_include_paths]`; the new US-0126 h2 section is part of the runbook. `tests/us0126_contract_test.py` is NOT installer-shipped (matches US-0121..US-0125 pattern); parity-validated via the new `OPENCODE_ADAPTER_PAIRS` runbook + test pairs (DQ3 lock).

### Architecture seeds for `/architecture`

- **Companion DEC**: `DEC-0126` (Optional — `/architecture` may author if a formal DEC need is found beyond US-0071/US-0121..US-0125 compose; otherwise cite R-0109 US-0126 DQ1-DQ8 directly in the US-0126 architecture section).
- **Sprint seeds (10 tasks within SPRINT_MAX_TASKS=12)**: T-anch (architecture.md `# US-0126` anchor after `# US-0125` before `# US-0089` per DEC-0073; NO-OP / verification), T-001 (runbook section + template mirror), T-002 (README blurb + template mirror), T-003 (`OPENCODE_ADAPTER_PAIRS` additive extension — 2 new pairs), T-004 (`tests/us0126_contract_test.py` + template — 12 markers), T-005 (consolidated reason-code table authoring), T-006 (US-0071 sanitization grep tests), T-007 (program DoD static documentation test), T-008 (default-host reminder + out-of-scope tests), T-009 (parity + Cursor-docs-not-deleted tests), T-010 (prior-story marker checklist). AC mapping 10 ACs → 10 tasks bijective. `/sprint-plan` may merge or split within the 12-task budget.

### Risks finalized (R1..R6 — 6 risks)

- R1 (MEDIUM) reason-code namespace collision → DQ2 consolidated table; NO `OPENCODE_VALIDATOR_FAILED` wrapper. R2 (MEDIUM) parity-scope drift → DQ3 additive `OPENCODE_ADAPTER_PAIRS` extension. R3 (MEDIUM) operator-sentence DEC leakage → DQ6/DQ7 US-0071 sanitization. R4 (LOW–MEDIUM) template-parity gap → DQ8 runbook pair in `OPENCODE_ADAPTER_PAIRS`. R5 (LOW–MEDIUM) program-DoD ambiguity → DQ5 operationally precise locked wording. R6 (LOW) Cursor-kit deletion temptation → DQ4 marker 11 `test_us0126_cursor_docs_not_deleted`.

### Isolation evidence (US-0048 / DEC-0038) — research (auto-20260825-01)

- `phase_id=research`, `role=tech-lead`, `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 — required)
- `fresh_context_marker=tl-US0126-research-20260825T155615Z-fresh`, `timestamp=2026-08-25T15:56:15Z` (UTC)
- `runtime_proof_id=rp-auto-20260825-01-research-tech-lead-20260825T155615Z-US-0126` (NEW — distinct from prior intake `...T155000Z...`, discovery `...T155500Z...`, sovereign-critic `...T160200Z...` proof ids; no prior id reused; RUNTIME_PROOF_REUSED forbidden)
- Canonical payload (sorted-key JSON per DEC-0038): `{"delivery_mode":"ultra_lean","macro_phase":"plan","model_id":"glm-5.2-high","orchestrator_run_id":"auto-20260825-01","phase_id":"research","proof_issued_at":"2026-08-25T15:56:15Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260825-01-research-tech-lead-20260825T155615Z-US-0126","sprint_id":"(pending)","story_id":"US-0126"}`
- `proof_hash=22035314D2CD5763ECDBED6A3426B696A57331035F84E3BDEC97FC7DFAC3B188` (SHA-256 uppercase hex of sorted-key compact JSON payload above)
- `proof_ttl_seconds=3600`, `proof_ttl=2026-08-25T16:56:15Z` (UTC = issued_at + 3600s)
- Independent recompute (Python one-liner, `C:\Users\flow\AppData\Local\Programs\Python\Python312\python.exe`): `python -c "import json,hashlib; p={'delivery_mode':'ultra_lean','macro_phase':'plan','model_id':'glm-5.2-high','orchestrator_run_id':'auto-20260825-01','phase_id':'research','proof_issued_at':'2026-08-25T15:56:15Z','proof_ttl_seconds':3600,'role':'tech-lead','runtime_proof_id':'rp-auto-20260825-01-research-tech-lead-20260825T155615Z-US-0126','sprint_id':'(pending)','story_id':'US-0126'}; print(hashlib.sha256(json.dumps(p,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest().upper())"` -> `22035314D2CD5763ECDBED6A3426B696A57331035F84E3BDEC97FC7DFAC3B188`
- `evidence_ref=docs/engineering/research.md ## R-0109 ### Deepened findings — US-0126 (L9940+; appended this phase) + docs/product/backlog.md ## US-0126 (NOT rewritten) + docs/product/vision.md ## Intake Notes — US-0126 + ## Discovery Notes — US-0126 (NOT rewritten) + docs/product/acceptance.md L154 (NOT rewritten) + handoffs/intake_evidence/US-0121-intake-20260822.json (NOT mutated) + docs/engineering/architecture.md (NOT mutated — # US-0126 NOT added; /architecture owns that H1) + docs/engineering/runbook.md (NOT mutated this phase — /architecture + /execute own the US-0126 h2 section) + scripts/check_intake_template_parity.py (NOT mutated this phase — /architecture + /execute own the OPENCODE_ADAPTER_PAIRS extension) + decisions/DEC-0124.md + decisions/DEC-0125.md (read-only compose)`

### Next scheduled phase

- `next_scheduled_phase=/architecture` (role=tech-lead per US-0069 / DEC-0051 phase→role matrix default; second canonical phase of `plan` macro per ultra_lean; research + architecture + sprint-plan merged into `plan` macro)
- `next_scheduled_role=tech-lead`
- `stop_condition=STOP after research completes. Orchestrator spawns /architecture in fresh tech-lead subagent (BUG-0006). Do NOT add # US-0126 to architecture.md from /research — /architecture owns that H1 (after # US-0125, before # US-0089 per DEC-0073). Do NOT mark US-0126 DONE. Do NOT tick acceptance L154. Do NOT mutate intake JSON. Do NOT wipe prior R-0109 locks. Do NOT rewrite D1–D10 discovery prose in vision.md.`

