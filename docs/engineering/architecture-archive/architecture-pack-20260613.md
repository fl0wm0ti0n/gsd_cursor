# Architecture archive pack (2026-06-13)

- Rollover trigger: `ARCH_HOT_MAX_LINES=3000, ARCH_HOT_MAX_STORY_SECTIONS=120`
- Source: `docs/engineering/architecture.md`
- Archived units (oldest first, contiguous prefix): 8
- Retained units in hot file: 17
- First archived heading: `# US-0082: Agent-driven codebase map bootstrap`
- Last archived heading: `# BUG-0007: Intake evidence truthfulness for `asked_topics` / `topic_coverage``
- Verification tuple (mandatory):
  - archived_body_lines=476
  - preamble_lines=10
  - retained_body_lines=2972

---

# US-0082: Agent-driven codebase map bootstrap

## Overview

**`US-0082`** ensures fresh repos can rely on `docs/engineering/codebase-map.md` through deterministic workflow ownership, while preserving **`/map-codebase`** as an explicit manual command. **`R-0060`** frames vendor practice (rules/docs as primary context) vs repo-owned map artifacts; **`DEC-0065`** locks lifecycle gates, idempotency, ownership, diagnostics, and parity expectations.

## Assumption challenge and alternatives

| Option | Summary | Verdict |
|--------|---------|---------|
| A - Guidance-only | Runbook reminders, no lifecycle hook | Rejected — misses **AC-1** for unattended bootstrap. |
| B - Generate on every `/auto` phase | Maximum automation | Rejected — churn / **`state.md`** noise (**R-0060**). |
| C - CI-only | Fail pipeline without map | Rejected as sole owner — late signal; still needs **AC-1** lifecycle naming. |
| D - Phase-gated + manual (chosen) | **`/architecture`** primary; optional **`/refresh-context`**; **`/map-codebase`** manual | **Chosen** — minimal automation that meets ACs and respects **DEC-0052**. |

## Deterministic approach

1. **Primary lifecycle point**: **`/architecture`** completion (**tech-lead**) — ensure map exists or deterministic block/skip with diagnostics before **`/sprint-plan`** handoff (sprint implements invocation: command wrapper, script, or documented mandatory step).
2. **Secondary (policy-gated)**: **`/refresh-context`** may re-materialize or verify map when scratchpad/profile explicitly enables refresh (default off to limit churn).
3. **Manual path**: **`/map-codebase`** unchanged for explicit operator runs (**AC-2**).
4. **Idempotency**: Stable ordering; avoid no-op file churn (**AC-3**).
5. **Ownership**: Same write surfaces as **`/map-codebase`**; **`state.md`** append-only discipline preserved (**AC-4**).
6. **Diagnostics**: **`CODEBASE_MAP_*`** reason family + remediation (**AC-5**).
7. **Guidance**: Runbook + **`/ask`** name responsibility locus (**AC-6**).
8. **Verification**: Active/template parity + fresh / rerun / failure-path tests (**AC-7**, **AC-8**).
9. **Compatibility**: Non-destructive treatment of existing maps (**AC-9**).
10. **Traceability**: **`BUG-0002`** closed as mismatch; this story owns implementation (**AC-10**).

## Fail codes (deterministic vocabulary)

- **`CODEBASE_MAP_MISSING`** — expected artifact absent at lifecycle checkpoint.
- **`CODEBASE_MAP_BLOCKED:<subreason>`** — generation blocked (permissions, policy, profile skip); subreason bounded in sprint.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Custom phase plans skip architecture | Diagnostics + optional CI guard (**DEC-0065** §9). |
| Overwriting local map customizations | Idempotent merge / section-stable refresh; destructive modes out of scope unless explicit. |
| Active/template drift | Parity manifest or existing test patterns for commands/rules (**AC-7**). |

## Decision linkage

- Research basis: **`R-0060`**
- Decision: **`DEC-0065`**
- Related: **`US-0001`** (command exists), **`BUG-0002`** (closed), **`DEC-0052`** (phase profiles)

---

# BUG-0003: Deterministic installer completeness in `missing`/`upgrade`

## Overview

**`BUG-0003`** closes a mode-specific installer trust gap where framework scripts may remain absent after `missing` and `upgrade` runs. **`R-0061`** confirms branch logic parity across `installer.ps1`, `installer.sh`, and `installer.py`; root cause is required-inventory omission (`scripts/enforce-triad-hot-surface.py`) from `docs/engineering/context/installer-owned-paths.manifest`. **`DEC-0066`** locks the minimal fix: manifest-authoritative required script inventory plus deterministic post-install completeness checks and parity tests.

## Assumption challenge and alternatives

| Option | Summary | Verdict |
|--------|---------|---------|
| A - Keep current flow + operator reminders | No structural change | Rejected - allows silent incompleteness recurrence. |
| B - Hard-code required scripts in PS1/SH/PY | Explicit lists per installer | Rejected - highest maintenance and parity drift risk. |
| C - Manifest as single source + shared completeness validator (chosen) | Minimal, deterministic, testable | **Chosen** - simplest path that satisfies bug acceptance and parity constraints. |

