# Architecture archive pack (2026-06-12)

- Rollover trigger: `ARCH_HOT_MAX_LINES=3500, ARCH_HOT_MAX_STORY_SECTIONS=120`
- Source: `docs/engineering/architecture.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 29
- First archived heading: `# US-0077: Documentation audience profiles and dual README strategy`
- Last archived heading: `# US-0077: Documentation audience profiles and dual README strategy`
- Verification tuple (mandatory):
  - archived_body_lines=112
  - preamble_lines=10
  - retained_body_lines=3489

---

# US-0077: Documentation audience profiles and dual README strategy

## Overview

**`US-0077`** adds **merged-scratchpad** (**`DEC-0055`**) controls **`DOC_AUDIENCE_PROFILE`**
and **`DOC_DETAIL_LEVEL`** so documentation generation and validation produce deterministic,
audience-appropriate output. **`R-0054`** supplies the **9-cell** semantic-key matrix;
**`DEC-0059`** locks paths, split rules, reason codes, validator location, and migration
defaults.

## Profile semantics

- **Dimensions**: `DOC_AUDIENCE_PROFILE` ∈ {`user`, `developer`, `both`} ×
  `DOC_DETAIL_LEVEL` ∈ {`concise`, `balanced`, `technical-deep`}.
- **Inputs**: **merged** scratchpad only (local → materialized baseline → example); invalid
  combination values → **`DOC_PROFILE_INVALID`**; merge failure → **`DOC_PROFILE_MERGE_ERROR`**.
- **Optional modes**: `SPEC_PACK_MODE` / `USER_GUIDE_MODE` are **additive** only — validators
  must not require their artifacts when **0** (**`R-0054`** §6).
- **Required keys per cell**: same **semantic key** sets as **`R-0054`** matrix (USER_* and
  DEV_* vocabulary); architecture adds **normative H2 literals** below for resolver binding.

## Artifact ownership

| Artifact | Role |
|----------|------|
| **`README.md`** (repo root) | **User channel** — all **`USER_*`** keys required for the resolved cell when profile audience includes **`user`**. |
| **`docs/developer/README.md`** | **Developer channel** — all **`DEV_*`** keys required when audience includes **`developer`** or **`both`**. |
| **`docs/engineering/runbook.md`** | **US-0030** command surface — unchanged; README may link into runbook; no profile-driven rewriting of runbook keys in this story. |
| **`docs/user-guides/US-xxxx.md`** | **US-0032** when enabled. |
| Spec-pack paths | **US-0031** when enabled. |

Cross-links from README to developer shard or runbook are allowed; **authoritative** section
bodies for **`DEV_*`** keys must not live in root README when the cell requires the developer
shard (**`DEC-0059`** §3).

## README split strategy

- **Canonical layout**: **two files** — root **`README.md`** + **`docs/developer/README.md`**.
- **`both` × `concise` / `balanced` / `technical-deep`**: user vs developer keys **split** per
  **`R-0054`**; **`technical-deep`** forbids inlining full **`DEV_*`** bodies in root (pointers
  only).
- **`developer` × \***: **`DEV_*`** content **only** in developer shard; root may include one
  minimal pointer section.
- **H2 budgets** (root README, user-facing body): follow **`R-0054`** table; overflow →
  **`DOC_SECTION_BUDGET_EXCEEDED`**.

## Semantic keys → canonical H2 titles (validator)

Exact heading text (Markdown `## …`) — execute phase implements resolver with trim/normalize
only; renames require updating this table and tests together.

**User channel (`README.md`)**

| Key | H2 title |
|-----|----------|
| `USER_PURPOSE` | `Purpose` |
| `USER_QUICKSTART` | `Quickstart` |
| `USER_EXAMPLES` | `Examples` |
| `USER_TROUBLESHOOTING` | `Troubleshooting` |
| `USER_LIMITATIONS` | `Limitations` |
| `USER_RELATED_DOCS` | `Related documentation` |

**Developer channel (`docs/developer/README.md`)**

| Key | H2 title |
|-----|----------|
| `DEV_PREREQS` | `Prerequisites` |
| `DEV_WORKFLOW` | `Workflow` |
| `DEV_QUALITY_GATES` | `Quality gates` |
| `DEV_ARCHITECTURE` | `Architecture notes` |
| `DEV_CONTRACTS` | `Contracts and interfaces` |
| `DEV_DECISIONS` | `Engineering decisions` |

Optional root pointer for developer-audience navigation (not a semantic-key substitute):
`## Contributing` with a single link line to **`docs/developer/README.md`** — does not count
toward **`DEV_*`** satisfaction.

## Validator and test strategy

1. **Script**: **`scripts/validate_doc_profile.py`** — loads merged scratchpad via
   **`installer.py`** merge (**`DEC-0058`** pattern); resolves cell; checks parse gates,
   completeness (**`DOC_SECTION_MISSING:<key>`**), H2 counts (**`DOC_SECTION_BUDGET_EXCEEDED`**),
   and **active + `template/`** mirror paths for the same logical files (**`DOC_TEMPLATE_PARITY_FAIL`**).
2. **Tests**: **`tests/run-tests.ps1`** / **`.sh`** invoke Tier **A/B/C** fixtures per **`R-0054`**
   (**`AC-8`**): three anchor snapshots, table-driven remaining cells, wiring smoke per
   audience at **`balanced`** depth.
3. **CI cost**: full 9× heavy generation is **not** required every run — resolver + fixture
   trees prove matrix coverage.
4. **US-0071**: validator and generator stdout/stderr use reason codes; markdown bodies on
   scanned surfaces stay within metadata guard allowlists (**extend** in execute if new tools
   emit planning tokens).

## Migration constraints

- **Defaults**: template/example scratchpad documents **`both`** + **`balanced`** as the
  framework recommendation; **absent keys** on merged scratchpad follow **`DEC-0059`** §6
  transition rule (treat as **`both`×`balanced`** for resolver until CI mandates explicit
  keys).
- **Repos without `docs/developer/README.md`**: must add it before claiming **`developer`** or
  **`both`** cells in validation; no silent split — generator/docs updates are **non-destructive**
  (relocate content deliberately, do not drop).
- **Installer/template**: when the framework ships the developer shard, update
  **`docs/engineering/context/installer-owned-paths.manifest`** (and **`template/`** mirror)
  per **`US-0030`** parity.

## Decision linkage

- Research basis: **`R-0054`**
- Decision: **`DEC-0059`**

---

