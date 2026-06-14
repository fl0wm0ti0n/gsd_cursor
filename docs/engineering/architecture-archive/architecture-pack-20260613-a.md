# Architecture archive pack (2026-06-13)

- Rollover trigger: `ARCH_HOT_MAX_LINES=3000, ARCH_HOT_MAX_STORY_SECTIONS=120`
- Source: `docs/engineering/architecture.md`
- Archived units (oldest first, contiguous prefix): 3
- Retained units in hot file: 15
- First archived heading: `# BUG-0008: CRLF `installer-owned-paths.manifest` → empty `install_include_paths` on Linux global npm`
- Last archived heading: `# US-0088: `/auto` continuous multi-phase loop + quiet backlog drain`
- Verification tuple (mandatory):
  - archived_body_lines=258
  - preamble_lines=10
  - retained_body_lines=2920

---

# BUG-0008: CRLF `installer-owned-paths.manifest` → empty `install_include_paths` on Linux global npm

## Overview

**`BUG-0008`** fixes global Linux installs where **`its-magic`** aborts with **`[INSTALL_MANIFEST_ERROR] install_include_paths section is empty`** even though the packaged manifest visibly lists paths. Research **`R-0069`** locks the root cause: CRLF line endings leave section headers as **`[install_include_paths]\r`**, so POSIX **`awk`** strict equality **`$0 == "[" s "]"`** in **`installer.sh`** **`get_manifest_paths`** never enters the section. **`US-0084`** (LF **`installer.sh`**, **`.gitattributes`**, prepublish guards) is adjacent but does not replace this bug’s manifest-section contract or publish/E2E closure.

## Assumption challenge and alternatives

| Option | Summary | Verdict |
|--------|---------|---------|
| A | Rely on **`.gitattributes`** + publish hygiene only | **Insufficient alone** — defensive parse still required for tarballs already in the wild and for any future CR leakage. |
| B | Replace **`awk`** with a heavier parser (Python/node) in **`installer.sh`** path | **Rejected** — breaks POSIX **`sh`** installer contract and scope. |
| C | Strip trailing **`\\r`** per line before section match + enforce LF at source + prepublish CR scan (**chosen**) | **Chosen** — minimal runtime fix + deterministic prevention (**R-0069**). |

## Normative contract

