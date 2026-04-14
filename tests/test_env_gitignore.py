#!/usr/bin/env python3
"""
Regression tests for .env gitignore and cursorignore safety (US-0085 / AC-9).
"""

from __future__ import annotations

import subprocess
from pathlib import Path


def test_env_is_gitignored():
    result = subprocess.run(
        ["git", "check-ignore", ".env"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        ".env should be gitignored but git check-ignore returned "
        f"exit {result.returncode}"
    )


def test_env_example_is_not_gitignored():
    result = subprocess.run(
        ["git", "check-ignore", ".env.example"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1, (
        ".env.example should NOT be gitignored but git check-ignore returned "
        f"exit {result.returncode}"
    )


def test_cursorignore_exists_and_contains_env_pattern():
    ci = Path(".cursorignore")
    assert ci.is_file(), ".cursorignore must exist at repo root"
    content = ci.read_text(encoding="utf-8")
    assert ".env" in content, ".cursorignore must contain .env pattern"


def test_env_example_exists_with_20_names():
    ex = Path(".env.example")
    assert ex.is_file(), ".env.example must exist at repo root"
    names = [
        line.split("=", 1)[0]
        for line in ex.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#") and "=" in line
    ]
    assert len(names) == 20, f"Expected 20 env var names, got {len(names)}: {names}"
