# Database-Changes Runbook

1. Confirm the change is within the approved architecture/requirements; if it requires a
   schema or contract change beyond that scope, surface it rather than deciding alone —
   see [../SKILL.md](../SKILL.md#boundaries).
2. Prefer additive, backward-compatible schema changes; avoid destructive changes (dropping
   columns/tables) unless the task explicitly calls for it.
3. Use the repository's existing migration tooling rather than ad hoc scripts.
4. Cover the change with relevant tests (e.g. migration correctness, persistence-layer
   behavior).
5. Validate the migration runs cleanly before reporting completion.
