# Architecture archive pack (2026-03-27)

- Rollover trigger: `ARCH_HOT_MAX_LINES=3500, ARCH_HOT_MAX_STORY_SECTIONS=120`
- Source: `docs/engineering/architecture.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 32
- First archived heading: `# US-0034: Multi-Repo and Contract Compatibility Observability`
- Last archived heading: `# US-0034: Multi-Repo and Contract Compatibility Observability`
- Verification tuple (mandatory):
  - archived_body_lines=176
  - preamble_lines=10
  - retained_body_lines=3365

---

# US-0034: Multi-Repo and Contract Compatibility Observability

## Overview

US-0034 adds optional compatibility observability across repositories and
components using manifest artifacts and contract-change signals. The goal is
deterministic impact visibility for planning, QA, and release decisions, not
runtime dependency orchestration.

This architecture follows the user clarification:
- Keep a global view for inventory and cross-repo links.
- Keep per-repo and per-component manifests close to each codebase.
- Surface API changes directly to dependent repos/components so agents can
  derive required work.

## Minimal manifest model

### A1) Global registry manifest (inventory + links)

Canonical artifact:
- `docs/engineering/manifests/registry.manifest.yaml`

Purpose:
- Source-of-truth inventory of known repos/components.
- Cross-repo contract dependency links.
- Ownership and lifecycle visibility.

Minimum required fields:
- `schema_version`
- `generated_at`
- `repos[]`: `{ repo_id, repo_url_or_path, owner, status, manifest_ref }`
- `contracts[]`: `{ contract_id, producer_repo, producer_component, contract_ref, version }`
- `compatibility_links[]`: `{ contract_id, consumer_repo, consumer_component, expected_version_range, criticality }`

### A2) Per-repo manifest

Canonical artifact (inside each repo):
- `docs/engineering/manifests/repo.manifest.yaml`

Purpose:
- Local declaration of exposed and consumed contracts.
- Repo-level owner/version/status metadata.

Minimum required fields:
- `schema_version`
- `repo_id`
- `owner`
- `version`
- `components[]` (references to component manifests)
- `exports[]` (contracts this repo publishes)
- `imports[]` (contracts this repo consumes)

### A3) Per-component manifest

Canonical artifact:
- `docs/engineering/manifests/components/<component_id>.manifest.yaml`

Purpose:
- Unit of scoped change analysis and protection checks.

Minimum required fields:
- `component_id`
- `repo_id`
- `owner`
- `status` (`active|deprecated|experimental|retired`)
- `exposed_contracts[]` (`contract_id`, `api_spec_ref`, `version`)
- `consumed_contracts[]` (`contract_id`, `expected_version_range`)
- `protected_interfaces[]` (interfaces expected to remain stable for non-target work)

### A4) Compatibility map and contract links

Compatibility is represented as producer->consumer edges in
`registry.manifest.yaml.compatibility_links[]`, with each edge tied to a
specific `contract_id` and expected consumer version range.

This creates a deterministic impact graph:
- Contract changes from producer side identify all consumer edges.
- Each edge yields a candidate impact task in sprint planning.

### A5) Change signal model (contract diff + impact)

Canonical artifact:
- `docs/engineering/compatibility-signals.md`

Each signal entry records one observed contract change:
- `signal_id` (`CS-xxxx`)
- `date`
- `story_id`
- `producer_repo` / `producer_component`
- `contract_id`
- `from_version` / `to_version`
- `change_type` (`additive|behavioral|breaking|docs-only`)
- `impacted_consumers[]`
- `severity` (`info|low|medium|high|critical`)
- `required_actions[]` (for impacted repos/components)
- `status` (`open|planned|validated|accepted-risk|resolved`)

Severity baseline:
- `breaking` with impacted consumers -> `high` (or `critical` for
  production-critical links).
- `behavioral` -> `medium`.
- `docs-only` drift -> `low`.

## Workflow integration

### B1) Phase responsibilities

| Phase | Manifest/compatibility responsibilities |
|------|------------------------------------------|
| `/intake` | If enabled, declare target repos/modules and contract artifacts in story scope. |
| `/architecture` | Define/confirm registry and local manifest updates; create compatibility approach and risk policy. |
| `/sprint-plan` | Convert compatibility links + open change signals into explicit tasks per impacted consumer. |
| `/execute` | Update local manifests when contracts/components change; append contract-change signals. |
| `/qa` | Validate impacted consumer coverage and verify signal statuses/evidence. |
| `/verify-work` | Confirm traceability from story -> signals -> tasks -> QA evidence. |
| `/release` | Apply compatibility gate only when enabled and unresolved high/critical findings exist. |
| `/refresh-context` | Curator compacts stale signals, verifies manifest consistency, and updates state summary. |

### B2) Impact derivation model for agents

When a contract change is detected, agents derive work deterministically:
1. Find `contract_id` in `registry.manifest.yaml`.
2. Enumerate `compatibility_links` for consumers.
3. For each consumer edge, create/verify tasks:
   - contract alignment update,
   - consumer regression/smoke verification,
   - docs alignment if public API docs changed.
4. Record findings in `compatibility-report.md` and link to story/sprint tasks.

### B3) Findings and gating policy

Canonical compatibility findings artifact:
- `docs/engineering/compatibility-report.md`

Minimum finding fields:
- `finding_id`
- `story_id`
- `contract_id`
- `producer` + `consumer`
- `severity`
- `evidence`
- `recommended_action`
- `gate_recommendation` (`none|decision-gate`)

Gate behavior:
- Default: non-blocking advisory output.
- If `CROSS_REPO_OBSERVABILITY=1` and unresolved `critical` findings exist,
  trigger decision gate before release progression.

### B4) Default-off / zero-overhead behavior

Control flags in `.cursor/scratchpad.md`:
- `CROSS_REPO_OBSERVABILITY=0` (default)
- `COMPATIBILITY_GATE_ON_CRITICAL=1` (effective only when observability is on)

When `CROSS_REPO_OBSERVABILITY=0`:
- No required manifest processing.
- No required compatibility report updates.
- No additional blocking gates.

## Artifacts and status taxonomy

Canonical files:
- `docs/engineering/manifests/registry.manifest.yaml`
- `docs/engineering/manifests/repo.manifest.yaml`
- `docs/engineering/manifests/components/<component_id>.manifest.yaml`
- `docs/engineering/compatibility-signals.md`
- `docs/engineering/compatibility-report.md`

Status taxonomy:
- Manifest entity status: `active|deprecated|experimental|retired`
- Signal status: `open|planned|validated|accepted-risk|resolved`
- Finding severity: `info|low|medium|high|critical`

---

