# OpenAPI Runbook

## Purpose

Defines how the Backend Agent keeps OpenAPI/Swagger documentation aligned with actual API
behavior, regardless of whether the repository is contract-first or code-first.

## When to Use

Any change that adds, modifies, or removes an HTTP API surface. For the broader workflow
of changing an API (request/response models, validation, business logic, error mapping),
see [../api-change/RUNBOOK.md](../api-change/RUNBOOK.md) — this runbook focuses
specifically on the OpenAPI/documentation dimension.

## Inputs

The assigned API contract (`backend-assignment.yaml` → `contracts.api`), the repository's
existing OpenAPI source of truth (if any), and the applicable framework
`CODE-STANDARDS.md` (for the framework's OpenAPI integration mechanism).

## Execution Steps

1. Identify the OpenAPI source of truth already in use in the repository:
   - **contract-first** — an OpenAPI spec file is the source of truth and
     implementation is generated from or validated against it;
   - **code-first** — OpenAPI is generated from annotations/decorators/code.
   Identifying which strategy is in effect is inspecting the assigned implementation
   context, not choosing an architecture — see
   [../../SKILL.md](../../SKILL.md#assignment-validation).
2. Preserve whichever strategy the repository already uses — do not switch a
   contract-first repository to code-first, or vice versa, without an explicit task
   instruction to do so.
3. Never let the spec and the runtime implementation diverge into two conflicting
   sources of truth — whichever is authoritative drives the other.
4. Document status/error responses (not just the happy path) and validation constraints
   where the framework's OpenAPI integration supports it.
5. Preserve the repository's existing naming and versioning conventions for
   paths/schemas.
6. If the repository has tooling to validate the generated/documented schema (e.g. spec
   linting, contract tests against the spec), run it.

## Escalation / Stop Conditions

Treat any change to a shared contract (request/response shape, endpoint, error format)
that was not already pre-approved as an escalation, not a documentation update — see
[../../SKILL.md](../../SKILL.md#contract-ownership) and the shared stop conditions in
[../README.md](../README.md#stop-conditions).

## Result Expectations

If the OpenAPI/contract surface changed, set `contracts.changed: true` in
`backend-result.yaml` and describe the change under `contracts.proposed_changes` when it
was not pre-approved. See
[../../templates/backend-result.yaml](../../templates/backend-result.yaml).

## Related Standards / Runbooks

- [../api-change/RUNBOOK.md](../api-change/RUNBOOK.md)
- The applicable framework `CODE-STANDARDS.md` (OpenAPI integration section).
- [../../SKILL.md](../../SKILL.md#contract-ownership)
