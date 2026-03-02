# Component Scope

- Mode: optional (`COMPONENT_SCOPE_MODE`)
- Story: US-0035

## Scope declaration

- scope_mode: on
- target_components:
  - api-gateway
- non_target_components:
  - web-app
  - worker
- allowed_interface_touch:
  - public-api-v1
- out_of_scope_constraints:
  - no intentional edits in non-target components without explicit approval
- approval_policy:
  - required: true
  - source: decision/handoff artifact
