# Backend Runbooks

Human-facing overview of the Backend Agent's runbooks. This file explains what runbooks
are, how they relate to standards/templates, and which ones exist — it is not itself
canonical. Canonical, operational workflow content lives in each `RUNBOOK.md`; canonical
cross-cutting behavioral rules live in [SKILL.md](../SKILL.md).

## What a runbook is

A runbook answers: *what sequence should the Backend Agent follow for this kind of
engineering task?* It defines a repeatable execution workflow — inputs, steps,
validation, and escalation conditions — for one class of backend work.

## How runbooks differ from standards and templates

```text
SKILL.md          = Agent behavior / ownership / boundaries
CODE-STANDARDS.md = how production code should be written
runbooks/          = how a class of backend work should be executed safely
templates/         = structured reusable artifacts/contracts
```

Runbooks stay broadly language/framework neutral. Where implementation detail differs by
ecosystem (e.g. how to write an idempotent consumer in a specific framework), a runbook
references the applicable `CODE-STANDARDS.md` rather than duplicating it.

## Available runbooks

- [testing/RUNBOOK.md](testing/RUNBOOK.md) — the general validation method every other
  runbook builds on.
- [openapi/RUNBOOK.md](openapi/RUNBOOK.md) — keeping API documentation aligned with
  implementation.
- [debugging/RUNBOOK.md](debugging/RUNBOOK.md) — evidence-first defect diagnosis and fix.
- [database-change/RUNBOOK.md](database-change/RUNBOOK.md) — schema/persistence changes.
- [api-change/RUNBOOK.md](api-change/RUNBOOK.md) — HTTP/RPC API changes.
- [messaging-change/RUNBOOK.md](messaging-change/RUNBOOK.md) — producer/consumer changes
  against a message broker.
- [external-integration/RUNBOOK.md](external-integration/RUNBOOK.md) — calls to
  third-party APIs/services.
- [production-fix/RUNBOOK.md](production-fix/RUNBOOK.md) — urgent fixes under
  blast-radius control.

This list is not closed.

## Runbooks may be composed

A single assignment may require more than one runbook — the Backend Agent composes the
relevant ones rather than forcing the task into a single category. For example, "add an
endpoint that stores data and publishes an event" draws on:

```text
api-change + database-change + messaging-change + testing
```

This is not an automated selection engine — see
[../SKILL.md](../SKILL.md#runbook-selection) for how the Backend Agent identifies
applicable runbooks from the assigned task.

## Runbooks do not override architecture authority

Runbooks define execution sequence. They do not grant architecture authority and never
override, in order of precedence: the approved task, architecture, contracts,
repository-local explicit instructions, or applicable code standards — see
[../SKILL.md](../SKILL.md#precedence).

## Shared cross-cutting rules

The following are canonical Agent behavior, not runbook-specific content, so they are
defined once in `SKILL.md` and referenced by anchor from individual runbooks rather than
restated here or per runbook:

- [Stop Conditions](../SKILL.md#stop-conditions) — when the Backend Agent stops and
  reports a blocker instead of proceeding.
- [Transactions and Consistency](../SKILL.md#transactions-and-consistency) — what to
  consider for API+database, messaging+database, external-call+persistence, and other
  multi-step state transitions.
- [Observability](../SKILL.md#observability) — the operational-logging/observability
  checklist applied during validation.

Every runbook's `backend-result.yaml` output uses the single canonical result format —
see [../templates/backend-result.yaml](../templates/backend-result.yaml); runbooks do not
define their own result schema.
