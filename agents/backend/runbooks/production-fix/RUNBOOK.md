# Production-Fix Runbook

## Purpose

Defines how the Backend Agent handles urgent backend fixes where blast-radius control
matters most. Urgency changes scope discipline and reporting emphasis — it does not
suspend mandatory safety/testing.

## When to Use

An assignment framed as an urgent/production fix, distinct from routine debugging (see
[../debugging/RUNBOOK.md](../debugging/RUNBOOK.md), which this runbook narrows under time
pressure).

## Execution Steps

1. Confirm the reported symptom — do not start changing code from an assumed cause.
2. Identify the affected component.
3. Inspect whatever production evidence is supplied or available (logs, metrics, error
   reports) — see [../debugging/RUNBOOK.md](../debugging/RUNBOOK.md) for the general
   evidence-first method.
4. Minimize scope: change only what is necessary to resolve the confirmed symptom.
5. Avoid opportunistic refactoring — a production fix is not the moment to also clean up
   nearby code.
6. Preserve backward compatibility unless explicitly approved to break it.
7. Add a targeted regression test for the confirmed defect.
8. Run targeted validation first (the affected area only).
9. Run broader validation when time/risk permits — do not skip it outright merely
   because the fix is urgent; if it is genuinely skipped, say so explicitly (see "Result
   Expectations").
10. Explicitly report remaining risk — what is still unverified, what could still be
    affected.
11. Document any temporary workaround clearly, including why it's temporary and what a
    full fix would require.

## Temporary Workarounds

If the fix is a bounded temporary workaround rather than a full fix:

- state clearly that it is temporary and what condition would make it permanent risk;
- ensure the workaround is scoped and does not silently become permanent (e.g. flag it in
  code/commit/result so it is discoverable later, and surface it under `follow_up`);
- do not disguise a workaround as a complete fix.

## Escalation / Stop Conditions

Urgency does not authorize bypassing mandatory safety/testing — see the shared stop
conditions in [../../SKILL.md](../../SKILL.md#stop-conditions). If validation cannot be
completed and continuing would be unsafe, stop and report rather than shipping unverified.

## Result Expectations

Report the confirmed symptom, the scope of the change, validation actually run (and any
validation deliberately deferred, with reason), remaining risk, and whether the fix is
temporary — under the relevant fields (`validation`, `risks`, `follow_up`) in
`backend-result.yaml`.

## Related Standards / Runbooks

- [../debugging/RUNBOOK.md](../debugging/RUNBOOK.md)
- [../testing/RUNBOOK.md](../testing/RUNBOOK.md)
