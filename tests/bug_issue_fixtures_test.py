"""
Tier A regression for bug issue validator + intake bug routing guard (US-0079 / DEC-0061 / R-0056).
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
VALIDATOR = os.path.join(ROOT, "scripts", "bug_issue_validate.py")
GUARD = os.path.join(ROOT, "scripts", "intake_bug_routing_guard.py")


def _run(args: list[str]) -> int:
    return subprocess.call([sys.executable, *args], cwd=ROOT)


def test_validator_self_test() -> None:
    assert _run([VALIDATOR, "--self-test"]) == 0


def test_repo_backlog_passes() -> None:
    assert (
        _run(
            [
                VALIDATOR,
                "--backlog",
                os.path.join(ROOT, "docs/product/backlog.md"),
                "--acceptance",
                os.path.join(ROOT, "docs/product/acceptance.md"),
                "--check-acceptance",
            ]
        )
        == 0
    )


def test_fixture_invalid_status() -> None:
    md = """## Bug issues (canonical)

### BUG-0001 — X
- Status: TRIAGED
- environment: a
- steps_to_reproduce: b
- expected: c
- actual: d
- evidence_refs: e
"""
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(md)
        path = f.name
    try:
        assert _run([VALIDATOR, "--backlog", path]) != 0
    finally:
        os.unlink(path)


def test_fixture_valid_single_bug() -> None:
    md = """## Bug issues (canonical)

### BUG-0001 — Sample
- Status: OPEN
- environment: Linux CI
- steps_to_reproduce: Run pytest
- expected: Green
- actual: Green
- evidence_refs: logs/ci.txt
"""
    acc = """## Bug acceptance (canonical)

- [ ] BUG-0001: Sample
"""
    d1 = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8")
    d2 = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8")
    try:
        d1.write(md)
        d1.close()
        d2.write(acc)
        d2.close()
        assert _run([VALIDATOR, "--backlog", d1.name, "--acceptance", d2.name, "--check-acceptance"]) == 0
    finally:
        os.unlink(d1.name)
        os.unlink(d2.name)


def test_intake_guard_story_clean() -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write("Add dark mode toggle for settings page.")
        path = f.name
    try:
        assert _run([GUARD, "--kind", "story", "--file", path]) == 0
    finally:
        os.unlink(path)


def test_intake_guard_defect_blocked() -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write(
            "Bug: app crashes on save. Steps to reproduce: open dialog, click save. "
            "Expected: file writes. Actual: segfault."
        )
        path = f.name
    try:
        assert _run([GUARD, "--kind", "story", "--file", path]) == 3
    finally:
        os.unlink(path)


def test_intake_guard_bug_kind_ok() -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write("same defect prose")
        path = f.name
    try:
        assert _run([GUARD, "--kind", "bug", "--file", path]) == 0
    finally:
        os.unlink(path)


def main() -> int:
    test_validator_self_test()
    test_repo_backlog_passes()
    test_fixture_invalid_status()
    test_fixture_valid_single_bug()
    test_intake_guard_story_clean()
    test_intake_guard_defect_blocked()
    test_intake_guard_bug_kind_ok()
    print("[BUG_ISSUE_FIXTURES_OK]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
