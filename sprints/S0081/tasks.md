# Sprint S0081 Tasks — US-0092

**sprint_id**: S0081  
**story_refs**: US-0092  
**dec_ref**: DEC-0078 (binding; composes on US-0088, DEC-0062, DEC-0047, DEC-0048)  
**task_count**: 10  
**within_limit**: true (10 ≤ `SPRINT_MAX_TASKS=12`); `SPRINT_AUTO_SPLIT` not triggered  
**bijection**: AC-1..AC-10 ↔ T-001..T-010 (strict 1:1 per architecture `# US-0092` § Atomic task seeds)

> No implementation or test code is authored in this phase — dev owns that in `/execute`.

---

## T-001 — Scratchpad `AUTO_FLOW_MODE` enum + new keys (active + template + local example) — AC-1

- **ac_ref**: AC-1
- **dec_ref**: DEC-0078 §1 (flow-mode contract); architecture `# US-0092` § Scratchpad contract
- **description**: Extend scratchpad comment block and key defaults for **`AUTO_FLOW_MODE=manual|auto_until_decision|full_autonomy`** (exact literals; **`full_autonomy`** default-off). Add **`AUTO_BLOCK_RETRY_MAX`** (default **`3`**) and **`AUTO_OUTER_DRIVER_TIMEOUT_SECONDS`** (optional unset). Document interaction with **`PHASE_MODE`**, **`PERMISSION_MODE`**, **`AUTO_BACKLOG_DRAIN`**, **`AUTO_BUG_QUEUE`**, safety caps (**`AUTO_LOOP_MAX_CYCLES`**, **`AUTO_BACKLOG_MAX_STORIES`**). Ship byte-identical locked strings in active + `template/` scratchpad family + `.cursor/scratchpad.local.example.md`.
- **files_affected**:
  - `.cursor/scratchpad.md`
  - `.cursor/scratchpad.local.example.md`
  - `template/.cursor/scratchpad.md`
  - `template/.cursor/scratchpad.local.example.md`
- **parity_touchpoints**: DEC-0078 §9 row 1 (scratchpad family).
- **acceptance_check**:
  - Comment block documents all three `AUTO_FLOW_MODE` literals including **`full_autonomy`**.
  - `AUTO_BLOCK_RETRY_MAX=3` and `AUTO_OUTER_DRIVER_TIMEOUT_SECONDS` documented with defaults.
  - Interaction matrix bullets cite drain, bug-queue, caps, TOKEN_PROFILE orthogonality pointer.
  - Active/template/local-example locked key strings byte-identical where mirrored.
- **status**: pending

---

## T-002 — Implement `scripts/auto_outer_driver.py` (stdlib, argv/exit codes, activation gate) — AC-2

- **ac_ref**: AC-2
- **dec_ref**: DEC-0078 §2 (outer-driver script); architecture `# US-0092` § Outer-driver script API
- **description**: Create stdlib-only **`scripts/auto_outer_driver.py`** (+ byte-identical **`template/scripts/`** mirror). Implement argv flags (`--repo`, `--max-cycles`, `--max-stories`, `--dry-run`, `--invoke-cmd`), activation gate requiring merged **`AUTO_FLOW_MODE=full_autonomy`** (else exit **2** `AUTO_FLOW_MODE_NOT_FULL_AUTONOMY`), loop body polling **`resume_brief`** + **`state.md`**, and exit-code vocabulary **0/1/2/3/4/5/6/124** per architecture table. Spawn-only — loops invocations, never performs phase-role work.
- **files_affected**:
  - `scripts/auto_outer_driver.py` (new)
  - `template/scripts/auto_outer_driver.py` (new — byte-identical)
- **parity_touchpoints**: DEC-0078 §9 row 2.
- **acceptance_check**:
  - Stdlib-only imports (`argparse`, `json`, `hashlib`, `pathlib`, `subprocess`, `re`, `datetime`).
  - `--dry-run` emits planned `/auto` hook invocations without side effects.
  - Wrong `AUTO_FLOW_MODE` → exit **2** with reason token present.
  - All documented exit codes reachable via test paths or `--self-test` helper.
  - Active / template script SHA-256 equal.
