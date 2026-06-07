# Architecture archive pack (2026-06-07)

- Rollover trigger: `ARCH_HOT_MAX_LINES=3500, ARCH_HOT_MAX_STORY_SECTIONS=120`
- Source: `docs/engineering/architecture.md`
- Archived units (oldest first, contiguous prefix): 4
- Retained units in hot file: 29
- First archived heading: `# US-0073: Scratchpad delivery simplification (example-only install policy)`
- Last archived heading: `# US-0076: Executable scratchpad-driven sync and auto-push wiring`
- Verification tuple (mandatory):
  - archived_body_lines=263
  - preamble_lines=10
  - retained_body_lines=3414

---

# US-0073: Scratchpad delivery simplification (example-only install policy)

## Overview

`US-0073` selects **Model B** from `R-0050`: installers ship **framework-owned**
`.cursor/scratchpad.local.example.md` as the primary default catalog; an
**effective baseline** is established only through **explicit materialization**
(or legacy committed `.cursor/scratchpad.md` on upgrade). The goal is simpler
delivery without weakening deterministic automation, upgrade parity, or
ownership rules already fixed in `DEC-0039`.

## Merge and safety model

### 1) Canonical precedence (merged key/value resolution)

Apply **after** loading each participating file:

1. `.cursor/scratchpad.local.md` (user-owned, never installer-overwritten).
2. `.cursor/scratchpad.md` **or** materialized baseline bytes (stable /
   auditable equivalent to historical committed baseline).
3. `.cursor/scratchpad.local.example.md` (framework-owned defaults; refreshed on
   upgrade per `DEC-0039`).

### 2) Fail-closed missing keys

If a **required** automation key is absent or invalid after merge, stop with
diagnostics that name which layers were consulted and how to remediate — **no**
silent inference (`AC-2`, `AC-4`).

### 3) Upgrade / legacy

- Preserve user local; refresh example only (`DEC-0039`).
- Repos with existing committed `scratchpad.md` keep deterministic behavior;
  migration paths that remove or replace baseline must be **explicitly**
  documented and test-covered.

### 4) Parity

Same policy across `installer.ps1`, `installer.sh`, `installer.py`, CLI, and
`template/` (`AC-6`, `AC-8`).

### 5) Regression focus

Fresh install, upgrade from legacy dual-file layout, missing baseline /
materialization, and local-only override; each maps to deterministic outcomes
(`AC-9`, `AC-10`).

## Decision linkage

- Research basis: `R-0050`
- Decision: `DEC-0055`

---

# US-0074: Baseline version-sync and TEST_COMMAND bootstrap

## Overview

`US-0074` closes persistent baseline failures in `tests/run-tests.ps1` /
`tests/run-tests.sh`: Homebrew stable formula alignment with npm, and installer
/ CLI bootstrap of `TEST_COMMAND` in materialized `docs/engineering/runbook.md`.
The design pins **one canonical version source** and **one bootstrap outcome
contract** so execute/QA can restore a fully green baseline without scope creep.

## Version sync model

### Canonical source

- **`package.json` `version`** is authoritative for semantic version and for the
  GitHub tag segment `v{version}` used in the Homebrew `url`.

### Homebrew stable formula rules

- Committed `packaging/homebrew/its-magic.rb` must satisfy, on every release that
  bumps npm:
  - `url` contains `.../refs/tags/v{package.json.version}.tar.gz`
  - Ruby `version "{package.json.version}"`
  - `sha256` matches the tarball for that tag
- Release scripts are the default enforcement path so formula and npm cannot
  diverge casually.

## TEST_COMMAND bootstrap model

### Surfaces and precedence

- Installers and CLI entrypoints materialize runbook commands per **`DEC-0046`**
  (user override wins; then stack detection; fail-fast diagnostics when
  unresolved).
- Baseline asserts require the **resolved** `TEST_COMMAND` after bootstrap to be
  **only** `npm run test` **or** `sh tests/run-tests.sh` for the detectable-stack
  scenarios under test (see **`R-0051`** post-discovery notes for detector/path
  pitfalls).

### Parity

- **`DEC-0056`** requires identical logical outcomes across
  `installer.ps1`, `installer.sh`, `installer.py`, and `bin/its-magic.js`
  delegation, with active + `template/` parity.

### PowerShell runner

- Emitting `tests/run-tests.ps1` as the bootstrap `TEST_COMMAND` is **out of
  scope** for the current baseline contract; widening requires an explicit future
  decision and test updates (`R-0051`).

