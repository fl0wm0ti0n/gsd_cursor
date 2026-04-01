# PO to TL archive pack (2026-03-28)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 2
- Retained units in hot file: 29
- First archived heading: `## Research Addendum — US-0078`
- Last archived heading: `## Intake Addendum — Official Remote Config Template, Docs, and Validation`
- Verification tuple (mandatory):
  - archived_body_lines=60
  - retained_body_lines=753

---

## Research Addendum — US-0078

> Placement: **prepend** hot copy for TL read model (`orchestrator_run_id=auto-20260328-01`). If triad **`--check`** fails after edits, **`--rollover`** per **DEC-0054** and retain **tail mirror** below.

- **Closure**: **`/research`** (**tech-lead**) complete for **`US-0078`**; **`R-0055`** extended with evidence schema sketch (**`topic_coverage`**, **`satisfied_by`**, **`ref`**), parser/validation rules, reason-code alignment, and **AC-8** regression matrix + tiered tests.
- **Next**: **`/architecture`** — lock **`ref`** binding and artifact placement (**DEC-0050** amendment or new DEC), migration for legacy intake evidence, active/template parity plan.
- **Decision gate before architecture**: **none** (remaining choices are normal architecture scope).

---

## Intake Addendum — Official Remote Config Template, Docs, and Validation

### New intake

User request: "Ship official `.cursor/remote.json` template + docs + validation."

Confirmed context in scratchpad:
- `REMOTE_EXECUTION` flag already exists.
- `REMOTE_CONFIG=.cursor/remote.json` already exists.
- Repository currently lacks an official `.cursor/remote.json` template artifact.

### Overlap and duplicate evaluation

- No direct duplicate found in current backlog.
- Related but non-duplicate stories:
  - `US-0017` template drift guard: parity governance only; does not define remote config schema or validation contract.
  - `US-0030` release doc-delta gate: release-time docs parity check; does not define remote execution configuration behavior.
  - `US-0028` optional security review: establishes "optional feature with zero-overhead-off mode" pattern; remote config is separate capability.
- Decision: create a new story so remote config contract/safety requirements remain explicit and testable.

### Accepted story

#### US-0036 — Official Remote Config Template, Docs, and Fail-Fast Validation
- Priority: P1
- Status: OPEN
- Intent: make remote execution safe and deterministic by shipping canonical config artifacts, schema guidance, and strict validation rules when enabled.

### TL guidance and boundaries

- In scope:
  - Canonical `.cursor/remote.json` in active + `template/`.
  - Documented schema/field contract and example targets.
  - Fail-fast validation behavior for enabled mode (`REMOTE_EXECUTION=1`).
  - Clear error-message contract and remediation hints.
  - Security guidance: no secrets committed in repo config.
  - README + runbook instructions, plus template parity verification.
  - Zero-overhead behavior when `REMOTE_EXECUTION=0`.
- Out of scope:
  - Implementing new remote transport protocols/backends.
  - Building external secret-management infrastructure.

### Planning recommendation

1. Define the remote config schema first (required/optional fields + allowed values).
2. Implement and document validation contract second (including error text expectations).
3. Add docs/runbook/README coverage and parity checks across active + template copies.
4. Include negative-path QA cases (missing file, malformed JSON, invalid fields, secret-like values).

---

