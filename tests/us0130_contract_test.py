"""US-0130: Operator-pinned sovereign-critic model (catalog role + scratchpad override).

10 contract markers (AC-1..AC-9). All static/fixture-based. No live critic spawn.
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, Dict, Optional


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _scripts_dir() -> Path:
    return _repo_root() / "scripts"


def _load_critic_lib():
    scripts = str(_scripts_dir())
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    import sovereign_critic_lib as mod  # noqa: E402

    return mod


def _load_tier_lib():
    scripts = str(_scripts_dir())
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    import model_tier_lib as mod  # noqa: E402

    return mod


def _load_tier_validate():
    scripts = str(_scripts_dir())
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    import model_tier_validate as mod  # noqa: E402

    return mod


REQUIRED_ROLES = {
    "po": "po-slug",
    "sa": "sa-slug",
    "dev": "dev-slug",
    "dev_difficult": "dev-diff-slug",
    "qa": "qa-slug",
    "security": "sec-slug",
    "release": "rel-slug",
}


def _v2_catalog(
    *,
    critic: Optional[str] = None,
    extra: Optional[Dict[str, str]] = None,
    pin_in_tiers: Optional[str] = None,
) -> Dict[str, Any]:
    roles = dict(REQUIRED_ROLES)
    if critic is not None:
        roles["critic"] = critic
    if extra:
        roles.update(extra)
    tiers = {
        "cheap": pin_in_tiers or "cheap-slug",
        "balanced": "balanced-slug",
        "strong": "strong-slug",
    }
    return {"schema_version": 2, "tiers": tiers, "roles": roles}


def _write_catalog(repo: Path, catalog: Dict[str, Any]) -> Path:
    repo.mkdir(parents=True, exist_ok=True)
    path = repo / "catalog.json"
    path.write_text(json.dumps(catalog), encoding="utf-8")
    return path


CURSOR_ONLY_REL = (
    ".cursor/model-catalog.local.example.role-based-balanced_cursor_only.json"
)
EXAMPLE_CATALOGS = (
    ".cursor/model-catalog.local.example.json",
    ".cursor/model-catalog.local.example.cursor-only.json",
    ".cursor/model-catalog.local.example.level-1-easy.json",
    ".cursor/model-catalog.local.example.level-2-complex.json",
    ".cursor/model-catalog.local.example.level-3-mega.json",
    ".cursor/model-catalog.local.example.level-4-super.json",
    ".cursor/model-catalog.local.example.role-based-balanced.json",
    ".cursor/model-catalog.local.example.role-based-highend.json",
    CURSOR_ONLY_REL,
)


class US0130PinWinsOverCatalogAndOpposition(unittest.TestCase):
    """Marker 1: test_us0130_pin_wins_over_catalog_and_opposition (AC-1/AC-3/AC-6)."""

    def test_us0130_pin_wins_over_catalog_and_opposition(self) -> None:
        lib = _load_critic_lib()
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            catalog_path = _write_catalog(
                repo,
                _v2_catalog(critic="catalog-critic-slug", pin_in_tiers="pin-critic-slug"),
            )
            pad = {
                "MODEL_SOVEREIGN-CRITIC": "pin-critic-slug",
                "MODEL_RESOLVE": "role_catalog",
                "MODEL_CATALOG": str(catalog_path),
                lib.CROSS_MODEL_REVIEW_KEY: "1",
            }
            result = lib.select_critic_model("producer-strong-slug", pad, "execute")
            self.assertEqual(result.critic_model_id, "pin-critic-slug")
            self.assertFalse(result.degraded)


class US0130CatalogCriticHitWhenPinAbsent(unittest.TestCase):
    """Marker 2: test_us0130_catalog_critic_hit_when_pin_absent (AC-2/AC-3/AC-6)."""

    def test_us0130_catalog_critic_hit_when_pin_absent(self) -> None:
        lib = _load_critic_lib()
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            catalog_path = _write_catalog(repo, _v2_catalog(critic="catalog-critic-slug"))
            pad = {
                "MODEL_RESOLVE": "role_catalog",
                "MODEL_CATALOG": str(catalog_path),
                lib.CROSS_MODEL_REVIEW_KEY: "1",
            }
            self.assertNotIn("MODEL_SOVEREIGN-CRITIC", pad)
            result = lib.select_critic_model("producer-strong-slug", pad, "execute")
            self.assertEqual(result.critic_model_id, "catalog-critic-slug")
            self.assertFalse(result.degraded)


class US0130OmittedCriticFallsBackToOpposition(unittest.TestCase):
    """Marker 3: test_us0130_omitted_critic_falls_back_to_opposition (AC-2/AC-3/AC-6)."""

    def test_us0130_omitted_critic_falls_back_to_opposition(self) -> None:
        lib = _load_critic_lib()
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            catalog_path = _write_catalog(repo, _v2_catalog())
            pad = {
                "MODEL_RESOLVE": "role_catalog",
                "MODEL_CATALOG": str(catalog_path),
                lib.CROSS_MODEL_REVIEW_KEY: "1",
            }
            result = lib.select_critic_model("producer-strong-slug", pad, "execute")
            producer_tier = lib._infer_producer_tier("producer-strong-slug")
            critic_tier = lib.CRITIC_TIER_OPPOSITION.get(producer_tier, lib.Tier.CHEAP)
            expected = lib._resolve_slug_for_tier("sovereign-critic", critic_tier, pad)
            self.assertEqual(result.critic_model_id, expected)
            self.assertNotEqual(result.critic_model_id, "catalog-critic-slug")


class US0130SameSlugKeepsDegradedMode(unittest.TestCase):
    """Marker 4: test_us0130_same_slug_keeps_degraded_mode (AC-4/AC-6)."""

    def test_us0130_same_slug_keeps_degraded_mode(self) -> None:
        lib = _load_critic_lib()
        pad = {
            "MODEL_SOVEREIGN-CRITIC": "same-slug",
            "MODEL_RESOLVE": "alias_only",
            lib.CROSS_MODEL_REVIEW_KEY: "1",
        }
        result = lib.select_critic_model("same-slug", pad, "execute")
        self.assertTrue(result.degraded)
        self.assertIsNotNone(result.reason_code)
        self.assertEqual(result.reason_code.value, "CROSS_MODEL_DEGRADED_MODE")
        self.assertEqual(result.critic_model_id, "same-slug")


class US0130ComposeUs0104FindingsSchemaUnchanged(unittest.TestCase):
    """Marker 5: test_us0130_compose_us0104_findings_schema_unchanged (AC-7/AC-6)."""

    def test_us0130_compose_us0104_findings_schema_unchanged(self) -> None:
        lib = _load_critic_lib()
        self.assertEqual(len(lib.FINDING_REQUIRED_FIELDS), 15)
        self.assertEqual(lib.LENS_VALUES, {"challenger", "architect", "subtractor"})
        self.assertEqual(lib.CROSS_MODEL_REVIEW_VALUES, {"0", "1"})
        self.assertEqual(lib.CROSS_MODEL_REVIEW_DEFAULT, "0")
        self.assertEqual(lib.CROSS_MODEL_ANTISLOP_THRESHOLD_DEFAULT, 6)
        self.assertEqual(lib.CROSS_MODEL_REWORK_MAX_DEFAULT, 2)
        self.assertEqual(lib.compute_anti_slop_aggregate([8, 7, 9]), 7)
        self.assertEqual(lib.compute_anti_slop_aggregate([]), 0)
        self.assertIn(lib.CROSS_MODEL_REVIEW_KEY, ("CROSS_MODEL_REVIEW",))
        self.assertEqual(
            lib.CROSS_MODEL_ANTISLOP_THRESHOLD_KEY, "CROSS_MODEL_ANTISLOP_THRESHOLD"
        )
        self.assertEqual(lib.CROSS_MODEL_REWORK_MAX_KEY, "CROSS_MODEL_REWORK_MAX")


class US0130UnderscoreAliasNotConsumed(unittest.TestCase):
    """Marker 6: test_us0130_underscore_alias_not_consumed (DQ3) (AC-1/AC-3/AC-6)."""

    def test_us0130_underscore_alias_not_consumed(self) -> None:
        lib = _load_critic_lib()
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            catalog_path = _write_catalog(
                repo,
                _v2_catalog(critic="catalog-critic-slug", pin_in_tiers="hyphen-pin-slug"),
            )
            pad_underscore_only = {
                "MODEL_SOVEREIGN_CRITIC": "underscore-slug",
                "MODEL_RESOLVE": "role_catalog",
                "MODEL_CATALOG": str(catalog_path),
                lib.CROSS_MODEL_REVIEW_KEY: "1",
            }
            ignored = lib.select_critic_model(
                "producer-strong-slug", pad_underscore_only, "execute"
            )
            self.assertEqual(ignored.critic_model_id, "catalog-critic-slug")
            self.assertNotEqual(ignored.critic_model_id, "underscore-slug")

            pad_both = dict(pad_underscore_only)
            pad_both["MODEL_SOVEREIGN-CRITIC"] = "hyphen-pin-slug"
            hyphen = lib.select_critic_model(
                "producer-strong-slug", pad_both, "execute"
            )
            self.assertEqual(hyphen.critic_model_id, "hyphen-pin-slug")
            self.assertNotEqual(hyphen.critic_model_id, "underscore-slug")


class US0130ExtraCriticAllowedMissingNotError(unittest.TestCase):
    """Marker 7: test_us0130_extra_critic_allowed_missing_not_error (DQ6) (AC-2/AC-6)."""

    def test_us0130_extra_critic_allowed_missing_not_error(self) -> None:
        mtl = _load_tier_lib()
        validate = _load_tier_validate()
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)

            with_critic = _write_catalog(repo / "with", _v2_catalog(critic="critic-slug"))
            ok, err = mtl.validate_catalog_schema(with_critic)
            self.assertTrue(ok, msg=str(err))

            missing = _write_catalog(repo / "missing", _v2_catalog())
            ok, err = mtl.validate_catalog_schema(missing)
            self.assertTrue(ok, msg=str(err))

            empty = _write_catalog(repo / "empty", _v2_catalog(critic="   "))
            ok, err = mtl.validate_catalog_schema(empty)
            self.assertFalse(ok)
            self.assertIsNotNone(err)
            self.assertIn("critic", err)
            code = mtl.catalog_validation_reason_code(err, {"schema_version": 2})
            self.assertEqual(code.value, "MODEL_CATALOG_SCHEMA_V2_INVALID")

            ok_v, errors, vcode = validate.validate_catalog(empty)
            self.assertFalse(ok_v)
            self.assertTrue(any("critic" in e for e in errors))
            self.assertEqual(vcode.value, "MODEL_CATALOG_SCHEMA_V2_INVALID")

            unknown = _write_catalog(
                repo / "unknown", _v2_catalog(extra={"typo_role": "x"})
            )
            ok, err = mtl.validate_catalog_schema(unknown)
            self.assertFalse(ok)
            self.assertIn("Unknown role keys", err or "")


class US0130CriticNotInCatalogRoleKeys(unittest.TestCase):
    """Marker 8: test_us0130_critic_not_in_catalog_role_keys (DQ1) (AC-2/AC-6)."""

    def test_us0130_critic_not_in_catalog_role_keys(self) -> None:
        mtl = _load_tier_lib()
        self.assertNotIn("critic", mtl.CATALOG_ROLE_KEYS)
        self.assertEqual(mtl.CATALOG_OPTIONAL_ROLE_KEYS, frozenset({"critic"}))
        self.assertNotIn("sovereign-critic", mtl.PHASE_LOGICAL_ROLE)
        self.assertNotIn("sovereign-critic", mtl.CANONICAL_PHASE_IDS)
        self.assertNotIn("critic", mtl.LOGICAL_ROLE_TO_CATALOG_KEY)
        self.assertNotIn("sovereign-critic", mtl.DEFAULT_PHASE_TIER_MATRIX)


class US0130CursorOnlyExampleShipsCritic(unittest.TestCase):
    """Marker 9: test_us0130_cursor_only_example_ships_critic (DQ4/DQ5) (AC-8/AC-6)."""

    def test_us0130_cursor_only_example_ships_critic(self) -> None:
        root = _repo_root()
        sys.path.insert(0, str(root))
        import installer  # type: ignore  # noqa: E402

        active = root / CURSOR_ONLY_REL
        template = root / "template" / CURSOR_ONLY_REL
        self.assertTrue(active.exists())
        self.assertTrue(template.exists())
        self.assertEqual(active.read_bytes(), template.read_bytes())

        data = json.loads(active.read_text(encoding="utf-8"))
        self.assertEqual(data["roles"]["critic"], "composer-2.5-fast")

        generic = json.loads(
            (root / ".cursor" / "model-catalog.local.example.role-based-balanced.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(generic["roles"]["critic"], "<your-critic-model-slug>")

        shipped = [
            path for path in installer.FRAMEWORK_EXACT if path.startswith(
                ".cursor/model-catalog.local.example"
            ) and path.endswith(".json")
        ]
        self.assertEqual(len(shipped), 9)
        self.assertIn(CURSOR_ONLY_REL, installer.FRAMEWORK_EXACT)

        manifest = (
            root / "docs" / "engineering" / "context" / "installer-owned-paths.manifest"
        ).read_text(encoding="utf-8")
        self.assertIn(CURSOR_ONLY_REL, manifest.splitlines())

        ps1 = (root / "installer.ps1").read_text(encoding="utf-8")
        self.assertIn(CURSOR_ONLY_REL, ps1)


class US0130InstallerNeverWritesLocalCatalog(unittest.TestCase):
    """Marker 10: test_us0130_installer_never_writes_local_catalog (DQ5) (AC-8/AC-6)."""

    def test_us0130_installer_never_writes_local_catalog(self) -> None:
        root = _repo_root()
        sys.path.insert(0, str(root))
        import installer  # type: ignore  # noqa: E402

        active_catalog = ".cursor/model-catalog.local.json"
        self.assertNotIn(active_catalog, installer.FRAMEWORK_EXACT)

        manifest = (
            root / "docs" / "engineering" / "context" / "installer-owned-paths.manifest"
        ).read_text(encoding="utf-8")
        self.assertNotIn(active_catalog, manifest.splitlines())

        py = (root / "installer.py").read_text(encoding="utf-8")
        self.assertNotIn('".cursor/model-catalog.local.json"', py)
        self.assertNotIn("'.cursor/model-catalog.local.json'", py)

        self.assertFalse((root / ".cursor" / "model-catalog.local.json").exists())


if __name__ == "__main__":
    unittest.main()
