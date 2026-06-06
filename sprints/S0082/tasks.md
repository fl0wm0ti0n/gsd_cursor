# Sprint S0082 Tasks — US-0093

**sprint_id**: S0082  
**story_refs**: US-0093  
**dec_ref**: DEC-0079 (binding; composes on DEC-0078, US-0065, US-0066)  
**task_count**: 10  
**within_limit**: true (10 ≤ `SPRINT_MAX_TASKS=12`); `SPRINT_AUTO_SPLIT` not triggered  
**bijection**: AC-1..AC-10 ↔ T-001..T-010 (strict 1:1 per architecture `# US-0093` § Atomic task seeds)

> No implementation or test code is authored in this phase — dev owns that in `/execute`.

---

## T-001 — Scratchpad `UAT_BROWSER_PROBE_MODE` + poll/fallback keys (active + template + local example) — AC-1

- **ac_ref**: AC-1
- **dec_ref**: DEC-0079 §2 (scratchpad keys); architecture `# US-0093` § Scratchpad contract
- **description**: Extend scratchpad comment block and key defaults for **`UAT_BROWSER_PROBE_MODE=cursor|http_fallback|playwright_fallback`** (default **`cursor`**), **`UAT_BROWSER_FALLBACK_CHAIN=0|1`** (default **`1`**), **`UAT_PROCESS_HEALTH_POLL_SECONDS`** (default **`60`**), **`UAT_PROCESS_HEALTH_POLL_INTERVAL_SECONDS`** (default **`2`**), optional **`DEV_SERVER_PORT`** / **`DEV_SERVER_COMMAND`**. Document orthogonality with **`PERMISSION_MODE`**, Cursor browser approval modes, and **`runtime-connectivity.md`** health URLs. Ship byte-identical locked strings in active + `template/` scratchpad family + `.cursor/scratchpad.local.example.md`.
- **files_affected**:
  - `.cursor/scratchpad.md`
  - `.cursor/scratchpad.local.example.md`
  - `template/.cursor/scratchpad.md`
  - `template/.cursor/scratchpad.local.example.md`
- **parity_touchpoints**: DEC-0079 §11 row 3 (scratchpad family).
- **acceptance_check**:
  - Comment block documents all three `UAT_BROWSER_PROBE_MODE` literals with default **`cursor`**.
  - Poll and fallback keys documented with defaults; CI **`http_fallback`** recipe pointer present.
  - Interaction bullets cite **`PERMISSION_MODE`**, browser approval, **`runtime-connectivity.md`** — not automation level.
  - Active/template/local-example locked key strings byte-identical where mirrored.
- **status**: done

---

## T-002 — Extend `uat_probe_lib.py`: mode resolution, `execution_tier`, fallback chain + agent-browser MCP command excerpts — AC-2

- **ac_ref**: AC-2
- **dec_ref**: DEC-0079 §1, §3, §5 (two-tier + MCP sequence + fallback); architecture `# US-0093` § Two-tier diagram, § Agent-browser MCP sequence
- **description**: Extend **`scripts/uat_probe_lib.py`** (+ byte-identical **`template/scripts/`** mirror): mode resolution from scratchpad; emit probe plans with **`execution_tier=agent|stdlib`** for **`browser_smoke`**; stdlib HTTP GET + optional Playwright subprocess fallback when MCP unavailable; **`--merge-result <fragment.json>`** helper stub (validation wiring completed in T-005). Add normative subsection **`### Browser UAT self-test (US-0093)`** to **`.cursor/commands/verify-work.md`**, **`qa.md`**, **`execute.md`** (+ template) — navigate → interact → screenshot → console/network → write **`browser_evidence_refs`**. Lib **never** calls browser MCP directly (**BUG-0006**).
- **files_affected**:
  - `scripts/uat_probe_lib.py`
  - `template/scripts/uat_probe_lib.py`
  - `.cursor/commands/verify-work.md`
  - `.cursor/commands/qa.md`
  - `.cursor/commands/execute.md`
  - `template/.cursor/commands/verify-work.md`
  - `template/.cursor/commands/qa.md`
  - `template/.cursor/commands/execute.md`
