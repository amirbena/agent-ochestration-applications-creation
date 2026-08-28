<!--
Written for the reviewer. A PR here may touch Agent Skill behavior, repository
governance, policies, templates, tooling, or documentation — none are "secondary".
Fill the sections that apply; mark the rest `None` / `N/A`. Do not fabricate content
to fill a section. Keep the body human-scannable (policies/github-issue-pr-authoring.md):
answer what changed / why / how it was validated / what needs reviewer attention, and
link the Issue or a canonical doc instead of pasting logs, full test output, restated
requirements, or an implementation diary.
-->

## Summary

<!-- What does this PR change, and why? In reviewer-oriented terms (what changes for a
consumer of this repository), not a restatement of which files were touched. -->

## Change Surface

<!-- Check every surface this PR touches. A PR may legitimately span several. -->

- [ ] Agent Skill behavior (`agents/<agent>/SKILL.md`)
- [ ] Agent policy / standards (`agents/<agent>/policies/`)
- [ ] Agent runbook (`agents/<agent>/runbooks/`)
- [ ] Agent template / contract (`agents/<agent>/templates/`)
- [ ] Agent metadata (`agents/<agent>/metadata/`)
- [ ] Repository governance (`AGENTS.md`, `policies/`, `CLAUDE.md`)
- [ ] Orchestration / runtime (future Team Lead / execution engine)
- [ ] GitHub / workflow (`.github/`)
- [ ] Tests / tooling (`scripts/`, `tests/`)
- [ ] Documentation (`README.md`, Agent `README.md`, `docs/`)
- [ ] Other: <!-- describe -->

## What Changed

<!-- Meaningful behavioral/architectural changes, grouped by logical change. Skip
trivial mechanical edits. -->

-

## Behavioral / Contract Change

<!-- Use where applicable; otherwise "N/A". -->

**Before:**
<!-- Previous behavior / rule / workflow. "N/A" if this PR adds something new. -->

**After:**
<!-- New behavior / rule / workflow. -->

**Intentionally unchanged:**
<!-- Adjacent behavior or governance a reviewer might expect this PR to touch but that
it deliberately does not. -->

## Governance Impact

<!-- State "None" if this PR does not alter governance. If it does, name exactly which
governance contract changes and why. Relevant areas may include: architecture authority;
Agent boundaries; Team Lead / orchestration boundaries; contract ownership; parallel
execution; review authority; release / Git lifecycle; runtime portability. Definitions
live in AGENTS.md / policies/ — reference them, do not restate. -->

## Portability / Packaging Impact

<!-- Does this affect whether a packaged Agent Skill still works on its own (no
dependency on root `AGENTS.md` / `policies/`)? Does it introduce or change an assumption
about a specific runtime (Claude Code, Codex, Cursor, gh CLI)? "None" if not applicable. -->

## Validation

**Automated:**
<!-- command → result, e.g. `python3 scripts/validate_repository.py` → pass;
`python3 -m pytest tests -q` → N passed -->

**Manual / semantic:**
<!-- What was verified by reading/reasoning, not just by running a script. -->

**Not run / not applicable:**
<!-- e.g. "documentation-only change; no validator applies" -->

## Reviewer Focus

<!-- Where should reviewer attention concentrate — a governance boundary, a moved
responsibility, a contract change, a portability implication, a validator assumption,
something intentionally easy to miss? Avoid "please review the code." -->

## Risk / Impact

- Breaking changes:
- Production / runtime behavior changed:
- Configuration / schema / contract migration:
- Security-sensitive change:

## Execution Metadata

<!--
Record the Agents/models that materially contributed — not whichever process ran
`gh pr create`. For single-Agent work, "Implemented by" is enough. Add the optional
roles below only when that role was actually performed by a distinct Agent/process — do
not populate hypothetical Agents from the expected pipeline. If the model is unknown,
write "<Model unavailable>" rather than guessing.
Execution participation (any role below, including "Validated by") describes who ran a
check — it is not an independent code-review approval and does not grant review authority
over this PR.
-->

- Implemented by: <Agent> — <Model>
<!-- Optional, only if a distinct Agent/process separately performed that role:
- Orchestrated by: <Agent> — <Model>
- Architecture by: <Agent> — <Model>
- Validated by (execution-side check, not review): <Agent> — <Model>
-->

## Related / Remaining Work

<!-- Linked Issue / research artifact / ADR / dependent or follow-up PR, plus anything
deliberately left outside this PR (migration, docs, known limitation). Write "None." if
nothing remains. -->

None.
