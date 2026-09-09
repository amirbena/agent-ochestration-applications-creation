# Agent Orchestration for Application Creation

A repository for building a system where specialized, runtime-neutral
software-engineering **Agents** collaborate to design and build software from a
natural-language description.

Today the repository contains the **foundation** for that system: the canonical rules
every Agent and contributor follows, the first Agent definition (the Backend Agent), and
the automation that keeps the repository consistent. The orchestration runtime that will
actually run Agents against a user's request is not built yet — see
[Current state](#current-state).

## What the project is building

The end vision:

1. A user describes an application or website in plain language.
2. A **Requirements** Agent turns that into a structured specification.
3. A **Team Lead** Agent plans the work and delegates it.
4. An **Architect** Agent decides the technology stack and high-level design.
5. Implementation Agents (**Backend**, **Frontend**, …) build within that design, with
   **QA**, **Code Review**, **Security**, **DevOps**, and **Release** Agents covering
   testing, review, hardening, packaging, and delivery.

Each role is a stable *Agent*; each Agent is defined by a portable *Skill* that any
compatible coding runtime can execute. See [How Agents are modeled](#how-agents-are-modeled).

## Current state

The repository is in its **foundation stage**. What that means concretely:

### Implemented today

| Area | What exists |
| --- | --- |
| Repository governance | [AGENTS.md](AGENTS.md) — the canonical, runtime-neutral entrypoint: global invariants, instruction precedence, and a task-routing table into the focused [policies/](policies/README.md) (branching, Git/PR/merge, validation & clean exit, Issue/PR authoring, Skill development, changelog discipline). |
| Backend Agent Skill | [agents/backend/](agents/backend/README.md) — the first Agent: role and boundaries in [SKILL.md](agents/backend/SKILL.md), composable global / per-language / per-framework `CODE-STANDARDS.md`, the Team Lead ↔ Backend execution-contract templates, and per-workflow runbooks. |
| Agent design format | [docs/templates/AGENT_HLD_TEMPLATE.md](docs/templates/AGENT_HLD_TEMPLATE.md) and [docs/templates/AGENT_LLD_TEMPLATE.md](docs/templates/AGENT_LLD_TEMPLATE.md) — the canonical shapes for future Agent research/design documents. |
| Repository automation | Three GitHub Actions workflows and three Issue Forms behind a template chooser, mapped in [.github/README.md](.github/README.md). |
| Validation tooling | [scripts/validate_repository.py](scripts/validate_repository.py) plus the [tests/](tests/) suite — deterministic, no LLM calls. |
| Change history | [CHANGELOG.md](CHANGELOG.md) with a `## Unreleased` workflow defined in [policies/changelog-policy.md](policies/changelog-policy.md). |

### Not implemented yet

Referenced throughout the docs for context, but **not** working functionality:

- Team Lead orchestration and cross-Agent coordination
- Requirements, Product, UX/UI, Architect, Frontend, QA, Code Review, Security, DevOps,
  and Release Agents
- LLM/model routing, a runtime execution engine, and any queues, databases, or APIs for
  the orchestration platform itself

The authoritative version of this list lives in
[AGENTS.md → Scope of This Repository Today](AGENTS.md#scope-of-this-repository-today).

## How Agents are modeled

The core principle is **Agent via Skill**:

- **Agent** — a stable software-engineering role (Backend, Frontend, Architect, QA, …),
  defined by responsibility and scope, independent of any tool or vendor.
- **Skill** — the portable operational definition of one Agent: its instructions,
  policies, runbooks, and templates. Authored once, consumed by any runtime.
- **Runtime** — the environment that executes a Skill (Claude Code, Codex, Cursor, or any
  other compatible coding agent).
- **Subagent / worker** — an optional internal mechanism an Agent may use to split up its
  own work. An implementation detail, never a top-level orchestration unit.

A Skill must stay correct when consumed on its own, so files under `agents/<agent>/` never
depend on the repository-root instructions. Full definitions and rationale are in
[AGENTS.md → Core Vocabulary](AGENTS.md#core-vocabulary-agent-via-skill).

## Repository structure

| Path | What it is | Look here to… |
| --- | --- | --- |
| [AGENTS.md](AGENTS.md) | Canonical repository-wide entrypoint (invariants, precedence, routing). | Understand the rules before making any change. |
| [policies/](policies/README.md) | Repository-development policies routed from `AGENTS.md`. Govern *this* repo; never packaged with an Agent Skill. | Find the detailed rule for branching, PRs, merges, validation, Skill authoring, or the changelog. |
| [agents/backend/](agents/backend/README.md) | The Backend Agent Skill. | See how an Agent is defined, bounded, and composed from standards + runbooks. |
| [.github/](.github/README.md) | Workflows, Issue Forms, and the PR template, with a navigational map. | See what automation runs and what it may change. |
| [scripts/](scripts/) | Deterministic validation / automation scripts (stdlib-only). | Run or read the repository checks. |
| [tests/](tests/) | Repository-structure and Agent-contract tests. | Confirm invariants are actually enforced, not just documented. |
| [docs/templates/](docs/templates/) | HLD/LLD templates for future Agent design work. | Start a new Agent's research/design document. |
| [CHANGELOG.md](CHANGELOG.md) | `## Unreleased` history of consumer-visible changes. | See what has changed recently. |

## Automation and validation

Two kinds of automation are kept deliberately separate:

- **Repository-development automation (exists today)** — keeps *this* repository
  consistent as it is built. It does not run Agents or build applications.
- **Application-creation runtime (planned)** — the future orchestration engine that will
  run Agents against a user's request. Not implemented.

The repository-development automation, all mapped in [.github/README.md](.github/README.md):

| Workflow | Trigger | Does |
| --- | --- | --- |
| [`repository-validation.yml`](.github/workflows/repository-validation.yml) | PR → `main` | Runs [`validate_repository.py`](scripts/validate_repository.py) and [`tests/`](tests/): Markdown integrity, required files, internal-link resolution, the portable-Skill boundary, and machine-checkable Agent contracts. Read-only. |
| [`pr-description-length.yml`](.github/workflows/pr-description-length.yml) | PR → `main` | Enforces a generous ceiling on a PR description's useful content ([`pr_description_length.py`](scripts/pr_description_length.py)). Read-only, no token. |
| [`sync-issue-labels.yml`](.github/workflows/sync-issue-labels.yml) | `issues` opened / edited | Reconciles an Issue's `type:*` / `area:*` / `priority:*` labels with its Engineering Task Form fields ([`sync_issue_labels.py`](scripts/sync_issue_labels.py)). Mutates labels only. |

`Repository Validation` and `PR Description Length` are required status checks on `main`,
alongside a pull-request review requirement. The validation check is deterministic and
calls no LLM/API — scenario-based or model-backed Agent evals are an intentionally
separate future extension, not part of this gate.

## Planned Agent roles

Only the **Backend** Agent has a Skill today. The rest are planned roles, referenced in
the docs for context:

Team Lead · Requirements · Product · UX/UI · Architect · **Backend** · Frontend · QA ·
Code Review · Security · DevOps · Release

New Agents follow the same `agents/<agent-name>/SKILL.md` convention and the design-doc
format in [docs/templates/](docs/templates/); see
[policies/skill-development-policy.md](policies/skill-development-policy.md).

## Getting started / local validation

There is no application to run yet — the useful local action is running the same checks
CI runs.

```bash
# Python 3.12+; pyyaml is needed for the full test suite
python -m pip install --upgrade pytest pyyaml

python scripts/validate_repository.py
python -m pytest tests
```

Then follow the workflow in [AGENTS.md](AGENTS.md): read the Global Invariants, route
through the [Task Routing](AGENTS.md#task-routing) table to the policy that owns your
task, work on a dedicated branch, and open a PR using the provided template.

## Further documentation

- [AGENTS.md](AGENTS.md) — canonical rules, precedence, and routing (read first).
- [policies/README.md](policies/README.md) — map of the repository-development policies.
- [.github/README.md](.github/README.md) — the automation and template map.
- [agents/backend/README.md](agents/backend/README.md) — the Backend Agent overview.
- [CHANGELOG.md](CHANGELOG.md) — recent consumer-visible changes.

Detailed governance and workflow rules are **not** duplicated here; each lives in its
canonical document linked above.
