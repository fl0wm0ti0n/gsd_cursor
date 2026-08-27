"""US-0127: Convergence critic conjunct — blocking-only open findings plus
non-blocking auto-resolve. 13 contract markers (AC-1..AC-4 + compose + R2).

All markers are static/fixture-based. No live critic spawn.
Marker 13 (T-007) lives in this file on purpose (ik_us0127_sprint_tanch_ceremony_overlap).
"""

from __future__ import annotations

import inspect
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, Dict, List


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _scripts_dir() -> Path:
    return _repo_root() / "scripts"


def _load_convergence():
    scripts = str(_scripts_dir())
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    import sovereign_convergence_lib as mod  # noqa: E402

    return mod


def _load_critic():
    scripts = str(_scripts_dir())
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    import sovereign_critic_lib as mod  # noqa: E402

    return mod


def _sample_finding(critic_lib, **overrides: Any) -> dict:
    row = critic_lib.build_sample_finding(
        orchestrator_run_id="us0127-fixture-run",
        phase_id="execute",
        status="open",
        blocking=False,
        finding_id="us0127-nb-001",
        lens="challenger",
        ts="2026-08-26T18:00:00.000Z",
    )
    row.update(overrides)
    return row


def _write_jsonl(repo: Path, rows: List[dict]) -> Path:
    path = repo / "handoffs" / "sovereign_critic_findings.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows),
        encoding="utf-8",
    )
    return path


def _run_hygiene(repo: Path, extra: List[str]) -> subprocess.CompletedProcess:
    script = _scripts_dir() / "sovereign_critic_hygiene.py"
    return subprocess.run(
        [sys.executable, str(script), "--repo", str(repo), *extra],
        capture_output=True,
        text=True,
        check=False,
    )


def _run_validate(jsonl_path: Path) -> subprocess.CompletedProcess:
    script = _scripts_dir() / "sovereign_critic_validate.py"
    return subprocess.run(
        [sys.executable, str(script), "--file", str(jsonl_path), "--enforce"],
        capture_output=True,
        text=True,
        check=False,
    )


class US0127OpenNonblockingPassesConvergence(unittest.TestCase):
    """Marker 1: test_us0127_open_nonblocking_passes_convergence (AC-1/AC-4)."""

    def test_us0127_open_nonblocking_passes_convergence(self) -> None:
        conv = _load_convergence()
        critic = _load_critic()
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            _write_jsonl(repo, [_sample_finding(critic, blocking=False, status="open")])
            result, skip = conv._eval_critic_resolved(repo)
            self.assertIsNone(skip)
            self.assertEqual(result.name, "critic_resolved")
            self.assertNotEqual(result.status, "fail")
            self.assertIn(result.status, ("pass", "skip"))
            self.assertNotEqual(
                result.reason_code, conv.ReasonCode.CONVERGENCE_CROSS_REVIEWER_OPEN.value
            )


class US0127OpenBlockingFailsConvergence(unittest.TestCase):
    """Marker 2: test_us0127_open_blocking_fails_convergence (AC-1/AC-4)."""

    def test_us0127_open_blocking_fails_convergence(self) -> None:
        conv = _load_convergence()
        critic = _load_critic()
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            _write_jsonl(
                repo,
                [
                    _sample_finding(
                        critic,
                        blocking=True,
                        status="open",
                        finding_id="us0127-b-001",
                    )
                ],
            )
            result, skip = conv._eval_critic_resolved(repo)
            self.assertIsNone(skip)
            self.assertEqual(result.status, "fail")
            self.assertEqual(
                result.reason_code, conv.ReasonCode.CONVERGENCE_CROSS_REVIEWER_OPEN.value
            )


class US0127AutoresolveIdempotentOnRerun(unittest.TestCase):
    """Marker 3: test_us0127_autoresolve_idempotent_on_rerun (AC-2/AC-4)."""

    def test_us0127_autoresolve_idempotent_on_rerun(self) -> None:
        critic = _load_critic()
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            path = _write_jsonl(repo, [_sample_finding(critic)])
            first, err1 = critic.auto_resolve_nonblocking_for_run(
                repo, "us0127-fixture-run", "execute"
            )
            self.assertIsNone(err1)
            self.assertGreaterEqual(first, 1)
            after_first = path.read_text(encoding="utf-8")
            second, err2 = critic.auto_resolve_nonblocking_for_run(
                repo, "us0127-fixture-run", "execute"
            )
            self.assertIsNone(err2)
            self.assertEqual(second, 0)
            self.assertEqual(path.read_text(encoding="utf-8"), after_first)
            rows = [json.loads(ln) for ln in after_first.splitlines() if ln.strip()]
            self.assertTrue(all(r.get("status") == "resolved" for r in rows))


