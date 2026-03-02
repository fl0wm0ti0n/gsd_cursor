# Release notes — S0026 (US-0031)

## Summary

- **Sprint:** S0026  
- **Story:** US-0031 — Optional Documentation Pack (Design Concept, CRS, Technical Spec)  
- **Release date:** 2026-03-02  
- **Status:** Released  

## Scope

Optional spec-pack workflow (Design Concept, CRS, Technical Specification) behind
`SPEC_PACK_MODE=0|1` with zero-overhead default-off behavior, validation
guidance, traceability, ownership, and active/template parity.

## Delivered

- **AC-1:** Single enable flag `SPEC_PACK_MODE=0|1` in `.cursor/scratchpad.md`
  (active and template), default `0`.
- **AC-2:** Intake, architecture, release, execute, qa document zero-overhead
  when `SPEC_PACK_MODE=0`.
- **AC-3:** Canonical paths when enabled: design-concept, crs,
  technical-specification + spec-pack README in active and template.
- **AC-4:** Minimum required sections in runbook and spec-pack README; completeness
  testable.
- **AC-5:** Release step 3c and `SPEC_PACK_INCOMPLETE` gate when enabled and
  required sections missing.
- **AC-6:** Traceability story ID → three artifact paths in runbook and
  spec-pack README.
- **AC-7:** Ownership (Design Concept: TL/architecture; CRS: PO/intake; Technical
  Spec: TL create, Dev update) in runbook.
- **AC-8:** Template parity: commands, runbook, README, US-0031 regression
  checks in run-tests.

## Gate evidence

| Gate        | Result | Evidence |
|------------|--------|----------|
| Check-in tests | PASS | tests/report.md 2026-03-01T23:07:17Z, Pass: 330, Fail: 0 |
| QA completion  | PASS | sprints/S0026/qa-findings.md, no blockers |
| UAT completeness | PASS | sprints/S0026/uat.json (8/8), uat.md |
| Backlog reconciliation | — | US-0031 → DONE, ACs checked |

## Artifacts

- `.cursor/scratchpad.md`, `template/.cursor/scratchpad.md` (SPEC_PACK_MODE)
- Commands: intake, architecture, release, execute, qa (active + template)
- `docs/engineering/runbook.md`, `docs/engineering/spec-pack/README.md`
- `tests/run-tests.ps1`, `tests/run-tests.sh` (US-0031 regression checks)

## Notes

- `SPEC_PACK_MODE=0` (default): no extra required steps; when set to `1`,
  release validates target-story spec-pack artifacts and blocks with
  `SPEC_PACK_INCOMPLETE` only when required sections are missing.
