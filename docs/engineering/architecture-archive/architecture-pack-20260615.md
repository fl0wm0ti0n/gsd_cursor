# Architecture archive pack (2026-06-15)

- Rollover trigger: `ARCH_HOT_MAX_LINES=3000, ARCH_HOT_MAX_STORY_SECTIONS=120`
- Source: `docs/engineering/architecture.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 15
- First archived heading: `# US-0090: Optional Caveman-style input compression (safe file scope)`
- Last archived heading: `# US-0090: Optional Caveman-style input compression (safe file scope)`
- Verification tuple (mandatory):
  - archived_body_lines=280
  - preamble_lines=10
  - retained_body_lines=2846

---

# US-0090: Optional Caveman-style input compression (safe file scope)

## Overview

**Composes on `# US-0089`** (response-side Caveman voice — `DEC-0072`). This
section delivers the **input-side** contract: an optional, script-invoked,
default-off file compressor under operator-controlled scope with sidecar
originals, hard deny-list, and single-algorithm safe-mode idempotency.

Binding decision: **`DEC-0073`** (composes on `DEC-0072` without rewriting
it). This section is a **self-contained summary** for sprint planners; open
`decisions/DEC-0073.md` for the normative statement, alternatives, and risk
resolutions.

## Forbidden surfaces (deny-list baseline — hard MUST)

Input compression **never** touches, even when an allow-list glob would
otherwise match, and even when an operator explicitly requests it:

- Secrets — `.env`, `.env.*`, `**/.env`, `**/.env.*` (**`US-0085`** /
  **`R-0072`**).
- Intake evidence — `handoffs/intake_evidence/*.json` (**`US-0078`** /
  **`DEC-0060`**; `BUG-0007` class risk).
- Canonical product / engineering authority — `docs/product/backlog.md`,
  `docs/product/acceptance.md`, `docs/engineering/state.md`,
  `docs/engineering/decisions.md`, `decisions/DEC-*.md` (**`US-0045`**,
  `DEC-0040`).
- Sprint lifecycle evidence — `sprints/*/*`.
- Publish / runtime / install surfaces — `package.json`,
  `package-lock.json`, `installer.*`, `.github/workflows/*.yml`,
  `.cursor/hooks/*.py`, `bin/its-magic.js`, `packaging/homebrew/*.rb`.
- Contract surfaces — `.cursor/rules/*.mdc`, `.cursor/commands/*.md`,
  `.cursor/skills/**/SKILL.md` (Caveman voice composes with them; compression
  must never rewrite them).
- Manifest / parity sources —
  `docs/engineering/context/installer-owned-paths.manifest`,
  `docs/engineering/release-targets.json`,
  `docs/engineering/token-cost-parity-manifest.md`.
- Binaries — `.png`, `.jpg`, `.pdf`, `.zip`, archives, fonts, media, `.bin`,
  `.exe`, `.dll`.
- Vendor-install text containing `npx skills add` (carried from
  `DEC-0072` §8).

`DEC-0073` §4.1 contains the verbatim baseline. Evaluation order:
deny-hard → `.gitignore` secret merge → optional `.cursorignore` overlay →
allow-list → literal-region scan → write. Deny always wins over allow.

## Minimal architecture

### A. Activation (DEC-0073 §2)

Activates only when **all** hold:

1. `CAVEMAN_COMPRESS_INPUT=1` in `.cursor/scratchpad.md` (default `0`).
2. `CAVEMAN_FILE_SCOPE=` resolves to a non-empty set after §5 grammar
   parsing.
3. CLI mode is explicit (`--write` for mutation; `--verify-originals` for
   read-only sidecar audit).

Default is off. Empty scope fails closed with
`CAVEMAN_COMPRESS_SCOPE_EMPTY`.

### B. Sidecar original policy (DEC-0073 §3)

Parallel tree: `docs/.caveman-originals/<relative/path>/<file>`. Atomic
write order: sidecar (temp+replace) → literal-region scan on proposed
output → target (temp+replace). Any step fails → no partial state.
`.gitkeep` materializes the root; repo-root `.gitignore` anchor
`docs/.caveman-originals/`. `.cursorignore` remains operator-owned per
**`US-0085`**.

