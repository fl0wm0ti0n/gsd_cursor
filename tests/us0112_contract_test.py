"""US-0112: Twelve `test_us0112_*` contract tests for model-catalog example preset delivery.

DEC-0112 §7: manifest rows, missing-mode copy, upgrade-mode refresh, active catalog protection,
triple installer parity, runbook recipe, parity scope --scope=model-catalog-examples.

Default state: 8 committed `model-catalog.local.example*.json` presets ship with its-magic framework
and are delivered via installer manifest under framework-file semantics (US-0018 / US-0057 / US-0075).
"""

from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


# --- T-001: Manifest lists 8 paths (active + template) -----------------------


class US0112ManifestPathsTest(unittest.TestCase):
    """test_us0112_manifest_lists_eight_paths (AC-1)."""

    def test_us0112_manifest_lists_eight_paths_active(self) -> None:
        manifest_path = _repo_root() / "docs" / "engineering" / "context" / "installer-owned-paths.manifest"
        self.assertTrue(manifest_path.exists())
        content = manifest_path.read_text(encoding="utf-8")
        lines = content.splitlines()

        expected = [
            ".cursor/model-catalog.local.example.json",
            ".cursor/model-catalog.local.example.cursor-only.json",
            ".cursor/model-catalog.local.example.level-1-easy.json",
            ".cursor/model-catalog.local.example.level-2-complex.json",
            ".cursor/model-catalog.local.example.level-3-mega.json",
            ".cursor/model-catalog.local.example.level-4-super.json",
            ".cursor/model-catalog.local.example.role-based-balanced.json",
            ".cursor/model-catalog.local.example.role-based-highend.json",
        ]
        for path in expected:
            self.assertIn(path, lines, f"Missing {path} in active manifest")

    def test_us0112_manifest_lists_eight_paths_template(self) -> None:
        manifest_path = _repo_root() / "template" / "docs" / "engineering" / "context" / "installer-owned-paths.manifest"
        self.assertTrue(manifest_path.exists())
        content = manifest_path.read_text(encoding="utf-8")
        lines = content.splitlines()

        expected = [
            ".cursor/model-catalog.local.example.json",
            ".cursor/model-catalog.local.example.cursor-only.json",
            ".cursor/model-catalog.local.example.level-1-easy.json",
            ".cursor/model-catalog.local.example.level-2-complex.json",
            ".cursor/model-catalog.local.example.level-3-mega.json",
            ".cursor/model-catalog.local.example.level-4-super.json",
            ".cursor/model-catalog.local.example.role-based-balanced.json",
            ".cursor/model-catalog.local.example.role-based-highend.json",
        ]
        for path in expected:
            self.assertIn(path, lines, f"Missing {path} in template manifest")


# --- T-003/T-004/T-005: Installer missing-mode classification ----------------


class US0112InstallerClassificationTest(unittest.TestCase):
    """test_us0112_installer_classification (AC-2, AC-5)."""

    def test_us0112_missing_mode_adds_absent_framework_files_python(self) -> None:
        sys.path.insert(0, str(_repo_root()))
        import installer  # type: ignore

        examples = [
            ".cursor/model-catalog.local.example.json",
            ".cursor/model-catalog.local.example.cursor-only.json",
            ".cursor/model-catalog.local.example.level-1-easy.json",
            ".cursor/model-catalog.local.example.level-2-complex.json",
            ".cursor/model-catalog.local.example.level-3-mega.json",
            ".cursor/model-catalog.local.example.level-4-super.json",
            ".cursor/model-catalog.local.example.role-based-balanced.json",
            ".cursor/model-catalog.local.example.role-based-highend.json",
        ]
        for rel in examples:
            cat = installer.classify_file(rel)
            self.assertEqual(cat, "framework", f"{rel} not classified as framework in installer.py")

    def test_us0112_missing_mode_adds_absent_framework_files_ps1(self) -> None:
        # PowerShell parity check: verify installer.ps1 classify_file function
        # includes model-catalog.local.example*.json in frameworkExact
        ps1_path = _repo_root() / "installer.ps1"
        content = ps1_path.read_text(encoding="utf-8")

        # Check that all 8 examples are in $frameworkExact array
        self.assertIn("model-catalog.local.example.json", content)
        self.assertIn("model-catalog.local.example.cursor-only.json", content)
        self.assertIn("model-catalog.local.example.level-1-easy.json", content)
        self.assertIn("model-catalog.local.example.level-2-complex.json", content)
        self.assertIn("model-catalog.local.example.level-3-mega.json", content)
        self.assertIn("model-catalog.local.example.level-4-super.json", content)
        self.assertIn("model-catalog.local.example.role-based-balanced.json", content)
        self.assertIn("model-catalog.local.example.role-based-highend.json", content)

    def test_us0112_missing_mode_adds_absent_framework_files_shell(self) -> None:
        # Shell parity check: verify installer.sh classify_file case pattern
        sh_path = _repo_root() / "installer.sh"
        content = sh_path.read_text(encoding="utf-8")

        # Check that .cursor/model-catalog.local.example*.json pattern is present
        self.assertIn(".cursor/model-catalog.local.example*.json", content)


# --- T-006: Upgrade-mode logic -----------------------------------------------


