# PO to TL archive pack (2026-06-06)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 2
- Retained units in hot file: 14
- First archived heading: `## Orchestrated architecture handoff — BUG-0011 / auto-20260606-02`
- Last archived heading: `## Orchestrated research handoff — BUG-0011 / auto-20260606-02`
- Verification tuple (mandatory):
  - archived_body_lines=106
  - retained_body_lines=754

---

## Orchestrated architecture handoff — BUG-0011 / auto-20260606-02

### Target

- `bug_id=BUG-0011`
- `orchestrator_run_id=auto-20260606-02`
- phase completed: **`architecture`** (**`tech-lead`**)
- `fresh_context_marker=tl-BUG0011-architecture-20260606T144123Z-fresh`
- `next_scheduled_phase=sprint-plan`
- `segment_work_item_kind=bug`
- `bug_queue_position=3` / `bug_queue_remaining=1`
- `dec_id=DEC-0077`

### Summary

- **`/architecture`** **PASS** — **`DEC-0077`** authored; **`docs/engineering/architecture.md`** **`# BUG-0011`** appended; **`# US-0089`** §6 cross-link amended (voice rules delivered here; qualitative brevity operator-verified); **`R-0077`** locked; voice-section outline, SHA bump policy, nine `test_caveman_voice_*` markers, harness **§30A**, runbook compact table locked.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Locked decisions (DEC-0077 summary)

1. **Rule append** — `## Voice compression (when CAVEMAN_MODE=1)` + six subsections (`### Precedence` through `### Ultra and literal regions`); compose on **DEC-0072** (no rewrite).
2. **Level semantics** — kit-native lite/full/ultra table; no Wenyan.
3. **SHA dual layer** — bump `_CAVEMAN_RULE_BASELINE_SHA256` + additive `test_caveman_voice_*`; preserve `test_caveman_default_off_*` bodies.
4. **Harness §30A** — `Voice compression rule markers (BUG-0011)`.
5. **Runbook** — compact 2-row table under Caveman mode; US-0090 subsection untouched.
6. **Template parity** — byte-identical `caveman.mdc` + runbook Caveman subsection.

### Atomic task seeds (8; `/sprint-plan` converts to T-xxx)

See **`docs/engineering/architecture.md`** **`# BUG-0011`** § Atomic task seeds.

### Evidence refs

- `decisions/DEC-0077.md`
- `docs/engineering/architecture.md` (**`# BUG-0011`**, **`# US-0089`** §6 amendment)
- `docs/engineering/decisions.md` (index + context pack)
- `docs/product/backlog.md` (`### BUG-0011` `architecture_notes`)
- `docs/engineering/research.md` (**`R-0077`**)
- `docs/engineering/state.md` (Architecture checkpoint — this run)
- `handoffs/resume_brief.md` (sprint-plan pointer)

### Next

- **`/sprint-plan`** (fresh **tech-lead** context) for **`BUG-0011`** — seed sprint from 8 task seeds + AC ↔ § map.

### Decision gate

- **None** — architecture satisfied; bug **OPEN**.

---

## Orchestrated research handoff — BUG-0011 / auto-20260606-02

### Target

- `bug_id=BUG-0011`
- `orchestrator_run_id=auto-20260606-02`
- phase completed: **`research`** (**`tech-lead`**)
- `fresh_context_marker=tl-BUG0011-research-20260606T143942Z-fresh`
- `next_scheduled_phase=architecture`
- `segment_work_item_kind=bug`
- `bug_queue_position=3` / `bug_queue_remaining=1`

### Summary

- **`/research`** **PASS** — extended **`R-0077`** with Q1–Q7 resolution. **Rule append**: `## Voice compression (when CAVEMAN_MODE=1)` with kit-native lite/full/ultra table, drop-filler/fragment directives, auto-clarity, persistence, `### Precedence` over user-rule prose. **Tests**: nine additive `test_caveman_voice_*` subtests + harness **§30A** candidate; intentional `_CAVEMAN_RULE_BASELINE_SHA256` bump; **DEC-0072** §6 `test_caveman_default_off_*` bodies preserved byte-unchanged. **US-0090** input compression orthogonal and untouched.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Key findings (architecture inputs)

1. **SHA (Q1)**: dual layer — marker subtests + baseline SHA bump at execute (not regression).
2. **Levels (Q2)**: upstream table semantics; kit-native examples; no Wenyan; not roleplay voice.
3. **Precedence (Q3)**: self-contained `### Precedence` in `caveman.mdc`; reply-voice only; does not override git/security/tool rules.
4. **Markers (Q4)**: `test_caveman_voice_section_heading_present` through `test_caveman_voice_template_parity` (nine subtests).
5. **Runbook (Q5)**: compact 2-row before/after under Caveman mode; full contract in rule file.
6. **Surface (Q6)**: dedicated `# BUG-0011` + `# US-0089` §6 cross-link (remove voice-gap note).
7. **Ultra (Q7)**: defer to existing 9-zone MUST; `### Ultra and literal regions` pointer stub only.

### Evidence refs

- `docs/engineering/research.md` (**`R-0077`** research extension)
- `docs/product/backlog.md` (`### BUG-0011` — `research_notes`)
- `docs/product/acceptance.md` (`BUG-0011` row — unchecked)
- `handoffs/intake_evidence/BUG-0011-intake-20260606.json`
- `.cursor/rules/caveman.mdc`; `template/.cursor/rules/caveman.mdc` (pre-voice SHA `E10EFC32…E47DE`)
- `decisions/DEC-0072.md` §2 (rule-only), §4 (9-zone), §6 (pinned tests)
- `tests/auto_command_contract_test.py` (`test_caveman_default_off_*`, `test_caveman_compress_input_*`)
- `docs/engineering/state.md` (Research checkpoint — this run)
- `handoffs/resume_brief.md` (architecture pointer)

### Architecture asks (companion DEC-xxxx)

1. Lock voice-section outline (heading text, precedence paragraph, intensity table shape, ultra deferral stub) in companion **DEC-xxxx** composing on **DEC-0072** (no rewrite).
2. Author `docs/engineering/architecture.md` **`# BUG-0011`** with AC map, atomic task seeds, SHA bump policy, harness §30A id, template parity inventory.
3. Amend `# US-0089` §6 forward-link — voice rules delivered here; qualitative brevity remains operator-verified.

### Next

- **`/architecture`** (fresh **tech-lead** context) for **`BUG-0011`** — lock companion DEC + architecture section before **`/sprint-plan`**.

### Decision gate

- **None** — research satisfied; bug **OPEN**.

---