## Deterministic approach

1. **Single required inventory source**: `docs/engineering/context/installer-owned-paths.manifest` owns required framework script paths for install completeness checks.
2. **Required path inclusion**: ensure `scripts/enforce-triad-hot-surface.py` is included in installer-owned install scope with paired clean ownership policy.
3. **Post-install invariant**: after mode-specific copy/classification logic, validate all required script paths exist; fail closed on missing entries.
4. **Stable diagnostics**: emit deterministic reason codes (`INSTALL_COMPLETENESS_FAILED`, `INSTALL_REQUIRED_SCRIPT_MISSING:<path>`) with remediation pointing to manifest parity/update path.
5. **Parity-safe implementation**: prefer shared completeness logic in `installer.py` with wrappers (`installer.ps1`, `installer.sh`) consuming the same contract.
6. **Status authority preserved**: `BUG-0003` remains **OPEN** in `docs/product/backlog.md` until execute/qa/verify-work/release close-out (**US-0045**).

## Verification strategy

- **Positive matrix**: `missing` and `upgrade` both produce complete required script set after install.
- **Negative matrix**: intentionally remove required script from staged source and assert deterministic fail code.
- **Parity matrix**: active + `template/` installer surfaces and manifest remain aligned.
- **Symmetry matrix**: install include and clean path ownership stay paired for required scripts.
- **Regression entrypoints**: extend installer-focused tests and lifecycle smoke checks referenced by sprint tasks.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Future manifest omissions reintroduce silent misses | Required inventory checks + regression fixtures tied to manifest updates. |
| Divergent wrapper behavior across platforms | Shared Python validation contract and wrapper reuse. |
| Over-blocking custom repos | Limit completeness gate to installer-owned framework paths. |
| Install/clean mismatch | Explicit paired review and test coverage for `install_include_paths` + `clean_paths`. |

## Decision linkage

- Research basis: **`R-0061`**
- Decision: **`DEC-0066`**
- Related: **`BUG-0001`**, **`US-0018`**, **`US-0045`**, **`DEC-0038`**

---

# BUG-0004: POSIX-safe installer shell startup for Unix CLI path

## Overview

**`BUG-0004`** addresses startup failure in Linux shell environments where installer execution aborts with `set: Illegal option -`. Research **`R-0063`** confirms Unix CLI flow (`bin/its-magic.js`) executes installer via `sh installer.sh`, so installer startup must remain POSIX-`sh` compatible and avoid bash-only `set` semantics. **`DEC-0068`** is normative for invocation/compatibility boundaries and regression requirements.

## Assumption challenge and alternatives

| Option | Summary | Verdict |
|--------|---------|---------|
| A - Force bash invocation in CLI | `bash installer.sh` on Unix | Rejected - adds dependency and weakens portability. |
| B - Dynamic shell detection and launcher branching | choose shell at runtime | Rejected - more complexity than needed for defect scope. |
| C - Keep `sh` contract and enforce POSIX-safe startup (chosen) | minimal and deterministic | **Chosen** - preserves current CLI behavior and fixes failure root. |

## Deterministic approach

1. **Unix launcher contract unchanged**: keep `bin/its-magic.js` Unix execution path via `spawnSync("sh", ...)`.
2. **Startup option safety**: `installer.sh` startup path must use POSIX-safe `set` options only (`set -e` baseline); no unconditional bash-only flags.
3. **Failure prevention**: startup must not fail on `/bin/sh` variants due to option incompatibility.
4. **Status authority preserved**: `BUG-0004` remains **OPEN** in `docs/product/backlog.md` until sprint delivery closes verification/release chain (**US-0045**).

## Verification strategy

- **Direct `sh` matrix**:
  - `sh installer.sh --target <tmp> --mode missing --create`
  - `sh installer.sh --target <tmp> --mode upgrade`
- **CLI Unix matrix**:
  - `node bin/its-magic.js --target <tmp> --mode missing --create`
- **Non-regression matrix**:
  - install completeness checks and existing manifest-governed behavior remain intact.
- **Parity matrix**:
  - retain consistent installer behavior expectations across wrapper paths and test harness coverage.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Bash-only options reintroduced later | Keep explicit `sh`-path regression coverage in shared tests. |
| Local shell mismatch hides regressions | Verify both direct `sh` and CLI invocation paths in deterministic tests. |
| Scope drift into unrelated resume bugs | Keep this architecture bounded to shell startup compatibility (`BUG-0005` tracked separately). |

## Decision linkage

- Research basis: **`R-0063`**
- Decision: **`DEC-0068`**
- Related: **`BUG-0005`**, **`US-0008`**, **`US-0018`**, **`US-0045`**

---

# BUG-0005: `resume_brief` refresh at bug-intake boundary for `/auto` resume

## Overview

