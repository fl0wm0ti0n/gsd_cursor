# Sprint S0116

## Metadata

- **sprint_id**: S0116
- **story_refs**: US-0116
- **priority**: P3
- **effort**: 1 day
- **owner**: dev
- **goal**: Close the operator-documentation gap for the **delivery & lifecycle family features** (US-0092, US-0095, US-0098, US-0099) in the framework README pair (`its_magic/README.md` ↔ `template/its_magic/README.md`). Add the `### Delivery & lifecycle (US-0092 / US-0095 / US-0098 / US-0099) umbrella section` under `## Commands and workflow` (L350), as a sibling — **4th sibling, first 4-cumulative-surface story** — to US-0113's `### Sovereign-loop era (US-0103–US-0112)` umbrella (L940), US-0114's `### Release & distribution (US-0041 / US-0062 / US-0111 / US-0112)` umbrella (L1225), and US-0115's `### Integration & observability (US-0034 / US-0084 / US-0086 / US-0093 / US-0096 / US-0101 / US-0102)` umbrella (L1410), with 4 nested `#### US-xxxx` operator subsections ordered US-id-ascending (US-0092 → US-0095 → US-0098 → US-0099), inserted immediately after the closing of US-0115's umbrella block (before L1665 `### Full scratchpad reference (detailed)`). Extend `### Full scratchpad reference (detailed)` (L1665) with a `### Delivery & lifecycle keys (US-0092 / US-0095 / US-0098 / US-0099)` sub-block — **true net-new key rows** ONLY (US-0098 `DEV_AUTO_LAUNCH_PROFILE` + `DEV_ENVIRONMENT_CONFIG` — the only 2 net-new scratchpad key rows) + **reason-code-only entries** for US-0099 (`DEV_ENV_BOOTSTRAP_*` family + `DEV_ENV_PROFILE_MISSING` — 5 reason codes) + **grouped cross-link pointers** to pre-US-0116 README surfaces for US-0092/US-0095 keys + **cross-link pointers** to US-0114's `### Release & distribution keys` block (L1806) for `DELIVERY_MODE` / `AUTO_INSTALL_DEPS` / `AUTO_RELEASE_NOTES` overlap + optional cross-link pointer to US-0115's `### Integration & observability keys` block (L1878) for `LEAN_MEMORY_*` family (default omit — angle-distinct). Preserve framework README byte-parity, run validators green, and keep regression tests green. Documentation-only; default-off posture preserved for optional runtime features (US-0092/US-0095/US-0098); bootstrap-on-install framing for US-0099 (install-time only, zero runtime cost). US-0113's L1682 sovereign-loop keys block, US-0114's L1806 release & distribution keys block, and US-0115's L1878 integration & observability keys block byte-stability preserved (4th-story cumulative byte-stability surface — pure addition, cross-link pointers + reason-code-only entries only; never edit prior released blocks).
- **status**: OPEN (per US-0045 — closure at /release)
- **created_at**: 2026-07-04T17:15:00Z
- **orchestrator_run_id**: auto-20260704-01
- **delivery_mode**: ultra_lean
- **macro_phase**: plan (sprint-plan — third canonical phase)
- **fresh_context_marker**: tl-US0116-sprint-plan-20260704T171500Z-fresh
- **resolved_phase_plan**: `["spec","plan","build+verify","ship"]` (ultra_lean macro — recomputed at story boundary per US-0044 / DEC-0022; `spec` already done via 5-story decomposition intake; `plan` = research + architecture + sprint-plan all complete; `build+verify` = `/execute` + `/qa` (merges plan-verify + execute QA + verify-work); `ship` = `/release` + `/refresh-context`)

## Scope

- **US-0116**: Delivery & lifecycle operator documentation in framework README
- **Architecture anchor**: `docs/engineering/architecture.md#US-0116` (h1 section appended in architecture phase; approach_locked=A1)
- **Research anchor**: `docs/engineering/research.md` `R-0104` (delivered 2026-07-04T09:30:00Z — 8/8 spec open questions closed)
- **Companion DEC**: none (US-0116 is documentation-only; no architectural, policy, or schema surface changed. Mirrors US-0113 / US-0114 / US-0115 sibling precedent. R-0104 § Decision-gate recommendation confirmed no DEC candidate; grep `^## DEC-` in `docs/engineering/decisions.md` returned no US-0116 companion DEC.)

