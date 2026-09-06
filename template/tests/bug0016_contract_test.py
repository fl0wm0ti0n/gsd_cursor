"""BUG-0016 OpenCode Layer-1 permissions vs kit duties — 7 contract markers.

Markers per architecture.md # BUG-0016 / R-0115 DQ7 / DEC-0122 §2 amended.
Static frontmatter harness only; no live OpenCode runtime probe.
"""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_AGENTS = REPO_ROOT / "template" / ".opencode" / "agents"
ACTIVE_AGENTS = REPO_ROOT / ".opencode" / "agents"
PLUGIN_PATH = REPO_ROOT / "template" / ".opencode" / "plugins" / "orchestrator.ts"
ACTIVE_PLUGIN = REPO_ROOT / ".opencode" / "plugins" / "orchestrator.ts"

EXPECTED_AGENTS = (
    "po",
    "tech-lead",
    "dev",
    "qa",
    "release",
    "curator",
    "security",
    "auto",
)
US0003_ROLES = frozenset(
    {"po", "tech-lead", "dev", "qa", "release", "curator", "security"}
)
PRODUCTION_DENY_GLOBS = frozenset(
    {
        "scripts/**",
        "its_magic/**",
        "**/*.py",
        "installer.*",
        "template/scripts/**",
        "template/its_magic/**",
    }
)
SPRINT_ROLES = ("tech-lead", "dev", "qa", "release")


def _split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        raise ValueError("missing opening frontmatter fence")
    rest = text[3:]
    if rest.startswith("\r\n"):
        rest = rest[2:]
    elif rest.startswith("\n"):
        rest = rest[1:]
    idx = rest.find("\n---")
    if idx < 0:
        raise ValueError("missing closing frontmatter fence")
    fm = rest[:idx]
    body = rest[idx + 4 :]
    if body.startswith("\r\n"):
        body = body[2:]
    elif body.startswith("\n"):
        body = body[1:]
    return fm, body


def _parse_scalar(token: str) -> str:
    token = token.strip()
    if len(token) >= 2 and token[0] == token[-1] and token[0] in ('"', "'"):
        return token[1:-1]
    return token


def _ordered_mapping_keys(fm: str, parent_key: str, parent_indent: int = 0) -> list[tuple[str, str]]:
    lines = fm.splitlines()
    prefix = " " * parent_indent
    child_prefix = " " * (parent_indent + 2)
    keys: list[tuple[str, str]] = []
    in_parent = False
    i = 0
    while i < len(lines):
        line = lines[i]
        if line == f"{prefix}{parent_key}:":
            in_parent = True
            i += 1
            continue
        if not in_parent:
            i += 1
            continue
        if line.startswith(child_prefix) and not line.startswith(child_prefix + " "):
            if ":" not in line:
                i += 1
                continue
            key_part, _, val_part = line.partition(":")
            key = _parse_scalar(key_part.strip())
            val = val_part.strip()
            if not val:
                i += 1
                continue
            keys.append((key, _parse_scalar(val)))
            i += 1
            continue
        if line.startswith(prefix) and line.strip():
            break
        if line.strip() and not line.startswith(prefix):
            break
        i += 1
    return keys


def _permission_subkey_value(fm: str, subkey: str) -> list[tuple[str, str]] | str:
    lines = fm.splitlines()
    for i, line in enumerate(lines):
        if line.strip() != "permission:":
            continue
        j = i + 1
        while j < len(lines):
            ln = lines[j]
            if ln.startswith("  ") and not ln.startswith("    ") and ln.strip():
                key_part, _, val_part = ln.partition(":")
                key = key_part.strip()
                val = val_part.strip()
                if key != subkey:
                    j += 1
                    continue
                if val:
                    return _parse_scalar(val)
                return _ordered_mapping_keys(fm, subkey, parent_indent=2)
            if ln.strip() and not ln.startswith(" "):
                break
            j += 1
    raise ValueError(f"permission.{subkey} not found")


def _read_agent(name: str, *, active: bool = False) -> tuple[str, str]:
    root = ACTIVE_AGENTS if active else TEMPLATE_AGENTS
    text = (root / f"{name}.md").read_text(encoding="utf-8")
    return _split_frontmatter(text)


# -- marker 1 --


def test_bug0016_po_tl_curator_bash_ask():
    """po / tech-lead / curator bash == ask (not deny/allow)."""
    for name in ("po", "tech-lead", "curator"):
        fm, _ = _read_agent(name)
        bash = _permission_subkey_value(fm, "bash")
        assert bash == "ask", f"{name} bash must be ask, got {bash!r}"
        assert bash not in ("deny", "allow")


# -- marker 2 --


def test_bug0016_po_intake_resume_state_allows():
    """PO edit allows intake_evidence/**, resume_brief.md, state.md; ** deny last; no scripts/**."""
    fm, _ = _read_agent("po")
    edit = _permission_subkey_value(fm, "edit")
    assert isinstance(edit, list)
    keys = [k for k, _ in edit]
    values = {k: v for k, v in edit}
    assert values.get("handoffs/intake_evidence/**") == "allow"
    assert values.get("handoffs/resume_brief.md") == "allow"
    assert values.get("docs/engineering/state.md") == "allow"
    assert keys[-1] == "**"
    assert values["**"] == "deny"
    assert "scripts/**" not in values or values["scripts/**"] != "allow"
    allow_keys = {k for k, v in edit if v == "allow"}
    assert "scripts/**" not in allow_keys


