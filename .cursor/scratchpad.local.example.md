# its-magic scratchpad (local overrides example)
#
# Copy this file to `.cursor/scratchpad.local.md` and set personal overrides.
# Local values override `.cursor/scratchpad.md` and should stay gitignored.
#
# Core behavior
# - MAGIC_CONTEXT_STRICT: 0|1 (require context refresh after code changes)
# - LOOP_UNTIL_GREEN: 0|1 (optional test loop)
# - RUN_TESTS_ON_EDIT: 0|1 (run tests after edits)
# - AUTO_IMPLEMENTATION_LOOP: 0|1 (auto cycle execute->qa->execute)
# - AUTO_LOOP_MAX_CYCLES: integer >= 1 (safety guard)
# - AUTO_PAUSE_REQUEST: 0|1 (request graceful stop at next safe boundary)
# - AUTO_PAUSE_POLICY: after_task|after_phase (safe stop boundary)
# - DONE: 0|1 (stop hook loops)
MAGIC_CONTEXT_STRICT=1
LOOP_UNTIL_GREEN=0
RUN_TESTS_ON_EDIT=0
AUTO_IMPLEMENTATION_LOOP=0
AUTO_LOOP_MAX_CYCLES=5
AUTO_PAUSE_REQUEST=0
AUTO_PAUSE_POLICY=after_phase
DONE=0
#
# Benchmarking
# - MAGIC_BENCH_SESSION: free-form id for live benchmark logging
MAGIC_BENCH_SESSION=
#
# Automation
# - AUTO_FLOW_MODE: manual|auto_until_decision
# - PHASE_MODE: interactive|auto
# - PERMISSION_MODE: interactive|auto
# - AUTO_INSTALL_DEPS: 0|1
# - AUTO_RELEASE_NOTES: 0|1
# - AUTO_BACKLOG_DRAIN: 0|1 (continue across multiple stories when enabled)
# - AUTO_BACKLOG_MAX_STORIES: integer >= 1 (max stories per auto run when drain enabled)
# - AUTO_BACKLOG_ON_BLOCK: stop|skip (behavior when a story blocks)
# - AUTO_STORY_SELECTION: priority_then_backlog_order
# - AUTO_EXECUTE_BULK: 0|1 (explicit bulk execute orchestration mode)
# - AUTO_EXECUTE_MAX_ITEMS: integer >= 1 (max planned items per bulk execute run)
# - AUTO_EXECUTE_ON_BLOCK: stop|skip (behavior when a planned item blocks)
# - AUTO_EXECUTE_SELECTION: planned_then_priority
# - AUTO_TEAM_SCOPE_ENFORCE: 0|1 (when TEAM_MODE=1, enforce TEAM_MEMBER + ACTIVE_TASK_IDS)
AUTO_FLOW_MODE=auto_until_decision
PHASE_MODE=interactive
PERMISSION_MODE=interactive
AUTO_INSTALL_DEPS=0
AUTO_RELEASE_NOTES=1
AUTO_BACKLOG_DRAIN=0
AUTO_BACKLOG_MAX_STORIES=1
AUTO_BACKLOG_ON_BLOCK=stop
AUTO_STORY_SELECTION=priority_then_backlog_order
AUTO_EXECUTE_BULK=0
AUTO_EXECUTE_MAX_ITEMS=1
AUTO_EXECUTE_ON_BLOCK=stop
AUTO_EXECUTE_SELECTION=planned_then_priority
AUTO_TEAM_SCOPE_ENFORCE=1
#
# Team mode
# - TEAM_MODE: 0|1 (enable task/member scoped team workflow)
# - TEAM_MEMBER: short id for current developer
# - ACTIVE_TASK_IDS: comma-separated task ids (for example T-12,T-13)
TEAM_MODE=0
TEAM_MEMBER=
ACTIVE_TASK_IDS=
#
# Sprint planning
# - SPRINT_MAX_TASKS: integer >= 1 (max atomic tasks per sprint, default 12)
# - SPRINT_AUTO_SPLIT: 0|1 (propose splitting when over threshold)
# - SPRINT_BULK_MAX_STORIES: integer >= 1 (candidate stories when /sprint-plan --bulk)
# - SPRINT_BULK_MAX_SPRINTS: integer >= 1 (generated sprints per /sprint-plan --bulk run)
# - SPRINT_BULK_SELECTION: priority_then_backlog_order
SPRINT_MAX_TASKS=12
SPRINT_AUTO_SPLIT=1
SPRINT_BULK_MAX_STORIES=5
SPRINT_BULK_MAX_SPRINTS=3
SPRINT_BULK_SELECTION=priority_then_backlog_order
#
# Remote execution
# - REMOTE_EXECUTION: 0|1
# - REMOTE_CONFIG: path to remote config
REMOTE_EXECUTION=0
REMOTE_CONFIG=.cursor/remote.json
#
# Sync policy
# - SYNC_POLICY_MODE: disabled|manual|by_phase|by_milestone|custom_phase_list
# - SYNC_CUSTOM_PHASES: comma-separated canonical phase IDs; only used when
#   SYNC_POLICY_MODE=custom_phase_list
# - ALLOW_AUTO_PUSH: 0|1 (default off; explicit opt-in required)
# - AUTO_PUSH_BRANCH_ALLOWLIST: comma-separated branches/patterns eligible for
#   auto-push. Protected/default branches are denied unless allowlisted.
SYNC_POLICY_MODE=manual
SYNC_CUSTOM_PHASES=
ALLOW_AUTO_PUSH=0
AUTO_PUSH_BRANCH_ALLOWLIST=
#
# Knowledge curation / intake
# - EARLY_RESEARCH: 0|1 (PO/TL search web during intake/architecture)
# - INTAKE_GUIDED_MODE: 0|1 (guided intake follow-up/options/research behavior)
# - INTAKE_SUBAGENT_FALLBACK: deny|allow (deny by default; when deny, missing
#   role-specific intake subagent capability fails fast)
# - ID_NAMESPACE_BOOTSTRAP: 0|1 (optional fresh-project ID bootstrap mode; when 1, allow first IDs to start at 0001 only if deterministic freshness checks pass)
# - TOKEN_PROFILE: lean|balanced|full (tiered token-cost profile defaults)
#   - lean: lowest-token default profile; reduce non-critical automation/research intensity
#   - balanced: default profile; preserves current behavior with moderate overhead
#   - full: highest-context profile; maximize context breadth/autonomy
# - STATE_HOT_MAX_LINES: integer >= 200 (hot-surface soft cap trigger for
#   archival rollover checks)
# - STATE_HOT_MAX_CHECKPOINTS: integer >= 10 (max recent checkpoints to retain
#   in `state.md` after rollover)
# - Manual-override precedence: explicit flag values in this file remain authoritative
#   for that flag and override profile defaults.
EARLY_RESEARCH=1
INTAKE_GUIDED_MODE=1
INTAKE_SUBAGENT_FALLBACK=deny
ID_NAMESPACE_BOOTSTRAP=0
TOKEN_PROFILE=balanced
STATE_HOT_MAX_LINES=1200
STATE_HOT_MAX_CHECKPOINTS=80
#
# Publish targets
# - RELEASE_PUBLISH_MODE: disabled|confirm|auto
#   - disabled: skip post-release publish target execution
#   - confirm: require explicit operator confirmation before publish (default)
#   - auto: allow publish without confirmation (explicit opt-in)
# - RELEASE_TARGETS_FILE: canonical target config path
# - RELEASE_TARGETS_DEFAULT: comma-separated default target IDs (optional)
RELEASE_PUBLISH_MODE=confirm
RELEASE_TARGETS_FILE=docs/engineering/release-targets.json
RELEASE_TARGETS_DEFAULT=
#
# Security review
# - SECURITY_REVIEW: 0|1 (enable optional security/compliance review; default off)
# - COMPLIANCE_PROFILES: comma-separated values (GDPR,SOC2,HIPAA,PCI-DSS,ISO27001)
#   Empty value means general security best practices only.
#   When SECURITY_REVIEW=0, the workflow adds zero security-review overhead.
SECURITY_REVIEW=0
COMPLIANCE_PROFILES=GDPR
#
# Compatibility observability
# - CROSS_REPO_OBSERVABILITY: 0|1 (enable compatibility visibility and checks)
# - COMPATIBILITY_GATE_ON_CRITICAL: 0|1 (when enabled, critical unresolved
#   compatibility findings trigger decision gate before release)
# - COMPATIBILITY_SOURCES: semicolon-separated sources
#   (repo=<path|url>,module=<id>,contract=<path|url>,docs=<path|url>)
CROSS_REPO_OBSERVABILITY=0
COMPATIBILITY_GATE_ON_CRITICAL=1
COMPATIBILITY_SOURCES=
#
# Component scope
# - COMPONENT_SCOPE_MODE: 0|1 (enable scoped planning/execution guardrails)
# - TARGET_COMPONENTS: comma-separated component IDs intended in scope
COMPONENT_SCOPE_MODE=0
TARGET_COMPONENTS=
#
# Optional docs packs
# - SPEC_PACK_MODE: 0|1 (enable Design Concept, CRS, Technical Spec generation/validation; default 0)
#   When 0, intake/architecture/release add no required spec-pack steps.
# - USER_GUIDE_MODE: 0|1 (enable per-feature user guides at docs/user-guides/US-xxxx.md; default 0)
#   When 0, intake/architecture/sprint-plan/execute/qa/release add no required user-guide steps or blocking checks.
SPEC_PACK_MODE=0
USER_GUIDE_MODE=0