class US0127AutoresolvePreservesAuditTrail(unittest.TestCase):
    """Marker 4: test_us0127_autoresolve_preserves_audit_trail (AC-2/AC-4)."""

    def test_us0127_autoresolve_preserves_audit_trail(self) -> None:
        critic = _load_critic()
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            original = _sample_finding(critic)
            path = _write_jsonl(repo, [original])
            critic.auto_resolve_nonblocking_for_run(repo, "us0127-fixture-run", "execute")
            rows = [
                json.loads(ln)
                for ln in path.read_text(encoding="utf-8").splitlines()
                if ln.strip()
            ]
            self.assertEqual(len(rows), 1)
            row = rows[0]
            self.assertEqual(row["status"], "resolved")
            self.assertEqual(row["finding_id"], original["finding_id"])
            self.assertEqual(row["lens"], original["lens"])
            self.assertEqual(row["ts"], original["ts"])
            self.assertEqual(row["orchestrator_run_id"], original["orchestrator_run_id"])
            self.assertEqual(row["phase_id"], original["phase_id"])


class US0127AutoresolveSkipsWhenBlockingOpen(unittest.TestCase):
    """Marker 5: test_us0127_autoresolve_skips_when_blocking_open (AC-2/AC-4)."""

    def test_us0127_autoresolve_skips_when_blocking_open(self) -> None:
        critic = _load_critic()
        cmd = (_repo_root() / ".cursor" / "commands" / "sovereign-critic.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("if read_open_blocking(repo) == []:", cmd)
        self.assertIn(
            "auto_resolve_nonblocking_for_run(repo, orchestrator_run_id, phase_id)",
            cmd,
        )
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            blocking = _sample_finding(
                critic, blocking=True, status="open", finding_id="us0127-b-002"
            )
            nonblocking = _sample_finding(
                critic, blocking=False, status="open", finding_id="us0127-nb-002"
            )
            path = _write_jsonl(repo, [blocking, nonblocking])
            before = path.read_text(encoding="utf-8")
            open_blocking = critic.read_open_blocking(repo)
            self.assertTrue(open_blocking)
            if open_blocking == []:
                critic.auto_resolve_nonblocking_for_run(
                    repo, "us0127-fixture-run", "execute"
                )
            self.assertEqual(path.read_text(encoding="utf-8"), before)
            rows = [json.loads(ln) for ln in before.splitlines() if ln.strip()]
            self.assertTrue(any(r.get("finding_id") == "us0127-nb-002" and r.get("status") == "open" for r in rows))


class US0127HygieneReport(unittest.TestCase):
    """Marker 6: test_us0127_hygiene_report (AC-3)."""

    def test_us0127_hygiene_report(self) -> None:
        critic = _load_critic()
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            _write_jsonl(repo, [_sample_finding(critic)])
            proc = _run_hygiene(repo, ["--report"])
            self.assertEqual(proc.returncode, 0, msg=proc.stderr)
            combined = proc.stdout + proc.stderr
            self.assertIn("open_nonblocking_count=", combined)
            self.assertIn("us0127-nb-001", combined)


class US0127HygieneDryRun(unittest.TestCase):
    """Marker 7: test_us0127_hygiene_dry_run (AC-3)."""

    def test_us0127_hygiene_dry_run(self) -> None:
        critic = _load_critic()
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            path = _write_jsonl(repo, [_sample_finding(critic)])
            before = path.read_bytes()
            proc = _run_hygiene(
                repo,
                [
                    "--resolve-nonblocking-for-run",
                    "us0127-fixture-run",
                    "--dry-run",
                    "--all-phases",
                ],
            )
            self.assertEqual(proc.returncode, 0, msg=proc.stderr)
            self.assertEqual(path.read_bytes(), before)
            combined = proc.stdout + proc.stderr
            self.assertIn("us0127-nb-001", combined)
            self.assertIn("dry-run", combined.lower())


class US0127HygieneConfirmRequired(unittest.TestCase):
    """Marker 8: test_us0127_hygiene_confirm_required (AC-3)."""

    def test_us0127_hygiene_confirm_required(self) -> None:
        critic = _load_critic()
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            _write_jsonl(repo, [_sample_finding(critic)])
            proc = _run_hygiene(
                repo,
                [
                    "--resolve-nonblocking-for-run",
                    "us0127-fixture-run",
                    "--phase-id",
                    "execute",
                ],
            )
            self.assertEqual(proc.returncode, 2, msg=proc.stdout + proc.stderr)
            combined = proc.stdout + proc.stderr
            self.assertIn("HYGIENE_RESOLVE_CONFIRM_REQUIRED", combined)


class US0127HygieneSelfTest(unittest.TestCase):
    """Marker 9: test_us0127_hygiene_self_test (AC-3)."""

    def test_us0127_hygiene_self_test(self) -> None:
        proc = _run_hygiene(_repo_root(), ["--self-test"])
        self.assertEqual(proc.returncode, 0, msg=proc.stdout + proc.stderr)
        self.assertIn("HYGIENE_SELF_TEST_OK", proc.stdout + proc.stderr)


class US0127HygienePhaseScopeRequired(unittest.TestCase):
    """Marker 10: test_us0127_hygiene_phase_scope_required (AC-3)."""

    def test_us0127_hygiene_phase_scope_required(self) -> None:
        critic = _load_critic()
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            _write_jsonl(repo, [_sample_finding(critic)])
            proc = _run_hygiene(
                repo, ["--resolve-nonblocking-for-run", "us0127-fixture-run"]
            )
            self.assertEqual(proc.returncode, 2, msg=proc.stdout + proc.stderr)
            combined = proc.stdout + proc.stderr
            self.assertIn("HYGIENE_RESOLVE_PHASE_SCOPE_REQUIRED", combined)


class US0127ComposeUs0104ReadOpenBlockingUnchanged(unittest.TestCase):
    """Marker 11: test_us0127_compose_us0104_read_open_blocking_unchanged (DQ7)."""

    def test_us0127_compose_us0104_read_open_blocking_unchanged(self) -> None:
        critic = _load_critic()
        src = inspect.getsource(critic.read_open_blocking)
        self.assertIn('obj.get("blocking") and obj.get("status") == "open"', src)
        sig = inspect.signature(critic.read_open_blocking)
        self.assertIn("repo", sig.parameters)
        resolve_src = inspect.getsource(critic.resolve_finding)
        self.assertIn("finding_id", inspect.signature(critic.resolve_finding).parameters)
        self.assertIn("status", inspect.signature(critic.resolve_finding).parameters)
        self.assertIn("write_text", resolve_src)
        schema = critic.FINDING_REQUIRED_FIELDS
        self.assertIn("blocking", schema)
        self.assertIn("status", schema)
        self.assertIn("finding_id", schema)


class US0127ComposeUs0110Conjunct3Contract(unittest.TestCase):
    """Marker 12: test_us0127_compose_us0110_conjunct3_contract (DQ8)."""

    def test_us0127_compose_us0110_conjunct3_contract(self) -> None:
        conv = _load_convergence()
        self.assertEqual(
            conv.CONVERGENCE_CONJUNCTS,
            (
                "backlog_clear",
                "zero_deferrals",
                "critic_resolved",
                "smoke_green",
                "ledger_clean",
            ),
        )
        self.assertEqual(
            conv.ReasonCode.CONVERGENCE_CROSS_REVIEWER_OPEN.value,
            "CONVERGENCE_CROSS_REVIEWER_OPEN",
        )
        self.assertIn("CONVERGENCE_CROSS_REVIEWER_OPEN", conv.REASON_CODES)
        eval_src = inspect.getsource(conv._eval_critic_resolved)
        self.assertIn("critic_register_not_yet_deployed", eval_src)
        self.assertIn("_qa_findings_has_open_critic", eval_src)
        self.assertIn("jsonl_authoritative", eval_src)
        helper_src = inspect.getsource(conv._critic_jsonl_has_open)
        self.assertIn("read_open_blocking", helper_src)
        self.assertNotIn('obj.get("blocking", True)', helper_src)


class US0127ValidateRejectsMissingBlocking(unittest.TestCase):
    """Marker 13: test_us0127_validate_rejects_missing_blocking (R2 / T-007)."""

    def test_us0127_validate_rejects_missing_blocking(self) -> None:
        critic = _load_critic()
        with tempfile.TemporaryDirectory() as tmp:
            row = _sample_finding(critic)
            del row["blocking"]
            self.assertNotIn("blocking", row)
            path = Path(tmp) / "missing-blocking.jsonl"
            path.write_text(json.dumps(row) + "\n", encoding="utf-8")
            proc = _run_validate(path)
            self.assertNotEqual(proc.returncode, 0, msg=proc.stdout + proc.stderr)
            combined = proc.stdout + proc.stderr
            self.assertTrue(
                "blocking" in combined.lower() or "missing fields" in combined.lower(),
                msg=combined,
            )


if __name__ == "__main__":
    unittest.main()
