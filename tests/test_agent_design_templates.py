"""Semantic checks for canonical Agent research/design documentation.

These tests protect required concepts and ownership boundaries without enforcing exact
prose, heading order, or template formatting.
"""

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
HLD_TEMPLATE = REPO_ROOT / "docs/templates/AGENT_HLD_TEMPLATE.md"
LLD_TEMPLATE = REPO_ROOT / "docs/templates/AGENT_LLD_TEMPLATE.md"
SKILL_POLICY = REPO_ROOT / "policies/skill-development-policy.md"
ISSUE_POLICY = REPO_ROOT / "policies/github-issue-pr-authoring.md"
README = REPO_ROOT / "README.md"

HLD_CONCEPTS = [
    "Purpose",
    "Position in the System",
    "Responsibilities",
    "Non-Responsibilities",
    "Authority and Decision Boundaries",
    "Inputs",
    "Outputs",
    "Agent Interactions",
    "Primary Workflows",
    "Parallelism and Ownership Boundaries",
    "Failure and Escalation Model",
    "Portability and Runtime Independence",
    "Key Design Decisions",
    "Open Questions",
]

LLD_CONCEPTS = [
    "Design Context",
    "Proposed Directory Structure",
    "SKILL.md Contract",
    "Metadata and Capabilities",
    "Assignment Contract",
    "Result Contract",
    "Policies",
    "Runbooks",
    "Templates",
    "Internal Workers / Subagents",
    "Workflow / State Model",
    "Validation",
    "Repository Integration",
    "Test Strategy",
    "Implementation Sequence",
    "Migration / Compatibility",
    "Remaining Implementation Questions",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_canonical_agent_design_templates_exist():
    assert HLD_TEMPLATE.is_file()
    assert LLD_TEMPLATE.is_file()


def test_hld_template_preserves_major_concepts():
    text = read(HLD_TEMPLATE)
    missing = [concept for concept in HLD_CONCEPTS if f"## {concept}" not in text]
    assert not missing, f"HLD template missing concepts: {missing}"
    assert "humans first and Agents second" in text
    assert "Non-Responsibilities" in text
    assert "Decision | Choice | Rationale" in text


def test_lld_template_preserves_major_concepts():
    text = read(LLD_TEMPLATE)
    missing = [concept for concept in LLD_CONCEPTS if f"## {concept}" not in text]
    assert not missing, f"LLD template missing concepts: {missing}"
    for marker in [
        "humans first and Agents second",
        "Agent = stable role",
        "Skill = portable operational definition",
        "Subagent / worker = internal execution mechanism",
        "N/A` is valid",
    ]:
        assert marker in text, f"LLD template missing semantic marker: {marker}"


def test_skill_policy_owns_agent_design_workflow_and_paths():
    text = read(SKILL_POLICY)
    for marker in [
        "## Agent research and design documents",
        "docs/agents/<agent-name>/HLD.md",
        "docs/agents/<agent-name>/LLD.md",
        "HLD owns architectural intent and boundaries; LLD owns implementation design.",
        "AGENT_HLD_TEMPLATE.md",
        "AGENT_LLD_TEMPLATE.md",
        "humans first and Agents second",
    ]:
        assert marker in text, f"Skill-development policy missing: {marker}"


def test_readme_and_issue_policy_link_without_copying_templates():
    for path in [README, ISSUE_POLICY]:
        text = read(path)
        assert "AGENT_HLD_TEMPLATE.md" in text
        assert "AGENT_LLD_TEMPLATE.md" in text
        hld_headings_copied = sum(f"## {heading}" in text for heading in HLD_CONCEPTS)
        lld_headings_copied = sum(f"## {heading}" in text for heading in LLD_CONCEPTS)
        assert hld_headings_copied < 3, f"{path.name} duplicates the HLD template"
        assert lld_headings_copied < 3, f"{path.name} duplicates the LLD template"


def test_agent_design_paths_do_not_create_premature_agent_directories():
    docs_agents = REPO_ROOT / "docs/agents"
    assert not docs_agents.exists() or not any(docs_agents.iterdir())
