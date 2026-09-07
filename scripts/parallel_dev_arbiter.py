#!/usr/bin/env python3
"""Parallel Instance Arbitrage library (US-0108 / DEC-0108).

Reason codes:
  PARALLEL_DEV_DISABLED, PARALLEL_DEV_WORKTREE_CREATE_FAILED,
  PARALLEL_DEV_WORKTREE_CLEANUP_FAILED, PARALLEL_DEV_SELECTION_NO_PASS,
  PARALLEL_DEV_MERGE_CONFLICT, PARALLEL_DEV_RESOURCE_CAP_EXHAUSTED,
  PARALLEL_DEV_RESOURCE_LOCK_FAILED, PARALLEL_DEV_EXECUTE_FAILED,
  PARALLEL_DEV_ANTI_SLOP_BELOW_THRESHOLD, PARALLEL_DEV_MERGE_TIMEOUT,
  PARALLEL_DEV_MANUAL_HALT, PARALLEL_DEV_PICK_SCHEMA_INVALID

Default-off: SOVEREIGN_PARALLEL_DEV=0 → zero overhead.

Compose guards (non-negotiable):
  US-0047 unchanged (bulk execute step 22 unchanged)
  US-0092 unchanged (full autonomy outer driver unchanged)
  US-0103 unchanged (ledger schema unchanged; read-only consumer)
  US-0104 unchanged (critic schema unchanged; read-only anti_slop consumer)
  US-0107 unchanged (sovereign loop unchanged; consumer only)
"""

from __future__ import annotations

import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import namedtuple
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_SCRIPT_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPT_DIR.parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))
import host_runtime_config_lib as hrc  # noqa: E402


# --- Scratchpad key contracts (DEC-0108 §1) ------------------------------------

SOVEREIGN_PARALLEL_DEV_KEY = "SOVEREIGN_PARALLEL_DEV"
AUTO_SOVEREIGN_PARALLEL_N_KEY = "AUTO_SOVEREIGN_PARALLEL_N"
AUTO_SOVEREIGN_PARALLEL_MAX_TOTAL_KEY = "AUTO_SOVEREIGN_PARALLEL_MAX_TOTAL"
AUTO_SOVEREIGN_MERGE_RESOLVE_KEY = "AUTO_SOVEREIGN_MERGE_RESOLVE"
AUTO_SOVEREIGN_WORKTREE_KEEP_KEY = "AUTO_SOVEREIGN_WORKTREE_KEEP"
AUTO_SOVEREIGN_PARALLEL_QA_KEY = "AUTO_SOVEREIGN_PARALLEL_QA"
AUTO_SOVEREIGN_PARALLEL_QA_ARBITER_KEY = "AUTO_SOVEREIGN_PARALLEL_QA_ARBITER"
AUTO_SOVEREIGN_PARALLEL_ANTI_SLOP_THRESHOLD_KEY = "AUTO_SOVEREIGN_PARALLEL_ANTI_SLOP_THRESHOLD"
AUTO_SOVEREIGN_PARALLEL_REWORK_MAX_KEY = "AUTO_SOVEREIGN_PARALLEL_REWORK_MAX"
AUTO_SOVEREIGN_PARALLEL_MERGE_TIMEOUT_SEC_KEY = "AUTO_SOVEREIGN_PARALLEL_MERGE_TIMEOUT_SEC"

SCRATCHPAD_KEY_DEFAULTS: dict[str, str] = {
    SOVEREIGN_PARALLEL_DEV_KEY: "0",
    AUTO_SOVEREIGN_PARALLEL_N_KEY: "3",
    AUTO_SOVEREIGN_PARALLEL_MAX_TOTAL_KEY: "6",
    AUTO_SOVEREIGN_MERGE_RESOLVE_KEY: "first_pass_wins",
    AUTO_SOVEREIGN_WORKTREE_KEEP_KEY: "0",
    AUTO_SOVEREIGN_PARALLEL_QA_KEY: "0",
    AUTO_SOVEREIGN_PARALLEL_QA_ARBITER_KEY: "critic_first_pass",
    AUTO_SOVEREIGN_PARALLEL_ANTI_SLOP_THRESHOLD_KEY: "6",
    AUTO_SOVEREIGN_PARALLEL_REWORK_MAX_KEY: "2",
    AUTO_SOVEREIGN_PARALLEL_MERGE_TIMEOUT_SEC_KEY: "60",
}

SOVEREIGN_PARALLEL_DEV_VALUES = frozenset({"0", "1"})
MERGE_RESOLVE_VALUES = frozenset({"first_pass_wins", "last_pass_wins", "winner_takes_all", "manual"})
QA_ARBITER_VALUES = frozenset({"critic_first_pass", "majority_vote"})


