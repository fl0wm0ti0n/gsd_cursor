"""US-0109 compose guard: US-0054 publish semaphore + US-0100 changelog + US-0110 convergence unchanged."""
from __future__ import annotations
import sys
from pathlib import Path

def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]

def test_us0109_us0054_compose_no_publish_semantics_change() -> None:
    arch_path = _repo_root() / "docs" / "engineering" / "architecture.md"
    content = arch_path.read_text(encoding="utf-8")
    assert "# US-0109" in content
    us0109_section = content.split("# US-0109")[1] if "# US-0109" in content else ""
    assert "US-0054" in us0109_section
    assert "publish" in us0109_section.lower() or "re-enter" in us0109_section.lower()

def test_us0109_us0100_compose_no_changelog_change() -> None:
    root = _repo_root()
    scripts_dir = str(root / "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    import self_healing_deploy_lib as mod
    assert not hasattr(mod, "write_changelog")
    assert not hasattr(mod, "promote_unreleased")

def test_us0109_us0110_compose_no_convergence_change() -> None:
    root = _repo_root()
    scripts_dir = str(root / "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    import self_healing_deploy_lib as mod
    assert not hasattr(mod, "evaluate_convergence")
    assert not hasattr(mod, "is_converged")
    assert not hasattr(mod, "convergence_predicate")
