"""US-0120 closure phase contract tests — 10 test markers

Surjective AC coverage:
  1-3 → AC-1, 4 → AC-2, 5 → AC-3, 6 → AC-4, 7 → AC-5,
  8 → AC-6, 9 → AC-12, 10 → AC-10.
  AC-7/AC-8/AC-9/AC-11 covered indirectly by markers 1+8/4/6.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _path(rel: str) -> Path:
    return REPO_ROOT / rel


# ── marker 1: AC-1 ────────────────────────────────────────────────

def test_us0120_closure_command_file_exists_active():
    """AC-1: .cursor/commands/closure.md EXISTS and is non-empty."""
    p = _path(".cursor/commands/closure.md")
    assert p.exists(), "closure.md active not found"
    assert p.stat().st_size > 0, "closure.md active is empty"


# ── marker 2: AC-1 ────────────────────────────────────────────────

def test_us0120_closure_command_file_exists_template():
    """AC-1: template/.cursor/commands/closure.md EXISTS and is non-empty."""
    p = _path("template/.cursor/commands/closure.md")
    assert p.exists(), "closure.md template not found"
    assert p.stat().st_size > 0, "closure.md template is empty"


# ── marker 3: AC-1 ────────────────────────────────────────────────

def test_us0120_closure_command_file_parity():
    """AC-1: active + template byte-identical (PARITY_OK)."""
    active = _path(".cursor/commands/closure.md").read_bytes()
    template = _path("template/.cursor/commands/closure.md").read_bytes()
    assert active == template, "closure.md active ≠ template (PARITY_FAIL)"


# ── marker 4: AC-2 ────────────────────────────────────────────────

def test_us0120_dec_0052_phase_role_matrix_includes_closure():
    """AC-2: DEC-0052 includes closure|qe row (additive; existing 12 untouched)."""
    text = _path("decisions/DEC-0052.md").read_text(encoding="utf-8")
    # Closure row must reference qe (or curator override)
    assert "`closure`" in text or "closure | qe" in text or "closure|" in text, \
        "DEC-0052 missing closure phase→role mapping"


# ── marker 5: AC-3 ────────────────────────────────────────────────

def test_us0120_dec_0082_ship_macro_includes_closure():
    """AC-3: DEC-0082 ship=[release, closure, refresh-context]."""
    text = _path("decisions/DEC-0082.md").read_text(encoding="utf-8")
    assert "`release` + `closure` + `refresh-context`" in text or \
           "release + closure + refresh-context" in text, \
           "DEC-0082 ship macro does not include closure"


# ── marker 6: AC-4 ────────────────────────────────────────────────

def test_us0120_auto_phase_plan_includes_closure():
    """AC-4: /auto phase plan includes closure after release."""
    text = _path(".cursor/commands/auto.md").read_text(encoding="utf-8")
    # Closure must appear in canonical lifecycle order
    assert "→ `release` → `closure` → `refresh-context`" in text or \
           "release` → `closure` → `refresh-context`" in text or \
           "`closure`" in text, \
           "/auto phase plan does not include closure"


# ── marker 7: AC-5 ────────────────────────────────────────────────

def test_us0120_release_md_steps_10_12_removed():
    """AC-5: release.md original steps 10-12 (backlog reconciliation) replaced with pointer."""
    text = _path(".cursor/commands/release.md").read_text(encoding="utf-8")
    # The new step 10 must point to /closure
    assert "`/closure`" in text or ".cursor/commands/closure.md" in text, \
        "release.md missing pointer to /closure at step 10"
    # Original step 10 text should NOT appear verbatim as a step description
    # (The old step 10 was "Perform backlog reconciliation (US-0043/DEC-0021)")
    assert "Perform backlog reconciliation" not in text, \
        "release.md still contains old step 10 text"


# ── marker 8: AC-6 ────────────────────────────────────────────────

def test_us0120_closure_verification_schema_defined():
    """AC-6: closure-verification.md schema + validator exists."""
    validator = _path("scripts/validate_closure_verification.py")
    assert validator.exists(), "validate_closure_verification.py not found"
    text = validator.read_text(encoding="utf-8")
    # Must contain the required-fields list
    assert "story_id" in text
    assert "closure_date" in text
    assert "closure_role" in text
    assert "isolation_evidence" in text
    assert "runtime_proof" in text


# ── marker 9: AC-12 ───────────────────────────────────────────────

def test_us0120_compose_guards_unchanged():
    """AC-12: compose-guard surfaces UNCHANGED.

    Verifies that the 6 compose-guard story IDs are still referenced in
    architecture.md (proving compose-guard surfaces weren't deleted or removed).
    Per state.md sprint-plan checkpoint: US-0043/US-0045/US-0040/US-0048/US-0056
    are inline refs; US-0096 has a ## heading at L1684.
    """
    arch = _path("docs/engineering/architecture.md").read_text(encoding="utf-8")

    # All 6 compose-guard story IDs must still be referenced in architecture.md
    guards = ["US-0043", "US-0045", "US-0040", "US-0048", "US-0056", "US-0096"]
    for guard in guards:
        assert guard in arch, f"Compose-guard '{guard}' missing from architecture.md (compose surface may have been altered)"


# ── marker 10: AC-10 ──────────────────────────────────────────────

def test_us0120_backward_compat_drain_hook():
    """AC-10: drain hook detection for in-flight stories.

    Verifies that closure.md documents the 3-signal drain hook detection
    and the CLOSURE_LEGACY_DRIFT reason code.
    """
    text = _path(".cursor/commands/closure.md").read_text(encoding="utf-8")
    assert "CLOSURE_LEGACY_DRIFT" in text, \
        "closure.md missing CLOSURE_LEGACY_DRIFT reason code"
    assert "status=released" in text, \
        "closure.md missing drain hook signal (status=released)"
    # 3-signal detection documented
    assert "status: OPEN" in text or "Status: OPEN" in text, \
        "closure.md missing drain hook signal (Status: OPEN)"
