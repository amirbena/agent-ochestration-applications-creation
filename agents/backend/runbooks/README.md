# Backend Runbooks

Human-facing overview of the Backend Agent's runbooks. This file explains what runbooks
are and holds the cross-cutting guidance shared across all of them; it is not itself a
canonical workflow. Canonical, operational workflow content lives in each `RUNBOOK.md`.

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

## Stop Conditions

Across all runbooks, the Backend Agent stops and reports (`result.status: blocked` in
`backend-result.yaml`, per [../templates/backend-result.yaml](../templates/backend-result.yaml))
when:

- the assigned architecture and repository materially conflict;
- a shared contract must change without approval;
- required architecture information is missing;
- a destructive database change is ambiguous;
- required credentials/environment are unavailable;
- validation cannot be completed and continuing would be unsafe;
- resolving the issue requires another Agent's ownership.

Individual runbooks reference this list rather than restating it, adding only
category-specific stop conditions where they exist.

## Transactions and Consistency

Relevant runbooks (API + database, messaging + database, external call + persistence,
multi-step state transitions) should have the Backend Agent consider:

- transaction boundaries;
- idempotency;
- optimistic/pessimistic locking, if the architecture uses it;
- outbox/inbox patterns, if assigned;
- reconciliation, if required;
- partial failure;
- retry duplication.

The Backend Agent uses only what the approved architecture/repository already supports —
it does not introduce a new consistency pattern unilaterally. If correctness requires an
architecture-level decision that hasn't been made, escalate (see "Stop Conditions"
above).

## Observability

Relevant runbooks require validating operational observability as part of the change:

- meaningful structured logs;
- correlation/trace propagation where the repository supports it;
- metrics for failure/retry paths where the repository supports them;
- no secret leakage;
- no excessive log noise.

This is a workflow checklist, not a restatement of the logging standard — see
[../policies/global/CODE-STANDARDS.md](../policies/global/CODE-STANDARDS.md#logging) for
the full logging rules.

## Result Expectations

Every runbook states what it expects reflected in `backend-result.yaml` for its category
(files changed, tests added/run, validation results, contract changes/proposals,
architecture concerns, blockers, risks, follow-up) — but there is only ever one canonical
result format. Runbooks do not define their own result schema; see
[../templates/backend-result.yaml](../templates/backend-result.yaml).
