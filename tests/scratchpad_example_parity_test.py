"""
BUG-0013 regression tests: Scratchpad example parity.

Ensures template/.cursor/scratchpad.local.example.md stays in sync with
canonical .cursor/scratchpad.md (canonical keys ⊆ template example keys),
while preserving the example-only header (L1-L5) and excluding
project-local flag overrides.
"""

import re
from pathlib import Path

import pytest

CANONICAL_PATH = Path(__file__).parent.parent / ".cursor" / "scratchpad.md"
TEMPLATE_PATH = (
    Path(__file__).parent.parent
    / "template"
    / ".cursor"
    / "scratchpad.local.example.md"
)
ACTIVE_EXAMPLE_PATH = (
    Path(__file__).parent.parent
    / ".cursor"
    / "scratchpad.local.example.md"
)


# -- helpers ------------------------------------------------------------------

def extract_keys(text):
    """Extract framework key-value pairs from scratchpad text.

    Parses both bare KEY=VALUE lines and commented-out # KEY=VALUE examples.
    Only returns the KEY name (strips the value to keep comparisons structural).
    """
    pattern = re.compile(r"^(?:#\s*)?([A-Z_][A-Z0-9_]*)=", re.MULTILINE)
    return set(pattern.findall(text))


def extract_sections(text):
    """Extract top-level section headers (lines starting with ## or #) from text."""
    pattern = re.compile(r"^#+\s+(.+)$", re.MULTILINE)
    return {m.strip() for m in pattern.findall(text)}


# -- parity check ------------------------------------------------------------

def test_bug0013_parity_check():
    """AC-1: template example contains all canonical sections (keys match 1:1 structurally)."""
    canonical_text = CANONICAL_PATH.read_text(encoding="utf-8")
    template_text = TEMPLATE_PATH.read_text(encoding="utf-8")

    canonical_keys = extract_keys(canonical_text)
    template_keys = extract_keys(template_text)

    # Allow template to have additional framework keys (e.g., commented examples)
    # but NOT the other way around
    missing_in_template = canonical_keys - template_keys

    assert not missing_in_template, (
        f"BUG-0013: template example missing {len(missing_in_template)} canonical key(s):\n"
        + "\n".join(f"  - {k}" for k in sorted(missing_in_template))
        + "\nSync from .cursor/scratchpad.md (canonical)."
    )


# -- header preserved ---------------------------------------------------------

def test_bug0013_header_preserved():
    """AC-1: example-only header comment in L1-L5 is intact after sync."""
    template_text = TEMPLATE_PATH.read_text(encoding="utf-8")
    lines = template_text.splitlines()[:5]

    expected_patterns = [
        r"its-magic|DEC-",      # L1: "its-magic" and/or DEC reference
        r"^\s*#.*$",            # L2: comment line (can be just "#")
        r"local.*gitignore",    # L3: "local" and "gitignore"
        r"materialize|baseline",# L4: materialize or baseline
        r"template",            # L5: template reference
    ]

    for idx, pattern in enumerate(expected_patterns, start=1):
        assert re.search(pattern, lines[idx - 1], re.IGNORECASE), (
            f"BUG-0013: Header line {idx} missing expected pattern '{pattern}'.\n"
            f"Line content: {lines[idx - 1]}"
        )


# -- local overrides excluded -------------------------------------------------

def test_bug0013_local_overrides_preserved():
    """AC-1: no project-local override values leaked into template example."""
    template_text = TEMPLATE_PATH.read_text(encoding="utf-8")

    # Project-local overrides: concrete values that MUST NOT appear in template.
    # Pattern: KEY=<project-specific-value> where value is non-empty AND is a
    # personal/project-specific setting (not a default/example).
    #
    # Allowed in template (framework defaults):
    #   MODEL_CATALOG=.cursor/model-catalog.local.json   (example path)
    #   MODEL_RESOLVE=alias_only                          (example)
    #   MODEL_FALLBACK=inherit                            (example)
    #   DEV_SERVER_COMMAND=                               (empty = unset)
    #
    # Forbidden in template (project-local overrides):
    #   DEV_SERVER_COMMAND=npm start                      (concrete command)
    #   DEV_SERVER_PORT=30000                             (concrete port)
    #   AUTO_PUSH_BRANCH_ALLOWLIST=main,develop           (concrete branch list)
    #   CAVEMAN_LEVEL=full                                (concrete flavor)
    #   FRAMEWORK_KIT_REPO=1                              (project-specific flag)
    #   TOKEN_PROFILE=lean                                (personal preference)

    forbidden_concrete_overrides = [
        # Concrete dev server settings
        r"^DEV_SERVER_COMMAND=\S+",      # non-empty concrete command
        r"^DEV_SERVER_PORT=\d+",         # concrete port number
        # Concrete branch allowlist (with at least 2 entries)
        r"^AUTO_PUSH_BRANCH_ALLOWLIST=\w+,\w+",
        # Concrete Caveman flavor
        r"^CAVEMAN_LEVEL=\w+",
        # Project-specific flags
        r"^FRAMEWORK_KIT_REPO=1",
        # Personal token profile (lean is a choice, balanced is default)
        r"^TOKEN_PROFILE=lean",
    ]

    violations = []
    for pattern in forbidden_concrete_overrides:
        if re.search(pattern, template_text, re.MULTILINE):
            match = re.search(pattern, template_text, re.MULTILINE)
            violations.append(f"  - Pattern '{pattern}' matched: '{match.group(0)}'")

    assert not violations, (
        "BUG-0013: Template example contains project-local overrides that\n"
        "should only appear in consumer's .cursor/scratchpad.local.md:\n"
        + "\n".join(violations)
    )


# -- active example mirror check ----------------------------------------------

def test_bug0013_active_example_mirror_in_sync():
    """AC-1: .cursor/scratchpad.local.example.md (active mirror) matches template."""
    if not ACTIVE_EXAMPLE_PATH.exists():
        pytest.skip("Active example mirror not present in this repo.")

    template_text = TEMPLATE_PATH.read_text(encoding="utf-8")
    active_text = ACTIVE_EXAMPLE_PATH.read_text(encoding="utf-8")

    # Strip header (first 5 lines) before comparing, since active mirror may differ
    template_body = "\n".join(template_text.splitlines()[5:])
    active_body = "\n".join(active_text.splitlines()[5:])

    assert template_body == active_body, (
        "BUG-0013: Active mirror .cursor/scratchpad.local.example.md body (from L6)\n"
        "does not match template/.cursor/scratchpad.local.example.md body.\n"
        "Re-sync from template."
    )