- **parity_touchpoints**: DEC-0079 §11 rows 1–2.
- **acceptance_check**:
  - Classified **`browser_smoke`** in **`cursor`** mode returns plan + **`UAT_PROBE_UNRESOLVED`** until agent completes — no fabricated evidence.
  - HTTP fallback path reachable when **`UAT_BROWSER_PROBE_MODE=http_fallback`** or MCP-unavailable heuristic fires.
  - Command excerpts document seven-step MCP sequence and evidence write-back to **`uat.json`**.
  - Active / template script and command delta strings byte-identical per US-0017.
- **status**: done

---

## T-003 — `manual_operator` verb routing in `classify_step` — AC-3

- **ac_ref**: AC-3
- **dec_ref**: DEC-0079 §4 (verb routing); architecture `# US-0093` § `manual_operator` verb routing
- **description**: Extend **`classify_step`** in **`uat_probe_lib.py`** (+ template mirror) with judgment-deny vs automatable-UI token table. **Precedence: judgment tokens win** over UI verbs. Automatable UI signals (`click`, `fill`, `navigate`, `smoke`, `form`, `submit`, `button`, `page load`, `scroll`, `ui`, `browser`, etc.) reclassify to **`browser_smoke`** when URL/stack resolves. Judgment-only steps remain **`manual_operator`** → **`UAT_PROBE_UNRESOLVED`**. Secret paths → **`UAT_PROBE_FORBIDDEN`** unchanged.
- **files_affected**:
  - `scripts/uat_probe_lib.py`
  - `template/scripts/uat_probe_lib.py`
- **parity_touchpoints**: DEC-0079 §11 row 1.
- **acceptance_check**:
  - Mixed-verb example `"operator visually confirms button click"` → judgment wins → unresolved.
  - Automatable UI step with resolvable URL → **`browser_smoke`** plan emitted.
  - Generic manual without UI verbs → **`manual_operator`** unresolved.
  - **`--self-test`** covers judgment, automatable, forbidden, and generic manual fixture classes.
- **status**: done

---

## T-004 — Complete `process_health` + `cli_smoke` execution branches — AC-4

- **ac_ref**: AC-4
- **dec_ref**: DEC-0079 §6 (stub completion); architecture `# US-0093` § Stub completion
- **description**: Replace stub branches in **`execute_probe`** for **`process_health`** and **`cli_smoke`**. **`process_health`**: extract startup command (backtick, quoted, regex, **`package.json`**, **`DEV_SERVER_COMMAND`** override); poll **`_read_health_url`** every **`UAT_PROCESS_HEALTH_POLL_INTERVAL_SECONDS`** until 2xx or cap → **`UAT_PROBE_PASS`** | **`UAT_PROBE_TIMEOUT`** | **`UAT_PROBE_FAILED`**. **`cli_smoke`**: backtick command parse; exit-code assertion; optional stdout substring — no LLM inference.
- **files_affected**:
  - `scripts/uat_probe_lib.py`
  - `template/scripts/uat_probe_lib.py`
- **parity_touchpoints**: DEC-0079 §11 row 1.
- **acceptance_check**:
  - **`process_health`** no longer returns **`UAT_PROBE_UNRESOLVED`** when command + health URL resolve.
  - **`cli_smoke`** executes subprocess and asserts exit code when command parse succeeds.
  - Reason codes remain in **DEC-0078** family; fail-closed on unresolvable parse.
  - **`--self-test`** includes process_health and cli_smoke positive + timeout fixtures.
- **status**: done

---

## T-005 — Evidence schema + `browser_evidence_refs` + `qa-findings.md` mirror contract — AC-5

- **ac_ref**: AC-5
- **dec_ref**: DEC-0079 §7 (evidence schema); architecture `# US-0093` § Evidence schema
- **description**: Lock **`probe_results[]`** extension with **`browser_evidence_refs`** fields (`navigation_url`, `screenshots[]` max 5, `console_summary`, `network_summary` — paths/counts only). Implement **`python scripts/uat_probe_lib.py --merge-result <fragment.json>`** validation: **`passed=true`** in **`cursor`** mode requires non-empty **`navigation_url`** + at least one screenshot or summary path — else downgrade to **`UAT_BROWSER_PROBE_FAILED`**. Document artifact layout **`sprints/Sxxxx/evidence/browser/`** in command docs and **`qa-findings.md`** **Runtime browser evidence** subsection template (**US-0065** AC-6).
- **files_affected**:
  - `scripts/uat_probe_lib.py`
  - `template/scripts/uat_probe_lib.py`
  - `.cursor/commands/verify-work.md`
  - `.cursor/commands/qa.md`
  - `template/.cursor/commands/verify-work.md`
  - `template/.cursor/commands/qa.md`
