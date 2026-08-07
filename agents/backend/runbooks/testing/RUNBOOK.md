# Testing Runbook

## Purpose

Defines how the Backend Agent plans and executes implementation-level validation. This
is the general method every other runbook's "task-specific validation" builds on — it is
not repeated in full inside them.

## When to Use

Every backend change. Testing is planned as part of the implementation
(see [../../SKILL.md](../../SKILL.md#test-execution-as-part-of-the-work-plan)), not a
category some tasks opt into.

## Inputs

The assignment (`backend-assignment.yaml`), the applicable language/framework
`CODE-STANDARDS.md` (for ecosystem-specific test mechanisms — mocking, fixtures, async
test support, etc.), and the repository's existing test setup.

## Before Implementation

- Inspect the repository's existing test tooling (test runner, assertion library,
  fixture/mocking conventions) rather than introducing a new one.
- Identify the existing unit/integration test structure and where new tests belong.
- Identify which modules are affected by the change.
- Identify the relevant test commands for the affected area.
- Determine whether the change requires unit tests, integration tests, or both — an
  integration test is required whenever the change crosses a real implementation
  boundary (persistence, HTTP, messaging, framework wiring); a task-specific runbook may
  name this explicitly for its category.

## During Implementation

- Add or update tests alongside the behavioral change — not as a separate follow-up step.
- Cover both the success path and failure/edge paths.
- Preserve test isolation: no dependence on execution order or shared mutable state
  between tests.
- Mock/fake external boundaries, not internal collaborators — avoid unnecessary mocking.
- Use the applicable language/framework standard for ecosystem-specific test mechanisms
  (parameterization, async test support, framework test slices, Testcontainers, etc.).

## Execution Order

```text
targeted unit tests
    ↓
targeted integration tests
    ↓
build / compile
    ↓
lint / static analysis
    ↓
broader regression scope when risk warrants it
```

## Failure Behavior

- Do not hide a test failure.
- Determine whether the failure is caused by the implementation, the environment, or
  pre-existing repository state.
- Fix implementation-caused failures.
- Report unrelated/pre-existing failures clearly rather than silently working around
  them or claiming they're unrelated without checking.
- Never mark validation as passed when it did not actually run.

## Escalation / Stop Conditions

If required validation cannot be run and continuing would be unsafe, stop and report —
see the shared stop conditions in [../../SKILL.md](../../SKILL.md#stop-conditions).

## Result Expectations

Populate `backend-result.yaml`'s `validation.unit_tests` / `validation.integration_tests`
/ `validation.build` / `validation.lint` / `validation.static_analysis` accurately: a
real `status` (`passed` / `failed` / `not_run` / `not_applicable`), the `command` run, and
— when `status` is `not_run` — a `reason`. See
[../../templates/backend-result.yaml](../../templates/backend-result.yaml).

## Related Standards / Runbooks

- [../../policies/global/CODE-STANDARDS.md](../../policies/global/CODE-STANDARDS.md#testing)
- The applicable language/framework `CODE-STANDARDS.md` for ecosystem-specific mechanisms.
- Task-specific runbooks (api-change, database-change, messaging-change,
  external-integration) for what must be tested for that category.