**`BUG-0005`** addresses **`RESUME_BRIEF_STALE`** on **`/auto`** immediately after canonical **`/intake bug`** persistence: the resume brief can still describe a pre-intake cycle (for example **`intake`**) while the backlog already reflects a new OPEN bug. Deterministic **`/auto`** precedence (**`start-from`** → parseable **`resume_brief`** → **`state.md`**) intentionally **does not** silently ignore a present-but-stale brief. **`R-0064`** and **`DEC-0069`** lock the fix as **intake-time refresh** of **`handoffs/resume_brief.md`** so normal **`/intake bug` → `/auto`** does not false-trigger stale-resume, without weakening fail-fast.

## Contracts (normative)

1. **Intake completion obligation**: On successful bug intake persistence (**`US-0045`**), the intake writer **must** refresh **`handoffs/resume_brief.md`** with **`bug_id`**, **`intended_resume_phase=discovery`** (default OPEN-bug continuation), boundary **`orchestrator_run_id`** / timestamp when known, and intake evidence pointer when present.
2. **Precedence unchanged**: Explicit **`start-from`** overrides; parseable brief is evaluated before **`state.md`**; stale/unparseable/ambiguous briefs **fail fast** (**`RESUME_BRIEF_STALE`**, etc.) — no silent fallback when a stale brief is present.
3. **Backlog authority**: Brief content **must not** contradict **`docs/product/backlog.md`** status facts for the referenced **`bug_id`**.
4. **Optional self-heal**: Orchestrator-side reconciliation is **not** normative for **`BUG-0005`**; any future self-heal requires strict predicates, idempotency, **`state.md` audit**, and a separate decision (**`DEC-0069`** §4).

## Affected artifacts

- **`handoffs/resume_brief.md`** — primary handoff surface refreshed at intake boundary.
- **`docs/engineering/state.md`** — phase breadcrumbs and auto continuation checkpoints remain authoritative for history; they do not replace a parseable brief in precedence order.
- **`.cursor/commands/intake.md`** (and **`template/`** parity) — normative command surface for implementing intake-time refresh.
- **`docs/engineering/auto-orchestration-reference.md`** / **`.cursor/commands/auto.md`** — precedence and fail-fast codes remain source of truth; **`DEC-0069`** adds intake-side obligation only.

## Acceptance / architecture alignment

- Satisfies **`BUG-0005`** expected behavior: after intake, **`/auto`** resolves a valid next phase without requiring manual **`start-from`** for the normal path.
- Preserves **`US-0045`** canonical status and **`US-0070` / `DEC-0052`** phase-plan materialization (default next phase after bug intake is **`discovery`** unless product documents an exception).
- Regression matrix: **`R-0064`** table (**five scenarios**) is minimum QA/sprint coverage.

## Decision linkage

- Research basis: **`R-0064`**
- Decision: **`DEC-0069`**
- Related: **`US-0037`**, **`US-0045`**, **`US-0070`**, **`US-0080`**, **`DEC-0038`** (strict-proof continuity on phase boundaries)

---

# US-0083: Explicit delegable intake topics without weakening fail-closed semantics

## Overview

**`US-0083`** adds a bounded, auditable delegation path for unresolved required intake topics so users can explicitly delegate a decision and continue, while preserving the existing fail-closed gate for non-delegated gaps. **`R-0062`** recommends the smallest viable extension: keep the current `topic_coverage` contract and add a third `satisfied_by` branch with strict evidence requirements. **`DEC-0067`** is normative for schema, validator branching, reason codes, and parity scope.

## Assumption challenge and alternatives

| Option | Summary | Verdict |
|--------|---------|---------|
| A - Keep current strict-only gate | No delegation branch | Rejected - preserves safety but fails AC-2/AC-3 user intent. |
| B - Global delegation toggle for all missing topics | One switch to bypass missing required topics | Rejected - too broad, increases implicit bypass risk. |
| C - Topic-scoped delegation branch in existing rows (chosen) | Minimal schema extension with explicit evidence per topic | **Chosen** - simplest path that preserves deterministic fail-closed semantics. |

## Deterministic approach

1. **Topic-row contract extension**: allow `topic_coverage[].satisfied_by=delegation_ref` in addition to existing `answer_ref` and `assumption_confirmation_ref`.
2. **Required delegation fields**: when `satisfied_by=delegation_ref`, require:
   - `delegation_scope` (bounded decision area),
   - `delegation_rationale` (why delegation is chosen),
   - `delegation_confidence` (`low|medium|high`).
3. **Evidence binding**: delegation rows must still carry a valid `ie:` `ref` and explicit `quoted_user_text`; hash verification remains deterministic and includes the delegated branch literal.
4. **Validator branch behavior**:
   - non-delegated unresolved required topic -> unchanged fail-closed path (`INTAKE_REQUIRED_TOPIC_MISSING`, optional `INTAKE_REQUIRED_PACK_INCOMPLETE`, umbrella `INTAKE_PERSISTENCE_BLOCKED`);
   - delegated topic with complete evidence -> passes as covered;
   - delegated topic with missing/malformed evidence -> fail closed with delegation-specific deterministic reason codes under `INTAKE_PERSISTENCE_BLOCKED`.
