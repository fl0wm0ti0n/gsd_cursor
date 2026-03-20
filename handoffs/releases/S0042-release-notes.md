# Release Notes - S0042 (`US-0062`)

## What shipped

- Introduced installer-owned metadata boundary at `its_magic/`.
- Canonicalized installed version marker to `its_magic/.its-magic-version`.
- Added backward-compatible migration for legacy root `.its-magic-version`.
- Updated clean/install ownership manifest to include `its_magic`.
- Updated regression coverage for install/upgrade/clean boundary behavior.

## Operational notes

- Existing repositories remain backward-compatible during upgrade.
- Legacy root version marker is removed after canonical write succeeds.