1. **Runtime (POSIX)**: **`get_manifest_paths`** in **`installer.sh`** must **`sub(/\\r$/, \"\")`** (or equivalent) on every line **before** section-header comparison and path emission so **`[install_include_paths]`** matches under CRLF inputs.
2. **Source / npm tarball**: Repo **`.gitattributes`** includes **`*.manifest text eol=lf`** so Git checkouts and packaged manifests default to LF.
3. **Prepublish**: **`scripts/guard_installer_publish.py`** (and **`template/scripts/`** parity) rejects byte **`\\r`** in **both** active and template **`installer-owned-paths.manifest`** paths (and existing **`installer.sh`** CR rules remain).
4. **Windows installer parity**: **`installer.ps1`** **`Get-ManifestSection`** trims carriage return (e.g. **`TrimEnd('`r')`**) before section logic, matching **`BUG-0008`** intake expectations.
5. **Canonical status**: **`BUG-0008`** remains **OPEN** in **`docs/product/backlog.md`** until **`/verify-work`** / release path per **US-0045**; do not mark **DONE** from architecture alone.

## Operator-facing reason codes

- **No new codes** for this architecture. Existing installer stderr remains **`[INSTALL_MANIFEST_ERROR] install_include_paths section is empty`** when the section is still empty after parse (should not reproduce for CRLF once mitigations ship; other empty-section causes keep the same literal).
- **Maintainer-facing** (prepublish): **`guard_installer_publish`** continues to emit deterministic **`guard_installer_publish: ...`** messages when **`\\r`** is present in **`installer.sh`** or manifest paths.

## Shipped in-repo mitigations (execute already landed; sprint may verify only)

- **`installer.sh`**: **`get_manifest_paths`** awk body strips trailing CR before **`/^\[/`** section match (**BUG-0008** comment in-tree).
- **`.gitattributes`**: **`*.manifest text eol=lf`**.
- **`scripts/guard_installer_publish.py`** + **`template/scripts/guard_installer_publish.py`**: CR rejection on packaged manifest paths.
- **`tests/installer_manifest_crlf_bug0008_test.py`**: CRLF fixture vs awk logic aligned with **`get_manifest_paths`**.
- **`tests/run-tests.sh`** / **`tests/run-tests.ps1`**: section **26P2** invokes the Python test.
- **`installer.ps1`**: **`Get-ManifestSection`** CR trim parity.

## Remaining delivery (not satisfied by doc-only architecture)

1. **Version bump** per release policy and **`npm publish`** so operators receive a tarball **after** the mitigations (broken field example: **`its-magic@0.1.2-40`**).
2. **Debian global E2E**: **`npm install -g`** the new version; **`cat -A`** on installed template manifest (no **`^M$`**); **`its-magic --target <repo> --mode missing`** (or equivalent) **without** **`[INSTALL_MANIFEST_ERROR]`** — align with backlog **done_definition** / intake evidence.
3. **`R-0069`**: set **closed** with a delivery closure stanza when **`BUG-0008`** is **DONE** (post-QA/release), same pattern as other research items tied to shipped defects.

## Regression obligations (sprint / CI)

| Gate | Obligation |
|------|------------|
| **26P2** | **`tests/run-tests.sh`** / **`tests/run-tests.ps1`** must keep **`installer_manifest_crlf_bug0008_test.py`** wired; **PASS** on PR and release candidates. |
| **Prepublish** | **`python scripts/guard_installer_publish.py`** (or **`npm`** **`prepublishOnly`** hook as wired) **PASS** — rejects CR in **`installer.sh`** and both manifest copies. |
| **Parity** | Template copies of **`guard_installer_publish.py`** and manifests stay aligned with root (**US-0084** / template policy). |

## Risks

| Risk | Mitigation |
|------|------------|
| Operators stay on old global version | Explicit publish + release notes / version bump task in sprint. |
| **26P2** skipped in custom CI | Document that **`run-tests`** section **26P2** is part of installer regression surface. |
| Only LF tested; mixed encodings | Current scope is CR strip + LF enforcement; BOM or other encodings out of scope unless product expands **R-0069**. |

## Decision linkage

- Research basis: **`R-0069`**
- Related: **`BUG-0008`**, **`US-0084`**, **`US-0045`**, installer contracts (**`DEC-0068`** shell path context)

---

# US-0087: `/auto` explicit bug targeting (OPEN bug queue / single `BUG-####`)

## Overview

**`US-0087`** adds a **default-off**, **fail-closed** bug-scheduler path for **`/auto`**: operators may bind continuation metadata to **one** **`BUG-####`** or to a deterministic **all OPEN bugs** queue (canonical **`docs/product/backlog.md`** **`## Bug issues (canonical)`**, ascending **numeric** id), then run the **same resolved phase plan** (**`US-0070`** / **`DEC-0052`**) **per bug** or per bounded queue segment—without in-process phase execution (**`BUG-0006`** / **`US-0069`** / **`AUTO_ORCHESTRATOR_PHASE_EXECUTION`**). Story-only **`AUTO_BACKLOG_DRAIN`** (**`US-0044`** / **`DEC-0022`**) remains a **separate** scheduler; this section locks **one active scheduler** rules and **AC-10** breadcrumbs. Research basis: **`R-0070`** (delivery closure moves with story **DONE**).

## Assumption challenge and alternatives

| Option | Summary | Verdict |
|--------|---------|---------|
| A | Fold bug drain into **`AUTO_BACKLOG_DRAIN`** as a profile | **Rejected** — selection rules, sort keys, and backlog sections differ (**`R-0070`**). |
| B | Bug cursor in **`state.md`** only; no **`resume_brief`** updates | **Rejected** — **`RESUME_BRIEF_STALE`** risk vs **`DEC-0069`** / **`BUG-0005`**. |
| C | Dedicated **`AUTO_BUG_*`** surface + argv mirror + hard scheduler mutex / argv override (**chosen**) | **Chosen** — explicit operator semantics and testable literals. |

## Architecture-locked scratchpad keys (merged; `template/` parity)

All **default-off** when unset; sprint implements in **`.cursor/scratchpad.md`** + **`template/.cursor/scratchpad.local.example.md`** (and any documented merge layers).

| Key | Values | Role |
|-----|--------|------|
| **`AUTO_BUG_QUEUE`** | **`0`** \| **`1`** | Master enable for bug-targeted **`/auto`** ( **`0`** = legacy behavior only). |
| **`AUTO_BUG_TARGET`** | **`all-open`** \| **`BUG-####`** | Required when **`AUTO_BUG_QUEUE=1`** (unless **explicit argv** supplies the target for that invocation — see precedence). |
| **`AUTO_BUG_MAX_ITEMS`** | non-negative integer | Optional cap on bugs consumed **per orchestrator run** for **`all-open`**; **`0`** or unset = no cap beyond queue. |
| **`AUTO_BUG_ON_BLOCK`** | **`stop`** \| **`skip`** | When a bug segment hits a **pause/stop** boundary: halt queue vs advance to next id (deterministic doc + tests). |

**Naming note**: **`AUTO_BUG_MAX_ITEMS`** is the **architecture-locked** name for “max bugs per run” (**AC-2** / **AC-4**); do not introduce parallel spellings without a **DEC** amendment.

## Architecture-locked `/auto` argv syntax (**AC-1**)

Canonical tokens (exact strings for docs + **`tests/auto_command_contract_test.py`**):

1. **Single OPEN bug**: **`bug-target=BUG-####`** (example: **`bug-target=BUG-0007`**) as a **`/auto`** argument token (space-delimited command argv as today’s Cursor command style documents).
2. **All OPEN bugs (ordered queue)**: **`bug-target=all-open`**.

**Aliases**: **none** in v1 — reduces **AC-7** / reference drift; future aliases require architecture bump + contract test row.

## Precedence and scheduler mutex (**AC-3**)

Resume-source order remains: **explicit `start-from`** > **explicit bug-target / story-drain argv** (if any) > **merged scratchpad** > **`handoffs/resume_brief.md`** > **`docs/engineering/state.md`** fallback — extended so **bug-target argv** is unambiguously parsed **before** scratchpad scheduler keys.

**One active scheduler** (fail-closed):

- If merged scratchpad has **`AUTO_BACKLOG_DRAIN=1`** (or equivalent active story drain) **and** **`AUTO_BUG_QUEUE=1`** **and** the invocation does **not** include an explicit **`bug-target=`** argv token that selects the bug scheduler for this run → **`AUTO_SCHEDULER_CONFLICT`** (documented with **`[AUTO_RESUME_ERROR]`** envelope in **`docs/engineering/auto-orchestration-reference.md`**; literal token **architecture-locked** here).
- When **explicit `bug-target=`** argv is present, it **selects** the bug scheduler for that invocation; **`AUTO_BACKLOG_DRAIN`** must **not** also drive story selection **for the same run** (orchestrator materialization picks **one** queue; story drain keys are **ignored** when argv bug-target wins — document in reference).

## Fail-closed reason codes (**AC-1**, **AC-4**, **AC-8**)

| Code | When |
|------|------|
| **`AUTO_BUG_QUEUE_EMPTY`** | **`bug-target=all-open`** (or equivalent) and **zero** OPEN bugs in canonical section. |
| **`AUTO_BUG_TARGET_UNKNOWN`** | Malformed id, wrong pattern, or **`BUG-####`** not found in canonical bug section. |
| **`AUTO_BUG_TARGET_NOT_OPEN`** | Known id but status **not** **OPEN** (e.g. **DONE**). |
| **`AUTO_SCHEDULER_CONFLICT`** | Story backlog drain + bug queue both enabled per mutex rule above without resolving argv. |

Existing codes (**`PHASE_POLICY_CONFLICT`**, **`START_FROM_PHASE_PLAN_EMPTY_INTERSECTION`**, **`RESUME_BRIEF_STALE`**, etc.) stay **orthogonal** — do **not** overload them for the table above.

## `DEC-0069` / `resume_brief` alignment (**AC-5**)

- **Single-bug segment**: **`resume_brief`** carries **`bug_id`**, **`intended_resume_phase`**, and boundary timestamps consistent with **`DEC-0069`** (post-intake refresh pattern applies where bug intake occurs; mid-queue segments refresh at **lawful** orchestrator boundaries so **`/auto`** without **`start-from`** does not false-trigger **`RESUME_BRIEF_STALE`**).
- **Multi-bug (`all-open`)**: After each bug’s terminal boundary (e.g. **`refresh-context`** completion or explicit queue stop), **either** refresh **`resume_brief`** with the **next** **`bug_id`** + cursor **or** document a **single** fail-closed exception path where **`state.md`** cursor is authoritative **only** if paired with a **non-stale** brief predicate (**R-0070** preference: paired updates; architecture **defaults** to **brief + state** paired writes at segment boundaries).

## Phase boundary visibility — **AC-10** locked fields

In addition to existing **`orchestrator_run_id`**, **`phase_boundary`**, **`next_scheduled_phase`**, **`story_id`**, **`bug_id`**, **`sprint_id`**:

| Field | Purpose |
|-------|---------|
| **`segment_work_item_kind`** | **`story`** — portfolio/meta **`US-0087`** planning segments without an active defect; **`bug`** — defect lifecycle segment. |
| **`active_bug_id`** | **`BUG-####`** actively bound **or** **`(none)`** when **`segment_work_item_kind=story`**. |
| **`bug_queue_position`** | 1-based index into the **deterministic** OPEN-bug ordering for the **current** bug segment when **`bug-target=all-open`**; omit or **`(none)`** for single-target runs without queue semantics. |
| **`bug_queue_remaining`** | Count of OPEN bugs **after** the current position in the same ordering (integer or **`(none)`**). |
| **`backlog_drain_active`** | Boolean: story **`AUTO_BACKLOG_DRAIN`** is driving scheduling **this** run. |
| **`bug_queue_active`** | Boolean: bug scheduler (**argv** or **`AUTO_BUG_*`**) is driving **this** run. |

**Invariant**: **`backlog_drain_active`** and **`bug_queue_active`** must **not** both be **true** for the same materialized run (matches mutex).

## Surfaces (execute phase)

| Path | Change |
|------|--------|
| **`.cursor/commands/auto.md`** | Inputs, precedence, optional bug-queue stub, fail-fast codes, **AC-10** pointer. |
| **`docs/engineering/auto-orchestration-reference.md`** | Normative §**Optional bug-queue mode** adjacent backlog-drain; resume precedence; reason-code list; **AC-10** tuple. |
| **`template/`** | Byte/literal parity for command + reference + scratchpad examples (**AC-10**). |
| **`tests/auto_command_contract_test.py`** | Markers for **`bug-target=`** argv literals, **`AUTO_SCHEDULER_CONFLICT`**, template parity (**AC-7**). |
| **`docs/engineering/runbook.md`** | Operator recipe **“targeted bug auto drain”** (**AC-9**). |

## Verification strategy

- Contract tests + template parity (**AC-7**, **AC-10**).
- Scripted matrix: argv-only bug target; scratchpad-only; conflict **`AUTO_BACKLOG_DRAIN` + `AUTO_BUG_QUEUE`**; empty OPEN queue; **DONE** bug id.
- **Triad**: **`python scripts/enforce-triad-hot-surface.py`** after hot-surface mutations (**`DEC-0054`**).

## Risks

| Risk | Mitigation |
|------|------------|
| Double scheduling | Mutex + booleans + **`AUTO_SCHEDULER_CONFLICT`**. |
| **`RESUME_BRIEF_STALE`** on queue advance | Paired **`resume_brief`** refresh at segment boundaries (**`DEC-0069`**). |
| Reason-code / literal drift | Single **# US-0087** vocabulary + **`auto_command_contract_test.py`**. |
| Template lag | Same edit set for **`template/`** paths (**AC-10**). |

## Decision linkage

- Research: **`R-0070`**
- Related: **`US-0044`**, **`DEC-0022`**, **`DEC-0069`**, **`BUG-0005`**, **`US-0070`**, **`DEC-0052`**, **`US-0079`**, **`DEC-0061`**, **`BUG-0006`**, **`US-0069`**, **`US-0080`**, **`DEC-0062`**

---

# US-0088: `/auto` continuous multi-phase loop + quiet backlog drain

## Overview

**`US-0088`** hardens **story-centric** **`/auto`** so a **single orchestrated run** (or a **documented equivalent outer driver** — see **AC-1 equivalence** below) advances through **all intersected lifecycle phases** in order until a **deterministic stop**, while **`AUTO_BACKLOG_DRAIN=1`** (**`US-0044`** / **`DEC-0022`**) can advance **OPEN** stories **without routine operator chatter** except where **AC-2** requires visibility. Normative multi-phase iteration lives in **`docs/engineering/auto-orchestration-reference.md`** **`## Steps`** item **5** (cross-anchor: **“reference Step 5”**); **`.cursor/commands/auto.md`** compact steps **must** point to that block unambiguously so **“Step 5”** cannot be confused with compact step numbering (**per `R-0071`**).

**Spawn-only** (**`BUG-0006`** / **`US-0069`** / **`AUTO_ORCHESTRATOR_PHASE_EXECUTION`**) is **unchanged**: the orchestrator **never** substitutes for a phase-role subagent.

**`US-0087`** bug-queue scheduler, argv literals, **`AUTO_SCHEDULER_CONFLICT`**, and **AC-10** bug tuple fields remain **architecture-locked** in **`# US-0087`** only — **no duplicate** bug-queue semantics here.

## Assumption challenge and alternatives (AC-1)

| Option | Summary | Verdict |
|--------|---------|---------|
| A | **Single Cursor `/auto` invocation** schedules **N** fresh subagent turns until stop | **Preferred default** when product/runtime allows — matches reference Step 5 literally. |
| B | **Documented outer driver** (operator or script re-invokes **`/auto`** with **`start-from`** / refreshed **`resume_brief`**) | **Allowed** only if **deterministically equivalent**: same phase order, same isolation + **DEC-0038** proofs per phase, same stop reasons — must be **named explicitly** in **`auto.md`**, reference, and runbook (**AC-1** / **AC-7**). |
| C | Rely on **`TOKEN_PROFILE=lean`** alone for “quiet” | **Rejected** — **`TOKEN_PROFILE`** is **context breadth / token-cost** (**`DEC-0035`** / **`US-0080`**), **not** notification policy (**per `R-0071`**). |

## Stop matrix (deterministic)

| Condition | Stop / advance | Operator notify (**AC-2**) |
|-----------|----------------|---------------------------|
| **Intersected plan** has **next** phase and no hard stop | **Continue** → preflight **US-0069** → spawn next phase subagent | **Quiet OK** when **`AUTO_QUIET=1`** (no routine “phase done” chatter). |
| **`decision_gate`** | **Stop** until resolved | **Always** (non-suppressible). |
| **`error`**, **missing critical input** | **Stop** | **Always**. |
| **`AUTO_PAUSE_REQUEST`** / **`pause`** | **Stop** at safe boundary | **Always**. |
| **`AUTO_LOOP_MAX_CYCLES`** / **`loop_max`** | **Stop** | **Always**. |
| **`blocked`** (e.g. sync/scope gate) | **Stop** | **Always**. |
| **US** lifecycle **DONE** boundary / **sprint segment** complete under active policy | **Stop** this segment; **`AUTO_BACKLOG_DRAIN=1`** may **advance** to **next eligible OPEN story** per **`DEC-0022`** (recompute materialized phase plan) | **Notify** on segment handoff / drain advance (counts as **non-routine**). |
| **`BACKLOG_MAX_STORIES_REACHED`** / drain cap | **Stop** | **Always**. |

**`stop_reason`** vocabulary stays **fixed**; continuous runs only **clarify** which reason fired after **which** phase depth.

## Quiet policy: **`AUTO_QUIET`** vs **`TOKEN_PROFILE`**

| Key | Values | Role |
|-----|--------|------|
| **`AUTO_QUIET`** | **`0`** \| **`1`** (**default `0`**) | **`1`** = suppress **routine** per-phase success chatter only; **must not** hide **`decision_gate`**, **errors**, **pause**, **`loop_max`**, **`blocked`**, or **missing inputs** (**backlog AC-2**). |
| **`TOKEN_PROFILE`** | **`lean`** \| **`balanced`** \| **`full`** | Unchanged — **DEC-0035** / **`US-0080`**; **orthogonal** to **`AUTO_QUIET`**. |

**Composition**: **`PHASE_MODE`** / **`PERMISSION_MODE`** remain **orthogonal** unless a future **DEC** documents an explicit matrix. **`template/`** + scratchpad example parity required when **`AUTO_QUIET`** ships (**AC-5**).

## **`DEC-0069` / resume pairing** (**`US-0037`**)

- At **every** materialized phase boundary in a **continuous** or **drain** run, **`handoffs/resume_brief.md`** **Latest** pointer and **`docs/engineering/state.md`** append must **mirror** the same tuple: **`intended_resume_phase`** / **`next_scheduled_phase`**, **`story_id`**, **`orchestrator_run_id`**, **`backlog_drain_stories_remaining_budget`** (when drain active), plus **`US-0087`** segment fields when applicable (**`# US-0087`**).
- **No weakening** of **`RESUME_BRIEF_STALE`** / unparseable fail-fast — fix is **deterministic refresh** at boundaries (**`DEC-0069`** / **`BUG-0005`** lineage), including reconciliation when a **new** story’s brief row could disagree with **`state.md`** mid-segment (**per `R-0071`** lesson).

## Interaction with **`US-0044`** backlog drain

- When **`AUTO_BACKLOG_DRAIN=1`**, after a **story** reaches its terminal boundary (**`refresh-context`** completion or policy stop), the orchestrator **reloads** backlog selection and **recomputes** the materialized phase plan for the **next** story (**reference Step 5**).
- **`backlog_drain_stories_remaining_budget`** (and **`AUTO_BACKLOG_MAX_STORIES`**) remain the **bounded** counters — **US-0088** does not remove caps.

## Contract-test expectations (**AC-4**, **`tests/auto_command_contract_test.py`**)

- **Positive (reference)**: Assert normative phrases for (1) **intersected resolved schedule order**, (2) **`AUTO_BACKLOG_DRAIN=1`** + **next eligible OPEN story** / **repeat**, (3) **recompute** / **reload** phase plan at **story boundary** — substring set **locked** in execute to avoid brittle noise (**per `R-0071`**).
- **Positive (command)**: Compact **`auto.md`** step that maps to **multi-phase spawn** must **explicitly** reference **reference Step 5** (or stable anchor text agreed in execute).
- **Negative**: Retain / extend **spawn-only** tests — no wording that implies the orchestrator may run **`execute`**, **`qa`**, etc. **in-turn** (**`BUG-0006`**).
- **Limitation**: Static tests prove **repo text**; they do not prove Cursor schedules **multiple** subagent turns — runbook (**AC-7**) states **operator** obligation when **outer driver** is used.

## Surfaces (execute phase)

| Path | Change |
|------|--------|
| **`.cursor/commands/auto.md`** | Cross-anchors to **reference Step 5**; **`AUTO_QUIET`**; stop matrix pointer; drain + resume pairing. |
| **`docs/engineering/auto-orchestration-reference.md`** | Step 5 ↔ compact step equivalence; continuous vs outer-driver; **AC-2** / **AC-10** tuple. |
| **`template/`** | Parity for command + reference + scratchpad keys. |
| **`tests/auto_command_contract_test.py`** | Continuation + drain substrings; spawn-only regression. |
| **`docs/engineering/runbook.md`** | **AC-7** recipe: caps, pause, gates, quiet. |

## Risks

| Risk | Mitigation |
|------|------------|
| **Step numbering drift** reintroduces **one-phase-stop** | Stable **“reference Step 5”** anchor + contract tests. |
| **`AUTO_QUIET=1`** hides **decision_gate** | **Non-suppressible** channel rules in **AC-2** + stop matrix. |
| **False `RESUME_BRIEF_STALE`** mid-run | **Paired** **`resume_brief`** + **`state.md`** refresh (**`DEC-0069`**). |
| **Double scheduler** with bug queue | **`# US-0087`** mutex only — **`AUTO_SCHEDULER_CONFLICT`**. |

## Decision linkage

- Research: **`R-0071`**
- Related: **`US-0044`**, **`DEC-0022`**, **`US-0037`**, **`DEC-0069`**, **`BUG-0005`**, **`US-0087`**, **`R-0070`**, **`BUG-0006`**, **`US-0069`**, **`US-0080`**, **`DEC-0062`**, **`DEC-0035`**

---

