# its-magic scratchpad
#
# Core behavior
# - MAGIC_CONTEXT_STRICT: 0|1 (require context refresh after code changes)
# - LOOP_UNTIL_GREEN: 0|1 (optional test loop)
# - RUN_TESTS_ON_EDIT: 0|1 (run tests after edits)
# - DONE: 0|1 (stop hook loops)
MAGIC_CONTEXT_STRICT=1
LOOP_UNTIL_GREEN=0
RUN_TESTS_ON_EDIT=0
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
# Remote execution
# - REMOTE_EXECUTION: 0|1
# - REMOTE_CONFIG: path to remote config
REMOTE_EXECUTION=0
REMOTE_CONFIG=.cursor/remote.json