### C. Allow-list grammar (DEC-0073 §5)

`CAVEMAN_FILE_SCOPE` accepts: named profile (v1: `docs-prose-only`) |
raw CSV globs | hybrid `profile:<name>;globs:<csv>`. Empty = pure opt-in.
Unknown profile fails closed with `CAVEMAN_COMPRESS_SCOPE_UNKNOWN_PROFILE`.

**Frozen v1 profile (`docs-prose-only`)**:

- `docs/user-guides/**/*.md`
- `docs/engineering/runbook.md`
- `docs/engineering/state-archive/**/*.md`
- `handoffs/archive/*.md`

### D. Compression algorithm — safe-mode only in v1 (DEC-0073 §6)

Single deterministic line-level minifier:

1. Collapse runs of ≥2 blank lines to one.
2. Trim trailing whitespace.
3. Normalize line endings to `\n`.
4. Preserve EOF-newline status.

Idempotent by construction: `compress(compress(f)) == compress(f)` byte-for-
byte. **Aggressive mode** (filler-word strip + prose rewriter) and **LLM-
assisted** compression are **out of scope** in v1. No `--mode` flag ships in
v1 — reserved for future DEC.

**Literal-region invariant** (`DEC-0072` §4 reused verbatim — nine zones):
fenced code, file paths, AC checklists, reason codes, IDs, contract markers,
strict-proof tuple fields, isolation evidence fields, git refs. Any byte
difference inside a zone fails closed with
`CAVEMAN_COMPRESS_LITERAL_REGION_DAMAGED` **before** commit.

### E. CLI contract (DEC-0073 §8)

`scripts/caveman_compress_input.py` (active + `template/scripts/` mirror).
Flags: `--dry-run` (default), `--write`, `--verify-originals`, `--report`
(JSON to stdout). Conflicting flags fail closed with
`CAVEMAN_COMPRESS_FLAG_CONFLICT`. Exit `0` only on zero violations.

### F. Reason-code vocabulary — 9 codes, 3 families, pre/during-write only (DEC-0073 §7)

| Family | Codes |
|--------|-------|
| **Gating** | `CAVEMAN_COMPRESS_MODE_DISABLED`, `CAVEMAN_COMPRESS_FLAG_CONFLICT` |
| **Scope** | `CAVEMAN_COMPRESS_SCOPE_EMPTY`, `CAVEMAN_COMPRESS_SCOPE_UNKNOWN_PROFILE`, `CAVEMAN_COMPRESS_SCOPE_VIOLATION` |
| **Integrity** | `CAVEMAN_COMPRESS_DENY_HIT`, `CAVEMAN_COMPRESS_NOT_IDEMPOTENT`, `CAVEMAN_COMPRESS_LITERAL_REGION_DAMAGED`, `CAVEMAN_COMPRESS_ORIGINAL_MISSING` |

No post-write codes. No new codes without a subsequent DEC revising §7.

## Three-axis non-substitution (DEC-0073 §1)

`TOKEN_PROFILE` (US-0080 / DEC-0062), `CAVEMAN_MODE` (DEC-0072 §1), and
`CAVEMAN_COMPRESS_INPUT` (this DEC) are **three independent axes**. None
substitutes for another. The following paragraph is published verbatim in
**`docs/engineering/auto-orchestration-reference.md`** and
**`docs/engineering/runbook.md`** (active + `template/` mirrors; extends
the DEC-0072 §1 published paragraph in-place):

> `TOKEN_PROFILE` controls context breadth. `CAVEMAN_MODE` controls reply
> voice. `CAVEMAN_COMPRESS_INPUT` controls input-side file mutation. None
> substitutes for another; setting one does not change the others. Combine
> freely.

Operator phrases from DEC-0072 §5 (`caveman on`, `caveman: lite`…) do **not**
activate input compression. Input compression is **script-invoked**, not
voice-toggled.

## Template parity (DEC-0073 §9) — 8-row inventory