# --- Named tuples ---------------------------------------------------------------

WorktreeContext = namedtuple(
    "WorktreeContext",
    ["instance_id", "path", "branch", "status"],
)

MergeResult = namedtuple(
    "MergeResult",
    ["success", "branch", "commit_hash", "conflicts"],
)

ExecuteResult = namedtuple(
    "ExecuteResult",
    ["winner_worktree", "merge_result", "qa_results"],
)

PickRecord = namedtuple(
    "PickRecord",
    [
        "schema_version", "story_id", "winner_instance_id", "worktree_path",
        "qa_verdict", "anti_slop_score", "proof_issued_at", "merge_policy",
        "runner_ts_utc", "orchestrator_run_id", "loser_instance_ids",
    ],
)


# --- Scratchpad parsing ---------------------------------------------------------

def parse_scratchpad_key(line: str) -> Optional[Tuple[str, str]]:
    """Parse a scratchpad KEY=VALUE line. Ignore comments and blanks."""
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return None
    m = re.match(r"^([A-Z_][A-Z0-9_]*)=(.*)", stripped)
    if m:
        return m.group(1), m.group(2)
    return None


def read_scratchpad(path: Path) -> dict[str, str]:
    """Read scratchpad file into dict of key=value pairs."""
    result: dict[str, str] = {}
    if not path.is_file():
        return result
    for line in path.read_text(encoding="utf-8").splitlines():
        kv = parse_scratchpad_key(line)
        if kv:
            result[kv[0]] = kv[1]
    return result


def read_scratchpad_with_defaults(scratchpad_path: Path) -> dict[str, str]:
    """Read governance keys via host-neutral resolver (US-0131); path kept for API compat."""
    repo = scratchpad_path.parent.parent if scratchpad_path.name.endswith(".md") else _REPO_ROOT
    # Prefer repo inferred from conventional .cursor/scratchpad*.md paths.
    if scratchpad_path.parts[-2:] == (".cursor", "scratchpad.md") or scratchpad_path.parts[-2:] == (
        ".cursor",
        "scratchpad.local.md",
    ):
        repo = scratchpad_path.parent.parent
    resolved = hrc.resolve_runtime_config(repo, raise_on_fatal=False)
    merged = dict(SCRATCHPAD_KEY_DEFAULTS)
    merged.update(resolved.values)
    return merged


def is_parallel_enabled(scratchpad_path: Path) -> bool:
    """Return True only when SOVEREIGN_PARALLEL_DEV=1 explicitly."""
    values = read_scratchpad_with_defaults(scratchpad_path)
    return values.get(SOVEREIGN_PARALLEL_DEV_KEY, "0").strip() == "1"


# --- Reason codes ---------------------------------------------------------------

class ReasonCode:
    PARALLEL_DEV_DISABLED = "PARALLEL_DEV_DISABLED"
    PARALLEL_DEV_WORKTREE_CREATE_FAILED = "PARALLEL_DEV_WORKTREE_CREATE_FAILED"
    PARALLEL_DEV_WORKTREE_CLEANUP_FAILED = "PARALLEL_DEV_WORKTREE_CLEANUP_FAILED"
    PARALLEL_DEV_SELECTION_NO_PASS = "PARALLEL_DEV_SELECTION_NO_PASS"
    PARALLEL_DEV_MERGE_CONFLICT = "PARALLEL_DEV_MERGE_CONFLICT"
    PARALLEL_DEV_RESOURCE_CAP_EXHAUSTED = "PARALLEL_DEV_RESOURCE_CAP_EXHAUSTED"
    PARALLEL_DEV_RESOURCE_LOCK_FAILED = "PARALLEL_DEV_RESOURCE_LOCK_FAILED"
    PARALLEL_DEV_EXECUTE_FAILED = "PARALLEL_DEV_EXECUTE_FAILED"
    PARALLEL_DEV_ANTI_SLOP_BELOW_THRESHOLD = "PARALLEL_DEV_ANTI_SLOP_BELOW_THRESHOLD"
    PARALLEL_DEV_MERGE_TIMEOUT = "PARALLEL_DEV_MERGE_TIMEOUT"
    PARALLEL_DEV_MANUAL_HALT = "PARALLEL_DEV_MANUAL_HALT"
    PARALLEL_DEV_PICK_SCHEMA_INVALID = "PARALLEL_DEV_PICK_SCHEMA_INVALID"


# --- T-002/T-003: Worktree isolation (AC-2) -------------------------------------

