# its-magic scratchpad (local overrides example)
#
# Copy this file to `.cursor/scratchpad.local.md` and set your personal values.
# This file is intended to stay local and is gitignored.
#
# Team identity / ownership
# - TEAM_MODE: 0|1
# - TEAM_MEMBER: short id for current developer
# - ACTIVE_TASK_IDS: comma-separated task ids (for example T-12,T-13)
TEAM_MODE=0
TEAM_MEMBER=
ACTIVE_TASK_IDS=
#
# Personal automation style
# - PHASE_MODE: interactive|auto
# - PERMISSION_MODE: interactive|auto
# - RUN_TESTS_ON_EDIT: 0|1
# - LOOP_UNTIL_GREEN: 0|1
# - AUTO_IMPLEMENTATION_LOOP: 0|1
# - AUTO_LOOP_MAX_CYCLES: integer >= 1
# - AUTO_PAUSE_POLICY: after_task|after_phase
PHASE_MODE=interactive
PERMISSION_MODE=interactive
RUN_TESTS_ON_EDIT=0
LOOP_UNTIL_GREEN=0
AUTO_IMPLEMENTATION_LOOP=0
AUTO_LOOP_MAX_CYCLES=5
AUTO_PAUSE_POLICY=after_phase
#
# Personal environment preferences
# - AUTO_INSTALL_DEPS: 0|1
# - REMOTE_EXECUTION: 0|1
# - REMOTE_CONFIG: path to your local remote config
AUTO_INSTALL_DEPS=0
REMOTE_EXECUTION=0
REMOTE_CONFIG=.cursor/remote.json