- **parity_touchpoints**: DEC-0079 §11 rows 1–2.
- **acceptance_check**:
  - JSON fragment schema matches DEC-0079 §7 example shape.
  - **`--merge-result`** rejects PASS without required evidence refs in **`cursor`** mode.
  - Command docs cite evidence paths and max screenshot cardinality.
  - No inline secrets in JSON — path refs only.
- **status**: done

---

## T-006 — New `UAT_BROWSER_*` reason codes + extended `--self-test` + MCP-unavailable heuristic — AC-6

- **ac_ref**: AC-6
- **dec_ref**: DEC-0079 §8 (reason codes); §5 (MCP-unavailable heuristic); architecture `# US-0093` § Reason codes, § Fallback selection
- **description**: Add reason codes **`UAT_BROWSER_UNAVAILABLE`**, **`UAT_BROWSER_PROBE_FAILED`**, **`UAT_BROWSER_PROBE_TIMEOUT`**. Extend **`--self-test`** fixture matrix for MCP-unavailable (**`CI=true`**, missing browser MCP inventory), fallback chain success/fail, and timeout paths. Wire deterministic MCP-unavailable heuristic (CI env, tool inventory, origin allowlist block). No silent PASS when browser + fallback both fail.
- **files_affected**:
  - `scripts/uat_probe_lib.py`
  - `template/scripts/uat_probe_lib.py`
  - `.cursor/commands/verify-work.md`
  - `.cursor/commands/qa.md`
  - `template/.cursor/commands/verify-work.md`
  - `template/.cursor/commands/qa.md`
- **parity_touchpoints**: DEC-0079 §11 rows 1–2.
- **acceptance_check**:
  - All three new codes emitted in documented scenarios; existing **DEC-0078** codes unchanged.
  - **`--self-test`** → **`[UAT_PROBE_LIB_SELF_TEST_OK]`** with browser fixture classes.
  - CI / headless path records **`UAT_BROWSER_UNAVAILABLE`** before fallback attempt when configured.
  - Command docs list new codes alongside existing probe vocabulary.
- **status**: done

---

## T-007 — Security deny-list assert + no credential fill documentation — AC-7

- **ac_ref**: AC-7
- **dec_ref**: DEC-0079 §9 (security); architecture `# US-0093` § Security
- **description**: Verify and document security invariants: no auto-read **`.env`**, no password/credential auto-fill in browser MCP sequence, no intake evidence mutation, **`UAT_PROBE_FORBIDDEN`** unchanged for secret paths. Respect Cursor origin/approval guardrails in command excerpts. Confirm **DEC-0078** §8 deny-list **not weakened** — add contract-test negative markers as needed (completed in T-009 cross-ref).
- **files_affected**:
  - `scripts/uat_probe_lib.py` (forbidden-path guards — extends existing)
  - `template/scripts/uat_probe_lib.py`
  - `.cursor/commands/verify-work.md`
  - `.cursor/commands/qa.md`
  - `.cursor/commands/execute.md`
  - `template/.cursor/commands/` mirrors
- **parity_touchpoints**: DEC-0079 §11 rows 1–2.
- **acceptance_check**:
  - Step containing **`.env`** / **`password`** / **`credential`** → **`UAT_PROBE_FORBIDDEN`** (not browser route).
  - MCP sequence docs explicitly forbid credential field fill.
  - No new code paths read **`.env`** or mutate **`handoffs/intake_evidence/`**.
  - Security callout present in operator docs (cross-ref T-008).
- **status**: done

---

## T-008 — Runbook + `auto-orchestration-reference.md` operator recipe — AC-8

- **ac_ref**: AC-8
- **dec_ref**: DEC-0079 §10 (operator docs); architecture `# US-0093` § Operator docs
- **description**: Add operator recipe: enable browser self-test keys, dev-server detection (**`package.json`** + **`DEV_SERVER_PORT`**), evidence locations under **`sprints/Sxxxx/evidence/browser/`**, fallback behavior (**`http_fallback`** for CI), **`@browser`** / Agent panel manual override. Ship byte-identical subsections in **`docs/engineering/runbook.md`** and **`docs/engineering/auto-orchestration-reference.md`** (+ template mirrors).
- **files_affected**:
  - `docs/engineering/runbook.md`
  - `docs/engineering/auto-orchestration-reference.md`
  - `template/docs/engineering/runbook.md`
  - `template/docs/engineering/auto-orchestration-reference.md`
