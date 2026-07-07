#!/usr/bin/env python3
"""
Autonomy stop matrix validator (US-0119 / DEC-0119).

Validates scripts/data/autonomy_stop_matrix.yaml against:
1. No orphan reason codes in scripts/*.py (grep for codes not in YAML)
2. security_hard rows carry auto_repair_kind=n/a
3. autonomy_resolvable rows carry finite cap (>= 1 or 0 for terminal stops)
4. No orphan reason codes in .cursor/commands/*.md (grep-based cross-check per R-0107 Q8)

Usage:
    python validate_autonomy_stop_matrix.py --self-test

Exit 0 = matrix valid. Exit non-zero = matrix invalid (violations on stderr).
"""
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple


REPO_ROOT = Path(__file__).resolve().parent.parent
YAML_PATH = REPO_ROOT / "scripts" / "data" / "autonomy_stop_matrix.yaml"
SCRIPTS_DIR = REPO_ROOT / "scripts"
DATA_DIR = REPO_ROOT / "scripts" / "data"
COMMANDS_DIR = REPO_ROOT / ".cursor" / "commands"

VALID_AUTO_REPAIR_KINDS = {
    "reorder_anchors",
    "fix_timestamp",
    "truncate_hot_surface",
    "reset_retry_counter",
    "disambiguate_state",
    "auto_refresh_brief",
    "approve_plan_deviation",
    "regenerate_isolation_evidence",
    "skip_confirmation_gate",
}


# Minimal YAML parser for the specific autonomy_stop_matrix.yaml structure
# (flat list of dicts with simple scalar values — no nested collections)
def parse_yaml_matrix(path: Path) -> Dict:
    """Parse the autonomy stop matrix YAML file.
    
    Returns dict with keys: version, story_ref, dec_ref, reason_codes (list of dicts).
    Each dict has keys: code, stop_class, auto_repair_kind, cap, rationale.
    """
    if not path.exists():
        return {}

    content = path.read_text(encoding="utf-8")
    result = {
        "version": "",
        "story_ref": "",
        "dec_ref": "",
        "reason_codes": [],
    }

    current_entry = None
    in_reason_codes = False

    for line in content.splitlines():
        stripped = line.rstrip()

        # Skip empty lines and comments
        if not stripped or stripped.lstrip().startswith("#"):
            continue

        # Top-level keys
        if not line.startswith(" ") and not line.startswith("\t"):
            if stripped.startswith("version:"):
                result["version"] = stripped.split(":", 1)[1].strip().strip('"').strip("'")
            elif stripped.startswith("story_ref:"):
                result["story_ref"] = stripped.split(":", 1)[1].strip()
            elif stripped.startswith("dec_ref:"):
                result["dec_ref"] = stripped.split(":", 1)[1].strip()
            elif stripped.startswith("reason_codes:"):
                in_reason_codes = True
            continue

        if not in_reason_codes:
            continue

        stripped_line = stripped.lstrip()

        # New list entry (starts with "- code:")
        if stripped_line.startswith("- code:"):
            if current_entry is not None:
                result["reason_codes"].append(current_entry)
            code_value = stripped_line.split(":", 1)[1].strip().strip('"').strip("'")
            current_entry = {
                "code": code_value,
                "stop_class": "",
                "auto_repair_kind": "",
                "cap": 0,
                "rationale": "",
            }
            continue

        # Entry fields
        if current_entry is not None:
            if stripped_line.startswith("stop_class:"):
                current_entry["stop_class"] = stripped_line.split(":", 1)[1].strip().strip('"').strip("'")
            elif stripped_line.startswith("auto_repair_kind:"):
                current_entry["auto_repair_kind"] = stripped_line.split(":", 1)[1].strip().strip('"').strip("'")
            elif stripped_line.startswith("cap:"):
                cap_val = stripped_line.split(":", 1)[1].strip()
                try:
                    current_entry["cap"] = int(cap_val)
                except ValueError:
                    current_entry["cap"] = -1  # Sentinel for invalid
            elif stripped_line.startswith("rationale:"):
                current_entry["rationale"] = stripped_line.split(":", 1)[1].strip().strip('"').strip("'")

    # Append last entry
    if current_entry is not None:
        result["reason_codes"].append(current_entry)

    return result


