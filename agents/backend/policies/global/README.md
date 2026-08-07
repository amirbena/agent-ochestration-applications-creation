# Global Backend Policy

Universal backend engineering expectations that apply regardless of language or framework.
Language- and framework-specific policies (future `policies/<language>/` and
`policies/<language>/<framework>/` directories) refine or override this baseline per the
precedence model in [../../SKILL.md](../../SKILL.md#precedence); they must not contradict
it without a documented reason tied to that language/framework.

- Preserve existing architecture unless the task explicitly changes it.
- Prefer small, scoped changes over broad rewrites.
- Validate inputs at appropriate boundaries (e.g. API entry points, external integrations).
- Propagate errors intentionally — do not swallow failures silently.
- Maintain backward compatibility when required by the task or contract.
- Avoid leaking secrets (credentials, tokens, keys) into code, logs, or committed files.
- Keep observability in mind (meaningful logs/errors) for behavior that can fail in
  production.
- Write tests for behavioral changes.
- Maintain API-contract consistency; do not silently change a shared contract (see
  [../../SKILL.md](../../SKILL.md#boundaries)).
- Avoid unnecessary dependencies.
- Follow the repository's existing tooling rather than replacing it unnecessarily.

## Adding language/framework policies

Future language policies live under `agents/backend/policies/<language>/`, with
framework-specific refinements nested under `agents/backend/policies/<language>/<framework>/`.
Examples of expected future directories (not a closed list):

```text
policies/java/
policies/kotlin/
policies/typescript/
policies/python/
policies/go/
policies/dotnet/
```

Each should document only what is specific to that language/framework — anything already
covered here does not need to be repeated.