## Verification

- Story acceptance re-runs consolidated tests and QA evidence so all four
  formerly failing checks pass without assert weakening (`US-0074` `AC-6`,
  `AC-7`, `AC-9`).
- Regression guidance lives in **`DEC-0056`** and this section for future drift.

## Decision linkage

- Research basis: **`R-0051`**
- Decision: **`DEC-0056`**

---

# US-0075: Upgrade scratchpad example–first refresh and paired catalog parity

## Overview

`US-0075` closes **example drift** and **paired-surface skew**: upgrade/install must refresh
**`.cursor/scratchpad.local.example.md`** from the shipped template **before or together with**
any step that advances materialized **`.cursor/scratchpad.md`**, so operators always see a
current **copy-from** catalog. **`AC-11`** adds **deterministic parity** between each
**baseline ↔ example** pair (active repo and `template/`) on **`##` sections** and **`KEY=`**
lines, with values allowed to differ only for documented conservative defaults.

## Ordering model

1. **Template catalog authority** — Framework vocabulary ships in
   **`template/.cursor/scratchpad.local.example.md`** (and is mirrored to active example on
   upgrade/install per pipeline design).
2. **No stale example + fresh baseline** — Any refresh of materialized **`scratchpad.md`**
   from **`template/.cursor/scratchpad.md`** is preceded by or bundled with example refresh
   from **`template/.cursor/scratchpad.local.example.md`** (**`DEC-0057`** §1).
3. **Parity surfaces** — Same ordering and diagnostics across installers, CLI, manifest, and
   `template/` (**`DEC-0057`**, **`US-0075`** **`AC-4`**, **`AC-8`**).

## Merge and ownership (unchanged)

- Precedence and layers remain **`DEC-0055`** (local → materialized baseline → example).
- User **`.cursor/scratchpad.local.md`** is never overwritten by framework refresh (**`DEC-0039`**).

## AC-11 parity gate

- Compare **paired** paths only: active **`.cursor/scratchpad.md`** ↔
  **`.cursor/scratchpad.local.example.md`** and **`template/.cursor/scratchpad.md`** ↔
  **`template/.cursor/scratchpad.local.example.md`**.
- Require **set equality** of **`##` section headers** and **`KEY=`** keys; manifest-documented
  local-only exceptions are the only allowed asymmetry (**`R-0052`** design).
- Enforce in **`tests/run-tests.*`** (or equivalent CI hook), not review-only.

## Diagnostics

- Distinguish **example** vs **materialized baseline** vs **user local** actions with
  deterministic reason families (**`DEC-0039`** alignment, **`US-0075`** **`AC-5`**).

## Verification

- Regression tests for outdated example + current template, post-upgrade example bytes, and
  absence of “baseline moved / example older than template” paths (**`US-0075`** **`AC-6`**,
  **`AC-9`**).

## Decision linkage

- Research basis: **`R-0052`**
- Decision: **`DEC-0057`**

---

# US-0076: Executable scratchpad-driven sync and auto-push wiring

## Overview

**`US-0076`** wires **merged scratchpad** (**`DEC-0055`**) into **`scripts/validate-and-push.ps1`**
and **`scripts/validate-and-push.sh`** so **`SYNC_POLICY_MODE`**, **`ALLOW_AUTO_PUSH`**,
**`SYNC_CUSTOM_PHASES`** (when applicable), and **`AUTO_PUSH_BRANCH_ALLOWLIST`** **actually**
gate an **opt-in** push path, while **`DEC-0018` / `US-0038`** remain the semantic authority
for **reason codes** and **gate order** (**`decisions/DEC-0058.md`** records the executable
contract).

## Approach

1. **Reuse merge** — Invoke **`installer.py`** `parse_scratchpad_file` + `merge_scratchpad_layers`
   (or a tiny extracted shared module) from both scripts so **local → baseline → example**
   precedence cannot drift from **`DEC-0055`**.
2. **Extend validate-and-push only** — Keep a **single** operator entrypoint (**PO/discovery**
   recommendation); avoid a parallel **`sync-from-scratchpad.*`** unless security review forces
   a split (not indicated).
3. **Policy evaluation before git** — After merge, evaluate **disabled / manual / eligibility**
   per **`DEC-0018`**; exit with **`SYNC_DISABLED`**, **`MANUAL_MODE_NO_AUTO`**,
   **`AUTO_PUSH_NOT_ENABLED`**, or **`SYNC_TRIGGER_NOT_ELIGIBLE`** without running tests when
   push is already ruled out (deterministic short-circuit order documented in runbook).