- **parity_touchpoints**: DEC-0079 §11 row 4.
- **acceptance_check**:
  - Runbook documents **`UAT_BROWSER_PROBE_MODE`** enablement and CI **`http_fallback`** recipe.
  - Evidence path convention and **`--merge-result`** usage documented.
  - **`@browser`** manual override recipe present.
  - Active / template doc delta strings byte-identical per US-0017.
- **status**: done

---

## T-009 — Contract tests `test_us0093_*` + optional harness §32 — AC-9

- **ac_ref**: AC-9
- **dec_ref**: DEC-0079 §11 (contract tests); architecture `# US-0093` § Contract-test expectations
- **description**: Extend **`tests/auto_command_contract_test.py`** (active-only) with markers: **`UAT_BROWSER_PROBE_MODE`** in scratchpad; **`browser_evidence_refs`** in verify-work + qa excerpts; **`UAT_BROWSER_UNAVAILABLE`**, **`UAT_BROWSER_PROBE_FAILED`**, **`UAT_BROWSER_PROBE_TIMEOUT`** in lib + docs; negative assert docs do **not** imply stdlib alone PASSes **`browser_smoke`** in **`cursor`** mode without evidence refs. Optional harness **§32** in **`tests/run-tests.ps1`** / **`.sh`** for **`pytest -k us0093`**.
- **files_affected**:
  - `tests/auto_command_contract_test.py`
  - `tests/run-tests.ps1` (optional §32)
  - `tests/run-tests.sh` (optional §32)
- **parity_touchpoints**: DEC-0079 §11 rows 6–8 (active-only tests).
- **acceptance_check**:
  - All positive markers pass after T-001..T-008 deliverables.
  - Negative marker fails if silent-PASS prose reintroduced.
  - Tests do not weaken **DEC-0078** / spawn-only contract markers.
  - `pytest -k us0093` green post-execute.
- **status**: done

---

## T-010 — Template parity `--scope=us-0093` + installer manifest + architecture linkage assert — AC-10

- **ac_ref**: AC-10
- **dec_ref**: DEC-0079 §11 (template parity); architecture `# US-0093` § Template parity; **US-0017**
- **description**: Wire **`python scripts/check_intake_template_parity.py --scope=us-0093`** 8-row inventory. Update **`docs/engineering/context/installer-owned-paths.manifest`** (+ template) if new paths touched. Add read-only architecture linkage assert subtest referencing **DEC-0079**, **US-0092**, **DEC-0078**, **US-0065**, **R-0041**. Run full parity verification on touched surfaces from T-001..T-009.
- **files_affected**:
  - `scripts/check_intake_template_parity.py` (scope table if not already wired)
  - `docs/engineering/context/installer-owned-paths.manifest`
  - `template/docs/engineering/context/installer-owned-paths.manifest`
  - `tests/auto_command_contract_test.py` (linkage assert — extends T-009)
- **parity_touchpoints**: DEC-0079 §11 full inventory verification.
- **acceptance_check**:
  - `check_intake_template_parity.py --scope=us-0093` exits 0 on clean tree post-execute.
  - All 8 parity rows from DEC-0079 §11 satisfied.
  - Linkage subtest asserts `# US-0093` references **DEC-0079** and compose-on stories.
  - No duplicate parity logic inside probe lib.
- **status**: done

---

## Recommended /execute ordering

1. **T-001** — scratchpad mode keys (foundation for lib mode resolution)
2. **T-003** — verb routing (parallel OK with T-004 after T-001)
3. **T-004** — process_health / cli_smoke completion (parallel OK with T-003)
4. **T-002** — browser execution tier + command MCP excerpts (depends T-001, T-003)
5. **T-005** — evidence schema + `--merge-result` (depends T-002)
6. **T-006** — reason codes + self-test fixtures (depends T-002, T-005)
7. **T-007** — security invariants (depends T-002 command excerpts)
8. **T-008** — operator docs (depends T-001 keys + T-006 fallback semantics)
9. **T-009** — contract tests (depends T-001..T-008 stable)
10. **T-010** — template parity + linkage (depends all delivery tasks)
