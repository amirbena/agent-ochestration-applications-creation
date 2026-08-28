<!--
Write for the reviewer: what changed, why, how it was validated, what deserves
attention, and what risk remains. Keep answers concise; link supporting Issues or
canonical documents instead of pasting requirements, logs, or implementation history.
Use `None` / `N/A` wherever a section does not apply.
-->

## Summary

<!-- What changed, why, and what outcome should a reviewer expect? -->

## What changed

<!-- Group meaningful changes by behavior or intent; skip mechanical file lists. -->

-

## Validation

<!-- Report only checks actually performed; summarize results rather than pasting output.
Include automated, manual/semantic, and not-run/not-applicable items as relevant. -->

- `command` — result
- Manual: <!-- what was verified, or N/A -->
- Not run / not applicable: <!-- reason, or None -->

## Reviewer notes

<!-- Call out non-obvious decisions, subtle behavior, specific review areas, or known
trade-offs. Write `None.` when there is nothing special to flag. -->

None.

## Risk / Impact

<!-- Low / Medium / High, followed by one or two sentences of context. Mention breaking,
runtime, migration, contract, or security impact when relevant. -->

Low —

<details>
<summary>Change surface and specialized impact</summary>

<!-- Check every surface touched. -->

### Change surface

- [ ] Agent Skill behavior (`agents/<agent>/SKILL.md`)
- [ ] Agent policy / standards (`agents/<agent>/policies/`)
- [ ] Agent runbook (`agents/<agent>/runbooks/`)
- [ ] Agent template / contract (`agents/<agent>/templates/`)
- [ ] Agent metadata (`agents/<agent>/metadata/`)
- [ ] Repository governance (`AGENTS.md`, `policies/`, `CLAUDE.md`)
- [ ] Orchestration / runtime
- [ ] GitHub / workflow (`.github/`)
- [ ] Tests / tooling (`scripts/`, `tests/`)
- [ ] Documentation (`README.md`, Agent `README.md`, `docs/`)
- [ ] Other: <!-- describe -->

### Behavioral / contract change

<!-- Optional. Use when behavior, contracts, authority, or workflow changed; otherwise
write `N/A`. -->

- Before:
- After:
- Intentionally unchanged:

### Governance impact

<!-- None, or a brief description. Relevant areas may include architecture authority,
Agent boundaries, orchestration, contract ownership, review/release authority, Git
lifecycle, or runtime portability. Reference canonical rules; do not restate them. -->

None.

### Portability / packaging impact

<!-- Optional. Note effects on standalone Agent Skill packaging or runtime-specific
assumptions; otherwise write `None`. -->

None.

</details>

<details>
<summary>Execution metadata</summary>

<!-- Record only Agents/models that materially participated. Authorship, assignment,
validation, and other execution participation are metadata — never review approval. If
the model is unknown, write `Model unavailable` rather than guessing. -->

- Implemented by: Agent — Model
<!-- Optional, only when a distinct Agent/process performed the role:
- Orchestrated by: Agent — Model
- Architecture by: Agent — Model
- Validated by (execution-side check, not review): Agent — Model
-->

</details>

## Related / Remaining Work

<!-- Optional: related/follow-up Issue, intentionally deferred work, or known remaining
work. Keep it concise; write `None.` when not applicable. -->

None.
