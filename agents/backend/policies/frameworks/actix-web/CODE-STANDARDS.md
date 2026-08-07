# Actix Web Framework Standards

Applies when the assignment names Actix Web as the framework, together with the
[Rust](../../languages/rust/CODE-STANDARDS.md) language standard. This standard adds only
what Actix Web itself introduces — general Rust rules live in the language standard.

## Framework

- Configure the `App`/service tree consistently with the repository's existing structure
  (route scoping, shared configuration) rather than introducing a parallel layout.
- Use extractors (path, query, JSON, form, etc.) to parse request data at the handler
  boundary instead of manually parsing the raw request inside handler bodies.
- Model shared application state explicitly via Actix's `web::Data` (or an equivalent
  already used in the repository) rather than global mutable statics.
- Use middleware for genuinely cross-cutting concerns (logging, auth, compression)
  instead of duplicating that logic per handler.
- Map errors to consistent HTTP responses through a shared error type implementing
  `ResponseError`, rather than formatting errors independently in each handler.
- Understand that Actix workers are OS threads running an async executor per worker —
  never perform blocking work directly inside an async handler; offload it (e.g. via
  `web::block`) to avoid stalling a worker.
- Protect any state shared across workers/handlers with the appropriate synchronization
  primitive — do not assume in-process state is automatically safe across workers.
- Implement startup/shutdown behavior consistent with the repository's existing server
  bootstrap code, including graceful shutdown where already configured.
- Structure handlers/services so business logic is testable independent of the HTTP
  layer — do not embed logic so deeply in a handler that it can only be exercised
  through a full HTTP request.
- Use Actix-specific primitives (custom extractors, guards, etc.) only when they provide
  clear value over a simpler approach — do not reach for framework-specific machinery by
  default.

## OpenAPI

Keep OpenAPI integration (where the repository already generates one) in sync with
actual routes and types.

## Testing

- Write integration tests using Actix's test utilities (`actix_web::test`) consistent
  with the repository's existing test conventions.
- Structure handlers/services so business logic can be unit tested independent of the
  test-server utilities.
- Run the repository's existing test command for the affected crate before reporting the
  implementation complete; if it cannot be run, report why, what was validated instead,
  and the remaining risk.

## Logging

Use structured logging/observability consistent with the repository's existing setup
rather than introducing a separate mechanism — see
[../../global/CODE-STANDARDS.md](../../global/CODE-STANDARDS.md#logging) and the Rust
language standard's logging section.