## Acceptance criteria (US-0116 — 8 ACs)

| AC | Description |
|----|-------------|
| AC-1 | `### Delivery & lifecycle umbrella section` under `## Commands and workflow` |
| AC-2 | Per-feature operator subsections for US-0092/US-0095/US-0098/US-0099 |
| AC-3 | Full scratchpad reference extension (true net-new keys only + cross-link pointers + reason-code-only entries) |
| AC-4 | Coverage preserved (`validate_readme_feature_coverage.py --enforce` green) |
| AC-5 | Framework README parity (`its_magic/README.md` ↔ `template/its_magic/README.md` byte-identical) |
| AC-6 | Audience + metadata hygiene |
| AC-7 | Runbook cross-links per feature (4 features → 4 anchors: US-0092 → L1958 h3 + L1989 h4 (parent h2 = `## Auto continuation resume contract` L1587); US-0095 → L1900 h3 (parent h2 = L1587); US-0098 → L244 h2 (top-level); US-0099 → L244 (parent h2) with secondary pointers to L250 (bootstrap paragraph) + L301 (normative contract anchor)) |
| AC-8 | Regression tests (coverage parity contract tests green; no test weakenings) |

## AC → task surjective coverage (6 tasks, 8 ACs)

| AC | Task(s) | Architecture anchor |
|----|---------|---------------------|
| AC-1 Umbrella section | T-001 | § Sprint seeds T-001 |
| AC-2 Per-feature operator subsections | T-002 | § Sprint seeds T-002 |
| AC-3 Full scratchpad reference extension | T-003 | § Sprint seeds T-003 |
| AC-4 Coverage preserved | T-005 | § Sprint seeds T-005 |
| AC-5 Framework README parity | T-004 | § Sprint seeds T-004 |
| AC-6 Audience + metadata hygiene | T-005 | § Sprint seeds T-005 |
| AC-7 Runbook cross-links per feature | T-002 | § Sprint seeds T-002 |
| AC-8 Regression tests | T-006 | § Sprint seeds T-006 |

**Surjectivity check**: AC-1..AC-8 all covered (8/8). Multi-AC tasks: **T-002** (AC-2+AC-7), **T-005** (AC-4+AC-6). Every AC has ≥1 task. No `PLAN_AC_COVERAGE_GAP`.

## Task count

- **Total**: 6
- **SPRINT_MAX_TASKS**: 12 (from `.cursor/scratchpad.md`)
- **Within limit**: yes (6 ≤ 12; `SPRINT_AUTO_SPLIT` not triggered)
- **SPRINT_AUTO_SPLIT_TRIGGERED**: false

## Tasks (T-001..T-006)

See `sprints/S0116/tasks.md` for atomic task definitions. Execution order (per architecture dependency chain):

```
T-001 (umbrella) → T-002 (4 subsections) → T-003 (scratchpad ref extension) →
T-004 (template byte-sync) → T-005 (validators) → T-006 (regression tests)
```