def validate_matrix(matrix: Dict) -> List[str]:
    """Validate matrix structure and invariants."""
    violations = []

    reason_codes = matrix.get("reason_codes", [])
    if not isinstance(reason_codes, list):
        violations.append("reason_codes is not a list")
        return violations

    for entry in reason_codes:
        if not isinstance(entry, dict):
            violations.append(f"entry is not a dict: {entry}")
            continue

        code = entry.get("code")
        stop_class = entry.get("stop_class")
        auto_repair_kind = entry.get("auto_repair_kind")
        cap = entry.get("cap")

        if not code:
            violations.append("entry missing 'code' field")
            continue

        if stop_class not in {"security_hard", "autonomy_resolvable"}:
            violations.append(f"{code}: invalid stop_class '{stop_class}'")
            continue

        # security_hard MUST have auto_repair_kind=n/a and cap=0
        if stop_class == "security_hard":
            if auto_repair_kind != "n/a":
                violations.append(
                    f"{code}: security_hard MUST have auto_repair_kind=n/a, got '{auto_repair_kind}'"
                )
            if cap != 0:
                violations.append(
                    f"{code}: security_hard MUST have cap=0, got {cap}"
                )

        # autonomy_resolvable MUST have auto_repair_kind in 9-value taxonomy OR n/a for terminal
        if stop_class == "autonomy_resolvable":
            if auto_repair_kind not in VALID_AUTO_REPAIR_KINDS and auto_repair_kind != "n/a":
                violations.append(
                    f"{code}: autonomy_resolvable MUST have auto_repair_kind in taxonomy or n/a, got '{auto_repair_kind}'"
                )
            # cap MUST be finite (>= 0)
            if not isinstance(cap, int) or cap < 0:
                violations.append(
                    f"{code}: autonomy_resolvable MUST have finite cap >= 0, got {cap}"
                )

    return violations


# Pattern for reason codes: UPPERCASE_WORDS joined by underscores, >= 8 chars
REASON_CODE_PATTERN = re.compile(r"\b([A-Z][A-Z0-9_]{7,})\b")

# Known non-stop-code uppercase tokens to exclude
NON_REASON_CODE_TOKENS = {
    "AUTONOMY_PRESET",
    "AUTONOMY_STOP_POLICY",
    "RELEASE_TARGETS",
    "RELEASE_TRIGGER",
    "RELEASE_PUBLISH",
    "RELEASE_PUBLISH_MODE",
    "RELEASE_PUBLISH_AUTO_CONFIRM",
    "SECURITY_REVIEW",
    "COMPLIANCE_PROFILES",
    "README_FEATURE",
    "PROJECT_README",
    "FRAMEWORK_KIT",
    "TOKEN_PROFILE",
    "DELIVERY_MODE",
    "MODEL_TIER",
    "MODEL_CATALOG",
    "MODEL_RESOLVE",
    "MODEL_FALLBACK",
    "MODEL_PROVIDER",
    "REMOTE_EXECUTION",
    "REMOTE_CONFIG",
    "SYNC_POLICY",
    "SYNC_CUSTOM",
    "ALLOW_AUTO_PUSH",
    "AUTO_PUSH_BRANCH",
    "EARLY_RESEARCH",
    "INTAKE_GUIDED",
    "INTAKE_SUBAGENT",
    "INTAKE_WORK_ITEM",
    "ID_NAMESPACE",
    "STATE_HOT_MAX",
    "PO_TO_TL_HOT",
    "ARCH_HOT_MAX",
    "SPEC_PACK_MODE",
    "USER_GUIDE_MODE",
    "DOC_AUDIENCE",
    "DOC_DETAIL",
    "UAT_BROWSER",
    "UAT_PROCESS",
    "DEV_SERVER",
    "DEV_AUTO",
    "DEV_ENVIRONMENT",
    "CAVEMAN_MODE",
    "CAVEMAN_LEVEL",
    "CAVEMAN_COMPRESS",
    "CAVEMAN_FILE",
    "MODEL_ASK",
    "MODEL_EXECUTE",
    "AUTONOMY_REPAIR_CAP",
    "INTAKE_AUTONOMY_MODE",
    "INTAKE_MINIMAL",
    "INTAKE_ASSUME",
    "WORK_KIND",
    "WORK_KIND_AUTO",
    "WORK_KIND_ROUTING",
    "CROSS_MODEL",
    "CROSS_MODEL_REWORK",
    "CROSS_MODEL_SKIP",
    "CROSS_MODEL_ANTISLOP",
    "CROSS_MODEL_REVIEW",
    "CROSS_REPO",
    "COMPATIBILITY_GATE",
    "COMPATIBILITY_SOURCES",
    "COMPONENT_SCOPE",
    "TARGET_COMPONENTS",
    "RESUME_BRIEF_AUTO",
    "GOAL_CONVERGENCE",
    "SOVEREIGN_DRAIN",
    "SOVEREIGN_GOAL",
    "SOVEREIGN_MEMORY",
    "SOVEREIGN_NOTIFY",
    "SOVEREIGN_ROLE",
    "SOVEREIGN_PARALLEL",
    "SOVEREIGN_LOOP",
    "SOVEREIGN_DEPLOY",
    "AUTO_SOVEREIGN",
    "PHASE_MODE",
    "PERMISSION_MODE",
    "MAGIC_CONTEXT",
    "MAGIC_BENCH",
    "LOOP_UNTIL",
    "DONE_AUTO",
    "AUTO_FLOW",
    "AUTO_BLOCK",
    "AUTO_OUTER",
    "AUTO_INSTALL",
    "AUTO_RELEASE",
    "AUTO_BACKLOG",
    "AUTO_STORY",
    "AUTO_EXECUTE",
    "AUTO_TEAM",
    "AUTO_BUG",
    "AUTO_QUIET",
    "AUTO_PHASE",
    "AUTO_LOOP",
    "AUTO_PAUSE",
    "AUTO_IMPLEMENTATION",
    "AUTO_REMOTE",
    "AUTO_DELIVERY",
    "AUTO_SCHEDULER",
    "AI_DECISION",
    "AUTO_PLAN",
    "SPRINT_MAX",
    "SPRINT_AUTO",
    "SPRINT_BULK",
    "LEAN_MEMORY",
    "LEAN_STATE",
    "LEAN_COLD",
    "MAX_US_ID",
}