| # | Active path | Template path | Change |
|---|-------------|---------------|--------|
| 1 | `scripts/caveman_compress_input.py` (**new**) | `template/scripts/caveman_compress_input.py` (**new**) | Byte-identical script. |
| 2 | `docs/engineering/runbook.md` | `template/docs/engineering/runbook.md` | `### Caveman input compression (US-0090)` subsection. |
| 3 | `docs/engineering/auto-orchestration-reference.md` | `template/docs/engineering/auto-orchestration-reference.md` | Replace DEC-0072 §1 paragraph with the three-sentence form. |
| 4 | `docs/engineering/architecture.md` `# US-0090` | active-only | This section. |
| 5 | `tests/auto_command_contract_test.py` | active-only | Extend in place with `test_caveman_compress_input_*`. |
| 6 | `tests/fixtures/caveman_compress/` (**new**) | active-only | Fixture classes 1–8 (see DEC-0073 §9 test strategy). |
| 7 | `.gitignore` | n/a | Add repo-root anchor `docs/.caveman-originals/`. |
| 8 | `docs/.caveman-originals/.gitkeep` (**new**) | active-only | Empty placeholder. |

**NEGATIVE parity (MUST NOT be touched)**:
`.cursor/rules/caveman.mdc` (+ `template/` mirror; pre-US-0090 SHA-256
`E10EFC32C628E790E69E2393F381108FE0B1F16E0BCDCFFFC162EFF6F91E47DE`
preserved — R10 mitigation), scratchpad byte strings (DEC-0072 §3 key
reservations retained; semantics activated without renaming),
`.cursor/skills/its-magic/SKILL.md` (+ mirror), contract-surface files
(DEC-0072 §7 rows 8/9 preserved), all canonical artifacts in the deny-list.

## Installer / publish (DEC-0073 §10)

- `docs/engineering/context/installer-owned-paths.manifest` (active +
  `template/`) gains `template/scripts/caveman_compress_input.py` under
  `install_include_paths` (R11 mitigation — defends against the exact
  BUG-0003 defect class).
- No new npm script; no new runtime / dev dependency (stdlib Python only).
- Parity test: extend `scripts/check_intake_template_parity.py` with
  `--scope=caveman-compress` mode (asserts script byte-identity).
- Install-completeness fixture: extend
  `tests/installer_completeness_bug0003_test.py` to verify
  `--mode missing` / `--mode upgrade` deliver
  `template/scripts/caveman_compress_input.py` across all three installer
  entrypoints.
- A new `run-tests` section (candidate `§26S`; exact number locked by
  `/sprint-plan`) runs the US-0090 contract and fixture suite.

## Test strategy (DEC-0073 §9 — STRATEGY ONLY; `/sprint-plan` + `/execute` own implementation)

Fixture classes under `tests/fixtures/caveman_compress/` (active only;
architecture may add but MUST NOT narrow):

1. **Whitespace baseline** — multi-blank collapse + trailing trim + LF
   normalize.
2. **Literal-region preservation** — one fixture per DEC-0072 §4 zone (9
   total).
3. **Deny-list refusal** — one fixture per DEC-0073 §4.1 entry class
   (asserts `CAVEMAN_COMPRESS_DENY_HIT` before any mutation).
4. **Scope violations** — empty / outside allow / unknown profile →
   respective scope reason codes.
5. **Idempotency (AC-6)** — compress twice, assert byte-equal.
6. **Mode-disabled** — `CAVEMAN_COMPRESS_INPUT=0` → `CAVEMAN_COMPRESS_MODE_DISABLED`.
7. **Original-missing** — `--verify-originals` on orphan →
   `CAVEMAN_COMPRESS_ORIGINAL_MISSING`.
8. **Flag-conflict** — conflicting / unknown CLI flags →
   `CAVEMAN_COMPRESS_FLAG_CONFLICT`.

Additional contract-test guards:

- Deny-list version guard — `--report`'s `deny_list_version` SHA-256 is
  stable across runs; changes require a DEC.
- Rule byte-identity guard (R10) — active and template
  `.cursor/rules/caveman.mdc` remain byte-equal post-US-0090 (SHA-256
  equality assertion).

Extend `tests/auto_command_contract_test.py` in place with a
`test_caveman_compress_input_*` prefix. Existing `test_caveman_default_off_*`
subtests (DEC-0072 §6 row 6 invariant) remain byte-unchanged.

## Guardrail invariants

- **Default off** — no file mutation without explicit
  `CAVEMAN_COMPRESS_INPUT=1` + non-empty `CAVEMAN_FILE_SCOPE` + `--write`.
