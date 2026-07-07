#!/usr/bin/env python3
"""Verify active vs template/scripts/ bytes match for DEC-0063 intake gate modules (BUG-0001).

Scoped modes (DEC-0073 §10 / US-0090):
  --scope=intake          (default) DEC-0063 intake pair table.
  --scope=caveman-compress DEC-0073 caveman input-compression pair table.
  --scope=readme-feature-coverage DEC-0074 README feature-coverage pair table.
  --scope=downstream-ci-guard   DEC-0075 downstream CI guard script pair table.
  --scope=us-0092               DEC-0078 full-autonomy outer driver + probe surfaces.
  --scope=us-0093               DEC-0079 browser UAT probe surfaces.
  --scope=us-0095               DEC-0080 native in-chat auto-chain surfaces.
  --scope=bug-0012              DEC-0081 native-chain compliance surfaces (BUG-0012).
  --scope=us-0096               DEC-0082 delivery modes surfaces (US-0096).
  --scope=project-readme        DEC-0083 project README bootstrap surfaces (US-0097).
  --scope=dev-environment       DEC-0084 dev auto-launch profile surfaces (US-0098).
  --scope=sovereign-parallel-dev DEC-0108 parallel instance arbitrage surfaces (US-0108).
  --scope=sovereign-self-healing-deploy DEC-0109 self-healing deploy loop surfaces (US-0109).
  --scope=release-trigger-adapter DEC-0111 release trigger adapter surfaces (US-0111).
  --scope=us-0119               DEC-0119 autonomous-autonomy preset surfaces (US-0119).
  --scope=all              union of all tables.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

INTAKE_TEMPLATE_PAIRS: tuple[tuple[str, str], ...] = (
    ("scripts/intake_evidence_validate.py", "template/scripts/intake_evidence_validate.py"),
    ("scripts/intake_evidence_lib.py", "template/scripts/intake_evidence_lib.py"),
    ("scripts/intake_bug_routing_guard.py", "template/scripts/intake_bug_routing_guard.py"),
    ("scripts/intake_bug_resume_brief_refresh.py", "template/scripts/intake_bug_resume_brief_refresh.py"),
    ("scripts/check_intake_template_parity.py", "template/scripts/check_intake_template_parity.py"),
)

# DEC-0073 §10 / US-0090 — Caveman input-compression surface pairs. Contents
# must be byte-identical between active and template paths; installer delivers
# template copies (BUG-0003 / DEC-0066).
CAVEMAN_COMPRESS_PAIRS: tuple[tuple[str, str], ...] = (
    ("scripts/caveman_compress_input.py", "template/scripts/caveman_compress_input.py"),
    ("docs/engineering/context/installer-owned-paths.manifest",
     "template/docs/engineering/context/installer-owned-paths.manifest"),
    ("docs/engineering/runbook.md", "template/docs/engineering/runbook.md"),
    ("docs/engineering/auto-orchestration-reference.md",
     "template/docs/engineering/auto-orchestration-reference.md"),
)

README_FEATURE_COVERAGE_PAIRS: tuple[tuple[str, str], ...] = (
    (
        "scripts/validate_readme_feature_coverage.py",
        "template/scripts/validate_readme_feature_coverage.py",
    ),
    (
        "scripts/readme_feature_coverage_lib.py",
        "template/scripts/readme_feature_coverage_lib.py",
    ),
    (
        "docs/engineering/context/readme-section-affinity.json",
        "template/docs/engineering/context/readme-section-affinity.json",
    ),
    (".cursor/commands/release.md", "template/.cursor/commands/release.md"),
    ("docs/engineering/runbook.md", "template/docs/engineering/runbook.md"),
    (
        "docs/engineering/context/installer-owned-paths.manifest",
        "template/docs/engineering/context/installer-owned-paths.manifest",
    ),
    (
        "scripts/check_intake_template_parity.py",
        "template/scripts/check_intake_template_parity.py",
    ),
)

US0092_PAIRS: tuple[tuple[str, str], ...] = (
    ("scripts/auto_outer_driver.py", "template/scripts/auto_outer_driver.py"),
    ("scripts/uat_probe_lib.py", "template/scripts/uat_probe_lib.py"),
    (
        "docs/engineering/context/installer-owned-paths.manifest",
        "template/docs/engineering/context/installer-owned-paths.manifest",
    ),
    (".cursor/commands/auto.md", "template/.cursor/commands/auto.md"),
    (".cursor/commands/verify-work.md", "template/.cursor/commands/verify-work.md"),
    (".cursor/commands/qa.md", "template/.cursor/commands/qa.md"),
    (
        "docs/engineering/auto-orchestration-reference.md",
        "template/docs/engineering/auto-orchestration-reference.md",
    ),
    ("docs/engineering/runbook.md", "template/docs/engineering/runbook.md"),
)

US0093_PAIRS: tuple[tuple[str, str], ...] = (
    ("scripts/uat_probe_lib.py", "template/scripts/uat_probe_lib.py"),
    (".cursor/commands/verify-work.md", "template/.cursor/commands/verify-work.md"),
    (".cursor/commands/qa.md", "template/.cursor/commands/qa.md"),
    (".cursor/commands/execute.md", "template/.cursor/commands/execute.md"),
    (
        ".cursor/scratchpad.local.example.md",
        "template/.cursor/scratchpad.local.example.md",
    ),
    ("docs/engineering/runbook.md", "template/docs/engineering/runbook.md"),
    (
        "docs/engineering/auto-orchestration-reference.md",
        "template/docs/engineering/auto-orchestration-reference.md",
    ),
    (
        "docs/engineering/context/installer-owned-paths.manifest",
        "template/docs/engineering/context/installer-owned-paths.manifest",
    ),
)

US0095_PAIRS: tuple[tuple[str, str], ...] = (
    (".cursor/commands/auto.md", "template/.cursor/commands/auto.md"),
    (
        "docs/engineering/auto-orchestration-reference.md",
        "template/docs/engineering/auto-orchestration-reference.md",
    ),
    ("docs/engineering/runbook.md", "template/docs/engineering/runbook.md"),
    ("README.md", "template/README.md"),
    (
        "scripts/check_intake_template_parity.py",
        "template/scripts/check_intake_template_parity.py",
    ),
)

BUG0012_PAIRS: tuple[tuple[str, str], ...] = (
    (".cursor/commands/auto.md", "template/.cursor/commands/auto.md"),
    (
        "docs/engineering/auto-orchestration-reference.md",
        "template/docs/engineering/auto-orchestration-reference.md",
    ),
    ("docs/engineering/runbook.md", "template/docs/engineering/runbook.md"),
    (
        "scripts/check_intake_template_parity.py",
        "template/scripts/check_intake_template_parity.py",
    ),
)

US0096_PAIRS: tuple[tuple[str, str], ...] = (
    (
        ".cursor/scratchpad.local.example.md",
        "template/.cursor/scratchpad.local.example.md",
    ),
    (".cursor/commands/auto.md", "template/.cursor/commands/auto.md"),
    (
        "docs/engineering/auto-orchestration-reference.md",
        "template/docs/engineering/auto-orchestration-reference.md",
    ),
    ("docs/engineering/runbook.md", "template/docs/engineering/runbook.md"),
    (".cursor/commands/quick.md", "template/.cursor/commands/quick.md"),
    (
        "scripts/check_intake_template_parity.py",
        "template/scripts/check_intake_template_parity.py",
    ),
    ("scripts/pack_json_validate.py", "template/scripts/pack_json_validate.py"),
)

PROJECT_README_PAIRS: tuple[tuple[str, str], ...] = (
    (
        "scripts/validate_project_readme_coverage.py",
        "template/scripts/validate_project_readme_coverage.py",
    ),
    (
        "scripts/project_readme_coverage_lib.py",
        "template/scripts/project_readme_coverage_lib.py",
    ),
    (".cursor/commands/execute.md", "template/.cursor/commands/execute.md"),
    (".cursor/commands/release.md", "template/.cursor/commands/release.md"),
    ("docs/engineering/runbook.md", "template/docs/engineering/runbook.md"),
    (
        "docs/engineering/context/installer-owned-paths.manifest",
        "template/docs/engineering/context/installer-owned-paths.manifest",
    ),
    (
        ".cursor/scratchpad.local.example.md",
        "template/.cursor/scratchpad.local.example.md",
    ),
    (
        "scripts/check_intake_template_parity.py",
        "template/scripts/check_intake_template_parity.py",
    ),
)

DEV_ENVIRONMENT_PAIRS: tuple[tuple[str, str], ...] = (
    (".cursor/commands/execute.md", "template/.cursor/commands/execute.md"),
    (".cursor/scratchpad.md", "template/.cursor/scratchpad.md"),
    (
        ".cursor/scratchpad.local.example.md",
        "template/.cursor/scratchpad.local.example.md",
    ),
    (
        "template/.cursor/dev-environment.json.example",
        "template/.cursor/dev-environment.json.example",
    ),
    (
        "scripts/dev_environment_lib.py",
        "template/scripts/dev_environment_lib.py",
    ),
    ("docs/engineering/runbook.md", "template/docs/engineering/runbook.md"),
    (
        "docs/engineering/auto-orchestration-reference.md",
        "template/docs/engineering/auto-orchestration-reference.md",
    ),
    (
        "scripts/check_intake_template_parity.py",
        "template/scripts/check_intake_template_parity.py",
    ),
)

RELEASE_CHANGELOG_PAIRS: tuple[tuple[str, str], ...] = (
    (
        "scripts/release_changelog_lib.py",
        "template/scripts/release_changelog_lib.py",
    ),
    (
        "scripts/release_changelog_validate.py",
        "template/scripts/release_changelog_validate.py",
    ),
    (
        "scripts/release_changelog_backfill.py",
        "template/scripts/release_changelog_backfill.py",
    ),
    ("CHANGELOG.md", "template/CHANGELOG.md"),
    (".cursor/commands/release.md", "template/.cursor/commands/release.md"),
    ("scripts/release-all.sh", "template/scripts/release-all.sh"),
    (
        "template/handoffs/releases/vX.Y.Z-release-notes.md.example",
        "template/handoffs/releases/vX.Y.Z-release-notes.md.example",
    ),
    (
        "scripts/check_intake_template_parity.py",
        "template/scripts/check_intake_template_parity.py",
    ),
)

MODEL_TIER_PAIRS: tuple[tuple[str, str], ...] = (
    (
        "scripts/model_tier_lib.py",
        "template/scripts/model_tier_lib.py",
    ),
    (
        "scripts/model_tier_validate.py",
        "template/scripts/model_tier_validate.py",
    ),
    (
        "docs/engineering/runbook.md",
        "template/docs/engineering/runbook.md",
    ),
    (
        ".cursor/scratchpad.md",
        "template/.cursor/scratchpad.md",
    ),
    (
        ".cursor/scratchpad.local.example.md",
        "template/.cursor/scratchpad.local.example.md",
    ),
    (
        "scripts/check_intake_template_parity.py",
        "template/scripts/check_intake_template_parity.py",
    ),
)

MODEL_TIER_OVERRIDES_PAIRS: tuple[tuple[str, str], ...] = (
    (
        ".cursor/scratchpad.md",
        "template/.cursor/scratchpad.md",
    ),
    (
        ".cursor/scratchpad.local.example.md",
        "template/.cursor/scratchpad.local.example.md",
    ),
    (
        ".cursor/model-catalog.local.example.role-based-balanced.json",
        "template/.cursor/model-catalog.local.example.role-based-balanced.json",
    ),
    (
        ".cursor/model-catalog.local.example.role-based-highend.json",
        "template/.cursor/model-catalog.local.example.role-based-highend.json",
    ),
    (
        "scripts/model_tier_lib.py",
        "template/scripts/model_tier_lib.py",
    ),
    (
        "scripts/model_tier_validate.py",
        "template/scripts/model_tier_validate.py",
    ),
    (
        "docs/engineering/runbook.md",
        "template/docs/engineering/runbook.md",
    ),
)

DOWNSTREAM_CI_GUARD_PAIRS: tuple[tuple[str, str], ...] = (
    (
        "scripts/check_downstream_ci_guard.py",
        "template/scripts/check_downstream_ci_guard.py",
    ),
    (
        "scripts/downstream_ci_guard_lib.py",
        "template/scripts/downstream_ci_guard_lib.py",
    ),
)

SOVEREIGN_ROLE_MANIFEST_PAIRS: tuple[tuple[str, str], ...] = (
    (
        ".cursor/sovereign-role-manifest.yaml",
        "template/.cursor/sovereign-role-manifest.yaml.example",
    ),
    (
        ".cursor/scratchpad.md",
        "template/.cursor/scratchpad.md",
    ),
    (
        "scripts/sovereign_role_manifest_validate.py",
        "template/scripts/sovereign_role_manifest_validate.py",
    ),
    (
        "scripts/sovereign_role_manifest_lib.py",
        "template/scripts/sovereign_role_manifest_lib.py",
    ),
    (
        "docs/engineering/runbook.md",
        "template/docs/engineering/runbook.md",
    ),
    (
        "docs/engineering/reason_codes.md",
        "template/docs/engineering/reason_codes.md",
    ),
    (
        "handoffs/sovereign_role_reviews.jsonl",
        "template/handoffs/sovereign_role_reviews.jsonl",
    ),
)

SOVEREIGN_PARALLEL_DEV_PAIRS: tuple[tuple[str, str], ...] = (
    (
        ".cursor/scratchpad.md",
        "template/.cursor/scratchpad.md",
    ),
    (
        "scripts/parallel_dev_arbiter.py",
        "template/scripts/parallel_dev_arbiter.py",
    ),
    (
        "tests/us0108_contract_test.py",
        "template/tests/us0108_contract_test.py",
    ),
    (
        "docs/engineering/runbook.md",
        "template/docs/engineering/runbook.md",
    ),
    (
        "docs/engineering/reason_codes.md",
        "template/docs/engineering/reason_codes.md",
    ),
    (
        "scripts/check_intake_template_parity.py",
        "template/scripts/check_intake_template_parity.py",
    ),
)

SOVEREIGN_SELF_HEALING_DEPLOY_PAIRS: tuple[tuple[str, str], ...] = (
    (
        ".cursor/scratchpad.md",
        "template/.cursor/scratchpad.md",
    ),
    (
        "scripts/self_healing_deploy_lib.py",
        "template/scripts/self_healing_deploy_lib.py",
    ),
    (
        "scripts/self_healing_deploy_validate.py",
        "template/scripts/self_healing_deploy_validate.py",
    ),
    (
        "tests/us0109_contract_test.py",
        "template/tests/us0109_contract_test.py",
    ),
    (
        "docs/engineering/runbook.md",
        "template/docs/engineering/runbook.md",
    ),
    (
        "docs/engineering/reason_codes.md",
        "template/docs/engineering/reason_codes.md",
    ),
)

# US-0111 release trigger adapter parity pairs
RELEASE_TRIGGER_ADAPTER_PAIRS: tuple[tuple[str, str], ...] = (
    (
        "scripts/release_trigger_adapters.py",
        "template/scripts/release_trigger_adapters.py",
    ),
    (
        "tests/us0111_contract_test.py",
        "template/tests/us0111_contract_test.py",
    ),
    (
        "docs/engineering/runbook.md",
        "template/docs/engineering/runbook.md",
    ),
    (
        "docs/engineering/reason_codes.md",
        "template/docs/engineering/reason_codes.md",
    ),
    (
        "scripts/check_intake_template_parity.py",
        "template/scripts/check_intake_template_parity.py",
    ),
)

# DEC-0118 §6 / US-0118 — Work-kind routing surface pairs. Contents must
# be byte-identical between active and template paths; installer delivers
# template copies (BUG-0003 / DEC-0066). 6 surface pairs per R-0106 Q6
# LOCKED. Note: scratchpad key parity is structural (key presence) via
# BUG-0013 test, NOT byte-parity (active scratchpad carries project-local
# overrides like DELIVERY_MODE=ultra_lean that must not leak to template).
WORK_KIND_ROUTING_PAIRS: tuple[tuple[str, str], ...] = (
    (
        "scripts/work_kind_classify_lib.py",
        "template/scripts/work_kind_classify_lib.py",
    ),
    (
        "scripts/work_kind_routing_lib.py",
        "template/scripts/work_kind_routing_lib.py",
    ),
    (
        "tests/us0118_contract_test.py",
        "template/tests/us0118_contract_test.py",
    ),
    (".cursor/commands/auto.md", "template/.cursor/commands/auto.md"),
    (".cursor/commands/intake.md", "template/.cursor/commands/intake.md"),
    (
        "docs/engineering/runbook.md",
        "template/docs/engineering/runbook.md",
    ),
    (
        "docs/engineering/context/installer-owned-paths.manifest",
        "template/docs/engineering/context/installer-owned-paths.manifest",
    ),
    (
        "scripts/check_intake_template_parity.py",
        "template/scripts/check_intake_template_parity.py",
    ),
)

# DEC-0119 §6 / US-0119 — Autonomous-autonomy preset surfaces. Contents must
# be byte-identical between active and template paths. 8 surface pairs.
AUTONOMY_PRESET_PAIRS: tuple[tuple[str, str], ...] = (
    ("scripts/autonomy_preset_lib.py", "template/scripts/autonomy_preset_lib.py"),
    ("scripts/validate_autonomy_stop_matrix.py", "template/scripts/validate_autonomy_stop_matrix.py"),
    ("docs/engineering/autonomy-stop-matrix.md", "template/docs/engineering/autonomy-stop-matrix.md"),
    ("docs/engineering/context/installer-owned-paths.manifest", "template/docs/engineering/context/installer-owned-paths.manifest"),
    ("docs/engineering/runbook.md", "template/docs/engineering/runbook.md"),
    (".cursor/commands/auto.md", "template/.cursor/commands/auto.md"),
    ("tests/us0119_autonomy_preset_test.py", "template/tests/us0119_autonomy_preset_test.py"),
)

SCOPES: dict[str, tuple[tuple[str, str], ...]] = {
    "intake": INTAKE_TEMPLATE_PAIRS,
    "caveman-compress": CAVEMAN_COMPRESS_PAIRS,
    "readme-feature-coverage": README_FEATURE_COVERAGE_PAIRS,
    "downstream-ci-guard": DOWNSTREAM_CI_GUARD_PAIRS,
    "us-0092": US0092_PAIRS,
    "us-0093": US0093_PAIRS,
    "us-0095": US0095_PAIRS,
    "bug-0012": BUG0012_PAIRS,
    "us-0096": US0096_PAIRS,
    "project-readme": PROJECT_README_PAIRS,
    "dev-environment": DEV_ENVIRONMENT_PAIRS,
    "release-changelog": RELEASE_CHANGELOG_PAIRS,
    "model-tier": MODEL_TIER_PAIRS,
    "model-tier-overrides": MODEL_TIER_OVERRIDES_PAIRS,
    "sovereign-role-manifest": SOVEREIGN_ROLE_MANIFEST_PAIRS,
    "sovereign-parallel-dev": SOVEREIGN_PARALLEL_DEV_PAIRS,
    "sovereign-self-healing-deploy": SOVEREIGN_SELF_HEALING_DEPLOY_PAIRS,
    "release-trigger-adapter": RELEASE_TRIGGER_ADAPTER_PAIRS,
    "work-kind-routing": WORK_KIND_ROUTING_PAIRS,
    "us-0119": AUTONOMY_PRESET_PAIRS,
    "all": (
        INTAKE_TEMPLATE_PAIRS
        + CAVEMAN_COMPRESS_PAIRS
        + README_FEATURE_COVERAGE_PAIRS
        + DOWNSTREAM_CI_GUARD_PAIRS
        + US0092_PAIRS
        + US0093_PAIRS
        + US0095_PAIRS
        + BUG0012_PAIRS
        + US0096_PAIRS
        + PROJECT_README_PAIRS
        + DEV_ENVIRONMENT_PAIRS
        + RELEASE_CHANGELOG_PAIRS
        + MODEL_TIER_PAIRS
        + MODEL_TIER_OVERRIDES_PAIRS
        + SOVEREIGN_ROLE_MANIFEST_PAIRS
        + SOVEREIGN_SELF_HEALING_DEPLOY_PAIRS
        + RELEASE_TRIGGER_ADAPTER_PAIRS
        + WORK_KIND_ROUTING_PAIRS
        + AUTONOMY_PRESET_PAIRS
    ),
}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--repo",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Repository root",
    )
    p.add_argument(
        "--scope",
        choices=sorted(SCOPES.keys()),
        default="intake",
        help="Parity pair table to verify.",
    )
    args = p.parse_args()
    root: Path = args.repo
    pairs = SCOPES[args.scope]
    failed = False
    for rel_active, rel_tpl in pairs:
        a = root / rel_active
        t = root / rel_tpl
        if not a.is_file() or not t.is_file():
            print(f"[INTAKE_TEMPLATE_PARITY_ERROR] missing file: {rel_active} or {rel_tpl}")
            failed = True
            continue
        ba = a.read_bytes()
        bt = t.read_bytes()
        if ba != bt:
            print(
                f"[INTAKE_TEMPLATE_PARITY_ERROR] mismatch: {rel_active} ({len(ba)}b) "
                f"!= {rel_tpl} ({len(bt)}b)"
            )
            failed = True
    if failed:
        return 2
    print(f"[INTAKE_TEMPLATE_PARITY_OK] scope={args.scope}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
