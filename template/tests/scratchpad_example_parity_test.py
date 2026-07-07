"""
BUG-0013: Scratchpad example parity tests.

Verifies template/.cursor/scratchpad.local.example.md stays in sync
with canonical .cursor/scratchpad.md, excluding project-local overrides.
"""

import re
from pathlib import Path

import pytest

CANONICAL = Path(__file__).parent.parent / ".cursor" / "scratchpad.md"
TEMPLATE = (
    Path(__file__).parent.parent
    / "template"
    / ".cursor"
    / "scratchpad.local.example.md"
)


def extract_keys(text):
    """Extract KEY=value keys from scratchpad text."""
    pattern = re.compile(r"^([A-Z_][A-Z0-9_]*)=", re.MULTILINE)
    return set(pattern.findall(text))


def extract_sections(text):
    """Extract # Section headers from scratchpad text."""
    pattern = re.compile(r"^(#+\s+.+)$", re.MULTILINE)
    return [m.strip() for m in pattern.findall(text)]


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def canonical_text():
    return CANONICAL.read_text(encoding="utf-8")


@pytest.fixture
def template_text():
    return TEMPLATE.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Test markers
# ---------------------------------------------------------------------------

def test_bug0013_parity_check(canonical_text, template_text):
    """AC-1: All canonical sections keys present in template example."""
    # 1) Section headers should be present
    canonical_sections = extract_sections(canonical_text)
    template_sections = extract_sections(template_text)
    missing_sections = set(canonical_sections) - set(template_sections)

    # 2) Keys (canonical keys ⊆ template example keys)
    canonical_keys = extract_keys(canonical_text)
    template_keys = extract_keys(template_text)
    missing_keys = canonical_keys - template_keys

    msg = []
    if missing_sections:
        msg.append(
            f"Template missing {len(missing_sections)} canonical section(s):\n"
            + "\n".join(f"  - {s}" for s in sorted(missing_sections))
        )
    if missing_keys:
        msg.append(
            f"Template missing {len(missing_keys)} canonical key(s):\n"
            + "\n".join(f"  - {k}" for k in sorted(missing_keys))
        )

    assert not msg, "\n".join(msg)


def test_bug0013_header_preserved(template_text):
    """AC-1: Example-only header comment (L1-L5) preserved intact."""
    lines = template_text.splitlines()[:5]

    expected_patterns = [
        r"^#",            # L1: comment line
        r"its-magic",     # L2: contains "its-magic"
        r"DEC-",          # L3: contains DEC reference
        r"Copy this file",# L4: contains copy instruction
        r"local>",        # L5: contains "local>" reference
    ]
    assert len(lines) >= 5, (
        f"Template header must have at least 5 lines; only {len(lines)} found"
    )

    for idx, pattern in enumerate(expected_patterns, start=1):
        assert pattern in lines[idx - 1] or re.match(pattern, lines[idx - 1]), (
            f"Header line {idx} missing expected pattern '{pattern}'.\n"
            f"Found: {lines[idx - 1]}"
        )


def test_bug0013_local_overrides_preserved(template_text):
    """AC-1: Project-local overrides NOT leaked into template example."""
    # Patterns indicating project-local overrides that should NOT be in template
    forbidden = [
        r"^MODEL_[A-Z]+=",   # Direct per-phase model overrides (e.g., MODEL_EXECUTE=...)
        r"^#MODEL_",          # Commented per-phase slug overrides
        r"^#MODEL_RESOLVE=local_catalog",  # Local catalog override (commented)
        r"^#MODEL_RESOLVE=role_catalog",   # Role catalog override (commented)
    ]

    violations = []
    for pattern in forbidden:
        matches = re.findall(pattern, template_text, re.MULTILINE)
        if matches:
            violations.append((pattern, matches[:3]))  # up to 3 examples

    assert not violations, (
        f"Template contains {len(violations)} project-local override pattern(s) "
        "that should NOT be present:\n"
        + "\n".join(
            f"  - {pat} (examples: {ex})" for pat, ex in violations
        )
        + "\nProject-local overrides belong in consumer's .cursor/scratchpad.local.md"
    )
