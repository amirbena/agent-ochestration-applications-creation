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


def test_agents_md_is_a_router_not_a_procedural_monolith():
    """AGENTS.md keeps the routing scaffold and routes Git detail out to policies/."""
    agents_md = read("AGENTS.md")
    for marker in [
        "## Global Invariants",
        "## Instruction Precedence",
        "## Canonical vs. Explanatory",
        "## Task Routing",
        "One canonical home per normative rule",
        "policies/repository-workflow.md",
        "policies/git-pr-merge-policy.md",
        "policies/skill-development-policy.md",
    ]:
        assert marker in agents_md, f"AGENTS.md router is missing: {marker}"
    # The detailed Git procedure must no longer live in AGENTS.md.
    assert "## Git Methodology" not in agents_md
    assert "Squash-Merge Local Branch Deletion" not in agents_md


def test_git_branch_prefixes_documented_in_repository_workflow_policy():
    workflow = read("policies/repository-workflow.md")
    for prefix in ["feature/", "fix/", "refactor/", "docs/", "test/", "chore/"]:
        assert prefix in workflow, (
            f"expected branch prefix '{prefix}' documented in policies/repository-workflow.md"
        )


def test_root_policies_are_repository_development_only():
    readme = read("policies/README.md")
    assert "developing this repository" in readme.lower() or "development of this repository" in readme.lower()
    # The router routes to each policy exactly once as a canonical home.
    agents_md = read("AGENTS.md")
    for policy in [
        "policies/repository-workflow.md",
        "policies/git-pr-merge-policy.md",
        "policies/validation-and-clean-exit.md",
        "policies/github-issue-pr-authoring.md",
        "policies/skill-development-policy.md",
        "policies/changelog-policy.md",
    ]:
        assert (REPO_ROOT / policy).is_file(), f"missing root policy: {policy}"
        assert agents_md.count(f"[{policy}]({policy})") >= 1, f"AGENTS.md does not route to {policy}"


def test_no_shared_layer_introduced():
    assert not (REPO_ROOT / "shared").exists(), "shared/ must not be introduced yet"


def test_every_agent_directory_has_a_skill_md():
    agents_dir = REPO_ROOT / "agents"
    agent_dirs = [p for p in agents_dir.iterdir() if p.is_dir()]
    assert agent_dirs, "expected at least one Agent directory under agents/"
    for agent_dir in agent_dirs:
        assert (agent_dir / "SKILL.md").is_file(), (
            f"agents/{agent_dir.name} is missing SKILL.md"
        )
