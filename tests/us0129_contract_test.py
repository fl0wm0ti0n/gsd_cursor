"""US-0129: Architecture hot-surface rollover linkage guard.

8 contract markers (AC-1..AC-5). Synthetic mini-architecture fixtures in temp
dirs — do not replay architecture-pack-20260825.md. All static/fixture-based.
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from typing import Optional


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _scripts_dir() -> Path:
    return _repo_root() / "scripts"


def _load_guard():
    scripts = str(_scripts_dir())
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    import arch_linkage_guard as mod  # noqa: E402

    return mod


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _mini_architecture() -> str:
    return (
        "# Architecture preamble\n\n"
        "# US-0042 — Required consumer heading\n\n"
        "Oldest story body for US-0042.\n\n"
        "# US-0043 — Second oldest\n\n"
        "Second story body.\n\n"
        "# US-0089 — Caveman input compression\n\n"
        "Caveman tail body.\n\n"
        "# US-0090 — After 0089 only\n\n"
        "Peer after 0089.\n"
    )


def _arch_file(repo: Path) -> Path:
    return repo.joinpath("docs", "engineering", "architecture.md")


def _consumer_src(heading: str) -> str:
    return (
        "from pathlib import Path\n\n"
        "def test_consumer_requires_heading():\n"
        "    root = Path(__file__).resolve().parents[1]\n"
        "    arch = root.joinpath('docs', 'engineering', 'architecture.md')"
        ".read_text(encoding='utf-8')\n"
        f"    assert '{heading}' in arch\n"
    )


def _tmp_noise_src(heading: str) -> str:
    return (
        "from pathlib import Path\n\n"
        "def test_tmp_fixture_must_be_ignored():\n"
        "    root = Path(__file__).resolve().parents[2]\n"
        "    arch = root.joinpath('docs', 'engineering', 'architecture.md')"
        ".read_text(encoding='utf-8')\n"
        f"    assert '{heading}' in arch\n"
    )


def _command_grep_src() -> str:
    return (
        "from pathlib import Path\n\n"
        "def test_command_file_grep_must_be_ignored():\n"
        "    root = Path(__file__).resolve().parents[1]\n"
        "    text = root.joinpath('.cursor', 'commands', 'architecture.md')"
        ".read_text(encoding='utf-8')\n"
        "    assert '# US-0999' in text\n"
    )


def _make_synth_repo(
    tmp: Path,
    *,
    auto_repair: Optional[str] = None,
    max_stories: int = 2,
    consumer_heading: str = "# US-0042",
    extra_tmp_heading: str = "# US-0067",
) -> Path:
    """Minimal repo: 4 H1 stories, max_stories=2 so oldest two would move."""
    _write(
        tmp / ".cursor" / "scratchpad.md",
        "\n".join(
            [
                f"ARCH_HOT_MAX_LINES=3500",
                f"ARCH_HOT_MAX_STORY_SECTIONS={max_stories}",
                "STATE_HOT_MAX_LINES=12000",
                "STATE_HOT_MAX_CHECKPOINTS=800",
                "PO_TO_TL_HOT_MAX_LINES=8000",
                "PO_TO_TL_HOT_MAX_SECTIONS=600",
            ]
            + (
                [f"ARCH_LINKAGE_AUTO_REPAIR={auto_repair}"]
                if auto_repair is not None
                else []
            )
        )
        + "\n",
    )
    _write(tmp / "docs" / "engineering" / "architecture.md", _mini_architecture())
    _write(tmp / "docs" / "engineering" / "state.md", "# Engineering State\n\n")
    _write(tmp / "tests" / "consumer_test.py", _consumer_src(consumer_heading))
    _write(tmp / "tests" / ".tmp-install" / "noise_test.py", _tmp_noise_src(extra_tmp_heading))
    _write(tmp / "tests" / "command_grep_test.py", _command_grep_src())
    _write(
        tmp / ".cursor" / "commands" / "architecture.md",
        "# command file\n# US-0999 — not a live architecture.md heading\n",
    )
    return tmp


class Us0129ContractTest(unittest.TestCase):
    def test_us0129_guard_discovers_contract_heading_set(self) -> None:
        """Marker 1 — AC-1 / DQ2: discover headings; exclude .tmp* and command greps."""
        g = _load_guard()
        live = g.discover_required_arch_headings(_repo_root())
        for tok in (
            "# US-0089",
            "# US-0090",
            "# US-0091",
            "# US-0093",
            "# BUG-0009",
            "# BUG-0010",
            "# BUG-0011",
            "# BUG-0012",
            "# US-0109",
        ):
            self.assertIn(tok, live, f"live discovery missing {tok}")
        self.assertNotIn("# US-0067", live)

        with tempfile.TemporaryDirectory() as td:
            repo = _make_synth_repo(Path(td))
            found = g.discover_required_arch_headings(repo)
            self.assertEqual(found, frozenset({"# US-0042"}))
            self.assertNotIn("# US-0067", found)
            self.assertNotIn("# US-0999", found)

    def test_us0129_pre_rollover_blocks_before_archive_write(self) -> None:
        """Marker 2 — AC-1 / AC-2 / DQ3: no pack/hot write on block; archiver unchanged."""
        g = _load_guard()
        eths_src = (_scripts_dir() / "enforce-triad-hot-surface.py").read_text(
            encoding="utf-8"
        )
        self.assertIn("def split_arch_stories(", eths_src)
        self.assertIn("- First archived heading:", eths_src)
        self.assertIn('"ARCH_HOT_MAX_LINES": "3500"', eths_src)
        guard_src = (_scripts_dir() / "arch_linkage_guard.py").read_text(encoding="utf-8")
        self.assertIn("split_arch_stories = _ETHS.split_arch_stories", guard_src)
        self.assertNotIn("def split_arch_stories(", guard_src)

        with tempfile.TemporaryDirectory() as td:
            repo = _make_synth_repo(Path(td))
            arch = _arch_file(repo)
            before = arch.read_bytes()
            archive_dir = repo / "docs" / "engineering" / "architecture-archive"
            archive_dir.mkdir(parents=True, exist_ok=True)
            before_packs = set(archive_dir.glob("architecture-pack-*.md"))
            rc, events = g.run_pre_guard(repo)
            self.assertEqual(rc, 1)
            self.assertTrue(events)
            self.assertEqual(arch.read_bytes(), before)
            self.assertEqual(set(archive_dir.glob("architecture-pack-*.md")), before_packs)

    def test_us0129_block_emits_arch_linkage_rollover_blocked_metadata(self) -> None:
        """Marker 3 — AC-2: story/bug id, missing heading, pack path, remediation."""
        g = _load_guard()
        with tempfile.TemporaryDirectory() as td:
            repo = _make_synth_repo(Path(td))
            rc, events = g.run_pre_guard(repo)
            self.assertEqual(rc, 1)
            self.assertGreaterEqual(len(events), 1)
            ev = events[0]
            line = ev.format_line()
            self.assertIn("ARCH_LINKAGE_ROLLOVER_BLOCKED", line)
            self.assertIn("story_id=US-0042", line)
            self.assertIn("missing_heading=# US-0042", line)
            self.assertIn("archive_pack_path=", line)
            self.assertIn("architecture-pack-", line)
            self.assertIn("ARCH_LINKAGE_AUTO_REPAIR=1", line)
            self.assertIn("remediation=", line)

    def test_us0129_auto_repair_default_off(self) -> None:
        """Marker 4 — AC-3 / DQ1: default-off; not in AUTONOMY_PRESET; no live =1."""
        g = _load_guard()
        self.assertFalse(g.auto_repair_enabled({}))
        self.assertFalse(g.auto_repair_enabled({"ARCH_LINKAGE_AUTO_REPAIR": "0"}))
        self.assertTrue(g.auto_repair_enabled({"ARCH_LINKAGE_AUTO_REPAIR": "1"}))

        pad = (_repo_root() / ".cursor" / "scratchpad.md").read_text(encoding="utf-8")
        live_assigns = [
            ln.strip()
            for ln in pad.splitlines()
            if ln.strip() and not ln.lstrip().startswith("#")
        ]
        self.assertFalse(
            any(ln.startswith("ARCH_LINKAGE_AUTO_REPAIR=1") for ln in live_assigns)
        )
        self.assertIn("# ARCH_LINKAGE_AUTO_REPAIR:", pad)

        preset = (_scripts_dir() / "autonomy_preset_lib.py").read_text(encoding="utf-8")
        self.assertNotIn("ARCH_LINKAGE_AUTO_REPAIR", preset)

        with tempfile.TemporaryDirectory() as td:
            repo = _make_synth_repo(Path(td))  # no live flag
            rc, _events = g.run_pre_guard(repo)
            self.assertEqual(rc, 1)

    def test_us0129_auto_repair_restores_h1_stub_idempotent(self) -> None:
        """Marker 5 — AC-3 / DQ8: stub before US-0089 tail; idempotent."""
        g = _load_guard()
        eths = g._ETHS
        with tempfile.TemporaryDirectory() as td:
            repo = _make_synth_repo(Path(td), auto_repair="1")
            rc_pre, _ = g.run_pre_guard(repo)
            self.assertEqual(rc_pre, 0)
            policy = eths.load_merged_policy(repo)
            result = eths.rollover_architecture(repo, policy, dry_run=False)
            self.assertIsNotNone(result)
            hot_after_roll = _arch_file(repo).read_text(encoding="utf-8")
            self.assertNotIn("# US-0042", hot_after_roll)
            self.assertIn("# US-0089", hot_after_roll)
            rc_post, events = g.run_post_guard(repo)
            self.assertEqual(rc_post, 0, msg=str(events))
            hot = _arch_file(repo).read_text(encoding="utf-8")
            self.assertIn("# US-0042 — Required consumer heading", hot)
            self.assertIn("Archived body in pack_ref:", hot)
            idx_stub = hot.find("# US-0042")
            idx_89 = hot.find("# US-0089")
            idx_90 = hot.find("# US-0090")
            self.assertGreater(idx_89, idx_stub)
            self.assertGreater(idx_90, idx_89)
            count_before = hot.count("# US-0042")
            rc2, _ = g.run_post_guard(repo)
            self.assertEqual(rc2, 0)
            hot2 = _arch_file(repo).read_text(encoding="utf-8")
            self.assertEqual(hot2.count("# US-0042"), count_before)
            state = (repo / "docs" / "engineering" / "state.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("Architecture linkage auto-repair audit (US-0129)", state)

    def test_us0129_post_rollover_verifies_active_linkage(self) -> None:
        """Marker 6 — AC-1 / AC-4 / DQ3: post-guard fail-closed when heading missing."""
        g = _load_guard()
        eths = g._ETHS
        with tempfile.TemporaryDirectory() as td:
            repo = _make_synth_repo(Path(td), max_stories=10)
            rc, events = g.run_post_guard(repo)
            self.assertEqual(rc, 0)
            self.assertEqual(events, [])

        with tempfile.TemporaryDirectory() as td:
            repo = _make_synth_repo(Path(td))  # repair off; unprotected rollover
            policy = eths.load_merged_policy(repo)
            eths.rollover_architecture(repo, policy, dry_run=False)
            rc, events = g.run_post_guard(repo)
            self.assertEqual(rc, 1)
            self.assertTrue(events)
            self.assertEqual(events[0].missing_heading, "# US-0042")
            self.assertIn("ARCH_LINKAGE_ROLLOVER_BLOCKED", events[0].format_line())

    def test_us0129_refresh_context_wires_pre_post_guard(self) -> None:
        """Marker 7 — AC-4: pre-guard → --rollover → post-guard → --check."""
        text = (_repo_root() / ".cursor" / "commands" / "refresh-context.md").read_text(
            encoding="utf-8"
        )
        pre = text.find("python scripts/arch_linkage_guard.py --pre")
        roll = text.find("python scripts/enforce-triad-hot-surface.py --rollover")
        post = text.find("python scripts/arch_linkage_guard.py --post")
        check = text.find("python scripts/enforce-triad-hot-surface.py --check")
        self.assertNotEqual(pre, -1)
        self.assertNotEqual(roll, -1)
        self.assertNotEqual(post, -1)
        self.assertNotEqual(check, -1)
        self.assertLess(pre, roll)
        self.assertLess(roll, post)
        self.assertLess(post, check)

    def test_us0129_b1_regression_unprotected_rollover_fails(self) -> None:
        """Marker 8 — AC-5: unprotected rollover drops a required heading (B-1 class)."""
        g = _load_guard()
        eths = g._ETHS
        with tempfile.TemporaryDirectory() as td:
            repo = _make_synth_repo(Path(td))
            policy = eths.load_merged_policy(repo)
            eths.rollover_architecture(repo, policy, dry_run=False)
            hot = _arch_file(repo).read_text(encoding="utf-8")
            self.assertNotIn("# US-0042", hot)
            self.assertIn("# US-0089", hot)
            required = g.discover_required_arch_headings(repo)
            self.assertIn("# US-0042", required)
            missing = [t for t in required if t not in hot]
            self.assertIn("# US-0042", missing)


if __name__ == "__main__":
    unittest.main()
