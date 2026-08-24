# Architecture archive pack (2026-08-24)

- Rollover trigger: `ARCH_HOT_MAX_LINES=3000, ARCH_HOT_MAX_STORY_SECTIONS=120`
- Source: `docs/engineering/architecture.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 49
- First archived heading: `## US-0116 — Delivery & lifecycle operator documentation in framework README`
- Last archived heading: `## US-0116 — Delivery & lifecycle operator documentation in framework README`
- Verification tuple (mandatory):
  - archived_body_lines=155
  - preamble_lines=1
  - retained_body_lines=2918

---

## US-0116 — Delivery & lifecycle operator documentation in framework README

### Overview

**US-0116** is a documentation-only story closing the operator-documentation gap for the **delivery & lifecycle** functional family — US-0092 (Delivery confirmation gate / full-autonomy outer driver + security posture), US-0095 (Native in-chat auto-chain), US-0098 (Dev environment auto-launch), US-0099 (Dev-environment copy-when-missing bootstrap). It adds an umbrella `### Delivery & lifecycle (US-0092 / US-0095 / US-0098 / US-0099) umbrella section` under `## Commands and workflow` (L350) in `its_magic/README.md`, as the **4th sibling** to US-0113's `### Sovereign-loop era (US-0103–US-0112) umbrella section` (L940), US-0114's `### Release & distribution (US-0041 / US-0062 / US-0111 / US-0112) umbrella section` (L1225), and US-0115's `### Integration & observability (US-0034 / US-0084 / US-0086 / US-0093 / US-0096 / US-0101 / US-0102) umbrella section` (L1410). The umbrella carries 4 nested per-feature `#### US-xxxx` operator subsections ordered US-id-ascending (US-0092 → US-0095 → US-0098 → US-0099), inserted immediately after the closing of US-0115's umbrella block (before L1665 `### Full scratchpad reference (detailed)`). A matching `### Delivery & lifecycle keys (US-0092 / US-0095 / US-0098 / US-0099)` sub-block is appended to `### Full scratchpad reference (detailed)` (L1665) as the **4th sibling** to US-0113's `### Sovereign-loop era keys` (L1682), US-0114's `### Release & distribution keys` (L1806), and US-0115's `### Integration & observability keys` (L1878), inserted immediately after US-0115's keys block close (before L2026 `### Remote execution config`). The sub-block covers **true net-new key rows** only (US-0098's 2 dev-environment keys: `DEV_AUTO_LAUNCH_PROFILE` / `DEV_ENVIRONMENT_CONFIG`) + **reason-code-only entries** for US-0099 (`DEV_ENV_BOOTSTRAP_*` family + `DEV_ENV_PROFILE_MISSING` — 5 reason codes) + **grouped cross-link pointers** to pre-US-0116 README surfaces for US-0092/US-0095 keys + **cross-link pointers** to US-0114's `### Release & distribution keys` block for `DELIVERY_MODE` / `AUTO_INSTALL_DEPS` / `AUTO_RELEASE_NOTES` overlap + optional cross-link pointer to US-0115's `### Integration & observability keys` block for `LEAN_MEMORY_*` family (default omit — angle-distinct). The framework README pair (`its_magic/README.md` ↔ `template/its_magic/README.md`) is kept byte-identical via one-way copy. No code, schema, installer, scratchpad canonical, or runbook content changes.

**Binding decision**: **companion_dec=none** (US-0116 is documentation-only; no architectural, policy, or schema surface is being changed; R-0104 § Decision gate recommendation confirmed no DEC required — mirrors US-0113 / US-0114 / US-0115 sibling precedent; grep `^## DEC-` in `docs/engineering/decisions.md` returned no matches — confirmed no companion DEC exists). **Research anchor**: **R-0104** (delivered 2026-07-04T09:30:00Z, 8/8 open questions closed). **Compose guards (non-negotiable, 23 — UNCHANGED, cumulative across all prior stories)**: DO NOT amend US-0091, US-0097, US-0017, US-0040, US-0100, US-0101, US-0102, US-0103, US-0104, US-0105, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112, US-0034, US-0084, US-0086, US-0093, US-0096, US-0041, US-0062. **Status authority**: **OPEN** per **US-0045** (closure at `/release`).

**Fresh context marker**: `tl-US0116-architecture-20260704T094900Z-fresh`
**Orchestrator run id**: `auto-20260704-01`
**Timestamp**: 2026-07-04T09:49:00Z
**Verdict**: PASS
**Next**: `/sprint-plan`

### Companion DEC

**companion_dec = none**. US-0116 is documentation-only (mirrors US-0113 / US-0114 / US-0115 sibling precedent). No architectural, policy, or schema surface is being changed. Grep for `^## DEC-` in `docs/engineering/decisions.md` returned no matches — confirmed no US-0116 companion DEC is required and none was proposed in R-0104 § Decision gate recommendation. The DC-4 deferral (4 missing `# US-0092` / `# US-0095` / `# US-0098` / `# US-0099` h1 anchors) is a triad-hygiene carry-over to US-0117, not a tradeoff requiring a DEC.

### Approach locked — A1

**A1: Single `### Delivery & lifecycle` umbrella + 4 nested `#### US-xxxx` subsections (h4 under h3 umbrella), sibling to US-0113's `### Sovereign-loop era` (L940), US-0114's `### Release & distribution` (L1225), and US-0115's `### Integration & observability` (L1410) umbrellas, inserted immediately after the closing of US-0115's umbrella block (before L1665 `### Full scratchpad reference (detailed)`).**

**Justification**:
- **Consistency with prior stories** — US-0113 established the umbrella+subsection shape for the sovereign-loop family; US-0114 mirrored it for the release & distribution family; US-0115 mirrored it for the integration & observability family. Four sibling umbrellas in release order (US-0113 → US-0114 → US-0115 → US-0116) under `## Commands and workflow` form a clean quad.
- **Design challenge: alternatives considered.**
  - **A2 (rejected):** 4 separate top-level `### US-xxxx` h3 sections scattered under `## Commands and workflow` rather than grouped under an umbrella. Rejected: breaks the family-grouping precedent set by US-0113/US-0114/US-0115, hurts operator discoverability (no single entry point for the delivery & lifecycle family), and complicates the AC-1 acceptance criterion which explicitly requires an umbrella section.
  - **A3 (rejected):** Reuse an existing delivery & lifecycle README section as the umbrella and nest the other 3 features under it. Rejected: the existing pre-US-0116 README surfaces for US-0092/US-0095 keys (`### Automation modes` L880, `### Sync policy (US-0038)` L909, `### Optional /auto backlog-drain mode (US-0044)` L2370) are feature-mode blocks, not family-grouping blocks; elevating any one to umbrella-holder conflates a feature section with a family section, breaks byte-stability of the pre-US-0116 blocks, and breaks the family-parity contract (US-0113/US-0114/US-0115 each have a dedicated umbrella header). US-0098 has no pre-US-0116 README section at all.
  - **A1 is the only viable option** that satisfies AC-1 (umbrella section), preserves US-0113/US-0114/US-0115 sibling consistency, and respects byte-stability of prior released blocks. Lock A1.

### Files to touch

- `its_magic/README.md` — APPEND umbrella `### Delivery & lifecycle (US-0092 / US-0095 / US-0098 / US-0099) umbrella section` (after US-0115 umbrella close, before L1665) + 4 nested `#### US-xxxx` operator subsections (US-0092 → US-0095 → US-0098 → US-0099) + `### Delivery & lifecycle keys (US-0092 / US-0095 / US-0098 / US-0099)` sub-block under `### Full scratchpad reference (detailed)` (after US-0115's `### Integration & observability keys` block at L1878; before L2026 `### Remote execution config`) covering 2 net-new key rows (US-0098) + 5 reason-code-only entries (US-0099) + grouped cross-link pointers (US-0092/US-0095 → pre-US-0116 surfaces; `DELIVERY_MODE` / `AUTO_INSTALL_DEPS` / `AUTO_RELEASE_NOTES` → US-0114 L1806; optional `LEAN_MEMORY_*` → US-0115 L1878 default omit).
- `template/its_magic/README.md` — byte-identical sync via one-way copy from `its_magic/README.md` (AC-5).

### Files NOT to touch

- `.cursor/scratchpad.md` — canonical scratchpad; US-0116 documents keys in README, never edits the canonical source.
- `docs/product/backlog.md` — status authority (US-0045); encoding hygiene prerequisite flagged separately to orchestrator.
- `docs/engineering/runbook.md` — AC-7 cross-links only (all 4 anchors pre-exist); no new runbook content.
- `docs/developer/README.md` — US-0097 compose guard.
- `docs/engineering/architecture.md` — other than this US-0116 anchor append; DC-4 (4 missing h1 anchors) deferred to US-0117.
- `installer.py` / `installer.ps1` / `installer.sh`, `scripts/*`, any test file — out of scope (documentation-only story).
- **Do NOT modify US-0113's `### Sovereign-loop era` / `### Sovereign-loop era keys` blocks (L940 / L1682), US-0114's `### Release & distribution` / `### Release & distribution keys` blocks (L1225 / L1806), or US-0115's `### Integration & observability` / `### Integration & observability keys` blocks (L1410 / L1878)** in `its_magic/README.md` — byte-stability contract (all 3 already released in S0113 / S0114 / S0115). US-0116 adds cross-link pointers to these blocks from its own net-new block; it never edits them. Execute-phase must verify `git diff HEAD -- its_magic/README.md` shows pure addition in the post-L1878 range (no removals/modifications to US-0113's L1682, US-0114's L1806, or US-0115's L1878 blocks).

### Sprint seeds (T-001..T-006)

6 tasks within `SPRINT_MAX_TASKS=12` (mirror US-0113 / US-0114 / US-0115 sibling pattern; `SPRINT_AUTO_SPLIT` not triggered):

| Task | Description | ACs covered |
|------|-------------|-------------|
| **T-001** | Add umbrella `### Delivery & lifecycle (US-0092 / US-0095 / US-0098 / US-0099) umbrella section` under `## Commands and workflow` (after US-0115 umbrella close, before L1665). Default-off framing for optional runtime features (US-0092 / US-0095 opt-in via `AUTO_FLOW_MODE=full_autonomy`; US-0098 opt-in via `DEV_AUTO_LAUNCH_PROFILE`); bootstrap-on-install framing for US-0099 (install-time only, zero runtime cost). 4-step enable order (US-0099 bootstrap → US-0098 auto-launch → US-0095 native in-chat chain primary → US-0092 outer-driver fallback) + runbook pointer line + zero-overhead-when-off contract line. | AC-1 |
| **T-002** | Add 4 per-feature `#### US-xxxx` operator subsections under the umbrella, ordered US-id-ascending (US-0092 → US-0095 → US-0098 → US-0099). US-0092 = full-autonomy outer driver + DEC-0078 security posture + hard caps + native-chain-vs-outer-driver routing (US-0095 primary, US-0092 fallback) + runbook cross-link to L1958 h3 + L1989 h4 (parent h2 = `## Auto continuation resume contract` L1587). US-0095 = native in-chat auto-chain (primary IDE recipe; compose-on-US-0044 `AUTO_BACKLOG_DRAIN`; drain-advance suppression `AUTO_QUIET=1`; `AUTO_IMPLEMENTATION_LOOP` + `AUTO_PAUSE_*` interaction; grouped cross-link to `### Automation modes` L880 + main reference list; optional `LEAN_MEMORY_*` cross-link to US-0115 L1878 — default omit, angle-distinct) + runbook cross-link to L1900 h3 (parent h2 = L1587). US-0098 = `DEV_AUTO_LAUNCH_PROFILE` default-off + `DEV_ENVIRONMENT_CONFIG` path + orthogonality to US-0065 / US-0086 / US-0067 / `AUTO_REMOTE_AUTOMATION_PROFILE` + detection precedence (US-0086 remote wins over docker-host-local per DEC-0084 §3) + compose-with-US-0099 + runbook cross-link to L244 h2. US-0099 = install-time copy-when-missing bootstrap (never overwrites) + customize-after-bootstrap contract + `DEV_ENV_BOOTSTRAP_*` reason-code family (5 codes) + `DEV_ENV_PROFILE_MISSING` remediation + compose-with-US-0098 + runbook cross-link to L244 (parent h2) with secondary pointers to L250 (bootstrap paragraph) + L301 (normative contract anchor). | AC-2, AC-7 |
| **T-003** | Add `### Delivery & lifecycle keys (US-0092 / US-0095 / US-0098 / US-0099)` sub-block under `### Full scratchpad reference (detailed)` (after US-0115's `### Integration & observability keys` block L1878; before L2026 `### Remote execution config`). True net-new key rows (2): US-0098 `DEV_AUTO_LAUNCH_PROFILE=off\|deterministic_v1` (default `off`) + `DEV_ENVIRONMENT_CONFIG=repo-relative path` (default `.cursor/dev-environment.json`). Reason-code-only entries (5): US-0099 `DEV_ENV_BOOTSTRAP_COPIED` / `DEV_ENV_BOOTSTRAP_SKIPPED_EXISTS` / `DEV_ENV_BOOTSTRAP_PATH_INVALID` / `DEV_ENV_BOOTSTRAP_SOURCE_MISSING` / `DEV_ENV_PROFILE_MISSING`. Grouped cross-link pointers (no duplicate rows): US-0092/US-0095 keys (`AUTO_FLOW_MODE` / `AUTO_IMPLEMENTATION_LOOP` / `AUTO_PAUSE_*` / `AUTO_LOOP_MAX_CYCLES` / `AUTO_BACKLOG_MAX_STORIES` / `ALLOW_AUTO_PUSH` / `AUTO_PUSH_BRANCH_ALLOWLIST` / `AUTO_BACKLOG_DRAIN` / `AUTO_BUG_QUEUE` etc.) → `### Automation modes` L880 + `### Sync policy (US-0038)` L909 + `### Optional /auto backlog-drain mode (US-0044)` L2370 + main reference list (NOT to US-0113's L1682 block — those keys are not there); `DELIVERY_MODE` / `AUTO_INSTALL_DEPS` / `AUTO_RELEASE_NOTES` → US-0114's `### Release & distribution keys` block (L1806); optional `LEAN_MEMORY_*` → US-0115's `### Integration & observability keys` block (L1878) — default omit (angle-distinct per open question #2). Byte-stability of US-0113 L1682 + US-0114 L1806 + US-0115 L1878 blocks preserved (net-new-keys-only + cross-link-pointer + reason-code-only shape; 4th-story cumulative surface). | AC-3 |
| **T-004** | Sync `template/its_magic/README.md` byte-identical via one-way copy from `its_magic/README.md`. Re-run `python -c "a=open(r'its_magic/README.md','rb').read(); b=open(r'template/its_magic/README.md','rb').read(); print('PARITY_OK' if a==b else 'PARITY_DIFF')"` (expect `PARITY_OK`) + `python scripts/check_intake_template_parity.py` (expect `[INTAKE_TEMPLATE_PARITY_OK] scope=intake`). | AC-5 |
| **T-005** | Run validators: `python scripts/validate_readme_feature_coverage.py --enforce` (expect `[README_FEATURE_COVERAGE_VALIDATE_OK]` exit 0 — catalog block L63 read-only) + `python scripts/validate_doc_profile.py` (expect `[DOC_PROFILE_VALIDATE_OK]`) + `python scripts/check-user-visible-metadata.py` (expect exit 0; US-IDs only in parenthetical catalog tags `(US-xxxx)`). | AC-4, AC-6 |
| **T-006** | Run regression tests: `python -m pytest tests/scratchpad_example_parity_test.py -q` (expect 4/4 PASS). **Forbid edits** to `.cursor/scratchpad.md`, `template/.cursor/scratchpad.local.example.md`, and `tests/scratchpad_example_parity_test.py` — if a test fails, the prose is wrong, not the test (fix prose, never relax test). | AC-8 |

**Execution order**: T-001 (umbrella) → T-002 (4 subsections) → T-003 (scratchpad ref extension) → T-004 (template byte-sync) → T-005 (validators) → T-006 (regression tests). Acyclic, mirrors US-0113/US-0114/US-0115.

### Test markers

Same 5 as US-0113 / US-0114 / US-0115 (no new tests proposed):

1. `tests/scratchpad_example_parity_test.py` — 4 markers (AC-5 indirect via scratchpad canonical parity, AC-8).
2. `scripts/validate_readme_feature_coverage.py --enforce` — AC-4.
3. `scripts/check_intake_template_parity.py` — AC-5.
4. `scripts/validate_doc_profile.py` — AC-6.
5. `scripts/check-user-visible-metadata.py` — AC-6.

### Compose guards (UNCHANGED — 23 guards, cumulative)

US-0116 is documentation-only and lives entirely outside the compose surface. The 23 compose guards (cumulative across all prior stories — same 23 as US-0115; US-0116 adds no new family-internal guards because all 4 in-scope features are delivery & lifecycle operators, not compose-surface features) remain UNCHANGED:

US-0091, US-0097, US-0017, US-0040, US-0100, US-0101, US-0102, US-0103, US-0104, US-0105, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112, US-0034, US-0084, US-0086, US-0093, US-0096, US-0041, US-0062.

### Stop conditions

**stop_conditions_met=yes**:

- **No DEC required** — confirmed (companion_dec=none; documentation-only; mirrors US-0113 / US-0114 / US-0115 sibling precedent; R-0104 § Decision gate recommendation confirmed no DEC candidate; grep `^## DEC-` in decisions.md returned no matches).
- **No feasibility unknown** — R-0104 closed all 8 spec open questions (cross-link-only to pre-US-0116 surfaces for US-0092/US-0095; `LEAN_MEMORY_*` angle-distinct default omit; `DELIVERY_MODE` bidirectional cross-link to US-0114; `AUTO_INSTALL_DEPS`/`AUTO_RELEASE_NOTES` cross-link to US-0114; runbook anchor h-levels CONFIRMED — US-0092 L1958 h3 + L1989 h4, US-0095 L1900 h3, US-0098 L244 h2, US-0099 L250 inside US-0098 h2 + L301 normative contract anchor; DC-4 deferred to US-0117; 4th-story byte-stability contract LOCKED; `AUTO_LOOP_MAX_CYCLES` / `AUTO_BACKLOG_MAX_STORIES` exact key names CONFIRMED).
- **No data migration risk** — documentation-only; no schema, no data, no installer, no scratchpad canonical changes.

### DC-4 resolution (deferred to US-0117)

**DC-4**: 4 missing `# US-xxxx` h1 anchors in active `docs/engineering/architecture.md` for the US-0116 family — `# US-0092`, `# US-0095`, `# US-0098`, `# US-0099`. Grep for `^# US-(0092|0095|0098|0099)` in `docs/engineering/architecture.md` returned no matches (confirmed in R-0104 § DC-4 confirmation; only present in archive packs; US-0098/US-0099 are referenced as `# US-0098` / `# US-0099` (bootstrap posture) in runbook L301 but have no dedicated h1 in active `architecture.md`). Not a US-0116 blocker — AC-7 is satisfiable via runbook cross-links (all 4 features have existing verified runbook anchors). US-0117 (Phase & role governance family) inherits DC-1 (5 anchors from US-0113: US-0103/0104/0105/0107/0110) + DC-2 (2 anchors from US-0114: US-0041/US-0062) + DC-3 (7 anchors from US-0115: US-0034/US-0084/US-0086/US-0093/US-0096/US-0101/US-0102) + DC-4 (4 anchors from US-0116: US-0092/US-0095/US-0098/US-0099) = **18 total missing `# US-xxxx` h1 anchors** as architecture.md triad hygiene closure.

**Deferral note for orchestrator**: This is a **deferral candidate** for the orchestrator's segment-boundary advance hook. **DO NOT append to `handoffs/sovereign_deferrals.jsonl` in architecture phase** (per instructions — segment-boundary advance hook handles it, not phase boundaries). `/architecture` documents the deferral in this findings block; does NOT add the h1 anchors. When US-0117 enters `plan` macro, its discovery should narrow-read this section and add the 4 missing h1 anchors as a task seed. Anchor format to use at that time: `# US-xxxx — <feature title>` (matching existing `# US-0108`, `# US-0109`, `# US-0111`, `# US-0112`, `# US-0113`, `# US-0114`, `# US-0115` format).

### Risks (finalized)

| Risk | Severity | Mitigation |
|------|----------|------------|
| **AC-3 byte-stability (4th-story cumulative surface — first 4-cumulative-surface story)** — US-0116 is the fourth story to extend `### Full scratchpad reference`; cumulative surface now covers 3 prior released blocks (US-0113 L1682 + US-0114 L1806 + US-0115 L1878). Risk of accidentally editing a prior released block. | **MEDIUM** | Net-new-keys-only (US-0098's 2 keys) + reason-code-only entries (US-0099's 5 reason codes) + grouped cross-link pointers LOCKED in `/architecture` (T-003). Execute-phase must verify `git diff HEAD -- its_magic/README.md` shows pure addition in the post-L1878 range (no removals/modifications to US-0113's L1682, US-0114's L1806, or US-0115's L1878 blocks). QA re-verifies. Mirrors S0114 / S0115 retrospective pattern extended to 4th story. |
| **AC-5 parity lockstep** — `its_magic/README.md` edited but `template/its_magic/README.md` not synced (or vice versa). | **MEDIUM** | T-004 mandates one-way copy `its_magic/README.md` → `template/its_magic/README.md` after T-001/T-002/T-003 complete. Execute-phase must re-run byte-parity check + `check_intake_template_parity.py`. QA re-verifies both gates. |
| **AC-2 US-0092/US-0095 angle overlap (native chain vs outer driver)** — Both share `AUTO_FLOW_MODE=full_autonomy` opt-in. | **LOW** | Primary/fallback boundary table mirrors runbook L1921–L1926 (US-0095 primary IDE; US-0092 fallback headless/CI or `NATIVE_CHAIN_UNAVAILABLE`). Angle-distinct narrative contract — US-0095 owns process angle (orchestrator self-chain mechanism); US-0092 owns security posture + outer-driver fallback. |
| **AC-2 US-0098/US-0099 angle boundary (runtime vs install-time)** — Both share the `## Dev environment auto-launch (US-0098 / DEC-0084)` h2 at runbook L244. | **LOW** | US-0098 = execute-phase runtime gate (default-off `DEV_AUTO_LAUNCH_PROFILE`); US-0099 = install-time bootstrap (copy-when-missing, runs only on `missing` / `upgrade` / `postinstall`). Distinct narrative angles — no overlap. T-002 separates them as `#### US-0098` and `#### US-0099` subsections under the umbrella. |
| **AC-3 `DELIVERY_MODE` / `AUTO_INSTALL_DEPS` / `AUTO_RELEASE_NOTES` overlap (cross-link to US-0114)** — US-0114's `### Release & distribution keys` block (L1806) owns these rows. | **MEDIUM→LOW** | Cross-link pointer to US-0114's block (T-003); US-0116 does NOT re-document `DELIVERY_MODE` defaults; US-0114 owns those rows. Angle-distinct: US-0114 = release-workflow angle; US-0116 = auto-chain lifecycle-shape / enablement angle. |
| **AC-3 `LEAN_MEMORY_*` family overlap (cross-link to US-0115)** — US-0115's `### Integration & observability keys` block (L1878) owns the canonical `LEAN_MEMORY_*` family rows per US-0096/DEC-0082. | **LOW** | Default omit; US-0095 is angle-distinct from US-0096's `LEAN_MEMORY_*` family (process angle vs memory angle). If the US-0095 composition narrative is essential, T-002 adds a brief single-sentence pointer ("composes with `LEAN_MEMORY_*` family documented in `### Integration & observability keys` above") — no key row duplication. |
| **AC-3 `AUTO_BACKLOG_DRAIN` / `AUTO_BUG_QUEUE` overlap (cross-link to US-0044/US-0087/US-0088)** — These keys are documented in pre-US-0116 README surfaces, NOT in US-0113's L1682 block. | **LOW** | Grouped cross-link pointer to `### Optional /auto backlog-drain mode (US-0044)` README section (L2370) and US-0087/US-0088 catalog one-liners (L2261/L2263); NOT a cross-link to US-0113's sovereign-loop keys block (those keys are not there — confirmed in R-0104 open question #1). |
| **AC-7 runbook cross-links** — 4 features, all anchors pre-exist (no gap, unlike US-0114's US-0062). US-0099 has no dedicated top-level runbook h2. | **LOW** | All 4 anchors verified in R-0104: US-0092 L1958 h3 + L1989 h4 (parent h2 = `## Auto continuation resume contract` L1587); US-0095 L1900 h3 (parent h2 = L1587); US-0098 L244 h2 (top-level); US-0099 L250 (paragraph inside US-0098's h2) + L301 normative contract anchor. T-002 uses the AC-7 cross-link format for US-0099 (L244 parent h2 with secondary pointers to L250 + L301). |
| **AC-4 encoding hygiene prerequisite (carried from US-0114)** — Working-tree `docs/product/backlog.md` has 185 stray `0xa7` (§) bytes per R-0102 / R-0103 / R-0104. Orchestrator must restore encoding hygiene before execute so AC-4 can be re-verified post-execute. | **MEDIUM (carried)** | `/architecture` makes no backlog.md edits. Flag to orchestrator: restore backlog.md encoding hygiene before execute. NOT a US-0116 blocker (research + architecture are read-only on backlog.md). |
| **AC-8 regression tests (4th-story cumulative surface)** — coverage parity contract tests weakened or failing. | **LOW–MEDIUM** | US-0116 is documentation-only; **forbid edits** to `.cursor/scratchpad.md`, `template/.cursor/scratchpad.local.example.md`, and `tests/scratchpad_example_parity_test.py` in execute-phase task list. If a test fails, fix prose, never relax test. T-006 confirms green. |
| **AC-1 umbrella placement (4th sibling)** — Risk of inserting the umbrella inside US-0115's block rather than after it. | **LOW** | Insert after US-0115 umbrella close (before L1665 `### Full scratchpad reference`), NOT inside it. Mirrors US-0115-after-US-0114 placement pattern. |
| **DC-4 architecture.md h1 anchors (4 missing)** — Triad-hygiene carry-over, not a US-0116 blocker. | **LOW** | Defer to US-0117 — US-0117 inherits DC-1 (5) + DC-2 (2) + DC-3 (7) + DC-4 (4) = 18 total. AC-7 satisfied via runbook cross-links. |
| **Decomposition drift** — Drain mutex (US-0116 ships first; US-0117 picks up the phase & role governance family). No intentional cross-story overlap with US-0117. | **LOW** | Bounded by angle-distinct narrative contract; US-0116 owns delivery & lifecycle feature operator guides only; US-0117 owns phase command catalog + role governance. |
| **Cross-story byte-stability contract (4th story)** — US-0116 is the fourth story to extend `### Full scratchpad reference`. | **MEDIUM** | Net-new-keys-only (US-0098's 2 keys) + reason-code-only entries (US-0099's 5 reason codes) + grouped cross-link pointers; execute verifies pure-addition `git diff` in the L1878–end range. Pattern now established as a quad (S0113/S0114/S0115 + US-0116). |

### Decision gate check

**No DECISION_GATE raised.** Architecture phase revealed no question requiring operator input. All 13 R-0104 carry-overs resolved by tech-lead within the `plan` macro:

1. Umbrella placement confirmed — immediately after the closing of the US-0115 integration & observability umbrella block (before L1665 `### Full scratchpad reference`), NOT inside it.
2. Scratchpad reference extension placement confirmed — immediately after the closing of US-0115's `### Integration & observability keys` block (L1878); before L2026 `### Remote execution config`. NOT inside US-0115's block.
3. 4 per-feature subsection ordering confirmed — US-id-ascending (US-0092 → US-0095 → US-0098 → US-0099).
4. US-0092/US-0095 grouped cross-link pointer to pre-US-0116 README surfaces confirmed (no net-new key rows for US-0092/US-0095).
5. US-0098 net-new key rows confirmed (`DEV_AUTO_LAUNCH_PROFILE` / `DEV_ENVIRONMENT_CONFIG` — the only true net-new key rows in the delivery & lifecycle keys sub-block).
6. US-0099 reason-code-only entries confirmed (5 reason codes — `DEV_ENV_BOOTSTRAP_*` family + `DEV_ENV_PROFILE_MISSING`; no scratchpad key block).
7. Cross-link pointer to US-0114's `### Release & distribution keys` block (L1806) for `DELIVERY_MODE` / `AUTO_INSTALL_DEPS` / `AUTO_RELEASE_NOTES` overlap confirmed (byte-stability — US-0114 owns those rows).
8. Optional cross-link pointer to US-0115's `### Integration & observability keys` block (L1878) for `LEAN_MEMORY_*` family overlap — default omit confirmed (angle-distinct per R-0104 open question #2 resolution).
9. DC-4 deferral confirmed — 4 missing h1 anchors (US-0092 / US-0095 / US-0098 / US-0099) deferred to US-0117 (US-0117 inherits 18 total).
10. Working-tree backlog.md encoding hygiene regression (185 stray 0xa7 bytes per R-0102 / R-0103 / R-0104) flagged to orchestrator for execute coordination.
11. Angle boundary for US-0092 vs US-0095 confirmed — US-0095 = primary (IDE native chain); US-0092 = optional fallback (headless/CI or `NATIVE_CHAIN_UNAVAILABLE`).
12. Angle boundary for US-0098 vs US-0099 confirmed — US-0098 = execute-phase runtime gate (default-off); US-0099 = install-time bootstrap (copy-when-missing, runs only on `missing` / `upgrade` / `postinstall`).
13. `#### US-0099` AC-7 cross-link format confirmed — points to L244 (parent h2 `## Dev environment auto-launch (US-0098 / DEC-0084)`) with secondary pointers to L250 (the bootstrap paragraph) and L301 (normative contract anchor `# US-0098` / `# US-0099` (bootstrap posture)); US-0099 does NOT have a dedicated top-level runbook h2.

No sovereign-memory digest call needed (US-0116 is documentation-only; existing digest context sufficient per R-0104 — S0113/S0114/S0115 retrospectives established the reusable patterns applied here; the cross-link pointer pattern + angle-distinct narrative pattern + cross-story byte-stability contract now form a quad). Verdict: **PASS**.

### Sovereign memory note

`assemble_sovereign_memory_digest(...)` NOT called (US-0116 documentation-only; existing digest context sufficient per R-0104). Sovereign-loop pattern for curator retrospective at segment close: "delivery & lifecycle family operator documentation completes the US-0113/US-0114/US-0115/US-0116 umbrella quad under `## Commands and workflow`; cross-story byte-stability contract now covers **three** prior released blocks (US-0113 L1682 + US-0114 L1806 + US-0115 L1878) — net-new-keys-only + cross-link-pointer + reason-code-only shape is the established quad-closure pattern; US-0116 is the first 4-cumulative-surface story." No write to `mistakes.jsonl` in architecture phase.

### Consequences

- Sprint: S0116 (pending `/sprint-plan`).
- Status authority: **OPEN** per **US-0045**; closure at `/release`.
- Framework README pair grows by umbrella + 4 subsections + scratchpad reference extension (both `its_magic/README.md` and `template/its_magic/README.md` byte-identical).
- 4 missing `architecture.md` h1 anchors deferred to US-0117 (DC-4, parallel to US-0113's DC-1 — 5 anchors, US-0114's DC-2 — 2 anchors, and US-0115's DC-3 — 7 anchors; US-0117 inherits 18 total).
- No new tests; no new DECs; no compose-surface changes.

### Evidence references

- `docs/product/backlog.md` — `## US-0116` block (lines 3947–3963, 8 ACs)
- `docs/engineering/research.md` — `R-0104` (delivered 2026-07-04T09:30:00Z, 8/8 open questions closed; 4 per-feature sub-findings)
- `handoffs/po_to_tl.md` — research handoff (topmost block) + spec handoff
- `docs/engineering/state.md` — research checkpoint (latest) + architecture checkpoint (this phase, appended)
- `handoffs/resume_brief.md` — top block updated to reflect architecture complete
- `.cursor/scratchpad.md` — delivery & lifecycle keys (L11–22 auto implementation loop / pause policy, L30–38 full-autonomy interaction, L41–56 backlog drain / bug queue, L63 active, L142–148 sync policy / auto-push allowlist, L173–186 delivery mode / lean memory, L201 release publish, L295–298 dev auto-launch profile) — canonical source for AC-3 extension (net-new + cross-links)
- `its_magic/README.md` — L350 (`## Commands and workflow`) umbrella target; L880 (`### Automation modes` — pre-US-0116 US-0092/US-0095 surface, grouped cross-link target); L909 (`### Sync policy (US-0038)` — pre-US-0116 US-0092 surface, grouped cross-link target); L940 (`### Sovereign-loop era` US-0113 sibling umbrella — byte-stability preserved); L1225 (`### Release & distribution` US-0114 sibling umbrella — byte-stability preserved); L1410 (`### Integration & observability` US-0115 sibling umbrella — byte-stability preserved); L1665 (`### Full scratchpad reference (detailed)`) extension target; L1682 (`### Sovereign-loop era keys` US-0113 sibling block — byte-stability preserved); L1806 (`### Release & distribution keys` US-0114 sibling block — byte-stability preserved + cross-link target for `DELIVERY_MODE` / `AUTO_INSTALL_DEPS` / `AUTO_RELEASE_NOTES`); L1878 (`### Integration & observability keys` US-0115 sibling block — byte-stability preserved + optional cross-link target for `LEAN_MEMORY_*`); L2026 (`### Remote execution config`) — confirmed insertion point for `### Delivery & lifecycle keys` block (before this line); L2261/L2263 (US-0087/US-0088 catalog one-liners — pre-US-0116 grouped cross-link targets); L2370 (`### Optional /auto backlog-drain mode (US-0044)` — pre-US-0116 grouped cross-link target for `AUTO_BACKLOG_DRAIN` / `AUTO_BUG_QUEUE` family)
- `docs/engineering/runbook.md` — 4 anchors: US-0092 L1958 h3 + L1989 h4 (parent h2 = `## Auto continuation resume contract` L1587); US-0095 L1900 h3 (parent h2 = L1587); US-0098 L244 h2 (top-level); US-0099 L250 (paragraph inside US-0098 h2) + L301 (normative contract anchor)
- `docs/engineering/architecture.md` — h1 inventory confirmed: `# US-0111` (L335), `# US-0112` (L454), `# US-0113` (L717), `# US-0114` (L914), `# US-0115` (L1117) exist; `# US-0092`/`# US-0095`/`# US-0098`/`# US-0099` missing (deferred to US-0117 as DC-4)
- `docs/engineering/decisions.md` — DEC-0078 (US-0092 security posture), DEC-0080 (US-0095 native chain), DEC-0081 (US-0095 orchestrator continuation), DEC-0082 (US-0096 delivery modes, referenced via `LEAN_MEMORY_*` overlap), DEC-0084 (US-0098/US-0099 dev environment + bootstrap posture), DEC-0018 (sync policy disabled, referenced via `AUTO_PUSH_BRANCH_ALLOWLIST`), DEC-0038 (runtime proof) — referenced, not amended; no US-0116 companion DEC (grep `^## DEC-` returned no matches)



