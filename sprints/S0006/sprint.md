# Sprint S0006

## Goal

Deliver US-0029 (Knowledge Curation & Early Research) by integrating web
research into early workflow phases, restructuring research.md for structured
R-xxxx entries, updating agents and commands for research sub-steps, and
expanding curator scope for knowledge base maintenance.

## Scope

- **In scope**: US-0029 (AC-1..AC-10).
- **Out of scope**: US-0028 (Security & Compliance Review — separate sprint
  after S0006 per architecture recommendation).

## Sizing Check

- `SPRINT_MAX_TASKS=12`
- `SPRINT_AUTO_SPLIT=1`
- Planned tasks: 10
- 10 < 12 — within threshold. Single sprint, no split required.

## Prerequisites

- S0005 (US-0025, US-0027, US-0026) complete.
- DEC-0011 accepted (R-xxxx research entry format).
- Architecture for US-0029 finalized in `docs/engineering/architecture.md`.

## Key decisions

- DEC-0011: Semi-structured R-xxxx entry format with minimal required fields
  (ID, date, topic). Optional enrichment (sources, confidence, linked stories,
  status). Knowledge base in research.md.

## Implementation order

Execute tasks T-001 through T-010 in sequence. T-001 (research.md restructure)
is the foundation — all subsequent tasks depend on the R-xxxx schema being in
place. T-009 (template parity) should be done after all active file changes are
complete to ensure copies are accurate.

## Risks

| Risk | Mitigation |
|------|------------|
| US-0029 touches 3 existing agents (PO, TL, curator) | Test that existing evaluation/challenge behavior still works after adding research sub-steps. Skip gracefully when EARLY_RESEARCH=0. |
| R-xxxx ID collisions | Auto-increment from highest existing ID in research.md. Read file before assigning new ID. |
| Template parity across 8 template files | Single template parity task (T-009) after all active changes complete. |
| Scratchpad flag additions | Update scratchpad.local.example.md alongside scratchpad.md so users see new options. |
| Existing research.md content lost during migration | Dev migrates existing US-0023 content to R-0001 entry in T-001. |

## Definition of Done

- research.md restructured with R-xxxx entry format and existing content
  migrated to R-0001 (AC-3, AC-4, AC-9).
- `/research` command produces structured R-xxxx entries (AC-3).
- PO agent performs early web research during `/intake` when EARLY_RESEARCH=1
  and persists as R-xxxx entry (AC-1).
- TL agent performs early web research during `/architecture` when
  EARLY_RESEARCH=1 and persists as R-xxxx entry (AC-2).
- `/intake` and `/architecture` command steps include explicit research
  sub-step (AC-5).
- R-xxxx entries are referenceable by ID across agents (AC-6).
- Curator includes research.md in maintenance scope (AC-7).
- EARLY_RESEARCH scratchpad flag controls PO/TL research behavior (AC-8).
- All 8 template copies updated to match active files (AC-10).