# -- marker 3 --


def test_bug0016_sprint_globs_are_s_star_not_sxxxx():
    """tech-lead/dev/qa/release sprint keys use sprints/S*/; Sxxxx absent from permission keys."""
    for name in SPRINT_ROLES:
        fm, _ = _read_agent(name)
        edit = _permission_subkey_value(fm, "edit")
        assert isinstance(edit, list)
        keys = [k for k, _ in edit]
        assert not any("Sxxxx" in k for k in keys), f"{name} still has Sxxxx key"
        sprint_keys = [k for k in keys if k.startswith("sprints/")]
        assert sprint_keys, f"{name} missing sprint permission keys"
        assert all(k.startswith("sprints/S*/") for k in sprint_keys), (
            f"{name} sprint keys must use sprints/S*/ not Sxxxx: {sprint_keys}"
        )
        assert not any("S[0-9]" in k for k in keys), f"{name} must keep S* not S[0-9]*"


# -- marker 4 --


def test_bug0016_release_duty_paths():
    """release allows release-findings, verify-work-to-release, state.md, resume_brief, runbook."""
    fm, _ = _read_agent("release")
    edit = _permission_subkey_value(fm, "edit")
    assert isinstance(edit, list)
    values = {k: v for k, v in edit}
    keys = [k for k, _ in edit]
    assert values.get("sprints/S*/release-findings.md") == "allow"
    assert values.get("handoffs/verify-work-to-release.md") == "allow"
    assert values.get("docs/engineering/state.md") == "allow"
    assert values.get("handoffs/resume_brief.md") == "allow"
    assert values.get("docs/engineering/runbook.md") == "allow"
    assert values.get("handoffs/verify_to_release.md") == "allow"
    assert keys[-1] == "**"
    assert values["**"] == "deny"
    bash = _permission_subkey_value(fm, "bash")
    assert bash == "ask"


# -- marker 5 --


def test_bug0016_success_test_c_non_dev_no_production_allow():
    """Non-dev roles: no production/code allow; object-form edit keeps ** deny last."""
    for name in sorted(US0003_ROLES - {"dev"}):
        fm, _ = _read_agent(name)
        edit = _permission_subkey_value(fm, "edit")
        if isinstance(edit, str):
            assert edit == "deny", f"{name} shorthand edit must be deny"
            continue
        keys = [k for k, _ in edit]
        values = {k: v for k, v in edit}
        assert keys[-1] == "**"
        assert values["**"] == "deny"
        allow_keys = {k for k, v in edit if v == "allow"}
        assert not allow_keys & PRODUCTION_DENY_GLOBS, (
            f"{name} production allow leak: {allow_keys & PRODUCTION_DENY_GLOBS}"
        )


# -- marker 6 --


def test_bug0016_security_auto_unchanged():
    """security edit deny + bash ask; auto edit/bash deny + 7-role task allow + * deny last."""
    sec_fm, _ = _read_agent("security")
    assert _permission_subkey_value(sec_fm, "edit") == "deny"
    assert _permission_subkey_value(sec_fm, "bash") == "ask"
    assert _permission_subkey_value(sec_fm, "task") == "deny"

    auto_fm, _ = _read_agent("auto")
    assert _permission_subkey_value(auto_fm, "edit") == "deny"
    assert _permission_subkey_value(auto_fm, "bash") == "deny"
    task = _permission_subkey_value(auto_fm, "task")
    assert isinstance(task, list)
    keys = [k for k, _ in task]
    values = {k: v for k, v in task}
    allow_roles = {k for k, v in task if v == "allow"}
    assert allow_roles == US0003_ROLES
    assert keys[-1] == "*"
    assert values["*"] == "deny"


# -- marker 7 --


def test_bug0016_active_template_agent_parity():
    """Eight agents byte-identical active↔template; write-guard does not duplicate edit globs."""
    for name in EXPECTED_AGENTS:
        active = ACTIVE_AGENTS / f"{name}.md"
        template = TEMPLATE_AGENTS / f"{name}.md"
        assert active.is_file() and template.is_file(), f"missing {name}.md"
        assert active.read_bytes() == template.read_bytes(), f"{name}.md parity fail"
    # DQ8 adjacent static check: plugin must not re-list Layer-1 duty globs as denies
    plugin = PLUGIN_PATH.read_text(encoding="utf-8")
    assert ACTIVE_PLUGIN.read_bytes() == PLUGIN_PATH.read_bytes()
    for forbidden in (
        "handoffs/intake_evidence",
        "sprints/S*/release-findings",
        "verify-work-to-release",
        'bash: "deny"',
        "Sxxxx",
    ):
        assert forbidden not in plugin, f"write-guard appears to encode Layer-1 glob {forbidden!r}"
    assert 'tool.hook("execute.before"' in plugin or 'ctx.tool.hook("execute.before"' in plugin