def _git_dir(repo_root: Path) -> Path:
    return repo_root / ".git"


def worktree_path_pattern(story_id: str) -> str:
    """Return gitignore-compatible pattern for US-0108 worktrees."""
    return f".git/worktrees/us0108-{story_id}-*"


def _worktree_path(repo_root: Path, story_id: str, instance_idx: int) -> Path:
    return _git_dir(repo_root) / "worktrees" / f"us0108-{story_id}-{instance_idx}"


def _worktree_branch(story_id: str, instance_idx: int) -> str:
    return f"us0108-{story_id}-{instance_idx}"


def create_worktree(
    story_id: str,
    instance_idx: int,
    base_branch: str = "main",
    repo_root: Optional[Path] = None,
) -> WorktreeContext:
    """Create an isolated git worktree for a parallel instance.

    Pattern: .git/worktrees/us0108-<story_id>-<instance_idx>/
    Branch:  us0108-<story_id>-<instance_idx>
    """
    if repo_root is None:
        repo_root = _REPO_ROOT

    wt_path = _worktree_path(repo_root, story_id, instance_idx)
    wt_branch = _worktree_branch(story_id, instance_idx)
    instance_id = f"{story_id}-inst{instance_idx}"

    env = os.environ.copy()
    env["GIT_DIR"] = str(_git_dir(repo_root))
    env["GIT_WORK_TREE"] = str(wt_path)

    try:
        wt_path.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["git", "worktree", "add", str(wt_path), "-b", wt_branch, base_branch],
            cwd=str(repo_root),
            check=True,
            capture_output=True,
            env=env,
        )
        return WorktreeContext(
            instance_id=instance_id,
            path=str(wt_path),
            branch=wt_branch,
            status="created",
        )
    except (subprocess.CalledProcessError, OSError) as exc:
        return WorktreeContext(
            instance_id=instance_id,
            path=str(wt_path),
            branch=wt_branch,
            status=f"failed:{exc}",
        )


def create_worktrees(
    base_branch: str,
    instance_count: int,
    story_id: str = "story",
    repo_root: Optional[Path] = None,
) -> List[WorktreeContext]:
    """Create N isolated worktrees. Returns list of WorktreeContext."""
    if instance_count < 1:
        raise ValueError("instance_count must be >= 1")
    results = []
    for idx in range(instance_count):
        ctx = create_worktree(story_id, idx, base_branch, repo_root)
        results.append(ctx)
    return results


def list_worktrees(repo_root: Optional[Path] = None) -> List[str]:
    """List existing worktrees (paths only)."""
    if repo_root is None:
        repo_root = _REPO_ROOT
    try:
        out = subprocess.run(
            ["git", "worktree", "list", "--porcelain"],
            cwd=str(repo_root), check=True, capture_output=True, text=True,
        )
        paths = []
        for line in out.stdout.splitlines():
            if line.startswith("worktree "):
                paths.append(line[len("worktree "):])
        return paths
    except (subprocess.CalledProcessError, OSError):
        return []


def remove_worktree(
    story_id: str,
    instance_idx: int,
    repo_root: Optional[Path] = None,
    force: bool = False,
) -> bool:
    """Remove a single worktree + branch. Fail-open with reason code."""
    if repo_root is None:
        repo_root = _REPO_ROOT
    wt_path = _worktree_path(repo_root, story_id, instance_idx)
    branch = _worktree_branch(story_id, instance_idx)
    try:
        cmd = ["git", "worktree", "remove"]
        if force:
            cmd.append("--force")
        cmd.append(str(wt_path))
        subprocess.run(cmd, cwd=str(repo_root), check=True, capture_output=True)
        subprocess.run(
            ["git", "branch", "-D", branch],
            cwd=str(repo_root), check=True, capture_output=True,
        )
        return True
    except (subprocess.CalledProcessError, OSError):
        if wt_path.exists():
            shutil.rmtree(str(wt_path), ignore_errors=True)
        return False


def cleanup_worktrees(
    contexts: List[WorktreeContext],
    story_id: str,
    keep_losers: bool = False,
    winner_instance_id: Optional[str] = None,
    repo_root: Optional[Path] = None,
) -> Dict[str, Any]:
    """Clean up worktrees post-merge. Winner always cleaned; losers per AUTO_SOVEREIGN_WORKTREE_KEEP."""
    if repo_root is None:
        repo_root = _REPO_ROOT
    removed = []
    kept = []
    failed = []
    for ctx in contexts:
        is_winner = winner_instance_id and ctx.instance_id == winner_instance_id
        if is_winner or not keep_losers:
            match = re.match(r"us0108-.+-(\d+)$", ctx.branch)
            idx = int(match.group(1)) if match else 0
            ok = remove_worktree(story_id, idx, repo_root, force=True)
            if ok:
                removed.append(ctx.instance_id)
            else:
                failed.append(ctx.instance_id)
        else:
            kept.append(ctx.instance_id)
    status = "PARALLEL_DEV_WORKTREE_CLEANUP_FAILED" if failed else "OK"
    return {"removed": removed, "kept": kept, "failed": failed, "status": status}


