#!/usr/bin/env python3
"""
Validate release changelog / version-doc consistency (US-0100 / DEC-0085).
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

REMEDIATION = {
    rcl.RELEASE_CHANGELOG_VERSION_MISSING: "Set explicit semver on queue row or pass valid --semver.",
    rcl.RELEASE_CHANGELOG_DUPLICATE_VERSION: "Resolve fingerprint mismatch; do not reuse semver for different work items.",
    rcl.RELEASE_CHANGELOG_WORK_ITEM_GAP: "Run derive/build_version_doc or complete sprint notes + backlog refs.",
    rcl.RELEASE_CHANGELOG_ORDER_INVALID: "Reorder CHANGELOG.md semver sections newest-first.",
    rcl.RELEASE_CHANGELOG_UNRELEASED_MISSING: "Add mandatory ## [Unreleased] header at top of CHANGELOG.md.",
    rcl.RELEASE_CHANGELOG_QUEUE_DRIFT: "Re-run bind_queue_release_version or reconcile queue release_version.",
    rcl.RELEASE_CHANGELOG_VERSION_DOC_MISSING: "Run build_version_doc or release_changelog_backfill before gh -F attach.",
    rcl.RELEASE_CHANGELOG_SPRINT_ORPHAN: "Include released sprint in semver doc or [Unreleased] via backfill.",
    rcl.RELEASE_CHANGELOG_BACKFILL_AMBIGUOUS: "Fix manifest collision; one semver intent per coalesce group.",
    rcl.RELEASE_CHANGELOG_IDEMPOTENCY_VIOLATION: "Remove duplicate work-item bullets for same version; re-run derive.",
}


def _emit(code: str, detail: str = "") -> None:
    msg = code if not detail else f"{code}: {detail}"
    print(msg, file=sys.stderr)
    rem = REMEDIATION.get(code, "See docs/engineering/runbook.md § Version-scoped release docs.")
    print(f"Remediation: {rem}", file=sys.stderr)


def validate(repo_root: str, enforce: bool) -> int:
    errors: list[str] = []
    cl_path = rcl.changelog_path(repo_root)
    if not os.path.isfile(cl_path):
        errors.append(rcl.RELEASE_CHANGELOG_UNRELEASED_MISSING)
    else:
        text = rcl.read_utf8(cl_path)
        if "## [Unreleased]" not in text:
            errors.append(rcl.RELEASE_CHANGELOG_UNRELEASED_MISSING)
        # semver order newest-first (skip Unreleased)
        versions: list[str] = []
        for m in re.finditer(r"^##\s+\[(.+?)\]", text, re.MULTILINE):
            v = m.group(1)
            if v.lower() == "unreleased":
                continue
            try:
                versions.append(rcl.normalize_semver(v))
            except rcl.ReleaseChangelogError:
                errors.append(rcl.RELEASE_CHANGELOG_VERSION_MISSING)
        # Simple order check: compare as strings after normalization (pre-release aware minimal)
        if len(versions) > 1:
            for i in range(len(versions) - 1):
                if versions[i] < versions[i + 1]:
                    errors.append(rcl.RELEASE_CHANGELOG_ORDER_INVALID)
                    break

    rows = rcl.parse_queue_rows(repo_root)
    for row in rows:
        if row.status != "released":
            continue
        rv = row.release_version.strip()
        if not rv:
            continue
        try:
            norm = rcl.normalize_semver(rv)
        except rcl.ReleaseChangelogError:
            errors.append(rcl.RELEASE_CHANGELOG_VERSION_MISSING)
            continue
        vdoc = rcl.version_doc_path(repo_root, norm)
        if not os.path.isfile(vdoc):
            errors.append(rcl.RELEASE_CHANGELOG_VERSION_DOC_MISSING)
        section = rcl.extract_changelog_section(norm, repo_root)
        if section is None:
            errors.append(rcl.RELEASE_CHANGELOG_VERSION_MISSING)
        # work item gap: story_refs should appear in version doc
        if os.path.isfile(vdoc):
            doc_text = rcl.read_utf8(vdoc)
            for token in re.split(r"[,;\s]+", row.story_refs):
                token = token.strip()
                if token and token not in doc_text:
                    errors.append(rcl.RELEASE_CHANGELOG_WORK_ITEM_GAP)

    # queue drift: coalesce groups vs bound semver
    groups = rcl.coalesce_sprints_by_semver(rows, repo_root)
    for semver, sids in groups.items():
        for sid in sids:
            row = next((r for r in rows if r.sprint_id == sid), None)
            if row and row.release_version.strip():
                try:
                    if rcl.normalize_semver(row.release_version) != semver:
                        errors.append(rcl.RELEASE_CHANGELOG_QUEUE_DRIFT)
                except rcl.ReleaseChangelogError:
                    errors.append(rcl.RELEASE_CHANGELOG_QUEUE_DRIFT)

    seen_errors = sorted(set(errors))
    for code in seen_errors:
        _emit(code)
    if seen_errors and enforce:
        return 1
    if not seen_errors:
        print("[RELEASE_CHANGELOG_VALIDATE_OK]")
        return 0
    if not enforce:
        print("[RELEASE_CHANGELOG_VALIDATE_WARN]")
        return 0
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=_REPO_ROOT, help="Repository root")
    parser.add_argument(
        "--enforce",
        action="store_true",
        help="Exit non-zero on any fail code (release gate / release-all.sh).",
    )
    args = parser.parse_args()
    return validate(os.path.abspath(args.repo), args.enforce)


if __name__ == "__main__":
    raise SystemExit(main())
