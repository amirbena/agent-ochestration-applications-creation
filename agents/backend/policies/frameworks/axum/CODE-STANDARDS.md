# Axum Framework Standards

Applies when the assignment names Axum as the framework, together with the
[Rust](../../languages/rust/CODE-STANDARDS.md) language standard. This standard adds only
what Axum itself introduces — general Rust rules live in the language standard.

## Framework

- Compose routers modularly (e.g. per resource, merged into the top-level router)
  consistent with the repository's existing structure.
- Use extractors to parse request data (path, query, body, headers) at the handler
  boundary instead of manually parsing the raw request inside handler bodies.
- Model shared application state explicitly via Axum's state mechanism (e.g.
  `State<T>`) rather than global mutable statics.
- Prefer typed request/response bodies over manual (de)serialization scattered through
  handlers — let the extractor/response types carry that responsibility.
- Map errors to consistent HTTP responses through a shared error type implementing
  `IntoResponse`, rather than letting each handler format errors independently.
- Be explicit about which async runtime (e.g. Tokio) and its configuration the
  repository targets — do not assume a different runtime.
- Protect shared state accessed across concurrent handlers with the appropriate
  synchronization primitive; Axum handlers run concurrently by default.
- Implement graceful shutdown consistent with the repository's existing server
  startup/shutdown code.
- Structure handlers/services so business logic is testable independent of the HTTP
  layer — do not embed logic so deeply in a handler that it can only be exercised
  through a full HTTP request.

## Prefer Axum/Tower-native mechanisms

Use Axum's middleware/`tower::Layer` composition for cross-cutting concerns (logging,
auth, timeouts) instead of duplicating that logic per handler, and take advantage of the
Tower ecosystem (timeouts, rate limiting, tracing layers) already used in the repository
rather than reimplementing equivalent behavior by hand — prefer Axum/Tower-native
extraction and middleware over manual HTTP plumbing.

## OpenAPI

Keep OpenAPI integration (where the repository already generates one, e.g. via a
schema-generation crate) in sync with actual routes and types.

## Testing

- Structure handlers/services so business logic can be unit tested independent of the
  HTTP layer.
- Write integration tests exercising the router (e.g. via `tower::ServiceExt::oneshot` or
  an HTTP test client) consistent with the repository's existing test conventions.
- Run the repository's existing test command for the affected crate before reporting the
  implementation complete; if it cannot be run, report why, what was validated instead,
  and the remaining risk.

## Logging

Use `tracing` (or the repository's existing observability setup) for structured
logging/spans rather than ad hoc `println!`-style output — see
[../../global/CODE-STANDARDS.md](../../global/CODE-STANDARDS.md#logging) and the Rust
language standard's logging section.