5. **Mode parity**: guided and low-touch intake use the same validation pipeline; delegation does not introduce mode-specific bypass behavior.
6. **Status authority unchanged**: canonical story status remains in `docs/product/backlog.md` (**`US-0045`**); `US-0083` stays `OPEN` through architecture.

## Fail codes (deterministic vocabulary)

- **`INTAKE_DELEGATION_EVIDENCE_MISSING`** - delegated topic is missing one or more required delegation fields.
- **`INTAKE_DELEGATION_EVIDENCE_INVALID`** - delegated topic has invalid field values or invalid/mismatched `ie:` evidence binding.
- **`INTAKE_PERSISTENCE_BLOCKED`** (umbrella) - retained for all blocked persistence outcomes.

## Verification strategy

- Delegated pass fixtures: required-topic rows with `delegation_ref` and complete evidence succeed.
- Non-delegated block fixtures: unresolved required topics without delegation remain blocked with existing codes.
- Delegated block fixtures: malformed/missing delegation fields fail with deterministic delegation codes.
- Parity fixtures: active + `template/` alignment for intake command/rules/validator surfaces.
- Mode parity fixtures: guided and low-touch produce the same validation outcome for equivalent evidence bundles.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Delegation becomes implicit bypass | Require explicit `delegation_ref` + `ie:`-bound user quote; no global toggle. |
| Schema drift across active/template | Include parity checks and mirrored fixtures in sprint scope. |
| Over-complex delegated metadata recreates intake friction | Keep metadata minimal (`scope`, `rationale`, `confidence`) only. |
| Downstream consumers treat delegated items as resolved facts | Preserve delegated marker and rationale in persisted evidence and handoffs. |

## Decision linkage

- Research basis: **`R-0062`**
- Decision: **`DEC-0067`**
- Related: **`US-0068`**, **`US-0078`**, **`US-0045`**, **`DEC-0050`**, **`DEC-0060`**

---

# US-0084: POSIX npm installer + Linux remote test targets (WSL / SSH / Docker)

## Overview

**`US-0084`** locks how the **published** npm **`installer.sh`** stays safe under Debian **`/bin/sh`** (often **dash**), how **LF** shell entrypoints are enforced in the publish path, and how dev/QA aim work at **WSL**, bare **SSH Linux**, or **Docker-over-SSH** using the **existing** **`US-0064`** contract (**`docs/engineering/release-targets.json`**, **`docs/engineering/runtime-connectivity.md`**) — no parallel remote schema. Research basis: **`R-0067`**.

## Assumption challenge and alternatives

| Option | Summary | Verdict |
|--------|---------|---------|
| A | Bash-only installer (`#!/usr/bin/env bash`, bash **`set`** flags) | **Rejected** — conflicts with **AC-1** / global npm **`sh`** path. |
| B | New remote JSON schema beside **`release-targets.json`** | **Rejected** — **AC-4** / **US-0064** alignment only. |
| C | POSIX **`sh`** startup + LF guards + doc map + optional **`scripts/`** helper (**chosen**) | **Chosen** — minimal delta vs repo today; **`R-0067`** confirms active **`installer.sh`** already uses **`set -e`** only on the unconditional path. |

## Published `installer.sh`: POSIX, dash, and LF (**AC-1**)

1. **Shebang and startup**: Keep **`#!/usr/bin/env sh`** and **only** POSIX-safe options on the unconditional startup block (today: **`set -e`** at **`installer.sh:2`**; preserve **BUG-0004** guard comment). **Forbidden** on that path: **`set -u`**, **`pipefail`**, **`set -o …`** bash-only bundles, or any **`set`** line that dash rejects.
2. **Single shipped copy**: **`package.json`** **`files`** ships root **`installer.sh`** (no in-repo **`template/installer.sh`** today). Architecture treats **git HEAD = publish source of truth**; any future mirrored **`template/`** copy triggers the same parity rules as other template mirrors.
3. **LF enforcement**: Add repo root **`.gitattributes`** with `*.sh text eol=lf` (and any other packaged shell entrypoints the sprint lists) so Windows checkouts do not silently CRLF the publish artifact. Complement with a **deterministic** check that rejects **`\\r`** in **`installer.sh`** (Python byte scan is sufficient on all maintainer OSes — **R-0067**).
4. **Invocation reality**: **`bin/its-magic.js`** spawns **`sh`** + package **`installer.sh`** on non-Windows — architecture does not change that contract; it requires the file on disk to remain dash-parseable.

## CI / prepublish guard shape (**AC-2**)

Layered gates (sprint may implement subset if documented, but **preferred full stack**):