- **status**: pending

---

## T-003 — Implement `scripts/uat_probe_lib.py` + wire `/verify-work` / `/qa` command excerpts — AC-3

- **ac_ref**: AC-3
- **dec_ref**: DEC-0078 §3 (UAT probe contract); architecture `# US-0092` § UAT probe contract
- **description**: Create shared stdlib resolver **`scripts/uat_probe_lib.py`** (+ template mirror) mapping acceptance steps to probe kinds (**build**, **test**, **api_health**, **process_health**, **browser_smoke**, **cli_smoke**, **manual_operator**). Fail-closed reason codes: **`UAT_PROBE_UNRESOLVED`**, **`UAT_STACK_PROFILE_UNKNOWN`**, **`UAT_PROBE_TIMEOUT`**, **`UAT_PROBE_FAILED`**, **`UAT_PROBE_FORBIDDEN`**, **`UAT_PROBE_PASS`**. Update **`.cursor/commands/verify-work.md`** and **`.cursor/commands/qa.md`** (+ template) with self-verify excerpt: derive UAT steps, execute probes, record evidence in **`uat.json`** / **`qa-findings.md`**; no silent PASS.
- **files_affected**:
  - `scripts/uat_probe_lib.py` (new)
  - `template/scripts/uat_probe_lib.py` (byte-identical)
  - `.cursor/commands/verify-work.md`
  - `.cursor/commands/qa.md`
  - `template/.cursor/commands/verify-work.md`
  - `template/.cursor/commands/qa.md`
- **parity_touchpoints**: DEC-0078 §9 rows 3–4.
- **acceptance_check**:
  - Probe catalog covers all seven kinds with stack-profile resolution hooks.
  - Unresolvable step returns **`UAT_PROBE_UNRESOLVED`** (not PASS).
  - Command excerpts cite shared resolver and evidence paths.
  - Active / template command delta strings byte-identical per US-0017.
- **status**: pending

---

## T-004 — Block-retry ledger writer + cap interaction in driver/orchestrator docs — AC-4

- **ac_ref**: AC-4
- **dec_ref**: DEC-0078 §4 (block-retry ledger); architecture `# US-0092` § Block-retry ledger
- **description**: Implement append-only ledger writer to **`handoffs/auto_block_retry/<orchestrator_run_id>.jsonl`** with names-only fields (`attempt_id`, `timestamp`, `orchestrator_run_id`, `story_id`, `stop_reason`, `reason_code`, `remediation_action`, `outcome`, `outer_cycle_index`, `implementation_loop_index`). Wire cap interaction in outer driver: recoverable **`blocked`**, transient **`missing_input`**, UAT/QA fail under **`AUTO_IMPLEMENTATION_LOOP=1`** retry within **`AUTO_BLOCK_RETRY_MAX`**; hard stop **`BLOCK_RETRY_CAP_EXHAUSTED`** (exit **6**). Document ledger + caps in auto orchestration reference.
- **files_affected**:
  - `scripts/auto_outer_driver.py` (ledger integration — extends T-002)
  - `handoffs/auto_block_retry/` (directory + `.gitkeep` or sample schema doc if needed)
  - `docs/engineering/auto-orchestration-reference.md` (+ template mirror for touched §)
- **parity_touchpoints**: Active-only ledger runtime path; reference doc positive parity.
- **acceptance_check**:
  - Ledger records append without secrets; JSONL one record per line.
  - Cap exhaustion yields exit **6** and reason token in driver output.
  - Cap interaction table documented (outer cycles, implementation loop, block retry, drain breadth).
  - Recoverable vs hard stops distinguished per stop matrix.
- **status**: pending

---

## T-005 — Drain-without-pause branch in outer driver + DEC-0069 boundary refresh — AC-5

