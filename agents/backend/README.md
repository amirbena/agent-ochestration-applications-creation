# Backend Agent

Human-facing overview of the Backend Agent Skill. This file is documentation for
developers/maintainers — it is **not** the canonical operational instruction source. The
canonical, runtime-neutral definition of how the Backend Agent behaves is
[SKILL.md](SKILL.md); if anything here ever conflicts with it, `SKILL.md` wins.

## What this Skill is

The Backend Agent is a portable software-engineering Agent responsible for implementing
backend work assigned through the orchestration system. It operates under:

```text
Architect
   ↓
Team Lead
   ↓
Backend Agent
```

The Architect defines the approved architecture and technology stack. The Team Lead
delegates the assignment. The Backend Agent implements and validates the backend change
within that assignment — it does not choose the stack or own architecture decisions. See
[SKILL.md](SKILL.md#technology-stack-ownership) for the full ownership model.

## Agent via Skill

The Backend Agent is defined as a portable **Skill**, not as a Claude-specific subagent.
The Skill (this directory) should be consumable by any compatible coding runtime — Claude
Code, Codex, Cursor, or others — per the repository-wide model in
[../../AGENTS.md](../../AGENTS.md#agent-model). The Backend Agent may internally use
subagents/workers as an execution mechanism to decompose its own work, but that is an
implementation detail: it does not change the external contract with the Team Lead — see
[SKILL.md](SKILL.md#execution-contract).

## Skill composition

The Backend Agent's applicable behavior for a given assignment is composed, not
hard-coded:

```text
SKILL.md
   +
global CODE-STANDARDS
   +
assigned language CODE-STANDARDS
   +
assigned framework CODE-STANDARDS
   +
repository-local instructions
   +
approved task / architecture / contracts
```

See [SKILL.md](SKILL.md#multi-language-architecture) for the full loading order and
precedence rules.

## Directory overview

- **`SKILL.md`** — the canonical operational definition: role, boundaries, execution
  workflow, policy loading, escalation behavior.
- **`metadata/`** — declarative, machine-readable Skill metadata (identity, capabilities,
  assignment/result contract shape). Describes *what* the Skill is, not *how* it behaves.
- **`policies/`** — normative code/engineering standards: global, per-language, and
  per-framework `CODE-STANDARDS.md` files.
- **`templates/`** — canonical structured artifacts, including the Team Lead ↔ Backend
  Agent execution-contract templates (`backend-assignment.yaml`, `backend-result.yaml`).
- **`runbooks/`** — repeatable engineering workflows, one `RUNBOOK.md` per class of work
  (testing, OpenAPI, debugging, database change, API change, messaging change, external
  integration, production fix). A task may draw on more than one.

## Currently supported policy set

Languages:

- Java
- Kotlin
- TypeScript
- Python
- Go
- Rust

Frameworks:

- Spring Boot (Java, Kotlin)
- NestJS (TypeScript)
- FastAPI (Python)
- Gin (Go)
- Axum (Rust)
- Actix Web (Rust)

This list is not closed — see [policies/languages/CODE-STANDARDS.md](policies/languages/CODE-STANDARDS.md)
and [policies/frameworks/CODE-STANDARDS.md](policies/frameworks/CODE-STANDARDS.md) for
how to add more.

## What this is not

This Skill defines the Backend Agent's role, standards, and execution contract. It does
not implement a runtime execution engine, orchestration, a Team Lead, or an Architect
Agent — those remain future work referenced only for context. No policy-resolution engine
or contract schema validator exists yet; the templates under `templates/` are canonical
documents, not executable code.
