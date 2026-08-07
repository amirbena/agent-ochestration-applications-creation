# External-Integration Runbook

## Purpose

Defines how the Backend Agent implements calls to third-party APIs/services/providers,
without inventing resilience architecture the task didn't assign.

## When to Use

Any change that adds or modifies a call to an external (third-party or another team's)
API/service.

## Inputs

The approved integration contract (`backend-assignment.yaml` → `contracts.external`,
`architecture.decisions`), the provider's documented API, and any existing adapter/client
pattern already in the repository.

## Execution Steps

1. Inspect the approved integration contract — endpoint(s), auth mechanism, expected
   request/response shape.
2. Respect the authentication/credential boundary — use the repository's existing
   secrets/credentials mechanism; never hard-code or log a credential (see
   [../../policies/global/CODE-STANDARDS.md](../../policies/global/CODE-STANDARDS.md#logging)).
3. Apply the timeout policy already used by the repository for external calls, or the
   one specified by the architecture; do not leave a call unbounded.
4. Apply the retry policy already assigned/established — distinguish retryable failures
   (timeouts, 5xx, connection errors) from non-retryable ones (4xx validation errors,
   auth failures) and do not retry the latter.
5. Confirm idempotency before retrying a call that has side effects — only retry safely
   when the operation is idempotent or an idempotency key is used.
6. Handle rate limiting / HTTP 429 responses according to the provider's documented
   contract (e.g. respecting a `Retry-After` header) if the task/architecture calls for
   it.
7. Use circuit-breaking behavior only where the approved architecture already provides
   it — do not introduce a circuit breaker unilaterally (see "Escalation / Stop
   Conditions" below).
8. Translate provider errors into the repository's internal error model rather than
   leaking provider-specific error shapes upward.
9. Validate the response shape at the boundary — do not trust an external response
   without validation.
10. Be aware of external schema drift — the provider's actual response can diverge from
    documentation; validate defensively rather than assuming exact conformance.
11. Log integration failures with useful context and without secrets (API keys, tokens,
    full request/response bodies containing sensitive data) — see
    [../../SKILL.md](../../SKILL.md#observability).
12. Add metrics/observability for the integration's failure and latency behavior where
    the repository already supports it.
13. Use test doubles/fakes for the provider in unit tests — do not call the real
    external service from a unit test.
14. Add controlled integration tests where possible (e.g. against a sandbox environment,
    a recorded-response fixture, or a local mock server) — see
    [../testing/RUNBOOK.md](../testing/RUNBOOK.md).
15. Implement fallback/degradation behavior only if the approved architecture specifies
    one — do not invent a fallback path unilaterally.

## Escalation / Stop Conditions

If required resilience behavior (retry policy, circuit breaker, fallback, rate-limit
handling) is not defined by the approved architecture and the integration genuinely needs
it for correctness, escalate rather than inventing the architecture — see the shared stop
conditions in [../../SKILL.md](../../SKILL.md#stop-conditions).

## Result Expectations

Report which resilience behaviors were implemented vs assumed-present in the
architecture, and note any gap under `architecture.concerns` or `risks` in
`backend-result.yaml`. Report unit test (fakes) and any integration test results under
`validation`.

## Related Standards / Runbooks

- [../testing/RUNBOOK.md](../testing/RUNBOOK.md)
- [../../SKILL.md](../../SKILL.md#transactions-and-consistency) — for external call +
  persistence consistency concerns.
- [../../policies/global/CODE-STANDARDS.md](../../policies/global/CODE-STANDARDS.md#logging)
