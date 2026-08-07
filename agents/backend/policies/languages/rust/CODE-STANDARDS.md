# Rust Language Standards

Applies whenever the assignment names Rust, regardless of framework. Framework-specific
concerns (e.g. Axum, Actix Web) belong in the corresponding
[framework standard](../../frameworks/CODE-STANDARDS.md), not here.

## Language

- Work with ownership and borrowing idiomatically — let the type system express who owns
  and who borrows data rather than fighting it with unnecessary indirection.
- Avoid unnecessary `.clone()`; reach for it only when ownership genuinely needs to be
  duplicated, not as a default way to satisfy the borrow checker.
- Keep lifetimes as simple as practical — prefer owned data or restructuring over
  intricate explicit lifetime annotations where either is a reasonable option.
- Model fallibility with `Result`, and absence with `Option`; handle both explicitly at
  the call site.
- Do not use `.unwrap()`/`.expect()` on the production/request-handling path unless the
  invariant making the value always present is genuinely guaranteed and documented at
  that call site.
- Define custom error types (or use the repository's existing error-handling
  crate/convention, e.g. `thiserror`/`anyhow`) instead of stringly-typed errors, so
  callers can handle failures programmatically.
- Prefer iterator-oriented style over manual indexing/loops when it is at least as clear.
- Model domain state with enums rather than booleans/flags/strings when the state is a
  closed set of variants.
- Use traits to express shared behavior intentionally — not to abstract prematurely over
  a single implementation.
- Use `async`/`await` consistently within an async codepath, and be explicit about which
  async runtime the repository targets.
- Be mindful of `Send`/`Sync` requirements when sharing data across tasks/threads; let
  compiler errors guide correct concurrency design rather than working around them
  unsafely.
- Handle concurrency through structured task spawning and explicit shutdown/cancellation
  signaling, consistent with the repository's existing patterns.
- Never perform blocking I/O or CPU-heavy work directly on an async runtime's worker
  threads — offload it via the runtime's blocking/spawn mechanism.
- Use interior mutability (`RefCell`, `Mutex`, `RwLock`, etc.) only where the design
  genuinely requires it, and prefer the narrowest primitive that provides the needed
  safety guarantee.
- Treat `unsafe` code as exceptional: it must be justified, minimized in scope, and
  documented with the invariant it relies on.
- Handle feature flags (Cargo features) carefully — do not introduce a new feature flag
  casually; understand what combinations must still compile.
- Keep dependencies minimal — prefer the standard library or an already-used dependency
  over adding a new crate for something already covered.

## Boilerplate reduction

- Prefer derives/macros where they are idiomatic and transparent (e.g. `#[derive(Debug,
  Clone, PartialEq, Serialize, Deserialize)]`) over hand-written equivalents.
- Avoid macro-heavy designs (custom procedural macros, deep DSL-style macro usage) that
  obscure important behavior — prefer explicit code when a macro would hide control flow
  or error handling that matters to the reader.
- Keep serialization/deserialization boundaries explicit (e.g. via `serde`), validating
  external input rather than trusting it once deserialized.

## Dependency/build tooling

Respect the repository's existing Cargo workspace/dependency structure rather than
introducing a parallel one.

## Testing

- Write unit tests alongside the code they cover (`#[cfg(test)]` modules) and integration
  tests where the repository's existing layout expects them (e.g. `tests/`).
- Keep tests isolated and independently runnable — no dependence on execution order or
  shared mutable global state.
- Test async code using the repository's existing async-test tooling (e.g.
  `#[tokio::test]`) rather than blocking the runtime with manual workarounds.
- Mock/fake external boundaries (network calls, databases) rather than internal
  functions; prefer trait-based fakes over heavy mocking frameworks unless the repository
  already uses one.
- Run the repository's existing test command (`cargo test` or equivalent) for the
  affected crate before reporting the implementation complete; if it cannot be run,
  report why, what was validated instead, and the remaining risk.

## Logging

- Use `tracing` (or the repository's existing structured-logging/tracing crate) rather
  than `println!`/`eprintln!` for production logging.
- Follow the global logging levels and content rules in
  [../../global/CODE-STANDARDS.md](../../global/CODE-STANDARDS.md#logging).

## Tooling

- Run `rustfmt` — do not hand-format.
- Run `clippy` and address its warnings, or document why a specific lint is intentionally
  allowed.
