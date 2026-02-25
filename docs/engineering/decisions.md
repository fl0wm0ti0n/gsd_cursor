# Decisions

- DEC-0001: Unused (clean placeholder)
- DEC-0002: Unused (clean placeholder)
- DEC-0003: Accepted — Upgrade mode uses `--mode upgrade` as 4th mode value, path-pattern file classification in installers, `.its-magic-version` for version tracking
- DEC-0004: Accepted — Mixed files (scratchpad.md, README.md) preserved on upgrade with notification about new content

- DEC-0005: Accepted — /ask command is a read-only command with context pack, no subagent role, no file mutations
- DEC-0006: Accepted — Critical evaluation added as step 0 in /intake and /architecture, not as separate /bug or /feature-request commands
- DEC-0007: Accepted — Every phase must run in a fresh subagent context; `/auto` is orchestration-only and spawns a new subagent for each phase/loop cycle
- DEC-0008: Accepted — Add dedicated `/memory-audit` command with read-only, non-blocking report output and explicit memory-drift vs template-drift separation (US-0017 reference only)

- DEC-0009: Accepted — Artifact lifecycle taxonomy: shared placeholder/populated/verified states, phase-ownership matrix, minimum evidence rules. Covers US-0025/US-0026/US-0027 shared foundation including milestone lifecycle states and UAT lifecycle phases.
- DEC-0010: Accepted — Traceability index lives as a section in `docs/engineering/state.md` (not a separate file). Format is story→sprint→tasks→status→evidence table. Maintained by Tech Lead, QA, and Curator.

- DEC-0011: Accepted — Research entry format uses semi-structured R-xxxx IDs with minimal required fields (id, date, topic) and optional enrichment (sources, confidence, linked stories, status). Knowledge base in `docs/engineering/research.md`.
- DEC-0012: Accepted — Security review as dedicated 7th agent role (`security.mdc`) with `/security-review` command, not augmented behavior on existing agents. Flag-controlled (`SECURITY_REVIEW`), zero overhead when disabled.
- DEC-0013: Accepted — Hybrid manifest topology: global registry + local repo/component manifests with explicit ownership and compatibility links.
- DEC-0014: Accepted — Contract diff propagation via structured compatibility signals including impacted consumers and severity-driven gate policy.
- DEC-0015: Accepted — Component-scoped mode uses declarative scope, QA protection checks, and decision-gate escalation for unapproved out-of-scope impact.
- DEC-0016: Accepted — Remote execution uses canonical `.cursor/remote.json` contract with strict mode-aware validation (fail-fast only when `REMOTE_EXECUTION=1`), actionable error reporting, env-var-only secret references, and zero-overhead default when remote mode is off.
- DEC-0017: Accepted — `/auto` continuation uses deterministic phase resolution with explicit `start-from` override, then `resume_brief` phase, then conservative `state.md` fallback; conflicts/staleness fail fast with structured errors and breadcrumb logging.
- DEC-0018: Accepted — Sync policy uses explicit control modes (`disabled|manual|by_phase|by_milestone|custom_phase_list`) with guarded auto-push eligibility, QA-first restrictions, branch allowlist safety, and mandatory pre-push `TEST_COMMAND` baseline.
- DEC-0019: Accepted — `/release` uses deterministic mandatory gate order (check-in tests -> QA -> UAT -> release finalization), no default bypass, and explicit decision-gate override path with evidence logging.
- DEC-0020: Accepted — Per-sprint immutable release notes (`handoffs/releases/Sxxxx-release-notes.md`) plus canonical `handoffs/release_queue.md` state tracker; deterministic `ready -> unreleased -> released` transitions, non-destructive legacy migration from `handoffs/release_notes.md`, and backward-compatible latest-pointer behavior.

Full records: `decisions/DEC-0003.md`, `decisions/DEC-0004.md`, `decisions/DEC-0005.md`, `decisions/DEC-0006.md`, `decisions/DEC-0007.md`, `decisions/DEC-0008.md`, `decisions/DEC-0009.md`, `decisions/DEC-0010.md`, `decisions/DEC-0011.md`, `decisions/DEC-0012.md`, `decisions/DEC-0013.md`, `decisions/DEC-0014.md`, `decisions/DEC-0015.md`, `decisions/DEC-0016.md`, `decisions/DEC-0017.md`, `decisions/DEC-0018.md`, `decisions/DEC-0019.md`, `decisions/DEC-0020.md`
