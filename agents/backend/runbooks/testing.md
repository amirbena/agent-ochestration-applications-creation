# Testing Runbook

1. Discover the repository's existing test tooling rather than introducing a new one.
2. Identify which tests are affected by the change.
3. Add or update unit/integration coverage relevant to the behavioral change.
4. Run targeted validation for the affected area first.
5. Expand validation (broader test suites) when the change's blast radius warrants it.
6. Report failures rather than hiding them — do not mark a task complete over a failing
   or skipped test without surfacing that explicitly.
