# Python Language Standards

Applies whenever the assignment names Python, regardless of framework.
Framework-specific concerns (e.g. FastAPI) belong in the corresponding
[framework standard](../../frameworks/CODE-STANDARDS.md), not here.

## Language

- Add type hints to public functions, methods, and module-level values; let internal
  local inference cover the rest.
- Avoid unnecessary dynamic behavior (`setattr`/`getattr` on arbitrary names, `eval`,
  monkeypatching production code) — prefer explicit, statically-analyzable structure.
- Handle exceptions explicitly and narrowly — catch specific exception types, never a
  bare `except:`, and never swallow an exception without either recovering or
  re-raising with context.
- Use context managers (`with`) for anything that acquires a resource (files, connections,
  locks) instead of manual acquire/release.
- Prefer iterators/generators for lazy or large-sequence processing instead of building
  intermediate lists purely out of habit.
- Use `async`/`await` consistently within an async codepath — do not mix blocking calls
  into an async function without explicitly offloading them (e.g. to a thread/executor).
- Be aware of which parts of the codebase are sync vs async; do not call blocking I/O
  from inside an async handler.
- Never use a mutable object (list, dict, set) as a default argument value — use `None`
  and initialize inside the function body.
- Organize modules/packages consistently with the repository's existing layout rather
  than introducing a new structure.
- Keep serialization/deserialization boundaries explicit — validate and convert external
  input at the boundary rather than trusting raw dicts deep inside business logic.
- Be mindful of performance-sensitive loops and I/O — batch or stream where the
  repository's existing patterns do so, and avoid quadratic behavior on data that can
  grow.

## Boilerplate reduction

- Use dataclasses (`@dataclass`) — or the repository's existing model layer, e.g.
  Pydantic — for structured data instead of loosely-typed dicts passed around as if they
  were records.
- Use `@property` where it clearly improves the model (e.g. a derived, read-only value) —
  not merely to make trivial field access look more "Pythonic."
- Prefer these language features when they clearly improve the model; do not add a
  decorator or reach for a metaprogramming pattern merely to make code appear more
  concise.

## Dependency/tooling

- Respect the repository's existing dependency-management tooling (e.g. pip with
  requirements files, Poetry, uv, pipenv) rather than introducing another one.
- Respect the repository's existing virtual-environment/project tooling rather than
  assuming a different one.
- Follow the repository's configured formatter and static-analysis tooling (e.g. black,
  ruff, mypy) rather than introducing a personal style.

## Testing

- Follow pytest conventions already used in the repository for test structure, fixtures,
  and naming.
- Use fixtures for shared setup instead of duplicating setup code or relying on
  module-level mutable state across tests.
- Use parameterized tests (`pytest.mark.parametrize`) for boundary/validation cases with
  multiple inputs rather than duplicating near-identical test functions.
- Use the repository's async test support (e.g. `pytest-asyncio`) for coroutine code —
  do not test async functions by wrapping them in ad hoc event-loop boilerplate.
- Keep tests isolated and independently runnable — no dependence on execution order or
  shared mutable global state.
- Mock external boundaries (HTTP clients, databases, external services) rather than
  internal functions/classes.
- Add integration tests when the change touches persistence, HTTP boundaries, or
  framework wiring — see the applicable framework standard.
- Run the repository's existing test command for the affected area before reporting the
  implementation complete; if it cannot be run, report why, what was validated instead,
  and the remaining risk.

## Logging

- Use the standard `logging` module (or the repository's existing logging abstraction)
  rather than `print()` for production logging.
- Follow the global logging levels and content rules in
  [../../global/CODE-STANDARDS.md](../../global/CODE-STANDARDS.md#logging).
