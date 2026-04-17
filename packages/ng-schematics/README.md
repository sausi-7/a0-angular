# packages/ng-schematics

Thin wrappers around Angular CLI schematics, exposed as tools the agent can call.

## Why

Asking an LLM to hand-write a correct Angular component / service / guard is expensive (tokens) and error-prone (style drift). The Angular CLI already knows how to scaffold these correctly. This package wraps `ng generate component|service|guard|...` calls so the agent can invoke them deterministically.

## Status

Phase 0: placeholder. Implementation lands in Phase 1.

## Contributing

Adding a new schematic tool is a well-scoped good-first-issue. Each tool is a small Python module with a Pydantic argument schema and a function that shells out to `ng generate ...` against the project's workspace directory.
