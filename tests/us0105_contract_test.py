"""US-0105: Eight `test_us0105_*` contract tests for Sovereign Memory.

DEC-0105 §12: scratchpad literals, directory bootstrap, JSONL v1 schemas,
injection digest char cap, decision dedup, mistake-tagging hooks, zero-overhead
default-off, compose regression guards.

Default-off: SOVEREIGN_MEMORY=0 → zero overhead.
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
import uuid
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _load_memory_lib():
    root = _repo_root()
    scripts_dir = str(root / "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    import sovereign_memory_lib as mod  # noqa: E402
    return mod


class US0105ScratchpadKeysTest(unittest.TestCase):
    """test_us0105_scratchpad_keys_literals (AC-1)."""

    def test_us0105_scratchpad_keys_literals(self) -> None:
        lib = _load_memory_lib()
        self.assertEqual(lib.SOVEREIGN_MEMORY_VALUES, {"0", "1"})
        self.assertEqual(lib.SOVEREIGN_MEMORY_DEFAULT, "0")
        self.assertEqual(lib.SOVEREIGN_MEMORY_TOP_N_DEFAULT, 5)
        self.assertEqual(lib.SOVEREIGN_MEMORY_TOP_K_DEFAULT, 3)
        self.assertEqual(lib.SOVEREIGN_MEMORY_MAX_CHARS_DEFAULT, 2048)
        self.assertEqual(lib.SOVEREIGN_MEMORY_JSONL_MAX_LINES_DEFAULT, 500)

        root = _repo_root()
        for pad_path in (root / ".cursor" / "scratchpad.md", root / "template" / ".cursor" / "scratchpad.md"):
            text = pad_path.read_text(encoding="utf-8")
            for key in (
                "SOVEREIGN_MEMORY",
                "SOVEREIGN_MEMORY_TOP_N",
                "SOVEREIGN_MEMORY_TOP_K",
                "SOVEREIGN_MEMORY_MAX_CHARS",
                "SOVEREIGN_MEMORY_JSONL_MAX_LINES",
            ):
                self.assertIn(key, text, f"missing {key} in {pad_path}")
            self.assertIn("SOVEREIGN_MEMORY=0", text)
            self.assertIn("SOVEREIGN_MEMORY_TOP_N=5", text)
            self.assertIn("SOVEREIGN_MEMORY_TOP_K=3", text)
            self.assertIn("SOVEREIGN_MEMORY_MAX_CHARS=2048", text)
            self.assertIn("SOVEREIGN_MEMORY_JSONL_MAX_LINES=500", text)
            self.assertIn("Sovereign Memory (US-0105 / DEC-0105)", text)

        self.assertFalse(lib.is_sovereign_memory_enabled({}))
        self.assertFalse(lib.is_sovereign_memory_enabled({lib.SOVEREIGN_MEMORY_KEY: "0"}))
        self.assertTrue(lib.is_sovereign_memory_enabled({lib.SOVEREIGN_MEMORY_KEY: "1"}))


class US0105DirectoryContractTest(unittest.TestCase):
    """test_us0105_sovereign_memory_directory_contract (AC-2)."""

    def test_us0105_sovereign_memory_directory_contract(self) -> None:
        lib = _load_memory_lib()
        root = _repo_root()
        for base in ("docs/engineering/sovereign-memory", "template/docs/engineering/sovereign-memory"):
            mem_dir = root / base
            self.assertTrue((mem_dir / ".gitkeep").is_file(), f"missing .gitkeep in {mem_dir}")
            retro = mem_dir / "retrospectives"
            self.assertTrue((retro / ".gitkeep").is_file(), f"missing retrospectives/.gitkeep in {mem_dir}")

        self.assertEqual(lib.MEMORY_DIR_REL.replace("\\", "/"), "docs/engineering/sovereign-memory")
        self.assertEqual(lib.ARCHIVE_DIR_REL.replace("\\", "/"), "docs/engineering/sovereign-memory-archive")
        self.assertEqual(lib.RETROSPECTIVES_SUBDIR, "retrospectives")
        self.assertEqual(set(lib.JSONL_FILENAMES.values()), {
            "decisions-log.jsonl",
            "mistakes.jsonl",
            "patterns.jsonl",
            "plan-drift-register.jsonl",
        })


class US0105JsonlSchemaContractTest(unittest.TestCase):
    """test_us0105_jsonl_schema_contract (AC-2 / AC-3)."""

    def test_us0105_jsonl_schema_contract(self) -> None:
        lib = _load_memory_lib()
        sample = lib.build_sample_decision()
        ok, err = lib.schema_check(sample, "decisions")
        self.assertTrue(ok, msg=err)

        mistake = lib.build_sample_mistake()
        ok_m, err_m = lib.schema_check(mistake, "mistakes")
        self.assertTrue(ok_m, msg=err_m)

        pattern = {
            "schema_version": 1,
            "ts": sample["ts"],
            "entry_id": str(uuid.uuid4()),
            "impact_score": 80,
            "text": "Always validate JSONL before append.",
            "tags": ["pattern"],
            "status": "active",
            "pattern_id": "validate-before-append",
            "applies_to": ["execute"],
        }
        ok_p, err_p = lib.schema_check(pattern, "patterns")
        self.assertTrue(ok_p, msg=err_p)

        drift = {
            "schema_version": 1,
            "ts": sample["ts"],
            "entry_id": str(uuid.uuid4()),
            "impact_score": 55,
            "text": "AC dropped without ledger entry.",
            "tags": ["drift"],
            "status": "active",
            "drift_type": "ac_drop",
            "from_artifact": "acceptance.md",
            "to_artifact": "acceptance.md",
        }
        ok_d, err_d = lib.schema_check(drift, "plan-drift")
        self.assertTrue(ok_d, msg=err_d)


class US0105InjectionDigestCharCapTest(unittest.TestCase):
    """test_us0105_injection_digest_char_cap (AC-3 / AC-4)."""

    def test_us0105_injection_digest_char_cap(self) -> None:
        lib = _load_memory_lib()

        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            mem = repo / "docs" / "engineering" / "sovereign-memory"
            mem.mkdir(parents=True)
            scratch = {lib.SOVEREIGN_MEMORY_KEY: "1", lib.SOVEREIGN_MEMORY_MAX_CHARS_KEY: "200"}

            sample = lib.build_sample_decision()
            sample["entry_id"] = str(uuid.uuid4())
            sample["impact_score"] = 90
            lib.append_decision(sample, repo, scratch)

            digest = lib.build_injection_digest(repo, scratch)
            self.assertLessEqual(digest.char_count, 200)
            self.assertIn("Recent learnings", digest.digest_text)

            block = lib.build_injection_digest_block(repo, scratch)
            self.assertIsNotNone(block)
            self.assertIn("sovereign_memory_digest", block or "")

        auto_ref = (_repo_root() / "docs" / "engineering" / "auto-orchestration-reference.md").read_text(encoding="utf-8")
        self.assertIn("sovereign_memory_digest", auto_ref)
        self.assertIn("build_injection_digest_block", auto_ref)


class US0105DecisionDedupBranchTest(unittest.TestCase):
    """test_us0105_decision_dedup_branch (AC-6)."""

    def test_us0105_decision_dedup_branch(self) -> None:
        lib = _load_memory_lib()

        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            scratch = {lib.SOVEREIGN_MEMORY_KEY: "1"}
            sample = lib.build_sample_decision()
            sample["entry_id"] = str(uuid.uuid4())

            ok1, code1 = lib.append_decision(sample, repo, scratch)
            self.assertTrue(ok1, msg=str(code1))

            dup = dict(sample)
            dup["entry_id"] = str(uuid.uuid4())
            ok2, code2 = lib.append_decision(dup, repo, scratch)
            self.assertFalse(ok2)
            self.assertEqual(code2, lib.ReasonCode.SOVEREIGN_MEMORY_DECISION_DUPLICATE)


class US0105MistakeTaggingLiteralsTest(unittest.TestCase):
    """test_us0105_mistake_tagging_literals (AC-6)."""

    def test_us0105_mistake_tagging_literals(self) -> None:
        lib = _load_memory_lib()
        self.assertEqual(lib.MISTAKE_TAG_VALUES, {
            "fix_failed",
            "revert_applied",
            "plan_fidelity_violation",
            "test_regression",
            "scope_creep",
        })

        auto = (_repo_root() / ".cursor" / "commands" / "auto.md").read_text(encoding="utf-8")
        execute = (_repo_root() / ".cursor" / "commands" / "execute.md").read_text(encoding="utf-8")
        for token in (
            "record_mistake_hook",
            "fix_failed",
            "revert_applied",
            "plan_fidelity_violation",
            "scope_creep",
            "FIX_FAILED",
            "REVERT_APPLIED",
            "PLAN_FIDELITY_VIOLATION",
            "PLAN_FIDELITY_SCOPE_GATE",
        ):
            self.assertIn(token, auto)
        self.assertIn("revert_applied", execute)
        self.assertIn("record_mistake_hook", execute)

        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            scratch = {lib.SOVEREIGN_MEMORY_KEY: "1"}
            ok, code = lib.record_mistake_hook(
                "fix_failed",
                text="Auto-loop exhausted fix attempts.",
                repo_root=repo,
                scratchpad=scratch,
            )
            self.assertTrue(ok, msg=str(code))
            path = lib.resolve_jsonl_path("mistakes", repo)
            self.assertTrue(path.is_file())


class US0105ZeroOverheadDefaultTest(unittest.TestCase):
    """test_us0105_zero_overhead_default (AC-1 / AC-4)."""

    def test_us0105_zero_overhead_default(self) -> None:
        lib = _load_memory_lib()

        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            scratch_off = {lib.SOVEREIGN_MEMORY_KEY: "0"}
            sample = lib.build_sample_decision()

            ok, code = lib.append_decision(sample, repo, scratch_off)
            self.assertFalse(ok)
            self.assertEqual(code, lib.ReasonCode.SOVEREIGN_MEMORY_DISABLED)
            self.assertFalse(lib.resolve_jsonl_path("decisions", repo).exists())

            digest = lib.build_injection_digest(repo, scratch_off)
            self.assertEqual(digest.digest_text, "")
            self.assertEqual(digest.entry_ids, [])
            self.assertIsNone(lib.build_injection_digest_block(repo, scratch_off))

            ok_m, code_m = lib.record_mistake_hook(
                "fix_failed",
                text="Should not write.",
                repo_root=repo,
                scratchpad=scratch_off,
            )
            self.assertFalse(ok_m)
            self.assertEqual(code_m, lib.ReasonCode.SOVEREIGN_MEMORY_DISABLED)


class US0105ComposeGuardsTest(unittest.TestCase):
    """test_us0105_compose_guards (AC-8)."""

    def test_us0105_compose_guards(self) -> None:
        root = _repo_root()
        research = (root / "docs" / "engineering" / "research.md").read_text(encoding="utf-8")
        self.assertIn("R-0093", research)
        self.assertNotIn("sovereign-memory/decisions-log.jsonl", research.split("## Schema")[0] if "## Schema" in research else research[:5000])

        dec0105 = (root / "decisions" / "DEC-0105.md").read_text(encoding="utf-8")
        self.assertIn("US-0029", dec0105)
        self.assertIn("US-0080", dec0105)
        self.assertIn("US-0103", dec0105)

        refresh = (root / ".cursor" / "commands" / "refresh-context.md").read_text(encoding="utf-8")
        self.assertIn("write_retrospective", refresh)
        self.assertIn("promote_from_ledger", refresh)
        self.assertIn("not injected v1", refresh.lower())


class US0105US0029ComposeTest(unittest.TestCase):
    """test_us0105_us0029_compose_no_research_schema_change (AC-8)."""

    def test_us0105_us0029_compose_no_research_schema_change(self) -> None:
        root = _repo_root()
        research = root / "docs" / "engineering" / "research.md"
        text = research.read_text(encoding="utf-8")
        self.assertIn("Entry format (per DEC-0011)", text)
        self.assertIn("R-xxxx ID format", text)
        self.assertIn("research.md", (root / "decisions" / "DEC-0105.md").read_text(encoding="utf-8"))
        lib = _load_memory_lib()
        sample = lib.build_sample_decision()
        self.assertEqual(sample.get("provenance_ref"), "R-0093")


class US0105US0080InjectionCharCapTest(unittest.TestCase):
    """test_us0105_us0080_injection_respects_char_cap (AC-8)."""

    def test_us0105_us0080_injection_respects_char_cap(self) -> None:
        lib = _load_memory_lib()
        scratch = (root := _repo_root()) / ".cursor" / "scratchpad.md"
        text = scratch.read_text(encoding="utf-8")
        self.assertIn("TOKEN_PROFILE", text)
        self.assertIn("SOVEREIGN_MEMORY_MAX_CHARS", text)

        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            mem = repo / "docs" / "engineering" / "sovereign-memory"
            mem.mkdir(parents=True)
            pad = {
                lib.SOVEREIGN_MEMORY_KEY: "1",
                lib.SOVEREIGN_MEMORY_MAX_CHARS_KEY: "64",
            }
            for idx in range(3):
                entry = lib.build_sample_decision()
                entry["entry_id"] = str(uuid.uuid4())
                entry["text"] = f"Long learning text number {idx} " * 5
                lib.append_decision(entry, repo, pad)

            digest = lib.build_injection_digest(repo, pad)
            self.assertLessEqual(digest.char_count, 64)


if __name__ == "__main__":
    unittest.main()
