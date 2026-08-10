"""Deterministic structural contract checks for Agent Skills.

These assert semantic structure (headings/markers/references exist) rather
than exact prose, so they stay robust to wording changes while still
catching a silently dropped responsibility, boundary, or reference. No
LLM/API calls are made.
"""

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = REPO_ROOT / "agents"

REQUIRED_SKILL_HEADINGS = [
    "## Role",
    "## Input Authority",
    "## Execution Contract",
    "## Technology Stack Ownership",
    "## Responsibilities",
    "## Boundaries",
    "## Contract Ownership",
    "## Assignment Validation",
    "## Stop Conditions",
    "## Self-Validation",
    "## Structure",
]

# Explicit ownership boundaries that must remain in place — these encode
# escalation rules from AGENTS.md ("Architecture Ownership") that the
# Backend Agent must not silently regain.
PROHIBITED_OWNERSHIP_MARKERS = [
    "Redefine or own the system architecture.",
    "Choose or infer the technology stack",
    "Merge, publish, or release code as if it were the Release Agent.",
    "Approve its own code review as if it were the Code Review Agent.",
]


def agent_dirs() -> list[Path]:
    return sorted(p for p in AGENTS_DIR.iterdir() if p.is_dir())


@pytest.fixture(params=agent_dirs(), ids=lambda p: p.name)
def agent_dir(request) -> Path:
    return request.param


def test_skill_md_has_required_sections(agent_dir: Path):
    skill_md = (agent_dir / "SKILL.md").read_text(encoding="utf-8")
    missing = [h for h in REQUIRED_SKILL_HEADINGS if h not in skill_md]
    assert not missing, f"{agent_dir.name}/SKILL.md missing sections: {missing}"


def test_metadata_skill_yaml_has_identity_fields():
    metadata = (AGENTS_DIR / "backend/metadata/skill.yaml").read_text(encoding="utf-8")
    for marker in ["id: backend", "reports_to: team-lead", "upstream_authority: architect-agent"]:
        assert marker in metadata, f"metadata/skill.yaml missing '{marker}'"


def test_backend_skill_preserves_prohibited_ownership_boundaries():
    skill_md = (AGENTS_DIR / "backend/SKILL.md").read_text(encoding="utf-8")
    missing = [m for m in PROHIBITED_OWNERSHIP_MARKERS if m not in skill_md]
    assert not missing, f"Backend SKILL.md dropped boundary statement(s): {missing}"


def test_backend_execution_contract_templates_exist():
    templates_dir = AGENTS_DIR / "backend/templates"
    assert (templates_dir / "backend-assignment.yaml").is_file()
    assert (templates_dir / "backend-result.yaml").is_file()


def test_backend_result_status_values_match_metadata():
    metadata = (AGENTS_DIR / "backend/metadata/skill.yaml").read_text(encoding="utf-8")
    result_template = (AGENTS_DIR / "backend/templates/backend-result.yaml").read_text(
        encoding="utf-8"
    )
    for status in ["completed", "completed_with_warnings", "blocked", "failed"]:
        assert status in metadata, f"metadata/skill.yaml missing status value '{status}'"
        assert status in result_template, (
            f"backend-result.yaml missing status value '{status}'"
        )


def test_supported_languages_have_a_policy_file():
    metadata = (AGENTS_DIR / "backend/metadata/skill.yaml").read_text(encoding="utf-8")
    match = re.search(r"languages:\n((?:\s+- .+\n)+)", metadata)
    assert match, "could not find supported_policies.languages in metadata/skill.yaml"
    languages = re.findall(r"- (\S+)", match.group(1))
    assert languages, "no languages parsed from metadata/skill.yaml"

    for language in languages:
        standard = AGENTS_DIR / "backend/policies/languages" / language / "CODE-STANDARDS.md"
        assert standard.is_file(), f"missing language policy file: {standard}"


def test_supported_frameworks_have_a_policy_file():
    metadata = (AGENTS_DIR / "backend/metadata/skill.yaml").read_text(encoding="utf-8")
    match = re.search(r"frameworks:\n((?:\s+- .+\n)+)", metadata)
    assert match, "could not find supported_policies.frameworks in metadata/skill.yaml"
    frameworks = re.findall(r"- (\S+)", match.group(1))
    assert frameworks, "no frameworks parsed from metadata/skill.yaml"

    for framework in frameworks:
        standard = (
            AGENTS_DIR / "backend/policies/frameworks" / framework / "CODE-STANDARDS.md"
        )
        assert standard.is_file(), f"missing framework policy file: {standard}"


def test_runbooks_listed_in_readme_exist_on_disk():
    runbooks_dir = AGENTS_DIR / "backend/runbooks"
    readme = (runbooks_dir / "README.md").read_text(encoding="utf-8")
    linked = re.findall(r"\[([\w-]+)/RUNBOOK\.md\]\(([\w-]+)/RUNBOOK\.md\)", readme)
    assert linked, "no runbook links found in runbooks/README.md"

    for name, path in linked:
        assert name == path
        runbook_file = runbooks_dir / path / "RUNBOOK.md"
        assert runbook_file.is_file(), f"runbooks/README.md references missing {runbook_file}"


def test_precedence_order_is_documented():
    skill_md = (AGENTS_DIR / "backend/SKILL.md").read_text(encoding="utf-8")
    start = skill_md.index("## Precedence")
    end = skill_md.index("## ", start + len("## Precedence"))
    section = skill_md[start:end]

    order = [
        "task/approved architecture",
        "repository-local explicit instructions",
        "framework policy",
        "language policy",
        "global backend policy",
    ]
    positions = [section.index(term) for term in order]
    assert positions == sorted(positions), "precedence order in SKILL.md changed unexpectedly"
