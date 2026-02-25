# its-magic scratchpad
#
# Shared team defaults live here.
# Personal developer overrides belong in `.cursor/scratchpad.local.md`
# (copy from `.cursor/scratchpad.local.example.md`).
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
AUTO_FLOW_MODE=manual
PHASE_MODE=interactive
PERMISSION_MODE=interactive
AUTO_INSTALL_DEPS=0
AUTO_RELEASE_NOTES=0
#
# Sprint planning
# - SPRINT_MAX_TASKS: integer >= 1 (max atomic tasks per sprint, default 12)
# - SPRINT_AUTO_SPLIT: 0|1 (propose splitting when over threshold)
SPRINT_MAX_TASKS=12
SPRINT_AUTO_SPLIT=1
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
# Knowledge curation
# - EARLY_RESEARCH: 0|1 (PO/TL search web during intake/architecture)
EARLY_RESEARCH=1

#
# Security review
# - SECURITY_REVIEW: 0|1 (enable optional security/compliance review; default off)
# - COMPLIANCE_PROFILES: comma-separated values (GDPR,SOC2,HIPAA,PCI-DSS,ISO27001)
#   Empty value means general security best practices only.
#   When SECURITY_REVIEW=0, the workflow adds zero security-review overhead.
SECURITY_REVIEW=0
COMPLIANCE_PROFILES=GDPR