| Layer | Purpose | Notes |
|-------|---------|-------|
| **Python regression** | Extend **`tests/installer_shell_bug0004_test.py`** (or successor): forbid **`set -euo`** / **`pipefail`** substrings; keep **`sh`** / CLI smokes. | Windows-friendly without **dash** on **`PATH`**. |
| **`dash -n`** | Syntax check under dash when **`dash`** exists (**CI** or dev opt-in). | **Skip with explicit reason** on runners without **`dash`** (**R-0067** open question); do not silently drop **AC-2** — document skip vs hard in runbook. |
| **`prepublishOnly`** (optional) | Run the same LF + token + (if available) **`dash -n`** gate before **`npm pack`/`publish`**. | Defense in depth for tarball-only mistakes. |

**Sprint deliverable**: at least one **CI** step **or** **`prepublishOnly`** path that **fails closed** on CRLF in **`installer.sh`** + forbidden **`set`** patterns; **`dash -n`** when the environment provides **`dash`**.

## Remote documentation map — **US-0064** alignment (**AC-4**, **AC-9**)

Canonical table for operator docs (runbook / developer guide); **no new keys** in **`release-targets.json`**.

| Operator path | Maps to | Scratchpad / config cues |
|---------------|---------|---------------------------|
| **WSL** | Local Linux kernel on the dev machine — run **`sh`/`dash`** and repo tests **inside WSL**; not a separate **`release-targets`** row by default. | Same repo; cite **environment label** in evidence (**AC-6**). |
| **Bare SSH Linux** | **`ssh-server`** target (**`release-targets.json`**: **`hostEnv`**, **`userEnv`**, **`authEnv`**, **`remoteCommand`**, **`runtime`**, ingress). | **`REMOTE_EXECUTION`**, **`REMOTE_CONFIG=.cursor/remote.json`** per **`.cursor/scratchpad.md`**; validate shape against **`runtime-connectivity.md`**. |
| **Docker-over-SSH** | **`ssh-server.dockerOverSsh`** — **`dockerHostEnv`**, **`dockerContextEnv`**, **`composeFile`**, **`service`** + operator **`DOCKER_HOST`** / context docs. | Cross-link **`runtime-connectivity.md`** **`docker_over_ssh`** summary (**`R-0067`**). |

## Helper script contract (**AC-5**, **AC-7**, **AC-10**)

- **Path / name**: **`scripts/remote_config_summary.py`** (Python 3, consistent with existing **`scripts/`** validators).
- **Inputs**: **`--config`** default **`REMOTE_CONFIG`** env or **`.cursor/remote.json`**; read-only; no network side effects.
- **Stdout**: **non-secret** summary only — target **label** (e.g. **`ssh-server`**), **host** as **env var name** and/or **“set / unset”** presence flags, **user** env name, **identity file path string** (path ref only, **never** key material), optional **`dockerOverSsh`** **enabled** flag and **env names**. **Do not** print resolved secret **values** (**R-0067** residual risk).
- **Stderr**: human-readable failure reason (deterministic prefix optional).
- **Exit codes** (locked for harness fixtures):
  - **0** — OK (config readable and shape acceptable for documented **US-0064** patterns).
  - **1** — usage / CLI error.
  - **2** — config file missing or unreadable.
  - **3** — invalid JSON.
  - **4** — schema / required-field mismatch vs documented **US-0064** operator contract (not a second schema — “doc conformance” check).
  - **5** — **`REMOTE_EXECUTION=0`** fast exit / intentionally skipped validation (if product chooses “no-op when remote off”; otherwise map no-op to **0** — sprint **`decisions.md`** must record the chosen branch).

## `/execute`, `/qa`, and runbook cues (**AC-3**, **AC-6**)

- **`docs/engineering/runbook.md`**: extend **REMOTE_EXECUTION** section (~**783+**) with **troubleshooting** — **`set: Illegal option -`**, **CRLF vs LF**, **`sh` vs `bash`**, **`dos2unix`**, reinstall from fixed version; pointer to **`installer.sh`** POSIX rules above.
- **Handoffs / evidence**: when **`REMOTE_EXECUTION=1`**, cite **environment label** (e.g. **`WSL`**, **`ssh:<hostEnv>`**, **`dockerOverSsh`**) and **never** paste secrets or key bodies (**AC-7**).

## Test harness rows (**AC-2**, **AC-10**)

Register beside existing installer Python tests (**`tests/run-tests.sh`** / **`tests/run-tests.ps1`**, **§26** style per **`R-0067`**):

| Row | Coverage |
|-----|----------|
| H1 | **LF** check + forbidden **`set`** tokens on **`installer.sh`** (extends **BUG-0004** test). |
| H2 | **`dash -n installer.sh`** when **`dash`** available (or documented CI matrix). |
| H3 | **`remote_config_summary.py`** — fixture **valid** minimal **`.cursor/remote.json`** → exit **0**, expected stdout keys/names only. |
| H4 | **`remote_config_summary.py`** — fixture **invalid JSON** → exit **3**. |
| H5 | **`remote_config_summary.py`** — fixture **schema/doc mismatch** → exit **4** (or **2** for missing file — separate fixture). |

