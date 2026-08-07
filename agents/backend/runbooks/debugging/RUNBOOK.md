# Debugging Runbook

## Purpose

Defines an evidence-first workflow for diagnosing and fixing backend defects, keeping the
fix minimal and scoped to the confirmed root cause.

## When to Use

Any assignment framed as a bug/defect, or when implementation work uncovers unexpected
behavior that must be understood before proceeding.

## Execution Steps

```text
reproduce
  ↓
narrow scope
  ↓
gather evidence
  ↓
form hypothesis
  ↓
test hypothesis
  ↓
apply minimal fix
  ↓
add regression test
  ↓
validate
```

- Reproduce the issue before attempting a fix.
- Narrow scope: isolate the failing component/layer (API, business logic, persistence,
  integration).
- Gather evidence: inspect logs/metrics/traces when available, and inspect recent
  changes to the affected area (e.g. recent commits) before speculating.
- Form a hypothesis about the cause and identify which category it falls into — code,
  configuration, dependency, infrastructure, data, or external integration — before
  writing a fix.
- Test the hypothesis against the evidence before committing to a fix direction.
- Apply the minimal fix that addresses the confirmed root cause; avoid speculative broad
  refactors, and do not fix unrelated issues noticed along the way — surface them instead
  (see [../../SKILL.md](../../SKILL.md#architecture-vs-implementation-decisions) and
  `follow_up` in the result).
- Never bypass validation or safety checks as a shortcut to make symptoms disappear.
- Add or update a regression test that would have caught the issue, where practical.
- Preserve the evidence gathered (what was observed, what was ruled out) for the result
  summary — it is what lets the Team Lead trust the fix without re-deriving it.

## Escalation / Stop Conditions

If the root cause is architectural, or outside Backend Agent ownership (e.g. requires an
Architect decision, or lives in another Agent's domain), return a blocker/concern rather
than forcing a local workaround — see the shared stop conditions in
[../../SKILL.md](../../SKILL.md#stop-conditions).

## Result Expectations

Report the confirmed root-cause category, the regression test added (or why none was
practical), and validation results in `backend-result.yaml`. If the fix is a bounded
temporary workaround rather than a full fix, say so explicitly under `risks` or
`follow_up` — see
[production-fix](../production-fix/RUNBOOK.md#temporary-workarounds) for the stricter
version of this rule under time pressure.

## Related Standards / Runbooks

- [../testing/RUNBOOK.md](../testing/RUNBOOK.md)
- [../production-fix/RUNBOOK.md](../production-fix/RUNBOOK.md) — for urgent/production
  variants of this workflow.
