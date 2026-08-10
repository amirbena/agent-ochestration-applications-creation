"""Deterministic structural checks for repository-wide invariants documented
in AGENTS.md ("Repository Layout") and README.md. No LLM/API calls.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def read(rel_path: str) -> str:
    return (REPO_ROOT / rel_path).read_text(encoding="utf-8")


def test_canonical_instruction_files_exist():
    for rel in ["AGENTS.md", "README.md", "CLAUDE.md", ".github/PULL_REQUEST_TEMPLATE.md"]:
        assert (REPO_ROOT / rel).is_file(), f"missing required file: {rel}"


def test_claude_md_is_a_thin_adapter_to_agents_md():
    claude_md = read("CLAUDE.md")
    assert "AGENTS.md" in claude_md, (
        "CLAUDE.md must point back to AGENTS.md as the canonical instruction source"
    )


def test_agents_md_declares_backend_agent_layout():
    agents_md = read("AGENTS.md")
    assert "agents/" in agents_md
    assert "backend/" in agents_md
    assert "SKILL.md" in agents_md


def test_agents_md_documents_git_branch_prefixes():
    agents_md = read("AGENTS.md")
    for prefix in ["feature/", "fix/", "refactor/", "docs/", "test/", "chore/"]:
        assert prefix in agents_md, f"expected branch prefix '{prefix}' documented in AGENTS.md"


def test_every_agent_directory_has_a_skill_md():
    agents_dir = REPO_ROOT / "agents"
    agent_dirs = [p for p in agents_dir.iterdir() if p.is_dir()]
    assert agent_dirs, "expected at least one Agent directory under agents/"
    for agent_dir in agent_dirs:
        assert (agent_dir / "SKILL.md").is_file(), (
            f"agents/{agent_dir.name} is missing SKILL.md"
        )