## Active + `template/` parity (**AC-8**)

Any new/edited **commands**, **scratchpad examples**, **`.cursor/remote.json`** template snippets, or **runbook** sections must be mirrored under **`template/`** per existing kit parity rules (same literals where the template carries the surface). **`package.json`** changes (e.g. **`prepublishOnly`**) apply to the **shipping** package only — template mirrors **commands/docs** that consumers receive.

## Risks

| Risk | Mitigation |
|------|------------|
| CI lacks **`dash`** | Documented **skip vs hard**; Python CRLF + substring gates remain mandatory. |
| Maintainer publish from Windows without local **`dash`** | **`prepublishOnly`** + Python checks; optional CI **`dash`**. |
| Helper duplicates **`runtime-connectivity.md`** | Helper = **validate + summarize**; prose stays in **`runtime-connectivity.md`** / runbook. |
| Secret leakage via “debug” print | **Names-only** / presence flags; code review + fixture asserts on stdout. |

## Decision linkage

- Research basis: **`R-0067`**
- Related: **`US-0064`**, **`US-0036`**, **BUG-0004**, **`docs/engineering/release-targets.json`**, **`docs/engineering/runtime-connectivity.md`**, **`bin/its-magic.js`**, **`package.json`**

---

# BUG-0006: `/auto` spawn-only enforcement (orchestrator must not execute phase work)

## Overview

**`BUG-0006`** closes the gap between **process** `/auto` orchestration (US-0080) and operator behavior: the orchestrator role must **only** schedule materialization, spawn fresh **phase-role** subagents, and verify boundaries—it must **not** author phase deliverables or perform phase work in the same context. **`R-0065`** recommends doc-first enforcement plus static regression; this section locks literals, surfaces, and acceptance hooks.

## Locked reason-code vocabulary

| Code | Use | Remediation (operator-facing) |
|------|-----|-------------------------------|
| **`AUTO_ORCHESTRATOR_PHASE_EXECUTION`** | Attempted direct orchestrator execution of a lifecycle phase (or equivalent “run `architecture` / `execute` / … in orchestrator context”) instead of spawning the required subagent. | Stop; spawn a **fresh** subagent for the canonical **`phase_id`** and **role** per the phase→role matrix (**DEC-0051**); do not merge phase output into orchestrator turns. |
| **`PHASE_CONTEXT_ISOLATION_VIOLATION`** (existing) | Orchestrator wrote phase artifacts or violated per-phase isolation (**DEC-0029**). | Distinct from spawn failure: isolation applies **after** correct spawn boundary; keep both codes documented side-by-side. |
| **`RUNTIME_PROOF_*`**, **`PHASE_ROLE_*`**, **`PHASE_POLICY_*`** (existing) | Strict proof, capability, phase-plan failures (**DEC-0038**, **DEC-0052**). | Unchanged; **`AUTO_ORCHESTRATOR_PHASE_EXECUTION`** must not overload these families. |
| **`[AUTO_RESUME_ERROR]`** codes (existing) | Resume precedence / brief / state resolution. | Separate from spawn integrity; no merge of semantics. |

## Technical approach (doc-first, test-backed)

1. **Normative command (active + template)**: **`.cursor/commands/auto.md`** and **`template/.cursor/commands/auto.md`** — strengthen **non-negotiable** language: “spawn fresh subagent per phase,” “orchestrator must not execute phase work / write phase deliverables,” and enumerate **`AUTO_ORCHESTRATOR_PHASE_EXECUTION`** in the fail-fast / reason-code excerpt (alongside existing **`PHASE_CONTEXT_ISOLATION_*`** / **`RUNTIME_PROOF_*`** markers).
2. **Expanded reference**: **`docs/engineering/auto-orchestration-reference.md`** — mirror the spawn-only rule; cross-link **DEC-0029** (isolation) and **DEC-0038** (strict proof) so operators cannot satisfy one gate and ignore the other; document **`AUTO_ORCHESTRATOR_PHASE_EXECUTION`** with one-line remediation.
3. **Regression**: extend **`tests/auto_command_contract_test.py`** with required substrings: spawn-only phrasing, forbidden orchestrator phase execution, literal **`AUTO_ORCHESTRATOR_PHASE_EXECUTION`**, and a **negative** check that the slim command does **not** imply in-orchestrator execution of named phases (pattern established in **`R-0065`** matrix rows 1–4).
4. **Out of scope**: no claim of runtime Cursor product enforcement; no replacement of isolation or proof tuples as subagent launchers.

## Files to touch (execute phase)

| Path | Change |
|------|--------|
| **`.cursor/commands/auto.md`** | Spawn-only + **`AUTO_ORCHESTRATOR_PHASE_EXECUTION`** + forbidden direct phase execution. |
| **`template/.cursor/commands/auto.md`** | Parity with active command (same literals where mirrored). |
| **`docs/engineering/auto-orchestration-reference.md`** | Expanded contract alignment + cross-links + reason code. |
| **`tests/auto_command_contract_test.py`** | Assertions for new literals and non-contradiction. |

