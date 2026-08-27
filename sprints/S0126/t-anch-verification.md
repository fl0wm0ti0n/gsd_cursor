# S0126 / US-0126 — T-anch verification (NO-OP / verification only)

- **fresh_context_marker**: dev-US0126-execute-20260825T163028Z-fresh
- **role**: dev (fresh per BUG-0006)
- **timestamp**: 2026-08-25T16:30:28Z (UTC)
- **model_id**: glm-5.2-high (CROSS_MODEL_REVIEW=1 — required)
- **orchestrator_run_id**: auto-20260825-01

## Verification checks (read-only; no mutation of architecture.md or DEC-0126)

| # | Check | Result |
|---|-------|--------|
| 1 | `# US-0126` H1 anchor in `docs/engineering/architecture.md` (after `# US-0125` L1481, before `# US-0089` L2053 per DEC-0073 §11) | PASS — anchor at L1747 (verified) |
| 2 | DEC-0126 Accepted at `decisions/DEC-0126.md` (§1 runbook section, §2 locked operator sentences, §3 consolidated reason-code table, §4 parity scope + layer split, §5 12-marker contract-test list, §6 template parity manifest unchanged, §7 compose-do-not-amend, §8 isolation + runtime proof) | PASS — Status: Accepted at L4 (verified); all 8 sections present |
| 3 | Compose guards 8/8 UNCHANGED baseline (US-0071, US-0113..US-0117, US-0121/DEC-0120, US-0122/DEC-0122, US-0123, US-0124/DEC-0124, US-0125/DEC-0125, US-0102/DEC-0087) | PASS — read-only consumers; US-0126 additive-only |
| 4 | 12-marker contract-test list locked in architecture AC-4 table | PASS — markers 1..12 enumerated at architecture L1905-L1918 |
| 5 | Runbook h2 placement (immediately after `## OpenCode thin commands + validator bridge (US-0125)` section) + reason-code table (4 `OPENCODE_*` US-0124 + 5 installer `OPENCODE_*`/`CURSOR_*` US-0121 + 3 reused cross-host + raw Python validator codes; NO `OPENCODE_VALIDATOR_FAILED` wrapper per DEC-0125 DQ7) + parity extension (2 new pairs in `OPENCODE_ADAPTER_PAIRS`: `tests/us0126_contract_test.py` ↔ template + `docs/engineering/runbook.md` ↔ template) + DoD/reminder/out-of-scope locked sentences + manifest unchanged lock locked in DEC-0126 §1–§8 | PASS — all contracts verified in DEC-0126 §1..§8 |
| 6 | `docs/engineering/runbook.md` does NOT yet have `## OpenCode host operator runbook (US-0126)` h2 pre-T-001 | PASS — h2 absent (verified; runbook ends at L4018 after US-0125 cross-link) |
| 7 | `tests/us0126_contract_test.py` + `template/tests/us0126_contract_test.py` do NOT yet exist pre-T-004 | PASS — both files absent (verified) |
| 8 | `OPENCODE_ADAPTER_PAIRS` in `scripts/check_intake_template_parity.py` does NOT yet list the 2 new pairs pre-T-003 (current 8 pairs only) | PASS — 8 pairs at L484-L517; US-0126 pairs absent (verified) |
| 9 | `README.md` + `template/its_magic/README.md` do NOT yet have the OpenCode host blurb pre-T-002 | PASS — README.md has only US-0124 bullet at L367; template/its_magic/README.md has US-0121..US-0125 subsections at L368-L407 but no US-0126 subsection (verified) |
| 10 | `installer-owned-paths.manifest` active↔template byte-identical pre-T-001 (DQ8 lock — UNCHANGED) | PASS — manifest pair byte-identical (verified via Python file hash compare) |
| 11 | `docs/engineering/runbook.md` active↔template byte-identical pre-T-001 (whole-file pair baseline) | PASS — runbook pair byte-identical 198822 bytes (verified via Python file hash compare) |
| 12 | `scripts/check_intake_template_parity.py` active↔template byte-identical pre-T-003 | PASS — parity script pair byte-identical (verified) |
| 13 | `.cursor/commands/` + `.cursor/agents/` present pre-T-009 (AC-10 baseline inventory) | PASS — 25 `.md` files in `.cursor/commands/`; 7 `.mdc` files in `.cursor/agents/` (captured for marker 11 baseline) |

## Critic NB (non-blocking)

- T-anch NO-OP only — no `architecture.md` / `DEC-0126.md` mutation in /execute (mirrors US-0122 / US-0123 / US-0124 / US-0125 T-anch ceremony).
- Architecture heading order (# US-0125 L1481 -> # US-0126 L1747 -> # US-0089 L2053) and DEC-0126 Accepted state are read-only verified, not mutated.
- Carry-in `ik_us0126_sp_ac1_marker_prose_gap` routed to T-001/T-004/T-006: AC-1 marker 1 grep must include h2 PLUS AC-1 operator phrases (stock OpenCode TUI/desktop/IDE as UI, `--host` opt-in, `/connect` keys, kit UX = slash commands + reason codes) — defense in depth beyond h2-only grep.
- Carry-in AC-10 inventory path pin: T-009 marker 11 uses a sorted file-name list of `.cursor/commands/*.md` + `.cursor/agents/*.mdc` captured at execute time (not a frozen git snapshot, not a hash manifest of the entire `.cursor/` directory).

## Verdict

PASS — T-anch baseline verified; proceed to T-001 (runbook h2 body with T-005 consolidated reason-code table inline).
