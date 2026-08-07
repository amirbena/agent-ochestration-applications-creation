# Backend Templates

This directory holds two different kinds of template; do not conflate them.

## Execution-contract templates (present)

- [backend-assignment.yaml](backend-assignment.yaml) — the canonical input contract from
  the Team Lead to the Backend Agent.
- [backend-result.yaml](backend-result.yaml) — the canonical output contract the Backend
  Agent returns to the Team Lead.

These are structural contracts, not optional accelerants — see
[../SKILL.md](../SKILL.md#execution-contract) for how the Backend Agent uses them. They
are canonical templates only; no parser, validator, or schema engine exists yet.

## Implementation/scaffolding templates (not yet included)

Reusable implementation/reference starting points (e.g. a service skeleton or Dockerfile
baseline) are optional accelerants, not mandatory generated boilerplate — the Backend
Agent may use, adapt, or ignore them based on the task's approved architecture and
repository-local conventions. None are included yet. Future examples, organized by
framework, may include:

```text
templates/spring-boot/
templates/nestjs/
templates/fastapi/
```