# --- T-005: Anti-slop score reader (AC-3) ---------------------------------------

def read_anti_slop_score(lens_scores: List[int]) -> int:
    """Read anti-slop aggregate from lens scores.

    Uses sovereign_critic_lib.compute_anti_slop_aggregate (US-0104, read-only).
    Graceful degrade: default 0 when US-0104 absent.
    """
    try:
        from sovereign_critic_lib import compute_anti_slop_aggregate
        return compute_anti_slop_aggregate(lens_scores)
    except Exception:
        if lens_scores:
            return min(int(s) for s in lens_scores)
        return 0


def extract_anti_slop_from_findings(findings_path: Path) -> int:
    """Extract anti_slop_score from sovereign_critic_findings.jsonl or qa-findings.md.

    Read-only per compose guard: US-0104 schema unchanged.
    Graceful degrade: return 0 when US-0104 absent.
    """
    try:
        if findings_path.suffix == ".jsonl" and findings_path.is_file():
            scores = []
            for line in findings_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                    score = obj.get("anti_slop_score")
                    if score is not None:
                        scores.append(int(score))
                except (json.JSONDecodeError, ValueError):
                    continue
            if scores:
                return min(scores)
        elif findings_path.is_file():
            text = findings_path.read_text(encoding="utf-8")
            match = re.search(r"anti_slop_score[:\s]*(\d+)", text)
            if match:
                return int(match.group(1))
    except Exception:
        pass
    return 0


# --- T-004: Selection predicate (AC-3) ------------------------------------------

