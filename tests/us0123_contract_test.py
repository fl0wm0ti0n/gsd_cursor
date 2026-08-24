"""US-0123 OpenCode per-role model slug routing — 8 contract markers."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = REPO_ROOT / "template" / ".opencode" / "agents"
EXAMPLE_CATALOG = REPO_ROOT / "template" / ".opencode" / "model-catalog.local.example.json"
MATERIALIZER = REPO_ROOT / "scripts" / "opencode_model_catalog_apply.py"
OPENCODE_GITIGNORE = REPO_ROOT / "template" / ".opencode" / ".gitignore"
CURSOR_CATALOG_EXAMPLE = REPO_ROOT / ".cursor" / "model-catalog.local.example.json"
SCRATCHPAD = REPO_ROOT / ".cursor" / "scratchpad.md"

VENDOR_SLUG_RE = re.compile(
    r"deepseek|moonshot|kimi|glm|claude|gpt|sonnet|opus|haiku|o1|o3|sk-",
    re.IGNORECASE,
)
PLACEHOLDER_ROLE_RE = re.compile(r"^[^/]+/<your-[^>]+-slug>$")
AUTH_SECRET_RE = re.compile(
    r"auth\.json|api_key|apikey|sk-[A-Za-z0-9]{8,}",
    re.IGNORECASE,
)


def _grep_vendor_hits(root: Path, rel_globs: list[str]) -> list[str]:
    hits: list[str] = []
    for pattern in rel_globs:
        for path in root.glob(pattern):
            if path.suffix in (".example.json", ".local.json"):
                continue
            if "model-catalog.local.example.json" in path.name:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except OSError:
                continue
            for line_num, line in enumerate(text.splitlines(), start=1):
                if VENDOR_SLUG_RE.search(line):
                    hits.append(f"{path}:{line_num}:{line.strip()}")
    return hits


def test_us0123_template_agents_omit_model():
    """Marker 1: template/.opencode/agents/*.md must not contain model: frontmatter."""
    assert AGENTS_DIR.is_dir(), "template/.opencode/agents missing"
    offenders: list[str] = []
    for agent in AGENTS_DIR.glob("*.md"):
        for line_num, line in enumerate(agent.read_text(encoding="utf-8").splitlines(), start=1):
            if re.match(r"^\s*model\s*:", line):
                offenders.append(f"{agent}:{line_num}")
    assert not offenders, "model: found in template agents: " + repr(offenders)


def test_us0123_no_vendor_slugs_in_template():
    """Marker 2: D3 grep on template OpenCode surfaces (excludes *.example.json / *.local.json)."""
    hits = _grep_vendor_hits(REPO_ROOT, [
        "template/.opencode/agents/**/*.md",
        "template/.opencode/opencode.json",
        "template/.opencode/opencode.jsonc",
    ])
    assert not hits, "vendor slug patterns in template/.opencode: " + repr(hits)


def test_us0123_example_catalog_placeholders_only():
    """Marker 3: example catalog exists; role values are <your-*-slug> placeholders only."""
    assert EXAMPLE_CATALOG.is_file(), "example catalog missing"
    data = json.loads(EXAMPLE_CATALOG.read_text(encoding="utf-8"))
    roles = data.get("roles", {})
    for role in ("po", "tech-lead", "dev", "qa", "release", "curator", "security", "auto"):
        value = roles.get(role)
        assert isinstance(value, str), f"role {role} missing string value"
        assert PLACEHOLDER_ROLE_RE.match(value.strip()), f"role {role} not placeholder form: {value}"
        slug = value.split("/", 1)[1]
        if not slug.startswith("<your-") and VENDOR_SLUG_RE.search(slug):
            raise AssertionError(f"real vendor slug in role {role}: {slug}")


def test_us0123_example_catalog_per_role_divergence():
    """Marker 4: ≥2 roles have different providers in the example catalog."""
    data = json.loads(EXAMPLE_CATALOG.read_text(encoding="utf-8"))
    providers = {
        str(v).split("/", 1)[0].strip()
        for v in data.get("roles", {}).values()
        if isinstance(v, str) and "/" in v
    }
    assert len(providers) >= 2, f"expected ≥2 providers, got {providers}"