Optional parity: if repo adds an **`auto`** template parity script later, include these paths; until then, **manual or sprint QA** verifies **`template/`** mirror.

## Acceptance hooks

- Contract test **`python tests/auto_command_contract_test.py`** (or full unittest suite per sprint) **PASS** after edits.
- **`BUG-0006`** **expected** in backlog: fail-fast when spawn boundary violated, with deterministic diagnostics — satisfied by documented **`AUTO_ORCHESTRATOR_PHASE_EXECUTION`** plus existing isolation/proof codes.
- Canonical status remains **`docs/product/backlog.md`** only (**US-0045**); closure moves to **DONE** only after execute/QA/verify per backlog.

## Risks

| Risk | Mitigation |
|------|------------|
| Code overlaps **`PHASE_CONTEXT_ISOLATION_VIOLATION`** | Table above + remediation text distinguishes “no spawn” vs “wrong writer.” |
| Template drift | Edit **`template/.cursor/commands/auto.md`** in the same change set as active **`auto.md`**. |
| False sense of runtime enforcement | Docs + static tests only; reference states process contract, not IDE automation. |

## Decision linkage

- Research basis: **`R-0065`**
- Related: **`US-0048`**, **`US-0069`**, **`US-0080`**, **`US-0045`**, **`DEC-0029`**, **`DEC-0038`**, **`DEC-0051`**, **`DEC-0052`**

---

# BUG-0007: Intake evidence truthfulness for `asked_topics` / `topic_coverage`

## Overview

**`BUG-0007`** closes the gap where **`scripts/intake_evidence_validate.py`** can return **`[INTAKE_EVIDENCE_VALIDATION_OK]`** on bundles such as **`handoffs/intake_evidence/BUG-0007-intake-20260403.json`** that list a full **`small-intake-pack`** in **`asked_topics`** while every **`topic_coverage`** row uses **`satisfied_by=answer_ref`** with the **same** (or trivially duplicated) **`quoted_user_text`**—i.e. no real per-topic elicitation. **`R-0066`** shows **`validate_intake_evidence`** in **`scripts/intake_evidence_lib.py`** enforces structural pack coverage, **`ie:`** integrity, and **DEC-0060**-aligned bindings, but not semantic distinction of answers across topics. This section locks the minimal validator + contract + test matrix so the exemplar **fails** after implementation while **US-0083** delegation and **equivalent_evidence_ref** paths stay **PASS**.

## Assumption challenge and alternatives

| Option | Idea | Verdict |
|--------|------|---------|
| A | Documentation-only reminder in **`/intake`** | **Rejected** — validator already certifies the bad exemplar (**R-0066**). |
| B | External chat transcript ingestion | **Deferred** — out of repo scope unless product mandates it. |
| C | Deterministic lib rules + contract + fixtures (**chosen**) | **Chosen** — same validation pipeline for guided and low-touch; fail-closed subcodes under **`INTAKE_PERSISTENCE_BLOCKED`**. |

**Residual risk**: Duplicate-text heuristics alone do not prove a “question was asked”; optional future **`question_*`** fields or stronger artifacts may be needed. Document any grandfathering in sprint **`decisions.md`** if legacy bundles must migrate.

## Locked technical approach

### 1) Core validation (`scripts/intake_evidence_lib.py`)

Extend **`validate_intake_evidence`** (and shared helpers the lib owns) with deterministic rules applied **after** existing **`ie:`** / pack / delegation / assumption checks:

1. **Duplicate **`answer_ref`** prose across distinct required topics** — For **`small-intake-pack`** (and equivalent required-topic sets), when multiple rows share **`satisfied_by=answer_ref`** and **identical** **`quoted_user_text`** (normalized per existing string rules in the lib), **fail** unless the row is covered by an allowed alternate satisfaction path (**`equivalent_evidence_ref`** / **`evidence_source`** semantics already in lib, **`delegation_ref`** per **DEC-0067**, or **`assumption_confirmation_ref`**). This targets the BUG-0007 pattern without treating two accidental short duplicate answers as the same class of abuse (tune: require duplicate across **all** required keys or use minimum distinct-count threshold — implementation sprint chooses the smallest rule that makes the exemplar **FAIL** and keeps matrix row 2 **PASS**).
2. **Optional phase-2** — If product requires stronger audit: add optional **`question_prompt_ref`** / **`question_text`** (or bind to a stable prompt id) for **`answer_ref`** rows; then **`INTAKE_ASKED_TOPIC_NOT_EVIDENCED`** applies when **`asked_topics`** lists a key without a bound prompt artifact. **Architecture default for first sprint**: implement (1) first; gate (2) behind explicit backlog if false positives appear.

**`scripts/intake_evidence_validate.py`**: keep CLI contract (**`--file`**, **`--stdin`**, **`--self-test`**); surface lib stderr codes unchanged.

