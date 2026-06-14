#!/usr/bin/env python3
"""
Idempotent one-time backfill for release changelog tiers A/B/C (US-0100 / DEC-0085).
"""

from __future__ import annotations

import argparse
import os
import re
import sys

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.normpath(os.path.join(_SCRIPT_DIR, ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

import release_changelog_lib as rcl  # noqa: E402

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None  # type: ignore


MANIFEST_REL = os.path.join(
    "docs", "engineering", "context", "release-version-backfill.manifest.yaml"
)


def _load_manifest(repo_root: str) -> dict:
    path = os.path.join(repo_root, MANIFEST_REL)
    if not os.path.isfile(path):
        return {"schema_version": 1, "entries": []}
    text = rcl.read_utf8(path)
    if yaml is not None:
        data = yaml.safe_load(text) or {}
    else:
        # Minimal stdlib fallback for schema_version + entries
        data = {"schema_version": 1, "entries": []}
        m = re.search(r"schema_version:\s*(\d+)", text)
        if m:
            data["schema_version"] = int(m.group(1))
        for em in re.finditer(
            r"-\s*sprint_id:\s*(S\d{4})\s*\n\s*semver:\s*[\"']?([^\"'\n]+)[\"']?",
            text,
        ):
            data.setdefault("entries", []).append(
                {"sprint_id": em.group(1), "semver": em.group(2).strip()}
            )
    return data


def _synthetic_semver(sprint_id: str) -> str:
    num = int(sprint_id[1:])
    return f"0.0.0-wf.{num:03d}"


def assign_semvers(repo_root: str) -> dict[str, str]:
    """Tier A → B → C precedence; returns sprint_id → semver."""
    rows = sorted(
        [r for r in rcl.parse_queue_rows(repo_root) if r.status == "released"],
        key=lambda r: r.last_updated,
    )
    manifest = _load_manifest(repo_root)
    tier_b: dict[str, str] = {}
    for entry in manifest.get("entries") or []:
        sid = entry.get("sprint_id", "").strip()
        sem = entry.get("semver", "").strip()
        if sid and sem:
            tier_b[sid] = rcl.normalize_semver(sem)
    # collision detection
    inv: dict[str, list[str]] = {}
    for sid, sem in tier_b.items():
        inv.setdefault(sem, []).append(sid)
    for sem, sids in inv.items():
        if len(sids) > 1:
            raise rcl.ReleaseChangelogError(
                rcl.RELEASE_CHANGELOG_BACKFILL_AMBIGUOUS,
                f"manifest maps {sids} → {sem}",
            )

    assignment: dict[str, str] = {}
    for row in rows:
        if row.release_version.strip():
            assignment[row.sprint_id] = rcl.normalize_semver(row.release_version)
        elif row.sprint_id in tier_b:
            assignment[row.sprint_id] = tier_b[row.sprint_id]
    for row in rows:
        if row.sprint_id in assignment:
            continue
        assignment[row.sprint_id] = _synthetic_semver(row.sprint_id)
    return assignment


def run_backfill(repo_root: str, dry_run: bool = False) -> int:
    rcl.ensure_changelog_stub(repo_root)
    try:
        assignment = assign_semvers(repo_root)
    except rcl.ReleaseChangelogError as exc:
        print(f"{exc.code}: {exc}", file=sys.stderr)
        return 1

    # coalesce by semver
    groups: dict[str, list[str]] = {}
    for sid, sem in assignment.items():
        groups.setdefault(sem, []).append(sid)

    for semver, sprint_ids in sorted(groups.items()):
        if dry_run:
            print(f"would build {semver} <- {sprint_ids}")
            continue
        try:
            rcl.build_version_doc(semver, sprint_ids, repo_root)
            rcl.promote_unreleased(semver, sprint_ids, repo_root)
            rcl.bind_queue_release_version(sprint_ids, semver, repo_root)
        except rcl.ReleaseChangelogError as exc:
            if exc.code == rcl.RELEASE_CHANGELOG_DUPLICATE_VERSION:
                print(rcl.RELEASE_CHANGELOG_IDEMPOTENCY_OK, file=sys.stderr)
                continue
            print(f"{exc.code}: {exc}", file=sys.stderr)
            return 1

    print("[RELEASE_CHANGELOG_BACKFILL_OK]")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=_REPO_ROOT)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--ensure-version",
        metavar="SEMVER",
        help="Ensure handoffs/releases/{semver}-release-notes.md exists (release-all.sh).",
    )
    args = parser.parse_args()
    root = os.path.abspath(args.repo)
    if args.ensure_version:
        try:
            path = rcl.ensure_version_doc_for_release(args.ensure_version, root)
            print(path)
            return 0
        except rcl.ReleaseChangelogError as exc:
            print(f"{exc.code}: {exc}", file=sys.stderr)
            return 1
    return run_backfill(root, dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