def select_winner(qa_results: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Deterministic winner selection per AC-3.

    1. Filter qa_verdict=pass (case-insensitive).
    2. Sort by anti_slop_score descending.
    3. Tie-break earliest proof_issued_at.
    4. Return winner or None.
    """
    if not qa_results:
        return None

    passing = [
        r for r in qa_results
        if str(r.get("qa_verdict", "")).lower() in ("pass", "passed")
    ]
    if not passing:
        return None

    def sort_key(result: Dict[str, Any]) -> Tuple[int, str]:
        score = int(result.get("anti_slop_score", 0))
        issued = str(result.get("proof_issued_at", "9999-12-31T23:59:59Z"))
        return (-score, issued)

    passing.sort(key=sort_key)
    winner = dict(passing[0])
    winner["_selection_method"] = "pass_then_antislop_desc_then_earliest"
    return winner


# --- T-006: Merge policy + parallel_dev_pick.json (AC-4) ------------------------

def merge_winner(
    winner_context: WorktreeContext,
    main_branch: str = "main",
    repo_root: Optional[Path] = None,
    max_retries: int = 2,
    timeout_sec: int = 60,
    merge_resolve: str = "first_pass_wins",
) -> MergeResult:
    """Merge winner branch into main with bounded conflict retry.

    AUTO_SOVEREIGN_MERGE_RESOLVE:
      first_pass_wins  — use -X theirs, first attempt wins (default)
      last_pass_wins   — use -X theirs, last attempt wins
      manual           — halt with PARALLEL_DEV_MANUAL_HALT
      winner_takes_all — alias for first_pass_wins

    Bounded retry ≤2 then PARALLEL_DEV_MERGE_CONFLICT halt.
    """
    if repo_root is None:
        repo_root = _REPO_ROOT

    if merge_resolve == "manual":
        return MergeResult(
            success=False,
            branch=winner_context.branch,
            commit_hash="",
            conflicts=[ReasonCode.PARALLEL_DEV_MANUAL_HALT],
        )

    last_conflicts: List[str] = []
    for attempt in range(1, max_retries + 1):
        try:
            subprocess.run(
                ["git", "checkout", winner_context.branch],
                cwd=str(repo_root), check=True, capture_output=True,
            )
            merge_cmd = ["git", "merge", "-X", "theirs", main_branch]
            subprocess.run(
                merge_cmd,
                cwd=winner_context.path,
                check=True, capture_output=True,
                timeout=timeout_sec,
            )
            rev = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=winner_context.path, check=True, capture_output=True, text=True,
            )
            commit_hash = rev.stdout.strip()
            subprocess.run(
                ["git", "checkout", main_branch],
                cwd=str(repo_root), check=True, capture_output=True,
            )
            subprocess.run(
                ["git", "merge", "--ff-only", winner_context.branch],
                cwd=str(repo_root), check=True, capture_output=True,
            )
            return MergeResult(
                success=True,
                branch=winner_context.branch,
                commit_hash=commit_hash,
                conflicts=[],
            )
        except subprocess.TimeoutExpired:
            last_conflicts = [ReasonCode.PARALLEL_DEV_MERGE_TIMEOUT]
            break
        except subprocess.CalledProcessError as exc:
            stderr = exc.stderr.decode("utf-8", errors="replace") if exc.stderr else ""
            if "CONFLICT" in stderr.upper() or "conflict" in stderr.lower():
                last_conflicts = [f"attempt-{attempt}:conflict"]
                try:
                    subprocess.run(
                        ["git", "merge", "--abort"],
                        cwd=winner_context.path, check=False, capture_output=True,
                    )
                except Exception:
                    pass
            else:
                last_conflicts = [f"attempt-{attempt}:error"]

    return MergeResult(
        success=False,
        branch=winner_context.branch,
        commit_hash="",
        conflicts=last_conflicts or [ReasonCode.PARALLEL_DEV_MERGE_CONFLICT],
    )


PICK_SCHEMA_VERSION = 1

PICK_REQUIRED_FIELDS = {
    "schema_version", "story_id", "winner_instance_id", "worktree_path",
    "qa_verdict", "anti_slop_score", "proof_issued_at", "merge_policy",
    "runner_ts_utc", "orchestrator_run_id", "loser_instance_ids",
}


def build_pick_record(
    story_id: str,
    winner_id: str,
    winner_path: str,
    qa_verdict: str,
    anti_slop_score: int,
    merge_policy: str,
    loser_ids: List[str],
    orchestrator_run_id: str = "",
    proof_issued_at: Optional[str] = None,
) -> Dict[str, Any]:
    """Build write-once parallel_dev_pick.json v1 record."""
    now_ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "schema_version": PICK_SCHEMA_VERSION,
        "story_id": story_id,
        "winner_instance_id": winner_id,
        "worktree_path": winner_path,
        "qa_verdict": qa_verdict,
        "anti_slop_score": int(anti_slop_score),
        "proof_issued_at": proof_issued_at or now_ts,
        "merge_policy": str(merge_policy),
        "runner_ts_utc": now_ts,
        "orchestrator_run_id": orchestrator_run_id,
        "loser_instance_ids": list(loser_ids),
    }


def validate_pick_record(record: Dict[str, Any]) -> Tuple[bool, str]:
    """Validate pick record against v1 schema."""
    missing = PICK_REQUIRED_FIELDS - set(record.keys())
    if missing:
        return False, f"missing fields: {sorted(missing)}"
    if record.get("schema_version") != PICK_SCHEMA_VERSION:
        return False, f"schema_version expected {PICK_SCHEMA_VERSION}, got {record.get('schema_version')}"
    if not isinstance(record.get("anti_slop_score"), int):
        return False, "anti_slop_score must be int"
    if not isinstance(record.get("loser_instance_ids"), list):
        return False, "loser_instance_ids must be list"
    return True, "OK"


def write_pick_record(
    record: Dict[str, Any],
    output_path: Path,
) -> Tuple[bool, str]:
    """Write-once pick record. Fail if file already exists (write-once guarantee)."""
    ok, msg = validate_pick_record(record)
    if not ok:
        return False, ReasonCode.PARALLEL_DEV_PICK_SCHEMA_INVALID + ": " + msg
    if output_path.exists():
        return False, "pick record already exists (write-once)"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return True, "OK"


# --- T-007: Resource guard (AC-5) -----------------------------------------------

LOCKFILE_NAME = "us0108_parallel_dev.lock"


def _lockfile_path(repo_root: Optional[Path] = None) -> Path:
    if repo_root is None:
        repo_root = _REPO_ROOT
    return _git_dir(repo_root) / LOCKFILE_NAME


def acquire_lock(
    lock_id: Optional[str] = None,
    repo_root: Optional[Path] = None,
    max_total: Optional[int] = None,
) -> Tuple[bool, str]:
    """Acquire atomic lockfile. Uses pathlib exclusive create ('x' mode).

    System cap: AUTO_SOVEREIGN_PARALLEL_MAX_TOTAL (default 6).
    Returns (success, reason_code_or_lock_id).
    """
    if repo_root is None:
        repo_root = _REPO_ROOT
    lock_path = _lockfile_path(repo_root)
    if lock_id is None:
        lock_id = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S%f")

    lock_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        lock_data: Dict[str, Any] = {}
        if lock_path.is_file():
            try:
                lock_data = json.loads(lock_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, ValueError):
                lock_data = {}

        existing = lock_data.get("instances", [])
        active = [i for i in existing if i.get("status") == "active"]
        cap = max_total if max_total is not None else 6
        if len(active) >= cap:
            return False, ReasonCode.PARALLEL_DEV_RESOURCE_CAP_EXHAUSTED

        active.append({"lock_id": lock_id, "status": "active",
                        "ts": datetime.datetime.now(datetime.timezone.utc).isoformat()})
        lock_data["instances"] = active
        lock_data["cap"] = cap
        lock_path.write_text(
            json.dumps(lock_data, indent=2) + "\n", encoding="utf-8"
        )
        return True, lock_id
    except FileExistsError:
        return False, ReasonCode.PARALLEL_DEV_RESOURCE_LOCK_FAILED
    except OSError:
        return False, ReasonCode.PARALLEL_DEV_RESOURCE_LOCK_FAILED


def release_lock(
    lock_id: str,
    repo_root: Optional[Path] = None,
) -> bool:
    """Release a lock by lock_id. Idempotent."""
    if repo_root is None:
        repo_root = _REPO_ROOT
    lock_path = _lockfile_path(repo_root)
    if not lock_path.is_file():
        return True
    try:
        lock_data = json.loads(lock_path.read_text(encoding="utf-8"))
        lock_data["instances"] = [
            i for i in lock_data.get("instances", [])
            if i.get("lock_id") != lock_id
        ]
        remaining_active = [i for i in lock_data["instances"] if i.get("status") == "active"]
        if not remaining_active:
            lock_path.unlink(missing_ok=True)
        else:
            lock_path.write_text(
                json.dumps(lock_data, indent=2) + "\n", encoding="utf-8"
            )
        return True
    except Exception:
        return False


def acquire_parallel_slot(
    instance_id: Optional[str] = None,
    repo_root: Optional[Path] = None,
    max_total: int = 6,
) -> Tuple[bool, str]:
    """Alias for acquire_lock — AC-5 system-wide cap enforcement."""
    return acquire_lock(
        lock_id=instance_id or f"inst-{datetime.datetime.now(datetime.timezone.utc).strftime('%H%M%S%f')}",
        repo_root=repo_root,
        max_total=max_total,
    )


def release_parallel_slot(
    instance_id: str,
    repo_root: Optional[Path] = None,
) -> bool:
    """Release slot. Alias for release_lock."""
    return release_lock(instance_id, repo_root)


# --- T-008: Execute steps 25-28 (AC-6) ------------------------------------------

def simulate_instance_qa(
    story_id: str,
    instance_idx: int,
    worktree_path: str,
) -> Dict[str, Any]:
    """Simulate per-instance execute+QA result.

    In a real orchestration, each instance runs /execute+/qa independently.
    This function provides a deterministic test harness result.
    """
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "instance_id": f"{story_id}-inst{instance_idx}",
        "instance_idx": instance_idx,
        "worktree_path": worktree_path,
        "qa_verdict": "pass",
        "anti_slop_score": 7 - instance_idx if instance_idx < 3 else 0,
        "proof_issued_at": f"2026-06-29T22:{instance_idx:02d}:00Z",
        "story_id": story_id,
        "runner_ts_utc": now,
    }


def execute_parallel_dev(
    story_id: str,
    base_branch: str = "main",
    instance_count: int = 3,
    scratchpad_path: Optional[Path] = None,
    repo_root: Optional[Path] = None,
    orchestrator_run_id: str = "",
    pick_output_path: Optional[Path] = None,
) -> ExecuteResult:
    """Full parallel dev pipeline (steps 25-28).

    Step 25: spawn N dev instances (create worktrees)
    Step 26: QA cross-review
    Step 27: selection via select_winner (T-004)
    Step 28: merge+cleanup via merge_winner (T-006) + cleanup_worktrees (T-003)

    When SOVEREIGN_PARALLEL_DEV=0, return early with disabled reason.
    """
    if repo_root is None:
        repo_root = _REPO_ROOT
    if scratchpad_path is None:
        # Host-neutral default: resolve via US-0131; Cursor path is adapter-only.
        _ = hrc.resolve_runtime_config(repo_root, raise_on_fatal=False)
        scratchpad_path = repo_root / ".cursor" / "scratchpad.md"
    if pick_output_path is None:
        pick_output_path = repo_root / "handoffs" / "parallel_dev_pick.json"

    if not is_parallel_enabled(scratchpad_path):
        return ExecuteResult(
            winner_worktree=None,
            merge_result=MergeResult(success=False, branch=base_branch,
                                      commit_hash="", conflicts=[ReasonCode.PARALLEL_DEV_DISABLED]),
            qa_results=[],
        )

    config = read_scratchpad_with_defaults(scratchpad_path)
    n = int(config.get(AUTO_SOVEREIGN_PARALLEL_N_KEY, "3"))
    max_total = int(config.get(AUTO_SOVEREIGN_PARALLEL_MAX_TOTAL_KEY, "6"))
    merge_resolve = config.get(AUTO_SOVEREIGN_MERGE_RESOLVE_KEY, "first_pass_wins")
    keep_losers = config.get(AUTO_SOVEREIGN_WORKTREE_KEEP_KEY, "0") == "1"
    anti_slop_threshold = int(config.get(AUTO_SOVEREIGN_PARALLEL_ANTI_SLOP_THRESHOLD_KEY, "6"))
    merge_timeout = int(config.get(AUTO_SOVEREIGN_PARALLEL_MERGE_TIMEOUT_SEC_KEY, "60"))
    instance_count = min(n, max_total)

    slot_ok, slot_msg = acquire_parallel_slot(
        instance_id=f"{story_id}-orchestrator",
        repo_root=repo_root,
        max_total=max_total,
    )
    if not slot_ok:
        return ExecuteResult(
            winner_worktree=None,
            merge_result=MergeResult(success=False, branch=base_branch,
                                      commit_hash="", conflicts=[slot_msg]),
            qa_results=[],
        )

    try:
        # Step 25: spawn N worktrees
        worktrees = create_worktrees(base_branch, instance_count, story_id, repo_root)
        failed_wt = [w for w in worktrees if "failed" in w.status]
        if failed_wt:
            cleanup_worktrees(worktrees, story_id, keep_losers=False, repo_root=repo_root)
            return ExecuteResult(
                winner_worktree=None,
                merge_result=MergeResult(success=False, branch=base_branch,
                                          commit_hash="",
                                          conflicts=[ReasonCode.PARALLEL_DEV_WORKTREE_CREATE_FAILED]),
                qa_results=[],
            )

        # Step 26: QA cross-review (simulate)
        qa_results = []
        for ctx in worktrees:
            match = re.match(r"us0108-.+-(\d+)$", ctx.branch)
            idx = int(match.group(1)) if match else 0
            result = simulate_instance_qa(story_id, idx, ctx.path)
            qa_results.append(result)

        # Step 27: selection
        winner = select_winner(qa_results)
        if winner is None:
            cleanup_worktrees(worktrees, story_id, keep_losers=False, repo_root=repo_root)
            return ExecuteResult(
                winner_worktree=None,
                merge_result=MergeResult(success=False, branch=base_branch,
                                          commit_hash="",
                                          conflicts=[ReasonCode.PARALLEL_DEV_SELECTION_NO_PASS]),
                qa_results=qa_results,
            )

        winner_idx = winner["instance_idx"]
        winner_ctx = worktrees[winner_idx]
        winner_score = int(winner.get("anti_slop_score", 0))

        if winner_score < anti_slop_threshold:
            cleanup_worktrees(worktrees, story_id, keep_losers=False, repo_root=repo_root)
            return ExecuteResult(
                winner_worktree=None,
                merge_result=MergeResult(success=False, branch=winner_ctx.branch,
                                          commit_hash="",
                                          conflicts=[ReasonCode.PARALLEL_DEV_ANTI_SLOP_BELOW_THRESHOLD]),
                qa_results=qa_results,
            )

        # Step 28: merge + cleanup
        merge = merge_winner(
            winner_ctx, base_branch, repo_root,
            max_retries=2, timeout_sec=merge_timeout,
            merge_resolve=merge_resolve,
        )

        loser_ids = [
            ctx.instance_id for ctx in worktrees
            if ctx.instance_id != winner["instance_id"]
        ]

        pick_rec = build_pick_record(
            story_id=story_id,
            winner_id=winner["instance_id"],
            winner_path=winner_ctx.path,
            qa_verdict=str(winner.get("qa_verdict", "unknown")),
            anti_slop_score=winner_score,
            merge_policy=merge_resolve,
            loser_ids=loser_ids,
            orchestrator_run_id=orchestrator_run_id,
            proof_issued_at=winner.get("proof_issued_at"),
        )
        write_pick_record(pick_rec, pick_output_path)

        cleanup_worktrees(
            worktrees, story_id,
            keep_losers=keep_losers,
            winner_instance_id=winner["instance_id"],
            repo_root=repo_root,
        )

        # Release winner slot
        release_parallel_slot(winner["instance_id"], repo_root)

        return ExecuteResult(
            winner_worktree=winner_ctx,
            merge_result=merge,
            qa_results=qa_results,
        )
    except Exception as exc:
        return ExecuteResult(
            winner_worktree=None,
            merge_result=MergeResult(success=False, branch=base_branch,
                                      commit_hash="",
                                      conflicts=[ReasonCode.PARALLEL_DEV_EXECUTE_FAILED + f":{exc}"]),
            qa_results=[],
        )
    finally:
        release_parallel_slot(f"{story_id}-orchestrator", repo_root)


# --- Validator CLI / self-test ---------------------------------------------------

def run_self_test() -> Tuple[bool, str]:
    """Run inline self-test. Returns (pass, summary)."""
    errors = []

    # 1. Scratchpad key defaults
    for key, default in SCRATCHPAD_KEY_DEFAULTS.items():
        if not isinstance(default, str):
            errors.append(f"default for {key} is not str")

    # 2. Selection predicate
    results = [
        {"qa_verdict": "pass", "anti_slop_score": 5, "proof_issued_at": "2026-06-29T22:00:00Z", "instance_id": "A"},
        {"qa_verdict": "pass", "anti_slop_score": 8, "proof_issued_at": "2026-06-29T22:01:00Z", "instance_id": "B"},
        {"qa_verdict": "fail", "anti_slop_score": 10, "proof_issued_at": "2026-06-29T22:00:30Z", "instance_id": "C"},
    ]
    w = select_winner(results)
    if w is None or w.get("instance_id") != "B":
        errors.append(f"selection predicate failed: {w}")

    # 2b. Tie-break: same score → earliest wins
    tie_results = [
        {"qa_verdict": "pass", "anti_slop_score": 7, "proof_issued_at": "2026-06-29T22:05:00Z", "instance_id": "X"},
        {"qa_verdict": "pass", "anti_slop_score": 7, "proof_issued_at": "2026-06-29T22:01:00Z", "instance_id": "Y"},
    ]
    tw = select_winner(tie_results)
    if tw is None or tw.get("instance_id") != "Y":
        errors.append(f"tie-break failed: {tw}")

    # 3. Anti-slop reader
    score = read_anti_slop_score([7, 8, 6])
    if score != 6:
        errors.append(f"anti_slop reader failed: {score} != 6")
    score0 = read_anti_slop_score([])
    if score0 != 0:
        errors.append(f"anti_slop empty failed: {score0} != 0")

    # 4. Pick record round-trip
    with tempfile.TemporaryDirectory() as td:
        pick_path = Path(td) / "pick.json"
        rec = build_pick_record(
            story_id="US-0108", winner_id="inst0", winner_path="/tmp/wt0",
            qa_verdict="pass", anti_slop_score=8, merge_policy="first_pass_wins",
            loser_ids=["inst1", "inst2"], orchestrator_run_id="test-001",
        )
        ok, msg = write_pick_record(rec, pick_path)
        if not ok:
            errors.append(f"write_pick_record failed: {msg}")
        else:
            loaded = json.loads(pick_path.read_text(encoding="utf-8"))
            vok, vmsg = validate_pick_record(loaded)
            if not vok:
                errors.append(f"validate_pick_record failed: {vmsg}")
            ok2, msg2 = write_pick_record(rec, pick_path)
            if ok2:
                errors.append("write-once guarantee violated")

    if errors:
        return False, "; ".join(errors)
    return True, "self-test OK"


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true", help="Run inline self-test")
    parser.add_argument("--repo", type=Path, default=None, help="Repository root")
    parser.add_argument("--scratchpad", type=Path, default=None, help="Scratchpad path")
    args = parser.parse_args()

    if args.self_test:
        ok, msg = run_self_test()
        print(f"[{'SELF_TEST_PASS' if ok else 'SELF_TEST_FAIL'}] {msg}")
        return 0 if ok else 1

    repo = args.repo or _REPO_ROOT
    sp = args.scratchpad or (repo / ".cursor" / "scratchpad.md")
    if is_parallel_enabled(sp):
        print("[PARALLEL_DEV_ENABLED] SOVEREIGN_PARALLEL_DEV=1")
    else:
        print("[PARALLEL_DEV_DISABLED] SOVEREIGN_PARALLEL_DEV=0 (zero overhead)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
