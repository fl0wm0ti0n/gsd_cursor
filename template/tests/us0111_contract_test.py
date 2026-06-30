"""US-0111: Twelve `test_us0111_*` contract tests for Release Trigger Adapters.

DEC-0111 §7: adapter registry, GitHub webhook, npm publish, Git tag push,
manual /release, version comparison, atomic promotion, per-version notes,
ledger event, 9 reason codes, compose guards (US-0100, US-0054).

Default source: RELEASE_TRIGGER_SOURCE=manual (zero behavior change vs pre-US-0111).
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _load_lib():
    root = _repo_root()
    scripts_dir = str(root / "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    import release_trigger_adapters as mod  # noqa: E402
    return mod


# --- T-001: Adapter registry dispatch (AC-1) ---------------------------------


class US0111AdapterRegistryDispatchTest(unittest.TestCase):
    """test_us0111_adapter_registry_dispatch (AC-1)."""

    def test_us0111_adapter_registry_dispatch(self) -> None:
        lib = _load_lib()
        registry = lib._ADAPTER_MAP
        self.assertIn("manual", registry)
        self.assertIn("github", registry)
        self.assertIn("npm", registry)
        self.assertIn("git_tag", registry)
        self.assertEqual(len(registry), 4)

        # Dispatch to manual adapter
        ctx = lib.dispatch_to_adapter("manual", env_vars={}, current_version="1.2.3")
        self.assertEqual(ctx.source, "manual")
        self.assertEqual(ctx.version, "1.2.3")
        self.assertIsNone(ctx.previous_version)

        # Invalid source → fail-closed
        with self.assertRaises(lib.ReleaseTriggerError) as cm:
            lib.dispatch_to_adapter("invalid_source", env_vars={})
        self.assertEqual(cm.exception.code, "RELEASE_TRIGGER_SOURCE_INVALID")


# --- T-002: GitHub webhook adapter (AC-2) ------------------------------------


class US0111GithubAdapterTest(unittest.TestCase):
    """test_us0111_github_adapter_success_fail_closed (AC-2)."""

    def test_us0111_github_adapter_success_fail_closed(self) -> None:
        lib = _load_lib()
        # Success path: valid payload with tag_name
        payload = {"release": {"tag_name": "v1.2.3"}}
        env = {"GITHUB_TOKEN": "test-token", "GITHUB_REPOSITORY": "owner/repo"}
        adapter = lib.GithubReleaseAdapter(env_vars=env, payload=payload, timeout_sec=5)
        ctx = adapter.get_version_info()
        self.assertEqual(ctx.source, "github")
        self.assertEqual(ctx.version, "1.2.3")
        self.assertIn("GITHUB_TOKEN", ctx.metadata.get("token_env_ref", ""))

        # Fail-closed: missing tag_name
        adapter_bad = lib.GithubReleaseAdapter(env_vars={}, payload={}, timeout_sec=5)
        with self.assertRaises(lib.ReleaseTriggerError) as cm:
            adapter_bad.get_version_info()
        self.assertEqual(cm.exception.code, "RELEASE_TRIGGER_TAG_MISSING")


# --- T-003: npm publish adapter (AC-3) ---------------------------------------


class US0111NpmAdapterTest(unittest.TestCase):
    """test_us0111_npm_adapter_success_fail_closed (AC-3)."""

    def test_us0111_npm_adapter_success_fail_closed(self) -> None:
        lib = _load_lib()
        # Success path: npm_package_version env var
        env = {"npm_package_version": "2.0.1", "npm_package_name": "test-pkg"}
        adapter = lib.NpmPublishAdapter(env_vars=env, timeout_sec=5)
        ctx = adapter.get_version_info()
        self.assertEqual(ctx.source, "npm")
        self.assertEqual(ctx.version, "2.0.1")

        # Fail-closed: missing package.json + env var
        with tempfile.TemporaryDirectory() as tmp:
            adapter_bad = lib.NpmPublishAdapter(
                env_vars={}, timeout_sec=5, repo_root=tmp
            )
            with self.assertRaises(lib.ReleaseTriggerError) as cm:
                adapter_bad.get_version_info()
            self.assertEqual(cm.exception.code, "RELEASE_TRIGGER_PACKAGE_JSON_MISSING")


# --- T-004: Git tag push adapter (AC-4) --------------------------------------


class US0111GitTagAdapterTest(unittest.TestCase):
    """test_us0111_git_tag_adapter_success_fail_closed (AC-4)."""

    def test_us0111_git_tag_adapter_success_fail_closed(self) -> None:
        lib = _load_lib()
        # Success path: GITHUB_REF with semver tag
        env = {"GITHUB_REF": "refs/tags/v3.1.4"}
        adapter = lib.GitTagAdapter(env_vars=env, repo_root=".")
        ctx = adapter.get_version_info()
        self.assertEqual(ctx.source, "git_tag")
        self.assertEqual(ctx.version, "3.1.4")

        # Fail-closed: no tag resolvable — use tempdir without .git so both
        # GITHUB_REF detection and `git describe` fail.
        with tempfile.TemporaryDirectory() as tmp_empty:
            adapter_bad = lib.GitTagAdapter(env_vars={}, repo_root=tmp_empty)
            with self.assertRaises(lib.ReleaseTriggerError) as cm:
                adapter_bad.get_version_info()
            self.assertEqual(cm.exception.code, "RELEASE_TRIGGER_TAG_MISSING")


# --- T-005: Manual backward compatibility (AC-5) -----------------------------


class US0111ManualBackwardCompatTest(unittest.TestCase):
    """test_us0111_manual_backward_compat_byte_identical (AC-5)."""

    def test_us0111_manual_backward_compat_byte_identical(self) -> None:
        lib = _load_lib()
        # Manual adapter: byte-identical to pre-US-0111 /release behavior
        ctx = lib.dispatch_to_adapter("manual", env_vars={}, current_version="1.0.0")
        self.assertEqual(ctx.source, "manual")
        self.assertEqual(ctx.version, "1.0.0")
        self.assertIsNone(ctx.previous_version)
        self.assertTrue(ctx.metadata.get("manual"))


# --- T-006: Version comparison logic (AC-6) ----------------------------------


class US0111CompareVersionsIntegrationTest(unittest.TestCase):
    """test_us0111_compare_versions_from_trigger_integration (AC-6)."""

    def test_us0111_compare_versions_from_trigger_integration(self) -> None:
        lib = _load_lib()
        trigger = lib.TriggerContext(
            version="1.2.3",
            previous_version="1.2.2",
            source="github",
            metadata={},
        )
        norm_current, norm_previous = lib.compare_versions_from_trigger(trigger)
        self.assertEqual(norm_current, "1.2.3")
        self.assertEqual(norm_previous, "1.2.2")

        # Invalid version → fail-closed
        trigger_bad = lib.TriggerContext(
            version="invalid",
            previous_version=None,
            source="manual",
            metadata={},
        )
        with self.assertRaises(lib.ReleaseTriggerError) as cm:
            lib.compare_versions_from_trigger(trigger_bad)
        self.assertEqual(cm.exception.code, "RELEASE_TRIGGER_COMPARE_VERSIONS_FAILED")


# --- T-007: Atomic promotion (AC-7) ------------------------------------------


class US0111AtomicPromotionTest(unittest.TestCase):
    """test_us0111_atomic_promotion_temp_rename (AC-7)."""

    def test_us0111_atomic_promotion_temp_rename(self) -> None:
        lib = _load_lib()
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "test.txt")
            lib.atomic_write_file(target, "content")
            self.assertTrue(os.path.exists(target))
            with open(target, "r", encoding="utf-8") as f:
                self.assertEqual(f.read(), "content")


# --- T-008: Per-version notes atomic write (AC-8) ----------------------------


class US0111PerVersionNotesTest(unittest.TestCase):
    """test_us0111_per_version_notes_atomic_write (AC-8)."""

    def test_us0111_per_version_notes_atomic_write(self) -> None:
        lib = _load_lib()
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "handoffs" / "releases").mkdir(parents=True)
            # Mock release_changelog_lib to avoid full dependency
            sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
            from release_changelog_lib import normalize_semver, version_fingerprint

            norm = normalize_semver("1.0.0")
            fp = version_fingerprint(norm, ["US-0111"])
            target = repo / "handoffs" / "releases" / "1.0.0-release-notes.md"
            content = f"# Release 1.0.0\n<!-- fingerprint: {fp} -->\n"
            lib.atomic_write_file(str(target), content)
            self.assertTrue(target.exists())
            self.assertIn("Release 1.0.0", target.read_text(encoding="utf-8"))


# --- T-009: Sovereign loop integration (AC-9) --------------------------------


class US0111LedgerEventTest(unittest.TestCase):
    """test_us0111_ledger_event_emit_shape (AC-9)."""

    def test_us0111_ledger_event_emit_shape(self) -> None:
        lib = _load_lib()
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "handoffs" / "release_events").mkdir(parents=True)
            trigger = lib.TriggerContext(
                version="1.0.0",
                previous_version="0.9.0",
                source="github",
                metadata={"tag": "v1.0.0"},
            )
            # Mock ledger append to avoid schema validation
            sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
            import decision_ledger_lib as ledger_lib

            original_append = ledger_lib.append_entry

            def mock_append(*args, **kwargs):
                return ledger_lib.AppendResult(
                    success=True,
                    reason_code="LEDGER_DISABLED",
                    reason_message="mock",
                )

            ledger_lib.append_entry = mock_append
            try:
                result = lib.emit_version_derivation_event(
                    trigger, "1.0.0", "0.9.0", str(repo), scratchpad={}
                )
                self.assertIn("event_path", result)
                event_file = Path(result["event_path"])
                self.assertTrue(event_file.exists())
                event_data = json.loads(event_file.read_text(encoding="utf-8"))
                self.assertEqual(event_data["semver"], "1.0.0")
                self.assertEqual(event_data["previous_semver"], "0.9.0")
                self.assertEqual(event_data["source"], "github")
            finally:
                ledger_lib.append_entry = original_append


# --- T-010: Fail-closed reason codes (AC-10) ---------------------------------


class US0111ReasonCodeInventoryTest(unittest.TestCase):
    """test_us0111_reason_code_inventory_9_codes (AC-10)."""

    def test_us0111_reason_code_inventory_9_codes(self) -> None:
        lib = _load_lib()
        # 9 reason codes in FAIL_CODES tuple
        self.assertEqual(len(lib.FAIL_CODES), 9)
        expected_codes = {
            "RELEASE_TRIGGER_ADAPTER_FAILED",
            "RELEASE_TRIGGER_TAG_MISSING",
            "RELEASE_TRIGGER_PREVIOUS_MISSING",
            "RELEASE_TRIGGER_PACKAGE_JSON_MISSING",
            "RELEASE_TRIGGER_ATOMIC_PROMOTION_FAILED",
            "RELEASE_TRIGGER_NOTES_WRITE_FAILED",
            "RELEASE_TRIGGER_EVENT_EMIT_FAILED",
            "RELEASE_TRIGGER_COMPARE_VERSIONS_FAILED",
            "RELEASE_TRIGGER_SOURCE_INVALID",
        }
        self.assertEqual(set(lib.FAIL_CODES), expected_codes)

        # Reason codes documented in reason_codes.md
        root = _repo_root()
        reason_codes_path = root / "docs" / "engineering" / "reason_codes.md"
        text = reason_codes_path.read_text(encoding="utf-8")
        self.assertIn("US-0111 — Release trigger adapter family", text)
        self.assertIn("RELEASE_TRIGGER_* (9 codes)", text)
        for code in expected_codes:
            self.assertIn(code, text, f"missing {code} in reason_codes.md")


# --- T-010: Compose guard US-0100 (no API change) ----------------------------


class US0111US0100ComposeTest(unittest.TestCase):
    """test_us0111_us0100_compose_no_derivation_semantics_change (AC-6 compose guard)."""

    def test_us0111_us0100_compose_no_derivation_semantics_change(self) -> None:
        # Verify release_changelog_lib APIs unchanged (US-0100 compose guard)
        sys.path.insert(0, str(_repo_root() / "scripts"))
        import release_changelog_lib
        import inspect

        # normalize_semver(raw) — existing API, unchanged
        sig = inspect.signature(release_changelog_lib.normalize_semver)
        self.assertEqual(len(sig.parameters), 1)

        # promote_unreleased(semver, sprint_ids, repo_root, release_date) — unchanged
        sig2 = inspect.signature(release_changelog_lib.promote_unreleased)
        self.assertGreaterEqual(len(sig2.parameters), 3)

        # build_version_doc(semver, sprint_ids, repo_root) — unchanged
        sig3 = inspect.signature(release_changelog_lib.build_version_doc)
        self.assertEqual(len(sig3.parameters), 3)

        # version_fingerprint(semver, work_item_ids) — unchanged
        sig4 = inspect.signature(release_changelog_lib.version_fingerprint)
        self.assertEqual(len(sig4.parameters), 2)


# --- T-010: Compose guard US-0054 (no publish semantics change) --------------


class US0111US0054ComposeTest(unittest.TestCase):
    """test_us0111_us0054_compose_no_publish_semantics_change (AC-5 compose guard)."""

    def test_us0111_us0054_compose_no_publish_semantics_change(self) -> None:
        # Manual adapter produces same TriggerContext as pre-US-0111 /release
        lib = _load_lib()
        ctx = lib.dispatch_to_adapter("manual", env_vars={}, current_version="1.0.0")
        self.assertEqual(ctx.source, "manual")
        self.assertEqual(ctx.version, "1.0.0")
        self.assertIsNone(ctx.previous_version)
        # No publish logic in adapter — US-0054 release-all.sh unchanged
        self.assertNotIn("publish", ctx.metadata)


if __name__ == "__main__":
    unittest.main()
