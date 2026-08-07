# Go Language Standards

Applies whenever the assignment names Go, regardless of framework. Framework-specific
concerns (e.g. Gin) belong in the corresponding
[framework standard](../../frameworks/CODE-STANDARDS.md), not here.

## Language

- Write idiomatic Go — favor the standard library and simple, explicit code over
  patterns imported from other languages; avoid unnecessary framework-style abstraction.
- Keep interfaces small; define them at the point of consumption rather than exposing
  large interfaces from the producing package.
- Handle every error explicitly at the call site — never discard an error with `_`
  unless there is a documented reason it cannot matter.
- Wrap errors with useful context (`fmt.Errorf("...: %w", err)`) as they cross
  meaningful boundaries, so failures are traceable without leaking implementation
  detail unnecessarily.
- Reserve `panic` for truly unrecoverable programming errors, not for normal error
  control flow or expected failure conditions.
- Use `defer` for resource cleanup immediately after acquiring the resource.
- Propagate `context.Context` through call chains that can be cancelled or carry
  deadlines; do not create a fresh `context.Background()` deep inside a call chain that
  already has one.
- Manage goroutine lifecycles explicitly — know how and when each goroutine exits; never
  start a goroutine without a clear termination condition.
- Ensure goroutines respect cancellation (via `context` or explicit signaling) and do
  not leak past the lifetime of the operation that started them.
- Use channels intentionally to communicate ownership or coordination — not as a default
  substitute for a plain function call or mutex.
- Use mutexes or `sync/atomic` primitives for shared mutable state instead of relying on
  incidental goroutine scheduling behavior.
- Design types to have useful zero values where practical, so callers aren't forced to
  always construct via a constructor.
- Choose pointer vs value receivers/parameters deliberately based on mutation and size,
  not by default habit.
- Prefer standard-library/native mechanisms before adding an abstraction layer or a new
  dependency to solve something the standard library already handles.

## Dependency/build tooling

Use Go modules for dependency management, respecting the repository's existing
`go.mod`/versioning rather than introducing a parallel mechanism.

## Testing

- Write table-driven tests for functions with multiple input/output cases, following the
  repository's existing test conventions.
- Use subtests (`t.Run`) to keep table-driven cases independently identifiable and
  independently runnable.
- Keep tests isolated — no dependence on execution order or shared mutable package-level
  state between tests.
- Mock/fake external boundaries (network calls, databases) via interfaces defined at the
  point of consumption, rather than mocking internal, unexported functions.
- Add integration tests when the change touches persistence, HTTP boundaries, or
  external services — using real or realistic infrastructure (e.g. an ephemeral test
  database) where practical; see the applicable framework standard.
- Add benchmarks when a change is performance-sensitive and the repository already uses
  them.
- Run the race detector (`go test -race`) on concurrency-sensitive changes when the
  repository's tooling supports it.
- Run the repository's existing test command for the affected package before reporting
  the implementation complete; if it cannot be run, report why, what was validated
  instead, and the remaining risk.

## Logging

- Use the repository's existing structured logger rather than raw `fmt.Println`/`log`
  package defaults, unless the repository itself standardizes on the latter.
- Follow the global logging levels and content rules in
  [../../global/CODE-STANDARDS.md](../../global/CODE-STANDARDS.md#logging).

## Tooling

- Run `gofmt` (or the repository's equivalent) — do not hand-format.
- Run `go vet` and any additional static tooling already configured in the repository.