### 2) Normative contract (`.cursor/commands/intake.md` + **`template/`** mirror)

- **`asked_topics`** may list only topics for which a **user-visible question** was posed **or** a **DEC-0060**-allowed alternate applies (**`delegation_ref`**, **`equivalent_evidence_ref`**, **`assumption_confirmation_ref`**).
- Explicitly **forbid** fabricating per-topic **`answer_ref`** rows by echoing one bug-report blob across all keys to satisfy the validator.
- Cross-link **DEC-0060** / **DEC-0067** / **US-0083** so operators do not conflate **`ie:`** integrity with “question asked.”

Parity: **`scripts/check_intake_template_parity.py`** (or successor) must stay **PASS** for any **`intake.md`** edit.

### 3) Locked reason codes (under umbrella **`INTAKE_PERSISTENCE_BLOCKED`**)

| Code | When |
|------|------|
| **`INTAKE_ANSWER_REF_NOT_TOPIC_DISTINCT`** | Distinct **`topic_key`** rows with **`satisfied_by=answer_ref`** share non-distinct **`quoted_user_text`** without **`equivalent_evidence_ref`** / other allowed alternate. |
| **`INTAKE_ASKED_TOPIC_NOT_EVIDENCED`** | (Optional / phase-2) **`asked_topics`** includes a topic without required question-binding artifact when that feature is enabled. |
| **Existing** | **`INTAKE_DELEGATION_EVIDENCE_MISSING`**, **`INTAKE_DELEGATION_EVIDENCE_INVALID`**, **`INTAKE_ASSUMPTION_CONFIRMATION_REQUIRED`**, **`INTAKE_REQUIRED_TOPIC_MISSING`** — **do not overload** for BUG-0007 duplicate-answer semantics. |

### 4) Test fixtures and regression matrix (**R-0066** § table — sprint must automate)

| # | Scenario | Expected |
|---|----------|----------|
| 1 | Fixture aligned with **`BUG-0007-intake-20260403.json`** (duplicate **`answer_ref`** across keys) | **FAIL** with **`INTAKE_ANSWER_REF_NOT_TOPIC_DISTINCT`** (or locked synonym) |
| 2 | Five **distinct** short answers + valid **`ie:`** | **PASS** |
| 3 | **`satisfied_by=delegation_ref`** + complete delegation metadata + valid **`ie:`** | **PASS** (**US-0083** / **DEC-0067** non-regression) |
| 4 | **`evidence_source=equivalent_evidence_ref`** row; topic omitted from **`asked_topics`** per lib rules | **PASS** |
| 5 | **`assumption_confirmation_ref`** path | **PASS** |
| 6 | **`python scripts/intake_evidence_validate.py --self-test`** | **PASS** after lib change |
| 7 | Active + **`template/`** parity | **PASS** |

Prefer **`tests/`** unittest module(s) invoking **`validate_intake_evidence`** directly (and/or subprocess on **`intake_evidence_validate.py`**) so CI mirrors operator commands.

## US-0083 / equivalent_evidence non-regression (hard gate)

- **Delegation**: Rows with **`satisfied_by=delegation_ref`**, required delegation fields, and valid **`ie:`** binding must **not** trip duplicate-**`answer_ref`** rules.
- **Equivalent evidence**: Topics satisfied via **`equivalent_evidence_ref`** / **`evidence_source`** must **not** be forced through fake per-topic **`answer_ref`** duplicates; validator behavior must match **`# US-0083`** architecture and **R-0062** intent.
- Sprint **execute** must add or extend fixtures that mirror **`handoffs/intake_evidence/US-0083-intake-20260331-b.json`** (or equivalent) and equivalent-evidence samples so matrix rows 3–4 cannot regress silently.

## Files to touch (execute phase — indicative)

| Path | Change |
|------|--------|
| **`scripts/intake_evidence_lib.py`** | New deterministic checks + codes. |
| **`.cursor/commands/intake.md`** | Truthfulness / forbid synthetic **`answer_ref`** echo. |
| **`template/.cursor/commands/intake.md`** | Parity. |
| **`tests/`** | New regression tests for BUG-0007 **FAIL** + US-0083 / equivalent-evidence **PASS**. |
| Optional | **`scripts/intake_bug_resume_brief_refresh.py`** / **`bug_issue_validate.py`** — only if a single choke-point should re-validate; avoid duplicate sources of truth (**R-0066**). |

## Risks

| Risk | Mitigation |
|------|------------|
| False positives on legitimate repeated short answers | Scope duplicate rule (e.g. “same blob across **all** pack keys”); tune in sprint with matrix row 2. |
| False confidence after only one heuristic | State residual risk; optional **`question_*`** follow-up. |
| Template drift | Same change set for active + **`template/`**; parity script **PASS**. |

## Decision linkage

- Research basis: **`R-0066`**
- Related: **`BUG-0007`**, **US-0068**, **US-0078**, **US-0079**, **US-0083**, **DEC-0060**, **DEC-0067**, **R-0062**, **R-0055**

---