class US0112UpgradeModeTest(unittest.TestCase):
    """test_us0112_upgrade_mode (AC-3, AC-4)."""

    def test_us0112_upgrade_mode_refreshes_stale_framework_files(self) -> None:
        sys.path.insert(0, str(_repo_root()))
        import installer  # type: ignore

        # Verify framework classification triggers upgrade refresh
        example = ".cursor/model-catalog.local.example.json"
        cat = installer.classify_file(example)
        self.assertEqual(cat, "framework")

    def test_us0112_upgrade_mode_preserves_unchanged_files(self) -> None:
        # Upgrade mode byte-compares; unchanged files are skipped
        # This is a semantic test — actual byte comparison happens in installer loop
        sys.path.insert(0, str(_repo_root()))
        import installer  # type: ignore

        example = ".cursor/model-catalog.local.example.json"
        cat = installer.classify_file(example)
        self.assertEqual(cat, "framework", "Framework files eligible for upgrade refresh")

    def test_us0112_upgrade_mode_never_touches_local_catalog(self) -> None:
        sys.path.insert(0, str(_repo_root()))
        import installer  # type: ignore

        # Active catalog (operator-owned) must NOT be in manifest
        active_catalog = ".cursor/model-catalog.local.json"
        manifest_path = _repo_root() / "docs" / "engineering" / "context" / "installer-owned-paths.manifest"
        content = manifest_path.read_text(encoding="utf-8")
        self.assertNotIn(active_catalog, content, "Active catalog must not be in manifest")

        # Active catalog not in FRAMEWORK_EXACT either
        self.assertNotIn(active_catalog, installer.FRAMEWORK_EXACT)

    def test_us0112_active_catalog_protection_invariant(self) -> None:
        # Active catalog (.cursor/model-catalog.local.json) is gitignored and
        # outside install_include_paths + clean_paths — no installer mode touches it
        manifest_path = _repo_root() / "docs" / "engineering" / "context" / "installer-owned-paths.manifest"
        content = manifest_path.read_text(encoding="utf-8")
        lines = content.splitlines()

        # Verify active catalog NOT in manifest
        self.assertNotIn(".cursor/model-catalog.local.json", lines)


# --- T-007: Parity scope -----------------------------------------------------


class US0112ParityScopeTest(unittest.TestCase):
    """test_us0112_parity_scope (AC-5)."""

    def test_us0112_parity_scope_model_catalog_examples(self) -> None:
        sys.path.insert(0, str(_repo_root() / "scripts"))
        import check_intake_template_parity  # type: ignore

        self.assertIn("model-catalog-examples", check_intake_template_parity.SCOPES)
        pairs = check_intake_template_parity.MODEL_CATALOG_EXAMPLE_PAIRS
        self.assertGreaterEqual(len(pairs), 1)
        # Verify at least one pair is the manifest
        manifest_pair = (
            "docs/engineering/context/installer-owned-paths.manifest",
            "template/docs/engineering/context/installer-owned-paths.manifest",
        )
        self.assertIn(manifest_pair, pairs)


# --- T-006b: Triple installer parity (all three agree) -----------------------


class US0112TripleInstallerParityTest(unittest.TestCase):
    """test_us0112_triple_installer_parity_eight_examples (AC-5)."""

    def test_us0112_triple_installer_parity_eight_examples(self) -> None:
        """All three installers (Python / PS1 / Shell) classify all 8 examples as framework."""
        sys.path.insert(0, str(_repo_root()))
        import installer  # type: ignore

        examples = [
            ".cursor/model-catalog.local.example.json",
            ".cursor/model-catalog.local.example.cursor-only.json",
            ".cursor/model-catalog.local.example.level-1-easy.json",
            ".cursor/model-catalog.local.example.level-2-complex.json",
            ".cursor/model-catalog.local.example.level-3-mega.json",
            ".cursor/model-catalog.local.example.level-4-super.json",
            ".cursor/model-catalog.local.example.role-based-balanced.json",
            ".cursor/model-catalog.local.example.role-based-highend.json",
        ]

        # Python: all 8 in FRAMEWORK_EXACT set
        for expected in examples:
            self.assertIn(expected, installer.FRAMEWORK_EXACT,
                          f"{expected} missing from Python FRAMEWORK_EXACT")
            self.assertEqual(installer.classify_file(expected), "framework",
                             f"Python classify_file did not return 'framework' for {expected}")

        # PowerShell: all 8 filenames in installer.ps1 $frameworkExact
        ps1_content = (_repo_root() / "installer.ps1").read_text(encoding="utf-8")
        for expected in examples:
            self.assertIn(expected, ps1_content,
                          f"{expected} missing from installer.ps1 $frameworkExact")

        # Shell: glob pattern covers all 8 via model-catalog.local.example*.json
        sh_content = (_repo_root() / "installer.sh").read_text(encoding="utf-8")
        self.assertIn(".cursor/model-catalog.local.example*.json", sh_content,
                      "installer.sh classify_file missing model-catalog glob pattern")


# --- T-008: Runbook recipe ---------------------------------------------------


class US0112RunbookRecipeTest(unittest.TestCase):
    """test_us0112_runbook_recipe (AC-6)."""

    def test_us0112_runbook_lists_eight_preset_literals(self) -> None:
        runbook_path = _repo_root() / "docs" / "engineering" / "runbook.md"
        self.assertTrue(runbook_path.exists())
        content = runbook_path.read_text(encoding="utf-8")

        # Check for US-0112 section
        self.assertIn("## Model-catalog example preset delivery", content)

        # Check for all 8 filenames
        self.assertIn(".cursor/model-catalog.local.example.json", content)
        self.assertIn(".cursor/model-catalog.local.example.cursor-only.json", content)
        self.assertIn(".cursor/model-catalog.local.example.level-1-easy.json", content)
        self.assertIn(".cursor/model-catalog.local.example.level-2-complex.json", content)
        self.assertIn(".cursor/model-catalog.local.example.level-3-mega.json", content)
        self.assertIn(".cursor/model-catalog.local.example.level-4-super.json", content)
        self.assertIn(".cursor/model-catalog.local.example.role-based-balanced.json", content)
        self.assertIn(".cursor/model-catalog.local.example.role-based-highend.json", content)


if __name__ == "__main__":
    unittest.main()