4. **Runbook commands unchanged in role** — Continue reading **`TEST_COMMAND`** and optional
   checks from **`docs/engineering/runbook.md`** only.
5. **QA scan** — Bounded file glob + marker rules per **`DEC-0058`** §6 (not free-form chat
   parsing).
6. **Optional dry-run** — Flag to print decisions and reason codes without **`git push`**.

## Invariants

- **No push** when **`ALLOW_AUTO_PUSH=0`** or mode is **`disabled`** / **`manual`** (**`AC-1`**).
- **No push** on merge/parse failure; **no silent push** on allowlist mismatch (**`AC-4`**).
- **Tests before push** when push is eligible: **`TEST_COMMAND`** required; optional checks
  when configured (**`AC-3`**).
- **Cross-platform parity** — PS1 and sh exit codes and reason tokens match (**`AC-6`**).
- **Operator strings** — **`US-0071`** hygiene on all new/changed script output (**`AC-9`**).

## Components / scripts touched (execute phase)

| Surface | Change |
|--------|--------|
| **`scripts/validate-and-push.ps1`** | Merged scratchpad gate + QA scan + branch allowlist + dry-run |
| **`scripts/validate-and-push.sh`** | Same behavior as PS1 |
| **`installer.py`** (or **`scripts/`** helper) | Callable merge entry (avoid duplicating precedence) |
| **`docs/engineering/runbook.md`** | Document invocation contract, **`SYNC_PHASE_BOUNDARY`**, scan rules |
| **`README.md`** + **`template/`** mirrors | **`AC-7`** operator guidance |
| **`tests/run-tests.ps1`** / **`.sh`** | **`AC-8`** regression fixtures / dry-run assertions |
| **`decisions/DEC-0058.md`** | Executable supplement to **`DEC-0018`** (accepted with architecture) |

## Failure reason codes (non-exhaustive; align with **`US-0038`**)

| Code | When |
|------|------|
| **`SYNC_DISABLED`** | Mode **`disabled`** |
| **`MANUAL_MODE_NO_AUTO`** | Mode **`manual`** or unset invalid treated as manual per policy |
| **`AUTO_PUSH_NOT_ENABLED`** | **`ALLOW_AUTO_PUSH≠1`** |
| **`SYNC_TRIGGER_NOT_ELIGIBLE`** | Boundary/mode mismatch (e.g. **`by_phase`** invocation not eligible per script rules) |
| **`TEST_COMMAND_MISSING`** / **`TEST_FAILED`** / **`TEST_TIMEOUT`** | Runbook test gate |
| **`OPTIONAL_CHECK_FAILED`** | Lint/typecheck when configured |
| **`BRANCH_NOT_ALLOWLISTED`** | Branch pattern fails deterministic allowlist match |
| **`BLOCKING_QA_FINDINGS`** | **`DEC-0058`** §6 scan hit |
| **`PRE_QA_AUTOPUSH_FORBIDDEN`** | **`US-0038`** QA-first signal not met (bounded rule in runbook) |
| **`[SCRATCHPAD_MERGE_ERROR]`** (family) | Merge/parse failure — **no push** |

## Tests strategy (**`AC-8`**)

- **Fixture or temp repo** paths: disabled/manual → no push path; allowlist mismatch →
  **`BRANCH_NOT_ALLOWLISTED`**; merged local override wins over baseline (**`DEC-0055`** spot
  check); **qa-findings** fixture with blocking marker → **`BLOCKING_QA_FINDINGS`**.
- **Dry-run** assertions: happy path reports **`SYNC_PUSHED`** or documented success token
  without invoking **`git push`** when tests are mocked/skipped in CI-safe mode.
- **PS1 / sh** both run the same cases where feasible.

## Migration / compatibility

- **Default-off unchanged**: teams with **`ALLOW_AUTO_PUSH=0`** or **`manual`/`disabled`** see
  **no new push behavior** — scripts may exit earlier with explicit reason codes (**`AC-1`**).
- **No Cursor auto-invocation** added by this story; CI/operator must **run** the script
  (**backlog boundaries**).
- **`DEC-0018`** records remain valid; **`DEC-0058`** **adds** executable interpretation — no
  weakening of **`US-0038`** gates.

## Decision linkage

- Research basis: **`R-0053`**
- Decision: **`DEC-0058`** (executable wiring; **`DEC-0018`** policy authority retained)

---

