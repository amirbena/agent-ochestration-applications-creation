# CI Demo Agent

Temporary, disposable Agent used only to demonstrate this repository's CI and Git
lifecycle (branch -> PR -> validation -> merge -> sync -> fix). It is not a production
Agent, is not referenced by [AGENTS.md](../../AGENTS.md), and performs no real
implementation work. It exists solely so a CI demonstration has a safe, isolated path to
change without touching the Backend Agent or any other production Agent.

## Role

Demonstrates the repository's Agent contract and CI validation flow. It does not design,
implement, test, review, secure, package, or release software.

## Input Authority

This Agent receives no assignments and has no upstream authority. It is not part of the
orchestration flow described in [AGENTS.md](../../AGENTS.md) and must never be wired into
it.

## Execution Contract

There is no execution contract. This Agent is not invoked by a Team Lead, another Agent,
or any runtime. Its only purpose is to exist as a minimal, valid `agents/<agent>/SKILL.md`
directory for CI demonstration purposes.

## Technology Stack Ownership

This Agent owns no technology stack and makes no stack decisions.

## Responsibilities

- Provide a small, isolated surface for demonstrating CI validation (pass and fail cases).
- Stay disposable: safe to delete at any time without affecting any real Agent.

## Boundaries

- Must never be treated as a production Agent.
- Must never be referenced from the Backend Agent or any other production Agent.
- Must never gain real responsibilities, policies, runbooks, or templates.
- Must never be used to implement application code or architecture changes.

## Contract Ownership

This Agent owns no contracts. It does not define or consume any shared API, schema, or
data contract.

## Assignment Validation

Not applicable. This Agent accepts no assignments.

## Stop Conditions

Any attempt to use this Agent for real implementation work, or to reference it from a
production Agent, is a stop condition — remove the reference and keep this Agent isolated.

## Self-Validation

Before any change under this directory is committed, confirm:

- the change stays inside `agents/ci-demo-agent/`;
- no production Agent file is modified;
- repository Markdown validation still passes for this file.

## Structure

```text
agents/ci-demo-agent/
  SKILL.md   this file
```