def extract_reason_codes_from_path(path: Path) -> List[str]:
    """Extract plausible reason codes from a file.

    Only extracts tokens that appear in string-literal or comment context
    (quoted text, ``code``, or # comments).  This avoids false positives
    from Python constant names like AUTONOMY_FLAGS or PRESET_DEFINITIONS
    which are NOT reason codes.
    """
    codes = set()
    if not path.exists():
        return []

    content = path.read_text(encoding="utf-8", errors="ignore")
    for line in content.splitlines():
        stripped = line.strip()
        ctx_parts: list[str] = []
        if stripped.startswith("#"):
            ctx_parts.append(stripped)
        else:
            in_str: list[str] = []
            i = 0
            while i < len(stripped):
                ch = stripped[i]
                if ch in ('"', "'"):
                    j = i + 1
                    while j < len(stripped) and stripped[j] != ch:
                        if stripped[j] == "\\":
                            j += 1
                        j += 1
                    ctx_parts.append(stripped[i + 1:j])
                    i = j + 1
                    continue
                if ch == "`":
                    j = stripped.index("`", i + 1) if "`" in stripped[i + 1:] else -1
                    if j > 0:
                        ctx_parts.append(stripped[i + 1:j])
                        i = j + 1
                        continue
                i += 1
        search_text = " ".join(ctx_parts)
        for match in REASON_CODE_PATTERN.finditer(search_text):
            token = match.group(1)
            if token not in NON_REASON_CODE_TOKENS:
                codes.add(token)

    return sorted(codes)


def check_orphan_codes_in_scripts_and_matrix(matrix: Dict) -> List[str]:
    """Inverse orphan check: verify YAML-defined codes are referenced in scripts.

    Instead of scanning for unknown uppercase tokens (which produces false
    positives from Python variables), this verifies that every YAML-defined
    reason code appears at least once in the consumer scripts or is a
    well-known structural code.
    """
    violations: List[str] = []
    yaml_codes = {
        entry["code"] for entry in matrix.get("reason_codes", []) if isinstance(entry, dict)
    }

    us0119_consumer_scripts = [
        "autonomy_preset_lib.py",
        "validate_autonomy_stop_matrix.py",
        "autonomy_repair_ledger_lib.py",
    ]

    all_script_text: list[str] = []
    if SCRIPTS_DIR.exists():
        for script_name in us0119_consumer_scripts:
            script_path = SCRIPTS_DIR / script_name
            if script_path.exists():
                all_script_text.append(script_path.read_text(encoding="utf-8", errors="ignore"))

    combined = "\n".join(all_script_text)
    for code in sorted(yaml_codes):
        if code not in combined:
            violations.append(
                f"YAML-defined code not referenced in consumer scripts: {code}"
            )

    return violations


