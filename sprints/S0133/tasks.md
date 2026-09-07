# Sprint S0133 - Task checklist (US-0131)

Total tasks: 9 (T-anch + T-001..T-008). SPRINT_MAX_TASKS=12; SPRINT_AUTO_SPLIT=1; no split. **T-009 folded into T-007** (marker 9 retained).

**Isolation**: `dev-US0131-execute-20260907T200826Z-fresh` · `model_id=composer-2.5` · `orchestrator_run_id=auto-20260907-us0131`

## Task execution order

1. T-anch (NO-OP / verification)
2. T-001 (schema + `.its-magic/config.example.json` + `host_runtime_config_lib.py`; pin `host_mode=None` auto-detect)
3. T-002 (LegacyScratchpadAdapter Model B pre-merge → shared namespace)
4. T-003 (OpenCode-only resolve path; `HOST_CONFIG_PATH_FORBIDDEN` only when OpenCode-only + forbidden cursor-sole request)
5. T-004 (migrate exhaustive 9-module hardcode inventory)
6. T-005 (capability matrix + both-host precedence + shadow diagnostic)
7. T-006 (installer/manifest kernel delivery + never-overwrite locals)
8. T-007 (NEW `tests/us0131_contract_test.py` — **10 markers including marker 9** + template mirror)
9. T-008 (runbook h2 + README + auto-orch cross-link + US-0126 additive `HOST_CONFIG_*` rows)
10. Integration verification

## Critic NB awareness (execute)

- **T-001 / T-003** (`us0131arc-*` NB1): `host_mode=None` means auto-detect — never treat None as OpenCode-only for `HOST_CONFIG_PATH_FORBIDDEN`. Forbidden path only when `host_mode="opencode"` or detected OpenCode-only **and** caller requests `.cursor/` as sole SOT.
- **T-004** (NB2 / R1): Exhaustive inventory of 9 shared-kernel modules (see sprint.md). Marker 8 must cover each migrated module. Do not drop `model_tier_validate.py` path inject (ignore `MODEL_*`).
- **T-007** (NB3): Former T-009 folded here — marker 9 `test_us0131_model_keys_ignored_us0132_boundary` is mandatory in the 10-marker set.

## Task checklist

- [x] **T-anch**: Verify `# US-0131` H1 in `docs/engineering/architecture.md`; verify DEC-0131 Accepted; approach A1 LOCKED; R-0116 DQ1–DQ10 LOCKED; 10-marker table locked; compose guards (US-0132 OUT OF SCOPE; BUG-0015/0016 not reopened); verify `tests/us0131_contract_test.py` does NOT yet exist (or document baseline). Record to `sprints/S0133/t-anch-verification.md`. NO mutation to `architecture.md` / `decisions/DEC-0131.md` in /execute. (DC / DEC baseline; NO-OP)

- [x] **T-001**: Create `.its-magic/config.example.json` (schema_version=1, `shared` KEY→string map, empty `host_overlays.cursor`/`host_overlays.opencode`). Create `scripts/host_runtime_config_lib.py` (+ `template/scripts/` byte-identical) with `resolve_runtime_config(repo_root, *, host_mode: str | None = None, required_keys: Iterable[str] | None = None) -> ResolvedRuntimeConfig{values, provenance, diagnostics}`. **Pin NB1**: `host_mode=None` = auto-detect from install surfaces; do not equate None with OpenCode-only. Support optional `ITS_MAGIC_CONFIG_ROOT` / `--config-root` for tests only. Fail-closed codes: `HOST_CONFIG_SCHEMA_UNSUPPORTED`, `HOST_CONFIG_INVALID`, `HOST_CONFIG_MISSING_REQUIRED`, `HOST_CONFIG_PATH_FORBIDDEN`, `HOST_CONFIG_SECRET_REJECTED`, `HOST_CONFIG_KEY_SHADOWED` (non-fatal unless `HOST_CONFIG_STRICT=1`; default off). Forbid secrets/slugs in examples. Tests: markers 1, 6. (AC-1)

- [x] **T-002**: Implement LegacyScratchpadAdapter inside lib (or adjacent helper): within Cursor layers preserve DEC-0055 Model B (`scratchpad.local.md` > `scratchpad.md` > example), map merged KEY=VAL into shared namespace, then apply DQ6 kit/cursor interleave for final values. Preserve DEC-0039 never-overwrite of `.cursor/scratchpad.local.md`. Ignore `MODEL_*` / `MODEL_TIER_*` (do not validate — US-0132). Tests: marker 2. (AC-2)

- [x] **T-003**: OpenCode-only path: resolve from `.its-magic/` + code defaults only; never require `.cursor/scratchpad*`. Emit `HOST_CONFIG_PATH_FORBIDDEN` only when host is OpenCode-only (explicit `host_mode="opencode"` or auto-detect OpenCode-only) **and** caller requests `.cursor/` as sole SOT. Forbid dumping kit governance keys into `opencode.json{,c}`. Tests: markers 3, 5. (AC-3)

- [x] **T-004**: Migrate **all** shared-kernel hardcode consumers to `resolve_runtime_config` (exhaustive R-0116 inventory — do not omit any):
  1. `scripts/auto_outer_driver.py`
  2. `scripts/opencode_auto_bridge.py`
  3. `scripts/enforce-triad-hot-surface.py`
  4. `scripts/dev_environment_lib.py`
  5. `scripts/caveman_compress_input.py`
  6. `scripts/parallel_dev_arbiter.py`
  7. `scripts/uat_probe_lib.py`
  8. `scripts/validate_autonomy_stop_matrix.py`
  9. `scripts/model_tier_validate.py` — **path inject only**; do not reinterpret/validate `MODEL_*`
  Mirror template counterparts where present. Cursor-only parity scripts stay Cursor-scoped. Tests: marker 8. (AC-4)

