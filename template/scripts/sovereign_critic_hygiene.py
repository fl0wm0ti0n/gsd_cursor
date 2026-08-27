#!/usr/bin/env python3
"""Operator-only sovereign-critic findings hygiene CLI (US-0127 / DEC-0110 §10).

Inventory:
  --report
  --resolve-nonblocking-for-run <orchestrator_run_id>
  --dry-run
  --confirm
  --self-test
  --all-phases
  --phase-id <phase_id>

Reason codes:
  HYGIENE_RESOLVE_CONFIRM_REQUIRED (exit 2)
  HYGIENE_RESOLVE_NO_CANDIDATES (exit 0 info)
  HYGIENE_RESOLVE_PARTIAL (exit 3)
  HYGIENE_RESOLVE_FAILED (exit 4)
  HYGIENE_REPORT_EMPTY (exit 0 info)
  HYGIENE_RESOLVE_PHASE_SCOPE_REQUIRED (exit 2)

Operator-only: /auto orchestrator does NOT call this during a run.
No advisory lock (Q3): /auto is single-threaded per repo; resolve_finding
already uses read-all + rewrite-all. Run only when the repo is quiet.
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from sovereign_critic_lib import (  # noqa: E402
    FINDINGS_PATH,
    auto_resolve_nonblocking_for_run,
    build_sample_finding,
    read_open_blocking,
    resolve_finding,
)

HYGIENE_RESOLVE_CONFIRM_REQUIRED = "HYGIENE_RESOLVE_CONFIRM_REQUIRED"
HYGIENE_RESOLVE_NO_CANDIDATES = "HYGIENE_RESOLVE_NO_CANDIDATES"
HYGIENE_RESOLVE_PARTIAL = "HYGIENE_RESOLVE_PARTIAL"
HYGIENE_RESOLVE_FAILED = "HYGIENE_RESOLVE_FAILED"
HYGIENE_REPORT_EMPTY = "HYGIENE_REPORT_EMPTY"
HYGIENE_RESOLVE_PHASE_SCOPE_REQUIRED = "HYGIENE_RESOLVE_PHASE_SCOPE_REQUIRED"

EXIT_OK = 0
EXIT_CONFIRM_OR_SCOPE = 2
EXIT_PARTIAL = 3
EXIT_FAILED = 4


def _emit(code: str, message: str = "") -> None:
    suffix = f" {message}" if message else ""
    print(f"[{code}]{suffix}")


def _load_rows(repo: Path) -> List[dict]:
    path = repo / FINDINGS_PATH
    if not path.is_file():
        return []
    rows: List[dict] = []
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not raw.strip():
            continue
        try:
            rows.append(json.loads(raw))
        except json.JSONDecodeError:
            continue
    return rows


def _is_open_nonblocking(obj: dict) -> bool:
    return obj.get("status") == "open" and obj.get("blocking") is False


def _candidates_for_run(
    rows: List[dict],
    orchestrator_run_id: str,
    *,
    all_phases: bool,
    phase_id: Optional[str],
) -> List[dict]:
    out: List[dict] = []
    for obj in rows:
        if not _is_open_nonblocking(obj):
            continue
        if str(obj.get("orchestrator_run_id")) != str(orchestrator_run_id):
            continue
        if all_phases:
            out.append(obj)
            continue
        if phase_id is not None and str(obj.get("phase_id")) == str(phase_id):
            out.append(obj)
    return out


def cmd_report(repo: Path) -> int:
    rows = _load_rows(repo)
    open_blocking = [r for r in rows if r.get("blocking") and r.get("status") == "open"]
    open_nonblocking = [r for r in rows if _is_open_nonblocking(r)]
    if not open_blocking and not open_nonblocking:
        _emit(HYGIENE_REPORT_EMPTY, "no open critic findings")
        return EXIT_OK
    print("open_blocking_count=" + str(len(open_blocking)))
    print("open_nonblocking_count=" + str(len(open_nonblocking)))
    for obj in open_nonblocking:
        print(
            "nonblocking\t"
            f"{obj.get('finding_id')}\t{obj.get('orchestrator_run_id')}\t"
            f"{obj.get('phase_id')}\t{obj.get('lens')}\t{obj.get('status')}"
        )
    for obj in open_blocking:
        print(
            "blocking\t"
            f"{obj.get('finding_id')}\t{obj.get('orchestrator_run_id')}\t"
            f"{obj.get('phase_id')}\t{obj.get('lens')}\t{obj.get('status')}"
        )
    return EXIT_OK


def cmd_resolve(
    repo: Path,
    orchestrator_run_id: str,
    *,
    dry_run: bool,
    confirm: bool,
    all_phases: bool,
    phase_id: Optional[str],
) -> int:
    if not all_phases and not phase_id:
        _emit(
            HYGIENE_RESOLVE_PHASE_SCOPE_REQUIRED,
            "pass --phase-id <phase_id> or --all-phases",
        )
        return EXIT_CONFIRM_OR_SCOPE
    if not dry_run and not confirm:
        _emit(HYGIENE_RESOLVE_CONFIRM_REQUIRED, "pass --confirm to apply")
        return EXIT_CONFIRM_OR_SCOPE

    rows = _load_rows(repo)
    candidates = _candidates_for_run(
        rows, orchestrator_run_id, all_phases=all_phases, phase_id=phase_id
    )
    if not candidates:
        _emit(HYGIENE_RESOLVE_NO_CANDIDATES, f"run={orchestrator_run_id}")
        return EXIT_OK

    print(f"candidates={len(candidates)}")
    for obj in candidates:
        print(
            f"{obj.get('finding_id')}\t{obj.get('orchestrator_run_id')}\t"
            f"{obj.get('phase_id')}\t{obj.get('lens')}"
        )

    if dry_run:
        print("dry-run: no JSONL mutation")
        return EXIT_OK

    path = repo / FINDINGS_PATH
    resolved = 0
    failed = 0
    if all_phases:
        phase_ids = sorted({str(obj.get("phase_id") or "") for obj in candidates})
        for pid in phase_ids:
            if not pid:
                failed += 1
                continue
            count, err = auto_resolve_nonblocking_for_run(repo, orchestrator_run_id, pid)
            resolved += count
            if err:
                failed += 1
    else:
        assert phase_id is not None
        count, err = auto_resolve_nonblocking_for_run(repo, orchestrator_run_id, phase_id)
        resolved += count
        if err:
            failed += 1

    if failed and resolved:
        _emit(HYGIENE_RESOLVE_PARTIAL, f"resolved={resolved} failed_groups={failed}")
        return EXIT_PARTIAL
    if failed and not resolved:
        _emit(HYGIENE_RESOLVE_FAILED, f"failed_groups={failed}")
        return EXIT_FAILED
    # Fallback: if helper returned 0 but we had candidates, try resolve_finding directly.
    if resolved == 0 and candidates:
        for obj in candidates:
            fid = str(obj.get("finding_id") or "")
            if fid and resolve_finding(path, fid, "resolved"):
                resolved += 1
            else:
                failed += 1
        if failed and resolved:
            _emit(HYGIENE_RESOLVE_PARTIAL, f"resolved={resolved} failed={failed}")
            return EXIT_PARTIAL
        if failed:
            _emit(HYGIENE_RESOLVE_FAILED, f"failed={failed}")
            return EXIT_FAILED
    print(f"resolved={resolved}")
    return EXIT_OK


def run_self_test() -> int:
    """Fixture-only self-test. No live critic spawn."""
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        (repo / "handoffs").mkdir()
        path = repo / FINDINGS_PATH
        row = build_sample_finding(
            orchestrator_run_id="hygiene-self-test",
            phase_id="execute",
            status="open",
            blocking=False,
            finding_id="hygiene-nb-001",
        )
        path.write_text(json.dumps(row) + "\n", encoding="utf-8")

        if cmd_report(repo) != EXIT_OK:
            print("self-test: report failed", file=sys.stderr)
            return 1
        rc = cmd_resolve(
            repo,
            "hygiene-self-test",
            dry_run=False,
            confirm=False,
            all_phases=False,
            phase_id=None,
        )
        if rc != EXIT_CONFIRM_OR_SCOPE:
            print("self-test: expected phase-scope required", file=sys.stderr)
            return 1
        rc = cmd_resolve(
            repo,
            "hygiene-self-test",
            dry_run=False,
            confirm=False,
            all_phases=False,
            phase_id="execute",
        )
        if rc != EXIT_CONFIRM_OR_SCOPE:
            print("self-test: expected confirm required", file=sys.stderr)
            return 1
        before = path.read_bytes()
        rc = cmd_resolve(
            repo,
            "hygiene-self-test",
            dry_run=True,
            confirm=False,
            all_phases=True,
            phase_id=None,
        )
        if rc != EXIT_OK or path.read_bytes() != before:
            print("self-test: dry-run mutated JSONL", file=sys.stderr)
            return 1
        rc = cmd_resolve(
            repo,
            "hygiene-self-test",
            dry_run=False,
            confirm=True,
            all_phases=False,
            phase_id="execute",
        )
        if rc != EXIT_OK:
            print("self-test: confirm resolve failed", file=sys.stderr)
            return 1
        if read_open_blocking(repo):
            print("self-test: unexpected open blocking after resolve", file=sys.stderr)
            return 1
        empty = Path(tmp) / "empty-repo"
        (empty / "handoffs").mkdir(parents=True)
        if cmd_report(empty) != EXIT_OK:
            print("self-test: empty report failed", file=sys.stderr)
            return 1
    print("[HYGIENE_SELF_TEST_OK]")
    return EXIT_OK


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Operator-only sovereign critic hygiene (US-0127)"
    )
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path.cwd(),
        help="Repository root (default: cwd)",
    )
    parser.add_argument("--report", action="store_true", help="Print open findings inventory")
    parser.add_argument(
        "--resolve-nonblocking-for-run",
        metavar="ORCHESTRATOR_RUN_ID",
        help="Resolve open non-blocking rows for this orchestrator_run_id",
    )
    parser.add_argument("--dry-run", action="store_true", help="List candidates; do not mutate JSONL")
    parser.add_argument("--confirm", action="store_true", help="Required to apply resolve")
    parser.add_argument("--self-test", action="store_true", help="Run fixture self-test")
    parser.add_argument(
        "--all-phases",
        action="store_true",
        help="Resolve across all phase_id values for the run",
    )
    parser.add_argument("--phase-id", help="Restrict resolve to this phase_id")
    args = parser.parse_args(argv)

    if args.self_test:
        return run_self_test()

    repo = args.repo.resolve()

    if args.report:
        return cmd_report(repo)

    if args.resolve_nonblocking_for_run:
        return cmd_resolve(
            repo,
            args.resolve_nonblocking_for_run,
            dry_run=args.dry_run,
            confirm=args.confirm,
            all_phases=args.all_phases,
            phase_id=args.phase_id,
        )

    parser.print_help()
    return EXIT_CONFIRM_OR_SCOPE


if __name__ == "__main__":
    raise SystemExit(main())
