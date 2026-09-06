<!--
Write for the reviewer: what changed, why, how it was validated, what deserves
attention, and what risk remains. Keep every answer to the concise review delta.
Link the Issue, canonical policy, ADR, or doc instead of reproducing requirements,
design history, test logs, or a command-by-command chronology — the diff already
shows the file-by-file changes, so do not restate them. Use `None` / `N/A` where a
section does not apply. Body-content guidance: the GitHub Issue / PR Authoring Policy
(../policies/github-issue-pr-authoring.md).
-->

## Summary

<!-- One or two sentences: what changed, why, and the outcome a reviewer should expect. -->

## What changed

<!-- 2–5 high-value bullets grouped by behavior or intent, not a file list. Add a
labeled sub-bullet only when that dimension actually changed:
  - Behavior / contract: what a caller or downstream now sees differently
  - Governance / policy: which canonical rule or invariant moved, and where it now lives
  - Portability / packaging: effect on standalone Agent-Skill packaging or runtime assumptions
-->

-

## Validation

<!-- Summarize results; do not paste test logs or full command output. Cover
automated, manual / semantic, and not-run / not-applicable checks as relevant. -->

- `command` — result
- Manual / semantic: <!-- what was verified, or N/A -->
- Not run / not applicable: <!-- reason, or None -->

## Reviewer notes

<!-- Only the non-obvious: decisions a reviewer could not infer from the diff, subtle
behavior, trade-offs taken, and where to focus review. `None.` when there is nothing
to flag. -->

None.

## Risk / Impact

<!-- Keep only when it materially helps review. Low / Medium / High plus one or two
sentences — call out breaking, runtime, migration, contract, or security impact.
Write `None.` when the change carries no meaningful risk. -->

Low —

<details>
<summary>Specialized impact — fill only what applies</summary>

<!-- Every field here is optional and used only where it adds genuine repository
value, never as always-filled ceremony. Delete a line rather than writing `N/A`
into it. Reference canonical rules; do not restate them. -->

- **Produced by:** <!-- Agent — Model, when a distinct Agent or process produced the change. Execution participation is metadata, never review approval. Omit otherwise. -->
- **Governance surface:** <!-- which canonical rule, invariant, or authority boundary this touches, and where the normative text now lives. Omit if none. -->
- **Behavior or contract change:** <!-- a single note, only when behavior, a contract, authority, or workflow actually changed — what changed and what deliberately stays the same. Omit otherwise. -->

</details>

<!-- Related / follow-up work: add one line linking a related or follow-up Issue when one exists. -->