- [x] **T-005**: Implement capability matrix (shared / Cursor-only / OpenCode-only / US-0132-owned) with deterministic fail/skip + reason codes (no silent unsupported parity). Implement both-host precedence per DEC-0131 §4 / DQ6 (kit-local > cursor-local > kit-baseline > cursor-baseline > example > defaults). When kit local and Cursor local disagree → kit wins + `HOST_CONFIG_KEY_SHADOWED`. No conflicting duplicate writes of locals. Tests: markers 4, 10. (AC-5, AC-6)

- [x] **T-006**: Deliver `.its-magic/config.example.json` as **kernel** install path for all `--host` modes via `[install_include_paths]` (triple-installer + manifest). Materialize missing `.its-magic/config.json` from example (Model B semantics). **Never overwrite** `.its-magic/config.local.json` or `.cursor/scratchpad.local.md`. Preserve US-0121 host-scoping on clean/upgrade. Tests: marker 7. (AC-7)

- [x] **T-007**: Create `tests/us0131_contract_test.py` (+ `template/tests/` byte-identical) with **exactly 10** markers (AC-8). Markers:
  1. `test_us0131_neutral_path_no_cursor_required`
  2. `test_us0131_cursor_adapter_preserves_dec0055_precedence`
  3. `test_us0131_opencode_only_resolves_shared_from_its_magic`
  4. `test_us0131_both_host_precedence_table`
  5. `test_us0131_rejects_opencode_json_governance_dump`
  6. `test_us0131_schema_fail_closed_codes`
  7. `test_us0131_installer_preserves_local_config`
  8. `test_us0131_shared_kernel_uses_resolver_not_hardcode`
  9. `test_us0131_model_keys_ignored_us0132_boundary` ← **former T-009; must not drop**
  10. `test_us0131_capability_matrix_reason_codes_documented`
  Static/fixture only — **no live OpenCode CI probe**. Fixtures: temp repos for cursor / opencode / both. (AC-8; R5)

- [x] **T-008**: Add runbook h2 `## Cross-host runtime configuration (US-0131)` (active + template byte-identical) covering precedence, migration, unsupported-capability behavior, `HOST_CONFIG_*` codes. README operator subsection + `docs/engineering/auto-orchestration-reference.md` cross-link. US-0126 table: **additive** `HOST_CONFIG_*` rows only (do not rewrite consolidated table ownership). Optional parity scope `us-0131` if clean pair set exists. (AC-8)

## Integration verification (post T-008)

- [x] Test gate: `python -m pytest tests/us0131_contract_test.py -v` → 10/10 PASS
- [x] Parity gate: active ↔ template lib / example / tests / runbook byte-identical where mirrored
- [x] Scope gate: no US-0132 model catalog / `MODEL_*` validation / materializer work; no BUG-0015/0016 reopen; no live OpenCode probe
- [x] Compose gate: DEC-0055/0039/0120 semantics preserved; DEC-0086/0087/0123 untouched
- [x] Status gate: US-0131 remains OPEN; AC checkboxes unchecked; intake JSON not mutated

## Files to touch (scope)

### New (create)

- `.its-magic/config.example.json` (+ ensure `.its-magic/config.local.json` gitignored)
- `scripts/host_runtime_config_lib.py` + `template/scripts/host_runtime_config_lib.py`
- `tests/us0131_contract_test.py` + `template/tests/us0131_contract_test.py`
- `sprints/S0133/t-anch-verification.md` (execute)

### Edit (scoped)

- Shared-kernel modules in T-004 inventory (9)
- Installer / `installer-owned-paths.manifest` (kernel example delivery)
- `docs/engineering/runbook.md` + template (US-0131 h2)
- README + `docs/engineering/auto-orchestration-reference.md`
- US-0126 additive `HOST_CONFIG_*` rows only
- Optional: `scripts/check_intake_template_parity.py` scope `us-0131`
- `.gitignore` for `.its-magic/config.local.json` if missing

### Verify read-only (no mutation)

- `docs/engineering/architecture.md # US-0131`
- `decisions/DEC-0131.md`
- `docs/engineering/research.md ## R-0116`
- `docs/product/backlog.md ## US-0131` Status/ACs (US-0045)
- `docs/product/acceptance.md` US-0131 row
- `handoffs/intake_evidence/US-0131-0132-intake-20260906.json`

### Compose-guard UNCHANGED (DO NOT TOUCH)

| File / surface | Reason |
|---|---|
| Backlog Status / AC checkboxes | US-0045 — closure only |
| `architecture.md` body beyond T-anch verify | locked in /architecture |
| DEC-0086 / DEC-0087 / DEC-0123 | US-0132 / model — out of scope |
| BUG-0015 / BUG-0016 artifacts | DONE — do not reopen |
| `opencode.json` kit-key dump | forbidden (DQ4) |
| Live OpenCode CI probe | forbidden |

## AC → Task surjective coverage

| AC | Task(s) |
|---|---|
| AC-1 | T-001, T-007 (m1, m6) |
| AC-2 | T-002, T-007 (m2) |
| AC-3 | T-003, T-007 (m3) |
| AC-4 | T-004, T-007 (m8) |
| AC-5 | T-005, T-007 (m10) |
| AC-6 | T-005, T-007 (m4, m5) |
| AC-7 | T-006, T-007 (m7) |
| AC-8 | T-007 (all 10 incl. m9), T-008 |
| DC / DEC | T-anch |

**Surjectivity check**: 8/8 ACs covered. No `PLAN_AC_COVERAGE_GAP`. Marker 9 retained in T-007.