- **ac_ref**: AC-5
- **dec_ref**: DEC-0078 §5 (drain-without-pause); architecture `# US-0092` § Drain-without-pause; **DEC-0069**
- **description**: Extend outer driver loop: on segment completion + **`AUTO_BACKLOG_DRAIN`** / bug-queue policy, schedule next OPEN story/bug **immediately** without operator pause. Ensure **`resume_brief`** + **`state.md`** refresh at every boundary per **DEC-0069**. Driver must not require manual re-**`/auto`** between drained items when **`AUTO_FLOW_MODE=full_autonomy`**.
- **files_affected**:
  - `scripts/auto_outer_driver.py` (drain-advance branch — extends T-002, T-004)
  - `.cursor/commands/auto.md` (+ template) drain-advance cross-ref if needed
- **parity_touchpoints**: Driver script parity via T-002; auto.md optional excerpt parity.
- **acceptance_check**:
  - `--dry-run` shows immediate next-item scheduling after simulated segment complete.
  - `BACKLOG_MAX_STORIES_REACHED` → exit **4** when cap hit.
  - Boundary refresh documented: paired `resume_brief` + `state.md` update at drain handoff.
  - No operator pause required between items when full_autonomy + drain enabled.
- **status**: pending

---

## T-006 — TOKEN_PROFILE orthography audit + grep fixes (runbook conflict, README family) — AC-6

- **ac_ref**: AC-6
- **dec_ref**: DEC-0078 §6 (TOKEN_PROFILE orthogonality); architecture `# US-0092` § TOKEN_PROFILE orthogonality audit
- **description**: Audit and fix conflicting prose: remove runbook “lowers default automation breadth” (active + template); ensure scratchpad comments state **`TOKEN_PROFILE`** = context breadth / token cost **only**. Grep scope: scratchpad comments, **`auto-orchestration-reference.md`**, **`runbook.md`**, README family, **`auto.md`** cross-refs. Eliminate forbidden patterns (`automation breadth`, `TOKEN_PROFILE.*drain`, `lean.*less automation`, etc.).
- **files_affected**:
  - `.cursor/scratchpad.md` (+ template + local example comments)
  - `docs/engineering/runbook.md`
  - `docs/engineering/auto-orchestration-reference.md`
  - `template/docs/engineering/runbook.md`
  - `template/docs/engineering/auto-orchestration-reference.md`
  - `README.md` / `template/README.md` (only if conflicting strings found)
- **parity_touchpoints**: DEC-0078 §9 rows 6–7, 9.
- **acceptance_check**:
  - Forbidden-pattern grep returns zero hits in scope after fix.
  - Runbook conflict string removed active + template.
  - Normative sentence **`TOKEN_PROFILE controls context breadth / token cost only`** present in reference docs.
  - No prose implies TOKEN_PROFILE gates automation, drain, or outer-driver invocation.
- **status**: pending

---

## T-007 — Stop matrix in `auto.md`, `auto-orchestration-reference.md` — AC-7

- **ac_ref**: AC-7
- **dec_ref**: DEC-0078 §7 (stop matrix); architecture `# US-0092` § Stop matrix
- **description**: Document full_autonomy stop matrix in **`.cursor/commands/auto.md`** and **`docs/engineering/auto-orchestration-reference.md`** (+ template mirrors): which gates remain non-suppressible (decision_gate, isolation, strict-proof, publish, security) vs relaxable transient stops; **`RELEASE_PUBLISH_MODE=auto`** explicit opt-in unchanged. Cross-link architecture `# US-0092` without rewriting `# US-0088` body.
- **files_affected**:
  - `.cursor/commands/auto.md`
  - `template/.cursor/commands/auto.md`
  - `docs/engineering/auto-orchestration-reference.md`
  - `template/docs/engineering/auto-orchestration-reference.md`
- **parity_touchpoints**: DEC-0078 §9 rows 5–6.
- **acceptance_check**:
  - Stop matrix table or equivalent lists hard vs relaxable rows per architecture.
  - `RELEASE_PUBLISH_MODE=auto` documented as explicit publish opt-in.
  - `full_autonomy` delta column distinguishes outer-driver re-invocation behavior.
  - Active / template stop-matrix strings byte-identical.
- **status**: pending

---

## T-008 — Contract tests in `auto_command_contract_test.py` — AC-8

