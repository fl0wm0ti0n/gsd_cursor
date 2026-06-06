"""BUG-0003 installer completeness regressions (DEC-0066)."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "installer.py"
ACTIVE_MANIFEST = ROOT / "docs" / "engineering" / "context" / "installer-owned-paths.manifest"
TEMPLATE_MANIFEST = ROOT / "template" / "docs" / "engineering" / "context" / "installer-owned-paths.manifest"
REQUIRED_SECTION = "required_install_script_paths"
TRIAD_SCRIPT = "scripts/enforce-triad-hot-surface.py"


def parse_manifest_sections(path: Path) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            current = line[1:-1]
            sections.setdefault(current, [])
            continue
        if current is not None:
            sections[current].append(line)
    return sections


def write_bootstrap_package_json(target: Path) -> None:
    payload = {
        "name": "tmp-installer-fixture",
        "version": "0.0.0",
        "scripts": {"test": "echo ok"},
    }
    (target / "package.json").write_text(json.dumps(payload), encoding="utf-8")


class InstallerCompletenessBug0003Test(unittest.TestCase):
    def run_installer(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(INSTALLER), *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

    def test_manifest_required_inventory_and_symmetry(self) -> None:
        active = parse_manifest_sections(ACTIVE_MANIFEST)
        template = parse_manifest_sections(TEMPLATE_MANIFEST)
        self.assertIn(REQUIRED_SECTION, active)
        self.assertEqual(active, template, "active/template manifest sections drifted")

        required = active[REQUIRED_SECTION]
        install_paths = active["install_include_paths"]
        clean_paths = active["clean_paths"]

        self.assertIn(TRIAD_SCRIPT, required)
        self.assertIn(TRIAD_SCRIPT, install_paths)
        self.assertIn(TRIAD_SCRIPT, clean_paths)
        for rel in required:
            self.assertIn(rel, install_paths, f"{rel} missing from install_include_paths")
            self.assertIn(rel, clean_paths, f"{rel} missing from clean_paths")

        active_triad = ROOT / TRIAD_SCRIPT
        template_triad = ROOT / "template" / TRIAD_SCRIPT
        self.assertTrue(active_triad.is_file())
        self.assertTrue(template_triad.is_file())
        self.assertEqual(active_triad.read_bytes(), template_triad.read_bytes())

    def test_missing_and_upgrade_keep_required_scripts_present(self) -> None:
        sections = parse_manifest_sections(ACTIVE_MANIFEST)
        required = sections[REQUIRED_SECTION]
        with tempfile.TemporaryDirectory() as td:
            target = Path(td)
            write_bootstrap_package_json(target)

            r_missing = self.run_installer("--target", str(target), "--mode", "missing", "--create")
            self.assertEqual(0, r_missing.returncode, r_missing.stdout + r_missing.stderr)
            for rel in required:
                self.assertTrue((target / rel).is_file(), f"missing install omitted required path: {rel}")

            user_file = target / "docs" / "product" / "vision.md"
            user_file.parent.mkdir(parents=True, exist_ok=True)
            user_file.write_text("# custom", encoding="utf-8")
            framework_file = target / ".cursor" / "commands" / "intake.md"
            framework_file.write_text("framework override", encoding="utf-8")

            r_upgrade = self.run_installer("--target", str(target), "--mode", "upgrade")
            self.assertEqual(0, r_upgrade.returncode, r_upgrade.stdout + r_upgrade.stderr)
            self.assertIn("custom", user_file.read_text(encoding="utf-8"))
            self.assertNotIn("framework override", framework_file.read_text(encoding="utf-8"))
            for rel in required:
                self.assertTrue((target / rel).is_file(), f"upgrade omitted required path: {rel}")

    def test_caveman_compress_input_shipped_by_installer(self) -> None:
        """US-0090 / DEC-0073 §10: installer delivers template/scripts/caveman_compress_input.py."""
        script_rel = "scripts/caveman_compress_input.py"
        sections = parse_manifest_sections(ACTIVE_MANIFEST)
        self.assertIn(script_rel, sections[REQUIRED_SECTION],
                      "caveman compressor must be listed in required_install_script_paths")
        self.assertIn(script_rel, sections["install_include_paths"])
        self.assertIn(script_rel, sections["clean_paths"])

        active_script = ROOT / script_rel
        template_script = ROOT / "template" / script_rel
        self.assertTrue(active_script.is_file())
        self.assertTrue(template_script.is_file())
        self.assertEqual(active_script.read_bytes(), template_script.read_bytes(),
                         "active/template caveman compressor bytes must match")

        with tempfile.TemporaryDirectory() as td:
            target = Path(td)
            write_bootstrap_package_json(target)
            for mode in ("missing", "upgrade"):
                if mode == "missing":
                    r = self.run_installer(
                        "--target", str(target), "--mode", mode, "--create",
                    )
                else:
                    r = self.run_installer(
                        "--target", str(target), "--mode", mode,
                    )
                self.assertEqual(0, r.returncode, r.stdout + r.stderr)
                self.assertTrue(
                    (target / script_rel).is_file(),
                    f"installer --mode={mode} must deliver {script_rel}",
                )

    def test_negative_missing_required_script_fails_deterministically(self) -> None:
        with tempfile.TemporaryDirectory() as sd, tempfile.TemporaryDirectory() as td:
            source_root = Path(sd) / "template"
            shutil.copytree(ROOT / "template", source_root)
            missing_script = source_root / TRIAD_SCRIPT
            missing_script.unlink()

            target = Path(td)
            write_bootstrap_package_json(target)

            r = self.run_installer(
                "--target",
                str(target),
                "--mode",
                "missing",
                "--create",
                "--source-root",
                str(source_root),
            )
            merged = r.stdout + r.stderr
            self.assertNotEqual(0, r.returncode)
            self.assertIn("INSTALL_COMPLETENESS_FAILED", merged)
            self.assertIn(f"INSTALL_REQUIRED_SCRIPT_MISSING:{TRIAD_SCRIPT}", merged)

    def _extract_ci_job_keys(self, ci_yml_path: Path) -> set[str]:
        import sys as _sys

        _sys.path.insert(0, str(ROOT / "scripts"))
        try:
            import downstream_ci_guard_lib as dci
        finally:
            _sys.path.pop(0)
        return set(dci.extract_job_keys(ci_yml_path.read_text(encoding="utf-8")))

    def _assert_downstream_safe_ci_inventory(self, target: Path) -> None:
        ci_path = target / ".github" / "workflows" / "ci.yml"
        self.assertTrue(ci_path.is_file(), "installed ci.yml must exist")
        job_keys = self._extract_ci_job_keys(ci_path)
        self.assertLessEqual(job_keys, {"checks", "auto-fix"},
                             f"installed ci.yml job keys must be downstream-safe; got {job_keys}")
        for forbidden in ("npm-test", "brew-test", "choco-test"):
            self.assertNotIn(forbidden, job_keys, f"packaging job {forbidden} must not leak")

    def test_downstream_ci_yml_job_inventory_missing_mode(self) -> None:
        """BUG-0009 / DEC-0075 §7: missing install ships checks+auto-fix only."""
        with tempfile.TemporaryDirectory() as td:
            target = Path(td)
            write_bootstrap_package_json(target)
            r = self.run_installer("--target", str(target), "--mode", "missing", "--create")
            self.assertEqual(0, r.returncode, r.stdout + r.stderr)
            self._assert_downstream_safe_ci_inventory(target)

    def test_downstream_ci_yml_job_inventory_upgrade_mode(self) -> None:
        """BUG-0009 / DEC-0075 §7: upgrade refresh keeps downstream-safe ci.yml."""
        with tempfile.TemporaryDirectory() as td:
            target = Path(td)
            write_bootstrap_package_json(target)
            r_missing = self.run_installer(
                "--target", str(target), "--mode", "missing", "--create",
            )
            self.assertEqual(0, r_missing.returncode, r_missing.stdout + r_missing.stderr)
            stale_ci = target / ".github" / "workflows" / "ci.yml"
            stale_ci.write_text(
                stale_ci.read_text(encoding="utf-8") + "\n  npm-test:\n    runs-on: ubuntu-latest\n",
                encoding="utf-8",
            )
            r_upgrade = self.run_installer("--target", str(target), "--mode", "upgrade")
            self.assertEqual(0, r_upgrade.returncode, r_upgrade.stdout + r_upgrade.stderr)
            self._assert_downstream_safe_ci_inventory(target)


if __name__ == "__main__":
    unittest.main()
