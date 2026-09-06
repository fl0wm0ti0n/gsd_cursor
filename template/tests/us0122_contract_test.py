"""US-0122 OpenCode role agents + Layer-1 permission matrix — 8 contract markers."""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = REPO_ROOT / "template" / ".opencode" / "agents"
KIT_OPENCODE_AGENTS = REPO_ROOT / ".opencode" / "agents"

EXPECTED_AGENT_NAMES = frozenset(
    {"po", "tech-lead", "dev", "qa", "release", "curator", "security", "auto"}
)
US0003_ROLES = frozenset(
    {"po", "tech-lead", "dev", "qa", "release", "curator", "security"}
)
AUTO_TASK_ALLOW = US0003_ROLES

VENDOR_SLUG_RE = re.compile(
    r"deepseek|moonshot|kimi|glm|claude|gpt|sonnet|opus|haiku|o1|o3|sk-",
    re.IGNORECASE,
)
CLONE_MARKER_RE = re.compile(
    r"/auto|/intake|/discovery|/research|/architecture|/sprint-plan|/execute|/qa|/release|/closure|/refresh-context"
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
MAX_AGENT_BYTES = 2048


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
    body = rest[idx + 4:]
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
    """Ordered glob/action pairs under a nested mapping key (e.g. permission.edit)."""
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
    perm_prefix = "permission:"
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


def _read_agent(name: str) -> tuple[str, str, str]:
    path = AGENTS_DIR / f"{name}.md"
    text = path.read_text(encoding="utf-8")
    fm, body = _split_frontmatter(text)
    return text, fm, body


# -- marker 1 --


def test_us0122_agent_inventory():
    """Eight markdown agents under template/.opencode/agents/; active↔template byte-identical (BUG-0016)."""
    md_files = sorted(p.stem for p in AGENTS_DIR.glob("*.md"))
    assert md_files == sorted(EXPECTED_AGENT_NAMES), f"agent inventory mismatch: {md_files}"
    assert KIT_OPENCODE_AGENTS.is_dir(), "kit-root .opencode/agents/ required for active↔template parity"
    kit_stems = sorted(p.stem for p in KIT_OPENCODE_AGENTS.glob("*.md"))
    assert kit_stems == sorted(EXPECTED_AGENT_NAMES), f"active agent inventory mismatch: {kit_stems}"
    for name in sorted(EXPECTED_AGENT_NAMES):
        active = KIT_OPENCODE_AGENTS / f"{name}.md"
        template = AGENTS_DIR / f"{name}.md"
        assert active.read_bytes() == template.read_bytes(), f"{name}.md active↔template parity mismatch"


# -- marker 2 --


def test_us0122_po_permission_object_form():
    """po.md permission.edit is object form, not shorthand."""
    _, fm, _ = _read_agent("po")
    edit = _permission_subkey_value(fm, "edit")
    assert isinstance(edit, list), "po permission.edit must be object mapping, not shorthand"
    assert edit, "po permission.edit mapping empty"


# -- marker 3 --


def test_us0122_po_production_code_denial():
    """PO edit deny-last; amended duty allows; no production path allow keys (BUG-0016 / DEC-0122 §2)."""
    _, fm, _ = _read_agent("po")
    edit_pairs = _permission_subkey_value(fm, "edit")
    assert isinstance(edit_pairs, list)
    keys = [k for k, _ in edit_pairs]
    values = {k: v for k, v in edit_pairs}
    assert keys[-1] == "**", "last edit key must be ** (deny-last)"
    assert values["**"] == "deny"
    assert values.get("docs/product/**") == "allow"
    assert values.get("handoffs/po_to_tl.md") == "allow"
    assert values.get("handoffs/intake_evidence/**") == "allow"
    assert values.get("handoffs/resume_brief.md") == "allow"
    assert values.get("docs/engineering/state.md") == "allow"
    bash = _permission_subkey_value(fm, "bash")
    assert bash == "ask", f"po bash must be ask after BUG-0016, got {bash!r}"
    allow_keys = {k for k, v in edit_pairs if v == "allow"}
    assert not allow_keys & PRODUCTION_DENY_GLOBS
    for glob in PRODUCTION_DENY_GLOBS:
        assert glob not in values or values[glob] != "allow"
    # Amended §2 sprint globs use S* (not literal Sxxxx) on owning roles
    for role in ("tech-lead", "dev", "qa", "release"):
        _, role_fm, _ = _read_agent(role)
        role_edit = _permission_subkey_value(role_fm, "edit")
        assert isinstance(role_edit, list)
        role_keys = [k for k, _ in role_edit]
        assert not any("Sxxxx" in k for k in role_keys), f"{role} still has Sxxxx permission key"
        if role != "release":
            assert any(k.startswith("sprints/S*/") for k in role_keys), f"{role} missing sprints/S*/ keys"
        else:
            assert "sprints/S*/release-findings.md" in role_keys


# -- marker 4 --


def test_us0122_auto_task_allowlist():
    """auto.md task object: exact 7-role allow set; * deny last."""
    _, fm, _ = _read_agent("auto")
    task = _permission_subkey_value(fm, "task")
    assert isinstance(task, list), "auto permission.task must be object mapping"
    keys = [k for k, _ in task]
    values = {k: v for k, v in task}
    allow_roles = {k for k, v in task if v == "allow"}
    assert allow_roles == AUTO_TASK_ALLOW
    assert keys[-1] == "*"
    assert values["*"] == "deny"


# -- marker 5 --


def test_us0122_security_edit_denied():
    """security.md permission.edit shorthand deny."""
    _, fm, _ = _read_agent("security")
    edit = _permission_subkey_value(fm, "edit")
    assert edit == "deny", f"security edit must be shorthand deny, got {edit!r}"


# -- marker 6 --


def test_us0122_no_vendor_slugs_in_template():
    """No vendor slug patterns in template/.opencode/agents/*.md."""
    hits = []
    for path in sorted(AGENTS_DIR.glob("*.md")):
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if VENDOR_SLUG_RE.search(line):
                hits.append(f"{path.name}:{i}:{line.strip()}")
    assert not hits, "vendor slug hits: " + repr(hits)


# -- marker 7 --


def test_us0122_prompt_size_clone_guard():
    """Each agent <= 2 KiB; no clone markers; single YAML frontmatter block."""
    for name in sorted(EXPECTED_AGENT_NAMES):
        path = AGENTS_DIR / f"{name}.md"
        raw = path.read_text(encoding="utf-8")
        assert len(raw.encode("utf-8")) <= MAX_AGENT_BYTES, f"{name}.md exceeds 2 KiB"
        _, body = _split_frontmatter(raw)
        scan_text = body
        assert CLONE_MARKER_RE.search(scan_text) is None, f"clone marker in {name}.md body"
        assert ".cursor/commands/" not in scan_text, f".cursor/commands/ literal in {name}.md body"
        assert "alwaysApply" not in raw, f"Cursor MDC key in {name}.md"
        assert raw.count("---") == 2, f"{name}.md must have exactly one frontmatter block (two --- fences)"
        _split_frontmatter(raw)


# -- marker 8 --


def test_us0122_role_id_parity():
    """Filenames match US-0003 roles + auto orchestrator; no extra product roles."""
    stems = {p.stem for p in AGENTS_DIR.glob("*.md")}
    assert stems == EXPECTED_AGENT_NAMES
    role_stems = stems - {"auto"}
    assert role_stems == US0003_ROLES
