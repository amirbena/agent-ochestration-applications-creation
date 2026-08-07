# Database-Change Runbook

## Purpose

Defines how the Backend Agent implements persistence changes — relational or
schema-less — while controlling data-loss and rollout risk. Does not prescribe one
migration tool; use whatever the repository already has.

## When to Use

Any change to persisted data shape: schema migrations, index changes, query changes with
data-shape implications, or NoSQL key/document-shape changes.

## Execution Steps

1. Inspect the approved persistence architecture for this task (from
   `backend-assignment.yaml` → `architecture.decisions` / `contracts.persistence`).
2. Inspect the repository's existing persistence conventions (ORM/query patterns,
   migration tooling, naming) — see
   [../../SKILL.md](../../SKILL.md#repository-local-rules).
3. Identify data-compatibility requirements: which existing rows/documents must remain
   valid, and under what constraints.
4. Identify migration/backfill requirements: does existing data need to be transformed,
   not just new schema/shape accepted going forward.
5. Assess rollout compatibility: can the old and new code paths coexist during a
   rolling deploy, or does the change require coordinated cutover.
6. Implement the persistence change.
7. Implement the migration/backfill when needed, using the repository's existing
   migration tooling rather than ad hoc scripts.
8. Keep migrations forward-safe where practical (see "Change-Specific Guidance" below).
9. Consider rollback/roll-forward implications — can this migration be reverted safely,
   and if not, say so explicitly in the result.
10. Update affected queries/indexes.
11. Add/update persistence-layer (repository/DAO) tests.
12. Add integration tests exercising the real (or realistic ephemeral) persistence
    layer — see [../testing/RUNBOOK.md](../testing/RUNBOOK.md).
13. Validate transaction behavior where the change touches multi-step writes — see
    [../../SKILL.md](../../SKILL.md#transactions-and-consistency).
14. Check performance-sensitive query paths affected by the change (new indexes needed,
    query plan changes).
15. Report any destructive or data-loss risk explicitly — never let it pass silently.

## Change-Specific Guidance

- **Relational migrations**: prefer additive, backward-compatible changes; avoid
  destructive changes (dropping columns/tables) unless the task explicitly calls for it.
- **Indexes**: consider build time and locking behavior on large tables; prefer
  online/concurrent index creation mechanisms where the database and repository tooling
  support them.
- **Nullable → non-null transitions**: backfill existing rows before tightening the
  constraint; do not tighten a constraint that existing data would immediately violate.
- **Column/field renames**: prefer add-new + migrate-readers + remove-old over an
  in-place rename when zero-downtime compatibility is required, so old and new code can
  coexist during rollout.
- **Enum/state changes**: adding a new variant is usually additive; removing or
  renaming one can break existing rows/consumers — treat as a compatibility risk, not a
  routine change.
- **NoSQL key/index changes**: changing a partition/shard key or a document shape that
  existing consumers read is a compatibility risk equivalent to a relational schema
  change — apply the same rollout-compatibility thinking.
- **Data backfills**: run them in a way that doesn't lock/starve production traffic
  (batching, throttling) when the repository's existing tooling supports it; report the
  backfill's scope and duration expectation.
- **Zero-downtime compatibility**: when required, prefer expand-and-contract (add new
  shape, migrate readers/writers, remove old shape in a later change) over a single
  breaking cutover.

## Escalation / Stop Conditions

- If the change requires a schema or contract change beyond the approved
  architecture/requirements, surface it rather than deciding alone — see
  [../../SKILL.md](../../SKILL.md#contract-ownership).
- If a destructive/data-loss change is ambiguous (not clearly and explicitly requested by
  the task), stop and report rather than guessing — see the shared stop conditions in
  [../../SKILL.md](../../SKILL.md#stop-conditions).

## Result Expectations

Validate the migration runs cleanly before reporting completion. Report destructive/
data-loss risk under `risks` (or `blockers` if the risk means the change should not
proceed without explicit confirmation), and persistence-layer/integration test results
under `validation` in `backend-result.yaml`.

## Related Standards / Runbooks

- [../testing/RUNBOOK.md](../testing/RUNBOOK.md)
- [../../SKILL.md](../../SKILL.md#transactions-and-consistency)
- The applicable framework `CODE-STANDARDS.md` (persistence/transactions section).
