# Messaging-Change Runbook

## Purpose

Defines how the Backend Agent implements producer/consumer changes against a message
broker (Kafka, Pulsar, RabbitMQ, SQS/SNS, NATS, or equivalent). Technology-neutral —
broker-specific mechanisms come from the applicable framework `CODE-STANDARDS.md` or
repository convention.

## When to Use

Any change that produces to, or consumes from, a message/event broker.

## Inputs

The assigned event/message contract (`backend-assignment.yaml` → `contracts.events`),
approved architecture (ordering/delivery-semantics decisions if made), and the
repository's existing producer/consumer conventions.

## Execution Steps

1. Identify producer/consumer ownership — is this service the producer, the consumer, or
   both, for the message(s) involved.
2. Inspect the existing event/message contract (schema, topic/queue/exchange naming).
3. Identify ordering requirements — does correctness depend on message order, and if so,
   how is it currently preserved (partition key, single consumer, sequence field).
4. Identify delivery semantics already in effect (at-most-once, at-least-once,
   exactly-once) — do not assume a stronger guarantee than the broker/repository
   actually provides.
5. Identify partition/routing key requirements so related messages keep their required
   ordering/locality.
6. Identify idempotency requirements — at-least-once delivery means consumers must
   tolerate duplicates; confirm how the repository already handles this (idempotency
   key, dedup table, natural idempotency).
7. Identify retry behavior already configured (backoff, max attempts).
8. Identify DLQ/dead-letter behavior — where do permanently-failing messages go, and is
   that already configured or part of this task.
9. Identify timeout/failure behavior for both produce and consume paths.
10. Preserve backward/forward compatibility of the message schema — do not remove or
    repurpose a field consumers depend on; prefer additive changes.
11. Never change an event contract silently — see "Escalation / Stop Conditions" below.
12. Add producer/consumer unit tests (message construction, handler logic in isolation).
13. Add integration tests where broker-backed behavior matters (e.g. against a local/test
    broker or Testcontainers-style setup) — see
    [../testing/RUNBOOK.md](../testing/RUNBOOK.md).
14. Validate duplicate/retry behavior when the change affects it (replaying a message
    should not corrupt state if idempotency is required).
15. Validate consumer failure handling (a poison message should not block the whole
    partition/queue indefinitely, if that matters for this broker/task).
16. Validate observability where the repository supports it — consumer lag, error
    counts, structured logs on failure — see
    [../../SKILL.md](../../SKILL.md#observability).

## Escalation / Stop Conditions

If an event-contract change affects other services/Agents (any consumer or producer this
Backend Agent doesn't own), escalate unless the change was already approved — do not
change a shared schema silently. See the shared stop conditions in
[../../SKILL.md](../../SKILL.md#stop-conditions).

## Result Expectations

Set `contracts.changed` in `backend-result.yaml` when the message/event schema changed;
report producer/consumer test results under `validation`; report any DLQ/ordering/
idempotency risk under `risks` if not fully addressed by this change.

## Related Standards / Runbooks

- [../testing/RUNBOOK.md](../testing/RUNBOOK.md)
- [../../SKILL.md](../../SKILL.md#transactions-and-consistency) — for messaging + database
  consistency concerns (e.g. outbox pattern).
- [../../SKILL.md](../../SKILL.md#contract-ownership)
