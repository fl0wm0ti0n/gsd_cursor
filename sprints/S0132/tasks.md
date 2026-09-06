# Sprint S0132 - Task checklist (BUG-0016)

Total tasks: 8 (T-anch + T-001..T-007). SPRINT_MAX_TASKS=12; SPRINT_AUTO_SPLIT=1; no split needed. Seeds kept **1:1** from architecture (critic NB `b0016ar-architect-002`).

**Isolation**: `tl-BUG0016-sprint-plan-20260906T185500Z-fresh` · `model_id=composer-2.5` · `orchestrator_run_id=auto-20260906-bug0016`

## Task execution order

1. T-anch (NO-OP / verification)
2. T-001 (`po.md` bash ask + intake_evidence/** + resume_brief.md + state.md; active + template)
3. T-002 (`tech-lead.md` + `curator.md` bash ask; tech-lead Sxxxx→S*; active + template)
4. T-003 (`dev.md` + `qa.md` Sxxxx→S*; active + template)
5. T-004 (`release.md` duty paths; active + template)
6. T-005 (amend `tests/us0122_contract_test.py` expectations to amended §2)
7. T-006 (NEW `tests/bug0016_contract_test.py` — 7 markers + parity gate)
8. T-007 (DQ8 write-guard verify; document only; amend DEC-0124/0125 only if proven)
9. Integration verification

## Critic NB awareness (execute)

- **T-007** (`b0016ar-challenger-001` / `ik_bug0016_arch_edge_and_proof`): Prove Layer-1 ∩ write-guard does not re-deny duty globs; amend DEC-0124/0125 only if proven; keep `S*` (not `S[0-9]*`); enforce active↔template parity + intentional us0122 realign.
- **T-anch..T-007 1:1** (`b0016ar-architect-002` / `ik_bug0016_arch_layer_coupling`): DEC-0122 §2 remains sole matrix SOT; execute ships frontmatter parity; CF2 runbook allow does not transfer US-0126 prose ownership.
- **T-anch / scope** (`b0016ar-subtractor-003` / `ik_bug0016_arch_scope_minimal`): T-anch read-only; no architecture.md mutation; do not invent DEC-0130 / `bash:allow` / live probe; do not mark BUG-0016 DONE; 7 markers required.

## Task checklist

- [x] **T-anch**: Verify `# BUG-0016` H1 present in `docs/engineering/architecture.md` (added in /architecture per DEC-0076); verify approach A* locked + R-0115 DQ1–DQ8 LOCKED + CF1–CF5 CLOSED; verify companion DEC none (DEC-0130 rejected); verify `decisions/DEC-0122.md` §2 already amended (sole SOT — do **not** re-amend in execute unless regression found); verify success test (c) prose intact; verify 7-marker contract-test list locked; verify compose guards (no US-0131/US-0132 reopen; no bash:allow; no live probe; security/auto unchanged in matrix); verify agent frontmatter still shows pre-execute gap (`bash: deny` / `Sxxxx` / missing release paths) OR document if partially present; verify `tests/bug0016_contract_test.py` does NOT yet exist (or document baseline). Record results to `sprints/S0132/t-anch-verification.md`. T-anch is NO-OP / verification only — NO mutation to `docs/engineering/architecture.md` or DEC-0122 body in /execute. (AC-5, AC-6, AC-8 baseline; NO-OP / verification only)

- [x] **T-001**: Edit `.opencode/agents/po.md` AND `template/.opencode/agents/po.md` (byte-identical) per architecture A* / DQ1 / DQ2. Set `bash: ask` (reject `allow` / keep object-form YAGNI). Edit allows: keep existing `docs/product/**` + `handoffs/po_to_tl.md`; **add** `handoffs/intake_evidence/**`, `handoffs/resume_brief.md`, `docs/engineering/state.md`; keep `**` → deny **last**. No `scripts/**` / production / code allow. MUST keep active ↔ template byte-identical. Tests: markers 1, 2, 7. (AC-1, AC-2, AC-7)

- [x] **T-002**: Edit `.opencode/agents/tech-lead.md` + `curator.md` AND template peers (byte-identical). Set both `bash: ask`. On tech-lead: replace permission-key `sprints/Sxxxx/…` → `sprints/S*/…` for owned sprint files (`sprint.md`, `tasks.md` per DEC-0122 §2 / architecture). Curator edit set unchanged except bash posture. MUST keep active ↔ template byte-identical. Tests: markers 1, 3, 7. (AC-1, AC-3, AC-7)

- [x] **T-003**: Edit `.opencode/agents/dev.md` + `qa.md` AND template peers (byte-identical). Replace sprint permission keys `sprints/Sxxxx/…` → `sprints/S*/…` for owned files (dev: progress.md / qa-findings.md; qa: qa-findings / plan-verify / verify-work / uat paths per matrix). `bash: ask` unchanged. MUST keep active ↔ template byte-identical. Tests: markers 3, 7. (AC-3, AC-7)

- [x] **T-004**: Edit `.opencode/agents/release.md` AND template peer (byte-identical). Keep `bash: ask`. **Add** edit allows: `sprints/S*/release-findings.md`, `handoffs/verify-work-to-release.md`, `docs/engineering/state.md`, `handoffs/resume_brief.md`, `docs/engineering/runbook.md`; keep existing `verify_to_release.md` + release handoff/CHANGELOG allows; `**` deny last. CF2: runbook allow does **not** transfer US-0126 prose ownership. MUST keep active ↔ template byte-identical. Tests: markers 4, 7. (AC-4, AC-7)

- [x] **T-005**: Amend `tests/us0122_contract_test.py` expectations to the amended DEC-0122 §2 matrix (intentional SOT realign — R5). Mirror template peer if paired. Do **not** invent a live OpenCode probe. Do **not** weaken success test (c) asserts. (AC-5, AC-8)

- [x] **T-006**: Create `tests/bug0016_contract_test.py` with 7 markers per architecture DQ7 (AC coverage). Markers:
  1. `test_bug0016_po_tl_curator_bash_ask` — po/tech-lead/curator `bash == ask` (not deny/allow)
  2. `test_bug0016_po_intake_resume_state_allows` — PO edit allows intake_evidence/**, resume_brief.md, state.md; `**` deny last; no scripts/** allow
  3. `test_bug0016_sprint_globs_are_s_star_not_sxxxx` — tech-lead/dev/qa/release sprint keys use `sprints/S*/`; `Sxxxx` absent from permission keys
  4. `test_bug0016_release_duty_paths` — release allows release-findings, verify-work-to-release, state.md, resume_brief.md, runbook.md
  5. `test_bug0016_success_test_c_non_dev_no_production_allow` — non-dev: no production/code allow; object-form edit keeps `**` deny last
  6. `test_bug0016_security_auto_unchanged` — security edit deny + bash ask; auto edit/bash deny + 7-role task allow + `*` deny last
  7. `test_bug0016_active_template_agent_parity` — eight agents byte-identical active↔template (or parity scope)
All markers static harness; **no live OpenCode probe**. Mirror to `template/tests/bug0016_contract_test.py` if required for parity. Optional: add parity scope `bug-0016` / extend `opencode-adapter` pairs. (AC-1..AC-8)

- [x] **T-007**: DQ8 / CF3 — read/verify plugin write-guard (`.opencode/plugins/orchestrator.ts` / DEC-0124) does **not** re-deny duty globs for owning roles after Layer-1 allows. Document findings in `sprints/S0132/progress.md` (or qa-findings foreshadow). Amend `decisions/DEC-0124.md` / `DEC-0125.md` **only if** a concrete contradiction is proven; otherwise leave compose-only. Keep `S*` (not `S[0-9]*`). (DQ8 adjacent)

## Integration verification (post T-007)

- [x] Test gate: `python -m pytest tests/bug0016_contract_test.py -v` -> 7/7 PASS
- [x] Compose gate: `python -m pytest tests/us0122_contract_test.py -q` still green after intentional realign
- [x] Parity gate: active + template agents byte-identical for touched roles
- [x] Parity gate: active + template `bug0016_contract_test.py` byte-identical (if mirrored)
- [x] Scope gate: no `bash: allow`; no DEC-0130; no US-0131/US-0132 reopen; no live OpenCode CI probe; no BUG-0015 reopen; security/auto unchanged
- [x] Write-guard gate: T-007 documented; DEC-0124/0125 untouched unless proven
- [x] Status gate: BUG-0016 remains OPEN; acceptance BUG-0016 unchecked; intake JSON not mutated

## Files to touch (scope)

### New (create)

- `tests/bug0016_contract_test.py`
- `template/tests/bug0016_contract_test.py` (byte-identical mirror if required for parity)
- `sprints/S0132/t-anch-verification.md`

### Edit (scoped)

- `.opencode/agents/po.md` + `template/.opencode/agents/po.md`
- `.opencode/agents/tech-lead.md` + `template/.opencode/agents/tech-lead.md`
- `.opencode/agents/curator.md` + `template/.opencode/agents/curator.md`
- `.opencode/agents/dev.md` + `template/.opencode/agents/dev.md`
- `.opencode/agents/qa.md` + `template/.opencode/agents/qa.md`
- `.opencode/agents/release.md` + `template/.opencode/agents/release.md`
- `tests/us0122_contract_test.py` (+ template peer if paired)
- Optional: `scripts/check_intake_template_parity.py` + template (`bug-0016` / opencode-adapter scope pairs)

### Verify read-only (no mutation unless T-007 proves)

- `docs/engineering/architecture.md # BUG-0016` (T-anch NO-OP)
- `decisions/DEC-0122.md` §2 (already amended — do not regress)
- `docs/product/backlog.md ### BUG-0016` (read-only Status/ACs — US-0045)
- `docs/product/acceptance.md` BUG-0016 row (read-only — US-0045)
- `handoffs/intake_evidence/BUG-0016-intake-20260906.json` (read-only)
- `docs/engineering/research.md ## R-0115` (read-only)
- `.opencode/plugins/orchestrator.ts` write-guard (T-007 verify)
- `.opencode/agents/security.md` + `auto.md` (unchanged — verify only)

### Compose-guard UNCHANGED (DO NOT TOUCH)

| File | Reason |
|---|---|
| `docs/product/backlog.md` Status/ACs | US-0045 canonical status — `/closure` mutates ONLY at execution time |
| `docs/product/acceptance.md` | US-0045 derived view — same |
| `docs/engineering/architecture.md` | Do not rewrite; T-anch is verification only |
| `decisions/DEC-0124.md` / `decisions/DEC-0125.md` | Compose-only unless T-007 proves double-deny |
| `decisions/DEC-0122.md` body beyond already-amended §2 | Sole SOT — no second matrix / no DEC-0130 |
| US-0131 / US-0132 backlog rows | Do not reopen |
| US-0126 full runbook ownership | Layer-1 allow ≠ prose ownership |
| BUG-0015 / S0131 artifacts | DONE compose-note only |

## AC -> Task surjective coverage

| AC | Task(s) |
|---|---|
| AC-1 (bash ask po/tl/curator) | T-001, T-002, T-006 (marker 1) |
| AC-2 (PO intake/resume/state) | T-001, T-006 (marker 2) |
| AC-3 (S* sprint globs) | T-002, T-003, T-006 (marker 3) |
| AC-4 (release duty paths) | T-004, T-006 (marker 4) |
| AC-5 (success test (c)) | T-anch, T-005, T-006 (marker 5) |
| AC-6 (security/auto unchanged) | T-anch, T-006 (marker 6) |
| AC-7 (active↔template parity) | T-001..T-004, T-006 (marker 7) |
| AC-8 (DEC-0122 sole SOT) | T-anch, T-005 |
| DQ8 Layer-1 ∩ write-guard | T-007 |

**Surjectivity check**: 8/8 ACs covered (AC-1..AC-8 each have at least 1 task) + DQ8 via T-007. No `PLAN_AC_COVERAGE_GAP`.