- **ac_ref**: AC-8
- **dec_ref**: DEC-0078 §8 (contract tests); architecture `# US-0092` § Contract-test expectations
- **description**: Extend **`tests/auto_command_contract_test.py`** (active-only) with markers: **`AUTO_FLOW_MODE=full_autonomy`** literal in scratchpad; **`TOKEN_PROFILE controls context breadth / token cost only`**; drain-advance-without-operator phrases; post-execute assert **`scripts/auto_outer_driver.py`** exists + runbook **`Full-autonomy outer driver (US-0092)`** heading; negative assert runbook lacks forbidden automation-breadth conflict string.
- **files_affected**:
  - `tests/auto_command_contract_test.py`
- **parity_touchpoints**: Active-only (tests).
- **acceptance_check**:
  - All positive markers pass after T-001..T-007 deliverables.
  - Negative marker fails if runbook conflict string reintroduced.
  - Tests do not weaken existing US-0088 / spawn-only contract markers.
  - `pytest -k` filter for US-0092 markers green post-execute.
- **status**: pending

---

## T-009 — Template parity + installer manifest entries — AC-9

- **ac_ref**: AC-9
- **dec_ref**: DEC-0078 §9 (template parity); architecture `# US-0092` § Surfaces; **US-0017**
- **description**: Ensure all touched surfaces mirror per **US-0017**: add **`auto_outer_driver.py`**, **`uat_probe_lib.py`** to **`docs/engineering/context/installer-owned-paths.manifest`** (+ template). Run **`python scripts/check_intake_template_parity.py --repo .`** on touched scope; fix any drift. Verify command/rules/runbook/scratchpad pairs from T-001..T-007.
- **files_affected**:
  - `docs/engineering/context/installer-owned-paths.manifest`
  - `template/docs/engineering/context/installer-owned-paths.manifest`
  - (parity verification only for surfaces delivered in prior tasks)
- **parity_touchpoints**: DEC-0078 §9 full inventory verification.
- **acceptance_check**:
  - Manifest lists new script paths active + template byte-identical.
  - `check_intake_template_parity.py --repo .` exits 0 on clean tree post-execute.
  - All positive-parity rows from sprint.md inventory satisfied.
  - No duplicate parity logic inside outer driver or probe lib.
- **status**: pending

---

## T-010 — Runbook `### Full-autonomy outer driver (US-0092)` + security deny-list callout — AC-10

- **ac_ref**: AC-10
- **dec_ref**: DEC-0078 §10 (security); architecture `# US-0092` § Security; § Runbook
- **description**: Add runbook subsection **`### Full-autonomy outer driver (US-0092)`**: enable keys → **`python scripts/auto_outer_driver.py --repo .`** once → interpret exit table. Include security deny-list callout: no auto-read **`.env`**, no intake evidence mutation, no publish without **`RELEASE_PUBLISH_MODE=auto`**; ledgers names-only. Ship byte-identical subsection in **`template/docs/engineering/runbook.md`**.
- **files_affected**:
  - `docs/engineering/runbook.md`
  - `template/docs/engineering/runbook.md`
- **parity_touchpoints**: DEC-0078 §9 row 7.
- **acceptance_check**:
  - Exact heading `### Full-autonomy outer driver (US-0092)` present active + template.
  - Operator recipe: enable `AUTO_FLOW_MODE=full_autonomy` → run driver once → exit code table.
  - Security callout lists `.env`, intake mutation, publish gate constraints.
  - Active / template runbook subsection byte-identical.
- **status**: pending

---

## Recommended /execute ordering

1. **T-001** — scratchpad contract (foundation for driver activation gate)
2. **T-002** — outer driver shell (stdlib, argv, exit codes)
3. **T-003** — UAT probe lib + command excerpts (parallel OK with T-002 after T-001)
4. **T-004** — block-retry ledger (depends T-002)
5. **T-005** — drain-without-pause branch (depends T-002, T-004)
6. **T-006** — TOKEN_PROFILE audit (parallel OK with T-007 after T-001)
7. **T-007** — stop matrix docs (parallel OK with T-006)
8. **T-008** — contract tests (depends T-001..T-007 stable)
9. **T-009** — template parity + manifest (depends all delivery tasks)
10. **T-010** — runbook + security (depends T-002 exit table; can parallel T-009)
