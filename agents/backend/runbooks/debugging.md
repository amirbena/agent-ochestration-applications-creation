# Debugging Runbook

1. Reproduce the issue before attempting a fix.
2. Isolate the failing component/layer (API, business logic, persistence, integration).
3. Identify root cause rather than the first workaround that makes symptoms disappear.
4. Fix the root cause; avoid bypassing validation or safety checks as a shortcut.
5. Add or update a test that would have caught the issue.
6. Report blockers rather than silently narrowing scope to avoid them.