- **Deny always wins over allow** — evaluation order in §B.
- **Sidecar-first atomic write** — no target mutation without a sidecar
  successfully written first; temp+replace on both.
- **Literal-region invariant** — DEC-0072 §4 nine zones reused verbatim;
  byte-equality required pre-commit.
- **Idempotent algorithm** — safe-mode minifier is strictly idempotent by
  construction.
- **No post-write reason codes** — all failures pre- or during-write.
- **No rule-file edit in v1** — `.cursor/rules/caveman.mdc` byte-identity
  preserved.
- **No scratchpad / contract-surface / canonical-artifact rewrite** —
  enforced structurally via §4.1 deny-list.
- **No vendor-install leak** — DEC-0072 §8 `npx skills add` ban carried.
- **No `TOKEN_PROFILE` / `CAVEMAN_MODE` / strict-proof / isolation /
  `AUTO_QUIET` / US-0071 contract change** — input compression is
  orthogonal.

## Risks and mitigations

- **R8** — aggressive-mode filler-word drift → **deferred aggressive mode
  entirely in v1** (DEC-0073 §6); future DEC must specify frozen list +
  `--report` hash.
- **R9** — reason-code proliferation → locked 9-code set grouped into three
  families; no additions without a subsequent DEC revising §7.
- **R10** — rule-subsection byte-identity → **no subsection added to
  `.cursor/rules/caveman.mdc` in v1**; pre-US-0090 SHA-256
  `E10EFC32C628E790E69E2393F381108FE0B1F16E0BCDCFFFC162EFF6F91E47DE`
  preserved; contract subtest guards byte-equality.
- **R11** — install-completeness omission → install-completeness fixture
  extension is **non-negotiable** (DEC-0073 §10); `/sprint-plan` MUST seed
  a task; `/release` MUST NOT ship without it.

## Decision linkage

- Research basis: **`R-0073`** (shared anchor with US-0089; no new `R-xxxx`
  allocated per DEC-0011 precedent).
- Decision: **`DEC-0073`** (composes on **`DEC-0072`** — forward-link, not
  rewrite).
- Related: **`US-0089`** / **`DEC-0072`** (response-side substrate),
  **`US-0053`** / **`DEC-0035`** (tiered profile), **`US-0080`** /
  **`DEC-0062`** (`TOKEN_PROFILE`), **`US-0085`** / **`DEC-0071`** (`.env`
  / `.cursorignore` / `.gitignore` defense-in-depth; `R-0072`),
  **`US-0078`** / **`DEC-0060`** (intake evidence integrity),
  **`US-0045`** (backlog status authority), **`DEC-0040`** (artifact
  ordering), **`US-0017`** (active / template parity policy),
  **`BUG-0001`** / **`DEC-0063`** + **`BUG-0003`** / **`DEC-0066`**
  (installer-completeness precedent), **`US-0088`** (`AUTO_QUIET`),
  **`US-0071`** (user-visible metadata), **`US-0048`** / **`DEC-0029`**
  (isolation evidence), **`US-0056`** / **`DEC-0038`** (strict runtime
  proof), **`US-0069`** / **`DEC-0051`** (phase-role matrix),
  **`BUG-0006`** (spawn-only).
- External reference (not vendored): JuliusBrussee/caveman (MIT) —
  `https://github.com/JuliusBrussee/caveman`.

## AC traceability

| AC | Governing section(s) |
|----|----------------------|
| AC-1 Gating | §A (activation) + DEC-0073 §2 + §7 |
| AC-2 Originals | §B (sidecar) + DEC-0073 §3 |
| AC-3 Deny list | §Forbidden surfaces + DEC-0073 §4 + §7 |
| AC-4 Scope | §C (allow-list grammar) + DEC-0073 §5 + §7 |
| AC-5 Operator UX | §E (CLI) + runbook subsection (row 2) + §B (revert via sidecar) |
| AC-6 Tests | §D (idempotent by construction) + test strategy classes 1–8 |
| AC-7 `# US-0090` | This section (links `# US-0089`, US-0053, US-0085, US-0078 / DEC-0060) |
| AC-8 Template parity | §Template parity + Installer / publish |