| ID | Title | ACs | Tranche | Risk |
|----|-------|-----|:--------|:-----|
| T-001 | Add `### Delivery & lifecycle (US-0092 / US-0095 / US-0098 / US-0099) umbrella section` under `## Commands and workflow` (after US-0115 umbrella close, before L1665; default-off framing for optional runtime features (US-0092/US-0095 opt-in via `AUTO_FLOW_MODE=full_autonomy`; US-0098 opt-in via `DEV_AUTO_LAUNCH_PROFILE`); bootstrap-on-install framing for US-0099 (install-time only, zero runtime cost); 4-step enable order US-0099 bootstrap → US-0098 auto-launch → US-0095 native in-chat chain primary → US-0092 outer-driver fallback; runbook pointer line; zero-overhead-when-off contract line) | AC-1 | A | LOW |
| T-002 | Add 4 per-feature `#### US-xxxx` operator subsections nested under umbrella (US-0092 → US-0095 → US-0098 → US-0099; US-0092 = full-autonomy outer driver + DEC-0078 security posture + hard caps + native-chain-vs-outer-driver routing (US-0095 primary, US-0092 fallback) + runbook L1958/L1989; US-0095 = native in-chat auto-chain primary + compose-on-US-0044 + drain-advance suppression + grouped cross-link to `### Automation modes` L880 + main reference list + optional `LEAN_MEMORY_*` cross-link to US-0115 L1878 (default omit) + runbook L1900; US-0098 = `DEV_AUTO_LAUNCH_PROFILE` default-off + `DEV_ENVIRONMENT_CONFIG` path + orthogonality to US-0065/US-0086/US-0067/`AUTO_REMOTE_AUTOMATION_PROFILE` + DEC-0084 §3 detection precedence + compose-with-US-0099 + runbook L244; US-0099 = install-time copy-when-missing bootstrap + customize-after-bootstrap contract + `DEV_ENV_BOOTSTRAP_*` reason-code family (5 codes) + `DEV_ENV_PROFILE_MISSING` remediation + compose-with-US-0098 + runbook L244/L250/L301) | AC-2, AC-7 | A | LOW–MEDIUM |
| T-003 | Extend `### Full scratchpad reference (detailed)` with `### Delivery & lifecycle keys (US-0092 / US-0095 / US-0098 / US-0099)` sub-block — **true net-new key rows** ONLY (US-0098 `DEV_AUTO_LAUNCH_PROFILE=off\|deterministic_v1` default `off` + `DEV_ENVIRONMENT_CONFIG=repo-relative path` default `.cursor/dev-environment.json`) + reason-code-only entries for US-0099 (5 codes: `DEV_ENV_BOOTSTRAP_COPIED` / `DEV_ENV_BOOTSTRAP_SKIPPED_EXISTS` / `DEV_ENV_BOOTSTRAP_PATH_INVALID` / `DEV_ENV_BOOTSTRAP_SOURCE_MISSING` / `DEV_ENV_PROFILE_MISSING`) + grouped cross-link pointers to pre-US-0116 README surfaces for US-0092/US-0095 keys (`### Automation modes` L880 + `### Sync policy (US-0038)` L909 + `### Optional /auto backlog-drain mode (US-0044)` L2370 + main reference list — NOT to US-0113's L1682 block; those keys are not there) + cross-link pointers to US-0114's `### Release & distribution keys` block (L1806) for `DELIVERY_MODE` / `AUTO_INSTALL_DEPS` / `AUTO_RELEASE_NOTES` + optional cross-link pointer to US-0115's `### Integration & observability keys` block (L1878) for `LEAN_MEMORY_*` family (default omit — angle-distinct per R-0104 open question #2); US-0113 L1682 + US-0114 L1806 + US-0115 L1878 byte-stability preserved (4th-story cumulative surface) | AC-3 | A | MEDIUM |
| T-004 | Sync `template/its_magic/README.md` byte-identical from `its_magic/README.md` (one-way copy); re-run parity + intake template parity | AC-5 | B | MEDIUM |
| T-005 | Run validators (`validate_readme_feature_coverage.py --enforce`, `validate_doc_profile.py`, `check-user-visible-metadata.py`); fix any drift; catalog block L63 read-only | AC-4, AC-6 | B | LOW (catalog) / MEDIUM (encoding prerequisite) |
| T-006 | Run regression tests (`pytest tests/scratchpad_example_parity_test.py -q` → expect 4 passed); no test weakenings; forbid edits to scratchpad canonical + test file | AC-8 | B | LOW–MEDIUM |

## Test markers (locked — no new tests proposed)

| Marker | File | ACs covered | Notes |
|--------|------|-------------|-------|
| `test_bug0013_parity_check` + 3 companions | `tests/scratchpad_example_parity_test.py` | AC-5 (indirect), AC-8 | US-0116 does NOT modify `.cursor/scratchpad.md` or `template/.cursor/scratchpad.local.example.md`; tests remain green by construction. |
| `validate_readme_feature_coverage.py --enforce` | `scripts/validate_readme_feature_coverage.py` | AC-4 | Coverage gate; `coverage_missing=[]` baseline (US-0117 not yet OPEN in-scope). Catalog block L63 read-only. |
| `check_intake_template_parity.py` | `scripts/check_intake_template_parity.py` | AC-5 | Framework README byte-parity gate. |
| `validate_doc_profile.py` | `scripts/validate_doc_profile.py` | AC-6 | Audience profile gate. |
| `check-user-visible-metadata.py` | `scripts/check-user-visible-metadata.py` | AC-6 | Metadata hygiene gate. |

**No new tests proposed.** AC-8 satisfied by existing tests remaining green (read-only gates, not edit targets). R-0104 confirmed no test weakenings.

## Files to touch

| # | Active path | Template path | Task | Parity |
|---|-------------|---------------|------|--------|
| 1 | `its_magic/README.md` | `template/its_magic/README.md` | T-001, T-002, T-003, T-004 | Byte-identical via T-004 one-way copy |

## Files NOT to touch (non-goals — hard)

- `.cursor/scratchpad.md` — canonical source of truth (never edit in docs stories; BUG-0013 precedent; US-0116 only documents existing keys).
- `template/.cursor/scratchpad.local.example.md` — canonical example (BUG-0013 ownership).
- `docs/product/backlog.md` — status authority (closure only at /release per US-0045). **Note:** working-tree copy has 185 stray `0xa7` bytes (encoding regression flagged in R-0102 + R-0103 + R-0104 + architecture) — orchestrator must restore encoding hygiene before execute so AC-4 can be re-verified post-execute. **NOT a US-0116 blocker.**
- `docs/engineering/runbook.md` — AC-7 cross-links only; **no new runbook content** (AC-7 forbids duplication). All 4 runbook cross-link targets already exist (verified in R-0104).
- `docs/developer/README.md` — separate audience surface owned by US-0097 (project README parity) compose guard; AC-6 is a validator gate, not an edit mandate.
- `docs/engineering/architecture.md` (other than the architecture phase `## US-0116` anchor already appended) — missing `# US-0092` / `# US-0095` / `# US-0098` / `# US-0099` h1 anchors **deferred to US-0117** (DC-4, parallel to US-0113's DC-1 — 5 anchors; US-0114's DC-2 — 2 anchors; US-0115's DC-3 — 7 anchors; US-0117 inherits 18 anchors total as architecture.md triad hygiene closure).
- `installer.py`, `installer.ps1`, `installer.sh` — no installer changes (US-0008/US-0018/US-0057/US-0075 + US-0062/DEC-0045 + US-0041/BUG-0003 compose guards).
- All `scripts/*` — validators are read-only gates, not edit targets.
- All delivery & lifecycle scripts and Python/PowerShell/Shell files — US-0092/US-0095/US-0098/US-0099 features are **documented only**, not amended.
- `tests/scratchpad_example_parity_test.py` — read-only regression gate; if it fails, fix prose not test.
- **Do NOT modify US-0113's `### Sovereign-loop era` / `### Sovereign-loop era keys` blocks (L940 / L1682), US-0114's `### Release & distribution` / `### Release & distribution keys` blocks (L1225 / L1806), or US-0115's `### Integration & observability` / `### Integration & observability keys` blocks (L1410 / L1878)** in `its_magic/README.md` — byte-stability contract (all 3 already released in S0113 / S0114 / S0115). US-0116 adds cross-link pointers to these blocks from its own net-new block; it never edits them. Execute-phase must verify `git diff HEAD -- its_magic/README.md` shows pure addition in the post-L1878 range (no removals/modifications to US-0113's L1682, US-0114's L1806, or US-0115's L1878 blocks).

## Compose guards (23 — all UNCHANGED, cumulative)

US-0116 lives entirely outside the compose surface (documentation-only; no code/scripts/installers/scratchpad canonical touched). 23 guards cumulative across all prior stories — same 23 as US-0115; US-0116 adds no new family-internal guards because all 4 in-scope features are delivery & lifecycle operators, not compose-surface features.

| Story | Compose rule (UNCHANGED) |
|-------|---------------------------|
| US-0091 | Feature coverage catalog anchor `<!-- readme-feature-coverage-catalog -->` (L63) + one-liners UNCHANGED — US-0116 appends narrative sections outside the catalog block. |
| US-0097 | Project README parity surface UNCHANGED — US-0116 touches framework README pair only, not project README. |
| US-0017 | Framework README parity contract UNCHANGED — US-0116 preserves byte-parity via T-004 lockstep. |
| US-0040 | Per-sprint release notes semantics UNCHANGED. |
| US-0100 | Semantic changelog UNCHANGED. |
| US-0101 | Catalog schema (DEC-0086) UNCHANGED — documented only. |
| US-0102 | Role catalog precedence (DEC-0087) UNCHANGED — documented only. |
| US-0103 | AI Decision Ledger schema/semantics UNCHANGED — documented only. |
| US-0104 | Cross-Model Adversarial Critic schema/semantics UNCHANGED — documented only. |
| US-0105 | Sovereign Memory schema/semantics UNCHANGED — documented only. |
| US-0107 | Sovereign Loop Mode schema/semantics UNCHANGED — documented only. |
| US-0108 | Parallel Instance Arbitrage schema/semantics UNCHANGED — documented only. |
| US-0109 | Self-Healing Deploy Loop schema/semantics UNCHANGED — documented only. |
| US-0110 | Goal-Based Convergence schema/semantics UNCHANGED — documented only. |
| US-0111 | Release Trigger Adapters schema/semantics UNCHANGED — documented only. |
| US-0112 | Model-Catalog Example Presets schema/semantics UNCHANGED — documented only. |
| US-0034 | Cross-repo compatibility observability schema/semantics UNCHANGED — documented only. |
| US-0084 | Codebase map freshness gate schema/semantics UNCHANGED — documented only. |
| US-0086 | Handoff hygiene validator schema/semantics UNCHANGED — documented only. |
| US-0093 | Scratchpad drift detector schema/semantics UNCHANGED — documented only. |
| US-0096 | Active context handoff schema/semantics UNCHANGED — documented only. |
| US-0041 | End-to-End Lifecycle QA schema/semantics UNCHANGED — documented only. |
| US-0062 | Installer-Owned `its_magic/` folder boundary (DEC-0045, amended by DEC-0083/US-0097) UNCHANGED — documented only. |

**23 guards UNCHANGED.**

## Non-goals

- No scratchpad canonical edits (`.cursor/scratchpad.md`, `template/.cursor/scratchpad.local.example.md`).
- No installer changes (`installer.py/ps1/sh`).
- No runbook content additions (`docs/engineering/runbook.md` — AC-7 cross-links only; all 4 anchors pre-exist).
- No `docs/developer/README.md` edits (separate audience surface; US-0097 compose guard).
- No `docs/engineering/architecture.md` edits beyond the `## US-0116` anchor already appended in the architecture phase. 4 missing feature h1 anchors (`# US-0092`, `# US-0095`, `# US-0098`, `# US-0099`) **deferred to US-0117** as DC-4 (parallel to US-0113's DC-1 — 5 anchors; US-0114's DC-2 — 2 anchors; US-0115's DC-3 — 7 anchors; US-0117 inherits 18 anchors total).
- No new tests proposed (read-only regression gates).
- No `scripts/*` edits (validators are read-only gates).
- No delivery & lifecycle script amendments (US-0092/US-0095/US-0098/US-0099 features documented only).
- **DC-4 deferral noted** for traceability; orchestrator's segment-boundary advance hook will handle at segment close. DO NOT append to `handoffs/sovereign_deferrals.jsonl` in sprint-plan phase.

## DC-4 deferral note (deferred to US-0117)

- **DC-4**: 4 missing `# US-xxxx` h1 anchors in active `docs/engineering/architecture.md` for the US-0116 family — `# US-0092`, `# US-0095`, `# US-0098`, `# US-0099`. Not a US-0116 blocker (AC-7 satisfied via runbook cross-links — all 4 features have existing verified runbook anchors). US-0117 inherits DC-1 (5) + DC-2 (2) + DC-3 (7) + DC-4 (4) = 18 total as architecture.md triad hygiene closure.
- Anchor format to use at US-0117 time: `# US-xxxx — <feature title>` (matching existing `# US-0108`, `# US-0109`, `# US-0111`, `# US-0112`, `# US-0113`, `# US-0114`, `# US-0115` format).

## Encoding hygiene prerequisite (carried from US-0114)

- Working-tree `docs/product/backlog.md` has 185 stray `0xa7` (§) bytes per R-0102 / R-0103 / R-0104. Sprint-plan phase is read-only on backlog.md. Flag to orchestrator: restore backlog.md encoding hygiene before execute so AC-4 can be re-verified post-execute. **NOT a US-0116 blocker.**

## 4th-story cumulative byte-stability surface note

US-0116 is the **first 4-cumulative-surface story** — the cumulative byte-stability surface now covers **3 prior released blocks** (US-0113's `### Sovereign-loop era keys` L1682 + US-0114's `### Release & distribution keys` L1806 + US-0115's `### Integration & observability keys` L1878). The cross-story byte-stability contract (S0114 retrospective — "net-new keys + cross-link pointers + reason-code-only entries; never edit prior story's released block") now scales to a quad. US-0116's only true net-new scratchpad key rows are US-0098's 2 dev-environment keys; the rest are grouped cross-link pointers to pre-US-0116 README surfaces + reason-code-only entries for US-0099. Execute-phase must verify `git diff HEAD -- its_magic/README.md` shows pure addition in the post-L1878 range (no removals/modifications to US-0113's L1682, US-0114's L1806, or US-0115's L1878 blocks). Pattern now established as a quad (S0113/S0114/S0115 + US-0116).

## Plan-verify readiness (ultra_lean merge note)

In **ultra_lean** delivery mode, `/plan-verify` is **merged into the `build+verify` macro under QA** — the orchestrator routes; this sprint does **not** pre-create `sprints/S0116/plan-verify.json`. The sprint-plan output is plan-verify-ready (surjective AC coverage, atomic tasks, test markers aligned) so QA can verify in one spawn within `build+verify`.

`build+verify` macro canonical phases (per ultra_lean):
1. `/execute` (dev) — first canonical phase
2. `/qa` (qa) — merges plan-verify + execute QA + verify-work

## Decision gate check

**No DECISION_GATE raised.** Architecture phase resolved all 13 R-0104 carry-overs within the `plan` macro (approach A1 locked; sprint seeds T-001..T-006; files to touch/not to touch locked; DC-4 deferred to US-0117; encoding hygiene prerequisite flagged; 4th-story cumulative byte-stability surface LOCKED). Sprint-plan revealed no question requiring operator input. Verdict: **PASS**.

## Sovereign memory note

Sprint-plan phase does NOT call `advance_sovereign_loop` (advance hook runs at segment boundary post `ship` macro). Sovereign-memory digest not re-assembled in sprint-plan (architecture phase already noted existing digest context sufficient per R-0104; US-0116 documentation-only). DC-4 deferral noted in non-goals for traceability.

Sovereign-loop pattern for curator retrospective at segment close: "delivery & lifecycle family operator documentation completes the US-0113/US-0114/US-0115/US-0116 umbrella quad under `## Commands and workflow`; cross-story byte-stability contract now covers **three** prior released blocks (US-0113 L1682 + US-0114 L1806 + US-0115 L1878) — net-new-keys-only + cross-link-pointer + reason-code-only shape is the established quad-closure pattern; US-0116 is the first 4-cumulative-surface story."

## Risks and mitigations (carried from architecture)

| ID | Risk | Severity | Sprint guard |
|----|------|----------|--------------|
| R1 | AC-3 byte-stability (4th-story cumulative surface — first 4-cumulative-surface story) — US-0116 is the fourth story to extend `### Full scratchpad reference`; cumulative surface now covers 3 prior released blocks (US-0113 L1682 + US-0114 L1806 + US-0115 L1878). Risk of accidentally editing a prior released block. | MEDIUM | T-003 mandates **net-new-keys-only (US-0098's 2 keys) + cross-link-pointer + reason-code-only (US-0099's 5 reason codes) shape** (architecture lock); US-0113's `### Sovereign-loop era keys` block + US-0114's `### Release & distribution keys` block + US-0115's `### Integration & observability keys` block byte-stability preserved. Execute-phase must verify `git diff HEAD -- its_magic/README.md` shows pure addition in the post-L1878 range (no removals/modifications to US-0113's L1682, US-0114's L1806, or US-0115's L1878 blocks). QA re-verifies. Mirrors S0114/S0115 retrospective pattern extended to 4th story. |
| R2 | AC-5 parity lockstep — `its_magic/README.md` edited but `template/its_magic/README.md` not synced (or vice versa) | MEDIUM | T-004 mandates one-way copy `its_magic/README.md` → `template/its_magic/README.md` after T-001/T-002/T-003 complete. Execute-phase runs `python -c "a=open(r'its_magic/README.md','rb').read(); b=open(r'template/its_magic/README.md','rb').read(); print('PARITY_OK' if a==b else 'PARITY_DIFF')"` (expect `PARITY_OK`) + `python scripts/check_intake_template_parity.py` (expect `[INTAKE_TEMPLATE_PARITY_OK] scope=intake`). QA re-verifies. |
| R3 | AC-2 US-0092/US-0095 angle overlap (native chain vs outer driver) — Both share `AUTO_FLOW_MODE=full_autonomy` opt-in | LOW | T-002 mandates primary/fallback boundary table mirrors runbook L1921–L1926 (US-0095 primary IDE; US-0092 fallback headless/CI or `NATIVE_CHAIN_UNAVAILABLE`). Angle-distinct narrative contract — US-0095 owns process angle (orchestrator self-chain mechanism); US-0092 owns security posture + outer-driver fallback. QA re-verifies. |
| R4 | AC-2 US-0098/US-0099 angle boundary (runtime vs install-time) — Both share the `## Dev environment auto-launch (US-0098 / DEC-0084)` h2 at runbook L244 | LOW | T-002 separates them as `#### US-0098` (execute-phase runtime gate, default-off `DEV_AUTO_LAUNCH_PROFILE`) and `#### US-0099` (install-time bootstrap, copy-when-missing, runs only on `missing` / `upgrade` / `postinstall`). Distinct narrative angles — no overlap. QA re-verifies. |
| R5 | AC-3 `DELIVERY_MODE` / `AUTO_INSTALL_DEPS` / `AUTO_RELEASE_NOTES` overlap (cross-link to US-0114) — US-0114's `### Release & distribution keys` block (L1806) owns these rows | MEDIUM→LOW | T-003 mandates cross-link pointer to US-0114's block (US-0114 owns release-workflow angle; US-0116 owns auto-chain lifecycle-shape / enablement angle); US-0116 does NOT re-document `DELIVERY_MODE` defaults. QA re-verifies. |
| R6 | AC-3 `LEAN_MEMORY_*` family overlap (cross-link to US-0115) — US-0115's `### Integration & observability keys` block (L1878) owns the canonical `LEAN_MEMORY_*` family rows per US-0096/DEC-0082 | LOW | T-003 default omit; US-0095 is angle-distinct from US-0096's `LEAN_MEMORY_*` family (process angle vs memory angle). If US-0095's subsection narrative references lean-memory composition, T-002 adds a brief single-sentence pointer ("composes with `LEAN_MEMORY_*` family documented in `### Integration & observability keys` above") — no key row duplication. |
| R7 | AC-3 `AUTO_BACKLOG_DRAIN` / `AUTO_BUG_QUEUE` overlap (cross-link to US-0044/US-0087/US-0088) — These keys are documented in pre-US-0116 README surfaces, NOT in US-0113's L1682 block | LOW | T-003 mandates grouped cross-link pointer to `### Optional /auto backlog-drain mode (US-0044)` README section (L2370) and US-0087/US-0088 catalog one-liners (L2261/L2263); NOT a cross-link to US-0113's sovereign-loop keys block (those keys are not there — confirmed in R-0104 open question #1). |
| R8 | AC-7 runbook cross-links — 4 features, all anchors pre-exist (no gap, unlike US-0114's US-0062). US-0099 has no dedicated top-level runbook h2 | LOW | T-002 uses the AC-7 cross-link format for US-0099 (L244 parent h2 with secondary pointers to L250 + L301). All 4 anchors verified in R-0104: US-0092 L1958 h3 + L1989 h4 (parent h2 = L1587); US-0095 L1900 h3 (parent h2 = L1587); US-0098 L244 h2 (top-level); US-0099 L250 (paragraph inside US-0098's h2) + L301 normative contract anchor. |
| R9 | AC-8 regression tests (4th-story cumulative surface) — coverage parity contract tests weakened or failing | LOW–MEDIUM | US-0116 documentation-only; **forbid edits** to `.cursor/scratchpad.md`, `template/.cursor/scratchpad.local.example.md`, and `tests/scratchpad_example_parity_test.py`. If a test fails, the prose is wrong, not the test — fix prose, never relax test. T-006 confirms green. |
| R10 | AC-4 encoding hygiene prerequisite (carried from US-0114) — working-tree backlog.md has 185 stray `0xa7` bytes per R-0102/R-0103/R-0104; could block validator | MEDIUM (carried) | T-005 runs `validate_readme_feature_coverage.py --enforce`; orchestrator must restore working-tree `backlog.md` encoding hygiene before execute. Catalog block L63 + US-0113/US-0114/US-0115 narrative blocks treated as read-only. NOT a US-0116 blocker (orchestrator-owned prerequisite). |
| R11 | AC-1 umbrella placement (4th sibling) — Risk of inserting the umbrella inside US-0115's block rather than after it | LOW | T-001 mandates placement after US-0115 umbrella close (before L1665 `### Full scratchpad reference`), NOT inside it. Mirrors US-0115-after-US-0114 placement pattern. QA re-verifies via grep. |
| R12 | DC-4 architecture.md h1 anchors (4 missing) — Triad-hygiene carry-over, not a US-0116 blocker | LOW | Defer to US-0117 — US-0117 inherits DC-1 (5) + DC-2 (2) + DC-3 (7) + DC-4 (4) = 18 total. AC-7 satisfied via runbook cross-links. |
| R13 | Decomposition drift — Drain mutex (US-0116 ships first; US-0117 picks up the phase & role governance family). No intentional cross-story overlap with US-0117 | LOW | Bounded by angle-distinct narrative contract; US-0116 owns delivery & lifecycle feature operator guides only; US-0117 owns phase command catalog + role governance. |
| R14 | Cross-story byte-stability contract (4th story) — US-0116 is the fourth story to extend `### Full scratchpad reference` | MEDIUM | Net-new-keys-only (US-0098's 2 keys) + reason-code-only entries (US-0099's 5 reason codes) + grouped cross-link pointers; execute verifies pure-addition `git diff` in the L1878–end range. Pattern now established as a quad (S0113/S0114/S0115 + US-0116). |

## Definition of done

- All 8 acceptance criteria covered surjectively (AC-1..AC-8 → T-001..T-006).
- T-001..T-006 executed in dependency order; all exit criteria met.
- `python -m pytest tests/scratchpad_example_parity_test.py -q` → 4 passed (no test weakenings).
- `python scripts/validate_readme_feature_coverage.py --repo . --enforce` → `[README_FEATURE_COVERAGE_VALIDATE_OK]` (exit 0).
- `python -c "a=open(r'its_magic/README.md','rb').read(); b=open(r'template/its_magic/README.md','rb').read(); print('PARITY_OK' if a==b else 'PARITY_DIFF')"` → `PARITY_OK`.
- `python scripts/check_intake_template_parity.py` → `[INTAKE_TEMPLATE_PARITY_OK] scope=intake`.
- `python scripts/validate_doc_profile.py` → PASS.
- `python scripts/check-user-visible-metadata.py` → PASS.
- `git diff HEAD -- its_magic/README.md` shows pure addition in the post-L1878 range (no removals/modifications to US-0113's L1682, US-0114's L1806, or US-0115's L1878 blocks).
- `docs/product/backlog.md` `## US-0116` retains **OPEN** through execute / qa / verify-work; closure at `/release` (US-0045).

## Next phase

Per **ultra_lean**, the orchestrator routes to the **`build+verify` macro** — `/execute` (dev, first canonical phase of `build+verify`), which then chains to `/qa` (merges plan-verify + execute QA + verify-work). Plan-verify is NOT a standalone phase in ultra_lean.

**Handoff**: `handoffs/po_to_tl.md` (sprint-plan handoff block prepended per ultra_lean artifact convention — orchestrator reads the topmost block).

**Stop**: sprint-plan complete; do not spawn the next phase. Orchestrator Task-spawns dev for `/execute`.
