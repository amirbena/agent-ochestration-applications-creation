# API-Change Runbook

## Purpose

Defines how the Backend Agent implements changes to HTTP/RPC-style application APIs,
keeping contract implementation separate from contract modification.

## When to Use

Adding, extending, or modifying an application API endpoint/operation.

## Inputs

The assigned API contract (`backend-assignment.yaml` → `contracts.api`), approved
architecture/requirement, the repository's existing API conventions, and the applicable
framework `CODE-STANDARDS.md`.

## Execution Steps

1. Read the approved requirement and architecture for this task.
2. Inspect the repository's existing API conventions (routing, response shape, error
   format, versioning).
3. Inspect the assigned contract/OpenAPI source of truth — see
   [../openapi/RUNBOOK.md](../openapi/RUNBOOK.md).
4. Determine which of these the work actually is:
   - **contract implementation** — implementing an already-approved contract;
   - **backward-compatible extension** — e.g. a new optional field, a new endpoint that
     doesn't affect existing consumers;
   - **contract modification** — changes the shape/meaning of an existing shared
     contract.
5. If the work is a contract modification that was not already approved, stop and
   escalate before implementing it — see "Escalation / Stop Conditions" below.
6. Implement request/response models.
7. Implement request validation at the boundary.
8. Implement the business/service behavior.
9. Implement error mapping to the repository's existing error-response convention.
10. Update OpenAPI/Swagger documentation where applicable — see
    [../openapi/RUNBOOK.md](../openapi/RUNBOOK.md).
11. Add unit tests for the request/response models, validation, and service behavior.
12. Add integration/API tests exercising serialization and the real routing/framework
    layer — see [../testing/RUNBOOK.md](../testing/RUNBOOK.md).
13. Validate backward compatibility where required (existing consumers must still work
    against the new response shape/behavior).
14. Run build/static checks.
15. Report any contract change explicitly, even a backward-compatible one — silence is
    not acceptable for shared-contract changes.

## Escalation / Stop Conditions

Stop and report before implementing an unapproved contract modification — do not
implement it "as if" it were approved. See
[../../SKILL.md](../../SKILL.md#contract-ownership) and the shared stop conditions in
[../README.md](../README.md#stop-conditions).

## Result Expectations

Set `contracts.changed` accurately in `backend-result.yaml`; if a modification was
proposed rather than pre-approved, list it under `contracts.proposed_changes` and set
`result.status: blocked` if the task cannot proceed without approval. Report unit and
API/integration test results under `validation`.

## Related Standards / Runbooks

- [../openapi/RUNBOOK.md](../openapi/RUNBOOK.md)
- [../testing/RUNBOOK.md](../testing/RUNBOOK.md)
- [../../SKILL.md](../../SKILL.md#contract-ownership)
- The applicable framework `CODE-STANDARDS.md` (request/response handling, validation,
  exception mapping sections).
