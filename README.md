# Agent Orchestration for Application Creation

A system for running and orchestrating specialized software-development Agents.

A user describes an application or website in natural language. The system interprets
that requirement and coordinates specialized engineering Agents to design, implement,
test, review, secure, package, and eventually release the resulting software.

## Status: foundation stage

This project is currently in its **foundation stage**. Only repository-wide conventions
and the first Agent — the **Backend Agent** — exist so far. Orchestration across Agents
(the Team Lead) is not implemented yet, and no functionality beyond the Backend Agent's
own Skill definition should be assumed to work.

## Agent model

Agents are organizational software-engineering roles, not hard-coded prompts or
Claude-specific subagents. Each Agent is defined by a portable **Skill**: the
instructions, policies, templates, and runbooks needed to perform that role. A Skill
should be consumable by any compatible coding runtime (Claude Code, Codex, Cursor, or
others) — this is the **Agent via Skill** principle. Agents may internally delegate to
subagents/workers to organize their own work, but subagents are an implementation detail,
not the system's orchestration abstraction.

Planned Agent roles:

- Team Lead
- Requirements
- Product
- UX/UI
- Architect
- Backend
- Frontend
- QA
- DevOps
- Code Review
- Security
- Release

[AGENTS.md](AGENTS.md) is the canonical, runtime-neutral routing entrypoint: global
invariants, instruction precedence, canonical-vs-explanatory, and a task-routing table
into the focused repository-development policies under [policies/](policies/).

## What exists today

- [AGENTS.md](AGENTS.md) — canonical, runtime-neutral repository-wide router.
- [policies/](policies/README.md) — routed repository-development policies (branching,
  Git/PR/merge, validation/clean-exit, Issue/PR authoring, Skill development). These
  govern development of *this* repository and are never packaged with an Agent Skill.
- [agents/backend/](agents/backend/SKILL.md) — the Backend Agent Skill: role, boundaries,
  self-validation expectations, and the policy/template/runbook structure it composes
  language- and framework-specific behavior from.
- [Agent HLD template](docs/templates/AGENT_HLD_TEMPLATE.md) and
  [Agent LLD template](docs/templates/AGENT_LLD_TEMPLATE.md) — canonical, human-readable
  formats for future Agent research and design documents under `docs/agents/<agent-name>/`.
- [.github/](.github/) — the Engineering Task Issue Form
  ([.github/ISSUE_TEMPLATE/engineering-task.yml](.github/ISSUE_TEMPLATE/engineering-task.yml))
  and the Pull Request template.

Nothing beyond this exists yet. In particular, there is no Team Lead orchestration, no
Requirements Agent intake, no other Agents, and no execution engine.

## Repository Validation (CI)

Every Pull Request against `main` runs the **`Repository Validation`** GitHub Actions
check ([.github/workflows/repository-validation.yml](.github/workflows/repository-validation.yml)).
It is deterministic and calls no LLM/API — it checks repository integrity (Markdown
encoding/formatting, internal link resolution, required repository/Agent files), the
portable-Agent-Skill boundary (no operational file under `agents/<agent>/` depends on
root `AGENTS.md` / `policies/`), and machine-checkable Agent contracts (required Skill
sections, boundary statements, policy/runbook cross-references). This is distinct from —
and not a substitute for — human or LLM-based code review.

Run it locally the same way CI does:

```bash
python scripts/validate_repository.py
pytest tests
```

`Repository Validation` is intended to be selected as a required status check once a
branch protection Ruleset is configured for this repository (used together with
"Require branches to be up to date before merging"). Scenario-based or model-backed
Agent behavioral evals are an intentionally separate, future extension — not part of
this required check, since they may be nondeterministic, costly, or depend on external
services.