def test_us0123_fail_closed_unknown_slug():
    """Marker 5: materializer fail-closed on empty/unknown/placeholder slug."""
    bad_catalogs = [
        {"schema_version": 2, "providers": {"deepseek": {"npm": "@ai-sdk/deepseek"}}, "roles": {
            "po": "deepseek/", "tech-lead": "deepseek/x", "dev": "deepseek/<your-deepseek-slug>",
            "qa": "deepseek/real-slug", "release": "deepseek/real-slug",
            "curator": "deepseek/real-slug", "security": "deepseek/real-slug", "auto": "deepseek/real-slug",
        }},
        {"schema_version": 2, "providers": {"deepseek": {"npm": "@ai-sdk/deepseek"}}, "roles": {
            "po": "deepseek/<your-deepseek-slug>", "tech-lead": "deepseek/<your-deepseek-slug>",
            "dev": "deepseek/<your-deepseek-slug>", "qa": "deepseek/<your-deepseek-slug>",
            "release": "deepseek/<your-deepseek-slug>", "curator": "deepseek/<your-deepseek-slug>",
            "security": "deepseek/<your-deepseek-slug>", "auto": "deepseek/<your-deepseek-slug>",
        }},
    ]
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        agents = tmp_path / ".opencode" / "agents"
        agents.mkdir(parents=True)
        for role in ("po", "tech-lead", "dev", "qa", "release", "curator", "security", "auto"):
            src = AGENTS_DIR / f"{role}.md"
            (agents / f"{role}.md").write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        catalog_path = tmp_path / ".opencode" / "model-catalog.local.json"
        for catalog in bad_catalogs:
            catalog_path.write_text(json.dumps(catalog), encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(MATERIALIZER), "--target", str(tmp_path)],
                capture_output=True,
                text=True,
            )
            combined = (proc.stdout or "") + (proc.stderr or "")
            assert proc.returncode != 0, f"expected non-zero for bad catalog: {catalog}"
            assert "OPENCODE_MODEL_SLUG_UNKNOWN" in combined, combined


def test_us0123_materializer_no_op_when_catalog_absent():
    """Marker 6: absent catalog → no-op exit 0; agents keep model: omitted."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        agents = tmp_path / ".opencode" / "agents"
        agents.mkdir(parents=True)
        for role in ("po", "dev"):
            agent_text = (AGENTS_DIR / f"{role}.md").read_text(encoding="utf-8")
            (agents / f"{role}.md").write_text(agent_text, encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(MATERIALIZER), "--target", str(tmp_path)],
            capture_output=True,
            text=True,
        )
        assert proc.returncode == 0, proc.stderr
        for role in ("po", "dev"):
            text = (agents / f"{role}.md").read_text(encoding="utf-8")
            assert "model:" not in text.split("---", 2)[1], f"model injected for {role}"


def test_us0123_auth_store_never_in_template_or_git():
    """Marker 7: no auth secrets in agent surfaces; gitignore covers *.local.json."""
    hits: list[str] = []
    for sub in ("agents", "commands", "plugins"):
        root = REPO_ROOT / "template" / ".opencode" / sub
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            for line_num, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                if AUTH_SECRET_RE.search(line):
                    hits.append(f"{path}:{line_num}:{line.strip()}")
    assert not hits, "auth/secret patterns in template/.opencode pack surfaces: " + repr(hits)
    gitignore = OPENCODE_GITIGNORE.read_text(encoding="utf-8")
    assert "*.local.json" in gitignore, ".opencode/.gitignore must cover *.local.json"
    assert "auth.json" in gitignore, ".opencode/.gitignore must list auth.json defense-in-depth"


def test_us0123_compose_cursor_unchanged():
    """Marker 8: Cursor catalog schema + scratchpad MODEL_* keys remain Cursor-side."""
    assert CURSOR_CATALOG_EXAMPLE.is_file()
    cursor_data = json.loads(CURSOR_CATALOG_EXAMPLE.read_text(encoding="utf-8"))
    assert "tiers" in cursor_data
    assert "schema_version" in cursor_data
    assert "roles" not in cursor_data or "providers" not in cursor_data or cursor_data.get("schema_version") != 2

    scratch = SCRATCHPAD.read_text(encoding="utf-8")
    for key in (
        "MODEL_TIER_",
        "MODEL_EXECUTE",
        "MODEL_PROVIDER_MODE",
        "MODEL_RESOLVE",
        "TOKEN_PROFILE",
    ):
        assert key in scratch, f"missing Cursor-side key family: {key}"
