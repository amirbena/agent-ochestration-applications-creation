# Gin Framework Standards

Applies when the assignment names Gin as the framework, together with the
[Go](../../languages/go/CODE-STANDARDS.md) language standard. This standard adds only
what Gin itself introduces — general Go rules live in the language standard.

## Framework

- Group routes logically (e.g. by resource or API version) using Gin's route groups
  rather than a flat, unorganized route list.
- Keep handlers thin — parse/validate the request, delegate to service/domain logic, and
  format the response; do not embed business logic in the handler itself.
- Use middleware for genuinely cross-cutting concerns (auth, logging, recovery) rather
  than repeating the same logic in every handler.
- Use Gin's binding/validation (`ShouldBind*`) at the boundary to parse and validate
  requests, and handle binding errors explicitly rather than ignoring them.
- Pass `*gin.Context` only through the handler/middleware layer — do not leak it into
  deeper service/domain code, which should depend on plain Go types and
  `context.Context` instead.
- Handle errors explicitly and map them to consistent HTTP responses (status code and
  body shape) rather than letting each handler invent its own error format.
- Keep response formatting consistent across the API (error shape, success envelope, if
  any) — follow whatever convention the repository has already established.
- Keep service/domain separation where the repository already has it — do not collapse
  everything into handler functions just because Gin allows it.
- Implement graceful shutdown (draining in-flight requests before exit) consistent with
  the repository's existing server startup/shutdown code.
- Wire dependencies (DB clients, config, other services) explicitly through constructors
  or Gin's context, not through hidden package-level globals.
- Do not introduce a heavyweight layered architecture merely because Gin is minimal —
  match the complexity to what the repository and task actually need.
- Use Gin-native facilities (route groups, binding, middleware chain) where they improve
  clarity, rather than reimplementing equivalent behavior by hand.

## Concurrency safety

Protect any shared state accessed across concurrent request handlers with the
appropriate Go concurrency primitive — Gin handlers run concurrently by default.

## OpenAPI

Keep OpenAPI/Swagger documentation in sync with routes where the repository already
generates or maintains one.

## Testing

- Write HTTP handler tests using Gin's test utilities (`httptest`, `gin.CreateTestContext`)
  consistent with the repository's existing test conventions.
- Add integration tests when a change touches persistence or an external service,
  exercising the real (or a realistic ephemeral) dependency rather than mocking it away
  entirely.
- Run the repository's existing test command for the affected package before reporting
  the implementation complete; if it cannot be run, report why, what was validated
  instead, and the remaining risk.

## Logging

Use structured logging and, where present, request/trace correlation consistent with the
repository's existing setup — see
[../../global/CODE-STANDARDS.md](../../global/CODE-STANDARDS.md#logging) and the Go
language standard's logging section.
