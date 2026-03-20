# Sprint S0047

- Story: `US-0068`
- Goal: enforce deterministic mandatory intake question packs (first and small intake) with fail-closed coverage gating before persistence.
- Status: execute complete (ready for QA)

## Scope

- Deterministic `first-intake-pack` and `small-intake-pack` schema with explicit topic IDs and required/optional classification.
- Fail-closed intake persistence gate when required coverage is missing, with bounded explicit-assumption confirmation path.
- Guided and low-touch mode compatibility while preserving critical minimum safety coverage.
- Intake evidence persistence for `asked_topics`, `missing_topics`, `assumptions_confirmed`, and deterministic block reason codes.
- Active/template parity and regression coverage for positive and blocked intake paths.
