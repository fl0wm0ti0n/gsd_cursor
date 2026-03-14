# Decisions

## Current context pack (2026-03-14)

- Latest completed/released stories:
  - `US-0059` (`S0038`), governed by `DEC-0041`.
  - `US-0058` (`S0037`), governed by `DEC-0040`.
  - `US-0057` (`S0036`), governed by `DEC-0039`.
  - `US-0056` (`S0035`), governed by `DEC-0038`.
  - `US-0055` (`S0034`), governed by `DEC-0037`.
  - `US-0054` (`S0033`), governed by `DEC-0036`.
  - `US-0052` (`S0031`), governed by `DEC-0034`.
  - `US-0053` (`S0032`), governed by `DEC-0035`.
- Latest architecture decision: `DEC-0041` for `US-0059` (intake capability
  fail-fast plus single-writer drift safety contract).
- Next prioritized open story: none in current active intake queue.
- Active intake/research target: none (awaiting next intake).
- No open decision gate at workflow boundary.

## Compact decision index (bounded summaries)

- `DEC-0041`: deterministic intake capability preflight with fail-fast
  `SUBAGENT_CAPABILITY_UNAVAILABLE`, explicit fallback policy, and
  single-writer self-write-aware drift safety
  (`INTAKE_CONCURRENT_WRITER_DETECTED` for external conflicts); linked story
  `US-0059`.
- `DEC-0040`: canonical artifact ordering matrix (`append-bottom`,
  `prepend-top`, `sorted-canonical`) plus fail-safe anchor handling and
  idempotent rerun contract; linked story `US-0058`.
- `DEC-0039`: Upgrade-safe scratchpad example refresh contract with explicit
  ownership boundaries (`.cursor/scratchpad.local.example.md` framework-owned,
  `.cursor/scratchpad.local.md` user-owned), deterministic diagnostics, and
  installer parity checks; linked story `US-0057`.
- `DEC-0038`: strict runtime attestation envelope and boundary
  validator for `/auto` with deterministic fail-closed reason codes and
  pause/resume provenance integration; linked story `US-0056`.
- `DEC-0037`: Deterministic status reconciliation command with canonical
  precedence, bounded repair, auditable normalization evidence, and resume
  readiness update; linked story `US-0055`.
- `DEC-0036`: Configurable multi-target publish contract with default
  confirmation boundary, schema validation, and first-class `custom` + `ssh`
  target support; linked story `US-0054`.
- `DEC-0035`: Tiered token profile (`lean|balanced|full`), compact
  active-context/archive policy, compact decisions index, and `/ask`
  narrow-read retrieval; linked story `US-0053`.
- `DEC-0034`: Optional fresh-project ID namespace bootstrap with deterministic
  freshness checks; linked story `US-0052`.
- `DEC-0033`: Intake decomposition + risk-aware PO questioning with bounded
  split heuristics and explicit user authority; linked story `US-0051`.
- `DEC-0032`: Installer-owned manifest controls install/clean ownership with
  clean-starter hygiene and lifecycle parity checks; linked story `US-0050`.
- `DEC-0029`: Per-phase fresh-context isolation evidence is mandatory at phase
  boundaries; linked story `US-0048`.
- `DEC-0025`: Canonical story status source is `docs/product/backlog.md`, with
  target-scoped derived reconciliation in acceptance/state.

## Canonical full records

- Full records live in decisions/DEC-xxxx.md.
- Index pattern: `decisions/DEC-0003.md` ... `decisions/DEC-0041.md`.
