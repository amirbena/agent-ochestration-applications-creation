# FastAPI Framework Standards

Applies when the assignment names FastAPI as the framework, together with the
[Python](../../languages/python/CODE-STANDARDS.md) language standard. This standard adds
only what FastAPI itself introduces — general Python rules live in the language standard.

## Framework

- Keep router/service/domain separation consistent with the repository's existing
  structure — do not restructure it without a task-justified reason.
- Define request/response schemas as Pydantic models; do not pass raw dicts across
  route boundaries.
- Let Pydantic validation happen at the boundary (request parsing) — do not duplicate
  the same validation manually inside handlers.
- Use FastAPI's dependency-injection system (`Depends`) for shared setup (auth,
  DB sessions, config) rather than reaching for globals or manual wiring.
- Keep a clear, consistent discipline between `async def` and `def` routes — only mark a
  route `async def` if its body is actually non-blocking; a blocking-body route should
  stay `def` so FastAPI can run it in a threadpool.
- Never call blocking I/O directly inside an `async def` route without offloading it
  (e.g. via a threadpool) — it blocks the entire event loop.
- Use the framework's lifespan/startup-shutdown hooks for resource setup/teardown
  (connections, background clients) instead of ad hoc module-level initialization.
- Map exceptions to responses through FastAPI's exception-handler mechanism rather than
  try/except sprinkled through route bodies.
- Use middleware for genuinely cross-cutting concerns (e.g. request logging, correlation
  IDs) — not for per-route logic that belongs in a dependency or the handler itself.
- Keep persistence/session boundaries explicit — acquire a DB session per request via
  dependency injection, not through a shared global session.
- Handle transactions according to the persistence library already used in the
  repository — FastAPI itself does not prescribe a transaction mechanism.
- Understand the limitations of FastAPI's built-in background tasks (they run
  in-process, after the response, with no durability guarantee) — do not use them for
  work that requires retries or durability; use the repository's existing task/queue
  infrastructure for that.
- Respect the repository's existing application startup/shutdown behavior (e.g. how
  configuration and secrets are loaded) rather than introducing a parallel mechanism.

## Prefer FastAPI/Pydantic-native declarations

Prefer FastAPI/Pydantic-native declarations (typed path/query/body parameters, Pydantic
field validators, dependency injection) over manual request parsing or hand-rolled
validation — they reduce boilerplate and keep validation and OpenAPI generation in sync
automatically.

## OpenAPI

Rely on FastAPI's automatic OpenAPI generation; keep schemas and route metadata accurate
rather than hand-maintaining a separate spec unless the repository is already
contract-first.

## Testing

- Write integration tests using FastAPI's `TestClient`/`AsyncClient` consistent with the
  repository's existing test conventions.
- Use dependency overrides (`app.dependency_overrides`) in tests to substitute test
  doubles rather than monkeypatching internals.
- Test application startup/shutdown behavior (lifespan handlers) where the repository's
  existing test conventions already cover it or the change touches it.
- Run the repository's existing test command for the affected module before reporting
  the implementation complete; if it cannot be run, report why, what was validated
  instead, and the remaining risk.

## Logging

Use structured logging consistent with the repository's existing logging setup — see
[../../global/CODE-STANDARDS.md](../../global/CODE-STANDARDS.md#logging) and the Python
language standard's logging section.