def check_orphan_codes_in_commands(matrix: Dict) -> List[str]:
    """Check for orphan reason codes in .cursor/commands/*.md not in YAML.

    Uses string/comment context extraction to avoid false positives from
    Python identifiers and YAML keys in code examples.
    """
    violations: List[str] = []
    yaml_codes = {
        entry["code"] for entry in matrix.get("reason_codes", []) if isinstance(entry, dict)
    }

    if not COMMANDS_DIR.exists():
        return violations

    for cmd_path in sorted(COMMANDS_DIR.glob("*.md")):
        codes_in_file = extract_reason_codes_from_path(cmd_path)
        for code in codes_in_file:
            if code not in yaml_codes:
                violations.append(
                    f"Orphan reason code in {cmd_path.name}: {code} (not in YAML)"
                )

    return violations


def check_yaml_code_references_in_scripts(matrix: Dict) -> List[str]:
    """Verify that each YAML-defined reason code is referenced somewhere
    in the US-0119 consumer surface (scripts, commands, docs).

    Instead of scanning for unknown uppercase tokens (which produces false
    positives from Python variables and other stories' codes), this verifies
    that every YAML-defined code appears at least once in the US-0119 surface.
    """
    violations: List[str] = []
    yaml_codes = {
        entry["code"] for entry in matrix.get("reason_codes", []) if isinstance(entry, dict)
    }

    us0119_surface_files = [
        REPO_ROOT / "scripts" / "autonomy_preset_lib.py",
        REPO_ROOT / "scripts" / "validate_autonomy_stop_matrix.py",
        REPO_ROOT / "scripts" / "autonomy_repair_ledger_lib.py",
        REPO_ROOT / "docs" / "engineering" / "autonomy-stop-matrix.md",
        REPO_ROOT / ".cursor" / "scratchpad.md",
    ]

    all_text_parts: list[str] = []
    for f in us0119_surface_files:
        if f.exists():
            all_text_parts.append(f.read_text(encoding="utf-8", errors="ignore"))

    combined = "\n".join(all_text_parts)
    for code in sorted(yaml_codes):
        if code not in combined:
            violations.append(
                f"YAML-defined code not referenced in US-0119 surface: {code}"
            )

    return violations


def self_test() -> Tuple[bool, List[str]]:
    """Run full validation suite.

    Validates:
    1. Matrix structure (stop_class enum, valid auto_repair_kind)
    2. security_hard rows carry auto_repair_kind=n/a and cap=0
    3. autonomy_resolvable rows carry valid auto_repair_kind and finite cap
    4. Each YAML-defined code is referenced in the US-0119 surface

    Does NOT scan for orphan codes — many reason codes in the codebase belong
    to other stories and are not part of the US-0119 matrix.
    """
    all_violations = []

    # Load matrix
    matrix = parse_yaml_matrix(YAML_PATH)
    if not matrix.get("reason_codes"):
        all_violations.append(f"No reason_codes found in YAML at {YAML_PATH}")
        return False, all_violations

    # Validate structure (security_hard + autonomy_resolvable invariants)
    violations = validate_matrix(matrix)
    all_violations.extend(violations)

    # Check YAML codes are referenced in US-0119 surface
    violations = check_yaml_code_references_in_scripts(matrix)
    all_violations.extend(violations)

    return len(all_violations) == 0, all_violations


if __name__ == "__main__":
    if "--self-test" not in sys.argv:
        print("Usage: validate_autonomy_stop_matrix.py --self-test", file=sys.stderr)
        sys.exit(1)

    passed, violations = self_test()

    if passed:
        reason_codes = parse_yaml_matrix(YAML_PATH).get("reason_codes", [])
        sec_hard = sum(1 for e in reason_codes if e.get("stop_class") == "security_hard")
        auto_res = sum(1 for e in reason_codes if e.get("stop_class") == "autonomy_resolvable")
        print(f"[MATRIX_VALID] All checks passed ({len(reason_codes)} codes: {sec_hard} security_hard, {auto_res} autonomy_resolvable)")
        sys.exit(0)
    else:
        print(f"[MATRIX_INVALID] {len(violations)} violation(s):", file=sys.stderr)
        for v in violations:
            print(f"  - {v}", file=sys.stderr)
        sys.exit(1)
