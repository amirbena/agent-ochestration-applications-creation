# TypeScript Language Standards

Applies whenever the assignment names TypeScript, regardless of framework.
Framework-specific concerns (e.g. NestJS decorators/DI) belong in the corresponding
[framework standard](../../frameworks/CODE-STANDARDS.md), not here.

## Language

- Keep strict typing enabled and honor the repository's `tsconfig` strictness settings —
  do not weaken them to make code compile faster.
- Avoid `any` unless explicitly justified; when a type genuinely cannot be known, use
  `unknown` and narrow it explicitly, or document why `any` was unavoidable.
- Prefer narrow, precise types over broad ones — model the actual set of valid values
  rather than widening for convenience.
- Use discriminated unions to model closed sets of variants instead of optional-field
  soup or stringly-typed state.
- Choose `interface` vs `type` intentionally and consistently with repository convention
  rather than mixing arbitrarily.
- Model `null`/`undefined` explicitly in types; do not suppress strict-null-checking
  errors with non-null assertions (`!`) as a default habit.
- Use `async`/`await` over raw `.then()` chains for anything beyond a single trivial
  call.
- Ensure every Promise is awaited, returned, or explicitly handled — never leave a
  floating Promise whose rejection can go unnoticed.
- Propagate errors intentionally through async boundaries — do not catch-and-discard in
  an `async` function unless recovery is meaningful.
- Keep module boundaries explicit — avoid deep relative imports that reach into another
  module's internals; export only the intended public surface.
- Separate DTOs/wire types from internal domain types where the two can diverge, rather
  than reusing one type for both.
- Remember that TypeScript types are erased at compile time — do not treat a type
  annotation as run-time validation; validate untrusted input (request bodies, external
  responses) explicitly at the boundary, distinct from compile-time typing.
- Be aware of Node's single-threaded event loop — do not perform blocking/CPU-heavy work
  synchronously inside a request path; offload it appropriately.
- Respect the repository's existing module system (ESM or CommonJS) — do not mix them
  within a package without a documented reason.

## Boilerplate reduction

- Prefer TypeScript language constructs (generics, mapped/utility types, discriminated
  unions, template literal types) to eliminate repetitive manual type handling instead of
  duplicating near-identical types or writing manual type guards where a built-in utility
  type suffices.
- Reach for a code-generation tool (e.g. generating types from an OpenAPI/GraphQL schema)
  only when the repository already uses one or the task justifies introducing it — do not
  hand-maintain a type that could be generated from an existing shared contract.

## Dependency/tooling

- Respect the repository's existing package manager (npm, pnpm, or yarn) and lockfile —
  do not switch package managers within a task.
- Follow the repository's configured linter/formatter rather than introducing a personal
  style.

## Testing

- Follow the testing conventions already established in the repository (test runner,
  file layout, naming — e.g. Jest, Vitest, Mocha).
- Keep unit tests isolated and independently runnable — no dependence on execution order
  or shared mutable module-level state between tests.
- Mock external boundaries (HTTP clients, databases, external services) rather than
  internal modules; excessive mocking of internal collaborators is a design smell.
- Await all async assertions explicitly; a dropped `await` in a test can make it pass
  regardless of the actual (possibly rejected) outcome.
- Add integration tests when the change touches persistence, HTTP boundaries, or
  framework wiring — see the applicable framework standard.
- Run the repository's existing test command for the affected area before reporting the
  implementation complete; if it cannot be run, report why, what was validated instead,
  and the remaining risk.

## Logging

- Use the repository's application logger where one exists; avoid production
  `console.log`/`console.error` once a proper logging abstraction is in place.
- Follow the global logging levels and content rules in
  [../../global/CODE-STANDARDS.md](../../global/CODE-STANDARDS.md#logging).
